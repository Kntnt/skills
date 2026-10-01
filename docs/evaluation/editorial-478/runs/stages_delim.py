# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Split a packet whose checker brief holds a block between `<<<NAME` lines.

`stages.py` was frozen with the plan, and it reads each block of a filled
checker brief from a backtick fence, as #475's runs filled it. The run
`post-case-study-clean-resp-3` handed its checker the drafted reply between a
`<<<REPLY` line and a `REPLY` line instead, so `stages.py` stops on it. This
script, written after that run, reads either form and writes the same files
and the same `stages.json`, with `split_by` saying how. It is used only where
`stages.py` stops (issue #478).

Usage: `uv run stages_delim.py PACKET`
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHECKER_OPENING = "You are checking one reply"
BLOCK = re.compile(
    r"[^\n]*\n\n(?:(`{3,})[A-Za-z]*\n(.*?)\n\1$|<<<(\w+)\n(.*?)\n\3$)",
    re.DOTALL | re.MULTILINE,
)
FENCE = re.compile(r"^(`{3,})[A-Za-z]*\n(.*?)\n\1$", re.DOTALL | re.MULTILINE)


def _texts(message: dict[str, object]) -> str:
    """The text blocks of one transcript message, joined."""

    content = message.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(
        str(block["text"])
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    )


def block(prompt: str, heading: str) -> str:
    """The block that follows a heading of the checker brief, in either form."""

    found = BLOCK.match(prompt.split(heading, 1)[1])
    if found is None:
        raise ValueError(f"no block after {heading!r}")
    return (found.group(2) if found.group(1) else found.group(4)) + "\n"


def split(packet: Path) -> dict[str, object]:
    """Write the five states of one packet, and return what was found."""

    out = packet / "stages"
    out.mkdir(exist_ok=True)
    for transcript in sorted((packet / "transcripts" / "subagents").glob("*.jsonl")):
        lines = [
            json.loads(line)
            for line in transcript.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        messages = [line["message"] for line in lines if "message" in line]
        prompt = _texts(messages[0]) if messages else ""
        if prompt.lstrip().startswith(CHECKER_OPENING):
            break
    else:
        raise ValueError(f"{packet}: no checker")
    returned = ""
    for message in messages:
        if message.get("role") == "assistant" and _texts(message).strip():
            returned = _texts(message)
    received = (packet / "supplied-input.md").read_text(encoding="utf-8")
    response = (packet / "response.txt").read_text(encoding="utf-8")
    final = block(prompt, "**The text as delivered.**")
    (out / "received.md").write_text(received, encoding="utf-8")
    (out / "delivered-reply.md").write_text(response, encoding="utf-8")
    (out / "final-text.md").write_text(final, encoding="utf-8")
    (out / "reply-draft.md").write_text(
        block(prompt, "**The reply.**"), encoding="utf-8"
    )
    (out / "checker-prompt.md").write_text(prompt, encoding="utf-8")
    (out / "checker-return.md").write_text(returned + "\n", encoding="utf-8")
    captured = packet / "captured-output.md"
    if captured.is_file():
        text: str | None = captured.read_text(encoding="utf-8")
        source = "captured-output.md"
    else:
        fences = FENCE.findall(response)
        text = fences[-1][1] + "\n" if fences else None
        source = "response.txt: last fenced block"
    if text is not None:
        (out / "delivered-text.md").write_text(text, encoding="utf-8")
    summary: dict[str, object] = {
        "packet": packet.name,
        "checkers": 1,
        "delivered_text_source": source,
        "delivered_text_equals_received": text == received if text else None,
        "checker_transcript": str(transcript.relative_to(packet)),
        "delivered_text_equals_final": (
            text.strip() == final.strip() if text is not None else None
        ),
        "split_by": "stages_delim.py, which also reads <<<NAME blocks",
    }
    (out / "stages.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    print(json.dumps(split(Path(sys.argv[1])), ensure_ascii=False))
