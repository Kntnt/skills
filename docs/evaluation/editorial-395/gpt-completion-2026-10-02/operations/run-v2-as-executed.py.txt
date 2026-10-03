# /// script
# requires-python = ">=3.12"
# ///
"""Capture one real, fresh Codex invocation for editorial issue #395.

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
import threading
import time
from pathlib import Path
from typing import Any
from collections.abc import Iterator

REPOSITORY = Path(__file__).resolve().parents[5]
NATIVE_CODEX = Path("/opt/homebrew/bin/codex").resolve()
CLEANUP = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py"
)
AUTHENTICATION = Path("/Users/thomas/.codex/auth.json")

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


def register(kind: str, identifier: str, scratch: Path) -> None:
    """Record owned resources locally and through the installed cleanup seam.

    The installed seam refuses non-system-temp paths; the local receipt still
    registers them for manual literal-path cleanup within the assigned root.
    """
    receipt = {"kind": kind, "identifier": identifier, "at": time.time()}
    with (scratch / "lifecycle.jsonl").open("a") as stream:
        stream.write(json.dumps(receipt) + "\n")
    env = dict(
        os.environ, KNTNT_HOME=str(scratch), UV_CACHE_DIR=str(scratch / "uv-cache")
    )
    result = subprocess.run(
        [
            "uv",
            "run",
            str(CLEANUP),
            "add",
            kind,
            identifier,
            "Editorial #395 isolated completion; local lifecycle receipt",
        ],
        cwd=REPOSITORY,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    with (scratch / "registration-receipts.jsonl").open("a") as stream:
        stream.write(
            json.dumps(
                {
                    **receipt,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )
            + "\n"
        )
    if kind == "pid" and result.returncode:
        raise RuntimeError(result.stderr)


def identity(rollout: Path) -> dict[str, str]:
    """Read the inherited current turn identity without forcing historical effort."""
    model = None
    for line in rollout.read_text().splitlines():
        event = json.loads(line)
        if event["type"] == "turn_context":
            model = {
                "model": event["payload"]["model"],
                "effort": event["payload"]["effort"],
            }
    if model is None:
        raise RuntimeError("The parent rollout exposes no model identity")
    return model


def capture_candidates(area: Path) -> Iterator[Path]:
    """Observe prose under owned roots, excluding only internal install/Git files."""
    for path in area.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".txt"}:
            continue
        if {".agents", ".git"}.intersection(path.relative_to(area).parts):
            continue
        yield path


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
    parser.add_argument("--timeout", type=int, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--parent-rollout", type=Path, required=True)
    parser.add_argument("--capture-output-name")
    parser.add_argument("--packet", type=Path)
    args = parser.parse_args()
    scratch = args.scratch_root.resolve()
    allowed = REPOSITORY.parent / "395.scratch"
    if scratch != allowed:
        parser.error("--scratch-root must be the assigned 395.scratch directory")
    if not args.output.resolve().is_relative_to(scratch):
        parser.error("--output must be inside the assigned scratch directory")
    if args.timeout != 5400:
        parser.error("The frozen completion deadline is 5400 seconds")
    if os.getpgrp() != os.getpid():
        os.setsid()
    register("pid", str(os.getpid()), scratch)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    prompt = args.prompt.read_text()
    model = identity(args.parent_rollout)
    cli_version = subprocess.check_output(
        [str(NATIVE_CODEX), "--version"], cwd=REPOSITORY, text=True
    ).strip()
    revision = subprocess.check_output(
        ["git", "rev-parse", f"{args.revision}^{{commit}}"], cwd=REPOSITORY, text=True
    ).strip()
    corpus_revision = subprocess.check_output(
        ["git", "rev-parse", f"{args.corpus_revision}^{{commit}}"],
        cwd=REPOSITORY,
        text=True,
    ).strip()
    root = scratch / ("native-" + output.name)
    root.mkdir(exist_ok=False)
    register("path", str(root), scratch)
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
    if args.packet:
        for member in args.packet.iterdir():
            if member.is_dir():
                shutil.copytree(member, work / member.name)
            else:
                shutil.copy2(member, work / member.name)

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
            "harness": cli_version,
            "deadline_seconds": args.timeout,
            "inherited_identity_source": str(args.parent_rollout),
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
    # Observe ephemeral files externally without changing the Skill's work.
    captured: dict[str, str] = {}
    capture_log: list[dict[str, object]] = []
    capture_stop = threading.Event()
    capture_directory = output / "file-versions"
    capture_directory.mkdir()

    def capture_versions() -> None:
        """Preserve transient prose, reports and dispositions before removal."""
        while True:
            for area in (work, root / "scratch"):
                for path in capture_candidates(area):
                    try:
                        contents = path.read_bytes()
                    except FileNotFoundError:
                        continue
                    name = str(path.relative_to(root))
                    digest = hashlib.sha256(contents).hexdigest()
                    if captured.get(name) == digest:
                        continue
                    captured[name] = digest
                    destination = f"{len(capture_log):04d}-{digest[:12]}{path.suffix}"
                    (capture_directory / destination).write_bytes(contents)
                    capture_log.append(
                        {
                            "path": name,
                            "sha256": digest,
                            "capture": destination,
                            "time": time.time(),
                        }
                    )
            if capture_stop.wait(0.1):
                break

    capture_thread = threading.Thread(target=capture_versions)
    capture_thread.start()
    before = inventory(root)
    write_json(output / "inventory-before.json", before)
    input_before = (work / args.input_name).stat()

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
        register("pid", str(process.pid), scratch)
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

    # End remaining run-owned helpers even after the parent returned normally.
    group_cleanup = {
        "process_group": process.pid,
        "term_sent": False,
        "kill_sent": False,
    }
    try:
        os.killpg(process.pid, signal.SIGTERM)
        group_cleanup["term_sent"] = True
        time.sleep(0.2)
        os.killpg(process.pid, signal.SIGKILL)
        group_cleanup["kill_sent"] = True
    except ProcessLookupError:
        pass
    write_json(output / "group-cleanup.json", group_cleanup)
    capture_stop.set()
    capture_thread.join()
    write_json(output / "file-versions.json", capture_log)

    # Preserve every correction-agent rollout and exact before/after changes.
    sessions = root / "home/.codex/sessions"
    if sessions.exists():
        shutil.copytree(sessions, output / "native-sessions")
    shutil.copy2(root / "home/.codex/config.toml", output / "harness-config-after.toml")
    after = inventory(root)
    write_json(output / "inventory-after.json", after)
    # A faulty Skill may remove its source; preserve that failure as evidence.
    source_after = work / args.input_name
    input_after = source_after.stat() if source_after.exists() else None
    write_json(
        output / "input-stat.json",
        {
            "before": {
                "mtime_ns": input_before.st_mtime_ns,
                "inode": input_before.st_ino,
            },
            "after": (
                {"mtime_ns": input_after.st_mtime_ns, "inode": input_after.st_ino}
                if input_after
                else None
            ),
        },
    )
    if args.capture_output_name:
        delivered = work / args.capture_output_name
        if delivered.is_file():
            shutil.copy2(delivered, output / "captured-output.md")
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
