# /// script
# requires-python = ">=3.12"
# ///
"""Capture trace facts for an already completed genre control, without scoring it."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


def text_values(value: Any) -> str:
    """Join actual tool-output strings without Python repr escaping."""

    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(text_values(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(text_values(item) for item in value.values())
    return ""


def main() -> None:
    """Preserve identities, visible resources and filesystem facts for review."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    args = parser.parse_args()
    run = args.case / "redline"
    metadata = json.loads((run / "run.json").read_text())
    genre = args.case.name.rsplit("-", 1)[0]
    sessions = []
    visible = ""
    for session in sorted((run / "native-sessions").rglob("*.jsonl")):
        identities = []
        calls = []
        finals = []
        for line in session.read_text().splitlines():
            event = json.loads(line)
            payload = event.get("payload", {})
            if event.get("type") == "turn_context":
                identities.append(
                    {key: payload.get(key) for key in ("model", "effort")}
                )
            if payload.get("type") == "custom_tool_call_output":
                visible += text_values(payload.get("output", ""))
            if payload.get("type") == "custom_tool_call":
                calls.append(payload.get("input", ""))
            if payload.get("phase") == "final_answer":
                finals.append(
                    "\n".join(
                        block.get("text", "") for block in payload.get("content", [])
                    )
                )
        sessions.append(
            {
                "file": str(session.relative_to(run)),
                "identities": identities,
                "tool_calls": calls,
                "final_messages": finals,
            }
        )
    resources: dict[str, dict[str, Any]] = {}
    for name in (
        "base.md",
        "base.review.md",
        "web-craft.md",
        "web-craft.review.md",
        f"genres/{genre}.md",
        f"genres/{genre}.review.md",
        "anti-slop.md",
        "mechanics.md",
    ):
        content = subprocess.check_output(
            [
                "git",
                "show",
                (
                    f"{metadata['instruction_revision']}:"
                    f"skills/kntnt/library/references/editorial/{name}"
                ),
            ],
            text=True,
        )
        paragraphs = [part.strip() for part in content.split("\n\n") if part.strip()]
        missing = [
            part
            for part in paragraphs
            if part not in visible
            and json.dumps(part, ensure_ascii=False)[1:-1] not in visible
        ]
        resources[name] = {
            "paragraphs": len(paragraphs),
            "missing_paragraphs": missing,
        }
    changes = json.loads((run / "filesystem-changes.json").read_text())
    outside_native_home = {
        kind: [path for path in changes[kind] if not path.startswith("home/.codex/")]
        for kind in ("created", "removed", "changed")
    }
    report = {
        "sessions": sessions,
        "resources_visible_across_sessions": resources,
        "outside_native_home_changes": outside_native_home,
        "note": "Facts only: classify native changes and judge each session separately.",
    }
    (run / "trace-audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "case": args.case.name,
                "sessions": len(sessions),
                "missing_resource_paragraphs": {
                    name: len(data["missing_paragraphs"])
                    for name, data in resources.items()
                },
                "outside_native_home_changes": outside_native_home,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
