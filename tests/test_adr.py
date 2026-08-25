"""The decision records under `docs/adr/`, and the numbers that cite them."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"

# Everywhere a reader is sent to find out what applies now, and so everywhere a
# number that answers to nothing is a broken pointer rather than a historical
# address: the always-loaded file and the documents it routes to, the rules
# document, the shipped scripts, and the suite itself, whose assertion messages
# cite a record for the reader whose check has just gone red (issue #69).
CITED_SUFFIXES = (".md", ".py")

# The three places a number is written as history and left alone. The archive
# reads as of each record's own date, so a record naming a deleted one — a
# consolidation's fold list most of all — is citing an address rather than
# pointing at current law; `CHANGELOG.md` and the rework dossier are the
# evidence for changes already made. Repointing any of them would falsify the
# account it is part of.
HISTORICAL_PATHS = (Path("docs/adr"), Path("docs/rework"), Path("CHANGELOG.md"))

# Directory names carrying no prose of this repository's own, matched wherever
# they sit, so a working copy's incidentals cannot fail the suite.
IGNORED_DIRECTORY_NAMES = frozenset({".git", ".venv", "__pycache__"})

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
    """Every file outside the archive that cites a record as a live pointer."""

    found: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in CITED_SUFFIXES:
            continue

        # One of the two exclusions is rooted and the other is not: a
        # historical account is a named place in this repository, while a
        # working copy's incidentals turn up at any depth.
        relative = path.relative_to(REPO_ROOT)
        if any(relative.is_relative_to(place) for place in HISTORICAL_PATHS):
            continue
        if IGNORED_DIRECTORY_NAMES.intersection(relative.parts):
            continue

        found.append(path)
    return found


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

    Only collision is asserted. Gaps in the sequence are legitimate — most of
    the sequence is a gap today — so nothing here requires it to be dense.
    """

    collisions = {
        number: names for number, names in _records().items() if len(names) > 1
    }

    assert collisions == {}


def test_every_cited_number_has_a_record() -> None:
    """A citation to a number no file carries is as broken as a stale record.

    What this judges is the prose a reader is sent to for current law, which is
    why the archive is not among the sources. A number written inside a record
    is an address as of that record's date — a consolidation names the records
    it supersedes precisely so the numbers stay findable in git — and a record
    is never rewritten to agree with a later arrangement (ADR-0112).
    """

    records = _records()
    dangling = {
        number: sources
        for number, sources in _citations().items()
        if number not in records
    }

    assert dangling == {}


def test_the_scan_reaches_every_kind_of_file_that_cites_a_record() -> None:
    """A walk that had drifted would judge nothing and pass regardless.

    The check above compares against an empty set, so a scan collecting no
    file, or only files citing nothing, is green for the wrong reason. The
    floor is one file of each kind that carries a citation today: the rules
    document, the contributor guide, a shipped script, and this suite.
    """

    cited = _citations()
    citing = {source for sources in cited.values() for source in sources}

    assert "docs/rules/skills.md" in citing
    assert "CONTRIBUTING.md" in citing
    assert "skills/kntnt/scripts/kntnt.py" in citing
    assert "tests/test_adr.py" in citing


def test_the_scan_reads_no_file_that_writes_a_number_as_history() -> None:
    """The archive's own citations are addresses, and stay unresolvable.

    A consolidation record names the records it supersedes by number, which is
    what makes those numbers findable in git after the records are deleted.
    Reading that list as a live pointer would either fail this suite or force
    the one edit a record never takes (ADR-0112). `CHANGELOG.md` and the rework
    dossier are the same kind of account.
    """

    sources = {str(path.relative_to(REPO_ROOT)) for path in _sources()}

    assert (
        "docs/adr/0112-how-this-repository-records-decisions-and-writes-tickets.md"
        not in sources
    )
    assert "docs/adr/README.md" not in sources
    assert "docs/rework/02-adr-triage.md" not in sources
    assert "CHANGELOG.md" not in sources
