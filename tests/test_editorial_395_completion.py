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


def test_completion_runner_rejects_missing_deadline_before_starting_native() -> None:
    """A caller cannot accidentally reuse the exhausted 1800-second bound."""
    result = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=REPOSITORY,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "--timeout" in result.stderr
    assert "--scratch-root" in result.stderr
    assert "--parent-rollout" in result.stderr


def test_observer_captures_work_under_an_assigned_git_parent(tmp_path: Path) -> None:
    """Only internal Git/install files are excluded from transient observation."""
    import runpy

    area = tmp_path / ".git" / "private" / "work"
    area.mkdir(parents=True)
    (area / "source.md").write_text("source")
    (area / ".git").mkdir()
    (area / ".git" / "internal.md").write_text("internal")
    (area / ".agents").mkdir()
    (area / ".agents" / "installed.md").write_text("installed")
    corrected = RUNNER.with_name("run-v2.py")
    observer = runpy.run_path(str(corrected))
    assert list(observer["capture_candidates"](area)) == [area / "source.md"]
