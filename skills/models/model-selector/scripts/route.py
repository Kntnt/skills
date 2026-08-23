#!/usr/bin/env python3
"""Resolve versioned model routing artifacts without external side effects."""

from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

PORTABLE_LEVELS = ("low", "medium", "high", "xhigh", "max")


def _fingerprint(point: dict[str, Any], portable: str, native: Any) -> str:
    """Bind every launch-relevant exact-point field into a stable identity."""

    value = {
        "model": point["model"],
        "channel": point["channel"],
        "serving_mode": point["serving_mode"],
        "portable_deliberation": portable,
        "native_deliberation": native,
    }
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _selected(request: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    """Select the weakest launchable point allowed by explicit dimensions."""

    overrides = request.get("overrides", {})
    deliberation = overrides.get("deliberation")
    candidates = [
        point
        for point in snapshot["mappings"]
        if point["channel"] in snapshot["harness"]["adapters"]
        and point["capability"] <= snapshot["main_seat"]["capability"]
        and (
            "model" not in overrides
            or point["model"] == overrides["model"]
            or overrides["model"] in point.get("aliases", [])
        )
        and (deliberation is None or deliberation in point["controls"])
    ]
    point = min(candidates, key=lambda candidate: candidate["capability"])
    records = [
        record
        for record in snapshot["evidence"].get("records", [])
        if record.get("model") == point["model"]
        and set(record.get("workload_tags", []))
        <= set(request.get("workload_tags", []))
    ]
    portable = overrides.get(
        "deliberation",
        max(
            records,
            key=lambda record: record["quality"],
            default={"portable_deliberation": "low"},
        )["portable_deliberation"],
    )
    native = point["controls"][portable]
    launch = point["launch"]
    arguments = {
        launch["model_flag"]: point["model"],
        launch["deliberation_flag"]: next(iter(native.values())),
    }
    fingerprint = _fingerprint(point, portable, native)

    evidence = snapshot["evidence"]
    evidence_class = (
        "mixed"
        if any(record.get("stale") for record in records)
        else "measurement_based"
        if records
        else "heuristic"
    )

    return {
        "request_id": request["request_id"],
        "status": "selected",
        "launch": {
            "model": point["model"],
            "resolved_alias": overrides.get("model")
            if overrides.get("model") in point.get("aliases", [])
            else None,
            "channel": point["channel"],
            "serving_mode": point["serving_mode"],
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
        "exclusions": [],
        "next_escalation": _escalation(request, point, portable),
        "audit": {"snapshot_identity": snapshot["snapshot_identity"]},
    }


def _escalation(
    request: dict[str, Any], point: dict[str, Any], portable: str
) -> dict[str, Any] | None:
    """Describe one existing-retry step only after externally bound failure."""

    prior = request.get("prior", {})
    failure = request.get("verified_failure", {})
    checker = request.get("checker", {})
    if (
        not request.get("reversible")
        or checker.get("kind") not in {"external", "declared"}
        or not failure
        or failure.get("configuration_fingerprint")
        != prior.get("configuration_fingerprint")
    ):
        return None

    current = prior.get("portable_deliberation", portable)
    if current not in PORTABLE_LEVELS:
        return None
    adjacent_index = PORTABLE_LEVELS.index(current) + 1
    if adjacent_index >= len(PORTABLE_LEVELS):
        return None
    adjacent = PORTABLE_LEVELS[adjacent_index]
    if adjacent not in point["controls"]:
        return None
    return {
        "model": point["model"],
        "portable_deliberation": adjacent,
        "consumes_existing_retry": True,
    }


def _refused(
    request: dict[str, Any], snapshot: dict[str, Any], code: str
) -> dict[str, Any]:
    """Return a stable refusal shape that cannot be mistaken for launchable."""

    return {
        "request_id": request.get("request_id"),
        "status": "refused",
        "reason": {"code": code},
        "audit": {"snapshot_identity": snapshot["snapshot_identity"]},
    }


def _inherit(
    request: dict[str, Any], snapshot: dict[str, Any], reason: str
) -> dict[str, Any]:
    """Return an audited no-override result with the frozen main seat."""

    return {
        "request_id": request["request_id"],
        "status": "inherit",
        "inheritance": {
            "reason": reason,
            "main_seat": deepcopy(snapshot["main_seat"]),
        },
        "audit": {"snapshot_identity": snapshot["snapshot_identity"]},
    }


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
    if snapshot["main_seat"].get("capability") is None:
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
        if "model" not in overrides
        or point["model"] == overrides["model"]
        or overrides["model"] in point.get("aliases", [])
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
        point["capability"] > snapshot["main_seat"]["capability"]
        for point in model_matches
    ):
        return _refused(request, snapshot, "above_main_seat_ceiling")

    safe = [
        point
        for point in model_matches
        if point["channel"] in snapshot["harness"]["adapters"]
        and point["capability"] <= snapshot["main_seat"]["capability"]
        and (deliberation is None or deliberation in point["controls"])
    ]
    if not safe:
        return _refused(request, snapshot, "empty_safe_candidate_set")
    if not snapshot["evidence"].get("records") and not overrides:
        return _inherit(request, snapshot, "insufficient_evidence")
    return _selected(request, snapshot)


def route(artifact: dict[str, Any]) -> dict[str, Any]:
    """Return ordered decisions and the exact snapshot used to derive them."""

    requests = artifact.get("requests", [])
    snapshot = deepcopy(artifact.get("snapshot", artifact.get("context", {})))
    snapshot.setdefault(
        "snapshot_identity",
        "sha256:"
        + hashlib.sha256(
            json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    )
    required = {
        "snapshot_version",
        "profile",
        "evidence",
        "harness",
        "main_seat",
        "mappings",
        "override_policy",
    }
    if artifact.get("schema_version") != 1:
        decisions = [
            _refused(request, snapshot, "invalid_request") for request in requests
        ]
    elif not required <= set(snapshot):
        decisions = [
            _refused(request, snapshot, "invalid_snapshot") for request in requests
        ]
    else:
        decisions = [_decision(request, snapshot) for request in requests]
    return {"schema_version": 1, "snapshot": snapshot, "decisions": decisions}


def main() -> int:
    """Read one artifact path and emit only its compact JSON response."""

    artifact = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(route(artifact), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
