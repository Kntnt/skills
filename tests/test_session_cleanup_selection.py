"""A transient selection read cannot authorize live-session resource cleanup."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)


@pytest.mark.parametrize("protection", ["owner", "ancestor"])
def test_start_retains_live_manifest_when_selection_read_fails_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, protection: str
) -> None:
    """Recovered resource data cannot bypass genuine live-identity protection."""

    # Load the actual hook without the audit fixture's synthetic OS probes.
    spec = importlib.util.spec_from_file_location("cleanup_selection", SCRIPT)
    assert spec and spec.loader
    cleanup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cleanup)
    selected_home = tmp_path / "selected-home"
    selected_home.mkdir()
    monkeypatch.setenv("KNTNT_HOME", str(selected_home))

    # Observe a real live identity independently of the production birth reader.
    pid = os.getpid() if protection == "owner" else os.getppid()
    assert pid > 1, "setup requires a live non-init identity"
    observed = subprocess.run(
        ["ps", "-p", str(pid), "-o", "lstart="],
        cwd=selected_home,
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )
    birth = observed.stdout.strip()
    assert observed.returncode == 0 and birth, "independent birth setup failed"
    os.kill(pid, 0)
    ancestors = cleanup.process_ancestors()
    assert ancestors is not None, "setup requires a complete actual process chain"
    if protection == "ancestor":
        assert pid in ancestors, "the recorded process must be a genuine ancestor"

    # The synthetic header is fixture data, never an authentic Harness receipt.
    path = cleanup.manifest_path("live-subject")
    path.parent.mkdir(parents=True)
    scratch = tmp_path / "recorded-scratch.txt"
    scratch.write_text("fixture resource must survive", encoding="utf-8")
    header: dict[str, Any] = {"kind": "session", "id": "live-subject"}
    if protection == "owner":
        header.update(owner_pid=pid, owner_started=birth)
    entries: list[dict[str, Any]] = [
        {"kind": "path", "id": str(scratch), "why": "fixture scratch"},
        {"kind": "container", "id": "fixture-not-a-real-container", "why": "fixture"},
    ]
    if protection == "ancestor":
        entries.append(
            {"kind": "pid", "id": str(pid), "started": birth, "why": "fixture ancestor"}
        )
    original = "".join(
        json.dumps(row, sort_keys=True) + "\n" for row in [header, *entries]
    ).encode()
    path.write_bytes(original)
    now = time.time()
    old = now - (cleanup.STALE_HOURS + 1) * 3600
    os.utime(path, (old, old))
    original_mtime = path.stat().st_mtime_ns
    assert now - path.stat().st_mtime > cleanup.STALE_HOURS * 3600
    assert path not in cleanup.foreign_manifests("readable-control")

    # Deny exactly the selection's first read; leave stat and recovery genuine.
    original_read = Path.read_text
    read_events: list[str] = []
    action_calls: list[dict[str, Any]] = []

    def read_once(named: Path, *args: Any, **kwargs: Any) -> str:
        """Only this manifest's first observation fails; later reads delegate."""

        if named == path and not read_events:
            read_events.append("PermissionError")
            raise PermissionError("controlled first selection read failure")
        text = original_read(named, *args, **kwargs)
        if named == path:
            read_events.append("success")
        return text

    def intercepted(entry: dict[str, Any]) -> dict[str, Any]:
        """Observe the action boundary without signaling or deleting anything."""

        action_calls.append(dict(entry))
        return {"outcome": "refused", "detail": "fixture action interception"}

    monkeypatch.setattr(Path, "read_text", read_once)
    for kind in cleanup.KINDS:
        monkeypatch.setitem(cleanup.ACTIONS, kind, intercepted)

    answer = cleanup.hook("codex", "SessionStart", {"session_id": "fresh-sweeper"})

    # Keep the actual failing sequence visible before the primary assertion.
    print(
        json.dumps(
            {
                "protection": protection,
                "pid": pid,
                "independent_birth": birth,
                "independent_ps_stdout": observed.stdout,
                "read_events_during_hook": list(read_events),
                "action_calls": action_calls,
                "hook_result": answer,
                "manifest_exists_after_hook": path.exists(),
            },
            sort_keys=True,
        )
    )
    assert action_calls == [], "selection read uncertainty authorized live resources"
    assert path.exists(), "live resource history must remain retryable"
    assert path.read_bytes() == original
    assert path.stat().st_mtime_ns == original_mtime
    assert scratch.read_bytes() == b"fixture resource must survive"
    assert not any(
        row["session"] == "live-subject" and row["acted"] for row in answer["swept"]
    )
    assert read_once(path, encoding="utf-8").encode() == original
    assert read_events.count("PermissionError") == 1 and "success" in read_events
