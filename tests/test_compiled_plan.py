"""The compiled-plan Interface shared across the pipeline."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
CONTRACT: Path = (
    REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "compiled-plan.md"
)
PIPELINE_RULES: Path = REPO_ROOT / "docs" / "rules" / "pipeline.md"
AGENTS: Path = REPO_ROOT / "AGENTS.md"
STANDARD: str = "docs/rules/skills.md"


def _read(path: Path) -> str:
    """Read one public contract surface as UTF-8."""

    return path.read_text(encoding="utf-8")


def test_the_collection_library_carries_the_compiled_plan_interface() -> None:
    """The producer and consumer share one three-part bundle contract."""

    assert CONTRACT.is_file(), (
        f"{CONTRACT}: `/compile` and `/dispatch` need one shared plan Interface"
        f" in the Collection Library. See {STANDARD}."
    )

    # Hold the complete bundle and both plan registers at their public seam.
    text = _read(CONTRACT)
    for promise in (
        "plan.md",
        "manifest.json",
        "tests/",
        "binding contract",
        "advisory appendix",
        "Identity and provenance",
        "Goal",
        "Scope and footprint",
        "Invariants",
        "Current implementation context",
        "Seam tests",
        "Verification",
        "Done criteria",
        "STOP conditions",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` is part of the compiled bundle or its"
            f" two-register plan and is no longer stated. See {STANDARD}."
        )


def test_the_manifest_is_only_the_mechanically_checked_subset() -> None:
    """The manifest identifies checks without retelling product intent."""

    # Pin every identity a consumer compares and the intent it must not copy.
    text = _read(CONTRACT)
    for promise in (
        "repository identity",
        "integration branch",
        "full HEAD",
        "child source fingerprint",
        "parent source fingerprint",
        "bundle fingerprint",
        "footprint",
        "serial allocations",
        "test destination",
        "base blob",
        "compiled blob",
        "verification commands",
        "done-criterion identifiers",
        "does not repeat the goal, invariants, implementation context, or STOP conditions",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` belongs to the manifest boundary. See {STANDARD}."
        )

    # The digest recipe has to reproduce the artifact without hashing itself.
    for promise in (
        "bundle fingerprint field omitted",
        "`plan.md` names the manifest field instead of copying its value",
        "lexicographic bundle-relative path order",
        "tests/<repository-relative destination>",
        "RFC 8785",
        "SHA-256",
        "path, byte length, and bytes",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` is required to reproduce the bundle"
            f" fingerprint independently. See {STANDARD}."
        )


def test_source_fingerprints_have_one_reproducible_snapshot_shape() -> None:
    """Producer and consumer canonicalise the same tracker facts identically."""

    # Extract only the worked child and parent source snapshots.
    text = _read(CONTRACT)
    section = text.split("#### Canonical source snapshots", maxsplit=1)
    assert len(section) == 2, (
        f"{CONTRACT}: source fingerprint prose names facts but exposes no"
        f" canonical snapshot shape. See {STANDARD}."
    )
    source_section = section[1].split("\n## ", maxsplit=1)[0]
    snapshots = [
        json.loads(snapshot)
        for snapshot in re.findall(r"```json\n(.*?)\n```", source_section, re.DOTALL)
    ]
    assert len(snapshots) == 2, (
        f"{CONTRACT}: the child and parent each need one canonical source"
        f" snapshot. See {STANDARD}."
    )

    # Pin exact top-level keys and normalized relation values.
    child, parent = snapshots
    assert set(child) == {"issue", "comments", "parent", "blocked_by"}
    assert set(parent) == {"issue", "comments"}
    assert set(child["issue"]) == {"number", "title", "body"}
    assert set(parent["issue"]) == {"number", "title", "body"}
    assert set(child["comments"][0]) == {"id", "author", "created_at", "body"}
    assert set(parent["comments"][0]) == {"id", "author", "created_at", "body"}
    assert child["parent"] == "#180"
    assert child["blocked_by"] == ["#179"]

    # Different tracker surfaces normalize to the same relation fields.
    for promise in (
        "Native relations are authoritative when available",
        "fallback lines are parsed only when the native surface is unavailable",
        "Relation provenance is not included",
        "ascending issue number",
    ):
        assert promise in source_section, (
            f"{CONTRACT}: `{promise}` is required to canonicalise native and"
            f" fallback tracker state identically. See {STANDARD}."
        )


def test_footprints_and_serial_allocations_are_exact() -> None:
    """Concurrent work can trust paths and identifiers without guessing."""

    # Keep all owner classes distinct and forbid a vague footprint.
    text = _read(CONTRACT)
    for footprint_class in (
        "reads",
        "modifies",
        "creates",
        "deletes",
        "compiler-owned test writes",
        "dispatcher-owned shared writes",
        "serial resources",
    ):
        assert footprint_class in text, (
            f"{CONTRACT}: `{footprint_class}` is an exact footprint class the"
            f" producer and consumer must distinguish. See {STANDARD}."
        )

    # Reject every shape that would make the later scope comparison guess.
    for prohibition in (
        "Globs are forbidden",
        "A directory cannot stand for unknown descendants",
        "An extra identifier is a STOP condition",
    ):
        assert prohibition in text, (
            f"{CONTRACT}: `{prohibition}` keeps execution inside the accepted"
            f" footprint and allocation. See {STANDARD}."
        )

    # One shared counter prevents sibling plans from racing the same registry.
    for promise in (
        "once per batch and once per registry",
        "highest committed identifier",
        "other fresh plans at the same HEAD",
        "deterministic ticket order",
        "Gaps are never reused",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` is part of deterministic batch serial"
            f" allocation. See {STANDARD}."
        )


def test_freshness_and_lifecycle_bind_git_tracker_and_bundle_state() -> None:
    """A plan is executable only in the exact world it was compiled from."""

    # Source and artifact checks jointly decide whether the baton is fresh.
    text = _read(CONTRACT)
    for promise in (
        "repository identity, integration branch, full HEAD, child source fingerprint, parent source fingerprint, and bundle fingerprint all match",
        "git rev-parse --git-common-dir",
        ".git/kntnt-pipeline/plans/<ticket>/",
        "temporary sibling",
        "complete candidate",
        "immutable bundle directories",
        "one atomic rename to replace or create `accepted`",
        "old complete bundle or the new complete bundle, never an absent canonical selection",
        "never reconciled in place",
        "retired when the ticket lands or is parked",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` is part of clone-local plan freshness or"
            f" lifecycle. See {STANDARD}."
        )


def test_compiler_owned_tests_remain_outside_executor_ownership() -> None:
    """The accepted seam test survives execution and lands unchanged."""

    # Pin authorship, review enforcement, and final ownership together.
    text = _read(CONTRACT)
    for promise in (
        "read-only guardrail",
        "not an operating-system security boundary",
        "re-hashes every materialised test",
        "changed, replaced, or deleted",
        "rejects the execution result",
        "exact accepted bytes",
        "permanent regression tests",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` keeps compiler-owned tests immutable at"
            f" the review seam and through landing. See {STANDARD}."
        )


def test_bundle_fixtures_pin_each_freshness_and_scope_outcome() -> None:
    """Worked bundles distinguish consumption from four rejection paths."""

    # These independent worked states are the expected results future producers
    # and consumers must preserve when they implement the shared Interface.
    fixtures: tuple[str, ...] = (
        "| Valid | Every Git, tracker-source, and bundle identity matches; execution changes only `modifies` and `creates`; every materialised test matches its compiled blob | Consume the bundle |",
        "| Stale source | A new child comment changes the child source fingerprint; every Git and bundle identity still matches | Recompile and atomically replace the stale bundle |",
        "| Changed HEAD | The integration branch now points to a different commit; every tracker-source and bundle identity still matches | Restart compilation for the batch at the new HEAD |",
        "| Changed test | The canonical bundle is fresh, but a materialised test no longer matches its compiled blob after execution | Reject the execution result; do not land the test or implementation |",
        "| Out of footprint | The canonical bundle is fresh, but execution changes `README.md`, which appears in no executor-owned write class | Reject the execution result; do not land any changed path |",
    )

    # Assert the public prose seam carries every worked outcome verbatim.
    text = _read(CONTRACT)
    for fixture in fixtures:
        assert fixture in text, (
            f"{CONTRACT}: the worked bundle fixtures omit `{fixture}`. See {STANDARD}."
        )


def test_pipeline_rules_are_reachable_without_copying_runtime_detail() -> None:
    """Contributors reach one shared grammar and ownership rule from AGENTS."""

    assert PIPELINE_RULES.is_file(), (
        f"{PIPELINE_RULES}: the three pipeline Skills need one authoring rule"
        f" for their shared promises. See docs/rules/docs.md."
    )

    # The rules module fixes cross-Skill promises but points to runtime detail.
    rules = _read(PIPELINE_RULES)
    for promise in (
        "#<ticket>",
        "current repository",
        "explicit references preserve the order written",
        "Bare selection is ordered by ascending issue number",
        "asks one yes-or-no question",
        "--yes",
        "refused rather than ignored",
        "fresh accepted compiled plan",
        "compiler-owned seam tests",
        "compiled-plan.md",
    ):
        assert promise in rules, (
            f"{PIPELINE_RULES}: `{promise}` is a shared pipeline promise or"
            f" its runtime-contract pointer. See docs/rules/docs.md."
        )

    # The always-loaded guide routes every author who changes that shared law.
    agents = _read(AGENTS)
    expected_pointer = (
        "- `docs/rules/pipeline.md` — read when changing how pipeline Skills "
        "select tickets, decide plan freshness or landed state, or own seam tests"
    )
    assert expected_pointer in agents, (
        f"{AGENTS}: the pipeline rules are not reachable for every class of"
        f" work they govern. See docs/rules/docs.md."
    )


def test_every_local_reference_from_the_shared_contracts_resolves() -> None:
    """An installed reader can follow every relative contract pointer."""

    # Resolve links from both the runtime Interface and the authoring rule.
    for path in (CONTRACT, PIPELINE_RULES):
        # Collect the local destinations exposed by this contract surface.
        text = _read(path)
        destinations = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        local_destinations = [
            destination.split("#", maxsplit=1)[0]
            for destination in destinations
            if "://" not in destination
        ]
        assert local_destinations, (
            f"{path}: the shared contract has no resolved local pointer. See"
            f" {STANDARD}."
        )

        # Report every broken address together for one corrective pass.
        missing = [
            destination
            for destination in local_destinations
            if not (path.parent / destination).resolve().exists()
        ]
        assert missing == [], (
            f"{path}: these local references resolve nowhere: {missing}. See"
            f" {STANDARD}."
        )
