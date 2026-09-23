"""The ClouDNS engine, driven against a loopback server standing in for the API.

Every case runs the shipped engine through `uv run`, as the Skill's body does,
with `KNTNT_HOME` under the test's own `tmp_path` and a Credential File the test
writes at `0600`. The service is an `http.server` in this process on a port the
operating system picks, passed to the engine as `--endpoint`; it records every
request it receives and answers canned JSON. Nothing here reaches the network
or reads the real `~/.kntnt`.
"""

from __future__ import annotations

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
from urllib.parse import parse_qsl

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ENGINE = REPO_ROOT / "skills" / "infrastructure" / "cloudns" / "scripts" / "cloudns.py"

# The exit statuses the engine promises: the service answered, the service
# could not be reached, and the engine refused before sending anything.
ANSWERED = 0
UNREACHED = 1
REFUSED = 2

# The two credential parameters, under the names ClouDNS reads them by, and
# values distinctive enough that finding one in output is never an accident.
SUB_USER = "kntnt-agent-7f3a"
PASSWORD = "p4ssw0rd-Value-0123456789-abcdefghij"

# What a successful call answers unless a case says otherwise.
SUCCESS = {"status": "Success", "statusDescription": "The record was added."}

POSIX_ONLY = pytest.mark.skipif(
    os.name != "posix", reason="POSIX mode bits mean nothing on Windows"
)


@dataclass
class Received:
    """One request the loopback server received."""

    method: str
    path: str
    body: str
    fields: list[tuple[str, str]]


@dataclass
class Service:
    """The stand-in API: canned answers by path, and every request received.

    A path given several answers gives them in turn, the last one from then on.
    """

    answers: dict[str, list[tuple[int, bytes]]] = field(default_factory=dict)
    requests: list[Received] = field(default_factory=list)
    port: int = 0

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self.port}/"

    def answer(self, path: str, content: object, status: int = 200) -> None:
        """Answer *path* with *content* as JSON, and *status*, after any before it."""

        self.answer_raw(path, json.dumps(content).encode(), status)

    def answer_raw(self, path: str, content: bytes, status: int = 200) -> None:
        """Answer *path* with *content* exactly, and *status*, after any before it."""

        self.answers.setdefault(path, []).append((status, content))

    def next_answer(self, path: str) -> tuple[int, bytes]:
        """The answer *path* gives now."""

        queued = self.answers.get(path)
        if not queued:
            return 200, json.dumps(SUCCESS).encode()
        return queued.pop(0) if len(queued) > 1 else queued[0]

    def fields(self, index: int = -1) -> dict[str, str]:
        return dict(self.requests[index].fields)


@pytest.fixture
def service() -> Iterator[Service]:
    """Serve a `Service` on the loopback interface for the length of one test."""

    state = Service()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode()
            state.requests.append(
                Received(
                    "POST", self.path, body, parse_qsl(body, keep_blank_values=True)
                )
            )
            status, content = state.next_answer(self.path.lstrip("/"))
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def do_GET(self) -> None:
            state.requests.append(Received("GET", self.path, "", []))
            self.send_response(405)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    state.port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield state
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def _credential_file(home: Path) -> Path:
    return home / ".kntnt" / "cloudns" / "credentials.json"


def _write_credentials(
    home: Path, content: dict[str, str] | None = None, mode: int = 0o600
) -> Path:
    """Put a Credential File in place, as `setup` or a person would."""

    path = _credential_file(home)
    path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    path.write_text(
        json.dumps(
            content
            if content is not None
            else {"sub-auth-user": SUB_USER, "auth-password": PASSWORD}
        ),
        encoding="utf-8",
    )
    path.chmod(mode)
    return path


def _run(home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the shipped engine through `uv run` against a home under *home*."""

    uv = shutil.which("uv")
    assert uv is not None
    return subprocess.run(
        [uv, "run", "--python", sys.executable, str(ENGINE), *args],
        env=os.environ | {"KNTNT_HOME": str(home)},
        cwd=home,
        text=True,
        capture_output=True,
        check=False,
    )


def _closed_port() -> int:
    """A loopback port nothing listens on, by binding one and letting it go."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


# --- The script ------------------------------------------------------------


def test_the_engine_declares_pep_723_metadata_and_no_dependency() -> None:
    """It runs anywhere `uv` does, on the standard library alone."""

    text = ENGINE.read_text(encoding="utf-8")

    assert "# /// script\n" in text
    assert "# dependencies = []\n" in text


# --- call ------------------------------------------------------------------


def test_call_posts_both_credentials_and_every_pair_in_the_body(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    answer = {
        "status": "Success",
        "statusDescription": "The record was added successfully.",
        "data": {"id": 42},
    }
    service.answer("dns/add-record.json", answer)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "dns/add-record.json",
        "domain-name=example.com",
        "record-type=A",
        "host=www",
        "record=192.0.2.1",
        "ttl=3600",
    )

    assert result.returncode == ANSWERED, result.stderr
    assert len(service.requests) == 1
    request = service.requests[0]
    assert request.method == "POST"
    assert request.path == "/dns/add-record.json"
    assert service.fields() == {
        "sub-auth-user": SUB_USER,
        "auth-password": PASSWORD,
        "domain-name": "example.com",
        "record-type": "A",
        "host": "www",
        "record": "192.0.2.1",
        "ttl": "3600",
    }
    assert result.stdout == json.dumps(answer)


def test_no_credential_reaches_the_url_or_the_output(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "dns/records.json",
        "domain-name=example.com",
    )

    assert result.returncode == ANSWERED, result.stderr
    url = service.requests[0].path
    assert PASSWORD not in url
    assert SUB_USER not in url
    assert "?" not in url
    assert PASSWORD not in result.stdout + result.stderr


def test_call_prints_the_body_verbatim_and_exits_0_on_an_in_band_failure(
    tmp_path: Path, service: Service
) -> None:
    """ClouDNS reports a failure in band, and the engine relays it untouched."""

    _write_credentials(tmp_path)
    service.answer_raw(
        "dns/mod-record.json",
        b'{"status":"Failed","statusDescription":"Invalid record-id param."}',
    )

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "dns/mod-record.json",
        "record-id=0",
    )

    assert result.returncode == ANSWERED
    assert (
        result.stdout
        == '{"status":"Failed","statusDescription":"Invalid record-id param."}'
    )


def test_call_exits_0_and_prints_the_body_where_the_service_answers_an_http_error(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    service.answer("dns/records.json", {"status": "Failed"}, status=500)

    result = _run(
        tmp_path, "call", f"--endpoint={service.endpoint}", "dns/records.json"
    )

    assert result.returncode == ANSWERED
    assert result.stdout == json.dumps({"status": "Failed"})


@pytest.mark.parametrize(
    "path", ["dns/delete-record.json", "dns/delete.json", "sub-users/delete.json"]
)
def test_a_deleting_path_without_yes_is_refused_and_sends_nothing(
    tmp_path: Path, service: Service, path: str
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        path,
        "domain-name=example.com",
        "record-id=7",
    )

    assert result.returncode == REFUSED
    assert service.requests == []
    assert path in result.stderr
    assert "--yes" in result.stderr


def test_a_deleting_path_with_yes_is_sent(tmp_path: Path, service: Service) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        "--yes",
        f"--endpoint={service.endpoint}",
        "dns/delete-record.json",
        "domain-name=example.com",
        "record-id=7",
    )

    assert result.returncode == ANSWERED, result.stderr
    assert [request.path for request in service.requests] == ["/dns/delete-record.json"]
    assert service.fields()["record-id"] == "7"


def test_delete_existing_records_without_yes_is_refused_and_sends_nothing(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "dns/records-import.json",
        "domain-name=example.com",
        "delete-existing-records=1",
    )

    assert result.returncode == REFUSED
    assert service.requests == []
    assert "dns/records-import.json" in result.stderr
    assert "delete-existing-records=1" in result.stderr
    assert "--yes" in result.stderr


def test_delete_existing_records_with_yes_is_sent(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        "--yes",
        f"--endpoint={service.endpoint}",
        "dns/records-import.json",
        "domain-name=example.com",
        "delete-existing-records=1",
    )

    assert result.returncode == ANSWERED, result.stderr
    assert service.fields()["delete-existing-records"] == "1"


def test_a_path_that_only_mentions_delete_elsewhere_is_not_gated(
    tmp_path: Path, service: Service
) -> None:
    """The gate reads the last segment's start, not the word anywhere."""

    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint={service.endpoint}",
        "dns/records.json",
        "delete-existing-records=0",
    )

    assert result.returncode == ANSWERED, result.stderr
    assert len(service.requests) == 1


@pytest.mark.parametrize(
    "pair", ["auth-password=x", "sub-auth-user=x", "auth-id=1", "sub-auth-id=1"]
)
def test_a_pair_naming_a_credential_parameter_is_refused(
    tmp_path: Path, service: Service, pair: str
) -> None:
    """The credential comes from the Credential File and from nowhere else."""

    _write_credentials(tmp_path)

    result = _run(
        tmp_path, "call", f"--endpoint={service.endpoint}", "dns/records.json", pair
    )

    assert result.returncode == REFUSED
    assert service.requests == []


@pytest.mark.parametrize(
    "path",
    [
        "dns/records.json?host=www",
        "https://elsewhere.example/dns/records.json",
        "../dns/records.json",
        "dns/records.json#top",
    ],
)
def test_a_path_that_is_not_a_plain_api_path_is_refused(
    tmp_path: Path, service: Service, path: str
) -> None:
    """Parameters travel in the body, and the call goes to the endpoint alone."""

    _write_credentials(tmp_path)

    result = _run(tmp_path, "call", f"--endpoint={service.endpoint}", path)

    assert result.returncode == REFUSED
    assert service.requests == []


def test_a_pair_without_a_value_separator_is_refused(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path, "call", f"--endpoint={service.endpoint}", "dns/records.json", "host"
    )

    assert result.returncode == REFUSED
    assert service.requests == []


def test_a_missing_credential_file_is_refused_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    result = _run(
        tmp_path, "call", f"--endpoint={service.endpoint}", "dns/records.json"
    )

    assert result.returncode == REFUSED
    assert "setup" in result.stderr
    assert service.requests == []


@POSIX_ONLY
def test_a_credential_file_others_may_read_is_refused_naming_the_mode(
    tmp_path: Path, service: Service
) -> None:
    path = _write_credentials(tmp_path, mode=0o644)

    result = _run(
        tmp_path, "call", f"--endpoint={service.endpoint}", "dns/records.json"
    )

    assert result.returncode == REFUSED
    assert "0644" in result.stderr
    assert "0600" in result.stderr
    assert str(path) in result.stderr
    assert PASSWORD not in result.stdout + result.stderr
    assert service.requests == []


def test_a_credential_file_missing_a_key_is_refused_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path, {"sub-auth-user": SUB_USER})

    result = _run(
        tmp_path, "call", f"--endpoint={service.endpoint}", "dns/records.json"
    )

    assert result.returncode == REFUSED
    assert "auth-password" in result.stderr
    assert "setup" in result.stderr
    assert service.requests == []


def test_an_unreachable_endpoint_exits_1_with_no_credential_in_the_output(
    tmp_path: Path,
) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        f"--endpoint=http://127.0.0.1:{_closed_port()}/",
        "dns/records.json",
        "domain-name=example.com",
    )

    assert result.returncode == UNREACHED
    assert result.stderr
    assert PASSWORD not in result.stdout + result.stderr
    assert SUB_USER not in result.stdout + result.stderr


def test_an_endpoint_that_is_not_http_is_refused(tmp_path: Path) -> None:
    _write_credentials(tmp_path)

    result = _run(tmp_path, "call", "--endpoint=file:///etc/", "dns/records.json")

    assert result.returncode == REFUSED


def test_an_unknown_flag_is_refused(tmp_path: Path, service: Service) -> None:
    _write_credentials(tmp_path)

    result = _run(
        tmp_path,
        "call",
        "--force",
        f"--endpoint={service.endpoint}",
        "dns/delete-record.json",
    )

    assert result.returncode == REFUSED
    assert service.requests == []


# --- status ----------------------------------------------------------------


def test_status_names_the_sub_user_and_the_zones_it_can_see(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    service.answer(
        "login/login.json", {"status": "Success", "statusDescription": "Success login."}
    )
    service.answer(
        "dns/list-zones.json",
        [
            {"name": "example.com", "type": "master", "zone": "domain", "status": "1"},
            {"name": "example.org", "type": "master", "zone": "domain", "status": "1"},
        ],
    )

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    report = json.loads(result.stdout)
    assert report["sub_user"] == SUB_USER
    assert report["accepted"] is True
    assert report["zones"] == ["example.com", "example.org"]
    assert [request.path for request in service.requests] == [
        "/login/login.json",
        "/dns/list-zones.json",
    ]
    listing = service.fields()
    assert listing["page"] == "1"
    assert listing["rows-per-page"] == "100"
    assert PASSWORD not in result.stdout + result.stderr


def test_status_pages_through_every_zone(tmp_path: Path, service: Service) -> None:
    """A full page means another may follow; a short or empty one ends the list."""

    _write_credentials(tmp_path)
    service.answer("login/login.json", {"status": "Success"})
    service.answer("dns/list-zones.json", [{"name": f"zone{n}.se"} for n in range(100)])
    service.answer("dns/list-zones.json", [{"name": "last.se"}])

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    zones = json.loads(result.stdout)["zones"]
    assert zones[-1] == "last.se"
    assert len(zones) == 101
    assert [dict(request.fields).get("page") for request in service.requests[1:]] == [
        "1",
        "2",
    ]


def test_status_relays_the_description_of_a_refused_login_and_exits_0(
    tmp_path: Path, service: Service
) -> None:
    _write_credentials(tmp_path)
    description = (
        "Invalid authentication, incorrect sub-auth-id, sub-auth-user or auth-password."
    )
    service.answer(
        "login/login.json", {"status": "Failed", "statusDescription": description}
    )

    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == ANSWERED, result.stderr
    report = json.loads(result.stdout)
    assert report["accepted"] is False
    assert report["description"] == description
    assert report["sub_user"] == SUB_USER
    assert report["zones"] is None
    assert [request.path for request in service.requests] == ["/login/login.json"]
    assert PASSWORD not in result.stdout + result.stderr


def test_status_without_a_credential_file_is_refused_naming_setup(
    tmp_path: Path, service: Service
) -> None:
    result = _run(tmp_path, "status", f"--endpoint={service.endpoint}")

    assert result.returncode == REFUSED
    assert "setup" in result.stderr
    assert service.requests == []


def test_status_exits_1_where_the_service_cannot_be_reached(tmp_path: Path) -> None:
    _write_credentials(tmp_path)

    result = _run(tmp_path, "status", f"--endpoint=http://127.0.0.1:{_closed_port()}/")

    assert result.returncode == UNREACHED
    assert PASSWORD not in result.stdout + result.stderr


# --- The body ------------------------------------------------------------


def test_the_bodys_setup_leaves_the_overwrite_gate_to_the_librarys_generate() -> None:
    """`generate` is the gate, so the body passes `--yes` to it and runs none of its own."""

    body = (ENGINE.parent.parent / "SKILL.md").read_text(encoding="utf-8")
    setup = body.split("## setup", 1)[1].split("\n## ", 1)[0]

    assert 'cloudns.py" setup' not in body
    generate = setup.index(
        'credentials.py" generate --skill=cloudns --key=auth-password --to-clipboard'
    )
    steps = setup.index("Tell the user")
    assert generate < steps
    assert "--yes" in setup[generate:steps]


def test_the_engine_has_no_setup_subcommand(tmp_path: Path) -> None:
    """The overwrite gate is the Library's, so the engine keeps no second one."""

    result = _run(tmp_path, "setup")

    assert result.returncode == REFUSED
    assert "usage:" in result.stderr
