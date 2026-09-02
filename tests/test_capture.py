"""Automatic local run-evidence capture shipped by the model-selector Skill."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
MODEL_SELECTOR: Path = REPO_ROOT / "skills" / "models" / "model-selector"
CAPTURE: Path = MODEL_SELECTOR / "scripts" / "capture.py"


def _load() -> Any:
    """Load the shipped capture module from its installed path."""

    spec = importlib.util.spec_from_file_location("model_selector_capture", CAPTURE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_default_data_uses_the_shared_kntnt_skill_directory() -> None:
    """Keep model-selector's user data under the shared Kntnt root."""

    # Assert the Collection-wide convention at the owning public seam.
    module = _load()
    assert module.default_data() == Path.home() / ".kntnt" / "model-selector"


def _seat() -> dict[str, Any]:
    """Provide the exact main seat an ordinary session runs on."""

    return {
        "model": "worker-v2-2026-05-01",
        "portable_deliberation": "medium",
        "native_deliberation": "think",
        "channel": "subscription-max",
        "surface": "cli",
        "adapter_id": "claude-code",
        "serving_mode": "standard",
    }


def _enabled(module: Any, tmp_path: Path, harness: str = "claude-code") -> Path:
    """Opt in to capture in an isolated data directory and Harness root."""

    data = tmp_path / "data"
    module.enable(data, tmp_path / "home", [harness], _command())
    return data


def _command() -> list[str]:
    """Provide the command a Harness would run for a lifecycle event."""

    return ["uv", "run", str(CAPTURE), "hook"]


def _start(module: Any, data: Path, session: str, harness: str = "claude-code") -> None:
    """Signal that substantive work began in one session."""

    module.hook(
        data,
        "SessionStart",
        {"session_id": session, "harness": harness, "seat": _seat()},
    )


def _finish(module: Any, data: Path, session: str, **payload: Any) -> dict[str, Any]:
    """Signal that one session reached a completion boundary."""

    answered = module.hook(
        data, "SessionEnd", {"session_id": session, "harness": "claude-code", **payload}
    )
    return cast(dict[str, Any], answered)


def _checker(result: str = "pass") -> dict[str, Any]:
    """Provide one objective checker's verdict over a session's work."""

    return {
        "identity": "pytest",
        "independent": True,
        "authority": "objective_checker",
        "result": result,
    }


def _ledger(data: Path) -> list[dict[str, Any]]:
    """Return every observation the evidence ledger holds."""

    path = data / "run-observations.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _drafts(data: Path) -> list[Path]:
    return sorted((data / "capture" / "drafts").glob("*.json"))


def _pending(data: Path) -> list[Path]:
    return sorted((data / "capture" / "pending").glob("*.json"))


def test_enabling_the_skill_alone_captures_nothing(tmp_path: Path) -> None:
    """Capture starts on an explicit opt-in, never on the Skill being Enabled."""

    module = _load()
    data = tmp_path / "data"

    # Drive a whole session's lifecycle without ever opting in.
    _start(module, data, "session-1")
    _finish(module, data, "session-1", checker=_checker())

    assert not (data / "capture").exists() or not _drafts(data)
    assert _ledger(data) == []


def test_the_first_opt_in_states_what_it_installs_and_retains(tmp_path: Path) -> None:
    """Consent names the integration, the retained data, cleanup and the way out."""

    module = _load()
    result = module.enable(
        tmp_path / "data", tmp_path / "home", ["claude-code"], _command()
    )
    consent = result["consent"]

    assert result["enabled"] is True
    for subject in ("integration", "retained", "cleanup", "opt_out"):
        assert consent[subject]
    assert result["harnesses"][0]["status"] == "installed"


def test_an_objectively_graded_run_imports_and_cleans_up(tmp_path: Path) -> None:
    """Lifecycle signals become one normalized import, and the draft goes."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1", checker=_checker(), benchmark="python")

    assert result["imported"]["accepted"], result
    assert result["imported"]["frontiers_rebuilt"] == ["python"]
    assert _drafts(data) == []
    assert _pending(data) == []

    # The permanent record is the normalized observation the ledger accepts.
    observation = _ledger(data)[0]
    assert observation["outcome"] == "pass"
    assert observation["benchmark_key"] == "python"
    assert observation["routed"]["model"] == _seat()["model"]


def test_a_retired_merge_collision_condition_is_not_recorded(tmp_path: Path) -> None:
    """A merge collision belongs to a later repair, not this attempt's outcome."""

    module = _load()
    data = _enabled(module, tmp_path)

    # Finish through the public lifecycle seam with the retired condition.
    _start(module, data, "session-1")
    result = _finish(
        module,
        data,
        "session-1",
        error={"kind": "merge_collision"},
        benchmark="python",
    )

    # Assert the obsolete condition never enters the normalized ledger.
    assert result["imported"]["accepted"]
    observation = _ledger(data)[0]
    assert observation["outcome"] == "infra_error"
    assert observation["non_model_condition"] == "mechanical_hinder"


def test_unchecked_work_waits_for_a_human_rather_than_grading_itself(
    tmp_path: Path,
) -> None:
    """No checker means no outcome: the work waits in bounded pending review."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1")

    assert result["pending"]
    assert _ledger(data) == []
    assert len(_pending(data)) == 1


def test_a_deferred_review_offers_save_failed_and_ignore(tmp_path: Path) -> None:
    """A human's own confirmation is an authority; their ignore discards it."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    pending = _finish(module, data, "session-1")["pending"]

    assert set(module.review_actions()) == {"save", "failed", "ignore"}
    saved = module.review(data, pending, "save")

    assert saved["imported"]["accepted"]
    assert _ledger(data)[0]["outcome"] == "pass"
    assert _ledger(data)[0]["outcome_authority"] == "user_confirmation"
    assert _pending(data) == []

    # A second session ignored is discarded rather than graded either way.
    _start(module, data, "session-2")
    ignored = _finish(module, data, "session-2")["pending"]
    module.review(data, ignored, "ignore")

    assert len(_ledger(data)) == 1
    assert _pending(data) == []


def test_a_harness_error_is_not_a_model_failure(tmp_path: Path) -> None:
    """Infrastructure keeps its own outcome and never lowers measured quality."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    _finish(module, data, "session-1", error={"kind": "mechanical_hinder"})

    observation = _ledger(data)[0]
    assert observation["outcome"] == "infra_error"
    assert observation["non_model_condition"] == "mechanical_hinder"

    # The frontier counts it beside the judged runs rather than inside them.
    frontier = json.loads((data / "derived-frontiers.json").read_text(encoding="utf-8"))
    point = next(iter(frontier["frontiers"].values()))["points"][0]
    assert point["runs"] == 0
    assert point["quality_lower_bound"] is None
    assert point["excluded"]["infra_error"] == 1


def test_model_self_confidence_never_grades_a_run(tmp_path: Path) -> None:
    """A self-report is refused rather than downgraded into weaker evidence."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    result = _finish(
        module,
        data,
        "session-1",
        checker={
            "identity": "the agent itself",
            "independent": False,
            "authority": "self_report",
            "result": "pass",
        },
    )

    assert _ledger(data) == []
    assert result["refusals"][0]["code"] in {
        "self_reported_outcome",
        "unchecked_outcome",
    }


def test_simultaneous_sessions_keep_separate_drafts(tmp_path: Path) -> None:
    """Two sessions at once are two drafts and two identities, never one."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    _start(module, data, "session-2")

    assert len(_drafts(data)) == 2

    _finish(module, data, "session-1", checker=_checker(), benchmark="python")
    _finish(module, data, "session-2", checker=_checker(), benchmark="python")
    keys = {observation["run_key"] for observation in _ledger(data)}

    assert len(keys) == 2
    assert _drafts(data) == []


def test_an_identical_observation_is_skipped_and_a_conflict_changes_nothing(
    tmp_path: Path,
) -> None:
    """The ledger's duplicate and conflict rules survive automatic import."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1", checker=_checker(), benchmark="python")
    before = _ledger(data)

    # The very same observation offered again adds nothing. An import that was
    # interrupted after writing and runs again is exactly this case.
    _start(module, data, "session-2")
    identity = _finish(module, data, "session-2")["pending"]
    record = (data / "capture" / "pending" / f"{identity}.json").read_bytes()
    module.review(data, identity, "save")
    held = _ledger(data)
    (data / "capture" / "pending" / f"{identity}.json").write_bytes(record)
    again = module.review(data, identity, "save")

    assert again["imported"]["skipped"]
    assert _ledger(data) == held

    # The same identity carrying a different result overwrites neither side.
    _start(module, data, "session-1")
    conflict = _finish(
        module, data, "session-1", checker=_checker("fail"), benchmark="python"
    )

    assert conflict["imported"]["rejected"][0]["code"] == "conflicting_identity"
    assert _ledger(data) == held
    assert before[0] in held


def test_unavailable_measurements_stay_null(tmp_path: Path) -> None:
    """An absence is never read as a zero."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1", checker=_checker())
    observation = _ledger(data)[0]

    assert observation["cost"]["cash"] is None
    assert observation["latency"]["first_useful_output_seconds"] is None
    assert observation["tokens"]["input"] is None
    assert observation["quota"]["charged"] is None


def test_abrupt_termination_is_reconciled_at_the_next_start(tmp_path: Path) -> None:
    """A draft with no end signal is not lost and is not a success either."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")

    # The Harness dies: no end hook ever runs for that session.
    stale = _drafts(data)[0]
    aged = datetime.now(UTC) - timedelta(hours=48)
    draft = json.loads(stale.read_text(encoding="utf-8"))
    draft["updated_at"] = aged.isoformat().replace("+00:00", "Z")
    stale.write_text(json.dumps(draft), encoding="utf-8")

    reconciled = module.reconcile(data)

    assert reconciled["reconciled"] == 1
    assert _drafts(data) == []
    assert len(_pending(data)) == 1
    assert _ledger(data) == []


def test_pending_work_expires_by_age_and_by_bounds(tmp_path: Path) -> None:
    """Retention is 30 days, 100 drafts and 1 MiB, oldest first."""

    module = _load()
    data = _enabled(module, tmp_path)
    retention = module.retention(data)

    assert retention == {"days": 30, "drafts": 100, "bytes": 1024 * 1024}

    # One pending capture older than the retention window goes.
    _start(module, data, "session-old")
    _finish(module, data, "session-old")
    old = _pending(data)[0]
    record = json.loads(old.read_text(encoding="utf-8"))
    stale = datetime.now(UTC) - timedelta(days=31)
    record["updated_at"] = stale.isoformat().replace("+00:00", "Z")
    old.write_text(json.dumps(record), encoding="utf-8")

    _start(module, data, "session-new")
    _finish(module, data, "session-new")
    swept = module.reconcile(data)

    assert swept["expired"] == 1
    assert len(_pending(data)) == 1


def test_the_draft_count_bound_removes_the_oldest_first(tmp_path: Path) -> None:
    """A hard bound is deterministic rather than a rejection of new work."""

    module = _load()
    data = _enabled(module, tmp_path)
    for index in range(105):
        _start(module, data, f"session-{index:03d}")
        _finish(module, data, f"session-{index:03d}")

    module.reconcile(data)
    kept = {path.stem for path in _pending(data)}

    assert len(kept) == 100
    assert _ledger(data) == []


def test_capture_retains_no_transcript_or_response_content(tmp_path: Path) -> None:
    """Only the metadata an observation needs may be written down."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    module.hook(
        data,
        "Stop",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "prompt": "the whole brief",
            "response": "the whole answer",
            "reasoning": "the whole thinking",
            "transcript_path": "/Users/thomas/.claude/projects/x/session.jsonl",
            "diff": "--- a/x\n+++ b/x",
            "terminal_output": "pytest ...",
            "secret": "sk-live-1234567890",
        },
    )
    _finish(module, data, "session-1", checker=_checker())
    written = "\n".join(
        path.read_text(encoding="utf-8") for path in (data / "capture").rglob("*.json")
    )
    written += json.dumps(_ledger(data))

    for forbidden in (
        "the whole brief",
        "the whole answer",
        "the whole thinking",
        "+++ b/x",
        "pytest ...",
        "sk-live-1234567890",
        "/Users/thomas",
    ):
        assert forbidden not in written


def test_the_session_identity_is_opaque(tmp_path: Path) -> None:
    """A raw Harness session id is an identity we hash rather than keep."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "/Users/thomas/Projects/skills#session-1")
    _finish(module, data, "/Users/thomas/Projects/skills#session-1", checker=_checker())
    observation = _ledger(data)[0]

    assert "/Users/thomas" not in json.dumps(observation)
    assert observation["session_identity"] != "/Users/thomas/Projects/skills#session-1"


def test_the_hook_path_is_fail_open(tmp_path: Path) -> None:
    """Capture failing must never take a session down with it."""

    module = _load()
    data = _enabled(module, tmp_path)

    # A draft store that cannot be written is still a hook that exits clean.
    drafts = data / "capture" / "drafts"
    for stale in drafts.glob("*.json"):
        stale.unlink()
    drafts.rmdir()
    drafts.write_text("not a directory", encoding="utf-8")
    result = module.hook(data, "SessionStart", {"session_id": "session-1"})

    assert result["ok"] is False
    assert result["fail_open"] is True

    # And the same through the command line the Harness actually runs.
    completed = subprocess.run(
        [sys.executable, str(CAPTURE), "hook", "--event=Stop", "--data", str(data)],
        input="{ not json",
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert data.exists()


def test_status_reports_health_pending_and_storage(tmp_path: Path) -> None:
    """Status answers the five questions without touching the network."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    reported = module.status(data, tmp_path / "home")

    assert reported["enabled"] is True
    assert reported["harnesses"][0]["harness"] == "claude-code"
    assert reported["harnesses"][0]["status"] == "healthy"
    assert reported["pending"] == 1
    assert reported["oldest_pending_age_seconds"] is not None
    assert reported["storage_bytes"] > 0


def test_disabling_removes_the_integration_and_keeps_the_evidence(
    tmp_path: Path,
) -> None:
    """Turning capture off is not a purge of what it already established."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1", checker=_checker())
    kept = _ledger(data)

    result = module.disable(data, tmp_path / "home")

    assert result["enabled"] is False
    assert result["harnesses"][0]["status"] == "removed"
    assert _ledger(data) == kept
    assert module.status(data, tmp_path / "home")["enabled"] is False

    # And with capture off, a lifecycle signal writes nothing again.
    _start(module, data, "session-2")
    assert _drafts(data) == []


def test_an_unsupported_harness_is_never_reported_healthy(tmp_path: Path) -> None:
    """A Harness that cannot carry the contract says so instead of pretending."""

    module = _load()
    data = tmp_path / "data"
    result = module.enable(data, tmp_path / "home", ["cursor"], _command())

    assert result["harnesses"][0]["status"] == "unsatisfied"
    assert result["harnesses"][0]["capability"]
    assert module.status(data, tmp_path / "home")["harnesses"][0]["status"] != "healthy"


def test_notifications_are_debounced_and_stay_out_of_model_context(
    tmp_path: Path,
) -> None:
    """A notice is for the user, and repeating it is not more information."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    first = _finish(module, data, "session-1", checker=_checker(), benchmark="python")
    _start(module, data, "session-2")
    second = _finish(module, data, "session-2", checker=_checker(), benchmark="python")

    assert first["notification"] is not None
    assert second["notification"] is None
    assert first["notification"]["channel"] == "user"


def test_the_manager_can_ask_capture_to_remove_its_own_integrations(
    tmp_path: Path,
) -> None:
    """The teardown word the Manager says needs no argument and no data path."""

    completed = subprocess.run(
        [sys.executable, str(CAPTURE), "remove-integrations"],
        text=True,
        capture_output=True,
        env={**os.environ, "HOME": str(tmp_path)},
        check=False,
    )
    answered = json.loads(completed.stdout)

    assert completed.returncode == 0
    assert answered["evidence_preserved"] is True
    assert [entry["status"] for entry in answered["removed"]]


def test_the_hook_path_is_local_only_and_bounded() -> None:
    """What the synchronous path may do is provable from what it can reach.

    The contract is that a hook does bounded local metadata I/O and nothing
    else. A module that cannot reach the network, cannot start a process, and
    holds no waiting call cannot break that contract however it is invoked.
    """

    source = CAPTURE.read_text(encoding="utf-8")

    for reachable in (
        "import socket",
        "import http",
        "import urllib",
        "import requests",
        "import subprocess",
        "import threading",
        "import asyncio",
        "time.sleep",
    ):
        assert reachable not in source, reachable


def test_capture_writes_nothing_outside_its_own_data_directory(tmp_path: Path) -> None:
    """A whole session's capture touches the selected directory and nothing else."""

    module = _load()
    data = _enabled(module, tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    _start(module, data, "session-1")
    _finish(module, data, "session-1", checker=_checker(), benchmark="python")

    assert list(elsewhere.iterdir()) == []
    written = {path.relative_to(tmp_path).parts[0] for path in tmp_path.rglob("*")}
    assert written <= {"data", "home", "elsewhere"}


def test_a_harness_naming_the_event_in_its_payload_is_understood(
    tmp_path: Path,
) -> None:
    """Claude Code and Codex hand the moment over on stdin, not on the command line.

    A hook that read only its command line would answer every moment as though
    it were none of them, and no session would ever reach a boundary.
    """

    module = _load()
    data = _enabled(module, tmp_path)

    module.hook(
        data,
        "",
        {
            "hook_event_name": "SessionStart",
            "session_id": "session-1",
            "harness": "claude-code",
            "seat": _seat(),
        },
    )
    assert len(_drafts(data)) == 1

    result = module.hook(
        data,
        "",
        {
            "hook_event_name": "SessionEnd",
            "session_id": "session-1",
            "harness": "claude-code",
            "checker": _checker(),
            "benchmark": "python",
        },
    )

    assert result["imported"]["accepted"]
    assert _drafts(data) == []


def test_the_installed_hook_carries_the_data_directory_it_was_enabled_for(
    tmp_path: Path,
) -> None:
    """A hook pointed at another directory reads an empty configuration."""

    module = _load()
    data = tmp_path / "elsewhere"
    module.enable(data, tmp_path / "home", ["claude-code"], [])
    settings = json.loads(
        (tmp_path / "home" / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    command = settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]

    assert f"--data {data}" in command


def test_opting_in_without_naming_a_harness_installs_into_every_one(
    tmp_path: Path,
) -> None:
    """The consent says every supported Harness, so it cannot install none."""

    module = _load()
    result = module.enable(tmp_path / "data", tmp_path / "home", [], _command())

    assert len(result["harnesses"]) == 3
    assert {entry["status"] for entry in result["harnesses"]} == {"installed"}


def test_a_nested_payload_object_is_filtered_by_its_own_keys(tmp_path: Path) -> None:
    """An allow-list one level deep is no allow-list."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    module.hook(
        data,
        "Stop",
        {
            "session_id": "session-1",
            "measurements": {"tokens": {"input": 10}, "transcript": "the whole thing"},
        },
    )
    written = (data / "capture" / "drafts").glob("*.json")

    assert "the whole thing" not in "\n".join(
        path.read_text(encoding="utf-8") for path in written
    )


def test_status_names_the_captures_a_review_can_be_asked_for(tmp_path: Path) -> None:
    """A review takes an identity, so status has to be where the identity comes from."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    identity = _finish(module, data, "session-1")["pending"]

    assert module.status(data, tmp_path / "home")["pending_identities"] == [identity]


def test_the_seat_recorded_at_opt_in_fingerprints_later_sessions(
    tmp_path: Path,
) -> None:
    """No Harness payload names the seat, so the agent supplies it once."""

    module = _load()
    data = tmp_path / "data"
    module.enable(data, tmp_path / "home", ["claude-code"], _command(), _seat())

    # A whole session whose payloads never mention the seat at all.
    module.hook(data, "SessionStart", {"session_id": "session-1"})
    result = module.hook(
        data,
        "SessionEnd",
        {"session_id": "session-1", "checker": _checker(), "benchmark": "python"},
    )

    assert result["imported"]["accepted"]
    assert _ledger(data)[0]["routed"]["model"] == _seat()["model"]


def test_a_capture_nothing_could_import_waits_instead_of_vanishing(
    tmp_path: Path,
) -> None:
    """A refused import is work to look at, not work to drop."""

    module = _load()
    data = _enabled(module, tmp_path)

    # No seat anywhere: the observation has no configuration to be about.
    module.hook(data, "SessionStart", {"session_id": "session-1"})
    result = module.hook(
        data, "SessionEnd", {"session_id": "session-1", "checker": _checker()}
    )

    assert result["imported"] is None
    assert result["refusals"]
    assert result["pending"]
    assert len(_pending(data)) == 1
    assert _ledger(data) == []


def test_work_waiting_on_a_human_says_so_to_the_human(tmp_path: Path) -> None:
    """A deferred review nobody is told about is a review nobody does."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    result = _finish(module, data, "session-1")
    notice = result["notification"]

    assert notice["channel"] == "user"
    assert result["pending"] in notice["text"]
    for choice in ("save", "failed", "ignore"):
        assert choice in notice["text"]
