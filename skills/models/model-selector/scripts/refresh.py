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
validator-conditional retrieval — ETag or Last-Modified, falling back to a
content hash — of the sources that are due. No model is started and no
evidence about anybody's work is written. The pass establishes what a source
says about the world; what the user's own work was worth is measured
elsewhere entirely.

## What it may touch, and what it may never store

**An unattended pass may now learn what a model costs** (ADR-0182). The rule
that it could learn what a model can do but never what it costs is reversed: a
rate card is exactly what this Skill has to be current about, and a price
carried with its source URL and its retrieval date is auditable in a way a
figure somebody typed eight months ago is not.

What the pass may never do is store a fact it cannot attribute. A source that
names no reader this module implements is retrieved and *not interpreted* —
its validators move and nothing else does — and an entry inside a source it
does read that claims an attribution this module cannot use is discarded
rather than re-attributed to whatever page it happened to arrive on. Failing
closed is what makes a source shape added later safe on the day it appears,
before anybody has taught this pass about it.

`FETCHABLE_KINDS` below is the complete list of what it may retrieve, and a
`kind` outside it — including one absent or unreadable — is still left for the
user's own `update`.

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

import catalogue
import profiles

SCHEMA_VERSION = 1

# Where the live source-state store sits, beside the measurement store under
# the selected data directory. Named here rather than imported from a peer:
# this module is an independent consumer of an on-disk contract.
SOURCE_STATE_FILE = "source-states.jsonl"

# The kinds an unattended pass may retrieve. It is now the whole documented
# vocabulary, the price-carrying kinds included (ADR-0182): what bounds the
# pass is attribution and a budget rather than a category of fact it is
# forbidden to look at. A value outside this set — one nobody has taught this
# module about — is still left for the user's own `update`.
FETCHABLE_KINDS = frozenset(
    {
        "model_release_index",
        "model_detail",
        "capability_source",
        "benchmark_release_index",
        "commercial_terms",
        "gateway_rate_card",
    }
)

# The whole pass, in seconds. It runs inside the hook that ends somebody's
# session, so the bound is on the pass rather than on each connection: a
# source reached after the budget is gone would be a source retrieved at the
# user's expense (ADR-0179).
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

# The two kinds that carry what a model costs rather than what it can do.
# They are retrieved like any other now; the name survives because `status`
# still says which of a machine's sources are the price-bearing ones.
COMMERCIAL_KINDS = frozenset({"commercial_terms", "gateway_rate_card"})

# The one document shape this pass knows how to make facts out of, named by a
# source's own `reads_as` member. A source naming no reader, or a reader this
# module has never heard of, is retrieved and left uninterpreted — which is
# every source on a machine until somebody registers one that is machine
# readable, and is why adding a reader later is safe.
READERS = frozenset({"catalogue-json"})
READER_FIELD = "reads_as"

# Exactly the members of a fetched entry that may reach the catalogue. Copied
# by name rather than passed through, so a document cannot smuggle a key into
# the file every decision is made from.
ENTRY_ALLOWED: tuple[str, ...] = (
    "id",
    "provider",
    "family",
    "aliases",
    "deliberation",
    "price",
    "long_context_threshold",
    "long_context",
    "reasoning_billed_as",
    "capability",
    "provider_says",
    "released",
)

# How old the user's own answers may be before `status` suggests revisiting
# them. Ninety days is roughly the interval at which this industry replaces a
# model somebody is paying for.
STALE_DAYS = 90

# What `status` names as the way to answer the questions again. The unattended
# pass asks nothing and stops nothing; saying so here is the whole of it.
SETUP = "/model-selector setup"


@dataclass(frozen=True)
class Retrieved:
    """One conditional retrieval's outcome, in the terms a `SourceState` records.

    `modified` is false where the server answered that the validators still
    hold, in which case it supplies neither a content hash nor a body.

    `body` is the bytes that arrived, kept only for as long as it takes a
    source's own reader to make facts out of them. A source naming no reader
    never has its body looked at, and no body is ever written anywhere.
    """

    modified: bool
    etag: str | None
    last_modified: str | None
    content_hash: str | None
    body: bytes | None = None


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
    reader: str | None
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
    row: dict[str, Any],
    line: int,
    now: datetime,
    shipped: dict[str, str | None],
    force: bool = False,
) -> Source:
    """Return one row's class and dueness, without retrieving anything.

    Fail closed: a kind outside `FETCHABLE_KINDS`, an absent kind, and a URI
    this pass may not open all leave the source to the user's own `update`.
    An unattended source with no retrieval on record has never been retrieved
    and is due; one whose kind has no cadence — an immutable model detail — is
    never due, because a known detail page is never fetched again.

    *force* is the user having typed `update --force`, which brings every
    mutable index forward to now. It does not reach a kind with no cadence:
    an immutable detail page says the same thing on every reading of it, so
    forcing one would spend a connection to learn nothing.
    """

    # Read defensively: this store is a file the user may hand-edit, and a
    # member of the wrong type is exactly the "unreadable" the fail-closed
    # rule below is written for.
    kind = row.get("kind") if isinstance(row.get("kind"), str) else None
    uri = row.get("uri") if isinstance(row.get("uri"), str) else None
    named = row.get(READER_FIELD)
    reader = named if isinstance(named, str) and named in READERS else None
    cadence = shipped.get(kind or "")

    # Why this pass may not retrieve the source, or None where it may.
    reason = None
    if kind not in FETCHABLE_KINDS:
        reason = "unrecognised_kind"
    elif uri is None or not uri.startswith(FETCHABLE_SCHEMES):
        reason = "unfetchable_uri"

    # A kind with a cadence is dated against its own last retrieval, and one
    # with no cadence is either an immutable detail nothing refetches — never
    # due — or a kind this pass does not know, which is always due, so a value
    # nobody has taught this module about is reported rather than dropped.
    retrieved = _parsed(row.get("last_retrieved_at"))
    next_due = _advanced(retrieved, cadence) if retrieved and cadence else None
    if cadence:
        due = force or next_due is None or next_due <= now
    else:
        due = reason is not None

    return Source(
        line=line,
        row=row,
        uri=uri,
        kind=kind,
        reader=reader,
        cadence=cadence,
        unattended=reason is None,
        reason=reason,
        next_due_at=_stamp(next_due) if next_due else None,
        due=due,
    )


def _plan(
    data: Path, now: datetime, force: bool = False
) -> tuple[list[str], list[Source], int]:
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
        sources.append(_classify(row, index, now, shipped, force))
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
            body = _body(response, deadline)
            if body is None:
                return None
            return Retrieved(
                modified=True,
                etag=response.headers.get("ETag"),
                last_modified=response.headers.get("Last-Modified"),
                content_hash=f"sha256:{hashlib.sha256(body).hexdigest()}",
                body=body,
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


def _body(response: Any, deadline: float) -> bytes | None:
    """Return one whole response body, or None where it cannot be bounded.

    Two bounds, both of which answer None rather than a partial read: a body
    larger than `MAX_RESPONSE_BYTES`, because a hash of a truncated body would
    report a page as unchanged on a change past the cut, and a body still
    arriving at the deadline, because this is spending a session's teardown.

    The bytes are kept rather than folded straight into a digest, so that a
    source naming a reader can be read without being fetched twice. They live
    exactly as long as the pass that fetched them.
    """

    chunks: list[bytes] = []
    read = 0
    while read <= MAX_RESPONSE_BYTES:
        if time.monotonic() >= deadline:
            return None
        chunk = response.read(CHUNK_BYTES)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
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


def _usable_url(raw: Any) -> str | None:
    """Return a URL this pass would be willing to say a fact came from."""

    return raw if isinstance(raw, str) and raw.startswith(FETCHABLE_SCHEMES) else None


def _entry(raw: Any, attribution: str | None, retrieved: str) -> dict[str, Any] | None:
    """Return one catalogue entry from one fetched one, or None where it has no source.

    The entry's own claim wins where it makes one. A claim this pass cannot
    use is a fact it cannot attribute, so the entry is discarded rather than
    quietly re-attributed to whatever page it happened to arrive on — which is
    the whole of what stops an unattended pass from inventing a rate card.
    """

    if not isinstance(raw, dict):
        return None
    identifier = raw.get("id")
    if not isinstance(identifier, str) or not identifier.strip():
        return None

    if "source_url" in raw:
        attribution = _usable_url(raw.get("source_url"))
    if attribution is None:
        return None

    entry = {key: raw[key] for key in ENTRY_ALLOWED if key in raw}
    entry["id"] = identifier
    entry["source_url"] = attribution
    entry["retrieved"] = retrieved
    return entry


def _learned(
    source: Source, body: bytes | None, retrieved: str
) -> list[dict[str, Any]]:
    """Return every catalogue entry one fetched document supports.

    A source naming no reader this module implements is not read at all: its
    validators moved and nothing else did. That is the state every source on
    every machine is in until somebody registers one that is machine readable,
    and it is what makes a reader added later safe on the day it appears.
    """

    if source.reader is None or body is None:
        return []
    try:
        document = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return []
    if not isinstance(document, dict):
        return []

    entries = document.get("models")
    if not isinstance(entries, list):
        return []

    attribution = (
        _usable_url(document.get("source_url"))
        if "source_url" in document
        else source.uri
    )
    return [
        entry
        for raw in entries
        if (entry := _entry(raw, attribution, retrieved)) is not None
    ]


def _placed(
    entry: dict[str, Any], known: dict[str, dict[str, str]]
) -> dict[str, Any] | None:
    """Return one entry with the two facts the catalogue cannot be read without.

    A document naming only a price for a model everything already knows is the
    ordinary case, and the catalogue's own reader rejects an entry carrying no
    provider and no family — so the entry is completed from what is already
    known rather than written in a shape nothing can load. A model nothing can
    place, and that names neither for itself, is not written at all.
    """

    identity = {
        **known.get(entry["id"], {}),
        **{key: entry[key] for key in ("provider", "family") if entry.get(key)},
    }
    if not identity.get("provider") or not identity.get("family"):
        return None
    return {**entry, **identity}


def _merge_catalogue(
    data: Path, entries: list[dict[str, Any]], stamp: str
) -> list[str]:
    """Fold what the pass learned into the refreshed catalogue, and say what moved.

    Field by field per model, so a pass that learned only a price leaves every
    other fact about that model exactly as it found it, and a model nothing
    knew about yesterday simply appears. Whether the profile enables it is not
    this file's question — `status` names it as something the user may want to
    adopt, and nothing here enables anything on anybody's behalf.
    """

    if not entries:
        return []

    path = data / catalogue.REFRESHED_FILE
    try:
        held = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        held = {}

    stored = held.get("models") if isinstance(held, dict) else None
    merged: dict[str, dict[str, Any]] = {
        row["id"]: row
        for row in (stored if isinstance(stored, list) else [])
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    known = {
        model.id: {"provider": model.provider, "family": model.family}
        for model in catalogue.load(data, _here()).models
    }

    written: list[str] = []
    for entry in entries:
        placed = _placed(entry, known)
        if placed is None:
            continue
        merged[entry["id"]] = {**merged.get(entry["id"], {}), **placed}
        written.append(entry["id"])

    if not written:
        return []

    # Through a temporary sibling and an atomic rename, as every store here is
    # written: a pass interrupted mid-write leaves the previous catalogue
    # standing rather than half of the new one.
    data.mkdir(parents=True, exist_ok=True)
    staged = path.parent / f"{path.name}.tmp"
    staged.write_text(
        json.dumps(
            {
                "generated_at": stamp,
                "models": [merged[name] for name in sorted(merged)],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    staged.replace(path)
    return sorted(set(written))


def refresh(
    data: Path,
    *,
    now: datetime | None = None,
    budget_seconds: float = BUDGET_SECONDS,
    retrieve: Retrieval | None = None,
    force: bool = False,
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
    lines, sources, unreadable = _plan(data, instant, force)

    # What the pass concluded, accumulated rather than written per source: one
    # rewrite of the store at the end is one moment it can be interrupted in.
    rewritten: dict[int, dict[str, Any]] = {}

    # What the pass concluded per source, which is not always the status the
    # row is left carrying — see `_status`.
    outcomes = {"unchanged": 0, "changed": 0, "not_due": 0}
    skipped = {"manual": 0, "unreachable": 0, "budget_exhausted": 0}

    # What the pass made of the sources it could read, accumulated the same
    # way and written once at the end, for the same reason.
    learned: list[dict[str, Any]] = []

    for source in sources:
        # A source this pass may not retrieve is left untouched entirely, so
        # that nothing about a source nobody has taught it about — its row's
        # own provenance included — is ever written by a pass nobody watched.
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
        learned += _learned(source, answer.body, stamp)

    # One rewrite of each store for the whole pass, and one account of it for
    # a caller that wants to see what happened.
    _write(data, lines, rewritten)
    adopted = _merge_catalogue(data, learned, stamp)

    return {
        "schema_version": SCHEMA_VERSION,
        "verb": "refresh",
        "data": str(data),
        "established": bool(sources),
        "considered": len(sources),
        "counts": {"known": len(sources), "unreadable": unreadable},
        "outcomes": outcomes,
        "skipped": skipped,
        "catalogue": adopted,
        "forced": force,
        "budget_seconds": budget_seconds,
    }


def _nudge(data: Path, instant: datetime) -> dict[str, Any]:
    """Say what the user may want to answer again, without asking them anything.

    Two things only, both of which the pass itself established and neither of
    which stops anything: answers old enough that this industry has replaced a
    model since, and models the catalogue now knows that the profile has never
    been asked about. Both name `setup`, and there the matter rests — a
    reminder placed anywhere a model reads would change what is being
    measured.
    """

    cat = catalogue.load(data, _here())
    profile = profiles.load(data, cat)
    enabled = set(profile.models)

    adoptable = sorted(model.id for model in cat.models if model.id not in enabled)
    unasked = sorted(
        {model.provider for model in cat.models if model.id not in enabled}
        - set(profile.providers)
    )

    answered = _parsed(profile.answered_at)
    stale = answered is None or (instant - answered).days > STALE_DAYS

    says: list[str] = []
    if profile.source == "file" and stale:
        says.append(f"the profile was answered more than {STALE_DAYS} days ago")
    if adoptable:
        says.append(f"{len(adoptable)} catalogue models are not enabled")
    if unasked:
        says.append(f"the profile was never asked about {', '.join(unasked)}")

    return {
        "profile_source": profile.source,
        "answered_at": profile.answered_at,
        "adoptable": adoptable,
        "unasked_providers": unasked,
        "says": f"{'; '.join(says)}; run `{SETUP}`" if says else None,
    }


def status(data: Path, *, now: datetime | None = None) -> dict[str, Any]:
    """Report what unattended refresh can and cannot keep current under *data*.

    This is the one surface the pass is reported on. It retrieves nothing and
    writes nothing, and it names `/model-selector update` as what resolves a
    source this pass could not reach or read, and `/model-selector setup` as
    what answers a profile the world has moved past.
    """

    instant = now or _now()
    _, sources, unreadable = _plan(data, instant)
    return {
        "profile": _nudge(data, instant),
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
                "priced": source.kind in COMMERCIAL_KINDS,
                "reads_as": source.reader,
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

    # `--force` is what `/model-selector update --force` promises: every
    # mutable index checked once, now, rather than when its cadence next
    # elapses. It changes nothing else about the pass — the budget, the one
    # connection at a time, and what may be stored are all unmoved.
    parser.add_argument("--force", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one refresh action."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = Path(args.data)
    if args.action == "refresh":
        _emit(refresh(data, force=args.force))
    else:
        _emit(status(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
