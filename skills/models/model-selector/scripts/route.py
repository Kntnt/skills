# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Resolve versioned model routing artifacts without external side effects."""

import hashlib
import json
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

PORTABLE_LEVELS: tuple[str, ...] = ("low", "medium", "high", "xhigh", "max")
COMMERCIAL_DIMENSIONS: tuple[str, ...] = (
    "cash",
    "rolling_quota",
    "weekly_quota",
    "allocated_subscription_cost",
    "latency",
)
REQUEST_SCHEMA_PATH: Path = (
    Path(__file__).resolve().parent.parent / "references" / "route-request.schema.json"
)
REQUEST_SCHEMA: dict[str, Any] = json.loads(
    REQUEST_SCHEMA_PATH.read_text(encoding="utf-8")
)


@dataclass(frozen=True, slots=True)
class Candidate:
    """Bind the named parts of one complete launchable exact point."""

    point: dict[str, Any]
    portable: str
    native: dict[str, Any]
    adapter: dict[str, Any]


@dataclass(frozen=True, slots=True)
class CandidatePool:
    """Keep candidate eligibility and its audit trail as one authority."""

    model_matches: tuple[dict[str, Any], ...]
    candidates: tuple[Candidate, ...]
    exclusions: tuple[dict[str, Any], ...]
    variant_exclusion_codes: tuple[str, ...]


def _schema_type_matches(value: Any, expected: str) -> bool:
    """Match the JSON type vocabulary without Python's boolean-number overlap."""

    match expected:
        case "object":
            return isinstance(value, dict)
        case "array":
            return isinstance(value, list)
        case "string":
            return isinstance(value, str)
        case "number":
            return _is_number(value)
        case "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        case "boolean":
            return isinstance(value, bool)
        case "null":
            return value is None
        case _:
            return False


def _resolve_schema_reference(reference: str, root: dict[str, Any]) -> dict[str, Any]:
    """Resolve a local JSON Pointer used by the shipped request schema."""

    value: Any = root
    for token in reference.removeprefix("#/").split("/"):
        value = value[token.replace("~1", "/").replace("~0", "~")]
    return cast(dict[str, Any], value)


def _schema_errors(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
    path: str,
) -> list[str]:
    """Validate the JSON Schema keywords used by the public routing contract."""

    # Resolve references and composition before inspecting concrete keywords.
    if "$ref" in schema:
        return _schema_errors(
            value,
            _resolve_schema_reference(schema["$ref"], root),
            root,
            path,
        )
    if "oneOf" in schema:
        branches = [
            _schema_errors(value, branch, root, path) for branch in schema["oneOf"]
        ]
        return (
            []
            if sum(not errors for errors in branches) == 1
            else [f"{path} must match exactly one allowed shape"]
        )
    if "allOf" in schema:
        return [
            error
            for branch in schema["allOf"]
            for error in _schema_errors(value, branch, root, path)
        ]
    if "anyOf" in schema:
        return (
            []
            if any(
                not _schema_errors(value, branch, root, path)
                for branch in schema["anyOf"]
            )
            else [f"{path} does not match an allowed shape"]
        )
    if "not" in schema and not _schema_errors(value, schema["not"], root, path):
        return [f"{path} matches a forbidden shape"]

    # Reject a mismatched primitive before collection-specific keywords run.
    expected_types = schema.get("type")
    if expected_types is not None:
        allowed = (
            [expected_types] if isinstance(expected_types, str) else expected_types
        )
        if not any(_schema_type_matches(value, expected) for expected in allowed):
            return [f"{path} has the wrong JSON type"]
    if "const" in schema and value != schema["const"]:
        return [f"{path} must equal {schema['const']!r}"]
    if "enum" in schema and value not in schema["enum"]:
        return [f"{path} is not an allowed value"]

    # Validate object membership and each declared or patterned property.
    errors: list[str] = []
    if isinstance(value, dict):
        required = schema.get("required", [])
        errors.extend(
            f"{path}.{field} is required" for field in required if field not in value
        )
        if len(value) < schema.get("minProperties", 0):
            errors.append(f"{path} has too few properties")
        properties = schema.get("properties", {})
        for field, child in value.items():
            child_path = f"{path}.{field}"
            if field in properties:
                errors.extend(
                    _schema_errors(child, properties[field], root, child_path)
                )
            elif schema.get("additionalProperties") is False:
                errors.append(f"{child_path} is not allowed")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(
                    _schema_errors(
                        child,
                        schema["additionalProperties"],
                        root,
                        child_path,
                    )
                )

    # Validate ordered array members and string cardinality constraints.
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path} has too few items")
        if "items" in schema:
            errors.extend(
                error
                for index, item in enumerate(value)
                for error in _schema_errors(
                    item,
                    schema["items"],
                    root,
                    f"{path}[{index}]",
                )
            )
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errors.append(f"{path} is too short")
    return errors


def _is_number(value: Any) -> bool:
    """Accept JSON numbers without treating booleans as capabilities or costs."""

    return isinstance(value, int | float) and not isinstance(value, bool)


def _snapshot_identity(snapshot: dict[str, Any]) -> str:
    """Hash canonical frozen routing facts without recursively hashing the digest."""

    canonical = deepcopy(snapshot)
    canonical.pop("snapshot_identity", None)
    encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def freeze_context(context: dict[str, Any]) -> dict[str, Any]:
    """Freeze caller-derived current facts into one reusable routing snapshot."""

    snapshot = deepcopy(context)
    snapshot.pop("snapshot_identity", None)
    snapshot["snapshot_identity"] = _snapshot_identity(snapshot)
    return snapshot


def _snapshot_structure_error(snapshot: Any, definition: str) -> str | None:
    """Return the first structural context or snapshot violation, if one exists."""

    # Treat the shipped JSON Schema as the structural runtime authority.
    errors = _schema_errors(
        snapshot,
        REQUEST_SCHEMA["$defs"][definition],
        REQUEST_SCHEMA,
        "snapshot",
    )
    return errors[0] if errors else None


def _snapshot_error(snapshot: dict[str, Any]) -> str | None:
    """Return the first cross-field snapshot invariant violation, if one exists."""

    # Validate cross-field mapping invariants the schema cannot express.
    for point in snapshot["mappings"]:
        native_order = point["native_control_order"]
        control_capabilities = point["control_capabilities"]
        if (
            any(native not in native_order for native in point["controls"].values())
            or (
                "max" in point["controls"]
                and point["controls"]["max"] != native_order[-1]
            )
            or set(control_capabilities) != set(point["controls"])
        ):
            return (
                "snapshot.mappings must freeze max as the highest verified "
                "native control"
            )

    # Detect a mutated supplied snapshot rather than blessing its old identity.
    if snapshot.get("snapshot_identity") != _snapshot_identity(snapshot):
        return "snapshot.snapshot_identity does not match its canonical frozen facts"
    return None


def _request_error(request: Any) -> str | None:
    """Return the first request-level contract violation, if one exists."""

    # Treat the shipped JSON Schema as the structural runtime authority.
    errors = _schema_errors(
        request,
        REQUEST_SCHEMA["$defs"]["request"],
        REQUEST_SCHEMA,
        "request",
    )
    if errors:
        return errors[0]

    return None


def _fingerprint(
    point: dict[str, Any],
    portable: str,
    native: Any,
    snapshot: dict[str, Any],
    adapter_id: str,
) -> str:
    """Bind every launch-relevant exact-point field into a stable identity."""

    value = {
        "model": point["model"],
        "channel": point["channel"],
        "harness": snapshot["harness"]["name"],
        "harness_inventory": snapshot["harness"]["inventory_revision"],
        "adapter_id": adapter_id,
        "surface": point.get("surface", snapshot["harness"]["surface"]),
        "serving_mode": point["serving_mode"],
        "portable_deliberation": portable,
        "native_deliberation": native,
        "tools": point.get("tools", []),
        "policy": point.get("policy", {}),
    }
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _adapter_can_launch(
    adapter: dict[str, Any],
    point: dict[str, Any],
    native: dict[str, Any],
    snapshot: dict[str, Any],
) -> bool:
    """Answer whether one concrete adapter can launch the complete exact point."""

    # Match every declared reachability dimension against the active Harness.
    if (
        adapter.get("channel") != point["channel"]
        or adapter.get("harness") != snapshot["harness"]["name"]
        or adapter.get("surface")
        != point.get("surface", snapshot["harness"]["surface"])
        or point["model"] not in adapter.get("models", [])
        or point["serving_mode"] not in adapter.get("serving_modes", [])
        or native not in adapter.get("native_controls", [])
        or point.get("tools", []) not in adapter.get("tool_sets", [])
        or point.get("policy", {}) not in adapter.get("policies", [])
    ):
        return False

    # Require a complete translation for every launch-relevant point field.
    launch = adapter.get("launch", {})
    native_flags = launch.get("native_control_flags", {})
    policy_flags = launch.get("policy_flags", {})
    return (
        isinstance(launch.get("model_flag"), str)
        and isinstance(launch.get("surface_flag"), str)
        and isinstance(launch.get("serving_mode_flag"), str)
        and isinstance(launch.get("tools_flag"), str)
        and isinstance(native_flags, dict)
        and set(native) <= set(native_flags)
        and isinstance(policy_flags, dict)
        and set(point.get("policy", {})) <= set(policy_flags)
    )


def _launch_adapter(
    point: dict[str, Any],
    native: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any] | None:
    """Resolve the first deterministic concrete adapter for an exact point."""

    compatible = [
        adapter
        for adapter in snapshot["harness"]["adapter_specs"]
        if _adapter_can_launch(adapter, point, native, snapshot)
    ]
    return min(compatible, key=lambda adapter: adapter["adapter_id"], default=None)


def _launch_arguments(
    adapter: dict[str, Any],
    point: dict[str, Any],
    native: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Translate one complete point into Harness-native launch arguments."""

    # Translate the complete point without dropping multi-field native controls.
    launch = adapter["launch"]
    arguments = {
        launch["model_flag"]: point["model"],
        launch["surface_flag"]: point.get("surface", snapshot["harness"]["surface"]),
        launch["serving_mode_flag"]: point["serving_mode"],
        launch["tools_flag"]: deepcopy(point.get("tools", [])),
    }
    arguments.update(
        {
            launch["native_control_flags"][field]: value
            for field, value in native.items()
        }
    )
    arguments.update(
        {
            launch["policy_flags"][field]: value
            for field, value in point.get("policy", {}).items()
        }
    )
    return arguments


def _model_capability(point: dict[str, Any]) -> float:
    """Resolve the model dimension of the frozen authority ceiling."""

    return float(point["model_capability"])


def _control_capability(point: dict[str, Any], portable: str) -> float:
    """Resolve deliberation capability without treating it as measured quality."""

    return float(point["control_capabilities"][portable])


def _within_main_seat(
    point: dict[str, Any], portable: str, snapshot: dict[str, Any]
) -> bool:
    """Apply both frozen model and deliberation authority ceilings."""

    main_seat = snapshot["main_seat"]
    model_ceiling = main_seat["model_capability"]
    deliberation_ceiling = main_seat["deliberation_capability"]
    if model_ceiling is None or deliberation_ceiling is None:
        return False
    return _model_capability(point) <= float(model_ceiling) and _control_capability(
        point, portable
    ) <= float(deliberation_ceiling)


def _exclusion(
    code: str,
    detail: str,
    point: dict[str, Any],
    portable: str | None = None,
) -> dict[str, Any]:
    """Build one stable hard-filter fact for compact and human audit output."""

    exclusion = {"code": code, "detail": detail, "model": point["model"]}
    if portable is not None:
        exclusion["portable_deliberation"] = portable
    return exclusion


def _candidate_pool(request: dict[str, Any], snapshot: dict[str, Any]) -> CandidatePool:
    """Evaluate every hard filter once and retain both results and reasons."""

    # Resolve the request dimensions used by every configured-point filter.
    overrides = request["overrides"]
    model_lock = overrides.get("model")
    portable_lock = overrides.get("deliberation")
    required_capabilities = set(request.get("required_capabilities", []))
    exact_model_exists = model_lock is not None and any(
        point["enabled"] and point["model"] == model_lock
        for point in snapshot["mappings"]
    )
    model_matches: list[dict[str, Any]] = []
    candidates: list[Candidate] = []
    exclusions: list[dict[str, Any]] = []
    variant_exclusion_codes: list[str] = []

    # Classify each point and exact portable variant through one authority.
    for point in snapshot["mappings"]:
        # Exclude disabled configuration before interpreting any dimensions.
        if not point["enabled"]:
            exclusions.append(
                _exclusion(
                    "disabled_point",
                    "The configured point is not enabled.",
                    point,
                )
            )
            continue

        # Preserve the independent model lock for availability and ambiguity.
        if model_lock is not None and not (
            point["model"] == model_lock
            or (not exact_model_exists and model_lock in point["aliases"])
        ):
            exclusions.append(
                _exclusion(
                    "model_override_mismatch",
                    "The point does not match the locked model dimension.",
                    point,
                )
            )
            continue
        model_matches.append(point)

        # Require frozen capability facts for the normalized workload needs.
        if not required_capabilities <= set(point["capabilities"]):
            exclusions.append(
                _exclusion(
                    "workload_capability_mismatch",
                    "The point does not cover every required workload capability.",
                    point,
                )
            )
            variant_exclusion_codes.append("workload_capability_mismatch")
            continue

        # Refuse approximation when the locked portable value has no mapping.
        if portable_lock is not None and portable_lock not in point["controls"]:
            exclusions.append(
                _exclusion(
                    "mapping_unavailable",
                    "The exact portable control has no verified native mapping.",
                    point,
                    portable_lock,
                )
            )
            variant_exclusion_codes.append("mapping_unavailable")
            continue

        # Evaluate only the locked value or each mapped value in scale order.
        portable_values = (
            [portable_lock]
            if portable_lock is not None
            else [
                portable
                for portable in PORTABLE_LEVELS
                if portable in point["controls"]
            ]
        )
        for portable in portable_values:
            native = point["controls"][portable]

            # Enforce both main-seat dimensions before resolving launch syntax.
            if not _within_main_seat(point, portable, snapshot):
                exclusions.append(
                    _exclusion(
                        "above_main_seat_ceiling",
                        "The complete point exceeds the frozen main seat.",
                        point,
                        portable,
                    )
                )
                variant_exclusion_codes.append("above_main_seat_ceiling")
                continue

            # Admit only variants with one complete active Harness adapter.
            adapter = _launch_adapter(point, native, snapshot)
            if adapter is None:
                exclusions.append(
                    _exclusion(
                        "adapter_unreachable",
                        "No active adapter can launch every field of this point.",
                        point,
                        portable,
                    )
                )
                variant_exclusion_codes.append("adapter_unreachable")
                continue
            candidates.append(Candidate(point, portable, native, adapter))

    # Freeze the evaluation so later selection cannot drift from its audit.
    return CandidatePool(
        tuple(model_matches),
        tuple(candidates),
        tuple(exclusions),
        tuple(variant_exclusion_codes),
    )


def _variant_fingerprint(
    point: dict[str, Any],
    portable: str,
    native: dict[str, Any],
    adapter: dict[str, Any],
    snapshot: dict[str, Any],
) -> str:
    """Fingerprint one expanded point variant before evidence selection."""

    return _fingerprint(
        point,
        portable,
        native,
        snapshot,
        adapter["adapter_id"],
    )


def _candidate_fingerprint(candidate: Candidate, snapshot: dict[str, Any]) -> str:
    """Fingerprint a named candidate without leaking its internal representation."""

    return _variant_fingerprint(
        candidate.point,
        candidate.portable,
        candidate.native,
        candidate.adapter,
        snapshot,
    )


def _evidence_is_relevant(
    record: dict[str, Any], request: dict[str, Any], point: dict[str, Any]
) -> bool:
    """Recognize measured facts from the same workload cohort and model."""

    return (
        record.get("model") == point["model"]
        and record.get("workload_cohort") == request.get("workload_cohort")
        and set(record.get("workload_tags", []))
        <= set(request.get("workload_tags", []))
    )


def _evidence_is_measurement(
    record: dict[str, Any],
    request: dict[str, Any],
    point: dict[str, Any],
    portable: str,
    native: dict[str, Any],
    fingerprint: str,
    snapshot: dict[str, Any],
) -> bool:
    """Require exact applicability, coverage, uncertainty, and quality floor."""

    # Match every decision-relevant identity field and workload stratum.
    harness = snapshot["harness"]
    identity_matches = (
        record.get("configuration_fingerprint") == fingerprint
        and record.get("model") == point["model"]
        and record.get("portable_deliberation") == portable
        and record.get("native_deliberation") == native
        and record.get("channel") == point["channel"]
        and record.get("harness") == harness["name"]
        and record.get("surface") == point.get("surface", harness["surface"])
        and record.get("serving_mode") == point["serving_mode"]
        and record.get("stage") == request["stage"]
        and record.get("workload_cohort") == request.get("workload_cohort")
        and set(record.get("workload_tags", []))
        <= set(request.get("workload_tags", []))
    )
    if not identity_matches or record.get("stale", False):
        return False

    # Keep unknown or weak decision support out of the green evidence class.
    coverage = record.get("coverage")
    uncertainty = record.get("uncertainty")
    quality_floor = snapshot["override_policy"].get("quality_floor")
    return (
        record.get("representative") is True
        and isinstance(coverage, dict)
        and coverage.get("decision_relevant") is True
        and isinstance(uncertainty, dict)
        and _is_number(uncertainty.get("lower_bound"))
        and _is_number(uncertainty.get("upper_bound"))
        and _is_number(quality_floor)
        and float(uncertainty["lower_bound"]) >= float(quality_floor)
    )


def _evidence_class(
    records: list[dict[str, Any]],
    request: dict[str, Any],
    point: dict[str, Any],
    portable: str,
    native: dict[str, Any],
    fingerprint: str,
    snapshot: dict[str, Any],
) -> str:
    """Classify only evidence applicable to the selected exact point."""

    if any(
        _evidence_is_measurement(
            record,
            request,
            point,
            portable,
            native,
            fingerprint,
            snapshot,
        )
        for record in records
    ):
        return "measurement_based"
    if any(_evidence_is_relevant(record, request, point) for record in records):
        return "mixed"
    return "heuristic"


def _quality_lower_bound(record: dict[str, Any]) -> float:
    """Read conservative measured quality without inventing missing uncertainty."""

    uncertainty = record.get("uncertainty")
    if isinstance(uncertainty, dict) and _is_number(uncertainty.get("lower_bound")):
        return float(uncertainty["lower_bound"])
    return float(record["quality"])


def _measurement_dominates(
    candidate: Candidate,
    record: dict[str, Any],
    other_candidate: Candidate,
    other_record: dict[str, Any],
) -> bool:
    """Apply multidimensional dominance only when every compared fact is known."""

    # Read every cost axis without inventing unavailable values.
    costs = candidate.point["commercial"]
    other_costs = other_candidate.point["commercial"]
    if any(
        not _is_number(costs[dimension]) or not _is_number(other_costs[dimension])
        for dimension in COMMERCIAL_DIMENSIONS
    ):
        return False

    # Require no worse quality and no worse value on every cost axis.
    quality = _quality_lower_bound(record)
    other_quality = _quality_lower_bound(other_record)
    no_worse = quality >= other_quality and all(
        float(costs[dimension]) <= float(other_costs[dimension])
        for dimension in COMMERCIAL_DIMENSIONS
    )
    strictly_better = quality > other_quality or any(
        float(costs[dimension]) < float(other_costs[dimension])
        for dimension in COMMERCIAL_DIMENSIONS
    )
    return no_worse and strictly_better


def _pareto_frontier(
    measured: list[tuple[Candidate, dict[str, Any]]],
) -> list[tuple[Candidate, dict[str, Any]]]:
    """Remove only candidates demonstrably dominated on quality and every cost."""

    return [
        item
        for index, item in enumerate(measured)
        if not any(
            _measurement_dominates(other[0], other[1], item[0], item[1])
            for other_index, other in enumerate(measured)
            if other_index != index
        )
    ]


def _shadow_cost(
    candidate: Candidate,
    shadow_prices: dict[str, Any],
) -> float | None:
    """Calculate a scenario cost only from a complete explicit conversion policy."""

    # Require known commercial values and prices for every non-cash dimension.
    commercial = candidate.point["commercial"]
    priced_dimensions = tuple(
        dimension for dimension in COMMERCIAL_DIMENSIONS if dimension != "cash"
    )
    if (
        not all(
            _is_number(commercial[dimension]) for dimension in COMMERCIAL_DIMENSIONS
        )
        or set(shadow_prices) != set(priced_dimensions)
        or not all(_is_number(value) for value in shadow_prices.values())
    ):
        return None

    # Convert only through the complete policy the frozen profile supplied.
    return float(commercial["cash"]) + sum(
        float(commercial[dimension]) * float(shadow_prices[dimension])
        for dimension in priced_dimensions
    )


def _frontier_audit(
    frontier: list[tuple[Candidate, dict[str, Any]]],
    snapshot: dict[str, Any],
) -> list[dict[str, Any]]:
    """Expose the exact non-dominated alternatives without collapsing their costs."""

    return [
        {
            "configuration_fingerprint": _candidate_fingerprint(candidate, snapshot),
            "model": candidate.point["model"],
            "portable_deliberation": candidate.portable,
            "quality_lower_bound": _quality_lower_bound(record),
            "commercial": deepcopy(candidate.point["commercial"]),
        }
        for candidate, record in frontier
    ]


def _measured_candidates(
    candidates: tuple[Candidate, ...],
    records: list[dict[str, Any]],
    request: dict[str, Any],
    snapshot: dict[str, Any],
) -> list[tuple[Candidate, dict[str, Any]]]:
    """Choose one conservative exact measurement per launchable candidate."""

    measured: list[tuple[Candidate, dict[str, Any]]] = []
    for candidate in candidates:
        # Retain only records that prove complete decision applicability.
        applicable = [
            record
            for record in records
            if _evidence_is_measurement(
                record,
                request,
                candidate.point,
                candidate.portable,
                candidate.native,
                _candidate_fingerprint(candidate, snapshot),
                snapshot,
            )
        ]
        if applicable:
            measured.append((candidate, max(applicable, key=_quality_lower_bound)))

    return measured


def _economic_candidate(
    frontier: list[tuple[Candidate, dict[str, Any]]],
    economics: dict[str, Any],
) -> tuple[Candidate | None, str]:
    """Apply an explicit human budget or quality-floor decision dimension."""

    # Map the named decision to its honest comparable commercial dimension.
    dimension = (
        "cash" if economics["decision"] == "route" else "allocated_subscription_cost"
    )
    known = [
        item for item in frontier if _is_number(item[0].point["commercial"][dimension])
    ]

    # Maximize conservative quality inside an explicit comparable budget.
    if "budget" in economics:
        affordable = [
            item
            for item in known
            if float(item[0].point["commercial"][dimension])
            <= float(economics["budget"])
        ]
        if not affordable:
            return None, f"budget_{dimension}"
        best_quality = max(_quality_lower_bound(item[1]) for item in affordable)
        quality_winners = [
            item for item in affordable if _quality_lower_bound(item[1]) == best_quality
        ]
        minimum_cost = min(
            float(item[0].point["commercial"][dimension]) for item in quality_winners
        )
        winners = [
            item
            for item in quality_winners
            if float(item[0].point["commercial"][dimension]) == minimum_cost
        ]
        return (
            winners[0][0] if len(winners) == 1 else None,
            f"budget_{dimension}",
        )

    # Minimize the named cost among points clearing the explicit quality floor.
    qualified = [
        item
        for item in known
        if _quality_lower_bound(item[1]) >= float(economics["quality_floor"])
    ]
    if not qualified:
        return None, f"quality_floor_{dimension}"
    minimum_cost = min(
        float(item[0].point["commercial"][dimension]) for item in qualified
    )
    winners = [
        item
        for item in qualified
        if float(item[0].point["commercial"][dimension]) == minimum_cost
    ]
    return (
        winners[0][0] if len(winners) == 1 else None,
        f"quality_floor_{dimension}",
    )


def _selection_decision(
    request: dict[str, Any],
    snapshot: dict[str, Any],
    pool: CandidatePool,
) -> dict[str, Any]:
    """Resolve one selected or underdetermined decision from an eligible pool."""

    # Match exact measurements once for every candidate and human output form.
    records = snapshot["evidence"]["records"]
    measured = _measured_candidates(pool.candidates, records, request, snapshot)
    decision_policy = "cold_start"
    frontier_audit: list[dict[str, Any]] = []

    # Resolve measured alternatives through explicit economics or Pareto policy.
    if measured:
        # Build the honest multidimensional frontier once for all output forms.
        frontier = _pareto_frontier(measured)
        frontier_audit = _frontier_audit(frontier, snapshot)
        economics = request.get("economics")

        # Give an explicit human budget or quality floor first precedence.
        if isinstance(economics, dict) and (
            "budget" in economics or "quality_floor" in economics
        ):
            winner, decision_policy = _economic_candidate(frontier, economics)
            if winner is None:
                return _inherit(
                    request,
                    snapshot,
                    "underdetermined_frontier",
                    {"frontier": frontier_audit},
                )
            eligible = [winner]

        # Accept a frontier containing exactly one non-dominated point.
        elif len(frontier) == 1:
            eligible = [frontier[0][0]]
            decision_policy = "pareto_dominance"

        # Resolve a tradeoff only through complete frozen shadow prices.
        else:
            shadow_prices = snapshot["override_policy"].get("shadow_prices")
            priced = (
                [(_shadow_cost(item[0], shadow_prices), item) for item in frontier]
                if isinstance(shadow_prices, dict)
                else []
            )
            if not priced or any(cost is None for cost, _ in priced):
                return _inherit(
                    request,
                    snapshot,
                    "underdetermined_frontier",
                    {"frontier": frontier_audit},
                )
            minimum = min(float(cost) for cost, _ in priced if cost is not None)
            winners = [
                item
                for cost, item in priced
                if cost is not None and float(cost) == minimum
            ]
            if len(winners) != 1:
                return _inherit(
                    request,
                    snapshot,
                    "underdetermined_frontier",
                    {"frontier": frontier_audit},
                )
            eligible = [winners[0][0]]
            decision_policy = "explicit_shadow_prices"

    # Refuse to treat a heuristic point as measured economic evidence.
    elif "economics" in request:
        return _inherit(request, snapshot, "insufficient_evidence")

    # Choose the workload-safe cold-start endpoint when measurements are absent.
    else:
        eligible = list(pool.candidates)
        decision_policy = (
            "cold_start_strongest"
            if not request["reversible"] and request["checker"]["kind"] == "none"
            else "cold_start_weakest"
        )

    # Choose the weakest or strongest complete candidate required by the policy.
    choose = max if decision_policy == "cold_start_strongest" else min
    candidate = choose(
        eligible,
        key=lambda item: (
            _model_capability(item.point),
            _control_capability(item.point, item.portable),
            PORTABLE_LEVELS.index(item.portable),
        ),
    )
    point = candidate.point
    portable = candidate.portable
    native = candidate.native
    adapter = candidate.adapter
    arguments = _launch_arguments(adapter, point, native, snapshot)
    fingerprint = _candidate_fingerprint(candidate, snapshot)

    # Classify and expose the exact winner from the same frozen evidence facts.
    overrides = request["overrides"]
    evidence = snapshot["evidence"]
    evidence_class = _evidence_class(
        records,
        request,
        point,
        portable,
        native,
        fingerprint,
        snapshot,
    )
    exclusions = deepcopy(list(pool.exclusions))

    return {
        "request_id": request["request_id"],
        "status": "selected",
        "launch": {
            "model": point["model"],
            "resolved_alias": overrides.get("model")
            if overrides.get("model") in point.get("aliases", [])
            else None,
            "adapter_id": adapter["adapter_id"],
            "surface": point.get("surface", snapshot["harness"]["surface"]),
            "channel": point["channel"],
            "serving_mode": point["serving_mode"],
            "tools": deepcopy(point.get("tools", [])),
            "policy": deepcopy(point.get("policy", {})),
            "portable_deliberation": portable,
            "native_deliberation": native,
            "configuration_fingerprint": fingerprint,
            "arguments": arguments,
            "commercial": deepcopy(point["commercial"]),
        },
        "evidence_class": evidence_class,
        "provenance": {
            "profile_revision": snapshot["profile"]["revision"],
            "evidence_identity": evidence["identity"],
            "evidence_vintage": evidence["vintage"],
        },
        "exclusions": exclusions,
        "next_escalation": _escalation(
            request,
            point,
            portable,
            native,
            adapter,
            snapshot,
            fingerprint,
        ),
        "audit": _audit(
            snapshot,
            {
                "decision_policy": decision_policy,
                "frontier": frontier_audit,
                "exclusions": deepcopy(exclusions),
            },
        ),
    }


def _audit(
    snapshot: dict[str, Any], facts: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Attach frozen provenance to every request-level routing outcome."""

    # Read shared facts defensively because invalid snapshots are still audited.
    profile = snapshot.get("profile")
    evidence = snapshot.get("evidence")
    harness = snapshot.get("harness")
    main_seat = snapshot.get("main_seat")
    return {
        "snapshot_identity": snapshot["snapshot_identity"],
        "provenance": {
            "profile_revision": profile.get("revision")
            if isinstance(profile, dict)
            else None,
            "evidence_identity": evidence.get("identity")
            if isinstance(evidence, dict)
            else None,
            "evidence_vintage": evidence.get("vintage")
            if isinstance(evidence, dict)
            else None,
            "harness_inventory_revision": harness.get("inventory_revision")
            if isinstance(harness, dict)
            else None,
            "main_seat_model": main_seat.get("model")
            if isinstance(main_seat, dict)
            else None,
        },
        **deepcopy(facts or {}),
    }


def _escalation(
    request: dict[str, Any],
    point: dict[str, Any],
    portable: str,
    native: dict[str, Any],
    adapter: dict[str, Any],
    snapshot: dict[str, Any],
    fingerprint: str,
) -> dict[str, Any] | None:
    """Describe one existing-retry step only after externally bound failure."""

    # Bind the prior attempt and external failure to the selected exact point.
    prior = request.get("prior", {})
    failure = request.get("verified_failure", {})
    checker = request.get("checker", {})
    exact_attempt = {
        "configuration_fingerprint": fingerprint,
        "model": point["model"],
        "channel": point["channel"],
        "surface": point.get("surface", snapshot["harness"]["surface"]),
        "serving_mode": point["serving_mode"],
        "adapter_id": adapter["adapter_id"],
        "portable_deliberation": portable,
        "native_deliberation": native,
    }

    # Suppress any retry not granted, checked, failed, and exactly matched.
    if (
        not request.get("reversible")
        or request.get("retry_available") is not True
        or checker.get("kind") not in {"external", "declared"}
        or not failure
        or failure.get("outcome") != "failed"
        or failure.get("checker") != checker
        or any(prior.get(field) != value for field, value in exact_attempt.items())
        or any(failure.get(field) != value for field, value in exact_attempt.items())
    ):
        return None

    # Resolve one adjacent supported point beneath the main-seat ceiling.
    adjacent_index = PORTABLE_LEVELS.index(portable) + 1
    if adjacent_index >= len(PORTABLE_LEVELS):
        return None
    adjacent = PORTABLE_LEVELS[adjacent_index]
    if adjacent not in point["controls"]:
        return None
    adjacent_native = point["controls"][adjacent]
    if not _within_main_seat(point, adjacent, snapshot):
        return None
    adjacent_adapter = _launch_adapter(point, adjacent_native, snapshot)
    if adjacent_adapter is None:
        return None
    adjacent_fingerprint = _variant_fingerprint(
        point,
        adjacent,
        adjacent_native,
        adjacent_adapter,
        snapshot,
    )

    # Return the complete next launch while consuming no new attempt.
    return {
        "model": point["model"],
        "adapter_id": adjacent_adapter["adapter_id"],
        "portable_deliberation": adjacent,
        "native_deliberation": deepcopy(adjacent_native),
        "configuration_fingerprint": adjacent_fingerprint,
        "arguments": _launch_arguments(
            adjacent_adapter,
            point,
            adjacent_native,
            snapshot,
        ),
        "consumes_existing_retry": True,
    }


def _refused(
    request: Any,
    snapshot: dict[str, Any],
    code: str,
    detail: str | None = None,
    exclusions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a stable refusal shape that cannot be mistaken for launchable."""

    request_id = (
        request.get("request_id")
        if isinstance(request, dict) and isinstance(request.get("request_id"), str)
        else None
    )
    return {
        "request_id": request_id,
        "status": "refused",
        "reason": {
            "code": code,
            "detail": detail or code.replace("_", " "),
        },
        "audit": _audit(snapshot, {"exclusions": deepcopy(exclusions or [])}),
    }


def _inherit(
    request: dict[str, Any],
    snapshot: dict[str, Any],
    reason: str,
    audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an audited no-override result with the frozen main seat."""

    return {
        "request_id": request["request_id"],
        "status": "inherit",
        "inheritance": {
            "reason": reason,
            "main_seat": deepcopy(snapshot["main_seat"]),
        },
        "audit": _audit(snapshot, audit),
    }


def _artifact_refusal(code: str, detail: str) -> dict[str, Any]:
    """Return one stable process-level refusal before request routing begins."""

    return {
        "schema_version": 1,
        "snapshot": None,
        "decisions": [],
        "artifact_refusal": {"code": code, "detail": detail},
    }


def _artifact_error(artifact: Any) -> str | None:
    """Validate the envelope facts required before a snapshot can be frozen."""

    if not isinstance(artifact, dict):
        return "The route artifact must be a JSON object."
    if set(artifact) - {"schema_version", "requests", "snapshot", "context"}:
        return "The route artifact contains an unsupported top-level field."
    if artifact.get("schema_version") != 1:
        return "schema_version must equal 1."
    requests = artifact.get("requests")
    if not isinstance(requests, list) or not requests:
        return "requests must be a non-empty ordered array."
    if ("snapshot" in artifact) == ("context" in artifact):
        return "Exactly one of snapshot or context must be supplied."
    snapshot_key = "snapshot" if "snapshot" in artifact else "context"
    if not isinstance(artifact[snapshot_key], dict):
        return f"{snapshot_key} must be a JSON object."
    request_ids = [
        request.get("request_id")
        for request in requests
        if isinstance(request, dict) and isinstance(request.get("request_id"), str)
    ]
    if len(request_ids) != len(set(request_ids)):
        return "request_id values must be unique within the ordered batch."
    return None


def _decision(request: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    """Apply hard refusals and inheritance before exact-point selection."""

    # Keep every verdict on the exact immutable main seat.
    if request["authority"] == "verdict":
        if not snapshot["harness"].get("inheritance"):
            return _refused(request, snapshot, "unrepresentable_verdict_inheritance")
        return _inherit(request, snapshot, "verdict_authority")

    # Distinguish absent profile state from invalid persisted state.
    if snapshot.get("profile") is None:
        return _inherit(request, snapshot, "missing_profile")
    if not snapshot["profile"].get("valid"):
        return _refused(request, snapshot, "invalid_profile")

    # Refuse selection when either frozen authority dimension is unknown.
    if (
        snapshot["main_seat"].get("model_capability") is None
        or snapshot["main_seat"].get("deliberation_capability") is None
    ):
        return _refused(request, snapshot, "unknown_main_seat_ceiling")

    # Reuse one hard-filter result for selection, refusals, and audit output.
    overrides = request["overrides"]
    deliberation = overrides.get("deliberation")
    pool = _candidate_pool(request, snapshot)

    # Refuse model locks that resolve to no enabled exact point.
    if overrides.get("model") and not pool.model_matches:
        return _refused(request, snapshot, "unavailable_override")

    # Refuse aliases that do not identify exactly one configured release.
    resolved_models = {point["model"] for point in pool.model_matches}
    if overrides.get("model") and len(resolved_models) > 1:
        return _refused(request, snapshot, "ambiguous_override")

    # Refuse portable locks unsupported by every model-matched point.
    if deliberation and not any(
        deliberation in point["controls"] for point in pool.model_matches
    ):
        return _refused(request, snapshot, "unavailable_override")

    # Give an explicit all-above-ceiling point its precise stable refusal.
    if (
        overrides
        and not pool.candidates
        and pool.variant_exclusion_codes
        and set(pool.variant_exclusion_codes) == {"above_main_seat_ceiling"}
    ):
        return _refused(request, snapshot, "above_main_seat_ceiling")

    # Refuse an empty safe set with the authoritative hard-filter audit.
    if not pool.candidates:
        return _refused(
            request,
            snapshot,
            "empty_safe_candidate_set",
            "No configured point remains after complete Harness filtering.",
            list(pool.exclusions),
        )

    # Honor a frozen policy that declines unmeasured automatic cold starts.
    if (
        not snapshot["evidence"].get("records")
        and not overrides
        and snapshot["override_policy"].get("cold_start") != "select"
    ):
        return _inherit(request, snapshot, "insufficient_evidence")

    return _selection_decision(request, snapshot, pool)


def route(artifact: Any) -> dict[str, Any]:
    """Return ordered decisions and the exact snapshot used to derive them."""

    # Refuse malformed envelopes once, before any request is interpreted.
    if error := _artifact_error(artifact):
        return _artifact_refusal("invalid_request", error)

    # Validate current facts or a reusable snapshot before identity is trusted.
    requests = artifact["requests"]
    source = "snapshot" if "snapshot" in artifact else "context"
    supplied = deepcopy(artifact[source])
    if error := _snapshot_structure_error(supplied, source):
        return _artifact_refusal("invalid_snapshot", error)

    # Freeze live caller-derived context once or preserve a supplied snapshot.
    snapshot = freeze_context(supplied) if source == "context" else supplied
    snapshot.setdefault("snapshot_identity", _snapshot_identity(snapshot))
    if error := _snapshot_error(snapshot):
        decisions = [
            _refused(request, snapshot, "invalid_snapshot", error)
            for request in requests
        ]
    else:
        # Preserve request order while isolating each request-level refusal.
        decisions = [
            _refused(request, snapshot, "invalid_request", error)
            if (error := _request_error(request))
            else _decision(request, snapshot)
            for request in requests
        ]

    return {"schema_version": 1, "snapshot": snapshot, "decisions": decisions}


def _recommendation_banner(decision: dict[str, Any]) -> dict[str, Any]:
    """Translate the shared evidence class into the human status banner."""

    evidence_class = decision.get("evidence_class", "heuristic")
    banners = {
        "heuristic": ("🔵 HEURISTISK STARTPUNKT", "low", False),
        "mixed": ("🟠 BLANDAD EVIDENS", "medium", False),
        "measurement_based": (
            "🟢 MÄTDATABASERAD REKOMMENDATION",
            "high",
            True,
        ),
    }
    text, confidence, is_production = banners[evidence_class]
    return {
        "class": evidence_class,
        "text": text,
        "confidence": confidence,
        "production_recommendation": is_production,
    }


def _recommendation_uncertainty(
    decision: dict[str, Any], snapshot: dict[str, Any]
) -> dict[str, Any]:
    """Expose recorded uncertainty for the selected fingerprint or honest unknowns."""

    if decision["status"] != "selected":
        return {"status": "unknown", "reason": decision["status"]}
    fingerprint = decision["launch"]["configuration_fingerprint"]
    records = [
        record
        for record in snapshot["evidence"]["records"]
        if record.get("configuration_fingerprint") == fingerprint
        and isinstance(record.get("uncertainty"), dict)
    ]
    if not records:
        return {
            "status": "unknown",
            "reason": "representative exact-point uncertainty is missing",
        }
    return {"status": "measured", **deepcopy(records[0]["uncertainty"])}


def _experiment_fingerprints(
    decision: dict[str, Any], snapshot: dict[str, Any]
) -> list[str]:
    """Freeze the selected point and its nearest launchable control neighbor."""

    launch = decision["launch"]
    fingerprints = [launch["configuration_fingerprint"]]
    adjacent_index = PORTABLE_LEVELS.index(launch["portable_deliberation"]) + 1
    if adjacent_index >= len(PORTABLE_LEVELS):
        return fingerprints
    adjacent = PORTABLE_LEVELS[adjacent_index]
    points = [
        point
        for point in snapshot["mappings"]
        if point["model"] == launch["model"]
        and point["channel"] == launch["channel"]
        and point["surface"] == launch["surface"]
        and point["serving_mode"] == launch["serving_mode"]
        and point["tools"] == launch["tools"]
        and point["policy"] == launch["policy"]
        and adjacent in point["controls"]
    ]
    if not points or not _within_main_seat(points[0], adjacent, snapshot):
        return fingerprints
    native = points[0]["controls"][adjacent]
    adapter = _launch_adapter(points[0], native, snapshot)
    if adapter is not None:
        fingerprints.append(
            _variant_fingerprint(points[0], adjacent, native, adapter, snapshot)
        )
    return fingerprints


def _experiment_brief(
    request: dict[str, Any], decision: dict[str, Any], snapshot: dict[str, Any]
) -> dict[str, Any] | None:
    """Build the detailed human evidence path without executing an experiment."""

    if (
        decision["status"] != "selected"
        or decision.get("evidence_class") == "measurement_based"
    ):
        return None

    # Freeze inputs, controls, measurements, and bounds for both plans.
    fingerprint = decision["launch"]["configuration_fingerprint"]
    return {
        "workload": request["workload"],
        "workload_cohort": request.get("workload_cohort"),
        "quality_floor": snapshot["override_policy"].get("quality_floor"),
        "checker": deepcopy(request["checker"]),
        "configuration_fingerprints": _experiment_fingerprints(decision, snapshot),
        "measurements": [
            "quality",
            "cash",
            "rolling_quota",
            "weekly_quota",
            "allocated_subscription_cost",
            "latency",
            "failure",
            "retry",
            "provenance",
        ],
        "run_bound": 2 if request.get("retry_available") else 1,
        "stopping_rule": "Stop when the conservative quality bound clears the floor or the run bound is spent.",
        "sequential_plan": "Run the selected point, then only its permitted adjacent escalation after checker-confirmed failure.",
        "parallel_plan": "Run isolated adjacent points against the same frozen workload and checker when the caller grants parallel capacity.",
        "observation_artifact": {
            "configuration_fingerprint": fingerprint,
            "unavailable_values": None,
        },
    }


def recommend(artifact: Any) -> dict[str, Any]:
    """Adapt shared routing decisions into the detailed human recommendation form."""

    # Resolve once through the same deep module used by compact routing callers.
    resolved = route(artifact)
    if "artifact_refusal" in resolved:
        return {
            "schema_version": resolved["schema_version"],
            "snapshot": resolved["snapshot"],
            "recommendations": [],
            "artifact_refusal": resolved["artifact_refusal"],
        }

    requests = artifact.get("requests", [])
    recommendations = []
    for request, decision in zip(requests, resolved["decisions"], strict=True):
        selected_fingerprint = (
            decision["launch"]["configuration_fingerprint"]
            if decision["status"] == "selected"
            else None
        )
        neighbors = [
            entry
            for entry in decision["audit"].get("frontier", [])
            if entry["configuration_fingerprint"] != selected_fingerprint
        ]
        recommendations.append(
            {
                "request_id": decision["request_id"],
                "decision": deepcopy(decision),
                "evidence_banner": _recommendation_banner(decision),
                "frontier_neighbors": deepcopy(neighbors),
                "uncertainty": _recommendation_uncertainty(
                    decision, resolved["snapshot"]
                ),
                "experiment_brief": _experiment_brief(
                    request, decision, resolved["snapshot"]
                ),
            }
        )
    return {
        "schema_version": resolved["schema_version"],
        "snapshot": resolved["snapshot"],
        "recommendations": recommendations,
    }


def main(argv: list[str] | None = None) -> int:
    """Read one artifact path and emit only its compact JSON response."""

    # Keep every CLI failure on the same machine-readable stdout seam.
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        response = _artifact_refusal(
            "invalid_arguments", "Route accepts exactly one artifact path."
        )
    else:
        try:
            content = Path(arguments[0]).read_text(encoding="utf-8")
        except OSError as error:
            response = _artifact_refusal("unreadable_artifact", str(error))
        else:
            try:
                artifact = json.loads(content)
            except json.JSONDecodeError as error:
                response = _artifact_refusal("malformed_json", str(error))
            else:
                response = route(artifact)
    print(json.dumps(response, sort_keys=True, separators=(",", ":")))
    return 2 if "artifact_refusal" in response else 0


if __name__ == "__main__":
    raise SystemExit(main())
