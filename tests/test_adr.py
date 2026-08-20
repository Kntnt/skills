"""The decision records under `docs/adr/`, and the numbers that cite them."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"
SKILLS = REPO_ROOT / "skills"

# The prose outside the collection that cites records the same way a record
# cites another one, so a number that has gone stale is caught wherever it is
# written rather than only where records supersede each other.
CITING_DOCS = ("CONTEXT.md", "README.md", "AGENTS.md", "CONTRIBUTING.md")

# A record's file is `NNNN-slug.md` and its number is that four-digit prefix;
# a citation is the same number written as `ADR-NNNN`.
RECORD = re.compile(r"^(\d{4})-.+\.md$")
CITATION = re.compile(r"ADR-(\d{4})")

# The clause every skill body opens its flag-refusal rule with, and the record
# that carries that rule. `delegation` states the rule in a longer sentence
# than its siblings, so what is pinned is the opening clause and the record
# closing the same paragraph rather than the sentence in full.
REFUSAL_CLAUSE = "A flag is refused rather than ignored where it has no work to do here"
REFUSAL_RECORD = "0059"


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


def _skill_bodies() -> list[Path]:
    """Every `SKILL.md` the collection ships, the Manager's among them."""

    return sorted(SKILLS.glob("*/*/SKILL.md")) + sorted(SKILLS.glob("*/SKILL.md"))


def test_the_flag_refusal_rule_cites_the_record_that_carries_it() -> None:
    """A citation can resolve and still name the wrong record.

    `tldr` attributed the flag-refusal rule to ADR-0029 while its siblings
    attributed the same rule to ADR-0059 — the record that withdrew ADR-0029's
    tolerance clause — so the skill cited, as authority for refusing a stray
    flag, the record that used to say a stray flag is tolerated. Nothing caught
    it: the check above reads no skill body at all, and 0029 has a file, so it
    would have resolved even where it did.

    The general form of this check is not writable. Whether a citation is apt
    requires knowing what each record carries, which is a reading and not a
    comparison. What is checkable is one rule written in one wording across
    every body that carries it, which is this one: the clause is fixed prose,
    so the record closing its paragraph is fixed too, and a body that names
    another one is wrong by that alone. A second rule stated as uniformly could
    be pinned the same way; nothing here generalises further than that.
    """

    bodies = _skill_bodies()

    # A glob that matched nothing, or a clause reworded out of every body,
    # would leave the loop below with nothing to judge and pass regardless.
    assert bodies

    carrying: list[str] = []
    misattributed: dict[str, list[str]] = {}
    for path in bodies:
        where = str(path.relative_to(REPO_ROOT))
        for paragraph in path.read_text(encoding="utf-8").split("\n\n"):
            if REFUSAL_CLAUSE not in paragraph:
                continue
            carrying.append(where)
            cited = CITATION.findall(paragraph)
            if cited[-1:] != [REFUSAL_RECORD]:
                misattributed[where] = cited

    assert carrying
    assert misattributed == {}
