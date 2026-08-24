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

# Every brief the skill hands out, the wave check's fixer included. The fixer
# runs no gate — the wave check reruns it on the branch the fixer leaves — so
# the waiting rule is not its to carry, while the confinement rule is every
# subagent's (ADR-0072).
ALL_BRIEFS = (*VERIFYING_BRIEFS, "fix.md")

# Which briefs the run hands a subagent that writes a ticket's code — the
# first build and the amend. Declared once: the invariant test quantifies
# over the reference directory itself, so a brief added later is classified
# from the moment it exists — here, or in EXEMPT_BRIEFS with its reason
# stated (issue #85).
CODE_WRITING_BRIEFS = (
    "brief.md",
    "amend.md",
)

# Every rule that applies to a subagent holding a code-writing brief, named
# by the opening of the paragraph that states it. A rule is carried whole —
# its opening paragraph and every paragraph under it up to the next rule —
# and in one wording wherever it belongs, the mechanism proven on the
# waiting rule (issue #85).
CODE_WRITING_RULES = {
    "the reservation rule (ADR-0071)": "**Numbers are reserved for you.**",
    "the run-owned files rule (ADR-0071)": "**Some files are the run's to write, not yours.**",
    "the waiting rule (issue #75)": "**A long command is waited on, not yielded to.**",
    "the confinement rule (ADR-0071)": "**Where you write.**",
}

# The reference directory's remaining briefs, each with the reason the
# code-writing rules are not its to carry — a stated exemption a reader
# checks, rather than an absence somebody has to notice (issue #85).
EXEMPT_BRIEFS = {
    "verify.md": "verdict only: its subagent runs the gate and reads the tree, and writes no work of its own",
    "repaired.md": "verdict only: the repair's verifier reads the merged tree, and writes no work of its own",
    "wave.md": "verdict only: the wave check is told to change nothing — the finder is never the fixer",
    "repair.md": "merges work two builders already made and may build nothing either ticket left undone, so it creates no record and no entry of its own",
    "fix.md": "runs alone on the integrated branch after the notes are applied — nothing builds beside it, and its findings may send it into the very files the run owns",
}


def _brief(name: str) -> str:
    """Read one of the skill's briefs."""

    return (SKILL / "references" / name).read_text(encoding="utf-8")


def _instructions(name: str) -> str:
    """One brief's fill-in instructions — everything above the brief itself."""

    return _brief(name).split("\n---\n", 1)[0]


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


def _manpage_section(heading: str) -> str:
    """Return one uppercase section from the orchestrate manpage."""

    text = (SKILL / "help.md").read_text(encoding="utf-8")
    marker = f"\n## {heading}\n"
    assert marker in text, f"{SKILL / 'help.md'}: no {heading} section to read."
    return text.partition(marker)[2].partition("\n## ")[0]


def _manpage_entry(heading: str, term: str) -> str:
    """Return the description following one tagged manpage term."""

    paragraphs = _manpage_section(heading).strip().split("\n\n")
    for index, paragraph in enumerate(paragraphs[:-1]):
        if paragraph.startswith(term):
            return paragraphs[index + 1]

    raise AssertionError(
        f"{SKILL / 'help.md'}: the {heading} section has no entry starting {term}."
    )


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


def _rule_statement(text: str, opening: str) -> str:
    """One rule as a brief states it, or the empty string.

    A rule is the paragraph opening with the rule's own bold sentence plus
    every paragraph under it up to the next bold-opening paragraph, so a rule
    that carries a placeholder and its follow-through is compared whole.
    """

    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n")]
    for index, paragraph in enumerate(paragraphs):
        if paragraph.startswith(opening):
            statement = [paragraph]
            for following in paragraphs[index + 1 :]:
                if following.startswith("**"):
                    break
                statement.append(following)
            return "\n\n".join(statement)
    return ""


def test_every_brief_the_reference_directory_holds_is_classified() -> None:
    """Every rule has to find every brief by hand, and nothing fails when one does not.

    Two rules reached some briefs and not the amending builder's, which took
    over a first builder's work in the same working tree knowing less than
    that builder did. So the classification quantifies over the briefs the
    directory actually holds rather than over a list of names: a brief added
    later fails here from the moment it exists, until it is declared
    code-writing or visibly exempt (issue #85).
    """

    on_disk = {path.name for path in (SKILL / "references").glob("*.md")}
    classified = set(CODE_WRITING_BRIEFS) | set(EXEMPT_BRIEFS)

    assert set(CODE_WRITING_BRIEFS).isdisjoint(EXEMPT_BRIEFS), (
        f"{SKILL / 'references'}: a brief is code-writing or exempt, never"
        f" both — an exemption on a code-writing brief is a contradiction a"
        f" reader cannot check. Both: "
        f"{sorted(set(CODE_WRITING_BRIEFS) & set(EXEMPT_BRIEFS))} (issue #85)."
    )
    assert on_disk == classified, (
        f"{SKILL / 'references'}: every brief the directory holds is declared"
        f" code-writing or exempt, and nothing is declared that the directory"
        f" does not hold — an unclassified brief is one no rule finds, and a"
        f" stale entry is a claim about nothing. Unclassified: "
        f"{sorted(on_disk - classified)}; stale: {sorted(classified - on_disk)}"
        f" (issue #85)."
    )


def test_every_code_writing_brief_carries_every_code_writing_rule() -> None:
    """A subagent obeys the brief it was given, and the amending builder's said less.

    The amending builder was briefed without the reservation rule and the
    run-owned files rule, so it could mint a duplicate record number or append
    straight to a run-owned file — the two collisions those rules exist to
    remove. So every code-writing brief carries every rule that applies to a
    code-writing subagent, in one wording, with every placeholder the rule
    carries explained by that brief's fill-in instructions (issue #85).
    """

    for rule, opening in CODE_WRITING_RULES.items():
        stated = {
            name: _rule_statement(_brief(name), opening) for name in CODE_WRITING_BRIEFS
        }
        wordings = set(stated.values())

        # Every code-writing brief states the rule at all.
        assert "" not in wordings, (
            f"{SKILL / 'references'}: every code-writing brief states {rule}"
            f" in a paragraph opening `{opening}`. These state it nowhere:"
            f" {sorted(name for name, statement in stated.items() if not statement)}"
            f" (issue #85)."
        )

        # One rule in one wording, whichever brief a subagent is holding.
        assert len(wordings) == 1, (
            f"{SKILL / 'references'}: every code-writing brief states {rule}"
            f" in the same wording, so a rule reads identically whichever"
            f" brief a subagent is holding. These differ: {sorted(stated)}"
            f" (issue #85)."
        )

        # A placeholder nothing explains is handed out unfilled.
        for name, statement in stated.items():
            instructions = _instructions(name)
            for placeholder in re.findall(r"`<[a-z-]+>`", statement):
                assert placeholder in instructions, (
                    f"{SKILL / 'references' / name}: the fill-in instructions"
                    f" say what {placeholder} in {rule} is replaced with"
                    f" (issue #85)."
                )


def test_the_build_step_resumes_a_subagent_left_waiting() -> None:
    """A subagent waiting on a command it started has neither finished nor failed.

    Recorded as a stop, its verdict is a fail and the ticket spends an amend on
    a build that was never finished. The repair is a resumption.
    """

    step = _step(6)

    assert "ends its turn waiting on a command it started" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 names the builder that ended its turn"
        f" waiting on a command it started. It is the run's commonest stop and"
        f" the one that is not a failure (issue #75)."
    )
    assert "resumed with that command's result" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says such a builder is resumed with the"
        f" command's result. Its stop is the mechanical kind, and the repair is"
        f" a resumption (issue #75)."
    )
    assert "rather than recorded" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says the waiting builder is resumed"
        f" rather than recorded. Recorded, an unfinished build becomes a failed"
        f" ticket nothing was wrong with (issue #75)."
    )


def test_the_verify_step_resumes_a_subagent_left_waiting() -> None:
    """A verifier that ended its turn mid-suite has reached no verdict to record."""

    step = _step(7)

    assert "ends its turn waiting on a command it started" in step, (
        f"{SKILL / 'SKILL.md'}: step 7 names the verifier that ended its turn"
        f" waiting on a command it started — the same mechanical stop the"
        f" builder makes, and the interviewed run made it twice (issue #75)."
    )
    assert "resumed with that command's result" in step, (
        f"{SKILL / 'SKILL.md'}: step 7 says such a verifier is resumed with the"
        f" command's result rather than leaving the ticket with a verdict"
        f" nobody reached (issue #75)."
    )
    assert "rather than recorded" in step, (
        f"{SKILL / 'SKILL.md'}: step 7 says the waiting verifier is resumed"
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

    for name in ALL_BRIEFS:
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
    """One rule stated seven ways is seven rules, and a subagent obeys the one it was given.

    The briefs are handed out one per subagent, so nothing but identical
    wording keeps a builder and a verifier held to the same rule.
    """

    stated = {name: _writing_paragraph(_brief(name)) for name in ALL_BRIEFS}
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

    step = _step(5)

    assert "scratch" in step, (
        f"{SKILL / 'SKILL.md'}: step 5 says `isolate` answers with a scratch"
        f" directory of the ticket's own, which is what the briefs confine"
        f" their subagents to (ADR-0071)."
    )
    assert "reservations" in step, (
        f"{SKILL / 'SKILL.md'}: step 5 says `isolate` answers with the record"
        f" numbers reserved for the ticket, which is what keeps two tickets in"
        f" one wave from minting the same one (ADR-0071)."
    )


def _fill_in_instructions() -> str:
    """The building brief's fill-in instructions — everything above the brief itself."""

    return _brief("brief.md").split("\n---\n", 1)[0]


def test_the_building_brief_makes_the_runs_own_files_the_runs_to_write() -> None:
    """Every parallel ticket appends to the same few files, so every one collides with every other.

    Three of eight tickets in an interviewed run collided at integration and
    every collision was in prose the repository's ground rules make each ticket
    append to. The repair machinery, built for disagreements, spent nineteen
    percent of that run settling appends that agreed (ADR-0071).
    """

    text = _brief("brief.md")
    where = SKILL / "references" / "brief.md"

    assert "`<run-owned>`" in text, (
        f"{where}: the brief carries the list of files the run writes itself."
        f" A builder told nothing of them appends to them, and so does every"
        f" ticket beside it (ADR-0071)."
    )
    assert "Never edit one of those files" in text, (
        f"{where}: the brief forbids editing a run-owned file, in those words."
        f" Naming the files without forbidding the edit leaves the collision"
        f" exactly where it was (ADR-0071)."
    )
    assert "`<note>`" in text, (
        f"{where}: the brief names the note path the builder writes its entry"
        f" to instead. An entry with nowhere to go is an entry written into"
        f" the file anyway, or lost (ADR-0071)."
    )
    assert "one ticket at a time" in text, (
        f"{where}: the brief says the run applies the notes one ticket at a"
        f" time, which is what makes withholding the file from the builder a"
        f" deferral rather than a loss (ADR-0071)."
    )


def test_the_building_brief_says_how_it_is_filled_in_where_the_run_owns_nothing() -> (
    None
):
    """A repository with no changelog and no append convention briefs as it always did."""

    instructions = _fill_in_instructions()
    where = SKILL / "references" / "brief.md"

    assert "`<run-owned>`" in instructions, (
        f"{where}: the fill-in instructions say what `<run-owned>` is replaced"
        f" with. A placeholder nothing explains is handed out unfilled."
    )
    assert "named none" in instructions, (
        f"{where}: the fill-in instructions say what becomes of the paragraph"
        f" where the orchestrator named no run-owned file, as they do for the"
        f" reservations a repository with no numbered registry has none of."
    )


def test_the_build_step_names_the_runs_own_files_and_briefs_them() -> None:
    """Which files every ticket appends to is a reading of prose, so it is the orchestrator's."""

    step = _step(6)

    assert "the run's own files" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 has the orchestrator name the run's own"
        f" files before the first wave is briefed. An engine cannot read a"
        f" repository's ground rules for what every ticket must touch"
        f" (ADR-0071)."
    )
    assert "the changelog" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 names the changelog as one of them."
        f" It is the file every repository has and every ticket appends to"
        f" (ADR-0071)."
    )
    assert "A builder never edits one of them" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says the briefs carry the list because"
        f" a builder never edits one of these files. A list passed without"
        f" that rule is a list a builder reads as advice (ADR-0071)."
    )


def test_the_integration_step_applies_the_waves_notes_before_the_wave_check() -> None:
    """Sequential appends cannot collide, and the run's own appends are verified like any other."""

    step = _step(8)

    assert "in the order this step integrated them" in step, (
        f"{SKILL / 'SKILL.md'}: step 8 applies the wave's notes in integration"
        f" order, one ticket's worth at a time. Appends made one after another"
        f" are the whole of why they are the run's to make (ADR-0071)."
    )
    assert "remove the notes from the branch" in step, (
        f"{SKILL / 'SKILL.md'}: step 8 takes the notes off the branch once"
        f" they are applied. A note left behind is a scaffolding file shipped"
        f" as part of the work (ADR-0071)."
    )
    assert "before step 11 reads the branch" in step, (
        f"{SKILL / 'SKILL.md'}: step 8 applies the notes before the wave check"
        f" runs, which is what makes the arrangement honest — the run's own"
        f" appends pass the same verification as everything else (ADR-0071)."
    )


def test_the_manpage_accounts_for_the_files_the_run_writes() -> None:
    """A developer reading the page has to know why no builder's commit carries its changelog line."""

    where = SKILL / "help.md"
    entry = _manpage_entry("FILES", "**Run-owned append files**")

    assert "ticket-specific notes" in entry, (
        f"{where}: the run-owned files entry says builders leave their"
        f" proposed entries in ticket-specific notes (ADR-0071)."
    )
    assert "applies those notes serially" in entry, (
        f"{where}: the entry says the orchestrator applies the notes serially,"
        f" which prevents append-only files from colliding (ADR-0071)."
    )


def test_the_question_step_asks_in_one_batch_between_plan_and_claim() -> None:
    """ADR-0070: every question a run needs a human for is asked before the
    first ticket is claimed, while the developer who typed the command is
    still there — and the answers reach the builders through the tickets."""

    step = _step(3)

    assert "leaves open" in step, (
        f"{SKILL / 'SKILL.md'}: step 3 has the orchestrator read every ticket"
        f" in scope for a decision its text leaves open. The label promises"
        f" there is nothing to ask, and the label is a claim triage can get"
        f" wrong (ADR-0070)."
    )
    assert "one batch" in step, (
        f"{SKILL / 'SKILL.md'}: step 3 asks everything it found in one batch,"
        f" while the developer who typed the command is still there — after"
        f" it, the developer is not addressed again until the report"
        f" (ADR-0070)."
    )
    assert "comment" in step, (
        f"{SKILL / 'SKILL.md'}: step 3 writes each answer as a comment on its"
        f" ticket, which is how it reaches the builder: the brief carries the"
        f" whole thread, so an answer on the ticket is an answer in the brief"
        f" (ADR-0065)."
    )
    assert "claim" in _step(4).splitlines()[0].lower(), (
        f"{SKILL / 'SKILL.md'}: the claim step follows the question step, so"
        f" every question is asked before the first ticket is claimed"
        f" (ADR-0070)."
    )


def test_the_question_step_parks_rather_than_guesses_under_yes() -> None:
    """`--yes` answers yes/no, and *which default?* is not one of those.

    Under the flag there is nobody to ask, so a ticket whose text leaves a
    decision open is returned to the human loop rather than guessed at.
    """

    step = _step(3)

    assert "park --ticket" in step, (
        f"{SKILL / 'SKILL.md'}: step 3 parks a ticket with an open decision"
        f" under `--yes`, through the engine's park verb — the label swap is"
        f" deterministic and belongs behind the engine's seam (ADR-0070)."
    )
    assert "needs-info" in step, (
        f"{SKILL / 'SKILL.md'}: step 3 says what parking does to the label —"
        f" `ready-for-agent` replaced with `needs-info`, the tracker saying"
        f" truthfully that the thinking is not finished (ADR-0070)."
    )
    assert "question on the ticket" in step, (
        f"{SKILL / 'SKILL.md'}: step 3 writes the question on the ticket"
        f" before the label moves, so the parked ticket carries what a human"
        f" must answer to bring it back (ADR-0070)."
    )


def test_the_build_step_triages_a_stop_before_recording_anything() -> None:
    """A stop is not an outcome until the orchestrator has read what it stopped on.

    The interviewed runs recorded stops over missing directories and taken
    numbers as failures, because the step gave the orchestrator no licence to
    do anything with a stop but write it down (ADR-0070, issue #74).
    """

    step = _step(6)

    assert "triaged before anything is recorded" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 triages a stopped subagent before"
        f" recording anything. One clause that disposes of every stop alike"
        f" records a missing directory as a ticket that could not be built"
        f" (ADR-0070)."
    )
    assert "decides anything about the work" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 states the question that sorts a stop —"
        f" whether fixing it decides anything about the work. Without it the"
        f" hinder and the decision are one pile again (ADR-0070)."
    )
    assert "mechanical hinder" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 names the mechanical hinder — a"
        f" condition of the environment, not a question of the requirement —"
        f" as the stop the orchestrator repairs itself (ADR-0070)."
    )
    assert "the same brief once more" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 dispatches the same brief once more"
        f" after repairing a hinder. A repaired condition with no redispatch"
        f" is a fixed machine and a lost ticket (ADR-0070)."
    )
    assert "survives its repair" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 bounds the repair to one — a hinder"
        f" that survives its repair is recorded as the failure it now is, for"
        f" the same reason the amend and the rebuild are bounded (ADR-0069)."
    )


def test_a_genuine_decision_mid_run_parks_the_ticket() -> None:
    """Nothing about the work was tried and found wanting, so no failure is recorded.

    The builder's brief says to stop rather than guess, which is right; what
    changes is what the orchestrator does with that stop (ADR-0070).
    """

    step = _step(6)

    assert "parks the ticket exactly as step 3 parks one" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 parks a mid-run decision with the"
        f" mechanism the plan-time batching uses — one park, not two"
        f" (ADR-0070, issue #74)."
    )
    assert "record no outcome" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 records no outcome for a parked"
        f" ticket. Recorded, the tracker would hold it settled and no answer"
        f" could bring it back to a run (ADR-0070)."
    )
    assert "the wave carries on without it" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 lets the wave carry on without the"
        f" parked ticket — a decision parks one ticket, never the night"
        f" (ADR-0070)."
    )


def test_the_verify_amend_and_repair_steps_share_the_triage() -> None:
    """One triage stated once, or four triages drifting apart.

    The desired behaviour covers a building, verifying, repairing, or amending
    subagent alike, so the later steps hand their stops to step 6's rule
    rather than restating it (issue #74).
    """

    for number in (7, 9, 10):
        step = _step(number)

        assert "triaged as step 6 triages a stop" in step, (
            f"{SKILL / 'SKILL.md'}: step {number} routes a stopped subagent"
            f" through the triage step 6 states, in those words — a stop"
            f" recorded untriaged is the failure-by-default issue #74 removed"
            f" (ADR-0070)."
        )


def test_the_integration_step_narrows_its_catch_all_to_work_found_wanting() -> None:
    """The clause that disposed of every stop alike now catches only real failures."""

    step = _step(8)

    assert "including a builder that stopped and reported" not in step, (
        f"{SKILL / 'SKILL.md'}: step 8 no longer folds a stopped builder into"
        f" its catch-all — a stop is triaged where it happened, and only its"
        f" found-wanting kind reaches integration as a fail (issue #74)."
    )
    assert "tried and found wanting" in step, (
        f"{SKILL / 'SKILL.md'}: step 8's catch-all names what it now catches"
        f" — work tried and found wanting, which is what the amend cycle"
        f" fronts (ADR-0070, issue #74)."
    )


def test_an_amended_verdict_can_drive_one_continuation_amend() -> None:
    """An #87-shaped distinct contract defect is new bounded information.

    Amend one may satisfy the first verdict while its fresh verifier finds a
    different concrete discrepancy. The state machine spends attempt two from
    that latest verdict and permits either amended verification to integrate,
    but a failed final verdict after attempt two is terminal (issue #97).
    """

    # Read the complete verifier-informed repair state machine.
    step = _step(9)

    # Spend two named attempts from successive complete verdicts, then stop.
    assert "at most two verifier-informed amends" in step
    assert "immediately preceding verifier's verdict pasted whole" in step
    assert "attempt 1's fresh verdict is a fail" in step
    assert "spend attempt 2" in step
    assert "Attempt 1 never exhausts" in step
    assert "A pass after either attempt" in step
    assert "failed final verification after attempt 2" in step
    assert "no attempt 3" in step


def test_the_continuation_keeps_the_full_verdict_rule_and_fresh_sessions() -> None:
    """An #89-shaped list of actionable findings remains one strict verdict.

    The continuation builder receives every finding verbatim, while its fresh
    verifier receives the ordinary full brief without earlier verdicts or
    builder reports. Several fixable findings never soften a fail or let the
    amender approve its own work (issue #97).
    """

    # Read the amend loop and its one shared building template.
    step = _step(9)
    amend = _brief("amend.md")

    # Keep the latest verdict whole for the builder and out of verification.
    assert "never a summary or an accumulation" in step
    assert "fresh building subagent" in step
    assert "fresh verdict subagent" in step
    assert "`verify.md` unchanged" in step
    assert "no builder report, earlier verdict, or amend history" in step
    assert "Every command it says failed and every criterion" in amend
    assert "pass only when every gate command and acceptance criterion passes" in step


def test_amend_recovery_uses_the_recorded_phase_without_minting_an_attempt() -> None:
    """A marker written before dispatch survives every interruption boundary.

    Plan exposes the exact spent count and amend returns the attempt it wrote,
    so resumption continues the recorded builder or verifier phase instead of
    spending the next opportunity on the same verdict (issue #97).
    """

    # Read the state transition and final Report contract together.
    step = _step(9)
    report = _step(12)

    # Resume the numbered phase and render its terminal meaning from disk.
    assert "`amends_spent`" in step
    assert "`amend_state`" in step
    assert "`attempt`" in step
    assert "--attempt <1-or-2>" in step
    assert "--phase building" in step
    assert "--phase verifying" in step
    assert "--phase passed" in step
    assert "--phase failed" in step
    assert "--verdict-file <path>" in step
    assert "`newly_recorded` false" in step
    assert "resume that recorded attempt" in step
    assert "Never call `amend` with a different attempt for the same verdict" in step
    assert "`amends_spent`" in report
    assert "exhausted verification-repair path" in report
    assert "failed before an available continuation amend completed" in report


def test_a_ceiling_of_one_waits_for_the_continuation_verdict() -> None:
    """No later ticket may build on work still inside either amend attempt.

    Direct-branch work remains in the current wave until a passing final
    verdict or terminal outcome; isolated continuation work remains confined
    to its ticket's existing allocation and cannot leak into siblings.
    """

    # Read the wave accounting boundary around amendment.
    amend = _step(9)
    integrate = _step(8)

    # Keep direct work pending and isolated work ticket-local until a verdict.
    assert "At a concurrency ceiling of one" in amend
    assert "no later ticket starts" in amend
    assert "same working tree, scratch directory, reservations" in amend
    assert "Nothing from one ticket's amend enters a sibling's" in amend
    assert "a failed verdict having gone through step 9 first" in integrate


def test_an_isolated_continuation_does_not_block_a_passing_siblings_accounting() -> (
    None
):
    """A ticket awaiting amend two does not serialize an already-passing sibling.

    Isolated worktrees let the run account for an independent ticket whose
    verdict already passed while another ticket receives its continuation.
    The flow must make that possible rather than merely promise it after
    imposing starting-order serialization (issue #97).
    """

    # Read the accounting flow and the continuation's worktree exception.
    integrate = _step(8)
    amend = _step(9)

    # Account a known passing sibling without waiting for the failed ticket.
    assert "without waiting for its step 9 result" in integrate
    assert "whose verdict already passed" in integrate
    assert "With worktrees" in integrate
    assert "unrelated completed tickets may still be accounted for" in amend


def test_the_manpage_describes_the_two_amend_bound_and_report_states() -> None:
    """Help distinguishes a spent continuation from unrelated failure paths."""

    # Read the public failure and outcome descriptions.
    failures = _manpage_section("FAILURES AND COLLISIONS")
    failed = _manpage_entry("OUTCOMES", "**failed**")

    # State the finite bound and the Report distinction a maintainer sees.
    assert "at most two verifier-informed amends" in failures
    assert "second amend" in failures
    assert "no third amend" in failures
    assert "`amends_spent`" in failed
    assert "exhausted" in failed
    assert "failed before an available continuation" in failed


def test_the_report_step_states_the_runs_conduct() -> None:
    """Act between waves, report once, lead with what is done and what is left.

    One interviewed developer got masses of information when what they wanted
    was for the work to be done (ADR-0070, issue #74).
    """

    step = _step(12)

    assert "between waves" in step, (
        f"{SKILL / 'SKILL.md'}: step 12 says what the run had standing to do"
        f" it has already done, between waves — a question at the far end is"
        f" the plan-time rule broken twice (ADR-0070)."
    )
    assert "what is done" in step, (
        f"{SKILL / 'SKILL.md'}: step 12 leads with what is done and what is"
        f" left for the developer, which is the report the interviewed"
        f" developer asked for (ADR-0070)."
    )
    assert "never as questions awaiting answers" in step, (
        f"{SKILL / 'SKILL.md'}: step 12 states findings as a list of"
        f" statements, never as questions awaiting answers — nobody is there"
        f" to answer, and the report is not a conversation (ADR-0070)."
    )
    assert "or mid-run" in step, (
        f"{SKILL / 'SKILL.md'}: step 12 names the tickets parked mid-run"
        f" beside the ones step 3 parked — a mid-run park the report cannot"
        f" name is a ticket the developer would not know to answer"
        f" (issue #74)."
    )


def test_the_manpage_describes_the_triage_of_a_stop() -> None:
    """The page said only that nothing integrates a stopped builder's ticket.

    A reader deciding whether to run the night unattended needs to know a
    wrong path costs a retry, not a ticket (ADR-0070, issue #74).
    """

    where = SKILL / "help.md"
    section = _manpage_section("BUILDER STOPS")

    assert "Mechanical hinder" in section, (
        f"{where}: the manpage names the mechanical hinder the run repairs"
        f" itself before dispatching the same brief once more (ADR-0070)."
    )
    assert "deterministic environment problem" in section, (
        f"{where}: the manpage confines a hinder to a deterministic"
        f" environment problem rather than a decision about the work"
        f" (ADR-0070)."
    )
    assert "parks the ticket" in section, (
        f"{where}: the manpage says a genuine decision parks the ticket"
        f" instead of guessing or failing it (ADR-0070)."
    )
    assert "failure path" in section, (
        f"{where}: the manpage routes every remaining stop through the"
        f" verification-failure path and its amend (issue #74)."
    )


def test_the_manpage_documents_the_open_decision_exception_to_yes() -> None:
    """The `--yes` entry promised every question an answer of yes; an open
    decision is now the documented exception, parked rather than guessed."""

    text = (SKILL / "help.md").read_text(encoding="utf-8")
    where = SKILL / "help.md"
    yes_entry = _manpage_entry("OPTIONS", "**--yes**")

    assert "parked" in yes_entry, (
        f"{where}: the `--yes` entry documents the exception — a ticket whose"
        f" text leaves a decision open is parked rather than answered, the"
        f" flag answering yes/no and *which default?* not being one"
        f" (ADR-0070)."
    )
    assert "needs-info" in text, (
        f"{where}: the manpage names the label a parked ticket is returned"
        f" under, so a developer reading the morning tracker knows what the"
        f" swap was and how to bring the ticket back (ADR-0070)."
    )


def test_the_wave_brief_reads_the_branch_for_coherence_beside_its_gate() -> None:
    """Five of six branch-level readings found defects the green gate never saw.

    A decision record asserting a default the branch had just changed, one
    release section holding two of the same heading, a register still listing
    findings the branch had closed, citations the branch's own edits
    invalidated — nothing a test suite sees, and a ticket forked before a
    sibling's record landed could not have seen it either, so the integrated
    branch is the one place it can be read (ADR-0072, issue #78).
    """

    text = _brief("wave.md")
    where = SKILL / "references" / "wave.md"

    assert "the branch agreeing with itself" in text, (
        f"{where}: the brief says what coherence means — the branch agreeing"
        f" with itself — beside its instruction to run the gate. A checker"
        f" told only to run commands reads nothing (ADR-0072)."
    )
    assert "one number answers twice" in text, (
        f"{where}: the brief names registries where one number answers twice."
        f" Two tickets forked apart mint the same record number, and git"
        f" merges the pair without a word (ADR-0072)."
    )
    assert "two of the same heading" in text, (
        f"{where}: the brief names release-notes structure — one release"
        f" section holding two of the same heading, the collision a clean"
        f" merge leaves and nobody reads twice (ADR-0072)."
    )
    assert "citations the branch's own edits invalidated" in text, (
        f"{where}: the brief names the citations the branch's own edits"
        f" invalidated. The field case broke the pointer inside the release"
        f" procedure's own pre-tag checklist (ADR-0072, issue #78)."
    )
    assert "made false" in text, (
        f"{where}: the brief names prose asserting what the branch's own"
        f" changes have made false — the decision record still stating the"
        f" default the branch just changed (ADR-0072)."
    )


def test_the_wave_briefs_verdict_has_three_shapes() -> None:
    """A clean pass, mechanical findings, or a stop — and nothing softer.

    Mechanical means the fix restates what the branch already decided; a
    finding that requires choosing between two tickets' intents is a
    disagreement merged onto the branch, and building the rest of the night
    on it is the outcome the check exists to prevent (ADR-0072).
    """

    text = _brief("wave.md")
    where = SKILL / "references" / "wave.md"

    assert "A clean pass" in text, (
        f"{where}: the verdict's first shape is a clean pass — gate and"
        f" reading both found nothing — and only that continues the run"
        f" (ADR-0072)."
    )
    assert "Mechanical findings" in text, (
        f"{where}: the verdict's second shape is mechanical findings, the"
        f" kind a separate session fixes by restating what the branch"
        f" already decided (ADR-0072)."
    )
    assert "restates what the branch has already decided" in text, (
        f"{where}: the brief defines mechanical — the fix restates what the"
        f" branch has already decided. Without the definition every finding"
        f" is whatever the checker calls it (ADR-0072)."
    )
    assert "where it stands" in text, (
        f"{where}: each finding is named with where it stands, so a fixer"
        f" that has not read the branch can find it (ADR-0072)."
    )
    assert "what the branch already decided that it contradicts" in text, (
        f"{where}: each finding names what the branch already decided that"
        f" it contradicts, which is the whole of what a mechanical fix may"
        f" restate (ADR-0072)."
    )
    assert "choosing between two tickets' intents" in text, (
        f"{where}: the brief says a finding that requires choosing between"
        f" two tickets' intents is a stop, exactly as a failed gate is —"
        f" that is a disagreement merged onto the branch (ADR-0072)."
    )
    assert "a verdict you are not sure of is a stop" in text, (
        f"{where}: the brief keeps the old rule's spine in the new verdict —"
        f" a verdict the checker is not sure of is a stop, never something"
        f" softer (ADR-0072)."
    )


def test_the_wave_brief_still_changes_nothing_and_never_fixes() -> None:
    """The checker reads; a separate session fixes; the finder is never the fixer.

    What licenses the fixer's commit ahead of a verdict is that the check
    that demanded it reads the result, so the change-nothing rule stays true
    of the checker itself (ADR-0072).
    """

    text = _brief("wave.md")
    where = SKILL / "references" / "wave.md"

    assert "Change nothing" in text, (
        f"{where}: the brief still forbids the checker to change anything."
        f" The coherence reading widens what it reads, never what it may"
        f" touch (ADR-0072)."
    )
    assert "a repair made here is a repair nobody verified" in text, (
        f"{where}: the brief keeps the reasoning that forbids the checker to"
        f" fix — a repair made here is a repair nobody verified — which the"
        f" loop answers rather than drops (ADR-0072)."
    )
    assert "the finder is never the fixer" in text, (
        f"{where}: the brief says the finder is never the fixer, in those"
        f" words. A checker that fixes is a repair nobody reads (ADR-0072)."
    )


def test_the_wave_brief_carries_the_reading_warning() -> None:
    """A correction convention preserves the false sentence verbatim, so a grep reports noise.

    The cheap implementation fails silently in exactly the direction the
    check exists to catch — confident wrongness on the branch (ADR-0072).
    """

    text = _brief("wave.md")
    where = SKILL / "references" / "wave.md"

    assert "preserve the false sentence verbatim" in text, (
        f"{where}: the brief warns that a correction convention can preserve"
        f" the false sentence verbatim and append the correction after it"
        f" (ADR-0072)."
    )
    assert "cannot tell a corrected assertion from an uncorrected one" in text, (
        f"{where}: the brief says what the convention does to a pattern"
        f" search — it cannot tell a corrected assertion from an uncorrected"
        f" one (ADR-0072)."
    )
    assert "read the surrounding text" in text, (
        f"{where}: the brief tells the checker to read the surrounding text"
        f" rather than grep, or it reports noise (ADR-0072)."
    )


def test_the_fix_brief_hands_the_fixer_the_findings_whole() -> None:
    """A finding trimmed in the retelling is a fix aimed at half of it."""

    text = _brief("fix.md")
    where = SKILL / "references" / "fix.md"
    instructions = text.split("\n---\n", 1)[0]

    assert "`<findings>`" in text, (
        f"{where}: the brief carries the wave check's findings. A fixer told"
        f" nothing of them rereads the branch, and the reader that finds is"
        f" never the writer that fixes (ADR-0072)."
    )
    assert "pasted whole" in instructions, (
        f"{where}: the fill-in instructions say the findings are pasted"
        f" whole rather than summarised — a summary is the orchestrator's"
        f" reading, not what the checker found (ADR-0072)."
    )


def test_the_fix_brief_states_the_mandate_as_the_record_states_it() -> None:
    """Restate what the branch decided, choose nothing.

    The mandate is a boundary that must hold in prose, and a fixer that
    drifts past it is caught only by the next check round (ADR-0072).
    """

    text = _brief("fix.md")
    where = SKILL / "references" / "fix.md"

    assert "estate what the branch decided, choose nothing" in text, (
        f"{where}: the brief states the mandate as the record states it —"
        f" restate what the branch decided, choose nothing (ADR-0072)."
    )
    assert "choosing between two tickets' intents" in text, (
        f"{where}: the brief names the finding that is not the fixer's — one"
        f" whose fix requires choosing between two tickets' intents"
        f" (ADR-0072)."
    )
    assert "name the choice" in text, (
        f"{where}: the brief says such a finding is left as it stands and"
        f" the choice named in the report, the run stopping on it as on a"
        f" failed gate (ADR-0072)."
    )


def test_the_fix_brief_commits_for_the_next_round_to_read() -> None:
    """The wave check reads the branch, so a fix only a working tree holds goes unread."""

    text = _brief("fix.md")
    where = SKILL / "references" / "fix.md"

    assert "leaving nothing uncommitted" in text, (
        f"{where}: the brief has the fixer commit on the branch, leaving"
        f" nothing uncommitted — the next check round reads the branch, not"
        f" a working tree (ADR-0072)."
    )
    assert "touch no branch other than" in text, (
        f"{where}: the brief confines the fixer to the branch the findings"
        f" stand on, as every other brief confines its subagent to what it"
        f" was given (ADR-0072)."
    )
    assert "gate and coherence both" in text, (
        f"{where}: the brief says the wave check runs again on the result —"
        f" gate and coherence both — which is what licenses a commit ahead"
        f" of a verdict: no fix escapes unread (ADR-0072)."
    )


def test_the_wave_step_loops_check_fix_check_to_a_fixed_point() -> None:
    """This class of defect never comes alone, so one fix-and-recheck round is not enough.

    Every field round that fixed one instance found another the first
    reading had not reached — the framing paragraph behind the annotated
    one, the second stale citation behind the first (ADR-0072).
    """

    step = _step(11)

    assert "fix.md" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 dispatches the fixer from"
        f" `$HERE/references/fix.md` on mechanical findings — the finding"
        f" session never fixes (ADR-0072)."
    )
    assert "findings pasted whole" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 fills the fixer's brief with the"
        f" findings pasted whole, so the fixer works from what the checker"
        f" found rather than a retelling (ADR-0072)."
    )
    assert "the finder is never the fixer" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 says the finder is never the fixer,"
        f" in those words — the fixer is a fresh subagent, never the"
        f" checking one (ADR-0072)."
    )
    assert "gate and coherence both" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 reruns the whole check after a fix —"
        f" gate and coherence both — so no fix escapes unread and the branch"
        f" the run continues from has passed a full check whole (ADR-0072)."
    )
    assert "a round finds nothing" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 ends the loop when a round finds"
        f" nothing. A single fix-and-recheck round ships whatever the first"
        f" reading missed with a green stamp on it (ADR-0072)."
    )
    assert "a round changes nothing" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 stops the run when a round changes"
        f" nothing — findings repeating with no fix the fixer can make is"
        f" the non-mechanical case wearing the mechanical one's clothes"
        f" (ADR-0072)."
    )


def test_the_wave_step_stops_on_a_choice_as_on_a_failed_gate() -> None:
    """Only a clean pass continues the run; a choice stops it exactly as a failure does."""

    step = _step(11)

    assert "A clean pass:" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 continues to the next wave only on a"
        f" clean pass — gate green and the reading finding nothing"
        f" (ADR-0072)."
    )
    assert "choice between two tickets' intents" in step, (
        f"{SKILL / 'SKILL.md'}: step 11 stops the run on a finding that is a"
        f" choice between two tickets' intents — a disagreement merged onto"
        f" the branch, not something a restatement settles (ADR-0072)."
    )


def test_the_manpage_describes_the_wave_loop_and_what_stops_it() -> None:
    """A developer reading the page has to know the branch check fixes as well as reads.

    The loop commits to the developer's branch between waves, which the old
    page's account — verification runs once, a failure stops the run — did
    not say could happen (ADR-0072).
    """

    where = SKILL / "help.md"
    entry = _manpage_entry("TICKET EXECUTION", "**Integrate**")

    assert "coherence" in entry, (
        f"{where}: the manpage says the post-merge check reads the branch"
        f" for coherence as well as running the verification (ADR-0072)."
    )
    assert "another subagent" in entry, (
        f"{where}: the manpage says another subagent fixes mechanical"
        f" coherence findings, keeping the finder separate from the fixer"
        f" (ADR-0072)."
    )
    assert "until a round is clean" in entry, (
        f"{where}: the manpage says the loop ends only when a round is clean,"
        f" so the reader knows what a clean pass means"
        f" (ADR-0072)."
    )
    assert "makes no progress stops the run" in entry, (
        f"{where}: the manpage says a non-progressing fix stops the run beside"
        f" a failed gate and an unresolved choice (ADR-0072)."
    )


def test_the_build_step_routes_a_discovered_edge_to_the_blocked_outcome() -> None:
    """A builder that finds its ticket depends on unresolved work the graph
    does not name found a missing edge, not a failure — the run corrects the
    graph and steps back rather than burning the ticket (ADR-0073, issue #79).
    """

    step = _step(6)

    assert "whether the missing thing has a number" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 states the boundary against parking —"
        f" a ticket without a done resolution is an edge, and an answer no"
        f" ticket carries is a question parked under ADR-0070 (ADR-0073)."
    )
    assert "a ticket without a done Ticket Resolution is an edge" in step
    assert "--outcome blocked" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 routes a discovered dependency to the"
        f" engine's blocked outcome, which writes the corrected edge rather"
        f" than a failure (ADR-0073)."
    )
    assert "without spending the ticket's one rebuild" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says the half-built tree is discarded"
        f" as a refused repair is while the rebuild stays unspent — the two"
        f" bounds answer different failures (ADR-0073, ADR-0069)."
    )
    assert "when its blocker has a done Ticket Resolution" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 says a blocked ticket is offered again"
        f" when its blocker has a done Ticket Resolution, the corrected edge being the whole"
        f" of the memory the mechanism needs (ADR-0073)."
    )
    assert "a done Ticket Resolution unblocking whatever waited on it" in _step(11)


def test_the_building_brief_stops_on_unresolved_work_the_ticket_does_not_name() -> None:
    """The builder's vocabulary was build or stop-and-fail, and the third move
    it invented — the scope quietly narrowed inside the commit — is exactly
    what verification exists to catch (ADR-0073, issue #79).
    """

    brief = _brief("brief.md")
    where = SKILL / "references" / "brief.md"

    assert "another ticket without a done Ticket Resolution" in brief, (
        f"{where}: the brief follows current resolution rather than tracker"
        f" closure when it identifies missing dependency work (ADR-0079)."
    )
    assert "stop and name the ticket it waits on" in brief, (
        f"{where}: the brief tells the builder the move exists — a dependency"
        f" on unresolved work the ticket does not name is stopped on and named"
        f" (ADR-0073)."
    )
    assert "Never build around it" in brief, (
        f"{where}: the brief forbids building around the missing work — a"
        f" torso completed around a hole is what the discarded tree replaces"
        f" (ADR-0073)."
    )
    assert "never narrow the scope" in brief, (
        f"{where}: the brief forbids narrowing the scope inside the commit,"
        f" which is exactly the case the verification verdict exists to catch"
        f" (ADR-0073)."
    )


def test_the_manpage_accounts_for_the_blocked_outcome() -> None:
    """A developer reading the morning's graph has to know a run can write an
    edge, and where to look for it (ADR-0073, issue #79).
    """

    where = SKILL / "help.md"
    edge = _manpage_entry("BUILDER STOPS", "**Discovered dependency**")
    outcomes = _manpage_section("OUTCOMES")

    assert "another ticket without a done Ticket Resolution" in edge, (
        f"{where}: the discovered-dependency entry limits the blocked outcome"
        f" to missing work carried by an unresolved ticket (ADR-0073)."
    )
    assert "writes the missing blocking edge" in edge, (
        f"{where}: the manpage says the run corrects the tracker graph with"
        f" the missing blocking edge (ADR-0073)."
    )
    assert "after its blocker has a done Ticket Resolution" in edge, (
        f"{where}: the manpage says the blocked ticket is offered again after"
        f" its blocker resolves done, rather than being settled (ADR-0073)."
    )
    assert "rather than in a sixth category" in outcomes, (
        f"{where}: the manpage keeps the report at five lists — a blocked"
        f" ticket follows the outcome implied by its blocker (ADR-0073)."
    )


def test_the_manpages_describe_reconciled_done_without_run_provenance() -> None:
    """Report groups on current Ticket Resolution while an external repair
    remains visibly outside Orchestrate's build and verification history."""

    # Read the root outcome contract and the addressed Reconciliation page.
    outcomes = _manpage_section("OUTCOMES")
    done = _manpage_entry("OUTCOMES", "**done**")
    reconcile = (SKILL / "help" / "reconcile.md").read_text(encoding="utf-8")

    # Define the grouping before describing either provenance path under done.
    assert "Report groups tickets by their current Ticket Resolution" in outcomes
    assert "completed outside Orchestrate" in done
    assert "unsuccessful Run Outcome" in done
    assert "does not claim Orchestrate built or independently verified" in done

    # Distinguish lifecycle recovery from a complete idempotent repeat.
    assert "interrupted" in reconcile
    assert "lifecycle repair" in reconcile
    assert "rather than agreement" in reconcile


def test_the_final_report_renders_reconciliation_provenance() -> None:
    """The Skill renders the engine's historical provenance instead of
    silently dropping it from the maintainer-facing Report."""

    # Read the execution contract for the final public report.
    report_step = _step(12)

    # Render both provenance fields and their external-completion meaning.
    assert "`run_outcome`" in report_step
    assert "`is_reconciled`" in report_step
    assert "completed outside Orchestrate" in report_step
    assert "not built or independently verified by Orchestrate" in report_step


def test_invalid_reconcile_form_routes_to_reconcile_synopsis() -> None:
    """Once the subcommand is recognized, its own grammar and help route make
    a malformed invocation actionable without showing unrelated run forms."""

    # Read the shipped parser instructions as the installed agent receives them.
    instructions = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    # Route recognized malformed forms to the addressed subcommand contract.
    assert "invalid recognized `reconcile` form" in instructions
    assert "`$HERE/help/reconcile.md`" in instructions
    assert "`/orchestrate reconcile --help`" in instructions


# Every brief that tells its subagent to run the project's verification gate.
# Before issue #80 each of them resolved *every command its contributing guide
# names for a change* alone, from scratch — nine resolutions over one
# interviewed tree — and the open-ended phrasing invited discovery beyond the
# list: one wave check found and ran a twenty-five-minute rendering rig no
# guide had named as a gate. The orchestrator now resolves the list once, at
# run start, and these briefs carry it.
GATE_CARRYING_BRIEFS = (
    "verify.md",
    "repair.md",
    "repaired.md",
    "wave.md",
    "amend.md",
)


def test_every_gate_brief_carries_the_gate_rather_than_rediscovering_it() -> None:
    """The gate travels into the brief; the phrase every subagent resolved alone is gone.

    Each of these briefs told its subagent to run every command the project's
    contributing guide names for a change, and each subagent resolved that
    phrase from scratch — nine times over the same tree in one interviewed
    wave (issue #80).
    """

    for name in GATE_CARRYING_BRIEFS:
        text = _brief(name)
        where = SKILL / "references" / name

        assert "`<gate>`" in text, (
            f"{where}: the brief carries the gate the orchestrator resolved"
            f" at run start. A subagent handed no list derives one, and each"
            f" derivation is a fresh reading of the same guide (issue #80)."
        )
        assert (
            "resolved once at run start from the project's contributing guide" in text
        ), (
            f"{where}: the brief says where the list came from — resolved"
            f" once at run start from the project's contributing guide — so"
            f" the subagent reads it as settled rather than as a starting"
            f" point for its own reading (issue #80)."
        )
        assert "every command its contributing guide names" not in text, (
            f"{where}: the brief no longer tells its subagent to resolve the"
            f" guide's commands itself — that phrase is the one every"
            f" subagent resolved alone, from scratch (issue #80)."
        )
        assert "If there is no such guide" not in text, (
            f"{where}: the no-guide fallback is the orchestrator's to resolve"
            f" at run start, not the subagent's — a brief that carries it"
            f" invites the rediscovery the carried gate exists to end"
            f" (issue #80)."
        )


def test_every_gate_brief_keeps_the_all_of_them_force_and_refuses_discovery() -> None:
    """All of them, not a subset — and nothing the list does not name.

    The strictness the carried list must not trade away is that the whole
    gate runs; what it adds is that a subagent no longer goes looking for
    more — the open-ended phrasing is how one wave check spent twenty-five
    minutes on a rig no guide named as a gate (issue #80).
    """

    for name in GATE_CARRYING_BRIEFS:
        text = _brief(name)
        where = SKILL / "references" / name

        assert "all of them, not a subset" in text, (
            f"{where}: the brief keeps the all-of-them force — run all of"
            f" them, not a subset. The carried list changes where the gate"
            f" comes from, never how much of it runs (issue #80)."
        )
        assert "a check this list does not name is not run in its place" in text, (
            f"{where}: the brief refuses discovery in those words — a check"
            f" the list does not name is not run in its place. Without the"
            f" refusal the list is a starting point, and a subagent that"
            f" goes looking finds a rig nothing asked for (issue #80)."
        )


def test_every_gate_briefs_fill_in_instructions_take_the_list() -> None:
    """A placeholder nothing explains is handed out unfilled."""

    for name in GATE_CARRYING_BRIEFS:
        instructions = _instructions(name)
        where = SKILL / "references" / name

        assert "`<gate>`" in instructions, (
            f"{where}: the fill-in instructions say what `<gate>` is replaced"
            f" with — the gate as the orchestrator resolved it at run start"
            f" (issue #80)."
        )
        assert "never re-derived" in instructions, (
            f"{where}: the fill-in instructions forbid re-deriving the list"
            f" at fill time — the resolution happened once, at run start,"
            f" and filling a brief is not a second reading of the guide"
            f" (issue #80)."
        )


def test_the_build_step_resolves_the_gate_once_at_run_start() -> None:
    """The orchestrator reads the contributing guide once and every brief carries the answer.

    Which commands gate a change is a reading of prose, like which files are
    the run's own — so it is made once, at run start, and held for the whole
    run rather than re-made by every subagent (issue #80).
    """

    step = _step(6)

    assert "esolve the gate" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 has the orchestrator resolve the gate"
        f" before the first wave is briefed. Left to the briefs, the same"
        f" phrase is resolved by every subagent over the same tree"
        f" (issue #80)."
    )
    assert "verbatim" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 takes the guide's commands verbatim —"
        f" the gate is what the guide names, not the orchestrator's reading"
        f" of what it meant (issue #80)."
    )
    assert "lint, format, and type checks the project is configured for" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 carries the no-guide fallback the"
        f" briefs used to state — the whole test suite and the checks the"
        f" project is configured for — because the fallback moved here"
        f" rather than being dropped (issue #80)."
    )
    assert "every brief that asks for verification" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 fills the resolved gate into every"
        f" brief that asks for verification, which is what makes one"
        f" resolution the run's rather than one subagent's (issue #80)."
    )
    assert "all of it and nothing in its place" in step, (
        f"{SKILL / 'SKILL.md'}: step 6 keeps the strictness beside the new"
        f" source — the list is the gate wherever it is carried, all of it"
        f" and nothing in its place (issue #80)."
    )


# The two verifying briefs that read acceptance criteria. A ticket whose body
# ends *deliver as a PR against the default branch* is unsatisfiable by
# construction: the building brief forbids the push, and a verifier told to
# check every criterion must fail the ticket for the builder's obedience. In
# one interviewed run that sentence ended a twelve-ticket night at ticket one,
# and two sibling tickets carried the same line (issue #82).
CRITERIA_READING_BRIEFS = (
    "verify.md",
    "repaired.md",
)


def _delivery_paragraph(text: str) -> str:
    """The paragraph of a brief that excludes delivery lines from the criteria, or the empty string."""

    for paragraph in text.split("\n\n"):
        if "not an acceptance criterion" in paragraph:
            return paragraph.strip()
    return ""


def test_every_criteria_reading_brief_excludes_the_delivery_channel() -> None:
    """A delivery clause the builder obeyed must not be a criterion the verifier fails.

    The building brief forbids the push, and the verifier had no licence to
    skip the line asking for it, so a correctly built ticket failed for the
    builder's obedience — and at a ceiling of one, that one sentence about
    delivery stopped the whole run (issue #82).
    """

    for name in CRITERIA_READING_BRIEFS:
        text = _brief(name)
        where = SKILL / "references" / name

        assert "prescribing the delivery channel" in text, (
            f"{where}: the brief names what is excluded — a line prescribing"
            f" the delivery channel. Without the exclusion the ticket is"
            f" unsatisfiable by construction: the builder may not do the one"
            f" thing the line asks (issue #82)."
        )
        assert "a pull request, a push, a release" in text, (
            f"{where}: the brief names the shapes a delivery line takes — a"
            f" pull request, a push, a release — so the exclusion is read as"
            f" the channel rather than as whatever the verifier decides it"
            f" covers (issue #82)."
        )
        assert "not an acceptance criterion" in text, (
            f"{where}: the brief says such a line is not an acceptance"
            f" criterion, in those words — the rule that every criterion is"
            f" checked stands, and this line is simply not one (issue #82)."
        )
        assert "delivery is the run's boundary" in text, (
            f"{where}: the brief says why — delivery is the run's boundary:"
            f" the run integrates into the branch, and publishing is the"
            f" developer's move after it (issue #82)."
        )
        assert "Note the clause in your report" in text, (
            f"{where}: the brief has the verifier note the clause in its"
            f" report, so the developer learns the ticket carried one rather"
            f" than the line vanishing without a word (issue #82)."
        )
        assert "take your verdict from the rest" in text, (
            f"{where}: the brief says the verdict is taken from the rest of"
            f" the ticket — excluded means excluded from the verdict, not"
            f" softened into a reservation (issue #82)."
        )


def test_the_briefs_state_the_delivery_exclusion_in_one_wording() -> None:
    """One rule stated two ways is two rules, and a verifier obeys the one it was given.

    The briefs are handed out one per subagent, so nothing but identical
    wording keeps a ticket's verifier and a repair's verifier held to the
    same exclusion.
    """

    stated = {
        name: _delivery_paragraph(_brief(name)) for name in CRITERIA_READING_BRIEFS
    }
    wordings = set(stated.values())

    assert "" not in wordings, (
        f"{SKILL / 'references'}: every criteria-reading brief states the"
        f" delivery exclusion in a paragraph of its own. These state none: "
        f"{sorted(name for name, rule in stated.items() if not rule)}."
    )
    assert len(wordings) == 1, (
        f"{SKILL / 'references'}: every criteria-reading brief states the"
        f" delivery exclusion in the same wording, so the briefs state one"
        f" rule rather than one each. These differ: {sorted(stated)}."
    )


def test_the_building_brief_mirrors_the_delivery_exclusion() -> None:
    """The builder is told from its own side what the verifier is told from its.

    A builder that reads *deliver as a PR* beside *do not push* holds a
    contradiction, and its brief's stop-rather-than-guess rule makes that a
    stop over a line that was never the work (issue #82).
    """

    text = _brief("brief.md")
    where = SKILL / "references" / "brief.md"

    assert "prescribing the delivery channel" in text, (
        f"{where}: the brief names the delivery line so the builder knows"
        f" which instruction the mirror sentence is about (issue #82)."
    )
    assert "not a requirement to build toward" in text, (
        f"{where}: the brief says a delivery instruction is not a requirement"
        f" to build toward — the builder may not push, so building toward it"
        f" is building toward a forbidden act (issue #82)."
    )
    assert "not a decision to stop over" in text, (
        f"{where}: the brief says the line is not a decision to stop over —"
        f" without that, the stop-rather-than-guess rule reads the"
        f" contradiction as a genuine decision and parks the ticket"
        f" (issue #82)."
    )
    assert "delivered by being integrated" in text, (
        f"{where}: the brief says how the work actually leaves the session —"
        f" it is delivered by being integrated — so the builder reads the"
        f" exclusion as settled rather than as a gap (issue #82)."
    )


def test_the_manpage_says_delivery_lines_are_not_criteria() -> None:
    """A developer reading the page has to know a delivery line cannot fail a ticket.

    The interviewed developer's fix was to edit the clause out of three
    issue bodies by hand; a reader of the page should know no such edit is
    needed (issue #82).
    """

    where = SKILL / "help.md"
    entry = _manpage_entry("TICKET EXECUTION", "**Verify**")

    assert "Delivery requests" in entry, (
        f"{where}: the verification entry identifies delivery requests"
        f" separately from acceptance criteria (issue #82)."
    )
    assert "do not change the verdict" in entry, (
        f"{where}: the manpage says delivery requests do not change the"
        f" verdict because delivery is outside the Skill (issue #82)."
    )


def test_the_build_step_uses_the_frozen_execution_decision() -> None:
    """Model-selector, not prose judgment, owns the exact builder configuration."""

    step = _step(6)

    assert "selected exact Harness-native model and deliberation controls" in step
    assert "locks only model" in step
    assert "`--deliberation` only deliberation" in step


def test_every_verdict_step_names_the_orchestrators_own_model() -> None:
    """Ticket verification, amended verdicts, repair verification, and the wave check.

    The verifiers on the inherited arrangement were the strongest part of
    every interviewed run, and the verdict is the only thing standing between
    an unattended night and a report the developer cannot trust (ADR-0074).
    """

    for number in (7, 9, 10, 11):
        step = _step(number)

        assert "exact inherited main-seat" in step or "exact inheritance" in step, (
            f"{SKILL / 'SKILL.md'}: step {number} runs its verdict on the"
            f" orchestrator's own model. A verdict sent down the ladder takes"
            f" the saving at the last thing that would catch a mistake"
            f" (ADR-0074)."
        )


def test_the_verify_step_states_exact_main_seat_inheritance() -> None:
    """Verdict authority carries the complete configuration rather than a model name."""

    step = _step(7)

    assert (
        "exact inheritance of the orchestrating session's complete main-seat model and deliberation configuration"
        in step
    )
    assert "no route, flag, circumstance, or failure may downgrade it" in step


def test_the_amend_and_repair_dispatches_delegate_as_builds_do() -> None:
    """Repairing a collision and amending a failed build are building.

    Left unnamed, the two dispatches keep the silent inheritance the build
    step just lost — and the amend carries a signal of its own: a ticket back
    for its amend has just demonstrated it was harder than it looked
    (ADR-0074, issue #83).
    """

    for number in (9, 10):
        step = _step(number)

        assert "frozen snapshot" in step, (
            f"{SKILL / 'SKILL.md'}: step {number} chooses its dispatch's model"
            f" as step 6 chooses a builder's, in those words — one judgment"
            f" stated once, not three drifting apart (ADR-0074)."
        )

    assert "bounded adjacent escalation" in _step(9)


def test_the_manpage_model_entry_carries_the_judged_default() -> None:
    """The flag keeps exactly its meaning; what changes is the default underneath it."""

    model_entry = _manpage_entry("OPTIONS", "**--model**")

    assert "Lock only the building model dimension" in model_entry
    assert "still selects deliberation" in model_entry
    assert "exact main-seat inheritance" in model_entry


def test_the_manpage_advises_running_from_the_strongest_model() -> None:
    """The Skill cannot choose the orchestrator's own seat, so the page says it instead.

    The session's model is the developer's move, and the run's judgment calls
    are only as good as the model asked to make them (ADR-0074, issue #83).
    """

    where = SKILL / "help.md"
    description = _manpage_section("DESCRIPTION")

    assert "most capable model" in description, (
        f"{where}: the description advises running the skill from the most"
        f" capable model available — the seat is the developer's move, so the"
        f" page is where it is said (ADR-0074)."
    )
    assert "only as reliable as that model" in description, (
        f"{where}: the description says why the seat matters — the run's"
        f" judgment calls are only as reliable as the selected model"
        f" (ADR-0074)."
    )


def test_the_manpage_says_the_gate_is_resolved_once() -> None:
    """A developer reading the page has to know what a verifier runs and who decided it."""

    where = SKILL / "help.md"
    entry = _manpage_entry("TICKET EXECUTION", "**Build**")

    assert "resolved once at the run's start" in entry, (
        f"{where}: the manpage says the gate is resolved once, at the run's"
        f" start, from the project's contributing guide — not rediscovered"
        f" by each verifying subagent (issue #80)."
    )
    assert "neither substitutes nor expands it" in entry, (
        f"{where}: the manpage says every verifier receives the exact gate and"
        f" neither substitutes nor expands it (issue #80)."
    )


def test_routing_is_a_preclaim_batch_and_verdicts_inherit_the_main_seat() -> None:
    """Route owns execution selection while the orchestrator retains verdict authority."""

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    model_entry = _manpage_entry("OPTIONS", "**--model**")
    deliberation_entry = _manpage_entry("OPTIONS", "**--deliberation**")

    assert 'kntnt.skills: "model-selector"' in skill
    assert skill.index("Before step 4") > skill.index("3. Before anything is claimed")
    assert "one versioned model-selector route request" in skill
    assert "complete main-seat model and deliberation configuration" in skill
    assert "selected exact Harness-native model and deliberation controls" in skill
    assert "Lock only the building model dimension" in model_entry
    assert "Lock only the building deliberation dimension" in deliberation_entry


def test_a_dry_run_preflights_routing_without_settling_ticket_decisions() -> None:
    """A dry run is an observable routing preview, never a tracker mutation."""

    step = _step(2)

    assert "read-only routing preflight" in step
    assert "proposed decisions and routing readiness" in step
    assert "without claiming, starting setup, or writing" in step
    assert "does not enter step 3" in step


def test_routing_covers_every_execution_and_verdict_dispatch_role() -> None:
    """Every builder is routed while every independent verdict retains the main seat."""

    execution_steps = {
        6: "initial builder",
        9: "amend",
        10: "collision repair",
        11: "mechanical wave fix",
    }
    verdict_steps = {
        7: "ticket verification",
        9: "amend verification",
        10: "repair verification",
        11: "wave checking",
    }

    for number, role in execution_steps.items():
        assert "selected exact" in _step(number), role

    assert "route the rebuild" in _step(10)

    for number, role in verdict_steps.items():
        assert "exact inherited main-seat" in _step(number), role
