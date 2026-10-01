# /// script
# requires-python = ">=3.12"
# ///
"""Execute the predeclared remaining matrix with two isolated native runs.

The first two invocations are already running. Their result files gate this
wave, so a launcher cannot silently exceed its declared concurrency.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
CLEANUP = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
REVISION = "fb16908712c4d47a36fc6ee9dfb3eb2714a19e65"


def main() -> int:
    """Leave one immutable evidence directory per commissioned invocation."""

    # Register the long-lived launcher in its own process group immediately.
    if os.getpgrp() != os.getpid():
        os.setsid()
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            "pid",
            str(os.getpid()),
            "Editorial #393 fixed-matrix launcher",
        ],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
    )
    staging = Path(json.loads((PACKET / "staging-location.json").read_text())["path"])
    manifest = json.loads((PACKET / "input-manifest.json").read_text())
    rows = json.loads((PACKET / "run-index.json").read_text())

    # Wait for the two already-started native sessions before launching more.
    while not all((staging / run / "result.json").exists() for run in ("r01", "r15")):
        time.sleep(10)

    def invoke(run: str) -> dict[str, object]:
        """Run one exact frozen turn; record a failure without rerunning it."""
        row = rows[run]
        is_write = row["fixture"] == "case-study-sv"
        turn = (
            "write-response"
            if is_write
            else "redline-response"
            if row["output_target"] == "response"
            else "redline-file"
        )
        command = [
            "uv",
            "run",
            str(PACKET / "harness/run.py"),
            f"--revision={REVISION}",
            f"--corpus-revision={REVISION}",
            f"--prompt={PACKET / 'turns' / (turn + '.txt')}",
            f"--input={REPOSITORY / manifest[row['fixture']]['path']}",
            f"--input-name={'source.md' if is_write else 'input.md'}",
            f"--output={staging / run}",
        ]
        if row["output_target"] != "response":
            command.append("--capture-output-name=output.md")
        with (staging / f"{run}-runner.log").open("w") as log:
            result = subprocess.run(
                command,
                cwd=REPOSITORY,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
                start_new_session=True,
            )
        status = {"run": run, "returncode": result.returncode}
        print(json.dumps(status), flush=True)
        return status

    # Map waits for every task; no unawaited session outlives this launcher.
    remaining = [run for run in rows if run not in {"r01", "r15", "r16", "r17"}]
    with ThreadPoolExecutor(max_workers=2) as executor:
        statuses = list(executor.map(invoke, remaining))
    (PACKET / "wave-status.json").write_text(json.dumps(statuses, indent=2) + "\n")
    return int(any(status["returncode"] != 0 for status in statuses))


if __name__ == "__main__":
    raise SystemExit(main())
