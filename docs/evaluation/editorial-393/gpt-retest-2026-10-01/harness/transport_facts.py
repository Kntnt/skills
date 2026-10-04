# /// script
# requires-python = ">=3.12"
# ///
"""Preserve exact closing-pass and inventory facts, without semantic scoring."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from resource_evidence import returned_strings


def main() -> None:
    """Link captured full files to actual parent/child returned tool material."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = args.run
    facts = json.loads((run / "deterministic-facts.json").read_text())
    captures = json.loads((run / "file-versions.json").read_text())
    sessions: list[dict[str, Any]] = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        role = (
            "parent"
            if meta["source"] == "exec"
            else meta["source"]["subagent"]["thread_spawn"]["agent_path"]
        )
        outputs = []
        for event in events:
            payload = event.get("payload", {})
            if event["type"] == "response_item" and payload.get("type") in {
                "function_call_output",
                "custom_tool_call_output",
            }:
                outputs.append(
                    {
                        "ordinal": event.get("ordinal"),
                        "call_id": payload.get("call_id"),
                        "strings": returned_strings(payload.get("output")),
                    }
                )
        sessions.append(
            {
                "id": meta["id"],
                "file": str(path.relative_to(run)),
                "role": role,
                "outputs": outputs,
            }
        )
    closing_files = []
    for capture in captures:
        file_path = Path(capture["path"])
        if not (
            "mechanical" in str(file_path.parent)
            and file_path.name
            in {"mechanical-input.md", "mechanical-output.md", "input.md", "output.md"}
        ):
            continue
        contents = (run / "file-versions" / capture["capture"]).read_bytes()
        sha = hashlib.sha256(contents).hexdigest()
        matches = []
        for session in sessions:
            for output in session["outputs"]:
                if any(contents.decode() in s for s in output["strings"]):
                    matches.append(
                        {
                            **{k: session[k] for k in ["id", "file", "role"]},
                            "ordinal": output["ordinal"],
                            "call_id": output["call_id"],
                        }
                    )
        closing_files.append(
            {
                **capture,
                "capture_hash_valid": sha == capture["sha256"],
                "matches_delivered_artifact": sha == facts["artifact"]["sha256"],
                "complete_bytes_returned_by_native_tool": matches,
            }
        )
    before = json.loads((run / "inventory-before.json").read_text())
    after = json.loads((run / "inventory-after.json").read_text())
    changes = {
        path: {"before": before.get(path), "after": after.get(path)}
        for path in sorted(before.keys() | after.keys())
        if before.get(path) != after.get(path)
    }
    report = {
        "method": "Exact externally captured file bytes found in actual returned native tool material. A missing match is a trace gap, never proof that a file was not read. Full writable-root inventory differences include native harness home and cache state, separately from work/scratch effects.",
        "closing_pass_files": closing_files,
        "inventory_changes": changes,
        "work_or_scratch_effects": {
            path: value
            for path, value in changes.items()
            if path.startswith(("work/", "scratch/"))
        },
    }
    (run / "transport-facts.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "run": run.name,
                "closing_files": len(closing_files),
                "work_scratch_changes": len(report["work_or_scratch_effects"]),
            }
        )
    )


if __name__ == "__main__":
    main()
