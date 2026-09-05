"""The always-loaded agent guide, and the files its references point at."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = REPO_ROOT / "AGENTS.md"

# The module that binds whoever writes a ticket in this repository. It is named
# here rather than looked up, because what has to hold is that this particular
# module is pointed at — a guide that lists four other files and omits this one
# is what the pointer exists to prevent.
TICKET_RULES = "docs/rules/tickets.md"

# The two records the module states in a phrase and cites. They are reachable
# through it and are not entries of their own: an author who meets the rules in
# three places meets them in none, and the guide is where the one place is
# named (issue #266).
TICKET_RECORDS = (
    "docs/adr/0067-a-ticket-asserts-only-what-stays-true-until-it-is-built.md",
    "docs/adr/0099-a-ticket-that-rewrites-an-invariant-declares-that-it-builds-alone.md",
)

# The coding-standard module carrying what a Skill's own shipped files must
# hold. Named here for the same reason the record above is: what has to hold is
# that this particular module is pointed at, before anything has been written.
STANDARD = "docs/rules/skills.md"

# The rules modules stating what the Manager's verbs promise and how a Skill
# routes delegated work, each with the word a reader skims the list for. Named
# here for the same reason the two above are: an agent about to change a verb's
# behaviour, or how work is delegated, has to be able to find the law before
# they write anything.
BEHAVIOUR = {
    "docs/rules/collection.md": "manager",
    "docs/rules/routing.md": "route",
}

# Every entry under `## References` is a backticked path, an em dash, and the
# clause saying when to read it.
REFERENCE = re.compile(r"^- `([^`]+)` — (read when [^\n]+)$", re.MULTILINE)


def _references() -> dict[str, str]:
    """Map each referenced path to the clause saying when it is read."""

    text = AGENTS.read_text(encoding="utf-8")
    return {match.group(1): match.group(2) for match in REFERENCE.finditer(text)}


def test_agents_md_points_at_the_module_that_binds_ticket_authors() -> None:
    """An agent about to write a ticket has to meet the convention somewhere.

    The convention is prose and lives in a rules module; this file is what an
    agent always has loaded, so the module is reachable only if this file names
    it (issue #67, issue #266). The clause matters as much as the path: a
    reader skims the list for the occasion, and an entry whose occasion never
    says *ticket* is an entry a ticket author skips.
    """

    references = _references()

    assert TICKET_RULES in references
    assert "ticket" in references[TICKET_RULES]


def test_agents_md_points_at_no_ticket_record_directly() -> None:
    """One occasion is answered by one entry, or it is answered by none.

    The rules a ticket author is under are settled across two records and a
    practice neither of them states, and an author who meets them in three
    entries reads whichever one they happen to open. The module states all of
    it and cites the records; the guide therefore names the module and lets the
    records be reached through it (issue #266).
    """

    references = _references()

    assert [record for record in TICKET_RECORDS if record in references] == []


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


def test_agents_md_points_at_the_law_the_collection_behaves_under() -> None:
    """What a verb promises is law, and law nobody can find is not consulted.

    The Manager's behavioural law and the routing law it delegates work under
    live in their own modules under `docs/rules/`, and this file is what an
    agent always has loaded, so they are reachable before anything is changed
    only if this file names them (issue #264). The clause matters as much as
    the path: a reader skims the list for the occasion, so an entry for the
    Manager's law that never says *Manager* is one its reader skips.
    """

    references = _references()

    for path, occasion in BEHAVIOUR.items():
        assert path in references
        assert occasion in references[path].lower()
