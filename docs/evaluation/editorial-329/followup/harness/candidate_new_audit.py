# /// script
# requires-python = ">=3.12"
# ///
"""Extract observable native facts for completed candidate runs, without scoring."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT: Path = Path("/Users/thomas/Projects/skills")


def strings(value: Any) -> list[str]:
    """Expose nested tool text while preserving its original serialized form."""
    if isinstance(value, dict):
        return [text for item in value.values() for text in strings(item)]
    if isinstance(value, list):
        return [text for item in value for text in strings(item)]
    if not isinstance(value, str):
        return []

    # Native tool output sometimes serializes a second JSON object as text.
    try:
        decoded = json.loads(value)
    except (ValueError, TypeError):
        return [value]
    return [value, *strings(decoded)] if not isinstance(decoded, str) else [value]


def audit(run: Path) -> dict[str, Any]:
    """Preserve source reads, actual identity, delegation and filesystem facts."""

    # Read only the completed evaluator captures, never another family's data.
    metadata = json.loads((run / "run.json").read_text())
    supplied = (run / "supplied-input.md").read_text()
    artifact_path = run / "artifact.md"
    artifact = artifact_path.read_text() if artifact_path.is_file() else None
    prose = (
        re.sub(r"\A---\n.*?\n---\n\n?", "", artifact, count=1, flags=re.DOTALL)
        if artifact
        else None
    )
    sessions: list[dict[str, Any]] = []
    for session in sorted((run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in session.read_text().splitlines()]
        observed: dict[str, Any] = {"file": str(session.relative_to(run))}
        outputs: list[str] = []
        calls: list[str] = []
        identities: list[dict[str, str]] = []
        spawns: list[dict[str, Any]] = []
        for event in events:
            payload = event.get("payload", {})
            if event["type"] == "session_meta":
                observed["session"] = {
                    key: payload.get(key)
                    for key in ("id", "parent_thread_id", "source")
                }
            if event["type"] == "turn_context":
                identities.append(
                    {key: payload.get(key) for key in ("model", "effort")}
                )
            if payload.get("type") in (
                "custom_tool_call_output",
                "function_call_output",
            ):
                outputs.extend(strings(payload.get("output", "")))
            if payload.get("type") == "custom_tool_call":
                calls.append(payload.get("input", ""))
            if payload.get("type") == "function_call" and payload.get(
                "name", ""
            ).endswith("spawn_agent"):
                arguments = json.loads(payload["arguments"])
                spawns.append(
                    {
                        key: arguments.get(key)
                        for key in (
                            "task_name",
                            "fork_turns",
                            "model",
                            "reasoning_effort",
                        )
                    }
                )
                spawns[-1]["message_encrypted"] = arguments.get(
                    "message", ""
                ).startswith("gAAAA")

        # Paragraph visibility is evidence of loading, not a semantic verdict.
        visible = "\n".join(outputs)
        observed.update(identities=identities, spawns=spawns, calls=calls)
        observed["complete_supplied_input_visible"] = supplied.strip() in visible
        observed["delivered_prose_visible"] = (
            prose.rstrip("\n") in visible if prose else None
        )
        resources: dict[str, int] = {}
        paths = [
            "base.md",
            "base.review.md",
            "web-craft.md",
            "web-craft.review.md",
            "anti-slop.md",
            "mechanics.md",
        ]
        for genre in (
            "opinion",
            "case-study",
            "article",
            "column",
            "web-copy",
            "general",
        ):
            paths.append(f"genres/{genre}.md")
            if genre != "general":
                paths.append(f"genres/{genre}.review.md")
        for relative in paths:
            resource = subprocess.check_output(
                [
                    "git",
                    "show",
                    f"{metadata['instruction_revision']}:skills/kntnt/library/references/editorial/{relative}",
                ],
                cwd=ROOT,
                text=True,
            )
            paragraphs = [
                part.strip() for part in resource.split("\n\n") if part.strip()
            ]
            resources[relative] = sum(part not in visible for part in paragraphs)
        observed["missing_resource_paragraphs"] = resources
        sessions.append(observed)

    # Keep complete parent-visible reports separately for convenient inspection.
    reports: list[str] = []
    for line in (run / "trace.jsonl").read_text().splitlines():
        event = json.loads(line)
        item = event.get("item", {})
        if (
            event["type"] == "item.completed"
            and item.get("type") == "command_execution"
        ):
            command = item.get("command", "")
            if re.search(r"\bcat\b|\.read_text\(", command) and re.search(
                r"report|finding", command, re.IGNORECASE
            ):
                output = item.get("aggregated_output", "")
                name = f"observed-report-{len(reports) + 1}.md"
                (run / name).write_text(output)
                reports.append(name)
    changes = json.loads((run / "filesystem-changes.json").read_text())
    report = {
        "sessions": sessions,
        "parent_visible_reports": reports,
        "outside_native_home_changes": {
            kind: {
                path: details
                for path, details in changes[kind].items()
                if not path.startswith("home/.codex/")
            }
            for kind in ("created", "removed", "changed")
        },
        "authentication_changed": changes["authentication_changed"],
        "note": "Observed facts only. Encrypted dispatch alone cannot establish full prompt or draft transport. Delivered prose visibility removes leading metadata and final newline separators only; manually confirm the relevant draft read and last approving checker.",
    }
    (run / "native-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    return {
        "run": str(run.relative_to(ROOT)),
        "sessions": len(sessions),
        "spawns": [spawn for session in sessions for spawn in session["spawns"]],
        "reports": reports,
        "outside_native_home_changes": {
            kind: list(values)
            for kind, values in report["outside_native_home_changes"].items()
        },
    }


def main() -> None:
    """Audit the explicitly selected completed runs and print bounded summaries."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, nargs="+")
    args = parser.parse_args()
    for run in args.runs:
        print(json.dumps(audit(run.resolve()), ensure_ascii=False))


if __name__ == "__main__":
    main()
