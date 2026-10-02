# /// script
# requires-python = ">=3.12"
# ///
"""Build identity-blind judge inputs from complete native capture evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCRATCH = Path(
    "/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-observation-mgldfmax"
)


def redact(text: str) -> str:
    """Remove producer identity, preserving all supplied source and assertions."""
    return re.sub(r"(?:gpt|claude)-[\w.]+", "[producer identity withheld]", text)


def draft_from_response(response: str) -> str | None:
    """Keep the exact fenced Text Artifact rather than reformatting it."""
    blocks = re.findall(
        r"^```[^\n]*\n(.*?)^```[ \t]*$", response, re.MULTILINE | re.DOTALL
    )
    artifacts = [block for block in blocks if "kntnt:" in block or "# Lervik" in block]
    return artifacts[0] if len(artifacts) == 1 else None


def main() -> None:
    """Write a neutral packet while retaining raw evidence separately."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=int)
    args = parser.parse_args()
    run = SCRATCH / f"sample-{args.index:02d}"
    destination = SCRATCH / f"judge-input-{args.index:02d}.md"
    response = (run / "response.txt").read_text()
    source = (run / "supplied-input.md").read_text()
    draft = draft_from_response(response)
    if draft is not None:
        (run / "draft.md").write_text(draft)

    # Compare every captured draft version with the delivered prose, exactly.
    def prose(text: str) -> str:
        """Remove only the allowed metadata wrapper, never prose whitespace."""
        if text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            if end >= 0:
                text = text[end + 5 :]
                text = text.removeprefix("\n")
        return text

    byte_comparisons: list[dict[str, Any]] = []
    for item in json.loads((run / "file-versions.json").read_text()):
        if "draft" not in Path(item["path"]).name:
            continue
        content = (run / "file-versions" / item["capture"]).read_text()
        byte_comparisons.append(
            {
                "path": item["path"],
                "capture": item["capture"],
                "time": item["time"],
                "sha256": item["sha256"],
                "prose_sha256": hashlib.sha256(prose(content).encode()).hexdigest(),
                "exact_delivered_prose_match": draft is not None
                and prose(content) == prose(draft),
            }
        )
    comparison_evidence = {
        "artifact_extracted": draft is not None,
        "delivered_prose_sha256": hashlib.sha256(prose(draft).encode()).hexdigest()
        if draft is not None
        else None,
        "draft_versions": byte_comparisons,
        "note": "Identify the final comparison's actual read path/version from child trace; a matching earlier draft alone does not establish V3.",
    }
    (run / "byte-comparisons.json").write_text(
        json.dumps(comparison_evidence, indent=2) + "\n"
    )
    packet = [
        "# Complete supplied source\n\n",
        source,
        "\n# Delivered user response\n\n",
        response,
        "\n# Extracted Text Artifact\n\n",
        draft or "Not extracted: judge from the complete response.\n",
    ]
    snapshots = json.loads((run / "file-versions.json").read_text())
    for item in snapshots:
        if item["path"] in {"work/source.md", "work/AGENTS.md"}:
            continue
        file = run / "file-versions" / item["capture"]
        packet.extend(
            [
                f"\n# Captured file version: {item['path']}\n\n",
                f"Capture time {item['time']}; SHA256 {item['sha256']}\n\n",
                file.read_text(),
            ]
        )
    roles: dict[str, Any] = {}
    seats: list[dict[str, Any]] = []
    tool_lines: list[str] = []
    for path in sorted((run / "native-sessions").rglob("*.jsonl")):
        session = path.name
        for line in path.read_text().splitlines():
            event = json.loads(line)
            payload = event.get("payload", {})
            if event["type"] == "session_meta":
                session = payload["id"]
                roles[session] = payload.get("source")
            if event["type"] == "turn_context":
                seats.append(
                    {
                        "session": session,
                        "model": payload.get("model"),
                        "effort": payload.get("effort"),
                    }
                )
            if event["type"] != "response_item":
                continue
            kind = payload.get("type")
            if kind in {"function_call", "custom_tool_call"}:
                tool_lines.append(
                    json.dumps(
                        {
                            "session": session,
                            "timestamp": event.get("timestamp"),
                            "call": payload,
                        },
                        ensure_ascii=False,
                    )
                )
            elif kind in {"function_call_output", "custom_tool_call_output"}:
                # Full resource output is available where scoped loading needs it.
                tool_lines.append(
                    json.dumps(
                        {
                            "session": session,
                            "timestamp": event.get("timestamp"),
                            "result": payload,
                        },
                        ensure_ascii=False,
                    )
                )
    audit = {
        "seats": seats,
        "lineage": roles,
        "all_same_inherited_seat": bool(seats)
        and all(
            seat["model"] == "gpt-6.1-sol" and seat["effort"] == "xhigh"
            for seat in seats
        ),
    }
    (run / "identity-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    packet.extend(
        [
            "\n# Trace identity check\n\n",
            json.dumps(
                {
                    "same_inherited_seat_verified": audit["all_same_inherited_seat"],
                    "lineage": roles,
                },
                indent=2,
            ),
            "\n# Tool calls and results, parent and children\n\n",
            "\n".join(tool_lines),
            "\n# Exact delivered-prose comparisons against captured draft versions\n\n",
            json.dumps(comparison_evidence, indent=2),
            "\n# Complete filesystem delta\n\n",
            (run / "filesystem-changes.json").read_text(),
            "\n# Run completion evidence\n\n",
            (run / "result.json").read_text(),
        ]
    )
    contents = redact("".join(packet))
    destination.write_text(contents)
    (run / "judge-input-digest.json").write_text(
        json.dumps(
            {
                "sha256": hashlib.sha256(contents.encode()).hexdigest(),
                "bytes": len(contents.encode()),
                "path": str(destination),
            },
            indent=2,
        )
        + "\n"
    )
    print(destination, len(contents.encode()))


if __name__ == "__main__":
    main()
