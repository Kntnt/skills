"""Stage one finished run's blind judge directories, as the plan's *Judging* says.

    uv run --no-project python judge_dirs.py RUN

It writes the run's states into `<scratch>/packets/RUN/states/` with
`states.py`, makes a directory `<scratch>/j/<token>/` for each judge — two
reply judges, and two correction judges where a checker ran — holding only the
files the plan names, appends the mapping to `judges.tsv` beside this file, and
writes each judge's whole message to `<scratch>/m/<token>.md`. `<token>` is
twelve random hexadecimal digits and names nothing about the run.
"""

import json
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE.parent
SCRATCH = Path("/Users/thomas/Projects/skills/.git/kntnt-orchestrate/477.scratch")


def fixture(run: str) -> str:
    for name in ("case-study-clean", "withheld-overclaim", "denied-overclaim"):
        if name in run:
            return name
    raise SystemExit(f"{run}: no fixture")


def message(brief: str, directory: Path, letter: str, expectation: str | None) -> str:
    text = (PLAN / brief).read_text(encoding="utf-8").strip()
    parts = [
        text,
        "---",
        f"Run directory: `{directory}`\n\nYour letter: `{letter}`",
    ]
    if expectation is not None:
        parts.append(f"**Frozen expectation**\n\n{expectation.strip()}")
    return "\n\n".join(parts) + "\n"


def main() -> int:
    run = sys.argv[1]
    packet = SCRATCH / "packets" / run
    states = packet / "states"
    subprocess.run(
        [sys.executable, str(HERE / "states.py"), str(packet), str(states)],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(HERE / "delivered.py"), str(states)], check=True
    )
    has_checker = json.loads((states / "states.json").read_text())["checkers"] > 0
    expectation = (PLAN / "expectations" / f"{fixture(run)}.md").read_text(
        encoding="utf-8"
    )
    rows = []
    (SCRATCH / "m").mkdir(exist_ok=True)
    for letter in ("a", "b"):
        token = secrets.token_hex(6)
        target = SCRATCH / "j" / token
        (target / "work").mkdir(parents=True)
        shutil.copy(packet / "supplied-input.md", target / "work" / "input.md")
        shutil.copy(packet / "response.txt", target / "response.md")
        if (packet / "captured-output.md").is_file():
            shutil.copy(packet / "captured-output.md", target / "work" / "output.md")
        (SCRATCH / "m" / f"{token}.md").write_text(
            message("judge-brief.md", target, letter, expectation), encoding="utf-8"
        )
        rows.append((run, "reply", letter, f"<scratch>/j/{token}"))
    if has_checker:
        for letter in ("a", "b"):
            token = secrets.token_hex(6)
            target = SCRATCH / "j" / token
            target.mkdir(parents=True)
            for source, name in (
                ("received.md", "input.md"),
                ("checked-delivered.md", "delivered.md"),
                ("draft-reply.md", "draft.md"),
                ("check-return.md", "check.md"),
                ("final-reply.md", "response.md"),
            ):
                shutil.copy(states / source, target / name)
            (SCRATCH / "m" / f"{token}.md").write_text(
                message("transition-judge-brief.md", target, letter, None),
                encoding="utf-8",
            )
            rows.append((run, "correction", letter, f"<scratch>/j/{token}"))
    with (HERE / "judges.tsv").open("a", encoding="utf-8") as table:
        for row in rows:
            table.write("\t".join(row) + "\n")
    for row in rows:
        print("\t".join(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
