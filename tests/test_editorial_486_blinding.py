"""Keep every counted semantic reader blind to ticket and arm path namespaces."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALUATION = ROOT / "docs/evaluation/editorial-486"


def test_all_counted_readers_receive_neutral_paths_in_every_visible_surface() -> None:
    """A random leaf cannot conceal a ticket-bearing ancestor or native cwd."""

    # Include validators as well as both judges of every completed baseline row.
    rows = json.loads((EVALUATION / "amend-1/counted-readers.json").read_text())
    assert sum(row["role"] == "validator" for row in rows) == 4
    assert sum(row["role"] == "judge" for row in rows) == 20
    leaks = []

    # Inspect supplied prompts, actual native contexts and returned tool surfaces.
    for row in rows:
        packet = EVALUATION / row["packet"]
        surfaces = {"invocation": (packet / "invocation.txt").read_text()}
        audit = json.loads((packet / "identity-audit.json").read_text())
        for number, lineage in enumerate(audit["lineage"]):
            surfaces[f"native-context-{number}"] = json.dumps(lineage)
        with gzip.open(packet / "trace.jsonl.gz", "rt") as stream:
            surfaces["tool-and-reply-trace"] = stream.read()
        for name, text in surfaces.items():
            for forbidden in (
                "ticket-486",
                "editorial-486",
                "/486/",
                "pre-article-",
                "post-article-",
            ):
                if forbidden in text:
                    leaks.append(f"{row['packet']} {name}: {forbidden}")
    assert not leaks, "Reader-visible identity leaks:\n" + "\n".join(leaks)
