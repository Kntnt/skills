"""The executor-plan contract of the Compile Skill."""

from __future__ import annotations

from pathlib import Path

from support.contract import STANDARD, assert_contract_markers

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SKILL: Path = REPO_ROOT / "skills" / "code" / "compile"
BODY: Path = SKILL / "SKILL.md"
HELP: Path = SKILL / "help.md"
COMPILING: Path = SKILL / "references" / "compiling.md"
COLD_READ: Path = SKILL / "references" / "cold-read.md"
TO_SLICES_BODY: Path = REPO_ROOT / "skills" / "code" / "to-slices" / "SKILL.md"
TO_SLICES_HELP: Path = REPO_ROOT / "skills" / "code" / "to-slices" / "help.md"


def test_the_body_selects_executable_children_without_scheduling_them() -> None:
    """Selection is deterministic while blocker eligibility remains downstream."""

    # Hold explicit and bare selection against the shared pipeline grammar.
    text = assert_contract_markers(
        BODY,
        (
            "`/compile [--yes]` or `/compile #<ticket> ...`",
            "preserve the order written",
            "ascending issue number",
            "configured executable-ready state",
            "fresh accepted bundle",
            "Blockers do not gate compilation",
        ),
        "Compilation must select requirements without taking over dispatch scheduling.",
    )

    # Give `--yes` work only at the bare confirmation checkpoint.
    assert "refuse `--yes` beside explicit references" in text, (
        f"{BODY}: explicit ticket references already confirm the selection, so"
        f" `--yes` has no work there and must be refused. See {STANDARD}."
    )

    # Keep the harness hint from advertising the forbidden combined form.
    assert "argument-hint: '[--yes] | [#<ticket> ...]" in text, (
        f"{BODY}: the argument hint must expose bare confirmation and explicit"
        f" selection as alternatives. See {STANDARD}."
    )


def test_the_body_reads_and_preserves_the_complete_durable_requirement() -> None:
    """Later tracker context remains part of the plan's source of truth."""

    # Hold every durable input and the precedence rule at the public seam.
    assert_contract_markers(
        BODY,
        (
            "$LIBRARY/references/slices.md",
            "complete body and every comment",
            "later comment outranks earlier contradictory text",
            "parent decision issue",
            "native blocking relations",
            "Write that answer to the child thread before compilation",
            "contradicts or widens",
        ),
        "A compiler that reads only the body can accept an obsolete requirement.",
    )


def test_the_body_parks_only_owner_incomplete_children() -> None:
    """One incomplete child does not turn a batch into tracker-wide failure."""

    # Keep the parking mutation narrow and sibling-independent.
    assert_contract_markers(
        BODY,
        (
            "one complete question",
            "needs-info",
            "remove only its executable-ready state",
            "preserve its scope labels and milestone",
            "continue with the remaining selected children",
            "Technical choices inside the repository's frames",
        ),
        "Parking must expose one owner decision without discarding sibling work or metadata.",
    )


def test_compilation_uses_one_clean_stable_vantage_for_the_batch() -> None:
    """Local edits and a red baseline never leak into an accepted plan."""

    # Pin the detached-tree baseline and both final source gates.
    assert_contract_markers(
        BODY,
        (
            "git rev-parse --git-common-dir",
            "full `HEAD`",
            "temporary detached worktree",
            "unrelated local edits",
            "untouched repository gate once for the batch",
            "stops the batch",
            "integration branch still points at the captured `HEAD`",
            "re-read the child and parent sources",
        ),
        "Every accepted sibling must describe the same clean Git and tracker world.",
    )


def test_compiling_builds_the_complete_shared_bundle_without_rewriting_it() -> None:
    """The local judgement reference produces the Library's deep Interface."""

    # Keep synthesis on the shared contract and require both plan registers.
    assert_contract_markers(
        COMPILING,
        (
            "$LIBRARY/references/compiled-plan.md",
            "Binding contract",
            "Advisory appendix",
            "exact footprint",
            "machine-checkable",
            "STOP condition",
            "manifest.json",
            "tests/",
        ),
        "The compiler must fill the shared bundle rather than create a private plan format.",
    )


def test_serial_allocations_are_batch_wide_and_never_extended() -> None:
    """Concurrent plans cannot claim the same repository serial identity."""

    # Keep local judgement on counts while the shared Interface owns allocation.
    assert_contract_markers(
        COMPILING,
        (
            "$LIBRARY/references/compiled-plan.md",
            "serial-resource count",
            "whole selected batch",
            "dynamic serial need",
        ),
        "Every accepted plan in the batch must carry an exclusive fixed allocation.",
    )


def test_compiler_owned_tests_are_red_for_the_intended_missing_behaviour() -> None:
    """A setup failure or already-green test cannot become executor evidence."""

    # Pin test authorship, overlay identity, and the meaningful-red gate.
    assert_contract_markers(
        COMPILING,
        (
            "finished compiler-owned test",
            "base blob",
            "compiled blob",
            "focused command",
            "intended behavioural assertion",
            "syntax, import, fixture, collection, or environment failure",
            "already green",
        ),
        "Accepted tests must independently distinguish the ticket's missing behaviour.",
    )


def test_every_corrected_bundle_receives_a_new_cold_reader() -> None:
    """Plan acceptance is an independent verdict on the exact candidate."""

    # Hold isolation, inherited authority, complete checks, and verdict shape.
    text = assert_contract_markers(
        COLD_READ,
        (
            "fresh-context subagent",
            "exact inherited main seat",
            "only the bundle and a clean detached tree",
            "reproduce the expected red result",
            "every acceptance criterion",
            "footprint and allocations",
            "PASS",
            "FAIL",
            "new cold reader",
            "owner-owned",
        ),
        "The compiler cannot accept its own intent as evidence that an executor can follow the plan.",
    )

    # Require provenance to come from the bundle rather than its author.
    assert "Captured repository identity" not in text
    assert "Captured integration branch" not in text


def test_bundle_fixtures_distinguish_every_consumer_boundary() -> None:
    """Worked states pin freshness, test ownership, and exact scope."""

    # Require the concrete outcomes the ticket selected as fixture coverage.
    fixtures: tuple[str, ...] = (
        "| Valid | Every Git, source, bundle, footprint, allocation, and test identity agrees | Send the complete candidate to cold read |",
        "| Stale source | A child or parent fingerprint changed while Git and bundle identities still agree | Recompile that child from the complete current thread |",
        "| Changed HEAD | The integration branch moved while tracker and bundle identities still agree | Restart the whole batch from the new tip |",
        "| Changed test | The overlay or materialised compiler-owned test differs from its compiled blob | Reject the candidate or execution result; never accept altered test bytes |",
        "| Out of footprint | A required or resulting executor write has no exact executor-owned class | Reject the candidate or execution result; widen only through honest recompilation |",
    )

    # Assert the local judgement reference applies every shared fixture.
    assert_contract_markers(
        COMPILING,
        fixtures,
        "Compilation must distinguish drift or tampering from a consumable plan.",
    )


def test_acceptance_publishes_one_immutable_bundle_and_atomic_pointer() -> None:
    """Interruption leaves the old accepted bundle or the complete new one."""

    # Pin the common-directory store and its immutable publication boundary.
    assert_contract_markers(
        BODY,
        (
            "<git-common-dir>/kntnt-pipeline/plans/<ticket>/bundles/<fingerprint>/",
            "immutable bundle directory",
            "accepted` pointer",
            "atomic rename",
            "bundle fingerprint",
            "child source fingerprint",
            "parent source fingerprint",
        ),
        "Acceptance must never expose a partial or internally stale bundle.",
    )


def test_completion_reports_every_selected_outcome_before_dispatch_handoff() -> None:
    """The owner gets a complete batch report and one valid successor line."""

    # Hold the reporting partition and owner-facing register together.
    assert_contract_markers(
        BODY,
        (
            "$LIBRARY/references/tldr-mode.md",
            "accepted",
            "parked",
            "already fresh",
            "failed",
            "captured `HEAD`",
            "bundle paths",
            "/dispatch #<ticket> #<ticket> ...",
            "blocked plans separately",
            "invent no empty handoff",
        ),
        "Every selected child needs one visible outcome without promising an unavailable successor.",
    )


def test_to_slices_hands_published_children_to_compile() -> None:
    """The producer names its now-shipped consumer at both handoff surfaces."""

    # Read the executable and user-facing producer surfaces.
    body = TO_SLICES_BODY.read_text(encoding="utf-8")
    help_text = TO_SLICES_HELP.read_text(encoding="utf-8")

    # Hold ordered child operands and discoverable help together.
    assert "/compile #<child> #<child> ..." in body, (
        f"{TO_SLICES_BODY}: the closing report must preserve approved child"
        f" order in the exact `/compile` handoff. See {STANDARD}."
    )
    assert help_text.count("**/compile --help**") == 1, (
        f"{TO_SLICES_HELP}: SEE ALSO must point to `/compile --help` exactly"
        f" once now that the successor ships. See {STANDARD}."
    )


def test_the_manpage_exposes_the_complete_compile_profile() -> None:
    """The public help describes selection, storage, output, and refusal."""

    # Pin the user-facing grammar and the important operational boundaries.
    assert_contract_markers(
        HELP,
        (
            "**/compile** [**--yes**] [**--** *INSTRUCTION*]",
            "**/compile** *#TICKET* ... [**--** *INSTRUCTION*]",
            "configured executable-ready state",
            "blockers",
            "Git common directory",
            "needs-info",
            "**/to-slices --help**",
        ),
        "A user must be able to predict what compilation selects, writes, and refuses.",
    )
