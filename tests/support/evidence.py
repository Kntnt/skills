"""Where committed evaluation evidence ends and the live evaluation documents begin."""

from __future__ import annotations

import re

EVALUATION = "docs/evaluation"

# A top-level directory of `docs/evaluation/` named for one evaluation: a name,
# a hyphen and the issue number it was run for, as `editorial-400`, `brief-444`
# and `redline-445`. The shape is matched rather than a list of names, so the
# next evaluation's packet is evidence the day it is committed.
PACKET = re.compile(r".+-\d+")

# What inside a packet stays live, because it is a tool every later evaluation
# runs or the document that says how to run it, not what that packet observed.
# `docs/evaluation/README.md` lists `editorial-388/` beside `corpus/` and
# `protocol.md` as what judging needs, and `protocol.md` names both runners.
LIVE_IN_A_PACKET = (
    "docs/evaluation/editorial-388/README.md",
    "docs/evaluation/editorial-388/harness/",
    "docs/evaluation/editorial-329/harness/run.py",
)


def is_evaluation_evidence(path: str) -> bool:
    """Say whether *path*, repository-relative and POSIX, is committed evidence.

    Evidence is what one evaluation or regression committed as its own record:
    a packet directory named for an issue (`editorial-400/`, `brief-444/`), a
    regression packet (`regressions/<n>/`), or a file directly under
    `records/` other than its README. A record of what a run saw, or of what
    was typed, is not an instruction and not the collection's own prose, and
    editing it to satisfy a lint falsifies it. `tests/test_evaluation.py`
    already draws the line: "Observed outputs and historical records are
    evidence, not requirements". So a scan of the collection's prose skips it.

    Everything else under `docs/evaluation/` is live and stays scanned: the
    protocol, the README and the template, the READMEs of `records/` and
    `regressions/`, `corpus/`, and the runners named in `LIVE_IN_A_PACKET`.
    """

    parts = path.split("/")
    if path.startswith(LIVE_IN_A_PACKET):
        return False
    if parts[:2] != ["docs", "evaluation"] or len(parts) < 4:
        return False

    first = parts[2]
    if first == "regressions":
        return parts[3].isdigit() and len(parts) > 4
    if first == "records":
        return len(parts) == 4 and parts[3] != "README.md"
    return PACKET.fullmatch(first) is not None
