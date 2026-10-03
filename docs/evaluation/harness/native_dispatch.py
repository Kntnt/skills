# /// script
# requires-python = ">=3.12"
# ///
"""Acquire a disclosed controlled dispatch through fresh native Codex stdin.

This evaluator helper does not change a shipped Skill. A successful receipt
establishes this instrumented boundary, never an opaque native spawn's input.
"""

from __future__ import annotations

import argparse
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


class CaptureError(Exception):
    """The authentic native records do not establish a complete dispatch."""


def digest(data: bytes) -> str:
    """Bind evidence without changing its bytes."""
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    """Write recorder metadata separately from native receipts."""
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def message_bytes(payload: dict[str, Any]) -> bytes:
    """Read only complete plaintext native message blocks."""
    blocks = payload.get("content", [])
    if not blocks or any(
        block.get("type") not in ("input_text", "output_text", "text")
        or not isinstance(block.get("text"), str)
        for block in blocks
    ):
        raise CaptureError("message contains unavailable or non-text content")
    return "".join(block["text"] for block in blocks).encode("utf-8")


def bind_trace(
    records: list[dict[str, Any]],
    prompt: bytes,
    model: str,
    effort: str,
    version: str,
) -> tuple[dict[str, Any], bytes]:
    """Require input, seat and terminal evidence in one fresh native thread."""
    metas = [row["payload"] for row in records if row.get("type") == "session_meta"]
    contexts = [row["payload"] for row in records if row.get("type") == "turn_context"]
    if len(metas) != 1 or not contexts:
        raise CaptureError("missing or ambiguous native thread/context")
    meta = metas[0]
    if meta.get("parent_thread_id") or meta.get("source") != "exec":
        raise CaptureError("native session is not a fresh top-level exec")
    if meta.get("cli_version") != version:
        raise CaptureError("actual native version differs from freeze")
    if len({context.get("turn_id") for context in contexts}) != 1:
        raise CaptureError("multiple native turns")
    if any(
        context.get("model") != model or context.get("effort") != effort
        for context in contexts
    ):
        raise CaptureError("actual native model/effort differs from freeze")
    turn_id = contexts[0]["turn_id"]
    inputs: list[tuple[int, bytes]] = []
    finals: list[tuple[int, bytes]] = []
    complete: list[tuple[int, dict[str, Any]]] = []
    for ordinal, row in enumerate(records, 1):
        payload = row.get("payload", {})
        if row.get("type") == "response_item" and payload.get("type") == "message":
            if payload.get("role") == "user":
                try:
                    text = message_bytes(payload)
                except CaptureError:
                    continue
                if text == prompt:
                    inputs.append((ordinal, text))
            if (
                payload.get("role") == "assistant"
                and payload.get("phase") == "final_answer"
            ):
                finals.append((ordinal, message_bytes(payload)))
        if row.get("type") == "event_msg" and payload.get("type") == "task_complete":
            complete.append((ordinal, payload))
    if len(inputs) != 1 or len(finals) != 1 or len(complete) != 1:
        raise CaptureError("missing or ambiguous exact input/final/completion")
    input_ordinal, _ = inputs[0]
    final_ordinal, result = finals[0]
    completion_ordinal, completion = complete[0]
    if not input_ordinal < final_ordinal < completion_ordinal:
        raise CaptureError("native record order does not bind input to result")
    if (
        completion.get("turn_id") != turn_id
        or completion.get("last_agent_message", "").encode() != result
    ):
        raise CaptureError("native terminal content or turn identity disagrees")
    return {
        "thread_id": meta.get("id"),
        "turn_id": turn_id,
        "input_ordinal": input_ordinal,
        "final_ordinal": final_ordinal,
        "completion_ordinal": completion_ordinal,
        "input_sha256": digest(prompt),
        "result_sha256": digest(result),
        "model": model,
        "effort": effort,
        "cli_version": version,
    }, result


def inventory(roots: list[Path]) -> dict[str, Any]:
    """Inventory all staged roots; only the known auth secret has no digest."""
    result: dict[str, Any] = {}
    for root in roots:
        for path in sorted(root.rglob("*")):
            key = str(path)
            if path.is_symlink():
                result[key] = {"symlink": os.readlink(path)}
            elif path.is_file():
                result[key] = {
                    "bytes": path.stat().st_size,
                    "sha256": None
                    if path.name == "auth.json"
                    else digest(path.read_bytes()),
                }
    return result


def stop_owned(child: subprocess.Popen[bytes]) -> None:
    """End an owned process group even when its leader already exited."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(child.pid, sig)
        except ProcessLookupError:
            return
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            continue
        # A completed leader can have surviving descendants.
        try:
            os.killpg(child.pid, 0)
        except ProcessLookupError:
            return
    raise CaptureError("owned native process group remains after termination")


def register(pid: int, cleanup: Path, env: dict[str, str], packet: Path) -> None:
    """Register each group before supplying a native task."""
    receipt = subprocess.run(
        [
            "uv",
            "run",
            str(cleanup),
            "add",
            "pid",
            str(pid),
            "Prospective native evaluation dispatch",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    with (packet / "registrations.jsonl").open("a") as stream:
        stream.write(
            json.dumps({"pid": pid, "pgid": os.getpgid(pid), "receipt": receipt.stdout})
            + "\n"
        )


def acquire(args: argparse.Namespace, prompt: bytes) -> bytes:
    """Capture one attempt, retaining unsuccessful receipts without retrying."""
    prompt.decode("utf-8")
    if not prompt:
        raise CaptureError("empty dispatch brief")
    packet: Path = args.packet.resolve()
    runtime = packet / "runtime"
    native_home = runtime / "home" / ".codex"
    native_home.mkdir(parents=True)
    native = str(args.native.resolve())
    actual_version = subprocess.check_output([native, "--version"], text=True).strip()
    if actual_version != f"codex-cli {args.version}":
        raise CaptureError("installed CLI differs from frozen version")
    write_json(
        packet / "request.json",
        {
            "method": "instrumented-native-stdin",
            "model": args.model,
            "effort": args.effort,
            "version": args.version,
            "prompt_sha256": digest(prompt),
            "prompt_bytes": len(prompt),
            "parent": args.parent,
            "role": args.role,
            "cwd": str(args.cwd.resolve()),
            "timeout_seconds": args.timeout,
        },
    )
    hooks = args.auth_home / "hooks.json"
    if not hooks.is_file():
        raise CaptureError("existing lifecycle hook configuration unavailable")
    shutil.copy2(hooks, native_home / "hooks.json")
    config = args.auth_home / "config.toml"
    if config.is_file():
        shutil.copy2(config, native_home / "config.toml")
    write_json(
        packet / "configuration.json",
        {
            "hooks_sha256": digest(hooks.read_bytes()),
            "config_sha256": digest(config.read_bytes()) if config.is_file() else None,
            "hooks_enabled_by_command": True,
        },
    )
    shutil.copy2(args.auth_home / "auth.json", native_home / "auth.json")
    (native_home / "auth.json").chmod(0o600)
    env = dict(os.environ)
    env.update(
        {
            "HOME": str(runtime / "home"),
            "CODEX_HOME": str(native_home),
            "KNTNT_HOME": str(packet / "lifecycle"),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    for name in (
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
        target = runtime / name.lower()
        target.mkdir()
        env[name] = str(target)
    roots = [args.cwd.resolve(), runtime, *[p.resolve() for p in args.inventory_root]]
    write_json(packet / "inventory-before.json", inventory(roots))
    if os.getpid() != os.getpgrp():
        os.setsid()
    register(os.getpid(), args.cleanup_script, env, packet)
    command = [
        native,
        "exec",
        "-C",
        str(args.cwd.resolve()),
        "--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox",
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
        "-",
    ]
    child: subprocess.Popen[bytes] | None = None
    started = time.monotonic()
    receipt: dict[str, Any] = {
        "status": "failed",
        "command": command,
        "runtime": str(runtime),
    }
    try:
        with (
            (packet / "events.jsonl").open("wb") as stdout,
            (packet / "stderr.txt").open("wb") as stderr,
        ):
            child = subprocess.Popen(
                command,
                env=env,
                cwd=args.cwd,
                stdin=subprocess.PIPE,
                stdout=stdout,
                stderr=stderr,
                start_new_session=True,
            )
            receipt.update({"pid": child.pid, "pgid": child.pid})
            register(child.pid, args.cleanup_script, env, packet)
            child.communicate(prompt, timeout=args.timeout)
        receipt["exit"] = child.returncode
        if child.returncode:
            raise CaptureError("native child did not complete successfully")
        sessions = sorted((native_home / "sessions").rglob("*.jsonl"))
        if len(sessions) != 1:
            raise CaptureError("missing or extra native sessions")
        records = [json.loads(line) for line in sessions[0].read_text().splitlines()]
        binding, result = bind_trace(
            records, prompt, args.model, args.effort, args.version
        )
        terminal = (packet / "terminal.txt").read_bytes()
        if terminal != result:
            raise CaptureError("CLI terminal bytes differ from native final message")
        receipt.update({"status": "complete", "binding": binding})
        (packet / "result.txt").write_bytes(result)
        return result
    except (CaptureError, subprocess.TimeoutExpired) as exc:
        receipt["reason"] = str(exc)
        raise CaptureError(str(exc)) from exc
    finally:
        if child is not None:
            try:
                stop_owned(child)
            except CaptureError:
                write_json(
                    packet / "cleanup-failed.json",
                    {"pgid": child.pid, "runtime": str(runtime)},
                )
                raise
        receipt["elapsed_seconds"] = time.monotonic() - started
        sessions_root = native_home / "sessions"
        if sessions_root.exists():
            shutil.copytree(sessions_root, packet / "native-sessions")
        write_json(packet / "inventory-after.json", inventory(roots))
        write_json(packet / "receipt.json", receipt)


def run(args: argparse.Namespace, prompt: bytes) -> bytes:
    """Clean private credentials on preparation failures as well as completion."""
    packet = args.packet.resolve()
    packet.mkdir(parents=True, exist_ok=False)
    (packet / "prompt.txt").write_bytes(prompt)
    runtime = packet / "runtime"
    try:
        return acquire(args, prompt)
    except Exception as exc:
        if not (packet / "receipt.json").exists():
            write_json(
                packet / "receipt.json", {"status": "failed", "reason": str(exc)}
            )
        raise
    finally:
        if runtime.exists() and not (packet / "cleanup-failed.json").exists():
            print(f"Delete owned disposable runtime: {runtime}", file=sys.stderr)
            shutil.rmtree(runtime)
            write_json(
                packet / "cleanup.json",
                {
                    "deleted_literal_path": str(runtime),
                    "exists": runtime.exists(),
                    "owned_group_ended": True,
                },
            )


def main() -> int:
    """Print only the complete child return on successful acquisition."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--timeout", type=float, default=180)
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
    args = parser.parse_args()
    try:
        result = run(args, sys.stdin.buffer.read())
    except (CaptureError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Native acquisition unavailable: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
