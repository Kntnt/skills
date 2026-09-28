# /// script
# requires-python = ">=3.12"
# ///
"""Run frozen Brief fixtures in ephemeral native Codex app-server threads.

The controller supplies user turns, never model responses. Full RPC events and
whole staged-workspace inventories remain beside each run. Authentication is
read from the existing Codex home; logs, state and temporary files are directed
to the ticket's private root. No HOME or CODEX_HOME variable is replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import selectors
import shutil
import signal
import subprocess
import time
import tomllib
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
PACKET = Path(__file__).resolve().parent
SCRATCH = Path(
    "/private/tmp/claude-501/-Users-thomas-Projects-skills/"
    "e8b2bc18-7919-41a5-8ca9-09238d1d9734/scratchpad/t444"
)
CLEANUP = Path(
    "/Users/thomas/.agents/skills/kntnt/features/session-cleanup/"
    "scripts/session_cleanup.py"
)


def save(path: Path, value: Any) -> None:
    """Keep structured evidence readable without losing exact request strings."""
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def inventory(root: Path) -> dict[str, Any]:
    """Hash every staged writable file, including installed Skills and scratch."""
    return {
        str(path.relative_to(root)): {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mode": path.stat().st_mode & 0o777,
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class NativeSession:
    """A bounded JSON-RPC connection whose event stream is the run's evidence."""

    def __init__(self, command: list[str], root: Path, evidence: Path) -> None:
        self.trace = (evidence / "trace.jsonl").open("w")
        self.stderr = (evidence / "stderr.txt").open("w")
        self.process = subprocess.Popen(
            command,
            cwd=root / "work",
            env={
                **os.environ,
                "TMPDIR": str(root / "scratch/tmp"),
                "UV_CACHE_DIR": str(root / "scratch/uv-cache"),
                "KNTNT_HOME": str(root / "scratch/home"),
                "XDG_CACHE_HOME": str(root / "scratch/cache"),
            },
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self.stderr,
            start_new_session=True,
        )
        subprocess.run(
            [
                "uv",
                "run",
                str(CLEANUP),
                "add",
                "pid",
                str(self.process.pid),
                "Ticket 444 native editorial evaluation",
            ],
            cwd=REPO,
            check=True,
            capture_output=True,
        )
        save(evidence / "process.json", {"pid": self.process.pid})
        self.selector = selectors.DefaultSelector()
        assert self.process.stdout is not None
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.buffer = b""
        self.request_id = 0

    def send(self, message: dict[str, Any]) -> None:
        """Record and send the exact client message."""
        self.trace.write(json.dumps({"direction": "client", **message}) + "\n")
        self.trace.flush()
        assert self.process.stdin is not None
        self.process.stdin.write((json.dumps(message) + "\n").encode())
        self.process.stdin.flush()

    def receive(self, deadline: float) -> dict[str, Any]:
        """Read an event with a bound independent of the model's progress."""
        while b"\n" not in self.buffer:
            if time.monotonic() >= deadline:
                raise TimeoutError("Native turn exceeded its 10-minute bound")
            if self.process.poll() is not None:
                raise RuntimeError(f"App server exited {self.process.returncode}")
            if self.selector.select(timeout=1):
                assert self.process.stdout is not None
                self.buffer += os.read(self.process.stdout.fileno(), 65536)
        line, self.buffer = self.buffer.split(b"\n", 1)
        event: dict[str, Any] = json.loads(line)
        self.trace.write(json.dumps({"direction": "server", **event}) + "\n")
        self.trace.flush()
        return event

    def request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """Wait for this request's answer while preserving all notifications."""
        self.request_id += 1
        identity = self.request_id
        self.send({"id": identity, "method": method, "params": params})
        deadline = time.monotonic() + 600
        while True:
            event = self.receive(deadline)
            if event.get("id") == identity and "method" not in event:
                if "error" in event:
                    raise RuntimeError(event["error"])
                result: dict[str, Any] = event["result"]
                return result

    def turn(self, thread: str, prompt: str) -> list[dict[str, Any]]:
        """Supply one real user turn and wait until its model turn finishes."""
        self.request(
            "turn/start",
            {
                "threadId": thread,
                "input": [{"type": "text", "text": prompt, "text_elements": []}],
            },
        )
        items: list[dict[str, Any]] = []
        deadline = time.monotonic() + 600
        while True:
            event = self.receive(deadline)
            if (
                event.get("method") == "item/completed"
                and event["params"].get("threadId") == thread
            ):
                items.append(event["params"]["item"])
            if (
                event.get("method") == "turn/completed"
                and event["params"].get("threadId") == thread
            ):
                if event["params"]["turn"]["status"] != "completed":
                    raise RuntimeError(event["params"]["turn"])
                return items
            if "id" in event and "method" in event:
                raise RuntimeError(f"Unexpected server request: {event['method']}")

    def close(self) -> None:
        """End the complete process group even after a timeout or failure."""
        try:
            if self.process.poll() is None:
                os.killpg(self.process.pid, signal.SIGTERM)
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait()
        except ProcessLookupError:
            self.process.wait()
        self.selector.close()
        self.trace.close()
        self.stderr.close()


def main() -> None:
    """Stage and execute one frozen fixture or one Write handoff."""
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    args = parser.parse_args()
    fixture: str = args.fixture
    evidence = PACKET / "runs" / fixture
    evidence.mkdir(parents=True, exist_ok=False)
    root = SCRATCH / fixture
    work = root / "work"
    for name in ("kntnt", "brief", "write"):
        source = REPO / "skills" / (name if name == "kntnt" else f"editorial/{name}")
        shutil.copytree(source, work / ".agents/skills" / name)
    for name in ("tmp", "uv-cache", "home", "cache", "logs", "state"):
        (root / "scratch" / name).mkdir(parents=True, exist_ok=True)
    catalogue = json.loads(Path("/Users/thomas/.codex/models_cache.json").read_text())
    save(root / "scratch/models.json", {"models": catalogue["models"]})
    if fixture.startswith("write-"):
        source_fixture = fixture.removeprefix("write-")
        shutil.copy2(PACKET / "runs" / source_fixture / "brief.md", work / "brief.md")
        for name in ("notes.md", "existing.md"):
            shutil.copy2(PACKET / "fixtures" / name, work / name)
        prompts = ["/write --output=draft.md brief.md"]
    else:
        prompts = json.loads((PACKET / "fixtures" / f"{fixture}.json").read_text())
        for name in ("notes.md", "existing.md"):
            shutil.copy2(PACKET / "fixtures" / name, work / name)
    save(evidence / "prompts.json", prompts)
    context = (
        "The installed Skills for this session are under .agents/skills. "
        "For an invocation, read and execute that Skill's SKILL.md. "
        "Brief's description: "
        + (work / ".agents/skills/brief/SKILL.md")
        .read_text()
        .split("description: ")[1]
        .split("\n")[0]
        + "\nThe writable evaluation workspace is this working directory and "
        + str(root / "scratch")
        + ". Put private temporary command directories inside that scratch area. "
        "Do not alter installed Skills or supplied sources. Deliver requested files "
        "relative to the working directory. Ask interview questions as ordinary "
        "assistant replies so the user can answer on the next turn."
    )
    (evidence / "harness-context.md").write_text(context + "\n")
    config: dict[str, Any] = {
        "features.hooks": False,
        "features.plugins": False,
        "features.plugin_hooks": False,
        "features.memories": False,
        "features.skip_host_skill_discovery": True,
        "features.multi_agent": True,
        "model_catalog_json": str(root / "scratch/models.json"),
        "sqlite_home": str(root / "scratch/state"),
        "log_dir": str(root / "scratch/logs"),
        "project_doc_max_bytes": 0,
        "model_reasoning_effort": "high",
        "approval_policy": "never",
        "sandbox_mode": "workspace-write",
        "sandbox_workspace_write.network_access": True,
        "sandbox_workspace_write.writable_roots": [str(root / "scratch")],
        "sandbox_workspace_write.exclude_tmpdir_env_var": True,
        "sandbox_workspace_write.exclude_slash_tmp": True,
    }
    user_config = tomllib.loads(Path("/Users/thomas/.codex/config.toml").read_text())
    for name in user_config.get("mcp_servers", {}):
        config[f"mcp_servers.{name}.enabled"] = False
    for name in user_config.get("plugins", {}):
        config[f"plugins.{name}.enabled"] = False
    command = ["codex", "app-server"]
    for key, value in config.items():
        command.extend(["-c", f"{key}={json.dumps(value)}"])
    save(evidence / "launch.json", {"command": command, "corpus": "99381cce"})
    before = inventory(root)
    save(evidence / "inventory-before.json", before)
    session = NativeSession(command, root, evidence)
    try:
        session.request(
            "initialize",
            {
                "clientInfo": {"name": "brief444evaluation", "version": "1.0"},
                "capabilities": {"experimentalApi": True},
            },
        )
        session.send({"method": "initialized", "params": {}})
        started = session.request(
            "thread/start",
            {
                "cwd": str(work),
                "ephemeral": True,
                "model": "gpt-6-astra",
                "approvalPolicy": "never",
                "sandbox": "workspace-write",
                "developerInstructions": context,
            },
        )
        save(evidence / "thread.json", started)
        thread = started["thread"]["id"]
        for number, prompt in enumerate(prompts, 1):
            print(f"{fixture}: turn {number}/{len(prompts)}", flush=True)
            items = session.turn(thread, prompt)
            save(evidence / f"turn-{number:02}.json", items)
            messages = [
                i.get("text", "") for i in items if i.get("type") == "agentMessage"
            ]
            (evidence / f"response-{number:02}.md").write_text(
                "\n\n".join(messages) + "\n"
            )
        save(evidence / "result.json", {"completed": True, "turns": len(prompts)})
    finally:
        session.close()
        after = inventory(root)
        save(evidence / "inventory-after.json", after)
        save(
            evidence / "changes.json",
            {
                "created": sorted(after.keys() - before.keys()),
                "removed": sorted(before.keys() - after.keys()),
                "changed": sorted(
                    k for k in before.keys() & after.keys() if before[k] != after[k]
                ),
            },
        )
        for name in ("brief.md", "draft.md"):
            if (work / name).is_file():
                shutil.copy2(work / name, evidence / name)
        save(evidence / "process-exit.json", {"returncode": session.process.returncode})


if __name__ == "__main__":
    main()
