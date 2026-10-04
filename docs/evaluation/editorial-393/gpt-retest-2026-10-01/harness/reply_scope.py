# /// script
# requires-python = ">=3.12"
# ///
"""Record complete prescribed reply passages and observed extra returned text."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from resource_evidence import REPOSITORY, returned_strings


def main() -> None:
    """An excerpt match proves its read, never the absence of another read."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = args.run
    revision = json.loads((run / "run.json").read_text())["instruction_revision"]
    base = subprocess.check_output(
        [
            "git",
            "show",
            f"{revision}:skills/kntnt/library/references/editorial/base.review.md",
        ],
        cwd=REPOSITORY,
        text=True,
    )
    needle = "A claim removed because the finding named that claim itself"
    start = base.index(needle)
    prefix = base[base.rfind("\n\n", 0, start) + 2 : start].strip()
    fragments = json.loads((run / "resource-evidence.json").read_text())[
        "fragment_observations"
    ]
    reports = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        source = meta["source"]
        if (
            not isinstance(source, dict)
            or "reply" not in source["subagent"]["thread_spawn"]["agent_path"]
        ):
            continue
        extras = []
        for event in events:
            payload = event.get("payload", {})
            if event["type"] != "response_item" or payload.get("type") not in {
                "function_call_output",
                "custom_tool_call_output",
            }:
                continue
            strings = returned_strings(payload.get("output"))
            for name, text in [
                ("base paragraph prefix", prefix),
                ("next delivery heading", "## Refusals"),
            ]:
                if any(text in value for value in strings):
                    extras.append(
                        {
                            "ordinal": event.get("ordinal"),
                            "call_id": payload.get("call_id"),
                            "extra": name,
                            "words": len(text.split()),
                            "exact_returned_passage": text,
                        }
                    )
        reports.append(
            {
                "session": meta["id"],
                "file": str(path.relative_to(run)),
                "complete_required_fragments": [
                    item["fragment"]
                    for item in fragments
                    if item["session"] == meta["id"]
                ],
                "returned_extra_passages": extras,
                "whole_dispatch": "encrypted and unverified",
            }
        )
    (run / "reply-scope-facts.json").write_text(
        json.dumps(
            {
                "method": "Exact complete expected fragments and two known extra passages matched against actual returned native tool material. This targeted audit cannot establish absence of every other possible read; trace-index.json retains all calls for inspection.",
                "checkers": reports,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(json.dumps({"run": run.name, "reply_checkers": len(reports)}))


if __name__ == "__main__":
    main()
