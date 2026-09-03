"""Complete model-routing fixtures shared across public seam tests."""

from __future__ import annotations

from typing import Any


def standing_policy(cohorts: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Provide the shipped Standing Policy exactly as the store projects it.

    The shipped values are written out here rather than imported, so a change
    to the store's own constants has to be answered deliberately in the
    fixtures that pin what routing sees.
    """

    default = {
        "revision": 0,
        "starting_rung": "cold_start",
        "floor": "weakest_enabled",
        "ceiling": "main_seat",
        "failure_threshold": {"failures": 2, "window": 4},
        "exploration": {
            "epsilon": 0.1,
            "max_per_run": 1,
            "seed": "kntnt-standing-policy-v1",
        },
    }
    return {
        "schema_version": 1,
        "default": default,
        "cohorts": {
            cohort: default | entry for cohort, entry in sorted((cohorts or {}).items())
        },
    }


def routing_snapshot() -> dict[str, Any]:
    """Provide one frozen exact-point routing context."""

    # Describe the smallest exact-point context used by routing unit tests.
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


def complete_routing_snapshot() -> dict[str, Any]:
    """Provide a complete point and a concrete data-driven Harness adapter."""

    # Complete the configured point with exact identity and safety facts.
    snapshot = routing_snapshot()
    point = snapshot["mappings"][0]
    point.update(
        {
            "aliases": [],
            "surface": "subagent",
            "tools": ["shell", "apply_patch"],
            "policy": {"sandbox": "workspace-write", "network": "disabled"},
            "capabilities": ["routine-python"],
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

    # Freeze every mapped native control in its verified order.
    point["controls"]["low"] = {"effort": "low", "summary": "auto"}
    point["native_control_order"] = [
        point["controls"]["low"],
        point["controls"]["medium"],
        point["controls"]["high"],
        point["controls"]["xhigh"],
    ]

    # Complete the immutable main-seat identity and authority ceiling.
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

    # Freeze selection policy and remove nominal evidence from cold-start tests.
    snapshot["override_policy"].update(
        {
            "cold_start": "select",
            "quality_floor": 0.9,
            "shadow_prices": None,
            "objective": "cost_first",
            "standing_policy": standing_policy(),
        }
    )
    snapshot["evidence"]["records"] = []

    # Declare one concrete adapter and its complete native translation.
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

    # Remove the deliberately shallow legacy fixture fields.
    snapshot["harness"].pop("adapters")
    snapshot["main_seat"].pop("capability")
    point.pop("capability")
    point.pop("launch")
    return snapshot
