# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read and change DNS at ClouDNS as the API sub-user the user delegated.

The credential is the sub-user's, held in this Skill's Credential File,
`<home>/.kntnt/cloudns/credentials.json`, under the two parameter names ClouDNS
reads it by: `sub-auth-user` and `auth-password`. This engine reads that file
itself, as `docs/rules/skills.md` states every such engine does, and puts the
two values in the body of the request and nowhere else (ADR-0218).

Two subcommands:

- `call [--yes] [--endpoint=<url>] <path> [<key>=<value>]...` POSTs to
  `<endpoint>/<path>` with the credential and every pair in the form body, and
  prints the response body verbatim. A call the service cannot undo — a path
  whose last segment begins with `delete`, or one carrying
  `delete-existing-records=1` — is refused without `--yes`.
- `status [--endpoint=<url>]` asks `login/login.json` whether the service
  accepts the credential and, where it does, lists the zones the sub-user can
  see, which are exactly the zones delegated to it.

The Credential File is written by the Collection Library's `credentials.py`,
whose `generate` is also the gate against overwriting a credential it holds.

Exit 0 wherever the service answered, whatever it answered, since ClouDNS
reports a failure in band with `status` and `statusDescription`; 1 where it
could not be reached; 2 on a refusal made here, before anything is sent. A
refusal's reason goes to stderr, and no output ever carries the password.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Sequence
from pathlib import Path
from typing import Final

# The exit statuses: the service answered, it could not be reached, and a
# refusal made here before anything was sent.
ANSWERED: Final = 0
UNREACHED: Final = 1
REFUSED: Final = 2

# The Skill whose Credential File this engine reads, and the two keys that
# file holds, named as ClouDNS reads them.
SKILL: Final = "cloudns"
SUB_USER_KEY: Final = "sub-auth-user"
PASSWORD_KEY: Final = "auth-password"
CREDENTIAL_KEYS: Final = (SUB_USER_KEY, PASSWORD_KEY)

# Every parameter ClouDNS authenticates by. A pair naming one is refused, so a
# call is made as the delegated sub-user and as nobody else.
AUTHENTICATION_PARAMETERS: Final = frozenset(
    {"auth-id", "sub-auth-id", SUB_USER_KEY, PASSWORD_KEY}
)

# Where the API is, and how long a call may take before it counts as unreached.
DEFAULT_ENDPOINT: Final = "https://api.cloudns.net/"
TIMEOUT_SECONDS: Final = 30

# The bits of a Credential File's mode no reader accepts: any access for group
# or world, as `ssh` refuses such a key.
LOOSE_BITS: Final = 0o077

# How `status` pages through `dns/list-zones.json`: the largest page the method
# permits, and a ceiling on pages so a service that always answers a full page
# cannot hold the engine forever.
ROWS_PER_PAGE: Final = 100
MAX_PAGES: Final = 1000

# What an API path is: segments of the characters ClouDNS's method paths use,
# ending in `.json`, so nothing it names can carry a query, a fragment, another
# host, or a climb out of the endpoint.
API_PATH: Final = re.compile(r"^[a-z0-9-]+(?:/[a-z0-9-]+)*\.json$")

# The pair that makes `dns/records-import.json` replace a zone's records.
DELETE_EXISTING: Final = ("delete-existing-records", "1")


class Refusal(Exception):
    """A refusal made before anything is sent, carrying the reason it prints."""


class Unreached(Exception):
    """The service could not be reached, carrying a reason free of the credential."""


def credential_file() -> Path:
    """The Credential File, under `KNTNT_HOME` or the user's home.

    Resolved exactly as the shim resolves the home `~/.kntnt` is under.

    Raises:
        Refusal: where there is no home to resolve and `KNTNT_HOME` is unset.
    """

    try:
        home = Path(os.environ.get("KNTNT_HOME", str(Path.home())))
    except RuntimeError as error:
        raise Refusal(
            f"no home directory could be resolved ({error}); set KNTNT_HOME"
        ) from error
    return home / ".kntnt" / SKILL / "credentials.json"


def load_credentials(path: Path) -> dict[str, str]:
    """Load an existing Credential File, refusing one others may read.

    Raises:
        Refusal: where the file admits group or world, or is not a flat JSON
            object of strings.
    """

    # Refuse a file others can read. Mode bits mean nothing on Windows, where
    # the file's ACL carries the restriction.
    mode = stat.S_IMODE(path.stat().st_mode)
    if os.name == "posix" and mode & LOOSE_BITS:
        raise Refusal(
            f"{path} has mode {mode:04o}, which admits group or world; a Credential"
            f" File needs mode 0600 (chmod 600 {path})"
        )

    # Accept only the shape the rule gives the file, since a person may have
    # written it by hand.
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(
            f"{path} could not be read as JSON ({type(error).__name__})"
        ) from error
    if not isinstance(content, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in content.items()
    ):
        raise Refusal(f"{path} is not a flat JSON object of strings")
    return content


def read_credentials(path: Path) -> dict[str, str]:
    """Read the Credential File a call needs, holding both keys.

    Raises:
        Refusal: where the file is missing, is refused by `load_credentials`,
            or lacks one of the two keys.
    """

    if not path.exists():
        raise Refusal(
            f"there is no Credential File at {path}; run /cloudns setup to make one"
        )
    content = load_credentials(path)
    missing = [key for key in CREDENTIAL_KEYS if not content.get(key)]
    if missing:
        raise Refusal(
            f"{path} holds no {' or '.join(missing)}; run /cloudns setup to fill it"
        )
    return content


def endpoint_url(endpoint: str, path: str) -> str:
    """The URL of *path* under *endpoint*, refusing either where it is malformed.

    Raises:
        Refusal: where *endpoint* is not an `http` or `https` URL with a host,
            or *path* is not a plain API path.
    """

    parts = urllib.parse.urlsplit(endpoint)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise Refusal(f"--endpoint={endpoint} is not an http or https URL")
    if not API_PATH.match(path):
        raise Refusal(
            f"{path!r} is not an API path such as dns/records.json; its parameters"
            " are given as <key>=<value> pairs"
        )
    return f"{endpoint.rstrip('/')}/{path}"


def post(url: str, fields: Sequence[tuple[str, str]]) -> bytes:
    """POST *fields* as a form body to *url* and return the response body.

    An HTTP error status is still an answer, so its body is returned as any
    other would be. The reason an unreached service gives is its type and the
    URL alone, neither of which carries the credential, which travels only in
    the body.

    Raises:
        Unreached: where no answer came back.
    """

    # Carry every field in a form body, where no URL, log or listing holds it.
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(fields).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    # Send it, taking an HTTP error's body as the answer it is.
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return bytes(response.read())
    except urllib.error.HTTPError as error:
        return bytes(error.read())
    except (urllib.error.URLError, OSError) as error:
        reason = error.reason if isinstance(error, urllib.error.URLError) else error
        detail = getattr(reason, "strerror", None) or type(reason).__name__
        raise Unreached(f"could not reach {url} ({detail})") from error


def authenticated(
    credentials: dict[str, str], pairs: Sequence[tuple[str, str]]
) -> list[tuple[str, str]]:
    """The form body: the two credential parameters, then *pairs* in order."""

    return [(key, credentials[key]) for key in CREDENTIAL_KEYS] + list(pairs)


def parse_pairs(given: Sequence[str]) -> list[tuple[str, str]]:
    """The `<key>=<value>` operands as pairs, in order.

    Raises:
        Refusal: where an operand has no `=` or no key, or names a parameter
            ClouDNS authenticates by.
    """

    pairs: list[tuple[str, str]] = []
    for operand in given:
        key, separator, value = operand.partition("=")
        if not separator or not key:
            raise Refusal(f"{operand!r} is not a <key>=<value> pair")
        if key in AUTHENTICATION_PARAMETERS:
            raise Refusal(
                f"{key} is read from the Credential File and is never given as a pair"
            )
        pairs.append((key, value))
    return pairs


def irreversible(path: str, pairs: Sequence[tuple[str, str]]) -> str | None:
    """Why a call cannot be undone at the service, or `None` where it can.

    The gate stands on the call's shape rather than on a list of methods: a
    path whose last segment before `.json` begins with `delete`, and any call
    carrying `delete-existing-records=1`.
    """

    segment = path.rsplit("/", 1)[-1].removesuffix(".json")
    if segment.startswith("delete"):
        return f"{path} deletes at ClouDNS"
    if DELETE_EXISTING in pairs:
        return (
            f"{path} with {'='.join(DELETE_EXISTING)} deletes a zone's existing records"
        )
    return None


def command_call(args: argparse.Namespace) -> int:
    """Send one call and print the service's answer verbatim."""

    # Refuse, before anything is read or sent, a malformed call and one the
    # service cannot undo.
    url = endpoint_url(args.endpoint, args.path)
    pairs = parse_pairs(args.pairs)
    reason = irreversible(args.path, pairs)
    if reason is not None and not args.yes:
        raise Refusal(
            f"refused {reason}, which cannot be undone. --yes asserts that the user"
            " asked for this deletion, or that a decision they already made covers"
            " it; nothing was sent"
        )

    # Send it as the sub-user, and relay whatever the service answered.
    credentials = read_credentials(credential_file())
    body = post(url, authenticated(credentials, pairs))
    sys.stdout.write(body.decode("utf-8", errors="replace"))
    return ANSWERED


def answer_of(body: bytes) -> object:
    """The service's answer as JSON, or its text where it is not JSON."""

    text = body.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def list_zones(
    endpoint: str, credentials: dict[str, str]
) -> tuple[list[str] | None, object]:
    """Every zone the sub-user can see, paging until a short page ends the list.

    Returns the zone names and `None`, or `None` and the service's
    `statusDescription` where a page failed in band.
    """

    zones: list[str] = []
    for page in range(1, MAX_PAGES + 1):
        paging = [("page", str(page)), ("rows-per-page", str(ROWS_PER_PAGE))]
        listing = answer_of(
            post(
                endpoint_url(endpoint, "dns/list-zones.json"),
                authenticated(credentials, paging),
            )
        )
        if not isinstance(listing, list):
            return None, description_of(listing)
        zones += [
            str(zone.get("name")) if isinstance(zone, dict) else str(zone)
            for zone in listing
        ]
        if len(listing) < ROWS_PER_PAGE:
            break
    return zones, None


def description_of(answer: object) -> object:
    """The `statusDescription` of an in-band answer, or the answer itself."""

    return answer.get("statusDescription") if isinstance(answer, dict) else answer


def command_status(args: argparse.Namespace) -> int:
    """Report the sub-user, whether ClouDNS accepts it, and the zones it can see."""

    # Ask the service whether it accepts the credential.
    path = credential_file()
    credentials = read_credentials(path)
    login = answer_of(
        post(
            endpoint_url(args.endpoint, "login/login.json"),
            authenticated(credentials, []),
        )
    )
    accepted = isinstance(login, dict) and login.get("status") == "Success"
    report: dict[str, object] = {
        "credential_file": str(path),
        "sub_user": credentials[SUB_USER_KEY],
        "accepted": accepted,
        "description": description_of(login),
        "zones": None,
    }

    # Where it does, list the zones delegated to the sub-user.
    if accepted:
        zones, failure = list_zones(args.endpoint, credentials)
        report["zones"] = zones
        if failure is not None:
            report["zones_description"] = failure

    print(json.dumps(report, indent=2))
    return ANSWERED


# Each subcommand's usage, written out because `argparse` would print a valued
# flag with its value separated, and this collection's grammar attaches it
# (ADR-0176).
USAGES: Final = {
    "call": "[--yes] [--endpoint=<url>] <path> [<key>=<value>]...",
    "status": "[--endpoint=<url>]",
}


def parser() -> argparse.ArgumentParser:
    """The command line. A usage error exits 2 with its subcommand's usage line."""

    root = argparse.ArgumentParser(
        prog="cloudns.py",
        usage="\n".join(f"%(prog)s {name} {usage}" for name, usage in USAGES.items()),
        description="Read and change DNS at ClouDNS as a delegated API sub-user.",
        allow_abbrev=False,
    )
    commands = root.add_subparsers(dest="command", required=True)
    subcommands = {
        name: commands.add_parser(
            name,
            prog=f"cloudns.py {name}",
            usage=f"%(prog)s {usage}",
            allow_abbrev=False,
        )
        for name, usage in USAGES.items()
    }

    call = subcommands["call"]
    call.add_argument("--yes", action="store_true")
    call.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    call.add_argument("path")
    call.add_argument("pairs", nargs="*")

    subcommands["status"].add_argument("--endpoint", default=DEFAULT_ENDPOINT)

    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Parse *argv*, run the subcommand, and return its exit status."""

    args = parser().parse_args(argv)
    try:
        match args.command:
            case "call":
                return command_call(args)
            case _:
                return command_status(args)
    except Refusal as refusal:
        print(f"cloudns.py: {refusal}", file=sys.stderr)
        return REFUSED
    except Unreached as unreached:
        print(f"cloudns.py: {unreached}", file=sys.stderr)
        return UNREACHED


if __name__ == "__main__":
    sys.exit(main())
