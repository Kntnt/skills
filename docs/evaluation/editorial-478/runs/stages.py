# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Split one Redline packet into the five states #478 judges apart.

A Redline run with a reply checker passes through five states that its packet
holds only inside transcripts: the text as it arrived, the final Text Artifact
step 9 produced, the reply as drafted, what the checker returned, and the reply
as delivered. A miss is judged against the state it belongs to, so each is
written to a file of its own under `<packet>/stages/`, with `stages.json`
saying where each came from and whether the delivered text is the final Text
Artifact the checker was shown (issue #478).

Usage: `uv run stages.py PACKET [PACKET ...]`
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

CHECKER_OPENING = "You are checking one reply"
SECTIONS = {
    "final-text.md": "**The text as delivered.**",
    "reply-draft.md": "**The reply.**",
}
FENCE = re.compile(r"^(`{3,})[A-Za-z]*\s*$")


@dataclass
class Checker:
    """One checker subagent: the brief it was given and what it returned."""

    transcript: Path
    prompt: str
    returned: str


def _texts(message: dict[str, object]) -> list[str]:
    """Every text block of one transcript message, in order."""

    content = message.get("content")
    if isinstance(content, str):
        return [content]
    if not isinstance(content, list):
        return []
    return [
        str(block["text"])
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    ]


def read_checkers(packet: Path) -> list[Checker]:
    """Every subagent of the packet whose first instruction is the checker brief."""

    found: list[Checker] = []
    for transcript in sorted((packet / "transcripts" / "subagents").glob("*.jsonl")):
        lines = [
            json.loads(line)
            for line in transcript.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        messages = [line["message"] for line in lines if "message" in line]
        if not messages:
            continue
        prompt = "\n".join(_texts(messages[0]))
        if not prompt.lstrip().startswith(CHECKER_OPENING):
            continue
        returned = ""
        for message in messages:
            if message.get("role") == "assistant":
                texts = [text for text in _texts(message) if text.strip()]
                if texts:
                    returned = texts[-1]
        found.append(Checker(transcript, prompt, returned))
    return found


def fenced_after(prompt: str, heading: str) -> str:
    """The fenced block that follows a heading of the checker brief, unfenced."""

    lines = prompt.split(heading, 1)[1].splitlines()
    for start, line in enumerate(lines):
        opened = FENCE.match(line)
        if opened is None:
            continue
        fence = opened.group(1)
        for end in range(start + 1, len(lines)):
            if lines[end].rstrip() == fence:
                return "\n".join(lines[start + 1 : end]) + "\n"
        break
    raise ValueError(f"no fenced block after {heading!r}")


def delivered_text(packet: Path) -> tuple[str | None, str]:
    """The text the run delivered, and where it was read from."""

    captured = packet / "captured-output.md"
    if captured.is_file():
        return captured.read_text(encoding="utf-8"), "captured-output.md"
    response = (packet / "response.txt").read_text(encoding="utf-8")
    blocks: list[str] = []
    lines = response.splitlines()
    index = 0
    while index < len(lines):
        opened = FENCE.match(lines[index])
        if opened is None:
            index += 1
            continue
        fence = opened.group(1)
        for end in range(index + 1, len(lines)):
            if lines[end].rstrip() == fence:
                blocks.append("\n".join(lines[index + 1 : end]) + "\n")
                index = end
                break
        index += 1
    if not blocks:
        return None, "response.txt: no fenced text"
    return blocks[-1], "response.txt: last fenced block"


def split(packet: Path) -> dict[str, object]:
    """Write the five states of one packet, and return what was found."""

    out = packet / "stages"
    out.mkdir(exist_ok=True)
    received = (packet / "supplied-input.md").read_text(encoding="utf-8")
    (out / "received.md").write_text(received, encoding="utf-8")
    response = (packet / "response.txt").read_text(encoding="utf-8")
    (out / "delivered-reply.md").write_text(response, encoding="utf-8")

    text, text_source = delivered_text(packet)
    if text is not None:
        (out / "delivered-text.md").write_text(text, encoding="utf-8")

    checkers = read_checkers(packet)
    summary: dict[str, object] = {
        "packet": packet.name,
        "checkers": len(checkers),
        "delivered_text_source": text_source,
        "delivered_text_equals_received": text == received if text else None,
    }
    if checkers:
        checker = checkers[0]
        final = fenced_after(checker.prompt, SECTIONS["final-text.md"])
        (out / "final-text.md").write_text(final, encoding="utf-8")
        draft = fenced_after(checker.prompt, SECTIONS["reply-draft.md"])
        (out / "reply-draft.md").write_text(draft, encoding="utf-8")
        (out / "checker-prompt.md").write_text(checker.prompt, encoding="utf-8")
        (out / "checker-return.md").write_text(
            checker.returned + "\n", encoding="utf-8"
        )
        summary["checker_transcript"] = str(checker.transcript.relative_to(packet))
        summary["delivered_text_equals_final"] = (
            text.strip() == final.strip() if text is not None else None
        )
    (out / "stages.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


def main(argv: list[str]) -> int:
    """Split every packet named on the command line."""

    for name in argv:
        print(json.dumps(split(Path(name)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
