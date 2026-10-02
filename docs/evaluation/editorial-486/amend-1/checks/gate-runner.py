# /// script
# requires-python = ">=3.12"
# ///
"""Run the unchanged contributing gate and retain its exact commands and results."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

REPOSITORY = Path("/Users/thomas/Projects/skills/.git/kntnt-orchestrate/486")
RUNTIME = Path("/private/tmp/kntnt-orchestrate-20261002.o7bmMK/role-70ef836a/amend-1")
OUTPUT = REPOSITORY / "docs/evaluation/editorial-486/amend-1/checks"


def register(kind: str, identifier: str) -> None:
    """Keep process ownership in the assigned physical scratch root."""
    with (RUNTIME / "resources.jsonl").open("a") as ledger:
        ledger.write(json.dumps({"kind": kind, "identifier": identifier}) + "\n")


def main() -> None:
    """Wait for all four commands, even if an earlier command reports failure."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    register("pid", str(os.getpid()))
    commands = json.loads((RUNTIME / "gate-commands.json").read_text())
    environment = {
        **os.environ,
        "TMPDIR": str(RUNTIME / "tmp"),
        "UV_CACHE_DIR": str(RUNTIME / "cache"),
        "UV_TOOL_DIR": str(RUNTIME / "tools"),
        "UV_PYTHON_INSTALL_DIR": str(RUNTIME / "data/uv/python"),
        "XDG_CACHE_HOME": str(RUNTIME / "cache"),
        "XDG_DATA_HOME": str(RUNTIME / "data"),
        "RUFF_CACHE_DIR": str(RUNTIME / "ruff-cache"),
        "MYPY_CACHE_DIR": str(RUNTIME / "mypy-cache"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "UV_NO_PROGRESS": "1",
    }
    rows = []
    for number, command in enumerate(commands, 1):
        started = time.time()
        with (OUTPUT / f"gate-{number}.log").open("w") as log:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=REPOSITORY,
                env=environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            register("pid", str(process.pid))
            code = process.wait()
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        rows.append(
            {
                "command": command,
                "returncode": code,
                "started": started,
                "ended": time.time(),
                "pid": process.pid,
            }
        )
        (OUTPUT / "gate-results.json").write_text(
            json.dumps(
                {
                    "commands": rows,
                    "complete": len(rows) == 4,
                    "home_preserved": environment.get("HOME") == os.environ.get("HOME"),
                    "codex_home_preserved": environment.get("CODEX_HOME")
                    == os.environ.get("CODEX_HOME"),
                },
                indent=2,
            )
            + "\n"
        )
        print(f"Gate {number}: exit {code}", flush=True)
    if any(row["returncode"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
