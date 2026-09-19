# /// script
# requires-python = ">=3.12"
# ///
"""Run the eight predeclared baseline invocations; preserve every result."""

import json
import os
import subprocess
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
RUNNER: Path = ROOT / "docs/evaluation/editorial-329/harness/run.py"
CLEANUP: str = "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"


def main() -> None:
    """Capture every declared baseline without overwriting an earlier attempt."""

    # Register this independent process group before launching any model.
    subprocess.run(
        [
            "uv",
            "run",
            CLEANUP,
            "add",
            "pid",
            str(os.getpid()),
            "Editorial #349 eight native baseline invocations",
        ],
        check=True,
        capture_output=True,
        cwd=ROOT,
    )

    # Keep the matrix order fixed before seeing any result.
    rows: list[tuple[str, str, str, str, str]] = [
        (
            "opinion-sv-r1",
            "opinion",
            "sv",
            "docs/evaluation/corpus/editorial-quality/sources/opinion.md",
            "6e531f5",
        ),
        (
            "opinion-sv-r2",
            "opinion",
            "sv",
            "docs/evaluation/corpus/editorial-quality/sources/opinion.md",
            "6e531f5",
        ),
        (
            "case-study-en_US-r1",
            "case-study",
            "en_US",
            "docs/evaluation/corpus/editorial-quality/sources/case-study.md",
            "6e531f5",
        ),
        (
            "case-study-en_US-r2",
            "case-study",
            "en_US",
            "docs/evaluation/corpus/editorial-quality/sources/case-study.md",
            "6e531f5",
        ),
        (
            "opinion-unknown-sv-r1",
            "opinion",
            "sv",
            "docs/evaluation/editorial-329/followup/fixtures/opinion-unknown-sv.md",
            "bf14dc2",
        ),
        (
            "opinion-absence-en_GB-r1",
            "opinion",
            "en_GB",
            "docs/evaluation/editorial-329/followup/fixtures/opinion-absence-en_GB.md",
            "bf14dc2",
        ),
        (
            "case-unprompted-en_US-r1",
            "case-study",
            "en_US",
            "docs/evaluation/editorial-329/followup/fixtures/case-unprompted-en_US.md",
            "bf14dc2",
        ),
        (
            "case-question-en_GB-r1",
            "case-study",
            "en_GB",
            "docs/evaluation/editorial-329/followup/fixtures/case-question-en_GB.md",
            "bf14dc2",
        ),
    ]
    results: list[dict[str, str | int]] = []

    # Freeze every input and retain every invocation, including failures.
    for case, genre, locale, source, source_revision in rows:
        source_path = ROOT / source
        frozen = subprocess.check_output(
            ["git", "show", f"{source_revision}:{source}"], cwd=ROOT
        )
        assert frozen == source_path.read_bytes(), source

        # Stage only the invocation and its complete source package.
        case_dir = FOLLOW / "runs/baseline" / case
        case_dir.mkdir(parents=True, exist_ok=False)
        prompt = case_dir / "prompt.txt"
        prompt.write_text(
            f"/write --genre={genre} --language={locale} --output=response source.md\n"
        )

        # Preserve failed runs and continue through the declared matrix.
        result = subprocess.run(
            [
                "python3",
                str(RUNNER),
                "--revision",
                "7ff6ec0",
                "--corpus-revision",
                "bf14dc2",
                "--prompt",
                str(prompt),
                "--input",
                str(source_path),
                "--input-name",
                "source.md",
                "--output",
                str(case_dir / "write"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        (case_dir / "runner-stdout.txt").write_text(result.stdout)
        (case_dir / "runner-stderr.txt").write_text(result.stderr)
        results.append(
            {
                "case": case,
                "returncode": result.returncode,
                "source_revision": source_revision,
            }
        )
        (FOLLOW / "harness/baseline-batch-results.json").write_text(
            json.dumps(results, indent=2) + "\n"
        )
        print(case, result.returncode, flush=True)


if __name__ == "__main__":
    main()
