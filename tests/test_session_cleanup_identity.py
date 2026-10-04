"""Process cleanup refuses signals unless the recorded OS identity still holds."""

from __future__ import annotations

import importlib.util
import json
import os
import selectors
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(
    os.environ.get(
        "KNTNT_SESSION_CLEANUP_SUBJECT_SCRIPT",
        str(ROOT / "skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"),
    )
)
PID = 98765432
BIRTH = "Sun Oct  4 12:00:00 2026"

# Preserve actual ps responses at the OS boundary while running the public CLI.
PROBE_DRIVER = """
import json, runpy, subprocess, sys, time
from pathlib import Path
destination = Path(sys.argv.pop())
script = sys.argv.pop(1)
sys.argv[0] = script
original = subprocess.run
observations = []
def observe(args, **kwargs):
    \"\"\"Preserve an authentic external observation without changing its result.\"\"\"
    row = {"argv": args, "cwd": str(kwargs.get("cwd")), "at": time.time()}
    try:
        answer = original(args, **kwargs)  # cwd is supplied by the observed caller.
        row.update(exit=answer.returncode, stdout=answer.stdout, stderr=answer.stderr)
        return answer
    except Exception as error:  # Record and re-raise the OS boundary failure.
        row["error"] = repr(error)
        raise
    finally:
        observations.append(row)
        destination.write_text(json.dumps(observations, indent=2))
subprocess.run = observe
runpy.run_path(script, run_name="__main__")
"""


def _cleanup() -> Any:
    """Load the public Feature seams without running a lifecycle event."""

    spec = importlib.util.spec_from_file_location("cleanup_identity", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def machine(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    """Intercept every OS signal and model observations at OS boundaries."""

    state: dict[str, Any] = {
        "birth": BIRTH,
        "pgid": PID,
        "live": True,
        "group_live": True,
        "signals": [],
        "after_term": {"live": False, "group_live": False},
        "after_kill": {"live": False, "group_live": False},
        "group_error": None,
    }

    def kill(target: int, number: int) -> None:
        """Deliver no real signal, including to a synthetic or foreign PID."""

        assert target in {PID, -PID}
        if number == 0:
            if target < 0 and state["group_error"] is not None:
                raise state["group_error"]("group observation unavailable")
            if not state["live" if target > 0 else "group_live"]:
                raise ProcessLookupError()
            return
        state["signals"].append((target, number))
        if number == signal.SIGTERM:
            state.update(state["after_term"])
        if number == signal.SIGKILL:
            state.update(state["after_kill"])

    def group(pid: int) -> int:
        """Expose group membership, including an unavailable lookup."""

        assert pid == PID
        if state["pgid"] is None:
            raise ProcessLookupError()
        return int(state["pgid"])

    def probe(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Expose ps identity failures at the external command seam."""

        assert Path(kwargs["cwd"]).is_dir()
        if "-axo" in args:
            return subprocess.CompletedProcess(args, 0, f"{os.getpid()} 1 python\n", "")
        assert args == ["ps", "-o", "lstart=", "-p", str(PID)]
        if state["birth"] is None:
            raise OSError("identity unreadable")
        return subprocess.CompletedProcess(args, 0, state["birth"], "")

    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    monkeypatch.setattr(os, "kill", kill)
    monkeypatch.setattr(os, "getpgid", group)
    monkeypatch.setattr(subprocess, "run", probe)
    # Move the clock past the grace after TERM; no startup race is involved.
    ticks = iter([0.0, 10.0])
    monkeypatch.setattr("time.monotonic", lambda: next(ticks))
    return state


@pytest.mark.parametrize("recorded", [None, "", "   "])
def test_missing_recorded_birth_refuses_every_destructive_signal(
    machine: dict[str, Any], recorded: str | None
) -> None:
    """Later knowledge cannot authenticate an empty historical registration."""

    entry = (
        {"id": str(PID)} if recorded is None else {"id": str(PID), "started": recorded}
    )

    result = _cleanup().stop_pid(entry)

    assert machine["signals"] == []
    assert result["outcome"] == "refused"
    assert "recorded" in result["detail"]


@pytest.mark.parametrize("current", [None, "", "   "])
def test_unavailable_current_birth_refuses_every_destructive_signal(
    machine: dict[str, Any], current: str | None
) -> None:
    """An unreadable identity is uncertainty, rather than a proven reused PID."""

    machine["birth"] = current

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == []
    assert result["outcome"] == "refused"
    assert "current" in result["detail"]


def test_mismatched_birth_leaves_the_reused_pid_alone(machine: dict[str, Any]) -> None:
    """A known foreign incarnation receives neither TERM nor KILL."""

    machine["birth"] = "Sun Oct  4 12:01:00 2026"

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == []
    assert result["outcome"] == "reused"


@pytest.mark.parametrize(
    ("changed", "outcome"),
    [
        ({"birth": "another birth"}, "reused"),
        ({"birth": ""}, "refused"),
        ({"birth": None}, "refused"),
        ({"pgid": PID + 1}, "refused"),
        ({"pgid": None}, "refused"),
    ],
)
def test_escalation_rechecks_the_current_intended_identity(
    machine: dict[str, Any], changed: dict[str, Any], outcome: str
) -> None:
    """TERM's earlier identity never authorizes KILL against a changed target."""

    machine["after_term"] = changed

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == [(-PID, signal.SIGTERM)]
    assert result["outcome"] == outcome


def test_unavailable_group_membership_refuses_term(machine: dict[str, Any]) -> None:
    """A failed group observation cannot silently downgrade the intended target."""

    machine["pgid"] = None

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == []
    assert result["outcome"] == "refused"


@pytest.mark.parametrize("initially_gone", [True, False])
def test_a_surviving_leaderless_group_is_refused(
    machine: dict[str, Any], initially_gone: bool
) -> None:
    """The missing leader cannot authenticate any members still in its group."""

    machine["live"] = not initially_gone
    machine["after_term"] = {"live": False}

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == ([] if initially_gone else [(-PID, signal.SIGTERM)])
    assert result["outcome"] == "refused"
    assert "group" in result["detail"]


def test_a_genuinely_gone_process_and_group_are_successful(
    machine: dict[str, Any],
) -> None:
    """A confirmed absence still completes a recorded cleanup."""

    machine.update(live=False, group_live=False)

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == []
    assert result == {"outcome": "gone", "detail": None}


@pytest.mark.parametrize("group_leader", [True, False])
def test_valid_owned_term_stops_only_the_intended_scope(
    machine: dict[str, Any], group_leader: bool
) -> None:
    """A follower never signals its caller's shared group."""

    if not group_leader:
        machine["pgid"] = PID + 1

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == [(-PID if group_leader else PID, signal.SIGTERM)]
    assert result == {
        "outcome": "stopped",
        "detail": "group" if group_leader else "process",
    }


def test_valid_owned_escalation_still_stops_the_group(machine: dict[str, Any]) -> None:
    """An unchanged authentic leader can authorize escalation."""

    machine["after_term"] = {}

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == [(-PID, signal.SIGTERM), (-PID, signal.SIGKILL)]
    assert result == {"outcome": "killed", "detail": "group"}


@pytest.mark.parametrize("recorded", ["", BIRTH])
def test_sweep_retains_unresolved_identity_without_backfilling(
    machine: dict[str, Any], recorded: str
) -> None:
    """The original manifest remains inspectable rather than disappearing on refusal."""

    cleanup = _cleanup()
    machine["birth"] = ""
    path = cleanup.manifest_path("unresolved")
    cleanup.append(path, {"kind": "session", "id": "unresolved"})
    cleanup.append(
        path, {"kind": "pid", "id": str(PID), "started": recorded, "why": "owned"}
    )
    original = path.read_bytes()

    result = cleanup.sweep(path, why="end")

    assert result["acted"][0]["outcome"] == "refused"
    assert machine["signals"] == []
    assert path.exists(), "unresolved cleanup must be retryable"
    assert path.read_bytes() == original
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    assert any(row.get("outcome") == "refused" for row in rows)
    assert any(row["event"] == "manifest-kept" for row in rows)

    # Retry an authentic recorded birth once the OS can identify it again.
    if recorded:
        machine["birth"] = BIRTH
        retry = cleanup.sweep(path, why="start")
        assert retry["acted"][0]["outcome"] == "stopped"
        assert not path.exists()


def test_first_registration_in_a_fresh_nested_home_has_authentic_birth_and_owner(
    tmp_path: Path,
) -> None:
    """Readiness and independent ps observations authenticate the public receipt."""

    fresh = tmp_path / "never-created" / "nested-home"
    assert not fresh.exists()
    program = """
import json, os, subprocess, sys
from pathlib import Path
print("READY", flush=True)
assert sys.stdin.readline().strip() == "record"
environment = {**os.environ, "KNTNT_HOME": sys.argv[2],
    "CLAUDE_PID": str(os.getpid()), "CLAUDE_CODE_SESSION_ID": "owned-fresh"}
answer = subprocess.run(
    [sys.executable, "-c", sys.argv[4], sys.argv[1], "add", "pid", str(os.getpid()), "owned readiness test", sys.argv[5]],
    cwd=Path(sys.argv[3]), env=environment, capture_output=True, text=True, check=False)
print(json.dumps({"exit": answer.returncode, "stdout": answer.stdout,
    "stderr": answer.stderr}), flush=True)
sys.stdin.read()
"""
    evidence = Path(
        os.environ.get(
            "KNTNT_SESSION_CLEANUP_TEST_EVIDENCE", str(tmp_path / "evidence")
        )
    )
    evidence.mkdir(parents=True, exist_ok=True)
    probe_file = evidence / f"public-probes-{os.getpid()}.json"
    with subprocess.Popen(
        [
            sys.executable,
            "-c",
            program,
            str(SCRIPT),
            str(fresh),
            str(tmp_path),
            PROBE_DRIVER,
            str(probe_file),
        ],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    ) as child:
        folder = evidence / f"first-registration-{child.pid}"
        folder.mkdir()
        try:
            birth_probe = subprocess.run(
                ["ps", "-o", "lstart=", "-p", str(child.pid)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            birth = birth_probe.stdout.strip()
            identity = {
                "pid": child.pid,
                "pgid": os.getpgid(child.pid),
                "sid": os.getsid(child.pid),
                "birth": birth,
            }
            (folder / "identity-before.json").write_text(json.dumps(identity))
            (folder / "birth-before.stdout").write_text(birth_probe.stdout)
            assert (
                birth and identity["pgid"] == child.pid and identity["sid"] == child.pid
            )

            # Register immediately in an already existing home before the subject runs.
            registration_script = os.environ.get(
                "KNTNT_SESSION_CLEANUP_REGISTRATION_SCRIPT", str(SCRIPT)
            )
            registration = subprocess.run(
                [
                    "uv",
                    "run",
                    registration_script,
                    "add",
                    "pid",
                    str(child.pid),
                    "owned first-registration regression",
                ],
                cwd=tmp_path,
                env={**os.environ, "KNTNT_HOME": str(tmp_path)},
                capture_output=True,
                text=True,
                check=False,
            )
            (folder / "installed-registration.stdout").write_text(registration.stdout)
            (folder / "installed-registration.stderr").write_text(registration.stderr)
            assert registration.returncode == 0, registration.stderr
            registered = json.loads(registration.stdout)
            assert registered["recorded"]["started"] == birth
            assert registered["recorded"]["id"] == str(child.pid)
            registered_birth = subprocess.run(
                ["ps", "-o", "lstart=", "-p", str(child.pid)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            registered_identity = {
                "pid": child.pid,
                "pgid": os.getpgid(child.pid),
                "sid": os.getsid(child.pid),
                "birth": registered_birth.stdout.strip(),
            }
            (folder / "identity-after-installed-registration.json").write_text(
                json.dumps(registered_identity)
            )
            assert registered_identity == identity

            # Readiness has its own generous bound, independent of the tested behavior.
            assert child.stdout is not None and child.stdin is not None
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ)
                ready = bool(selector.select(timeout=20))
            assert ready, "owned process did not establish readiness"
            assert child.stdout.readline().strip() == "READY"
            (folder / "readiness.json").write_text(json.dumps({"ready": ready}))
            assert not fresh.exists()
            child.stdin.write("record\n")
            child.stdin.flush()
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ)
                answered = bool(selector.select(timeout=20))
            assert answered, "public registration did not answer after readiness"
            raw = child.stdout.readline()
            (folder / "public-response.json").write_text(raw)
            (folder / "actual-public-probes.json").write_bytes(probe_file.read_bytes())
            answer = json.loads(raw)
            assert answer["exit"] == 0, answer["stderr"]
            receipt = json.loads(answer["stdout"])
            after = subprocess.run(
                ["ps", "-o", "lstart=", "-p", str(child.pid)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            ancestry = subprocess.run(
                ["ps", "-axo", "pid=,ppid=,comm="],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            (folder / "birth-after.stdout").write_text(after.stdout)
            (folder / "ancestry.stdout").write_text(ancestry.stdout)
            manifest = Path(receipt["manifest"]).read_bytes()
            (folder / "public-manifest.jsonl").write_bytes(manifest)
            assert after.stdout.strip() == birth
            assert receipt["recorded"]["started"] == birth, (
                "fresh-home probe lost authentic birth"
            )
            header = json.loads(manifest.splitlines()[0])
            assert header["owner_pid"] == child.pid
            assert header["owner_started"] == birth
            assert header["harness"] == "claude-code"
            assert receipt["session"] == "owned-fresh"
        finally:
            # Closing the owned child's pipe ends it naturally; no signals are sent.
            output, error = child.communicate(timeout=20)
            (folder / "natural-exit.json").write_text(
                json.dumps(
                    {"exit": child.returncode, "stdout": output, "stderr": error}
                )
            )
            assert child.returncode == 0, error
            with pytest.raises(ProcessLookupError):
                os.killpg(child.pid, 0)


@pytest.mark.parametrize("birth", ["", None])
def test_public_add_reports_a_failed_birth_probe_without_recording_a_pid(
    machine: dict[str, Any], capsys: pytest.CaptureFixture[str], birth: str | None
) -> None:
    """A failed observation cannot produce a successful empty registration."""

    machine["birth"] = birth
    cleanup = _cleanup()

    status = cleanup.main(["add", "pid", str(PID), "owned test"])

    output = capsys.readouterr()
    assert status == 1
    assert output.out == ""
    assert "cannot establish the start identity" in output.err
    assert not list(cleanup.sessions_dir().glob("*.jsonl"))
    assert machine["signals"] == []


@pytest.mark.parametrize("leader_survives", [True, False])
def test_kill_does_not_claim_cleanup_while_the_target_remains(
    machine: dict[str, Any], leader_survives: bool
) -> None:
    """A delivered signal does not establish that the process group disappeared."""

    machine["after_term"] = {}
    machine["after_kill"] = {"live": leader_survives, "group_live": True}

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == [(-PID, signal.SIGTERM), (-PID, signal.SIGKILL)]
    assert result["outcome"] in {"failed", "refused"}
    assert "remain" in result["detail"]


@pytest.mark.parametrize("failure", [PermissionError, OSError])
def test_an_unreadable_leaderless_group_is_unresolved(
    machine: dict[str, Any], failure: type[OSError]
) -> None:
    """Failure to observe the group is not evidence of its absence."""

    machine.update(live=False, group_error=failure)

    result = _cleanup().stop_pid({"id": str(PID), "started": BIRTH})

    assert machine["signals"] == []
    assert result["outcome"] == "refused"


def test_unusable_state_home_reports_probe_failure_without_a_pid_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A state directory initialization failure stays fail closed."""

    unusable = tmp_path / "file-instead-of-home"
    unusable.write_text("owned fixture")
    monkeypatch.setenv("KNTNT_HOME", str(unusable))
    cleanup = _cleanup()

    result = cleanup.main(["add", "pid", str(os.getpid()), "owned fixture"])

    assert result == 1
    assert "cannot establish the start identity" in capsys.readouterr().err
    assert cleanup.process_chain() is None
    assert unusable.read_text() == "owned fixture"
