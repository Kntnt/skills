# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Capture local run evidence automatically during ordinary Harness work.

`record` can import a prepared observation, and `observe` can prepare one for
work a caller deliberately routed. Neither covers the ordinary case: a user
works in their Harness all day and the evidence that should eventually replace
public benchmark priors is never written down, because writing it down is a
thing they have to remember to do.

This is that capture, and it is an explicit opt-in of an Enabled Skill rather
than a consequence of enabling one, because it installs persistent Harness
integration and handles local metadata. What it writes is the minimum an
observation needs: identities are opaque, measurements the environment did not
expose stay `null`, and no prompt, response, reasoning, diff, terminal output,
or transcript is ever copied. What it produces is the same normalized
`RunObservation` the routed contract produces (issue #96) — one representation,
extended with the stratum ordinary work belongs to, never a second one.

Nothing here grades a run. An outcome needs an objective checker, a declared
failure signal, or the user's own confirmation; a session that offers none waits
in a bounded pending-review store until a human answers it or retention takes
it. Model self-confidence is refused rather than believed, and an infrastructure
error keeps its own outcome so that it can never lower a configuration's
measured quality.
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

# The stratum ordinary interactive work belongs to. The routed strata name work
# a caller deliberately launched; this names the work nobody routed at all.
INTERACTIVE_STRATUM = "interactive_session"

# The maintainer's retention decision: pending and failed drafts live at most
# thirty days, and never more than a hundred of them or a mebibyte in total.
RETENTION_DAYS = 30
RETENTION_DRAFTS = 100
RETENTION_BYTES = 1024 * 1024

# A draft nobody has touched for this long belongs to a session that ended
# without ever saying so, which is the abrupt-termination case reconciliation
# exists for.
ABANDONED_AFTER_SECONDS = 6 * 60 * 60

REVIEW_ACTIONS: tuple[str, ...] = ("save", "failed", "ignore")

# Every lifecycle signal this feature understands, per Harness family. A stop is
# an observation that a turn ended and never that its work succeeded.
START_EVENTS = frozenset({"SessionStart", "session.created"})
TURN_EVENTS = frozenset({"Stop", "SubagentStop", "session.idle"})
ERROR_EVENTS = frozenset({"session.error"})
END_EVENTS = frozenset({"SessionEnd", "session.deleted"})

# Where a Harness names the lifecycle moment inside the payload rather than on
# the command line. Claude Code and Codex both do, so a hook installed without a
# per-event command still knows which moment it is answering.
EVENT_FIELDS: tuple[str, ...] = ("hook_event_name", "event", "type")

# The measurements a draft may carry, so that an object named `measurements` in
# a Harness payload cannot smuggle material in under a wanted key.
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

# The only fields a lifecycle payload may contribute. Everything else a Harness
# sends — and Harnesses send whole transcripts — is dropped before anything is
# written, so nothing forbidden can arrive by sitting beside what is wanted.
PAYLOAD_ALLOWED = frozenset(
    {
        "session_id",
        "harness",
        "harness_inventory_revision",
        "seat",
        "benchmark",
        "checker",
        "error",
        "measurements",
        "task",
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

# The conditions a non-model outcome may carry, and which of them are
# infrastructure rather than an abstention.
INFRA_CONDITIONS = frozenset({"mechanical_hinder", "tracker_failure"})
ABSTAIN_CONDITIONS = frozenset({"open_decision", "discovered_dependency"})


def _observations() -> Any:
    """Load the observation contract this Skill already ships.

    Capture reuses that contract rather than restating it: the same
    normalization, the same validation, and the same ledger rules answer for
    automatically captured work as for work a caller routed.
    """

    path = Path(__file__).resolve().parent / "observations.py"
    spec = importlib.util.spec_from_file_location("model_selector_observations", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("the observation contract could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _now() -> str:
    """Return this instant, as the contract writes instants."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _parsed(instant: Any) -> datetime | None:
    """Return one recorded instant as a datetime, or None where it is unusable."""

    if not isinstance(instant, str):
        return None
    try:
        return datetime.fromisoformat(instant)
    except ValueError:
        return None


def _age(instant: Any) -> float | None:
    """Return how many seconds ago *instant* was, or None where it is unusable."""

    parsed = _parsed(instant)
    if parsed is None:
        return None
    return (datetime.now(UTC) - parsed).total_seconds()


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


def _pending(data: Path) -> Path:
    """Return where captures awaiting a human are kept."""

    return home(data) / "pending"


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


def retention(data: Path) -> dict[str, int]:
    """Return the retention bounds pending and failed captures are held under."""

    stored = config(data).get("retention")
    if isinstance(stored, dict) and {"days", "drafts", "bytes"} <= set(stored):
        return {key: int(stored[key]) for key in ("days", "drafts", "bytes")}
    return {
        "days": RETENTION_DAYS,
        "drafts": RETENTION_DRAFTS,
        "bytes": RETENTION_BYTES,
    }


def review_actions() -> tuple[str, ...]:
    """Return the choices a deferred review offers."""

    return REVIEW_ACTIONS


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
        "Only observation metadata: opaque session and task identities, "
        "timestamps, the exact resolved configuration, checker identity and "
        "result, and available usage, cost, quota and latency values. Never "
        "prompts, responses, reasoning, source, diffs, terminal output, "
        "secrets or transcripts."
    ),
    "cleanup": (
        f"An imported capture is deleted immediately. Pending and failed "
        f"captures are kept at most {RETENTION_DAYS} days, {RETENTION_DRAFTS} "
        f"drafts and {RETENTION_BYTES} bytes, oldest removed first."
    ),
    "opt_out": (
        "Run `capture disable`, or make model-selector Disabled: either removes "
        "every hook this feature owns and keeps the evidence already accepted."
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
    captured work has no configuration to be evidence about.
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
    _pending(data).mkdir(exist_ok=True)
    _config_path(data).write_text(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "enabled": True,
                "consented_at": _now(),
                "seat": {key: (seat or {}).get(key) for key in SEAT_ALLOWED},
                "harnesses": named,
                "retention": {
                    "days": RETENTION_DAYS,
                    "drafts": RETENTION_DRAFTS,
                    "bytes": RETENTION_BYTES,
                },
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
        "retention": retention(data),
    }


def disable(data: Path, root: Path) -> dict[str, Any]:
    """Stop capture and remove every integration this feature owns.

    Accepted evidence is untouched. Turning a measurement off is not a reason to
    forget what it already measured, and a purge is a separate act the user has
    to ask for by name.
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
    session's evidence under a configuration it never ran on.
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
    """Return the exact seat this session ran on, as far as it is known.

    A payload that names one wins, because a session can be running on something
    other than what was configured; what the opt-in recorded is the fallback,
    and an empty seat is the honest answer where neither said.
    """

    seat = payload.get("seat")
    if isinstance(seat, dict) and seat.get("model"):
        return {key: seat.get(key) for key in SEAT_ALLOWED}
    held = draft.get("seat")
    if isinstance(held, dict) and held.get("model"):
        return held
    return configured if isinstance(configured, dict) else {}


def _outcome(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    """Return the outcome an external judgement established, or why there is none.

    Nothing in the session may establish its own outcome. A checker names itself
    and is independent, a declared failure signal comes from the Harness, and a
    human's confirmation comes from a review. Everything else waits.
    """

    error = payload.get("error")
    if isinstance(error, dict):
        condition = error.get("kind")
        if condition in INFRA_CONDITIONS:
            return {"result": "infra_error", "condition": condition}, None
        if condition in ABSTAIN_CONDITIONS:
            return {"result": "abstain", "condition": condition}, None
        return {"result": "infra_error", "condition": "mechanical_hinder"}, None

    checker = payload.get("checker")
    if not isinstance(checker, dict):
        return None, None
    if checker.get("authority") == "self_report" or not checker.get("independent"):
        return None, "self_reported_outcome"
    result = checker.get("result")
    if result not in ("pass", "fail"):
        return None, "unchecked_outcome"
    return {
        "result": result,
        "authority": checker.get("authority") or "objective_checker",
        "checker": {
            "identity": checker.get("identity"),
            "independent": True,
        },
    }, None


def _attempt(draft: dict[str, Any], outcome: dict[str, Any]) -> dict[str, Any]:
    """Return the routed-contract attempt one completed session amounts to.

    Ordinary work runs on the session's own main seat rather than on a point
    anybody routed to, which is exactly what an inherited decision is. Recording
    it that way keeps one normalized representation instead of inventing a
    second one for work that was never routed.
    """

    measurements = draft.get("measurements")
    attempt: dict[str, Any] = {
        "attempt_id": draft["session_identity"],
        "session_identity": draft["session_identity"],
        "task_identity": draft["task_identity"],
        "workload_stratum": INTERACTIVE_STRATUM,
        "attempt_index": 1,
        "harness": {
            "name": draft.get("harness"),
            "inventory_revision": draft.get("harness_inventory_revision"),
        },
        "benchmark": {"key": draft.get("benchmark") or INTERACTIVE_STRATUM},
        "decision": _decision(draft),
        "outcome": _outcome_block(outcome),
        "started_at": draft.get("started_at"),
        "completed_at": draft.get("completed_at") or _now(),
    }
    if isinstance(measurements, dict):
        attempt["measurements"] = measurements
    return attempt


def _decision(draft: dict[str, Any]) -> dict[str, Any]:
    """Return the decision an ordinary session amounts to.

    Nothing was routed, so the status is the inheritance that actually happened:
    the work ran on the session's own main seat, and the contract fingerprints
    it from that seat. Provenance names the captured environment rather than a
    frozen routing snapshot, because there was no routing to freeze — the
    identity is stable for one seat in one Harness, so the same environment
    observed twice is the same provenance.
    """

    seat = draft.get("seat") or {}
    return {
        "status": "inherit",
        "inheritance": {"main_seat": seat},
        "evidence_class": "captured_local_run",
        "audit": {
            "snapshot_identity": "capture:"
            + _opaque(
                json.dumps(
                    {"seat": seat, "harness": draft.get("harness")}, sort_keys=True
                )
            ),
            "provenance": {
                "main_seat_model": seat.get("model"),
                "profile_revision": draft.get("profile_revision"),
                "evidence_identity": draft.get("evidence_identity"),
                "evidence_vintage": draft.get("evidence_vintage"),
            },
        },
    }


def _outcome_block(outcome: dict[str, Any]) -> dict[str, Any]:
    """Return one established outcome in the shape the contract reads."""

    if outcome["result"] in ("infra_error", "abstain"):
        return {
            "result": outcome["result"],
            "authority": "harness",
            "condition": outcome["condition"],
        }
    return {
        "result": outcome["result"],
        "authority": outcome["authority"],
        "checker": outcome["checker"],
    }


def _import(data: Path, attempt: dict[str, Any]) -> dict[str, Any]:
    """Normalize one attempt through the contract and import what it yields."""

    observations = _observations()
    emitted = observations.observe(
        {"schema_version": observations.SCHEMA_VERSION, "attempts": [attempt]}
    )
    if not emitted.get("observations"):
        return {"imported": None, "refusals": emitted.get("refusals", [])}
    imported = observations.record(
        {
            "schema_version": observations.SCHEMA_VERSION,
            "observations": emitted["observations"],
        },
        data,
    )
    return {"imported": imported, "refusals": emitted.get("refusals", [])}


def _review_notice(data: Path, identity: str) -> dict[str, Any] | None:
    """Return the user-facing notice that one capture is waiting on them.

    Work nobody judged is the one case where capture needs a person, so the
    person is told — with the identity to answer and the three answers there
    are. Debounced like every other notice, and out of the model's context for
    the same reason.
    """

    return _notice(
        data,
        "review",
        f"A captured session is waiting for your judgement: {identity}. "
        f"Answer it with /model-selector capture --review={identity} "
        f"--action=save|failed|ignore.",
    )


def _notification(data: Path, accepted: list[str]) -> dict[str, Any] | None:
    """Return the user-facing notice for an accepted import, debounced.

    A notice is for the person, never for the model: repeating it every session
    would be noise, and putting it anywhere an agent reads would change the very
    configuration being measured.
    """

    if not accepted:
        return None
    return _notice(
        data, "accepted", f"{len(accepted)} local run observation(s) accepted."
    )


def _notice(data: Path, kind: str, text: str) -> dict[str, Any] | None:
    """Return one debounced user-facing notice, or None where it is too soon."""

    marker = home(data) / f"notified-{kind}.json"
    try:
        last = json.loads(marker.read_text(encoding="utf-8")).get("at")
    except (OSError, ValueError):
        last = None
    age = _age(last)
    if age is not None and age < 60 * 60:
        return None
    _store(marker, {"at": _now()})
    return {"channel": "user", "text": text}


def _complete(
    data: Path, draft: dict[str, Any], payload: dict[str, Any]
) -> dict[str, Any]:
    """Answer one completion boundary: import it, or leave it for a human."""

    outcome, refusal = _outcome(payload)
    draft = {
        **draft,
        "completed_at": _now(),
        "updated_at": _now(),
        "benchmark": payload.get("benchmark") or draft.get("benchmark"),
        "seat": _seat_of(draft, payload, _configured_seat(data)),
    }
    _draft_path(data, draft["session_key"]).unlink(missing_ok=True)

    # An outcome nobody established is not this feature's to invent.
    if outcome is None:
        pending = _pending(data) / f"{draft['session_identity']}.json"
        _store(pending, {**draft, "refusal": refusal})
        return {
            "ok": True,
            "fail_open": False,
            "pending": draft["session_identity"],
            "imported": None,
            "refusals": [{"code": refusal}] if refusal else [],
            "notification": _review_notice(data, draft["session_identity"]),
        }

    result = _import(data, _attempt(draft, outcome))
    imported = result["imported"]

    # Nothing importable is not nothing that happened: the work waits for a
    # human with the reason attached, rather than being discarded quietly.
    if imported is None:
        _store(
            _pending(data) / f"{draft['session_identity']}.json",
            {**draft, "refusals": result["refusals"]},
        )
        return {
            "ok": True,
            "fail_open": False,
            "pending": draft["session_identity"],
            "imported": None,
            "refusals": result["refusals"],
            "notification": _review_notice(data, draft["session_identity"]),
        }

    accepted = list(imported["accepted"])
    return {
        "ok": True,
        "fail_open": False,
        "pending": None,
        "imported": imported,
        "refusals": result["refusals"],
        "notification": _notification(data, accepted),
    }


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
            "pending": None,
            "imported": None,
            "refusals": [],
            "notification": None,
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
    """Return the answer for a signal capture is not listening for."""

    return {
        "ok": True,
        "fail_open": False,
        "pending": None,
        "imported": None,
        "refusals": [],
        "notification": None,
    }


def _hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal under an opted-in configuration."""

    event = _moment(event, payload)
    if not config(data).get("enabled"):
        return _idle()

    clean = _clean(payload)
    session = clean.get("session_id")
    if not session:
        return _idle()

    held = _draft(data, session) or {
        "schema_version": SCHEMA_VERSION,
        "session_key": session,
        "session_identity": _opaque(session),
        "task_identity": _opaque(clean.get("task") or session),
        "harness": clean.get("harness") or _configured_harness(data),
        "harness_inventory_revision": clean.get("harness_inventory_revision"),
        "started_at": _now(),
        "seat": {},
    }
    draft = {
        **held,
        "session_key": session,
        "updated_at": _now(),
        "seat": _seat_of(held, clean, _configured_seat(data)),
        "benchmark": clean.get("benchmark") or held.get("benchmark"),
    }
    if isinstance(clean.get("measurements"), dict):
        draft["measurements"] = clean["measurements"]

    if event in END_EVENTS or (event in TURN_EVENTS and _judged(clean)):
        return _complete(data, draft, clean)
    if event in ERROR_EVENTS:
        return _complete(data, draft, {**clean, "error": clean.get("error") or {}})

    # A start or an unjudged turn is a draft update and nothing more.
    _store(_draft_path(data, session), draft)
    return _idle()


def _judged(payload: dict[str, Any]) -> bool:
    """Return whether this signal carries an external judgement of the work."""

    return isinstance(payload.get("checker"), dict) or isinstance(
        payload.get("error"), dict
    )


def review(data: Path, identity: str, action: str) -> dict[str, Any]:
    """Settle one pending capture the way a human answered it."""

    if action not in REVIEW_ACTIONS:
        raise ValueError(f"action must be one of {', '.join(REVIEW_ACTIONS)}")
    path = _pending(data) / f"{identity}.json"
    if not path.exists():
        return {"imported": None, "reviewed": None}

    draft = json.loads(path.read_text(encoding="utf-8"))
    path.unlink()
    if action == "ignore":
        return {"imported": None, "reviewed": "ignore"}

    outcome = {
        "result": "pass" if action == "save" else "fail",
        "authority": "user_confirmation",
        "checker": {"identity": "user", "independent": True},
    }
    result = _import(data, _attempt(draft, outcome))
    return {**result, "reviewed": action}


def _records(directory: Path) -> list[Path]:
    """Return every stored capture in *directory*, oldest first."""

    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"), key=lambda path: path.stat().st_mtime)


def reconcile(data: Path) -> dict[str, Any]:
    """Reconcile abandoned drafts and apply the retention bounds.

    Deterministic and daemon-free: it runs at a start or a status pass, decides
    from what is on disk, and removes the oldest first wherever a bound is
    exceeded.
    """

    bounds = retention(data)
    reconciled = 0
    for path in _records(_drafts(data)):
        try:
            draft = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            path.unlink(missing_ok=True)
            continue
        age = _age(draft.get("updated_at"))
        if age is None or age < ABANDONED_AFTER_SECONDS:
            continue

        # A session that ended without saying so is unjudged work, not a
        # success and not a failure: it goes to review like any other.
        path.unlink(missing_ok=True)
        _store(_pending(data) / f"{draft['session_identity']}.json", draft)
        reconciled += 1

    expired = 0
    for path in _records(_pending(data)):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            path.unlink(missing_ok=True)
            expired += 1
            continue
        age = _age(record.get("updated_at"))
        if age is not None and age > bounds["days"] * 86400:
            path.unlink(missing_ok=True)
            expired += 1

    # Hard bounds are applied oldest first, so a bound is a deterministic
    # eviction rather than a refusal of the work happening now.
    held = _records(_pending(data))
    while len(held) > bounds["drafts"]:
        held.pop(0).unlink(missing_ok=True)
        expired += 1
    while sum(path.stat().st_size for path in held) > bounds["bytes"] and held:
        held.pop(0).unlink(missing_ok=True)
        expired += 1

    return {"reconciled": reconciled, "expired": expired, "pending": len(held)}


def _storage(data: Path) -> int:
    """Return how many bytes the capture store is using right now."""

    if not home(data).exists():
        return 0
    return sum(path.stat().st_size for path in home(data).rglob("*") if path.is_file())


def status(data: Path, root: Path) -> dict[str, Any]:
    """Report capture's own state, without a network request or an evaluation."""

    integrations = _integrations()
    current = config(data)

    # A status pass is one of the two moments abandoned work is reconciled at,
    # so what it reports is the state after that sweep rather than before it.
    if current.get("enabled"):
        reconcile(data)

    pending = _records(_pending(data))
    ages = [
        _age(json.loads(path.read_text(encoding="utf-8")).get("updated_at"))
        for path in pending
    ]
    known = [age for age in ages if age is not None]
    return {
        "enabled": bool(current.get("enabled")),
        "harnesses": [
            integrations.health(owner(), harness, root)
            for harness in current.get("harnesses") or []
        ],
        "pending": len(pending),
        "pending_identities": [path.stem for path in pending],
        "oldest_pending_age_seconds": max(known) if known else None,
        "storage_bytes": _storage(data),
        "retention": retention(data),
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
    hooks out of every Harness, and leaves the accepted evidence alone. It is
    answerable at any time, because removing what is already gone is a state
    rather than an error.
    """

    data = default_data()
    result = disable(data, Path.home())
    return {"removed": result["harnesses"], "evidence_preserved": True}


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
            "enable",
            "disable",
            "hook",
            "status",
            "reconcile",
            "review",
            "remove-integrations",
        ),
    )

    # Every action but the Manager's teardown is invoked by this Skill, which
    # resolves the data directory itself; the teardown is invoked by something
    # that must not have to know where this Skill keeps its evidence.
    parser.add_argument("--data", default=str(default_data()))
    parser.add_argument("--root", default=str(Path.home()))
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--event", default="")
    parser.add_argument("--id", dest="identity", default="")
    parser.add_argument("--action", dest="review_action", default="")
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
    elif args.action == "status":
        _emit(status(data, root))
    elif args.action == "reconcile":
        _emit(reconcile(data))
    else:
        _emit(review(data, args.identity, args.review_action))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
