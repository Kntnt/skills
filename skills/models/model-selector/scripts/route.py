# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Resolve versioned model routing artifacts without external side effects."""

from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
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

    # Resolve local references and composition before inspecting concrete keywords.
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


def _snapshot_error(snapshot: Any) -> str | None:
    """Return the first nested snapshot contract violation, if one exists."""

    # Treat the shipped JSON Schema as the structural runtime authority.
    errors = _schema_errors(
        snapshot,
        REQUEST_SCHEMA["$defs"]["snapshot"],
        REQUEST_SCHEMA,
        "snapshot",
    )
    if errors:
        return errors[0]

    # JSON Schema establishes the nested types used by the semantic checks below.
    assert isinstance(snapshot, dict)

    # Validate cross-field mapping invariants JSON Schema cannot express.
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
            return "snapshot.mappings must freeze max as the highest verified native control"

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


def _launchable_variants(
    point: dict[str, Any],
    snapshot: dict[str, Any],
    portable_lock: str | None = None,
) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    """Expand one configured mapping into complete launchable point variants."""

    variants: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for portable, native in point["controls"].items():
        if portable_lock is not None and portable != portable_lock:
            continue
        if not _within_main_seat(point, portable, snapshot):
            continue
        adapter = _launch_adapter(point, native, snapshot)
        if adapter is not None:
            variants.append((portable, native, adapter))
    return variants


def _selection_exclusions(
    request: dict[str, Any], snapshot: dict[str, Any]
) -> list[dict[str, Any]]:
    """Explain each configured exact point removed by a routing hard filter."""

    overrides = request["overrides"]
    portable_lock = overrides.get("deliberation")
    exclusions: list[dict[str, Any]] = []
    for point in snapshot["mappings"]:
        if not point["enabled"]:
            exclusions.append(
                {
                    "code": "disabled_point",
                    "detail": "The configured point is not enabled.",
                    "model": point["model"],
                }
            )
            continue
        if "model" in overrides and not (
            point["model"] == overrides["model"]
            or overrides["model"] in point["aliases"]
        ):
            exclusions.append(
                {
                    "code": "model_override_mismatch",
                    "detail": "The point does not match the locked model dimension.",
                    "model": point["model"],
                }
            )
            continue
        if portable_lock is not None and portable_lock not in point["controls"]:
            exclusions.append(
                {
                    "code": "mapping_unavailable",
                    "detail": "The exact portable control has no verified native mapping.",
                    "model": point["model"],
                    "portable_deliberation": portable_lock,
                }
            )
            continue

        # Audit only the locked variant or every automatic variant in scale order.
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
            if not _within_main_seat(point, portable, snapshot):
                exclusions.append(
                    {
                        "code": "above_main_seat_ceiling",
                        "detail": "The complete point exceeds the frozen main seat.",
                        "model": point["model"],
                        "portable_deliberation": portable,
                    }
                )
            elif _launch_adapter(point, native, snapshot) is None:
                exclusions.append(
                    {
                        "code": "adapter_unreachable",
                        "detail": "No active adapter can launch every field of this point.",
                        "model": point["model"],
                        "portable_deliberation": portable,
                    }
                )
    return exclusions


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
    candidate: tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]],
    record: dict[str, Any],
    other_candidate: tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]],
    other_record: dict[str, Any],
) -> bool:
    """Apply multidimensional dominance only when every compared fact is known."""

    costs = candidate[0]["commercial"]
    other_costs = other_candidate[0]["commercial"]
    if any(
        not _is_number(costs[dimension]) or not _is_number(other_costs[dimension])
        for dimension in COMMERCIAL_DIMENSIONS
    ):
        return False

    # Require no worse conservative quality and no worse value on every cost axis.
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
    measured: list[
        tuple[
            tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]],
            dict[str, Any],
        ]
    ],
) -> list[
    tuple[
        tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]],
        dict[str, Any],
    ]
]:
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
    candidate: tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]],
    shadow_prices: dict[str, Any],
) -> float | None:
    """Calculate a scenario cost only from a complete explicit conversion policy."""

    commercial = candidate[0]["commercial"]
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
    return float(commercial["cash"]) + sum(
        float(commercial[dimension]) * float(shadow_prices[dimension])
        for dimension in priced_dimensions
    )


def _frontier_audit(
    frontier: list[
        tuple[
            tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]],
            dict[str, Any],
        ]
    ],
    snapshot: dict[str, Any],
) -> list[dict[str, Any]]:
    """Expose the exact non-dominated alternatives without collapsing their costs."""

    return [
        {
            "configuration_fingerprint": _variant_fingerprint(*candidate, snapshot),
            "model": candidate[0]["model"],
            "portable_deliberation": candidate[1],
            "quality_lower_bound": _quality_lower_bound(record),
            "commercial": deepcopy(candidate[0]["commercial"]),
        }
        for candidate, record in frontier
    ]


def _selected(request: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    """Select the weakest launchable point allowed by explicit dimensions."""

    overrides = request.get("overrides", {})
    deliberation = overrides.get("deliberation")
    points = [
        point
        for point in snapshot["mappings"]
        if point["enabled"]
        and (
            "model" not in overrides
            or point["model"] == overrides["model"]
            or overrides["model"] in point.get("aliases", [])
        )
        and (deliberation is None or deliberation in point["controls"])
    ]
    candidates = [
        (point, portable, native, adapter)
        for point in points
        for portable, native, adapter in _launchable_variants(
            point, snapshot, deliberation
        )
    ]
    records = snapshot["evidence"]["records"]
    measured = [
        (candidate, record)
        for candidate in candidates
        for record in records
        if _evidence_is_measurement(
            record,
            request,
            candidate[0],
            candidate[1],
            candidate[2],
            _variant_fingerprint(*candidate, snapshot),
            snapshot,
        )
    ]
    decision_policy = "cold_start"
    frontier_audit: list[dict[str, Any]] = []
    if measured:
        frontier = _pareto_frontier(measured)
        frontier_audit = _frontier_audit(frontier, snapshot)
        if len(frontier) == 1:
            eligible = [frontier[0][0]]
            decision_policy = "pareto_dominance"
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
    else:
        eligible = candidates
        decision_policy = (
            "cold_start_strongest"
            if not request["reversible"] and request["checker"]["kind"] == "none"
            else "cold_start_weakest"
        )
    choose = max if decision_policy == "cold_start_strongest" else min
    point, portable, native, adapter = choose(
        eligible,
        key=lambda candidate: (
            _model_capability(candidate[0]),
            _control_capability(candidate[0], candidate[1]),
            PORTABLE_LEVELS.index(candidate[1]),
        ),
    )
    arguments = _launch_arguments(adapter, point, native, snapshot)
    fingerprint = _variant_fingerprint(
        point,
        portable,
        native,
        adapter,
        snapshot,
    )

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
    exclusions = _selection_exclusions(request, snapshot)

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
        "exclusions": deepcopy(exclusions),
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

    if request.get("authority") not in {"execution", "verdict"}:
        return _refused(request, snapshot, "invalid_request")
    if request["authority"] == "verdict":
        if not snapshot["harness"].get("inheritance"):
            return _refused(request, snapshot, "unrepresentable_verdict_inheritance")
        return _inherit(request, snapshot, "verdict_authority")
    if snapshot.get("profile") is None:
        return _inherit(request, snapshot, "missing_profile")
    if not snapshot["profile"].get("valid"):
        return _refused(request, snapshot, "invalid_profile")
    if (
        snapshot["main_seat"].get("model_capability") is None
        or snapshot["main_seat"].get("deliberation_capability") is None
    ):
        return _refused(request, snapshot, "unknown_main_seat_ceiling")

    overrides = request.get("overrides", {})
    if set(overrides) - {"model", "deliberation"}:
        return _refused(request, snapshot, "invalid_request")
    deliberation = overrides.get("deliberation")
    if deliberation is not None and deliberation not in PORTABLE_LEVELS:
        return _refused(request, snapshot, "invalid_request")

    model_matches = [
        point
        for point in snapshot["mappings"]
        if point["enabled"]
        and (
            "model" not in overrides
            or point["model"] == overrides["model"]
            or overrides["model"] in point["aliases"]
        )
    ]
    if overrides.get("model") and not model_matches:
        return _refused(request, snapshot, "unavailable_override")
    exact_models = {
        point["model"]
        for point in model_matches
        if point["model"] == overrides.get("model")
    }
    resolved_models = {point["model"] for point in model_matches}
    if overrides.get("model") and not exact_models and len(resolved_models) > 1:
        return _refused(request, snapshot, "ambiguous_override")
    if deliberation and not any(
        deliberation in point["controls"] for point in model_matches
    ):
        return _refused(request, snapshot, "unavailable_override")
    if overrides.get("model") and all(
        not any(
            _within_main_seat(point, portable, snapshot)
            for portable in point["controls"]
            if deliberation is None or portable == deliberation
        )
        for point in model_matches
    ):
        return _refused(request, snapshot, "above_main_seat_ceiling")
    if deliberation and all(
        not _within_main_seat(point, deliberation, snapshot)
        for point in model_matches
        if deliberation in point["controls"]
    ):
        return _refused(request, snapshot, "above_main_seat_ceiling")

    safe = [
        point
        for point in model_matches
        if (deliberation is None or deliberation in point["controls"])
        and _launchable_variants(point, snapshot, deliberation)
    ]
    if not safe:
        exclusions = _selection_exclusions(request, snapshot)
        return _refused(
            request,
            snapshot,
            "empty_safe_candidate_set",
            "No configured point remains after complete Harness filtering.",
            exclusions,
        )
    if (
        not snapshot["evidence"].get("records")
        and not overrides
        and snapshot["override_policy"].get("cold_start") != "select"
    ):
        return _inherit(request, snapshot, "insufficient_evidence")
    return _selected(request, snapshot)


def route(artifact: Any) -> dict[str, Any]:
    """Return ordered decisions and the exact snapshot used to derive them."""

    # Refuse malformed envelopes once, before any request is interpreted.
    if error := _artifact_error(artifact):
        return _artifact_refusal("invalid_request", error)

    requests = artifact.get("requests", [])
    snapshot = deepcopy(artifact.get("snapshot", artifact.get("context", {})))
    snapshot.setdefault("snapshot_identity", _snapshot_identity(snapshot))
    if error := _snapshot_error(snapshot):
        decisions = [
            _refused(request, snapshot, "invalid_snapshot", error)
            for request in requests
        ]
    else:
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

    # Freeze inputs, controls, measurements, and bounds for either execution plan.
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
