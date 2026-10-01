# /// script
# requires-python = ">=3.12"
# ///
"""Run the remaining fixed matrix with two independent native sessions at once."""

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


def run_one(index: int) -> dict[str, object]:
    """Preserve every fixed row; service interruptions are handled separately."""
    output = SCRATCH / f"sample-{index:02d}"
    if index <= 6:
        locale = "en_US" if index % 2 else "en_GB"
        prompt = PACKET / f"prompts/write-{locale}.txt"
        source = (
            REPOSITORY / "docs/evaluation/corpus/editorial-quality/sources/opinion.md"
        )
        extra: list[str] = []
    else:
        prompt = PACKET / "prompts/checker.txt"
        source = (
            REPOSITORY
            / "docs/evaluation/editorial-362/checker/fixtures/p3-document-scope.md"
        )
        extra = ["--capture-output-name", "report.md"]
    command = [
        "uv",
        "run",
        str(PACKET / "harness/run.py"),
        "--revision",
        REVISION,
        "--corpus-revision",
        REVISION,
        "--prompt",
        str(prompt),
        "--input",
        str(source),
        "--input-name",
        "source.md",
        "--output",
        str(output),
        "--timeout",
        "2400",
        *extra,
    ]
    result = subprocess.run(
        command, cwd=REPOSITORY, capture_output=True, text=True, check=False
    )
    record = {
        "index": index,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    (SCRATCH / f"launch-{index:02d}.json").write_text(
        json.dumps(record, indent=2) + "\n"
    )
    print(json.dumps(record), flush=True)
    return record


def main() -> None:
    """Own the campaign while existing first rows finish, then run the rest."""
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
            "Fixed GPT retest matrix runner",
        ],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
    )
    while not all((SCRATCH / f"sample-{i:02d}/result.json").exists() for i in (1, 2)):
        time.sleep(1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(run_one, range(3, 13)))
    (SCRATCH / "campaign-results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
