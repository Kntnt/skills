# /// script
# requires-python = ">=3.12"
# ///
"""Run the ten frozen genre controls sequentially without discarding failures.

Each child uses run.py's fresh installation, native trace and inventory capture.
The evaluator judges completed cases independently while later cases run.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[4]
RUNNER = Path(__file__).with_name("run.py")
CONTROLS = REPOSITORY / "docs/evaluation/editorial-329/runs/controls-genres"
INSTRUCTIONS = "f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9"
CORPUS = "6e531f5fe0b610e046ae58787f246cc6239acbcc"


def main() -> None:
    """Capture every declared control, preserving each child's exit status."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=INSTRUCTIONS)
    parser.add_argument(
        "--genres",
        nargs="+",
        choices=["article", "case-study", "column", "opinion", "web-copy"],
        default=["article", "case-study", "column", "opinion", "web-copy"],
    )
    args = parser.parse_args()
    # Sequence the model sessions so each Redline has room for its correction.
    for genre in args.genres:
        for kind in ["clean", "flawed"]:
            identifier = f"{genre}-{kind}"
            case = CONTROLS / identifier
            print(json.dumps({"event": "started", "case": identifier}), flush=True)
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    str(RUNNER),
                    "--revision",
                    args.revision,
                    "--corpus-revision",
                    CORPUS,
                    "--prompt",
                    str(case / "invocation.txt"),
                    "--input",
                    str(case / "prepared-input.md"),
                    "--input-name",
                    "input.md",
                    "--output",
                    str(case / "redline"),
                ],
                cwd=REPOSITORY,
                check=False,
            )
            print(
                json.dumps(
                    {
                        "event": "completed",
                        "case": identifier,
                        "returncode": result.returncode,
                    }
                ),
                flush=True,
            )


if __name__ == "__main__":
    main()
