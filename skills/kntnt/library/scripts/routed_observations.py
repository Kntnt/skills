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
import importlib.util
import json
import math
import re
import sys
from collections.abc import Callable, Collection
from copy import deepcopy
from datetime import UTC, datetime
from functools import cache
from pathlib import Path
from typing import Any, TypedDict, cast

# The version shared by attempt and observation envelopes.
SCHEMA_VERSION: int = 1

# The workload strata an attempt may be charged to. Orchestrate's five building
# roles are distinct strata because a mechanical wave fix and an initial build
# are different work, and an amend is a different attempt at the same work;
# delegation's execution subagent is the sixth. The seventh is the work nobody
# routed at all — an ordinary interactive session, which automatic capture no
# longer produces (ADR-0156).
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
SCORE_DIMENSION: re.Pattern[str] = re.compile(r"^[a-z][a-z0-9_]{0,31}$")

# The Standing Policy facts one frozen decision carries into the row it
# produces. A ratchet reads the ladder the run itself froze — its revision, its
# Cohort, and its resolved Rungs — so a policy that has moved since cannot
# reinterpret an attempt made under the one before it.
STANDING_POLICY_FIELDS: tuple[str, ...] = (
    "policy_revision",
    "workload_cohort",
    "starting_rung",
    "current_rung",
    "floor",
    "ceiling",
    "next_rung_up",
)

# The decision policy that names an Exploration Attempt. A row carrying it
# bought contrast at a Rung nobody would run production on, so the ratchet
# reads it and steps over it rather than counting it as a verdict on the
# Cohort's own Rung (ADR-0151).
EXPLORATION_POLICY: str = "exploration"

# Where the Standing Policy this ledger ratchets lives: the Library's own
# module, beside this one.
STANDING_POLICY_MODULE: str = "standing_policy.py"

# The Library's own argument grammar, beside this module, and the flags of this
# engine that carry no value. The grammar is told which they are rather than
# knowing one engine's by name, so a valueless flag added here never takes the
# operand written behind it (ADR-0152).
ARGUMENT_GRAMMAR_MODULE: str = "argument_grammar.py"
VALUELESS_FLAGS: frozenset[str] = frozenset({"--import"})

# Who may judge an attempt a machine is allowed to act on unasked. A frozen
# rubric and the user's own word establish an outcome perfectly well, but
# neither is a judgement the run itself reached, so the ratchet that escalates
# a Cohort and the import that files a row with no user step read these three
# and no others (issue #222).
MACHINE_AUTHORITIES: frozenset[str] = frozenset(
    {"independent_verifier", "objective_checker", "declared_failure_signal"}
)

# What else a routed caller may file unasked: the outcomes no model produced.
# A hinder, an open decision, a discovered dependency, and a tracker failure
# are what happened rather than a verdict on a configuration, and they are kept
# by the same import that keeps the verdicts.
NON_MODEL_OUTCOMES: frozenset[str] = frozenset({"abstain", "infra_error"})

# The stable code an import refuses under where the ledger itself could not be
# reached. It is the caller's account of a write that did not happen, never a
# reason for the work that produced the row to stop (ADR-0137).
IMPORT_FAILED: str = "automatic_import_failed"

# What one Cohort's threshold evaluation came to. Every import answers for
# every Cohort it touched, because "nothing moved" is a finding too.
POLICY_MOVED: str = "moved"
POLICY_STALE: str = "stale_policy_context"
POLICY_CEILING: str = "standing_policy_ceiling_reached"
POLICY_BELOW: str = "below_threshold"

# What a sanitized artifact identity looks like: an algorithm and its digest,
# never a file name and never a path.
ARTIFACT_HASH: re.Pattern[str] = re.compile(r"^[a-z0-9]+:[0-9a-f]{16,128}$")

# What an emitted string may never be. An absolute path names the machine the
# work ran on, a newline is where a transcript starts, and a long value is
# material rather than an identity.
ABSOLUTE_PATH: re.Pattern[str] = re.compile(r"^(?:[/~]|[A-Za-z]:[\\/]|\\\\)")
MAX_EMITTED_LENGTH: int = 200

# Where the ledger keeps what this module writes, under the selected data
# directory. Both names are the evidence ledger's own.
LEDGER_FILE: str = "run-observations.jsonl"
FRONTIER_FILE: str = "derived-frontiers.json"

# The confidence a conservative success rate is reported at. Wilson's interval
# is used rather than the raw rate so one passing attempt cannot read as
# certainty.
WILSON_Z: float = 1.96

# What one derived frontier is identified by: the check the outcomes came from,
# the stage of the run, the Cohort of the work, and the tags narrowing it. Rows
# differing on any member are never compared as one frontier.
type FrontierIdentity = tuple[str, str, str, tuple[str, ...]]


class WorkloadIdentity(TypedDict):
    """The Cohort a carrier names, or the three absences that name none."""

    stage: str | None
    workload_cohort: str | None
    workload_tags: list[str] | None


# The plain identity strings a projected evidence record reads off the routed
# point the ledger row kept. The native control is the sixth and is the
# Harness's own object rather than a string, so it is held to its own shape;
# `harness` is a seventh that the routed point does not carry itself and comes
# from the row's provenance instead.
ROUTED_IDENTITIES: tuple[str, ...] = (
    "model",
    "portable_deliberation",
    "channel",
    "surface",
    "serving_mode",
)


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
    fingerprint: str,
    benchmark_key: str,
    task_id: str,
    seed: Any,
    attempt_index: int,
    run_identity: Any = None,
) -> str:
    """Return the ledger's run key for one exact attempt at one exact task."""

    parts = [fingerprint, benchmark_key, task_id, "null" if seed is None else str(seed)]
    if run_identity is not None:
        parts.append(str(run_identity))
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
    return _identity_error(attempt)


def _identity_error(carrier: dict[str, Any]) -> str | None:
    """Return why a workload identity cannot be read, or None where it can.

    The three fields name the Cohort of the request a routed attempt answered,
    and they are optional: every row written before routed callers carried one
    is still a row. What is refused is a field that is present and is not the
    identity it claims to be, which is a different thing from a field that is
    absent.
    """

    for field in ("stage", "workload_cohort"):
        value = carrier.get(field)
        if value is not None and (not isinstance(value, str) or not value):
            return f"{field} must be a non-empty string where it is present."
    tags = carrier.get("workload_tags")
    if tags is not None and (
        not isinstance(tags, list)
        or any(not isinstance(tag, str) or not tag for tag in tags)
    ):
        return "workload_tags must be non-empty strings where they are present."
    return None


def _workload_identity(carrier: dict[str, Any]) -> WorkloadIdentity:
    """Return the Cohort a carrier names, or the three explicit absences.

    A Cohort is one identity rather than three fields that happen to sit
    together, so a carrier holding only some of them names none: half a Cohort
    would let a projected record assert a stage against runs that never
    declared a workload.
    """

    stage, cohort = carrier.get("stage"), carrier.get("workload_cohort")
    tags = carrier.get("workload_tags")
    if (
        not isinstance(stage, str)
        or not isinstance(cohort, str)
        or not isinstance(tags, list)
    ):
        return {"stage": None, "workload_cohort": None, "workload_tags": None}
    return {
        "stage": stage,
        "workload_cohort": cohort,
        "workload_tags": sorted({str(tag) for tag in tags}),
    }


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


def _audited_policy(audit: Any) -> dict[str, Any] | None:
    """Return the Standing Policy one frozen decision ran under, or None.

    A verdict inherits by authority rather than by policy and carries no block
    at all, so absence is ordinary here rather than a fault: such a row is
    evidence the ledger keeps and never evidence a policy may move on.
    """

    block = audit.get("standing_policy") if isinstance(audit, dict) else None
    if not isinstance(block, dict):
        return None
    return {field: deepcopy(block.get(field)) for field in STANDING_POLICY_FIELDS}


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

    prior = attempt.get("prior_attempt_id")
    observation = {
        "run_key": _run_key(
            configuration["configuration_fingerprint"],
            attempt["benchmark"]["key"],
            attempt["task_identity"],
            attempt.get("seed"),
            attempt["attempt_index"],
            attempt.get("run_identity"),
        ),
        "attempt_id": attempt["attempt_id"],
        "prior_attempt_id": prior if isinstance(prior, str) and prior else None,
        "run_identity": attempt.get("run_identity"),
        "session_identity": attempt["session_identity"],
        "task_id": attempt["task_identity"],
        "seed": attempt.get("seed") if isinstance(attempt.get("seed"), str) else None,
        "attempt_index": attempt["attempt_index"],
        "workload_stratum": attempt["workload_stratum"],
        **_workload_identity(attempt),
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
            "standing_policy": _audited_policy(audit),
            "exploration": audit.get("decision_policy") == EXPLORATION_POLICY
            if isinstance(audit, dict)
            else False,
            "harness": attempt["harness"]["name"],
            "harness_inventory_revision": attempt["harness"].get("inventory_revision"),
        },
        "artifact_hashes": list(hashes),
    }

    # Hold every emitted string to an identity rather than to material.
    if field := _unsanitized(observation, "observation"):
        return None, "unsanitized_value", f"{field} carries material, not an identity."
    return observation, "", ""


def _policy_account(chain: list[dict[str, Any]], charge: Any) -> dict[str, Any]:
    """Return what a cheap-first policy actually cost across its whole sequence.

    The policy is charged for every attempt that failed, for the checker that
    judged them, and for the retry that finally passed — however many links
    that took, because a policy that escalates twice cost what both
    escalations cost. A dimension no contributor exposed stays null rather
    than reading as a saving.
    """

    charge = charge if isinstance(charge, dict) else {}
    charged: dict[str, float | int | None] = {}
    for dimension in POLICY_DIMENSIONS:
        contributions = [_dimension(link, dimension) for link in chain]
        contributions.append(_number(charge.get(dimension)))
        charged[dimension] = (
            None
            if any(value is None for value in contributions)
            else sum(value for value in contributions if value is not None)
        )
    return {
        "identity": "cheap_first",
        "attempts": [link["run_key"] for link in chain],
        "retries": chain[-1]["retries"],
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
    chains: dict[str, list[dict[str, Any]]] = {}
    for attempt in artifact["attempts"]:
        observation, code, detail = _observation(attempt)
        if observation is None:
            attempt_id = (
                attempt.get("attempt_id") if isinstance(attempt, dict) else None
            )
            refusals.append(_refusal(attempt_id, code, detail))
            continue

        # Charge an escalated attempt to the policy its whole sequence spent.
        prior_id = attempt.get("prior_attempt_id")
        held = chains.get(prior_id, []) if isinstance(prior_id, str) else []
        chain = [*held, observation]
        if len(chain) > 1:
            observation["policy"] = _policy_account(
                chain, attempt.get("checker_charge")
            )

        # Report only what an explicit import would accept unchanged.
        if invalid := validate(observation):
            refusals.append(
                _refusal(attempt["attempt_id"], invalid["code"], invalid["detail"])
            )
            continue
        chains[attempt["attempt_id"]] = chain
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
    if detail := _identity_error(observation):
        return {"code": "invalid_observation", "detail": detail}
    if not isinstance(observation.get("provenance"), dict) or not observation[
        "provenance"
    ].get("snapshot_identity"):
        return {
            "code": "incomplete_observation",
            "detail": "provenance must name the frozen routing snapshot.",
        }
    if unsafe_field := _unsanitized(observation, "observation"):
        return {
            "code": "unsanitized_value",
            "detail": f"{unsafe_field} carries material, not an identity.",
        }

    # Recompute the identity last, so a forged key never masks a worse fault.
    expected = _run_key(
        observation["configuration_fingerprint"],
        observation["benchmark_key"],
        observation["task_id"],
        observation.get("seed"),
        observation["attempt_index"],
        observation.get("run_identity"),
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


def _wilson_bounds(successes: int, runs: int) -> tuple[float | None, float | None]:
    """Return the two-sided conservative interval of one configuration.

    Both ends are kept rather than the lower one alone, because the interval
    is what a decision is made against: a point whose bounds are far apart is
    an unfinished measurement rather than a measured mediocrity, and only the
    pair says which of the two it is.
    """

    if runs == 0:
        return None, None
    rate = successes / runs
    centre = rate + WILSON_Z**2 / (2 * runs)
    spread = WILSON_Z * math.sqrt((rate * (1 - rate) + WILSON_Z**2 / (4 * runs)) / runs)
    divisor = 1 + WILSON_Z**2 / runs
    return round((centre - spread) / divisor, 6), round((centre + spread) / divisor, 6)


def _mean(values: list[float | int | None]) -> float | None:
    """Return the mean of a complete set of measurements, or None where one is not."""

    known = [value for value in values if value is not None]
    return sum(known) / len(known) if values and len(known) == len(values) else None


def _frontier_identity(record: dict[str, Any]) -> FrontierIdentity | None:
    """Return the exact frontier one ledger row belongs to, or None for no frontier.

    A frontier compares configurations, so everything else about the work it
    compares them on has to be held still: the check the outcome came from,
    the stage of the run, the Cohort the work belongs to, and the tags that
    narrow it. A row naming no Cohort is comparable within nothing, which is
    why it stays in the ledger and enters no frontier.
    """

    named = _workload_identity(record)
    stage, cohort, tags = (
        named["stage"],
        named["workload_cohort"],
        named["workload_tags"],
    )
    benchmark_key = record.get("benchmark_key")
    if stage is None or cohort is None or tags is None:
        return None
    if not isinstance(benchmark_key, str) or not benchmark_key:
        return None
    return benchmark_key, stage, cohort, tuple(tags)


def _frontier_named(identity: FrontierIdentity) -> dict[str, Any]:
    """Return one frontier identity in the four fields a reader reads it by."""

    benchmark_key, stage, cohort, tags = identity
    return {
        "benchmark_key": benchmark_key,
        "stage": stage,
        "workload_cohort": cohort,
        "workload_tags": list(tags),
    }


def _frontier_key(identity: FrontierIdentity) -> str:
    """Return the stable storage key of one frontier identity.

    The identity is four values rather than one name, and joining them into a
    readable key would make the separator part of the contract. The digest
    keys the entry; the entry itself carries all four fields in the open.
    """

    return _digest(_frontier_named(identity))


def _frontier_groups(
    records: list[dict[str, Any]],
) -> dict[FrontierIdentity, list[dict[str, Any]]]:
    """Group every ledger row that names a frontier under the frontier it names."""

    grouped: dict[FrontierIdentity, list[dict[str, Any]]] = {}
    for record in records:
        identity = _frontier_identity(record)
        if identity is not None:
            grouped.setdefault(identity, []).append(record)
    return {identity: grouped[identity] for identity in sorted(grouped)}


def _frontier(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return one frontier from the runs eligible for it.

    Quality is read from judged model outcomes alone. An infrastructure error
    and an abstention are counted where they happened and kept out of the rate,
    because neither says the configuration did the work badly.
    """

    points = []
    for fingerprint in sorted(
        {str(record["configuration_fingerprint"]) for record in records}
    ):
        at_point = [
            record
            for record in records
            if record["configuration_fingerprint"] == fingerprint
        ]
        judged = [
            record for record in at_point if record["outcome"] in DECISIVE_RESULTS
        ]
        successes = sum(1 for record in judged if record["outcome"] == "pass")
        lower, upper = _wilson_bounds(successes, len(judged))
        points.append(
            {
                "configuration_fingerprint": fingerprint,
                "runs": len(judged),
                "successes": successes,
                "quality_lower_bound": lower,
                "quality_upper_bound": upper,
                "excluded": {
                    result: sum(1 for r in at_point if r["outcome"] == result)
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

    This is the only ledger mutation in the contract, so it is also where the
    Standing Policy of every Cohort the append touched is evaluated. An
    identity already held with identical content is skipped; the same identity
    with different content is a conflict that changes nothing at all.
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

    # Append accepted rows, then rebuild only the frontiers whose set changed
    # and evaluate the Standing Policy of every Cohort the append touched.
    frontiers: list[dict[str, Any]] = []
    policies: list[dict[str, Any]] = []
    if accepted:
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / LEDGER_FILE).open("a", encoding="utf-8") as ledger:
            for observation in accepted:
                ledger.write(json.dumps(observation, sort_keys=True) + "\n")
        frontiers = _rebuild_frontiers(directory, accepted)
        policies = _evaluate_standing_policy(directory, accepted)

    return {
        "schema_version": SCHEMA_VERSION,
        "accepted": [str(observation["run_key"]) for observation in accepted],
        "skipped": skipped,
        "rejected": rejected,
        "frontiers_rebuilt": frontiers,
        "standing_policy": policies,
    }


def machine_judged(observations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the observations a routed caller may file without asking anybody.

    This is the collection's one eligibility rule, and it has two callers:
    Orchestrate's automatic import at each verdict, and the import a routed
    caller asks `observe` for. A second copy of it is how two seams writing one
    ledger would come to disagree about what may enter it (issue #222).
    """

    return [
        observation
        for observation in observations
        if observation.get("outcome_authority") in MACHINE_AUTHORITIES
        or observation.get("outcome") in NON_MODEL_OUTCOMES
    ]


def _rebuild_frontiers(
    directory: Path, accepted: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Recompute the derived frontiers whose eligible run set actually changed."""

    # A row naming no Cohort is ledger accounting and no frontier's member, so
    # an import made entirely of such rows rebuilds nothing and says so.
    affected = sorted(
        {
            identity
            for identity in (
                _frontier_identity(observation) for observation in accepted
            )
            if identity is not None
        }
    )
    if not affected:
        return []

    # Keep only entries written under the current frontier identity. The file
    # is a reproducible summary of append-only rows, so an entry from an older
    # shape is discarded rather than migrated or left beside the new ones.
    path = directory / FRONTIER_FILE
    derived: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "frontiers": {}}
    if path.exists():
        held = json.loads(path.read_text(encoding="utf-8"))
        derived["frontiers"] = {
            key: entry
            for key, entry in held.get("frontiers", {}).items()
            if isinstance(entry, dict) and "workload_cohort" in entry
        }

    grouped = _frontier_groups(list(_ledger(directory).values()))
    for identity in affected:
        derived["frontiers"][_frontier_key(identity)] = {
            **_frontier_named(identity),
            **_frontier(grouped.get(identity, [])),
        }
    path.write_text(
        json.dumps(derived, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return [_frontier_named(identity) for identity in affected]


@cache
def _standing_policy_store() -> Any:
    """Load the Standing Policy store the ratchet reads and writes.

    The store is the Library's own module rather than either Skill's, and it is
    loaded from beside this one by path: a peer Skill's `scripts/` is not an
    interface this module may reach into, and neither is a `sys.path` it does
    not own (ADR-0149).
    """

    path = Path(__file__).resolve().parent / STANDING_POLICY_MODULE
    spec = importlib.util.spec_from_file_location("kntnt_standing_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("the Standing Policy store is missing from the Library")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _instant(value: Any) -> datetime | None:
    """Return one comparable instant, reading a naive one as UTC.

    The history writes UTC and an emitted row carries whatever its Harness
    stated, so the two are made comparable here rather than at every ordering
    and epoch test that needs them to be.
    """

    parsed = _timestamp(value)
    if parsed is None:
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def _carried_policy_block(row: dict[str, Any]) -> dict[str, Any]:
    """Return the frozen Standing Policy one ledger row carries, or an empty one."""

    provenance = row.get("provenance")
    carried = (
        provenance.get("standing_policy") if isinstance(provenance, dict) else None
    )
    return carried if isinstance(carried, dict) else {}


def _rung(value: Any) -> dict[str, str] | None:
    """Return one well-formed Rung — a model and a portable level — or None.

    The store raises on anything else, and a hand-written artifact reaches
    `record` without its carried policy being held to any shape, so the two
    Rungs the ratchet reads are checked here rather than at the write.
    """

    if not isinstance(value, dict) or set(value) != {"model", "portable_deliberation"}:
        return None
    if any(not isinstance(level, str) or not level for level in value.values()):
        return None
    return {
        "model": value["model"],
        "portable_deliberation": value["portable_deliberation"],
    }


def _row_rung(row: dict[str, Any]) -> dict[str, str] | None:
    """Return the Rung one ledger row actually ran on, or None where it names none."""

    routed = row.get("routed")
    routed = routed if isinstance(routed, dict) else {}
    return _rung(
        {
            "model": routed.get("model"),
            "portable_deliberation": routed.get("portable_deliberation"),
        }
    )


def _epoch(rows: list[dict[str, Any]], cohort: str) -> datetime | None:
    """Return when one Cohort's current policy epoch began, or None for none.

    Every movement starts one — a threshold trip and a reset alike. Evidence
    from before it has already been answered, so it can neither escalate the
    same Cohort twice nor immediately undo the reset a person asked for.
    """

    started = [
        instant
        for row in rows
        if row.get("workload_cohort") == cohort
        and (instant := _instant(row.get("effective_at"))) is not None
    ]
    return max(started) if started else None


def _eligible_at(
    row: dict[str, Any], cohort: str, revision: int, epoch: datetime | None
) -> datetime | None:
    """Return when an eligible row completed, or None where it is not one.

    Eligibility is what makes `N of M` mean anything, and a pass is as eligible
    as a failure: one Cohort, one machine judgement, one Rung — the policy's
    own start, so a retry that already escalated is not counted against the
    start it escalated from — under the revision in force now and inside the
    current epoch. An Exploration Attempt buys information at a Rung nobody
    chose and is excluded with the rest.
    """

    if row.get("workload_cohort") != cohort:
        return None
    if row.get("outcome") not in DECISIVE_RESULTS:
        return None
    if row.get("outcome_authority") not in MACHINE_AUTHORITIES:
        return None
    provenance = row.get("provenance")
    if isinstance(provenance, dict) and provenance.get("exploration") is True:
        return None
    carried = _carried_policy_block(row)
    if carried.get("policy_revision") != revision:
        return None
    rung = _row_rung(row)
    if rung is None or carried.get("starting_rung") != rung:
        return None
    above = carried.get("next_rung_up")
    if above is not None and _rung(above) is None:
        return None
    completed = _instant(row.get("completed_at"))
    if completed is None or (epoch is not None and completed <= epoch):
        return None
    return completed


def _policy_window(
    directory: Path, cohort: str, revision: int, epoch: datetime | None, size: int
) -> list[dict[str, Any]]:
    """Return the last *size* eligible rows of one Cohort, oldest first.

    The order is the instant each row completed and then its run key, so two
    rows the same Harness stamped alike still have one place each. The window
    need not be full: a Cohort with three eligible rows is judged on three.
    """

    ordered = sorted(
        (
            (completed, str(row["run_key"]), row)
            for row in _ledger(directory).values()
            if (completed := _eligible_at(row, cohort, revision, epoch)) is not None
        ),
        key=lambda entry: (entry[0], entry[1]),
    )
    return [row for _, _, row in ordered[-size:]]


def _failure_threshold(store: Any, effective: dict[str, Any]) -> tuple[int, int]:
    """Return the failures and the window one Cohort trips at.

    The shipped pair is the whole of version 1 and nothing sets it, so a
    threshold of any other shape reached the store by hand. It is answered with
    the shipped numbers rather than by refusing to evaluate a policy the store
    itself still reads perfectly well.
    """

    shipped = store.DEFAULT_FAILURE_THRESHOLD
    threshold = effective.get("failure_threshold")
    stated = threshold if isinstance(threshold, dict) else {}
    failures, window = stated.get("failures"), stated.get("window")
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 1
        for value in (failures, window)
    ):
        return int(shipped["failures"]), int(shipped["window"])
    return cast(int, failures), cast(int, window)


def _evaluate_cohort(
    store: Any, directory: Path, cohort: str, accepted: list[dict[str, Any]]
) -> dict[str, Any]:
    """Ratchet one Cohort where the import brought it to its failure threshold."""

    effective = store.effective_policy(directory, cohort)
    revision = int(effective["revision"])
    needed, size = _failure_threshold(store, effective)
    account: dict[str, Any] = {
        "workload_cohort": cohort,
        "threshold": {"failures": needed, "window": size},
        "failures": 0,
        "window": 0,
        "run_keys": [],
        "row": None,
    }

    # Keep an in-flight run frozen under an older revision from moving a policy
    # another run or a reset has already changed. Its evidence stays in the
    # ledger; only its authority over the policy is gone.
    if not any(
        observation.get("workload_cohort") == cohort
        and _carried_policy_block(observation).get("policy_revision") == revision
        for observation in accepted
    ):
        return account | {"outcome": POLICY_STALE}

    # Count the verified failures among the rows this epoch leaves eligible.
    epoch = _epoch(store.history(directory), cohort)
    window = _policy_window(directory, cohort, revision, epoch, size)
    failed = [row for row in window if row["outcome"] == "fail"]
    account |= {
        "failures": len(failed),
        "window": len(window),
        "run_keys": [str(row["run_key"]) for row in failed],
    }
    if len(failed) < needed:
        return account | {"outcome": POLICY_BELOW}

    # Move to the Rung the triggering failure's own frozen decision named next,
    # and stop where that decision already stood at the Cohort's ceiling.
    triggering = failed[-1]
    rung = _rung(_carried_policy_block(triggering).get("next_rung_up"))
    if rung is None:
        return account | {"outcome": POLICY_CEILING}
    store.move_starting_rung(
        directory,
        cohort,
        rung,
        {
            "kind": store.THRESHOLD_CAUSE,
            "run_keys": account["run_keys"],
            "source_run_identity": triggering.get("run_identity"),
        },
    )
    return account | {"outcome": POLICY_MOVED, "row": store.history(directory)[-1]}


def _evaluate_standing_policy(
    directory: Path, accepted: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Answer for every Cohort one import touched, moving the ones that tripped.

    This is the ratchet's only seam, and it sits inside `record` so that the
    engine's automatic import at each verdict and the user's own `record` verb
    reach it identically — a policy that moved for one and not the other would
    be two policies. It only ever moves a Cohort up; the way back down is
    `config policy reset`, which a person asks for (ADR-0149). A row naming no
    Cohort is ledger accounting and moves nothing.
    """

    store = _standing_policy_store()
    touched = sorted(
        {
            observation["workload_cohort"]
            for observation in accepted
            if isinstance(observation.get("workload_cohort"), str)
            and observation["workload_cohort"]
        }
    )
    return [_evaluate_cohort(store, directory, cohort, accepted) for cohort in touched]


def _ordered_chain(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Order one task's attempts inside one run as they were actually made.

    `attempt_index` is what each row states about its own place; the links
    `prior_attempt_id` holds are what the rows after it state about the
    sequence. The links are followed where the ledger holds a whole unbroken
    one, and validate the order when they do; a chain from before they were
    written, or one whose links do not reach every row exactly once, is still
    ordered by the index every row has always carried.
    """

    by_index = sorted(
        rows, key=lambda row: (int(row["attempt_index"]), str(row["run_key"]))
    )
    named = {
        str(row["attempt_id"]): row
        for row in rows
        if isinstance(row.get("attempt_id"), str)
    }
    heads = [row for row in rows if row.get("prior_attempt_id") is None]
    if len(by_index) < 2 or len(named) != len(rows) or len(heads) != 1:
        return by_index

    # Walk the links forward, stopping at the first one that is not a chain.
    following: dict[str, dict[str, Any]] = {}
    for row in rows:
        prior = row.get("prior_attempt_id")
        if isinstance(prior, str) and prior not in following:
            following[prior] = row
    linked = [heads[0]]
    seen = {str(heads[0]["attempt_id"])}
    while (next_row := following.get(str(linked[-1]["attempt_id"]))) is not None:
        if str(next_row["attempt_id"]) in seen:
            break
        seen.add(str(next_row["attempt_id"]))
        linked.append(next_row)
    return linked if len(linked) == len(rows) else by_index


def _chain_commercial(
    records: list[dict[str, Any]],
) -> dict[tuple[FrontierIdentity, str], dict[str, Any]]:
    """Return what each frontier point's successful chains were measured to cost.

    A chain is one task's routed attempts inside one run — the session that
    produced them where a row names no run — and it is grouped from the whole
    ledger rather than from one frontier: a cheap build that
    failed and the amend that then passed are different strata, so a chain
    assembled inside one frontier would never see the escalation it exists to
    price. What the chain cost is all of it — the attempt that failed, the
    checker that judged it, and the retry after it — and Time to Verified Pass
    is the run from its first launch to the instant its first passing verdict
    landed, retries included. Both are charged to the configuration that
    finally passed, because a cheap point that needed two escalations to get
    there saved nobody anything, and they are charged inside the Cohort that
    pass belongs to, a row being evidence only there (ADR-0145). A chain no
    verdict passed contributes nothing at all: an unfinished measurement is
    not a fast free one, and a censored zero is what would make it look like
    the cheapest point on the frontier.
    """

    chains: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in records:
        # A row the ledger does not hold whole belongs to no chain: it is
        # damaged accounting rather than one link of a policy's sequence.
        if not isinstance(record.get("task_id"), str) or not isinstance(
            record.get("attempt_index"), int
        ):
            continue

        # A chain is one run's sequence. A row naming no run — a hand recorded
        # observation, a row older than run identity — falls back to the
        # session that produced it, which is a required field and is the same
        # boundary: grouping those by task alone would assemble attempts from
        # unrelated runs into one chain and charge the whole of it once.
        run = record.get("run_identity")
        boundary = run if isinstance(run, str) and run else record["session_identity"]
        chains.setdefault((str(boundary), str(record["task_id"])), []).append(record)

    # Charge each whole chain, once, to the point its first pass landed on.
    spent: dict[tuple[FrontierIdentity, str], list[float | int | None]] = {}
    elapsed: dict[tuple[FrontierIdentity, str], list[float | int | None]] = {}
    for chain in chains.values():
        ordered = _ordered_chain(chain)
        passed = next(
            (
                position
                for position, row in enumerate(ordered)
                if row["outcome"] == "pass"
            ),
            None,
        )
        if passed is None:
            continue
        winner = ordered[passed]
        identity = _frontier_identity(winner)
        if identity is None:
            continue
        point = (identity, str(winner["configuration_fingerprint"]))
        reached = ordered[: passed + 1]
        cash = [_dimension(row, "cash") for row in reached]
        spent.setdefault(point, []).append(
            None if any(value is None for value in cash) else sum(cash)  # type: ignore[arg-type]
        )
        elapsed.setdefault(point, []).append(
            _elapsed(reached[0].get("started_at"), winner.get("completed_at"))
        )

    # Report a mean only where every contributing chain carried the measure.
    return {
        point: {
            "cash": _mean(spent[point]),
            "rolling_quota": None,
            "weekly_quota": None,
            "allocated_subscription_cost": None,
            "latency": _mean(elapsed[point]),
        }
        for point in spent
    }


def _projected_record(
    identity: FrontierIdentity,
    point: dict[str, Any],
    row: dict[str, Any],
    commercial: dict[str, Any],
) -> dict[str, Any] | None:
    """Return the evidence record one frontier point states, or None for none.

    The interval comes from the point, the exact configuration from the row
    that ran on it, and the Cohort from the frontier all its rows share. A
    point with no decisive run states nothing here: the numeric quality and
    the interval an evidence record requires do not exist for it, and a
    missing measurement is never a zero.
    """

    lower, upper = point["quality_lower_bound"], point["quality_upper_bound"]
    if not point["runs"] or lower is None or upper is None:
        return None

    # Read the exact point off the routed decision the ledger row kept whole.
    routed = row.get("routed")
    routed = routed if isinstance(routed, dict) else {}
    provenance = row.get("provenance")
    provenance = provenance if isinstance(provenance, dict) else {}
    named: dict[str, Any] = {field: routed.get(field) for field in ROUTED_IDENTITIES}
    named["harness"] = provenance.get("harness")
    native = routed.get("native_deliberation")

    # Refuse to name a point whose own identity the ledger does not hold whole.
    if any(not isinstance(value, str) or not value for value in named.values()):
        return None
    if not isinstance(native, dict) or not native:
        return None

    _, stage, cohort, tags = identity
    return {
        "configuration_fingerprint": str(point["configuration_fingerprint"]),
        **named,
        "native_deliberation": native,
        "stage": stage,
        "workload_cohort": cohort,
        "workload_tags": list(tags),
        "representative": True,
        "coverage": {"decision_relevant": True},
        "uncertainty": {"lower_bound": lower, "upper_bound": upper},
        "quality": round(point["successes"] / point["runs"], 6),
        "stale": False,
        "commercial": commercial,
    }


def project(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return what a ledger states as routing evidence, and how new it is.

    This is the ledger read as evidence rather than as accounting: one record
    per exact configuration inside one frontier, carrying the conservative
    interval that frontier's judged runs establish (ADR-0145). Nothing is
    classified here: the route module owns the only classifier there is
    (ADR-0083), and a second one answering the same question in a second place
    is exactly what would let `record` and `route` disagree about one ledger.
    """

    projected: list[dict[str, Any]] = []
    vintages: list[str] = []
    unknown: dict[str, Any] = {
        "cash": None,
        "rolling_quota": None,
        "weekly_quota": None,
        "allocated_subscription_cost": None,
        "latency": None,
    }
    charged = _chain_commercial(records)
    for identity, rows in _frontier_groups(records).items():
        for point in _frontier(rows)["points"]:
            # Order one point's rows so the record names the same one twice.
            members = sorted(
                (
                    row
                    for row in rows
                    if row["configuration_fingerprint"]
                    == point["configuration_fingerprint"]
                ),
                key=lambda row: str(row["run_key"]),
            )

            # Keep only points the ledger states a whole measurement for.
            evidence = _projected_record(
                identity,
                point,
                members[0],
                charged.get(
                    (identity, str(point["configuration_fingerprint"])), dict(unknown)
                ),
            )
            if evidence is None:
                continue

            # Date the evidence by the rows it was actually derived from.
            projected.append(evidence)
            vintages.extend(
                str(row["completed_at"])
                for row in members
                if isinstance(row.get("completed_at"), str)
            )

    return {"records": projected, "vintage": max(vintages) if vintages else None}


def projected_evidence(directory: Path) -> dict[str, Any]:
    """Return the evidence records the ledger under *directory* states."""

    return project(list(_ledger(directory).values()))


def _argument_grammar() -> Any:
    """Load the argument grammar this engine reads its command line with.

    The grammar is the Library's own module rather than this engine's habit,
    and it is loaded from beside this one by path, exactly as the Standing
    Policy store above is: a peer Skill's `scripts/` is not an interface this
    module may reach into, and neither is a `sys.path` it does not own
    (ADR-0149).
    """

    path = Path(__file__).resolve().parent / ARGUMENT_GRAMMAR_MODULE
    spec = importlib.util.spec_from_file_location("kntnt_argument_grammar", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("the argument grammar is missing from the Library")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The one implementation, bound to the names this engine parses with.
_GRAMMAR: Any = _argument_grammar()
_option: Callable[[list[str], str], str | None] = _GRAMMAR.option
_split: Callable[[list[str], Collection[str]], tuple[list[str], list[str]]] = (
    _GRAMMAR.split
)


def _operands_first(arguments: list[str]) -> list[str]:
    """Return the same arguments with the operands ahead of the options.

    The Skills write one invocation order — the command path, then the flags,
    then the operands (ADR-0097) — while this parser reads its path first, so
    the shared grammar normalises both into the one this engine reads.
    """

    operands, options = _split(arguments, VALUELESS_FLAGS)
    return operands + options


def _flags(options: list[str], names: Collection[str]) -> dict[str, str] | None:
    """Return what each option this engine has was given, or None for the rest.

    The grammar keeps a separated value directly behind its flag, so the line
    reads as one flag at a time however the caller spelled it. A flag this
    command does not have, one written twice, and one with nothing behind it
    are each the whole line's refusal rather than a value quietly dropped.
    """

    given: dict[str, str] = {}
    rest = list(options)
    while rest:
        token = rest.pop(0)
        name = token.split("=", 1)[0]
        taken = [token] if "=" in token else [token, *rest[:1]]
        value = _option(taken, name)
        if name not in names or name in given or value is None:
            return None
        given[name] = value
        if "=" not in token:
            rest.pop(0)
    return given


def _import_observations(
    observations: list[dict[str, Any]], directory: Path
) -> dict[str, Any]:
    """File the observations this call may file, and report every identity.

    A ledger that cannot be written is reported as the refusal it is and never
    raised: the caller asking for this has already done the work the row
    describes, and evidence is not a reason to fail it (ADR-0137).
    """

    # Answer with an empty account where this call observed nothing fileable.
    account: dict[str, Any] = {
        "imported": [],
        "identically_skipped": [],
        "conflicting": [],
        "refused": [],
        "standing_policy": [],
    }
    eligible = machine_judged(observations)
    if not eligible:
        return account

    # File them, and turn a ledger this call cannot write into its own refusal.
    try:
        filed = record(
            {"schema_version": SCHEMA_VERSION, "observations": eligible}, directory
        )
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        account["refused"] = [
            {
                "run_key": str(observation["run_key"]),
                "code": IMPORT_FAILED,
                "detail": str(error),
            }
            for observation in eligible
        ]
        return account

    # Keep the accepted, duplicate, conflicting, and refused identities apart.
    account["imported"] = [str(key) for key in filed["accepted"]]
    account["identically_skipped"] = [str(key) for key in filed["skipped"]]
    account["standing_policy"] = filed["standing_policy"]
    for rejection in filed["rejected"]:
        run_key = rejection.get("run_key")
        if run_key is not None and rejection.get("code") == "conflicting_identity":
            account["conflicting"].append(str(run_key))
        else:
            account["refused"].append(rejection)
    return account


def _observe_command(arguments: list[str]) -> tuple[dict[str, Any], int]:
    """Emit one artifact from completed attempts, and file what it may.

    The artifact is what this command has always written. The import is the
    routed caller's, asked for by name: the verb a user runs by hand keeps its
    one side effect, and the caller that wants its evidence filed says so and
    names the ledger it goes to (issue #222).
    """

    # Read the one operand and the flags, refusing a ledger nothing writes.
    operands, options = _split(arguments, VALUELESS_FLAGS)
    if not operands or operands[0].startswith("-"):
        return _artifact_refusal("invalid_arguments", "Observe needs one path."), 2
    asked_to_import = "--import" in options
    given = _flags(
        [option for option in options if option != "--import"],
        ("--artifact", "--data"),
    )
    if (
        len(operands) > 1
        or options.count("--import") > 1
        or given is None
        or ("--data" in given and not asked_to_import)
    ):
        return _artifact_refusal("invalid_arguments", "Unsupported options."), 2

    # Name the artifact this call writes and the ledger an import would reach.
    destination = None if "--artifact" not in given else Path(given["--artifact"])
    directory = (
        Path(given["--data"]).expanduser()
        if "--data" in given
        else Path.home() / ".kntnt" / "model-selector"
    )

    read, failure = _read(operands[0])
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
        "import": None,
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

    # File the eligible observations where the caller asked this call to.
    if asked_to_import:
        report["import"] = _import_observations(response["observations"], directory)
    return report, 0


def _record_command(arguments: list[str]) -> tuple[dict[str, Any], int]:
    """Import one reported artifact into the selected evidence directory."""

    arguments = _operands_first(arguments)
    if not arguments or arguments[0].startswith("-"):
        return _artifact_refusal("invalid_arguments", "Record needs one path."), 2
    rest = arguments[1:]
    directory = Path.home() / ".kntnt" / "model-selector"
    if rest:
        data = _option(rest, "--data")
        if data is None:
            return _artifact_refusal("invalid_arguments", "Unsupported options."), 2
        directory = Path(data).expanduser()
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
