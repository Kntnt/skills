"""Automatic local usage capture shipped by the model-selector Skill."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
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


def _seat(**overrides: str) -> dict[str, Any]:
    """Provide the exact main seat an ordinary session runs on."""

    base = {
        "model": "worker-v2-2026-05-01",
        "portable_deliberation": "medium",
        "native_deliberation": "think",
        "channel": "subscription-max",
        "surface": "cli",
        "adapter_id": "claude-code",
        "serving_mode": "standard",
    }
    return {**base, **overrides}


def _enabled(module: Any, tmp_path: Path, harness: str = "claude-code") -> Path:
    """Opt in to capture in an isolated data directory and Harness root."""

    data = tmp_path / "data"
    module.enable(data, tmp_path / "home", [harness], _command())
    return data


def _command() -> list[str]:
    """Provide the command a Harness would run for a lifecycle event."""

    return ["uv", "run", str(CAPTURE), "hook"]


def _start(
    module: Any, data: Path, session: str, harness: str = "claude-code", **payload: Any
) -> None:
    """Signal that substantive work began in one session."""

    module.hook(
        data,
        "SessionStart",
        {"session_id": session, "harness": harness, "seat": _seat(), **payload},
    )


def _finish(module: Any, data: Path, session: str, **payload: Any) -> dict[str, Any]:
    """Signal that one session reached its end."""

    answered = module.hook(
        data, "SessionEnd", {"session_id": session, "harness": "claude-code", **payload}
    )
    return cast(dict[str, Any], answered)


def _usage_records(data: Path) -> list[dict[str, Any]]:
    """Return every Usage Record the store already holds."""

    path = data / "usage-records.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _drafts(data: Path) -> list[Path]:
    return sorted((data / "capture" / "drafts").glob("*.json"))


def test_enabling_the_skill_alone_captures_nothing(tmp_path: Path) -> None:
    """Capture starts on an explicit opt-in, never on the Skill being Enabled."""

    module = _load()
    data = tmp_path / "data"

    # Drive a whole session's lifecycle without ever opting in.
    _start(module, data, "session-1")
    _finish(module, data, "session-1")

    assert not (data / "capture").exists() or not _drafts(data)
    assert _usage_records(data) == []


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
    assert "Seat" in consent["retained"]
    assert "usage" in consent["retained"].lower()
    assert "no waiting store" in consent["cleanup"]
    assert result["harnesses"][0]["status"] == "installed"


def test_a_finished_session_writes_one_usage_record_and_cleans_up(
    tmp_path: Path,
) -> None:
    """A finished session becomes a Usage Record immediately, and the draft goes."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1")

    assert result["recorded"], result
    assert _drafts(data) == []

    record = _usage_records(data)[0]
    assert record["seat"]["model"] == _seat()["model"]
    assert record["harness"]["name"] == "claude-code"
    assert record["started_at"] is not None
    assert record["completed_at"] is not None
    assert record["elapsed_seconds"] is not None


def test_a_usage_record_carries_no_outcome_checker_or_cohort(tmp_path: Path) -> None:
    """Ordinary work is measured, never judged: nothing here grades a session."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    record = _usage_records(data)[0]

    for absent in (
        "outcome",
        "outcome_authority",
        "checker",
        "non_model_condition",
        "workload_cohort",
        "workload_stratum",
        "stage",
        "workload_tags",
        "configuration_fingerprint",
        "benchmark_key",
        "run_key",
    ):
        assert absent not in record, absent
    assert set(record) == set(module.USAGE_RECORD_FIELDS)


def test_a_harness_error_still_writes_a_usage_record_like_any_other_ending(
    tmp_path: Path,
) -> None:
    """There is no outcome any more, so an error is not an infrastructure verdict."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    result = module.hook(
        data,
        "session.error",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "error": {"kind": "mechanical_hinder"},
        },
    )

    assert result["recorded"]
    record = _usage_records(data)[0]
    assert "error" not in record
    assert "outcome" not in record
    assert _drafts(data) == []


def test_the_same_finished_session_appended_twice_adds_nothing_the_second_time(
    tmp_path: Path,
) -> None:
    """Idempotency is by session identity and Seat, not by wall-clock luck."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    before = _usage_records(data)

    # The Harness redelivers the same ending, for instance after a restart.
    _start(module, data, "session-1")
    again = _finish(module, data, "session-1")

    assert again["recorded"] == []
    assert again["skipped"]
    assert _usage_records(data) == before


def test_a_session_that_ran_on_two_seats_produces_one_usage_record_per_seat(
    tmp_path: Path,
) -> None:
    """A session that switched model or deliberation ran two configurations."""

    module = _load()
    data = _enabled(module, tmp_path)

    module.hook(
        data,
        "SessionStart",
        {"session_id": "session-1", "harness": "claude-code", "seat": _seat()},
    )
    module.hook(
        data,
        "Stop",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "seat": _seat(model="worker-v3-2026-08-01"),
        },
    )
    result = module.hook(
        data, "SessionEnd", {"session_id": "session-1", "harness": "claude-code"}
    )

    records = _usage_records(data)
    assert len(result["recorded"]) == 2
    assert len(records) == 2
    models = {record["seat"]["model"] for record in records}
    assert models == {"worker-v2-2026-05-01", "worker-v3-2026-08-01"}
    assert len({record["session_identity"] for record in records}) == 1


def test_simultaneous_sessions_keep_separate_drafts(tmp_path: Path) -> None:
    """Two sessions at once are two drafts and two identities, never one."""

    module = _load()
    data = _enabled(module, tmp_path)

    _start(module, data, "session-1")
    _start(module, data, "session-2")

    assert len(_drafts(data)) == 2

    _finish(module, data, "session-1")
    _finish(module, data, "session-2")
    keys = {record["usage_key"] for record in _usage_records(data)}

    assert len(keys) == 2
    assert _drafts(data) == []


def test_unavailable_measurements_stay_null(tmp_path: Path) -> None:
    """An absence is never read as a zero."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    record = _usage_records(data)[0]

    for category in module.MEASUREMENT_ALLOWED:
        assert record["usage"][category] is None


def test_capture_retains_no_transcript_or_response_content(tmp_path: Path) -> None:
    """Only the metadata a Usage Record needs may be written down."""

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
    _finish(module, data, "session-1")
    written = "\n".join(
        path.read_text(encoding="utf-8") for path in (data / "capture").rglob("*.json")
    )
    written += json.dumps(_usage_records(data))

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
    _finish(module, data, "/Users/thomas/Projects/skills#session-1")
    record = _usage_records(data)[0]

    assert "/Users/thomas" not in json.dumps(record)
    assert record["session_identity"] != "/Users/thomas/Projects/skills#session-1"


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


def test_status_reports_health_and_storage(tmp_path: Path) -> None:
    """Status answers what it is enabled, healthy, and using, nothing more."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    reported = module.status(data, tmp_path / "home")

    assert reported["enabled"] is True
    assert reported["harnesses"][0]["harness"] == "claude-code"
    assert reported["harnesses"][0]["status"] == "healthy"
    assert reported["storage_bytes"] >= 0
    assert "pending" not in reported
    assert "retention" not in reported


def test_disabling_removes_the_integration_and_keeps_usage_records(
    tmp_path: Path,
) -> None:
    """Turning capture off is not a purge of what it already established."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    kept = _usage_records(data)

    result = module.disable(data, tmp_path / "home")

    assert result["enabled"] is False
    assert result["harnesses"][0]["status"] == "removed"
    assert _usage_records(data) == kept
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


def test_a_gated_harness_is_never_reported_healthy_either(tmp_path: Path) -> None:
    """Codex's own trust review is reported through the same presence field.

    `/model-selector status` carries `healthy`, `gated`, and `absent` in the
    one per-Harness field this ticket's own key interfaces name — the
    lifecycle ticket (#223) that would otherwise define this section has not
    landed, so the state is added to the field that already exists rather
    than to one this ticket invents.
    """

    module = _load()
    data = tmp_path / "data"
    module.enable(data, tmp_path / "home", ["codex"], _command())
    reported = module.status(data, tmp_path / "home")

    assert reported["harnesses"][0]["harness"] == "codex"
    assert reported["harnesses"][0]["status"] == "gated"


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
    assert answered["usage_records_preserved"] is True
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
    _finish(module, data, "session-1")

    assert list(elsewhere.iterdir()) == []
    written = {path.relative_to(tmp_path).parts[0] for path in tmp_path.rglob("*")}
    assert written <= {"data", "home", "elsewhere"}


def test_the_usage_store_sits_beside_the_evidence_ledger(tmp_path: Path) -> None:
    """A second store rather than a second kind of ledger row."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")

    assert (data / module.USAGE_LEDGER_FILE).exists()
    assert not (data / "capture" / module.USAGE_LEDGER_FILE).exists()
    assert not (data / "run-observations.jsonl").exists()


def test_a_harness_naming_the_event_in_its_payload_is_understood(
    tmp_path: Path,
) -> None:
    """Claude Code and Codex hand the moment over on stdin, not on the command line.

    A hook that read only its command line would answer every moment as though
    it were none of them, and no session would ever reach its end.
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
        },
    )

    assert result["recorded"]
    assert _drafts(data) == []


def test_the_opencode_event_envelope_yields_a_session_identity(
    tmp_path: Path,
) -> None:
    """OpenCode hands its own event object over unmodified (ADR-0090): the
    plugin interprets nothing, so the session identity nested inside that
    event — never on the command line, and at a different path per event —
    has to reach the hook from the payload itself.
    """

    module = _load()
    data = _enabled(module, tmp_path, "opencode")

    module.hook(
        data,
        "",
        {
            "type": "session.created",
            "harness": "opencode",
            "properties": {"info": {"id": "session-1"}},
        },
    )
    assert len(_drafts(data)) == 1

    result = module.hook(
        data,
        "",
        {
            "type": "session.deleted",
            "harness": "opencode",
            "properties": {"info": {"id": "session-1"}},
        },
    )

    assert _drafts(data) == []
    assert result["recorded"]
    assert _usage_records(data)[0]["session_identity"] == module._opaque("session-1")


def test_the_opencode_idle_events_own_session_field_is_understood(
    tmp_path: Path,
) -> None:
    """`session.idle` nests the identity directly under `sessionID`, a
    different path than `session.created` and `session.deleted` use, and
    both still name the same session."""

    module = _load()
    data = _enabled(module, tmp_path, "opencode")

    module.hook(
        data,
        "",
        {
            "type": "session.created",
            "harness": "opencode",
            "properties": {"info": {"id": "session-2"}},
        },
    )
    module.hook(
        data,
        "",
        {
            "type": "session.idle",
            "harness": "opencode",
            "properties": {"sessionID": "session-2"},
        },
    )

    # One draft, updated by the second event rather than orphaned as a second one.
    assert len(_drafts(data)) == 1


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


def test_the_seat_recorded_at_opt_in_fingerprints_later_sessions(
    tmp_path: Path,
) -> None:
    """No Harness payload names the seat, so the agent supplies it once."""

    module = _load()
    data = tmp_path / "data"
    module.enable(data, tmp_path / "home", ["claude-code"], _command(), _seat())

    # A whole session whose payloads never mention the seat at all.
    module.hook(data, "SessionStart", {"session_id": "session-1"})
    result = module.hook(data, "SessionEnd", {"session_id": "session-1"})

    assert result["recorded"]
    assert _usage_records(data)[0]["seat"]["model"] == _seat()["model"]


def test_a_session_with_no_seat_known_at_all_still_writes_a_usage_record(
    tmp_path: Path,
) -> None:
    """Nothing here waits for anybody to supply a Seat before it measures."""

    module = _load()
    data = _enabled(module, tmp_path)

    module.hook(data, "SessionStart", {"session_id": "session-1"})
    result = module.hook(data, "SessionEnd", {"session_id": "session-1"})

    assert result["recorded"]
    record = _usage_records(data)[0]
    assert record["seat"] == {key: None for key in module.SEAT_ALLOWED}


def test_no_pending_review_notification_or_retention_surface_remains() -> None:
    """Ordinary work is measured, never judged: nothing here waits on a human."""

    module = _load()
    for removed in (
        "review",
        "reconcile",
        "retention",
        "review_actions",
        "RETENTION_DAYS",
        "RETENTION_DRAFTS",
        "RETENTION_BYTES",
        "ABANDONED_AFTER_SECONDS",
        "REVIEW_ACTIONS",
    ):
        assert not hasattr(module, removed), removed
