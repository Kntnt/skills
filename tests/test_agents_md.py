"""The always-loaded agent guide, and the files its references point at."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = REPO_ROOT / "AGENTS.md"

# The rules module that binds whoever writes a ticket in this repository. It is
# named here rather than looked up, because what has to hold is that this
# particular module is pointed at — a guide that lists every other file an
# agent may need and omits this one is what the pointer exists to prevent.
TICKETS = "docs/rules/tickets.md"

# The rules module carrying what a Skill's own shipped files must hold. Named
# here for the same reason the module above is: what has to hold is that this
# particular module is pointed at, before anything has been written.
STANDARD = "docs/rules/skills.md"

# Every entry under `## References` is a backticked path, an em dash, and the
# clause saying when to read it.
REFERENCE = re.compile(r"^- `([^`]+)` — (read when [^\n]+)$", re.MULTILINE)


def _references() -> dict[str, str]:
    """Map each referenced path to the clause saying when it is read."""

    text = AGENTS.read_text(encoding="utf-8")
    return {match.group(1): match.group(2) for match in REFERENCE.finditer(text)}


def test_agents_md_points_at_the_rules_a_ticket_author_is_held_to() -> None:
    """An agent about to write a ticket has to meet the rules somewhere.

    The rules are prose and live in one module — what a ticket may assert
    while it waits, and when it declares that it builds alone (ADR-0112).
    This file is what an agent always has loaded, so the module is reachable
    only if this file names it (issue #67). The clause matters as
    much as the path: a reader skims the list for the occasion, and an entry
    whose occasion never says *ticket* is an entry a ticket author skips.
    """

    references = _references()

    assert TICKETS in references
    assert "ticket" in references[TICKETS]


def test_every_file_agents_md_references_exists() -> None:
    """A pointer to a path nothing carries points nowhere.

    Records are renamed by their own slugs and moved between directories, and
    nothing else in this repository reads this list, so a stale entry here is
    silent until an agent goes looking and finds nothing.
    """

    references = _references()

    # A reworded list, or a heading shape this pattern stops matching, would
    # leave nothing to judge and pass regardless.
    assert references

    missing = [path for path in references if not (REPO_ROOT / path).exists()]

    assert missing == []


def test_agents_md_points_at_the_standard_a_new_skill_is_held_to() -> None:
    """A Skill's own files carry requirements the suite enforces and nothing states.

    An author who reads this file, writes a Skill, and runs the suite meets
    those requirements as a red check on a rule nobody told them about (issue
    #69). The module is the answer, and this file is what an agent always has
    loaded, so the module is reachable before anything is written only if this
    file names it — and the clause has to say *Skill*, because a reader skims
    the list for the occasion rather than the path.
    """

    references = _references()

    assert STANDARD in references
    assert "skill" in references[STANDARD].lower()


def test_rule_placement_names_every_specialized_rule_module() -> None:
    """The placement inventory stays complete as rule subjects are added."""

    # Isolate the inventory rather than accepting a filename cited elsewhere.
    rules_directory = REPO_ROOT / "docs" / "rules"
    placement_rules = rules_directory / "docs.md"
    text = placement_rules.read_text(encoding="utf-8")
    placement = text.split("## Where a rule goes", maxsplit=1)[1].split(
        "## What earns a record", maxsplit=1
    )[0]

    # Require every specialized module to appear in the placement inventory.
    expected = {
        path.name for path in rules_directory.glob("*.md") if path != placement_rules
    }
    missing = sorted(name for name in expected if f"`{name}`" not in placement)

    assert missing == [], (
        f"{placement_rules}: the placement inventory omits these rule modules:"
        f" {missing}. A new subject needs both its module and its routing entry."
    )
