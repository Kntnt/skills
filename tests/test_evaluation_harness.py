"""The staged runner's isolation, its inventory and its teardown."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
HARNESS: Path = REPO_ROOT / "docs" / "evaluation" / "editorial-388" / "harness"

# Long enough that the process is unmistakably alive when the test stops it,
# short enough that a failure to stop it costs a minute rather than a day.
LIVE_SECONDS = 60


def _module() -> Any:
    """Load the runner under the name its own evidence names it by."""

    if "staged_run" in sys.modules:
        return sys.modules["staged_run"]
    spec = importlib.util.spec_from_file_location(
        "staged_run", HARNESS / "staged_run.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["staged_run"] = module
    spec.loader.exec_module(module)
    return module


staged_run = _module()


def test_every_writable_path_the_run_is_given_is_inside_its_own_root(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"

    given = staged_run.environment(root)

    for name in [
        "HOME",
        "CLAUDE_CONFIG_DIR",
        "TMPDIR",
        "UV_CACHE_DIR",
        "UV_PYTHON_INSTALL_DIR",
        "XDG_DATA_HOME",
        "XDG_CACHE_HOME",
        "XDG_CONFIG_HOME",
    ]:
        assert Path(given[name]).is_relative_to(root), name


def test_the_starting_sessions_own_harness_identity_never_reaches_the_run(
    tmp_path: Path,
) -> None:
    for name, value in [
        ("CLAUDECODE", "1"),
        ("CLAUDE_CODE_SSE_PORT", "4242"),
        ("KNTNT_HOME", str(tmp_path / "elsewhere")),
        ("ANTHROPIC_API_KEY", "not-a-real-key"),
        ("PATH_MARKER_FOR_TEST", "kept"),
    ]:
        os.environ[name] = value
    try:
        given = staged_run.environment(tmp_path / "root")
    finally:
        for name in [
            "CLAUDECODE",
            "CLAUDE_CODE_SSE_PORT",
            "KNTNT_HOME",
            "ANTHROPIC_API_KEY",
            "PATH_MARKER_FOR_TEST",
        ]:
            del os.environ[name]

    assert "CLAUDECODE" not in given
    assert "CLAUDE_CODE_SSE_PORT" not in given
    assert "KNTNT_HOME" not in given
    assert "ANTHROPIC_API_KEY" not in given
    assert given["PATH_MARKER_FOR_TEST"] == "kept"


def test_the_inventory_hashes_every_file_it_covers_but_never_the_credential(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    (root / "home").mkdir(parents=True)
    secret = root / "home" / ".credentials.json"
    secret.write_text('{"claudeAiOauth": {"accessToken": "secret"}}')
    (root / "work").mkdir()
    (root / "work" / "source.md").write_text("material\n")
    (root / "work" / "link").symlink_to(root / "work" / "source.md")

    covered = staged_run.inventory(root, secret)

    assert "sha256" in covered["work/source.md"]
    assert "sha256" not in covered["home/.credentials.json"]
    assert covered["home/.credentials.json"]["size"] == secret.stat().st_size
    assert covered["work/link"]["type"] == "symlink"
    assert covered["work"]["type"] == "directory"


def test_stopping_a_run_ends_everything_its_process_group_started() -> None:
    # A shell that outlives its own child is the shape a run has: killing the
    # leader alone would leave the sleep behind, which is what `_stop` is for.
    # The working directory is the repository, which no test removes.
    process = subprocess.Popen(
        ["sh", "-c", f"sleep {LIVE_SECONDS} & sleep {LIVE_SECONDS}"],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        start_new_session=True,
    )
    assert not staged_run._gone(process.pid)

    staged_run._stop(process)

    # The group is reaped asynchronously, so the check is given a moment.
    for _ in range(50):
        if staged_run._gone(process.pid):
            break
        time.sleep(0.1)
    assert staged_run._gone(process.pid)


def test_harvest_keeps_the_session_record_and_every_nested_agent(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    session = "11111111-2222-3333-4444-555555555555"
    project = root / "home" / ".claude" / "projects" / "-some-work"
    (project / session / "subagents").mkdir(parents=True)
    (project / f"{session}.jsonl").write_text('{"type": "user"}\n')
    (project / session / "subagents" / "agent-abc.jsonl").write_text(
        '{"type": "user"}\n'
    )
    (project / session / "subagents" / "agent-abc.meta.json").write_text(
        '{"agentType": "x"}'
    )
    (project / session / "tool-results").mkdir()
    (project / session / "tool-results" / "big.txt").write_text("offloaded\n")
    packet = tmp_path / "packet"
    packet.mkdir()

    kept = staged_run.harvest(root, session, packet)

    assert kept["missing"] == []
    assert kept["subagent_transcripts"] == 1
    assert (packet / "transcripts" / "parent.jsonl").is_file()
    assert (packet / "transcripts" / "subagents" / "agent-abc.meta.json").is_file()
    assert (packet / "transcripts" / "extra" / "tool-results" / "big.txt").is_file()


def test_harvest_names_a_session_record_that_was_never_written(tmp_path: Path) -> None:
    root = tmp_path / "root"
    (root / "home" / ".claude" / "projects").mkdir(parents=True)
    packet = tmp_path / "packet"
    packet.mkdir()

    kept = staged_run.harvest(root, "no-such-session", packet)

    assert kept["missing"] == ["parent-transcript"]
    assert kept["parent_transcript"] is None
    assert not (packet / "transcripts" / "parent.jsonl").exists()


def test_a_run_that_started_no_subagent_reports_no_missing_trace(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    session = "11111111-2222-3333-4444-555555555555"
    project = root / "home" / ".claude" / "projects" / "-some-work"
    project.mkdir(parents=True)
    (project / f"{session}.jsonl").write_text('{"type": "user"}\n')
    packet = tmp_path / "packet"
    packet.mkdir()

    kept = staged_run.harvest(root, session, packet)

    assert kept["missing"] == []
    assert kept["subagents_directory"] == "absent"
    assert kept["subagent_transcripts"] == 0


def test_the_private_root_is_removed_however_the_run_ends(tmp_path: Path) -> None:
    packet = tmp_path / "packet"
    packet.mkdir()
    beside = Path(tempfile.mkdtemp(prefix=staged_run.ROOT_PREFIX))
    try:
        with staged_run.private_root(packet) as root:
            (root / "work").mkdir()
            made = root
            assert made.is_dir()
            raise RuntimeError("the run failed")
    except RuntimeError:
        pass

    assert not made.exists()
    assert beside.is_dir(), "a root this run did not make must not be removed"
    cleanup = json.loads((packet / "cleanup.json").read_text())
    assert cleanup["removed"] is True
    assert cleanup["removed_only"] == str(made)
    shutil.rmtree(beside)
