"""Transactional persistence for disposable dispatch execution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any, Final

import pytest  # type: ignore[import-not-found]  # CI's mypy command omits pytest.

REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
JOURNAL_PATH: Final[Path] = (
    REPO_ROOT / "skills" / "code" / "dispatch" / "scripts" / "journal.py"
)
CONTRIBUTING_PATH: Final[Path] = REPO_ROOT / "CONTRIBUTING.md"
CI_PATH: Final[Path] = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def _load() -> ModuleType:
    """Load the shipped journal helper from its installed location."""

    # Import the script as a module without adding its directory to sys.path.
    spec = importlib.util.spec_from_file_location("dispatch_journal", JOURNAL_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _opening(
    ref: str = "refs/heads/rework", invocation: str = "/dispatch #184"
) -> dict[str, Any]:
    """Return one complete set of immutable run-opening inputs."""

    # Keep every fixture invocation explicit and reproducibly fingerprinted.
    return {
        "repository": "github.com/Kntnt/skills",
        "integration_ref": ref,
        "opening_head": "1" * 40,
        "invocation": invocation,
        "instruction": "Keep the protected rework labels portable.",
        "selection": ["#184", "#185"],
        "at_once": 2,
        "route": {"model": None, "deliberation": "medium"},
    }


def _open(module: ModuleType, root: Path, **changes: Any) -> Any:
    """Open one deterministic fixture journal."""

    # Apply only the requested opening overrides before slot selection.
    opening = _opening()
    opening.update(changes)
    return module.Journal.open(root, opening, opened_at="2026-08-27T08:09:10Z")


def _record_attempt(journal: Any, ticket: str = "#184") -> None:
    """Record the durable prefix shared by executor crash fixtures."""

    # Persist global selection before beginning one selected ticket's attempt.
    _record_event(
        journal,
        "selection-recorded",
        payload={"tickets": journal.metadata["selection"]},
    )
    _record_ticket_attempt(journal, ticket)


def _record_ticket_attempt(journal: Any, ticket: str) -> None:
    """Record one selected ticket from bundle consumption through attempt start."""

    # Consume and route the compiled bundle before assigning disposable work.
    _record_event(
        journal,
        "bundle-consumed",
        ticket=ticket,
        payload={
            "bundle_fingerprint": f"sha256:{'2' * 64}",
            "execution_base": "1" * 40,
        },
    )
    _record_event(
        journal,
        "route-recorded",
        ticket=ticket,
        payload={"attempt": 1, "decision": {"status": "selected"}},
        artifacts={"route-response": b'{"decision":"selected"}\n'},
    )
    _record_event(
        journal, "ticket-assigned", ticket=ticket, payload={"assignee": "thomas"}
    )
    _record_event(
        journal,
        "attempt-started",
        ticket=ticket,
        payload={"attempt": 1, "base": "1" * 40},
    )


def _record_landing_window(journal: Any, ticket: str) -> dict[str, Any]:
    """Record one approved patch through its ticket-specific landing window."""

    # Bind landing to the exact review of the captured ticket patch.
    _record_event(journal, "patch-captured", ticket=ticket)
    review = _record_event(journal, "review-completed", ticket=ticket)
    return _record_event(
        journal,
        "landing-started",
        ticket=ticket,
        payload={"review_sequence": review["sequence"]},
    )


def _git_evidence(
    landing: dict[str, Any], ticket: str, *, landed: bool = False
) -> dict[str, Any]:
    """Return complete R1 evidence for one exact landing event."""

    # Derive every observation and expected trailer from the selected window.
    payload = landing["payload"]
    trailers = {
        "Kntnt-Ticket": ticket,
        "Kntnt-Plan": f"sha256:{'2' * 64}",
    }
    return {
        "ticket": ticket,
        "landing_sequence": landing["sequence"],
        "integration_ref_head": (
            payload["candidate"] if landed else payload["previous_head"]
        ),
        "candidate_commit": payload["candidate"],
        "candidate_reachable": landed,
        "candidate_tree": payload["tree"],
        "test_blobs": payload["test_blobs"],
        "expected_trailers": trailers,
        "observed_trailers": trailers,
    }


def _transition_resolution(
    target_label: str | None, assignees: list[str]
) -> dict[str, Any]:
    """Return a portable transition receipt resolved outside the helper."""

    # Keep policy explicit while the journal validates only its receipt.
    return {
        "executable_ready_label": "custom-ready",
        "target_label": target_label,
        "preserved_labels": ["scope:rework", "priority:high"],
        "milestone": "Skills Next",
        "status": "open",
        "assignees": assignees,
        "agent_instruction_address": "AGENTS.md#issue-tracker",
        "issue_tracker_convention_address": "docs/agents/triage-labels.md",
    }


def _pre_projection() -> dict[str, Any]:
    """Return the tracker state observed before a portable transition."""

    # Describe the state against which the fixture transition was resolved.
    return {
        "labels": ["custom-ready", "scope:rework", "priority:high"],
        "milestone": "Skills Next",
        "status": "open",
        "assignees": ["thomas"],
    }


def _event_payload(
    journal: Any,
    event_type: str,
    *,
    ticket: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construct one schema-complete payload with exact sequence references."""

    # Supply the recovery-complete receipt for every event vocabulary member.
    payload_defaults: dict[str, dict[str, Any]] = {
        "selection-recorded": {"tickets": journal.metadata["selection"]},
        "bundle-consumed": {
            "bundle_fingerprint": f"sha256:{'2' * 64}",
            "execution_base": "1" * 40,
            "source_fingerprints": {
                "child_fingerprint": f"sha256:{'3' * 64}",
                "parent_fingerprint": f"sha256:{'4' * 64}",
            },
            "footprint": {
                "reads": [],
                "modifies": ["skills/code/dispatch/scripts/journal.py"],
                "creates": [],
                "deletes": [],
                "compiler_owned_tests": ["tests/test_dispatch_journal.py"],
                "dispatcher_owned_writes": [],
                "serial_resources": [],
            },
            "allocations": [],
            "tests": [
                {
                    "destination": "tests/test_dispatch_journal.py",
                    "compiled_blob": f"git:{'5' * 40}",
                }
            ],
            "command_ids": ["seam", "gate"],
            "done_criterion_ids": ["AC-1", "scope", "test-integrity"],
        },
        "bundle-released": {
            "bundle_fingerprint": f"sha256:{'2' * 64}",
            "reason": "stranded cleanup",
        },
        "route-recorded": {"attempt": 1, "decision": {"status": "selected"}},
        "ticket-assigned": {"assignee": "thomas"},
        "attempt-started": {
            "attempt": 1,
            "attempt_id": "#184/1",
            "base": "1" * 40,
            "worktree": "worktrees/run/184/1",
            "branch": "kntnt-dispatch/run/184/1",
        },
        "attempt-returned": {"attempt": 1},
        "patch-captured": {
            "attempt": 1,
            "changed_paths": ["skills/code/dispatch/scripts/journal.py"],
        },
        "dispatcher-write-recorded": {"paths": ["skills/kntnt/catalog.json"]},
        "review-completed": {
            "attempt": 1,
            "verdict": "APPROVE",
            "finding_summary": "All binding checks pass.",
        },
        "revise-requested": {
            "attempt": 2,
            "prior_attempt": 1,
            "review_sequence": 1,
        },
        "executor-rehydrated": {
            "attempt": 2,
            "revision_sequence": 1,
            "route_sequence": 1,
        },
        "rebuild-requested": {
            "review_sequence": 1,
            "head": "4" * 40,
            "compile_invocation": "/compile #184",
            "resume_invocation": "/dispatch #184",
        },
        "owner-answered": {"for_sequence": 1, "answer": "Use the binding plan."},
        "landing-started": {
            "review_sequence": 1,
            "previous_head": "1" * 40,
            "candidate": "3" * 40,
            "tree": "4" * 40,
            "test_blobs": {"tests/test_dispatch_journal.py": f"git:{'5' * 40}"},
        },
        "human-conflict": {
            "landing_sequence": 1,
            "attempt": 1,
            "branch": "kntnt-dispatch/run/184/1",
            "worktree": "worktrees/run/184/1",
        },
        "landed": {
            "landing_sequence": 1,
            "commit": "3" * 40,
            "tree": "4" * 40,
            "bundle_fingerprint": f"sha256:{'2' * 64}",
            "test_blobs": {"tests/test_dispatch_journal.py": f"git:{'5' * 40}"},
        },
        "parked": {
            "park_class": "owner-info",
            "message": "Which outcome should win?",
            "reason": "owner decision required",
            "patch_sequence": None,
        },
        "stranded": {"reason": "route refused"},
        "bundle-retired": {"bundle_fingerprint": f"sha256:{'2' * 64}"},
        "resource-cleaned": {"resources": []},
        "observation-recorded": {"attempt": 1},
        "run-completed": {"tickets": {"#184": "landed"}},
    }
    complete_payload = {**payload_defaults.get(event_type, {}), **(payload or {})}

    # Cleanup fixtures acknowledge every disposable attempt resource already
    # named by the durable projection.
    if event_type == "resource-cleaned" and "resources" not in (payload or {}):
        receipts = journal.project()["tickets"][ticket]["receipts"]
        complete_payload["resources"] = [
            entry["payload"][field]
            for entry in receipts.get("attempt-started", [])
            for field in ("worktree", "branch")
        ]

    # Sequence defaults bind dependent fixtures to the latest durable boundary.
    if ticket is not None:
        receipts = journal.project()["tickets"][ticket]["receipts"]

        def latest_sequence(kind: str) -> int | None:
            """Return the newest fixture receipt sequence for one event kind."""

            entries = receipts.get(kind, [])
            return entries[-1]["sequence"] if entries else None

        # Map each referencing event to its exact predecessor receipt kind.
        sequence_fields = {
            "revise-requested": ("review_sequence", "review-completed"),
            "executor-rehydrated": ("revision_sequence", "revise-requested"),
            "rebuild-requested": ("review_sequence", "review-completed"),
            "owner-answered": ("for_sequence", "human-conflict"),
            "landing-started": ("review_sequence", "review-completed"),
            "human-conflict": ("landing_sequence", "landing-started"),
            "landed": ("landing_sequence", "landing-started"),
            "parked": ("patch_sequence", "patch-captured"),
        }
        if event_type in sequence_fields:
            field, predecessor = sequence_fields[event_type]
            if field not in (payload or {}):
                complete_payload[field] = latest_sequence(predecessor)

        # Fresh-context fixtures also bind to the original Route point.
        if event_type == "executor-rehydrated" and "route_sequence" not in (
            payload or {}
        ):
            complete_payload["route_sequence"] = latest_sequence("route-recorded")

    # Return the schema-complete payload after all context-sensitive defaults.
    return complete_payload


def _event_artifacts(
    event_type: str, artifacts: dict[str, bytes] | None = None
) -> dict[str, bytes]:
    """Construct the complete durable artifact set for one event type."""

    # Supply every byte stream required by the event vocabulary.
    artifact_defaults: dict[str, dict[str, bytes]] = {
        "bundle-consumed": {
            "bundle-plan": b"# Plan\n",
            "bundle-manifest": b"{}\n",
            "bundle-tests": b"test bytes",
        },
        "route-recorded": {"route-response": b'{"decision":"selected"}\n'},
        "patch-captured": {"patch": b"diff"},
        "dispatcher-write-recorded": {"dispatcher-write-proposal": b"proposal"},
        "review-completed": {"review-finding": b"review finding"},
        "observation-recorded": {"observation-input": b"{}\n"},
    }
    return {**artifact_defaults.get(event_type, {}), **(artifacts or {})}


def _recompiled_bundle_payload(
    source_fingerprints: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return a bundle whose durable identity is valid after REBUILD."""

    # Change the bundle identity and base while accepting recorded source facts.
    return {
        "bundle_fingerprint": f"sha256:{'6' * 64}",
        "execution_base": "4" * 40,
        "source_fingerprints": source_fingerprints
        or {
            "child_fingerprint": f"sha256:{'3' * 64}",
            "parent_fingerprint": f"sha256:{'4' * 64}",
        },
    }


def _record_event(
    journal: Any,
    event_type: str,
    *,
    ticket: str | None = None,
    payload: dict[str, Any] | None = None,
    artifacts: dict[str, bytes] | None = None,
    recorded_at: str | None = None,
) -> dict[str, Any]:
    """Record one event assembled by the schema-complete fixture builders."""

    # Keep normal recording separate from deliberate schema fault injection.
    return dict(
        journal.record(
            event_type,
            ticket=ticket,
            payload=_event_payload(journal, event_type, ticket=ticket, payload=payload),
            artifacts=_event_artifacts(event_type, artifacts),
            recorded_at=recorded_at,
        )
    )


def _record_incomplete_event(
    journal: Any,
    event_type: str,
    *,
    ticket: str | None = None,
    missing_payload_field: str | None = None,
    missing_artifact: str | None = None,
) -> dict[str, Any]:
    """Inject one deliberate schema omission without burdening normal recording."""

    # Start from independently constructed valid payload and artifact surfaces.
    payload = _event_payload(journal, event_type, ticket=ticket)
    artifacts = _event_artifacts(event_type)

    # Remove only the boundary selected by the negative schema fixture.
    if missing_payload_field is not None:
        payload.pop(missing_payload_field, None)
    if missing_artifact is not None:
        artifacts.pop(missing_artifact)

    # Exercise journal refusal with the independently damaged event surfaces.
    return dict(
        journal.record(
            event_type,
            ticket=ticket,
            payload=payload,
            artifacts=artifacts,
        )
    )


def _record_tracker_transition(
    journal: Any,
    transition_id: str,
    target_label: str | None,
    assignees: list[str],
) -> dict[str, Any]:
    """Record one complete portable transition plan and verified completion."""

    # Persist the exact resolved mutation before modeling its observed result.
    resolution = _transition_resolution(target_label, assignees)
    planned = _record_event(
        journal,
        "tracker-transition-planned",
        ticket="#184",
        payload={
            "transition_id": transition_id,
            "resolution": resolution,
            "pre_projection": _pre_projection(),
        },
    )
    labels = ["scope:rework", "priority:high"]
    if target_label is not None:
        labels.append(target_label)

    # Repeat the resolution and observed projection in the completion boundary.
    return _record_event(
        journal,
        "tracker-transition-completed",
        ticket="#184",
        payload={
            "transition_id": transition_id,
            "planned_sequence": planned["sequence"],
            "resolution": resolution,
            "observed_post_projection": {
                "labels": labels,
                "milestone": "Skills Next",
                "status": "open",
                "assignees": assignees,
            },
        },
    )


def _record_terminal(journal: Any, terminal: str) -> None:
    """Record one schema-complete ticket through its terminal boundary."""

    # Establish the shared attempt prefix before selecting a terminal route.
    _record_attempt(journal)
    if terminal == "stranded":
        _record_event(journal, "stranded", ticket="#184")
        return

    # Landed and parked outcomes both require paid patch work to be durable.
    _record_event(journal, "patch-captured", ticket="#184")
    if terminal == "parked":
        _record_event(journal, "parked", ticket="#184")
        return

    # A landed outcome binds approval, landing window, and terminal receipt.
    review = _record_event(journal, "review-completed", ticket="#184")
    landing = _record_event(
        journal,
        "landing-started",
        ticket="#184",
        payload={"review_sequence": review["sequence"]},
    )
    _record_event(
        journal,
        "landed",
        ticket="#184",
        payload={"landing_sequence": landing["sequence"]},
    )


def _record_rebuild_boundary(journal: Any, *, should_release_bundle: bool) -> None:
    """Record the shared prefix through an optional post-REBUILD release."""

    # Reach the single durable request for a replacement compiled bundle.
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"verdict": "REBUILD"},
    )
    _record_event(journal, "rebuild-requested", ticket="#184")

    # Release the initial bundle only when the fixture crosses that boundary.
    if should_release_bundle:
        _record_event(journal, "bundle-released", ticket="#184")


def _complete_terminal(journal: Any, terminal: str) -> None:
    """Advance one terminal ticket through every archive prerequisite."""

    # Record the terminal-specific tracker and bundle disposition boundaries.
    if terminal == "landed":
        _record_tracker_transition(journal, "T-LAND", None, ["thomas"])
        _record_event(journal, "bundle-retired", ticket="#184")
    elif terminal == "parked":
        _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])
        _record_event(journal, "bundle-retired", ticket="#184")
    else:
        _record_event(journal, "bundle-released", ticket="#184")
    _record_event(journal, "resource-cleaned", ticket="#184")
    _record_event(journal, "run-completed", payload={"tickets": {"#184": terminal}})


def _leave_pending_archive(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    observation: bool = False,
) -> tuple[Any, dict[str, Any]]:
    """Move one parked run while leaving authenticated cleanup pending."""

    # Build a completed parked run with every retained artifact the case needs.
    opening = {**_opening(), "selection": ["#184"]}
    journal = module.Journal.open(tmp_path, opening, opened_at="2026-08-27T08:09:10Z")
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    _record_event(journal, "review-completed", ticket="#184")
    if observation:
        _record_event(journal, "observation-recorded", ticket="#184")
    _record_event(journal, "parked", ticket="#184")
    _complete_terminal(journal, "parked")
    original_finalize = module.Journal._finalize_archive

    # Interrupt exactly after the move so the next open exercises recovery.
    def interrupt_cleanup(self: Any) -> None:
        """Leave the archive at its authenticated pending boundary."""

        raise OSError("simulated pending archive")

    # Move the slot under interruption, then restore normal cleanup behavior.
    monkeypatch.setattr(module.Journal, "_finalize_archive", interrupt_cleanup)
    with pytest.raises(OSError, match="simulated pending archive"):
        journal.archive()
    monkeypatch.setattr(module.Journal, "_finalize_archive", original_finalize)
    return journal, opening


def _seed_artifact_event(journal: Any, event_type: str) -> None:
    """Record the exact predecessor prefix for one artifact crash fixture."""

    # Seed global and bundle predecessors needed by early artifact events.
    if event_type in {"bundle-consumed", "route-recorded"}:
        _record_event(journal, "selection-recorded")
    if event_type == "bundle-consumed":
        return
    if event_type == "route-recorded":
        _record_event(journal, "bundle-consumed", ticket="#184")
        return

    # Seed the executor and review predecessors needed by later artifact events.
    _record_attempt(journal)
    if event_type in {"review-completed", "observation-recorded"}:
        _record_event(journal, "patch-captured", ticket="#184")
    if event_type == "observation-recorded":
        _record_event(journal, "review-completed", ticket="#184")


def test_branch_slots_are_independent_and_one_invocation_owns_each(
    tmp_path: Path,
) -> None:
    """The full ref serializes one branch without blocking another branch."""

    # Open the same ref twice and a distinct ref once under one journal root.
    module = _load()
    first = _open(module, tmp_path)
    resumed = module.Journal.open(
        tmp_path, _opening(), opened_at="2026-08-27T09:00:00Z"
    )
    other = module.Journal.open(
        tmp_path,
        _opening(ref="refs/heads/feature/journal"),
        opened_at="2026-08-27T09:00:00Z",
    )

    # Verify ref-scoped ownership and deterministic slot naming.
    assert resumed.path == first.path
    assert other.path != first.path
    assert first.path.name == module.sha256_hex(b"refs/heads/rework")

    # Refuse a competing invocation that resolves to the occupied branch slot.
    with pytest.raises(
        module.JournalRefusal, match="active run opening does not match"
    ):
        module.Journal.open(
            tmp_path,
            _opening(invocation="/dispatch --at-once=1 #184"),
            opened_at="2026-08-27T09:00:00Z",
        )


def test_opening_metadata_explains_every_fingerprint_input(tmp_path: Path) -> None:
    """The fingerprint identifies concrete metadata instead of replacing it."""

    # Read the canonical opening metadata written for one deterministic run.
    module = _load()
    journal = _open(module, tmp_path)
    metadata = json.loads((journal.path / "metadata.json").read_text(encoding="utf-8"))

    # Verify every fingerprint input remains independently inspectable.
    assert metadata["schema"] == "kntnt.dispatch-journal/v1"
    assert metadata["opened_at"] == "2026-08-27T08:09:10Z"
    assert metadata["repository"] == "github.com/Kntnt/skills"
    assert metadata["integration_ref"] == "refs/heads/rework"
    assert metadata["opening_head"] == "1" * 40
    assert metadata["invocation"] == "/dispatch #184"
    assert metadata["instruction"] == "Keep the protected rework labels portable."
    assert metadata["selection"] == ["#184", "#185"]
    assert metadata["at_once"] == 2
    assert metadata["route"] == {"model": None, "deliberation": "medium"}
    assert metadata["run_fingerprint"] == module.run_fingerprint(_opening())


def test_events_are_canonical_contiguous_and_hash_chained(tmp_path: Path) -> None:
    """Each immutable event proves its predecessor and exact canonical bytes."""

    # Record a short prefix whose timestamps and ordering are deterministic.
    module = _load()
    journal = _open(module, tmp_path)
    _record_event(
        journal,
        "selection-recorded",
        payload={"tickets": ["#184", "#185"]},
        recorded_at="2026-08-27T08:10:00Z",
    )
    _record_event(journal, "bundle-consumed", ticket="#184")
    _record_event(journal, "route-recorded", ticket="#184")
    _record_event(
        journal,
        "ticket-assigned",
        ticket="#184",
        payload={"assignee": "thomas"},
        recorded_at="2026-08-27T08:11:00Z",
    )

    # Read the published bytes needed to verify naming and hash continuity.
    events = sorted((journal.path / "events").iterdir())
    first_bytes = events[0].read_bytes()
    second = json.loads(events[1].read_text(encoding="utf-8"))

    # Assert sequence names, canonical encoding, and predecessor hashes.
    assert [path.name for path in events] == [
        "00000001.json",
        "00000002.json",
        "00000003.json",
        "00000004.json",
    ]
    assert first_bytes == module.canonical_json(json.loads(first_bytes))
    assert second["previous_sha256"] == f"sha256:{module.sha256_hex(first_bytes)}"
    assert journal.validate()["event_count"] == 4


def test_canonical_json_uses_the_manifest_domain_and_utf16_key_order() -> None:
    """JCS bytes reject floats and follow UTF-16 property ordering."""

    # Construct keys whose Unicode and UTF-16 sort orders differ.
    module = _load()
    value = {"\ue000": 1, "\U00010000": 2, "line": "one\ntwo", "truth": True}

    # Verify canonical output and refusal outside the shared numeric domain.
    assert (
        module.canonical_json(value).decode()
        == '{"line":"one\\ntwo","truth":true,"𐀀":2,"":1}'
    )
    with pytest.raises(module.JournalRefusal, match="floating-point"):
        module.canonical_json({"invalid": 1.5})


def test_artifacts_are_durable_before_their_referring_event(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An event publication failure leaves at most an unreferenced artifact."""

    # Reach a patch boundary and retain the publisher used by other writes.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    original = module._atomic_publish

    def interrupt_event(path: Path, content: bytes) -> None:
        """Crash only at the event boundary after artifact publication."""

        if path.parent.name == "events":
            raise OSError("simulated event crash")
        original(path, content)

    # Install the crash only for the authoritative event publication.
    monkeypatch.setattr(module, "_atomic_publish", interrupt_event)

    # Attempt to record an event after its artifact has become durable.
    with pytest.raises(OSError, match="simulated event crash"):
        _record_event(
            journal,
            "patch-captured",
            ticket="#184",
            payload={"attempt": 1, "changed_paths": ["journal.py"]},
            artifacts={"patch": b"diff --git a/a b/a\n"},
        )

    # Confirm recovery sees no event but may safely ignore the complete bulk.
    artifacts = list((journal.path / "artifacts" / "patch").iterdir())
    assert len(artifacts) == 1
    assert artifacts[0].read_bytes() == b"diff --git a/a b/a\n"
    assert journal.validate()["event_count"] == 5


def test_event_publication_never_exposes_partial_or_temporary_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A rename-window crash leaves the authoritative sequence untouched."""

    # Build the durable prefix immediately before ticket assignment.
    module = _load()
    journal = _open(module, tmp_path)
    _record_event(journal, "selection-recorded")
    _record_event(journal, "bundle-consumed", ticket="#184")
    _record_event(journal, "route-recorded", ticket="#184")
    original = module.os.replace

    def interrupt_rename(source: Path, destination: Path) -> None:
        """Crash after the temporary file flush but before publication."""

        if Path(destination).parent.name == "events":
            raise OSError("simulated rename crash")
        original(source, destination)

    # Interrupt only the rename that would publish the next event.
    monkeypatch.setattr(module.os, "replace", interrupt_rename)

    # Exercise the temporary-file crash window.
    with pytest.raises(OSError, match="simulated rename crash"):
        _record_event(
            journal, "ticket-assigned", ticket="#184", payload={"assignee": "thomas"}
        )

    # Verify that neither partial bytes nor an apparent fourth event escaped.
    assert journal.validate()["event_count"] == 3


def test_artifact_references_carry_digest_length_and_relative_path(
    tmp_path: Path,
) -> None:
    """Every event can validate the exact durable bytes it names."""

    # Record an observation whose exact bytes have a known digest and length.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    _record_event(journal, "review-completed", ticket="#184")
    event = _record_event(
        journal,
        "observation-recorded",
        ticket="#184",
        payload={"attempt": 1},
        artifacts={"observation-input": b"{}\n"},
    )
    reference = event["artifacts"]["observation-input"]

    # Verify the complete relative artifact identity and aggregate validation.
    assert reference == {
        "path": f"artifacts/observation-input/{module.sha256_hex(b'{}\n')}",
        "sha256": f"sha256:{module.sha256_hex(b'{}\n')}",
        "byte_length": 3,
    }
    assert journal.validate()["artifact_count"] == 7


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("last_event", "expected_action"),
    [
        ("attempt-started", "replay-attempt"),
        ("attempt-returned", "replay-attempt"),
        ("patch-captured", "review-patch"),
        ("revise-requested", "resume-revision"),
        ("landing-started", "reconcile-landing"),
        ("rebuild-requested", "await-recompile"),
        ("human-conflict", "resume-human-conflict"),
        ("landed", "complete-tracker-transition"),
        ("parked", "complete-tracker-transition"),
        ("tracker-transition-completed", "retire-bundle"),
        ("stranded", "release-bundle"),
    ],
)
def test_projection_distinguishes_each_recovery_window(
    tmp_path: Path, last_event: str, expected_action: str
) -> None:
    """Resume derives one safe next action from the immutable prefix."""

    # Establish the common executor prefix shared by every recovery boundary.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)

    # Extend the common prefix only as far as this crash fixture requires.
    if last_event not in {"attempt-started", "attempt-returned"}:
        _record_event(
            journal,
            "patch-captured",
            ticket="#184",
            payload={
                "attempt": 1,
                "changed_paths": ["skills/code/dispatch/scripts/journal.py"],
            },
            artifacts={"patch": b"diff"},
        )
    if last_event == "attempt-returned":
        _record_event(journal, "attempt-returned", ticket="#184")
    elif last_event == "revise-requested":
        _record_event(
            journal,
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "REVISE"},
        )
        _record_event(
            journal,
            "revise-requested",
            ticket="#184",
            payload={"attempt": 2},
        )
    elif last_event == "landing-started":
        _record_event(
            journal,
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "APPROVE"},
        )
        _record_event(
            journal,
            "landing-started",
            ticket="#184",
            payload={"candidate": "3" * 40, "previous_head": "1" * 40},
        )
    elif last_event == "rebuild-requested":
        _record_event(
            journal,
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "REBUILD"},
        )
        _record_event(
            journal, "rebuild-requested", ticket="#184", payload={"head": "4" * 40}
        )
    elif last_event == "human-conflict":
        review = _record_event(
            journal,
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "REBUILD"},
        )
        _record_event(
            journal,
            "landing-started",
            ticket="#184",
            payload={"review_sequence": review["sequence"]},
        )
        _record_event(
            journal,
            "human-conflict",
            ticket="#184",
            payload={
                "branch": "kntnt-dispatch/run/184/1",
                "worktree": "worktrees/run/184/1",
            },
        )
    elif last_event in {"landed", "tracker-transition-completed"}:
        _record_event(
            journal,
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "APPROVE"},
        )
        _record_event(
            journal,
            "landing-started",
            ticket="#184",
            payload={"candidate": "3" * 40, "previous_head": "1" * 40},
        )
        _record_event(
            journal,
            "landed",
            ticket="#184",
            payload={"commit": "3" * 40, "tree": "4" * 40},
        )
    elif last_event == "parked":
        _record_event(
            journal,
            "parked",
            ticket="#184",
            payload={
                "park_class": "owner-info",
                "message": "Which outcome should win?",
            },
        )
    elif last_event == "stranded":
        _record_event(
            journal, "stranded", ticket="#184", payload={"reason": "route refused"}
        )

    # A completed tracker transition is the durable gate before retirement.
    if last_event == "tracker-transition-completed":
        _record_tracker_transition(journal, "T-LAND", None, ["thomas"])

    # Assert the newest boundary selects the expected recovery action.
    assert journal.project()["tickets"]["#184"]["recovery_action"] == expected_action


def test_tracker_completion_repeats_and_verifies_the_portable_resolution(
    tmp_path: Path,
) -> None:
    """Changed conventions cannot alter a transition already made durable."""

    # Complete one parked transition with a portable resolved tracker receipt.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    _record_event(
        journal,
        "parked",
        ticket="#184",
        payload={
            "park_class": "owner-info",
            "message": "Which outcome should win?",
        },
    )
    completed = _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])

    # Confirm the exact resolved mutation is part of validated state.
    assert completed["payload"]["resolution"]["target_label"] == "needs-owner"
    assert journal.validate()["event_count"] == 8

    # Refuse a completion observation that contradicts the durable resolution.
    with pytest.raises(module.JournalRefusal, match="observed tracker projection"):
        resolution = _transition_resolution("needs-owner", [])
        _record_event(
            journal,
            "tracker-transition-completed",
            ticket="#184",
            payload={
                "transition_id": "T-PARK-INFO",
                "planned_sequence": completed["payload"]["planned_sequence"],
                "resolution": resolution,
                "observed_post_projection": {
                    "labels": ["scope:rework", "needs-info"],
                    "milestone": "Skills Next",
                    "status": "open",
                    "assignees": [],
                },
            },
        )


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("transition_id", "terminal", "park_class", "target_label", "assignees"),
    [
        ("T-LAND", "landed", None, None, ["thomas"]),
        ("T-PARK-INFO", "parked", "owner-info", "awaiting-context", []),
        ("T-PARK-HUMAN", "parked", "human-repair", "manual-repair", []),
    ],
)
def test_each_tracker_transition_keeps_concrete_resolution_receipts(
    tmp_path: Path,
    transition_id: str,
    terminal: str,
    park_class: str | None,
    target_label: str | None,
    assignees: list[str],
) -> None:
    """Every transition survives with non-default labels and convention sources."""

    # Reach the transition's matching terminal state from one consumed attempt.
    module = _load()
    journal = _open(module, tmp_path)
    if terminal == "landed":
        # A landing transition follows independently verified Git evidence.
        _record_terminal(journal, terminal)

    else:
        # A parking transition records its exact information or repair class.
        _record_attempt(journal)
        _record_event(journal, "patch-captured", ticket="#184")
        _record_event(
            journal,
            "parked",
            ticket="#184",
            payload={"park_class": park_class},
        )

    # Persist and repeat the concrete convention resolution around mutation.
    completed = _record_tracker_transition(
        journal,
        transition_id,
        target_label,
        assignees,
    )
    receipts = journal.project()["tickets"]["#184"]["receipts"]
    planned = receipts["tracker-transition-planned"][-1]

    # Verify both receipts preserve labels, assignment, and convention sources.
    assert planned["payload"]["transition_id"] == transition_id
    assert completed["payload"]["transition_id"] == transition_id
    assert completed["payload"]["resolution"] == planned["payload"]["resolution"]
    assert planned["payload"]["resolution"]["executable_ready_label"] == "custom-ready"
    assert planned["payload"]["resolution"]["target_label"] == target_label
    assert planned["payload"]["resolution"]["preserved_labels"] == [
        "scope:rework",
        "priority:high",
    ]
    assert completed["payload"]["observed_post_projection"]["assignees"] == assignees
    assert planned["payload"]["resolution"]["agent_instruction_address"]
    assert planned["payload"]["resolution"]["issue_tracker_convention_address"]


def test_projection_is_idempotent_and_preserves_every_ticket_receipt(
    tmp_path: Path,
) -> None:
    """A complete in-memory account is derived without a mutable state file."""

    # Record recoverable executor receipts and snapshot every persistent path.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1, "changed_paths": ["journal.py"]},
        artifacts={"patch": b"diff"},
    )
    before = sorted(path.relative_to(journal.path) for path in journal.path.rglob("*"))

    # Project twice and snapshot the filesystem again around the read-only work.
    first = journal.project()
    second = journal.project()
    after = sorted(path.relative_to(journal.path) for path in journal.path.rglob("*"))

    # Verify deterministic projection, neutrality, and receipt retention.
    assert second == first
    assert after == before
    receipts = first["tickets"]["#184"]["receipts"]
    assert receipts["route-recorded"][0]["artifacts"]["route-response"]
    assert receipts["patch-captured"][0]["payload"]["changed_paths"] == ["journal.py"]


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "corruption", ["missing-artifact", "broken-chain", "sequence-gap"]
)
def test_validation_refuses_corrupt_durable_state(
    tmp_path: Path, corruption: str
) -> None:
    """Recovery never repairs or infers through an ambiguous journal."""

    # Build a valid event and artifact prefix before injecting one corruption.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1},
        artifacts={"patch": b"diff"},
    )
    _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"attempt": 1, "verdict": "APPROVE"},
    )
    events = sorted((journal.path / "events").iterdir())

    # Corrupt one independent identity or ordering invariant.
    if corruption == "missing-artifact":
        next((journal.path / "artifacts" / "patch").iterdir()).unlink()
    elif corruption == "broken-chain":
        value = json.loads(events[1].read_text(encoding="utf-8"))
        value["previous_sha256"] = f"sha256:{'0' * 64}"
        events[1].write_bytes(module.canonical_json(value))
    else:
        events[1].rename(events[1].with_name("00000003.json"))

    # Refuse every ambiguous durable prefix instead of attempting repair.
    with pytest.raises(module.JournalRefusal):
        journal.validate()


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("field", "contradiction"),
    [
        ("candidate_commit", "9" * 40),
        ("candidate_tree", "9" * 40),
        ("test_blobs", {"tests/test_dispatch_journal.py": f"git:{'9' * 40}"}),
        (
            "expected_trailers",
            {"Kntnt-Ticket": "#184", "Kntnt-Plan": f"sha256:{'9' * 64}"},
        ),
        (
            "observed_trailers",
            {"Kntnt-Ticket": "#185", "Kntnt-Plan": f"sha256:{'2' * 64}"},
        ),
    ],
)
def test_previous_head_still_validates_every_candidate_identity(
    tmp_path: Path, field: str, contradiction: Any
) -> None:
    """An unadvanced ref never bypasses candidate or R1 trailer validation."""

    # Build one valid landing window whose integration ref has not advanced.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    landing = _record_landing_window(journal, "#184")
    evidence = _git_evidence(landing, "#184")

    # Validate the complete previous-head evidence before fault injection.
    assert journal.project(git_evidence=[evidence])

    # Mutate exactly one candidate fact after the valid control assertion.
    evidence[field] = contradiction

    # Reject the single candidate fact changed by the parameterized fixture.
    with pytest.raises(module.JournalRefusal, match="contradictory Git evidence"):
        journal.project(git_evidence=[evidence])


def test_git_evidence_selects_concurrent_windows_by_ticket_and_sequence(
    tmp_path: Path,
) -> None:
    """Concurrent candidates cannot borrow another ticket's Git observations."""

    # Interleave two ticket-specific landing windows in one run journal.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal, "#184")
    first = _record_landing_window(journal, "#184")
    _record_ticket_attempt(journal, "#185")
    second = _record_landing_window(journal, "#185")
    evidence = [_git_evidence(first, "#184"), _git_evidence(second, "#185")]

    # Both exact windows validate regardless of their global event order.
    assert journal.project(git_evidence=evidence)

    # Retarget one observation only after validating both exact windows.
    evidence[0]["landing_sequence"] = second["sequence"]

    # Reject evidence retargeted to the other concurrent ticket's window.
    with pytest.raises(module.JournalRefusal, match="sequence does not name"):
        journal.project(git_evidence=evidence)


def test_landing_tests_are_bound_to_the_latest_consumed_bundle(tmp_path: Path) -> None:
    """A caller cannot invent protected-test identities at landing time."""

    # Reach an approved landing boundary backed by one canonical bundle map.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    review = _record_event(journal, "review-completed", ticket="#184")

    # Refuse a landing map that differs from its consumed bundle destination.
    with pytest.raises(module.JournalRefusal, match="landing tests contradict"):
        _record_event(
            journal,
            "landing-started",
            ticket="#184",
            payload={
                "review_sequence": review["sequence"],
                "test_blobs": {"tests/other.py": f"git:{'9' * 40}"},
            },
        )


def test_git_evidence_cannot_agree_with_a_landing_that_contradicts_its_bundle(
    tmp_path: Path,
) -> None:
    """R1 evidence remains independently bound to canonical bundle tests."""

    # Start from a validated landing window and its durable event prefix.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    landing = _record_landing_window(journal, "#184")
    events = journal._read_validated()["events"]
    contradictory = {"tests/other.py": f"git:{'9' * 40}"}
    events[landing["sequence"] - 1]["payload"]["test_blobs"] = contradictory
    evidence = _git_evidence(landing, "#184")
    evidence["test_blobs"] = contradictory

    # Agreement between landing and Git cannot override the bundle.
    with pytest.raises(module.JournalRefusal, match="contradictory Git evidence"):
        module._validate_git_evidence(events, [evidence])


def test_completion_archives_atomically_and_retains_a_parked_patch(
    tmp_path: Path,
) -> None:
    """The active slot becomes one compact archive without losing paid work."""

    # Complete a parked run containing one superseded and one retained patch.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    older_patch = _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1},
        artifacts={"patch": b"superseded patch"},
    )
    latest_patch = _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1},
        artifacts={"patch": b"valuable patch"},
    )
    _record_event(
        journal,
        "parked",
        ticket="#184",
        payload={"park_class": "owner-info", "message": "Choose A or B?"},
    )
    _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])
    _record_event(
        journal,
        "bundle-retired",
        ticket="#184",
        payload={"bundle_fingerprint": f"sha256:{'2' * 64}"},
    )
    _record_event(journal, "resource-cleaned", ticket="#184")
    _record_event(journal, "run-completed", payload={"tickets": {"#184": "parked"}})

    # Move the completed slot and read its compact authenticated receipt.
    archive = journal.archive()
    receipt = json.loads((archive / "receipt.json").read_text(encoding="utf-8"))

    # Verify audit identity, R2 retention, and removal of retired bulk.
    assert journal.path == archive
    assert list((tmp_path / "active").iterdir()) == []
    assert archive.parent == tmp_path / "archive"
    assert receipt["run_fingerprint"] == module.run_fingerprint(
        {**_opening(), "selection": ["#184"]}
    )
    assert receipt["tickets"]["#184"]["terminal"] == "parked"
    assert set(receipt["tickets"]["#184"]["bundle"]["source_fingerprints"]) == {
        "child_fingerprint",
        "parent_fingerprint",
    }
    assert receipt["tickets"]["#184"]["route_decisions"][0]["attempt"] == 1
    assert receipt["retained_artifacts"] == [latest_patch["artifacts"]["patch"]]
    assert not (archive / older_patch["artifacts"]["patch"]["path"]).exists()
    assert (archive / latest_patch["artifacts"]["patch"]["path"]).is_file()
    assert receipt["tickets"]["#184"]["bundle"]["footprint"]
    assert receipt["tickets"]["#184"]["route_decisions"] == [
        {"attempt": 1, "decision": {"status": "selected"}}
    ]
    assert receipt["tickets"]["#184"]["retained_patch"]["byte_length"] == 14
    assert (archive / "artifacts" / "patch").is_dir()
    assert not (archive / "artifacts" / "bundle-plan").exists()
    assert not (archive / "artifacts" / "route-response").exists()


def test_compact_receipt_preserves_validated_serial_allocations(tmp_path: Path) -> None:
    """Archive audit fields retain the exact compiled-plan allocation contract."""

    # Consume one bundle with an exact declared serial allocation.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_event(journal, "selection-recorded")
    payload = _event_payload(journal, "bundle-consumed", ticket="#184")
    payload["footprint"]["serial_resources"] = ["docs/adr"]
    payload["allocations"] = [{"registry": "docs/adr", "identifiers": ["0113", "0114"]}]
    _record_event(journal, "bundle-consumed", ticket="#184", payload=payload)
    _record_event(journal, "route-recorded", ticket="#184")
    _record_event(journal, "ticket-assigned", ticket="#184")
    _record_event(journal, "attempt-started", ticket="#184")
    _record_event(journal, "patch-captured", ticket="#184")
    _record_event(journal, "parked", ticket="#184")
    _complete_terminal(journal, "parked")

    # Archiving must copy the validated audit values without flattening them.
    archive = journal.archive()
    receipt = json.loads((archive / "receipt.json").read_text(encoding="utf-8"))
    ticket_receipt = receipt["tickets"]["#184"]

    # Verify allocation structure and Route attempt identity remain intact.
    assert ticket_receipt["bundle"]["allocations"] == payload["allocations"]
    assert ticket_receipt["route_decisions"][0] == {
        "attempt": 1,
        "decision": {"status": "selected"},
    }


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("corruption", "message"),
    [
        ("source-shape", "source_fingerprints"),
        ("allocation-registry", "allocation receipt"),
        ("missing-allocation", "do not cover serial_resources"),
        ("test-destination", "compiler_owned_tests"),
        ("overlapping-writes", "footprint classes overlap"),
    ],
)
def test_bundle_consumption_refuses_invalid_compiled_plan_audit_fields(
    tmp_path: Path, corruption: str, message: str
) -> None:
    """A consumed bundle is verified before it can supersede recovery state."""

    # Construct the valid compact audit subset before injecting one defect.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_event(journal, "selection-recorded")
    payload = _event_payload(journal, "bundle-consumed", ticket="#184")

    # Corrupt one independent compiled-plan audit invariant.
    if corruption == "source-shape":
        payload["source_fingerprints"] = {"child": f"sha256:{'3' * 64}"}
    elif corruption == "allocation-registry":
        payload["allocations"] = [{"registry": "docs/adr", "identifiers": ["0113"]}]
    elif corruption == "missing-allocation":
        payload["footprint"]["serial_resources"] = ["docs/adr"]
    elif corruption == "test-destination":
        payload["tests"][0]["destination"] = "tests/other.py"
    else:
        payload["footprint"]["creates"] = ["skills/code/dispatch/scripts/journal.py"]

    # Refuse the malformed bundle before its consumption event becomes durable.
    with pytest.raises(module.JournalRefusal, match=message):
        _record_event(journal, "bundle-consumed", ticket="#184", payload=payload)


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("footprint_field", "path"),
    [
        ("reads", "src/*.py"),
        ("modifies", "src/file?.py"),
        ("creates", "src/[ab].py"),
        ("deletes", "docs/**/old.md"),
        ("compiler_owned_tests", "tests/test_[ab].py"),
        ("dispatcher_owned_writes", "skills/?/catalog.json"),
        ("serial_resources", "docs/adr/[0-9]*"),
    ],
)
def test_every_bundle_footprint_class_refuses_glob_syntax(
    tmp_path: Path, footprint_field: str, path: str
) -> None:
    """Compiled footprint paths are literal relative POSIX identities."""

    # Put one glob spelling into each independently validated footprint class.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_event(journal, "selection-recorded")
    payload = _event_payload(journal, "bundle-consumed", ticket="#184")
    payload["footprint"][footprint_field] = [path]
    if footprint_field == "compiler_owned_tests":
        payload["tests"][0]["destination"] = path
    if footprint_field == "serial_resources":
        payload["allocations"] = [{"registry": path, "identifiers": ["one"]}]

    # No matching semantics may enter the durable compiled-plan receipt.
    with pytest.raises(module.JournalRefusal, match="bundle footprint"):
        _record_event(journal, "bundle-consumed", ticket="#184", payload=payload)


def test_bundle_footprint_accepts_literal_relative_posix_paths(tmp_path: Path) -> None:
    """Punctuation without glob meaning remains valid in compiled paths."""

    # Exercise every footprint class with a distinct literal relative path.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_event(journal, "selection-recorded")
    payload = _event_payload(journal, "bundle-consumed", ticket="#184")
    payload["footprint"] = {
        "reads": ["src/read-file.py"],
        "modifies": ["src/modify_file.py"],
        "creates": ["src/new.file+one.py"],
        "deletes": ["docs/old-file.md"],
        "compiler_owned_tests": ["tests/test.literal.py"],
        "dispatcher_owned_writes": ["skills/kntnt/catalog-v2.json"],
        "serial_resources": ["docs/adr"],
    }
    payload["tests"] = [
        {"destination": "tests/test.literal.py", "compiled_blob": f"git:{'5' * 40}"}
    ]
    payload["allocations"] = [{"registry": "docs/adr", "identifiers": ["0113"]}]

    # The schema accepts exact paths while preserving their literal spelling.
    event = _record_event(journal, "bundle-consumed", ticket="#184", payload=payload)
    assert event["payload"]["footprint"] == payload["footprint"]


def test_archive_refuses_an_incomplete_run(tmp_path: Path) -> None:
    """Moving an active prefix cannot masquerade as terminal completion."""

    # Leave one active run at a nonterminal executor boundary.
    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)

    # Refuse the archive move before any active-slot state changes.
    with pytest.raises(module.JournalRefusal, match="run-completed"):
        journal.archive()


def test_event_vocabulary_covers_dispatch_without_owning_its_decisions() -> None:
    """Persistence names every boundary while policy remains in the Skill."""

    # Load the vocabulary and enumerate required persistence boundaries.
    module = _load()
    required = {
        "selection-recorded",
        "bundle-consumed",
        "route-recorded",
        "ticket-assigned",
        "attempt-started",
        "attempt-returned",
        "patch-captured",
        "review-completed",
        "revise-requested",
        "executor-rehydrated",
        "rebuild-requested",
        "owner-answered",
        "landing-started",
        "human-conflict",
        "landed",
        "parked",
        "stranded",
        "tracker-transition-planned",
        "tracker-transition-completed",
        "bundle-retired",
        "resource-cleaned",
        "observation-recorded",
        "run-completed",
    }

    # Verify vocabulary coverage and the absence of external policy mechanisms.
    assert required <= module.EVENT_TYPES
    source = JOURNAL_PATH.read_text(encoding="utf-8")
    for forbidden in (
        "import subprocess",
        "import requests",
        "import gh",
        "git merge",
        "wave scheduler",
    ):
        assert forbidden not in source


def test_internal_cli_opens_and_projects_the_same_validated_slot(
    tmp_path: Path, capfd: pytest.CaptureFixture[str]
) -> None:
    """The Skill can drive the deep interface through stable JSON responses."""

    # Prepare the same opening document for two separate CLI invocations.
    module = _load()
    opening_path = tmp_path / "opening.json"
    opening_path.write_text(json.dumps(_opening()), encoding="utf-8")
    arguments = ["--root", str(tmp_path / "journal"), "--opening", str(opening_path)]

    # Open the slot and verify its immutable invocation identity.
    assert module.main(["open", *arguments]) == 0
    opened = json.loads(capfd.readouterr().out)
    assert opened["metadata"]["run_fingerprint"] == module.run_fingerprint(_opening())

    # Project the same slot through the CLI without bypassing validation.
    assert module.main(["project", *arguments]) == 0
    projected = json.loads(capfd.readouterr().out)
    assert projected["tickets"]["#184"]["recovery_action"] == "start-ticket"


def test_journal_is_in_both_strict_mypy_gates() -> None:
    """The shipped helper cannot regress outside the documented CI contract."""

    # Name the exact script path that both strict gate definitions must include.
    journal_argument = "skills/code/dispatch/scripts/journal.py"

    # Verify contributor and automation commands enforce the same typed surface.
    assert journal_argument in CONTRIBUTING_PATH.read_text(encoding="utf-8")
    assert journal_argument in CI_PATH.read_text(encoding="utf-8")


def test_business_state_uses_one_typed_representation() -> None:
    """Event, transition, terminal, and recovery values are typed once."""

    # Load the public vocabulary exported by the persistence module.
    module = _load()

    # Verify enum identities and self-describing lexical validators together.
    assert module.EventType.PATCH_CAPTURED.value == "patch-captured"
    assert module.TransitionId.LAND.value == "T-LAND"
    assert module.TerminalState.PARKED.value == "parked"
    assert module.RecoveryAction.REVIEW_PATCH.value == "review-patch"
    assert module.ContinuationMode.FRESH.value == "fresh-context"
    assert (
        module.TERMINAL_REQUIREMENTS[module.TerminalState.STRANDED].bundle_boundary
        is module.EventType.BUNDLE_RELEASED
    )
    assert (
        module.TERMINAL_REQUIREMENTS[
            module.TerminalState.STRANDED
        ].requires_tracker_completion
        is False
    )
    assert module.ARTIFACT_KIND_PATTERN.fullmatch("route-response")
    assert module.TICKET_REFERENCE_PATTERN.fullmatch("#184")
    assert module.OBJECT_ID_PATTERN.fullmatch("1" * 40)
    assert module.CONTENT_DIGEST_PATTERN.fullmatch(f"sha256:{'2' * 64}")
    assert module.COMPILED_BLOB_PATTERN.fullmatch(f"git:{'3' * 40}")
    assert module.UTC_INSTANT_PATTERN.fullmatch("2026-08-27T08:09:10Z")


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "event_type", [event_type.value for event_type in _load().EventType]
)
def test_every_event_refuses_an_incomplete_recovery_payload(
    tmp_path: Path, event_type: str
) -> None:
    """No vocabulary entry becomes durable without every recovery field."""

    # Select one mandatory payload field from the parameterized event schema.
    module = _load()
    journal = _open(module, tmp_path)
    field = min(module.EVENT_PAYLOAD_FIELDS[module.EventType(event_type)])
    ticket = None if event_type in {"selection-recorded", "run-completed"} else "#184"

    # Refuse the deliberately incomplete payload before event publication.
    with pytest.raises(module.JournalRefusal, match="payload fields are incomplete"):
        _record_incomplete_event(
            journal,
            event_type,
            ticket=ticket,
            missing_payload_field=field,
        )

    # Confirm failed schema construction left no durable event behind.
    assert journal.validate()["event_count"] == 0


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("event_type", "artifact"),
    [
        ("bundle-consumed", "bundle-plan"),
        ("route-recorded", "route-response"),
        ("patch-captured", "patch"),
        ("dispatcher-write-recorded", "dispatcher-write-proposal"),
        ("review-completed", "review-finding"),
        ("observation-recorded", "observation-input"),
    ],
)
def test_every_artifact_event_refuses_incomplete_recovery_bulk(
    tmp_path: Path, event_type: str, artifact: str
) -> None:
    """Artifact-bearing boundaries publish only with their exact durable bulk."""

    # Prepare an empty slot for one parameterized artifact-bearing event.
    module = _load()
    journal = _open(module, tmp_path)

    # Refuse the event after removing exactly one required artifact kind.
    with pytest.raises(
        module.JournalRefusal, match="recovery artifacts are incomplete"
    ):
        _record_incomplete_event(
            journal,
            event_type,
            ticket="#184",
            missing_artifact=artifact,
        )

    # Confirm neither an event nor an incomplete recovery claim became durable.
    assert journal.validate()["event_count"] == 0


def test_newer_attempt_events_supersede_older_revision_state(tmp_path: Path) -> None:
    """A later round, not an old monotone flag, decides recovery."""

    # Record one complete first attempt ending in a durable revision request.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1, "changed_paths": ["journal.py"]},
        artifacts={"patch": b"first patch"},
    )
    review = _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"attempt": 1, "verdict": "REVISE"},
    )
    _record_event(
        journal,
        "revise-requested",
        ticket="#184",
        payload={
            "attempt": 2,
            "prior_attempt": 1,
            "review_sequence": review["sequence"],
        },
    )
    _record_event(
        journal,
        "route-recorded",
        ticket="#184",
        payload={"attempt": 2},
    )
    _record_event(
        journal,
        "attempt-started",
        ticket="#184",
        payload={"attempt": 2, "base": "1" * 40},
    )

    # Verify the newer attempt boundary supersedes the earlier revision flag.
    assert journal.project()["tickets"]["#184"]["recovery_action"] == "replay-attempt"

    # Capture the newer attempt's patch as the latest recovery boundary.
    _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 2, "changed_paths": ["journal.py"]},
        artifacts={"patch": b"second patch"},
    )

    # Verify recovery follows the newer patch instead of older state.
    assert journal.project()["tickets"]["#184"]["recovery_action"] == "review-patch"


def test_archive_requires_every_terminal_cleanup_boundary(tmp_path: Path) -> None:
    """A terminal label alone cannot erase unfinished recovery work."""

    # Stop a valid landed ticket before tracker, retirement, and cleanup facts.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1},
    )
    review = _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"attempt": 1, "verdict": "APPROVE"},
    )
    landing = _record_event(
        journal,
        "landing-started",
        ticket="#184",
        payload={"review_sequence": review["sequence"]},
    )
    _record_event(
        journal,
        "landed",
        ticket="#184",
        payload={
            "landing_sequence": landing["sequence"],
            "commit": "3" * 40,
            "tree": "4" * 40,
        },
    )

    # Refuse completion while the shared terminal prerequisites remain absent.
    with pytest.raises(module.JournalRefusal, match="cleanup"):
        _record_event(journal, "run-completed", payload={"tickets": {"#184": "landed"}})


def test_stranded_refuses_cleanup_before_bundle_release(tmp_path: Path) -> None:
    """Stranding preserves the canonical plan slot while releasing run escrow."""

    # Stop one ticket exactly at its stranded terminal boundary.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_terminal(journal, "stranded")

    # Cleanup cannot imply release or misuse the landed/parked retirement fact.
    with pytest.raises(module.JournalRefusal, match="requires bundle release"):
        _record_event(journal, "resource-cleaned", ticket="#184")

    # Confirm the refused cleanup did not invent landed/parked retirement state.
    assert "bundle-retired" not in journal.project()["tickets"]["#184"]["receipts"]


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "boundary", ["run-completed", "archive"]
)
def test_stranded_release_is_required_by_later_completion_gates(
    tmp_path: Path, boundary: str
) -> None:
    """Run completion and archive readiness independently require release."""

    # Build a valid stranded prefix without its required release receipt.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_terminal(journal, "stranded")
    events = journal._read_validated()["events"]

    # Add only a synthetic cleanup envelope to isolate each later order gate.
    events.append({"type": "resource-cleaned", "ticket": "#184"})
    with pytest.raises(module.JournalRefusal, match="release"):
        if boundary == "run-completed":
            module._validate_run_completion_payload(
                {"tickets": {"#184": "stranded"}}, events
            )
        else:
            module._validate_archive_readiness(events, journal.project())


def test_stranded_archive_releases_escrow_without_retiring_canonical_slot(
    tmp_path: Path,
) -> None:
    """Stranded completion records release while leaving accepted plan state alone."""

    # Place canonical plan state outside the journal before completing the run.
    module = _load()
    journal_root = tmp_path / "journal"
    journal = _open(module, journal_root, selection=["#184"])
    canonical_slot = tmp_path / "git-common" / "kntnt-pipeline" / "plans" / "184"
    canonical_slot.mkdir(parents=True)
    accepted = canonical_slot / "accepted"
    accepted.write_text(f"bundles/{'2' * 64}\n", encoding="utf-8")
    _record_terminal(journal, "stranded")
    _complete_terminal(journal, "stranded")

    # Archive retains a release receipt and never emits retirement semantics.
    assert "bundle-retired" not in journal.project()["tickets"]["#184"]["receipts"]
    archive = journal.archive()
    receipt = json.loads((archive / "receipt.json").read_text(encoding="utf-8"))

    # Confirm the release receipt and external canonical pointer both survive.
    assert receipt["tickets"]["#184"]["bundle_release"]["reason"]
    assert accepted.read_text(encoding="utf-8") == f"bundles/{'2' * 64}\n"


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("terminal", "boundary", "expected_action"),
    [
        ("landed", "terminal", "complete-tracker-transition"),
        ("landed", "tracker", "retire-bundle"),
        ("landed", "retirement", "clean-resources"),
        ("landed", "cleanup", "complete-run"),
        ("parked", "terminal", "complete-tracker-transition"),
        ("parked", "tracker", "retire-bundle"),
        ("parked", "retirement", "clean-resources"),
        ("parked", "cleanup", "complete-run"),
        ("stranded", "terminal", "release-bundle"),
        ("stranded", "release", "clean-stranded"),
        ("stranded", "cleanup", "complete-run"),
    ],
)
def test_each_terminal_cleanup_boundary_reopens_to_one_projection(
    tmp_path: Path, terminal: str, boundary: str, expected_action: str
) -> None:
    """Every terminal crash prefix reopens the same branch slot idempotently."""

    # Record the terminal and preserve deterministic opening inputs.
    module = _load()
    opening = {**_opening(), "selection": ["#184"]}
    journal = module.Journal.open(tmp_path, opening, opened_at="2026-08-27T08:09:10Z")
    _record_terminal(journal, terminal)

    # Advance only through the durable boundary this crash fixture names.
    if boundary in {"tracker", "retirement", "cleanup"}:
        if terminal == "landed":
            _record_tracker_transition(journal, "T-LAND", None, ["thomas"])
        elif terminal == "parked":
            _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])
    if boundary in {"retirement", "cleanup"} and terminal != "stranded":
        _record_event(journal, "bundle-retired", ticket="#184")
    if terminal == "stranded" and boundary in {"release", "cleanup"}:
        _record_event(journal, "bundle-released", ticket="#184")
    if boundary == "cleanup":
        _record_event(journal, "resource-cleaned", ticket="#184")

    # Reopen directly after the selected terminal prerequisite boundary.
    reopened = module.Journal.open(tmp_path, opening)

    # Verify slot identity and the exact next recovery action after the crash.
    assert reopened.path == journal.path
    assert reopened.project()["tickets"]["#184"]["recovery_action"] == expected_action


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "event_type",
    [
        "bundle-consumed",
        "route-recorded",
        "patch-captured",
        "dispatcher-write-recorded",
        "review-completed",
        "observation-recorded",
    ],
)
def test_each_artifact_event_crash_reopens_before_the_event(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    event_type: str,
) -> None:
    """Every artifact/event crash leaves only safe unreferenced durable bulk."""

    # Seed the exact predecessor and snapshot its validated projection.
    module = _load()
    opening = _opening()
    journal = module.Journal.open(tmp_path, opening, opened_at="2026-08-27T08:09:10Z")
    _seed_artifact_event(journal, event_type)
    before = journal.project()
    original = module._atomic_publish

    def interrupt_event(path: Path, content: bytes) -> None:
        """Crash only when the event would become authoritative."""

        if path.parent.name == "events":
            raise OSError("simulated event crash")
        original(path, content)

    # Install the crash only at the authoritative event boundary.
    monkeypatch.setattr(module, "_atomic_publish", interrupt_event)

    # Publish required artifact bytes before interrupting their referring event.
    with pytest.raises(OSError, match="simulated event crash"):
        _record_event(journal, event_type, ticket="#184")

    # Reopen the same branch slot from the unchanged event prefix.
    reopened = module.Journal.open(tmp_path, opening)

    # Verify both event count and complete projection match the pre-crash state.
    assert reopened.validate()["event_count"] == before["event_count"]
    assert reopened.project() == before


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "crash_stage", ["before-move", "after-move", "during-cleanup"]
)
def test_archive_crashes_resume_to_the_same_compact_archive(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    crash_stage: str,
) -> None:
    """All archive crash windows resume without a second active run."""

    # Complete one parked run ready for an atomic archive move.
    module = _load()
    opening = {**_opening(), "selection": ["#184"]}
    journal = module.Journal.open(tmp_path, opening, opened_at="2026-08-27T08:09:10Z")
    _record_terminal(journal, "parked")
    _complete_terminal(journal, "parked")

    # Interrupt the atomic move or either side of incremental bulk cleanup.
    if crash_stage == "before-move":
        original_replace = module.os.replace

        def interrupt_move(source: Path, destination: Path) -> None:
            """Crash at the one rename that releases the active branch slot."""

            if Path(destination).parent == tmp_path / "archive":
                raise OSError("simulated archive move crash")
            original_replace(source, destination)

        monkeypatch.setattr(module.os, "replace", interrupt_move)
    elif crash_stage == "after-move":
        original_finalize = module.Journal._finalize_archive

        def interrupt_cleanup(self: Any) -> None:
            """Crash after the atomic move and before retired bulk deletion."""

            raise OSError("simulated archive cleanup crash")

        monkeypatch.setattr(module.Journal, "_finalize_archive", interrupt_cleanup)
    else:
        original_unlink = module.Path.unlink
        interrupted = False

        def interrupt_deletion(path: Path, *, missing_ok: bool = False) -> None:
            """Crash after one retired artifact has already been deleted."""

            nonlocal interrupted
            if not interrupted and "artifacts" in path.parts and path.is_file():
                interrupted = True
                original_unlink(path, missing_ok=missing_ok)
                raise OSError("simulated archive deletion crash")
            original_unlink(path, missing_ok=missing_ok)

        monkeypatch.setattr(module.Path, "unlink", interrupt_deletion)

    # Trigger the archive crash after all prerequisites are durable.
    with pytest.raises(OSError, match="simulated archive"):
        journal.archive()

    # Restore the interrupted boundary before reopening the same invocation.
    if crash_stage == "before-move":
        monkeypatch.setattr(module.os, "replace", original_replace)
    elif crash_stage == "after-move":
        monkeypatch.setattr(module.Journal, "_finalize_archive", original_finalize)
    else:
        monkeypatch.setattr(module.Path, "unlink", original_unlink)
    reopened = module.Journal.open(tmp_path, opening)
    projection = reopened.project()
    archive = reopened.archive()

    # Verify recovery completes one archive and preserves its compact receipt.
    assert projection["completed"] is True
    assert projection["tickets"]["#184"]["terminal"] == "parked"
    assert list((tmp_path / "active").iterdir()) == []
    assert not (archive / ".archive-pending").exists()
    assert (archive / "receipt.json").is_file()
    assert (archive / "artifacts" / "patch").is_dir()
    assert not (archive / "artifacts" / "bundle-plan").exists()


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("artifact_kind", "corruption", "message"),
    [
        ("patch", "missing", "retained artifact is missing"),
        ("patch", "changed", "retained artifact identity changed"),
        ("observation-input", "missing", "retained artifact is missing"),
        ("observation-input", "changed", "retained artifact identity changed"),
    ],
)
def test_pending_archive_refuses_missing_or_changed_retained_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    artifact_kind: str,
    corruption: str,
    message: str,
) -> None:
    """Pending cleanup trusts retained bytes only after full identity checks."""

    # Leave a parked patch and observation at the pending-cleanup boundary.
    module = _load()
    journal, opening = _leave_pending_archive(
        module, tmp_path, monkeypatch, observation=True
    )
    receipt = json.loads((journal.path / "receipt.json").read_text(encoding="utf-8"))
    reference = next(
        item
        for item in receipt["retained_artifacts"]
        if f"/{artifact_kind}/" in item["path"]
    )
    retained_path = journal.path / reference["path"]

    # Change exactly the retained boundary named by this fixture.
    if corruption == "missing":
        retained_path.unlink()
    else:
        retained_path.write_bytes(b"changed retained bytes")

    # Reopening refuses before pending cleanup can delete any retired bulk.
    with pytest.raises(module.JournalRefusal, match=message):
        module.Journal.open(tmp_path, opening)


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "mutation",
    [
        "terminal",
        "continuation",
        "route-audit",
        "bundle-audit",
        "event-count",
        "final-event",
        "retained-top-level",
        "retained-nested",
        "remove-both-r2-references",
    ],
)
def test_pending_archive_authenticates_every_compact_receipt_fact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
) -> None:
    """Pending cleanup accepts only the exact receipt published before its move."""

    # Leave a completed parked run at the authenticated archive boundary.
    module = _load()
    journal, opening = _leave_pending_archive(module, tmp_path, monkeypatch)
    receipt_path = journal.path / "receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    patch_reference = receipt["tickets"]["#184"]["retained_patch"]
    patch_path = journal.path / patch_reference["path"]

    # Mutate one audit fact without changing the pending authenticator.
    if mutation == "terminal":
        receipt["tickets"]["#184"]["terminal"] = "landed"
    elif mutation == "continuation":
        receipt["tickets"]["#184"]["continuation"] = "fresh-context"
    elif mutation == "route-audit":
        receipt["tickets"]["#184"]["route_decisions"][0]["attempt"] = 2
    elif mutation == "bundle-audit":
        receipt["tickets"]["#184"]["bundle"]["bundle_fingerprint"] = (
            f"sha256:{'9' * 64}"
        )
    elif mutation == "event-count":
        receipt["event_count"] += 1
    elif mutation == "final-event":
        receipt["final_event_sha256"] = f"sha256:{'9' * 64}"
    elif mutation == "retained-top-level":
        receipt["retained_artifacts"] = []
    elif mutation == "retained-nested":
        receipt["tickets"]["#184"]["retained_patch"] = None
    else:
        receipt["retained_artifacts"] = []
        receipt["tickets"]["#184"]["retained_patch"] = None
    receipt_path.write_bytes(module.canonical_json(receipt))

    # Authentication refuses before altered references can authorize deletion.
    with pytest.raises(module.JournalRefusal, match="pending marker"):
        module.Journal.open(tmp_path, opening)
    assert patch_path.is_file()


def test_new_terminal_round_invalidates_older_completion_receipts(
    tmp_path: Path,
) -> None:
    """Tracker, retirement, and cleanup must follow the latest terminal event."""

    # Complete every prerequisite for one initial landed terminal round.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_terminal(journal, "landed")
    _record_tracker_transition(journal, "T-LAND", None, ["thomas"])
    _record_event(journal, "bundle-retired", ticket="#184")
    _record_event(journal, "resource-cleaned", ticket="#184")
    landing = journal.project()["tickets"]["#184"]["receipts"]["landing-started"][-1]

    # A newer terminal receipt starts a fresh completion tail even when its
    # terminal kind matches the prior round.
    _record_event(
        journal,
        "landed",
        ticket="#184",
        payload={"landing_sequence": landing["sequence"]},
    )

    # Verify the new terminal invalidates all older completion receipts.
    assert (
        journal.project()["tickets"]["#184"]["recovery_action"]
        == "complete-tracker-transition"
    )
    with pytest.raises(module.JournalRefusal, match="precedes cleanup"):
        _record_event(
            journal,
            "run-completed",
            payload={"tickets": {"#184": "landed"}},
        )


def test_owner_answer_resumes_its_exact_human_conflict(
    tmp_path: Path,
) -> None:
    """An owner answer resumes the exact landing conflict it references."""

    # Reach a human-conflict boundary without duplicating the REBUILD contract.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    review = _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"verdict": "APPROVE"},
    )
    _record_event(
        journal,
        "landing-started",
        ticket="#184",
        payload={"review_sequence": review["sequence"]},
    )
    conflict = _record_event(journal, "human-conflict", ticket="#184")
    _record_event(
        journal,
        "owner-answered",
        ticket="#184",
        payload={"for_sequence": conflict["sequence"]},
    )

    # Recovery follows the referenced conflict instead of the answer name.
    assert (
        journal.project()["tickets"]["#184"]["recovery_action"]
        == "resume-human-conflict"
    )


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "source_fingerprints",
    [
        {
            "child_fingerprint": f"sha256:{'3' * 64}",
            "parent_fingerprint": f"sha256:{'4' * 64}",
        },
        {
            "child_fingerprint": f"sha256:{'7' * 64}",
            "parent_fingerprint": f"sha256:{'4' * 64}",
        },
    ],
)
def test_rebuild_waits_through_release_for_new_verified_bundle(
    tmp_path: Path, source_fingerprints: dict[str, str]
) -> None:
    """Source identity comparisons remain outside journal recovery policy."""

    # Stop once at REBUILD so the intermediate recovery action is observable.
    module = _load()
    opening = {**_opening(), "selection": ["#184"]}
    journal = module.Journal.open(tmp_path, opening, opened_at="2026-08-27T08:09:10Z")
    _record_rebuild_boundary(journal, should_release_bundle=False)
    after_rebuild = journal.project()["tickets"]["#184"]["recovery_action"]

    # Releasing the old escrow leaves the durable recompile handoff unchanged.
    _record_event(journal, "bundle-released", ticket="#184")
    reopened = module.Journal.open(tmp_path, opening)
    after_release = reopened.project()["tickets"]["#184"]["recovery_action"]

    # A later consumption changes the head and bundle fingerprint.
    _record_event(
        reopened,
        "bundle-consumed",
        ticket="#184",
        payload=_recompiled_bundle_payload(source_fingerprints),
    )
    after_consumption = reopened.project()["tickets"]["#184"]["recovery_action"]
    consumed_receipts = reopened.project()["tickets"]["#184"]["receipts"][
        "bundle-consumed"
    ]

    # Compare recovery and confirm both source fingerprints remain durable.
    assert [after_rebuild, after_release, after_consumption] == [
        "await-recompile",
        "await-recompile",
        "continue-ticket",
    ]
    assert consumed_receipts[-1]["payload"]["source_fingerprints"] == (
        source_fingerprints
    )


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("case", "message"),
    [
        ("old-bundle", "old fingerprint"),
        ("wrong-head", "different head"),
        ("missing-release", "post-rebuild release"),
    ],
)
def test_post_rebuild_bundle_consumption_refuses_unverified_recompilation(
    tmp_path: Path, case: str, message: str
) -> None:
    """REBUILD advances only on a released and freshly identified compilation."""

    # Record the exact REBUILD boundary shared by every refusal.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_rebuild_boundary(journal, should_release_bundle=case != "missing-release")
    payload = _recompiled_bundle_payload()

    # Keep one invalid bundle identity or omit the required release boundary.
    if case == "old-bundle":
        payload["bundle_fingerprint"] = f"sha256:{'2' * 64}"
    elif case == "wrong-head":
        payload["execution_base"] = "9" * 40

    # The failed consumption cannot supersede await-recompile durably.
    with pytest.raises(module.JournalRefusal, match=message):
        _record_event(
            journal,
            "bundle-consumed",
            ticket="#184",
            payload=payload,
        )
    assert journal.project()["tickets"]["#184"]["recovery_action"] == "await-recompile"


def test_duplicate_initial_bundle_consumption_is_refused(tmp_path: Path) -> None:
    """One ticket cannot consume twice before a durable REBUILD."""

    # Record the ticket's selection and its one permitted initial consumption.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_event(journal, "selection-recorded")
    _record_event(journal, "bundle-consumed", ticket="#184")
    event_count = journal.validate()["event_count"]

    # Refuse a duplicate even when it repeats the complete initial identity.
    with pytest.raises(module.JournalRefusal, match="requires a newer rebuild"):
        _record_event(journal, "bundle-consumed", ticket="#184")
    assert journal.validate()["event_count"] == event_count


def test_second_consumption_after_rebuild_replacement_is_refused(
    tmp_path: Path,
) -> None:
    """The single REBUILD boundary authorizes exactly one replacement bundle."""

    # Consume the initial bundle and one valid post-release replacement.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_rebuild_boundary(journal, should_release_bundle=True)
    _record_event(
        journal,
        "bundle-consumed",
        ticket="#184",
        payload=_recompiled_bundle_payload(),
    )
    event_count = journal.validate()["event_count"]

    # Refuse another new identity regardless of its otherwise valid schema.
    payload = _recompiled_bundle_payload()
    payload["bundle_fingerprint"] = f"sha256:{'9' * 64}"
    with pytest.raises(module.JournalRefusal, match="already consumed"):
        _record_event(
            journal,
            "bundle-consumed",
            ticket="#184",
            payload=payload,
        )
    assert journal.validate()["event_count"] == event_count


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("rehydrated", "expected_mode", "rehydration_count"),
    [
        (False, "live-context", 0),
        (True, "fresh-context", 1),
    ],
)
def test_revision_context_mode_survives_reopen_and_archive(
    tmp_path: Path,
    rehydrated: bool,
    expected_mode: str,
    rehydration_count: int,
) -> None:
    """R3 remains a reportable fact without relying on session continuity."""

    # Record one revision that begins with a live executor context.
    module = _load()
    opening = {**_opening(), "selection": ["#184"]}
    journal = module.Journal.open(tmp_path, opening, opened_at="2026-08-27T08:09:10Z")
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"verdict": "REVISE"},
    )
    _record_event(journal, "revise-requested", ticket="#184")

    # Only a lost executor context emits the explicit R3 durability boundary.
    if rehydrated:
        _record_event(journal, "executor-rehydrated", ticket="#184")
        journal = module.Journal.open(tmp_path, opening)
        immediate = journal.project()["tickets"]["#184"]
        assert immediate["continuation"] == "fresh-context"
        assert immediate["recovery_action"] == "resume-revision"

    # Later terminal facts preserve the projected continuation mode.
    _record_event(journal, "stranded", ticket="#184")
    _complete_terminal(journal, "stranded")
    reopened = module.Journal.open(tmp_path, opening)

    # Reopening projects the durable continuation mode without session memory.
    assert reopened.project()["tickets"]["#184"]["continuation"] == expected_mode

    # The compact receipt preserves both the summary and exact R3 receipts.
    archive = reopened.archive()
    receipt = json.loads((archive / "receipt.json").read_text(encoding="utf-8"))

    # Final reporting can distinguish the mode and inspect exact R3 receipts.
    assert receipt["tickets"]["#184"]["continuation"] == expected_mode
    assert len(receipt["tickets"]["#184"]["rehydrations"]) == rehydration_count


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("case", "message"),
    [
        ("revision-sequence", "sequence does not name prior revise-requested"),
        ("route-sequence", "sequence does not name prior route-recorded"),
        ("attempt", "rehydration names a different revision attempt"),
    ],
)
def test_r3_rehydration_refuses_mismatched_durable_identity(
    tmp_path: Path, case: str, message: str
) -> None:
    """R3 cannot borrow a revision, Route point, or attempt identity."""

    # Record one exact Route-to-revision chain eligible for fresh rehydration.
    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    review = _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"verdict": "REVISE"},
    )
    revision = _record_event(journal, "revise-requested", ticket="#184")
    payload: dict[str, Any] = {}

    # Break only the durable identity named by this refusal case.
    if case == "revision-sequence":
        payload["revision_sequence"] = review["sequence"]
    elif case == "route-sequence":
        payload["route_sequence"] = review["sequence"]
    else:
        payload = {"attempt": 3, "revision_sequence": revision["sequence"]}

    # No invalid R3 fact may become part of the projection or later archive.
    with pytest.raises(module.JournalRefusal, match=message):
        _record_event(
            journal,
            "executor-rehydrated",
            ticket="#184",
            payload=payload,
        )
    assert journal.project()["tickets"]["#184"]["continuation"] == "live-context"
