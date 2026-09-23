"""The NodePing engine, driven as the Skill's body drives it.

Every case runs the shipped engine through `uv run` against a `KNTNT_HOME`
under the test's own `tmp_path`, holding a Credential File the test writes,
and points it with `--endpoint` at a loopback HTTP server in this process that
records each request and answers canned JSON. Nothing here reaches the
network or reads the real `~/.kntnt`.
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
from collections.abc import Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "infrastructure" / "nodeping"
ENGINE = SKILL / "scripts" / "nodeping.py"

# The exit statuses the engine promises: the service answered, the service
# could not be reached, and a refusal the engine made itself.
ANSWERED = 0
TRANSPORT = 1
REFUSED = 2

# A token long and distinctive enough that finding it in output is never an
# accident of some other text containing it.
TOKEN = "NodePingTok3n-0123456789-abcdefghij"

# The file modes the Credential File rule names.
FILE_MODE = 0o600
DIRECTORY_MODE = 0o700
LOOSE_MODE = 0o644

# The account `GET accounts` answers with in the canned success.
ACCOUNT = {
    "201205050153W2Q4C": {"_id": "201205050153W2Q4C", "name": "Kntnt Monitoring"}
}

POSIX_ONLY = pytest.mark.skipif(
    os.name != "posix",
    reason="POSIX mode bits mean nothing on Windows, where the ACL is used",
)


@dataclass
class Request:
    """One request the loopback service received."""

    method: str
    path: str
    headers: dict[str, str]
    body: bytes


@dataclass
class Service:
    """A loopback stand-in for NodePing: what it answers, and what arrived."""

    port: int = 0
    status: int = 200
    answer: bytes = b'{"ok":true}'
    requests: list[Request] = field(default_factory=list)

    @property
    def endpoint(self) -> str:
        """The endpoint to pass, shaped as the real default is, trailing slash and all."""

        return f"http://127.0.0.1:{self.port}/api/1/"


@pytest.fixture
def service() -> Iterator[Service]:
    """Serve a fresh loopback service for one test, and stop it afterwards."""

    served = Service()

    class Handler(BaseHTTPRequestHandler):
        def _answer(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            served.requests.append(
                Request(self.command, self.path, dict(self.headers), body)
            )
            self.send_response(served.status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(served.answer)))
            self.end_headers()
            self.wfile.write(served.answer)

        do_GET = do_POST = do_PUT = do_DELETE = _answer

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


def _run(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the shipped engine against a home under *tmp_path*."""

    uv = shutil.which("uv")
    assert uv is not None
    return subprocess.run(
        [uv, "run", "--python", sys.executable, str(ENGINE), *args],
        env=os.environ | {"KNTNT_HOME": str(tmp_path)},
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )


def _credentials(
    tmp_path: Path, content: dict[str, str] | None = None, mode: int = FILE_MODE
) -> Path:
    """Put the Skill's Credential File in place, as `setup` or a person would."""

    path = tmp_path / ".kntnt" / "nodeping" / "credentials.json"
    path.parent.mkdir(parents=True, mode=DIRECTORY_MODE)
    path.write_text(json.dumps({"token": TOKEN} if content is None else content))
    path.chmod(mode)
    return path


def _form(request: Request) -> dict[str, list[str]]:
    return parse_qs(request.body.decode("utf-8"), keep_blank_values=True)


def _assert_no_token(
    result: subprocess.CompletedProcess[str], service: Service
) -> None:
    """The token stands in no output and in no part of a request but its header."""

    assert TOKEN not in result.stdout
    assert TOKEN not in result.stderr
    for request in service.requests:
        assert TOKEN not in request.path
        assert TOKEN.encode() not in request.body


# --- The script ----------------------------------------------------------


def test_the_engine_declares_pep_723_metadata_and_no_dependency() -> None:
    """It runs anywhere `uv` does, on the standard library alone."""

    text = ENGINE.read_text(encoding="utf-8")

    assert "# /// script\n" in text
    assert "# dependencies = []\n" in text


# --- A call --------------------------------------------------------------


def test_a_post_sends_the_operand_as_the_json_field_with_the_token_as_basic_user(
    tmp_path: Path, service: Service
) -> None:
    """The token rides as the Basic user name with an empty password, and nowhere else."""

    _credentials(tmp_path)
    service.answer = b'{"_id":"X-1","label":"kntnt.se"}\n'
    check = {"type": "HTTP", "target": "https://kntnt.se/", "label": "kntnt.se"}

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "POST",
        "checks",
        json.dumps(check),
    )

    assert result.returncode == ANSWERED, result.stderr
    assert result.stdout == service.answer.decode()
    [request] = service.requests
    assert request.method == "POST"
    assert request.path == "/api/1/checks"
    expected = base64.b64encode(f"{TOKEN}:".encode()).decode()
    assert request.headers["Authorization"] == f"Basic {expected}"
    assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert json.loads(_form(request)["json"][0]) == check
    _assert_no_token(result, service)


@pytest.mark.parametrize("endpoint_suffix", ["/api/1/", "/api/1"])
def test_the_endpoint_and_the_path_are_joined_with_one_slash(
    tmp_path: Path, service: Service, endpoint_suffix: str
) -> None:
    """A default ending in `/` and a path without one make `…/api/1/checks`, not `//`."""

    _credentials(tmp_path)
    endpoint = f"http://127.0.0.1:{service.port}{endpoint_suffix}"

    result = _run(
        tmp_path, "call", f"--endpoint={endpoint}", "GET", "checks?uptime=true"
    )

    assert result.returncode == ANSWERED, result.stderr
    assert [request.path for request in service.requests] == [
        "/api/1/checks?uptime=true"
    ]


def test_a_put_sends_its_operand_and_is_not_gated(
    tmp_path: Path, service: Service
) -> None:
    """Overwriting and disabling can be undone, so neither needs `--yes`."""

    _credentials(tmp_path)
    change = {"enabled": "false", "label": "kntnt.se (paused)"}

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "PUT",
        "checks/X-1",
        json.dumps(change),
    )

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.requests
    assert request.method == "PUT"
    assert request.path == "/api/1/checks/X-1"
    assert json.loads(_form(request)["json"][0]) == change


def test_a_refusal_by_the_service_exits_0_with_its_body_verbatim(
    tmp_path: Path, service: Service
) -> None:
    """The service answered, so the engine relays the answer rather than judging it."""

    _credentials(tmp_path)
    service.status = 400
    service.answer = b'{"error":"Invalid check type"}'

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "POST",
        "checks",
        '{"type":"NOPE"}',
    )

    assert result.returncode == ANSWERED
    assert result.stdout == '{"error":"Invalid check type"}'
    assert "400" in result.stderr
    _assert_no_token(result, service)


@pytest.mark.parametrize(
    ("method", "operand", "why"),
    [
        ("POST", "[1, 2]", "JSON object"),
        ("POST", "{not json", "JSON object"),
        ("GET", '{"id": "X-1"}', "query string"),
        ("PATCH", None, "PATCH"),
    ],
)
def test_a_malformed_call_is_refused_and_sends_nothing(
    tmp_path: Path, service: Service, method: str, operand: str | None, why: str
) -> None:
    """An operand that is no JSON object, one on a GET, and an unknown method."""

    _credentials(tmp_path)
    args = ["call", f"--endpoint={service.endpoint}", method, "checks"]

    result = _run(tmp_path, *args, *([operand] if operand is not None else []))

    assert result.returncode == REFUSED
    assert why in result.stderr
    assert service.requests == []


# --- The gate ------------------------------------------------------------


@pytest.mark.parametrize(
    ("method", "path", "operand"),
    [
        ("DELETE", "checks/X-1", None),
        ("GET", "checks/X-1?action=delete", None),
        ("GET", "checks/X-1?id=X-1&action=DELETE", None),
        ("POST", "checks/X-1", '{"action": "Delete"}'),
        ("PUT", "contacts/C-1", '{"action": "delete", "name": "x"}'),
        ("GET", 'schedules/Days?json={"action":"delete"}', None),
    ],
)
def test_a_deletion_without_yes_exits_2_sends_nothing_and_names_what_it_refused(
    tmp_path: Path, service: Service, method: str, path: str, operand: str | None
) -> None:
    """Both spellings of a deletion — the method and the `action` parameter — are gated."""

    _credentials(tmp_path)
    args = ["call", f"--endpoint={service.endpoint}", method, path]

    result = _run(tmp_path, *args, *([operand] if operand is not None else []))

    assert result.returncode == REFUSED
    assert service.requests == []
    assert f"{method} {path}" in result.stderr
    assert "--yes" in result.stderr
    assert "authoriz" in result.stderr
    _assert_no_token(result, service)


@pytest.mark.parametrize(
    ("method", "path", "operand"),
    [
        ("DELETE", "checks/X-1", None),
        ("GET", "checks/X-1?action=delete", None),
        ("POST", "checks/X-1", '{"action": "Delete"}'),
    ],
)
def test_a_deletion_with_yes_is_sent(
    tmp_path: Path, service: Service, method: str, path: str, operand: str | None
) -> None:
    """`--yes` asserts the deletion is authorized, and the engine then sends it."""

    _credentials(tmp_path)
    args = ["call", "--yes", f"--endpoint={service.endpoint}", method, path]

    result = _run(tmp_path, *args, *([operand] if operand is not None else []))

    assert result.returncode == ANSWERED, result.stderr
    [request] = service.requests
    assert request.method == method
    assert request.path == f"/api/1/{path}"
    if operand is not None:
        assert json.loads(_form(request)["json"][0]) == json.loads(operand)


# --- The Credential File -------------------------------------------------


def test_a_missing_credential_file_exits_2_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    result = _run(tmp_path, "call", f"--endpoint={service.endpoint}", "GET", "checks")

    assert result.returncode == REFUSED
    assert "/nodeping setup" in result.stderr
    assert service.requests == []


def test_a_credential_file_without_a_token_exits_2_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    _credentials(tmp_path, {"other": "value"})

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == REFUSED
    assert "token" in result.stderr
    assert "/nodeping setup" in result.stderr
    assert service.requests == []


@POSIX_ONLY
def test_a_credential_file_group_or_world_may_read_exits_2_naming_the_mode(
    tmp_path: Path, service: Service
) -> None:
    path = _credentials(tmp_path, mode=LOOSE_MODE)

    result = _run(tmp_path, "call", f"--endpoint={service.endpoint}", "GET", "checks")

    assert result.returncode == REFUSED
    assert str(path) in result.stderr
    assert "0644" in result.stderr
    assert "0600" in result.stderr
    assert service.requests == []
    _assert_no_token(result, service)


def test_an_unreachable_endpoint_exits_1_with_no_token_in_the_message(
    tmp_path: Path,
) -> None:
    _credentials(tmp_path)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    result = _run(
        tmp_path, "call", f"--endpoint=http://127.0.0.1:{port}/api/1/", "GET", "checks"
    )

    assert result.returncode == TRANSPORT
    assert result.stderr.strip()
    assert TOKEN not in result.stdout
    assert TOKEN not in result.stderr


# --- status --------------------------------------------------------------


def test_status_asks_for_the_account_and_prints_its_answer(
    tmp_path: Path, service: Service
) -> None:
    _credentials(tmp_path)
    service.answer = json.dumps(ACCOUNT).encode()

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    assert json.loads(result.stdout) == ACCOUNT
    assert "Kntnt Monitoring" in result.stdout
    [request] = service.requests
    assert (request.method, request.path) == ("GET", "/api/1/accounts")
    assert request.headers["Authorization"].startswith("Basic ")
    _assert_no_token(result, service)


def test_status_relays_the_services_refusal_and_exits_0(
    tmp_path: Path, service: Service
) -> None:
    """A 403 is an answer, so only a transport failure is 1 and a local refusal 2."""

    _credentials(tmp_path)
    service.status = 403
    service.answer = b'{"error":"Invalid token"}'

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED
    assert result.stdout == '{"error":"Invalid token"}'
    assert "403" in result.stderr
    _assert_no_token(result, service)


# --- The body ------------------------------------------------------------


def test_the_bodys_setup_leaves_the_overwrite_gate_to_the_librarys_set() -> None:
    """`set` is the gate, so the body passes `--yes` to it and runs no check of its own.

    The status step comes after the store, so one answer says both that the
    file is written and whether the service accepts the token.
    """

    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    setup = body.split("## setup", 1)[1].split("\n## ", 1)[0]

    assert 'credentials.py" show' not in setup
    store = setup.index(
        'credentials.py" set --skill=nodeping --key=token --from-clipboard'
    )
    status = setup.index('nodeping.py" status')
    assert store < status
    assert "--yes" in setup[store:status]
