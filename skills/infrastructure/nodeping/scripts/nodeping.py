# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Send one call to NodePing's API with the token the Skill's Credential File holds.

Two subcommands:

- `call [--yes] [--endpoint=<url>] <METHOD> <path> [<json>]` sends *METHOD* to
  `<endpoint>/<path>`, the optional operand being a JSON object sent as the
  form field `json`, which is how NodePing takes parameters in a request body.
- `status [--endpoint=<url>]` sends `GET accounts`, which is how the Skill
  learns whether the service accepts the token and which account it reaches.

Either prints the response body verbatim and exits 0 wherever the service
answered, whatever it answered; 1 where it could not be reached; and 2 on a
refusal the engine makes itself, with the reason on stderr. A deletion — the
`DELETE` method, or an `action` parameter whose value is `delete` in any case,
in the path's query string or the JSON operand — is refused without `--yes`,
because NodePing accepts the verb as a parameter in place of the method.

The token is read from `<home>/.kntnt/nodeping/credentials.json` as
`docs/rules/skills.md` states (ADR-0218) and is sent as the user name of HTTP
Basic authentication with an empty password. It appears nowhere else: not in
the URL, an argument, a log line, an error or the output.
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import stat
import sys
import urllib.error
import urllib.request
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final
from urllib.parse import parse_qsl, urlencode, urlsplit

# The exit statuses: the service answered, it could not be reached, and a
# refusal this engine made itself.
ANSWERED: Final = 0
TRANSPORT: Final = 1
REFUSED: Final = 2

# Where the service is. `--endpoint` overrides it only so a test can point the
# engine at a loopback server, which is why plain HTTP is accepted for a
# loopback host alone: anywhere else it would carry the token in the clear.
ENDPOINT: Final = "https://api.nodeping.com/api/1/"
LOOPBACK: Final = frozenset({"127.0.0.1", "::1", "localhost"})

# The methods NodePing's resources take, and those that carry a body.
METHODS: Final = frozenset({"GET", "POST", "PUT", "DELETE"})
WITH_BODY: Final = frozenset({"POST", "PUT"})

# How long one call may take before it counts as unreachable.
TIMEOUT_SECONDS: Final = 60

# The mode a Credential File needs, and the bits no reader accepts.
FILE_MODE: Final = 0o600
LOOSE_BITS: Final = 0o077

SETUP: Final = "run /nodeping setup to store the NodePing API token"


class Refusal(Exception):
    """A refusal this engine can name, carrying the reason it prints."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Answer a redirect as the response it is rather than following it.

    Following one would resend the credential to wherever the redirect
    points, and NodePing's API has no reason to redirect a call.
    """

    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def credential_file() -> Path:
    """The Skill's Credential File, its home resolved exactly as the shim resolves it.

    Raises:
        Refusal: where there is no home to resolve and `KNTNT_HOME` is unset.
    """

    try:
        home = Path(os.environ.get("KNTNT_HOME", str(Path.home())))
    except RuntimeError as error:
        raise Refusal(
            f"no home directory could be resolved ({error}); set KNTNT_HOME to"
            " the directory `.kntnt` is under"
        ) from error
    return home / ".kntnt" / "nodeping" / "credentials.json"


def read_token() -> str:
    """The token the Credential File holds, refusing a file others may read.

    Raises:
        Refusal: where the file is missing, admits group or world, is not a
            flat JSON object of strings, or holds no `token`.
    """

    # Refuse a missing file and one others can read, as `ssh` refuses such a
    # key. Mode bits mean nothing on Windows, where the ACL carries it.
    path = credential_file()
    if not path.exists():
        raise Refusal(f"there is no Credential File at {path}; {SETUP}")
    if os.name == "posix":
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & LOOSE_BITS:
            raise Refusal(
                f"{path} has mode {mode:04o}, which admits group or world; a"
                f" Credential File needs mode {FILE_MODE:04o} (chmod 600 {path})"
            )

    # Accept only the shape the rule gives the file, since a person may have
    # written it by hand, and say nothing of what it holds.
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{path} could not be read as JSON; {SETUP}") from error
    if not isinstance(content, dict) or not all(
        isinstance(value, str) for value in content.values()
    ):
        raise Refusal(f"{path} is not a flat JSON object of strings; {SETUP}")
    token: str = content.get("token", "")
    if not token:
        raise Refusal(f"{path} holds no token; {SETUP}")
    return token


def url_for(endpoint: str, path: str) -> str:
    """Join *endpoint* and *path* with exactly one slash, refusing a bad endpoint.

    Raises:
        Refusal: where the endpoint is neither HTTPS nor plain HTTP to a
            loopback host.
    """

    parts = urlsplit(endpoint)
    loopback = parts.scheme == "http" and parts.hostname in LOOPBACK
    if not (parts.scheme == "https" and parts.hostname) and not loopback:
        raise Refusal(
            f"--endpoint={endpoint} is neither an https:// URL nor http:// to a"
            " loopback host"
        )
    return f"{endpoint.rstrip('/')}/{path.lstrip('/')}"


def parse_operand(method: str, operand: str | None) -> dict[str, Any] | None:
    """The JSON operand as an object, refusing one a call cannot carry.

    Raises:
        Refusal: where the operand is not a JSON object, or is given with a
            method that carries no body.
    """

    if operand is None:
        return None
    if method not in WITH_BODY:
        raise Refusal(
            f"{method} carries no body; put its parameters in the path's query"
            " string instead of a JSON operand"
        )
    try:
        fields = json.loads(operand)
    except json.JSONDecodeError as error:
        raise Refusal(f"the operand is not a JSON object ({error})") from error
    if not isinstance(fields, dict):
        raise Refusal("the operand is not a JSON object")
    return fields


def names_deletion(fields: dict[str, Any]) -> bool:
    """Whether *fields* carry an `action` parameter whose value is `delete`."""

    return any(
        name.lower() == "action"
        and isinstance(value, str)
        and value.lower() == "delete"
        for name, value in fields.items()
    )


def deletes(method: str, path: str, fields: dict[str, Any] | None) -> bool:
    """Whether the call deletes, by its method or by an `action` parameter.

    NodePing reads parameters from the query string and from a JSON object
    named `json`, which may itself stand in the query string, so every one of
    those places is read.
    """

    if method == "DELETE":
        return True
    for name, value in parse_qsl(urlsplit(path).query, keep_blank_values=True):
        if names_deletion({name: value}):
            return True
        if name.lower() == "json":
            try:
                embedded = json.loads(value)
            except json.JSONDecodeError:
                continue
            if isinstance(embedded, dict) and names_deletion(embedded):
                return True
    return fields is not None and names_deletion(fields)


def send(url: str, method: str, fields: dict[str, Any] | None, token: str) -> int:
    """Send the call, print the response body verbatim, and return the exit status.

    The token goes into the authorization header and nowhere else, and no
    message this prints is built from anything that could hold it.
    """

    # Build the request: the token as the Basic user name with an empty
    # password, the operand as the form field NodePing reads it from.
    credential = base64.b64encode(f"{token}:".encode()).decode("ascii")
    headers = {"Authorization": f"Basic {credential}", "Accept": "application/json"}
    data = None
    if fields is not None:
        data = urlencode({"json": json.dumps(fields)}).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)

    # Send it, taking an HTTP error status as an answer like any other.
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, body = error.code, error.read()
    except urllib.error.URLError as error:
        print(f"nodeping.py: could not reach {url} ({error.reason})", file=sys.stderr)
        return TRANSPORT
    except (OSError, http.client.HTTPException) as error:
        print(
            f"nodeping.py: could not reach {url} ({type(error).__name__})",
            file=sys.stderr,
        )
        return TRANSPORT

    # Relay the answer, naming a status outside 2xx beside it.
    sys.stdout.buffer.write(body)
    sys.stdout.flush()
    if not 200 <= status < 300:
        print(f"nodeping.py: the service answered HTTP {status}", file=sys.stderr)
    return ANSWERED


def call(args: argparse.Namespace) -> int:
    """Hold the call to its form and the gate, then send it.

    Raises:
        Refusal: where the form, the gate or the Credential File refuses it.
    """

    method = args.method.upper()
    if method not in METHODS:
        raise Refusal(
            f"{args.method} is not a method NodePing takes (GET, POST, PUT, DELETE)"
        )
    fields = parse_operand(method, args.json)
    url = url_for(args.endpoint, args.path)
    if deletes(method, args.path, fields) and not args.yes:
        raise Refusal(
            f"refused {args.method} {args.path} without --yes: it deletes at"
            " NodePing, which cannot be undone. --yes asserts that this deletion"
            " is already authorized by the user; pass it only then"
        )
    return send(url, method, fields, read_token())


def status(args: argparse.Namespace) -> int:
    """Ask for the account the token reaches.

    Raises:
        Refusal: where the endpoint or the Credential File refuses it.
    """

    return send(url_for(args.endpoint, "accounts"), "GET", None, read_token())


# Each subcommand's usage, written out because `argparse` would print a valued
# flag with its value separated, and this collection's grammar attaches it
# (ADR-0176).
USAGES: Final = {
    "call": "[--yes] [--endpoint=<url>] <METHOD> <path> [<json>]",
    "status": "[--endpoint=<url>]",
}


def parser() -> argparse.ArgumentParser:
    """The command line; a usage error exits 2 with its usage line."""

    root = argparse.ArgumentParser(
        prog="nodeping.py",
        usage="\n".join(f"%(prog)s {name} {usage}" for name, usage in USAGES.items()),
        description="Send one call to NodePing's API.",
    )
    commands = root.add_subparsers(dest="command", required=True)

    call_command = commands.add_parser(
        "call", prog="nodeping.py call", usage=f"%(prog)s {USAGES['call']}"
    )
    call_command.add_argument("--yes", action="store_true")
    call_command.add_argument("--endpoint", default=ENDPOINT)
    call_command.add_argument("method")
    call_command.add_argument("path")
    call_command.add_argument("json", nargs="?")

    status_command = commands.add_parser(
        "status", prog="nodeping.py status", usage=f"%(prog)s {USAGES['status']}"
    )
    status_command.add_argument("--endpoint", default=ENDPOINT)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Parse *argv*, run the subcommand, and return its exit status."""

    args = parser().parse_args(argv)
    try:
        return call(args) if args.command == "call" else status(args)
    except Refusal as refusal:
        print(f"nodeping.py: {refusal}", file=sys.stderr)
        return REFUSED


if __name__ == "__main__":
    sys.exit(main())
