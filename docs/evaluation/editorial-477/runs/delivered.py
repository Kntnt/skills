"""Complete a run's states where the reply fenced its text with three backticks.

    uv run --no-project python delivered.py STATES_DIR

`states.py`, frozen with the plan, finds the delivered text in the reply only
inside a fence of four or more backticks. A reply may fence it with three. This
reads the same packet again with a fence of three or more and, where it finds
the text and `states.py` did not, writes `delivered.md`, rewrites
`final-reply.md` without the text, and sets `x1` in `states.json` as
`states.py` would have. It changes nothing where `states.py` found the text,
and records in `states.json` that it ran.
"""

import json
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(`{3,})markdown\n(.*?)\n\1$", re.DOTALL | re.MULTILINE)


def main() -> int:
    states = Path(sys.argv[1])
    packet = states.parent
    record = json.loads((states / "states.json").read_text())
    if (states / "delivered.md").is_file():
        return 0
    response = (packet / "response.txt").read_text(encoding="utf-8")
    fenced = FENCE.search(response)
    if not fenced:
        return 0
    delivered = fenced.group(2) + "\n"
    (states / "delivered.md").write_text(delivered, encoding="utf-8")
    final = response[: fenced.start()] + response[fenced.end() :]
    (states / "final-reply.md").write_text(final.strip() + "\n", encoding="utf-8")
    if record["checkers"]:
        checked = (states / "checked-delivered.md").read_text(encoding="utf-8")
        record["x1"] = checked == delivered
    record["delivered_by"] = "delivered.py"
    (states / "states.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
