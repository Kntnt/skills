"""Keep absent native checker states distinct from an empty return (#489)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR = ROOT / "docs/evaluation/editorial-489/harness/states.py"


@pytest.mark.parametrize("encrypted", [False, True])
def test_native_checker_state_is_preserved_or_explicitly_missing(
    tmp_path: Path, encrypted: bool
) -> None:
    """Exercise the packet CLI using native task and final-message boundaries."""
    packet = tmp_path / "packet"
    sessions = packet / "native-sessions"
    sessions.mkdir(parents=True)
    artifact = "# Title\n\nA complete text.\n"
    draft = "The title identifies its subject.\n"
    brief = (
        "You are checking one reply against the two texts it describes.\n"
        "**The text as it arrived.** This is the complete text:\n\n"
        f"```markdown\n{artifact}```\n\n"
        "**The text as delivered.** This is the complete text:\n\n"
        f"```markdown\n{artifact}```\n\n"
        "**The reply.** This is everything:\n\n"
        f"```markdown\n{draft}```\n\n"
        "**The duties the reply is held to.**\n"
    )
    task_content = (
        [{"type": "encrypted_content", "encrypted_content": "gAAAA-unavailable"}]
        if encrypted
        else [{"type": "input_text", "text": brief}]
    )
    events = [
        {"type": "session_meta", "payload": {"id": "checker", "source": "subagent"}},
        {
            "type": "response_item",
            "payload": {
                "type": "agent_message",
                "recipient": "/root/reply_check",
                "content": task_content,
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "phase": "final_answer",
                "content": [
                    {
                        "type": "output_text",
                        "text": "1. False statements.\nnone\n2. Claim changes.\nnone",
                    }
                ],
            },
        },
    ]
    (sessions / "checker.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    (packet / "supplied-input.md").write_text(artifact)
    (packet / "captured-output.md").write_text(artifact)
    (packet / "response.txt").write_text(draft)
    out = tmp_path / "states"

    # The evaluator command observes public trace states, never guesses a draft.
    result = subprocess.run(
        [sys.executable, str(EXTRACTOR), str(packet), str(out)],
        cwd=ROOT,
        env=os.environ.copy(),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    state = json.loads((out / "states.json").read_text())
    assert state["checkers"] == 1
    if encrypted:
        assert state["complete"] is False
        assert "checker brief encrypted" in state["missing"]
        assert state["x1"] is None
        assert not (out / "draft-reply.md").exists()
    else:
        assert state["complete"] is True
        assert state["missing"] == []
        assert state["x1"] is True
        assert (out / "checked-received.md").read_text() == artifact
        assert (out / "checked-delivered.md").read_text() == artifact
        assert (out / "draft-reply.md").read_text() == draft
    assert (out / "check-return.md").read_text().endswith("none\n")
