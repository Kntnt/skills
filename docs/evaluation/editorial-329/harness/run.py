# /// script
# requires-python = ">=3.12"
# ///
"""Capture one real, fresh Codex invocation for editorial issue #338.

This evaluator-owned artifact does not judge prose or implement a Skill. It
leaves its registered private root for literal-path cleanup after inspection.
An existing output directory is refused so failed evidence is never replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import signal
import stat
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[4]
NATIVE_CODEX = Path("/opt/homebrew/Caskroom/codex/0.155.1/bin/codex")
CLEANUP = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
AUTHENTICATION = Path("/Users/thomas/.codex/auth.json")
PARENT_ROLLOUT = Path(
    "/Users/thomas/.codex/sessions/2026/09/19/"
    "rollout-2026-09-19T19-59-11-01a0bad2-7a37-7d53-80a8-0c909db58d6c.jsonl"
)
SKILLS = {
    "kntnt": "kntnt",
    **{name: f"editorial/{name}" for name in ("write", "redline", "proofread")},
}


def write_json(path: Path, value: object) -> None:
    """Persist evaluator evidence outside the model's writable workspace."""
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def inventory(root: Path) -> dict[str, dict[str, Any]]:
    """Cover every private path without following links or publishing secrets."""

    # File contents are represented by hashes; auth retains only its mode/size.
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(root.rglob("*")):
        info = path.lstat()
        item: dict[str, Any] = {"mode": stat.S_IMODE(info.st_mode)}
        if path.is_symlink():
            item.update(type="symlink", target=str(path.readlink()))
        elif path.is_dir():
            item.update(type="directory")
        elif path.is_file():
            item.update(type="file", size=info.st_size)
            if path != root / "home/.codex/auth.json":
                item["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            item.update(type="other")
        result[str(path.relative_to(root))] = item
    return result


def register(kind: str, identifier: str) -> None:
    """Register owned resources immediately while the user's home is active."""
    subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            kind,
            identifier,
            "Editorial #338 isolated native evaluation",
        ],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    )


def identity() -> dict[str, str]:
    """Read the actual parent identity rather than guess an API model name."""
    for line in PARENT_ROLLOUT.read_text().splitlines():
        event = json.loads(line)
        if event["type"] == "turn_context":
            return {
                "model": event["payload"]["model"],
                "effort": event["payload"]["effort"],
            }
    raise RuntimeError("The parent rollout exposes no model identity")


def main() -> int:
    """Run one supplied prompt and preserve success, failure and disk evidence."""

    # The caller chooses frozen revisions and material, never a model override.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--corpus-revision", required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--input-name", choices=["source.md", "input.md"], required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    prompt = args.prompt.read_text()
    model = identity()
    revision = subprocess.check_output(
        ["git", "rev-parse", f"{args.revision}^{{commit}}"], cwd=REPOSITORY, text=True
    ).strip()
    corpus_revision = subprocess.check_output(
        ["git", "rev-parse", f"{args.corpus_revision}^{{commit}}"],
        cwd=REPOSITORY,
        text=True,
    ).strip()
    root = Path(tempfile.mkdtemp(prefix="kntnt-editorial-329-run-")).resolve()
    register("path", str(root))
    write_json(output / "location.json", {"root": str(root), "cleanup_required": True})

    # Export immutable instruction bytes, keeping the active installation intact.
    archive = subprocess.check_output(
        ["git", "archive", revision, *(f"skills/{path}" for path in SKILLS.values())],
        cwd=REPOSITORY,
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        bundle.extractall(root / "export", filter="data")
    work = root / "work"
    for name, source in SKILLS.items():
        shutil.copytree(root / "export/skills" / source, work / ".agents/skills" / name)
    subprocess.run(["git", "init", "-q", str(work)], cwd=REPOSITORY, check=True)
    for directory in [
        "home/.codex",
        "scratch/tmp",
        "scratch/cache",
        "scratch/data",
        "scratch/uv-cache",
    ]:
        (root / directory).mkdir(parents=True, exist_ok=True)
    shutil.copy2(AUTHENTICATION, root / "home/.codex/auth.json")
    auth_before = hashlib.sha256((root / "home/.codex/auth.json").read_bytes()).digest()
    config = (
        f"model = {json.dumps(model['model'])}\n"
        f"model_reasoning_effort = {json.dumps(model['effort'])}\n"
        'service_tier = "default"\n'
    )
    (root / "home/.codex/config.toml").write_text(config)
    context = (
        "# Evaluation harness dispatch\n\n"
        "For a `/write` or `/redline` invocation, read and execute the corresponding "
        "`.agents/skills/<name>/SKILL.md` in this project. These are the installed "
        "Skills for this invocation. Follow their shipped instructions.\n\n"
        f"The separate harness scratch area is `{root / 'scratch'}`. "
        "Its existence does not authorize a Skill to leave files behind.\n"
    )
    (work / "AGENTS.md").write_text(context)
    (output / "harness-context.md").write_text(context)
    (output / "invocation.txt").write_text(prompt)
    shutil.copy2(args.input, work / args.input_name)
    shutil.copy2(args.input, output / "supplied-input.md")

    # Confine model writes to inventoried work and scratch, including UV caches.
    env = {
        key: value for key, value in os.environ.items() if not key.startswith("KNTNT_")
    }
    for key in ["CODEX_THREAD_ID", "CODEX_SESSION_ID"]:
        env.pop(key, None)
    env.update(
        HOME=str(root / "home"),
        CODEX_HOME=str(root / "home/.codex"),
        TMPDIR=str(root / "scratch/tmp"),
        UV_CACHE_DIR=str(root / "scratch/uv-cache"),
        UV_PYTHON_INSTALL_DIR=str(root / "scratch/data/uv/python"),
        XDG_DATA_HOME=str(root / "scratch/data"),
        XDG_CACHE_HOME=str(root / "scratch/cache"),
    )
    command = [
        str(NATIVE_CODEX),
        "exec",
        "--ignore-rules",
        "-s",
        "workspace-write",
        "-c",
        "sandbox_workspace_write.network_access=true",
        "-c",
        "sandbox_workspace_write.exclude_tmpdir_env_var=true",
        "-c",
        "sandbox_workspace_write.exclude_slash_tmp=true",
        "--add-dir",
        str(root / "scratch"),
        "-C",
        str(work),
        "--skip-git-repo-check",
        "--json",
        "-o",
        str(output / "response.txt"),
        "-",
    ]
    write_json(
        output / "run.json",
        {
            "instruction_revision": revision,
            "corpus_revision": corpus_revision,
            "harness": "Codex CLI 0.155.1",
            "parent_identity": model,
            "input_name": args.input_name,
            "input_source": str(args.input.resolve()),
            "argv": command,
            "environment": {
                key: env[key]
                for key in [
                    "HOME",
                    "CODEX_HOME",
                    "TMPDIR",
                    "UV_CACHE_DIR",
                    "UV_PYTHON_INSTALL_DIR",
                    "XDG_DATA_HOME",
                    "XDG_CACHE_HOME",
                ]
            },
            "note": "Identity must also be checked against each native turn_context after the run.",
        },
    )
    before = inventory(root)
    write_json(output / "inventory-before.json", before)

    # Native traces and evaluator captures are kept outside the writable root.
    started = time.monotonic()
    timed_out = False
    with (
        (output / "trace.jsonl").open("w") as stdout,
        (output / "stderr.txt").open("w") as stderr,
    ):
        process = subprocess.Popen(
            command,
            cwd=work,
            env=env,
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr,
            text=True,
            start_new_session=True,
        )
        register("pid", str(process.pid))
        write_json(
            output / "process.json", {"pid": process.pid, "process_group": process.pid}
        )
        try:
            process.communicate(prompt, timeout=args.timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()

    # Preserve every correction-agent rollout and exact before/after changes.
    sessions = root / "home/.codex/sessions"
    if sessions.exists():
        shutil.copytree(sessions, output / "native-sessions")
    after = inventory(root)
    write_json(output / "inventory-after.json", after)
    write_json(
        output / "filesystem-changes.json",
        {
            "created": {path: after[path] for path in after.keys() - before.keys()},
            "removed": {path: before[path] for path in before.keys() - after.keys()},
            "changed": {
                path: {"before": before[path], "after": after[path]}
                for path in before.keys() & after.keys()
                if before[path] != after[path]
            },
            "authentication_changed": auth_before
            != hashlib.sha256((root / "home/.codex/auth.json").read_bytes()).digest(),
            "note": "Classify individual Harness and Skill effects from the trace; do not treat all changes as Skill artifacts or ignore all home/scratch changes.",
        },
    )
    result = {
        "returncode": process.returncode,
        "timed_out": timed_out,
        "duration_seconds": round(time.monotonic() - started, 2),
        "root": str(root),
        "cleanup_required": True,
    }
    write_json(output / "result.json", result)
    print(json.dumps(result), flush=True)
    return process.returncode or int(timed_out)


if __name__ == "__main__":
    raise SystemExit(main())
