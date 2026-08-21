"""The prose rules the orchestrate skill's briefs cannot be handed out without."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "code" / "orchestrate"

# Every brief this skill hands a subagent that is told to run something the
# project gates a change on. A run interviewed for issue #75 lost more turns to
# a suite that outlived its subagent's patience than to anything else, so each
# of these carries the same instruction about a command that takes long.
VERIFYING_BRIEFS = (
    "brief.md",
    "verify.md",
    "repair.md",
    "repaired.md",
    "wave.md",
    "amend.md",
)


def _brief(name: str) -> str:
    """Read one of the skill's briefs."""

    return (SKILL / "references" / name).read_text(encoding="utf-8")


def _waiting_paragraph(text: str) -> str:
    """The paragraph of a brief that tells its subagent to wait, or the empty string."""

    for paragraph in text.split("\n\n"):
        if "in the background" in paragraph:
            return paragraph.strip()
    return ""


def _step(number: int) -> str:
    """One numbered step of the skill's body, with everything indented under it."""

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^{number}\. .*?(?=^\d+\. |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"{SKILL / 'SKILL.md'}: no step {number} to read."
    return match.group(0)


def test_every_verifying_brief_tells_its_subagent_to_wait_out_a_long_command() -> None:
    """A gate that outlives a subagent's patience ends the turn, and unattended that is a dead run.

    The interviewed run's dominant failure mode was a builder or a verifier
    ending its turn with the suite still running and nothing committed. A human
    was there to arm a wait by hand and resume it; unattended, nothing wakes it.
    """

    for name in VERIFYING_BRIEFS:
        text = _brief(name)
        where = SKILL / "references" / name

        assert "start it in the background" in text, (
            f"{where}: the brief says a command that takes long is started in"
            f" the background. A suite run in the foreground is a suite that"
            f" outlives the turn it was started in (issue #75)."
        )
        assert "wait on its completion with whatever waiting facility" in text, (
            f"{where}: the brief says the subagent waits on the command's"
            f" completion with whatever waiting facility the harness gives it."
            f" A command started and not waited on is a gate nobody reads"
            f" (issue #75)."
        )
        assert "Never end your turn while it runs" in text, (
            f"{where}: the brief forbids ending the turn while the command"
            f" runs, in those words. Unattended there is no session left to"
            f" resume it, so a turn ended there is a dead run (issue #75)."
        )
        assert (
            "a turn ended with the gate still running is a build that did not"
            " finish or a verdict that was not reached" in text
        ), (
            f"{where}: the brief names what a turn ended mid-gate actually is"
            f" — a build that did not finish or a verdict that was not reached"
            f" — so waiting reads as part of the work rather than as idleness"
            f" to yield in (issue #75)."
        )


def test_the_briefs_state_the_waiting_rule_in_one_wording() -> None:
    """One rule stated six ways is six rules, and a subagent obeys the one it was given.

    The briefs are handed out one per subagent, so nothing but identical
    wording keeps a builder and a verifier held to the same rule.
    """

    stated = {name: _waiting_paragraph(_brief(name)) for name in VERIFYING_BRIEFS}
    wordings = set(stated.values())

    assert "" not in wordings, (
        f"{SKILL / 'references'}: every brief states the waiting rule in a"
        f" paragraph of its own. These state none: "
        f"{sorted(name for name, rule in stated.items() if not rule)}."
    )
    assert len(wordings) == 1, (
        f"{SKILL / 'references'}: every brief states the waiting rule in the"
        f" same wording, so the briefs state one rule rather than one each."
        f" These differ: {sorted(stated)}."
    )


def test_the_build_step_resumes_a_subagent_left_waiting() -> None:
    """A subagent waiting on a command it started has neither finished nor failed.

    Recorded as a stop, its verdict is a fail and the ticket spends an amend on
    a build that was never finished. The repair is a resumption.
    """

    step = _step(5)

    assert "ends its turn waiting on a command it started" in step, (
        f"{SKILL / 'SKILL.md'}: step 5 names the builder that ended its turn"
        f" waiting on a command it started. It is the run's commonest stop and"
        f" the one that is not a failure (issue #75)."
    )
    assert "resumed with that command's result" in step, (
        f"{SKILL / 'SKILL.md'}: step 5 says such a builder is resumed with the"
        f" command's result. Its stop is the mechanical kind, and the repair is"
        f" a resumption (issue #75)."
    )
    assert "rather than recorded" in step, (
        f"{SKILL / 'SKILL.md'}: step 5 says the waiting builder is resumed"
        f" rather than recorded. Recorded, an unfinished build becomes a failed"
        f" ticket nothing was wrong with (issue #75)."
    )


def test_the_verify_step_resumes_a_subagent_left_waiting() -> None:
    """A verifier that ended its turn mid-suite has reached no verdict to record."""

    step = _step(6)

    assert "ends its turn waiting on a command it started" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 names the verifier that ended its turn"
        f" waiting on a command it started — the same mechanical stop the"
        f" builder makes, and the interviewed run made it twice (issue #75)."
    )
    assert "resumed with that command's result" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says such a verifier is resumed with the"
        f" command's result rather than leaving the ticket with a verdict"
        f" nobody reached (issue #75)."
    )
    assert "rather than recorded" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says the waiting verifier is resumed"
        f" rather than recorded. A verdict that was not reached is not a fail"
        f" (issue #75)."
    )


def _writing_paragraph(text: str) -> str:
    """The paragraph of a brief that confines its subagent, or the empty string."""

    for paragraph in text.split("\n\n"):
        if paragraph.startswith("**Where you write.**"):
            return paragraph.strip()
    return ""


def test_every_brief_confines_its_subagent_to_its_tree_and_its_own_scratch() -> None:
    """A working tree isolates the files a ticket edits, and nothing else.

    Two subagents in sibling working trees chose the same scratch log path for
    the same gate, and one nearly read the other's exit status as its own; a
    cleanup glob at the shared scratch root deleted the engine's own state file
    mid-run. Neither is something a merge, a test, or a gate would ever catch.
    """

    for name in VERIFYING_BRIEFS:
        text = _brief(name)
        where = SKILL / "references" / name

        assert "`<scratch>`" in text, (
            f"{where}: the brief names the scratch directory its subagent"
            f" writes in. A subagent given no path of its own picks one, and"
            f" the one it picks is the one its sibling picked (ADR-0071)."
        )
        assert "Nothing outside those two is yours to write in" in text, (
            f"{where}: the brief confines its subagent to the working tree it"
            f" was given and that scratch directory. Anywhere else is shared"
            f" with whatever is being built beside it (ADR-0071)."
        )


def test_the_briefs_state_the_confinement_rule_in_one_wording() -> None:
    """One rule stated six ways is six rules, and a subagent obeys the one it was given.

    The briefs are handed out one per subagent, so nothing but identical
    wording keeps a builder and a verifier held to the same rule.
    """

    stated = {name: _writing_paragraph(_brief(name)) for name in VERIFYING_BRIEFS}
    wordings = set(stated.values())

    assert "" not in wordings, (
        f"{SKILL / 'references'}: every brief states the confinement rule in a"
        f" paragraph of its own, opening `**Where you write.**`. These state"
        f" none: {sorted(name for name, rule in stated.items() if not rule)}."
    )
    assert len(wordings) == 1, (
        f"{SKILL / 'references'}: every brief states the confinement rule in"
        f" the same wording, so the briefs state one rule rather than one each."
        f" These differ: {sorted(stated)}."
    )


def test_the_building_brief_hands_the_builder_the_numbers_it_may_take() -> None:
    """Two tickets that each read a registry for its next free number read the same one.

    Both created a record under that number, git merged the pair cleanly, and
    nothing in either repository would ever have said so. The reservation is
    what the builder takes instead of reading the directory (ADR-0071).
    """

    text = _brief("brief.md")
    where = SKILL / "references" / "brief.md"

    assert "`<reservations>`" in text, (
        f"{where}: the brief carries the numbers `isolate` reserved for this"
        f" ticket. A builder told nothing of them reads the directory, which"
        f" is the read three siblings make at the same moment (ADR-0071)."
    )
    assert "rather than reading the directory" in text, (
        f"{where}: the brief says the builder takes the reserved number rather"
        f" than reading the directory for the next free one. Naming the number"
        f" without forbidding the read leaves the read in place (ADR-0071)."
    )
    assert "one above the highest" in text, (
        f"{where}: the brief says next free means one above the highest, so a"
        f" reservation that expires is a gap rather than a number the next"
        f" ticket backfills (ADR-0067)."
    )


def test_the_isolation_step_says_what_isolate_answers() -> None:
    """What every ticket in a wave may reach for, the run hands out before the wave builds."""

    step = _step(4)

    assert "scratch" in step, (
        f"{SKILL / 'SKILL.md'}: step 4 says `isolate` answers with a scratch"
        f" directory of the ticket's own, which is what the briefs confine"
        f" their subagents to (ADR-0071)."
    )
    assert "reservations" in step, (
        f"{SKILL / 'SKILL.md'}: step 4 says `isolate` answers with the record"
        f" numbers reserved for the ticket, which is what keeps two tickets in"
        f" one wave from minting the same one (ADR-0071)."
    )
