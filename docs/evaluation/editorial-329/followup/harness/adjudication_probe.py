# /// script
# requires-python = ">=3.12"
# ///
"""Capture the four frozen finding-adjudication probes without scoring them."""

from __future__ import annotations

import concurrent.futures
import json
import os
import subprocess
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
PROBES: Path = FOLLOW / "probes/finding-adjudication"
CASES: tuple[str, ...] = ("column", "opinion", "chronology", "document-scope")


def run_case(case: str) -> dict[str, object]:
    """Run one complete immutable source/draft/report package in isolation."""
    destination = PROBES / case
    result = subprocess.run(
        [
            "uv",
            "run",
            str(ROOT / "docs/evaluation/editorial-329/harness/run.py"),
            "--revision",
            "ae24f9b3",
            "--corpus-revision",
            "bf14dc2",
            "--prompt",
            str(PROBES / "prompt.txt"),
            "--input",
            str(destination / "input.md"),
            "--input-name",
            "input.md",
            "--output",
            str(destination / "run"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (destination / "runner-stdout.txt").write_text(result.stdout)
    (destination / "runner-stderr.txt").write_text(result.stderr)
    return {"case": case, "returncode": result.returncode}


def main() -> None:
    """Register the launcher and persist each completion across two lanes."""

    # The external launcher creates this process's dedicated process group.
    subprocess.run(
        [
            "uv",
            "run",
            "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py",
            "add",
            "pid",
            str(os.getpid()),
            "Four finding-adjudication probes",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    results: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_case, case) for case in CASES]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            (PROBES / "results.json").write_text(json.dumps(results, indent=2) + "\n")
            print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
