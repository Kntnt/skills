# /// script
# requires-python = ">=3.12"
# ///
"""Copy semantic evidence into one neutral packet for independent judges."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]


def section(label: str, value: str) -> str:
    """Fence exact material without allowing an internal fence to close it."""
    longest = 2
    for line in value.splitlines():
        if line.startswith("`"):
            longest = max(longest, len(line) - len(line.lstrip("`")))
    fence = "`" * (longest + 1)
    boundary = "" if value.endswith("\n") else "\n"
    return f"\n### {label}\n\n{fence}text\n{value}{boundary}{fence}\n"


def main() -> None:
    """Use only evaluator-accepted deliveries, never classify a stop by regex."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staging", type=Path)
    parser.add_argument("dispositions", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    # The evaluator explicitly marks delivery/stop after reading the reply.
    dispositions = json.loads(args.dispositions.read_text())
    rows = json.loads((PACKET / "run-index.json").read_text())
    selected = [r for r, d in dispositions.items() if d["counted"]]
    # Neutral order derives solely from run identifiers, never from outcomes.
    selected.sort(key=lambda r: hashlib.sha256(r.encode()).digest())
    mapping = {}
    contents = [(PACKET / "judge-brief.md").read_text()]
    for index, run in enumerate(selected, start=1):
        neutral = f"sample-{index:02d}"
        mapping[neutral] = run
        directory = args.staging / run
        write = rows[run]["fixture"] == "case-study-sv"
        contents.append(
            f"\n## {neutral}\n\nTask: "
            + ("translation/composition" if write else "source-blind review")
            + f". Requested output target: {rows[run]['output_target']}.\n"
        )
        contents.append(
            section("Formal Invocation", (directory / "invocation.txt").read_text())
        )
        contents.append(
            section(
                "Complete original source" if write else "Complete supplied input",
                (directory / "supplied-input.md").read_text(),
            )
        )
        if dispositions[run]["delivered"]:
            contents.append(
                section(
                    "Delivered Text Artifact", (directory / "delivered.md").read_text()
                )
            )
        else:
            contents.append("\nNo Text Artifact was delivered.\n")
        contents.append(
            section("User-facing reply", (directory / "response.txt").read_text())
        )
    args.output.write_text("".join(contents))
    # This map remains outside the judge input; it is evaluator provenance.
    (PACKET / "semantic-map.json").write_text(json.dumps(mapping, indent=2) + "\n")
    print(json.dumps({"samples": len(selected), "bytes": args.output.stat().st_size}))


if __name__ == "__main__":
    main()
