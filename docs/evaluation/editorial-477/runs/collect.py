"""Copy each written judgement from its blind directory into its run's packet.

    uv run --no-project python collect.py

Reads `judges.tsv`. A reply judge's `judgement-<letter>.md` becomes the
packet's `judgement-<letter>.md`, and a correction judge's becomes
`correction-<letter>.md`. A directory whose judgement has been copied is
removed, as the plan's *Judging* says; one still without a judgement is left.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRATCH = Path("/Users/thomas/Projects/skills/.git/kntnt-orchestrate/477.scratch")

for line in (HERE / "judges.tsv").read_text(encoding="utf-8").splitlines():
    run, kind, letter, where = line.split("\t")
    directory = SCRATCH / where.removeprefix("<scratch>/")
    written = directory / f"judgement-{letter}.md"
    name = f"judgement-{letter}.md" if kind == "reply" else f"correction-{letter}.md"
    if written.is_file():
        shutil.copy(written, SCRATCH / "packets" / run / name)
        shutil.rmtree(directory)
        print(f"{run}\t{name}")
