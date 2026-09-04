# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Summarize observed Usage Record cost and elapsed time, per named Seat.

`recommend`, `chart` and `compare` build their answer from derived
frontiers, and a frontier is quality: judged runs grouped into points, with
Wilson bounds and cost means attached (`references/pareto-selection.md`). A
Usage Record has no verdict and belongs to no Cohort, so it reaches none of
that by design (CONTEXT.md `Usage Record`) — it is never a selector input: it
enters no frontier, clears no quality floor, breaks no tie, and never makes a
point eligible that quality evidence excluded (issue #226 decision 2).

What a Usage Record can answer is a different, equally real question none of
that evidence answers: what has a Seat this recommendation names actually
cost and taken, on this machine, so far. This module is that answer, read
straight from the store `capture.py` appends to (`usage-records.jsonl`,
beside the evidence ledger under the selected data directory) and reported
per Seat, beside a recommendation or a frontier table and never inside it.

It is a Skill-owned reader rather than a Collection Library module: nothing
outside this Skill's own `recommend`, `chart` and `compare` renders this
section, so there is no second consumer the Library exists to serve yet
(issue #226's readiness addendum). It is called only from `SKILL.md`'s own
prose, after `route.py`'s selection core has already returned a decision —
never from inside it — so "a Usage Record never chooses" is a property of
where this module is called from, not a rule every caller has to remember.

## Matching a Usage Record to a named point

`recommend`'s frontier-neighbour entries (`_frontier_audit` in `route.py`)
carry only `model` and `portable_deliberation`, never the finer identity
fields — `channel`, `surface`, `native_deliberation`, `adapter_id` — the
selected launch happens to carry too. A Usage Record's own Seat is finer
than that for a session's own main turns, and coarser still for a delegated
subagent's: the Collection Library's `session_records.py` can read a
subagent's exact model and native deliberation control from Claude Code's
own transcript, but never its channel, surface, adapter or serving mode
(issue #225), so those stay an explicit `null` on every delegated Seat
capture writes.

`(model, portable_deliberation)` is therefore the coarsest identity both a
named point and a Usage Record's Seat can name, and the only one every kind
of named point — a selected launch and a frontier neighbour alike — can
supply without this module re-deriving anything `route.py`'s selection core
already owns. Every point is matched by exactly this pair, launch included:
using a finer key for one row and a coarser one for another would make one
table's record count mean two different things. A Usage Record whose Seat
carries no resolved portable deliberation at all — every delegated Seat
capture writes today — matches no point and is absent from every row's
count; that is a known, stated limitation of what issue #225 resolved, not a
silent gap.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Named once here rather than imported from `capture.py`: this module reads
# the store as an independent consumer of an on-disk contract, the same
# posture `capture.py` itself takes on `routed_observations.py`'s own ledger
# file name, and a plain string keeps this reader free of any dependency on
# capture's own pipeline. `tests/test_model_selector.py` asserts the two
# stay the same name.
USAGE_LEDGER_FILE = "usage-records.jsonl"


def _records(directory: Path) -> list[dict[str, Any]]:
    """Return every Usage Record the store under *directory* holds.

    A missing, truncated, or unparseable store is an absence, never a
    failure: every other read of this append-only JSONL store a user may
    hand-edit answers the same way, and a Usage Record's own presentation
    has no better claim to raising than the evidence ledger's does.
    """

    path = directory / USAGE_LEDGER_FILE
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    records: list[dict[str, Any]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            loaded = json.loads(stripped)
        except ValueError:
            continue
        if isinstance(loaded, dict):
            records.append(loaded)
    return records


def _names(record: dict[str, Any], point: dict[str, Any]) -> bool:
    """Return whether one Usage Record's own Seat names one recommended point."""

    seat = record.get("seat")
    if not isinstance(seat, dict):
        return False
    return seat.get("model") == point.get("model") and seat.get(
        "portable_deliberation"
    ) == point.get("portable_deliberation")


def _instants(record: dict[str, Any]) -> list[str]:
    """Return every instant one Usage Record actually names."""

    return [
        value
        for value in (record.get("started_at"), record.get("completed_at"))
        if isinstance(value, str) and value
    ]


def _mean(values: list[float | None]) -> float | None:
    """Return the mean of a complete set of measurements, or None where one is not.

    A category no contributing record measured stays unmeasured for the
    point too, the same rule `routed_observations.py`'s own `_mean` applies
    to a chain's cost, applied here to a Seat's observed usage.
    """

    known = [value for value in values if value is not None]
    return sum(known) / len(known) if values and len(known) == len(values) else None


def _number(value: Any) -> float | None:
    """Return one stored measurement as a number, or None where it is not one."""

    return (
        value
        if isinstance(value, int | float) and not isinstance(value, bool)
        else None
    )


def _elapsed(record: dict[str, Any]) -> float | None:
    """Return one Usage Record's own elapsed seconds, read rather than recomputed."""

    return _number(record.get("elapsed_seconds"))


def _tokens(record: dict[str, Any]) -> dict[str, Any]:
    """Return one Usage Record's own token category mapping, or an empty one."""

    usage = record.get("usage")
    tokens = usage.get("tokens") if isinstance(usage, dict) else None
    return tokens if isinstance(tokens, dict) else {}


def _token_categories(records: list[dict[str, Any]]) -> list[str]:
    """Return every token category any of *records* actually names, sorted.

    Read from the data rather than a list held here, so a category this
    reader never enumerates on its own — the Harness read it, and
    `session_records.py` decided the set (issue #225) — still surfaces the
    moment a Usage Record carries it.
    """

    categories: set[str] = set()
    for record in records:
        categories.update(_tokens(record))
    return sorted(categories)


def _token_mean(records: list[dict[str, Any]], category: str) -> float | None:
    """Return one token category's mean per Usage Record, or None where incomplete."""

    return _mean([_number(_tokens(record).get(category)) for record in records])


def usage_by_seat(
    directory: Path, points: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return one observed-usage summary per named point, in the order given.

    *points* is the exact ordered list a caller names for one request or one
    frontier row: the selected launch where one was selected, its frontier
    neighbours, or every point a chart table renders — each a `{"model":
    ..., "portable_deliberation": ...}` pair, the coarsest identity both a
    named point and a Usage Record's own Seat can name (see the module
    docstring). Nothing here reads a frontier, clears a quality floor, or
    breaks a tie: this function is called after a decision already exists,
    never from inside making one.

    Each returned entry echoes the point's own `model` and
    `portable_deliberation`, then reports `records` (the Usage Record count
    behind it), `tokens` (one mean per category any matched record actually
    names, or `null` where any one of them did not carry it), `elapsed_seconds`
    (mean, same rule), and `vintage` (`earliest` and `latest` instant any
    matched record names, or both `null` for none). A point no Usage Record
    names returns `records: 0` and every other field `null` or empty — an
    absence stated plainly, never a zero.
    """

    all_records = _records(directory)
    summaries: list[dict[str, Any]] = []
    for point in points:
        matched = [record for record in all_records if _names(record, point)]
        instants = [instant for record in matched for instant in _instants(record)]
        summaries.append(
            {
                "model": point.get("model"),
                "portable_deliberation": point.get("portable_deliberation"),
                "records": len(matched),
                "tokens": {
                    category: _token_mean(matched, category)
                    for category in _token_categories(matched)
                },
                "elapsed_seconds": _mean([_elapsed(record) for record in matched]),
                "vintage": {
                    "earliest": min(instants) if instants else None,
                    "latest": max(instants) if instants else None,
                },
            }
        )
    return summaries
