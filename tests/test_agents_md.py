"""The always-loaded agent guide, and the files its references point at."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = REPO_ROOT / "AGENTS.md"

# The record that binds whoever writes a ticket in this repository. It is named
# here rather than looked up, because what has to hold is that this particular
# record is pointed at — a guide that lists four other files and omits this one
# is what the pointer exists to prevent.
TICKET_RECORD = (
    "docs/adr/0067-a-ticket-asserts-only-what-stays-true-until-it-is-built.md"
)

# The rules module carrying what a Skill's own shipped files must hold. Named
# here for the same reason the record above is: what has to hold is that this
# particular module is pointed at, before anything has been written.
STANDARD = "docs/rules/skills.md"

# Every entry under `## References` is a backticked path, an em dash, and the
# clause saying when to read it.
REFERENCE = re.compile(r"^- `([^`]+)` — (read when [^\n]+)$", re.MULTILINE)


def _references() -> dict[str, str]:
    """Map each referenced path to the clause saying when it is read."""

    text = AGENTS.read_text(encoding="utf-8")
    return {match.group(1): match.group(2) for match in REFERENCE.finditer(text)}


def test_agents_md_points_at_the_record_that_binds_ticket_authors() -> None:
    """An agent about to write a ticket has to meet the convention somewhere.

    The convention is prose and lives in a record; this file is what an agent
    always has loaded, so the record is reachable only if this file names it
    (issue #67). The clause matters as much as the path: a reader skims the
    list for the occasion, and an entry whose occasion never says *ticket* is
    an entry a ticket author skips.
    """

    references = _references()

    assert TICKET_RECORD in references
    assert "ticket" in references[TICKET_RECORD]


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
