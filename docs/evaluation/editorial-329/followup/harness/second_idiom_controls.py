# /// script
# requires-python = ">=3.12"
# ///
"""Capture the three unchanged source-blind idiom controls after the pair batch."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
CLEANUP: Path = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
ROWS: list[tuple[str, Path, str]] = [
    (
        "idiom-frozen-clean",
        ROOT / "docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md",
        "6e531f5",
    ),
    (
        "idiom-first-sv-r1",
        FOLLOW / "runs/candidate/case-study-sv-r1/draft.md",
        "20de1df7",
    ),
    (
        "idiom-first-sv-r2",
        FOLLOW / "runs/candidate/case-study-sv-r2/draft.md",
        "20de1df7",
    ),
]


def run_row(row: tuple[str, Path, str]) -> dict[str, object]:
    """Expose only the unchanged artifact and formal Redline options."""

    # Verify each original input against its committed evidence before staging.
    name, source, source_revision = row
    frozen = subprocess.check_output(
        ["git", "show", f"{source_revision}:{source.relative_to(ROOT)}"], cwd=ROOT
    )
    if frozen != source.read_bytes():
        raise RuntimeError(f"Frozen input mismatch: {source}")
    case = FOLLOW / "runs/second-candidate" / name
    case.mkdir(parents=True, exist_ok=False)
    (case / "input.md").write_bytes(frozen)
    prompt = case / "redline-prompt.txt"
    prompt.write_text(
        "/redline --genre=case-study --language=sv --output=response input.md\n"
    )

    # Capture the complete native result, preserving failed attempts too.
    result = subprocess.run(
        [
            "uv",
            "run",
            str(ROOT / "docs/evaluation/editorial-329/harness/run.py"),
            "--revision",
            "82db439",
            "--corpus-revision",
            "20de1df7",
            "--prompt",
            str(prompt),
            "--input",
            str(case / "input.md"),
            "--input-name",
            "input.md",
            "--output",
            str(case / "redline"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (case / "runner-stdout.txt").write_text(result.stdout)
    (case / "runner-stderr.txt").write_text(result.stderr)
    entry: dict[str, object] = {
        "case": name,
        "returncode": result.returncode,
        "source_revision": source_revision,
    }
    print(json.dumps(entry), flush=True)
    return entry


def main() -> None:
    """Register the batch and maintain the two-native-parent ceiling."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", nargs="+", choices=[row[0] for row in ROWS])
    args = parser.parse_args()
    selected = [row for row in ROWS if not args.cases or row[0] in args.cases]

    # Register the owned batch before starting any native invocation.
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            "pid",
            str(os.getpid()),
            "Second-candidate source-blind idiom controls",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run_row, selected))
    (FOLLOW / f"harness/second-idiom-{os.getpid()}-results.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
