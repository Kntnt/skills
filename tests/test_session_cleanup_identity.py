"""Process cleanup refuses signals unless the recorded OS identity still holds."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import selectors
import signal
import subprocess
import sys
import threading
import time
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


@pytest.mark.parametrize(
    "observation",
    [
        "valid",
        "missing-link",
        "malformed",
        "nonzero",
        "os-error",
        "timeout",
    ],
)
def test_public_registration_uses_only_a_complete_nearest_owner_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    observation: str,
) -> None:
    """Valid nearest ownership survives while incomplete observations stay unknown."""

    cleanup = _cleanup()
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    monkeypatch.setenv("CLAUDE_PID", "41")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "outer")
    monkeypatch.setenv("CODEX_SESSION_ID", "nearest")

    def observe(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Model valid and unusable ps results at the OS command boundary."""

        assert Path(kwargs["cwd"]).is_dir()
        if "-axo" not in args:
            return subprocess.CompletedProcess(args, 0, BIRTH, "")
        if observation == "os-error":
            raise OSError("ps unavailable")
        if observation == "timeout":
            raise subprocess.TimeoutExpired(args, 5)
        table = f"{os.getpid()} 42 python\n42 41 codex\n41 1 claude\n"
        if observation == "missing-link":
            table = f"{os.getpid()} 42 python\n"
        if observation == "malformed":
            table = "not a process table\n"
        return subprocess.CompletedProcess(
            args, int(observation == "nonzero"), table, ""
        )

    monkeypatch.setattr(subprocess, "run", observe)

    receipt = cleanup.add("container", "never-invoked", "owned parser fixture")

    header, entries = cleanup.read_manifest(Path(receipt["manifest"]))
    assert len(entries) == 1
    if observation == "valid":
        assert receipt["session"] == "nearest"
        assert header["harness"] == "codex"
        assert header["owner_pid"] == 42
        assert header["owner_started"] == BIRTH
    else:
        assert receipt["session"].startswith("unowned-")
        assert header["owner_pid"] == 0
        assert header["owner_started"] == ""


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

            # Register in an existing home before the subject runs.
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

            # Readiness has a separate generous bound.
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
            # Closing the owned pipe ends the child naturally, without signals.
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


@pytest.mark.parametrize("recorded", ["", BIRTH])
def test_mixed_manifest_retries_only_unresolved_process_work(
    machine: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    recorded: str,
) -> None:
    """Completed removals cannot authorize deleting a replacement at that name."""

    cleanup = _cleanup()
    machine["birth"] = ""
    scratch = tmp_path / "owned-replacement"
    scratch.mkdir()
    path = cleanup.manifest_path("mixed")
    cleanup.append(path, {"kind": "session", "id": "mixed"})
    cleanup.append(
        path,
        {
            "kind": "pid",
            "id": str(PID),
            "started": recorded,
            "why": "owned pid",
        },
    )
    cleanup.append(path, {"kind": "path", "id": str(scratch), "why": "owned path"})
    cleanup.append(
        path,
        {
            "kind": "container",
            "id": "owned-intercepted",
            "why": "owned container",
        },
    )
    with path.open("a") as handle:
        handle.write('not-json\n[]\n{"kind":"unknown"}\n')
    original = path.read_bytes()
    process_probe = subprocess.run
    removals: list[list[str]] = []

    def external(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Intercept the container runtime while retaining modeled ps probes."""

        if args[0] == "/intercepted/docker":
            assert args == ["/intercepted/docker", "rm", "--force", "owned-intercepted"]
            removals.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")
        return process_probe(args, **kwargs)

    monkeypatch.setattr("shutil.which", lambda name: "/intercepted/docker")
    monkeypatch.setattr(subprocess, "run", external)

    first = cleanup.hook("codex", "SessionEnd", {"session_id": "mixed"})
    assert first["swept"][0]["entries"] == 3
    assert [row["outcome"] for row in first["swept"][0]["acted"]] == [
        "refused",
        "deleted",
        "removed",
    ]
    assert not scratch.exists()
    assert path.read_bytes().startswith(original), "retain original raw evidence"
    scratch.mkdir()
    (scratch / "replacement").write_text("new owned resource")
    os.utime(path, (1, 1))

    second = cleanup.hook("codex", "SessionStart", {"session_id": "next"})

    assert (scratch / "replacement").exists(), "retry deleted a replacement resource"
    assert len(removals) == 1, "retry re-authorized a completed container removal"
    assert second["swept"] == [
        {
            "session": "mixed",
            "entries": 1,
            "acted": [
                {
                    "kind": "pid",
                    "id": str(PID),
                    "outcome": "refused",
                    "detail": (
                        "the current start identity is unreadable"
                        if recorded
                        else "the recorded start identity is missing"
                    ),
                }
            ],
        }
    ]
    assert cleanup.read_manifest(path)[1] == [
        {
            "kind": "pid",
            "id": str(PID),
            "started": recorded,
            "why": "owned pid",
        }
    ]
    assert path.read_bytes().startswith(original)
    assert machine["signals"] == []
    if recorded:
        machine["birth"] = BIRTH
    else:
        machine.update(live=False, group_live=False)

    third = cleanup.hook("codex", "SessionEnd", {"session_id": "mixed"})

    assert third["swept"][0]["acted"][0]["outcome"] == (
        "stopped" if recorded else "gone"
    )
    assert not path.exists()
    assert (scratch / "replacement").read_text() == "new owned resource"
    assert len(removals) == 1
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    acted = [row for row in rows if row["event"] == "acted"]
    assert [row["kind"] for row in acted] == ["pid", "path", "container", "pid", "pid"]
    assert acted[3]["sweeper_session"] == "next"
    assert acted[3]["sweeper_harness"] == "codex"
    assert acted[3]["why"] == "start"
    assert sum(row["event"] == "manifest-kept" for row in rows) == 2


def test_an_interrupted_manifest_tail_cannot_reactivate_a_completed_removal(
    machine: dict[str, Any],
    tmp_path: Path,
) -> None:
    """A partial last line cannot swallow the record consuming an old name."""

    cleanup = _cleanup()
    path = cleanup.manifest_path("interrupted")
    scratch = tmp_path / "interrupted-owned-path"
    scratch.mkdir()
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": ""})
    cleanup.append(path, {"kind": "path", "id": str(scratch)})
    with path.open("a") as handle:
        handle.write('{"interrupted":')

    cleanup.sweep(path, why="end")
    assert not scratch.exists()
    scratch.mkdir()
    retry = cleanup.sweep(path, why="end")

    assert scratch.exists(), "an interrupted tail hid the consumed authorization"
    assert [row["kind"] for row in retry["acted"]] == ["pid"]


@pytest.mark.parametrize("self_cycle", [True, False])
def test_cyclic_ancestry_cannot_identify_an_owner_or_authorize_start_cleanup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    self_cycle: bool,
) -> None:
    """A usable-looking prefix cannot establish ownership of a cyclic chain."""

    cleanup = _cleanup()
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    pid = os.getpid()
    table = (
        f"{pid} {pid} codex\n" if self_cycle else f"{pid} 42 python\n42 {pid} codex\n"
    )

    def observe(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Supply a contradictory OS ancestry without touching any process."""

        return subprocess.CompletedProcess(
            args, 0, table if "-axo" in args else BIRTH, ""
        )

    monkeypatch.setattr(subprocess, "run", observe)
    old = cleanup.manifest_path("old")
    scratch = tmp_path / "cycle-protected"
    scratch.mkdir()
    cleanup.append(old, {"kind": "path", "id": str(scratch)})
    original = old.read_bytes()
    os.utime(old, (1, 1))

    answer = cleanup.hook("codex", "SessionStart", {"session_id": "new"})

    assert answer["swept"] == [], "a cycle must make the start observation unusable"
    assert scratch.exists()
    assert old.read_bytes() == original
    assert cleanup.session_owner() == ("", 0, "")
    header, _ = cleanup.read_manifest(cleanup.manifest_path("new"))
    assert header["owner_pid"] == 0
    assert header["owner_started"] == ""


def test_a_ready_authenticated_owned_group_is_stopped_by_feature_term(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Observe authentic Feature TERM, parent reaping, and group disappearance."""

    cleanup = _cleanup()
    selected = tmp_path / "feature-state"
    lifecycle = tmp_path / "installed-state"
    selected.mkdir()
    lifecycle.mkdir()
    monkeypatch.setenv("KNTNT_HOME", str(selected))
    monkeypatch.setenv("CLAUDE_PID", str(os.getpid()))
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "owned-feature-term")
    evidence = Path(
        os.environ.get(
            "KNTNT_SESSION_CLEANUP_TEST_EVIDENCE",
            str(tmp_path / "evidence"),
        )
    )
    evidence.mkdir(parents=True, exist_ok=True)
    program = """
import signal, sys
def terminated(number, frame):
    print("FEATURE TERM RECEIVED", flush=True)
    raise SystemExit(0)
signal.signal(signal.SIGTERM, terminated)
print("READY", flush=True)
assert sys.stdin.readline() == "GO\\n"
print("ACTIVE", flush=True)
while True:
    signal.pause()
"""
    original_kill = os.kill

    def identity(pid: int) -> dict[str, Any]:
        """Observe real birth and scope without reconstructing any registry field."""

        observed = subprocess.run(
            ["ps", "-o", "lstart=", "-p", str(pid)],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "pid": pid,
            "pgid": os.getpgid(pid),
            "sid": os.getsid(pid),
            "birth": observed.stdout.strip() if observed.returncode == 0 else "",
            "argv": observed.args,
            "stdout": observed.stdout,
            "stderr": observed.stderr,
            "exit": observed.returncode,
            "at": time.time(),
        }

    def same(left: dict[str, Any], right: dict[str, Any]) -> bool:
        """Require a contemporaneous nonempty match of all identity coordinates."""

        return bool(left["birth"]) and all(
            left[key] == right[key] for key in ("pid", "pgid", "sid", "birth")
        )

    with subprocess.Popen(
        [sys.executable, "-c", program],
        cwd=tmp_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    ) as child:
        folder = evidence / f"feature-term-{child.pid}"
        folder.mkdir()
        signals: list[dict[str, Any]] = []
        reaper: threading.Thread | None = None
        authenticated: dict[str, Any] | None = None
        try:
            before = identity(child.pid)
            (folder / "identity-before.json").write_text(json.dumps(before, indent=2))
            assert before["birth"] and before["pgid"] == before["sid"] == child.pid
            argv = [
                "uv",
                "run",
                os.environ.get(
                    "KNTNT_SESSION_CLEANUP_REGISTRATION_SCRIPT",
                    str(SCRIPT),
                ),
                "add",
                "pid",
                str(child.pid),
                "owned Feature TERM regression",
            ]
            started = time.time()
            installed = subprocess.run(
                argv,
                cwd=tmp_path,
                env={**os.environ, "KNTNT_HOME": str(lifecycle)},
                capture_output=True,
                text=True,
                check=False,
            )
            (folder / "installed-registration.stdout").write_text(installed.stdout)
            (folder / "installed-registration.stderr").write_text(installed.stderr)
            (folder / "installed-command.json").write_text(
                json.dumps(
                    {
                        "argv": argv,
                        "cwd": str(tmp_path),
                        "start": started,
                        "end": time.time(),
                        "exit": installed.returncode,
                        "selected_state_preexisted": lifecycle.is_dir(),
                    },
                    indent=2,
                )
            )
            assert installed.returncode == 0, installed.stderr
            registered = json.loads(installed.stdout)
            after = identity(child.pid)
            (folder / "identity-after.json").write_text(json.dumps(after, indent=2))
            manifest = Path(registered["manifest"]).read_bytes()
            (folder / "installed-manifest.jsonl").write_bytes(manifest)
            owner = identity(os.getpid())
            headers = [
                json.loads(line)
                for line in manifest.splitlines()
                if json.loads(line).get("kind") == "session"
            ]
            assert same(before, after)
            assert registered["recorded"]["kind"] == "pid"
            assert registered["recorded"]["id"] == str(child.pid)
            assert registered["recorded"]["started"] == before["birth"]
            assert headers[-1]["owner_pid"] == os.getpid()
            assert headers[-1]["owner_started"] == owner["birth"]
            authenticated = before
            ancestry = subprocess.run(
                ["ps", "-axo", "pid=,ppid=,comm="],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            (folder / "ancestry.stdout").write_text(ancestry.stdout)
            (folder / "owner.json").write_text(json.dumps(owner, indent=2))

            # Readiness and active execution precede the subject's deadline.
            assert child.stdout is not None and child.stdin is not None
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ)
                ready = bool(selector.select(timeout=20))
            assert ready, "owned Feature-stop child did not become ready"
            assert child.stdout.readline() == "READY\n"
            child.stdin.write("GO\n")
            child.stdin.flush()
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ)
                active = bool(selector.select(timeout=20))
            assert active, "authenticated child did not enter its signal wait"
            assert child.stdout.readline() == "ACTIVE\n"
            (folder / "readiness.json").write_text(
                json.dumps({"ready": ready, "active": active})
            )
            receipt = cleanup.add("pid", str(child.pid), "owned Feature TERM")
            (folder / "public-registration.json").write_text(
                json.dumps(receipt, indent=2)
            )
            (folder / "public-manifest.jsonl").write_bytes(
                Path(receipt["manifest"]).read_bytes()
            )
            assert receipt["recorded"]["started"] == before["birth"]
            assert receipt["session"] == "owned-feature-term"

            def signal_owned(target: int, number: int) -> None:
                """Authenticate immediately before each real destructive signal."""

                assert target in {child.pid, -child.pid}
                if number:
                    current = identity(child.pid)
                    assert same(before, current), "refuse unresolved or reused target"
                    signals.append(
                        {"target": target, "signal": number, "identity": current}
                    )
                    (folder / "signals.json").write_text(json.dumps(signals, indent=2))
                original_kill(target, number)

            monkeypatch.setattr(os, "kill", signal_owned)
            reaper = threading.Thread(target=child.wait, kwargs={"timeout": 20})
            reaper.start()

            result = cleanup.sweep(Path(receipt["manifest"]), why="end")

            (folder / "feature-result.json").write_text(json.dumps(result, indent=2))
            reaper.join(timeout=20)
            assert not reaper.is_alive(), "owned child was not reaped"
            output, error = child.communicate(timeout=20)
            (folder / "exit.json").write_text(
                json.dumps(
                    {
                        "exit": child.returncode,
                        "stdout": output,
                        "stderr": error,
                    },
                    indent=2,
                )
            )
            assert [row["signal"] for row in signals] == [signal.SIGTERM]
            assert signals[0]["target"] == -child.pid
            assert "FEATURE TERM RECEIVED" in output
            assert child.returncode == 0
            assert result["acted"][0]["outcome"] == "stopped"
            assert result["acted"][0]["detail"] == "group"
            assert not Path(receipt["manifest"]).exists()
        finally:
            monkeypatch.setattr(os, "kill", original_kill)
            if child.poll() is None:
                if authenticated is None:
                    assert child.stdin is not None
                    child.stdin.close()
                    child.stdin = None
                else:
                    current = identity(child.pid)
                    assert same(authenticated, current), "cleanup identity unresolved"
                    original_kill(-child.pid, signal.SIGTERM)
                child.wait(timeout=20)
            if reaper is not None:
                reaper.join(timeout=20)
            with pytest.raises(ProcessLookupError):
                original_kill(-child.pid, 0)
            (folder / "group-absent.json").write_text(
                json.dumps({"pgid": child.pid, "absent": True})
            )


def test_overlapping_sweeps_cannot_repeat_a_named_container_removal(
    machine: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A second sweep must observe consumption before it can authorize work."""

    cleanup = _cleanup()
    path = cleanup.manifest_path("overlap")
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": ""})
    cleanup.append(path, {"kind": "container", "id": "owned-intercepted"})
    original_open = Path.open
    original_read = Path.read_text
    original_probe = subprocess.run
    pending_write = threading.Event()
    release = threading.Event()
    second_started = threading.Event()
    second_read = threading.Event()
    removals: list[list[str]] = []
    failures: list[Exception] = []

    def opening(named: Path, *args: Any, **kwargs: Any) -> Any:
        """Hold the first consumption at the file boundary until contention."""

        if named == path and args and args[0] == "a" and not pending_write.is_set():
            pending_write.set()
            assert release.wait(timeout=20), (
                "controlled manifest write was not released"
            )
        return original_open(named, *args, **kwargs)

    def reading(named: Path, *args: Any, **kwargs: Any) -> str:
        """Observe whether the concurrent reader entered before consumption."""

        if named == path and threading.current_thread().name == "second-sweep":
            second_read.set()
        return original_read(named, *args, **kwargs)

    def external(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Deliver no container call beyond the OS boundary interception."""

        if args[0] == "/intercepted/docker":
            removals.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")
        return original_probe(args, **kwargs)

    def run_sweep() -> None:
        """Retain worker failures while asserting readiness independently."""

        if threading.current_thread().name == "second-sweep":
            second_started.set()
        try:
            cleanup.sweep(path, why="end")
        except Exception as error:  # noqa: BLE001 - relay thread failures to the test
            failures.append(error)

    monkeypatch.setattr(Path, "open", opening)
    monkeypatch.setattr(Path, "read_text", reading)
    monkeypatch.setattr("shutil.which", lambda name: "/intercepted/docker")
    monkeypatch.setattr(subprocess, "run", external)
    first = threading.Thread(target=run_sweep, name="first-sweep")
    second = threading.Thread(target=run_sweep, name="second-sweep")
    first.start()
    try:
        assert pending_write.wait(timeout=20), "first sweep did not reach the write"
        second.start()
        assert second_started.wait(timeout=20), "second sweep did not start"
        second_read.wait(timeout=1)
    finally:
        release.set()
        first.join(timeout=20)
        if second.ident is not None:
            second.join(timeout=20)
    assert not first.is_alive() and not second.is_alive()
    assert failures == []
    assert len(removals) == 1, "overlapping sweeps re-authorized the same name"
    assert machine["signals"] == []


def test_a_completed_pid_action_is_logged_even_if_consumption_cannot_be_written(
    machine: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A registry write failure cannot hide the action that already happened."""

    cleanup = _cleanup()
    path = cleanup.manifest_path("write-failure")
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": BIRTH})
    original = path.read_bytes()
    original_open = Path.open

    def opening(named: Path, *args: Any, **kwargs: Any) -> Any:
        """Fail only the actual manifest append at the file boundary."""

        if named == path and args and args[0] == "a":
            raise PermissionError("controlled manifest append refusal")
        return original_open(named, *args, **kwargs)

    monkeypatch.setattr(Path, "open", opening)
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"session_id":"write-failure"}'))

    status = cleanup.main(["hook", "--harness=codex", "--event=SessionEnd"])

    assert status == 0
    assert capsys.readouterr() == ("", "")
    assert machine["signals"] == [(-PID, signal.SIGTERM)]
    assert path.read_bytes() == original
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    assert any(row["event"] == "acted" and row["outcome"] == "stopped" for row in rows)
    assert any(row["event"] == "hook-failed" for row in rows)


def test_a_later_explicit_registration_authorizes_only_its_own_removal(
    machine: dict[str, Any],
    tmp_path: Path,
) -> None:
    """Identical values in a new line are new authority, not old replay."""

    cleanup = _cleanup()
    path = cleanup.manifest_path(cleanup.current_key())
    scratch = tmp_path / "registered-again"
    scratch.mkdir()
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": ""})
    cleanup.add("path", str(scratch), "owned replacement")
    cleanup.add("path", str(scratch), "owned replacement")

    first = cleanup.sweep(path, why="end")
    assert [row["outcome"] for row in first["acted"]] == ["refused", "deleted", "gone"]
    scratch.mkdir()
    cleanup.add("path", str(scratch), "owned replacement")
    second = cleanup.sweep(path, why="end")

    assert [row["outcome"] for row in second["acted"]] == ["refused", "deleted"]
    scratch.mkdir()
    third = cleanup.sweep(path, why="end")
    assert [row["kind"] for row in third["acted"]] == ["pid"]
    assert scratch.exists()
    assert machine["signals"] == []


@pytest.mark.parametrize("available", [True, False])
def test_failed_or_unavailable_container_attempts_do_not_become_retry_authority(
    machine: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    available: bool,
) -> None:
    """An unresolved PID cannot change the previous single-attempt contract."""

    cleanup = _cleanup()
    path = cleanup.manifest_path("container-failure")
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": ""})
    cleanup.append(path, {"kind": "container", "id": "never-invoked"})
    original_probe = subprocess.run
    calls: list[list[str]] = []

    def external(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Intercept even unsuccessful runtime invocations."""

        if args[0] == "/intercepted/docker":
            calls.append(args)
            return subprocess.CompletedProcess(args, 1, "", "controlled failure")
        return original_probe(args, **kwargs)

    monkeypatch.setattr(
        "shutil.which", lambda name: "/intercepted/docker" if available else None
    )
    monkeypatch.setattr(subprocess, "run", external)

    first = cleanup.sweep(path, why="end")
    second = cleanup.sweep(path, why="end")

    assert first["acted"][1]["outcome"] == ("failed" if available else "unavailable")
    assert [row["kind"] for row in second["acted"]] == ["pid"]
    assert len(calls) == int(available)
    assert machine["signals"] == []


def test_an_unwritable_consumption_record_prevents_name_based_removal(
    machine: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A failed consumption write retains the old obligation without acting."""

    cleanup = _cleanup()
    path = cleanup.manifest_path("no-write")
    scratch = tmp_path / "write-protected-removal"
    scratch.mkdir()
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": ""})
    cleanup.append(path, {"kind": "path", "id": str(scratch)})
    original = path.read_bytes()
    original_open = Path.open

    def opening(named: Path, *args: Any, **kwargs: Any) -> Any:
        """Refuse only the pending manifest's consumption append."""

        if named == path and args and args[0] == "a":
            raise PermissionError("controlled consumption refusal")
        return original_open(named, *args, **kwargs)

    monkeypatch.setattr(Path, "open", opening)
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"session_id":"no-write"}'))

    assert cleanup.main(["hook", "--event=SessionEnd"]) == 0

    assert scratch.exists()
    assert path.read_bytes() == original
    assert machine["signals"] == []


def test_consumption_preserves_unknown_owner_age_but_new_work_refreshes_it(
    machine: dict[str, Any],
    tmp_path: Path,
) -> None:
    """Cleanup bookkeeping is not new owner activity under the age backstop."""

    cleanup = _cleanup()
    path = cleanup.manifest_path(cleanup.current_key())
    scratch = tmp_path / "age-owned-scratch"
    scratch.mkdir()
    cleanup.append(path, {"kind": "pid", "id": str(PID), "started": ""})
    cleanup.add("path", str(scratch), "owned age fixture")
    os.utime(path, (1, 1))

    cleanup.sweep(path, why="start")

    assert path in cleanup.foreign_manifests("next"), "consumption reset orphan age"
    assert path.stat().st_mtime_ns == 1_000_000_000
    scratch.mkdir()
    cleanup.add("path", str(scratch), "new owner activity")
    assert path not in cleanup.foreign_manifests("next")
    assert machine["signals"] == []
