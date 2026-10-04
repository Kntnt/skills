# /// script
# requires-python = ">=3.12"
# ///
"""Expose captured Write comparisons and exact last-checked delivery bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from resource_evidence import returned_strings


def main() -> None:
    """Retain reports as readable evidence, never as semantic judge material."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = args.run
    captures = json.loads((run / "file-versions.json").read_text())
    drafts = []
    retained = []
    for capture in captures:
        path = Path(capture["path"])
        if "write-source-check-" not in str(path.parent):
            continue
        if re.fullmatch(r"draft(?:-\d+)?\.md", path.name):
            drafts.append(capture)
        elif re.fullmatch(r"(?:report|validation|dispositions)-\d+\.md", path.name):
            target = run / path.name
            target.write_bytes(
                (run / "file-versions" / capture["capture"]).read_bytes()
            )
            retained.append({**capture, "readable_copy": path.name})
    last = drafts[-1] if drafts else None
    last_bytes = (
        (run / "file-versions" / last["capture"]).read_bytes() if last else None
    )
    if last_bytes is not None:
        (run / "last-checked-draft.md").write_bytes(last_bytes)
    artifact = (
        (run / "delivered.md").read_bytes() if (run / "delivered.md").exists() else None
    )
    prose = (
        re.sub(rb"\A---\n[\s\S]*?\n---\n\n", b"", artifact, count=1)
        if artifact is not None
        else None
    )
    reads = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        for event in events:
            payload = event.get("payload", {})
            if event["type"] != "response_item" or payload.get("type") not in {
                "function_call_output",
                "custom_tool_call_output",
            }:
                continue
            if last_bytes is not None and any(
                last_bytes.decode() in text
                for text in returned_strings(payload.get("output"))
            ):
                reads.append(
                    {
                        "session": meta["id"],
                        "source": meta["source"],
                        "file": str(path.relative_to(run)),
                        "ordinal": event.get("ordinal"),
                        "call_id": payload.get("call_id"),
                    }
                )
    report = {
        "method": "Last externally captured source-check draft and exact delivered prose after removing only leading handoff metadata. Complete returned-byte matches establish observed reads, not the correctness of a comparison or an encrypted dispatch.",
        "reports_and_dispositions": retained,
        "last_checked_capture": last,
        "complete_returned_last_checked_reads": reads,
        "delivered_prose_sha256": hashlib.sha256(prose).hexdigest() if prose else None,
        "delivered_prose_matches_last_checked": prose == last_bytes
        if prose is not None and last_bytes is not None
        else None,
    }
    (run / "write-verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "run": run.name,
                "last_checked_matches": report["delivered_prose_matches_last_checked"],
            }
        )
    )


if __name__ == "__main__":
    main()
