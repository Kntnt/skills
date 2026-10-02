# /// script
# requires-python = ">=3.12"
# ///
"""Repeat only file judges whose supplied delivery link disclosed the ticket."""

from __future__ import annotations

import concurrent.futures
import importlib.util
import json
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[4]
EVALUATION = REPOSITORY / "docs/evaluation/editorial-486"
HERE = EVALUATION / "amend-1"
SCRATCH = (REPOSITORY.parent / "486.scratch").resolve() / "amend-1/direct"
START = "5457c89405aece11b325937f9f07407f01974f7c"


def campaign() -> Any:
    """Reuse the committed native seat audit and complete packet preservation."""
    sys.path.insert(0, str(EVALUATION / "harness"))
    spec = importlib.util.spec_from_file_location(
        "frozen_campaign", EVALUATION / "harness/campaign.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(row: dict[str, str]) -> dict[str, str]:
    """Substitute only the frozen neutral reply link before an independent reading."""
    helper = campaign()
    original = EVALUATION / row["packet"]
    run = original.parents[1]
    prepared = json.loads((HERE / "file-materials.json").read_text())
    reply = next(entry for entry in prepared if entry["run"] == run.name)
    token = secrets.token_hex(8)
    materials = SCRATCH / "materials" / token
    (materials / "work").mkdir(parents=True)
    shutil.copyfile(run / "supplied-input.md", materials / "work/input.md")
    shutil.copyfile(run / "captured-output.md", materials / "work/output.md")
    shutil.copyfile(EVALUATION / reply["material"], materials / "response.md")

    # Refuse any identifying material before launching a blinded native reader.
    for path in materials.rglob("*.md"):
        assert not any(
            name in path.read_text()
            for name in (
                "ticket-486",
                "editorial-486",
                "/486/",
                "pre-article-",
                "post-article-",
            )
        ), path
    packet = SCRATCH / "packets" / token
    command = [
        "uv",
        "run",
        str(HERE / "direct-one.py"),
        f"--revision={START}",
        f"--corpus-revision={START}",
        f"--prompt={EVALUATION / 'control-judge-brief-file.md'}",
        f"--input={materials / 'work/input.md'}",
        "--input-name=input.md",
        f"--output={packet}",
        "--task=judge",
        f"--materials={materials}",
        f"--expectation={run / 'expectation.md'}",
        f"--letter={original.name}",
    ]
    with (SCRATCH / "logs" / f"{token}.log").open("w") as log:
        process = subprocess.Popen(
            command,
            cwd=REPOSITORY,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        with (SCRATCH / "resources.jsonl").open("a") as ledger:
            ledger.write(
                json.dumps({"kind": "pid", "identifier": str(process.pid)}) + "\n"
            )
        code = process.wait()
    helper.audit(packet)
    destination = HERE / "readers" / token
    helper.preserve(packet, destination)
    result = {
        "role": "judge",
        "packet": str(destination.relative_to(EVALUATION)),
        "source_packet": row["packet"],
        "sanitized_response": reply["material"],
    }
    helper.write_json(destination / "mapping.json", result)
    if code or not (destination / f"judgement-{original.name}.md").is_file():
        raise RuntimeError(f"Incomplete reader retained: {destination}")
    print(json.dumps(result), flush=True)
    return result


def main() -> None:
    """Retain valid readers and replace only the ten path-compromised file readings."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    with (SCRATCH / "resources.jsonl").open("a") as ledger:
        ledger.write(json.dumps({"kind": "pid", "identifier": str(os.getpid())}) + "\n")
    originals = json.loads((HERE / "original-readers.json").read_text())
    affected = [
        row for row in originals if row["role"] == "judge" and "-file-" in row["packet"]
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(read, affected))
    helper = campaign()
    helper.write_json(HERE / "file-judges.json", rows)
    previous = json.loads((HERE / "direct-readings.json").read_text())
    preserved = [
        row
        for row in previous
        if row["role"] == "validator" or "-resp-" in row["source_packet"]
    ]
    helper.write_json(HERE / "counted-readers.json", preserved + rows)


if __name__ == "__main__":
    main()
