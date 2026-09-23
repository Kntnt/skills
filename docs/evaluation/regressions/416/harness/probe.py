"""Run one #416 probe: a Skill typed into `claude -p` in a seat with no subagent tool."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import time
from pathlib import Path

W = Path("/Users/thomas/Projects/skills/.git/kntnt-orchestrate/416")
S = Path("/Users/thomas/Projects/skills/.git/kntnt-orchestrate/416.scratch")
BASE = "65e0659991a61d8e2185837f1cd4fa0fe070453f"
PACKET = W / "docs/evaluation/regressions/416"
DENIED = ["Agent", "Task", "Workflow"]
PROMPTS = {
    "orchestrate": "/orchestrate --dry-run #416",
    "ready-for-agent-check": "/ready-for-agent-check #416",
    "delegation": "/delegation on --project --yes",
}
STAGED = {
    "kntnt": "kntnt",
    "delegation": "agents/delegation",
    "model-selector": "models/model-selector",
}

spec = importlib.util.spec_from_file_location(
    "staged_run", W / "docs/evaluation/editorial-388/harness/staged_run.py"
)
assert spec and spec.loader
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)


def command(prompt: str) -> list[str]:
    return [
        "claude",
        "-p",
        prompt,
        "--model",
        "claude-opus-5-5",
        "--effort",
        "high",
        "--dangerously-skip-permissions",
        "--strict-mcp-config",
        "--output-format",
        "stream-json",
        "--verbose",
        "--disallowedTools",
        *DENIED,
    ]


def run(cmd, cwd, env, stream: Path, stderr: Path, timeout=1500):
    started = time.monotonic()
    with stream.open("w") as out, stderr.open("w") as err:
        p = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=out,
            stderr=err,
            start_new_session=True,
        )
        timed_out = False
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(p.pid, signal.SIGTERM)
            p.wait()
    time.sleep(2)
    try:
        os.killpg(p.pid, 0)
        gone = False
    except ProcessLookupError:
        gone = True
    return {
        "returncode": p.returncode,
        "timed_out": timed_out,
        "duration_seconds": round(time.monotonic() - started, 1),
        "process_group": p.pid,
        "process_group_gone_after": gone,
    }


def git_state():
    return {
        "status_porcelain": subprocess.run(
            ["git", "-C", str(W), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout,
        "worktrees": subprocess.run(
            [
                "git",
                "-C",
                "/Users/thomas/Projects/skills",
                "worktree",
                "list",
                "--porcelain",
            ],
            capture_output=True,
            text=True,
            check=False,
        ).stdout,
    }


def main(skill: str, n: str) -> None:
    prompt = PROMPTS[skill]
    cmd = command(prompt)
    stream = PACKET / f"{skill}-{n}.jsonl"
    errfile = S / f"{skill}-{n}.stderr.txt"
    record: dict = {
        "skill": skill,
        "probe": n,
        "argv": cmd,
        "base_commit": BASE,
        "harness": subprocess.check_output(["claude", "--version"], text=True).strip(),
    }
    if skill == "delegation":
        root = S / f"delegation-{n}"
        assert not root.exists()
        for d in [
            "home/.claude",
            "repo",
            "scratch/tmp",
            "scratch/cache",
            "scratch/data",
            "scratch/uv-cache",
        ]:
            (root / d).mkdir(parents=True)
        (root / "home/.claude").chmod(0o700)
        archive = subprocess.check_output(
            [
                "git",
                "-C",
                str(W),
                "archive",
                BASE,
                *(f"skills/{p}" for p in STAGED.values()),
            ]
        )
        with tarfile.open(fileobj=io.BytesIO(archive)) as t:
            t.extractall(root / "export", filter="data")
        for name, src in STAGED.items():
            shutil.copytree(
                root / "export/skills" / src, root / "home/.claude/skills" / name
            )
        shutil.rmtree(root / "export")
        secret = root / "home/.claude" / sr.CREDENTIALS
        record["credential_source"] = sr.install_credential(secret)
        env = sr.environment(root)
        subprocess.run(["git", "init", "-q", str(root / "repo")], env=env, check=True)
        cwd = root / "repo"
        record["working_directory"] = str(cwd)
        record["environment"] = {
            k: env[k]
            for k in [
                "HOME",
                "CLAUDE_CONFIG_DIR",
                "TMPDIR",
                "UV_CACHE_DIR",
                "UV_PYTHON_INSTALL_DIR",
                "XDG_DATA_HOME",
                "XDG_CACHE_HOME",
                "XDG_CONFIG_HOME",
            ]
        }
        record["listing_before"] = {
            "repo": sr.inventory(root / "repo", secret),
            "home": sr.inventory(root / "home", secret),
        }
        record["outcome"] = run(cmd, cwd, env, stream, errfile)
        record["listing_after"] = {
            "repo": sr.inventory(root / "repo", secret),
            "home": sr.inventory(root / "home", secret),
        }
    else:
        env = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith(sr.STRIPPED_PREFIXES) and k not in sr.STRIPPED_NAMES
        }
        record["working_directory"] = str(W)
        record["environment"] = {
            "HOME": env["HOME"],
            "note": "real HOME; KNTNT_, CLAUDE_ and ANTHROPIC_ variables of the launching session stripped",
        }
        record["git_before"] = git_state()
        record["outcome"] = run(cmd, W, env, stream, errfile)
        record["git_after"] = git_state()
    record["stderr"] = errfile.read_text()
    (S / f"{skill}-{n}.record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(skill, n, json.dumps(record["outcome"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
