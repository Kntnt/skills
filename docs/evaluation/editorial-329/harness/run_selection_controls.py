# /// script
# requires-python = ">=3.12"
# ///
"""Capture seven frozen selection controls, one fresh native session at a time."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def main() -> None:
    """Keep every failure and let the evaluator judge the captured artifacts."""
    for case in [
        "metadata-none",
        "instruction-none",
        "legacy-abt",
        "flag-pac",
        "instruction-abt",
        "report-pac",
        "article-excerpt",
    ]:
        print(json.dumps({"started": case}), flush=True)
        result = subprocess.run(
            [
                "uv",
                "run",
                str(HERE / "run.py"),
                "--revision=f8cac6d",
                "--corpus-revision=6e531f5",
                f"--prompt={HERE / 'selection-prompts' / (case + '.txt')}",
                f"--input={HERE / 'selection-inputs' / (case + '.md')}",
                "--input-name=input.md",
                f"--output={ROOT / 'docs/evaluation/editorial-329/runs/controls-selection' / case / 'redline'}",
            ],
            cwd=ROOT,
            check=False,
        )
        print(json.dumps({"completed": case, "exit": result.returncode}), flush=True)


if __name__ == "__main__":
    main()
