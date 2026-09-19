# /// script
# requires-python = ">=3.12"
# ///
"""Extract observable identity, loading and filesystem facts without judging prose."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT: Path = Path("/Users/thomas/Projects/skills")


def text_values(value: Any) -> str:
    """Decode nested tool envelopes without discarding the original strings."""
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return value
        return value + "\n" + (text_values(decoded) if decoded != value else "")
    if isinstance(value, list):
        return "\n".join(text_values(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(text_values(item) for item in value.values())
    return ""


def main() -> None:
    """Preserve machine-observable facts; semantic judgement stays separate."""

    # Read only the named completed invocation and immutable product resources.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--genre")
    args = parser.parse_args()
    run = args.run
    config = json.loads((run / "run.json").read_text())
    sessions: list[dict[str, Any]] = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        entry: dict[str, Any] = {
            "file": str(path.relative_to(run)),
            "identities": [],
            "calls": [],
            "visible_output": "",
            "finals": [],
        }
        for line in path.read_text().splitlines():
            event = json.loads(line)
            payload = event.get("payload", {})
            if event.get("type") == "session_meta":
                entry["id"] = payload.get("id")
                entry["parent_thread_id"] = payload.get("parent_thread_id")
            if event.get("type") == "turn_context":
                entry["identities"].append(
                    {key: payload.get(key) for key in ("model", "effort")}
                )
            if payload.get("type") in ("function_call", "custom_tool_call"):
                entry["calls"].append(
                    {
                        "name": payload.get("name"),
                        "input": payload.get("arguments", payload.get("input")),
                    }
                )
            if payload.get("type") in (
                "function_call_output",
                "custom_tool_call_output",
            ):
                entry["visible_output"] += text_values(payload.get("output", "")) + "\n"
            if payload.get("phase") == "final_answer":
                entry["finals"].append(text_values(payload.get("content", [])))
        sessions.append(entry)

    # Check exact resource paragraphs in visible outputs, without inferring reads.
    genre = args.genre or run.parent.name.split("-en_")[0].split("-sv")[0]
    names = ["base.md", "web-craft.md", f"genres/{genre}.md"]
    if run.name == "redline":
        names += [
            "base.review.md",
            "web-craft.review.md",
            f"genres/{genre}.review.md",
            "anti-slop.md",
            "mechanics.md",
        ]
    for entry in sessions:
        entry["missing_resource_paragraphs"] = {}
        for name in names:
            content = subprocess.check_output(
                [
                    "git",
                    "show",
                    f"{config['instruction_revision']}:skills/kntnt/library/references/editorial/{name}",
                ],
                cwd=ROOT,
                text=True,
            )
            paragraphs = [
                part.strip() for part in content.split("\n\n") if part.strip()
            ]
            entry["missing_resource_paragraphs"][name] = [
                part for part in paragraphs if part not in entry["visible_output"]
            ]

    # Preserve readable checker reports and explicit complete source reads.
    if run.name == "write":
        source = (run / "supplied-input.md").read_text().strip()
        for entry in sessions:
            entry["complete_source_visible"] = source in entry["visible_output"]
        reports: list[dict[str, str]] = []
        for line in (run / "trace.jsonl").read_text().splitlines():
            item = json.loads(line).get("item", {})
            command = item.get("command", "")
            if (
                item.get("status") == "completed"
                and "cat " in command
                and "report.md" in command
            ):
                reports.append(
                    {"command": command, "output": item.get("aggregated_output", "")}
                )
        (run / "source-check-reports.json").write_text(
            json.dumps(reports, ensure_ascii=False, indent=2) + "\n"
        )

    # Keep every changed path and separate native state from Skill effects.
    changes = json.loads((run / "filesystem-changes.json").read_text())
    outside_native = {
        kind: {
            path: data
            for path, data in changes[kind].items()
            if not path.startswith("home/.codex/")
        }
        for kind in ("created", "removed", "changed")
    }
    report = {
        "sessions": sessions,
        "outside_native_home_changes": outside_native,
        "authentication_changed": changes["authentication_changed"],
        "note": "Observable facts only. Encrypted dispatches do not establish exact supplied draft bytes.",
    }
    (run / "trace-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "run": str(run),
                "sessions": len(sessions),
                "outside_native_home_changes": outside_native,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
