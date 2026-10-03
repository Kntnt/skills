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
import stat
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


def retained_message(row: dict[str, Any], turn_id: str, role: str) -> bytes:
    """Require complete retained content and agreeing message/turn identities."""
    payload = row["payload"]
    identity = payload.get("id")
    retained = row.get("metadata", {}).get("retained_source", {})
    if (
        not isinstance(identity, str)
        or not identity
        or payload.get("internal_chat_message_metadata_passthrough", {}).get("turn_id")
        != turn_id
        or retained.get("complete") is not True
        or retained.get("id")
        != {"message_id": identity, "turn_id": turn_id, "role": role}
    ):
        raise CaptureError("missing or conflicting retained message identity")
    return message_bytes(payload)


def native_item_bytes(payload: dict[str, Any], thread_id: str, turn_id: str) -> bytes:
    """Read the native v2 completed item independently of its retained copy."""
    item = payload["item"]
    expected_type = "text" if item["type"] == "UserMessage" else "Text"
    if payload.get("thread_id") != thread_id or payload.get("turn_id") != turn_id:
        raise CaptureError("native completed item identity disagrees")
    if not isinstance(item.get("id"), str) or not item["id"]:
        raise CaptureError("native completed item identity unavailable")
    blocks = item.get("content", [])
    if not blocks or any(
        block.get("type") != expected_type or not isinstance(block.get("text"), str)
        for block in blocks
    ):
        raise CaptureError("native completed item plaintext unavailable")
    return "".join(block["text"] for block in blocks).encode("utf-8")


def bind_trace(
    records: list[dict[str, Any]], prompt: bytes, model: str, effort: str, version: str
) -> tuple[dict[str, Any], bytes]:
    """Bind one initial v2 task and both final representations in a fresh turn."""
    # Establish the actual fresh session and turn before selecting any content.
    metas = [row["payload"] for row in records if row.get("type") == "session_meta"]
    contexts = [
        (ordinal, row["payload"])
        for ordinal, row in enumerate(records, 1)
        if row.get("type") == "turn_context"
    ]
    if len(metas) != 1 or len(contexts) != 1:
        raise CaptureError("missing or ambiguous native thread/context")
    meta = metas[0]
    thread_id = meta.get("id")
    if (
        not isinstance(thread_id, str)
        or not thread_id
        or meta.get("session_id") != thread_id
    ):
        raise CaptureError("missing or conflicting native thread identity")
    if meta.get("parent_thread_id") or meta.get("source") != "exec":
        raise CaptureError("native session is not a fresh top-level exec")
    if meta.get("cli_version") != version:
        raise CaptureError("actual native version differs from freeze")
    context_ordinal, context = contexts[0]
    turn_id = context.get("turn_id")
    if (
        not isinstance(turn_id, str)
        or not turn_id
        or context.get("root_turn_id") != turn_id
    ):
        raise CaptureError("missing or conflicting native turn identity")
    if context.get("model") != model or context.get("effort") != effort:
        raise CaptureError("actual native model/effort differs from freeze")

    # Select the initial task boundary, never a later matching user echo.
    inputs: list[tuple[int, dict[str, Any]]] = []
    finals: list[tuple[int, dict[str, Any]]] = []
    native_inputs: list[tuple[int, dict[str, Any]]] = []
    native_finals: list[tuple[int, dict[str, Any]]] = []
    starts: list[tuple[int, dict[str, Any]]] = []
    completions: list[tuple[int, dict[str, Any]]] = []
    for ordinal, row in enumerate(records, 1):
        payload = row.get("payload", {})
        if row.get("type") == "response_item" and payload.get("type") == "message":
            kinds = payload.get("internal_chat_message_metadata_passthrough", {}).get(
                "content_item_kinds", []
            )
            if payload.get("role") == "user" and (
                ordinal > context_ordinal
                or "user_input_order" in row.get("metadata", {})
                or "user.text" in kinds
            ):
                inputs.append((ordinal, row))
            if (
                payload.get("role") == "assistant"
                and payload.get("phase") == "final_answer"
            ):
                finals.append((ordinal, row))
        if row.get("type") == "event_msg":
            if payload.get("type") == "task_started":
                starts.append((ordinal, payload))
            if payload.get("type") == "task_complete":
                completions.append((ordinal, payload))
            if payload.get("type") == "item_completed":
                if (
                    payload.get("thread_id") != thread_id
                    or payload.get("turn_id") != turn_id
                ):
                    raise CaptureError("native completed item identity disagrees")
                item = payload.get("item", {})
                if item.get("type") == "UserMessage":
                    native_inputs.append((ordinal, payload))
                if (
                    item.get("type") == "AgentMessage"
                    and item.get("phase") == "final_answer"
                ):
                    native_finals.append((ordinal, payload))
    if any(
        len(items) != 1
        for items in (inputs, finals, native_inputs, native_finals, starts, completions)
    ):
        raise CaptureError("missing or ambiguous initial input/final/native completion")

    # Cross-check independently recorded initial and final plaintext and identity.
    input_ordinal, input_row = inputs[0]
    native_input_ordinal, native_input = native_inputs[0]
    final_ordinal, final_row = finals[0]
    native_final_ordinal, native_final = native_finals[0]
    start_ordinal, start = starts[0]
    completion_ordinal, completion = completions[0]
    if (
        input_row.get("metadata", {}).get("user_input_order") != 0
        or input_row["payload"]
        .get("internal_chat_message_metadata_passthrough", {})
        .get("content_item_kinds")
        != ["user.text"]
        or retained_message(input_row, turn_id, "user") != prompt
        or native_item_bytes(native_input, thread_id, turn_id) != prompt
    ):
        raise CaptureError("authentic initial user content or order disagrees")
    result = retained_message(final_row, turn_id, "assistant")
    if (
        native_final["item"].get("id") != final_row["payload"]["id"]
        or native_item_bytes(native_final, thread_id, turn_id) != result
        or completion.get("turn_id") != turn_id
        or completion.get("last_agent_message", "").encode("utf-8") != result
        or start.get("turn_id") != turn_id
        or start.get("root_turn_id") != turn_id
    ):
        raise CaptureError("native terminal content or turn identity disagrees")
    if (
        not start_ordinal
        < context_ordinal
        < input_ordinal
        < native_input_ordinal
        < native_final_ordinal
        < final_ordinal
        < completion_ordinal
    ):
        raise CaptureError("native record order does not bind initial input to result")
    return {
        "thread_id": thread_id,
        "turn_id": turn_id,
        "input_ordinal": input_ordinal,
        "native_input_ordinal": native_input_ordinal,
        "final_ordinal": final_ordinal,
        "native_final_ordinal": native_final_ordinal,
        "completion_ordinal": completion_ordinal,
        "input_sha256": digest(prompt),
        "result_sha256": digest(result),
        "model": model,
        "effort": effort,
        "cli_version": version,
    }, result


def inventory(
    roots: list[Path], credential_paths: list[Path] | None = None
) -> dict[str, Any]:
    """Track paths, kinds, modes and bytes; redact only enumerated credentials."""
    # Exact private paths protect credentials without hiding ordinary auth.json.
    credentials = {path.absolute() for path in credential_paths or []}
    result: dict[str, Any] = {}
    for root in roots:
        for path in [root, *sorted(root.rglob("*"))]:
            metadata = path.lstat()
            entry: dict[str, Any] = {"mode": stat.S_IMODE(metadata.st_mode)}
            if stat.S_ISLNK(metadata.st_mode):
                entry.update(kind="symlink", symlink=os.readlink(path))
            elif stat.S_ISDIR(metadata.st_mode):
                entry["kind"] = "directory"
            elif stat.S_ISREG(metadata.st_mode):
                redacted = path.absolute() in credentials
                entry.update(
                    kind="file",
                    bytes=metadata.st_size,
                    sha256=None if redacted else digest(path.read_bytes()),
                )
                if redacted:
                    entry["credential_redacted"] = True
            else:
                entry.update(kind="other", file_type=stat.S_IFMT(metadata.st_mode))
            result[str(path)] = entry
    return result


def environment(packet: Path) -> dict[str, str]:
    """Keep acquisition and lifecycle tool storage inside the owned packet."""
    env = dict(os.environ)
    runtime = packet / "runtime"
    env.update(KNTNT_HOME=str(packet / "lifecycle"), PYTHONDONTWRITEBYTECODE="1")
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
        env[name] = str(runtime / name.lower())
    return env


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
        cwd=packet,
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
    actual_version = subprocess.check_output(
        [native, "--version"],
        cwd=args.cwd,
        env=environment(packet),
        text=True,
        timeout=15,
    ).strip()
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
    env = environment(packet)
    env.update(HOME=str(runtime / "home"), CODEX_HOME=str(native_home))
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
        Path(env[name]).mkdir(exist_ok=True)
    roots = [args.cwd.resolve(), packet, *[p.resolve() for p in args.inventory_root]]
    credentials = [native_home / "auth.json"]
    write_json(packet / "inventory-before.json", inventory(roots, credentials))
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
        write_json(packet / "inventory-after.json", inventory(roots, credentials))
        write_json(packet / "receipt.json", receipt)


def run(args: argparse.Namespace, prompt: bytes | None = None) -> bytes:
    """Clean private credentials on preparation failures as well as completion."""
    packet = args.packet.resolve()
    packet.mkdir(parents=True, exist_ok=False)
    runtime = packet / "runtime"
    try:
        # Register ownership before stdin can block or native preparation starts.
        if os.getpid() != os.getpgrp():
            os.setsid()
        register(os.getpid(), args.cleanup_script, environment(packet), packet)
        if prompt is None:
            prompt = sys.stdin.buffer.read()
        (packet / "prompt.txt").write_bytes(prompt)
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
        result = run(args)
    except (CaptureError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Native acquisition unavailable: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
