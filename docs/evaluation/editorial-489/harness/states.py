# /// script
# requires-python = ">=3.12"
# ///
"""Extract public GPT-native reply states and explicitly report capture gaps.

The packet CLI accepts PACKET OUTDIR. It never reconstructs an encrypted
checker brief from the terminal reply or treats it as an empty checker return.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
from pathlib import Path
from typing import Any

OPENING = "You are checking one reply against the two texts it describes."
FENCE = re.compile(
    r"^(`{3,})(?:markdown|md|text)?\s*\n(.*?)\n\1[ \t]*$", re.MULTILINE | re.DOTALL
)


def text_of(payload: dict[str, Any]) -> str:
    """Read public message content without attempting to decode ciphertext."""
    return "".join(block.get("text", "") for block in payload.get("content", []))


def records(path: Path) -> list[dict[str, Any]]:
    """Support native rollouts before and after evidence compression."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def between(brief: str, start: str, end: str) -> str | None:
    """Extract complete fenced material, refusing ambiguous unfenced wrappers."""
    if start not in brief or end not in brief:
        return None
    chunk = brief.split(start, 1)[1].split(end, 1)[0]
    match = FENCE.search(chunk)
    return match.group(2) + "\n" if match else None


def extract(packet: Path, out: Path) -> dict[str, Any]:
    """Keep absent states absent and expose the reason beside every packet."""
    out.mkdir(parents=True, exist_ok=False)
    received = (packet / "supplied-input.md").read_text()
    response = (packet / "response.txt").read_text()
    (out / "received.md").write_text(received)
    delivered: str | None = None
    final = response
    if (packet / "captured-output.md").is_file():
        delivered = (packet / "captured-output.md").read_text()
    elif match := FENCE.search(response):
        delivered = match.group(2) + "\n"
        final = response[: match.start()] + response[match.end() :]
    if delivered is not None:
        (out / "delivered.md").write_text(delivered)
    (out / "final-reply.md").write_text(final.strip() + "\n")

    # Identify the actual checker delegate, including encrypted task messages.
    checkers: list[tuple[Path, list[dict[str, Any]], str]] = []
    sessions = packet / "native-sessions"
    paths = sorted([*sessions.rglob("*.jsonl"), *sessions.rglob("*.jsonl.gz")])
    for path in paths:
        events = records(path)
        for event in events:
            payload = event.get("payload", {})
            if (
                event.get("type") != "response_item"
                or payload.get("type") != "agent_message"
            ):
                continue
            text = text_of(payload)
            recipient = payload.get("recipient", "").lower()
            if OPENING in text or ("check" in recipient and "reply" in recipient):
                checkers.append((path, events, text))
                break
    missing: list[str] = []
    state: dict[str, Any] = {"checkers": len(checkers), "x1": None, "missing": missing}
    if not paths:
        missing.append("native trace unavailable")
    if len(checkers) > 1:
        missing.append("multiple checker delegates: application boundary ambiguous")
    if checkers:
        path, events, brief = checkers[0]
        state["checker_transcript"] = str(path.relative_to(packet))
        if OPENING not in brief:
            missing.append("checker brief encrypted")
        else:
            endings = (
                "**The measurement of the delivered text.**"
                if "**The measurement of the delivered text.**" in brief
                else "**The duties the reply is held to.**"
            )
            boundaries = {
                "checked-received.md": (
                    "**The text as it arrived.**",
                    "**The text as delivered.**",
                ),
                "checked-delivered.md": (
                    "**The text as delivered.**",
                    "**The reply.**",
                ),
                "draft-reply.md": ("**The reply.**", endings),
            }
            for name, (start, end) in boundaries.items():
                material = between(brief, start, end)
                if material is None:
                    missing.append(f"unavailable or ambiguous {name}")
                else:
                    (out / name).write_text(material)
            checked = out / "checked-delivered.md"
            if checked.is_file() and delivered is not None:
                state["x1"] = checked.read_text() == delivered
        returns = [
            event["payload"]
            for event in events
            if event.get("type") == "response_item"
            and event.get("payload", {}).get("role") == "assistant"
            and event["payload"].get("phase") == "final_answer"
        ]
        if returns:
            (out / "check-return.md").write_text(text_of(returns[-1]).strip() + "\n")
        else:
            missing.append("checker terminal return unavailable")
    state["complete"] = not missing
    (out / "states.json").write_text(json.dumps(state, indent=2) + "\n")
    return state


if __name__ == "__main__":
    extract(Path(sys.argv[1]), Path(sys.argv[2]))
