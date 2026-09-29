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
        f" (ADR-0177) — implied, it is skipped by whichever agent finds"
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
        f" (ADR-0180). See {STANDARD}."
    )


NUMBER_WORDS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
]


def _section(text: str, heading: str) -> str:
    """The lines under `heading`, up to the next heading of any level."""

    lines = text.splitlines()
    start = lines.index(heading) + 1
    end = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("#")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def _criteria_in_the_brief() -> list[str]:
    """Each numbered thing that stops a builder, as the brief lists it."""

    text = (SKILL / "references" / "review.md").read_text(encoding="utf-8")
    section = _section(text, "## What you are looking for")
    return [
        line for line in section.splitlines() if line[:1].isdigit() and ". **" in line
    ]


def test_the_review_brief_counts_its_own_list() -> None:
    """The brief tells the reviewer how many things to go through.

    A count that falls behind the list tells the reviewer to stop one short,
    and the item it drops is always the newest one.
    """

    path = SKILL / "references" / "review.md"
    text = path.read_text(encoding="utf-8")
    word = NUMBER_WORDS[len(_criteria_in_the_brief())]

    for sentence in (
        f"{word.capitalize()} things stop a builder or cost it.",
        f"Go through all {word} for this ticket",
        f"The {word} above catch",
    ):
        assert sentence in text, (
            f"{path}: the brief lists {word} things that stop a builder, so"
            f" every sentence that counts them says {word}; expected"
            f" {sentence!r}. A count behind the list tells the reviewer to stop"
            f" before the newest item. See {STANDARD}."
        )


def test_the_review_brief_reports_a_requirement_that_contradicts_a_rule() -> None:
    """Both stops of the unattended run of 2026-09-23 were of this shape (#440).

    #397 contradicted a rule the repository stated, and #416 a rule its
    blocker #394 was set to write. Each ticket was ready alone, and each
    reached the wave check of /orchestrate instead of this one.
    """

    path = SKILL / "references" / "review.md"
    item = next(
        (
            line
            for line in _criteria_in_the_brief()
            if "contradicts a rule" in line.split("**")[1]
        ),
        None,
    )

    assert item is not None, (
        f"{path}: the brief lists a requirement that contradicts a rule among"
        f" the things that stop a builder, in a bold lead containing"
        f" 'contradicts a rule'. Two tickets each ready alone stopped a run at"
        f" the wave check over exactly that (#440). See {STANDARD}."
    )
    for phrase, why in (
        ("states now", "a rule the repository states now"),
        ("will write", "a rule another ticket this one names will write"),
        ("whole thread", "reading that named ticket's whole thread"),
        ("Stop", "classing the finding as a Stop"),
    ):
        assert phrase in item, (
            f"{path}: the contradicted-rule item covers {why}, in words"
            f" containing {phrase!r}. See {STANDARD}."
        )


def test_the_help_page_lists_every_criterion_the_brief_does() -> None:
    """The manpage says what the check does, so it lists what the reviewer looks for."""

    path = SKILL / "help.md"
    section = _section(path.read_text(encoding="utf-8"), "## REVIEW CRITERIA")
    entries = [line for line in section.splitlines() if line.startswith("**")]

    assert "**Contradicted rule**" in entries, (
        f"{path}: REVIEW CRITERIA carries a **Contradicted rule** entry, the"
        f" manpage's name for the brief's requirement that contradicts a rule."
        f" See {STANDARD}."
    )
    assert len(entries) == len(_criteria_in_the_brief()), (
        f"{path}: REVIEW CRITERIA carries one entry per thing the review brief"
        f" lists ({len(_criteria_in_the_brief())}), and it carries"
        f" {len(entries)}. See {STANDARD}."
    )
