# /// script
# requires-python = ">=3.12"
# ///
"""Verify delivered prose occurs intact in the last checker's actual file read."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def main() -> None:
    """Use the captured read, not the checker's approval, as byte evidence."""

    # Metadata and outer blank lines are the only delivery elements removed.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    args = parser.parse_args()
    case = args.case
    run = case / "write"
    audit = json.loads((run / "trace-audit.json").read_text())
    draft = (case / "draft.md").read_text()
    prose = re.sub(r"\A---\n.*?\n---\n", "", draft, count=1, flags=re.DOTALL).strip(
        "\n"
    )
    children = [session for session in audit["sessions"] if session["parent_thread_id"]]
    checked: list[dict[str, Any]] = []

    # Each visible read must cover the complete delivered prose continuously.
    for child in children:
        read_calls = [
            call
            for call in child["calls"]
            if "draft" in str(call["input"])
            and ("cat " in str(call["input"]) or "read_text" in str(call["input"]))
        ]
        checked.append(
            {
                "session": child["file"],
                "has_explicit_draft_read": bool(read_calls),
                "complete_delivered_prose_visible": prose in child["visible_output"],
                "read_calls": read_calls,
            }
        )
    last = checked[-1] if checked else None
    result = {
        "normalization": "Remove only leading delivery YAML map and outer blank lines; preserve all prose characters and internal whitespace.",
        "checker_reads": checked,
        "last_checker_matches": bool(
            last
            and last["has_explicit_draft_read"]
            and last["complete_delivered_prose_visible"]
        ),
        "note": "A match proves continuous final prose was visibly read. Inspect the native read command/output for complete draft boundaries and truncation; checker approval alone is insufficient.",
    }
    (run / "checked-prose-audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {"case": case.name, "last_checker_matches": result["last_checker_matches"]}
        )
    )


if __name__ == "__main__":
    main()
