# /// script
# requires-python = ">=3.12"
# ///
"""Reuse the frozen native capture runner with the resolved neutral scratch root."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[4]
EVALUATION = REPOSITORY / "docs/evaluation/editorial-486"


def identity() -> dict[str, str]:
    """Keep the original independently verified native seat without reselection."""
    run = EVALUATION / "runs/pre-article-clean-file-1/run.json"
    return dict(json.loads(run.read_text())["parent_identity"])


def main() -> int:
    """Substitute only temporary paths and the source of verified seat metadata."""
    source = EVALUATION / "harness/run.py"
    spec = importlib.util.spec_from_file_location("frozen_capture", source)
    assert spec and spec.loader
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.SCRATCH = (REPOSITORY.parent / "486.scratch").resolve() / "amend-1/direct"
    runner.identity = identity
    return int(runner.main())


if __name__ == "__main__":
    raise SystemExit(main())
