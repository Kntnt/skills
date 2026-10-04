# /// script
# requires-python = ">=3.12"
# ///
"""Capture a genuine ordinary native parent and retain every delegated session.

This task-local evaluator keeps the accepted one-child recorder unchanged.
Parent terminal binding reuses its strict authentic native-v2 checks.
"""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import threading
import time
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any

REPOSITORY: Path = Path(__file__).resolve().parents[5]
HELPER: Path = REPOSITORY / "docs/evaluation/harness/native_dispatch.py"
SPEC: ModuleSpec | None = importlib.util.spec_from_file_location(
    "accepted_native_dispatch", HELPER
)
assert SPEC is not None and SPEC.loader is not None
DISPATCH: ModuleType = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISPATCH)
SKILLS: dict[str, str] = {
    "kntnt": "kntnt",
    **{name: f"editorial/{name}" for name in ("write", "redline", "proofread")},
}


def capture_parent(
    sessions: Path,
    prompt: bytes,
    terminal: bytes,
    model: str,
    effort: str,
    version: str,
) -> tuple[dict[str, Any], bytes]:
    """Bind the sole fresh parent while preserving all child raw identities."""

    # Read every raw session without selecting a matching later result.
    records: dict[Path, list[dict[str, Any]]] = {}
    identities: list[dict[str, Any]] = []
    parents: list[Path] = []
    for path in sorted(sessions.rglob("*.jsonl")):
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        metas = [row["payload"] for row in rows if row.get("type") == "session_meta"]
        if len(metas) != 1:
            raise DISPATCH.CaptureError("missing or ambiguous session metadata")
        meta = metas[0]
        records[path] = rows
        identities.append(
            {
                "path": str(path),
                "retained_path": str(
                    Path("native-sessions") / path.relative_to(sessions)
                ),
                "sha256": DISPATCH.digest(path.read_bytes()),
                "thread_id": meta.get("id"),
                "session_id": meta.get("session_id"),
                "thread_source": meta.get("thread_source"),
                "source": meta.get("source"),
                "parent_thread_id": meta.get("parent_thread_id"),
                "version": meta.get("cli_version"),
                "contexts": [
                    row["payload"] for row in rows if row.get("type") == "turn_context"
                ],
            }
        )
        if (
            meta.get("source") == "exec"
            and meta.get("thread_source") == "user"
            and meta.get("parent_thread_id") is None
        ):
            parents.append(path)

    # Require a unique ordinary parent and reuse the complete native binding.
    if len(parents) != 1:
        raise DISPATCH.CaptureError("missing or ambiguous fresh parent session")
    binding, result = DISPATCH.bind_trace(
        records[parents[0]], prompt, model, effort, version
    )
    if terminal != result:
        raise DISPATCH.CaptureError("parent terminal bytes differ from native final")

    # Reject duplicate, empty or foreign identities instead of merging sessions.
    thread_ids = [entry["thread_id"] for entry in identities]
    if (
        any(not isinstance(identity, str) or not identity for identity in thread_ids)
        or len(set(thread_ids)) != len(thread_ids)
        or any(
            entry["session_id"] != binding["thread_id"]
            or entry["thread_source"] != "subagent"
            for entry in identities
            if entry["thread_id"] != binding["thread_id"]
        )
    ):
        raise DISPATCH.CaptureError("delegate identity is missing or conflicting")

    # Bind every delegate to this captured tree, preserving the raw identities.
    known = {entry["thread_id"] for entry in identities}
    connected = {binding["thread_id"]}
    pending = [entry for entry in identities if entry["thread_id"] not in connected]
    while pending:
        progressed = False
        for entry in pending[:]:
            source = entry["source"]
            spawn = (
                source.get("subagent", {}).get("thread_spawn", {})
                if isinstance(source, dict)
                else {}
            )
            parent = entry["parent_thread_id"]
            if parent not in known or spawn.get("parent_thread_id") != parent:
                raise DISPATCH.CaptureError("delegate ancestry does not agree")
            if (
                entry["version"] != version
                or not entry["contexts"]
                or any(
                    context.get("model") != model or context.get("effort") != effort
                    for context in entry["contexts"]
                )
            ):
                raise DISPATCH.CaptureError("delegate seat missing or different")
            if parent in connected:
                connected.add(entry["thread_id"])
                pending.remove(entry)
                progressed = True
        if not progressed:
            raise DISPATCH.CaptureError("delegate ancestry is disconnected or cyclic")

    return {"parent": binding, "sessions": identities}, result


def run(args: argparse.Namespace, prompt: bytes) -> bytes:
    """Record one ordinary native attempt with real HOME and immutable product bytes."""

    # Register this new group before any native preparation or blocking work.
    packet: Path = args.packet.resolve()
    packet.mkdir(parents=True, exist_ok=False)
    env: dict[str, str] = DISPATCH.environment(packet)
    env.update(CODEX_HOME=str(packet / "runtime/native"))
    env.pop("CODEX_THREAD_ID", None)
    env.pop("CODEX_SESSION_ID", None)
    if os.getpid() != os.getpgrp():
        os.setsid()
    DISPATCH.register(os.getpid(), args.cleanup_script, env, packet)
    child: subprocess.Popen[bytes] | None = None
    runtime = packet / "runtime"
    native_home = runtime / "native"
    work = packet / "work"
    receipt: dict[str, Any] = {
        "status": "failed",
        "method": "ordinary-native-parent",
        "recorder_path": str(Path(__file__).resolve()),
        "recorder_sha256": DISPATCH.digest(Path(__file__).read_bytes()),
        "helper_path": str(HELPER),
        "helper_sha256": DISPATCH.digest(HELPER.read_bytes()),
        "requested_revision": args.revision,
        "model": args.model,
        "effort": args.effort,
        "cli_version": args.version,
        "timeout_seconds": args.timeout,
        "prompt_sha256": DISPATCH.digest(prompt),
        "materials": str(args.materials.resolve()),
    }
    started = time.monotonic()
    sampling_stop = threading.Event()
    sampling_thread: threading.Thread | None = None
    versions: list[dict[str, Any]] = []
    sampled: dict[str, str] = {}
    sampling_errors: list[str] = []

    def sample_versions() -> None:
        """Retain observed working-text bytes without asserting continuous coverage."""

        # Sample material and command scratch, excluding installed instructions.
        destination = packet / "file-versions"
        destination.mkdir()
        while not sampling_stop.is_set():
            for root in (work, Path(env["TMPDIR"])):
                for path in sorted(root.rglob("*")):
                    if path.is_relative_to(work / ".agents") or path.is_relative_to(
                        work / ".git"
                    ):
                        continue
                    try:
                        if not path.is_file() or path.is_symlink():
                            continue
                        contents = path.read_bytes()
                        contents.decode("utf-8")
                    except (FileNotFoundError, UnicodeDecodeError, OSError):
                        # Disappearing or non-text files supply no sampled version.
                        continue
                    sha = DISPATCH.digest(contents)
                    if sampled.get(str(path)) == sha:
                        continue
                    sampled[str(path)] = sha
                    name = f"observed-{len(versions):04d}-{sha[:12]}{path.suffix}"
                    (destination / name).write_bytes(contents)
                    versions.append(
                        {
                            "path": str(path),
                            "sha256": sha,
                            "capture": name,
                            "observed_monotonic": time.monotonic(),
                        }
                    )
            sampling_stop.wait(0.1)

    def observe_versions() -> None:
        """Carry any observer failure across the thread boundary to the receipt."""

        # A background exception must reject acquisition instead of silently passing.
        try:
            sample_versions()
        except Exception as exc:  # noqa: BLE001 — fail closed across the thread boundary
            sampling_errors.append(str(exc))
            sampling_stop.set()

    try:
        # Preserve the exact task even if immutable staging fails before native launch.
        (packet / "prompt.txt").write_bytes(prompt)
        if any((args.materials / name).exists() for name in (".agents", ".git")):
            raise DISPATCH.CaptureError(
                "materials cannot replace installed Skills or git metadata"
            )

        # Stage the declared commit, copying no mutable runtime Skill instructions.
        revision = subprocess.check_output(
            ["git", "rev-parse", f"{args.revision}^{{commit}}"],
            cwd=REPOSITORY,
            text=True,
            timeout=15,
        ).strip()
        archive = subprocess.check_output(
            ["git", "archive", revision, *(f"skills/{p}" for p in SKILLS.values())],
            cwd=REPOSITORY,
            timeout=30,
        )
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(packet / "export", filter="data")
        for name, source in SKILLS.items():
            shutil.copytree(
                packet / "export/skills" / source, work / ".agents/skills" / name
            )
        shutil.copytree(args.materials, work, dirs_exist_ok=True)
        subprocess.run(["git", "init", "-q", str(work)], cwd=packet, check=True)
        context = (
            "# Installed editorial Skills\n\n"
            "For a `/write`, `/redline` or `/proofread` invocation, read and execute "
            "the corresponding `.agents/skills/<name>/SKILL.md` in this project. "
            "These are the installed Skills. Follow their shipped instructions.\n"
        )
        (work / "AGENTS.md").write_text(context)
        (packet / "harness-context.md").write_text(context)

        # Preserve real HOME and keep private authentication and caches separate.
        native_home.mkdir(parents=True)
        for key in (
            "TMPDIR",
            "UV_CACHE_DIR",
            "UV_TOOL_DIR",
            "UV_TOOL_BIN_DIR",
            "UV_PYTHON_INSTALL_DIR",
            "UV_PROJECT_ENVIRONMENT",
            "XDG_CACHE_HOME",
            "XDG_DATA_HOME",
            "XDG_CONFIG_HOME",
        ):
            Path(env[key]).mkdir(exist_ok=True)
        for name in ("auth.json", "hooks.json", "config.toml"):
            source = args.auth_home / name
            if name != "config.toml" or source.is_file():
                shutil.copy2(source, native_home / name)
        (native_home / "auth.json").chmod(0o600)
        actual_version = subprocess.check_output(
            [str(args.native), "--version"], cwd=work, env=env, text=True, timeout=15
        ).strip()
        if actual_version != f"codex-cli {args.version}":
            raise DISPATCH.CaptureError("installed CLI differs from declared version")
        roots = [packet, *[path.resolve() for path in args.inventory_root]]
        credentials = [native_home / "auth.json"]
        DISPATCH.write_json(
            packet / "inventory-before.json", DISPATCH.inventory(roots, credentials)
        )

        # Begin stage observation before the native task can create working files.
        sampling_thread = threading.Thread(target=observe_versions)
        sampling_thread.start()

        # Start one genuine parent with lifecycle hooks and bounded writable roots.
        command = [
            str(args.native),
            "exec",
            "-C",
            str(work),
            "--skip-git-repo-check",
            "-s",
            "workspace-write",
            "--add-dir",
            str(runtime),
            "--dangerously-bypass-hook-trust",
            "--enable",
            "hooks",
            "--json",
            "--output-last-message",
            str(packet / "terminal.txt"),
            "-m",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.effort}"',
            "-c",
            "sandbox_workspace_write.network_access=true",
            "-",
        ]
        receipt.update(revision=revision, command=command, real_home=env["HOME"])
        with (
            (packet / "events.jsonl").open("wb") as stdout,
            (packet / "stderr.txt").open("wb") as stderr,
        ):
            child = subprocess.Popen(
                command,
                cwd=work,
                env=env,
                stdin=subprocess.PIPE,
                stdout=stdout,
                stderr=stderr,
                start_new_session=True,
            )
            DISPATCH.register(child.pid, args.cleanup_script, env, packet)
            receipt.update(pid=child.pid, pgid=child.pid)
            child.communicate(prompt, timeout=args.timeout)
        receipt["exit"] = child.returncode
        if child.returncode:
            raise DISPATCH.CaptureError("ordinary native parent exited unsuccessfully")

        # Bind the exact parent task/result and all genuinely captured descendants.
        capture, result = capture_parent(
            native_home / "sessions",
            prompt,
            (packet / "terminal.txt").read_bytes(),
            args.model,
            args.effort,
            args.version,
        )
        receipt.update(status="complete", capture=capture)
        (packet / "result.txt").write_bytes(result)
        return result

    # Retain failed native acquisition without a retry or inferred parent result.
    except Exception as exc:
        # Broad capture keeps unexpected preparation/transport failures as evidence.
        receipt["reason"] = str(exc)
        raise
    finally:
        # Stop only the known group before retaining native state or removing secrets.
        cleanup_error: Exception | None = None
        if child is not None:
            try:
                DISPATCH.stop_owned(child)
            except Exception as exc:  # noqa: BLE001 — preserve unresolved ownership
                # Ownership errors retain reachable private state and failed receipts.
                cleanup_error = exc
                receipt.update(status="failed", cleanup_reason=str(exc))
                receipt["reason"] = str(exc)
                DISPATCH.write_json(
                    packet / "cleanup-failed.json",
                    {"pgid": child.pid, "runtime": str(runtime), "reason": str(exc)},
                )
        sampling_stop.set()
        if sampling_thread is not None:
            sampling_thread.join()
        observer_error: Exception | None = None
        if sampling_errors:
            observer_error = DISPATCH.CaptureError("stage observer failed")
            receipt.update(status="failed", observer_reason=sampling_errors)
            if cleanup_error is None:
                receipt["reason"] = str(observer_error)
            DISPATCH.write_json(packet / "sampling-errors.json", sampling_errors)
        DISPATCH.write_json(packet / "file-versions.json", versions)
        if (native_home / "sessions").exists():
            shutil.copytree(native_home / "sessions", packet / "native-sessions")
        receipt["elapsed_seconds"] = time.monotonic() - started
        DISPATCH.write_json(packet / "receipt.json", receipt)
        DISPATCH.write_json(
            packet / "inventory-after.json",
            DISPATCH.inventory(
                [packet, *[path.resolve() for path in args.inventory_root]],
                [native_home / "auth.json"],
            ),
        )
        if runtime.exists() and cleanup_error is None:
            print(f"Delete owned disposable runtime: {runtime}", file=sys.stderr)
            shutil.rmtree(runtime)
            DISPATCH.write_json(
                packet / "cleanup.json",
                {"deleted_literal_path": str(runtime), "exists": runtime.exists()},
            )
        if cleanup_error is not None:
            raise cleanup_error
        if observer_error is not None:
            raise observer_error


def main() -> int:
    """Expose the finite parent acquisition boundary without rewriting its prompt."""

    # Declare the immutable install, supplied materials and actual native seat.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--materials", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument(
        "--native", type=Path, default=Path(shutil.which("codex") or "codex")
    )
    parser.add_argument("--auth-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument(
        "--cleanup-script",
        type=Path,
        default=Path.home()
        / ".agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py",
    )
    parser.add_argument("--inventory-root", type=Path, action="append", default=[])
    parser.add_argument("--timeout", type=float, required=True)
    args = parser.parse_args()

    # Return only complete parent bytes; failure diagnostics remain separate.
    try:
        result = run(args, args.prompt.read_bytes())
    except Exception as exc:  # noqa: BLE001 — report all acquisition failures as explicit exits
        # Unanticipated native/preparation failures must also be explicit exits.
        print(f"Ordinary parent acquisition unavailable: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
