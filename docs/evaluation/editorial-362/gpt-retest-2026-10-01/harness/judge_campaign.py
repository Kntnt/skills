# /// script
# requires-python = ">=3.12"
# ///
"""Judge each writing run in a fresh native session as its capture completes."""

from __future__ import annotations

import concurrent.futures
import json
import os
import subprocess
import time
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
SCRATCH = Path(
    "/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-observation-mgldfmax"
)
CLEANUP = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
REVISION = "fb16908712c4d47a36fc6ee9dfb3eb2714a19e65"


def judge_one(index: int) -> dict[str, object]:
    """Wait for complete raw evidence, then expose only an identity-blind packet."""
    result_path = SCRATCH / f"sample-{index:02d}/result.json"
    while not result_path.exists():
        time.sleep(1)
    result = json.loads(result_path.read_text())
    if result["returncode"] or result["timed_out"]:
        print(
            json.dumps({"index": index, "awaiting_void_resolution": result}), flush=True
        )
        return {"index": index, "awaiting_void_resolution": True}
    subprocess.run(
        ["uv", "run", str(PACKET / "harness/prepare_judge.py"), str(index)],
        cwd=REPOSITORY,
        check=True,
    )
    command = [
        "uv",
        "run",
        str(PACKET / "harness/run.py"),
        "--revision",
        REVISION,
        "--corpus-revision",
        REVISION,
        "--prompt",
        str(PACKET / "prompts/write-judge.txt"),
        "--input",
        str(SCRATCH / f"judge-input-{index:02d}.md"),
        "--input-name",
        "input.md",
        "--output",
        str(SCRATCH / f"judge-{index:02d}"),
        "--capture-output-name",
        "judgement.md",
        "--timeout",
        "2400",
    ]
    run = subprocess.run(
        command, cwd=REPOSITORY, check=False, capture_output=True, text=True
    )
    record = {
        "index": index,
        "returncode": run.returncode,
        "stdout": run.stdout,
        "stderr": run.stderr,
    }
    (SCRATCH / f"judge-launch-{index:02d}.json").write_text(
        json.dumps(record, indent=2) + "\n"
    )
    print(json.dumps(record), flush=True)
    return record


def main() -> None:
    """Own the judge campaign; the writing-run captures stay untouched."""
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
            "Blind GPT semantic judge campaign",
        ],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(judge_one, range(1, 7)))
    (SCRATCH / "judge-campaign-results.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
