# /// script
# requires-python = ">=3.12"
# ///
"""Check one saved reply against the fenced-delivery rule.

Reads a reply and the fixture the run was given, and reports the three facts
the regression turns on: how many fenced code blocks the reply holds and which
of them carries the Text Artifact, whether any part of the artifact sits
outside a fence, and whether the fenced text's leading frontmatter block is
byte-identical to the fixture's. A reply carrying no Text Artifact at all —
a correct no-change status, or a run that stopped before it read the text —
is reported as not exercised rather than as a miss.
Usage: `check.py <response.md> <fixture.md>`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>[^`]*)$")
DELIMITER = "---"


def blocks(reply: str) -> list[tuple[str, str]]:
    """Every fenced code block in the reply, as its info string and content."""

    found: list[tuple[str, str]] = []
    lines = reply.split("\n")
    index = 0
    while index < len(lines):
        opening = FENCE.match(lines[index])
        if opening is None:
            index += 1
            continue
        marker = opening.group("fence")
        body: list[str] = []
        index += 1
        while index < len(lines):
            closing = FENCE.match(lines[index])
            if closing is not None and closing.group("fence").startswith(
                marker[0] * len(marker)
            ):
                break
            body.append(lines[index])
            index += 1
        found.append((opening.group("info").strip(), "\n".join(body)))
        index += 1
    return found


def frontmatter(text: str) -> str | None:
    """The leading frontmatter block, delimiters included, or None where there is none."""

    lines = text.split("\n")
    if not lines or lines[0].strip() != DELIMITER:
        return None
    for number, line in enumerate(lines[1:], start=1):
        if line.strip() == DELIMITER:
            return "\n".join(lines[: number + 1])
    return None


def main() -> int:
    """Report the three facts and exit non-zero where any of them fails."""

    reply = Path(sys.argv[1]).read_text(encoding="utf-8")
    fixture = Path(sys.argv[2]).read_text(encoding="utf-8")

    fenced = blocks(reply)
    carrying = [(info, body) for info, body in fenced if "kntnt:" in body]
    outside = reply
    for _, body in fenced:
        outside = outside.replace(body, "")

    print(f"fenced blocks: {len(fenced)}")
    for number, (info, body) in enumerate(fenced, start=1):
        head = body.split("\n")[0] if body else ""
        tail = [line for line in body.split("\n") if line.strip()]
        print(f"  block {number}: info={info!r} lines={len(body.split(chr(10)))}")
        print(f"    first: {head!r}")
        print(f"    last:  {(tail[-1] if tail else '')!r}")
    print(f"blocks carrying the artifact: {len(carrying)}")
    print(f"artifact content outside every fence: {'kntnt:' in outside}")

    if not carrying and "kntnt:" not in outside:
        print("result: not exercised (the reply carries no Text Artifact)")
        return 0

    ok = len(carrying) == 1 and "kntnt:" not in outside
    if len(carrying) == 1:
        inside = frontmatter(carrying[0][1])
        expected = frontmatter(fixture)
        print(f"fenced frontmatter block: {inside!r}")
        print(f"fixture frontmatter block: {expected!r}")
        identical = inside is not None and inside == expected
        print(f"frontmatter byte-identical: {identical}")
        ok = ok and identical
    print(f"result: {'pass' if ok else 'MISS'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
