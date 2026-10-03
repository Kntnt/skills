"""The controlled recorder must refuse unsupported evidence, not infer it."""

from __future__ import annotations

import argparse
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
    """Use the public native record shapes, with one input and completed turn."""
    return [
        {
            "type": "session_meta",
            "payload": {"id": "fresh", "source": "exec", "cli_version": "0.160.0"},
        },
        {
            "type": "turn_context",
            "payload": {"turn_id": "turn", "model": "gpt-6-astra", "effort": "high"},
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": PROMPT.decode()}],
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "phase": "final_answer",
                "content": [{"type": "output_text", "text": RESULT.decode()}],
            },
        },
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
    with pytest.raises(DISPATCH.CaptureError):
        DISPATCH.bind_trace(trace(), PROMPT.rstrip(), "gpt-6-astra", "high", "0.160.0")


@pytest.mark.parametrize("field,value", [("model", "gpt-6.1-sol"), ("effort", "xhigh")])
def test_actual_seat_cannot_be_replaced_by_requested_seat(
    field: str, value: str
) -> None:
    """A syntactically valid requested seat is no evidence of the launched one."""
    records = trace()
    records[1]["payload"][field] = value
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
        records[2]["payload"]["content"] = [
            {"type": "input_text", "encrypted_content": "gAAAA"}
        ]
    elif case == "duplicate":
        records.insert(3, records[2])
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
    assert found[str(link)] == {"symlink": str(file)}


def test_timeout_cleanup_stops_owned_group_without_touching_other_process() -> None:
    """A bounded helper can stop its own work without broad process matching."""
    owned = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"], start_new_session=True
    )
    other = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"], start_new_session=True
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

    def failed_registration(*args: Any) -> None:
        raise subprocess.SubprocessError("registration unavailable")

    monkeypatch.setattr(DISPATCH, "register", failed_registration)
    with pytest.raises(subprocess.SubprocessError):
        DISPATCH.run(args, PROMPT)
    assert not (packet / "runtime").exists()
    assert (packet / "prompt.txt").read_bytes() == PROMPT
    assert '"status": "failed"' in (packet / "receipt.json").read_text()
    assert all(
        b"PRIVATE_SENTINEL" not in p.read_bytes()
        for p in packet.rglob("*")
        if p.is_file()
    )
