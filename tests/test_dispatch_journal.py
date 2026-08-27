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

    journal.record(
        "selection-recorded", payload={"tickets": journal.metadata["selection"]}
    )
    journal.record(
        "bundle-consumed",
        ticket=ticket,
        payload={"bundle_fingerprint": f"sha256:{'2' * 64}", "base": "1" * 40},
    )
    journal.record(
        "route-recorded",
        ticket=ticket,
        payload={"attempt": 1, "decision": "selected"},
        artifacts={"route-response": b'{"decision":"selected"}\n'},
    )
    journal.record("ticket-assigned", ticket=ticket, payload={"assignee": "thomas"})
    journal.record(
        "attempt-started", ticket=ticket, payload={"attempt": 1, "base": "1" * 40}
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
    journal.record(
        "selection-recorded",
        payload={"tickets": ["#184", "#185"]},
        recorded_at="2026-08-27T08:10:00Z",
    )
    journal.record(
        "ticket-assigned",
        ticket="#184",
        payload={"assignee": "thomas"},
        recorded_at="2026-08-27T08:11:00Z",
    )

    events = sorted((journal.path / "events").iterdir())
    first_bytes = events[0].read_bytes()
    second = json.loads(events[1].read_text(encoding="utf-8"))

    assert [path.name for path in events] == ["00000001.json", "00000002.json"]
    assert first_bytes == module.canonical_json(json.loads(first_bytes))
    assert second["previous_sha256"] == f"sha256:{module.sha256_hex(first_bytes)}"
    assert journal.validate()["event_count"] == 2


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
    original = module._atomic_publish

    def interrupt_event(path: Path, content: bytes) -> None:
        """Crash only at the event boundary after artifact publication."""

        if path.parent.name == "events":
            raise OSError("simulated event crash")
        original(path, content)

    monkeypatch.setattr(module, "_atomic_publish", interrupt_event)

    with pytest.raises(OSError, match="simulated event crash"):
        journal.record(
            "patch-captured",
            ticket="#184",
            payload={"attempt": 1, "changed_paths": ["journal.py"]},
            artifacts={"patch": b"diff --git a/a b/a\n"},
        )

    artifacts = list((journal.path / "artifacts" / "patch").iterdir())
    assert len(artifacts) == 1
    assert artifacts[0].read_bytes() == b"diff --git a/a b/a\n"
    assert list((journal.path / "events").iterdir()) == []


def test_event_publication_never_exposes_partial_or_temporary_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A rename-window crash leaves the authoritative sequence untouched."""

    module = _load()
    journal = _open(module, tmp_path)
    original = module.os.replace

    def interrupt_rename(source: Path, destination: Path) -> None:
        """Crash after the temporary file flush but before publication."""

        if Path(destination).parent.name == "events":
            raise OSError("simulated rename crash")
        original(source, destination)

    monkeypatch.setattr(module.os, "replace", interrupt_rename)

    with pytest.raises(OSError, match="simulated rename crash"):
        journal.record("ticket-assigned", ticket="#184", payload={"assignee": "thomas"})

    assert list((journal.path / "events").iterdir()) == []
    assert journal.validate()["event_count"] == 0


def test_artifact_references_carry_digest_length_and_relative_path(
    tmp_path: Path,
) -> None:
    """Every event can validate the exact durable bytes it names."""

    module = _load()
    journal = _open(module, tmp_path)
    event = journal.record(
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
    assert journal.validate()["artifact_count"] == 1


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("last_event", "expected_action"),
    [
        ("attempt-started", "replay-attempt"),
        ("patch-captured", "review-patch"),
        ("revise-requested", "resume-revision"),
        ("landing-started", "reconcile-landing"),
        ("rebuild-requested", "await-recompile"),
        ("human-conflict", "resume-human-conflict"),
        ("landed", "complete-tracker-transition"),
        ("parked", "complete-tracker-transition"),
        ("tracker-transition-completed", "retire-and-clean"),
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
    if last_event != "attempt-started":
        journal.record(
            "patch-captured",
            ticket="#184",
            payload={
                "attempt": 1,
                "changed_paths": ["skills/code/dispatch/scripts/journal.py"],
            },
            artifacts={"patch": b"diff"},
        )
    if last_event == "revise-requested":
        journal.record(
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "REVISE"},
        )
        journal.record(
            "revise-requested",
            ticket="#184",
            payload={"attempt": 2, "finding": "exact correction"},
        )
    elif last_event == "landing-started":
        journal.record(
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "APPROVE"},
        )
        journal.record(
            "landing-started",
            ticket="#184",
            payload={"candidate": "3" * 40, "previous_head": "1" * 40},
        )
    elif last_event == "rebuild-requested":
        journal.record(
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "REBUILD"},
        )
        journal.record("rebuild-requested", ticket="#184", payload={"head": "4" * 40})
    elif last_event == "human-conflict":
        journal.record(
            "human-conflict",
            ticket="#184",
            payload={
                "branch": "kntnt-dispatch/run/184/1",
                "worktree": "worktrees/run/184/1",
            },
        )
    elif last_event in {"landed", "tracker-transition-completed"}:
        journal.record(
            "review-completed",
            ticket="#184",
            payload={"attempt": 1, "verdict": "APPROVE"},
        )
        journal.record(
            "landing-started",
            ticket="#184",
            payload={"candidate": "3" * 40, "previous_head": "1" * 40},
        )
        journal.record(
            "landed", ticket="#184", payload={"commit": "3" * 40, "tree": "4" * 40}
        )
    elif last_event == "parked":
        journal.record(
            "parked",
            ticket="#184",
            payload={"class": "owner-info", "question": "Which outcome should win?"},
        )
    elif last_event == "stranded":
        journal.record("stranded", ticket="#184", payload={"reason": "route refused"})

    # A completed tracker transition is the durable gate before retirement.
    if last_event == "tracker-transition-completed":
        resolution = _transition_resolution(None, ["thomas"])
        planned = journal.record(
            "tracker-transition-planned",
            ticket="#184",
            payload={
                "transition_id": "T-LAND",
                "resolution": resolution,
                "pre_projection": _pre_projection(),
            },
        )
        journal.record(
            "tracker-transition-completed",
            ticket="#184",
            payload={
                "transition_id": "T-LAND",
                "planned_sequence": planned["sequence"],
                "resolution": resolution,
                "observed_post_projection": {
                    "labels": ["scope:rework", "priority:high"],
                    "milestone": "Skills Next",
                    "status": "open",
                    "assignees": ["thomas"],
                },
            },
        )

    assert journal.project()["tickets"]["#184"]["recovery_action"] == expected_action


def test_tracker_completion_repeats_and_verifies_the_portable_resolution(
    tmp_path: Path,
) -> None:
    """Changed conventions cannot alter a transition already made durable."""

    module = _load()
    journal = _open(module, tmp_path)
    journal.record(
        "parked",
        ticket="#184",
        payload={"class": "owner-info", "question": "Which outcome should win?"},
    )
    resolution = _transition_resolution("needs-owner", [])
    planned = journal.record(
        "tracker-transition-planned",
        ticket="#184",
        payload={
            "transition_id": "T-PARK-INFO",
            "resolution": resolution,
            "pre_projection": _pre_projection(),
        },
    )
    completed = journal.record(
        "tracker-transition-completed",
        ticket="#184",
        payload={
            "transition_id": "T-PARK-INFO",
            "planned_sequence": planned["sequence"],
            "resolution": resolution,
            "observed_post_projection": {
                "labels": ["scope:rework", "priority:high", "needs-owner"],
                "milestone": "Skills Next",
                "status": "open",
                "assignees": [],
            },
        },
    )

    assert completed["payload"]["resolution"]["target_label"] == "needs-owner"
    assert journal.validate()["event_count"] == 3

    with pytest.raises(module.JournalRefusal, match="observed tracker projection"):
        journal.record(
            "tracker-transition-completed",
            ticket="#184",
            payload={
                "transition_id": "T-PARK-INFO",
                "planned_sequence": planned["sequence"],
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
    journal.record(
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
    journal.record(
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1},
        artifacts={"patch": b"diff"},
    )
    journal.record(
        "review-completed", ticket="#184", payload={"attempt": 1, "verdict": "APPROVE"}
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
    journal.record(
        "landing-started",
        ticket="#184",
        payload={
            "candidate": "3" * 40,
            "previous_head": "1" * 40,
            "required_evidence": {"integration_ref_head": "1" * 40},
        },
    )

    assert journal.project(evidence={"integration_ref_head": "1" * 40})
    with pytest.raises(module.JournalRefusal, match="contradictory external evidence"):
        journal.project(evidence={"integration_ref_head": "9" * 40})


def test_completion_archives_atomically_and_retains_a_parked_patch(
    tmp_path: Path,
) -> None:
    """The active slot becomes one compact archive without losing paid work."""

    module = _load()
    journal = _open(module, tmp_path, selection=["#184"])
    journal.record(
        "patch-captured",
        ticket="#184",
        payload={"attempt": 1},
        artifacts={"patch": b"valuable patch"},
    )
    journal.record(
        "parked",
        ticket="#184",
        payload={"class": "owner-info", "question": "Choose A or B?"},
    )
    resolution = _transition_resolution("needs-owner", [])
    planned = journal.record(
        "tracker-transition-planned",
        ticket="#184",
        payload={
            "transition_id": "T-PARK-INFO",
            "resolution": resolution,
            "pre_projection": _pre_projection(),
        },
    )
    journal.record(
        "tracker-transition-completed",
        ticket="#184",
        payload={
            "transition_id": "T-PARK-INFO",
            "planned_sequence": planned["sequence"],
            "resolution": resolution,
            "observed_post_projection": {
                "labels": ["scope:rework", "priority:high", "needs-owner"],
                "milestone": "Skills Next",
                "status": "open",
                "assignees": [],
            },
        },
    )
    journal.record(
        "bundle-retired", ticket="#184", payload={"fingerprint": f"sha256:{'2' * 64}"}
    )
    journal.record("resource-cleaned", ticket="#184", payload={"resources": []})
    journal.record("run-completed", payload={"tickets": {"#184": "parked"}})

    archive = journal.archive()
    receipt = json.loads((archive / "receipt.json").read_text(encoding="utf-8"))

    assert not journal.path.exists()
    assert archive.parent == tmp_path / "archive"
    assert receipt["run_fingerprint"] == module.run_fingerprint(
        {**_opening(), "selection": ["#184"]}
    )
    assert receipt["tickets"]["#184"]["terminal"] == "parked"
    assert (archive / "artifacts" / "patch").is_dir()


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
