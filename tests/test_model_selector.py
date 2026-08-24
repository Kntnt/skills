"""Public contracts shipped by the model-selector Skill."""

import hashlib
import importlib.util
import json
import re
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
MODEL_SELECTOR: Path = REPO_ROOT / "skills" / "models" / "model-selector"


def _load_router() -> Any:
    """Load the shipped public routing module from its installed path."""

    path = MODEL_SELECTOR / "scripts" / "route.py"
    spec = importlib.util.spec_from_file_location("model_selector_route", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _routing_snapshot() -> dict[str, Any]:
    """Provide one frozen exact-point routing context."""

    return {
        "snapshot_version": 1,
        "profile": {"revision": "profile-7", "valid": True},
        "evidence": {
            "identity": "ledger-9",
            "vintage": "2026-08-01T00:00:00Z",
            "records": [
                {
                    "model": "worker-v2",
                    "portable_deliberation": "low",
                    "workload_tags": ["python"],
                    "quality": 0.93,
                },
                {
                    "model": "worker-v2",
                    "portable_deliberation": "high",
                    "workload_tags": ["python"],
                    "quality": 0.88,
                },
            ],
        },
        "harness": {
            "name": "codex",
            "surface": "subagent",
            "inventory_revision": "inventory-3",
            "inheritance": True,
            "adapters": ["native"],
        },
        "main_seat": {
            "model": "main-v3",
            "channel": "native",
            "serving_mode": "standard",
            "native_deliberation": {"effort": "xhigh"},
            "portable_deliberation": "xhigh",
            "capability": 100,
        },
        "mappings": [
            {
                "model": "worker-v2",
                "channel": "native",
                "serving_mode": "standard",
                "capability": 70,
                "controls": {
                    "low": {"effort": "low"},
                    "medium": {"effort": "medium"},
                    "high": {"effort": "high"},
                    "xhigh": {"effort": "xhigh"},
                    "max": {"effort": "xhigh"},
                },
                "launch": {
                    "model_flag": "model",
                    "deliberation_flag": "reasoning_effort",
                },
                "commercial": {
                    "cash": 1.0,
                    "rolling_quota": 2.0,
                    "weekly_quota": 3.0,
                    "allocated_subscription_cost": None,
                    "latency": 4.0,
                },
            }
        ],
        "override_policy": {
            "portable_levels": ["low", "medium", "high", "xhigh", "max"]
        },
    }


def _complete_routing_snapshot() -> dict[str, Any]:
    """Provide a complete point and a concrete data-driven Harness adapter."""

    snapshot = _routing_snapshot()
    point = snapshot["mappings"][0]
    point.update(
        {
            "aliases": [],
            "surface": "subagent",
            "tools": ["shell", "apply_patch"],
            "policy": {"sandbox": "workspace-write", "network": "disabled"},
            "model_capability": 70,
            "enabled": True,
            "control_capabilities": {
                "low": 1,
                "medium": 2,
                "high": 3,
                "xhigh": 4,
                "max": 4,
            },
        }
    )
    point["controls"]["low"] = {"effort": "low", "summary": "auto"}
    point["native_control_order"] = [
        point["controls"]["low"],
        point["controls"]["medium"],
        point["controls"]["high"],
        point["controls"]["xhigh"],
    ]
    snapshot["main_seat"].update(
        {
            "surface": "subagent",
            "adapter_id": "codex-main-seat",
            "model_capability": 100,
            "deliberation_capability": 4,
            "tools": ["shell", "apply_patch"],
            "policy": {"sandbox": "workspace-write", "network": "disabled"},
        }
    )
    snapshot["override_policy"].update(
        {"cold_start": "select", "quality_floor": 0.9, "shadow_prices": None}
    )
    snapshot["evidence"]["records"] = []
    snapshot["harness"]["adapter_specs"] = [
        {
            "adapter_id": "codex-native-subagent",
            "channel": "native",
            "harness": "codex",
            "surface": "subagent",
            "models": ["worker-v2"],
            "serving_modes": ["standard"],
            "native_controls": list(point["controls"].values()),
            "tool_sets": [["shell", "apply_patch"]],
            "policies": [
                {"sandbox": "workspace-write", "network": "disabled"},
                {"sandbox": "read-only", "network": "disabled"},
            ],
            "launch": {
                "model_flag": "model",
                "surface_flag": "surface",
                "serving_mode_flag": "service_tier",
                "native_control_flags": {
                    "effort": "reasoning_effort",
                    "summary": "reasoning_summary",
                },
                "tools_flag": "tools",
                "policy_flags": {"sandbox": "sandbox", "network": "network"},
            },
        }
    ]
    snapshot["harness"].pop("adapters")
    snapshot["main_seat"].pop("capability")
    point.pop("capability")
    point.pop("launch")
    return snapshot


def test_route_selects_an_exact_launchable_point() -> None:
    """The public seam returns a complete Harness-native launch decision."""

    result = _load_router().route(
        {
            "schema_version": 1,
            "snapshot": _complete_routing_snapshot(),
            "requests": [
                {
                    "request_id": "build-1",
                    "authority": "execution",
                    "stage": "build",
                    "workload": "Change the Python parser",
                    "workload_cohort": "python-refactor",
                    "workload_tags": ["python"],
                    "reversible": True,
                    "checker": {"kind": "external", "signal": "pytest"},
                    "overrides": {},
                }
            ],
        }
    )

    assert result["decisions"][0]["status"] == "selected"
    assert result["decisions"][0]["launch"]["arguments"] == {
        "model": "worker-v2",
        "surface": "subagent",
        "service_tier": "standard",
        "reasoning_effort": "low",
        "reasoning_summary": "auto",
        "tools": ["shell", "apply_patch"],
        "sandbox": "workspace-write",
        "network": "disabled",
    }
    assert result["decisions"][0]["launch"]["native_deliberation"] == {
        "effort": "low",
        "summary": "auto",
    }
    assert result["snapshot"]["profile"]["revision"] == "profile-7"


def test_route_uses_a_complete_harness_adapter_and_point_fingerprint() -> None:
    """Reachability, translation, and identity cover every launch-relevant fact."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    decision = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    assert decision["launch"]["arguments"] == {
        "model": "worker-v2",
        "surface": "subagent",
        "service_tier": "standard",
        "reasoning_effort": "low",
        "reasoning_summary": "auto",
        "tools": ["shell", "apply_patch"],
        "sandbox": "workspace-write",
        "network": "disabled",
    }
    assert decision["launch"]["adapter_id"] == "codex-native-subagent"
    assert decision["audit"]["provenance"] == {
        "profile_revision": "profile-7",
        "evidence_identity": "ledger-9",
        "evidence_vintage": "2026-08-01T00:00:00Z",
        "harness_inventory_revision": "inventory-3",
        "main_seat_model": "main-v3",
    }

    filtered = _complete_routing_snapshot()
    unreachable_point = deepcopy(filtered["mappings"][0])
    unreachable_point.update({"model": "worker-v3", "tools": ["browser"]})
    filtered["mappings"].append(unreachable_point)
    filtered["harness"]["adapter_specs"][0]["models"].append("worker-v3")
    filtered_decision = router.route(
        {
            "schema_version": 1,
            "snapshot": filtered,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    assert filtered_decision["status"] == "selected"
    assert filtered_decision["exclusions"] == [
        {
            "code": "adapter_unreachable",
            "detail": "No active adapter can launch every field of this point.",
            "model": "worker-v3",
            "portable_deliberation": "low",
        }
    ]
    assert filtered_decision["audit"]["exclusions"] == filtered_decision["exclusions"]

    changed_tools = _complete_routing_snapshot()
    changed_tools["mappings"][0]["tools"] = ["shell"]
    unreachable = router.route(
        {
            "schema_version": 1,
            "snapshot": changed_tools,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    assert unreachable["status"] == "refused"
    assert unreachable["reason"]["code"] == "empty_safe_candidate_set"
    assert unreachable["audit"]["exclusions"][0]["code"] == "adapter_unreachable"

    changed_policy = _complete_routing_snapshot()
    changed_policy["mappings"][0]["policy"]["sandbox"] = "read-only"
    changed_commercial = _complete_routing_snapshot()
    changed_commercial["mappings"][0]["commercial"]["cash"] = 99.0
    policy_decision = router.route(
        {
            "schema_version": 1,
            "snapshot": changed_policy,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    commercial_decision = router.route(
        {
            "schema_version": 1,
            "snapshot": changed_commercial,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    assert (
        decision["launch"]["configuration_fingerprint"]
        != policy_decision["launch"]["configuration_fingerprint"]
    )
    assert (
        decision["launch"]["configuration_fingerprint"]
        == commercial_decision["launch"]["configuration_fingerprint"]
    )


def test_route_requires_verified_mappings_below_the_complete_main_seat() -> None:
    """Automatic, explicit, and max controls respect exact mapping ceilings."""

    router = _load_router()
    missing_automatic = _complete_routing_snapshot()
    missing_automatic["mappings"][0]["controls"].pop("low")
    missing_automatic["mappings"][0]["control_capabilities"].pop("low")
    missing_automatic["mappings"][0]["native_control_order"].pop(0)
    missing_automatic["harness"]["adapter_specs"][0]["native_controls"] = list(
        missing_automatic["mappings"][0]["controls"].values()
    )
    automatic = router.route(
        {
            "schema_version": 1,
            "snapshot": missing_automatic,
            "requests": [_request()],
        }
    )["decisions"][0]
    assert automatic["status"] == "selected"
    assert automatic["launch"]["portable_deliberation"] == "medium"

    unverified_max = _complete_routing_snapshot()
    unverified_max["mappings"][0]["controls"]["max"] = {
        "effort": "maximum",
        "summary": "detailed",
    }
    max_decision = router.route(
        {
            "schema_version": 1,
            "snapshot": unverified_max,
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )["decisions"][0]
    assert max_decision["status"] == "refused"
    assert max_decision["reason"]["code"] == "invalid_snapshot"

    deliberation_ceiling = _complete_routing_snapshot()
    deliberation_ceiling["main_seat"]["deliberation_capability"] = 2
    above_deliberation = router.route(
        {
            "schema_version": 1,
            "snapshot": deliberation_ceiling,
            "requests": [_request(overrides={"deliberation": "high"})],
        }
    )["decisions"][0]
    assert above_deliberation["status"] == "refused"
    assert above_deliberation["reason"]["code"] == "above_main_seat_ceiling"

    model_ceiling = _complete_routing_snapshot()
    model_ceiling["mappings"][0]["model_capability"] = 101
    above_model = router.route(
        {
            "schema_version": 1,
            "snapshot": model_ceiling,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]
    assert above_model["status"] == "refused"
    assert above_model["reason"]["code"] == "above_main_seat_ceiling"


def _request(**changes: Any) -> dict[str, Any]:
    """Build one valid execution request with explicit variations."""

    request = {
        "request_id": "route-1",
        "authority": "execution",
        "stage": "build",
        "workload": "Change the Python parser",
        "workload_cohort": "python-refactor",
        "workload_tags": ["python"],
        "reversible": True,
        "checker": {"kind": "external", "signal": "pytest"},
        "overrides": {},
    }
    request.update(changes)
    return request


def _measurement_record(decision: dict[str, Any], **changes: Any) -> dict[str, Any]:
    """Build exact representative evidence from a public selected decision."""

    launch = decision["launch"]
    record = {
        "configuration_fingerprint": launch["configuration_fingerprint"],
        "model": launch["model"],
        "portable_deliberation": launch["portable_deliberation"],
        "native_deliberation": launch["native_deliberation"],
        "channel": launch["channel"],
        "harness": "codex",
        "surface": launch["surface"],
        "serving_mode": launch["serving_mode"],
        "stage": "build",
        "workload_cohort": "python-refactor",
        "workload_tags": ["python"],
        "representative": True,
        "coverage": {"decision_relevant": True},
        "uncertainty": {"lower_bound": 0.92, "upper_bound": 0.96},
        "quality": 0.94,
        "stale": False,
    }
    record.update(changes)
    return record


def test_route_preserves_batch_order_and_inherits_the_verdict_seat() -> None:
    """Every request produces one same-position discriminated decision."""

    verdict = _request(request_id="verdict", authority="verdict", stage="verify")
    execution = _request(request_id="execution")
    decisions = _load_router().route(
        {
            "schema_version": 1,
            "snapshot": _complete_routing_snapshot(),
            "requests": [verdict, execution],
        }
    )["decisions"]

    assert [decision["request_id"] for decision in decisions] == [
        "verdict",
        "execution",
    ]
    assert decisions[0]["status"] == "inherit"
    assert decisions[0]["inheritance"]["main_seat"]["model"] == "main-v3"
    assert "launch" not in decisions[0]
    assert decisions[1]["status"] == "selected"


def test_route_honors_independent_overrides_and_matched_lower_evidence() -> None:
    """A model lock leaves effort selectable and evidence need not rank adjacency."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    snapshot["mappings"][0]["commercial"]["allocated_subscription_cost"] = 1.0
    low = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [
                _request(overrides={"model": "worker-v2", "deliberation": "low"})
            ],
        }
    )["decisions"][0]
    high = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [
                _request(overrides={"model": "worker-v2", "deliberation": "high"})
            ],
        }
    )["decisions"][0]
    snapshot["evidence"]["records"] = [
        _measurement_record(low),
        _measurement_record(
            high,
            quality=0.9,
            uncertainty={"lower_bound": 0.9, "upper_bound": 0.92},
        ),
    ]
    result = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    assert result["launch"]["model"] == "worker-v2"
    assert result["launch"]["portable_deliberation"] == "low"
    assert result["evidence_class"] == "measurement_based"


def test_route_freezes_max_native_value_in_the_fingerprint() -> None:
    """Max resolves from the snapshot and changes exact-point identity."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    first = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )
    changed = _complete_routing_snapshot()
    changed_native = {"effort": "maximum", "summary": "detailed"}
    changed["mappings"][0]["controls"]["xhigh"] = changed_native
    changed["mappings"][0]["controls"]["max"] = changed_native
    changed["mappings"][0]["native_control_order"][-1] = changed_native
    changed["harness"]["adapter_specs"][0]["native_controls"] = list(
        changed["mappings"][0]["controls"].values()
    )
    reused = router.route(
        {
            "schema_version": 1,
            "snapshot": first["snapshot"],
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )
    later = router.route(
        {
            "schema_version": 1,
            "snapshot": changed,
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )

    assert first["decisions"] == reused["decisions"]
    assert first["decisions"][0]["launch"]["native_deliberation"] == {"effort": "xhigh"}
    assert (
        first["decisions"][0]["launch"]["configuration_fingerprint"]
        != later["decisions"][0]["launch"]["configuration_fingerprint"]
    )


def test_route_emits_only_a_bounded_adjacent_escalation() -> None:
    """Only one fully bound, launchable, below-seat retry may escalate."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    selected = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    launch = selected["launch"]
    prior = {
        field: launch[field]
        for field in (
            "configuration_fingerprint",
            "model",
            "channel",
            "surface",
            "serving_mode",
            "adapter_id",
            "portable_deliberation",
            "native_deliberation",
        )
    }
    verified_failure = {
        **prior,
        "outcome": "failed",
        "checker": {"kind": "external", "signal": "pytest"},
    }
    request = _request(
        overrides={"deliberation": "low"},
        retry_available=True,
        prior=prior,
        verified_failure=verified_failure,
    )
    escalation = router.route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [request]}
    )["decisions"][0]["next_escalation"]

    assert escalation["model"] == "worker-v2"
    assert escalation["portable_deliberation"] == "medium"
    assert escalation["native_deliberation"] == {"effort": "medium"}
    assert escalation["configuration_fingerprint"].startswith("sha256:")
    assert escalation["arguments"]["reasoning_effort"] == "medium"
    assert escalation["consumes_existing_retry"] is True

    mismatches: list[dict[str, Any]] = [
        {"retry_available": False},
        {"prior": {**prior, "model": "other"}},
        {
            "verified_failure": {
                **verified_failure,
                "native_deliberation": {"effort": "medium"},
            }
        },
        {
            "verified_failure": {
                **verified_failure,
                "checker": {"kind": "external", "signal": "mypy"},
            }
        },
    ]
    for mismatch in mismatches:
        changed_request = deepcopy(request)
        changed_request.update(mismatch)
        decision = router.route(
            {
                "schema_version": 1,
                "snapshot": snapshot,
                "requests": [changed_request],
            }
        )["decisions"][0]
        assert decision["next_escalation"] is None, mismatch

    bounded = deepcopy(snapshot)
    bounded["main_seat"]["deliberation_capability"] = 1
    bounded_decision = router.route(
        {"schema_version": 1, "snapshot": bounded, "requests": [request]}
    )["decisions"][0]
    assert bounded_decision["next_escalation"] is None


def test_route_inherits_without_a_profile_or_discriminating_evidence() -> None:
    """Absence and honest uncertainty never trigger setup or invented facts."""

    snapshot = _complete_routing_snapshot()
    snapshot["profile"] = None
    absent = _load_router().route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]
    snapshot = _complete_routing_snapshot()
    snapshot["evidence"]["records"] = []
    snapshot["override_policy"]["cold_start"] = "inherit"
    uncertain = _load_router().route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]

    assert absent["status"] == "inherit"
    assert absent["inheritance"]["reason"] == "missing_profile"
    assert uncertain["status"] == "inherit"
    assert uncertain["inheritance"]["reason"] == "insufficient_evidence"


def test_route_refuses_every_unsafe_family_without_launch_arguments() -> None:
    """Invalid, unavailable, unsafe, and empty states fail before launch."""

    cases: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    invalid = _complete_routing_snapshot()
    invalid["profile"]["valid"] = False
    cases.append((invalid, _request(), "invalid_profile"))
    cases.append(
        (
            _complete_routing_snapshot(),
            _request(overrides={"deliberation": "auto"}),
            "invalid_request",
        )
    )
    cases.append(
        (
            _complete_routing_snapshot(),
            _request(overrides={"model": "missing"}),
            "unavailable_override",
        )
    )
    unavailable = _complete_routing_snapshot()
    unavailable["mappings"][0]["controls"].pop("xhigh")
    unavailable["mappings"][0]["control_capabilities"].pop("xhigh")
    unavailable["harness"]["adapter_specs"][0]["native_controls"] = list(
        unavailable["mappings"][0]["controls"].values()
    )
    cases.append(
        (
            unavailable,
            _request(overrides={"deliberation": "xhigh"}),
            "unavailable_override",
        )
    )
    unknown = _complete_routing_snapshot()
    unknown["main_seat"]["model_capability"] = None
    cases.append((unknown, _request(), "unknown_main_seat_ceiling"))
    above = _complete_routing_snapshot()
    above["mappings"][0]["model_capability"] = 101
    cases.append(
        (above, _request(overrides={"model": "worker-v2"}), "above_main_seat_ceiling")
    )
    unreachable = _complete_routing_snapshot()
    unreachable["harness"]["adapter_specs"] = []
    cases.append((unreachable, _request(), "empty_safe_candidate_set"))
    verdict = _complete_routing_snapshot()
    verdict["harness"]["inheritance"] = False
    cases.append(
        (verdict, _request(authority="verdict"), "unrepresentable_verdict_inheritance")
    )

    for snapshot, request, expected in cases:
        decision = _load_router().route(
            {"schema_version": 1, "snapshot": snapshot, "requests": [request]}
        )["decisions"][0]
        assert decision["status"] == "refused"
        assert decision["reason"]["code"] == expected
        assert "launch" not in decision


def test_route_derives_a_snapshot_once_and_resolves_exact_aliases() -> None:
    """Current inputs become a reusable snapshot before alias resolution."""

    context = _complete_routing_snapshot()
    context["mappings"][0]["aliases"] = ["worker-latest"]
    result = _load_router().route(
        {
            "schema_version": 1,
            "context": context,
            "requests": [_request(overrides={"model": "worker-latest"})],
        }
    )

    assert result["snapshot"]["snapshot_identity"].startswith("sha256:")
    assert result["decisions"][0]["launch"]["model"] == "worker-v2"
    assert result["decisions"][0]["launch"]["resolved_alias"] == "worker-latest"


def test_route_refuses_invalid_snapshots_and_ambiguous_aliases() -> None:
    """Unreproducible context and non-exact aliases are never guessed."""

    invalid = _complete_routing_snapshot()
    invalid.pop("commercial_facts", None)
    invalid.pop("mappings")
    invalid_decision = _load_router().route(
        {"schema_version": 1, "snapshot": invalid, "requests": [_request()]}
    )["decisions"][0]
    ambiguous = _complete_routing_snapshot()
    ambiguous["mappings"][0]["aliases"] = ["worker-latest"]
    duplicate = deepcopy(ambiguous["mappings"][0])
    duplicate["model"] = "worker-v3"
    ambiguous["mappings"].append(duplicate)
    ambiguous_decision = _load_router().route(
        {
            "schema_version": 1,
            "snapshot": ambiguous,
            "requests": [_request(overrides={"model": "worker-latest"})],
        }
    )["decisions"][0]

    assert invalid_decision["reason"]["code"] == "invalid_snapshot"
    assert ambiguous_decision["reason"]["code"] == "ambiguous_override"


def test_route_cli_is_machine_readable_and_does_not_modify_its_input(
    tmp_path: Path,
) -> None:
    """The shipped process seam emits JSON while leaving local state untouched."""

    artifact = tmp_path / "route.json"
    artifact.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "snapshot": _complete_routing_snapshot(),
                "requests": [_request()],
            }
        ),
        encoding="utf-8",
    )
    before = artifact.read_bytes()
    completed = subprocess.run(
        ["uv", "run", str(MODEL_SELECTOR / "scripts" / "route.py"), str(artifact)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(completed.stdout)["decisions"][0]["status"] == "selected"
    assert completed.stderr == ""
    assert artifact.read_bytes() == before


def test_route_cli_returns_stable_artifact_refusals_without_tracebacks(
    tmp_path: Path,
) -> None:
    """Arguments, paths, JSON, and envelope errors remain machine-readable."""

    script = str(MODEL_SELECTOR / "scripts" / "route.py")
    malformed_json = tmp_path / "malformed.json"
    malformed_json.write_text("{not-json", encoding="utf-8")
    invalid_envelope = tmp_path / "invalid.json"
    invalid_envelope.write_text(
        json.dumps({"schema_version": 1, "requests": []}), encoding="utf-8"
    )
    cases = [
        ([], "invalid_arguments"),
        ([str(tmp_path / "absent.json")], "unreadable_artifact"),
        ([str(malformed_json)], "malformed_json"),
        ([str(invalid_envelope)], "invalid_request"),
    ]

    for arguments, expected in cases:
        completed = subprocess.run(
            ["uv", "run", script, *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
        response = json.loads(completed.stdout)
        assert completed.returncode == 2, expected
        assert completed.stderr == "", expected
        assert response["artifact_refusal"]["code"] == expected
        assert response["artifact_refusal"]["detail"], expected
        assert response["decisions"] == [], expected


def test_route_and_recommend_refuse_malformed_envelopes_without_exceptions() -> None:
    """Both public seams preserve stable artifact refusals for invalid envelopes."""

    router = _load_router()
    artifacts = [
        {"schema_version": 1, "snapshot": [], "requests": [_request()]},
        {"schema_version": 1, "requests": []},
    ]

    for artifact in artifacts:
        routed = router.route(artifact)
        recommended = router.recommend(artifact)

        assert routed["artifact_refusal"]["code"] == "invalid_request"
        assert recommended["artifact_refusal"] == routed["artifact_refusal"]
        assert recommended["recommendations"] == []


def test_route_labels_stale_measurements_mixed_and_keeps_costs_separate() -> None:
    """Staleness remains visible and commercial dimensions are not collapsed."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    selected = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    snapshot["evidence"]["records"] = [_measurement_record(selected, stale=True)]
    decision = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    assert decision["evidence_class"] == "mixed"
    assert decision["launch"]["commercial"] == {
        "cash": 1.0,
        "rolling_quota": 2.0,
        "weekly_quota": 3.0,
        "allocated_subscription_cost": None,
        "latency": 4.0,
    }


def test_route_requires_exact_representative_evidence_for_measurement_class() -> None:
    """Partial, stale, uncertain, or weak evidence never becomes green."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    snapshot["evidence"]["records"] = []
    explicit = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    exact = _measurement_record(explicit)
    snapshot["evidence"]["records"] = [exact]

    measured = router.route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]
    assert measured["status"] == "selected"
    assert measured["evidence_class"] == "measurement_based"

    partial_records = [
        {**exact, "stale": True},
        {**exact, "stage": "verify"},
        {**exact, "channel": "gateway"},
        {**exact, "native_deliberation": {"effort": "medium"}},
        {**exact, "representative": False},
        {**exact, "coverage": {"decision_relevant": False}},
        {**exact, "uncertainty": None},
        {
            **exact,
            "uncertainty": {"lower_bound": 0.82, "upper_bound": 0.96},
        },
    ]

    for partial in partial_records:
        changed = deepcopy(snapshot)
        changed["evidence"]["records"] = [partial]
        decision = router.route(
            {"schema_version": 1, "snapshot": changed, "requests": [_request()]}
        )["decisions"][0]
        assert decision["status"] == "selected"
        assert decision["evidence_class"] == "mixed", partial

    unrelated = deepcopy(snapshot)
    unrelated["evidence"]["records"] = [
        {**exact, "workload_cohort": "typescript-frontend"}
    ]
    heuristic = router.route(
        {"schema_version": 1, "snapshot": unrelated, "requests": [_request()]}
    )["decisions"][0]
    assert heuristic["status"] == "selected"
    assert heuristic["evidence_class"] == "heuristic"


def test_route_cold_start_uses_workload_safety_before_economics() -> None:
    """Safe exploration starts weak; unchecked irreversible work starts strong."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    stronger = deepcopy(snapshot["mappings"][0])
    stronger.update({"model": "worker-v3", "model_capability": 90})
    snapshot["mappings"].append(stronger)
    snapshot["harness"]["adapter_specs"][0]["models"].append("worker-v3")

    safe = router.route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]
    consequential = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [
                _request(
                    reversible=False,
                    checker={"kind": "none"},
                )
            ],
        }
    )["decisions"][0]

    assert safe["launch"]["model"] == "worker-v2"
    assert safe["launch"]["portable_deliberation"] == "low"
    assert consequential["launch"]["model"] == "worker-v3"
    assert consequential["launch"]["portable_deliberation"] == "max"
    assert consequential["evidence_class"] == "heuristic"


def test_route_uses_pareto_costs_and_only_explicit_shadow_prices() -> None:
    """Separate commercial dimensions prevent an invented universal winner."""

    router = _load_router()
    snapshot = _complete_routing_snapshot()
    first = snapshot["mappings"][0]
    first["commercial"] = {
        "cash": 1.0,
        "rolling_quota": 4.0,
        "weekly_quota": 2.0,
        "allocated_subscription_cost": 1.0,
        "latency": 4.0,
    }
    second = deepcopy(first)
    second.update(
        {
            "model": "worker-v3",
            "model_capability": 80,
            "commercial": {
                "cash": 2.0,
                "rolling_quota": 1.0,
                "weekly_quota": 1.0,
                "allocated_subscription_cost": 2.0,
                "latency": 2.0,
            },
        }
    )
    snapshot["mappings"].append(second)
    snapshot["harness"]["adapter_specs"][0]["models"].append("worker-v3")

    first_decision = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [
                _request(overrides={"model": "worker-v2", "deliberation": "low"})
            ],
        }
    )["decisions"][0]
    second_decision = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [
                _request(overrides={"model": "worker-v3", "deliberation": "low"})
            ],
        }
    )["decisions"][0]
    snapshot["evidence"]["records"] = [
        _measurement_record(
            first_decision,
            quality=0.94,
            uncertainty={"lower_bound": 0.92, "upper_bound": 0.96},
        ),
        _measurement_record(
            second_decision,
            quality=0.96,
            uncertainty={"lower_bound": 0.94, "upper_bound": 0.98},
        ),
    ]

    ambiguous = router.route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]
    assert ambiguous["status"] == "inherit"
    assert ambiguous["inheritance"]["reason"] == "underdetermined_frontier"
    assert len(ambiguous["audit"]["frontier"]) == 2

    dominated = deepcopy(snapshot)
    dominated["mappings"][1]["commercial"] = {
        "cash": 3.0,
        "rolling_quota": 5.0,
        "weekly_quota": 3.0,
        "allocated_subscription_cost": 2.0,
        "latency": 5.0,
    }
    dominated["evidence"]["records"][1].update(
        {
            "quality": 0.91,
            "uncertainty": {"lower_bound": 0.9, "upper_bound": 0.92},
        }
    )
    dominant = router.route(
        {"schema_version": 1, "snapshot": dominated, "requests": [_request()]}
    )["decisions"][0]
    assert dominant["status"] == "selected"
    assert dominant["launch"]["model"] == "worker-v2"

    priced = deepcopy(snapshot)
    priced["override_policy"]["shadow_prices"] = {
        "rolling_quota": 1.0,
        "weekly_quota": 0.1,
        "allocated_subscription_cost": 0.1,
        "latency": 0.1,
    }
    selected = router.route(
        {"schema_version": 1, "snapshot": priced, "requests": [_request()]}
    )["decisions"][0]
    assert selected["status"] == "selected"
    assert selected["launch"]["model"] == "worker-v3"
    assert selected["launch"]["commercial"] == snapshot["mappings"][1]["commercial"]
    assert selected["audit"]["decision_policy"] == "explicit_shadow_prices"

    recommendation = router.recommend(
        {"schema_version": 1, "snapshot": priced, "requests": [_request()]}
    )["recommendations"][0]
    assert recommendation["decision"] == selected
    assert recommendation["evidence_banner"]["class"] == "measurement_based"
    assert recommendation["frontier_neighbors"][0]["model"] == "worker-v2"
    assert recommendation["uncertainty"] == {
        "status": "measured",
        "lower_bound": 0.94,
        "upper_bound": 0.98,
    }
    assert recommendation["experiment_brief"] is None


def test_route_and_recommend_share_selection_but_not_presentation() -> None:
    """Both public forms adapt one exact selection result without semantic drift."""

    router = _load_router()
    artifact = {
        "schema_version": 1,
        "snapshot": _complete_routing_snapshot(),
        "requests": [_request(overrides={"deliberation": "low"})],
    }

    route_result = router.route(deepcopy(artifact))
    recommend_result = router.recommend(deepcopy(artifact))
    recommendation = recommend_result["recommendations"][0]

    assert recommendation["decision"] == route_result["decisions"][0]
    assert recommendation["evidence_banner"] == {
        "class": "heuristic",
        "text": "🔵 HEURISTISK STARTPUNKT",
        "confidence": "low",
        "production_recommendation": False,
    }
    assert recommendation["frontier_neighbors"] == []
    assert recommendation["uncertainty"]["status"] == "unknown"
    fingerprints = recommendation["experiment_brief"]["configuration_fingerprints"]
    assert (
        fingerprints[0]
        == route_result["decisions"][0]["launch"]["configuration_fingerprint"]
    )
    assert len(fingerprints) == 2
    assert fingerprints[0] != fingerprints[1]
    assert recommendation["experiment_brief"]["checker"] == {
        "kind": "external",
        "signal": "pytest",
    }
    assert recommendation["experiment_brief"]["sequential_plan"]
    assert recommendation["experiment_brief"]["parallel_plan"]


def test_route_totally_validates_nested_snapshot_and_request_families() -> None:
    """Malformed nested state becomes detailed refusals rather than exceptions."""

    snapshot_changes: list[tuple[str, Any]] = [
        ("profile", {"revision": 7, "valid": True}),
        (
            "evidence",
            {"identity": "ledger-9", "vintage": "2026-08-01T00:00:00Z", "records": {}},
        ),
        ("harness", {"name": "codex", "adapters": "native", "inheritance": True}),
        ("main_seat", {"model": "main-v3", "capability": "highest"}),
        ("mappings", [{"model": "worker-v2", "controls": []}]),
        (
            "mappings",
            [
                {
                    **_complete_routing_snapshot()["mappings"][0],
                    "commercial": {"cash": "cheap"},
                }
            ],
        ),
        ("override_policy", {"portable_levels": ["low", "high"]}),
    ]

    for family, malformed in snapshot_changes:
        snapshot = _complete_routing_snapshot()
        snapshot[family] = malformed
        decision = _load_router().route(
            {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
        )["decisions"][0]
        assert decision["status"] == "refused", family
        assert decision["reason"]["code"] == "invalid_snapshot", family
        assert decision["reason"]["detail"], family

    request_changes: list[tuple[str, Any]] = [
        ("request_id", 7),
        ("checker", []),
        ("overrides", []),
        ("prior", []),
        ("verified_failure", []),
    ]

    for family, malformed in request_changes:
        invalid_request = _request(request_id="invalid")
        invalid_request[family] = malformed
        decisions = _load_router().route(
            {
                "schema_version": 1,
                "snapshot": _complete_routing_snapshot(),
                "requests": [invalid_request, _request(request_id="valid")],
            }
        )["decisions"]
        assert [decision["request_id"] for decision in decisions] == [
            "invalid" if family != "request_id" else None,
            "valid",
        ]
        assert decisions[0]["status"] == "refused", family
        assert decisions[0]["reason"]["code"] == "invalid_request", family
        assert decisions[0]["reason"]["detail"], family
        assert decisions[1]["status"] == "selected", family


def _read(relative: str) -> str:
    """Read one model-selector artifact through its shipped path."""

    return (MODEL_SELECTOR / relative).read_text(encoding="utf-8")


def _seed_records() -> list[dict[str, Any]]:
    """Parse the bundled JSONL evidence through its shipped representation."""

    return [
        json.loads(line)
        for line in _read("data/seed-evidence.jsonl").splitlines()
        if line
    ]


def _reasoning_controls(record: dict[str, Any]) -> list[str]:
    """Return the ordered reasoning choices declared by one model seed."""

    controls = cast(dict[str, Any], record["supported_controls"])
    effort = cast(list[str], controls.get("effort", []))
    thinking = cast(dict[str, Any], controls.get("thinking", {}))
    return effort or cast(list[str], thinking.get("modes", []))


def _nested_keys(value: Any) -> set[str]:
    """Collect every object key from an arbitrarily nested JSON value."""

    if isinstance(value, dict):
        return set(value) | {
            key for child in value.values() for key in _nested_keys(child)
        }
    if isinstance(value, list):
        return {key for child in value for key in _nested_keys(child)}
    return set()


def _assert_contains_all(text: str, expected: set[str]) -> None:
    """Report every required contract fragment absent from shipped prose."""

    missing = {fragment for fragment in expected if fragment not in text}
    assert not missing, f"missing contract fragments: {sorted(missing)}"


def _capability_prior_id(record: dict[str, Any]) -> str:
    """Derive the stable identity documented for a capability prior."""

    # Bind the provenance-preserving wording into the prior identity.
    claim = cast(dict[str, Any], record["claim"])
    claim_hash = hashlib.sha256(
        json.dumps(claim, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    # Normalize tag order before it participates in the digest.
    normalized_tags = json.dumps(
        {
            "capability": sorted(cast(list[str], record["capability_tags"])),
            "workload": sorted(cast(list[str], record["workload_tags"])),
        },
        sort_keys=True,
        separators=(",", ":"),
    )

    # Bind model, source, time, tags, and claim into one stable key.
    identity = "|".join(
        [
            cast(str, record["provider"]),
            cast(str, record["model_seed_id"]),
            cast(str, record["source_url"]),
            cast(str, record.get("effective_at") or record["retrieved_at"]),
            normalized_tags,
            claim_hash,
        ]
    )

    return f"capability-prior:{hashlib.sha256(identity.encode()).hexdigest()}"


def test_cold_start_chooses_the_lowest_safe_complete_configuration() -> None:
    """Cold start must not prefer a measured maximum."""

    contract = "\n".join([_read("SKILL.md"), _read("references/pareto-selection.md")])
    public_help = "\n".join([_read("help.md"), _read("help/recommend.md")])
    required_rules = {
        "weakest plausibly capable enabled model",
        "lowest plausibly sufficient supported reasoning control",
        "task complexity, ambiguity, context demand, autonomy, tool use, reversibility, consequence of failure and objective checkability",
        "escalate exactly one adjacent reasoning rung",
        "strongest plausible enabled configuration",
        "refuse unsafe exploration",
    }
    public_rules = {
        "weakest plausibly capable enabled model",
        "lowest plausibly sufficient supported reasoning control",
        "one adjacent reasoning rung",
        "strongest plausible enabled configuration",
        "unsafe exploration",
    }

    _assert_contains_all(contract, required_rules)
    _assert_contains_all(public_help, public_rules)


def test_recommendation_output_distinguishes_evidence_classes_in_text() -> None:
    """A cold-start guess must not look like a measured production choice."""

    execution_contract = "\n".join(
        [_read("SKILL.md"), _read("references/pareto-selection.md")]
    )
    public_help = "\n".join([_read("help.md"), _read("help/recommend.md")])
    banners = {
        "🔵 HEURISTISK STARTPUNKT",
        "🟠 BLANDAD EVIDENS",
        "🟢 MÄTDATABASERAD REKOMMENDATION",
    }
    required_details = {
        "exactly one prominent, text-bearing status banner",
        "classification reason",
        "confidence",
        "evidence still missing",
        "exploration start or a production recommendation",
    }

    _assert_contains_all(execution_contract, banners)
    _assert_contains_all(public_help, banners)
    _assert_contains_all(execution_contract, required_details)


def test_uncertain_results_include_an_agent_ready_experiment_brief() -> None:
    """Uncertain results must include an executable evidence path."""

    execution_contract = "\n".join(
        [_read("SKILL.md"), _read("references/pareto-selection.md")]
    )
    public_help = "\n".join([_read("help.md"), _read("help/recommend.md")])
    brief_contract = {
        "Immediately after a blue or orange banner",
        "Snabbaste vägen till mätdata",
        "workload artifact, cohort, rubric, quality floor",
        "external checker or declared failure signal",
        "exact configuration fingerprints",
        "quality, cost, quota, latency, failure, retry and provenance measurements",
        "bounded run budget and a confidence-based stopping rule",
        "observation artifact and import form accepted by `model-selector record`",
        "quota-efficient sequential plan",
        "time-efficient parallel plan",
        "isolated agents run adjacent configurations against the same frozen task and checker",
    }

    _assert_contains_all(execution_contract, brief_contract)
    assert (
        "plans the experiment but performs no network request, evaluation, or write"
        in public_help
    )


def test_downward_probes_are_safe_and_cannot_replace_the_incumbent_early() -> None:
    """A downward probe cannot replace a measured incumbent early."""

    contract = _read("references/pareto-selection.md")
    probe_rules = {
        "adjacent lower point",
        "missing or too uncertain",
        "could change the relevant frontier or selected policy",
        "representative, reversible and objectively checkable",
        "does not replace the production recommendation",
        "conservative quality bound clears the floor",
        "opportunity and expected decision value",
    }

    _assert_contains_all(contract, probe_rules)


def test_each_seeded_reasoning_curve_has_a_capability_prior() -> None:
    """Every seeded reasoning curve needs cold-start evidence."""

    records = _seed_records()
    models = {
        record["seed_id"]
        for record in records
        if record["record_type"] in {"model_version_seed", "model_reference_seed"}
        and len(_reasoning_controls(record)) > 1
    }
    priors = [
        record["model_seed_id"]
        for record in records
        if record["record_type"] == "capability_prior_seed"
    ]

    assert models <= set(priors)


def test_capability_priors_are_provenanced_categorical_evidence() -> None:
    """Provider prose must remain a low-confidence experiment prior."""

    records = _seed_records()
    models = {
        record["seed_id"]: record
        for record in records
        if record["record_type"] in {"model_version_seed", "model_reference_seed"}
    }
    priors = [
        record for record in records if record["record_type"] == "capability_prior_seed"
    ]
    required_fields = {
        "seed_id",
        "prior_id",
        "model_seed_id",
        "provider",
        "source_url",
        "retrieved_at",
        "workload_tags",
        "capability_tags",
        "claim",
        "status",
        "confidence",
    }
    forbidden_fields = {
        "quality",
        "score",
        "uncertainty",
        "success_probability",
        "cost",
        "dominance",
        "pareto",
    }
    first_party_hosts = {
        "anthropic": "platform.claude.com",
        "openai": "developers.openai.com",
        "spacexai": "docs.x.ai",
    }
    ledger_contract = _read("references/evidence-ledger.md")

    assert priors
    assert len({prior["prior_id"] for prior in priors}) == len(priors)
    for prior in priors:
        assert required_fields <= set(prior)
        assert prior["seed_id"] == prior["prior_id"]
        assert prior["prior_id"] == _capability_prior_id(prior)
        assert re.fullmatch(r"capability-prior:[a-f0-9]{64}", prior["prior_id"])
        assert prior["model_seed_id"] in models
        assert prior["provider"] == models[prior["model_seed_id"]]["provider"]
        assert (
            urlparse(prior["source_url"]).hostname
            == first_party_hosts[prior["provider"]]
        )
        assert re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", prior["retrieved_at"]
        )
        assert prior["confidence"] == "low"
        assert "low_confidence" in prior["status"]
        assert prior["claim"]["form"] in {"verbatim_excerpt", "faithful_paraphrase"}
        assert prior["claim"]["text"]
        assert all(
            re.fullmatch(r"[a-z0-9_]+", tag)
            for field in ("workload_tags", "capability_tags")
            for tag in prior[field]
        )
        assert forbidden_fields.isdisjoint(_nested_keys(prior))

    assert "`capability-priors.jsonl`" in ledger_contract
    assert "`CapabilityPrior`" in ledger_contract
    assert "`capability_prior_seed`" in ledger_contract
    assert (
        "never enters numeric quality, uncertainty, success probability, cost or Pareto calculations"
        in ledger_contract
    )


def test_commands_keep_capability_priors_offline_and_append_only() -> None:
    """Recommend reads priors; Update alone refreshes their ledger."""

    records = _seed_records()
    manifest = records[0]
    skill = _read("SKILL.md")
    command_rules = {
        "applicable `capability_prior_seed` rows in place",
        "when no newer ledger record exists",
        "Relevant matched measurements override capability priors",
        "existing model/release-source cadence",
        "append changed capability-prior records without rewriting history",
    }

    assert manifest["record_type"] == "seed_manifest"
    assert "capability_prior" in manifest["scope"]
    _assert_contains_all(skill, command_rules)


def test_route_exposes_the_public_model_routing_contract() -> None:
    """Delegated callers receive ordered, exact, reproducible decisions."""

    skill = _read("SKILL.md")
    route_help = _read("help/route.md")
    route_contract = _read("references/model-routing.md")
    public_contract = f"{skill}\n{route_help}\n{route_contract}"
    required_fragments = {
        "`selected`, `inherit`, or `refused`",
        "same order",
        "low`, `medium`, `high`, `xhigh`, and `max",
        "profile revision",
        "evidence vintage and identity",
        "Harness inventory",
        "main-seat identity",
        "control mappings",
        "commercial facts",
        "override policy",
        "configuration fingerprint",
        "Harness-native launch arguments",
        "exact configured model version or resolved alias",
        "native deliberation control",
        "serving mode",
        "evidence class",
        "provenance",
        "exclusions",
        "bounded next escalation",
        "never starts setup",
        "performs no network access",
        "writes no configuration or evidence",
    }

    _assert_contains_all(public_contract, required_fragments)
    assert "| `route` | `$HERE/help/route.md` |" in skill
    assert "/model-selector route <path>" in skill


def test_route_contract_pins_filtering_overrides_and_refusals() -> None:
    """Routing cannot approximate an unsafe or unreachable exact point."""

    contract = _read("references/model-routing.md")
    required_fragments = {
        "invalid_profile",
        "ambiguous_override",
        "unavailable_override",
        "unknown_main_seat_ceiling",
        "above_main_seat_ceiling",
        "unrepresentable_verdict_inheritance",
        "empty_safe_candidate_set",
        "locks only that dimension",
        "actual spawn capabilities",
        "concrete current-Harness adapter",
        "never interpolates, rounds, or guesses",
        "adjacency does not imply quality ordering",
        "matched evidence may prefer a lower portable level",
        "Missing evidence remains unknown",
        "external checker or declared failure signal",
        "one adjacent portable level on the same model",
        "Cash, rolling quota, weekly quota, allocated subscription cost, and latency",
    }

    _assert_contains_all(contract, required_fragments)
