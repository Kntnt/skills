# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Make one call to Postmark's API with a token from the Skill's Credential File.

Postmark issues two kinds of token: a server token, sent as
`X-Postmark-Server-Token`, for everything one server does, and an account
token, sent as `X-Postmark-Account-Token`, for servers, domains and sender
signatures across the account. The Credential File,
`<home>/.kntnt/postmark/credentials.json`, holds the account token under
`account-token` and each server token under `server:<name>`.

Three subcommands:

- `call` sends one request with the token it is told to use, and prints the
  response body verbatim, with any credential in it masked.
- `status` reads every token the file holds against the service and prints
  what each answered, as one JSON document.
- `setup-server` fetches one server's token with the account token, has the
  Library's `credentials.py set --from-stdin` store it under `server:<name>`,
  and verifies it with `GET server`.

`call` and `status` exit 0 wherever the service answered, whatever it
answered; 1 where it could not be reached; 2 on a refusal made before anything
was sent. `setup-server` exits 0 where the token was stored and Postmark
accepted it; 1 where Postmark could not be reached or the Library's `set`
failed as a tool; and 2 on any refusal: its own, one from Postmark, which it
names by HTTP status and `ErrorCode` alone, and the Library's, passed on as it
stands.

A token appears in its header and nowhere else: never in the URL, an
argument, a line printed or an error (docs/rules/skills.md, ADR-0218). The one
handoff beside the header is `setup-server`'s: the token it fetched is written
to the standard input of the Library's `set`, which is the Library's own write
path into the Credential File. Nor does a token Postmark returns reach a
print: a server's `ApiTokens` and a webhook's HTTP password are masked in
every answer before it is printed, since what the engine prints reaches the
transcript, and `setup-server` prints no answer at all.

What Postmark cannot undo — a deletion, a send and a data removal — is refused
without `--yes`.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import stat
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final

# The exit statuses: the service answered, it could not be reached or a tool
# failed, and a refusal.
ANSWERED: Final = 0
TRANSPORT: Final = 1
REFUSED: Final = 2

# Where Postmark's API is. A test points `--endpoint` at a loopback server.
ENDPOINT: Final = "https://api.postmarkapp.com"

# The headers each kind of token travels in, and the server token Postmark
# accepts for a send it validates and does not deliver.
SERVER_HEADER: Final = "X-Postmark-Server-Token"
ACCOUNT_HEADER: Final = "X-Postmark-Account-Token"
TEST_TOKEN: Final = "POSTMARK_API_TEST"

# The Credential File's keys: the account token, and the prefix a server's
# name follows.
ACCOUNT_KEY: Final = "account-token"
SERVER_PREFIX: Final = "server:"

# The bits of a Credential File's mode no reader accepts, and the mode it needs.
LOOSE_BITS: Final = 0o077
FILE_MODE: Final = 0o600

# The methods Postmark's API uses, and those of them that carry a body.
METHODS: Final = ("GET", "POST", "PUT", "PATCH", "DELETE")
WITH_BODY: Final = ("POST", "PUT", "PATCH")

# A POST to a path whose first segment is one of these sends email, or asks
# Postmark to erase a recipient's data; neither can be taken back.
SENDING: Final = "email"
DATA_REMOVAL: Final = "data-removals"

# How long one request may take before it counts as a transport failure.
TIMEOUT_SECONDS: Final = 60

# How many servers `status` and `setup-server` ask for in one page, which is
# Postmark's page maximum.
SERVER_PAGE: Final = 500

# The Skill whose Credential File the Library's `set` writes.
SKILL: Final = "postmark"

# The fields whose value is a credential wherever Postmark returns them: a
# server's tokens, in `ApiTokens`, and the password a webhook's `HttpAuth`
# sends. What stands in their place.
CREDENTIAL_FIELDS: Final = ("ApiTokens", "Password")
MASK: Final = "[redacted]"

# What `status` says in place of the account where the file holds no
# account token.
NO_ACCOUNT_TOKEN: Final = (
    "The Credential File holds no account token. `/postmark setup account` adds"
    " one, which lists the account's servers and manages servers, domains,"
    " sender signatures and data removals."
)


class Refusal(Exception):
    """A refusal this engine names, carrying the reason it prints.

    `call` and `status` refuse only before anything is sent; `setup-server`
    also refuses over what Postmark answered.
    """


class PassedOn(Exception):
    """A refusal from the Library's `set`, carrying its stderr to pass on unchanged."""


class Unreachable(Exception):
    """The service could not be reached, carrying the reason it prints."""


class Failure(Exception):
    """A tool the engine started failed, carrying the reason it prints."""


@dataclass(frozen=True)
class Answer:
    """What the service answered: its HTTP status and its body, verbatim."""

    status: int
    body: bytes


def masked(value: object) -> object:
    """*value* with every credential field's value masked, at any depth."""

    if isinstance(value, list):
        return [masked(item) for item in value]
    if not isinstance(value, dict):
        return value
    shown: dict[str, object] = {}
    for key, item in value.items():
        if key not in CREDENTIAL_FIELDS or not item:
            shown[key] = masked(item)
        elif isinstance(item, list):
            # A list keeps its length, so a server with two tokens shows two.
            shown[key] = [MASK] * len(item)
        else:
            shown[key] = MASK
    return shown


def printable(body: bytes) -> bytes:
    """A body as `call` prints it: verbatim, unless a credential had to be masked."""

    try:
        parsed = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return body
    shown = masked(parsed)
    return body if shown == parsed else json.dumps(shown).encode("utf-8")


def credential_file() -> Path:
    """The Credential File, under the home the shim resolves.

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
    return home / ".kntnt" / "postmark" / "credentials.json"


def read_credentials(path: Path) -> dict[str, str]:
    """Read the Credential File as the rule states.

    Raises:
        Refusal: where the file is missing, admits group or world, or is not a
            flat JSON object of strings.
    """

    # A missing file is a Skill nobody has set up yet.
    if not path.exists():
        raise Refusal(
            f"there is no Credential File at {path}; run `/postmark setup account`"
            " or `/postmark setup server <name>` to store a Postmark token"
        )

    # Refuse a file others can read, as `ssh` refuses such a key. Mode bits
    # mean nothing on Windows, where the file's ACL carries the restriction.
    mode = stat.S_IMODE(path.stat().st_mode)
    if os.name == "posix" and mode & LOOSE_BITS:
        raise Refusal(
            f"{path} has mode {mode:04o}, which admits group or world; the"
            f" Credential File needs mode {FILE_MODE:04o} (chmod 600 {path})"
        )

    # Accept only the shape the rule gives the file, since a person may have
    # written it by hand.
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{path} could not be read as JSON ({error})") from error
    if not isinstance(content, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in content.items()
    ):
        raise Refusal(f"{path} is not a flat JSON object of strings")
    return content


def servers_held(credentials: dict[str, str]) -> dict[str, str]:
    """Each server the file holds a token for, by name, in name order."""

    return {
        key.removeprefix(SERVER_PREFIX): value
        for key, value in sorted(credentials.items())
        if key.startswith(SERVER_PREFIX)
    }


def url(endpoint: str, path: str) -> str:
    """The endpoint and the path joined with exactly one slash."""

    return f"{endpoint.rstrip('/')}/{path.lstrip('/')}"


def gate(method: str, path: str, test: bool) -> str | None:
    """Why *method* on *path* needs `--yes`, or `None` where it does not.

    A deletion and a send cannot be undone at Postmark, and neither can a data
    removal, which erases a recipient's data. A send under the test token
    delivers nothing and is not gated; archiving a message stream can be
    undone and is not either.
    """

    first = path.lstrip("/").split("?", 1)[0].split("/", 1)[0].lower()
    if method == "DELETE":
        return (
            "Postmark cannot undo a deletion; --yes asserts the user has"
            " authorized deleting this object"
        )
    if method == "POST" and first == SENDING and not test:
        return (
            "Postmark cannot undo a send; --yes asserts the user has seen the"
            " message in full and authorized sending it"
        )
    if method == "POST" and first == DATA_REMOVAL:
        return (
            "Postmark cannot undo a data removal; --yes asserts the user has"
            " authorized erasing this recipient's data"
        )
    return None


def request(
    endpoint: str, method: str, path: str, header: str, token: str, body: bytes | None
) -> Answer:
    """Send one request and return what the service answered.

    A POST, PUT or PATCH without a body is sent with an empty one, because
    Postmark asks for `Content-Length: 0` on the calls that take none.

    Raises:
        Unreachable: where no answer came back, naming the URL and the reason
            and never the token, which is in a header the reason never quotes.
    """

    target = url(endpoint, path)
    prepared = urllib.request.Request(
        target,
        data=body if body is not None else (b"" if method in WITH_BODY else None),
        method=method,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            header: token,
        },
    )
    try:
        with urllib.request.urlopen(prepared, timeout=TIMEOUT_SECONDS) as response:
            return Answer(response.status, response.read())
    except urllib.error.HTTPError as error:
        # An error status is still an answer, and its body is what says why.
        with error:
            return Answer(error.code, error.read())
    except (urllib.error.URLError, OSError, http.client.HTTPException) as error:
        reason = getattr(error, "reason", error)
        raise Unreachable(f"{method} {target} could not be sent ({reason})") from error


def choose_token(args: argparse.Namespace) -> tuple[str, str]:
    """The header and the token the call names, read from the file where needed.

    Raises:
        Refusal: where the file does not hold the token asked for.
    """

    if args.test:
        return SERVER_HEADER, TEST_TOKEN
    path = credential_file()
    credentials = read_credentials(path)
    if args.account:
        if ACCOUNT_KEY not in credentials:
            raise Refusal(
                f"{path} holds no account token; run `/postmark setup account`"
                " to store one"
            )
        return ACCOUNT_HEADER, credentials[ACCOUNT_KEY]
    token = credentials.get(f"{SERVER_PREFIX}{args.server}")
    if token is None:
        raise Refusal(
            f"{path} holds no token for the server {args.server!r}; run"
            f" `/postmark setup server {args.server}` to store one"
        )
    return SERVER_HEADER, token


def command_call(args: argparse.Namespace) -> int:
    """Send the one request `call` names, and print the answer verbatim."""

    # Settle the request before anything is read or sent.
    method = args.method.upper()
    if method not in METHODS:
        raise Refusal(f"{args.method} is not one of {', '.join(METHODS)}")
    body: bytes | None = None
    if args.json is not None:
        if method not in WITH_BODY:
            raise Refusal(
                f"a {method} carries no body; pass JSON only with POST, PUT or PATCH"
            )
        try:
            json.loads(args.json)
        except json.JSONDecodeError as error:
            raise Refusal(f"the body is not JSON ({error})") from error
        body = args.json.encode("utf-8")

    # Refuse what Postmark cannot undo unless the user's authorization is asserted.
    reason = gate(method, args.path, args.test)
    if reason is not None and not args.yes:
        raise Refusal(
            f"refused {method} /{args.path.lstrip('/')} without --yes: {reason}"
        )

    # Send it with the token the path needs, and relay the answer as it came.
    header, token = choose_token(args)
    answer = request(args.endpoint, method, args.path, header, token, body)
    sys.stdout.buffer.write(printable(answer.body))
    sys.stdout.flush()
    if not 200 <= answer.status < 300:
        print(f"postmark.py: Postmark answered HTTP {answer.status}", file=sys.stderr)
    return ANSWERED


def relayed(answer: Answer) -> dict[str, object]:
    """An answer as `status` reports it: the status, and the body with any credential masked."""

    text = answer.body.decode("utf-8", errors="replace")
    try:
        body: object = masked(json.loads(text))
    except json.JSONDecodeError:
        body = text
    return {"status": answer.status, "body": body}


def command_status(args: argparse.Namespace) -> int:
    """Read every token the file holds against the service, and print the answers."""

    # Nothing to verify is a Skill nobody has set up.
    path = credential_file()
    credentials = read_credentials(path)
    servers = servers_held(credentials)
    if ACCOUNT_KEY not in credentials and not servers:
        raise Refusal(
            f"{path} holds no Postmark token; run `/postmark setup account` or"
            " `/postmark setup server <name>` to store one"
        )

    # The account's servers, where the file holds the token that lists them.
    account: dict[str, object] = {"held": False, "note": NO_ACCOUNT_TOKEN}
    if ACCOUNT_KEY in credentials:
        answer = request(
            args.endpoint,
            "GET",
            f"servers?count={SERVER_PAGE}&offset=0",
            ACCOUNT_HEADER,
            credentials[ACCOUNT_KEY],
            None,
        )
        account = {"held": True} | relayed(answer)

    # Each server token, verified against the server it names.
    verified = {
        name: relayed(
            request(args.endpoint, "GET", "server", SERVER_HEADER, token, None)
        )
        for name, token in servers.items()
    }

    print(
        json.dumps(
            {"credential_file": str(path), "account": account, "servers": verified},
            indent=2,
        )
    )
    return ANSWERED


def error_code(answer: Answer) -> int | None:
    """The `ErrorCode` of a refusal's body, or `None` where none can be read."""

    try:
        body = json.loads(answer.body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    code = body.get("ErrorCode") if isinstance(body, dict) else None
    return code if isinstance(code, int) and not isinstance(code, bool) else None


def refused(call: str, answer: Answer) -> str:
    """What a refusal from Postmark is reported as: its status and its code alone.

    The body is never quoted, since an answer carrying a server carries its
    tokens.
    """

    code = error_code(answer)
    return f"Postmark answered {call} with HTTP {answer.status}" + (
        f" and ErrorCode {code}" if code is not None else ""
    )


def list_servers(endpoint: str, token: str) -> list[dict[str, object]]:
    """Every server of the account, read page by page with the account token.

    Paging stops once `TotalCount` servers have been read, or at the first page
    that comes back empty, whichever comes first.

    Raises:
        Refusal: where Postmark refuses a page or answers one in a shape that
            is not a list of servers, naming neither the body nor a token.
        Unreachable: where Postmark could not be reached.
    """

    servers: list[dict[str, object]] = []
    total: int | None = None
    while total is None or len(servers) < total:
        answer = request(
            endpoint,
            "GET",
            f"servers?count={SERVER_PAGE}&offset={len(servers)}",
            ACCOUNT_HEADER,
            token,
            None,
        )
        if not 200 <= answer.status < 300:
            raise Refusal(refused("GET servers", answer))
        try:
            page = json.loads(answer.body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            page = None
        listed = page.get("Servers") if isinstance(page, dict) else None
        count = page.get("TotalCount") if isinstance(page, dict) else None
        if (
            not isinstance(listed, list)
            or not all(isinstance(server, dict) for server in listed)
            or not isinstance(count, int)
        ):
            raise Refusal(
                "Postmark's answer to GET servers could not be read as a list of"
                " servers"
            )
        if not listed:
            break
        total = count
        servers.extend(listed)
    return servers


def server_token(servers: list[dict[str, object]], name: str) -> str:
    """The first token Postmark lists for the one server called exactly *name*.

    Raises:
        Refusal: where no server, or more than one, carries *name*, or the one
            that does lists no token. None of them names a token.
    """

    matches = [server for server in servers if server.get("Name") == name]
    if not matches:
        names = ", ".join(json.dumps(server.get("Name")) for server in servers)
        raise Refusal(
            f"Postmark holds no server named {json.dumps(name)}; the account's"
            f" servers are {names or 'none'}. The name has to match exactly,"
            " case and spaces included"
        )
    if len(matches) > 1:
        raise Refusal(
            f"Postmark holds several servers named {json.dumps(name)}, so which"
            " one's token to store cannot be told from the name; the token has to"
            " come through the clipboard, copied from that server's API Tokens tab"
        )
    tokens = matches[0].get("ApiTokens")
    first = tokens[0] if isinstance(tokens, list) and tokens else None
    if not isinstance(first, str) or not first.strip():
        raise Refusal(
            f"Postmark lists no token in ApiTokens for the server {json.dumps(name)};"
            " create one on that server's API Tokens tab, or store one through the"
            " clipboard"
        )
    return first


def store_server_token(
    library: Path, home: Path, name: str, token: str, replace: bool
) -> None:
    """Have the Library's `set` store *token* under `server:<name>`, over stdin.

    The token is written to the standard input of that one process and to
    nothing else, so it never stands in an argument every user can read. The
    process runs in *home*, the directory `.kntnt` is under, which no run of
    this collection replaces.

    Raises:
        PassedOn: where `set` refuses, carrying its stderr as it stands.
        Failure: where `uv` cannot be started or `set` fails as a tool.
    """

    script = library / "scripts" / "credentials.py"
    command = [
        "uv",
        "run",
        str(script),
        "set",
        *(["--yes"] if replace else []),
        f"--skill={SKILL}",
        f"--key={SERVER_PREFIX}{name}",
        "--from-stdin",
    ]
    try:
        result = subprocess.run(
            command,
            cwd=home,
            input=token,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        raise Failure(
            f"uv could not be started to run {script} ({error.strerror})"
        ) from error
    if result.returncode == REFUSED:
        raise PassedOn(result.stderr)
    if result.returncode != 0:
        raise Failure(
            f"{script} set exited with {result.returncode}, and the token was not"
            " confirmed stored"
        )


def command_setup_server(args: argparse.Namespace) -> int:
    """Fetch one server's token with the account token, store it, and verify it."""

    # Only the account token reaches a server's token, and the Library's `set`
    # is what stores it.
    path = credential_file()
    credentials = read_credentials(path)
    if ACCOUNT_KEY not in credentials:
        raise Refusal(
            f"{path} holds no account token, so there is nothing to fetch a"
            " server's token with; store this server's token through the"
            " clipboard instead, or store the account token with"
            " `/postmark setup account` first"
        )
    if not (args.library / "scripts" / "credentials.py").is_file():
        raise Refusal(f"--library={args.library} holds no scripts/credentials.py")

    # Find the one server of that name and take its first token.
    token = server_token(
        list_servers(args.endpoint, credentials[ACCOUNT_KEY]), args.name
    )
    key = f"{SERVER_PREFIX}{args.name}"
    store_server_token(args.library, path.parents[2], args.name, token, args.yes)

    # Verify the stored token against the server it belongs to.
    answer = request(args.endpoint, "GET", "server", SERVER_HEADER, token, None)
    if not 200 <= answer.status < 300:
        print(
            json.dumps(
                {"key": key, "status": answer.status, "error_code": error_code(answer)}
            )
        )
        print(
            f"postmark.py: {refused('GET server', answer)} under the token now"
            f" stored as {key} in {path}; check or regenerate it in Postmark and"
            f" run `/postmark setup --yes server {args.name}`",
            file=sys.stderr,
        )
        return REFUSED
    try:
        server = json.loads(answer.body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        server = None
    if not isinstance(server, dict):
        server = {}
    print(
        json.dumps(
            {
                "key": key,
                "server_id": server.get("ID"),
                "server_name": server.get("Name"),
            }
        )
    )
    return ANSWERED


# Each subcommand's usage, written out because `argparse` would print a valued
# flag with its value separated, and this collection's grammar attaches it
# (ADR-0176).
USAGES: Final = {
    "call": (
        "[--yes] [--endpoint=<url>] (--account | --server=<name> | --test)"
        " <METHOD> <path> [<json>]"
    ),
    "status": "[--endpoint=<url>]",
    "setup-server": "[--yes] [--endpoint=<url>] --library=<dir> <name>",
}


def parser() -> argparse.ArgumentParser:
    """The command line. A usage error exits 2 with its subcommand's usage."""

    root = argparse.ArgumentParser(
        prog="postmark.py",
        usage="\n".join(f"%(prog)s {name} {usage}" for name, usage in USAGES.items()),
        description="Make one call to Postmark's API.",
    )
    commands = root.add_subparsers(dest="command", required=True)

    call = commands.add_parser(
        "call", prog="postmark.py call", usage=f"%(prog)s {USAGES['call']}"
    )
    call.add_argument("--yes", action="store_true")
    call.add_argument("--endpoint", default=ENDPOINT)
    token = call.add_mutually_exclusive_group(required=True)
    token.add_argument("--account", action="store_true")
    token.add_argument("--server")
    token.add_argument("--test", action="store_true")
    call.add_argument("method")
    call.add_argument("path")
    call.add_argument("json", nargs="?")

    status = commands.add_parser(
        "status", prog="postmark.py status", usage=f"%(prog)s {USAGES['status']}"
    )
    status.add_argument("--endpoint", default=ENDPOINT)

    setup_server = commands.add_parser(
        "setup-server",
        prog="postmark.py setup-server",
        usage=f"%(prog)s {USAGES['setup-server']}",
    )
    setup_server.add_argument("--yes", action="store_true")
    setup_server.add_argument("--endpoint", default=ENDPOINT)
    setup_server.add_argument("--library", required=True, type=Path)
    setup_server.add_argument("name")

    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Parse *argv*, run the subcommand, and return its exit status."""

    args = parser().parse_args(argv)
    try:
        if args.command == "call":
            return command_call(args)
        if args.command == "setup-server":
            return command_setup_server(args)
        return command_status(args)
    except Refusal as refusal:
        print(f"postmark.py: {refusal}", file=sys.stderr)
        return REFUSED
    except PassedOn as refusal:
        sys.stderr.write(str(refusal))
        return REFUSED
    except (Unreachable, Failure) as failure:
        print(f"postmark.py: {failure}", file=sys.stderr)
        return TRANSPORT


if __name__ == "__main__":
    sys.exit(main())
