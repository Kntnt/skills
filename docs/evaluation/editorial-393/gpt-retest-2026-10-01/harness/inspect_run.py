# /// script
# requires-python = ">=3.12"
# ///
"""Derive inspectable transport and identity facts from one native run.

The report makes no semantic verdict and never treats a no-change status as
text. Fenced response bytes or the explicit captured file are the artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def digest(contents: bytes) -> str:
    """Represent exact artifact bytes without normalising whitespace."""
    return hashlib.sha256(contents).hexdigest()


def inspect(run: Path) -> dict[str, Any]:
    """Preserve the facts separately from later language judgements."""

    # Only a complete result can be read as a finished filesystem inventory.
    result = json.loads((run / "result.json").read_text())
    supplied = (run / "supplied-input.md").read_bytes()
    response_path = run / "response.txt"
    response = response_path.read_text() if response_path.exists() else ""
    facts: dict[str, Any] = {"result": result, "input_sha256": digest(supplied)}

    # Extract only a complete outer artifact fence, preserving its inner bytes.
    blocks = list(
        re.finditer(r"(?m)^(`{3,})(markdown|html|text)\n([\s\S]*?)^\1\s*$", response)
    )
    delivered = (
        (run / "captured-output.md").read_bytes()
        if (run / "captured-output.md").exists()
        else blocks[0].group(3).encode()
        if len(blocks) == 1
        else None
    )
    facts["artifact"] = {
        "fenced_artifact_count": len(blocks),
        "present": delivered is not None,
        "source": "explicit-file"
        if (run / "captured-output.md").exists()
        else "response-fence"
        if delivered is not None
        else "none",
        "sha256": digest(delivered) if delivered is not None else None,
        "input_identical": delivered == supplied if delivered is not None else None,
    }
    if delivered is not None:
        (run / "delivered.md").write_bytes(delivered)

    # Keep every parent/child identity and relationship the native trace exposes.
    identities = []
    encrypted_calls = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(
            event["payload"] for event in events if event["type"] == "session_meta"
        )
        contexts = [
            event["payload"] for event in events if event["type"] == "turn_context"
        ]
        identities.append(
            {
                "file": str(path.relative_to(run)),
                "id": meta["id"],
                "source": meta["source"],
                "seats": sorted(
                    {(context["model"], context["effort"]) for context in contexts}
                ),
            }
        )
        for event in events:
            payload = event.get("payload", {})
            if (
                event["type"] == "response_item"
                and payload.get("type") == "function_call"
                and payload.get("name") in {"spawn_agent", "send_message"}
            ):
                arguments = json.loads(payload["arguments"])
                if str(arguments.get("message", "")).startswith("gAAAA"):
                    encrypted_calls.append(
                        {
                            "session": meta["id"],
                            "name": payload["name"],
                            "call_id": payload.get("call_id"),
                            "note": "dispatch message encrypted; use actual child reads rather than infer its complete brief",
                        }
                    )
    facts["identities"] = identities
    facts["encrypted_dispatches"] = encrypted_calls
    facts["all_recorded_seats_match"] = all(
        identity["seats"] == [("gpt-6.1-sol", "xhigh")] for identity in identities
    )

    # Identify exact matching transient files without guessing their workflow role.
    captures = json.loads((run / "file-versions.json").read_text())
    facts["artifact_matches_captures"] = [
        capture
        for capture in captures
        if delivered is not None and capture["sha256"] == digest(delivered)
    ]
    before = json.loads((run / "inventory-before.json").read_text())
    after = json.loads((run / "inventory-after.json").read_text())
    input_name = json.loads((run / "run.json").read_text())["input_name"]
    facts["source_inventory_unchanged"] = before.get(f"work/{input_name}") == after.get(
        f"work/{input_name}"
    )
    staged = {
        path: value
        for path, value in before.items()
        if path.startswith(("export/", "work/.agents/"))
    }
    facts["staged_install_unchanged"] = all(
        after.get(path) == value for path, value in staged.items()
    ) and not any(
        path.startswith(("export/", "work/.agents/"))
        for path in after.keys() - before.keys()
    )
    facts["work_created"] = {
        path: after[path]
        for path in after.keys() - before.keys()
        if path.startswith("work/")
    }
    facts["work_removed"] = {
        path: before[path]
        for path in before.keys() - after.keys()
        if path.startswith("work/")
    }
    facts["work_changed"] = {
        path: {"before": before[path], "after": after[path]}
        for path in before.keys() & after.keys()
        if path.startswith("work/") and before[path] != after[path]
    }
    return facts


def main() -> None:
    """Write facts beside a completed run without touching staged model files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    facts = inspect(args.run)
    (args.run / "deterministic-facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "run": args.run.name,
                "artifact": facts["artifact"],
                "seats_match": facts["all_recorded_seats_match"],
            }
        )
    )


if __name__ == "__main__":
    main()
