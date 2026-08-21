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

    text = (SKILL / "help.md").read_text(encoding="utf-8")
    where = SKILL / "help.md"

    assert "the run's own to write" in text, (
        f"{where}: the manpage says some files are the run's to write rather"
        f" than any builder's, beside its account of worktrees and"
        f" integration (ADR-0071)."
    )
    assert "leaves it as a note" in text, (
        f"{where}: the manpage says a builder with an entry for such a file"
        f" leaves it as a note the run applies later, which is what a reader"
        f" of the diff would otherwise have to work out (ADR-0071)."
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

    text = (SKILL / "help.md").read_text(encoding="utf-8")
    where = SKILL / "help.md"

    assert "mechanical hinder" in text, (
        f"{where}: the manpage names the mechanical hinder the run repairs"
        f" itself before dispatching the same brief once more (ADR-0070)."
    )
    assert "decide anything about the work" in text, (
        f"{where}: the manpage states what separates a hinder from a decision"
        f" — whether fixing it decides anything about the work (ADR-0070)."
    )
    assert "the wave carries on without it" in text, (
        f"{where}: the manpage says a mid-run decision parks the ticket and"
        f" the wave carries on without it — a decision costs one ticket,"
        f" never the night (ADR-0070)."
    )
    assert "tried and found wanting" in text, (
        f"{where}: the manpage says the stop that stays a failure is the one"
        f" whose work was tried and found wanting, which the amend fronts"
        f" (issue #74)."
    )


def test_the_manpage_documents_the_open_decision_exception_to_yes() -> None:
    """The `--yes` entry promised every question an answer of yes; an open
    decision is now the documented exception, parked rather than guessed."""

    text = (SKILL / "help.md").read_text(encoding="utf-8")
    where = SKILL / "help.md"
    yes_entry = next(
        (line for line in text.splitlines() if line.startswith("- `--yes`")), ""
    )

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

    text = (SKILL / "help.md").read_text(encoding="utf-8")
    where = SKILL / "help.md"

    assert "coherence" in text, (
        f"{where}: the manpage says the post-merge check reads the branch"
        f" for coherence as well as running the verification (ADR-0072)."
    )
    assert "the finder is never the fixer" in text, (
        f"{where}: the manpage says a separate subagent fixes what the"
        f" check finds mechanical — the finder is never the fixer"
        f" (ADR-0072)."
    )
    assert "a round finds nothing" in text, (
        f"{where}: the manpage says the loop ends when a round finds"
        f" nothing, so the reader knows what a clean pass now means"
        f" (ADR-0072)."
    )
    assert "a round changes nothing" in text, (
        f"{where}: the manpage says the run stops when a round changes"
        f" nothing, beside the failed gate and the choice — the three"
        f" things that stop the loop (ADR-0072)."
    )
