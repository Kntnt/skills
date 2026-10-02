# /// script
# requires-python = ">=3.12"
# ///
"""Execute the predeclared remaining matrix with two isolated native runs.

The first Redline is finished and the corrected Write is already running.
That Write occupies one worker slot until its result exists.
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

    def invoke(run: str) -> dict[str, object]:
        """Run one exact frozen turn; record a failure without rerunning it."""
        if (staging / run).exists():
            while not (staging / run / "result.json").exists():
                time.sleep(10)
            result = json.loads((staging / run / "result.json").read_text())
            return {
                "run": run,
                "returncode": result["returncode"],
                "already_running": True,
            }
        row = rows[run]
        is_write = row["fixture"] == "case-study-sv"
        turn = (
            "write-current-identifier"
            if is_write
            else "redline-current-genre-response"
            if row.get("metadata_construction_repair")
            and row["output_target"] == "response"
            else "redline-current-genre-file"
            if row.get("metadata_construction_repair")
            else "redline-response"
            if row["output_target"] == "response"
            else "redline-file"
        )
        command = [
            "uv",
            "run",
            str(PACKET / "harness/run.py"),
            "--timeout=5400",
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
    remaining = [
        "w01",
        "r04",
        *[f"c{i:02d}" for i in range(3, 13)],
        "r13",
        "r14",
        "w02",
        "w03",
    ]
    with ThreadPoolExecutor(max_workers=2) as executor:
        statuses = list(executor.map(invoke, remaining))
    (PACKET / "wave-status.json").write_text(json.dumps(statuses, indent=2) + "\n")
    return int(any(status["returncode"] != 0 for status in statuses))


if __name__ == "__main__":
    raise SystemExit(main())
