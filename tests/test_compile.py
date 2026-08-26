"""The executor-plan contract of the Compile Skill."""

from __future__ import annotations

from pathlib import Path

from support.contract import STANDARD

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SKILL: Path = REPO_ROOT / "skills" / "code" / "compile"
BODY: Path = SKILL / "SKILL.md"
HELP: Path = SKILL / "help.md"
COMPILING: Path = SKILL / "references" / "compiling.md"
COLD_READ: Path = SKILL / "references" / "cold-read.md"
TO_SLICES_BODY: Path = REPO_ROOT / "skills" / "code" / "to-slices" / "SKILL.md"
TO_SLICES_HELP: Path = REPO_ROOT / "skills" / "code" / "to-slices" / "help.md"


def _assert_contract_markers(
    path: Path,
    markers: tuple[str, ...],
    consequence: str,
) -> str:
    """Return an agent document after holding its required contract markers."""

    # Read the public prose seam once for every marker in this contract.
    text = path.read_text(encoding="utf-8")

    # Report the behavioural consequence of whichever obligation disappears.
    for marker in markers:
        assert marker in text, (
            f"{path}: the contract must state `{marker}`. {consequence} See {STANDARD}."
        )

    return text


def test_the_body_selects_executable_children_without_scheduling_them() -> None:
    """Selection is deterministic while blocker eligibility remains downstream."""

    # Hold explicit and bare selection against the shared pipeline grammar.
    text = _assert_contract_markers(
        BODY,
        (
            "/compile [--yes] [#<ticket> ...]",
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


def test_the_body_reads_and_preserves_the_complete_durable_requirement() -> None:
    """Later tracker context remains part of the plan's source of truth."""

    # Hold every durable input and the precedence rule at the public seam.
    _assert_contract_markers(
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
    _assert_contract_markers(
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
    _assert_contract_markers(
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
    _assert_contract_markers(
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

    # Hold the one-pass allocation rule and its exhaustion boundary.
    _assert_contract_markers(
        COMPILING,
        (
            "once per registry",
            "deterministic selected-ticket order",
            "highest committed identifier",
            "other fresh plans at the captured `HEAD`",
            "Gaps are not reused",
            "another identifier is a STOP condition",
        ),
        "Every accepted plan in the batch must carry an exclusive fixed allocation.",
    )


def test_compiler_owned_tests_are_red_for_the_intended_missing_behaviour() -> None:
    """A setup failure or already-green test cannot become executor evidence."""

    # Pin test authorship, overlay identity, and the meaningful-red gate.
    _assert_contract_markers(
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
    _assert_contract_markers(
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


def test_bundle_fixtures_distinguish_every_consumer_boundary() -> None:
    """Worked states pin freshness, test ownership, and exact scope."""

    # Require the concrete outcomes the ticket selected as fixture coverage.
    fixtures: tuple[str, ...] = (
        "| Valid |",
        "| Stale source |",
        "| Changed HEAD |",
        "| Changed test |",
        "| Out of footprint |",
    )

    # Assert the local judgement reference applies every shared fixture.
    text = COMPILING.read_text(encoding="utf-8")
    for fixture in fixtures:
        assert fixture in text, (
            f"{COMPILING}: the worked bundle fixtures omit `{fixture}`. A"
            f" compiler must distinguish source drift, branch drift, test"
            f" tampering, and scope drift from a consumable plan. See {STANDARD}."
        )


def test_acceptance_publishes_one_immutable_bundle_and_atomic_pointer() -> None:
    """Interruption leaves the old accepted bundle or the complete new one."""

    # Pin the common-directory store and its immutable publication boundary.
    _assert_contract_markers(
        BODY,
        (
            ".git/kntnt-pipeline/plans/<ticket>/bundles/<fingerprint>/",
            "immutable bundle directory",
            "accepted` pointer",
            "atomic rename",
            "bundle fingerprint",
            "child source fingerprint",
            "parent source fingerprint",
        ),
        "Acceptance must never expose a partial or internally stale bundle.",
    )


def test_completion_reports_every_selected_outcome_without_inventing_dispatch() -> None:
    """The owner gets a complete batch report before the successor exists."""

    # Hold the reporting partition and owner-facing register together.
    _assert_contract_markers(
        BODY,
        (
            "$LIBRARY/references/tldr-mode.md",
            "accepted",
            "parked",
            "already fresh",
            "failed",
            "captured `HEAD`",
            "bundle paths",
            "invent no `/dispatch` invocation",
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
    _assert_contract_markers(
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
