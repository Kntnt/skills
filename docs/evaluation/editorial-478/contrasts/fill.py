# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Fill Redline's reply-check brief the way a run fills it, for a replay.

A replay hands the checker's own half of `reply-check.md` — everything after
its `---` — to a fresh session, filled with a received text, a delivered text,
a drafted reply and the measurement of the delivered text, exactly as the
historical run in #475 filled it: each text in a four-backtick `markdown`
fence, the measurement in a `json` fence, and `<library>` replaced inside its
backticks by a path. A replay is diagnosis, never a Redline run (issue #478).

Usage: `uv run fill.py BRIEF CONTRAST_DIR LIBRARY > prompt.txt`, where BRIEF is
a copy of `reply-check.md` read from the revision under test and CONTRAST_DIR
holds `received.md`, `delivered.md`, `reply.md` and `measurement.json`.
"""

from __future__ import annotations

import sys
from pathlib import Path


def fill(brief: str, contrast: Path, library: str) -> str:
    """The checker's half of the brief with every placeholder filled."""

    half = brief.split("\n---\n", 1)[1].lstrip("\n")

    def text(name: str) -> str:
        return (contrast / name).read_text(encoding="utf-8").rstrip("\n")

    filled = (
        half.replace("`<received>`", f"````markdown\n{text('received.md')}\n````")
        .replace("`<delivered>`", f"````markdown\n{text('delivered.md')}\n````")
        .replace("`<reply>`", f"````markdown\n{text('reply.md')}\n````")
        .replace("`<measurement>`", f"```json\n{text('measurement.json')}\n```")
        .replace("<library>", library)
    )
    for placeholder in ("<received>", "<delivered>", "<reply>", "<measurement>"):
        if placeholder in filled:
            raise ValueError(f"{placeholder} left unfilled")
    return filled


def main(argv: list[str]) -> int:
    """Print the filled brief for one contrast."""

    brief, contrast, library = argv
    sys.stdout.write(
        fill(Path(brief).read_text(encoding="utf-8"), Path(contrast), library)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
