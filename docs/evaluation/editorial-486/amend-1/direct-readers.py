# /// script
# requires-python = ">=3.12"
# ///
"""Repeat the compromised readers with the original method on neutral host paths."""

from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import os
import secrets
import shutil
import subprocess
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[4]
EVALUATION = REPOSITORY / "docs/evaluation/editorial-486"
HERE = EVALUATION / "amend-1"
SCRATCH = (REPOSITORY.parent / "486.scratch").resolve() / "amend-1/direct"
START = "5457c89405aece11b325937f9f07407f01974f7c"


def read(row: dict[str, str]) -> dict[str, str]:
    """Give each independent reader authentic bytes without identifying paths."""

    # Stage only the original reader's material under a fresh anonymous name.
    token = secrets.token_hex(8)
    original = EVALUATION / row["packet"]
    materials = SCRATCH / "materials" / token
    materials.mkdir()
    validator = row["role"] == "validator"
    letter = original.name[-1] if validator else original.name
    if validator:
        shutil.copyfile(original / "supplied-input.md", materials / "text.md")
        brief = EVALUATION / "validation-brief.md"
        source = materials / "text.md"
        extra = []
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
        source = materials / "work/input.md"
        extra = [f"--materials={materials}", f"--expectation={run / 'expectation.md'}"]

    # Reuse the exact committed capture, audit and preservation implementation.
    spec = importlib.util.spec_from_file_location(
        "frozen_campaign", EVALUATION / "harness/campaign.py"
    )
    assert spec and spec.loader
    import sys

    sys.path.insert(0, str(EVALUATION / "harness"))
    campaign = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(campaign)
    packet = SCRATCH / "packets" / token
    command = [
        "uv",
        "run",
        str(HERE / "direct-one.py"),
        f"--revision={START}",
        f"--corpus-revision={START}",
        f"--prompt={brief}",
        f"--input={source}",
        f"--input-name={'text.md' if validator else 'input.md'}",
        f"--output={packet}",
        f"--task={'validate' if validator else 'judge'}",
        f"--letter={letter}",
        *extra,
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
    campaign.audit(packet)
    destination = HERE / "readers" / token
    campaign.preserve(packet, destination)
    result = {
        "role": row["role"],
        "packet": str(destination.relative_to(EVALUATION)),
        "source_packet": row["packet"],
    }
    campaign.write_json(destination / "mapping.json", result)
    report = destination / f"{'validation' if validator else 'judgement'}-{letter}.md"
    if code or not report.exists():
        raise RuntimeError(f"Incomplete reader retained: {destination}")
    print(json.dumps(result), flush=True)
    return result


def main() -> None:
    """Finish one phase and permit inspection before the next phase is launched."""
    if os.getpgrp() != os.getpid():
        os.setsid()
    with (SCRATCH / "resources.jsonl").open("a") as ledger:
        ledger.write(json.dumps({"kind": "pid", "identifier": str(os.getpid())}) + "\n")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=["validator", "judge"], required=True)
    args = parser.parse_args()
    originals = json.loads((HERE / "original-readers.json").read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(
            pool.map(read, [row for row in originals if row["role"] == args.role])
        )
    (HERE / f"{args.role}s.json").write_text(json.dumps(rows, indent=2) + "\n")
    if args.role == "judge":
        validators = json.loads((HERE / "validators.json").read_text())
        (HERE / "counted-readers.json").write_text(
            json.dumps(validators + rows, indent=2) + "\n"
        )


if __name__ == "__main__":
    main()
