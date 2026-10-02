"""Index preserved native facts without substituting them for semantic judgement."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    """Read one retained JSON artifact."""
    return json.loads(path.read_text())


def captured(output: Path, suffix: str) -> bytes | None:
    """Return the last external capture of a named private file."""
    matches = [
        entry
        for entry in read_json(output / "file-versions.json")
        if entry["path"].endswith("/" + suffix)
    ]
    if not matches:
        return None
    return (output / "file-versions" / str(matches[-1]["capture"])).read_bytes()


def inspect(output: Path) -> dict[str, Any]:
    """Extract lifecycle, identity, filesystem and byte-equality observations."""
    before = read_json(output / "inventory-before.json")
    after = read_json(output / "inventory-after.json")
    run = read_json(output / "run.json")
    result = read_json(output / "result.json")
    input_path = "work/" + run["input_name"]
    sessions = []
    calls = []
    errors = []
    for trace in sorted((output / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in trace.read_text().splitlines()]
        metadata = next(e["payload"] for e in events if e["type"] == "session_meta")
        identity = sorted(
            {
                (e["payload"].get("model"), e["payload"].get("effort"))
                for e in events
                if e["type"] == "turn_context"
            }
        )
        completed = any(
            e["type"] == "event_msg" and e["payload"].get("type") == "task_complete"
            for e in events
        )
        sessions.append(
            {
                "id": metadata["id"],
                "source": metadata.get("source"),
                "cli_version": metadata.get("cli_version"),
                "seats": identity,
                "task_complete": completed,
                "trace": str(trace.relative_to(output)),
            }
        )
        for line_number, event in enumerate(events, start=1):
            payload = event.get("payload", {})
            if event["type"] == "response_item" and payload.get("type") in {
                "function_call",
                "custom_tool_call",
            }:
                calls.append(
                    {
                        "session": metadata["id"],
                        "line": line_number,
                        "name": payload.get("name"),
                        "arguments": payload.get("arguments", payload.get("input")),
                        "call_id": payload.get("call_id"),
                    }
                )
            if event["type"] == "event_msg" and payload.get("type") in {
                "error",
                "turn.failed",
                "turn_aborted",
            }:
                errors.append(
                    {"session": metadata["id"], "line": line_number, "payload": payload}
                )
    for line_number, line in enumerate(
        (output / "trace.jsonl").read_text().splitlines(), start=1
    ):
        event = json.loads(line)
        if event.get("type") in {"error", "turn.failed"}:
            errors.append(
                {"trace": "trace.jsonl", "line": line_number, "payload": event}
            )

    native_response_path = output / "response.txt"
    native_response = (
        native_response_path.read_bytes() if native_response_path.exists() else None
    )
    response = captured(output, "observer-response.md")
    delivered_file = output / "delivered.md"
    delivered = delivered_file.read_bytes() if delivered_file.exists() else None
    mechanical_input = captured(output, "mechanical-pass-input.md")
    mechanical_output = captured(output, "mechanical-pass-output.md")
    scratch = {key: value for key, value in after.items() if key.startswith("scratch/")}
    installed_keys = {key for key in before | after if key.startswith("work/.agents/")}
    work_changes = {
        key: {"before": before.get(key), "after": after.get(key)}
        for key in before | after
        if key.startswith("work/") and before.get(key) != after.get(key)
    }
    findings = {
        "input_sha256": hashlib.sha256(
            (output / "supplied-input.md").read_bytes()
        ).hexdigest(),
        "input_preserved": before.get(input_path) == after.get(input_path),
        "input_stat_preserved": (
            read_json(output / "input-stat.json")["before"]
            == read_json(output / "input-stat.json")["after"]
        ),
        "installed_files_unchanged": all(
            before.get(key) == after.get(key) for key in installed_keys
        ),
        "result": result,
        "seats": sessions,
        "native_errors": errors,
        "native_tool_calls": len(calls),
        "observer_response_matches_native": (
            response.rstrip() == native_response.rstrip()
            if response is not None and native_response is not None
            else None
        ),
        "delivered_substring_native": delivered in native_response
        if delivered is not None and native_response is not None
        else None,
        "mechanical_input_equals_output": (
            mechanical_input == mechanical_output
            if mechanical_output is not None
            else None
        ),
        "mechanical_output_equals_delivered": (
            mechanical_output == delivered
            if mechanical_output is not None and delivered is not None
            else None
        ),
        "mechanical_output_equals_supplied_input": (
            mechanical_output == (output / "supplied-input.md").read_bytes()
            if mechanical_output is not None
            else None
        ),
        "scratch_files": scratch,
        "work_changes": work_changes,
        "limits": [
            "Encrypted dispatch text is not decoded; actual child reads establish only visible scope.",
            "A file-read command must be checked against its returned output for truncation or failure.",
            "External captures poll at 100 ms; an uncaptured temporary version is not asserted present.",
            "No semantic or resource-loading pass follows merely from a tool count or task completion.",
        ],
    }
    (output / "checks.json").write_text(
        json.dumps(findings, indent=2, ensure_ascii=False) + "\n"
    )
    (output / "native-tool-index.json").write_text(
        json.dumps(calls, indent=2, ensure_ascii=False) + "\n"
    )
    return findings


def main() -> None:
    """Audit only explicit completed output directories supplied by the evaluator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outputs", nargs="+", type=Path)
    args = parser.parse_args()
    for output in args.outputs:
        facts = inspect(output)
        print(
            json.dumps(
                {
                    "output": str(output),
                    "returncode": facts["result"]["returncode"],
                    "errors": len(facts["native_errors"]),
                    "sessions": len(facts["seats"]),
                    "all_tasks_complete": all(
                        s["task_complete"] for s in facts["seats"]
                    ),
                    "input_preserved": facts["input_preserved"],
                    "install_unchanged": facts["installed_files_unchanged"],
                    "mechanical_delivery_equal": facts[
                        "mechanical_output_equals_delivered"
                    ],
                }
            )
        )


if __name__ == "__main__":
    main()
