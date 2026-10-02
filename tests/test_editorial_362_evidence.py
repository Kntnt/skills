"""Keep the completed retest attributable to its untouched source worktree."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINALISATION = ROOT / "docs/evaluation/editorial-362/finalisation-2026-10-02"


def test_integrated_retest_preserves_every_attributable_source_file() -> None:
    """The pre-transfer inventory constrains evidence, including uncommitted files."""

    # Read the independent inventory captured before the evidence transfer.
    inventory = json.loads((FINALISATION / "source-inventory.json").read_text())
    assert inventory["source_head"] == "27061b27037f3ea215ed2619a189c8aa4f1565a2"
    assert len(inventory["files"]) == 630

    # Compare all transferred bytes without consulting the retained worktree.
    for entry in inventory["files"]:
        relative = Path(entry["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        path = ROOT / relative
        assert path.is_file(), f"Missing preserved evidence: {relative}"
        contents = path.read_bytes()
        assert len(contents) == entry["bytes"], relative
        assert hashlib.sha256(contents).hexdigest() == entry["sha256"], relative


def test_native_audit_accounts_for_all_counted_runs_and_final_checker_reads() -> None:
    """The complete frozen matrix remains inspectable through its audit command."""

    # Run the evaluator's public read-only command in the repository working directory.
    result = subprocess.run(
        [sys.executable, str(FINALISATION / "audit.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

    # Hold the commissioned matrix and exact final-read evidence to independent counts.
    receipt = json.loads(result.stdout)
    assert receipt["counted_write_runs"] == 6
    assert receipt["counted_scope_runs"] == 6
    assert receipt["counted_judges"] == 7
    assert receipt["counted_native_sessions"] == 30
    assert receipt["nested_comparisons"] == 11
    write = [
        row for row in receipt["samples"] if row["sample"].startswith("runs/opinion-")
    ]
    assert all(row["exact_prose_in_final_checker_tool_output"] for row in write)
