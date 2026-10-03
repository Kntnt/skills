# /// script
# requires-python = ">=3.12"
# ///
"""Index retained native events without turning a self-report into evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def audit(run: Path) -> dict[str, Any]:
    """Keep exact trace pointers, actual tool inputs and service interruptions."""
    sessions = []
    service_events = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        calls = []
        outputs = {
            e["payload"].get("call_id"): e
            for e in events
            if e["type"] == "response_item"
            and e["payload"].get("type")
            in {"custom_tool_call_output", "function_call_output"}
        }
        for event in events:
            payload = event.get("payload", {})
            kind = payload.get("type")
            if event["type"] in {"error", "turn.failed"} or (
                event["type"] == "event_msg"
                and kind in {"error", "turn_failed", "turn_aborted"}
            ):
                service_events.append(
                    {
                        "file": str(path.relative_to(run)),
                        "ordinal": event.get("ordinal"),
                        "event": event,
                    }
                )
            if event["type"] != "response_item" or kind not in {
                "custom_tool_call",
                "function_call",
            }:
                continue
            output = outputs.get(payload.get("call_id"))
            rendered = json.dumps(output, ensure_ascii=False) if output else ""
            calls.append(
                {
                    "ordinal": event.get("ordinal"),
                    "timestamp": event["timestamp"],
                    "name": payload.get("name"),
                    "input": payload.get("input", payload.get("arguments")),
                    "output_ordinal": output.get("ordinal") if output else None,
                    "output_contains_truncation_notice": "truncated output" in rendered,
                }
            )
        sessions.append(
            {
                "file": str(path.relative_to(run)),
                "id": meta["id"],
                "source": meta["source"],
                "first_event": events[0]["timestamp"],
                "last_event": events[-1]["timestamp"],
                "lifecycle": [
                    {
                        "ordinal": e.get("ordinal"),
                        "timestamp": e["timestamp"],
                        "type": e["payload"]["type"],
                    }
                    for e in events
                    if e["type"] == "event_msg"
                    and e["payload"].get("type")
                    in {"task_started", "task_complete", "turn_aborted"}
                ],
                "calls": calls,
            }
        )
    # Provider errors may also appear in the native JSON event stream. Ordinary
    # token_count/rate_limits account metadata is deliberately never matched.
    stream_errors = []
    for line in (run / "trace.jsonl").read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") in {"error", "turn.failed"}:
            stream_errors.append(event)
    return {
        "sessions": sessions,
        "native_service_events": service_events,
        "stream_errors": stream_errors,
        "limit": "An input naming a glob or a path is indexed, not credited as a complete individual resource read. Encrypted dispatch briefs remain unverified.",
    }


def main() -> None:
    """Write an index beside the immutable retained native rollouts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    report = audit(args.run)
    (args.run / "trace-index.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "run": args.run.name,
                "sessions": len(report["sessions"]),
                "native_service_events": len(report["native_service_events"]),
                "stream_errors": len(report["stream_errors"]),
            }
        )
    )


if __name__ == "__main__":
    main()
