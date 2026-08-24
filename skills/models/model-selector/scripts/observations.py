# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Turn externally judged routed attempts into importable run observations.

The module is the emission half of the evidence ledger's import contract: a
caller that routed work through the public Model Routing Module hands back the
attempt it completed, and this module answers with the normalized, sanitized
`RunObservation` records `record` accepts. Emission copies an allow-list and
never the caller's material, so a prompt, a response, a ticket body, a diff, a
transcript, or a filesystem path cannot reach the artifact by being present in
the input. Nothing here writes evidence except `record`, which is the single
ledger mutation seam in this contract.
"""

import hashlib
import json
import math
import re
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, cast

SCHEMA_VERSION = 1

# The workload strata an attempt may be charged to. Orchestrate's five building
# roles are distinct strata because a mechanical wave fix and an initial build
# are different work, and an amend is a different attempt at the same work;
# delegation's execution subagent is the sixth. The seventh is the work nobody
# routed at all — an ordinary interactive session, which automatic capture
# observes on the main seat it ran on rather than on a point somebody chose.
STRATA: tuple[str, ...] = (
    "initial_build",
    "amend",
    "collision_repair",
    "rebuild",
    "mechanical_wave_fix",
    "delegated_execution",
    "interactive_session",
)

# What an attempt can have come to. The first two are judgements of the model's
# work; the last two are the environment's and the workflow's, and the ledger
# keeps them apart from quality for exactly that reason.
DECISIVE_RESULTS: tuple[str, ...] = ("pass", "fail")
CONDITIONAL_RESULTS: tuple[str, ...] = ("abstain", "infra_error")
RESULTS: tuple[str, ...] = DECISIVE_RESULTS + CONDITIONAL_RESULTS

# Who may establish a decisive outcome. Every one of them is external to the
# attempt being judged: an independent verifier, an objective checker, a frozen
# rubric, a declared failure signal, or the user saying so.
DECISIVE_AUTHORITIES: frozenset[str] = frozenset(
    {
        "independent_verifier",
        "objective_checker",
        "frozen_rubric",
        "declared_failure_signal",
        "user_confirmation",
    }
)

# Who may establish a non-model condition beside them: the Harness the attempt
# ran on and the tracker the work is accounted in.
CONDITION_AUTHORITIES: frozenset[str] = DECISIVE_AUTHORITIES | {"harness", "tracker"}

# The conditions that end an attempt without saying anything about the model.
CONDITIONS: tuple[str, ...] = (
    "mechanical_hinder",
    "open_decision",
    "discovered_dependency",
    "tracker_failure",
    "merge_collision",
)

# The usage categories an observation carries. Each is a number the environment
# exposed or an explicit null; a missing measurement is never a zero.
TOKEN_CATEGORIES: tuple[str, ...] = (
    "input",
    "output",
    "cache_read",
    "cache_write",
    "reasoning",
)
COST_FIELDS: tuple[str, ...] = ("cash", "provider_bill", "allocated_subscription_cost")
QUOTA_BASES: tuple[str, ...] = ("provider_charged_quota", "reconstructed_raw_usage")

# The dimensions a cheap-first policy is charged in. A policy is a configuration
# of its own, so its account carries the failed first attempt, the checker, and
# the retry rather than only the attempt that finally passed.
POLICY_DIMENSIONS: tuple[str, ...] = (
    "cash",
    "rolling_quota",
    "weekly_quota",
    "allocated_subscription_cost",
    "wall_seconds",
)

# What a score dimension may be called. A normalized identifier keeps free
# prose, verdict text, and reviewer commentary out of a numeric record.
SCORE_DIMENSION = re.compile(r"^[a-z][a-z0-9_]{0,31}$")

# What a sanitized artifact identity looks like: an algorithm and its digest,
# never a file name and never a path.
ARTIFACT_HASH = re.compile(r"^[a-z0-9]+:[0-9a-f]{16,128}$")

# What an emitted string may never be. An absolute path names the machine the
# work ran on, a newline is where a transcript starts, and a long value is
# material rather than an identity.
ABSOLUTE_PATH = re.compile(r"^(?:[/~]|[A-Za-z]:[\\/]|\\\\)")
MAX_EMITTED_LENGTH = 200

# Where the ledger keeps what this module writes, under the selected data
# directory. Both names are the evidence ledger's own.
LEDGER_FILE = "run-observations.jsonl"
FRONTIER_FILE = "derived-frontiers.json"

# The confidence a conservative success rate is reported at. Wilson's interval
# is used rather than the raw rate so one passing attempt cannot read as
# certainty.
WILSON_Z = 1.96


def _refusal(attempt_id: Any, code: str, detail: str) -> dict[str, Any]:
    """Return one stable per-attempt refusal that names no caller material."""

    return {
        "attempt_id": attempt_id if isinstance(attempt_id, str) else None,
        "code": code,
        "detail": detail,
    }


def _artifact_refusal(code: str, detail: str) -> dict[str, Any]:
    """Return one stable process-level refusal before any attempt is read."""

    return {
        "schema_version": SCHEMA_VERSION,
        "observations": [],
        "refusals": [],
        "artifact_refusal": {"code": code, "detail": detail},
    }


def _digest(value: Any) -> str:
    """Return the canonical digest of one JSON-representable value."""

    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _run_key(
    fingerprint: str, benchmark_key: str, task_id: str, seed: Any, attempt_index: int
) -> str:
    """Return the ledger's run key for one exact attempt at one exact task."""

    parts = [fingerprint, benchmark_key, task_id, "null" if seed is None else str(seed)]
    parts.append(str(attempt_index))
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _number(value: Any) -> float | int | None:
    """Return a finite measurement, or None where the environment exposed none.

    A measurement the environment did not expose is None here and stays None
    all the way into the artifact; it never becomes a zero, because a zero is a
    reading and an absence is not.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value if math.isfinite(value) else None


def _timestamp(value: Any) -> datetime | None:
    """Parse one ISO-8601 instant, or None where it is absent or unreadable."""

    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _measured(value: Any, derived: float | None) -> float | int | None:
    """Return the exposed measurement, else the one its own instants establish."""

    exposed = _number(value)
    return derived if exposed is None else exposed


def _elapsed(started: Any, completed: Any) -> float | None:
    """Return the seconds between two instants, or None where either is absent."""

    first, last = _timestamp(started), _timestamp(completed)
    return None if first is None or last is None else (last - first).total_seconds()


def _attempt_error(attempt: Any) -> str | None:
    """Return why one attempt cannot be read at all, or None where it can."""

    if not isinstance(attempt, dict):
        return "An attempt must be a JSON object."
    for field in ("attempt_id", "session_identity", "task_identity"):
        if not isinstance(attempt.get(field), str) or not attempt[field]:
            return f"{field} must be a non-empty string."
    if attempt.get("workload_stratum") not in STRATA:
        return f"workload_stratum must be one of {', '.join(STRATA)}."
    index = attempt.get("attempt_index")
    if isinstance(index, bool) or not isinstance(index, int) or index < 1:
        return "attempt_index must be a positive integer."
    benchmark = attempt.get("benchmark")
    if not isinstance(benchmark, dict) or not isinstance(benchmark.get("key"), str):
        return "benchmark.key must identify the workload."
    harness = attempt.get("harness")
    if not isinstance(harness, dict) or not isinstance(harness.get("name"), str):
        return "harness.name must identify the active Harness."
    if not isinstance(attempt.get("decision"), dict):
        return "decision must be the public route decision this attempt ran on."
    return None


def _outcome_refusal(attempt: dict[str, Any], outcome: Any) -> str | None:
    """Return why an outcome cannot establish this attempt, or None where it can.

    Only an external judgement decides. A builder's or a subagent's own report
    is not one, an unchecked subjective success is not one, and a workflow or
    Harness condition establishes an abstention or an infrastructure error
    rather than a model failure.
    """

    if not isinstance(outcome, dict):
        return "no_outcome"
    result, authority = outcome.get("result"), outcome.get("authority")
    condition, checker = outcome.get("condition"), outcome.get("checker")
    if result not in RESULTS:
        return "no_outcome"
    if authority == "self_report":
        return "self_reported_outcome"

    # Hold a decisive outcome to an external judgement of this exact attempt.
    if result in DECISIVE_RESULTS:
        if condition is not None:
            return "non_model_condition_outcome"
        if authority not in DECISIVE_AUTHORITIES:
            return "unchecked_outcome"
        if not isinstance(checker, dict) or not checker.get("identity"):
            return "unchecked_outcome"
        if checker.get("independent") is not True:
            return "self_reported_outcome"
        return None

    # Hold a non-decisive outcome to a named condition and a stated authority.
    if condition not in CONDITIONS:
        return "missing_non_model_condition"
    if authority not in CONDITION_AUTHORITIES:
        return "unchecked_outcome"
    return None


def _configuration(attempt: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    """Return the exact point this attempt ran on, or why there is none.

    A selected decision names the point exactly. An inheritance ran on the
    frozen main seat, which is equally exact and is fingerprinted here from the
    seat it names. A refusal launched nothing, so it stays audit data.
    """

    decision = attempt["decision"]
    status = decision.get("status")
    if status == "selected" and isinstance(decision.get("launch"), dict):
        launch = decision["launch"]
        return {
            "route_status": "selected",
            "configuration_fingerprint": launch.get("configuration_fingerprint"),
            "model": launch.get("model"),
            "resolved_alias": launch.get("resolved_alias"),
            "portable_deliberation": launch.get("portable_deliberation"),
            "native_deliberation": launch.get("native_deliberation"),
            "channel": launch.get("channel"),
            "surface": launch.get("surface"),
            "adapter_id": launch.get("adapter_id"),
            "serving_mode": launch.get("serving_mode"),
        }, None

    # Fingerprint the frozen main seat an inherited execution actually launched.
    if status == "inherit":
        seat = decision.get("inheritance", {}).get("main_seat")
        if not isinstance(seat, dict) or not seat.get("model"):
            return None, "unfingerprinted_inheritance"
        return {
            "route_status": "inherit",
            "configuration_fingerprint": _digest(
                {"inherited_main_seat": seat, "schema_version": SCHEMA_VERSION}
            ),
            "model": seat.get("model"),
            "resolved_alias": None,
            "portable_deliberation": seat.get("portable_deliberation"),
            "native_deliberation": seat.get("native_deliberation"),
            "channel": seat.get("channel"),
            "surface": seat.get("surface"),
            "adapter_id": seat.get("adapter_id"),
            "serving_mode": seat.get("serving_mode"),
        }, None

    return None, "unlaunched_decision"


def _scores(outcome: dict[str, Any]) -> tuple[dict[str, float] | None, str | None]:
    """Return the permitted score dimensions of one outcome, or why it is unusable."""

    scores = outcome.get("scores")
    if scores is None:
        return None, None
    if not isinstance(scores, dict):
        return None, "invalid_scores"
    permitted: dict[str, float] = {}
    for dimension, value in scores.items():
        measured = _number(value)
        if not isinstance(dimension, str) or not SCORE_DIMENSION.match(dimension):
            return None, "invalid_scores"
        if measured is None:
            return None, "invalid_scores"
        permitted[dimension] = measured
    return permitted, None


def _quota(measurements: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    """Return the quota facts of one attempt under exactly one accounting basis."""

    basis = measurements.get("quota_basis")
    charged = _number(measurements.get("charged_quota"))
    multiplier = _number(measurements.get("quota_multiplier"))
    if basis is not None and basis not in QUOTA_BASES:
        return {}, "invalid_quota_accounting"
    if basis == "provider_charged_quota" and multiplier is not None:
        return {}, "invalid_quota_accounting"
    if basis == "reconstructed_raw_usage" and multiplier is None:
        return {}, "invalid_quota_accounting"
    return {
        "basis": basis,
        "charged": charged,
        "multiplier": multiplier,
        "rolling": _number(measurements.get("rolling_quota")),
        "weekly": _number(measurements.get("weekly_quota")),
    }, None


def _unsanitized(value: Any, path: str) -> str | None:
    """Return the field path of the first value that is material, not identity."""

    if isinstance(value, str):
        if ABSOLUTE_PATH.match(value) or "\n" in value or "\r" in value:
            return path
        return path if len(value) > MAX_EMITTED_LENGTH else None
    if isinstance(value, dict):
        for key, nested in value.items():
            if found := _unsanitized(key, f"{path}.{key}"):
                return found
            if found := _unsanitized(nested, f"{path}.{key}"):
                return found
        return None
    if isinstance(value, list):
        for index, nested in enumerate(value):
            if found := _unsanitized(nested, f"{path}[{index}]"):
                return found
    return None


def _observation(attempt: dict[str, Any]) -> tuple[dict[str, Any] | None, str, str]:
    """Return the sanitized observation of one attempt, or its stable refusal.

    Every field is copied by name from a small allow-list, so material the
    caller happens to hold beside the facts — a brief, an answer, a verdict, a
    diff — has no path into the artifact even when it sits in the same object.
    """

    if error := _attempt_error(attempt):
        return None, "invalid_attempt", error
    if code := _outcome_refusal(attempt, attempt.get("outcome")):
        return None, code, "An external judgement of this attempt is required."
    configuration, unlaunchable = _configuration(attempt)
    if configuration is None:
        return None, cast(str, unlaunchable), "This decision launched nothing."
    if not isinstance(configuration["configuration_fingerprint"], str):
        return None, "unfingerprinted_configuration", "The point has no fingerprint."

    # Refuse an attempt that never reached the boundary it would be judged at.
    started, completed = attempt.get("started_at"), attempt.get("completed_at")
    if not isinstance(completed, str):
        return None, "incomplete_attempt", "An attempt needs the instant it ended."
    started = started if isinstance(started, str) else None

    outcome = cast(dict[str, Any], attempt["outcome"])
    scores, invalid_scores = _scores(outcome)
    if invalid_scores is not None:
        return None, invalid_scores, "Score dimensions must be normalized numbers."
    measurements = attempt.get("measurements")
    measurements = measurements if isinstance(measurements, dict) else {}
    quota, invalid_quota = _quota(measurements)
    if invalid_quota is not None:
        return None, invalid_quota, "One accounting basis applies its multiplier once."

    # Read the usage the environment actually exposed, leaving the rest null.
    tokens = measurements.get("tokens")
    tokens = tokens if isinstance(tokens, dict) else {}
    resolution = attempt.get("resolution")
    resolution = resolution if isinstance(resolution, dict) else {}
    audit = attempt["decision"].get("audit", {})
    provenance = audit.get("provenance", {}) if isinstance(audit, dict) else {}
    hashes = attempt.get("artifact_hashes") or []
    if not isinstance(hashes, list) or any(
        not isinstance(digest, str) or not ARTIFACT_HASH.match(digest)
        for digest in hashes
    ):
        return None, "unsanitized_artifact_hash", "Artifact identities are digests."

    observation = {
        "run_key": _run_key(
            cast(str, configuration["configuration_fingerprint"]),
            attempt["benchmark"]["key"],
            attempt["task_identity"],
            attempt.get("seed"),
            attempt["attempt_index"],
        ),
        "session_identity": attempt["session_identity"],
        "task_id": attempt["task_identity"],
        "seed": attempt.get("seed") if isinstance(attempt.get("seed"), str) else None,
        "attempt_index": attempt["attempt_index"],
        "workload_stratum": attempt["workload_stratum"],
        "configuration_fingerprint": configuration["configuration_fingerprint"],
        "benchmark_key": attempt["benchmark"]["key"],
        "routed": {
            field: configuration[field]
            for field in (
                "model",
                "resolved_alias",
                "portable_deliberation",
                "native_deliberation",
                "channel",
                "surface",
                "adapter_id",
                "serving_mode",
            )
        },
        "resolved": {
            "model": resolution.get("model") or configuration["model"],
            "fallback_from": resolution.get("fallback_from"),
        },
        "outcome": outcome["result"],
        "outcome_authority": outcome["authority"],
        "checker": (
            {
                "identity": outcome["checker"]["identity"],
                "independent": bool(outcome["checker"].get("independent")),
            }
            if isinstance(outcome.get("checker"), dict)
            else None
        ),
        "non_model_condition": outcome.get("condition"),
        "scores": scores,
        "tokens": {
            category: _number(tokens.get(category)) for category in TOKEN_CATEGORIES
        },
        "tool_calls": _number(measurements.get("tool_calls")),
        "retries": _number(measurements.get("retries")),
        "cost": {field: _number(measurements.get(field)) for field in COST_FIELDS},
        "quota": quota,
        "latency": {
            "wall_seconds": _measured(
                measurements.get("wall_seconds"), _elapsed(started, completed)
            ),
            "first_useful_output_seconds": _measured(
                measurements.get("first_useful_output_seconds"),
                _elapsed(started, measurements.get("first_useful_output_at")),
            ),
        },
        "started_at": started,
        "completed_at": completed,
        "policy": None,
        "provenance": {
            "route_status": configuration["route_status"],
            "snapshot_identity": audit.get("snapshot_identity")
            if isinstance(audit, dict)
            else None,
            "evidence_class": attempt["decision"].get("evidence_class"),
            "profile_revision": provenance.get("profile_revision"),
            "evidence_identity": provenance.get("evidence_identity"),
            "evidence_vintage": provenance.get("evidence_vintage"),
            "main_seat_model": provenance.get("main_seat_model"),
            "harness": attempt["harness"]["name"],
            "harness_inventory_revision": attempt["harness"].get("inventory_revision"),
        },
        "artifact_hashes": list(hashes),
    }

    # Hold every emitted string to an identity rather than to material.
    if field := _unsanitized(observation, "observation"):
        return None, "unsanitized_value", f"{field} carries material, not an identity."
    return observation, "", ""


def _policy_account(
    observation: dict[str, Any], prior: dict[str, Any], charge: Any
) -> dict[str, Any]:
    """Return what a cheap-first policy actually cost across its whole sequence.

    The policy is charged for the attempt that failed, for the checker that
    judged it, and for the retry that followed. A dimension no contributor
    exposed stays null rather than reading as a saving.
    """

    charge = charge if isinstance(charge, dict) else {}
    charged: dict[str, float | int | None] = {}
    for dimension in POLICY_DIMENSIONS:
        contributions = [
            _dimension(prior, dimension),
            _dimension(observation, dimension),
            _number(charge.get(dimension)),
        ]
        charged[dimension] = (
            None
            if any(value is None for value in contributions)
            else sum(contributions)
        )
    return {
        "identity": "cheap_first",
        "attempts": [prior["run_key"], observation["run_key"]],
        "retries": observation["retries"],
        "charged": charged,
    }


def _dimension(observation: dict[str, Any], dimension: str) -> float | int | None:
    """Return one commercial or latency dimension of an emitted observation."""

    if dimension == "wall_seconds":
        return cast(float | None, observation["latency"]["wall_seconds"])
    if dimension in ("rolling_quota", "weekly_quota"):
        return cast(float | None, observation["quota"][dimension.split("_")[0]])
    return cast(float | None, observation["cost"][dimension])


def observe(artifact: Any) -> dict[str, Any]:
    """Return the importable observations of one batch of completed attempts.

    Each attempt is answered in input order, either by one sanitized
    observation or by one stable refusal. Nothing is written, nothing is
    imported, and an attempt that no external judgement completed produces no
    observation at all.
    """

    if error := _envelope_error(artifact, "attempts"):
        return _artifact_refusal("invalid_artifact", error)

    observations: list[dict[str, Any]] = []
    refusals: list[dict[str, Any]] = []
    emitted: dict[str, dict[str, Any]] = {}
    for attempt in artifact["attempts"]:
        observation, code, detail = _observation(attempt)
        if observation is None:
            attempt_id = (
                attempt.get("attempt_id") if isinstance(attempt, dict) else None
            )
            refusals.append(_refusal(attempt_id, code, detail))
            continue

        # Charge an escalated attempt to the policy its whole sequence spent.
        prior = emitted.get(attempt.get("prior_attempt_id"))
        if prior is not None:
            observation["policy"] = _policy_account(
                observation, prior, attempt.get("checker_charge")
            )

        # Report only what an explicit import would accept unchanged.
        if invalid := validate(observation):
            refusals.append(
                _refusal(attempt["attempt_id"], invalid["code"], invalid["detail"])
            )
            continue
        emitted[attempt["attempt_id"]] = observation
        observations.append(observation)

    return {
        "schema_version": SCHEMA_VERSION,
        "observations": observations,
        "refusals": refusals,
    }


def _envelope_error(artifact: Any, member: str) -> str | None:
    """Return why one versioned envelope cannot be read, or None where it can."""

    if not isinstance(artifact, dict):
        return "The artifact must be a JSON object."
    if artifact.get("schema_version") != SCHEMA_VERSION:
        return f"schema_version must equal {SCHEMA_VERSION}."
    if set(artifact) - {"schema_version", member}:
        return "The artifact contains an unsupported top-level field."
    if not isinstance(artifact.get(member), list) or not artifact[member]:
        return f"{member} must be a non-empty ordered array."
    return None


def validate(observation: Any) -> dict[str, str] | None:
    """Return why one observation may not be imported, or None where it may.

    This is the import validation itself rather than a rehearsal of it: the
    emitter runs it before reporting an artifact as importable, and `record`
    runs it again on whatever it is handed, so a hand-written artifact meets
    exactly the rules an emitted one met.
    """

    if not isinstance(observation, dict):
        return {"code": "invalid_observation", "detail": "It must be a JSON object."}
    required = (
        "run_key",
        "task_id",
        "attempt_index",
        "configuration_fingerprint",
        "benchmark_key",
        "outcome",
        "outcome_authority",
        "completed_at",
        "provenance",
        "workload_stratum",
    )
    for field in required:
        if observation.get(field) in (None, ""):
            return {
                "code": "incomplete_observation",
                "detail": f"{field} must be present.",
            }

    # Hold the outcome to the same external authority emission requires.
    outcome = {
        "result": observation["outcome"],
        "authority": observation["outcome_authority"],
        "condition": observation.get("non_model_condition"),
        "checker": observation.get("checker"),
    }
    if code := _outcome_refusal({}, outcome):
        return {"code": code, "detail": "An external judgement establishes an outcome."}
    if observation["workload_stratum"] not in STRATA:
        return {"code": "invalid_observation", "detail": "Unknown workload stratum."}
    if not isinstance(observation.get("provenance"), dict) or not observation[
        "provenance"
    ].get("snapshot_identity"):
        return {
            "code": "incomplete_observation",
            "detail": "provenance must name the frozen routing snapshot.",
        }
    if field := _unsanitized(observation, "observation"):
        return {
            "code": "unsanitized_value",
            "detail": f"{field} carries material, not an identity.",
        }

    # Recompute the identity last, so a forged key never masks a worse fault.
    expected = _run_key(
        observation["configuration_fingerprint"],
        observation["benchmark_key"],
        observation["task_id"],
        observation.get("seed"),
        observation["attempt_index"],
    )
    if observation["run_key"] != expected:
        return {
            "code": "invalid_run_key",
            "detail": "The run key must derive from the identity it names.",
        }
    return None


def merge(artifact: Any, observations: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge produced observations into a caller-owned artifact idempotently.

    An identical observation is skipped rather than repeated, and one that
    claims an identity already present with different content is a conflict:
    both sources are surfaced and neither is overwritten.
    """

    merged = deepcopy(artifact) if isinstance(artifact, dict) else None
    if merged is None or not isinstance(merged.get("observations"), list):
        merged = {"schema_version": SCHEMA_VERSION, "observations": []}
    held = {
        cast(str, existing["run_key"]): existing for existing in merged["observations"]
    }
    added: list[str] = []
    skipped: list[str] = []
    conflicts: list[dict[str, Any]] = []
    for observation in observations:
        run_key = cast(str, observation["run_key"])
        existing = held.get(run_key)
        if existing is None:
            merged["observations"].append(observation)
            held[run_key] = observation
            added.append(run_key)
        elif existing == observation:
            skipped.append(run_key)
        else:
            conflicts.append(
                {
                    "run_key": run_key,
                    "code": "conflicting_identity",
                    "held": _digest(existing),
                    "offered": _digest(observation),
                }
            )
    return {
        "artifact": merged,
        "added": added,
        "skipped": skipped,
        "conflicts": conflicts,
    }


def _ledger(directory: Path) -> dict[str, dict[str, Any]]:
    """Return the run observations already held, keyed by their run key."""

    path = directory / LEDGER_FILE
    if not path.exists():
        return {}
    held: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            held[str(record["run_key"])] = record
    return held


def _wilson_lower_bound(successes: int, runs: int) -> float | None:
    """Return the conservative success rate of one configuration, or None."""

    if runs == 0:
        return None
    rate = successes / runs
    centre = rate + WILSON_Z**2 / (2 * runs)
    spread = WILSON_Z * math.sqrt((rate * (1 - rate) + WILSON_Z**2 / (4 * runs)) / runs)
    return round((centre - spread) / (1 + WILSON_Z**2 / runs), 6)


def _mean(values: list[float | int | None]) -> float | None:
    """Return the mean of a complete set of measurements, or None where one is not."""

    known = [value for value in values if value is not None]
    return sum(known) / len(known) if values and len(known) == len(values) else None


def _frontier(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return one benchmark's frontier from the runs eligible for it.

    Quality is read from judged model outcomes alone. An infrastructure error
    and an abstention are counted where they happened and kept out of the rate,
    because neither says the configuration did the work badly.
    """

    points = []
    for fingerprint in sorted(
        {str(record["configuration_fingerprint"]) for record in records}
    ):
        cohort = [
            record
            for record in records
            if record["configuration_fingerprint"] == fingerprint
        ]
        judged = [record for record in cohort if record["outcome"] in DECISIVE_RESULTS]
        successes = sum(1 for record in judged if record["outcome"] == "pass")
        points.append(
            {
                "configuration_fingerprint": fingerprint,
                "runs": len(judged),
                "successes": successes,
                "quality_lower_bound": _wilson_lower_bound(successes, len(judged)),
                "excluded": {
                    result: sum(1 for r in cohort if r["outcome"] == result)
                    for result in CONDITIONAL_RESULTS
                },
                "cost": {
                    dimension: _mean(
                        [_dimension(record, dimension) for record in judged]
                    )
                    for dimension in POLICY_DIMENSIONS
                },
            }
        )
    return {"points": points, "non_dominated": _non_dominated(points)}


def _non_dominated(points: list[dict[str, Any]]) -> list[str]:
    """Return the points no completely measured peer dominates."""

    surviving = []
    for point in points:
        dominated = any(
            peer is not point and _dominates(peer, point) for peer in points
        )
        if not dominated:
            surviving.append(str(point["configuration_fingerprint"]))
    return surviving


def _dominates(peer: dict[str, Any], point: dict[str, Any]) -> bool:
    """Say whether *peer* is at least as good everywhere and better somewhere."""

    quality, other = point["quality_lower_bound"], peer["quality_lower_bound"]
    if quality is None or other is None or other < quality:
        return False
    costs = [
        (peer["cost"][dimension], point["cost"][dimension])
        for dimension in POLICY_DIMENSIONS
    ]
    if any(mine is None or theirs is None for mine, theirs in costs):
        return False
    if any(mine > theirs for mine, theirs in costs):
        return False
    return other > quality or any(mine < theirs for mine, theirs in costs)


def record(artifact: Any, directory: Path) -> dict[str, Any]:
    """Append every complete unseen observation and rebuild what changed.

    This is the only ledger mutation in the contract, and it happens because a
    user asked for it. An identity already held with identical content is
    skipped; the same identity with different content is a conflict that
    changes nothing at all.
    """

    accepted: list[dict[str, Any]] = []
    skipped: list[str] = []
    rejected: list[dict[str, Any]] = []
    held = _ledger(directory)
    for observation in artifact["observations"]:
        if invalid := validate(observation):
            rejected.append({"run_key": None, **invalid})
            continue
        run_key = cast(str, observation["run_key"])
        existing = held.get(run_key)
        if existing == observation:
            skipped.append(run_key)
        elif existing is not None:
            rejected.append(
                {
                    "run_key": run_key,
                    "code": "conflicting_identity",
                    "detail": "A different observation already holds this run key.",
                }
            )
        else:
            accepted.append(observation)

    # Append accepted rows, then rebuild only the frontiers whose set changed.
    frontiers: list[str] = []
    if accepted:
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / LEDGER_FILE).open("a", encoding="utf-8") as ledger:
            for observation in accepted:
                ledger.write(json.dumps(observation, sort_keys=True) + "\n")
        frontiers = _rebuild_frontiers(directory, accepted)

    return {
        "schema_version": SCHEMA_VERSION,
        "accepted": [str(observation["run_key"]) for observation in accepted],
        "skipped": skipped,
        "rejected": rejected,
        "frontiers_rebuilt": frontiers,
    }


def _rebuild_frontiers(directory: Path, accepted: list[dict[str, Any]]) -> list[str]:
    """Recompute the derived frontiers whose eligible run set actually changed."""

    path = directory / FRONTIER_FILE
    derived: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "frontiers": {}}
    if path.exists():
        derived = json.loads(path.read_text(encoding="utf-8"))
    affected = sorted({str(observation["benchmark_key"]) for observation in accepted})
    records = list(_ledger(directory).values())
    for benchmark_key in affected:
        derived["frontiers"][benchmark_key] = _frontier(
            [record for record in records if record["benchmark_key"] == benchmark_key]
        )
    path.write_text(
        json.dumps(derived, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return affected


def _observe_command(arguments: list[str]) -> tuple[dict[str, Any], int]:
    """Emit one artifact from completed attempts into caller-owned scratch."""

    if not arguments or arguments[0].startswith("-"):
        return _artifact_refusal("invalid_arguments", "Observe needs one path."), 2
    destination: Path | None = None
    rest = arguments[1:]
    if rest:
        if rest[0] != "--artifact" or len(rest) != 2:
            return _artifact_refusal("invalid_arguments", "Unsupported options."), 2
        destination = Path(rest[1])
    read, failure = _read(arguments[0])
    if failure is not None:
        return failure, 2
    response = observe(read)
    if "artifact_refusal" in response:
        return response, 2

    # Merge into the caller's own artifact, which is the only thing written.
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "verb": "observe",
        "artifact": None if destination is None else str(destination),
        "importable": [],
        "skipped": [],
        "conflicts": [],
        "refusals": response["refusals"],
        "observations": response["observations"],
    }
    if destination is not None:
        existing = None
        if destination.exists():
            existing = json.loads(destination.read_text(encoding="utf-8"))
        merged = merge(existing, response["observations"])
        report |= {
            "importable": merged["added"],
            "skipped": merged["skipped"],
            "conflicts": merged["conflicts"],
        }
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(merged["artifact"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        report["importable"] = [
            str(observation["run_key"]) for observation in response["observations"]
        ]
    return report, 0


def _record_command(arguments: list[str]) -> tuple[dict[str, Any], int]:
    """Import one reported artifact into the selected evidence directory."""

    if not arguments or arguments[0].startswith("-"):
        return _artifact_refusal("invalid_arguments", "Record needs one path."), 2
    rest = arguments[1:]
    directory = Path.home() / ".model-selector"
    if rest:
        if rest[0] != "--data" or len(rest) != 2:
            return _artifact_refusal("invalid_arguments", "Unsupported options."), 2
        directory = Path(rest[1]).expanduser()
    read, failure = _read(arguments[0])
    if failure is not None:
        return failure, 2
    if error := _envelope_error(read, "observations"):
        return _artifact_refusal("invalid_artifact", error), 2
    return {"verb": "record", **record(read, directory)}, 0


def _read(path: str) -> tuple[Any, dict[str, Any] | None]:
    """Return one JSON artifact, or the process refusal that replaces it."""

    try:
        content = Path(path).read_text(encoding="utf-8")
    except OSError as error:
        return None, _artifact_refusal("unreadable_artifact", str(error))
    try:
        return json.loads(content), None
    except json.JSONDecodeError as error:
        return None, _artifact_refusal("malformed_json", str(error))


def main(argv: list[str] | None = None) -> int:
    """Route one command to its seam and emit only machine-readable JSON."""

    arguments = sys.argv[1:] if argv is None else argv
    commands = {"observe": _observe_command, "record": _record_command}
    if not arguments or arguments[0] not in commands:
        response: dict[str, Any] = _artifact_refusal(
            "invalid_arguments", "Use observe <path> or record <path>."
        )
        status = 2
    else:
        response, status = commands[arguments[0]](arguments[1:])
    print(json.dumps(response, sort_keys=True, separators=(",", ":")))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
