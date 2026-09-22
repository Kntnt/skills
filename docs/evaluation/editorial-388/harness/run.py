# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Run one staged Skill invocation in a Claude-native Harness, and keep its trace.

A Claude-family evaluation made from an ordinary session cannot answer `T1` or
`R2`, because the session that starts a subagent cannot read that subagent's
transcript. Claude Code writes both records to disk — the session's own and one
per subagent, beside a `.meta.json` naming the call that started it — so a run
launched with its own configuration directory has every one of them in a place
this runner can preserve. That is the whole of what this file adds: one real
invocation, staged from a frozen revision, with the complete native trace kept
where an evaluator reads it afterwards (issue #388).

It judges nothing and writes no record. What it produces is an evidence packet:
the exact invocation material, the revisions it was staged from, the identity
the Harness resolved, the before-and-after inventories of every writable root,
the reply, and `transcripts/` holding the parent record and every nested agent.
`trace_index.py` beside this file turns those transcripts into the index and the
completeness status an evaluator reads; it is run here so the packet is
self-contained, and can be run again over a saved packet.

The run is isolated rather than sandboxed. Its `HOME`, its Claude configuration
directory, its temporary directory and its caches are all inside one private
root, which is inventoried before and after and removed on every exit; the
Skills it can reach are the staged ones alone, and no hook, no Measurement store
and no configuration of the machine's own is in scope. What isolation does not
do is stop a run writing outside that root, which is why the packet carries the
inventories rather than a claim: an effect outside the root is read from the
Skill's own delivery account and from the working copy, exactly as before.

Provider isolation (`docs/evaluation/protocol.md`) holds by construction: this
runner starts `claude` and nothing else, so it belongs to a Claude session and
a Claude-family evaluation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent

# The Skills one staged installation holds. The Manager comes with them because
# every Skill's shim finds the engine beside itself, and Proofread comes because
# Redline's closing pass invokes the installed Skill next to it.
STAGED_SKILLS = {
    "kntnt": "kntnt",
    **{
        name: f"editorial/{name}"
        for name in ("write", "redline", "proofread", "unslop")
    },
}

# Where the Harness keeps the credential a run authenticates with. The keychain
# entry is per configuration directory, so a run with its own directory has none
# and is answered with the file form the Harness also accepts.
KEYCHAIN_SERVICE = "Claude Code-credentials"
CREDENTIALS = ".credentials.json"

# What must not reach the run: this session's own Harness identity, and every
# variable of this collection's that would point a staged Skill at the machine's
# installation instead of the staged one.
STRIPPED_PREFIXES = ("KNTNT_", "CLAUDE_", "ANTHROPIC_")
STRIPPED_NAMES = frozenset({"CLAUDECODE"})


def write_json(path: Path, value: object) -> None:
    """Persist evaluator evidence outside the run's own writable root."""

    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def inventory(root: Path, secret: Path) -> dict[str, dict[str, Any]]:
    """Hash every path under *root*, without following links or publishing *secret*.

    The credential keeps its mode and size alone, so that a packet committed to
    the repository cannot carry it and a change to it is still visible.
    """

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
            if path != secret:
                item["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            item.update(type="other")
        result[str(path.relative_to(root))] = item
    return result


def credential(destination: Path) -> str:
    """Give the staged configuration directory a credential of its own.

    Returns where it came from, so the packet says how the run authenticated
    without saying what with.
    """

    # The file form first: a machine that keeps it on disk needs no keychain.
    installed = Path.home() / ".claude" / CREDENTIALS
    if installed.is_file():
        shutil.copy2(installed, destination)
        destination.chmod(0o600)
        return str(installed)

    # The working directory is the repository, which nothing in this run removes.
    found = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=True,
    )
    stored = json.loads(found.stdout)
    handle = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(handle, "w") as opened:
        json.dump({"claudeAiOauth": stored["claudeAiOauth"]}, opened)
    return f"keychain:{KEYCHAIN_SERVICE}"


def stage(root: Path, revision: str) -> None:
    """Export the Skills of one frozen revision into the run's own installation.

    `git archive` rather than a copy of the working tree, so that what the run
    reads is the revision the packet names and never whatever is checked out.
    """

    archive = subprocess.check_output(
        [
            "git",
            "archive",
            revision,
            *(f"skills/{path}" for path in STAGED_SKILLS.values()),
        ],
        cwd=REPOSITORY,
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        bundle.extractall(root / "export", filter="data")
    skills = root / "home" / ".claude" / "skills"
    for name, source in STAGED_SKILLS.items():
        shutil.copytree(root / "export" / "skills" / source, skills / name)
    shutil.rmtree(root / "export")


def environment(root: Path) -> dict[str, str]:
    """Return the environment the run sees, with every writable path inside *root*."""

    kept = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(STRIPPED_PREFIXES) and key not in STRIPPED_NAMES
    }
    home = root / "home"
    kept.update(
        HOME=str(home),
        CLAUDE_CONFIG_DIR=str(home / ".claude"),
        TMPDIR=str(root / "scratch" / "tmp"),
        UV_CACHE_DIR=str(root / "scratch" / "uv-cache"),
        UV_PYTHON_INSTALL_DIR=str(root / "scratch" / "data" / "uv" / "python"),
        XDG_DATA_HOME=str(root / "scratch" / "data"),
        XDG_CACHE_HOME=str(root / "scratch" / "cache"),
        XDG_CONFIG_HOME=str(home / ".config"),
    )
    return kept


def harvest(root: Path, session: str, packet: Path) -> dict[str, Any]:
    """Copy the native records of one session out of the run's root.

    Everything the Harness wrote for this session is preserved verbatim: its own
    transcript, every subagent transcript with the `.meta.json` that names the
    call which started it, and whatever else it kept beside them — offloaded
    tool results among it. What was not found is named rather than passed over.
    """

    transcripts = packet / "transcripts"
    transcripts.mkdir(parents=True, exist_ok=True)
    projects = root / "home" / ".claude" / "projects"
    found = sorted(projects.rglob(f"{session}.jsonl")) if projects.is_dir() else []
    missing: list[str] = []

    if not found:
        missing.append("parent-transcript")
        return {
            "parent_transcript": None,
            "subagent_transcripts": 0,
            "missing": missing,
        }
    parent = found[0]
    shutil.copy2(parent, transcripts / "parent.jsonl")

    # The directory beside the parent record holds the nested agents.
    beside = parent.with_suffix("")
    subagents = beside / "subagents"
    kept = 0
    # A run that started no subagent has no such directory, which is the run
    # having delegated nothing rather than a trace segment gone astray; a
    # delegation whose child is absent is `trace-status.json`'s to report.
    if subagents.is_dir():
        shutil.copytree(subagents, transcripts / "subagents")
        kept = len(list((transcripts / "subagents").glob("agent-*.jsonl")))
    for extra in sorted(beside.iterdir()) if beside.is_dir() else []:
        if extra.name == "subagents":
            continue
        target = transcripts / "extra" / extra.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(extra, target) if extra.is_dir() else shutil.copy2(
            extra, target
        )

    return {
        "parent_transcript": str(parent.relative_to(root)),
        "subagent_transcripts": kept,
        "subagents_directory": "present" if subagents.is_dir() else "absent",
        "missing": missing,
    }


def response_of(stream: Path) -> tuple[str, dict[str, Any]]:
    """Return the run's final reply and the Harness's own result event."""

    reply = ""
    result: dict[str, Any] = {}
    for line in stream.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            event = json.loads(stripped)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            result = event
            reply = event.get("result") or ""
    return reply, result


def index(packet: Path) -> dict[str, Any]:
    """Run the indexer beside this file over the finished packet."""

    specification = importlib.util.spec_from_file_location(
        "trace_index", HERE / "trace_index.py"
    )
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    sys.modules["trace_index"] = module
    specification.loader.exec_module(module)
    module.main([str(packet)])
    return dict(module.read_packet(packet)["status"])


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read what the evaluator froze for this run, and never a model's own choice."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--corpus-revision", required=True)
    parser.add_argument("--invocation", required=True)
    parser.add_argument("--instruction", default=None)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--input-name", default="source.md")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="opus")
    parser.add_argument("--effort", default="high")
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--capture-output-name", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Stage one invocation, run it, preserve its trace, and clean up after it."""

    arguments = parse_args(argv)
    packet = arguments.output.resolve()
    packet.mkdir(parents=True, exist_ok=False)

    # The two revisions are resolved to full commits, so the packet names what
    # was staged rather than whatever the branch has moved to since.
    revisions = {
        name: subprocess.check_output(
            ["git", "rev-parse", f"{value}^{{commit}}"], cwd=REPOSITORY, text=True
        ).strip()
        for name, value in (
            ("instruction_revision", arguments.revision),
            ("corpus_revision", arguments.corpus_revision),
        )
    }
    version = subprocess.check_output(
        ["claude", "--version"], cwd=REPOSITORY, text=True
    ).strip()

    root = Path(tempfile.mkdtemp(prefix="kntnt-editorial-388-run-")).resolve()
    try:
        return _run(arguments, packet, root, revisions, version)
    finally:
        shutil.rmtree(root, ignore_errors=True)
        write_json(
            packet / "cleanup.json",
            {
                "root": str(root),
                "removed": not root.exists(),
                "removed_only": str(root),
            },
        )


def _run(
    arguments: argparse.Namespace,
    packet: Path,
    root: Path,
    revisions: dict[str, str],
    version: str,
) -> int:
    """Everything between the private root existing and the packet being whole."""

    # The staged installation, the working directory the invocation is typed in,
    # and the scratch every cache is pointed at.
    for directory in [
        "home/.claude",
        "work",
        "scratch/tmp",
        "scratch/cache",
        "scratch/data",
        "scratch/uv-cache",
    ]:
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / "home" / ".claude").chmod(0o700)
    stage(root, revisions["instruction_revision"])
    work = root / "work"
    shutil.copy2(arguments.input, work / arguments.input_name)
    shutil.copy2(arguments.input, packet / "supplied-input.md")
    secret = root / "home" / ".claude" / CREDENTIALS
    source = credential(secret)

    # The prompt is the Formal Invocation as an evaluator types it, with the
    # Contextual Instruction after it where the fixture has one and nothing else
    # at all: framing added here is guidance the run was not supposed to get.
    prompt = arguments.invocation
    if arguments.instruction:
        prompt = f"{prompt}\n{arguments.instruction}"
    (packet / "invocation.txt").write_text(arguments.invocation + "\n")
    (packet / "contextual-instruction.txt").write_text(
        (arguments.instruction or "none") + "\n"
    )
    (packet / "prompt.txt").write_text(prompt + "\n")

    session = str(uuid.uuid4())
    command = [
        "claude",
        "--print",
        "--session-id",
        session,
        "--model",
        arguments.model,
        "--effort",
        arguments.effort,
        "--dangerously-skip-permissions",
        "--strict-mcp-config",
        "--output-format",
        "stream-json",
        "--verbose",
        "--add-dir",
        str(root / "scratch"),
    ]
    running = environment(root)
    write_json(
        packet / "run.json",
        {
            **revisions,
            "harness": version,
            "requested_identity": {
                "model": arguments.model,
                "effort": arguments.effort,
            },
            "session_id": session,
            "credential_source": source,
            "staged_skills": sorted(STAGED_SKILLS),
            "input_name": arguments.input_name,
            "input_source": str(arguments.input.resolve()),
            "working_directory": str(work),
            "argv": command,
            "prompt_on": "stdin",
            "environment": {
                key: running[key]
                for key in [
                    "HOME",
                    "CLAUDE_CONFIG_DIR",
                    "TMPDIR",
                    "UV_CACHE_DIR",
                    "UV_PYTHON_INSTALL_DIR",
                    "XDG_DATA_HOME",
                    "XDG_CACHE_HOME",
                    "XDG_CONFIG_HOME",
                ]
            },
            "note": "The identity requested here is a request; the seats in trace-index.json are what ran.",
        },
    )
    before = inventory(root, secret)
    write_json(packet / "inventory-before.json", before)

    # The run itself, in a process group of its own so that a timeout or an
    # interruption stops everything it started rather than the launcher alone.
    started = time.monotonic()
    timed_out = False
    interrupted = False
    with (
        (packet / "stream.jsonl").open("w") as output,
        (packet / "stderr.txt").open("w") as errors,
    ):
        process = subprocess.Popen(
            command,
            cwd=work,
            env=running,
            stdin=subprocess.PIPE,
            stdout=output,
            stderr=errors,
            text=True,
            start_new_session=True,
        )
        write_json(
            packet / "process.json", {"pid": process.pid, "process_group": process.pid}
        )
        try:
            process.communicate(prompt, timeout=arguments.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _stop(process)
        except KeyboardInterrupt:
            interrupted = True
            _stop(process)

    # Everything the Harness recorded, copied out before the root is removed.
    kept = harvest(root, session, packet)
    reply, result = response_of(packet / "stream.jsonl")
    (packet / "response.txt").write_text(reply)
    after = inventory(root, secret)
    write_json(packet / "inventory-after.json", after)
    write_json(
        packet / "filesystem-changes.json",
        {
            "created": {path: after[path] for path in after.keys() - before.keys()},
            "removed": {path: before[path] for path in before.keys() - after.keys()},
            "changed": {
                path: {"before": before[path], "after": after[path]}
                for path in before.keys() & after.keys()
                if before[path] != after[path]
            },
            "note": "Harness, cache and Skill effects are separated by reading trace-index.json; nothing here is a Skill artifact on its own.",
        },
    )
    if arguments.capture_output_name:
        delivered = work / arguments.capture_output_name
        if delivered.is_file():
            shutil.copy2(delivered, packet / "captured-output.md")

    outcome = {
        "returncode": process.returncode,
        "timed_out": timed_out,
        "interrupted": interrupted,
        "duration_seconds": round(time.monotonic() - started, 2),
        "harness_result": {
            key: result.get(key)
            for key in (
                "is_error",
                "subtype",
                "num_turns",
                "total_cost_usd",
                "terminal_reason",
            )
        },
        "transcripts": kept,
        "process_group_gone": _gone(process.pid),
    }
    write_json(packet / "result.json", outcome)
    status = index(packet)
    write_json(
        packet / "packet.json",
        {
            "schema_version": 1,
            "ticket": "#388",
            "produced_by": "docs/evaluation/editorial-388/harness/run.py",
            "invocation": arguments.invocation,
            "status": status["status"],
            "reasons": status["reasons"],
        },
    )
    print(json.dumps({**outcome, "trace": status}, ensure_ascii=False), flush=True)
    return process.returncode or int(timed_out or interrupted)


def _stop(process: subprocess.Popen[str]) -> None:
    """End the run's whole process group, politely and then not."""

    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=15)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()


def _gone(group: int) -> bool:
    """Whether the run's process group has no member left."""

    try:
        os.killpg(group, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    return False


if __name__ == "__main__":
    raise SystemExit(main())
