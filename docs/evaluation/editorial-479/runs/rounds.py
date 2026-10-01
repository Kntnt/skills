"""Write a packet's four review stages to its `rounds.md` (issue #479).

The plan asks that the first review's findings, each correction round's
proposal, the re-review's decision and the delivered text be told apart. This
reads them from a packet the #388 runner kept: the correction briefs from
`trace-index.json`, what each correction subagent returned and what the session
said next from `transcripts/parent.jsonl`, and the delivered text from
`captured-output.md` or the reply. It extracts and compares; it judges nothing.

Usage: python3 rounds.py PACKET [PACKET ...]
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

BRIEF_OPENING = "You are making one correction to one text."


def section(prompt: str, start: str, end: str) -> str:
    head = prompt.find(start)
    tail = prompt.find(end, head)
    if head < 0 or tail < 0:
        return ""
    return prompt[head + len(start) : tail].strip()


def fenced(text: str) -> str | None:
    """The body of the longest fenced block in TEXT, or None."""
    blocks = re.findall(
        r"^(`{3,}|~{3,})[^\n]*\n(.*?)^\1\s*$", text, re.MULTILINE | re.DOTALL
    )
    if not blocks:
        return None
    return max((body for _, body in blocks), key=len)


def report(returned: str) -> str:
    """The subagent's own report, out of the Harness's hand-back frame."""
    marker = "The report follows:\n"
    if marker not in returned:
        return returned
    body = returned.split(marker, 1)[1]
    body = re.split(r"^agentId: ", body, maxsplit=1, flags=re.MULTILINE)[0]
    return "\n".join(line.removeprefix("  ") for line in body.splitlines())


def handed_text(prompt: str) -> str:
    body = section(prompt, "**The text.**", "**The findings.**")
    return fenced(body) or body


def differences(before: str, after: str) -> str:
    if before.rstrip("\n") == after.rstrip("\n"):
        return "No difference.\n"
    lines = difflib.unified_diff(
        before.rstrip("\n").splitlines(),
        after.rstrip("\n").splitlines(),
        "before",
        "after",
        lineterm="",
        n=0,
    )
    return "```diff\n" + "\n".join(lines) + "\n```\n"


def tool_result_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )
    return ""


def session_events(transcript: Path) -> list[tuple[str, str, str]]:
    """(kind, id, text) in order: tool uses, tool results and assistant text."""
    events = []
    for line in transcript.read_text().splitlines():
        record = json.loads(line)
        message = record.get("message")
        if not isinstance(message, dict) or not isinstance(
            message.get("content"), list
        ):
            continue
        for part in message["content"]:
            kind = part.get("type")
            if kind == "tool_use":
                events.append(("use", part["id"], part.get("name", "")))
            elif kind == "tool_result":
                text = tool_result_text(part.get("content"))
                events.append(("result", part["tool_use_id"], text))
            elif kind == "text" and record.get("type") == "assistant":
                events.append(("text", "", part["text"]))
    return events


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.strip().splitlines())


def write_rounds(packet: Path) -> None:
    index = json.loads((packet / "trace-index.json").read_text())
    session = next(agent for agent in index["agents"] if agent["role"] == "session")
    events = session_events(packet / "transcripts" / "parent.jsonl")
    supplied = (packet / "supplied-input.md").read_text()
    reply = (packet / "response.txt").read_text()
    briefs = [
        call
        for call in session["calls"]
        if call["tool"] == "Agent"
        and call["arguments"].get("prompt", "").startswith(BRIEF_OPENING)
    ]
    out = [f"# The review stages of `{packet.name}`\n"]
    out.append(
        "Extracted by `rounds.py` from `trace-index.json`, `transcripts/` and the "
        "delivered text. It judges nothing.\n"
    )
    out.append("## 1. The first review's findings\n")
    if briefs:
        findings = section(
            briefs[0]["arguments"]["prompt"], "**The findings.**", "**The contract.**"
        )
        out.append("From the first correction brief the session handed a subagent:\n")
        out.append(quote(findings) + "\n")
    else:
        out.append(
            "The session started no correction subagent. Its findings, if any, are "
            "the ones its reply reports.\n"
        )
    for number, call in enumerate(briefs, 1):
        prompt = call["arguments"]["prompt"]
        position = next(
            i
            for i, event in enumerate(events)
            if event[0] == "use" and event[1] == call["tool_use_id"]
        )
        returned = next(
            (
                event[2]
                for event in events[position:]
                if event[0] == "result" and event[1] == call["tool_use_id"]
            ),
            None,
        )
        out.append(f"## 2. Round {number}: the correction proposal\n")
        if number > 1:
            findings = section(prompt, "**The findings.**", "**The contract.**")
            out.append("The findings this round was handed:\n")
            out.append(quote(findings) + "\n")
        if returned is None:
            out.append("The trace kept no return from this subagent.\n")
            continue
        returned = report(returned)
        proposal = fenced(returned)
        if proposal is None:
            out.append("The return carries no fenced text. It reads:\n")
            out.append(quote(returned) + "\n")
        else:
            out.append(
                "Differences between the text the round was handed and the text "
                "it returned:\n"
            )
            out.append(differences(handed_text(prompt), proposal))
            note = re.sub(
                r"^(`{3,}|~{3,})[^\n]*\n\s*^\1[ \t]*$\n?",
                "",
                returned.replace(proposal, ""),
                flags=re.MULTILINE,
            ).strip()
            if note:
                out.append("The subagent's note beside its text:\n")
                out.append(quote(note) + "\n")
        out.append(f"## 3. Round {number}: what the session said next\n")
        after = []
        for event in events[position + 1 :]:
            if event[0] == "use" and any(
                event[1] == later["tool_use_id"] for later in briefs[number:]
            ):
                break
            if event[0] == "text" and event[2].strip() != reply.strip():
                after.append(event[2])
        out.append(
            quote("\n\n".join(after)) + "\n"
            if after
            else "The session wrote no text after the round.\n"
        )
    out.append("## 4. The delivered text\n")
    captured = packet / "captured-output.md"
    if captured.exists():
        out.append("`captured-output.md` against the input:\n")
        out.append(differences(supplied, captured.read_text()))
    else:
        delivered = fenced(reply)
        if delivered is None:
            out.append("The reply delivers no text.\n")
        else:
            out.append("The text in the reply against the input:\n")
            out.append(differences(supplied, delivered))
    (packet / "rounds.md").write_text("\n".join(out))


if __name__ == "__main__":
    for argument in sys.argv[1:]:
        write_rounds(Path(argument))
