# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Resolve versioned model routing artifacts without external side effects."""

import hashlib
import json
import math
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

# The one launch destination that names no flag: a native control the active
# Harness applies to a spawned subagent from the session it inherits from.
CARRIED_DESTINATION: dict[str, str] = {"carried_by": "inheritance"}

# Share the inheritance states that require further evidence work.
EVIDENCE_INHERITANCE_REASONS: frozenset[str] = frozenset(
    {
        "insufficient_evidence",
        "underdetermined_frontier",
        "quality_floor_not_cleared",
    }
)
REQUEST_SCHEMA_PATH: Path = (
    Path(__file__).resolve().parent.parent / "references" / "route-request.schema.json"
)
RESPONSE_SCHEMA_PATH: Path = (
    Path(__file__).resolve().parent.parent / "references" / "route-response.schema.json"
)
REQUEST_SCHEMA: dict[str, Any] = json.loads(
    REQUEST_SCHEMA_PATH.read_text(encoding="utf-8")
)
RESPONSE_SCHEMA: dict[str, Any] = json.loads(
    RESPONSE_SCHEMA_PATH.read_text(encoding="utf-8")
)
SCHEMAS_BY_ID: dict[str, dict[str, Any]] = {
    REQUEST_SCHEMA["$id"]: REQUEST_SCHEMA,
    RESPONSE_SCHEMA["$id"]: RESPONSE_SCHEMA,
}


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


@dataclass(frozen=True, slots=True)
class EvidencePool:
    """Partition candidates by exact representative evidence coverage."""

    measured: tuple[tuple[Candidate, dict[str, Any]], ...]
    unknown: tuple[Candidate, ...]
    below_floor: tuple[Candidate, ...]


@dataclass(frozen=True, slots=True)
class SelectionOutcome:
    """Carry one resolved candidate and the policy facts that selected it."""

    candidate: Candidate
    decision_policy: str
    frontier: tuple[dict[str, Any], ...]
    exclusions: tuple[dict[str, Any], ...]


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


def _resolve_schema_reference(
    reference: str,
    root: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve a JSON Pointer across the shipped request and response schemas."""

    # Select the current root for local pointers or the named shipped schema.
    if reference.startswith("#"):
        resolved_root = root
        pointer = reference
    else:
        identifier, _, fragment = reference.partition("#")
        resolved_root = SCHEMAS_BY_ID[identifier]
        pointer = f"#{fragment}"

    # Walk the escaped JSON Pointer tokens against the resolved schema root.
    value: Any = resolved_root
    for token in pointer.removeprefix("#/").split("/"):
        value = value[token.replace("~1", "/").replace("~0", "~")]
    return cast(dict[str, Any], value), resolved_root


def _schema_errors(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
    path: str,
) -> list[str]:
    """Validate the JSON Schema keywords used by the public routing contract."""

    # Resolve references and composition before inspecting concrete keywords.
    if "$ref" in schema:
        resolved, resolved_root = _resolve_schema_reference(schema["$ref"], root)
        return _schema_errors(
            value,
            resolved,
            resolved_root,
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
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path} has too many items")
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

    return (isinstance(value, int) and not isinstance(value, bool)) or (
        isinstance(value, float) and math.isfinite(value)
    )


def _canonical_digest(value: Any) -> str:
    """Hash one JSON value through the module's canonical encoding."""

    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _snapshot_identity(snapshot: dict[str, Any]) -> str:
    """Hash canonical frozen routing facts without recursively hashing the digest."""

    canonical = deepcopy(snapshot)
    canonical.pop("snapshot_identity", None)
    return _canonical_digest(canonical)


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
    return _canonical_digest(value)


def _is_carried(destination: Any) -> bool:
    """Recognize the destination that names inheritance rather than a flag."""

    return bool(destination == CARRIED_DESTINATION)


def _destination_key(destination: Any) -> str | None:
    """Return the native argument key emitted by one destination."""

    if isinstance(destination, str):
        return destination
    if isinstance(destination, dict) and isinstance(destination.get("parameter"), str):
        return cast(str, destination["parameter"])
    return None


def _destination_value(destination: Any, value: Any) -> Any:
    """Render a parameter destination's value without changing exact facts."""

    if isinstance(destination, dict) and isinstance(destination.get("value"), str):
        return cast(str, destination["value"]).replace("{value}", str(value))
    return deepcopy(value)


def _destination_accepts(destination: Any, value: Any) -> bool:
    """Require a valid destination whose fixed value matches the point."""

    if _destination_key(destination) is not None or _is_carried(destination):
        return True
    return bool(isinstance(destination, dict) and destination.get("fixed") == value)


def _launch_destinations(adapter: dict[str, Any]) -> tuple[Any, ...]:
    """Collect every scalar and mapped destination declared by an adapter."""

    launch = adapter.get("launch", {})
    native = launch.get("native_control_flags", {})
    policy = launch.get("policy_flags", {})
    return (
        launch.get("model_flag"),
        launch.get("surface_flag"),
        launch.get("serving_mode_flag"),
        launch.get("tools_flag"),
        *(native.values() if isinstance(native, dict) else ()),
        *(policy.values() if isinstance(policy, dict) else ()),
    )


def _carries_control(adapter: dict[str, Any]) -> bool:
    """Answer whether one adapter leaves a native control to inheritance."""

    return any(
        _is_carried(destination)
        for destination in adapter["launch"]["native_control_flags"].values()
    )


def _carries_launch_value(adapter: dict[str, Any]) -> bool:
    """Answer whether any complete-point fact is carried by inheritance."""

    return any(
        _is_carried(destination) for destination in _launch_destinations(adapter)
    )


def _attests_inheritance(adapter: dict[str, Any]) -> bool:
    """Require the declaring session's attestation for a carried control.

    The shipped schema validates the attestation wherever one is present, so
    a carried mapping declared without one is a claim about the Harness that
    nobody verified, and the adapter cannot launch anything.
    """

    return "inheritance_attestation" in adapter


def _launch_destinations_are_unique(adapter: dict[str, Any]) -> bool:
    """Prevent complete-point fields from overwriting one launch argument."""

    # Compare only emitted parameters; fixed and carried facts emit nothing.
    keys = [
        key
        for destination in _launch_destinations(adapter)
        if (key := _destination_key(destination)) is not None
    ]
    return len(keys) == len(set(keys))


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

    # Admit carried destinations only where the session attested the Harness.
    if _carries_launch_value(adapter) and not _attests_inheritance(adapter):
        return False

    # Require a complete translation for every launch-relevant point field.
    launch = adapter.get("launch", {})
    native_flags = launch.get("native_control_flags", {})
    policy_flags = launch.get("policy_flags", {})
    return (
        _destination_accepts(launch.get("model_flag"), point["model"])
        and _destination_accepts(
            launch.get("surface_flag"),
            point.get("surface", snapshot["harness"]["surface"]),
        )
        and _destination_accepts(launch.get("serving_mode_flag"), point["serving_mode"])
        and _destination_accepts(launch.get("tools_flag"), point.get("tools", []))
        and isinstance(native_flags, dict)
        and set(native) <= set(native_flags)
        and all(
            _destination_accepts(native_flags[field], value)
            for field, value in native.items()
        )
        and isinstance(policy_flags, dict)
        and set(point.get("policy", {})) <= set(policy_flags)
        and all(
            _destination_accepts(policy_flags[field], value)
            for field, value in point.get("policy", {}).items()
        )
        and _launch_destinations_are_unique(adapter)
    )


def _launch_adapter(
    point: dict[str, Any],
    native: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any] | None:
    """Resolve the first deterministic adapter that addresses an exact point."""

    compatible = [
        adapter
        for adapter in snapshot["harness"]["adapter_specs"]
        if not _carries_control(adapter)
        and _adapter_can_launch(adapter, point, native, snapshot)
    ]
    return min(compatible, key=lambda adapter: adapter["adapter_id"], default=None)


def _carried_adapter(
    point: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any] | None:
    """Resolve the adapter that launches a point at the seat's own control.

    A carried control is not a dimension this module selects over, so such an
    adapter is reachable only at the frozen main seat's exact native value and
    never through the portable expansion an addressable adapter is matched by.
    """

    native = snapshot["main_seat"]["native_deliberation"]
    compatible = [
        adapter
        for adapter in snapshot["harness"]["adapter_specs"]
        if _carries_control(adapter)
        and _adapter_can_launch(adapter, point, native, snapshot)
    ]
    return min(compatible, key=lambda adapter: adapter["adapter_id"], default=None)


def _launch_arguments(
    adapter: dict[str, Any],
    point: dict[str, Any],
    native: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Translate one complete point into Harness-native launch arguments."""

    # Pair every exact-point value with its declared launch destination.
    launch = adapter["launch"]
    destinations = [
        (launch["model_flag"], point["model"]),
        (
            launch["surface_flag"],
            point.get("surface", snapshot["harness"]["surface"]),
        ),
        (launch["serving_mode_flag"], point["serving_mode"]),
        (launch["tools_flag"], point.get("tools", [])),
        *(
            (launch["native_control_flags"][field], value)
            for field, value in native.items()
        ),
        *(
            (launch["policy_flags"][field], value)
            for field, value in point.get("policy", {}).items()
        ),
    ]

    # Emit parameter destinations only, rendering an optional value template.
    arguments: dict[str, Any] = {}
    for destination, value in destinations:
        if (key := _destination_key(destination)) is not None:
            arguments[key] = _destination_value(destination, value)
    return arguments


def _model_capability(point: dict[str, Any]) -> float:
    """Resolve the model dimension of the frozen authority ceiling."""

    return float(point["model_capability"])


def _control_capability(point: dict[str, Any], portable: str) -> float:
    """Resolve deliberation capability without treating it as measured quality."""

    return float(point["control_capabilities"][portable])


def _model_within_main_seat(point: dict[str, Any], snapshot: dict[str, Any]) -> bool:
    """Apply the frozen model dimension of the authority ceiling on its own.

    A carried deliberation control launches at the seat's own value, so the
    model is the only dimension such a point can exceed the ceiling in.
    """

    model_ceiling = snapshot["main_seat"]["model_capability"]
    return model_ceiling is not None and _model_capability(point) <= float(
        model_ceiling
    )


def _candidate_control_capability(
    candidate: Candidate, snapshot: dict[str, Any]
) -> float:
    """Read the deliberation authority one candidate actually launches under."""

    if _carries_control(candidate.adapter):
        return float(snapshot["main_seat"]["deliberation_capability"])
    return _control_capability(candidate.point, candidate.portable)


def _within_main_seat(
    point: dict[str, Any], portable: str, snapshot: dict[str, Any]
) -> bool:
    """Apply both frozen model and deliberation authority ceilings."""

    deliberation_ceiling = snapshot["main_seat"]["deliberation_capability"]
    if deliberation_ceiling is None:
        return False
    return _model_within_main_seat(point, snapshot) and _control_capability(
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

        # Retain incomparable selections in the snapshot but never rank them.
        if point["model_capability"] is None:
            exclusions.append(
                _exclusion(
                    "capability_rank_unavailable",
                    "No shared benchmark ranks this model against the main seat.",
                    point,
                )
            )
            variant_exclusion_codes.append("capability_rank_unavailable")
            continue

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

        # Refuse to let a request lock a dimension inheritance decides.
        carried = _carried_adapter(point, snapshot)
        if carried is not None and portable_lock is not None:
            exclusions.append(
                _exclusion(
                    "carried_control_not_selectable",
                    "The active Harness carries this deliberation control by "
                    "inheritance.",
                    point,
                    portable_lock,
                )
            )
            variant_exclusion_codes.append("carried_control_not_selectable")
            continue

        # Resolve a carried control from the frozen main seat rather than
        # expanding a dimension this seam cannot address.
        if carried is not None:
            main_seat = snapshot["main_seat"]
            carried_portable = cast(str, main_seat["portable_deliberation"])
            if not _model_within_main_seat(point, snapshot):
                exclusions.append(
                    _exclusion(
                        "above_main_seat_ceiling",
                        "The complete point exceeds the frozen main seat.",
                        point,
                        carried_portable,
                    )
                )
                variant_exclusion_codes.append("above_main_seat_ceiling")
                continue
            candidates.append(
                Candidate(
                    point,
                    carried_portable,
                    main_seat["native_deliberation"],
                    carried,
                )
            )
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


def _evidence_is_applicable(
    record: dict[str, Any],
    request: dict[str, Any],
    point: dict[str, Any],
    portable: str,
    native: dict[str, Any],
    fingerprint: str,
    snapshot: dict[str, Any],
) -> bool:
    """Require exact representative applicability and bounded uncertainty."""

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

    # Keep unknown or weak decision support out of exact evidence coverage.
    coverage = record.get("coverage")
    uncertainty = record.get("uncertainty")
    return (
        record.get("representative") is True
        and isinstance(coverage, dict)
        and coverage.get("decision_relevant") is True
        and isinstance(uncertainty, dict)
        and _is_number(uncertainty.get("lower_bound"))
        and _is_number(uncertainty.get("upper_bound"))
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
    """Require applicable exact evidence that clears the frozen quality floor."""

    # Combine exact applicability with the independent conservative floor.
    return _evidence_is_applicable(
        record,
        request,
        point,
        portable,
        native,
        fingerprint,
        snapshot,
    ) and _evidence_clears_quality_floor(record, snapshot)


def _evidence_clears_quality_floor(
    record: dict[str, Any],
    snapshot: dict[str, Any],
) -> bool:
    """Compare one bounded record with the frozen conservative quality floor."""

    # Preserve unknown bounds rather than coercing them into passing values.
    uncertainty = record.get("uncertainty")
    quality_floor = snapshot["override_policy"].get("quality_floor")
    return (
        isinstance(uncertainty, dict)
        and _is_number(uncertainty.get("lower_bound"))
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


def _candidate_evidence(
    candidates: tuple[Candidate, ...],
    records: list[dict[str, Any]],
    request: dict[str, Any],
    snapshot: dict[str, Any],
) -> EvidencePool:
    """Partition candidates without treating missing evidence as dominance."""

    # Collect one strongest conservative exact record per candidate.
    measured: list[tuple[Candidate, dict[str, Any]]] = []
    unknown: list[Candidate] = []
    below_floor: list[Candidate] = []
    for candidate in candidates:
        # Distinguish exact failing evidence from an entirely unknown point.
        fingerprint = _candidate_fingerprint(candidate, snapshot)
        applicable = [
            record
            for record in records
            if _evidence_is_applicable(
                record,
                request,
                candidate.point,
                candidate.portable,
                candidate.native,
                fingerprint,
                snapshot,
            )
        ]
        qualifying = [
            record
            for record in applicable
            if _evidence_clears_quality_floor(record, snapshot)
        ]
        if qualifying:
            measured.append((candidate, max(qualifying, key=_quality_lower_bound)))
        elif applicable:
            below_floor.append(candidate)
        else:
            unknown.append(candidate)

    # Freeze the evidence partition for deterministic selection and audit.
    return EvidencePool(tuple(measured), tuple(unknown), tuple(below_floor))


def _evidence_exclusions(
    evidence: EvidencePool,
    include_unknown: bool,
) -> list[dict[str, Any]]:
    """Expose unknown and known-failing exact points as stable audit facts."""

    # Preserve candidate identity without disclosing repeated launch arguments.
    below_floor = [
        _exclusion(
            "quality_floor_not_cleared",
            "Exact representative evidence does not clear the quality floor.",
            candidate.point,
            candidate.portable,
        )
        for candidate in evidence.below_floor
    ]
    unknown = [
        _exclusion(
            "missing_exact_evidence",
            "No exact representative evidence covers this candidate.",
            candidate.point,
            candidate.portable,
        )
        for candidate in evidence.unknown
    ]
    return below_floor + (unknown if include_unknown else [])


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


def _resolve_measured_policy(
    request: dict[str, Any],
    snapshot: dict[str, Any],
    measured: list[tuple[Candidate, dict[str, Any]]],
    exclusions: list[dict[str, Any]],
) -> SelectionOutcome | dict[str, Any]:
    """Resolve exact measurements through human economics or Pareto policy."""

    # Build the honest multidimensional frontier once for every measured policy.
    frontier = _pareto_frontier(measured)
    frontier_audit = _frontier_audit(frontier, snapshot)
    audit = {
        "frontier": frontier_audit,
        "exclusions": deepcopy(exclusions),
    }
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
                audit,
            )
        candidate = winner

    # Accept a frontier containing exactly one non-dominated point.
    elif len(frontier) == 1:
        candidate = frontier[0][0]
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
                audit,
            )
        minimum = min(float(cost) for cost, _ in priced if cost is not None)
        winners = [
            item for cost, item in priced if cost is not None and float(cost) == minimum
        ]
        if len(winners) != 1:
            return _inherit(
                request,
                snapshot,
                "underdetermined_frontier",
                audit,
            )
        candidate = winners[0][0]
        decision_policy = "explicit_shadow_prices"

    # Preserve the measured frontier and filtering facts with the chosen point.
    return SelectionOutcome(
        candidate,
        decision_policy,
        tuple(frontier_audit),
        tuple(deepcopy(exclusions)),
    )


def _resolve_selection_policy(
    request: dict[str, Any],
    snapshot: dict[str, Any],
    evidence_pool: EvidencePool,
    exclusions: list[dict[str, Any]],
) -> SelectionOutcome | dict[str, Any]:
    """Resolve evidence state into one candidate or honest inheritance."""

    # Never let measured points dominate candidates whose evidence is unknown.
    measured = list(evidence_pool.measured)
    if measured and evidence_pool.unknown:
        frontier = _pareto_frontier(measured)
        return _inherit(
            request,
            snapshot,
            "insufficient_evidence",
            {
                "frontier": _frontier_audit(frontier, snapshot),
                "exclusions": deepcopy(exclusions),
            },
        )

    # Resolve measured alternatives through explicit economics or Pareto policy.
    if measured:
        return _resolve_measured_policy(request, snapshot, measured, exclusions)

    # Refuse to treat a heuristic point as measured economic evidence.
    if "economics" in request:
        return _inherit(
            request,
            snapshot,
            "insufficient_evidence",
            {"exclusions": deepcopy(exclusions)},
        )

    # Inherit when every candidate has exact evidence below the quality floor.
    if not evidence_pool.unknown:
        return _inherit(
            request,
            snapshot,
            "quality_floor_not_cleared",
            {"exclusions": deepcopy(exclusions)},
        )

    # Choose the workload-safe cold-start endpoint when measurements are absent.
    decision_policy = (
        "cold_start_strongest"
        if not request["reversible"] and request["checker"]["kind"] == "none"
        else "cold_start_weakest"
    )

    # Choose the weakest or strongest complete candidate required by the policy.
    choose = max if decision_policy == "cold_start_strongest" else min
    candidate = choose(
        evidence_pool.unknown,
        key=lambda item: (
            _model_capability(item.point),
            _candidate_control_capability(item, snapshot),
            PORTABLE_LEVELS.index(item.portable),
        ),
    )
    return SelectionOutcome(
        candidate,
        decision_policy,
        (),
        tuple(deepcopy(exclusions)),
    )


def _selected_decision(
    request: dict[str, Any],
    snapshot: dict[str, Any],
    records: list[dict[str, Any]],
    selection: SelectionOutcome,
) -> dict[str, Any]:
    """Serialize one resolved candidate as the complete selected result."""

    # Translate and fingerprint the candidate selected by shared policy.
    candidate = selection.candidate
    point = candidate.point
    portable = candidate.portable
    native = candidate.native
    adapter = candidate.adapter
    arguments = _launch_arguments(adapter, point, native, snapshot)
    fingerprint = _candidate_fingerprint(candidate, snapshot)

    # Classify the exact winner from the same frozen evidence facts.
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

    # Expose the complete launch, provenance, escalation, and audit contract.
    exclusions = deepcopy(list(selection.exclusions))
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
            candidate,
            snapshot,
            fingerprint,
        ),
        "audit": _audit(
            snapshot,
            {
                "decision_policy": selection.decision_policy,
                "frontier": deepcopy(list(selection.frontier)),
                "exclusions": deepcopy(exclusions),
            },
        ),
    }


def _selection_decision(
    request: dict[str, Any],
    snapshot: dict[str, Any],
    pool: CandidatePool,
) -> dict[str, Any]:
    """Resolve one selected or underdetermined decision from an eligible pool."""

    # Partition exact evidence once for every candidate and human output form.
    records = snapshot["evidence"]["records"]
    evidence_pool = _candidate_evidence(pool.candidates, records, request, snapshot)
    measured = bool(evidence_pool.measured)
    exclusions = deepcopy(list(pool.exclusions)) + _evidence_exclusions(
        evidence_pool,
        include_unknown=measured,
    )

    # Resolve shared policy before the selected response is serialized.
    outcome = _resolve_selection_policy(
        request,
        snapshot,
        evidence_pool,
        exclusions,
    )
    if isinstance(outcome, dict):
        return outcome

    # Serialize a launch only after policy resolved one complete candidate.
    return _selected_decision(request, snapshot, records, outcome)


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


def _is_objectively_checked(request: dict[str, Any]) -> bool:
    """Recognize reversible work whose failure an independent signal catches."""

    return request["reversible"] and request["checker"]["kind"] in {
        "external",
        "declared",
    }


def _escalation(
    request: dict[str, Any],
    candidate: Candidate,
    snapshot: dict[str, Any],
    fingerprint: str,
) -> dict[str, Any] | None:
    """Describe one existing-retry step only after externally bound failure."""

    # Bind the prior attempt and external failure to the selected exact point.
    point = candidate.point
    portable = candidate.portable
    native = candidate.native
    adapter = candidate.adapter
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
        not _is_objectively_checked(request)
        or request.get("retry_available") is not True
        or not failure
        or failure.get("outcome") != "failed"
        or failure.get("checker") != checker
        or any(prior.get(field) != value for field, value in exact_attempt.items())
        or any(failure.get(field) != value for field, value in exact_attempt.items())
    ):
        return None

    # Move only along a dimension this adapter addresses: a control the
    # Harness carries has no adjacency, the seat alone deciding its value.
    if _carries_control(adapter):
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
    """Resolve one request while keeping explicit locks above inheritance."""

    # Keep every verdict on the exact immutable main seat.
    if request["authority"] == "verdict":
        if not snapshot["harness"].get("inheritance"):
            return _refused(request, snapshot, "unrepresentable_verdict_inheritance")
        return _inherit(request, snapshot, "verdict_authority")

    # Refuse rather than drop a lock that an unparameterized launch cannot carry.
    decision = _execution_decision(request, snapshot)
    if decision["status"] == "inherit" and request["overrides"]:
        reason = decision["inheritance"]["reason"]
        return _refused(
            request,
            snapshot,
            "unavailable_override",
            f"No exact point can carry the explicit override: {reason}.",
            decision["audit"].get("exclusions", []),
        )
    return decision


def _execution_decision(
    request: dict[str, Any], snapshot: dict[str, Any]
) -> dict[str, Any]:
    """Apply hard refusals and inheritance before exact-point selection.

    Every inheritance here answers an automatic dimension. `_decision()` owns
    the field-lock authority and converts one into a refusal whenever the
    request locks a dimension that an inherited launch could not carry.
    """

    # Distinguish absent profile state from invalid persisted state.
    if snapshot.get("profile") is None:
        return _inherit(request, snapshot, "missing_profile")
    if not snapshot["profile"].get("valid"):
        return _refused(request, snapshot, "invalid_profile")

    # Keep missing selection controls on the exact seat for automatic work.
    if (
        not snapshot["mappings"]
        and not request["overrides"]
        and snapshot["harness"].get("inheritance")
    ):
        return _inherit(request, snapshot, "unavailable_selection_controls")

    # Refuse selection when either frozen authority dimension is unknown.
    if (
        snapshot["main_seat"].get("model_capability") is None
        or snapshot["main_seat"].get("deliberation_capability") is None
    ):
        return _refused(request, snapshot, "unknown_main_seat_ceiling")

    # Preserve an explicit lock as a refusal when no point can carry it.
    if not snapshot["mappings"]:
        return _refused(request, snapshot, "unavailable_override")

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

    # Name a lock on a dimension inheritance decides rather than an empty set.
    if not pool.candidates and set(pool.variant_exclusion_codes) == {
        "carried_control_not_selectable"
    }:
        return _refused(
            request,
            snapshot,
            "unavailable_override",
            "The active Harness carries this deliberation control by inheritance.",
            list(pool.exclusions),
        )

    # Preserve automatic fresh-context delegation when controls are unavailable.
    if not pool.candidates:
        if (
            not overrides
            and snapshot["harness"].get("inheritance")
            and pool.variant_exclusion_codes
            and set(pool.variant_exclusion_codes)
            <= {"adapter_unreachable", "capability_rank_unavailable"}
        ):
            return _inherit(
                request,
                snapshot,
                "unavailable_selection_controls",
                {"exclusions": list(pool.exclusions)},
            )

        # Refuse every other empty safe set with the hard-filter audit.
        return _refused(
            request,
            snapshot,
            "empty_safe_candidate_set",
            "No configured point remains after complete Harness filtering.",
            list(pool.exclusions),
        )

    # Honor a frozen policy that declines unmeasured automatic cold starts,
    # except for the reversible objectively checked work whose failure the
    # caller's own checker catches and whose start the contract promises.
    if (
        not snapshot["evidence"].get("records")
        and not overrides
        and snapshot["override_policy"].get("cold_start") != "select"
        and not _is_objectively_checked(request)
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


def _recommendation_evidence_state(
    decision: dict[str, Any],
) -> tuple[str, str, list[str]]:
    """Derive the human evidence class, reason, and missing decision input."""

    # Preserve selected classes and classify unresolved measured states.
    status = decision["status"]
    reason = (
        decision.get("inheritance", {}).get("reason")
        if status == "inherit"
        else decision.get("reason", {}).get("code")
    ) or status
    if status == "selected":
        evidence_class = decision["evidence_class"]
    elif status == "inherit" and (
        decision["audit"].get("frontier")
        or any(
            exclusion["code"] == "quality_floor_not_cleared"
            for exclusion in decision["audit"].get("exclusions", [])
        )
    ):
        evidence_class = "mixed"
    else:
        evidence_class = "heuristic"

    # State why the class applies and what still blocks production selection.
    selected_reasons = {
        "heuristic": "Representative exact-point measurements did not determine the selected point.",
        "mixed": "Relevant evidence exists, but an exact decision-relevant match remains incomplete.",
        "measurement_based": "Representative exact-point evidence determined the selected point and cleared the quality floor.",
    }
    missing_by_reason = {
        "underdetermined_frontier": [
            "an explicit policy that resolves the measured frontier"
        ],
        "insufficient_evidence": [
            "representative exact-point evidence for every launchable candidate"
        ],
        "quality_floor_not_cleared": [
            "exact evidence whose conservative bound clears the quality floor"
        ],
    }
    default_missing = (
        []
        if evidence_class == "measurement_based"
        else ["representative exact-point evidence clearing the quality floor"]
    )
    classification_reason = (
        selected_reasons[evidence_class] if status == "selected" else reason
    )
    missing_evidence = missing_by_reason.get(reason, default_missing)
    return evidence_class, classification_reason, missing_evidence


def _recommendation_presentation(
    status: str,
    evidence_class: str,
) -> tuple[str, str, bool, str]:
    """Resolve accessible banner text and recommendation disposition."""

    # Avoid claiming an exploration start when no point was selected.
    selected_banners = {
        "heuristic": ("🔵 HEURISTISK STARTPUNKT", "low"),
        "mixed": ("🟠 BLANDAD EVIDENS", "medium"),
        "measurement_based": ("🟢 MÄTDATABASERAD REKOMMENDATION", "high"),
    }
    if status == "selected":
        text, confidence = selected_banners[evidence_class]
    elif evidence_class == "mixed":
        text, confidence = "🟠 BLANDAD EVIDENS — INGET EXAKT VAL", "medium"
    else:
        text, confidence = "🔵 INGEN REKOMMENDATION", "low"
    is_production = status == "selected" and evidence_class == "measurement_based"
    recommendation_kind = (
        "production_recommendation"
        if is_production
        else "exploration_start"
        if status == "selected"
        else "no_selection"
    )
    return text, confidence, is_production, recommendation_kind


def _recommendation_banner(decision: dict[str, Any]) -> dict[str, Any]:
    """Translate shared status and evidence facts into an honest human banner."""

    # Resolve evidence meaning independently from accessible presentation.
    status = decision["status"]
    evidence_class, classification_reason, missing_evidence = (
        _recommendation_evidence_state(decision)
    )
    text, confidence, is_production, recommendation_kind = _recommendation_presentation(
        status, evidence_class
    )

    # Emit every accessibility and evidence field promised by human recommend.
    return {
        "class": evidence_class,
        "text": text,
        "confidence": confidence,
        "classification_reason": classification_reason,
        "missing_evidence": missing_evidence,
        "recommendation_kind": recommendation_kind,
        "production_recommendation": is_production,
    }


def _candidate_uncertainty(
    request: dict[str, Any],
    candidate: Candidate,
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Resolve one candidate's uncertainty through exact applicability."""

    # Retain only representative, current, bounded, exact-point evidence.
    fingerprint = _candidate_fingerprint(candidate, snapshot)
    records = [
        record
        for record in snapshot["evidence"]["records"]
        if _evidence_is_applicable(
            record,
            request,
            candidate.point,
            candidate.portable,
            candidate.native,
            fingerprint,
            snapshot,
        )
    ]
    if not records:
        return {
            "configuration_fingerprint": fingerprint,
            "model": candidate.point["model"],
            "portable_deliberation": candidate.portable,
            "status": "unknown",
            "reason": "representative exact-point uncertainty is missing",
        }

    # Report the strongest conservative applicable record deterministically.
    record = max(records, key=_quality_lower_bound)
    return {
        "configuration_fingerprint": fingerprint,
        "model": candidate.point["model"],
        "portable_deliberation": candidate.portable,
        "status": "measured",
        **deepcopy(record["uncertainty"]),
    }


def _recommendation_uncertainty(
    request: dict[str, Any],
    decision: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Retain selected or inherited uncertainty without reviving weak evidence."""

    # Bypass candidate lookup for refusals and non-evidence inheritance.
    inheritance_reason = decision.get("inheritance", {}).get("reason")
    if decision["status"] == "refused" or (
        decision["status"] == "inherit"
        and inheritance_reason not in EVIDENCE_INHERITANCE_REASONS
    ):
        return {"status": "unknown", "reason": decision["status"]}

    # Reuse the shared hard-filtered request candidates for uncertainty.
    candidates = _candidate_pool(request, snapshot).candidates
    if decision["status"] == "selected":
        fingerprint = decision["launch"]["configuration_fingerprint"]
        candidate = next(
            (
                item
                for item in candidates
                if _candidate_fingerprint(item, snapshot) == fingerprint
            ),
            None,
        )
        if candidate is None:
            return {
                "status": "unknown",
                "reason": "selected candidate is unavailable",
            }
        uncertainty = _candidate_uncertainty(request, candidate, snapshot)
        return {
            key: value
            for key, value in uncertainty.items()
            if key in {"status", "reason", "lower_bound", "upper_bound"}
        }

    # Preserve per-frontier intervals for evidence-driven inheritance only.
    frontier = {
        entry["configuration_fingerprint"]
        for entry in decision["audit"].get("frontier", [])
    }
    filter_to_frontier = inheritance_reason == "underdetermined_frontier" and bool(
        frontier
    )
    relevant = [
        candidate
        for candidate in candidates
        if not filter_to_frontier
        or _candidate_fingerprint(candidate, snapshot) in frontier
    ]
    uncertainties = [
        _candidate_uncertainty(request, candidate, snapshot) for candidate in relevant
    ]

    # Summarize complete, partial, or absent applicable intervals honestly.
    measured = sum(item["status"] == "measured" for item in uncertainties)
    status = (
        "measured"
        if uncertainties and measured == len(uncertainties)
        else "mixed"
        if measured
        else "unknown"
    )
    return {
        "status": status,
        "reason": inheritance_reason,
        "candidates": uncertainties,
    }


def _experiment_fingerprints(
    request: dict[str, Any],
    decision: dict[str, Any],
    snapshot: dict[str, Any],
) -> list[str]:
    """Freeze exact comparable points for selected and inherited evidence paths."""

    # Start inherited experiments with their measured frontier and safe pool.
    if decision["status"] != "selected":
        fingerprints = [
            entry["configuration_fingerprint"]
            for entry in decision["audit"].get("frontier", [])
        ]
        for candidate in _candidate_pool(request, snapshot).candidates:
            fingerprint = _candidate_fingerprint(candidate, snapshot)
            if fingerprint not in fingerprints:
                fingerprints.append(fingerprint)
        return fingerprints[:2]

    # Begin a selected experiment with its exact launch point.
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

    # Emit plans only for exploratory selections or evidence-driven inheritance.
    inheritance_reason = decision.get("inheritance", {}).get("reason")
    if (
        decision["status"] == "refused"
        or (
            decision["status"] == "selected"
            and decision.get("evidence_class") == "measurement_based"
        )
        or (
            decision["status"] == "inherit"
            and inheritance_reason not in EVIDENCE_INHERITANCE_REASONS
        )
    ):
        return None

    # Freeze comparable points and derive an explicit checker-backed rubric.
    fingerprints = _experiment_fingerprints(request, decision, snapshot)
    if not fingerprints:
        return None
    rubric = request.get("rubric") or {
        "kind": "checker_outcome",
        "pass_condition": deepcopy(request["checker"]),
    }

    # Freeze inputs, controls, measurements, bounds, and record import form.
    return {
        "workload": request["workload"],
        "workload_cohort": request.get("workload_cohort"),
        "rubric": deepcopy(rubric),
        "quality_floor": snapshot["override_policy"].get("quality_floor"),
        "checker": deepcopy(request["checker"]),
        "configuration_fingerprints": fingerprints,
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
        "run_bound": len(fingerprints) * (2 if request.get("retry_available") else 1),
        "stopping_rule": "Stop when confidence makes the conservative quality bound clear the floor or the finite run bound is spent.",
        "sequential_plan": "Run the weakest listed point, then only its permitted adjacent escalation after checker-confirmed failure.",
        "parallel_plan": "Run isolated adjacent points against the same frozen workload and checker when the caller grants parallel capacity.",
        "observation_artifact": {
            "schema_version": 1,
            "configuration_fingerprints": deepcopy(fingerprints),
            "unavailable_values": None,
        },
        "record_import": {
            "command": "/model-selector record <path>",
            "artifact": "observation_artifact",
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

    # Pair each request with its shared-core decision and human-only evidence.
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
                    request,
                    decision,
                    resolved["snapshot"],
                ),
                "experiment_brief": _experiment_brief(
                    request, decision, resolved["snapshot"]
                ),
            }
        )

    # Return detailed output over the same frozen snapshot and decision order.
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
