"""Lifecycle audit distinguishes empty manifests from retained cleanup history."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest

SCRIPT: Path = (
    Path(__file__).resolve().parents[1]
    / "skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)


@pytest.fixture
def cleanup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Any:
    """Use public Feature behavior with every external action intercepted."""

    spec = importlib.util.spec_from_file_location("cleanup_audit", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))

    def signal_refused(target: int, number: int) -> None:
        """No real process is a target in these audit regressions."""

        raise AssertionError(f"unexpected process signal {target}: {number}")

    def observe(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Supply complete ownerless ancestry without invoking a real runtime."""

        assert args == ["ps", "-axo", "pid=,ppid=,comm="]
        assert Path(kwargs["cwd"]).is_dir()
        return subprocess.CompletedProcess(args, 0, f"{os.getpid()} 1 python\n", "")

    monkeypatch.setattr(os, "kill", signal_refused)
    monkeypatch.setattr(subprocess, "run", observe)
    return module


@pytest.mark.parametrize("moment", ["SessionEnd", "SessionStart"])
@pytest.mark.parametrize("interrupted", [False, True])
def test_retained_consumed_history_is_not_reported_as_recorded_nothing(
    cleanup: Any,
    monkeypatch: pytest.MonkeyPatch,
    moment: str,
    interrupted: bool,
) -> None:
    """Retiring old bookkeeping must neither replay work nor deny its recording."""

    cleanup.open_session("subject", "codex", "subject")
    path = cleanup.manifest_path("subject")
    cleanup.append(path, {"kind": "container", "id": "intercepted", "why": "owned"})
    original = path.read_bytes()
    calls: list[list[str]] = []
    original_run = subprocess.run
    original_unlink = Path.unlink

    def runtime(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Observe one removal at the container command boundary only."""

        if args[0] == "/intercepted/docker":
            assert args == ["/intercepted/docker", "rm", "--force", "intercepted"]
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")
        return original_run(args, **kwargs)

    def retain(named: Path, *args: Any, **kwargs: Any) -> None:
        """Leave the real consumed history after the action has completed."""

        if named == path:
            if interrupted:
                raise RuntimeError("controlled interruption before manifest retirement")
            raise PermissionError("controlled manifest unlink failure")
        original_unlink(named, *args, **kwargs)

    monkeypatch.setattr("shutil.which", lambda name: "/intercepted/docker")
    monkeypatch.setattr(subprocess, "run", runtime)
    monkeypatch.setattr(Path, "unlink", retain)
    if interrupted:
        with pytest.raises(RuntimeError, match="controlled interruption"):
            cleanup.hook("codex", "SessionEnd", {"session_id": "subject"})
    else:
        first = cleanup.hook("codex", "SessionEnd", {"session_id": "subject"})
        assert first["swept"][0]["acted"][0]["outcome"] == "removed"
    assert path.read_bytes().startswith(original)
    assert cleanup.read_manifest(path)[1] == []
    assert len(calls) == 1
    monkeypatch.setattr(Path, "unlink", original_unlink)
    os.utime(path, (1, 1))
    session = "sweeper" if moment == "SessionStart" else "subject"

    answer = cleanup.hook("codex", moment, {"session_id": session})

    assert answer["session"] == session
    assert answer["swept"] == [{"session": "subject", "entries": 0, "acted": []}]
    assert len(calls) == 1, "retained consumption cannot authorize another removal"
    assert not path.exists()
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    assert [row["outcome"] for row in rows if row["event"] == "acted"] == ["removed"]
    assert not any(
        row["event"] == "recorded-nothing" and row["session"] == "subject"
        for row in rows
    ), "fully consumed resource history is not evidence that nothing was recorded"


@pytest.mark.parametrize("moment", ["SessionEnd", "SessionStart"])
def test_genuinely_empty_history_keeps_its_subject_and_sweeper_audit(
    cleanup: Any, moment: str
) -> None:
    """The empty audit remains attributable to the subject rather than its sweeper."""

    cleanup.open_session("empty", "codex", "empty")
    path = cleanup.manifest_path("empty")
    os.utime(path, (1, 1))
    session = "sweeper" if moment == "SessionStart" else "empty"

    answer = cleanup.hook("codex", moment, {"session_id": session})

    assert answer["swept"] == [{"session": "empty", "entries": 0, "acted": []}]
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    empty = [row for row in rows if row["event"] == "recorded-nothing"]
    assert len(empty) == 1
    assert empty[0]["session"] == "empty"
    assert empty[0]["harness"] == "codex"
    assert empty[0]["why"] == ("start" if moment == "SessionStart" else "end")
    assert empty[0]["sweeper_session"] == (session if moment == "SessionStart" else "")
    assert empty[0]["sweeper_harness"] == ("codex" if moment == "SessionStart" else "")
    assert not path.exists()


@pytest.mark.parametrize("moment", ["SessionEnd", "SessionStart"])
@pytest.mark.parametrize("failure", ["permission", "encoding", "partial"])
def test_unreadable_history_is_retained_without_an_invented_empty_audit(
    cleanup: Any,
    monkeypatch: pytest.MonkeyPatch,
    moment: str,
    failure: str,
) -> None:
    """Missing read evidence cannot establish that no resource was recorded."""

    cleanup.open_session("unknown", "codex", "unknown")
    path = cleanup.manifest_path("unknown")
    cleanup.append(path, {"kind": "container", "id": "intercepted", "why": "owned"})
    if failure == "partial":
        header = path.read_bytes().splitlines()[0]
        path.write_bytes(header + b'\n{"kind":"container","id":')
    original = path.read_bytes()
    os.utime(path, (1, 1))
    original_read = Path.read_text
    original_run = subprocess.run
    calls: list[list[str]] = []

    def unreadable(named: Path, *args: Any, **kwargs: Any) -> str:
        """Fail only the subject manifest's observation at the file boundary."""

        if named == path and failure != "partial":
            if failure == "permission":
                raise PermissionError("controlled manifest read failure")
            raise UnicodeDecodeError(
                "utf-8", b"\xff", 0, 1, "controlled invalid encoding"
            )
        return original_read(named, *args, **kwargs)

    def runtime(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        """Intercept removal if the recorded work becomes readable later."""

        if args[0] == "/intercepted/docker":
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")
        return original_run(args, **kwargs)

    monkeypatch.setattr(Path, "read_text", unreadable)
    monkeypatch.setattr("shutil.which", lambda name: "/intercepted/docker")
    monkeypatch.setattr(subprocess, "run", runtime)
    session = "sweeper" if moment == "SessionStart" else "unknown"

    answer = cleanup.hook("codex", moment, {"session_id": session})

    assert path.exists(), "an unreadable registry is not completed cleanup"
    assert path.read_bytes() == original
    assert path.stat().st_mtime_ns == 1_000_000_000
    assert calls == []
    assert answer["session"] == session
    assert answer["swept"] == [{"session": "unknown", "entries": None, "acted": []}]
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    assert not any(row["event"] == "recorded-nothing" for row in rows)
    kept = [row for row in rows if row["event"] == "manifest-kept"]
    assert len(kept) == 1
    assert kept[0]["session"] == "unknown"
    assert kept[0]["why"] == ("start" if moment == "SessionStart" else "end")
    assert kept[0]["sweeper_session"] == (session if moment == "SessionStart" else "")
    assert kept[0]["sweeper_harness"] == ("codex" if moment == "SessionStart" else "")
    assert kept[0]["detail"]

    # A transient observation failure leaves the authentic work retryable.
    if failure != "partial":
        monkeypatch.setattr(Path, "read_text", original_read)
        recovered = cleanup.hook("codex", "SessionEnd", {"session_id": "unknown"})
        assert recovered["swept"][0]["acted"][0]["outcome"] == "removed"
        assert len(calls) == 1
        assert not path.exists()


@pytest.mark.parametrize("moment", ["SessionEnd", "SessionStart"])
def test_a_missing_read_cannot_deny_the_selected_manifest_history(
    cleanup: Any, monkeypatch: pytest.MonkeyPatch, moment: str
) -> None:
    """A failed selected-file read is uncertainty even when it reports absence."""

    cleanup.open_session("unobserved", "codex", "unobserved")
    path = cleanup.manifest_path("unobserved")
    cleanup.append(path, {"kind": "container", "id": "intercepted", "why": "owned"})
    original = path.read_bytes()
    os.utime(path, (1, 1))
    original_read = Path.read_text

    def vanished_read(named: Path, *args: Any, **kwargs: Any) -> str:
        """Fail the selected observation without authorizing real resource work."""

        if named == path:
            raise FileNotFoundError("controlled selected manifest read absence")
        return original_read(named, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", vanished_read)
    session = "sweeper" if moment == "SessionStart" else "unobserved"

    answer = cleanup.hook("codex", moment, {"session_id": session})

    assert path.exists(), "a failed absence read cannot retire resource history"
    assert path.read_bytes() == original
    assert path.stat().st_mtime_ns == 1_000_000_000
    assert answer["swept"] == [{"session": "unobserved", "entries": None, "acted": []}]
    rows = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    assert not any(row["event"] == "recorded-nothing" for row in rows)
    assert any(
        row["event"] == "manifest-kept" and row["session"] == "unobserved"
        for row in rows
    )
