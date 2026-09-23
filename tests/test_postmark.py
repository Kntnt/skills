"""The postmark engine, driven as its Skill drives it, against a loopback server.

Every case runs the shipped engine through `uv run` with `KNTNT_HOME` under the
test's own `tmp_path`, so nothing here reads the real `~/.kntnt`, and passes a
loopback `http.server` in this process as `--endpoint`, so nothing reaches
Postmark. The server records every request it receives and answers canned
JSON, which is how a case sees what the engine sent: which header carried which
token, which path, which body, and whether anything was sent at all.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import stat
import subprocess
import sys
import threading
from collections.abc import Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ENGINE = (
    REPO_ROOT / "skills" / "infrastructure" / "postmark" / "scripts" / "postmark.py"
)

# The exit statuses the engine promises: the service answered, the service
# could not be reached, and a refusal made before anything was sent.
ANSWERED = 0
TRANSPORT = 1
REFUSED = 2

# The two headers Postmark authenticates by, and the server token Postmark
# accepts for a send it does not deliver.
SERVER_HEADER = "X-Postmark-Server-Token"
ACCOUNT_HEADER = "X-Postmark-Account-Token"
TEST_TOKEN = "POSTMARK_API_TEST"

# Tokens long and distinctive enough that finding one in output is never an
# accident of some other text containing it.
ACCOUNT_TOKEN = "acct-7f3e9c1a-Account-Token-0123456789"
TRANSACTIONAL_TOKEN = "srv-2b8d4e6f-Transactional-Token-9876543210"
BROADCAST_TOKEN = "srv-5a1c3e7b-Broadcast-Token-1357924680"
TOKENS = (ACCOUNT_TOKEN, TRANSACTIONAL_TOKEN, BROADCAST_TOKEN)

# The two servers the Credential File holds a token for, the second with a
# space in its name as Postmark allows.
TRANSACTIONAL = "transactional"
BROADCAST = "My Broadcast"

# The file modes the rule names: what a Credential File is held at, and a mode
# every reader refuses.
FILE_MODE = 0o600
LOOSE_MODE = 0o644

POSIX_ONLY = pytest.mark.skipif(
    os.name != "posix",
    reason="POSIX mode bits mean nothing on Windows, where the ACL is used",
)


@dataclass
class Received:
    """One request the loopback server received."""

    method: str
    path: str
    headers: dict[str, str]
    body: bytes


@dataclass
class Service:
    """The loopback stand-in for Postmark: canned answers, and what arrived."""

    port: int = 0
    answers: dict[tuple[str, str], tuple[int, bytes]] = field(default_factory=dict)
    received: list[Received] = field(default_factory=list)

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def answer(self, method: str, path: str, status: int, body: object) -> None:
        """Answer *method* on *path* with *status* and *body* as JSON."""

        self.answers[(method, path)] = (status, json.dumps(body).encode())


# What the loopback server answers a request nobody set an answer for.
DEFAULT_ANSWER = b'{"ErrorCode":0,"Message":"OK"}'


@pytest.fixture
def service() -> Iterator[Service]:
    """Serve a fresh loopback stand-in for one test, and stop it afterwards."""

    served = Service()

    class Handler(BaseHTTPRequestHandler):
        def _answer(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            served.received.append(
                Received(self.command, self.path, dict(self.headers), body)
            )
            status, content = served.answers.get(
                (self.command, self.path), (200, DEFAULT_ANSWER)
            )
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _answer

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    served.port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield served
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def _credential_file(tmp_path: Path) -> Path:
    return tmp_path / ".kntnt" / "postmark" / "credentials.json"


def _write_credentials(
    tmp_path: Path, content: dict[str, str] | None = None, mode: int = FILE_MODE
) -> Path:
    """Write the Credential File under *tmp_path*, by default with all three tokens."""

    path = _credential_file(tmp_path)
    path.parent.mkdir(parents=True, mode=0o700)
    held = (
        {
            "account-token": ACCOUNT_TOKEN,
            f"server:{TRANSACTIONAL}": TRANSACTIONAL_TOKEN,
            f"server:{BROADCAST}": BROADCAST_TOKEN,
        }
        if content is None
        else content
    )
    path.write_text(json.dumps(held), encoding="utf-8")
    path.chmod(mode)
    return path


def _run(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the shipped engine against a home under *tmp_path*.

    Loopback is kept off any proxy the environment names, so the request the
    engine makes is the one the loopback server receives.
    """

    uv = shutil.which("uv")
    assert uv is not None
    return subprocess.run(
        [uv, "run", "--python", sys.executable, str(ENGINE), *args],
        env=os.environ
        | {
            "KNTNT_HOME": str(tmp_path),
            "NO_PROXY": "127.0.0.1,localhost",
            "no_proxy": "127.0.0.1,localhost",
        },
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )


def _assert_no_token(
    result: subprocess.CompletedProcess[str], received: list[Received]
) -> None:
    """No token stands in the output, a URL or a body; only in its own header."""

    for token in TOKENS:
        assert token not in result.stdout, "a token reached stdout"
        assert token not in result.stderr, "a token reached stderr"
        for request in received:
            assert token not in request.path, "a token reached the URL"
            assert token.encode() not in request.body, "a token reached the body"


# The account token and each server token go in their own header, and nowhere
# else.


def test_the_account_token_goes_in_the_account_header_alone(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    servers = {"TotalCount": 1, "Servers": [{"ID": 1, "Name": TRANSACTIONAL}]}
    service.answer("GET", "/servers?count=50&offset=0", 200, servers)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--account",
        "GET",
        "servers?count=50&offset=0",
    )

    assert result.returncode == ANSWERED, result.stderr
    assert result.stdout == json.dumps(servers)
    [request] = service.received
    assert request.path == "/servers?count=50&offset=0"
    assert request.headers[ACCOUNT_HEADER] == ACCOUNT_TOKEN
    assert SERVER_HEADER not in request.headers
    assert request.headers["Accept"] == "application/json"
    _assert_no_token(result, service.received)


def test_a_server_token_goes_in_the_server_header_alone(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    service.answer("GET", "/server", 200, {"ID": 2, "Name": BROADCAST})

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={BROADCAST}",
        "GET",
        "/server",
    )

    assert result.returncode == ANSWERED, result.stderr
    assert result.stdout == json.dumps({"ID": 2, "Name": BROADCAST})
    [request] = service.received
    assert request.path == "/server"
    assert request.headers[SERVER_HEADER] == BROADCAST_TOKEN
    assert ACCOUNT_HEADER not in request.headers
    _assert_no_token(result, service.received)


@pytest.mark.parametrize("path", ["server", "/server"])
@pytest.mark.parametrize("trailing", ["", "/"])
def test_the_endpoint_and_the_path_are_joined_with_one_slash(
    tmp_path: Path, service: Service, path: str, trailing: str
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}{trailing}",
        f"--server={TRANSACTIONAL}",
        "GET",
        path,
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.path == "/server"


def test_a_server_the_file_holds_no_token_for_is_refused(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--server=outbound",
        "GET",
        "server",
    )

    assert result.returncode == REFUSED
    assert "setup server" in result.stderr
    assert service.received == []
    _assert_no_token(result, service.received)


def test_the_account_token_missing_from_the_file_is_refused(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path, {f"server:{TRANSACTIONAL}": TRANSACTIONAL_TOKEN})

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--account",
        "GET",
        "servers",
    )

    assert result.returncode == REFUSED
    assert "setup account" in result.stderr
    assert service.received == []


# The test token needs no Credential File and no `--yes`, since nothing leaves.


SEND = {
    "From": "sender@example.com",
    "To": "receiver@example.com",
    "Subject": "Hello",
    "TextBody": "Hello.",
    "MessageStream": "outbound",
}


@POSIX_ONLY
def test_a_test_send_uses_the_test_token_without_reading_the_file(
    tmp_path: Path, service: Service
) -> None:
    # A file every reader refuses: had the engine read it, it would refuse.
    _write_credentials(tmp_path, mode=LOOSE_MODE)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--test",
        "POST",
        "email",
        json.dumps(SEND),
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.method == "POST"
    assert request.path == "/email"
    assert request.headers[SERVER_HEADER] == TEST_TOKEN
    assert ACCOUNT_HEADER not in request.headers
    assert json.loads(request.body) == SEND
    _assert_no_token(result, service.received)


def test_a_test_send_needs_no_credential_file(tmp_path: Path, service: Service) -> None:
    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--test",
        "POST",
        "/email/withTemplate",
        json.dumps({"TemplateAlias": "welcome", "TemplateModel": {}}),
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.headers[SERVER_HEADER] == TEST_TOKEN


# What Postmark cannot undo is refused without `--yes`, and sent with it.


GATED = [
    pytest.param(["--account", "DELETE", "servers/7"], "/servers/7", id="delete"),
    pytest.param(
        [f"--server={TRANSACTIONAL}", "POST", "email", json.dumps(SEND)],
        "/email",
        id="send",
    ),
    pytest.param(
        [f"--server={TRANSACTIONAL}", "POST", "/email/batch", json.dumps([SEND])],
        "/email/batch",
        id="batch",
    ),
    pytest.param(
        [f"--server={TRANSACTIONAL}", "POST", "email/bulk", json.dumps(SEND)],
        "/email/bulk",
        id="bulk",
    ),
    pytest.param(
        [f"--server={TRANSACTIONAL}", "POST", "email/withTemplate", "{}"],
        "/email/withTemplate",
        id="template-send",
    ),
    pytest.param(
        [f"--server={TRANSACTIONAL}", "POST", "email/batchWithTemplates", "{}"],
        "/email/batchWithTemplates",
        id="template-batch",
    ),
    pytest.param(
        [
            "--account",
            "POST",
            "data-removals",
            json.dumps({"RequestedBy": "a@example.com", "RequestedFor": "b@x.se"}),
        ],
        "/data-removals",
        id="data-removal",
    ),
    pytest.param(
        [f"--server={TRANSACTIONAL}", "delete", "templates/welcome"],
        "/templates/welcome",
        id="lowercase-delete",
    ),
]


@pytest.mark.parametrize(("arguments", "path"), GATED)
def test_a_call_postmark_cannot_undo_is_refused_without_yes(
    tmp_path: Path, service: Service, arguments: list[str], path: str
) -> None:
    _write_credentials(tmp_path)

    result = _run(tmp_path, "call", f"--endpoint={service.endpoint}", *arguments)

    assert result.returncode == REFUSED
    assert service.received == []
    assert path in result.stderr, "the refusal names what it refused"
    assert "--yes" in result.stderr, "the refusal says what --yes asserts"
    _assert_no_token(result, service.received)


@pytest.mark.parametrize(("arguments", "path"), GATED)
def test_a_call_postmark_cannot_undo_is_sent_with_yes(
    tmp_path: Path, service: Service, arguments: list[str], path: str
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path, "call", "--yes", f"--endpoint={service.endpoint}", *arguments
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.path == path
    assert request.method == arguments[1].upper()


def test_archiving_a_message_stream_is_not_gated(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={TRANSACTIONAL}",
        "POST",
        "message-streams/broadcasts/archive",
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.method == "POST"
    assert request.path == "/message-streams/broadcasts/archive"
    assert request.headers["Content-Length"] == "0"


def test_a_put_sends_its_json_operand_as_the_body(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    template = {
        "Name": "Welcome",
        "Subject": "Welcome, {{name}}",
        "HtmlBody": "<p>Hi</p>",
    }

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={TRANSACTIONAL}",
        "PUT",
        "templates/welcome",
        json.dumps(template),
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.method == "PUT"
    assert json.loads(request.body) == template
    assert request.headers["Content-Type"] == "application/json"


def test_a_patch_sends_its_json_operand_as_the_body(
    tmp_path: Path, service: Service
) -> None:
    # Postmark edits a message stream with PATCH, so the engine carries a body
    # on it as it does on POST and PUT.
    _write_credentials(tmp_path)
    stream = {"Name": "Newsletters"}

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={TRANSACTIONAL}",
        "PATCH",
        "message-streams/broadcasts",
        json.dumps(stream),
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.received
    assert request.method == "PATCH"
    assert json.loads(request.body) == stream


def test_an_operand_on_a_method_that_takes_no_body_is_refused(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={TRANSACTIONAL}",
        "GET",
        "templates",
        "{}",
    )

    assert result.returncode == REFUSED
    assert service.received == []


def test_an_operand_that_is_not_json_is_refused(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={TRANSACTIONAL}",
        "PUT",
        "templates/welcome",
        "{not json",
    )

    assert result.returncode == REFUSED
    assert "JSON" in result.stderr
    assert service.received == []


def test_an_error_the_service_answers_is_relayed_with_exit_zero(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    error = {"ErrorCode": 10, "Message": "Bad or missing API token"}
    service.answer("GET", "/server", 401, error)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        f"--server={TRANSACTIONAL}",
        "GET",
        "server",
    )

    assert result.returncode == ANSWERED
    assert result.stdout == json.dumps(error)
    assert "401" in result.stderr


# The Credential File is read as the rule states, and its absence names setup.


def test_a_missing_credential_file_is_refused_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--account",
        "GET",
        "servers",
    )

    assert result.returncode == REFUSED
    assert "setup" in result.stderr
    assert service.received == []


@POSIX_ONLY
def test_a_credential_file_others_may_read_is_refused_naming_the_mode(
    tmp_path: Path, service: Service
) -> None:
    path = _write_credentials(tmp_path, mode=LOOSE_MODE)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "--account",
        "GET",
        "servers",
    )

    assert result.returncode == REFUSED
    assert str(path) in result.stderr
    assert "0644" in result.stderr
    assert "0600" in result.stderr
    assert stat.S_IMODE(path.stat().st_mode) == LOOSE_MODE
    assert service.received == []
    _assert_no_token(result, service.received)


def _unreachable_endpoint() -> str:
    """A loopback address nothing listens on: bound once, then released."""

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return f"http://127.0.0.1:{port}"


def test_a_transport_failure_exits_one_without_a_token(tmp_path: Path) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={_unreachable_endpoint()}",
        "--account",
        "GET",
        "servers",
    )

    assert result.returncode == TRANSPORT
    assert result.stderr
    _assert_no_token(result, [])


# `status` reads every token the file holds against the service.


def _status(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    report = json.loads(result.stdout)
    assert isinstance(report, dict)
    return report


def test_status_lists_the_servers_and_verifies_each_server_token(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    servers = {
        "TotalCount": 3,
        "Servers": [
            {"ID": 1, "Name": TRANSACTIONAL},
            {"ID": 2, "Name": BROADCAST},
            {"ID": 3, "Name": "staging"},
        ],
    }
    service.answer("GET", "/servers?count=500&offset=0", 200, servers)
    service.answer("GET", "/server", 200, {"ID": 1, "Name": TRANSACTIONAL})

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    report = _status(result)
    assert report["account"] == {"held": True, "status": 200, "body": servers}
    assert report["servers"] == {
        BROADCAST: {"status": 200, "body": {"ID": 1, "Name": TRANSACTIONAL}},
        TRANSACTIONAL: {"status": 200, "body": {"ID": 1, "Name": TRANSACTIONAL}},
    }
    by_header = sorted(
        request.headers.get(SERVER_HEADER) or request.headers[ACCOUNT_HEADER]
        for request in service.received
    )
    assert by_header == sorted(TOKENS)
    _assert_no_token(result, service.received)


def test_status_relays_a_token_the_service_refuses(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path, {f"server:{TRANSACTIONAL}": TRANSACTIONAL_TOKEN})
    error = {"ErrorCode": 10, "Message": "Bad or missing API token"}
    service.answer("GET", "/server", 401, error)

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    report = _status(result)
    assert report["servers"] == {TRANSACTIONAL: {"status": 401, "body": error}}
    _assert_no_token(result, service.received)


def test_status_without_an_account_token_says_what_setup_account_adds(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path, {f"server:{TRANSACTIONAL}": TRANSACTIONAL_TOKEN})

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    report = _status(result)
    account = report["account"]
    assert isinstance(account, dict)
    assert account["held"] is False
    assert "setup account" in account["note"]
    assert [request.path for request in service.received] == ["/server"]


def test_status_with_no_credential_file_is_refused_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == REFUSED
    assert "setup" in result.stderr
    assert service.received == []


def test_status_with_a_file_holding_no_token_is_refused_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path, {})

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == REFUSED
    assert "setup" in result.stderr
    assert service.received == []


def test_status_exits_one_on_a_transport_failure(tmp_path: Path) -> None:
    _write_credentials(tmp_path)

    result = _run(tmp_path, "status", f"--endpoint={_unreachable_endpoint()}")

    assert result.returncode == TRANSPORT
    _assert_no_token(result, [])
