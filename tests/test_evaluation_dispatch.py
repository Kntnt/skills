"""The controlled recorder must refuse unsupported evidence, not infer it."""

from __future__ import annotations

import argparse
import copy
import io
import importlib.util
import os
import subprocess
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT: Path = Path(__file__).resolve().parents[1]
SPEC: ModuleSpec | None = importlib.util.spec_from_file_location(
    "native_dispatch", ROOT / "docs/evaluation/harness/native_dispatch.py"
)
assert SPEC is not None and SPEC.loader is not None
DISPATCH: ModuleType = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISPATCH)
PROMPT: bytes = 'Neutral Åäö β\n`alpha` "bravo"\n\n'.encode()
RESULT: bytes = "Complete β\n".encode()


def trace() -> list[dict[str, Any]]:
    """Model intact CLI0.160.0 v2 records, including both message boundaries.

    The shape comes from neutral child 01a10227-fbdc-7612-9440-161b323c6d4d,
    source SHA b8277827541e7e61dd39d5458689babbe95992f944a854b5f40d52613691fb7e.
    Values here are synthetic; the preserved primary rollout remains unchanged.
    """

    def message(role: str, text: bytes, identity: str, order: int) -> dict[str, Any]:
        """Provide the native retained message's complete identity metadata."""
        return {
            "type": "response_item",
            "payload": {
                "type": "message",
                "id": identity,
                "role": role,
                "content": [
                    {
                        "type": "input_text" if role == "user" else "output_text",
                        "text": text.decode(),
                    }
                ],
                "internal_chat_message_metadata_passthrough": {
                    "turn_id": "turn",
                    "content_item_kinds": [
                        "user.text" if role == "user" else "unknown"
                    ],
                },
                **({"phase": "final_answer"} if role == "assistant" else {}),
            },
            "metadata": {
                "retained_source": {
                    "id": {"message_id": identity, "turn_id": "turn", "role": role},
                    "complete": True,
                },
                "user_input_order": order,
            },
        }

    return [
        {
            "type": "session_meta",
            "payload": {
                "id": "fresh",
                "session_id": "fresh",
                "source": "exec",
                "cli_version": "0.160.0",
            },
        },
        {
            "type": "event_msg",
            "payload": {
                "type": "task_started",
                "turn_id": "turn",
                "root_turn_id": "turn",
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "<environment_context>neutral</environment_context>",
                    }
                ],
                "internal_chat_message_metadata_passthrough": {
                    "turn_id": "turn",
                    "content_item_kinds": ["environments.environment_context"],
                },
            },
        },
        {
            "type": "turn_context",
            "payload": {
                "turn_id": "turn",
                "root_turn_id": "turn",
                "model": "gpt-6-astra",
                "effort": "high",
            },
        },
        message("user", PROMPT, "input", 0),
        {
            "type": "event_msg",
            "payload": {
                "type": "item_completed",
                "thread_id": "fresh",
                "turn_id": "turn",
                "item": {
                    "type": "UserMessage",
                    "id": "native-input",
                    "content": [{"type": "text", "text": PROMPT.decode()}],
                },
            },
        },
        {
            "type": "event_msg",
            "payload": {
                "type": "item_completed",
                "thread_id": "fresh",
                "turn_id": "turn",
                "item": {
                    "type": "AgentMessage",
                    "id": "final",
                    "phase": "final_answer",
                    "content": [{"type": "Text", "text": RESULT.decode()}],
                },
            },
        },
        message("assistant", RESULT, "final", 1),
        {
            "type": "event_msg",
            "payload": {
                "type": "task_complete",
                "turn_id": "turn",
                "last_agent_message": RESULT.decode(),
            },
        },
    ]


def test_exact_utf8_input_and_complete_native_result() -> None:
    """Unicode and trailing empty lines are part of both authentic boundaries."""
    receipt, result = DISPATCH.bind_trace(
        trace(), PROMPT, "gpt-6-astra", "high", "0.160.0"
    )
    assert result == RESULT
    assert receipt["input_sha256"] == DISPATCH.digest(PROMPT)
    assert receipt["native_input_ordinal"] == 6
    with pytest.raises(DISPATCH.CaptureError):
        DISPATCH.bind_trace(trace(), PROMPT.rstrip(), "gpt-6-astra", "high", "0.160.0")


@pytest.mark.parametrize("field,value", [("model", "gpt-6.1-sol"), ("effort", "xhigh")])
def test_actual_seat_cannot_be_replaced_by_requested_seat(
    field: str, value: str
) -> None:
    """A syntactically valid requested seat is no evidence of the launched one."""
    records = trace()
    records[3]["payload"][field] = value
    with pytest.raises(DISPATCH.CaptureError):
        DISPATCH.bind_trace(records, PROMPT, "gpt-6-astra", "high", "0.160.0")


@pytest.mark.parametrize(
    "case",
    ["sealed", "duplicate", "version", "parent", "partial", "wrong-turn", "truncated"],
)
def test_unavailable_or_conflicting_native_evidence_fails(case: str) -> None:
    """A draft, copied result or ciphertext never completes a native receipt."""
    records = trace()
    if case == "sealed":
        records[4]["payload"]["content"] = [
            {"type": "input_text", "encrypted_content": "gAAAA"}
        ]
    elif case == "duplicate":
        records.insert(6, records[4])
    elif case == "version":
        records[0]["payload"]["cli_version"] = "0.159.3"
    elif case == "parent":
        records[0]["payload"]["parent_thread_id"] = "old-history"
    elif case == "partial":
        records.pop()
    elif case == "wrong-turn":
        records[-1]["payload"]["turn_id"] = "another-turn"
    elif case == "truncated":
        records[-1]["payload"]["last_agent_message"] = "Complete"
    with pytest.raises(DISPATCH.CaptureError):
        DISPATCH.bind_trace(records, PROMPT, "gpt-6-astra", "high", "0.160.0")


@pytest.mark.parametrize(
    "case",
    [
        "later-echo",
        "native-input-conflict",
        "missing-thread",
        "session-conflict",
        "input-turn",
        "input-order",
        "incomplete-input",
        "native-thread",
        "native-turn",
        "missing-native-input",
        "native-final-conflict",
        "native-final-id",
        "final-turn",
        "missing-turn",
        "missing-start",
    ],
)
def test_initial_and_final_native_identity_conflicts_are_rejected(case: str) -> None:
    """A matching later echo or one disagreeing native representation is insufficient."""
    records = trace()
    if case == "later-echo":
        echo = copy.deepcopy(records[4])
        records[4]["payload"]["content"][0]["text"] = "Different initial task"
        records.insert(6, echo)
    elif case == "native-input-conflict":
        records[5]["payload"]["item"]["content"][0]["text"] = "Different initial task"
    elif case == "missing-thread":
        del records[0]["payload"]["id"]
    elif case == "session-conflict":
        records[0]["payload"]["session_id"] = "other-thread"
    elif case == "input-turn":
        records[4]["metadata"]["retained_source"]["id"]["turn_id"] = "other-turn"
    elif case == "input-order":
        records[4]["metadata"]["user_input_order"] = 1
    elif case == "incomplete-input":
        records[4]["metadata"]["retained_source"]["complete"] = False
    elif case == "native-thread":
        records[5]["payload"]["thread_id"] = "other-thread"
    elif case == "native-turn":
        records[5]["payload"]["turn_id"] = "other-turn"
    elif case == "missing-native-input":
        del records[5]
    elif case == "native-final-conflict":
        records[6]["payload"]["item"]["content"][0]["text"] = "Other final"
    elif case == "native-final-id":
        records[6]["payload"]["item"]["id"] = "other-final"
    elif case == "final-turn":
        records[7]["payload"]["internal_chat_message_metadata_passthrough"][
            "turn_id"
        ] = "other-turn"
    elif case == "missing-turn":
        del records[3]["payload"]["turn_id"]
    elif case == "missing-start":
        del records[1]
    with pytest.raises(DISPATCH.CaptureError):
        DISPATCH.bind_trace(records, PROMPT, "gpt-6-astra", "high", "0.160.0")


def test_inventory_includes_dot_git_and_preserves_symlink_identity(
    tmp_path: Path,
) -> None:
    """Storage paths do not remove actual product side effects from evidence."""
    (tmp_path / ".git").mkdir()
    file = tmp_path / ".git" / "written.txt"
    file.write_bytes(PROMPT)
    link = tmp_path / "link"
    link.symlink_to(file)
    found = DISPATCH.inventory([tmp_path])
    assert found[str(file)]["sha256"] == DISPATCH.digest(PROMPT)
    assert found[str(link)]["symlink"] == str(file)


def test_inventory_masks_only_explicit_private_credential_and_tracks_modes(
    tmp_path: Path,
) -> None:
    """Ordinary same-basename content, empty directories and modes are observable."""
    ordinary = tmp_path / "auth.json"
    private = tmp_path / "private" / "auth.json"
    private.parent.mkdir()
    ordinary.write_bytes(b"AAA")
    ordinary.chmod(0o644)
    private.write_bytes(b"PRIVATE_SENTINEL")
    private.chmod(0o600)
    empty = tmp_path / "empty"
    empty.mkdir()
    before = DISPATCH.inventory([tmp_path], [private])
    ordinary.write_bytes(b"BBB")
    ordinary.chmod(0o600)
    empty.chmod(0o700)
    mode_changed = DISPATCH.inventory([tmp_path], [private])
    empty.rmdir()
    after = DISPATCH.inventory([tmp_path], [private])
    assert before[str(ordinary)]["sha256"] != after[str(ordinary)]["sha256"]
    assert before[str(ordinary)]["mode"] != after[str(ordinary)]["mode"]
    assert before[str(private)]["sha256"] is None
    assert before[str(private)]["credential_redacted"] is True
    assert before[str(empty)]["mode"] != mode_changed[str(empty)]["mode"]
    assert str(empty) in before and str(empty) not in after
    assert before[str(tmp_path)]["kind"] == "directory"


def test_helper_registers_before_reading_input_or_starting_preparation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No stdin wait, native version process or credential copy precedes ownership."""
    packet = tmp_path / "packet"
    args = argparse.Namespace(packet=packet, cleanup_script=tmp_path / "cleanup.py")
    events: list[str] = []
    monkeypatch.setattr(DISPATCH.os, "getpgrp", lambda: os.getpid())
    monkeypatch.setattr(DISPATCH, "register", lambda *args: events.append("register"))

    class Input(io.BytesIO):
        """Expose stdin read ordering without starting a process."""

        def read(self, *args: Any) -> bytes:
            events.append("stdin")
            return super().read(*args)

    monkeypatch.setattr(DISPATCH.sys, "stdin", argparse.Namespace(buffer=Input(PROMPT)))

    def prepared(args: argparse.Namespace, prompt: bytes) -> bytes:
        """Observe preparation only after ownership and complete input capture."""
        events.append("prepare")
        assert prompt == PROMPT
        return RESULT

    monkeypatch.setattr(DISPATCH, "acquire", prepared)
    assert DISPATCH.run(args) == RESULT
    assert events == ["register", "stdin", "prepare"]


def test_timeout_cleanup_stops_owned_group_without_touching_other_process(
    tmp_path: Path,
) -> None:
    """A bounded helper can stop its own work without broad process matching."""
    owned = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        start_new_session=True,
        cwd=tmp_path,
    )
    other = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        start_new_session=True,
        cwd=tmp_path,
    )
    try:
        DISPATCH.stop_owned(owned)
        assert owned.poll() is not None
        assert other.poll() is None
        with pytest.raises(ProcessLookupError):
            os.killpg(owned.pid, 0)
    finally:
        DISPATCH.stop_owned(owned)
        DISPATCH.stop_owned(other)


def test_preparation_failure_removes_private_auth_and_retains_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Failure before native launch leaves evidence rather than credentials."""
    auth = tmp_path / "auth"
    auth.mkdir()
    (auth / "auth.json").write_text("PRIVATE_SENTINEL")
    (auth / "hooks.json").write_text('{"hooks": {}}')
    packet = tmp_path / "packet"
    args = argparse.Namespace(
        packet=packet,
        cwd=tmp_path,
        native=Path(sys.executable),
        auth_home=auth,
        version="0.160.0",
        model="gpt-6-astra",
        effort="high",
        timeout=1,
        parent="fresh-parent",
        role="neutral",
        inventory_root=[],
        cleanup_script=tmp_path / "unused.py",
    )
    monkeypatch.setattr(
        DISPATCH.subprocess, "check_output", lambda *a, **k: "codex-cli 0.160.0\n"
    )
    monkeypatch.setattr(DISPATCH.os, "getpgrp", lambda: os.getpid())

    copy_original = DISPATCH.shutil.copy2
    monkeypatch.setattr(DISPATCH, "register", lambda *args: None)

    def failed_credential_copy(source: Path, destination: Path) -> None:
        """Fail only after an actual private credential file has been staged."""
        copy_original(source, destination)
        if source.name == "auth.json":
            raise OSError("credential staging unavailable")

    monkeypatch.setattr(DISPATCH.shutil, "copy2", failed_credential_copy)
    with pytest.raises(OSError, match="credential staging unavailable"):
        DISPATCH.run(args, PROMPT)
    assert not (packet / "runtime").exists()
    assert (packet / "prompt.txt").read_bytes() == PROMPT
    assert '"status": "failed"' in (packet / "receipt.json").read_text()
    assert all(
        b"PRIVATE_SENTINEL" not in p.read_bytes()
        for p in packet.rglob("*")
        if p.is_file()
    )
