"""The rules the review check cannot be run without."""

from __future__ import annotations

from pathlib import Path

from support.contract import STANDARD

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

    assert "Never review a ticket in this context" in text, (
        f"{SKILL / 'SKILL.md'}: the body forbids reviewing a ticket in the"
        f" session that holds it, in those words. The isolation is the whole"
        f" mechanism, and the body is the only thing an agent executes"
        f" (ADR-0109) — implied, it is skipped by whichever agent finds"
        f" spawning a subagent inconvenient. See {STANDARD}."
    )
    assert "subagent" in text, (
        f"{SKILL / 'SKILL.md'}: the body says the review happens in a subagent."
        f" A reviewer that helped write the ticket reads its own intent back"
        f" out of it and calls it clear, which is the one failure this skill"
        f" exists to avoid. See {STANDARD}."
    )


def test_the_body_briefs_the_reviewer_from_the_whole_thread() -> None:
    """Triage files its criteria as a comment, so the body alone is not the ticket.

    A reviewer given only the body reports the open questions that triage
    answered before this skill ever ran.
    """

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "The requirement is the thread and not the body" in text, (
        f"{SKILL / 'SKILL.md'}: the body says the requirement is the whole"
        f" thread. Triage files its criteria as a comment, so a reviewer given"
        f" the body alone is measuring the untriaged ticket. See {STANDARD}."
    )
    assert "oldest first" in text, (
        f"{SKILL / 'SKILL.md'}: the body says the comments reach the reviewer"
        f" oldest first. A thread read out of order is a thread whose settled"
        f" decisions arrive before the questions they answered (ADR-0065). See"
        f" {STANDARD}."
    )


def test_the_review_brief_refuses_to_be_summarised() -> None:
    """A summary of the ticket is the reviewing agent's reading of it.

    The whole check is what a reader with only the ticket concludes, so a
    brief carrying somebody else's precis of it measures that reader instead.
    """

    text = (SKILL / "references" / "review.md").read_text(encoding="utf-8")

    assert "pasted whole" in text, (
        f"{SKILL / 'references' / 'review.md'}: the brief says the ticket is"
        f" pasted whole. A precis of it is somebody else's reading, and what"
        f" the check measures is the reader who has only the ticket. See"
        f" {STANDARD}."
    )
    assert "Tell the reviewer nothing else" in text, (
        f"{SKILL / 'references' / 'review.md'}: the brief forbids telling the"
        f" reviewer anything the ticket does not carry. Context the builder"
        f" will not have is exactly what makes a thin ticket read as clear. See"
        f" {STANDARD}."
    )
