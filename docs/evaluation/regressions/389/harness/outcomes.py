# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read the mechanical facts out of each packet in this regression.

It judges nothing about the editorial quality of a run and decides no case. What
it reports is what a reader would otherwise have to count by hand: how many
correction rounds the trace records, how many times the closing Proofread shim
was invoked, whether the text the reply delivers is byte-identical to the text
the run was given, and whether the trace is whole (issue #389).
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

FENCE = re.compile(r"```(?:markdown|md)?\n(.*?)\n```", re.DOTALL)


def delivered_text(response: str) -> str | None:
    """Return the fenced Text Artifact of a reply, where it carries exactly one."""

    blocks = FENCE.findall(response)
    return blocks[0] + "\n" if len(blocks) == 1 else None


def facts(packet: Path) -> dict[str, Any]:
    """Describe one run packet without reading its own account of itself."""

    result = json.loads((packet / "result.json").read_text(encoding="utf-8"))
    index = json.loads((packet / "trace-index.json").read_text(encoding="utf-8"))
    status = json.loads((packet / "trace-status.json").read_text(encoding="utf-8"))
    supplied = (packet / "supplied-input.md").read_text(encoding="utf-8")
    response = (packet / "response.txt").read_text(encoding="utf-8")
    session = index["agents"][0]

    # A run may write the shim's path out in full or build it from the Skill's
    # own `$HERE`, and both are the same invocation: what identifies it is the
    # shim's file name beside the Skill's name, and not the spelling of the
    # directory above it. Counted on the literal path alone, a run that built
    # the path from a variable read as a run with no closing pass at all.
    shim_calls = 0
    for call in session["calls"]:
        command = (call.get("arguments") or {}).get("command") or ""
        if "proofread" in command.lower() and "invoke.py" in command:
            shim_calls += 1

    delivered = delivered_text(response)
    return {
        "invocation": (packet / "invocation.txt").read_text(encoding="utf-8").strip(),
        "revision": json.loads((packet / "run.json").read_text(encoding="utf-8"))[
            "instruction_revision"
        ],
        "returncode": result["returncode"],
        "duration_seconds": round(result["duration_seconds"]),
        "trace_status": status["status"],
        "correction_rounds": len(session.get("delegations") or []),
        "proofread_shim_invocations": shim_calls,
        "supplied_sha256": hashlib.sha256(supplied.encode()).hexdigest(),
        "delivered_sha256": (
            hashlib.sha256(delivered.encode()).hexdigest() if delivered else None
        ),
        "delivered_is_the_supplied_text": delivered == supplied,
    }


def main(argv: list[str]) -> int:
    """Print one JSON object per packet named on the command line."""

    report = {path.name: facts(Path(path)) for path in map(Path, argv[1:])}
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
