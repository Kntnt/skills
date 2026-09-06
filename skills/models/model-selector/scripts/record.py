# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""File a graded attempt, and never let the filing cost the caller anything.

This is the other half of `selection.py`. A caller that took a routed attempt and
had it judged hands the outcome back here, one JSON object or a list of them,
and the estimator is that much less ignorant next time. Anything the file gets
wrong is reported and skipped: by the time this runs, the work is already done
and already graded, so a rejected row is a gap in the evidence rather than a
failure of anybody's task. That is why this exits 0 even when every row was
refused, and why the report says what happened to each one.

Rows arriving with token counts but no price are priced here against the
catalogue as it stands today, which is the closest this Skill can get to what
the attempt actually cost.

A row whose attempt the store already holds is folded into it rather than
added beside it, and reported under `merged`: one attempt is one row however
many sides of a run file about it, and a caller that files the same row twice
after a crash changes nothing (issue #291).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import catalogue
import evidence
from catalogue import Catalogue

# Where the data directory sits when the caller does not say. Named here as
# it is in `selection.py`: both are entry points a user invokes directly, and
# neither is the other's caller.
DEFAULT_DATA = Path(".kntnt") / "model-selector"


def main(argv: Sequence[str] | None = None) -> int:
    """Append what the file holds, print what happened, and exit 0."""

    args = _parse(argv)
    try:
        report, problem = _file_rows(Path(args.path), _data_dir(args.data))
    except Exception as failure:  # noqa: BLE001 - filing evidence never fails the caller's work
        # A broad catch, on purpose. Evidence is a side effect of somebody
        # else's finished work, so no failure in here is allowed to read as a
        # failure of that work.
        report, problem = (
            evidence.AppendReport([], [], []),
            f"filing failed: {failure!r}",
        )

    print(
        json.dumps(
            {
                "accepted": [list(entry) for entry in report.accepted],
                "merged": [list(entry) for entry in report.merged],
                "rejected": [list(entry) for entry in report.rejected],
                "problem": problem,
            }
        )
    )
    return 0


def _file_rows(path: Path, data_dir: Path) -> tuple[evidence.AppendReport, str | None]:
    """Read the rows, price what needs pricing, and append them."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as unreadable:
        return evidence.AppendReport(
            [], [], []
        ), f"{path} could not be read: {unreadable}"

    entries = raw if isinstance(raw, list) else [raw]
    rows = [entry for entry in entries if isinstance(entry, dict)]
    unusable = len(entries) - len(rows)

    here = Path(__file__).resolve().parent.parent
    cat = catalogue.load(data_dir, here)
    kinds = evidence.load_kinds(here)
    report = evidence.append(data_dir, [_priced(row, cat, kinds) for row in rows])

    problem = f"{unusable} entries were not JSON objects" if unusable else None
    return report, problem


def _priced(
    row: Mapping[str, Any], cat: Catalogue, kinds: evidence.KindPriors
) -> dict[str, Any]:
    """Return the row with a price, where it carried tokens and no cost.

    Priced against the catalogue as it stands today, which is the closest this
    Skill can get to what the attempt actually cost, and against the row's own
    kind, because that is what says which of a vendor's two cards applied.
    """

    priced = dict(row)
    tokens = priced.get("tokens")
    if priced.get("cost_usd") is not None or not isinstance(tokens, dict):
        return priced

    matched = catalogue.resolve(cat, str(priced.get("model") or ""))
    if matched:
        kind = str(priced.get("kind") or "")
        priced["cost_usd"] = catalogue.cost_usd(
            matched[0], _counts(tokens), kind, kinds
        )
    return priced


def _counts(tokens: Mapping[str, Any]) -> dict[str, float | None]:
    """Return the token counts as numbers, admitting the ones that are not."""

    counted: dict[str, float | None] = {}
    for category, value in tokens.items():
        usable = isinstance(value, (int, float)) and not isinstance(value, bool)
        counted[str(category)] = float(value) if usable else None
    return counted


def _data_dir(named: str | None) -> Path:
    """Return the data directory, defaulting under a home this may not have."""

    if named:
        return Path(named).expanduser()
    try:
        return Path.home() / DEFAULT_DATA
    except RuntimeError:
        return Path.cwd() / DEFAULT_DATA


def _parse(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command line. The only thing in this Skill that may fail."""

    parser = argparse.ArgumentParser(
        prog="record.py", description="File one or more graded attempts as evidence."
    )
    parser.add_argument("--data")
    parser.add_argument("path")
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
