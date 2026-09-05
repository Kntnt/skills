"""The decision records under `docs/adr/`, and the numbers that cite them."""

from __future__ import annotations

import re
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"
STANDARD_DIR = REPO_ROOT / "docs" / "rules"

# Everywhere a reader is sent to find out what applies now, and so everywhere a
# number that answers to nothing is a broken pointer rather than a historical
# address: the always-loaded file and the documents it routes to, the rules
# modules, the shipped Skills and their scripts, and the suite itself, whose
# assertion messages cite a record for the reader whose check has just gone red
# (issue #69).
CITED_SUFFIXES = (".md", ".py")

# The two places a number is written as history and left alone. The archive
# reads as of each record's own date, so a record naming a deleted one — a
# consolidation's fold list most of all — is citing an address rather than
# pointing at current law, and `CHANGELOG.md` is the evidence for changes
# already made. Repointing either would falsify the account it is part of.
HISTORICAL_PATHS = (Path("docs/adr"), Path("CHANGELOG.md"))

# Directory names carrying no prose of this repository's own, matched wherever
# they sit, so a working copy's incidentals cannot fail the suite.
IGNORED_DIRECTORY_NAMES = frozenset({".git", ".venv", "__pycache__"})

# The rules module binding whoever writes a ticket here, and every record
# settling a rule it states: what a ticket may assert (0067), the numbers a run
# reserves so that it can (0071), the edge a discovered dependency corrects
# rather than builds around (0073), the declaration an invariant ticket makes
# (0099), the thread that outranks the body it amends (0065), and the builder a
# readiness review reads a ticket against (0180, the reform's own record). The
# module names each rule in a phrase and cites its record rather than arguing it
# again, so a rule that arrives without its number is one the reader can only
# take on this file's word — and a number here that the module never states a
# rule for is a citation with no rule under it (issue #266).
TICKET_RULES = STANDARD_DIR / "tickets.md"
TICKET_RULE_RECORDS = ("0065", "0067", "0071", "0073", "0099", "0180")

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

    Only collision is asserted. Gaps in the sequence are legitimate — the
    consolidation left most of the sequence a gap — so nothing here requires
    the numbering to be dense, and a number is never reused.
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
    is never rewritten to agree with a later arrangement (ADR-0180).
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
    floor is one file of each kind that carries a citation today: a rules
    module, the contributor guide, a shipped script, and this suite.
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
    the one edit a record never takes (ADR-0180). `CHANGELOG.md` is the same
    kind of account.
    """

    sources = {str(path.relative_to(REPO_ROOT)) for path in _sources()}

    assert (
        "docs/adr/0180-how-this-repository-records-decisions-and-writes-tickets.md"
        not in sources
    )
    assert "docs/adr/README.md" not in sources
    assert "CHANGELOG.md" not in sources


def test_the_ticket_rules_cite_the_record_behind_every_rule_they_state() -> None:
    """A rule restated in a rules module carries the record that settled it.

    The module exists so an author meets every rule in one place, and it buys
    that by naming each rule in a phrase instead of re-arguing it. The record
    is what makes the phrase checkable: it holds the field evidence, the
    alternatives and their costs, and it is where a reader goes to find out
    whether a rule is a finding or a taste. A rule stated there with no number
    beside it is the one case the arrangement cannot survive — the reasoning
    has been dropped rather than delegated (issue #266).

    Equality rather than containment, because the two failures are the same
    failure seen from either end: a rule whose record went uncited, and a
    record cited for a rule the module no longer states.
    """

    cited = set(CITATION.findall(TICKET_RULES.read_text(encoding="utf-8")))

    assert cited == set(TICKET_RULE_RECORDS), (
        f"{cited ^ set(TICKET_RULE_RECORDS)}:"
        f" {TICKET_RULES.relative_to(REPO_ROOT)} states each of its rules in a"
        f" phrase and cites the record carrying its reasoning. See {STANDARD}"
        f" for the same arrangement in the module beside it."
    )
