"""Capture the isolated native startup attempt without changing user state."""

from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
PACKET = REPO / "docs/evaluation/regressions/390"
ROOT = REPO / ".scratch-390/native-recorded"
OUTPUT = PACKET / "runs/recorded-column"


def inventory() -> dict[str, str]:
    """Hash staged work and scratch; authentication bytes never enter evidence."""
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for area in (ROOT / "work", ROOT / "tmp")
        for path in sorted(area.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    """Bound startup and reap its process group before recording the outcome."""

    # Set actual runtime locations to confine all child state to owned paths.
    environment = dict(os.environ)
    for name in ("CODEX_THREAD_ID", "CODEX_SESSION_ID"):
        environment.pop(name, None)
    environment.update(
        HOME=str(ROOT / "home"),
        CODEX_HOME=str(ROOT / "home/.codex"),
        TMPDIR=str(ROOT / "tmp"),
        UV_CACHE_DIR=str(REPO / ".scratch-390/uv-cache"),
        XDG_CACHE_HOME=str(ROOT / "home/cache"),
        XDG_DATA_HOME=str(ROOT / "home/data"),
    )
    command = [
        "/opt/homebrew/bin/codex",
        "exec",
        "--ignore-rules",
        "-s",
        "workspace-write",
        "--skip-git-repo-check",
        "--json",
        "-C",
        str(ROOT / "work"),
        "--add-dir",
        str(ROOT / "tmp"),
        "-o",
        str(OUTPUT / "response.txt"),
        "-",
    ]
    (OUTPUT / "before.json").write_text(json.dumps(inventory(), indent=2) + "\n")
    (OUTPUT / "invocation.txt").write_text(
        (PACKET / "tasks/recorded-column.txt").read_text()
    )
    started = time.monotonic()

    # Capture streams directly so the complete native record survives a timeout.
    with (
        (OUTPUT / "events.jsonl").open("w") as stdout,
        (OUTPUT / "stderr.txt").open("w") as stderr,
    ):
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr,
            text=True,
            cwd=ROOT / "work",
            env=environment,
            start_new_session=True,
        )
        record = {
            "argv": command,
            "pid": process.pid,
            "process_group": process.pid,
            "harness": "codex-cli 0.155.1",
            "model": "gpt-5.6-sol",
            "effort": "xhigh",
            "timeout_seconds": 45,
            "registration": "local ledger; user confines writes to this worktree",
        }
        (OUTPUT / "process.json").write_text(json.dumps(record, indent=2) + "\n")
        try:
            process.communicate((OUTPUT / "invocation.txt").read_text(), timeout=45)
            record["timed_out"] = False
        except subprocess.TimeoutExpired:
            record["timed_out"] = True
        finally:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()

    record.update(exit_status=process.returncode, elapsed=time.monotonic() - started)
    (OUTPUT / "process.json").write_text(json.dumps(record, indent=2) + "\n")
    (OUTPUT / "after.json").write_text(json.dumps(inventory(), indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
