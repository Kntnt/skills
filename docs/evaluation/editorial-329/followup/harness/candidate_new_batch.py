# /// script
# requires-python = ">=3.12"
# ///
"""Run the fixed new/general candidate cells without judging or rewriting output."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
RUNNER: Path = ROOT / "docs/evaluation/editorial-329/harness/run.py"
CLEANUP: Path = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
ROWS: list[tuple[str, str, str, str, str]] = (
    [
        (
            f"opinion-unknown-sv-r{n}",
            "opinion",
            "sv",
            "opinion-unknown-sv.md",
            "bf14dc2",
        )
        for n in (1, 2)
    ]
    + [
        (
            f"opinion-absence-en_GB-r{n}",
            "opinion",
            "en_GB",
            "opinion-absence-en_GB.md",
            "bf14dc2",
        )
        for n in (1, 2)
    ]
    + [
        (
            f"case-unprompted-en_US-r{n}",
            "case-study",
            "en_US",
            "case-unprompted-en_US.md",
            "bf14dc2",
        )
        for n in (1, 2)
    ]
    + [
        (
            f"case-question-en_GB-r{n}",
            "case-study",
            "en_GB",
            "case-question-en_GB.md",
            "bf14dc2",
        )
        for n in (1, 2)
    ]
    + [
        ("article-sv-r1", "article", "sv", "article.md", "6e531f5"),
        ("column-sv-r1", "column", "sv", "column.md", "6e531f5"),
        ("web-copy-en_US-r1", "web-copy", "en_US", "web-copy.md", "6e531f5"),
        ("general-en_GB-r1", "general", "en_GB", "article.md", "6e531f5"),
    ]
)


def run_cell(row: tuple[str, str, str, str, str], stage: str) -> dict[str, object]:
    """Capture one immutable invocation, refusing existing evidence directories."""

    # Confirm the actual input against its frozen source or extracted artifact.
    case, genre, locale, filename, source_revision = row
    case_dir = FOLLOW / "runs/candidate" / case
    case_dir.mkdir(parents=True, exist_ok=True)
    if stage == "write":
        base = (
            FOLLOW / "fixtures"
            if source_revision == "bf14dc2"
            else ROOT / "docs/evaluation/corpus/editorial-quality/sources"
        )
        supplied = base / filename
        frozen = subprocess.check_output(
            ["git", "show", f"{source_revision}:{supplied.relative_to(ROOT)}"], cwd=ROOT
        )
        if frozen != supplied.read_bytes():
            raise ValueError(f"Source changed: {supplied}")
        invocation = (
            f"/write --genre={genre} --language={locale} --output=response source.md\n"
        )
        input_name = "source.md"
    else:
        supplied = case_dir / "write/artifact.md"
        if not supplied.is_file():
            return {
                "case": case,
                "stage": stage,
                "skipped": "No independently extracted Write artifact",
            }
        invocation = "/redline --output=response input.md\n"
        input_name = "input.md"

    # The existing runner owns native isolation, capture and registration.
    prompt = case_dir / f"{stage}-prompt.txt"
    prompt.write_text(invocation)
    process = subprocess.run(
        [
            "uv",
            "run",
            str(RUNNER),
            "--revision",
            "8f92e12",
            "--corpus-revision",
            "bf14dc2",
            "--prompt",
            str(prompt),
            "--input",
            str(supplied),
            "--input-name",
            input_name,
            "--output",
            str(case_dir / stage),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (case_dir / f"{stage}-runner-stdout.txt").write_text(process.stdout)
    (case_dir / f"{stage}-runner-stderr.txt").write_text(process.stderr)
    return {
        "case": case,
        "stage": stage,
        "returncode": process.returncode,
        "source_revision": source_revision,
    }


def main() -> None:
    """Run two independent cells at a time and persist each completed result."""

    # Register the batch immediately; the launcher gives it its own group.
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            "pid",
            str(os.getpid()),
            "Editorial fidelity candidate new/general evaluation batch",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["write", "redline"])
    parser.add_argument("--cases", nargs="*")
    args = parser.parse_args()
    selected = [row for row in ROWS if not args.cases or row[0] in args.cases]
    results: list[dict[str, object]] = []

    # Separate outputs keep parallel runs from changing each other's inputs.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_cell, row, args.stage) for row in selected]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            path = (
                FOLLOW
                / "harness"
                / f"candidate-new-{args.stage}-{os.getpid()}-results.json"
            )
            path.write_text(json.dumps(results, indent=2) + "\n")
            print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
