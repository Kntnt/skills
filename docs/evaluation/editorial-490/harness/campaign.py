# /// script
# requires-python = ">=3.12"
# ///
"""Execute frozen rows and neutral independent readers, retaining native evidence."""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import json
import os
import secrets
import shutil
import subprocess
from pathlib import Path

from run import REPOSITORY, SCRATCH, register, write_json

EVALUATION = REPOSITORY / "docs/evaluation/editorial-490"
START = "4cf05813f94c2fa7147898878027835e14d29859"


def audit(packet: Path) -> None:
    """Require the frozen native seat for every preserved parent and child turn."""
    seats: list[dict[str, object]] = []
    lineage: list[dict[str, object]] = []
    for path in (packet / "native-sessions").rglob("*.jsonl"):
        for line in path.read_text().splitlines():
            event = json.loads(line)
            payload = event.get("payload", {})
            if event["type"] == "session_meta":
                lineage.append(payload)
            elif event["type"] == "turn_context":
                seats.append(
                    {
                        "session": path.name,
                        "model": payload.get("model"),
                        "effort": payload.get("effort"),
                    }
                )
    valid = bool(seats) and all(
        s["model"] == "gpt-6.1-sol" and s["effort"] == "xhigh" for s in seats
    )
    write_json(
        packet / "identity-audit.json",
        {"same_seat": valid, "seats": seats, "lineage": lineage},
    )
    if not valid:
        raise RuntimeError(f"Native seat not established: {packet}")


def preserve(packet: Path, destination: Path) -> None:
    """Deliver complete traces compressed, without any private authentication."""
    shutil.copytree(
        packet,
        destination,
        ignore=shutil.ignore_patterns("native-sessions", "trace.jsonl"),
    )
    for source in (packet / "native-sessions").rglob("*.jsonl"):
        target = (
            destination
            / "native-sessions"
            / source.relative_to(packet / "native-sessions")
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(str(target) + ".gz", "wb") as stream:
            stream.write(source.read_bytes())
    with gzip.open(destination / "trace.jsonl.gz", "wb") as stream:
        stream.write((packet / "trace.jsonl").read_bytes())


def invoke(arguments: list[str]) -> Path:
    """Start one native runner in its own group and wait for its captured result."""
    token = secrets.token_hex(8)
    packet = SCRATCH / "packets" / token
    with (SCRATCH / "logs" / f"{token}.log").open("w") as stream:
        process = subprocess.Popen(
            [
                "uv",
                "run",
                str(EVALUATION / "harness/run.py"),
                f"--output={packet}",
                *arguments,
            ],
            cwd=REPOSITORY,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        register("pid", str(process.pid))
        code = process.wait()
    if code:
        preserve(packet, EVALUATION / "voided" / token)
        raise RuntimeError(
            f"Native process exited {code}; preserved void attempt {token}"
        )
    audit(packet)
    return packet


def reader(
    materials: Path,
    brief: Path,
    role: str,
    letter: str,
    expectation: Path | None = None,
) -> Path:
    """Give a fresh independent reader only the frozen material and neutral paths."""
    source = materials / "text.md" if role == "validate" else materials / "input.md"
    if not source.exists():
        source = materials / "work/input.md"
    arguments = [
        f"--revision={START}",
        f"--corpus-revision={START}",
        f"--prompt={brief}",
        f"--input={source}",
        "--input-name=input.md",
        f"--materials={materials}",
        f"--task={role}",
        f"--letter={letter}",
    ]
    if expectation:
        arguments.append(f"--expectation={expectation}")
    return invoke(arguments)


def validation() -> None:
    """Validate each frozen contrast before native baseline or candidate wording."""
    for name in ("q1", "q2", "q3", "q4", "q5"):
        materials = SCRATCH / "materials" / secrets.token_hex(8)
        shutil.copytree(EVALUATION / "inputs" / name, materials)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = {
                letter: pool.submit(
                    reader,
                    materials,
                    EVALUATION / "validation-brief.md",
                    "validate",
                    letter,
                )
                for letter in ("a", "b")
            }
            for letter, future in futures.items():
                packet = future.result()
                preserve(packet, EVALUATION / "validation" / name / letter)
                print(f"Validated {name}/{letter}", flush=True)


def native_one(arm: str, revision: str, target: str, repeat: int) -> Path:
    """Capture one native Redline row, then independently judge its terminal reply."""
    name = (
        f"{arm}-case-study-clean-{'resp' if target == 'response' else 'file'}-{repeat}"
    )
    prompt = SCRATCH / "materials" / f"{secrets.token_hex(8)}.txt"
    prompt.write_text(
        f"/redline --genre=casestudy --language=sv --output={target} input.md\n"
    )
    arguments = [
        f"--revision={revision}",
        f"--corpus-revision={START}",
        f"--prompt={prompt}",
        f"--input={EVALUATION / 'inputs/case-study-clean.md'}",
        "--input-name=input.md",
    ]
    if target != "response":
        arguments.append("--capture-output-name=output.md")
    packet = invoke(arguments)
    materials = SCRATCH / "materials" / secrets.token_hex(8)
    (materials / "work").mkdir(parents=True)
    shutil.copyfile(packet / "supplied-input.md", materials / "work/input.md")
    shutil.copyfile(packet / "response.txt", materials / "response.md")
    if (packet / "captured-output.md").exists():
        shutil.copyfile(packet / "captured-output.md", materials / "work/output.md")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            letter: pool.submit(
                reader,
                materials,
                EVALUATION / "judge-brief.md",
                "judge",
                letter,
                EVALUATION / "expectations/case-study-clean.md",
            )
            for letter in ("a", "b")
        }
        for letter, future in futures.items():
            judged = future.result()
            preserve(judged, packet / "reply-judges" / letter)
            shutil.copyfile(
                judged / f"judgement-{letter}.md", packet / f"judgement-{letter}.md"
            )
    destination = EVALUATION / "runs" / name
    preserve(packet, destination)
    print(f"Captured and reply-judged {name}: {destination}", flush=True)
    return packet


def main() -> None:
    """Run one prospective phase, never proceeding autonomously to candidate selection."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    register("pid", str(os.getpid()))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["validation", "native"])
    parser.add_argument("--arm", default="pre")
    parser.add_argument("--revision", default=START)
    parser.add_argument(
        "--target", default="response", choices=["response", "output.md"]
    )
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args()
    if args.phase == "validation":
        validation()
    else:
        native_one(args.arm, args.revision, args.target, args.repeat)


if __name__ == "__main__":
    main()
