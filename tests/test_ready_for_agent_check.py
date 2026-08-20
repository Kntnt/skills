"""The rules the review check cannot be run without."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "code" / "ready-for-agent-check"


def test_the_body_forbids_reviewing_a_ticket_in_this_context() -> None:
    """The isolation is the mechanism, so the instruction has to be in the body.

    A reviewer that helped write the ticket reads its own intent back out of
    it and calls it clear. That is the one failure this skill exists to avoid,
    and a body that only implied it would be carried out by whichever agent
    found spawning a subagent inconvenient.
    """

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "Never review a ticket in this context" in text
    assert "subagent" in text


def test_the_body_briefs_the_reviewer_from_the_whole_thread() -> None:
    """Triage files its criteria as a comment, so the body alone is not the ticket.

    A reviewer given only the body reports the open questions that triage
    answered before this skill ever ran, which is the shape of ADR-0065's
    failure with the reader changed.
    """

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "ADR-0065" in text
    assert "oldest first" in text


def test_the_review_brief_refuses_to_be_summarised() -> None:
    """A summary of the ticket is the reviewing agent's reading of it.

    The whole check is what a reader with only the ticket concludes, so a
    brief carrying somebody else's precis of it measures that reader instead.
    """

    text = (SKILL / "references" / "review.md").read_text(encoding="utf-8")

    assert "pasted whole" in text
    assert "Tell the reviewer nothing else" in text


def test_the_skill_declares_no_flag_it_would_have_to_refuse() -> None:
    """Nothing is written here, so `--yes` has no question to answer.

    The Manager's own grammar rule is that a flag with no work is an error
    rather than a no-op, and a skill that quietly accepted one would teach the
    opposite of what every other skill in the collection teaches (ADR-0059).
    """

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "there is no question for `--yes` to answer" in text
    assert "ADR-0059" in text
