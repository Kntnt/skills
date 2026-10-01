# /// script
# requires-python = ">=3.12"
# ///
"""Identify complete resource text actually returned by retained native tools."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[5]


def returned_strings(value: Any, depth: int = 0) -> list[str]:
    """Unwrap native text/JSON wrappers, never decrypt or execute their content."""
    if depth > 12:
        return []
    if isinstance(value, dict):
        return [s for v in value.values() for s in returned_strings(v, depth + 1)]
    if isinstance(value, list):
        return [s for v in value for s in returned_strings(v, depth + 1)]
    if not isinstance(value, str):
        return []
    strings = [value]
    candidates = [value]
    # A batched exec may return several complete JSON lines in one text block,
    # even when a later line in that same block was truncated.
    candidates.extend(
        line for line in value.splitlines() if line.startswith(("{", "["))
    )
    # UV may put its harmless installation line before a resolver JSON object.
    if "{" in value:
        candidates.append(value[value.index("{") :])
    for candidate in candidates:
        try:
            decoded = json.loads(candidate)
        except json.JSONDecodeError:
            try:
                # A complete resolver object can precede an EXIT/status line.
                # raw_decode still refuses any incomplete or truncated object.
                decoded, _ = json.JSONDecoder().raw_decode(candidate.lstrip())
            except json.JSONDecodeError:
                continue
        if decoded != value:
            strings.extend(returned_strings(decoded, depth + 1))
    return strings


def main() -> None:
    """Credit only the complete committed text, with its native event pointer."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    revision = json.loads((args.run / "run.json").read_text())["instruction_revision"]
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", revision, "skills"],
        cwd=REPOSITORY,
        text=True,
    ).splitlines()
    resources = {}
    for name in paths:
        if not name.endswith(".md") or not name.startswith(
            ("skills/kntnt/library/references/", "skills/editorial/")
        ):
            continue
        content = subprocess.check_output(
            ["git", "show", f"{revision}:{name}"], cwd=REPOSITORY
        )
        resources[name] = content
    observed = []
    for path in sorted((args.run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        seen = set()
        scope_seen = set()
        for event in events:
            payload = event.get("payload", {})
            if event["type"] != "response_item" or payload.get("type") not in {
                "custom_tool_call_output",
                "function_call_output",
            }:
                continue
            strings = returned_strings(payload.get("output"))
            pointer = {
                "session": meta["id"],
                "file": str(path.relative_to(args.run)),
                "ordinal": event.get("ordinal"),
                "call_id": payload.get("call_id"),
            }
            for name, content in resources.items():
                text = content.decode().strip()
                if name not in seen and text and any(text in s for s in strings):
                    seen.add(name)
                    observed.append(
                        {
                            **pointer,
                            "resource": name,
                            "complete_returned_content": True,
                            "words": len(content.decode().split()),
                            "sha256": hashlib.sha256(content).hexdigest(),
                        }
                    )
            for text in strings:
                try:
                    decoded, _ = json.JSONDecoder().raw_decode(text[text.index("{") :])
                except (ValueError, json.JSONDecodeError):
                    continue
                if not isinstance(decoded, dict) or not isinstance(
                    decoded.get("scopes"), dict
                ):
                    continue
                for scope, data in decoded["scopes"].items():
                    key = (decoded.get("code"), scope)
                    if key in scope_seen or not isinstance(data, dict):
                        continue
                    content = data.get("content")
                    if not isinstance(content, str):
                        continue
                    scope_seen.add(key)
                    observed.append(
                        {
                            **pointer,
                            "language": decoded.get("code"),
                            "scope": scope,
                            "source": data.get("source"),
                            "complete_returned_content": True,
                            "words": len(content.split()),
                            "sha256": hashlib.sha256(content.encode()).hexdigest(),
                        }
                    )
    report = {
        "revision": revision,
        "method": "Unique complete returned resource text per native session; whitespace word count. This is observed resource volume, not a comprehension verdict. Absent matches may reflect wrappers, truncation or partial reads and are gaps, not automatic failures. Mandatory-set costing is a separate contract comparison.",
        "observations": observed,
    }
    (args.run / "resource-evidence.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"run": args.run.name, "complete_matches": len(observed)}))


if __name__ == "__main__":
    main()
