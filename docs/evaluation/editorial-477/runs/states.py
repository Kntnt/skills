"""Write apart the states a Redline run's reply passed through (#477).

    uv run --no-project python states.py PACKET OUTDIR

From one packet of the staged runner it writes, each to a file of its own:

- `received.md`: the text the run was given (`supplied-input.md`).
- `delivered.md`: the text the run delivered, from the fenced block of its
  response or, for a file-target run, from `captured-output.md`; absent where
  the run delivered none.
- `checked-received.md`, `checked-delivered.md`, `draft-reply.md`: the two texts
  and the drafted reply as the reply checker was handed them, read from the
  checker's own transcript.
- `check-return.md`: what the checker returned, its last message.
- `final-reply.md`: the reply the run delivered, without the delivered text.
- `states.json`: whether a checker ran, how many, and `x1`: whether the
  delivered text is byte for byte the text the checker was handed as delivered.

The checker is the one subagent whose first message opens with the reply-check
brief's first sentence. Nothing is inferred from what the run says it did.
"""

import json
import re
import sys
from pathlib import Path

OPENING = "You are checking one reply against the two texts it describes."
FENCE = re.compile(r"(`{4,})markdown\n(.*?)\n\1", re.DOTALL)


def first_text(record: dict) -> str:
    content = record.get("message", {}).get("content")
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content or [] if b.get("type") == "text")


def between(brief: str, start: str, end: str) -> str:
    chunk = brief[brief.index(start) + len(start) : brief.index(end)]
    found = FENCE.search(chunk)
    return found.group(2) + "\n" if found else chunk.strip() + "\n"


def main() -> int:
    packet, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    received = (packet / "supplied-input.md").read_text(encoding="utf-8")
    (out / "received.md").write_text(received, encoding="utf-8")
    response = (packet / "response.txt").read_text(encoding="utf-8")
    fenced = FENCE.search(response)
    delivered = None
    if (packet / "captured-output.md").is_file():
        delivered = (packet / "captured-output.md").read_text(encoding="utf-8")
        final = response
    elif fenced:
        delivered = fenced.group(2) + "\n"
        final = response[: fenced.start()] + response[fenced.end() :]
    else:
        final = response
    if delivered is not None:
        (out / "delivered.md").write_text(delivered, encoding="utf-8")
    (out / "final-reply.md").write_text(final.strip() + "\n", encoding="utf-8")

    checkers = []
    for path in sorted((packet / "transcripts" / "subagents").glob("*.jsonl")):
        records = [json.loads(line) for line in path.read_text().splitlines() if line]
        if records and first_text(records[0]).startswith(OPENING):
            checkers.append((path, records))
    states = {"checkers": len(checkers), "x1": None}
    if checkers:
        path, records = checkers[0]
        brief = first_text(records[0])
        texts = {
            "checked-received.md": (
                "**The text as it arrived.**",
                "**The text as delivered.**",
            ),
            "checked-delivered.md": ("**The text as delivered.**", "**The reply.**"),
        }
        for name, (start, end) in texts.items():
            (out / name).write_text(between(brief, start, end), encoding="utf-8")
        reply_end = (
            "**The measurement of the delivered text.**"
            if "**The measurement of the delivered text.**" in brief
            else "**The duties the reply is held to.**"
        )
        (out / "draft-reply.md").write_text(
            between(brief, "**The reply.**", reply_end), encoding="utf-8"
        )
        last = [r for r in records if r.get("message", {}).get("role") == "assistant"]
        (out / "check-return.md").write_text(
            first_text(last[-1]).strip() + "\n", encoding="utf-8"
        )
        states["checker_transcript"] = path.name
        checked = (out / "checked-delivered.md").read_text(encoding="utf-8")
        if delivered is not None:
            states["x1"] = checked == delivered
    (out / "states.json").write_text(
        json.dumps(states, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
