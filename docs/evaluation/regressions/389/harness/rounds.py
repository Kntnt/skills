# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read, for each packet, which state of the text each round started from.

A run of more than one round can restore a state that is neither the text it
delivered a round earlier nor the text it was given, so `outcomes.py`'s one
comparison against the supplied input cannot say which state came back. The
correction brief carries the complete Text Artifact as it stood when the round
started, and the trace records every delegation's prompt verbatim, so the state
before each round is readable from the packet itself.

This reads those states out and compares them with the text the reply delivers.
It judges nothing and decides no case: what it reports is which round's
pre-round state the delivered text is, where it is one of them (issue #389).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HEADER = "**The text.** This is the complete Text Artifact, exactly as it now stands:"
FINDINGS = "**The findings.**"


def digest(text: str) -> str:
    """Return the SHA-256 a reader can recompute from the file beside it."""

    return hashlib.sha256(text.encode()).hexdigest()


def pre_round_text(prompt: str) -> str | None:
    """Return the Text Artifact a correction brief handed its round."""

    start = prompt.find(HEADER)
    end = prompt.find(FINDINGS, start + 1)
    if start < 0 or end < 0:
        return None
    return prompt[start + len(HEADER) : end].strip() + "\n"


def facts(packet: Path) -> dict[str, Any]:
    """Describe the states one run passed through, and the one it delivered."""

    index = json.loads((packet / "trace-index.json").read_text(encoding="utf-8"))
    supplied = (packet / "supplied-input.md").read_text(encoding="utf-8")
    response = (packet / "response.txt").read_text(encoding="utf-8")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from outcomes import delivered_text

    delivered = delivered_text(response)
    states: list[dict[str, Any]] = []
    for ordinal, delegation in enumerate(
        index["agents"][0].get("delegations") or [], 1
    ):
        text = pre_round_text(delegation.get("prompt") or "")
        states.append(
            {
                "round": ordinal,
                "pre_round_sha256": digest(text) if text else None,
                "pre_round_is_the_supplied_text": text == supplied,
                "delivered_is_this_pre_round_state": (
                    delivered is not None and text == delivered
                ),
            }
        )

    restored = [
        state["round"] for state in states if state["delivered_is_this_pre_round_state"]
    ]
    return {
        "rounds": len(states),
        "states": states,
        "delivered_sha256": digest(delivered) if delivered else None,
        "delivered_is_the_pre_round_state_of_round": restored[0] if restored else None,
    }


def main(argv: list[str]) -> int:
    """Print one JSON object per packet named on the command line."""

    report = {path.name: facts(Path(path)) for path in map(Path, argv[1:])}
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
