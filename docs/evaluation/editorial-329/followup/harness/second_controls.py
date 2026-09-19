# /// script
# requires-python = ">=3.12"
# ///
"""Run frozen second-candidate controls, preserving every native attempt."""

from __future__ import annotations

import concurrent.futures
import json
import os
import subprocess
from pathlib import Path

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
CLEANUP: Path = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
ROWS: list[tuple[str, str, str, str | None]] = [
    *[
        (f"timetable-r{n}", "timetable.md", "--output=response", None)
        for n in (1, 2, 3)
    ],
    ("certainty-r1", "certainty.md", "--output=response", None),
    ("delivery-response", "delivery.md", "--max=0 --output=response", None),
    ("delivery-in-place", "delivery.md", "--max=0 --in-place", "input.md"),
    ("delivery-file", "delivery.md", "--max=0 --output=result.md", "result.md"),
]


def run_control(row: tuple[str, str, str, str | None]) -> dict[str, object]:
    """Run one frozen source-blind control and retain file-target evidence."""

    # Inputs are committed before evaluation and are never synthesized per run.
    name, filename, flags, capture = row
    source = FOLLOW / "controls-second" / filename
    frozen = subprocess.check_output(
        ["git", "show", f"20de1df7:{source.relative_to(ROOT)}"], cwd=ROOT
    )
    if frozen != source.read_bytes():
        raise ValueError(f"Unfrozen control: {source}")
    target = FOLLOW / "probes/second-controls" / name
    target.mkdir(parents=True, exist_ok=False)
    prompt = target / "prompt.txt"
    prompt.write_text(f"/redline {flags} input.md\n")
    command = [
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
        str(source),
        "--input-name",
        "input.md",
        "--output",
        str(target / "run"),
    ]
    if capture:
        command.extend(["--capture-output-name", capture])
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, check=False
    )
    (target / "runner-stdout.txt").write_text(result.stdout)
    (target / "runner-stderr.txt").write_text(result.stderr)
    return {"control": name, "returncode": result.returncode}


def main() -> None:
    """Run two independent controls concurrently in a registered process group."""

    # The launcher creates this group's lifetime; native children own theirs.
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            "pid",
            str(os.getpid()),
            "Second-candidate supplemental native controls",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    results: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_control, row) for row in ROWS]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            (
                FOLLOW / "harness" / f"second-controls-{os.getpid()}-results.json"
            ).write_text(json.dumps(results, indent=2) + "\n")
            print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
