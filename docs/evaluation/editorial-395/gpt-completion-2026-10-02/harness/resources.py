"""Retain resource-content observations from actual native tool returns."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def strings(value: Any) -> list[str]:
    """Unwrap structured tool returns; never assume a read request succeeded."""
    if isinstance(value, dict):
        return [part for child in value.values() for part in strings(child)]
    if isinstance(value, list):
        return [part for child in value for part in strings(child)]
    if not isinstance(value, str):
        return []
    result = [value]
    pending = [value]
    seen = {value}
    for _ in range(4):
        next_layer = []
        for item in pending:
            for literal in re.findall(r'"(?:\\.|[^"\\])*"', item):
                try:
                    decoded = json.loads(literal)
                except json.JSONDecodeError:
                    continue
                if isinstance(decoded, str) and decoded not in seen:
                    seen.add(decoded)
                    result.append(decoded)
                    next_layer.append(decoded)
        pending = next_layer
    for line in value.splitlines():
        if line.startswith(("{", "[")):
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(parsed, str):
                result.extend(strings(parsed))
    return result


def inspect(output: Path, repository: Path, revision: str) -> None:
    """Compare exact frozen resources with returned content and line coverage."""
    observations = {}
    installed = json.loads((output / "inventory-before.json").read_text())
    resources = {}
    for key in installed:
        if not key.startswith("work/.agents/skills/") or not key.endswith(".md"):
            continue
        path = key.removeprefix("work/.agents/")
        repository_path = path
        if path.startswith(("skills/write/", "skills/redline/", "skills/proofread/")):
            repository_path = "skills/editorial/" + path.removeprefix("skills/")
        resources[path] = subprocess.check_output(
            ["git", "show", f"{revision}:{repository_path}"], cwd=repository, text=True
        ).rstrip()
    for trace in (output / "native-sessions").rglob("*.jsonl"):
        events = [json.loads(line) for line in trace.read_text().splitlines()]
        metadata = next(e["payload"] for e in events if e["type"] == "session_meta")
        returned = "\n".join(
            part
            for event in events
            if event["type"] == "response_item"
            and event["payload"].get("type")
            in {"function_call_output", "custom_tool_call_output"}
            for part in strings(event["payload"].get("output"))
        )
        observed = []
        language_scopes = []
        for path, content in resources.items():
            full = content in returned
            nonblank = [line for line in content.splitlines() if line.strip()]
            missing = [line for line in nonblank if line not in returned]
            if full or not missing:
                observed.append(
                    {
                        "path": ".agents/" + path,
                        "full_resource_text_in_returned_output": full,
                        "all_nonblank_lines_visible_across_returns": not missing,
                        "missing_nonblank_lines": missing if not full else [],
                    }
                )
            if "/references/languages/" in path and not path.endswith("README.md"):
                sections = re.split(
                    r"(?m)^## (Composition|Review|Anti-slop|Mechanics)\n", content
                )
                for index in range(1, len(sections), 2):
                    scope_content = sections[index + 1].strip()
                    if scope_content and scope_content in returned:
                        language_scopes.append(
                            {
                                "path": ".agents/" + path,
                                "scope": sections[index].lower(),
                                "complete_scope_content_in_returned_output": True,
                            }
                        )
        observations[metadata["id"]] = {
            "source": metadata.get("source"),
            "resources": observed,
            "language_scopes": language_scopes,
            "limit": "Line coverage across separate returns does not prove order or exact encrypted dispatch scope.",
        }
    (output / "resource-observations.json").write_text(
        json.dumps(observations, indent=2, ensure_ascii=False) + "\n"
    )


def main() -> None:
    """Inspect explicit retained invocations only."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outputs", nargs="+", type=Path)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    for output in args.outputs:
        inspect(output, args.repository, args.revision)


if __name__ == "__main__":
    main()
