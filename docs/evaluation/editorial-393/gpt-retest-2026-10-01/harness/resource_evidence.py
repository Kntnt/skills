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
    delivery_name = "skills/kntnt/library/references/delivery.md"
    delivery_text = resources[delivery_name].decode()
    truth_start = delivery_text.index("## The truth of a report about the text")
    truth_end = delivery_text.index("\n## ", truth_start + 1)
    review_name = "skills/kntnt/library/references/editorial/base.review.md"
    review_text = resources[review_name].decode()
    claim_start = review_text.index(
        "A claim removed because the finding named that claim itself"
    )
    claim_end = review_text.index("\n\n", claim_start)
    fragments = {
        "delivery-truth": (delivery_name, delivery_text[truth_start:truth_end].strip()),
        "base-claim-account": (review_name, review_text[claim_start:claim_end].strip()),
    }
    session_events = {
        path: [json.loads(line) for line in path.read_text().splitlines()]
        for path in sorted((args.run / "native-sessions").rglob("*.jsonl"))
    }
    # A source checker can receive the resolved guidance as complete plain text,
    # rather than call the resolver again. Establish its bytes only from actual
    # complete resolver objects in this run, then match actual returned material.
    known_scopes = {}
    for events in session_events.values():
        for event in events:
            payload = event.get("payload", {})
            if event["type"] != "response_item" or payload.get("type") not in {
                "custom_tool_call_output",
                "function_call_output",
            }:
                continue
            for text in returned_strings(payload.get("output")):
                try:
                    decoded, _ = json.JSONDecoder().raw_decode(text[text.index("{") :])
                except (ValueError, json.JSONDecodeError):
                    continue
                if not isinstance(decoded, dict) or not isinstance(
                    decoded.get("scopes"), dict
                ):
                    continue
                for scope, data in decoded["scopes"].items():
                    if isinstance(data, dict) and isinstance(data.get("content"), str):
                        known_scopes[(decoded.get("code"), scope)] = data
    observed = []
    fragment_observed = []
    for path, events in session_events.items():
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        seen = set()
        scope_seen = set()
        fragment_seen = set()
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
            for name, (resource, content) in fragments.items():
                if name not in fragment_seen and any(content in s for s in strings):
                    fragment_seen.add(name)
                    fragment_observed.append(
                        {
                            **pointer,
                            "fragment": name,
                            "resource": resource,
                            "complete_returned_fragment": True,
                            "words": len(content.split()),
                            "sha256": hashlib.sha256(content.encode()).hexdigest(),
                        }
                    )
            for key, data in known_scopes.items():
                content = data["content"]
                if (
                    key in scope_seen
                    or not content
                    or not any(content in text for text in strings)
                ):
                    continue
                scope_seen.add(key)
                observed.append(
                    {
                        **pointer,
                        "language": key[0],
                        "scope": key[1],
                        "source": data.get("source"),
                        "complete_returned_content": True,
                        "words": len(content.split()),
                        "sha256": hashlib.sha256(content.encode()).hexdigest(),
                        "presentation": "exact resolved guidance returned as plain text",
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
        "fragment_observations": fragment_observed,
        "fragment_note": "Selected reply-check passages are recorded separately. Their words must not be added again where the same session already has the complete containing resource credited. A complete fragment match does not prove that nothing else was read.",
    }
    (args.run / "resource-evidence.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"run": args.run.name, "complete_matches": len(observed)}))


if __name__ == "__main__":
    main()
