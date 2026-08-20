"""The decision records under `docs/adr/`, and the numbers that cite them."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"

# The prose outside the collection that cites records the same way a record
# cites another one, so a number that has gone stale is caught wherever it is
# written rather than only where records supersede each other.
CITING_DOCS = ("CONTEXT.md", "README.md", "AGENTS.md", "CONTRIBUTING.md")

# A record's file is `NNNN-slug.md` and its number is that four-digit prefix;
# a citation is the same number written as `ADR-NNNN`.
RECORD = re.compile(r"^(\d{4})-.+\.md$")
CITATION = re.compile(r"ADR-(\d{4})")


def _records() -> dict[str, list[str]]:
    """Map each four-digit number to the record filenames claiming it."""

    claimed: dict[str, list[str]] = {}
    for path in sorted(ADR.glob("*.md")):
        match = RECORD.match(path.name)
        if match is None:
            continue
        claimed.setdefault(match.group(1), []).append(path.name)
    return claimed


def _sources() -> list[Path]:
    """Every file the collection cites a record from."""

    return sorted(ADR.glob("*.md")) + [REPO_ROOT / name for name in CITING_DOCS]


def _citations() -> dict[str, list[str]]:
    """Map each cited number to the files citing it, repository-relative."""

    cited: dict[str, list[str]] = {}
    for path in _sources():
        where = str(path.relative_to(REPO_ROOT))
        for number in CITATION.findall(path.read_text(encoding="utf-8")):
            citing = cited.setdefault(number, [])
            if where not in citing:
                citing.append(where)
    return cited


def test_no_two_records_claim_the_same_number() -> None:
    """A number names one record, or a citation cannot say which it means.

    Only collision is asserted. Gaps in the sequence are legitimate — 0031 to
    0034 are gaps today — so nothing here requires the numbering to be dense.
    """

    collisions = {
        number: names for number, names in _records().items() if len(names) > 1
    }

    assert collisions == {}


def test_every_cited_number_has_a_record() -> None:
    """A citation to a number no file carries is as broken as a stale record."""

    records = _records()
    dangling = {
        number: sources
        for number, sources in _citations().items()
        if number not in records
    }

    assert dangling == {}
