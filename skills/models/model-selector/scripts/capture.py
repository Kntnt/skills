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

This is an explicit opt-in of an Enabled Skill rather than a consequence of
enabling one, because it installs persistent Harness integration and handles
local session metadata. What it writes is the minimum a Usage Record needs:
identities are opaque, measurements the environment did not expose stay
`null`, and no prompt, response, reasoning, diff, terminal output, or
transcript is ever copied.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

# Every lifecycle signal this feature understands, per Harness family. A stop
# is one turn of an ongoing session and never a session's own end; a Seat's
# Usage Record is timed on its own first and last such turn. Codex CLI 0.153.0
# names its own moments in camelCase (`sessionStart`, `stop`, `sessionEnd`),
# confirmed from its installed binary's own `HookEventName`, never in Claude
# Code's PascalCase.
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
PAYLOAD_ALLOWED = frozenset(
    {
        "session_id",
        "harness",
        "harness_inventory_revision",
        "seat",
        "measurements",
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


def _config_path(data: Path) -> Path:
    """Return where the capture configuration is kept."""

    return home(data) / "capture.json"


def _drafts(data: Path) -> Path:
    """Return where per-session drafts are kept."""

    return home(data) / "drafts"


def config(data: Path) -> dict[str, Any]:
    """Return the capture configuration, or the off state where there is none."""

    off: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "enabled": False,
        "harnesses": [],
    }
    path = _config_path(data)
    if not path.exists():
        return off
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return off
    return loaded if isinstance(loaded, dict) else off


def _integrations() -> Any:
    """Load the Collection Library's owned-integration mechanics.

    Harness-specific installation is not this feature's knowledge to hold: it is
    the Library's, so that a second Skill needing the same thing finds it there
    rather than reaching into this one (ADR-0012).
    """

    here = Path(__file__).resolve().parent
    for candidate in (
        here.parent.parent.parent / "kntnt" / "library" / "scripts" / "integrations.py",
        here.parent / "library" / "scripts" / "integrations.py",
    ):
        if candidate.exists():
            spec = importlib.util.spec_from_file_location(
                "kntnt_integrations", candidate
            )
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError("the Collection Library's integration mechanics are missing")


def owner() -> str:
    """Return the stable ownership identity every installed integration carries."""

    return "kntnt.model-selector.capture"


CONSENT = {
    "integration": (
        "Local session lifecycle hooks are installed into each named Harness, "
        "owned by this feature and removed with it."
    ),
    "retained": (
        "Only Usage Record fields: the opaque session identity and usage key, "
        "the Harness and its inventory revision, the exact Seat the work ran "
        "on, the usage categories the environment exposed, and the two "
        "instants a session ran between. Never prompts, responses, reasoning, "
        "source, diffs, terminal output, secrets or transcripts."
    ),
    "cleanup": (
        "A finished session is appended to the Usage Record store immediately, "
        "one record per Seat it ran on. There is no waiting store, nothing is "
        "queued for review, and nothing expires."
    ),
    "opt_out": (
        "Run `capture disable`, or make model-selector Disabled: either removes "
        "every hook this feature owns and keeps the Usage Records already "
        "appended."
    ),
}


def enable(
    data: Path,
    root: Path,
    harnesses: list[str],
    command: list[str],
    seat: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Opt in to automatic capture and install the integration it needs.

    *seat* is the exact main seat this Harness is running on. No lifecycle
    payload carries it — a Harness reports what happened, not what it is — and a
    script may not guess it, so the agent that knows supplies it once here and
    every session captured afterwards is fingerprinted from it. Without it,
    captured work has no configuration to be measured about.
    """

    integrations = _integrations()

    # Naming no Harness means every Harness an adapter exists for, which is what
    # the consent the user just gave says it installs into.
    named = list(harnesses) or list(integrations.SUPPORTED)
    runs = _hook_command(command, data)
    installed = [
        integrations.install(owner(), harness, root, runs) for harness in named
    ]

    home(data).mkdir(parents=True, exist_ok=True)
    _drafts(data).mkdir(exist_ok=True)
    _config_path(data).write_text(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "enabled": True,
                "consented_at": _now(),
                "seat": {key: (seat or {}).get(key) for key in SEAT_ALLOWED},
                "harnesses": named,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "enabled": True,
        "consent": dict(CONSENT),
        "harnesses": installed,
    }


def disable(data: Path, root: Path) -> dict[str, Any]:
    """Stop capture and remove every integration this feature owns.

    Accepted Usage Records are untouched. Turning a measurement off is not a
    reason to forget what it already measured, and a purge is a separate act
    the user has to ask for by name.
    """

    integrations = _integrations()
    current = config(data)
    removed = [
        integrations.remove(owner(), harness, root)
        for harness in current.get("harnesses") or list(integrations.SUPPORTED)
    ]

    if _config_path(data).exists():
        _config_path(data).write_text(
            json.dumps({**current, "enabled": False}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return {"enabled": False, "harnesses": removed}


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


def _configured_harness(data: Path) -> str | None:
    """Return the Harness a payload that named none must have come from.

    The installer writes the Harness into the command it installs, so an
    ordinary hook always names one. Where a caller has not, one configured
    Harness answers it and several cannot: guessing between them would file a
    session's usage under a configuration it never ran on.
    """

    configured = config(data).get("harnesses")
    if isinstance(configured, list) and len(configured) == 1:
        named = configured[0]
        return named if isinstance(named, str) else None
    return None


def _configured_seat(data: Path) -> dict[str, Any]:
    """Return the seat recorded when capture was opted in to."""

    seat = config(data).get("seat")
    return seat if isinstance(seat, dict) else {}


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


def _seat_of(
    draft: dict[str, Any], payload: dict[str, Any], configured: dict[str, Any]
) -> dict[str, Any]:
    """Return the exact seat this lifecycle signal says work ran on.

    A payload that names one wins, because a session can be running on
    something other than what was configured; the seat this draft is
    currently tracking is the fallback, and the seat recorded at opt-in
    answers where neither said.
    """

    seat = payload.get("seat")
    if isinstance(seat, dict) and seat.get("model"):
        return {key: seat.get(key) for key in SEAT_ALLOWED}
    held = draft.get("seat")
    if isinstance(held, dict) and held.get("model"):
        return held
    return configured if isinstance(configured, dict) else {}


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


def _finish(data: Path, draft: dict[str, Any]) -> dict[str, Any]:
    """Answer one session-ending signal: append its Usage Records and forget the draft.

    A session that ran on more than one Seat produces one Usage Record per
    Seat. A session that ended abruptly — an error included, there being no
    outcome left for an error to carry — contributes whatever its own record
    establishes and nothing more; nothing here waits for a human.
    """

    records = [_usage_record(draft, entry) for entry in draft.get("seats", {}).values()]
    appended = _append(data, records)
    _draft_path(data, draft["session_key"]).unlink(missing_ok=True)
    return {"ok": True, "fail_open": False, **appended}


def hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal, and never let answering it cost the session.

    This is the synchronous path a Harness runs, so it does bounded local
    metadata I/O and nothing else: no network request, no model call, no test
    run, no repository scan, and no long-lived work. Every failure in it is
    swallowed, because a capture that breaks a session is worse than no capture.
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
    """Answer one lifecycle signal under an opted-in configuration."""

    event = _moment(event, payload)
    if not config(data).get("enabled"):
        return _idle()

    clean = _clean(_normalized(payload))
    session = clean.get("session_id")
    if not session:
        return _idle()

    now = _now()
    held = _draft(data, session) or {
        "schema_version": SCHEMA_VERSION,
        "session_key": session,
        "session_identity": _opaque(session),
        "harness": clean.get("harness") or _configured_harness(data),
        "harness_inventory_revision": clean.get("harness_inventory_revision"),
        "seat": {},
        "seats": {},
    }
    seat = _seat_of(held, clean, _configured_seat(data))
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
        return _finish(data, draft)

    # A start or a turn is a draft update and nothing more.
    _store(_draft_path(data, session), draft)
    return _idle()


def _storage(data: Path) -> int:
    """Return how many bytes the capture store is using right now."""

    if not home(data).exists():
        return 0
    return sum(path.stat().st_size for path in home(data).rglob("*") if path.is_file())


def status(data: Path, root: Path) -> dict[str, Any]:
    """Report capture's own state, without a network request or an evaluation."""

    integrations = _integrations()
    current = config(data)
    return {
        "enabled": bool(current.get("enabled")),
        "harnesses": [
            integrations.health(owner(), harness, root)
            for harness in current.get("harnesses") or []
        ],
        "storage_bytes": _storage(data),
    }


def _hook_command(supplied: list[str], data: Path) -> list[str]:
    """Return the command a Harness runs for a lifecycle event.

    The data directory travels inside it. A hook installed for one directory and
    run against another is a hook that reads an empty configuration and answers
    every session as though capture were off.
    """

    command = list(supplied) or ["uv", "run", str(Path(__file__).resolve()), "hook"]
    if data.resolve() != default_data().resolve() and "--data" not in command:
        command += ["--data", str(data)]
    return command


def default_data() -> Path:
    """Return the data directory this Skill keeps its evidence in by default."""

    return Path.home() / ".kntnt" / "model-selector"


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
        choices=("enable", "disable", "hook", "status", "remove-integrations"),
    )

    # Every action but the Manager's teardown is invoked by this Skill, which
    # resolves the data directory itself; the teardown is invoked by something
    # that must not have to know where this Skill keeps its evidence.
    parser.add_argument("--data", default=str(default_data()))
    parser.add_argument("--root", default=str(Path.home()))
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--event", default="")
    parser.add_argument("--owner", default=owner())
    parser.add_argument("--seat", default="")
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
    elif args.action == "enable":
        try:
            seat = json.loads(args.seat) if args.seat else {}
        except ValueError:
            seat = {}
        _emit(enable(data, root, args.harness, args.command, seat))
    elif args.action == "disable":
        _emit(disable(data, root))
    else:
        _emit(status(data, root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
