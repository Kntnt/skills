#!/usr/bin/env python3
"""launch.py NN ARM — run one turn as a fresh `claude -p --agent kntnt-opus-high` session.

The prompt is the arm's turn file followed by the three dispatch lines, on stdin.
The session runs in its own process group, in the run's work directory, and is
stopped with its group if it outlives the timeout.
"""

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

S = Path("/Users/thomas/Projects/skills/.git/kntnt-orchestrate/399.scratch")
E = Path(
    "/Users/thomas/Projects/skills/.git/kntnt-orchestrate/399/docs/evaluation/editorial-399"
)
nn, arm = sys.argv[1], sys.argv[2]
run = S / "runs" / f"case-study-clean-{nn}"
work = run / "work"
turn = (E / f"redline-turn-{arm}.md").read_text()
prompt = (
    turn.rstrip("\n")
    + "\n\n"
    + f"Working directory: {work}\n"
    + f"Run directory: {run}\n"
    + "The user typed: /redline --genre=case-study --language=sv --output=response input.md\n"
)
out = S / "evaluator" / "streams"
tag = f"{nn}-{int(time.time())}"
(out / f"{tag}.prompt.txt").write_text(prompt)
command = [
    "claude",
    "--print",
    "--agent",
    "kntnt-opus-high",
    "--model",
    "claude-opus-5-5",
    "--effort",
    "high",
    "--dangerously-skip-permissions",
    "--strict-mcp-config",
    "--output-format",
    "stream-json",
    "--verbose",
]
(out / f"{tag}.argv.json").write_text(json.dumps(command))
with (out / f"{tag}.jsonl").open("w") as o, (out / f"{tag}.stderr.txt").open("w") as e:
    p = subprocess.Popen(
        command,
        cwd=work,
        stdin=subprocess.PIPE,
        stdout=o,
        stderr=e,
        text=True,
        start_new_session=True,
    )
    (out / f"{tag}.pid").write_text(str(p.pid))
    p.stdin.write(prompt)
    p.stdin.close()
    try:
        code = p.wait(timeout=3600)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)
        time.sleep(5)
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        code = "timeout"
(out / f"{tag}.exit").write_text(str(code))
print(tag, code)
