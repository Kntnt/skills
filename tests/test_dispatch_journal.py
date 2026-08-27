"""Transactional persistence for disposable dispatch execution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest  # type: ignore[import-not-found]  # CI's mypy command omits pytest.

REPO_ROOT = Path(__file__).resolve().parent.parent
JOURNAL_PATH = REPO_ROOT / "skills" / "code" / "dispatch" / "scripts" / "journal.py"
CONTRIBUTING_PATH = REPO_ROOT / "CONTRIBUTING.md"
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def _load() -> ModuleType:
    """Load the shipped journal helper from its installed location."""

    spec = importlib.util.spec_from_file_location("dispatch_journal", JOURNAL_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _opening(
    ref: str = "refs/heads/rework", invocation: str = "/dispatch #184"
) -> dict[str, Any]:
    """Return one complete set of immutable run-opening inputs."""

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

    opening = _opening()
    opening.update(changes)
    return module.Journal.open(root, opening, opened_at="2026-08-27T08:09:10Z")


def _record_attempt(journal: Any, ticket: str = "#184") -> None:
    """Record the durable prefix shared by executor crash fixtures."""

    _record_event(
        journal,
        "selection-recorded",
        payload={"tickets": journal.metadata["selection"]},
    )
    _record_event(
        journal,
        "bundle-consumed",
        ticket=ticket,
        payload={"bundle_fingerprint": f"sha256:{'2' * 64}", "base": "1" * 40},
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


def _transition_resolution(
    target_label: str | None, assignees: list[str]
) -> dict[str, Any]:
    """Return a portable transition receipt resolved outside the helper."""

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

    return {
        "labels": ["custom-ready", "scope:rework", "priority:high"],
        "milestone": "Skills Next",
        "status": "open",
        "assignees": ["thomas"],
    }


def _record_event(
    journal: Any,
    event_type: str,
    *,
    ticket: str | None = None,
    payload: dict[str, Any] | None = None,
    artifacts: dict[str, bytes] | None = None,
    recorded_at: str | None = None,
    omit_payload_field: str | None = None,
    omit_artifact: str | None = None,
) -> dict[str, Any]:
    """Record one schema-complete event while tests vary only relevant fields."""

    # Supply the recovery-complete receipt for every event vocabulary member.
    payload_defaults: dict[str, dict[str, Any]] = {
        "selection-recorded": {"tickets": journal.metadata["selection"]},
        "bundle-consumed": {
            "bundle_fingerprint": f"sha256:{'2' * 64}",
            "execution_base": "1" * 40,
            "source_fingerprints": {
                "child": f"sha256:{'3' * 64}",
                "parent": f"sha256:{'4' * 64}",
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

    # Supply the durable bytes required to recover each artifact boundary.
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

    # Translate first-generation fixture aliases before applying exact overrides.
    overrides = dict(payload or {})
    if event_type == "bundle-consumed" and "base" in overrides:
        overrides["execution_base"] = overrides.pop("base")
    if event_type == "parked":
        if "class" in overrides:
            overrides["park_class"] = overrides.pop("class")
        if "question" in overrides:
            overrides["message"] = overrides.pop("question")
    if event_type == "bundle-retired" and "fingerprint" in overrides:
        overrides["bundle_fingerprint"] = overrides.pop("fingerprint")
    if event_type == "revise-requested" and "finding" in overrides:
        overrides.pop("finding")
    complete_payload = {**payload_defaults.get(event_type, {}), **overrides}
    complete_artifacts = {**artifact_defaults.get(event_type, {}), **(artifacts or {})}

    # Cleanup fixtures acknowledge every disposable attempt resource already
    # named by the durable projection.
    if event_type == "resource-cleaned" and "resources" not in overrides:
        receipts = journal.project()["tickets"][ticket]["receipts"]
        complete_payload["resources"] = [
            entry["payload"][field]
            for entry in receipts.get("attempt-started", [])
            for field in ("worktree", "branch")
        ]
    if omit_payload_field is not None:
        complete_payload.pop(omit_payload_field, None)
    if omit_artifact is not None:
        complete_artifacts.pop(omit_artifact, None)

    # Sequence defaults bind dependent fixtures to the latest durable boundary.
    if ticket is not None:
        receipts = journal.project()["tickets"][ticket]["receipts"]

        def latest_sequence(kind: str) -> int | None:
            """Return the newest fixture receipt sequence for one event kind."""

            entries = receipts.get(kind, [])
            return entries[-1]["sequence"] if entries else None

        sequence_fields = {
            "revise-requested": ("review_sequence", "review-completed"),
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

    return dict(
        journal.record(
            event_type,
            ticket=ticket,
            payload=complete_payload,
            artifacts=complete_artifacts,
            recorded_at=recorded_at,
        )
    )


def _record_tracker_transition(
    journal: Any,
    transition_id: str,
    target_label: str | None,
    assignees: list[str],
) -> dict[str, Any]:
    """Record one complete portable transition plan and verified completion."""

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

    _record_attempt(journal)
    if terminal == "stranded":
        _record_event(journal, "stranded", ticket="#184")
        return

    _record_event(journal, "patch-captured", ticket="#184")
    if terminal == "parked":
        _record_event(journal, "parked", ticket="#184")
        return

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


def _complete_terminal(journal: Any, terminal: str) -> None:
    """Advance one terminal ticket through every archive prerequisite."""

    if terminal == "landed":
        _record_tracker_transition(journal, "T-LAND", None, ["thomas"])
        _record_event(journal, "bundle-retired", ticket="#184")
    elif terminal == "parked":
        _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])
        _record_event(journal, "bundle-retired", ticket="#184")
    _record_event(journal, "resource-cleaned", ticket="#184")
    _record_event(journal, "run-completed", payload={"tickets": {"#184": terminal}})


def _seed_artifact_event(journal: Any, event_type: str) -> None:
    """Record the exact predecessor prefix for one artifact crash fixture."""

    if event_type in {"bundle-consumed", "route-recorded"}:
        _record_event(journal, "selection-recorded")
    if event_type == "bundle-consumed":
        return
    if event_type == "route-recorded":
        _record_event(journal, "bundle-consumed", ticket="#184")
        return

    _record_attempt(journal)
    if event_type in {"review-completed", "observation-recorded"}:
        _record_event(journal, "patch-captured", ticket="#184")
    if event_type == "observation-recorded":
        _record_event(journal, "review-completed", ticket="#184")


def test_branch_slots_are_independent_and_one_invocation_owns_each(
    tmp_path: Path,
) -> None:
    """The full ref serializes one branch without blocking another branch."""

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

    assert resumed.path == first.path
    assert other.path != first.path
    assert first.path.name == module.sha256_hex(b"refs/heads/rework")

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

    module = _load()
    journal = _open(module, tmp_path)
    metadata = json.loads((journal.path / "metadata.json").read_text(encoding="utf-8"))

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

    events = sorted((journal.path / "events").iterdir())
    first_bytes = events[0].read_bytes()
    second = json.loads(events[1].read_text(encoding="utf-8"))

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

    module = _load()
    value = {"\ue000": 1, "\U00010000": 2, "line": "one\ntwo", "truth": True}

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

    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    original = module._atomic_publish

    def interrupt_event(path: Path, content: bytes) -> None:
        """Crash only at the event boundary after artifact publication."""

        if path.parent.name == "events":
            raise OSError("simulated event crash")
        original(path, content)

    monkeypatch.setattr(module, "_atomic_publish", interrupt_event)

    with pytest.raises(OSError, match="simulated event crash"):
        _record_event(
            journal,
            "patch-captured",
            ticket="#184",
            payload={"attempt": 1, "changed_paths": ["journal.py"]},
            artifacts={"patch": b"diff --git a/a b/a\n"},
        )

    artifacts = list((journal.path / "artifacts" / "patch").iterdir())
    assert len(artifacts) == 1
    assert artifacts[0].read_bytes() == b"diff --git a/a b/a\n"
    assert journal.validate()["event_count"] == 5


def test_event_publication_never_exposes_partial_or_temporary_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A rename-window crash leaves the authoritative sequence untouched."""

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

    monkeypatch.setattr(module.os, "replace", interrupt_rename)

    with pytest.raises(OSError, match="simulated rename crash"):
        _record_event(
            journal, "ticket-assigned", ticket="#184", payload={"assignee": "thomas"}
        )

    assert journal.validate()["event_count"] == 3


def test_artifact_references_carry_digest_length_and_relative_path(
    tmp_path: Path,
) -> None:
    """Every event can validate the exact durable bytes it names."""

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
        ("stranded", "clean-stranded"),
    ],
)
def test_projection_distinguishes_each_recovery_window(
    tmp_path: Path, last_event: str, expected_action: str
) -> None:
    """Resume derives one safe next action from the immutable prefix."""

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
            payload={"attempt": 2, "finding": "exact correction"},
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
            payload={"class": "owner-info", "question": "Which outcome should win?"},
        )
    elif last_event == "stranded":
        _record_event(
            journal, "stranded", ticket="#184", payload={"reason": "route refused"}
        )

    # A completed tracker transition is the durable gate before retirement.
    if last_event == "tracker-transition-completed":
        _record_tracker_transition(journal, "T-LAND", None, ["thomas"])

    assert journal.project()["tickets"]["#184"]["recovery_action"] == expected_action


def test_tracker_completion_repeats_and_verifies_the_portable_resolution(
    tmp_path: Path,
) -> None:
    """Changed conventions cannot alter a transition already made durable."""

    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)
    _record_event(
        journal,
        "parked",
        ticket="#184",
        payload={"class": "owner-info", "question": "Which outcome should win?"},
    )
    completed = _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])

    assert completed["payload"]["resolution"]["target_label"] == "needs-owner"
    assert journal.validate()["event_count"] == 8

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


def test_projection_is_idempotent_and_preserves_every_ticket_receipt(
    tmp_path: Path,
) -> None:
    """A complete in-memory account is derived without a mutable state file."""

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

    first = journal.project()
    second = journal.project()
    after = sorted(path.relative_to(journal.path) for path in journal.path.rglob("*"))

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

    with pytest.raises(module.JournalRefusal):
        journal.validate()


def test_projection_refuses_contradictory_external_evidence(tmp_path: Path) -> None:
    """The caller may bind observed Git facts without giving Git to the helper."""

    module = _load()
    journal = _open(module, tmp_path)
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
    _record_event(
        journal,
        "landing-started",
        ticket="#184",
        payload={
            "review_sequence": review["sequence"],
            "candidate": "3" * 40,
            "previous_head": "1" * 40,
        },
    )

    evidence: dict[str, Any] = {
        "integration_ref_head": "1" * 40,
        "candidate_commit": None,
        "candidate_reachable": False,
        "candidate_tree": None,
        "test_blobs": {},
    }

    assert journal.project(git_evidence=evidence)
    with pytest.raises(module.JournalRefusal, match="contradictory Git evidence"):
        journal.project(git_evidence={**evidence, "integration_ref_head": "9" * 40})


def test_completion_archives_atomically_and_retains_a_parked_patch(
    tmp_path: Path,
) -> None:
    """The active slot becomes one compact archive without losing paid work."""

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
        payload={"class": "owner-info", "question": "Choose A or B?"},
    )
    _record_tracker_transition(journal, "T-PARK-INFO", "needs-owner", [])
    _record_event(
        journal,
        "bundle-retired",
        ticket="#184",
        payload={"fingerprint": f"sha256:{'2' * 64}"},
    )
    _record_event(journal, "resource-cleaned", ticket="#184")
    _record_event(journal, "run-completed", payload={"tickets": {"#184": "parked"}})

    archive = journal.archive()
    receipt = json.loads((archive / "receipt.json").read_text(encoding="utf-8"))

    assert journal.path == archive
    assert list((tmp_path / "active").iterdir()) == []
    assert archive.parent == tmp_path / "archive"
    assert receipt["run_fingerprint"] == module.run_fingerprint(
        {**_opening(), "selection": ["#184"]}
    )
    assert receipt["tickets"]["#184"]["terminal"] == "parked"
    assert receipt["tickets"]["#184"]["bundle"]["source_fingerprints"]
    assert receipt["retained_artifacts"] == [latest_patch["artifacts"]["patch"]["path"]]
    assert not (archive / older_patch["artifacts"]["patch"]["path"]).exists()
    assert (archive / latest_patch["artifacts"]["patch"]["path"]).is_file()
    assert receipt["tickets"]["#184"]["bundle"]["footprint"]
    assert receipt["tickets"]["#184"]["route_decisions"] == [{"status": "selected"}]
    assert receipt["tickets"]["#184"]["retained_patch"]["byte_length"] == 14
    assert (archive / "artifacts" / "patch").is_dir()
    assert not (archive / "artifacts" / "bundle-plan").exists()
    assert not (archive / "artifacts" / "route-response").exists()


def test_archive_refuses_an_incomplete_run(tmp_path: Path) -> None:
    """Moving an active prefix cannot masquerade as terminal completion."""

    module = _load()
    journal = _open(module, tmp_path)
    _record_attempt(journal)

    with pytest.raises(module.JournalRefusal, match="run-completed"):
        journal.archive()


def test_event_vocabulary_covers_dispatch_without_owning_its_decisions() -> None:
    """Persistence names every boundary while policy remains in the Skill."""

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

    module = _load()
    opening_path = tmp_path / "opening.json"
    opening_path.write_text(json.dumps(_opening()), encoding="utf-8")
    arguments = ["--root", str(tmp_path / "journal"), "--opening", str(opening_path)]

    assert module.main(["open", *arguments]) == 0
    opened = json.loads(capfd.readouterr().out)
    assert opened["metadata"]["run_fingerprint"] == module.run_fingerprint(_opening())

    assert module.main(["project", *arguments]) == 0
    projected = json.loads(capfd.readouterr().out)
    assert projected["tickets"]["#184"]["recovery_action"] == "start-ticket"


def test_journal_is_in_both_strict_mypy_gates() -> None:
    """The shipped helper cannot regress outside the documented CI contract."""

    journal_argument = "skills/code/dispatch/scripts/journal.py"

    assert journal_argument in CONTRIBUTING_PATH.read_text(encoding="utf-8")
    assert journal_argument in CI_PATH.read_text(encoding="utf-8")


def test_business_state_uses_one_typed_representation() -> None:
    """Event, transition, terminal, and recovery values are typed once."""

    module = _load()

    assert module.EventType.PATCH_CAPTURED.value == "patch-captured"
    assert module.TransitionId.LAND.value == "T-LAND"
    assert module.TerminalState.PARKED.value == "parked"
    assert module.RecoveryAction.REVIEW_PATCH.value == "review-patch"
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

    module = _load()
    journal = _open(module, tmp_path)
    field = min(module.EVENT_PAYLOAD_FIELDS[module.EventType(event_type)])
    ticket = None if event_type in {"selection-recorded", "run-completed"} else "#184"

    with pytest.raises(module.JournalRefusal, match="payload fields are incomplete"):
        _record_event(
            journal,
            event_type,
            ticket=ticket,
            omit_payload_field=field,
        )

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

    module = _load()
    journal = _open(module, tmp_path)

    with pytest.raises(
        module.JournalRefusal, match="recovery artifacts are incomplete"
    ):
        _record_event(
            journal,
            event_type,
            ticket="#184",
            omit_artifact=artifact,
        )

    assert journal.validate()["event_count"] == 0


def test_newer_attempt_events_supersede_older_revision_state(tmp_path: Path) -> None:
    """A later round, not an old monotone flag, decides recovery."""

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

    assert journal.project()["tickets"]["#184"]["recovery_action"] == "replay-attempt"

    _record_event(
        journal,
        "patch-captured",
        ticket="#184",
        payload={"attempt": 2, "changed_paths": ["journal.py"]},
        artifacts={"patch": b"second patch"},
    )

    assert journal.project()["tickets"]["#184"]["recovery_action"] == "review-patch"


def test_archive_requires_every_terminal_cleanup_boundary(tmp_path: Path) -> None:
    """A terminal label alone cannot erase unfinished recovery work."""

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
    with pytest.raises(module.JournalRefusal, match="cleanup"):
        _record_event(journal, "run-completed", payload={"tickets": {"#184": "landed"}})


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
        ("stranded", "terminal", "clean-stranded"),
        ("stranded", "cleanup", "complete-run"),
    ],
)
def test_each_terminal_cleanup_boundary_reopens_to_one_projection(
    tmp_path: Path, terminal: str, boundary: str, expected_action: str
) -> None:
    """Every terminal crash prefix reopens the same branch slot idempotently."""

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
    if boundary == "cleanup":
        _record_event(journal, "resource-cleaned", ticket="#184")

    reopened = module.Journal.open(tmp_path, opening)

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

    monkeypatch.setattr(module, "_atomic_publish", interrupt_event)

    with pytest.raises(OSError, match="simulated event crash"):
        _record_event(journal, event_type, ticket="#184")

    reopened = module.Journal.open(tmp_path, opening)

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

    assert projection["completed"] is True
    assert projection["tickets"]["#184"]["terminal"] == "parked"
    assert list((tmp_path / "active").iterdir()) == []
    assert not (archive / ".archive-pending").exists()
    assert (archive / "receipt.json").is_file()
    assert (archive / "artifacts" / "patch").is_dir()
    assert not (archive / "artifacts" / "bundle-plan").exists()


def test_new_terminal_round_invalidates_older_completion_receipts(
    tmp_path: Path,
) -> None:
    """Tracker, retirement, and cleanup must follow the latest terminal event."""

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


def test_rebuild_and_owner_answer_sequences_follow_the_newest_boundary(
    tmp_path: Path,
) -> None:
    """Fresh rounds supersede old rebuilds while answers resume their conflict."""

    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    _record_attempt(journal)
    _record_event(journal, "patch-captured", ticket="#184")
    review = _record_event(
        journal,
        "review-completed",
        ticket="#184",
        payload={"verdict": "REBUILD"},
    )
    _record_event(journal, "rebuild-requested", ticket="#184")

    assert journal.project()["tickets"]["#184"]["recovery_action"] == "await-recompile"

    _record_event(journal, "bundle-consumed", ticket="#184")
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
        payload={"attempt": 2, "attempt_id": "#184/2"},
    )

    assert journal.project()["tickets"]["#184"]["recovery_action"] == "replay-attempt"

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

    assert (
        journal.project()["tickets"]["#184"]["recovery_action"]
        == "resume-human-conflict"
    )
