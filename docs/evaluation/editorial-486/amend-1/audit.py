# /// script
# requires-python = ">=3.12"
# ///
"""Independently audit the replacement readers and unchanged original evaluation."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[4]
EVALUATION = REPOSITORY / "docs/evaluation/editorial-486"
HERE = EVALUATION / "amend-1"


def digest(path: Path) -> str:
    """Compare authentic source and delivered bytes, not their prose descriptions."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Verify every original byte, replacement prompt, seat and material inventory."""

    # Preserve the original freeze, runs, judgements and historical results verbatim.
    originals = json.loads((HERE / "original-files.json").read_text())
    for name, expected in originals.items():
        assert digest(REPOSITORY / name) == expected, name
    counted = json.loads((HERE / "counted-readers.json").read_text())
    assert len(counted) == 24
    assert len({row["packet"] for row in counted}) == 24
    expected_sources = json.loads((HERE / "original-readers.json").read_text())
    assert {row["source_packet"] for row in counted} == {
        row["packet"] for row in expected_sources
    }
    samples = []

    # Normalize only the deliberately substituted directory line in each prompt.
    for row in counted:
        packet = EVALUATION / row["packet"]
        source = EVALUATION / row["source_packet"]
        before_prompt = (source / "invocation.txt").read_text()
        after_prompt = (packet / "invocation.txt").read_text()
        normalize = lambda text: re.sub(
            r"(?m)^Run directory: .+$", "Run directory: [anonymous]", text
        )
        assert normalize(before_prompt) == normalize(after_prompt), row
        assert digest(packet / "supplied-input.md") == digest(
            source / "supplied-input.md"
        ), row
        result = json.loads((packet / "result.json").read_text())
        assert result["returncode"] == 0 and not result["timed_out"], row
        audit = json.loads((packet / "identity-audit.json").read_text())
        assert audit["same_seat"] and audit["seats"], row
        assert all(
            seat["model"] == "gpt-6.1-sol" and seat["effort"] == "xhigh"
            for seat in audit["seats"]
        ), row
        assert all(meta["cli_version"] == "0.160.0" for meta in audit["lineage"]), row

        # Prove every supplied file is authentic and remained unmodified in place.
        before = json.loads((packet / "inventory-before.json").read_text())
        after = json.loads((packet / "inventory-after.json").read_text())
        material_names = [
            name
            for name in before
            if name.startswith("work/") and before[name]["type"] == "file"
        ]
        for name in material_names:
            assert before[name] == after[name], (row, name)
        stat = json.loads((packet / "input-stat.json").read_text())
        assert stat["before"] == stat["after"], row
        changes = json.loads((packet / "filesystem-changes.json").read_text())
        assert not changes["authentication_changed"], row
        if row["role"] == "judge":
            run = source.parents[1]
            response = run / "response.txt"
            if "sanitized_response" in row:
                entries = json.loads((HERE / "file-materials.json").read_text())
                entry = next(item for item in entries if item["run"] == run.name)
                raw = response.read_bytes()
                neutral = EVALUATION / row["sanitized_response"]
                assert digest(response) == entry["raw_sha256"], row
                for replacement in entry["substitutions"]:
                    old = replacement["before"].encode()
                    assert raw.count(old) == 1, row
                    raw = raw.replace(old, replacement["after"].encode())
                assert raw == neutral.read_bytes(), row
                assert digest(neutral) == entry["neutral_sha256"], row
                response = neutral
            assert before["work/response.md"]["sha256"] == digest(response), row
            if "-file-" in run.name:
                assert before["work/work/output.md"]["sha256"] == digest(
                    run / "captured-output.md"
                ), row

        # Check actual reader-visible messages, policies, tool calls and results.
        public = [after_prompt, json.dumps(audit["lineage"])]
        for path in packet.rglob("*.jsonl.gz"):
            with gzip.open(path, "rt") as stream:
                public.append(stream.read())
        for text in public:
            assert not any(
                name in text
                for name in (
                    "ticket-486",
                    "editorial-486",
                    "/486/",
                    "pre-article-",
                    "post-article-",
                )
            ), row
        with gzip.open(packet / "trace.jsonl.gz", "rt") as stream:
            events = [json.loads(line) for line in stream]
        replies = [
            event["item"]["text"]
            for event in events
            if event["type"] == "item.completed"
            and event["item"]["type"] == "agent_message"
        ]
        assert (packet / "response.txt").read_text().rstrip("\n") == replies[-1].rstrip(
            "\n"
        ), row
        samples.append(
            {
                **row,
                "seat": "gpt-6.1-sol/xhigh",
                "cli": "0.160.0",
                "prompt_changed_only_in_directory": True,
                "source_and_materials_preserved": True,
                "native_sessions": len(audit["lineage"]),
                "ticket_and_arm_leaks": 0,
            }
        )
    print(
        json.dumps(
            {
                "original_files_preserved": len(originals),
                "counted_readers": len(counted),
                "validators": sum(row["role"] == "validator" for row in counted),
                "judges": sum(row["role"] == "judge" for row in counted),
                "samples": samples,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
