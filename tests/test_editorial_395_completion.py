"""Check the completion runner's public CLI before a native seat is touched."""

import os
import subprocess
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
RUNNER = (
    REPOSITORY
    / "docs/evaluation/editorial-395/gpt-completion-2026-10-02/harness/run.py"
)


def test_completion_runner_requires_owned_paths_and_explicit_deadline() -> None:
    """Invocation cannot inherit the old temporary root or short deadline."""
    # Ask only for CLI documentation; this must never launch a native session.
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--help"],
        cwd=REPOSITORY,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "--scratch-root" in result.stdout
    assert "--parent-rollout" in result.stdout
    assert "--timeout" in result.stdout
