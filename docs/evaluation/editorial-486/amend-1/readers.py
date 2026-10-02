# /// script
# requires-python = ">=3.12"
# ///
"""Repeat only path-compromised readers against unchanged, preserved materials."""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import hashlib
import json
import os
import secrets
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[4]
EVALUATION = REPOSITORY / "docs/evaluation/editorial-486"
HERE = EVALUATION / "amend-1"
SCRATCH = (REPOSITORY.parent / "486.scratch").resolve() / "amend-1"
NATIVE = Path("/opt/homebrew/bin/codex").resolve()


def save(path: Path, value: object) -> None:
    """Persist externally captured evidence with actual native identities."""
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def register(kind: str, identifier: str) -> None:
    """Record every owned process and scratch path at creation time."""
    with (SCRATCH / "resources.jsonl").open("a") as ledger:
        ledger.write(json.dumps({"kind": kind, "identifier": identifier}) + "\n")


def hashes(root: Path) -> dict[str, str]:
    """Inventory exact material bytes before and after each independent reading."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def read(row: dict[str, str]) -> dict[str, str]:
    """Use frozen briefs and authentic files through a neutral virtual directory."""

    # Keep every actual write in this ticket's resolved physical scratch root.
    token = secrets.token_hex(8)
    root = SCRATCH / token
    root.mkdir()
    register("path", str(root))
    materials = root / "materials"
    materials.mkdir()
    home = root / "home"
    (home / ".codex").mkdir(parents=True)
    packet = root / "packet"
    packet.mkdir()
    original = EVALUATION / row["packet"]
    letter = original.name[-1] if row["role"] == "validator" else original.name
    if row["role"] == "validator":
        shutil.copyfile(original / "supplied-input.md", materials / "text.md")
        brief = EVALUATION / "validation-brief.md"
        report = f"validation-{letter}.md"
        expectation = ""
    else:
        run = original.parents[1]
        (materials / "work").mkdir()
        shutil.copyfile(run / "supplied-input.md", materials / "work/input.md")
        shutil.copyfile(run / "response.txt", materials / "response.md")
        file_target = "-file-" in run.name
        if file_target:
            shutil.copyfile(run / "captured-output.md", materials / "work/output.md")
        brief = EVALUATION / (
            "control-judge-brief-file.md" if file_target else "control-judge-brief.md"
        )
        report = f"judgement-{letter}.md"
        expectation = (
            "\n**Frozen expectation**: " + (run / "expectation.md").read_text()
        )
    before = hashes(materials)
    prompt = (
        brief.read_text()
        + f"\n---\nRun directory: /run\nYour letter: {letter}\n"
        + expectation
    )
    (packet / "invocation.txt").write_text(prompt)
    shutil.copytree(materials, packet / "supplied-materials")

    # A read-only neutral cwd exposes no host paths; the adapter confines file access.
    config = (
        'model = "gpt-6.1-sol"\nmodel_reasoning_effort = "xhigh"\n'
        'service_tier = "default"\nweb_search = "disabled"\n'
        "[features]\nshell_tool = false\nunified_exec = false\n"
        "shell_snapshot = false\napps = false\nplugins = false\nmulti_agent = false\n"
        "[mcp_servers.materials]\n"
        f"command = {json.dumps(sys.executable)}\n"
        f"args = {json.dumps([str(HERE / 'materials.py'), '--root', str(materials), '--report', report, '--log', str(packet / 'materials-rpc.jsonl')])}\n"
    )
    (home / ".codex/config.toml").write_text(config)
    shutil.copy2(Path("/Users/thomas/.codex/auth.json"), home / ".codex/auth.json")
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("KNTNT_", "CODEX_"))
    }
    for name in ("tmp", "cache", "data"):
        (root / name).mkdir()
    environment.update(
        HOME=str(home),
        CODEX_HOME=str(home / ".codex"),
        TMPDIR=str(root / "tmp"),
        XDG_CACHE_HOME=str(root / "cache"),
        XDG_DATA_HOME=str(root / "data"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    command = [
        str(NATIVE),
        "exec",
        "--ignore-rules",
        "-s",
        "read-only",
        "-C",
        "/",
        "--skip-git-repo-check",
        "--json",
        "-o",
        str(packet / "response.txt"),
        "-",
    ]
    version = subprocess.check_output(
        [str(NATIVE), "--version"], cwd=REPOSITORY, text=True
    ).strip()
    save(
        packet / "run.json",
        {
            "argv": command,
            "environment": {
                key: environment[key]
                for key in (
                    "HOME",
                    "CODEX_HOME",
                    "TMPDIR",
                    "XDG_CACHE_HOME",
                    "XDG_DATA_HOME",
                )
            },
            "harness": version,
            "public_directory": "/run",
            "physical_root": str(root),
            "source_packet": row["packet"],
            "brief_sha256": hashlib.sha256(brief.read_bytes()).hexdigest(),
        },
    )
    started = time.time()
    with (
        (packet / "trace.jsonl").open("w") as stdout,
        (packet / "stderr.txt").open("w") as stderr,
    ):
        process = subprocess.Popen(
            command,
            cwd=REPOSITORY,
            env=environment,
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr,
            text=True,
            start_new_session=True,
        )
        register("pid", str(process.pid))
        save(
            packet / "process.json", {"pid": process.pid, "process_group": process.pid}
        )
        timed_out = False
        try:
            process.communicate(prompt, timeout=1800)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
    save(
        packet / "result.json",
        {
            "returncode": process.returncode,
            "timed_out": timed_out,
            "started": started,
            "ended": time.time(),
        },
    )
    save(
        packet / "materials-inventory.json",
        {"before": before, "after": hashes(materials)},
    )

    # Preserve complete native contexts and public tool results, never authentication.
    lineage: list[dict[str, Any]] = []
    seats: list[dict[str, Any]] = []
    for path in sorted((home / ".codex/sessions").rglob("*.jsonl")):
        for line in path.read_text().splitlines():
            event = json.loads(line)
            if event["type"] == "session_meta":
                lineage.append(event["payload"])
            if event["type"] == "turn_context":
                seats.append(
                    {
                        "session": path.name,
                        "model": event["payload"].get("model"),
                        "effort": event["payload"].get("effort"),
                    }
                )
        destination = (
            packet / "native-sessions" / path.relative_to(home / ".codex/sessions")
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(str(destination) + ".gz", "wb") as stream:
            stream.write(path.read_bytes())
    valid = bool(seats) and all(
        seat["model"] == "gpt-6.1-sol" and seat["effort"] == "xhigh" for seat in seats
    )
    save(
        packet / "identity-audit.json",
        {"seats": seats, "lineage": lineage, "same_seat": valid},
    )
    if (materials / report).exists():
        shutil.copyfile(materials / report, packet / report)
    destination = HERE / "readers" / token
    shutil.copytree(packet, destination, ignore=shutil.ignore_patterns("trace.jsonl"))
    with gzip.open(destination / "trace.jsonl.gz", "wb") as stream:
        stream.write((packet / "trace.jsonl").read_bytes())
    result = {
        **row,
        "source_packet": row["packet"],
        "packet": str(destination.relative_to(EVALUATION)),
    }
    save(destination / "mapping.json", result)
    if (
        process.returncode
        or timed_out
        or not valid
        or not (destination / report).is_file()
    ):
        raise RuntimeError(f"Interrupted/incomplete reader retained: {destination}")
    print(json.dumps(result), flush=True)
    return result


def main() -> None:
    """Run one reader phase; validate the distinction before commissioning judges."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    register("pid", str(os.getpid()))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=["validator", "judge"], required=True)
    args = parser.parse_args()
    originals = json.loads((HERE / "original-readers.json").read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(
            pool.map(read, [row for row in originals if row["role"] == args.role])
        )
    save(HERE / f"{args.role}s.json", rows)
    if args.role == "judge":
        validators = json.loads((HERE / "validators.json").read_text())
        save(HERE / "counted-readers.json", validators + rows)


if __name__ == "__main__":
    main()
