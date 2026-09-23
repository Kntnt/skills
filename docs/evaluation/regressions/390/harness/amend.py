# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Capture one frozen #390 native case in a private staged installation."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
PACKET = REPO / "docs/evaluation/regressions/390"
SCRATCH = (
    Path(
        "/Users/thomas/Projects/skills/.git/orchestrate-session-389-391-gpt/scratch/390"
    )
    / "amend-1a1acf"
)
CASES = (
    "recorded-column",
    "paraphrased-column",
    "clean-reuse",
    "paraphrased-headline",
    "write-column",
)


def save(path: Path, value: Any) -> None:
    """Retain exact metadata in a readable, deterministic encoding."""
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def inventory(root: Path) -> dict[str, str]:
    """Hash supplied work and temporary files, excluding private runtime state."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for area in (root / "work", root / "tmp")
        for path in sorted(area.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    """Stage, bound and capture one real invocation without judging its prose."""

    # A new directory prevents an attempt from overwriting an earlier trace.
    case = sys.argv[1]
    if case not in CASES:
        raise SystemExit(f"Unknown case: {case}")
    root = SCRATCH / case
    output = PACKET / "amend-1a1acf" / case
    output.mkdir(parents=True)
    work = root / "work"
    temporary = root / "tmp"
    profile = root / "codex-profile"
    for directory in (work, temporary, profile):
        directory.mkdir(parents=True)
    staged = work / ".agents/skills"
    for skill in ("kntnt", "write", "redline", "proofread"):
        source = REPO / "skills" / (skill if skill == "kntnt" else f"editorial/{skill}")
        shutil.copytree(
            source,
            staged / skill,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
    fixture = "column-source" if case == "write-column" else case
    operand = "source.md" if case == "write-column" else "input.md"
    shutil.copyfile(PACKET / "fixtures" / f"{fixture}.md", work / operand)
    context = (PACKET / "runs/recorded-column/harness-context.md").read_text()
    context += (
        "\nEvery private temporary directory, including each UV command's fresh "
        "directory, must be created below the initial TMPDIR. Preserve that "
        "base as a task-specific variable before assigning a command's TMPDIR. "
        "Use mktemp -d with a full template below that base. The sandbox permits "
        "network access and writes only under this run's private root. "
        "Pass this containment instruction to fresh child agents.\n"
    )
    (work / "AGENTS.md").write_text(context)
    (output / "harness-context.md").write_text(context)
    invocation = (PACKET / "tasks" / f"{case}.txt").read_text()
    (output / "invocation.txt").write_text(invocation)
    save(
        output / "instruction-digests.json",
        {
            str(path.relative_to(staged)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(staged.rglob("*"))
            if path.is_file()
        },
    )

    # Use the CLI's dedicated configuration directory for this native instance.
    shutil.copyfile(Path.home() / ".codex/auth.json", profile / "auth.json")
    (profile / "auth.json").chmod(0o600)
    (profile / "config.toml").write_text(
        'model = "gpt-5.6-sol"\nmodel_reasoning_effort = "xhigh"\n'
        'service_tier = "default"\napproval_policy = "never"\n'
        "[features]\nmulti_agent = true\n"
        "[sandbox_workspace_write]\nnetwork_access = true\n"
        "exclude_tmpdir_env_var = true\nexclude_slash_tmp = true\n"
    )
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("CODEX_", "KNTNT_"))
    }
    environment.update(
        CODEX_HOME=str(profile),
        KNTNT_HOME=str(root / "kntnt-state"),
        TMPDIR=str(temporary),
        UV_CACHE_DIR=str(SCRATCH / "uv-cache"),
        XDG_CACHE_HOME=str(root / "cache"),
        XDG_DATA_HOME=str(root / "data"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    command = [
        "/opt/homebrew/bin/codex",
        "exec",
        "--ignore-rules",
        "-s",
        "workspace-write",
        "--add-dir",
        str(root),
        "--skip-git-repo-check",
        "--json",
        "-C",
        str(work),
        "-o",
        str(output / "response.txt"),
        "-",
    ]
    save(output / "before.json", inventory(root))
    started = time.monotonic()

    # Start in a process group and register before waiting on native execution.
    with (
        (output / "events.jsonl").open("w") as stdout,
        (output / "stderr.txt").open("w") as stderr,
    ):
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr,
            text=True,
            cwd=work,
            env=environment,
            start_new_session=True,
        )
        record = {
            "product_revision": "09fb8991",
            "argv": command,
            "pid": process.pid,
            "process_group": process.pid,
            "harness": "codex-cli 0.155.1",
            "model": "gpt-5.6-sol",
            "effort": "xhigh",
            "timeout_seconds": 1800,
        }
        save(output / "process.json", record)
        try:
            for owned_pid in (os.getpid(), process.pid):
                subprocess.run(
                    [
                        "uv",
                        "run",
                        "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py",
                        "add",
                        "pid",
                        str(owned_pid),
                        f"#390 native {case}",
                    ],
                    cwd=REPO,
                    env=environment,
                    check=True,
                    stdout=stderr,
                    stderr=stderr,
                    timeout=30,
                )
            process.communicate(invocation, timeout=1800)
            record["timed_out"] = False
        except subprocess.TimeoutExpired:
            record["timed_out"] = True
        finally:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()

    record.update(exit_status=process.returncode, elapsed=time.monotonic() - started)
    save(output / "process.json", record)
    save(output / "after.json", inventory(root))
    if (profile / "sessions").exists():
        shutil.copytree(profile / "sessions", output / "native")
    print(json.dumps(record), flush=True)


if __name__ == "__main__":
    if os.getpgrp() != os.getpid():
        os.setsid()
    main()
