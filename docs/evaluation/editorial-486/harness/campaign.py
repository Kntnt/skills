# /// script
# requires-python = ">=3.12"
# ///
"""Run frozen native rows and independent readers without exposing their arms."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import gzip
import hashlib
import json
import os
import secrets
import shutil
import subprocess
from pathlib import Path

from run import REPOSITORY, SCRATCH, inventory, register, write_json

EVALUATION = REPOSITORY / "docs/evaluation/editorial-486"
START = "5457c89405aece11b325937f9f07407f01974f7c"


def exported(revision: str, path: str) -> bytes:
    """Read committed fixture bytes, never live product or fixture edits."""
    return subprocess.check_output(
        ["git", "show", f"{revision}:{path}"], cwd=REPOSITORY
    )


def invoke(arguments: list[str], log: Path) -> None:
    """Wait for a native runner and stop the campaign on infrastructure failure."""
    with log.open("w") as stream:
        process = subprocess.Popen(
            ["uv", "run", str(EVALUATION / "harness/run.py"), *arguments],
            cwd=REPOSITORY,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        register("pid", str(process.pid))
        code = process.wait()
    if code:
        raise RuntimeError(f"Native attempt exited {code}; preserve and inspect {log}")


def audit(packet: Path) -> None:
    """Retain parent/child identities and reject drift from the frozen native seat."""
    seats = []
    lineage = []
    for path in sorted((packet / "native-sessions").rglob("*.jsonl")):
        for line in path.read_text().splitlines():
            event = json.loads(line)
            if event["type"] == "session_meta":
                lineage.append(event["payload"])
            if event["type"] == "turn_context":
                payload = event["payload"]
                seats.append(
                    {
                        "session": path.name,
                        "model": payload.get("model"),
                        "effort": payload.get("effort"),
                    }
                )
    valid = bool(seats) and all(
        seat["model"] == "gpt-6.1-sol" and seat["effort"] == "xhigh" for seat in seats
    )
    write_json(
        packet / "identity-audit.json",
        {"seats": seats, "lineage": lineage, "same_seat": valid},
    )
    if not valid:
        raise RuntimeError(f"Seat not established at {packet}")


def preserve(packet: Path, destination: Path) -> None:
    """Copy counted evidence after judging and compress complete native traces."""
    shutil.copytree(
        packet,
        destination,
        ignore=shutil.ignore_patterns("native-sessions", "trace.jsonl"),
    )
    for path in (packet / "native-sessions").rglob("*.jsonl"):
        target = (
            destination
            / "native-sessions"
            / path.relative_to(packet / "native-sessions")
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(str(target) + ".gz", "wb") as stream:
            stream.write(path.read_bytes())
    with gzip.open(destination / "trace.jsonl.gz", "wb") as stream:
        stream.write((packet / "trace.jsonl").read_bytes())


def wave(label: str) -> None:
    """Inventory this ticket's writable scope without inspecting other tickets."""
    path = EVALUATION / "runs/waves"
    path.mkdir(exist_ok=True)
    write_json(path / f"{label}-scratch.json", inventory(SCRATCH))
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPOSITORY,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        text=True,
    )
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    write_json(
        path / f"{label}-repo.json",
        {"head": head, "status": status, "session_scratchpad": "none supplied"},
    )


def validate(name: str, letter: str, fixtures: str) -> None:
    """Give an independent validator one anonymous input and a neutral brief."""
    token = secrets.token_hex(6)
    materials = SCRATCH / "v" / token
    materials.mkdir(parents=True)
    text = materials / "text.md"
    text.write_bytes(
        exported(fixtures, f"docs/evaluation/editorial-486/inputs/{name}.md")
    )
    packet = SCRATCH / "readers" / token
    invoke(
        [
            f"--revision={START}",
            f"--corpus-revision={START}",
            f"--prompt={EVALUATION / 'validation-brief.md'}",
            f"--input={text}",
            "--input-name=text.md",
            f"--output={packet}",
            "--task=validate",
            f"--letter={letter}",
        ],
        SCRATCH / "logs" / f"validation-{token}.log",
    )
    audit(packet)
    preserve(packet, EVALUATION / "validation" / f"{name}-{letter}")
    with (EVALUATION / "validation/validators.tsv").open("a") as stream:
        stream.write(f"{name}\t{letter}\t{token}\n")


def judge(row: dict[str, str], packet: Path, letter: str, expectation: Path) -> None:
    """Use byte-copied #480 briefs and a separate neutral packet for each reader."""
    token = secrets.token_hex(6)
    materials = SCRATCH / "j" / token
    (materials / "work").mkdir(parents=True)
    shutil.copyfile(packet / "supplied-input.md", materials / "work/input.md")
    shutil.copyfile(packet / "response.txt", materials / "response.md")
    file_target = row["capture"] == "yes"
    if file_target and (packet / "captured-output.md").exists():
        shutil.copyfile(packet / "captured-output.md", materials / "work/output.md")
    reader = SCRATCH / "readers" / token
    brief = EVALUATION / (
        "control-judge-brief-file.md" if file_target else "control-judge-brief.md"
    )
    invoke(
        [
            f"--revision={START}",
            f"--corpus-revision={START}",
            f"--prompt={brief}",
            f"--input={packet / 'supplied-input.md'}",
            "--input-name=input.md",
            f"--output={reader}",
            "--task=judge",
            f"--materials={materials}",
            f"--letter={letter}",
            f"--expectation={expectation}",
        ],
        SCRATCH / "logs" / f"judge-{token}.log",
    )
    audit(reader)
    judgement = reader / f"judgement-{letter}.md"
    if not judgement.exists():
        raise RuntimeError(f"Judge delivered no judgement: {reader}")
    shutil.copyfile(judgement, packet / judgement.name)
    preserve(reader, packet / "judges" / letter)
    with (EVALUATION / "runs/judges.tsv").open("a") as stream:
        stream.write(f"{row['run']}\t{letter}\t{token}\n")


def lane(rows: list[dict[str, str]], fixtures: str) -> None:
    """Run each input sequentially while independent inputs occupy other lanes."""
    for row in rows:
        packet = SCRATCH / "packets" / row["run"]
        if packet.exists():
            raise RuntimeError(
                f"Attempt already exists: {packet}; do not silently rerun"
            )
        token = secrets.token_hex(6)
        staged = SCRATCH / "inputs" / token
        staged.mkdir(parents=True)
        text = staged / "input.md"
        text.write_bytes(exported(fixtures, row["input"]))
        prompt = staged / "invocation.txt"
        prompt.write_text(row["invocation"] + "\n")
        expectation = staged / "expectation.md"
        expectation.write_bytes(
            exported(fixtures, row["input"].replace(".md", ".expectation.md"))
        )
        arguments = [
            f"--revision={row['revision']}",
            f"--corpus-revision={START}",
            f"--prompt={prompt}",
            f"--input={text}",
            "--input-name=input.md",
            f"--output={packet}",
        ]
        if row["capture"] == "yes":
            arguments.append("--capture-output-name=output.md")
        print(f"start {row['run']}", flush=True)
        invoke(arguments, SCRATCH / "logs" / f"{row['run']}.log")
        audit(packet)
        shutil.copyfile(expectation, packet / "expectation.md")
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            readers = [
                pool.submit(judge, row, packet, letter, expectation)
                for letter in ("a", "b")
            ]
            for reader in readers:
                reader.result()
        preserve(packet, EVALUATION / "runs" / row["run"])
        digest = hashlib.sha256((packet / "response.txt").read_bytes()).hexdigest()
        print(f"complete {row['run']} response {digest}", flush=True)


def main() -> None:
    """Run either the prospective validation or one immutable arm matrix."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    register("pid", str(os.getpid()))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--matrix", type=Path)
    args = parser.parse_args()
    for name in ("logs", "inputs", "packets", "readers"):
        (SCRATCH / name).mkdir(exist_ok=True)
    label = "validation" if args.validate else args.matrix.stem
    wave(f"{label}-before")
    try:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=4 if args.validate else 3
        ) as pool:
            if args.validate:
                jobs = [
                    pool.submit(validate, name, letter, args.fixtures)
                    for name in ("article-inference", "article-promise")
                    for letter in ("a", "b")
                ]
            else:
                with args.matrix.open() as stream:
                    rows = list(csv.DictReader(stream, delimiter="\t"))
                jobs = [
                    pool.submit(
                        lane,
                        [row for row in rows if row["lane"] == str(number)],
                        args.fixtures,
                    )
                    for number in range(3)
                ]
            for job in jobs:
                job.result()
    finally:
        wave(f"{label}-after")


if __name__ == "__main__":
    main()
