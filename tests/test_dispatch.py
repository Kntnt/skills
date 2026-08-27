"""The execution and landing contract of the Dispatch Skill."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import NamedTuple

from support.contract import STANDARD, assert_contract_markers

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SKILL: Path = REPO_ROOT / "skills" / "code" / "dispatch"
BODY: Path = SKILL / "SKILL.md"
HELP: Path = SKILL / "help.md"
EXECUTOR: Path = SKILL / "references" / "executor.md"
REVIEW: Path = SKILL / "references" / "review.md"
RECOVERY: Path = SKILL / "references" / "recovery.md"
COMPILE_BODY: Path = REPO_ROOT / "skills" / "code" / "compile" / "SKILL.md"
COMPILE_HELP: Path = REPO_ROOT / "skills" / "code" / "compile" / "help.md"


class TrackerConvention(NamedTuple):
    """Provide one resolved repository tracker vocabulary."""

    executable_ready_label: str
    needs_info_label: str
    ready_for_human_label: str
    scope_label: str


class TrackerTransition(NamedTuple):
    """Name the behavioural columns in one published transition row."""

    trigger_notice: str
    label_delta: str
    assignment: str
    preserved: str


class MaterializedAttempt(NamedTuple):
    """Name the Git identities in one materialized executor fixture."""

    repository: Path
    index_path: Path
    base_tree: str
    expected_test_blob: str


def _git(
    repository: Path,
    *arguments: str,
    environment: dict[str, str] | None = None,
) -> str:
    """Run one real Git command in a fixture repository."""

    # Keep fixture commands isolated while retaining Git's normal environment.
    completed = subprocess.run(
        ("git", "-C", str(repository), *arguments),
        check=True,
        capture_output=True,
        env={**os.environ, **(environment or {})},
        text=True,
    )

    return completed.stdout.strip()


def _materialized_attempt(
    tmp_path: Path, *, replaces_test: bool
) -> MaterializedAttempt:
    """Create a repository whose canonical test is dispatcher-materialized."""

    # Establish the captured attempt base with or without an older test blob.
    repository = tmp_path / ("replacement" if replaces_test else "addition")
    repository.mkdir()
    _git(repository, "init", "--quiet")
    _git(repository, "config", "user.name", "Dispatch Fixture")
    _git(repository, "config", "user.email", "dispatch@example.test")
    (repository / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    if replaces_test:
        (repository / "test_seam.py").write_text(
            "assert VALUE == 0\n", encoding="utf-8"
        )
    _git(repository, "add", ".")
    _git(repository, "commit", "--quiet", "-m", "captured base")

    # Materialize canonical compiler bytes into a private dispatcher index.
    (repository / "test_seam.py").write_text("assert VALUE == 2\n", encoding="utf-8")
    index = repository / ".git" / "dispatch-materialized-index"
    environment = {"GIT_INDEX_FILE": str(index)}
    _git(repository, "read-tree", "HEAD", environment=environment)
    _git(repository, "add", "--", "test_seam.py", environment=environment)
    base_tree = _git(repository, "write-tree", environment=environment)
    expected_test_blob = _git(repository, "hash-object", "--", "test_seam.py")

    # Model one executor-owned change after the dispatcher materialization.
    (repository / "app.py").write_text("VALUE = 2\n", encoding="utf-8")

    return MaterializedAttempt(repository, index, base_tree, expected_test_blob)


def _capture_executor_patch(attempt: MaterializedAttempt) -> str:
    """Capture executor-owned paths against the materialized tree."""

    # Stage only executor-owned results into the materialized private index.
    environment = {"GIT_INDEX_FILE": str(attempt.index_path)}
    _git(attempt.repository, "add", "--", "app.py", environment=environment)

    return _git(
        attempt.repository,
        "diff",
        "--cached",
        "--binary",
        "--full-index",
        attempt.base_tree,
        "--",
        "app.py",
        environment=environment,
    )


def _verify_canonical_test_blob(attempt: MaterializedAttempt) -> None:
    """Reject a result whose separately inventoried test blob changed."""

    # Compare the destination directly with the canonical escrow identity.
    actual_blob = _git(attempt.repository, "hash-object", "--", "test_seam.py")
    if actual_blob != attempt.expected_test_blob:
        raise AssertionError("canonical test blob changed")


def _tracker_transition_rows() -> dict[str, TrackerTransition]:
    """Parse the published tracker transition table into executable fixture rows."""

    # Collect the behavioural columns for stable transition identifiers.
    rows: dict[str, TrackerTransition] = {}
    for line in RECOVERY.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `T-"):
            continue
        cells = tuple(cell.strip() for cell in line.strip("|").split("|"))
        rows[cells[0].strip("`")] = TrackerTransition(*cells[1:5])

    return rows


def _assert_tracker_convention(
    rows: dict[str, TrackerTransition],
    convention: TrackerConvention,
) -> None:
    """Project every transition through one non-default convention fixture."""

    # Resolve this fixture's lifecycle, preservation, and assignment facts.
    executable = convention.executable_ready_label
    needs_info = convention.needs_info_label
    ready_for_human = convention.ready_for_human_label
    scope = convention.scope_label
    initial_labels = {executable, scope, "priority-critical"}
    target_labels = {
        "T-LAND": None,
        "T-PARK-INFO": needs_info,
        "T-PARK-HUMAN": ready_for_human,
    }
    target_variables = {
        "T-LAND": "add nothing",
        "T-PARK-INFO": "add `needs_info_label`",
        "T-PARK-HUMAN": "add `ready_for_human_label`",
    }
    expected_assignments = {
        "T-LAND": ("octocat",),
        "T-PARK-INFO": (),
        "T-PARK-HUMAN": (),
    }

    # Execute all three symbolic rows through the resolved convention.
    for transition_id, target_label in target_labels.items():
        transition = rows[transition_id]
        projected_labels = initial_labels - {executable}
        if target_label is not None:
            projected_labels.add(target_label)
        projected_assignees = (
            ("octocat",) if transition.assignment == "Preserve" else ()
        )
        assert "Remove `executable_ready_label`" in transition.label_delta
        assert target_variables[transition_id] in transition.label_delta
        assert scope in projected_labels
        assert executable not in projected_labels
        assert projected_assignees == expected_assignments[transition_id]
        assert "`preserved_labels`" in transition.preserved
        assert "milestone" in transition.preserved

    # Keep published policy symbolic under this arbitrary vocabulary.
    text = RECOVERY.read_text(encoding="utf-8")
    assert all(label not in text for label in convention)


def test_live_and_dry_run_grammar_keep_confirmation_and_mutation_disjoint() -> None:
    """Every accepted form has one predictable selection and mutation boundary."""

    # Hold flag order, explicit order, bare confirmation, and strict dry run.
    text = assert_contract_markers(
        BODY,
        (
            "--at-once=<n>",
            "--model=<name>",
            "--deliberation=<low|medium|high|xhigh|max>",
            "Every flag precedes every operand",
            "preserve the order written",
            "ascending issue number",
            "asks one yes-or-no question",
            "refuse `--yes` beside `--dry-run`",
            "complete invocation",
        ),
        "Selection must never narrow or mutate because one operand is invalid.",
    )

    # Expose the alternatives to the Harness without advertising mixed forms.
    assert "argument-hint: '[--dry-run] [--at-once=<n>]" in text
    assert "[--yes] | [--at-once=<n>]" in text
    assert "[#<ticket> ...] [-- <instruction>]" in text


def test_dispatch_eligibility_and_resume_use_live_git_truth() -> None:
    """A ticket runs once, from one fresh plan, on the branch that owns the run."""

    # Require every eligibility fact and exact-invocation recovery key.
    assert_contract_markers(
        BODY,
        (
            "open executable child",
            "fresh accepted compiled plan",
            "exactly one selected landing commit",
            "reachable from the integration tip",
            "no active journal",
            "Issue closure is never the landing signal",
            "exact recorded invocation",
            "exact resume line",
        ),
        "Tracker state cannot replace plan freshness, Git reachability, or journal ownership.",
    )


def test_dry_run_and_each_live_turn_recompute_the_current_frontier() -> None:
    """The scheduler exposes useful foresight without freezing later work."""

    # Pin read-only output and the live scheduling inputs.
    assert_contract_markers(
        BODY,
        (
            "current graph",
            "footprint exclusions",
            "first executable frontier",
            "provisional later waves",
            "Route readiness",
            "opens no journal",
            "blockers first",
            "Solo Ticket",
            "greedily fill",
            "selection order",
            "recompute",
        ),
        "Dry run is descriptive while live scheduling remains a current decision.",
    )


def test_footprint_conflicts_cover_every_executor_and_test_write() -> None:
    """Concurrent attempts cannot race on a path either plan relies upon."""

    # Hold read/write collision semantics and their two deliberate exclusions.
    assert_contract_markers(
        BODY,
        (
            "writes a path the other reads or writes",
            "`modifies`, `creates`, and `deletes`",
            "compiler-owned test destinations",
            "dispatcher-owned shared writes do not exclude",
            "pre-allocated serial resources do not exclude",
        ),
        "The frontier must be parallel only where plan footprints prove independence.",
    )


def test_routing_is_durable_before_claim_and_replayed_exactly() -> None:
    """Recovery never silently changes the executor configuration."""

    # Bind dispatch to the shared doctrine and public Route Interface.
    assert_contract_markers(
        BODY,
        (
            "$LIBRARY/references/delegation-mode.md",
            "/model-selector route",
            "locks only the model field",
            "locks only the deliberation field",
            "exact main seat",
            "refusal launches nothing",
            "durable before",
            "replay",
            "authenticated user",
            "already assigned to another actor",
        ),
        "A claim or attempt must never precede its complete reproducible Route decision.",
    )

    # Keep assignment after the durable Route boundary, never in selection.
    body = BODY.read_text(encoding="utf-8")
    assert body.index("Store the complete Route response") < body.index(
        "immediately before execution, assign the child"
    )
    assert "foreign assignment" not in body


def test_executor_receives_one_self_contained_bounded_workplace() -> None:
    """Execution is isolated from tracker access and dispatcher-owned state."""

    # Keep the delegated role narrow enough for independent review.
    assert_contract_markers(
        EXECUTOR,
        (
            "complete compiled plan",
            "captured `HEAD`",
            "compiler-owned tests",
            "exact write paths",
            "serial allocations",
            "ticket-specific scratch",
            "no tracker access",
            "dispatcher-owned write proposal",
            "Advisory",
            "Binding",
        ),
        "The executor must need no hidden context and own no shared integration state.",
    )


def test_attempts_become_durable_full_index_patches_before_disposal() -> None:
    """A disposable worktree never becomes the only copy of paid work."""

    # Hold isolation, full inventory, and artifact-before-event order.
    assert_contract_markers(
        BODY,
        (
            "even at `--at-once=1`",
            "disposable linked worktree",
            "temporary dispatch branch",
            "created, modified, deleted, mode-changed, symlink, and binary",
            "full-index binary patch",
            "ordered changed paths",
            "patch digest",
            "before recording `patch-captured`",
            "never trimmed or replayed",
            "last accepted checkpoint",
        ),
        "Recovery must survive removal of every ordinary attempt worktree and branch.",
    )


def test_patch_capture_uses_materialized_base_and_separate_test_evidence() -> None:
    """Patch authority excludes bytes supplied or owned by the dispatcher."""

    # Pin the patch base, path ownership, and independent canonical-test check.
    assert_contract_markers(
        BODY,
        (
            "materialized attempt base",
            "executor-owned `modifies`, `creates`, and `deletes`",
            "excludes compiler-owned test destinations",
            "dispatcher-owned writes",
            "Inventory the test destinations separately",
            "verify every destination's Git blob",
            "rejects the complete execution result",
        ),
        "A dispatcher-supplied test must not appear to be executor work or evade tamper detection.",
    )


def test_executor_patch_excludes_unchanged_materialized_canonical_tests(
    tmp_path: Path,
) -> None:
    """New and replaced seam tests remain outside the executor-owned patch."""

    # Exercise both canonical-test shapes through a real temporary Git index.
    for replaces_test in (False, True):
        attempt = _materialized_attempt(tmp_path, replaces_test=replaces_test)
        patch = _capture_executor_patch(attempt)

        assert "diff --git a/app.py b/app.py" in patch
        assert "test_seam.py" not in patch
        _verify_canonical_test_blob(attempt)


def test_tampered_materialized_test_rejects_the_complete_executor_result(
    tmp_path: Path,
) -> None:
    """Patch exclusion cannot hide a changed compiler-owned destination."""

    # Capture the allowed executor path after materializing the canonical base.
    attempt = _materialized_attempt(tmp_path, replaces_test=False)
    patch = _capture_executor_patch(attempt)
    assert "test_seam.py" not in patch

    # Independently inventoried blob verification rejects the whole result.
    (attempt.repository / "test_seam.py").write_text(
        "assert VALUE == 999\n",
        encoding="utf-8",
    )
    try:
        _verify_canonical_test_blob(attempt)
    except AssertionError as error:
        assert str(error) == "canonical test blob changed"
    else:
        raise AssertionError("tampered canonical test was accepted")


def test_bundle_escrow_and_compiler_owned_tests_are_byte_authoritative() -> None:
    """The executor cannot weaken the independent acceptance seam."""

    # Require escrow ordering and canonical review and landing bytes.
    assert_contract_markers(
        BODY,
        (
            "byte-for-byte verified bundle escrow",
            "before recording `bundle-consumed`",
            "materialises tests from the escrow",
            "Git blob identity",
            "changed, replaced, deleted, or relocated",
            "rejects the complete execution result",
            "canonical escrow bytes",
        ),
        "Compiler-owned tests must remain independent evidence through landing.",
    )


def test_review_checks_the_result_and_keeps_four_verdicts_disjoint() -> None:
    """A strong unchanged main seat owns every verdict and integration decision."""

    # Pin the review evidence and each verdict's exclusive boundary.
    assert_contract_markers(
        REVIEW,
        (
            "unchanged main seat",
            "bundle identities",
            "STOP conditions",
            "exact footprint",
            "canonical test blobs",
            "full diff",
            "every done criterion",
            "every seam command",
            "complete repository gate",
            "APPROVE",
            "REVISE",
            "REBUILD",
            "PARK",
            "at most two",
            "one fresh executor",
            "second rebuild",
        ),
        "Review must distinguish correctable execution from a stale or undecidable contract.",
    )


def test_a_sibling_landing_does_not_stale_an_active_parallel_attempt() -> None:
    """Consumed work integrates against the newer tip instead of rebuilding."""

    # Hold the distinction between admitted work and an unstarted stale plan.
    assert_contract_markers(
        REVIEW,
        (
            "does not retroactively stale",
            "already-consumed parallel plan",
            "newer combined tip",
        ),
        "A sibling landing must not discard an already-running compatible attempt.",
    )
    assert "current source fingerprints" not in REVIEW.read_text(encoding="utf-8")


def test_landing_rebuilds_and_verifies_one_dispatcher_authored_commit() -> None:
    """Only independently rechecked bytes advance the invocation branch."""

    # Hold fresh-candidate assembly, atomic ref movement, and R1 verification.
    assert_contract_markers(
        BODY,
        (
            "fresh landing candidate",
            "accepted executor patch",
            "canonical tests",
            "dispatcher-owned writes",
            "combined diff",
            "one dispatcher-authored commit",
            "Kntnt-Ticket",
            "Kntnt-Plan",
            "expected tip",
            "reachability, trailer identity, tree identity, and compiled test blobs",
        ),
        "Executor-local history must never advance or define the integration branch.",
    )


def test_recovery_publishes_one_portable_tracker_transition_contract() -> None:
    """Tracker mutations remain idempotent across convention and process drift."""

    # Require all three transitions and concrete planned/completed receipts.
    text = assert_contract_markers(
        RECOVERY,
        (
            "sole authoritative tracker-transition contract",
            "`T-LAND`",
            "`T-PARK-INFO`",
            "`T-PARK-HUMAN`",
            "executable_ready_label",
            "needs_info_label",
            "ready_for_human_label",
            "preserved_labels",
            "tracker-transition-planned",
            "tracker-transition-completed",
            "idempotent",
            "milestone",
            "assignees",
        ),
        "Recovery must replay recorded tracker policy rather than today's vocabulary.",
    )

    # Keep published policy independent of this worktree's labels.
    assert "rework-ready-for-agent" not in text


def test_tracker_transitions_execute_against_non_default_label_conventions() -> None:
    """Symbolic transition rows preserve scope under arbitrary tracker terms."""

    # Project the symbolic deltas through two non-default convention fixtures.
    rows = _tracker_transition_rows()
    conventions: tuple[TrackerConvention, ...] = (
        TrackerConvention(
            executable_ready_label="queued-for-bot",
            needs_info_label="awaiting-answer",
            ready_for_human_label="human-queue",
            scope_label="project-cerulean",
        ),
        TrackerConvention(
            executable_ready_label="robot-green",
            needs_info_label="question-open",
            ready_for_human_label="maintainer-needed",
            scope_label="release-sunrise",
        ),
    )

    # Execute every transition against each repository's arbitrary vocabulary.
    for convention in conventions:
        _assert_tracker_convention(rows, convention)


def test_recovery_matrix_covers_every_approved_interruption_window() -> None:
    """Each last durable event has one bounded continuation."""

    # Distinguish paid work, Git movement, and cleanup boundaries.
    assert_contract_markers(
        RECOVERY,
        (
            "`attempt-started`, no patch event",
            "`patch-captured`, no review",
            "`REVISE` recorded",
            "`landing-started`, no `landed` event",
            "`REBUILD` recorded",
            "`human-conflict` recorded",
            "`landed`, no `tracker-transition-completed`",
            "`parked`, no `tracker-transition-completed`",
            "`tracker-transition-completed`, no retirement",
            "`stranded`, no cleanup event",
        ),
        "An interrupted run must neither repeat paid work nor skip an external mutation.",
    )


def test_fresh_r3_context_is_durable_reported_and_free_of_revision_cost() -> None:
    """Lost continuity remains visible without consuming correction budget."""

    # Require recovery, public help, and final reporting to expose the R3 fact.
    for path in (BODY, HELP, RECOVERY):
        assert_contract_markers(
            path,
            (
                "fresh-context",
                "final report",
                "without consuming a revision round",
            ),
            "A rehydrated REVISE must remain durable and visible after compaction.",
        )


def test_material_context_is_shown_and_persisted_before_confirmation() -> None:
    """A confirmed run can recover without relying on conversation prose."""

    # Pin selective context materialization and its byte-identical journal form.
    text = assert_contract_markers(
        BODY,
        (
            "Conversation Context that materially affects execution",
            "omit context that does not affect execution",
            "exact resume line",
            "before confirmation",
            "same UTF-8 bytes",
            "effective instruction",
            "never depends on conversation prose",
        ),
        "Confirmation and recovery must name the same self-contained invocation.",
    )

    # Materialize before displaying the command and confirmation question.
    assert text.index(
        "Conversation Context that materially affects execution"
    ) < text.index("before confirmation")
    assert text.index("before confirmation") < text.index("asks one yes-or-no question")


def test_parked_patch_and_human_conflict_have_deliberate_retention() -> None:
    """Useful evidence survives without turning disposable resources into authority."""

    # Pin R2 retention and the one exceptional retained worktree.
    assert_contract_markers(
        RECOVERY,
        (
            "latest full parked patch",
            "until that ticket lands or is explicitly abandoned",
            "never authority",
            "preserve only the named worktree and branch",
            "immutable-test warning",
            "one exact owner decision",
            "same invocation",
            "full review",
            "Record the owner's answer",
            "mechanical instruction",
            "changes durable product intent",
            "posted to the child",
            "/compile #<ticket>",
        ),
        "Retention must be inspectable, minimal, and unable to bypass recompilation or review.",
    )


def test_terminal_transition_precedes_bundle_retirement_and_cleanup() -> None:
    """Tracker completion and run resources recover independently and in order."""

    # Hold retirement ordering, three-state projection, and exit invariant.
    assert_contract_markers(
        RECOVERY,
        (
            "tracker transition completes before bundle retirement",
            "Landed",
            "Parked",
            "Stranded",
            "every selected ticket",
            "integration tree is clean",
            "active journal",
            "atomically archived",
            "ordinary worktrees",
            "temporary branches",
            "stranded canonical slot",
        ),
        "Completion must be machine-checkable without erasing recoverable state.",
    )


def test_observation_and_completion_report_do_not_take_over_future_land() -> None:
    """Dispatch reports execution evidence while leaving knowledge closure downstream."""

    # Keep observations user-imported and today's report honest.
    assert_contract_markers(
        BODY,
        (
            "/model-selector observe",
            "beside the archived journal",
            "/model-selector record",
            "imports no evidence",
            "$LIBRARY/references/tldr-mode.md",
            "Landed, Parked, or Stranded",
            "invent no `/land` invocation",
        ),
        "Dispatch must expose judged evidence without importing it or closing the durable loop.",
    )


def test_compile_excludes_landed_batons_and_hands_only_eligible_plans_to_dispatch() -> (
    None
):
    """The producer names its shipped successor without creating an invalid run."""

    # Read both compile surfaces after dispatch exists.
    body = COMPILE_BODY.read_text(encoding="utf-8")
    help_text = COMPILE_HELP.read_text(encoding="utf-8")

    # Hold the defensive Git guard and exact ordered successor handoff.
    for marker in (
        "$LIBRARY/references/landed-change.md",
        "selected reachable baton",
        "even when executable-ready label drift",
        "/dispatch #<ticket> #<ticket> ...",
        "compile-selection order",
        "blocked plans separately",
        "invent no empty handoff",
    ):
        assert marker in body, (
            f"{COMPILE_BODY}: the dispatch successor contract must state `{marker}`."
            f" See {STANDARD}."
        )

    assert help_text.count("**/dispatch --help**") == 1


def test_the_manpage_exposes_the_complete_dispatch_profile() -> None:
    """A user can predict selection, recovery, outcomes, and refusal from help."""

    # Pin both grammar families and the operationally important sections.
    assert_contract_markers(
        HELP,
        (
            "**/dispatch** [**--at-once=**_N_] [**--model=**_NAME_]",
            "**--dry-run**",
            "dispatch-eligible",
            "APPROVE",
            "REVISE",
            "REBUILD",
            "PARK",
            "Landed",
            "Parked",
            "Stranded",
            "Git common directory",
            "exact recorded invocation",
            "**/compile --help**",
            "**/model-selector route --help**",
        ),
        "The manpage must describe the command's complete public operating profile.",
    )


def test_historical_runtime_lessons_are_live_rules_without_repository_citations() -> (
    None
):
    """Installed prose carries current behaviour rather than archive archaeology."""

    # Hold the rescued field lessons across the executable and recovery frames.
    text = (
        BODY.read_text(encoding="utf-8")
        + REVIEW.read_text(encoding="utf-8")
        + RECOVERY.read_text(encoding="utf-8")
    )
    for marker in (
        "journal persistence only",
        "exact recorded invocation",
        "clean integration tree",
        "even at `--at-once=1`",
        "temporary dispatch branch",
        "current integration tip",
        "at most two review-informed rounds",
        "pre-allocated serial resources",
        "combined diff",
        "newly discovered numbered dependency",
        "unchanged main seat",
        "exact recorded decision",
        "constructive correction",
        "dispatcher-owned writes serially",
    ):
        assert marker in text, (
            f"Dispatch must carry the current operational lesson `{marker}` without"
            f" requiring an installed reader to open repository history. See {STANDARD}."
        )

    # The transactional exception cannot grow back into the retired engine.
    assert "no workflow engine" in text
    assert "ADR-" not in text
