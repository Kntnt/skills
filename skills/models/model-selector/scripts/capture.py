# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Capture local session usage automatically during ordinary Harness work.

A user works in their Harness all day, and what that costs — the Seat it ran
on, what it used, how long it took — is never written down, because writing
it down is a thing they have to remember to do. This is that capture, and it
measures ordinary work; it never judges it (ADR-0156). An ordinary session has
no independent verifier in it, so a finished session produces a Usage Record
rather than a `RunObservation`: one per Seat it ran on, carrying no outcome,
no checker, and no Cohort, appended to its own store the moment the session
ends. Nothing waits for a human, ever.

Capture follows this Skill's own Enabled state and asks for nothing beyond
it (#223). The Manager installs this feature's owned lifecycle integration
into every supported Detected Harness of the Global layer the moment the
Skill is Enabled, placed, or refreshed, and removes every entry the moment
it is Disabled — the same two seams that already place and remove the
Skill's own files. There is no second opt-in, no consent prompt, and no
configuration state of this feature's own to go stale: disk is the one
truth (ADR-0090), so a hook either runs because a Harness's own
configuration names it or it does not run at all. What it writes is the
minimum a Usage Record needs: identities are opaque, measurements the
environment did not expose stay `null`, and no prompt, response, reasoning,
diff, terminal output, or transcript is ever copied.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

# Every lifecycle signal this feature understands, per Harness family. A stop
# is one turn of an ongoing session and never a session's own end; a Seat's
# Usage Record is timed on its own first and last such turn. Codex CLI
# 0.153.0's own `hooks.json` names its moments in the same PascalCase Claude
# Code's `settings.json` does, which is what this feature's own hook table is
# registered under; the camelCase spellings (`sessionStart`, `stop`,
# `sessionEnd`) are the app-server protocol's own `HookEventName`, the
# normalized runtime view `hooks/list` reports back, and are accepted here as
# the same convention rather than as a confirmed reading of any payload
# (ADR-0157).
START_EVENTS = frozenset({"SessionStart", "sessionStart", "session.created"})
TURN_EVENTS = frozenset({"Stop", "stop", "SubagentStop", "session.idle"})
ERROR_EVENTS = frozenset({"session.error"})
END_EVENTS = frozenset({"SessionEnd", "sessionEnd", "session.deleted"})

# Where a Harness names the lifecycle moment inside the payload rather than on
# the command line. Claude Code and Codex both do, so a hook installed without a
# per-event command still knows which moment it is answering. `eventName` is
# Codex's own field for this everywhere else its JSON API names a moment
# (`hooks/list`'s `HookMetadata`, its `HookRunSummary` notifications); its
# hook-invocation payload was not directly observable — every attempt to
# drive a hook to fire, trust-bypassed or not, ran into Codex's own
# session/auth lifecycle rather than a shape problem — so this is carried as
# the same convention rather than as a confirmed reading of that payload.
EVENT_FIELDS: tuple[str, ...] = ("hook_event_name", "eventName", "event", "type")

# The usage categories a Usage Record may carry, so that an object named
# `measurements` in a Harness payload cannot smuggle material in under a
# wanted key. Named rather than counted, so a key added here is a key this
# comment still describes (ADR-0156).
MEASUREMENT_ALLOWED = frozenset(
    {
        "tokens",
        "tool_calls",
        "retries",
        "cost",
        "quota",
        "latency",
        "fallback_from",
    }
)

# The only fields a lifecycle payload may contribute. Everything else a
# Harness sends — and Harnesses send whole transcripts — is dropped before
# anything is written, so nothing forbidden can arrive by sitting beside what
# is wanted. A Usage Record carries no outcome, so a payload's checker and
# error content are never read for their value, only the event name is.
#
# `transcript_path` is locate-only (#225): it is read at a session's end to
# open that session's own finished record through the Collection Library's
# reader, and it never reaches a draft written to disk or a Usage Record —
# `_hook` reads it locally out of the cleaned payload and passes it straight
# to `_finish` without ever folding it into the draft this dict's other
# fields build up.
PAYLOAD_ALLOWED = frozenset(
    {
        "session_id",
        "harness",
        "harness_inventory_revision",
        "seat",
        "measurements",
        "transcript_path",
    }
)
SEAT_ALLOWED = frozenset(
    {
        "model",
        "resolved_alias",
        "portable_deliberation",
        "native_deliberation",
        "channel",
        "surface",
        "adapter_id",
        "serving_mode",
    }
)

# Where the Usage Record store lives, beside the evidence ledger under the
# selected data directory, and the fields every row carries. Named once here
# rather than left for a consumer to infer, following the Library's own
# precedent for its ledger file (`LEDGER_FILE` in `routed_observations.py`).
USAGE_LEDGER_FILE = "usage-records.jsonl"
USAGE_RECORD_FIELDS: tuple[str, ...] = (
    "usage_key",
    "session_identity",
    "harness",
    "seat",
    "usage",
    "started_at",
    "completed_at",
    "elapsed_seconds",
)


def _now() -> str:
    """Return this instant, as a Usage Record writes instants."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _parsed(instant: Any) -> datetime | None:
    """Return one recorded instant as a datetime, or None where it is unusable."""

    if not isinstance(instant, str):
        return None
    try:
        return datetime.fromisoformat(instant)
    except ValueError:
        return None


def _opaque(value: Any) -> str:
    """Return one stable opaque identity for a Harness-supplied identifier.

    A session id is a path, a ticket number, or a workspace name often enough
    that keeping it raw would leak exactly what the data boundary excludes. The
    digest is stable, so the same session is the same identity across events.
    """

    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return digest[:32]


def home(data: Path) -> Path:
    """Return the capture home inside one data directory."""

    return data / "capture"


def _drafts(data: Path) -> Path:
    """Return where per-session drafts are kept."""

    return home(data) / "drafts"


def _by_path(name: str, *candidates: Path) -> Any:
    """Load one module by path under *name*, from the first candidate that exists.

    Every module this one reaches is loaded this way rather than imported: a
    Skill's scripts are placed, not installed, so there is no package for an
    ordinary import to resolve against. The loaded module is registered under
    *name* before it executes, which is what lets its own dataclasses resolve
    the annotations they declare.
    """

    for candidate in candidates:
        if not candidate.exists():
            continue
        spec = importlib.util.spec_from_file_location(name, candidate)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    raise RuntimeError(f"{name} is missing")


def _library(*relative: str) -> tuple[Path, Path]:
    """Return the two places a Collection Library module may sit, in order.

    Two layouts, tried in turn: this repository's own
    `skills/models/model-selector/scripts/` sits three directories above
    `skills/kntnt/library/`, while an Enabled Skill's installed copy — the
    only copy the Manager's own install and remove seams ever run (#223) —
    sits at `<layer>/model-selector/scripts/`, two directories above the
    sibling `<layer>/kntnt/library/`.
    """

    here = Path(__file__).resolve().parent
    tail = Path("kntnt", "library", "scripts", *relative)
    return here.parent.parent.parent / tail, here.parent.parent / tail


def _integrations() -> Any:
    """Load the Collection Library's owned-integration mechanics.

    Harness-specific installation is not this feature's knowledge to hold: it is
    the Library's, so that a second Skill needing the same thing finds it there
    rather than reaching into this one (ADR-0012).
    """

    return _by_path("kntnt_integrations", *_library("integrations.py"))


def _session_records() -> Any:
    """Load the Collection Library's session-record reader.

    Reading a finished session's own record is Harness-specific mechanics of
    exactly the kind ADR-0090 already put in the Library, so it lives beside
    `integrations.py` rather than here — a second consumer finds it there
    instead of reaching into this Skill (#225).
    """

    return _by_path("kntnt_session_records", *_library("session_records.py"))


def _refresh() -> Any:
    """Load this Skill's own unattended source refresh, from beside this module.

    It is this Skill's own knowledge rather than the Library's, so it sits in
    `scripts/` next to this file and needs neither of the two layouts a
    Library module is resolved through.
    """

    return _by_path(
        "model_selector_refresh", Path(__file__).resolve().parent / "refresh.py"
    )


def owner() -> str:
    """Return the stable ownership identity every installed integration carries."""

    return "kntnt.model-selector.capture"


def install(
    data: Path, root: Path, harnesses: list[str], command: list[str]
) -> dict[str, Any]:
    """Install this feature's owned integration, idempotently.

    This is the word the Manager says at every seam that places or refreshes
    an Enabled Skill's files (#223): install, repair, and refresh are the
    same convergence over whatever is on disk (ADR-0090), so being asked
    twice changes nothing. Naming no Harness means every Harness the
    Collection Library has an adapter for.

    Only a named Harness the Library's `integrations.SUPPORTED` actually
    holds an adapter for is attempted; the rest is reported as a single
    count naming the supported set rather than one row each, because a
    caller naming Detected Harnesses in bulk — this collection ships an
    adapter for three of the seventy-odd this machine may have — would
    otherwise bury the outcome that matters under rows for Harnesses no
    adapter exists for (#223 decision 3).
    """

    integrations = _integrations()
    supported = set(integrations.SUPPORTED)
    named = list(harnesses) or list(integrations.SUPPORTED)
    attempted = [harness for harness in named if harness in supported]
    unsupported = [harness for harness in named if harness not in supported]
    runs = _hook_command(command, data)
    installed = [
        integrations.install(owner(), harness, root, runs) for harness in attempted
    ]
    return {
        "installed": installed,
        "unsupported": {"count": len(unsupported), "supported": sorted(supported)},
    }


def disable(data: Path, root: Path) -> dict[str, Any]:
    """Remove every integration this feature owns, wherever it installed one.

    Accepted Usage Records are untouched. Every Harness the Collection
    Library has an adapter for is attempted, whether or not this machine
    ever held our entry there: removal reads the Harness's own file and
    converges it (ADR-0090), so trying one that never carried our entry is a
    converged state rather than an error, and there is no separate on/off
    flag of this feature's own left to update — the Harness's own
    configuration is the one truth capture ever reads.
    """

    integrations = _integrations()
    removed = [
        integrations.remove(owner(), harness, root)
        for harness in integrations.SUPPORTED
    ]
    return {"harnesses": removed}


def _opencode_session_id(payload: dict[str, Any]) -> str | None:
    """Return the session identity OpenCode's own event envelope carries.

    OpenCode's plugin hands its event object on unmodified (ADR-0090: it
    interprets nothing), and that object never carries the identity where
    Claude Code and Codex do — it nests it inside `properties`, and at a
    different path per event: `session.idle` names it directly as
    `sessionID`, while `session.created` and `session.deleted` embed it in
    the session record at `info.id`.
    """

    properties = payload.get("properties")
    if not isinstance(properties, dict):
        return None
    session_id = properties.get("sessionID")
    if isinstance(session_id, str) and session_id:
        return session_id
    info = properties.get("info")
    if isinstance(info, dict):
        info_id = info.get("id")
        if isinstance(info_id, str) and info_id:
            return info_id
    return None


def _normalized(payload: Any) -> dict[str, Any]:
    """Return one lifecycle payload with a Harness's own envelope unwrapped.

    Claude Code and Codex already hand over a flat payload naming what this
    feature needs directly, under the keys `_clean` allow-lists. OpenCode's
    forwarded event does not, so its session identity is found here once
    rather than by every caller of `_clean` re-deriving OpenCode's own shape.
    """

    if not isinstance(payload, dict):
        return {}
    if isinstance(payload.get("session_id"), str) and payload["session_id"]:
        return payload
    session_id = _opencode_session_id(payload)
    if session_id is None:
        return payload
    return {**payload, "session_id": session_id}


def _clean(payload: Any) -> dict[str, Any]:
    """Return only the allow-listed fields of one lifecycle payload."""

    if not isinstance(payload, dict):
        return {}
    kept = {key: value for key, value in payload.items() if key in PAYLOAD_ALLOWED}
    seat = kept.get("seat")
    if isinstance(seat, dict):
        kept["seat"] = {key: seat.get(key) for key in SEAT_ALLOWED}

    # An allow-list one level deep is no allow-list: a nested object is filtered
    # by its own keys rather than copied because its parent's key was wanted.
    measurements = kept.get("measurements")
    if isinstance(measurements, dict):
        kept["measurements"] = {
            key: value
            for key, value in measurements.items()
            if key in MEASUREMENT_ALLOWED
        }
    return kept


def _draft_path(data: Path, session: str) -> Path:
    """Return where one session's draft is kept."""

    return _drafts(data) / f"{_opaque(session)}.json"


def _draft(data: Path, session: str) -> dict[str, Any] | None:
    """Return one session's draft, or None where there is none to read."""

    path = _draft_path(data, session)
    if not path.exists():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def _store(path: Path, record: dict[str, Any]) -> None:
    """Write one capture record, creating the directories it needs."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _seat_of(draft: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    """Return the exact seat this lifecycle signal says work ran on.

    A payload that names one wins, because a session can be running on
    something other than what the draft already tracks; the seat this draft
    is currently tracking is the fallback. Nothing is supplied at
    installation any more (#223 decision 7): the Seat comes from the
    Harness's own record of the finished session, read once at that
    session's end (`_measured_seats`), or from an explicit null where
    neither a payload nor that record ever named one.
    """

    seat = payload.get("seat")
    if isinstance(seat, dict) and seat.get("model"):
        return {key: seat.get(key) for key in SEAT_ALLOWED}
    held = draft.get("seat")
    if isinstance(held, dict) and held.get("model"):
        return held
    return {}


def _touch_seat(
    seats: dict[str, dict[str, Any]],
    seat: dict[str, Any],
    measurements: Any,
    now: str,
) -> dict[str, dict[str, Any]]:
    """Return *seats* with one Seat's own active window opened or extended.

    A Usage Record's instants are its own Seat's first and last turn rather
    than the whole session's, because a session that changed Seat mid-way ran
    two configurations and each is timed on what it actually did (ADR-0156
    decision 3). Usage attribution between two Seats active in one session is
    issue #225's to settle; here, the usage last observed while a Seat was
    current is what that Seat's own record carries.
    """

    key = _opaque(json.dumps(seat, sort_keys=True))
    existing = seats.get(key) or {}
    return {
        **seats,
        key: {
            "seat": seat,
            "started_at": existing.get("started_at") or now,
            "completed_at": now,
            "measurements": (
                measurements
                if isinstance(measurements, dict)
                else existing.get("measurements") or {}
            ),
        },
    }


def _elapsed_seconds(started: Any, completed: Any) -> float | None:
    """Return the seconds between two instants, or None where either is unusable."""

    first, last = _parsed(started), _parsed(completed)
    return None if first is None or last is None else (last - first).total_seconds()


def _usage_key(session_identity: str, seat: dict[str, Any]) -> str:
    """Return the stable idempotency key of one session's Usage Record on one Seat.

    Idempotency is by session identity and Seat: the same finished session
    appended twice is skipped under this key, not repeated (ADR-0156 decision 2).
    """

    canonical = json.dumps(
        {"session_identity": session_identity, "seat": seat}, sort_keys=True
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _usage_record(draft: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    """Return one Usage Record: what one finished session cost on one Seat.

    It carries no outcome, no checker, and no Cohort — a Usage Record is never
    quality — only the identities, the Seat, the usage the environment
    exposed, and the two instants between which that Seat actually ran.
    """

    seat = {key: (entry.get("seat") or {}).get(key) for key in SEAT_ALLOWED}
    measurements = entry.get("measurements") or {}
    started = entry.get("started_at")
    completed = entry.get("completed_at")
    return {
        "usage_key": _usage_key(draft["session_identity"], seat),
        "session_identity": draft["session_identity"],
        "harness": {
            "name": draft.get("harness"),
            "inventory_revision": draft.get("harness_inventory_revision"),
        },
        "seat": seat,
        "usage": {key: measurements.get(key) for key in MEASUREMENT_ALLOWED},
        "started_at": started,
        "completed_at": completed,
        "elapsed_seconds": _elapsed_seconds(started, completed),
    }


def _usage_ledger(directory: Path) -> dict[str, dict[str, Any]]:
    """Return every Usage Record the store already holds, keyed by usage key."""

    path = directory / USAGE_LEDGER_FILE
    if not path.exists():
        return {}
    held: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            held[str(record["usage_key"])] = record
    return held


def _append(directory: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Append every unseen Usage Record to the store beside the evidence ledger.

    A record whose usage key the store already holds is skipped rather than
    repeated: the same finished session appended twice adds nothing the
    second time.
    """

    held = _usage_ledger(directory)
    accepted = [record for record in records if record["usage_key"] not in held]
    skipped = [record["usage_key"] for record in records if record["usage_key"] in held]
    if accepted:
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / USAGE_LEDGER_FILE).open("a", encoding="utf-8") as ledger:
            for record in accepted:
                ledger.write(json.dumps(record, sort_keys=True) + "\n")
    return {
        "recorded": [record["usage_key"] for record in accepted],
        "skipped": skipped,
    }


def _measured_seats(
    harness: str | None, transcript_path: Any, configured: dict[str, Any]
) -> list[dict[str, Any]] | None:
    """Return this session's own Seats and usage as its finished record states them.

    The Seat and the usage are read from the Harness's own record of the
    finished session where one can be read at all: the exact model, the
    deliberation control in force, and the token categories the Harness
    counted — nothing else is taken from it (#225 decision 1). The record
    supplies neither channel, surface, adapter, nor serving mode for any
    Seat, so the main Seat keeps those from *configured* — the seat this
    session's own lifecycle signals already established — while a delegated
    Seat the record cannot describe carries an explicit null on each of them
    rather than borrowing the main Seat's answer.

    Returns None where nothing could be read at all, so the caller falls back
    to whatever the lifecycle signals themselves already established — a
    missing, truncated, or unparseable record is an absence, never a raised
    error (ADR-0156 decision 4, applied to this read by ADR-0158).
    """

    if not harness or not isinstance(transcript_path, str) or not transcript_path:
        return None
    try:
        groups = _session_records().usage(harness, transcript_path)
    except Exception:  # noqa: BLE001 - a broken record is an absence, not a failure
        return None
    if not groups:
        return None

    entries = []
    for group in groups:
        seat = (
            {key: configured.get(key) for key in SEAT_ALLOWED}
            if group.get("role") == "main"
            else dict.fromkeys(SEAT_ALLOWED)
        )
        seat["model"] = group.get("model")
        seat["native_deliberation"] = group.get("native_deliberation")
        entries.append(
            {
                "seat": seat,
                "started_at": group.get("started_at"),
                "completed_at": group.get("completed_at"),
                "measurements": {"tokens": group.get("tokens")},
            }
        )
    return entries


def _finish(
    data: Path, draft: dict[str, Any], harness: str | None, transcript_path: Any
) -> dict[str, Any]:
    """Answer one session-ending signal: append its Usage Records and forget the draft.

    A session that ran on more than one Seat produces one Usage Record per
    Seat, read from the Harness's own finished record where one can be read
    (`_measured_seats`) and from what the lifecycle signals themselves
    already established otherwise. A session that ended abruptly — an error
    included, there being no outcome left for an error to carry — contributes
    whatever its own record establishes and nothing more; nothing here waits
    for a human.
    """

    measured = _measured_seats(harness, transcript_path, draft.get("seat") or {})
    entries = (
        measured if measured is not None else list(draft.get("seats", {}).values())
    )
    records = [_usage_record(draft, entry) for entry in entries]
    appended = _append(data, records)
    _draft_path(data, draft["session_key"]).unlink(missing_ok=True)

    # The session is over, so the one invocation with nothing left to delay
    # carries this Skill's own unattended source refresh (ADR-0167). It is a
    # sibling action on the same seam rather than part of capture's own
    # measurement path: it writes source states and nothing capture owns, and
    # its every failure is swallowed here exactly as this path's own are.
    with suppress(Exception):
        _refresh().refresh(data)

    return {"ok": True, "fail_open": False, **appended}


def hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal, and never let answering it cost the session.

    This is the synchronous path a Harness runs, so it does bounded local
    metadata I/O and nothing else: no model call, no test run, no repository
    scan, and no long-lived work. Every failure in it is swallowed, because a
    capture that breaks a session is worse than no capture. The one thing a
    session's own last invocation additionally carries is this Skill's
    unattended source refresh, which reaches the network only as bounded
    conditional metadata retrieval under a stated budget, in a module of its
    own (ADR-0167).
    """

    try:
        return _hook(data, event, payload)
    except Exception as exc:  # noqa: BLE001 - the hook path is fail-open by contract
        return {
            "ok": False,
            "fail_open": True,
            "detail": type(exc).__name__,
            "recorded": [],
            "skipped": [],
        }


def _moment(event: str, payload: Any) -> str:
    """Return the lifecycle moment this signal is, from wherever it was named.

    A Harness that interpolates the event into the command it runs says it
    there; Claude Code and Codex instead hand the whole event over on stdin, so
    an installed hook that took only the command line would answer every moment
    as if it were none of them.
    """

    if event:
        return event
    if not isinstance(payload, dict):
        return ""
    for field in EVENT_FIELDS:
        named = payload.get(field)
        if isinstance(named, str) and named:
            return named
    return ""


def _idle() -> dict[str, Any]:
    """Return the answer for a signal that neither opens nor closes a session."""

    return {"ok": True, "fail_open": False, "recorded": [], "skipped": []}


def _hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal.

    There is no separate on/off state of this feature's own to check any
    more (#223): a hook only ever runs because a Harness's own configuration
    names it, which only happens once this Skill's integration has been
    installed, so answering the signal is the whole of the work.
    """

    event = _moment(event, payload)
    clean = _clean(_normalized(payload))
    session = clean.get("session_id")
    if not session:
        return _idle()

    now = _now()
    held = _draft(data, session) or {
        "schema_version": SCHEMA_VERSION,
        "session_key": session,
        "session_identity": _opaque(session),
        "harness": clean.get("harness"),
        "harness_inventory_revision": clean.get("harness_inventory_revision"),
        "seat": {},
        "seats": {},
    }
    seat = _seat_of(held, clean)
    draft = {
        **held,
        "session_key": session,
        "updated_at": now,
        "seat": seat,
        "seats": _touch_seat(
            held.get("seats") or {}, seat, clean.get("measurements"), now
        ),
    }

    if event in END_EVENTS or event in ERROR_EVENTS:
        return _finish(
            data,
            draft,
            clean.get("harness") or draft.get("harness"),
            clean.get("transcript_path"),
        )

    # A start or a turn is a draft update and nothing more.
    _store(_draft_path(data, session), draft)
    return _idle()


def _storage(data: Path) -> int:
    """Return how many bytes the capture store is using right now."""

    if not home(data).exists():
        return 0
    return sum(path.stat().st_size for path in home(data).rglob("*") if path.is_file())


def status(data: Path, root: Path) -> dict[str, Any]:
    """Report capture's own state, without a network request or an evaluation.

    Every Harness the Collection Library has an adapter for is reported,
    whether or not this machine happens to hold our entry there right now —
    there is no separate configuration of this feature's own left to consult
    (#223): the Harness's own file is read fresh, exactly as `install` and
    `remove` already read it (ADR-0090). Each one's health is reported beside
    whether its finished session record can supply measurements at all
    (#225): a store of Usage Records that stays empty because a Harness
    keeps no readable record is something to say plainly here, never
    something left for the user to discover from the store itself.
    """

    integrations = _integrations()
    reader = _session_records()
    return {
        "harnesses": [
            {
                **integrations.health(owner(), harness, root),
                "measurements": harness in reader.SUPPORTED,
            }
            for harness in integrations.SUPPORTED
        ],
        "storage_bytes": _storage(data),
    }


def _row_count(path: Path) -> int:
    """Return how many non-blank JSONL lines one file holds."""

    return sum(
        1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    )


def purge_paths(data: Path) -> list[dict[str, Any]]:
    """Return what this feature owns beyond the ledger, present or not.

    This is the preview `config reset --evidence` renders before it removes
    the whole `capture/` subdirectory — drafts and all — and the Usage Record
    store beside it, keeping the Harness hooks installed (issue #227).
    `capture/` is a directory rather than a JSONL file, so it is sized in
    bytes; the Usage Record store is JSONL, sized in rows.
    """

    directory = home(data)
    ledger = data / USAGE_LEDGER_FILE
    entries: list[dict[str, Any]] = []
    if directory.exists():
        entries.append(
            {
                "path": str(directory),
                "present": True,
                "unit": "bytes",
                "count": _storage(data),
            }
        )
    else:
        entries.append({"path": str(directory), "present": False})
    if ledger.exists():
        entries.append(
            {
                "path": str(ledger),
                "present": True,
                "unit": "rows",
                "count": _row_count(ledger),
            }
        )
    else:
        entries.append({"path": str(ledger), "present": False})
    return entries


def purge(data: Path) -> list[dict[str, Any]]:
    """Remove everything this feature owns beyond the ledger, and report it.

    The Harness hooks stay installed, since this verb never touches them and
    there is no on/off flag of this feature's own for a purge to clear any
    more (#223): a session that starts after a purge is captured exactly as
    one before it was, into a `capture/` this verb's own removal recreates.
    """

    report = purge_paths(data)
    shutil.rmtree(home(data), ignore_errors=True)
    (data / USAGE_LEDGER_FILE).unlink(missing_ok=True)
    return report


def _hook_command(supplied: list[str], data: Path) -> list[str]:
    """Return the command a Harness runs for a lifecycle event.

    The data directory travels inside it. A hook installed for one directory
    and run against another writes its drafts and records where nobody looks
    for them.
    """

    command = list(supplied) or ["uv", "run", str(Path(__file__).resolve()), "hook"]
    if data.resolve() != default_data().resolve() and "--data" not in command:
        command += ["--data", str(data)]
    return command


def default_data() -> Path:
    """Return the data directory this Skill keeps its evidence in by default."""

    return Path.home() / ".kntnt" / "model-selector"


def install_integrations(harnesses: list[str]) -> dict[str, Any]:
    """Install this feature's owned integration, resolving its own data and root.

    This is the mirror of `remove_integrations`, the other word the Manager
    says at the seams that place or refresh an Enabled Skill's files (#223):
    it resolves this Skill's own default data directory and Harness root
    itself, because the Manager asking for it must not have to know where
    this Skill keeps its evidence (ADR-0090), exactly as removal already
    does for the opposite word.
    """

    return install(default_data(), Path.home(), harnesses, [])


def remove_integrations() -> dict[str, Any]:
    """Remove every integration this feature owns, wherever it installed one.

    This is the word the Manager says when the Skill is being made Disabled,
    withdrawn, or uninstalled: it runs while these files still exist, takes the
    hooks out of every Harness, and leaves the accepted Usage Records alone. It
    is answerable at any time, because removing what is already gone is a state
    rather than an error.
    """

    data = default_data()
    result = disable(data, Path.home())
    return {"removed": result["harnesses"], "usage_records_preserved": True}


def _emit(payload: dict[str, Any]) -> None:
    """Print one machine-readable answer."""

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse one capture invocation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=(
            "install-integrations",
            "remove-integrations",
            "hook",
            "status",
            "purge",
        ),
    )

    # Every action but the Manager's own two — install and remove — is
    # invoked by this Skill, which resolves the data directory itself; the
    # Manager's two are invoked by something that must not have to know
    # where this Skill keeps its evidence.
    parser.add_argument("--data", default=str(default_data()))
    parser.add_argument("--root", default=str(Path.home()))
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--event", default="")
    parser.add_argument("--owner", default=owner())

    # `--yes` gates only `purge`'s write, exactly as `config reset --evidence`
    # needs it: a preview without it is a success, never a refusal.
    parser.add_argument("--yes", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one capture action."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = Path(args.data)
    root = Path(args.root)

    # The hook is the only action a Harness runs, and it is fail-open whatever
    # reaches it — including a payload that is not JSON at all.
    if args.action == "hook":
        try:
            payload = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            payload = {}
        named = args.harness[0] if args.harness else None
        if named and isinstance(payload, dict) and not payload.get("harness"):
            payload["harness"] = named
        _emit(hook(data, args.event, payload))
        return 0

    if args.action == "remove-integrations":
        _emit(remove_integrations())
    elif args.action == "install-integrations":
        _emit(install_integrations(args.harness))
    elif args.action == "purge":
        _emit(
            {
                "schema_version": SCHEMA_VERSION,
                "verb": "purge",
                "confirmed": args.yes,
                "data": str(data),
                "paths": purge(data) if args.yes else purge_paths(data),
            }
        )
    else:
        _emit(status(data, root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
