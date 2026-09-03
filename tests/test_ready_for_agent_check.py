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
        f" (ADR-0046) — implied, it is skipped by whichever agent finds"
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


def test_the_review_brief_names_the_builder_it_measures_against() -> None:
    """The reviewer's own ease is not the builder's, so the brief has to say whose is.

    The reviewer runs on whatever Seat the harness gives a subagent, and the
    builder is routed at or below it. A brief that leaves the builder unnamed
    is answered from the reviewer's own capability, and a strong reviewer
    reports a ticket clean for a reason the ticket does not carry.
    """

    text = (SKILL / "references" / "review.md").read_text(encoding="utf-8")

    assert "no more capable than you" in text, (
        f"{SKILL / 'references' / 'review.md'}: the brief names the builder as"
        f" a Seat no more capable than the reviewer. Unnamed, every test"
        f" phrased as what a builder could do is answered from the reviewer's"
        f" own capability, which is the one thing the ticket cannot carry"
        f" (ADR-0155). See {STANDARD}."
    )


def test_the_skill_declares_no_flag_it_would_have_to_refuse() -> None:
    """Nothing is written here, so `--yes` has no question to answer.

    The Manager's own grammar rule is that a flag with no work is an error
    rather than a no-op, and a skill that quietly accepted one would teach the
    opposite of what every other skill in the collection teaches.
    """

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "there is no question for `--yes` to answer" in text, (
        f"{SKILL / 'SKILL.md'}: this skill writes nothing and asks nothing, so"
        f" the body says plainly that `--yes` has no question to answer. A flag"
        f" quietly accepted here teaches the opposite of what every other skill"
        f" in the collection teaches. See {STANDARD}."
    )
    assert (
        "a flag accepted and ignored teaches that flags sometimes do nothing" in text
    ), (
        f"{SKILL / 'SKILL.md'}: the paragraph refusing a flag with no work"
        f" carries the reason an installed reader needs to apply the rule. See"
        f" {STANDARD}."
    )
