# /// script
# requires-python = ">=3.12"
# ///
"""Capture one additional repair and a fresh strict source comparison."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
PROBES: Path = ROOT / "docs/evaluation/editorial-329/followup/probes/third-comparison"
CASES: tuple[str, ...] = ("column", "opinion-sv", "opinion-en_US")


def run_case(case: str, stage: str) -> dict[str, object]:
    """Capture only the named output file; earlier evidence stays isolated."""
    destination = PROBES / case / stage
    output_name = "revised.md" if stage == "repair" else "report.md"
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
            str(PROBES / f"{stage}-prompt.txt"),
            "--input",
            str(destination / "input.md"),
            "--input-name",
            "input.md",
            "--output",
            str(destination / "run"),
            "--capture-output-name",
            output_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (destination / "runner-stdout.txt").write_text(result.stdout)
    (destination / "runner-stderr.txt").write_text(result.stderr)
    return {"case": case, "stage": stage, "returncode": result.returncode}


def main() -> None:
    """Run the selected frozen stage in at most two isolated native lanes."""

    # The external launcher supplies a dedicated process group.
    subprocess.run(
        [
            "uv",
            "run",
            "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py",
            "add",
            "pid",
            str(os.getpid()),
            "Third-comparison continuation diagnostic",
        ],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["repair", "check"])
    parser.add_argument("--cases", choices=CASES, nargs="+", default=list(CASES))
    args = parser.parse_args()
    results: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_case, case, args.stage) for case in args.cases]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            (PROBES / f"{args.stage}-results.json").write_text(
                json.dumps(results, indent=2) + "\n"
            )
            print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
