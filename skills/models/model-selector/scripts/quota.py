# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""How much of a subscription's week has gone, and whether that holds it back.

List-price dollars are not quota. The ranking orders one USD figure, and what
actually runs out is a weekly subscription window whose size in those dollars
nobody has recorded — so quota is a guard here and never a currency: it narrows
the pool before anything is ranked, and the ranking itself is untouched
(ADR-0205). A subscription channel is left out of a machine-chosen answer while
either of two things holds of the weekly window of the Harness it names: the
share used is more than `AHEAD` points past the share of the window elapsed, or
the share used is at or above `CEILING` whatever the pace.

Two sources, both local, and nothing else. No network call, no credential read,
and the same behaviour for any user of the public collection. Codex publishes
its own window in every `token_count` event of its session logs, so that figure
is read from the logs directly. Nothing of Claude Code's does — its transcripts
carry no rate-limit fields — but its status line is handed the windows on
standard input, so the `kntnt.statusline` Feature writes them to `quota.json` in
this Skill's data directory as it draws. Every other harness reads that file
too: a status line is a thing a harness can be asked to write, and a session log
is not a thing one can be asked for.

Absence is the ordinary state here rather than a failure. A machine with no
file, an unreadable one, one in another shape, one written more than a day ago,
one past the reset instant it names, no session log, a damaged tree — each is a
harness with no guard, said nowhere in an answer, refused never, and reported
plainly by `status`. This runs inside somebody else's turn, and a guard that
stopped the work over an optimisation would be worse than no guard at all.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Where the figure a status line writes is kept, under this Skill's data
# directory. Keyed by the Harness whose plan pays, because neither source can
# name a provider and both can name the harness they are.
QUOTA_FILE = "quota.json"

# How far ahead of the week a channel may run before it is held back, in points
# of the window. Ten is wide enough that an ordinary heavy morning does not
# hold a channel back for the rest of the day, and narrow enough that a pace
# which would exhaust the week early is caught while there is still a week to
# save. It is a guard rather than a budget: nothing is spent by the difference.
AHEAD = 10.0

# The share of the window at which a channel is held back whatever the pace.
# Ninety leaves a tenth of the week for the work only this channel can do — a
# user's own session, a model lock, a pool that would otherwise be empty — and
# late in a window the pace test alone would admit a channel that is nearly out.
CEILING = 90.0

# How old a figure may be before it says nothing. A status line runs whenever a
# session renders and a Codex session writes one of these events every turn, so
# a figure older than this is from a machine nobody has worked on since; and on
# a seven-day window a day of drift is already worth more than the `AHEAD`
# points the rule turns on.
STALE_SECONDS = 24 * 60 * 60

# The window this rule is about, in the whole minutes both sources spell it in.
# Any other window is a different question, and is read as no figure rather
# than compared against thresholds that were not chosen for it.
WEEK_MINUTES = 10080

# What Codex leaves under a home, and the depth its session logs sit at:
# `YYYY/MM/DD/rollout-*.jsonl`. Matched at that exact depth rather than walked,
# so the listing cannot descend a tree of unknown size.
CODEX_SESSIONS = Path(".codex") / "sessions"
CODEX_LOGS = "*/*/*/rollout-*.jsonl"

# Where the data directory sits when the caller does not say, which is what
# every other engine of this Skill means by the same absence.
DEFAULT_DATA = Path(".kntnt") / "model-selector"

# How much of the session tree one read looks at. The read happens inside
# somebody else's turn, so it is bounded rather than complete: the most
# recently modified files, and the end of each, scanned backwards for the last
# event carrying a window. A machine with years of sessions costs what a
# machine with a week's costs.
CODEX_FILES = 20
CODEX_TAIL = 64 * 1024

# Where a figure came from, as `status` names it.
WRITTEN = "quota.json"
LOGGED = "codex session log"

# Why a harness has no figure. Each is a phrase `status` renders as it stands,
# because *there is no guard here* is only useful to somebody who can tell
# which of these it is — one of them is a file to go and look at, and the rest
# are a machine behaving normally.
NO_FILE = "nothing has written one"
UNREADABLE = "the file could not be read"
ANOTHER_SHAPE = "the file is in another shape"
NOT_NAMED = "the file carries no readable weekly window for this harness"
NO_LOG = "no readable session log carries a weekly window"
STALE = "the figure was taken more than twenty-four hours ago"
PASSED = "the window it names has already reset"

# The harness whose figure is read from its own session logs rather than from
# the file, and the harnesses reported on whether or not anything has written a
# figure for them — so that `status` can say there is none, and which reason it
# is, rather than saying nothing at all.
CODEX = "codex"
REPORTED = ("claude-code", CODEX)


@dataclass(frozen=True)
class Figure:
    """One harness's weekly window, as one source last reported it.

    `taken_at` is the instant the figure was established rather than the
    instant it was stored: `written_at` for the file, and the event's own
    `timestamp` for a session log.
    """

    harness: str
    source: str
    used_percent: float
    resets_at: int
    taken_at: int


@dataclass(frozen=True)
class Account:
    """What the rule makes of one harness's window, or why it makes nothing.

    `held_back` is the rule's verdict on the figure and never what a particular
    call did with it: a call whose pool would otherwise empty ranks a held-back
    channel anyway. `absent` is None where there is a figure, and otherwise one
    of the reasons above, with every figure beside it null.
    """

    harness: str
    source: str | None
    used_percent: float | None
    elapsed_percent: float | None
    resets_at: int | None
    age_seconds: float | None
    held_back: bool
    absent: str | None


def accounts(
    data_dir: Path, codex_root: Path, *, now: float | None = None
) -> list[Account]:
    """Return what the rule makes of every harness a source can speak for.

    Both roots are arguments rather than resolved here, so that the engine, the
    report and a test all ask the same question of whichever trees they mean.
    """

    moment = time.time() if now is None else now
    written, unwritten = _written(data_dir)
    logged, unlogged = _logged(codex_root)

    reported: list[Account] = []
    for harness in sorted({*REPORTED, *written}):
        if harness == CODEX:
            figure, absent = logged, unlogged
        else:
            figure = written.get(harness)
            absent = unwritten if unwritten is not None else NOT_NAMED
        reported.append(_judged(harness, figure, absent, moment))
    return reported


def held_back(
    data_dir: Path, codex_root: Path, *, now: float | None = None
) -> frozenset[str]:
    """Return the harnesses whose weekly window the rule holds back."""

    return frozenset(
        account.harness
        for account in accounts(data_dir, codex_root, now=now)
        if account.held_back
    )


def codex_root() -> Path:
    """Return where Codex keeps its session logs, under this machine's home.

    `--data` does not move it: the logs are the Harness's own files rather than
    anything this Skill writes.
    """

    return _home() / CODEX_SESSIONS


def data_root() -> Path:
    """Return where `quota.json` is, which is not where `--data` points.

    Like the daily catalogue pass's own marker, this file is always under the
    one root: it is written by a status line, which is handed no `--data` and
    has no way to learn what one call passed. A caller that means another
    directory hands this module that directory instead.
    """

    return _home() / DEFAULT_DATA


def _home() -> Path:
    """Return the home both roots hang off.

    `KNTNT_HOME` first, which is how every script of this collection that has
    to be pointed at another home already resolves one, and how the status line
    writing the file resolves the root it writes into — so the reader and the
    writer agree on a machine where it is set as well as on one where it is
    not. A machine with no home directory at all falls back to where it stands
    rather than raising, this resolution happening inside somebody else's turn.
    """

    override = os.environ.get("KNTNT_HOME")
    if override:
        return Path(override)
    try:
        return Path.home()
    except RuntimeError:
        return Path.cwd()


def _judged(
    harness: str, figure: Figure | None, absent: str | None, moment: float
) -> Account:
    """Return the rule's verdict on one figure, or the account that has none."""

    if figure is None:
        return _nothing(harness, absent or NO_FILE)

    age = moment - figure.taken_at
    if age > STALE_SECONDS:
        return _nothing(harness, STALE)
    if figure.resets_at <= moment:
        return _nothing(harness, PASSED)

    elapsed = _elapsed(figure.resets_at, moment)
    return Account(
        harness=harness,
        source=figure.source,
        used_percent=figure.used_percent,
        elapsed_percent=elapsed,
        resets_at=figure.resets_at,
        age_seconds=age,
        held_back=figure.used_percent - elapsed > AHEAD
        or figure.used_percent >= CEILING,
        absent=None,
    )


def _elapsed(resets_at: int, moment: float) -> float:
    """Return the share of the window gone, in points, clamped to the window.

    One minus what is left of it over its whole length. A reset further off
    than the window is long is a clock somebody has moved rather than a window
    that has not started, so the share is held at nought rather than going
    negative and making every used share look ahead of the pace.
    """

    left = (resets_at - moment) / (WEEK_MINUTES * 60)
    return max(0.0, min(1.0, 1.0 - left)) * 100.0


def _nothing(harness: str, why: str) -> Account:
    """Return the account of a harness this machine has no figure for."""

    return Account(
        harness=harness,
        source=None,
        used_percent=None,
        elapsed_percent=None,
        resets_at=None,
        age_seconds=None,
        held_back=False,
        absent=why,
    )


def _written(data_dir: Path) -> tuple[dict[str, Figure], str | None]:
    """Return the figures the status line's file offers, and why it offers none.

    The reason is about the file rather than about a harness, so a harness the
    file does not name — or names in a shape this cannot read — falls back to
    `NOT_NAMED` at the caller. Both failures are the same thing to a reader:
    there is no readable window here.
    """

    path = data_dir / QUOTA_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, NO_FILE
    except OSError:
        return {}, UNREADABLE
    except ValueError:
        return {}, ANOTHER_SHAPE

    channels = raw.get("channels") if isinstance(raw, dict) else None
    if not isinstance(channels, dict):
        return {}, ANOTHER_SHAPE

    found: dict[str, Figure] = {}
    for harness, entry in channels.items():
        if not isinstance(harness, str):
            continue
        figure = _figure(harness, WRITTEN, entry, _epoch(_member(entry, "written_at")))
        if figure is not None:
            found[harness] = figure
    return found, None


def _logged(root: Path) -> tuple[Figure | None, str | None]:
    """Return the newest window Codex's own session logs carry, or None.

    Concurrent sessions each hold their own last-fetched value, so the
    machine-wide figure is the latest by the event's own timestamp across the
    files read — neither the newest file nor the last line of it.
    """

    try:
        recent = _recent(root)
    except OSError:
        # A broad enough catch to cover a tree being written while it is
        # listed. Nothing here may raise at a caller mid-task, and a machine
        # whose session tree cannot be listed simply has no figure.
        return None, NO_LOG

    newest: Figure | None = None
    for path in recent:
        figure = _tail(path)
        if figure is not None and (newest is None or figure.taken_at > newest.taken_at):
            newest = figure
    return (newest, None) if newest is not None else (None, NO_LOG)


def _recent(root: Path) -> list[Path]:
    """Return the most recently modified session logs, newest first."""

    dated = []
    for path in root.glob(CODEX_LOGS):
        try:
            dated.append((path.stat().st_mtime, path))
        except OSError:
            # A session log that went away between the listing and the stat.
            continue
    dated.sort(key=lambda found: found[0], reverse=True)
    return [path for _, path in dated[:CODEX_FILES]]


def _tail(path: Path) -> Figure | None:
    """Return the newest window in the end of one log, scanning backwards.

    The file is never parsed whole. A `token_count` event is written every turn
    and the last one is what the window is, so the end of the file answers the
    question and the rest of it is somebody's whole session.
    """

    try:
        with path.open("rb") as stream:
            stream.seek(0, os.SEEK_END)
            start = max(0, stream.tell() - CODEX_TAIL)
            stream.seek(start)
            tail = stream.read()
    except OSError:
        return None

    lines = tail.split(b"\n")
    if start > 0:
        # The read began mid-file, so the first fragment is half of a line.
        lines = lines[1:]

    for line in reversed(lines):
        figure = _event(line)
        if figure is not None:
            return figure
    return None


def _event(line: bytes) -> Figure | None:
    """Return the window one log line carries, or None where it carries none.

    An event with no `rate_limits` is skipped rather than ending the scan: a
    log's last events are frequently not `token_count` ones at all, and
    stopping at the first of those would read almost every session as a machine
    with no figure.
    """

    try:
        event = json.loads(line)
    except ValueError:
        return None
    if not isinstance(event, dict):
        return None

    payload = event.get("payload")
    if not isinstance(payload, dict):
        return None
    limits = payload.get("rate_limits")
    if not isinstance(limits, dict):
        return None

    taken = _instant(event.get("timestamp"))
    if taken is None:
        return None
    return _figure(CODEX, LOGGED, limits.get("primary"), taken)


def _figure(harness: str, source: str, entry: Any, taken: int | None) -> Figure | None:
    """Return one window as both sources spell it, or None where it is not one.

    Codex's own spellings throughout, so that the file the status line writes
    and the log Codex writes land in one shape and the rule is written once.
    Any window but the week is no figure: the thresholds were chosen for a week
    and say nothing about a five-hour window.
    """

    used = _number(_member(entry, "used_percent"))
    resets = _number(_member(entry, "resets_at"))
    window = _number(_member(entry, "window_minutes"))
    if used is None or resets is None or taken is None or window != WEEK_MINUTES:
        return None
    return Figure(harness, source, used, int(resets), taken)


def _member(entry: Any, name: str) -> Any:
    """Return one member of a JSON object, or None where it is not an object."""

    return entry.get(name) if isinstance(entry, dict) else None


def _instant(raw: Any) -> int | None:
    """Return an ISO 8601 instant as Unix epoch seconds, or None.

    A timestamp with no zone is read as UTC, which is what Codex writes and the
    only reading that cannot silently move a figure by the local offset.
    """

    if not isinstance(raw, str):
        return None
    try:
        moment = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return int(moment.timestamp())


def _epoch(raw: Any) -> int | None:
    """Return a Unix instant as whole seconds, or None where it is not one."""

    seconds = _number(raw)
    return None if seconds is None else int(seconds)


def _number(raw: Any) -> float | None:
    """Return a float, or None for anything that is not a number."""

    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    return float(raw)


def _rendered(account: Account) -> dict[str, Any]:
    """Return one account as the JSON object `status` renders."""

    return {
        "harness": account.harness,
        "source": account.source,
        "used_percent": account.used_percent,
        "elapsed_percent": (
            None
            if account.elapsed_percent is None
            else round(account.elapsed_percent, 1)
        ),
        "resets_at": account.resets_at,
        "age_seconds": (
            None if account.age_seconds is None else round(account.age_seconds)
        ),
        "held_back": account.held_back,
        "absent": account.absent,
    }


def _parse(argv: list[str] | None) -> argparse.Namespace:
    """Read the command line. The only thing in this module that may fail."""

    parser = argparse.ArgumentParser(
        prog="quota.py",
        description="Report each Harness's weekly subscription window.",
    )
    parser.add_argument("--data")
    parser.add_argument("--codex")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Print one account per harness as JSON and exit 0, whatever is there."""

    args = _parse(argv)
    data_dir = Path(args.data).expanduser() if args.data else data_root()
    root = Path(args.codex).expanduser() if args.codex else codex_root()
    print(
        json.dumps(
            {"accounts": [_rendered(account) for account in accounts(data_dir, root)]}
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
