# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Keep the source states current without anybody typing `update`.

Discovery exists in this Skill and nothing ever ran it. `update` revalidates
provider indexes on a cadence and reports what it finds, but every turn of
that loop is a thing the user has to remember, so the machine could sit weeks
past every cadence answering from a model list nobody had revisited — silently
and confidently, because no verb reports an empty answer (issue #247).

This module is the turn nobody has to remember. It rides the session-end
invocation this Skill's lifecycle integration already installs, and it does
exactly one thing: validator-conditional retrieval — ETag or Last-Modified,
falling back to a content hash — of the non-commercial sources that are due.
**It interprets nothing.** No page is parsed for meaning, no model is started,
and no evidence beyond the source's own state is written. The unattended pass
establishes *that* something moved; the person's next `update` establishes
*what* (ADR-0167).

## What it may touch, and what it may never touch

An unattended fetch that mis-parsed a commercial page would write a wrong
fact that silently reshapes which model wins, and the user holds knowledge
those pages do not state — what a plan actually costs and how a quota
actually behaves. So the split is by `kind`, and it is the whole design:

**An unattended pass may change what a model is judged capable of, never what
it is judged to cost.** `FETCHABLE_KINDS` below is the complete list of what
it may retrieve; `commercial_terms`, `gateway_rate_card`, and **any other
value, including one absent or unreadable, are treated as commercial** — not
fetched, and reported as due by `status` until the user runs `update`. Failing
closed is what makes a `kind` added later safe on the day it appears, before
anybody has taught this pass about it.

## Dueness, and the defect this module must not reinstall

Cadence is measured from `last_retrieved_at` and from nothing else. A source
found not due records the look in `last_checked_at` and never touches the
retrieval field, because measuring cadence from the last look would push every
source's next due date forward at every session end and nothing would ever
become due again — which is issue #247's own defect, reinstalled by its fix.

A source whose `last_retrieved_at` is absent or null has never been retrieved
and is due. That is the state every existing row is in: the field is new here,
and the retrieval date lived only inside `finding` prose nothing parses. No
migration is written and no prose is read; the field starts empty and the
first pass fills it.

## What it costs a session

Nothing anybody can feel, and that is a number rather than an intention: one
connection at a time, no retries, and a total budget of `BUDGET_SECONDS`
across the whole pass, enforced in-process. Exceeding it, or reaching no
network at all, changes no fact the store holds about a source and leaves
every unfinished source due for the next attempt.

Every retrieval failure is answered here, as an unreachable source. A failure
of the store itself — an unwritable directory, a name a directory holds — is
raised rather than hidden, and the caller is what swallows it: `capture.py`
suppresses everything this module can raise, exactly as it already does for
its own work, which is where the guarantee that a refresh never costs a
session belongs. Nothing here surfaces anything to the user either way.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol

SCHEMA_VERSION = 1

# Where the live source-state store sits, beside the evidence ledger under
# the selected data directory. Named here rather than imported from a peer:
# this module is an independent consumer of an on-disk contract, the posture
# `usage_evidence.py` already takes on capture's own store.
SOURCE_STATE_FILE = "source-states.jsonl"

# The kinds an unattended pass may retrieve. Everything outside this set is
# commercial as far as this module is concerned — the two documented
# commercial kinds and every value it does not recognise alike — and is left
# for the user's own `update`. `references/evidence-ledger.md` holds the
# closed six-value vocabulary these four are drawn from.
FETCHABLE_KINDS = frozenset(
    {
        "model_release_index",
        "model_detail",
        "capability_source",
        "benchmark_release_index",
    }
)

# The whole pass, in seconds. It runs inside the hook that ends somebody's
# session, so the bound is on the pass rather than on each connection: a
# source reached after the budget is gone would be a source retrieved at the
# user's expense (ADR-0167).
BUDGET_SECONDS = 2.0

# What a conditional retrieval may read before the source is abandoned as
# unvalidatable. A hash of a truncated body is a validator that would report
# a page as unchanged on a change past the cut, so an oversized response is
# reported as unreachable and stays due for the typed `update` instead.
MAX_RESPONSE_BYTES = 4 * 1024 * 1024

# How much of a response body is read at a time, so the deadline above is
# checked between reads rather than only before the first one.
CHUNK_BYTES = 64 * 1024

# The statuses only a typed `update` can establish, because both are readings
# of a source rather than facts about reaching one. `_status` keeps them.
UNRESOLVED_STATUSES = frozenset({"unreachable", "invalid"})

# Sent so a provider can see who is asking. Nothing else travels: no cookie,
# no credential, and no identifier of this machine or its user.
USER_AGENT = "kntnt-model-selector-refresh/1"

# The schemes a stored URI may carry. The store is a file a user may
# hand-edit, so a `file://` row must never become a local read.
FETCHABLE_SCHEMES = ("https://", "http://")

# ISO-8601 durations, in the subset a cadence is written in. Years and months
# advance the calendar; weeks and days are exact spans.
DURATION = re.compile(
    r"^P(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?(?:(?P<weeks>\d+)W)?(?:(?P<days>\d+)D)?$"
)

# The two kinds the vocabulary itself calls commercial. Every other value
# outside `FETCHABLE_KINDS` is treated the same way and reported as such.
COMMERCIAL_KINDS = frozenset({"commercial_terms", "gateway_rate_card"})


@dataclass(frozen=True)
class Retrieved:
    """One conditional retrieval's outcome, in the terms a `SourceState` records.

    `modified` is false where the server answered that the validators still
    hold, in which case it supplies no content hash. Nothing here describes
    what the source says: reading that is the typed `update`'s work.
    """

    modified: bool
    etag: str | None
    last_modified: str | None
    content_hash: str | None


class Retrieval(Protocol):
    """The one seam this module reaches the network through."""

    def __call__(
        self, uri: str, etag: str | None, last_modified: str | None, timeout: float
    ) -> Retrieved | None:
        """Retrieve *uri* conditionally, or answer None where nothing could."""


@dataclass(frozen=True)
class Source:
    """One store row, classified and dated, before anything is retrieved.

    This is what both verbs are built on: `refresh` retrieves the due members
    of it that it may, and `status` reports the same classification without
    retrieving anything at all.
    """

    line: int
    row: dict[str, Any]
    uri: str | None
    kind: str | None
    cadence: str | None
    unattended: bool
    reason: str | None
    next_due_at: str | None
    due: bool


def default_data() -> Path:
    """Return the data directory this Skill keeps its evidence in by default."""

    return Path.home() / ".kntnt" / "model-selector"


def _here() -> Path:
    """Return the Skill directory this module ships inside."""

    return Path(__file__).resolve().parent.parent


def cadences() -> dict[str, str | None]:
    """Return the shipped default cadence per source kind.

    They are data rather than sentences because code has to read them: they
    were prose in `references/evidence-ledger.md` and in no shipped file, so
    nothing could compute dueness from them. The configuration does not
    override them — the profile carries no cadence member and never did.
    """

    shipped = json.loads(
        (_here() / "data" / "refresh-cadences.json").read_text(encoding="utf-8")
    )
    return dict(shipped["cadences"])


def _now() -> datetime:
    """Return this instant, as a source state dates one."""

    return datetime.now(UTC)


def _stamp(instant: datetime) -> str:
    """Return one instant in the form every stored timestamp is written in."""

    return instant.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parsed(instant: Any) -> datetime | None:
    """Return one recorded instant as a datetime, or None where it is unusable."""

    if not isinstance(instant, str) or not instant:
        return None

    try:
        parsed = datetime.fromisoformat(instant)
    except ValueError:
        return None

    # A stored instant is written in UTC; one hand-edited without an offset is
    # read as UTC rather than as this machine's local time.
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _advanced(instant: datetime, cadence: str) -> datetime | None:
    """Return when *instant* next falls due under *cadence*.

    Months and years advance the calendar rather than a fixed span of days,
    because "monthly" is what the reference says and 2026-08-23 plus a month
    is 2026-09-23. A day that the target month is too short for takes that
    month's last day, the ordinary reading of a monthly schedule.
    """

    match = DURATION.match(cadence)
    if match is None or not any(match.groups()):
        return None
    parts = {name: int(value or 0) for name, value in match.groupdict().items()}

    # The calendar step first, so the exact span below is added to a real date.
    months = instant.month - 1 + parts["years"] * 12 + parts["months"]
    year = instant.year + months // 12
    month = months % 12 + 1
    day = min(instant.day, _days_in(year, month))
    stepped = instant.replace(year=year, month=month, day=day)

    return stepped + timedelta(weeks=parts["weeks"], days=parts["days"])


def _days_in(year: int, month: int) -> int:
    """Return how many days one calendar month holds."""

    following = datetime(year + month // 12, month % 12 + 1, 1, tzinfo=UTC)
    return (following - timedelta(days=1)).day


def _lines(data: Path) -> list[str]:
    """Return the source-state store's own lines, or none where there is no store.

    An unreadable store is an absence rather than a failure, exactly as every
    other read of this Skill's hand-editable JSONL answers.
    """

    path = data / SOURCE_STATE_FILE
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return [line for line in text.splitlines() if line.strip()]


def _classify(
    row: dict[str, Any], line: int, now: datetime, shipped: dict[str, str | None]
) -> Source:
    """Return one row's class and dueness, without retrieving anything.

    Fail closed: a kind outside `FETCHABLE_KINDS`, an absent kind, and a URI
    this pass may not open all leave the source to the user's own `update`.
    An unattended source with no retrieval on record has never been retrieved
    and is due; one whose kind has no cadence — an immutable model detail — is
    never due, because a known detail page is never fetched again.
    """

    # Read defensively: this store is a file the user may hand-edit, and a
    # member of the wrong type is exactly the "unreadable" the fail-closed
    # rule below is written for.
    kind = row.get("kind") if isinstance(row.get("kind"), str) else None
    uri = row.get("uri") if isinstance(row.get("uri"), str) else None
    cadence = shipped.get(kind or "")

    # Why this pass may not retrieve the source, or None where it may.
    reason = None
    if kind not in FETCHABLE_KINDS:
        commercial = kind in COMMERCIAL_KINDS
        reason = "commercial" if commercial else "unrecognised_kind"
    elif uri is None or not uri.startswith(FETCHABLE_SCHEMES):
        reason = "unfetchable_uri"

    # A kind with a cadence is dated against its own last retrieval, and one
    # with no cadence is either an immutable detail nothing refetches — never
    # due — or a kind this pass does not know, which is always due, so a value
    # nobody has taught this module about is reported rather than dropped.
    retrieved = _parsed(row.get("last_retrieved_at"))
    next_due = _advanced(retrieved, cadence) if retrieved and cadence else None
    if cadence:
        due = next_due is None or next_due <= now
    else:
        due = reason is not None

    return Source(
        line=line,
        row=row,
        uri=uri,
        kind=kind,
        cadence=cadence,
        unattended=reason is None,
        reason=reason,
        next_due_at=_stamp(next_due) if next_due else None,
        due=due,
    )


def _plan(data: Path, now: datetime) -> tuple[list[str], list[Source], int]:
    """Return the store's lines, every row it could read, and how many it could not."""

    lines = _lines(data)
    shipped = cadences()
    sources: list[Source] = []
    unreadable = 0
    for index, line in enumerate(lines):
        try:
            row = json.loads(line)
        except ValueError:
            unreadable += 1
            continue
        if not isinstance(row, dict):
            unreadable += 1
            continue
        sources.append(_classify(row, index, now, shipped))
    return lines, sources, unreadable


def _retrieve(
    uri: str, etag: str | None, last_modified: str | None, timeout: float
) -> Retrieved | None:
    """Retrieve one source conditionally, within *timeout* seconds in total.

    *timeout* is the whole allowance for this one source, not a per-socket
    limit: a server that accepts the connection and then drips bytes would
    otherwise spend it once on connecting and again on every read, and the
    pass's own budget would bound nothing. Half of it goes to the socket, so
    no single blocking operation can outlast the allowance, and the body is
    read in chunks against a deadline computed from the whole of it.

    Every failure answers None, which leaves the source exactly as it was and
    due for the next attempt: this runs inside somebody's session teardown,
    where a raised error would be worse than a source nobody refreshed.
    """

    # Whichever validators the source's own row holds, so a source that has
    # not moved answers 304 and costs a header exchange.
    request = urllib.request.Request(uri, headers={"User-Agent": USER_AGENT})
    if etag:
        request.add_header("If-None-Match", etag)
    if last_modified:
        request.add_header("If-Modified-Since", last_modified)

    deadline = time.monotonic() + timeout
    try:
        with urllib.request.urlopen(request, timeout=timeout / 2) as response:
            digest = _hashed(response, deadline)
            if digest is None:
                return None
            return Retrieved(
                modified=True,
                etag=response.headers.get("ETag"),
                last_modified=response.headers.get("Last-Modified"),
                content_hash=digest,
            )
    except urllib.error.HTTPError as error:
        if error.code != 304:
            return None
        return Retrieved(
            modified=False,
            etag=error.headers.get("ETag"),
            last_modified=error.headers.get("Last-Modified"),
            content_hash=None,
        )
    except Exception:  # noqa: BLE001 - the unattended pass is fail-open by contract
        return None


def _hashed(response: Any, deadline: float) -> str | None:
    """Return one response body's digest, or None where it cannot be bounded.

    Two bounds, both of which answer None rather than a partial digest: a
    body larger than `MAX_RESPONSE_BYTES`, because a hash of a truncated body
    would report a page as unchanged on a change past the cut, and a body
    still arriving at the deadline, because this is spending a session's
    teardown.
    """

    digest = hashlib.sha256()
    read = 0
    while read <= MAX_RESPONSE_BYTES:
        if time.monotonic() >= deadline:
            return None
        chunk = response.read(CHUNK_BYTES)
        if not chunk:
            return f"sha256:{digest.hexdigest()}"
        digest.update(chunk)
        read += len(chunk)
    return None


def _status(row: dict[str, Any], concluded: str, changed: bool) -> str:
    """Return the status this pass may leave on one row.

    A typed `update`'s unresolved diagnostic — a source it could not reach, or
    retrieved and could not read — is not this pass's to clear, because this
    pass reads nothing and so establishes nothing that answers either. Only
    content that actually moved supersedes one: a look, and a retrieval that
    finds the same bytes, leave it standing where the user can still see it.
    """

    recorded = row.get("status")
    if changed or recorded not in UNRESOLVED_STATUSES:
        return concluded
    return str(recorded)


def _retrieved_row(
    row: dict[str, Any], answer: Retrieved, now: str
) -> tuple[dict[str, Any], str]:
    """Return one row updated by a retrieval, and what that retrieval concluded.

    The two are not always the same word: `_status` may keep a diagnostic the
    row already carried, while what this pass concluded about the source is
    still `unchanged` or `changed`, and that is what the pass reports.

    Only the members a retrieval speaks to move. `finding` and
    `parser_version` are the typed `update`'s own record of what it made of
    the source, and this pass makes nothing of it, so both are left as that
    pass wrote them.
    """

    content_hash = answer.content_hash or row.get("content_hash")
    changed = answer.modified and content_hash != row.get("content_hash")
    concluded = "changed" if changed else "unchanged"

    return {
        **row,
        "status": _status(row, concluded, changed),
        "etag": answer.etag or row.get("etag"),
        "last_modified": answer.last_modified or row.get("last_modified"),
        "content_hash": content_hash,
        "last_checked_at": now,
        "last_retrieved_at": now,
        "last_changed_at": now if changed else row.get("last_changed_at"),
    }, concluded


def _write(data: Path, lines: list[str], rewritten: dict[int, dict[str, Any]]) -> None:
    """Replace the changed rows in place, appending nothing.

    The store holds one row per source with no superseding history, so a pass
    rewrites the row for each source it concluded on and leaves every other
    line exactly as it found it — the untouched ones by their own original
    text, so a row this module does not understand cannot be reshaped by
    being read and written back.
    """

    if not rewritten:
        return

    # Every line the pass concluded on, re-serialized; every other line by its
    # own original text.
    kept = [
        json.dumps(rewritten[index], sort_keys=True) if index in rewritten else line
        for index, line in enumerate(lines)
    ]

    # Through a temporary sibling and an atomic rename, as the reference asks
    # of every store here. A write that fails raises, and the caller is what
    # answers for it.
    path = data / SOURCE_STATE_FILE
    temporary = path.parent / f"{path.name}.tmp"
    temporary.write_text("".join(line + "\n" for line in kept), encoding="utf-8")
    temporary.replace(path)


def refresh(
    data: Path,
    *,
    now: datetime | None = None,
    budget_seconds: float = BUDGET_SECONDS,
    retrieve: Retrieval | None = None,
) -> dict[str, Any]:
    """Run one unattended pass over the source states under *data*.

    Writes `SourceState` rows and nothing else: no capability fact, no
    benchmark fact, no evidence record, and no derived frontier is created,
    changed or rebuilt by it. It answers every retrieval failure itself and
    raises only where the store cannot be written, which its caller swallows. A machine that has run `setup` and never
    `update` has no rows to iterate, so the pass correctly does nothing —
    `status` is where that is said, because a permanently empty pass must not
    be indistinguishable from a working one.
    """

    # The clock the budget is spent against is monotonic, so a machine whose
    # wall clock moves mid-pass cannot extend or end it.
    instant = now or _now()
    stamp = _stamp(instant)
    fetch = retrieve or _retrieve
    deadline = time.monotonic() + budget_seconds
    lines, sources, unreadable = _plan(data, instant)

    # What the pass concluded, accumulated rather than written per source: one
    # rewrite of the store at the end is one moment it can be interrupted in.
    rewritten: dict[int, dict[str, Any]] = {}

    # What the pass concluded per source, which is not always the status the
    # row is left carrying — see `_status`.
    outcomes = {"unchanged": 0, "changed": 0, "not_due": 0}
    skipped = {"manual": 0, "unreachable": 0, "budget_exhausted": 0}

    for source in sources:
        # A source this pass may not retrieve is left untouched entirely, so
        # that nothing about a commercial source — its row's own provenance
        # included — is ever written by a pass nobody watched.
        if not source.unattended:
            skipped["manual"] += 1
            continue

        # A source whose cadence has not elapsed records the look and keeps
        # every fact it had, its retrieval timestamp above all.
        if not source.due:
            rewritten[source.line] = {
                **source.row,
                "status": _status(source.row, "not_due", changed=False),
                "last_checked_at": stamp,
            }
            outcomes["not_due"] += 1
            continue

        # One connection at a time, no retries, and never one started with no
        # budget left to finish it in.
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            skipped["budget_exhausted"] += 1
            continue
        answer = fetch(
            str(source.uri),
            source.row.get("etag"),
            source.row.get("last_modified"),
            remaining,
        )
        if answer is None:
            # A source nothing could reach records the look and nothing else.
            # Its validators, its status and its dueness stay exactly what
            # they were, so the next pass attempts it again.
            rewritten[source.line] = {**source.row, "last_checked_at": stamp}
            skipped["unreachable"] += 1
            continue
        rewritten[source.line], concluded = _retrieved_row(source.row, answer, stamp)
        outcomes[concluded] += 1

    # One rewrite for the whole pass, and one account of it for a caller that
    # wants to see what happened.
    _write(data, lines, rewritten)

    return {
        "schema_version": SCHEMA_VERSION,
        "verb": "refresh",
        "data": str(data),
        "established": bool(sources),
        "considered": len(sources),
        "counts": {"known": len(sources), "unreadable": unreadable},
        "outcomes": outcomes,
        "skipped": skipped,
        "budget_seconds": budget_seconds,
    }


def status(data: Path, *, now: datetime | None = None) -> dict[str, Any]:
    """Report what unattended refresh can and cannot keep current under *data*.

    This is the one surface the pass is reported on. It retrieves nothing and
    writes nothing, and it names `/model-selector update` as what resolves
    both the sources this pass may never fetch and a machine that has no
    source states at all.
    """

    instant = now or _now()
    _, sources, unreadable = _plan(data, instant)
    return {
        "schema_version": SCHEMA_VERSION,
        "verb": "status",
        "data": str(data),
        "store": str(data / SOURCE_STATE_FILE),
        "established": bool(sources),
        "sources": [
            {
                "source_key": source.row.get("source_key"),
                "uri": source.uri,
                "provider": source.row.get("provider"),
                "kind": source.kind,
                "unattended": source.unattended,
                "reason": source.reason,
                "cadence": source.cadence,
                "last_retrieved_at": source.row.get("last_retrieved_at"),
                "next_due_at": source.next_due_at,
                "due": source.due,
                "recorded_status": source.row.get("status"),
            }
            for source in sources
        ],
        "counts": {
            "known": len(sources),
            "unreadable": unreadable,
            "unattended_due": sum(1 for one in sources if one.unattended and one.due),
            "manual_due": sum(1 for one in sources if not one.unattended and one.due),
        },
        "resolves": "/model-selector update",
    }


def _emit(payload: dict[str, Any]) -> None:
    """Print one machine-readable answer."""

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse one refresh invocation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("refresh", "status"))
    parser.add_argument("--data", default=str(default_data()))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one refresh action."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = Path(args.data)
    _emit(refresh(data) if args.action == "refresh" else status(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
