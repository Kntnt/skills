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
    """Install capture in an isolated data directory and Harness root."""

    data = tmp_path / "data"
    module.install(data, tmp_path / "home", [harness], _command())
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


def _assistant_line(
    model: str,
    effort: str,
    *,
    timestamp: str,
    is_sidechain: bool = False,
    input: int = 0,
    output: int = 0,
    cache_read: int = 0,
    cache_creation: int = 0,
    thinking: int | None = None,
) -> str:
    """Provide one assistant line exactly as Claude Code's own transcript writes it."""

    usage: dict[str, Any] = {
        "input_tokens": input,
        "output_tokens": output,
        "cache_read_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_creation,
    }
    if thinking is not None:
        usage["output_tokens_details"] = {"thinking_tokens": thinking}
    return json.dumps(
        {
            "type": "assistant",
            "isSidechain": is_sidechain,
            "message": {"model": model, "usage": usage},
            "effort": effort,
            "timestamp": timestamp,
        }
    )


def _write_transcript(path: Path, *lines: str) -> None:
    """Write one Claude Code session transcript, creating its directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# `test_enabling_the_skill_alone_captures_nothing` is removed: it pinned the
# opt-in contract this ticket ends (#223) — a hook fired directly, bypassing
# any install, and expected no-op. There is no longer a separate on/off state
# for a hook invocation to be gated on: a hook only ever runs because a
# Harness's own configuration names it, which only happens once this
# feature's integration has actually been installed, so the question the
# removed test asked no longer has a meaningful negative case to assert.


def test_installing_reports_per_harness_results(tmp_path: Path) -> None:
    """Installing answers with what each named Harness's own install did.

    There is no more consent to state before anything is written (#223
    decision 9): the disclosure moved to this Skill's own `help.md`, read
    before Select answers, and installing is simply the Manager's own word,
    answered in JSON.
    """

    module = _load()
    result = module.install(
        tmp_path / "data", tmp_path / "home", ["claude-code"], _command()
    )

    assert "consent" not in result
    assert "enabled" not in result
    assert result["installed"][0]["harness"] == "claude-code"
    assert result["installed"][0]["status"] == "installed"
    assert result["unsupported"] == {
        "count": 0,
        "supported": ["claude-code", "codex", "opencode"],
    }


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
    if drafts.is_dir():
        for stale in drafts.glob("*.json"):
            stale.unlink()
        drafts.rmdir()
    else:
        drafts.parent.mkdir(parents=True, exist_ok=True)
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


def _ran(action: str, *arguments: str, stdin: str = "") -> Any:
    """Run one capture action the way something outside this suite runs it."""

    return subprocess.run(
        [sys.executable, str(CAPTURE), action, *arguments],
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def test_the_hook_path_leaves_the_harnesss_own_channel_empty(tmp_path: Path) -> None:
    """A Harness reads its own hook's standard output as its own protocol.

    Codex parses what a hook it owns prints there and refuses an object
    carrying fields from anywhere else — its own binary says `hook returned
    invalid session start JSON output`, and the user sees a failed session
    start and a failed turn while the hook itself ran, did its work, and
    exited zero (#259). So the diagnostic object leaves on standard error and
    the channel a Harness reads stays empty, on every path.
    """

    module = _load()
    data = _enabled(module, tmp_path)
    started = _ran(
        "hook",
        "--event=SessionStart",
        "--data",
        str(data),
        stdin=json.dumps({"session_id": "session-1", "harness": "claude-code"}),
    )

    assert started.returncode == 0
    assert started.stdout == ""
    assert json.loads(started.stderr)["ok"] is True

    # And the fail-open answer travels the same way rather than falling back
    # onto the channel the Harness reads.
    drafts = data / "capture" / "drafts"
    if drafts.is_dir():
        for stale in drafts.glob("*.json"):
            stale.unlink()
        drafts.rmdir()
    drafts.write_text("not a directory", encoding="utf-8")
    broken = _ran(
        "hook",
        "--event=SessionStart",
        "--data",
        str(data),
        stdin=json.dumps({"session_id": "session-2", "harness": "claude-code"}),
    )

    assert broken.returncode == 0
    assert broken.stdout == ""
    answered = json.loads(broken.stderr)
    assert answered["ok"] is False
    assert answered["fail_open"] is True


def test_no_other_action_answers_anywhere_but_standard_output(tmp_path: Path) -> None:
    """Only the one action a Harness runs moved.

    `install-integrations` and `remove-integrations` are the Manager's own two
    words at the seams that place and remove an Enabled Skill's files, and
    their JSON answer is the seam's own answer; `status` and `purge` are read
    by this Skill's own instructions and by the person who typed them. Nothing
    but a Harness parses a stream as a protocol, and a Harness runs none of
    these four.
    """

    home = tmp_path / "home"
    home.mkdir()
    for action in ("install-integrations", "status", "purge", "remove-integrations"):
        completed = subprocess.run(
            [sys.executable, str(CAPTURE), action],
            text=True,
            capture_output=True,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        assert completed.returncode == 0, completed.stderr
        assert json.loads(completed.stdout), action


def test_the_installed_command_is_the_one_it_installs_today(tmp_path: Path) -> None:
    """Moving the channel moves no argument onto the installed command line.

    Codex records its trust decision per hook entry, keyed over the entry as
    written, so an argument added here re-gates the hook: it stops running
    until the user reviews it again. A Harness and a person therefore invoke
    the identical command line, which is also why the channel moved for both
    of them at once rather than for whoever could be told apart (#259).
    """

    module = _load()
    data = tmp_path / "data"
    module.install(data, tmp_path / "home", ["codex"], [])
    hooks = json.loads(
        (tmp_path / "home" / ".codex" / "hooks.json").read_text(encoding="utf-8")
    )

    assert hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"] == " ".join(
        [
            "uv",
            "run",
            str(CAPTURE),
            "hook",
            "--data",
            str(data),
            f"--owner={module.owner()}",
            "--harness=codex",
        ]
    )


def test_status_reports_health_and_storage(tmp_path: Path) -> None:
    """Status answers what is healthy and using, nothing more.

    There is no separate `enabled` flag any more (#223): every Harness the
    Collection Library has an adapter for is reported, whatever this machine
    happens to hold right now, because the Harness's own file is the one
    truth capture reads.
    """

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    reported = module.status(data, tmp_path / "home")

    assert "enabled" not in reported
    by_harness = {entry["harness"]: entry for entry in reported["harnesses"]}
    assert set(by_harness) == {"claude-code", "codex", "opencode"}
    assert by_harness["claude-code"]["status"] == "healthy"
    assert by_harness["codex"]["status"] == "absent"
    assert reported["storage_bytes"] >= 0
    assert "pending" not in reported
    assert "retention" not in reported


def test_disabling_removes_the_integration_and_keeps_usage_records(
    tmp_path: Path,
) -> None:
    """Disabling is not a purge of what capture already established."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    kept = _usage_records(data)

    result = module.disable(data, tmp_path / "home")

    assert "enabled" not in result
    by_harness = {entry["harness"]: entry for entry in result["harnesses"]}
    assert by_harness["claude-code"]["status"] == "removed"
    assert _usage_records(data) == kept
    status = module.status(data, tmp_path / "home")
    assert all(entry["status"] == "absent" for entry in status["harnesses"])


def test_purge_reports_the_capture_home_in_bytes_and_the_ledger_in_rows(
    tmp_path: Path,
) -> None:
    """A preview sizes the directory by byte and the JSONL store by row.

    Removing `capture/` clears its stored drafts; the Harness hooks stay
    installed and keep measuring (issue #227).
    """

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    home = module.home(data)
    ledger = data / "usage-records.jsonl"
    assert home.exists() and ledger.exists()

    # A preview reports both exact paths and their size, and writes nothing.
    preview = module.purge_paths(data)
    by_path = {entry["path"]: entry for entry in preview}
    assert by_path[str(home)] == {
        "path": str(home),
        "present": True,
        "unit": "bytes",
        "count": module.status(data, tmp_path / "home")["storage_bytes"],
    }
    assert by_path[str(ledger)] == {
        "path": str(ledger),
        "present": True,
        "unit": "rows",
        "count": 1,
    }
    assert home.exists() and ledger.exists(), "a preview must write nothing"


def test_purge_removes_the_capture_home_and_the_usage_ledger(tmp_path: Path) -> None:
    """Confirmed, purge removes both and reports exactly what it found.

    The hooks a Harness already runs stay installed: making the Skill
    Disabled is what removes those, and this verb never touches them.
    """

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")
    home = module.home(data)
    ledger = data / "usage-records.jsonl"

    preview = module.purge_paths(data)
    removed = module.purge(data)

    assert removed == preview
    assert not home.exists()
    assert not ledger.exists()

    # The Harness's own hook file is untouched: this verb never reaches it.
    settings = json.loads(
        (tmp_path / "home" / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    assert settings["hooks"]["SessionStart"]

    # There is no on/off flag of this feature's own left for a purge to clear
    # (#223): a session that starts after a purge is captured exactly as one
    # before it was, into a `capture/` this next signal recreates.
    _start(module, data, "session-2")
    assert len(_drafts(data)) == 1


def test_purge_reports_an_absent_home_and_ledger_as_absent(tmp_path: Path) -> None:
    """A data directory that never captured anything purges as a no-op."""

    module = _load()
    data = tmp_path / "data"
    report = module.purge(data)

    assert report == [
        {"path": str(module.home(data)), "present": False},
        {"path": str(data / "usage-records.jsonl"), "present": False},
    ]
    assert not data.exists() or not list(data.iterdir())


def test_the_purge_cli_previews_without_yes_and_removes_with_it(
    tmp_path: Path,
) -> None:
    """Unlike a destructive reset elsewhere in the collection, a purge preview
    is a success rather than a refusal — it simply writes nothing yet."""

    module = _load()
    data = _enabled(module, tmp_path)
    _start(module, data, "session-1")
    _finish(module, data, "session-1")

    preview = subprocess.run(
        [sys.executable, str(CAPTURE), "purge", "--data", str(data)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert preview.returncode == 0, preview.stdout + preview.stderr
    rendered = json.loads(preview.stdout)
    assert rendered["confirmed"] is False
    assert module.home(data).exists()

    done = subprocess.run(
        [sys.executable, str(CAPTURE), "purge", "--yes", "--data", str(data)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["confirmed"] is True
    assert not module.home(data).exists()


def test_an_unsupported_harness_is_collapsed_to_a_single_count(tmp_path: Path) -> None:
    """A Harness no adapter exists for is never attempted, never one row each.

    A caller naming Detected Harnesses in bulk would otherwise get one
    Unsatisfied row per Harness this collection has no adapter for — seventy
    of them, as of this ticket — burying the outcome that matters (#223
    decision 3). Named Harnesses no adapter exists for are reported as a
    single count naming the supported set instead.
    """

    module = _load()
    data = tmp_path / "data"
    result = module.install(data, tmp_path / "home", ["cursor", "windsurf"], _command())

    assert result["installed"] == []
    assert result["unsupported"] == {
        "count": 2,
        "supported": ["claude-code", "codex", "opencode"],
    }
    assert all(
        entry["status"] != "healthy"
        for entry in module.status(data, tmp_path / "home")["harnesses"]
    )


def test_a_gated_harness_is_never_reported_healthy_either(tmp_path: Path) -> None:
    """Codex's own trust review is reported through the same presence field."""

    module = _load()
    data = tmp_path / "data"
    module.install(data, tmp_path / "home", ["codex"], _command())
    reported = module.status(data, tmp_path / "home")

    by_harness = {entry["harness"]: entry for entry in reported["harnesses"]}
    assert by_harness["codex"]["status"] == "gated"


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
    """What capture itself may do is provable from what it can reach.

    The contract is that capture does bounded local metadata I/O and nothing
    else. A module that cannot reach the network, cannot start a process, and
    holds no waiting call cannot break that contract however it is invoked.
    These absences are what keep the contract true of this module now that the
    same session-end invocation also dispatches a bounded conditional
    retrieval (ADR-0167): that work lives in `refresh.py` and is held to its
    own pins in `test_refresh.py`, and none of it reaches here.
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


def test_the_installed_hook_carries_the_data_directory_it_was_installed_for(
    tmp_path: Path,
) -> None:
    """A hook pointed at another directory writes where nobody looks for it."""

    module = _load()
    data = tmp_path / "elsewhere"
    module.install(data, tmp_path / "home", ["claude-code"], [])
    settings = json.loads(
        (tmp_path / "home" / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    command = settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]

    assert f"--data {data}" in command


def test_naming_no_harness_installs_into_every_supported_one(
    tmp_path: Path,
) -> None:
    """Naming no Harness means every Harness an adapter exists for."""

    module = _load()
    result = module.install(tmp_path / "data", tmp_path / "home", [], _command())

    assert len(result["installed"]) == 3
    assert {entry["status"] for entry in result["installed"]} == {"installed"}
    assert result["unsupported"]["count"] == 0


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


# `test_the_seat_recorded_at_opt_in_fingerprints_later_sessions` is removed:
# nothing is supplied at installation any more (#223 decision 7) — the
# `--seat` argument, the configured-seat fallback, and the `seat` key in the
# capture configuration are all gone, so there is no opt-in seat left for a
# later session with no payload seat to fall back on. What replaced it is
# `test_a_session_with_no_seat_known_at_all_still_writes_a_usage_record`
# below, unchanged: such a session still writes a Usage Record, its Seat
# fields explicit nulls.


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


def test_no_separate_consent_or_configuration_state_remains() -> None:
    """Capture follows the Skill's own Enabled state and asks for nothing (#223).

    There is no second opt-in, no consent text, no stored on/off flag, and no
    Harness-guessing fallback left: disk — the Harness's own configuration —
    is the one truth capture ever reads (ADR-0090).
    """

    module = _load()
    for removed in (
        "CONSENT",
        "enable",
        "config",
        "_config_path",
        "_configured_harness",
        "_configured_seat",
    ):
        assert not hasattr(module, removed), removed

    # The mirror word replaces the old opt-in action, and the old actions no
    # longer parse at all.
    assert module.parse_args(["install-integrations"]).action == "install-integrations"
    for stale in ("enable", "disable"):
        try:
            module.parse_args([stale])
        except SystemExit as exc:
            assert exc.code != 0
        else:
            raise AssertionError(f"{stale!r} still parses as an action")


# --- Reading the finished session's own record (#225) ------------------------


def test_a_finished_session_reads_its_exact_model_effort_and_tokens_from_the_record(
    tmp_path: Path,
) -> None:
    """The Seat and the usage come from the Harness's own record, not a guess."""

    module = _load()
    data = _enabled(module, tmp_path)
    transcript = tmp_path / "session-1.jsonl"
    _write_transcript(
        transcript,
        _assistant_line(
            "claude-opus-5",
            "high",
            timestamp="2026-09-01T10:00:00Z",
            input=10,
            output=20,
            cache_read=5,
            cache_creation=3,
            thinking=7,
        ),
    )

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1", transcript_path=str(transcript))

    assert result["recorded"]
    record = _usage_records(data)[0]
    assert record["seat"]["model"] == "claude-opus-5"
    assert record["seat"]["native_deliberation"] == "high"
    assert record["usage"]["tokens"] == {
        "input": 10,
        "output": 20,
        "cache_read": 5,
        "cache_creation": 3,
        "thinking": 7,
    }


def test_a_record_read_with_no_payload_seat_leaves_channel_and_surface_null(
    tmp_path: Path,
) -> None:
    """Nothing is supplied at installation any more, so nothing is left to fall
    back on but the record and the payload themselves (#223 decision 7).

    The record supplies the exact model and the deliberation control; a
    session whose payloads never named a seat either has no configured seat
    left to borrow channel or surface from, so both stay an explicit null.
    """

    module = _load()
    data = _enabled(module, tmp_path)
    transcript = tmp_path / "session-1.jsonl"
    _write_transcript(
        transcript,
        _assistant_line(
            "claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1
        ),
    )

    module.hook(
        data, "SessionStart", {"session_id": "session-1", "harness": "claude-code"}
    )
    module.hook(
        data,
        "SessionEnd",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "transcript_path": str(transcript),
        },
    )

    record = _usage_records(data)[0]
    assert record["seat"]["model"] == "claude-opus-5"
    assert record["seat"]["native_deliberation"] == "high"
    assert record["seat"]["channel"] is None
    assert record["seat"]["surface"] is None


def test_a_session_that_delegated_work_writes_a_second_record_for_that_seat(
    tmp_path: Path,
) -> None:
    """A subagent's turns are counted against its own Seat, never the main one's."""

    module = _load()
    data = _enabled(module, tmp_path)
    session_dir = tmp_path / "session-1"
    transcript = tmp_path / "session-1.jsonl"
    _write_transcript(
        transcript,
        _assistant_line(
            "claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=10
        ),
    )
    _write_transcript(
        session_dir / "subagents" / "agent-a1.jsonl",
        _assistant_line(
            "claude-sonnet-5",
            "medium",
            timestamp="2026-09-01T10:01:00Z",
            is_sidechain=True,
            input=3,
        ),
    )

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1", transcript_path=str(transcript))

    records = _usage_records(data)
    assert len(result["recorded"]) == 2
    assert len(records) == 2

    by_model = {record["seat"]["model"]: record for record in records}
    assert by_model["claude-opus-5"]["usage"]["tokens"]["input"] == 10
    assert by_model["claude-sonnet-5"]["usage"]["tokens"]["input"] == 3

    # The delegated Seat's own surface is not the main session's to lend.
    delegated = by_model["claude-sonnet-5"]
    for field in ("channel", "surface", "adapter_id", "serving_mode"):
        assert delegated["seat"][field] is None, field
    assert delegated["seat"]["native_deliberation"] == "medium"


def test_a_missing_record_still_writes_the_row_with_every_measurement_null(
    tmp_path: Path,
) -> None:
    """A Harness that kept no readable record is an absence, not a failure.

    Nothing here names a seat at all — no payload and no opt-in — so the row
    still measures nothing, exactly as it did before this ticket.
    """

    module = _load()
    data = _enabled(module, tmp_path)

    module.hook(
        data, "SessionStart", {"session_id": "session-1", "harness": "claude-code"}
    )
    result = module.hook(
        data,
        "SessionEnd",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "transcript_path": str(tmp_path / "never-written.jsonl"),
        },
    )

    assert result["recorded"]
    record = _usage_records(data)[0]
    assert record["usage"]["tokens"] is None
    assert record["seat"]["model"] is None


def test_a_truncated_record_still_writes_the_row_and_never_raises(
    tmp_path: Path,
) -> None:
    """An unparseable line is skipped; the row is still written."""

    module = _load()
    data = _enabled(module, tmp_path)
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text("{ not json at all\nstill not json\n", encoding="utf-8")

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1", transcript_path=str(transcript))

    assert result["recorded"]
    assert _usage_records(data)[0]["usage"]["tokens"] is None


def test_no_forbidden_content_reaches_a_usage_record_from_a_read_transcript(
    tmp_path: Path,
) -> None:
    """Even a transcript packed with everything forbidden yields none of it."""

    module = _load()
    data = _enabled(module, tmp_path)
    session_dir = tmp_path / "session-1"
    transcript = tmp_path / "session-1.jsonl"
    line = json.loads(
        _assistant_line(
            "claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1
        )
    )
    line["message"]["content"] = [{"type": "text", "text": "the whole answer"}]
    line["message"]["reasoning"] = "the whole thinking"
    line["cwd"] = "/Users/thomas/Projects/skills"
    line["toolUseResult"] = {"stdout": "pytest ...", "diff": "--- a/x\n+++ b/x"}
    _write_transcript(transcript, json.dumps(line))
    _write_transcript(
        session_dir / "subagents" / "agent-a1.jsonl",
        _assistant_line(
            "claude-sonnet-5",
            "medium",
            timestamp="2026-09-01T10:01:00Z",
            is_sidechain=True,
            input=1,
        ),
    )

    _start(module, data, "session-1")
    result = _finish(module, data, "session-1", transcript_path=str(transcript))

    assert result["recorded"]
    written = json.dumps(_usage_records(data)) + json.dumps(result)
    for forbidden in (
        "the whole answer",
        "the whole thinking",
        "pytest ...",
        "+++ b/x",
        "/Users/thomas",
        str(transcript),
    ):
        assert forbidden not in written


def test_the_transcript_path_never_reaches_a_persisted_draft(tmp_path: Path) -> None:
    """A locate-only field is read to open the record and retained nowhere."""

    module = _load()
    data = _enabled(module, tmp_path)
    transcript = tmp_path / "the-session-transcript.jsonl"

    module.hook(
        data,
        "Stop",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "transcript_path": str(transcript),
        },
    )
    written = "\n".join(
        path.read_text(encoding="utf-8") for path in (data / "capture").rglob("*.json")
    )

    assert str(transcript) not in written
    assert "transcript_path" not in written


def test_transcript_path_is_an_allowed_payload_field(tmp_path: Path) -> None:
    """The locate-only field is named on the allow-list rather than inferred."""

    module = _load()
    assert "transcript_path" in module.PAYLOAD_ALLOWED


def test_status_names_which_harnesses_supply_measurements(tmp_path: Path) -> None:
    """A store of empty rows is not something to leave for the user to discover."""

    module = _load()
    data = tmp_path / "data"
    module.install(data, tmp_path / "home", ["claude-code", "codex"], _command())
    reported = module.status(data, tmp_path / "home")

    by_harness = {entry["harness"]: entry for entry in reported["harnesses"]}
    assert by_harness["claude-code"]["measurements"] is True
    assert by_harness["codex"]["measurements"] is False


def test_an_unreadable_record_falls_back_to_whatever_the_lifecycle_signals_gave(
    tmp_path: Path,
) -> None:
    """A payload-supplied seat still measures a session the record cannot describe."""

    module = _load()
    data = _enabled(module, tmp_path)

    module.hook(
        data,
        "SessionStart",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "seat": _seat(),
            "measurements": {"tokens": {"input": 42}},
        },
    )
    result = module.hook(
        data,
        "SessionEnd",
        {
            "session_id": "session-1",
            "harness": "claude-code",
            "transcript_path": str(tmp_path / "never-written.jsonl"),
        },
    )

    assert result["recorded"]
    record = _usage_records(data)[0]
    assert record["seat"]["model"] == _seat()["model"]
    assert record["usage"]["tokens"] == {"input": 42}
