"""Reading the one statement two suites both have to agree about.

A genre's base half closes by naming the technique that genre is ordinarily
written with, or by stating that it has none, and its first word is the
canonical value (ADR-0164). The resource format's suite checks that every
genre states it; the fixture corpus's suite checks that a fixture turning on a
resolved arc names a genre supplying the one it needs. Read in two places, it
is written here once.
"""

from __future__ import annotations

from pathlib import Path

GENRE_TECHNIQUE_HEADING = "## The technique this genre is ordinarily written with"


def ordinary_technique_section(path: Path) -> str | None:
    """What a genre's base half states below that heading.

    `None` where the genre carries no such section at all, which is a
    different failure from a section that is present and says nothing.
    """

    _, heading, below = path.read_text(encoding="utf-8").partition(
        f"\n{GENRE_TECHNIQUE_HEADING}\n"
    )

    return below.partition("\n## ")[0].strip() if heading else None


def ordinary_technique(section: str) -> str:
    """The canonical value that statement opens on: a technique, or `none`."""

    return section.split()[0].strip(".,").lower()
