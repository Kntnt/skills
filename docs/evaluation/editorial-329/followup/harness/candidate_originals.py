# /// script
# requires-python = ">=3.12"
# ///
"""Capture frozen original-source candidate Writes and optional blind pairs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
RUNNER: Path = ROOT / "docs/evaluation/editorial-329/harness/run.py"
CLEANUP: Path = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
ROWS: list[tuple[str, str, int]] = (
    [
        ("opinion", locale, repeat)
        for locale in ["sv", "en_GB", "en_US"]
        for repeat in [1, 2]
    ]
    + [("case-study", "en_US", repeat) for repeat in [1, 2, 3]]
    + [("case-study", "sv", repeat) for repeat in [1, 2]]
)


def run_row(
    row: tuple[str, str, int],
    *,
    revision: str,
    corpus: str,
    wave: str,
    pipeline: bool,
) -> dict[str, object]:
    """Stage only the frozen source and formal invocation for one fresh run."""

    # Verify source bytes before staging this independent invocation.
    genre, locale, repeat = row
    case_id = f"{genre}-{locale}-r{repeat}"
    source_relative = f"docs/evaluation/corpus/editorial-quality/sources/{genre}.md"
    source = ROOT / source_relative
    frozen = subprocess.check_output(
        ["git", "show", f"6e531f5:{source_relative}"], cwd=ROOT
    )
    if frozen != source.read_bytes():
        raise RuntimeError(f"Frozen source mismatch: {source}")

    # Keep every attempt in a new evidence directory.
    case = FOLLOW / "runs" / wave / case_id
    case.mkdir(parents=True, exist_ok=False)
    prompt = case / "write-prompt.txt"
    prompt.write_text(
        f"/write --genre={genre} --language={locale} --output=response source.md\n"
    )
    result = subprocess.run(
        [
            "uv",
            "run",
            str(RUNNER),
            "--revision",
            revision,
            "--corpus-revision",
            corpus,
            "--prompt",
            str(prompt),
            "--input",
            str(source),
            "--input-name",
            "source.md",
            "--output",
            str(case / "write"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    # Preserve runner diagnostics separately from native model captures.
    (case / "write-runner-stdout.txt").write_text(result.stdout)
    (case / "write-runner-stderr.txt").write_text(result.stderr)
    entry: dict[str, object] = {
        "case": case_id,
        "returncode": result.returncode,
        "source_revision": "6e531f5",
    }
    (case / "write-runner-result.json").write_text(json.dumps(entry, indent=2) + "\n")
    print(json.dumps(entry), flush=True)

    # Wait for evaluator extraction, never guess a refusal is an artifact.
    if pipeline:
        while (
            not (case / "draft.md").exists() and not (case / "withheld.json").exists()
        ):
            time.sleep(2)
        if (case / "withheld.json").exists():
            entry["redline"] = "skipped: Write withheld the artifact"
            return entry
        redline_prompt = case / "redline-prompt.txt"
        redline_prompt.write_text("/redline --output=response input.md\n")
        redline = subprocess.run(
            [
                "uv",
                "run",
                str(RUNNER),
                "--revision",
                revision,
                "--corpus-revision",
                corpus,
                "--prompt",
                str(redline_prompt),
                "--input",
                str(case / "draft.md"),
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
        (case / "redline-runner-stdout.txt").write_text(redline.stdout)
        (case / "redline-runner-stderr.txt").write_text(redline.stderr)
        entry["redline_returncode"] = redline.returncode
        (case / "pair-result.json").write_text(json.dumps(entry, indent=2) + "\n")
        print(json.dumps(entry), flush=True)
    return entry


def main() -> None:
    """Register this process and retain all attempts, including failed runs."""

    # Resolve evaluator-only paths while preserving historical defaults.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="8f92e12")
    parser.add_argument("--corpus", default="bf14dc2")
    parser.add_argument("--wave", default="candidate")
    parser.add_argument("--pipeline", action="store_true")
    parser.add_argument(
        "--cases",
        nargs="+",
        choices=[f"{genre}-{locale}-r{repeat}" for genre, locale, repeat in ROWS],
    )
    args = parser.parse_args()
    selected = [
        row
        for row in ROWS
        if not args.cases or f"{row[0]}-{row[1]}-r{row[2]}" in args.cases
    ]

    # Record the owned batch before launching native sessions.
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            "pid",
            str(os.getpid()),
            "Editorial #349 original candidate native evaluation batch",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )

    # Limit concurrency while allowing independent repetitions to progress.
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(
                partial(
                    run_row,
                    revision=args.revision,
                    corpus=args.corpus,
                    wave=args.wave,
                    pipeline=args.pipeline,
                ),
                selected,
            )
        )
    (FOLLOW / f"harness/{args.wave}-original-write-results.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
