# /// script
# requires-python = ">=3.12"
# ///
"""Run the frozen delivery matrix and independent identity-blind judges."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import secrets
import subprocess
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parents[1]
SCRATCH = Path("/private/tmp/kntnt-orchestrate-20261002.o7bmMK/ticket-488-scratch")
RUNNER = PACKET / "harness/run.py"
CLEANUP = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
START = "5457c89405aece11b325937f9f07407f01974f7c"
ROWS = [
    *[
        (f"article-unnamed-{i}", "article-unnamed", "article", "response")
        for i in range(1, 4)
    ],
    *[
        (f"opinion-flawed-{i}", "opinion-flawed", "opinion", "response")
        for i in range(1, 4)
    ],
    ("article-clean-response", "article-clean", "article", "response"),
    ("article-clean-file", "article-clean", "article", "output.md"),
    ("column-flawed-file", "column-flawed", "column", "output.md"),
]
EXPECTATIONS = {
    "article-unnamed": "The headline names no subject: report its defect or repair it to identify the subject the body supplies without an unsupported claim. Preserve the calm explanation, byline, quoted summary, undecided funding and non-commercial next step.",
    "opinion-flawed": "Detect unsupported motives, a population inference contradicted by the booking denominator, contradictory costs and a vague exhortation. Report unresolved defects beside the artifact. Preserve qualified facts and the proposal.",
    "article-clean": "The text is clean and conforms to its anatomy. Preserve every byte in a file-target delivery. A response-target run may return only a short Swedish no-change status where unchanged with no unresolved findings.",
    "column-flawed": "Detect incompatible participation claims and a generic opening/ending. The scene cannot be established from text alone: report the contradiction rather than inventing a replacement memory. Preserve reflection and doubt; report unresolved defects beside the artifact.",
}


def invoke(command: list[str], record: Path) -> dict[str, object]:
    """Wait for a native capture and preserve even an interrupted launch."""
    result = subprocess.run(
        command, cwd=REPOSITORY, capture_output=True, text=True, check=False
    )
    value = {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    record.write_text(json.dumps(value, indent=2) + "\n")
    return value


def run_row(
    row: tuple[str, str, str, str], arm: str, revision: str
) -> dict[str, object]:
    """Expose only neutral native roots and judge each completed terminal reply."""
    name, fixture, genre, target = row
    token = secrets.token_hex(6)
    output = SCRATCH / "packets" / token
    prompt = SCRATCH / f"prompt-{token}.txt"
    prompt.write_text(
        f"/redline --genre={genre} --language=sv --output={target} input.md\n"
    )
    command = [
        "uv",
        "run",
        str(RUNNER),
        "--revision",
        revision,
        "--corpus-revision",
        START,
        "--prompt",
        str(prompt),
        "--input",
        str(PACKET / f"inputs/{fixture}.md"),
        "--input-name",
        "input.md",
        "--output",
        str(output),
        "--timeout",
        "2400",
    ]
    if target != "response":
        command.extend(["--capture-output-name", "output.md"])
    launch = invoke(command, SCRATCH / f"launch-{token}.json")
    mapping: dict[str, object] = {
        "arm": arm,
        "row": name,
        "fixture": fixture,
        "target": target,
        "revision": revision,
        "packet": str(output),
        "launch": launch,
        "judges": [],
    }
    if launch["returncode"]:
        print(json.dumps(mapping), flush=True)
        return mapping

    # Each judge gets its own root and sees no trace, identity or arm name.
    judges: list[dict[str, object]] = []
    mapping["judges"] = judges
    for letter in ("a", "b"):
        judge_token = secrets.token_hex(6)
        judge_output = SCRATCH / "packets" / judge_token
        judge_prompt = SCRATCH / f"prompt-{judge_token}.txt"
        judge_prompt.write_text(
            (PACKET / "judge-brief.md").read_text()
            + f"\nOutput target: `{target}`.\n\nFrozen expectation: {EXPECTATIONS[fixture]}\n"
        )
        judge_command = [
            "uv",
            "run",
            str(RUNNER),
            "--revision",
            revision,
            "--corpus-revision",
            START,
            "--prompt",
            str(judge_prompt),
            "--input",
            str(output / "supplied-input.md"),
            "--input-name",
            "input.md",
            "--output",
            str(judge_output),
            "--judge-response",
            str(output / "response.txt"),
            "--capture-output-name",
            "judgement.md",
            "--timeout",
            "2400",
        ]
        if target != "response" and (output / "captured-output.md").exists():
            judge_command.extend(
                ["--judge-artifact", str(output / "captured-output.md")]
            )
        judge_launch = invoke(judge_command, SCRATCH / f"launch-{judge_token}.json")
        judges.append(
            {"letter": letter, "packet": str(judge_output), "launch": judge_launch}
        )
        # Persist completed mapping even if a subsequent judge is interrupted.
        (SCRATCH / f"mapping-{arm}-{name}.json").write_text(
            json.dumps(mapping, indent=2) + "\n"
        )
    print(
        json.dumps({"row": name, "arm": arm, "returncode": launch["returncode"]}),
        flush=True,
    )
    return mapping


def main() -> None:
    """Own the campaign and wait until every run and judge ends."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            "pid",
            str(os.getpid()),
            "Ticket 488 native matrix",
        ],
        cwd=REPOSITORY,
        env={**os.environ, "KNTNT_HOME": str(SCRATCH / "cleanup-home")},
        check=True,
        capture_output=True,
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=["pre", "post", "rev"], required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--row", action="append")
    args = parser.parse_args()
    rows = [row for row in ROWS if args.row is None or row[0] in args.row]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(run_row, row, args.arm, args.revision) for row in rows
        ]
        results = [future.result() for future in futures]
    (SCRATCH / f"campaign-{args.arm}.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
