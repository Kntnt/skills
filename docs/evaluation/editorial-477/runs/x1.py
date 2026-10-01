"""Read X1 again for every run with a checker, whatever fence the brief used.

    uv run --no-project python x1.py PACKETS_DIR

`states.py`, frozen with the plan, reads the texts out of the checker's brief
only inside a fence of four or more backticks; where the run fenced them with
three, `checked-delivered.md` keeps the fence and the line before it, and its
`x1` compares that wrapper too. This takes the fenced text out of
`checked-delivered.md` with a fence of three or more backticks, compares it with
`delivered.md`, and writes the result to `states.json` as `x1_text`, beside the
frozen script's `x1`. A run with no checker or no delivered text gets `null`.
"""

import json
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(`{3,})[a-z]*\n(.*?)\n\1$", re.DOTALL | re.MULTILINE)


def text_of(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    found = FENCE.search(raw)
    return found.group(2) + "\n" if found else raw


def main() -> int:
    for states in sorted(Path(sys.argv[1]).glob("*/states")):
        record = json.loads((states / "states.json").read_text())
        checked, delivered = states / "checked-delivered.md", states / "delivered.md"
        value = None
        if record["checkers"] and checked.is_file() and delivered.is_file():
            value = text_of(checked) == delivered.read_text(encoding="utf-8")
        record["x1_text"] = value
        (states / "states.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8"
        )
        print(f"{states.parent.name}\tx1={record['x1']}\tx1_text={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
