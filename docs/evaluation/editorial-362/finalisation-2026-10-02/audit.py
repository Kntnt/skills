#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Audit retained retest bytes and native lifecycle without running a Skill."""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PACKET = HERE.parent / "gpt-retest-2026-10-01"


def strings(value: Any) -> list[str]:
    """Recover text from native structured outputs, including nested JSON text."""

    # Decode structured native results while retaining their literal text.
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return [value]
        return [value, *strings(decoded)] if not isinstance(decoded, str) else [value]
    if isinstance(value, dict):
        return [text for item in value.values() for text in strings(item)]
    if isinstance(value, list):
        return [text for item in value for text in strings(item)]
    return []


def prose(text: str) -> str:
    """Remove only the permitted metadata wrapper, preserving prose whitespace."""

    # Separate metadata without normalising the actual artifact.
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5 :].removeprefix("\n")
    return text


def sessions(sample: Path) -> list[dict[str, Any]]:
    """Check every captured native session's inherited identity and completion."""

    # Require positive native evidence rather than the run's own account.
    rows = []
    for path in sorted((sample / "native-sessions").rglob("*.jsonl")):
        events = [json.loads(line) for line in path.read_text().splitlines()]
        meta = next(e["payload"] for e in events if e["type"] == "session_meta")
        seats = [e["payload"] for e in events if e["type"] == "turn_context"]
        assert seats and all(
            seat["model"] == "gpt-6.1-sol" and seat["effort"] == "xhigh"
            for seat in seats
        ), path
        assert meta["cli_version"] == "0.159.3", path
        assert any(
            e["type"] == "event_msg" and e["payload"].get("type") == "task_complete"
            for e in events
        ), path
        rows.append(
            {
                "file": path.relative_to(ROOT).as_posix(),
                "started": events[0]["timestamp"],
                "child": isinstance(meta["source"], dict),
                "events": events,
            }
        )
    return rows


def audit() -> dict[str, Any]:
    """Return checkable evidence facts; semantic judgments remain unchanged."""

    # Verify the original scratch transfer against its retained destinations.
    transfer = json.loads((PACKET / "validation/transfer-manifest.json").read_text())
    marker = "/docs/evaluation/"
    for entry in transfer["files"]:
        relative = "docs/evaluation/" + entry["retained_path"].split(marker, 1)[1]
        assert (
            hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            == entry["sha256"]
        ), relative

    # Audit every counted run and judge, excluding voids and the capability smoke.
    samples = sorted((PACKET / "runs").iterdir()) + sorted(
        (PACKET / "judges").iterdir()
    )
    rows = []
    for sample in samples:
        result = json.loads((sample / "result.json").read_text())
        run = json.loads((sample / "run.json").read_text())
        cleanup = json.loads((sample / "cleanup.json").read_text())
        assert result["returncode"] == 0 and not result["timed_out"], sample
        assert run["instruction_revision"] == "fb16908712c4d47a36fc6ee9dfb3eb2714a19e65"
        assert cleanup["process_group_absent_before_removal"], sample
        assert cleanup["root_absent_after_removal"], sample
        assert cleanup.get("evidence_preserved") or cleanup.get(
            "evidence_preserved_external_to_root"
        ), sample
        native = sessions(sample)
        captures = json.loads((sample / "file-versions.json").read_text())
        for capture in captures:
            data = (sample / "file-versions" / capture["capture"]).read_bytes()
            assert hashlib.sha256(data).hexdigest() == capture["sha256"], sample
        row = {
            "sample": sample.relative_to(PACKET).as_posix(),
            "seconds": result["duration_seconds"],
            "native_sessions": [
                {key: value for key, value in entry.items() if key != "events"}
                for entry in native
            ],
            "capture_hashes_verified": len(captures),
            "cleanup_receipt_verified": True,
        }
        if sample.parent.name == "runs" and sample.name.startswith("opinion-"):
            draft = (sample / "draft.md").read_text()
            response = (sample / "response.txt").read_text()
            assert draft in re.findall(
                r"^```[^\n]*\n(.*?)^```[ \t]*$", response, re.MULTILINE | re.DOTALL
            ), sample
            children = sorted(
                (entry for entry in native if entry["child"]),
                key=lambda entry: entry["started"],
            )
            assert 1 <= len(children) <= 2, sample
            final = children[-1]
            outputs = [
                e["payload"]
                for e in final["events"]
                if e["type"] == "response_item"
                and e["payload"].get("type")
                in {"function_call_output", "custom_tool_call_output"}
            ]
            assert any(prose(draft) in text for text in strings(outputs)), sample
            matching = [
                capture
                for capture in captures
                if "draft" in Path(capture["path"]).name
                and prose((sample / "file-versions" / capture["capture"]).read_text())
                == prose(draft)
            ]
            assert matching, sample
            row["comparisons"] = len(children)
            row["final_checker"] = final["file"]
            row["delivered_prose_sha256"] = hashlib.sha256(
                prose(draft).encode()
            ).hexdigest()
            row["exact_prose_in_final_checker_tool_output"] = True
            row["matching_captures"] = matching
        rows.append(row)

    # Keep semantic readings literal instead of normalising away their qualifications.
    scores = {}
    for sample in sorted((PACKET / "judges").glob("opinion-*")):
        text = (sample / "captured-output.md").read_text()
        scores[sample.name] = {
            parts[1].strip(): parts[2].strip()
            for line in text.splitlines()
            if line.startswith("|")
            and len(parts := line.split("|")) > 2
            and parts[1].strip()
            in {"F1", "G2", "L1", "R2", "O1", "V1", "V2", "V3", "V4", "X"}
        }
    write = [row for row in rows if row["sample"].startswith("runs/opinion-")]
    scope = [row for row in rows if row["sample"].startswith("runs/p3-")]
    return {
        "method": "Read-only byte/native audit; no Skill, model or semantic judge launched.",
        "original_transfer_hashes_verified": len(transfer["files"]),
        "counted_write_runs": len(write),
        "counted_scope_runs": len(scope),
        "counted_judges": len(rows) - len(write) - len(scope),
        "counted_native_sessions": sum(len(row["native_sessions"]) for row in rows),
        "nested_comparisons": sum(row["comparisons"] for row in write),
        "write_median_seconds": statistics.median(row["seconds"] for row in write),
        "scope_median_seconds": statistics.median(row["seconds"] for row in scope),
        "raw_scores_verbatim": scores,
        "samples": rows,
        "limits": "Opaque dispatch contents remain unverified. Semantic judgments, method-error dispositions and historical cleanup claims are preserved, not rejudged or replayed.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
