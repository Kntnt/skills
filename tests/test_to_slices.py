"""The durable publication contract of the To Slices Skill."""

from __future__ import annotations

from pathlib import Path

from support.contract import STANDARD

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SKILL: Path = REPO_ROOT / "skills" / "code" / "to-slices"
BODY: Path = SKILL / "SKILL.md"
SLICING: Path = SKILL / "references" / "slicing.md"
PUBLISHING: Path = SKILL / "references" / "publishing.md"
FRAME_BODY: Path = REPO_ROOT / "skills" / "code" / "frame" / "SKILL.md"
FRAME_HELP: Path = REPO_ROOT / "skills" / "code" / "frame" / "help.md"


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


def test_the_body_validates_the_frame_record_before_synthesis() -> None:
    """Invalid or stale framing returns to its producer with the baton intact."""

    # Hold every branch that distinguishes valid drift from resumed framing.
    _assert_contract_markers(
        BODY,
        (
            "$LIBRARY/references/frame-record.md",
            "/frame --resume=<path>",
            "git diff --name-only <framing-commit>..HEAD",
            "every changed path is named in section 7",
            "update section 1 to `HEAD`",
        ),
        "Invalid or stale framing must return to its producer with the baton intact.",
    )


def test_the_body_gates_publication_on_committed_knowledge() -> None:
    """The durable manifest resolves in every clone before it reaches GitHub."""

    # Read the executable contract at the committed-knowledge gate.
    text = BODY.read_text(encoding="utf-8")

    # Require history rather than working-tree existence as the evidence seam.
    assert "git cat-file -e HEAD:<path>" in text, (
        f"{BODY}: every section 7 address is checked against `HEAD`, not the"
        f" working tree. Local-only knowledge would strand `/land` in another"
        f" clone. See {STANDARD}."
    )

    # Resolve a precise address rather than accepting its containing file.
    assert "verify that exact heading or line in the committed blob" in text, (
        f"{BODY}: an address-qualified knowledge entry must resolve at its"
        f" heading or line. File existence alone accepts a stale pointer. See"
        f" {STANDARD}."
    )

    # Keep the Skill from acquiring commit authority through recovery wording.
    assert "stage or commit nothing" in text, (
        f"{BODY}: the Skill leaves the owner's files untouched when knowledge"
        f" exists only locally. Committing it would require authority the"
        f" slicing invocation does not grant. See {STANDARD}."
    )


def test_the_body_previews_the_whole_graph_at_the_approval_seam() -> None:
    """The owner approves one complete durable graph rather than fragments."""

    # Hold the complete graph shape at the only owner checkpoint.
    text = _assert_contract_markers(
        BODY,
        (
            "complete decision issue",
            "delivered behaviour",
            "seam contract",
            "blockers",
            "builds alone",
            "granularity and blocking edges",
        ),
        "The owner checkpoint must see the whole graph it approves.",
    ).casefold()

    # Limit assumed approval to a proposal already complete from the record.
    assert "first complete proposal" in text, (
        f"{BODY}: `--yes` pre-approves the first complete proposal. It cannot"
        f" answer a missing owner decision or repair an incomplete record."
        f" See {STANDARD}."
    )


def test_the_slicing_reference_keeps_tickets_vertical_and_edges_semantic() -> None:
    """Slice judgement preserves independently verifiable delivery."""

    # Pin every slice form and the distinction between necessity and order.
    _assert_contract_markers(
        SLICING,
        (
            "Tracer bullets",
            "one fresh context",
            "Expand–contract",
            "cannot be implemented or verified honestly",
            "shared files",
            "Builds alone",
            "decision rule",
        ),
        "A horizontal task, preferred order, or open experiment must not masquerade as a slice.",
    )


def test_publication_is_recoverable_and_deletion_waits_for_read_back() -> None:
    """A partial tracker transaction retains one exact recovery baton."""

    # Hold identity, ordering, relation, and verification obligations together.
    text = _assert_contract_markers(
        PUBLISHING,
        (
            "Frame Record path and framing commit",
            "stable child provenance marker",
            "recover every child globally",
            "dependency order",
            "native parent",
            "native blocking",
            "read the decision issue and every child back",
            "body, state, labels, milestone, parentage, and every blocking edge",
            "delete the Frame Record",
        ),
        "A successful create call alone does not prove the approved tracker graph exists.",
    )

    # Make record deletion structurally later than the complete read-back.
    assert text.index("read the decision issue and every child back") < text.index(
        "delete the Frame Record"
    ), (
        f"{PUBLISHING}: the complete read-back must precede record deletion."
        f" A partial publication keeps the record as its recovery baton. See"
        f" {STANDARD}."
    )

    # Preserve outside edits instead of gaining overwrite authority.
    assert "report the conflict and preserve the Frame Record" in text, (
        f"{PUBLISHING}: re-invocation repairs missing publication but never"
        f" silently overwrites conflicting tracker content. See {STANDARD}."
    )


def test_publication_fixtures_distinguish_complete_and_partial_read_back() -> None:
    """Worked tracker states pin the record-consumption boundary."""

    # Keep concrete outcomes for both sides of the destructive gate.
    fixtures: tuple[str, ...] = (
        "| Complete | Parent `#200`; children `#201` and `#202`; both parent relations; `#202` blocked by `#201`; every body, state, label, and milestone agrees | Delete the Frame Record |",
        "| Partial | Parent `#200`; children `#201` and `#202`; parent relation for `#202` missing; every other field agrees | Preserve the Frame Record; recover `#202` by its marker and repair only the relation |",
    )

    # Assert the public prose seam carries each independently worked fixture.
    text = PUBLISHING.read_text(encoding="utf-8")
    for fixture in fixtures:
        assert fixture in text, (
            f"{PUBLISHING}: the worked publication fixtures omit `{fixture}`."
            f" The deletion gate must distinguish complete read-back from an"
            f" orphaned child without inferring the result. See {STANDARD}."
        )


def test_frame_hands_its_completed_record_to_to_slices() -> None:
    """The producer names its now-shipped consumer at both handoff surfaces."""

    # Read the executable and user-facing producer surfaces.
    body = FRAME_BODY.read_text(encoding="utf-8")
    help_text = FRAME_HELP.read_text(encoding="utf-8")

    # Hold the concrete baton and its discoverable successor together.
    assert "/to-slices .kntnt/frames/<slug>.md" in body, (
        f"{FRAME_BODY}: the closing report must hand over the exact record it"
        f" produced now that its consumer ships. See {STANDARD}."
    )
    assert help_text.count("**/to-slices --help**") == 1, (
        f"{FRAME_HELP}: SEE ALSO must point to `/to-slices --help` exactly"
        f" once when that successor exists. See {STANDARD}."
    )
