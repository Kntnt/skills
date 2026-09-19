# /// script
# requires-python = ">=3.12"
# ///
"""Launch a source-blind pair only after its exact artifact has been extracted."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
CLEANUP: Path = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)


def main() -> None:
    """Register the independent runner immediately and retain native evidence."""

    # Refuse unprepared and already-run cases rather than replacing evidence.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case")
    args = parser.parse_args()
    case = FOLLOW / "runs/candidate" / args.case
    if not (case / "draft.md").is_file() or (case / "redline").exists():
        raise RuntimeError("The draft must exist and the Redline run must be new")
    prompt = case / "redline-prompt.txt"
    prompt.write_text("/redline --output=response input.md\n")

    # Start this runner in its own process group with retained diagnostics.
    with (
        (case / "redline-runner-stdout.txt").open("w") as stdout,
        (case / "redline-runner-stderr.txt").open("w") as stderr,
    ):
        process = subprocess.Popen(
            [
                "uv",
                "run",
                str(ROOT / "docs/evaluation/editorial-329/harness/run.py"),
                "--revision",
                "8f92e12",
                "--corpus-revision",
                "bf14dc2",
                "--prompt",
                str(prompt),
                "--input",
                str(case / "draft.md"),
                "--input-name",
                "input.md",
                "--output",
                str(case / "redline"),
            ],
            cwd=ROOT,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
        )
        subprocess.run(
            [
                "uv",
                "run",
                str(CLEANUP),
                "add",
                "pid",
                str(process.pid),
                f"Editorial original source-blind Redline {args.case}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    (case / "redline-runner-process.json").write_text(
        json.dumps({"pid": process.pid, "process_group": process.pid}) + "\n"
    )
    print(process.pid)


if __name__ == "__main__":
    main()
