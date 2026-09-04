"""Public contracts shipped by the model-selector Skill."""

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal, cast
from urllib.parse import urlparse

import pytest
from support.model_routing import (
    complete_routing_snapshot as _complete_routing_snapshot,
)
from support.model_routing import standing_policy as _standing_policy_fixture

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
MODEL_SELECTOR: Path = REPO_ROOT / "skills" / "models" / "model-selector"
CONTEXT_SCRIPT: Path = MODEL_SELECTOR / "scripts" / "context.py"
PROFILE_FIXTURE: Path = REPO_ROOT / "tests" / "support" / "model_selector_profile.json"
ROUTED_OBSERVATIONS: Path = (
    REPO_ROOT / "skills" / "kntnt" / "library" / "scripts" / "routed_observations.py"
)


def _load_router() -> Any:
    """Load the shipped public routing module from its installed path."""

    path = MODEL_SELECTOR / "scripts" / "route.py"
    spec = importlib.util.spec_from_file_location("model_selector_route", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_context_module() -> Any:
    """Load Context beside the exact routing module it imports at runtime."""

    # Preserve the interpreter's module table across this isolated import.
    previous = sys.modules.get("route")
    sys.modules["route"] = _load_router()
    path = MODEL_SELECTOR / "scripts" / "context.py"
    spec = importlib.util.spec_from_file_location("model_selector_context", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if previous is None:
        del sys.modules["route"]
    else:
        sys.modules["route"] = previous
    return module


def _runtime_context_request(
    objective: str = "cost_first", **request_changes: Any
) -> dict[str, Any]:
    """Provide exact session facts beside one ordered routing request."""

    # Pin the strongest scored fixture model and its top portable control.
    request = _request()
    request.update(request_changes)
    return {
        "schema_version": 1,
        "requests": [request],
        "runtime": {
            "objective": objective,
            "harness": {
                "name": "claude-code",
                "surface": "claude-code",
                "inventory_revision": "claude-code/agent-tool",
                "inheritance": True,
                "inheritance_attestation": {
                    "carried_by_default": True,
                    "verified": "claude-code/agent-tool",
                },
            },
            "main_seat": {
                "model": "claude-opus-5",
                "surface": "claude-code",
                "serving_mode": "standard",
                "native_deliberation": {"effort": "max"},
                "portable_deliberation": "max",
                "tools": [],
                "policy": {},
            },
        },
    }


def _invoke_context(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Invoke the Context process through its shipped public CLI seam."""

    return subprocess.run(
        ["uv", "run", str(CONTEXT_SCRIPT), *arguments],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _derive_context(
    tmp_path: Path,
    artifact: dict[str, Any],
    profile: bytes | None = None,
) -> dict[str, Any]:
    """Invoke the public context process against an isolated fixture profile."""

    # Place the persisted profile and request at their public filesystem seams.
    data = tmp_path / "model-selector"
    data.mkdir(parents=True, exist_ok=True)
    if profile is None:
        profile = PROFILE_FIXTURE.read_bytes()
    if profile:
        (data / "config.json").write_bytes(profile)
    request = tmp_path / "context-request.json"
    request.write_text(json.dumps(artifact), encoding="utf-8")

    # Exercise the shipped CLI grammar rather than importing its internals.
    result = _invoke_context(f"--data={data}", str(request))
    assert result.returncode == 0, result.stdout + result.stderr
    return cast(dict[str, Any], json.loads(result.stdout))


def test_context_derives_a_routeable_claude_code_artifact(tmp_path: Path) -> None:
    """Stored selections and session facts become one accepted route context."""

    # Derive current context and feed it unchanged to the routing Interface.
    derived = _derive_context(tmp_path, _runtime_context_request())
    routed = _load_router().route(derived)

    # Assert automatic routing selected a complete shipped-adapter launch.
    assert routed["decisions"][0]["status"] == "selected"
    assert routed["decisions"][0]["launch"]["arguments"] == {"model": "haiku"}
    assert routed["snapshot"]["profile"] == {"revision": "7", "valid": True}
    assert routed["snapshot"]["override_policy"] == {
        "portable_levels": ["low", "medium", "high", "xhigh", "max"],
        "cold_start": "select",
        "quality_floor": 0.7,
        "shadow_prices": None,
        "objective": "cost_first",
        "standing_policy": _standing_policy_fixture(),
    }
    assert routed["snapshot"]["evidence"] == {
        "identity": f"sha256:{hashlib.sha256(b'[]').hexdigest()}",
        "vintage": "2026-08-23",
        "records": [],
    }
    ranks = {
        mapping["model"]: mapping["model_capability"]
        for mapping in derived["context"]["mappings"]
    }
    assert ranks == {
        "claude-haiku-4-5-20251001": 30.0,
        "claude-sonnet-5": 55.0,
        "claude-opus-5": 63.0,
        "claude-fable-5": 62.0,
        "gpt-5.6-sol": 61.0,
        "grok-4.6": 61.0,
    }
    assert all(
        set(mapping["commercial"].values()) == {None}
        for mapping in derived["context"]["mappings"]
    )
    assert (tmp_path / "model-selector" / "config.json").read_bytes() == (
        PROFILE_FIXTURE.read_bytes()
    )


def test_context_maps_observed_codex_max_and_ignores_ultra(tmp_path: Path) -> None:
    """The pinned CLI dialect launches portable controls and nothing wider."""

    # Lock the OpenAI fixture selection at the highest portable CLI value.
    derived = _derive_context(
        tmp_path,
        _runtime_context_request(
            overrides={"model": "gpt-5.6-sol", "deliberation": "max"}
        ),
    )
    routed = _load_router().route(derived)

    # Assert exact Codex syntax and the boundary below observed `ultra`.
    assert routed["decisions"][0]["launch"]["arguments"] == {
        "-m": "gpt-5.6-sol",
        "-c": "model_reasoning_effort=max",
    }
    mapping = next(
        item
        for item in derived["context"]["mappings"]
        if item["model"] == "gpt-5.6-sol"
    )
    cli = json.loads(
        (REPO_ROOT / "tests" / "support" / "codex_cli_0_152_1.json").read_text()
    )
    cli_help = (
        REPO_ROOT / "tests" / "support" / "codex_cli_0_152_1_exec_help.txt"
    ).read_text()
    cli_sol = next(item for item in cli["models"] if item["id"] == "gpt-5.6-sol")
    assert cli["version"] == "codex-cli 0.152.1"
    assert cli["config_reference"].endswith("/openai/codex/blob/main/docs/config.md")
    assert "-c, --config <key=value>" in cli_help
    assert "-m, --model <MODEL>" in cli_help
    assert "max" in mapping["controls"]
    assert "ultra" in cli_sol["supported_reasoning_levels"]
    assert "ultra" not in mapping["controls"]


def test_context_retains_uncovered_selections_and_omits_disabled_ones(
    tmp_path: Path,
) -> None:
    """Profile normalization stays auditable beyond available adapters."""

    # Derive mappings from every enabled validated selection in the fixture.
    mappings = _derive_context(tmp_path, _runtime_context_request())["context"][
        "mappings"
    ]
    models = [mapping["model"] for mapping in mappings]

    # Assert uncovered mappings remain while invalid selections do not enter.
    assert "grok-4.6" in models
    assert "gpt-5.6-luna" not in models
    assert [
        mapping["serving_mode"]
        for mapping in mappings
        if mapping["model"] == "claude-opus-5"
    ] == ["standard", "fast"]

    # Turn the disabled covered selection on but leave it unvalidated.
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    luna = next(
        selection
        for selection in profile["model_selections"]
        if selection["canonical_provider_model_id"] == "gpt-5.6-luna"
    )
    luna.update({"enabled": True, "validation_status": "pending"})
    unvalidated = _derive_context(
        tmp_path / "unvalidated",
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )["context"]["mappings"]
    assert "gpt-5.6-luna" not in {mapping["model"] for mapping in unvalidated}


def test_context_retains_seedless_and_unavailable_mode_selections(
    tmp_path: Path,
) -> None:
    """Every enabled validated profile selection stays visible for audit."""

    # Add a validated model absent from the seed and preserve its unknown rank.
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    seedless = deepcopy(profile["model_selections"][-1])
    seedless.update(
        {
            "selection_id": "seedless",
            "family": "seedless",
            "requested_model_id": "seedless-model",
            "canonical_provider_model_id": "seedless-model",
            "provider_release_id": None,
            "controls": {
                **seedless["controls"],
                "effort": {"policy": "explicit", "values": ["max"]},
            },
        }
    )
    profile["model_selections"].append(seedless)
    mappings = _derive_context(
        tmp_path / "seedless",
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )["context"]["mappings"]
    retained = next(
        mapping for mapping in mappings if mapping["model"] == "seedless-model"
    )

    # Keep the selection auditable without inventing unsupported mappings.
    assert retained["model_capability"] is None
    assert retained["controls"] == {}
    assert retained["control_capabilities"] == {}
    assert retained["native_control_order"] == []
    assert "artifact_refusal" not in _load_router().route(
        {
            "schema_version": 1,
            "context": _derive_context(
                tmp_path / "seedless-route",
                _runtime_context_request(),
                json.dumps(profile).encode(),
            )["context"],
            "requests": [_request()],
        }
    )

    # Keep an explicitly selected but unavailable serving mode unlaunchable.
    unavailable = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    grok = unavailable["model_selections"][-1]
    grok["controls"]["serving_modes"] = {
        "policy": "explicit",
        "values": ["batch"],
    }
    unavailable_mappings = _derive_context(
        tmp_path / "unavailable-mode",
        _runtime_context_request(),
        json.dumps(unavailable).encode(),
    )["context"]["mappings"]
    assert any(
        mapping["model"] == "grok-4.6" and mapping["serving_mode"] == "batch"
        for mapping in unavailable_mappings
    )


def test_context_leaves_seedless_all_supported_controls_unknown(
    tmp_path: Path,
) -> None:
    """An absent seed never invents portable controls or capability ranks."""

    # Add a seedless selection that requests only verified supported controls.
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    seedless = deepcopy(profile["model_selections"][-1])
    seedless.update(
        {
            "selection_id": "seedless-all",
            "family": "seedless-all",
            "requested_model_id": "seedless-all-model",
            "canonical_provider_model_id": "seedless-all-model",
            "provider_release_id": None,
            "controls": {
                **seedless["controls"],
                "effort": {"policy": "all_supported", "values": None},
            },
        }
    )
    profile["model_selections"].append(seedless)
    derived = _derive_context(
        tmp_path,
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )
    mapping = next(
        item
        for item in derived["context"]["mappings"]
        if item["model"] == "seedless-all-model"
    )

    # Preserve explicit unknowns in a valid, unlaunchable frozen mapping.
    assert mapping["controls"] == {}
    assert mapping["control_capabilities"] == {}
    assert mapping["native_control_order"] == []

    assert "artifact_refusal" not in _load_router().route(derived)


def test_context_omits_unsupported_explicit_control_ranks(tmp_path: Path) -> None:
    """Explicit profile intent cannot become an unsupported model mapping."""

    # Request a portable value absent from the known model's supported seed.
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    grok = profile["model_selections"][-1]
    grok["controls"]["effort"] = {"policy": "explicit", "values": ["max"]}
    mappings = _derive_context(
        tmp_path,
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )["context"]["mappings"]
    mapping = next(item for item in mappings if item["model"] == "grok-4.6")

    # Retain the selection while withholding unsupported control assertions.
    assert mapping["controls"] == {}
    assert mapping["control_capabilities"] == {}
    assert mapping["native_control_order"] == []

    # Route the isolated unavailable mapping as automatic execution work.
    context = _derive_context(
        tmp_path / "isolated",
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )["context"]
    context["mappings"] = [
        item for item in context["mappings"] if item["model"] == "grok-4.6"
    ]
    context["harness"]["adapter_specs"] = []
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": context,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Inherit with an explicit audit fact instead of refusing the empty pool.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "unavailable_selection_controls"
    assert decision["audit"]["exclusions"][0]["code"] == "mapping_unavailable"


def test_context_benchmark_coverage_counts_distinct_models() -> None:
    """Multiple channels for one model cannot outweigh wider coverage."""

    # Give an older benchmark one duplicated model and a newer one another.
    context = _load_context_module()
    model_seeds = {
        "main": {"seed_id": "model-main"},
        "candidate-a": {"seed_id": "model-a"},
        "candidate-b": {"seed_id": "model-b"},
    }
    records = [
        {"record_type": "benchmark_definition_seed", "seed_id": "alpha:1"},
        {"record_type": "benchmark_definition_seed", "seed_id": "beta:2"},
        {
            "record_type": "evaluation_prior_seed",
            "benchmark_seed_id": "alpha:1",
            "model_seed_id": "model-main",
            "score": 30,
        },
        {
            "record_type": "evaluation_prior_seed",
            "benchmark_seed_id": "alpha:1",
            "model_seed_id": "model-a",
            "score": 10,
        },
        {
            "record_type": "evaluation_prior_seed",
            "benchmark_seed_id": "beta:2",
            "model_seed_id": "model-main",
            "score": 30,
        },
        {
            "record_type": "evaluation_prior_seed",
            "benchmark_seed_id": "beta:2",
            "model_seed_id": "model-b",
            "score": 20,
        },
    ]

    # Let equal distinct coverage use the documented newest-version tiebreak.
    ranks, main_rank = context._capability_ranks(
        records,
        model_seeds,
        ["candidate-a", "candidate-a", "candidate-b"],
        "main",
    )
    assert ranks == {"candidate-a": None, "candidate-b": 20}
    assert main_rank == 30


def test_context_keeps_an_unsupported_harness_on_the_main_seat(
    tmp_path: Path,
) -> None:
    """A valid context with no matching adapter preserves inherited execution."""

    # Describe a Harness no shipped template covers at the same top-ranked seat.
    request = _runtime_context_request()
    request["runtime"]["harness"] = {
        "name": "unsupported",
        "surface": "unsupported",
        "inventory_revision": "unsupported/worker",
        "inheritance": True,
        "inheritance_attestation": {
            "carried_by_default": True,
            "verified": "unsupported/worker",
        },
    }
    request["runtime"]["main_seat"]["surface"] = "unsupported"
    decision = _load_router().route(_derive_context(tmp_path, request))["decisions"][0]

    # Assert the uncovered Harness inherits with a complete audit reason.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "unavailable_selection_controls"
    assert {item["code"] for item in decision["audit"]["exclusions"]} == {
        "adapter_unreachable"
    }


def test_context_keeps_a_missing_attestation_auditable(tmp_path: Path) -> None:
    """An unverifiable carried seam removes only its concrete adapters."""

    # Remove the live-session fact no persisted profile can honestly supply.
    request = _runtime_context_request()
    del request["runtime"]["harness"]["inheritance_attestation"]
    derived = _derive_context(tmp_path, request)

    # Retain configured Claude points while their launch seam is unavailable.
    adapters = derived["context"]["harness"]["adapter_specs"]
    mappings = derived["context"]["mappings"]
    assert not [adapter for adapter in adapters if adapter["surface"] == "agent-tool"]
    assert [mapping for mapping in mappings if mapping["surface"] == "agent-tool"]

    # A Harness that disclaims inheritance cannot validate a carried adapter.
    unsupported = _runtime_context_request()
    unsupported["runtime"]["harness"]["inheritance"] = False
    unsupported_adapters = _derive_context(tmp_path / "unsupported", unsupported)[
        "context"
    ]["harness"]["adapter_specs"]
    assert not [
        adapter
        for adapter in unsupported_adapters
        if adapter["surface"] == "agent-tool"
    ]


def test_context_treats_missing_or_invalid_profiles_as_absent(tmp_path: Path) -> None:
    """Configuration trouble inherits without setup or persistent repair."""

    # Derive from missing, malformed, and structurally invalid profiles.
    for index, profile in enumerate((b"", b"{}", b"\xff")):
        derived = _derive_context(
            tmp_path / str(index),
            _runtime_context_request(),
            profile,
        )
        decision = _load_router().route(derived)["decisions"][0]

        # Assert both absent-profile forms produce the same safe inheritance.
        assert derived["context"]["profile"] is None
        assert derived["context"]["mappings"] == []
        assert decision["status"] == "inherit"
        assert decision["inheritance"]["reason"] == "missing_profile"


def test_context_treats_dangling_profile_references_as_invalid(
    tmp_path: Path,
) -> None:
    """A selection cannot attach to an access channel that does not exist."""

    # Break one required profile relationship without changing either shape.
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    profile["model_selections"][0]["channel_id"] = "missing-channel"
    derived = _derive_context(
        tmp_path,
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )
    decision = _load_router().route(derived)["decisions"][0]

    # Reject the whole persisted profile through the absent-profile path.
    assert derived["context"]["profile"] is None
    assert derived["context"]["mappings"] == []
    assert derived["context"]["harness"]["adapter_specs"] == []
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "missing_profile"


def test_context_rejects_incomplete_channel_billing_contract(tmp_path: Path) -> None:
    """A persisted channel cannot validate without its billing-specific facts."""

    # Remove one required subscription fact from an otherwise complete profile.
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    for channel in profile["access_channels"]:
        channel.update({"region": "global", "currency": "USD", "sources": []})
        if channel["billing_type"] == "subscription":
            channel.update(
                {
                    "tier": None,
                    "billing_period": "month",
                    "recurring_amount": None,
                    "tax_treatment": None,
                    "included_overage_policy": "included_only",
                    "reset_windows": None,
                    "quota_multipliers": {},
                }
            )
        else:
            channel["rate_source"] = None
    del profile["access_channels"][0]["currency"]
    derived = _derive_context(
        tmp_path,
        _runtime_context_request(),
        json.dumps(profile).encode(),
    )

    # Assert the invalid profile follows the normal absent-profile branch.
    assert derived["context"]["profile"] is None
    assert derived["context"]["mappings"] == []


def test_context_inherits_an_unknown_main_seat_without_overrides(
    tmp_path: Path,
) -> None:
    """A main seat outside the numeric comparison never gains a fake ceiling."""

    # Use the documented seed gap with and without an exact model lock.
    automatic = _runtime_context_request()
    automatic["runtime"]["main_seat"]["model"] = "claude-fable-5-1"
    derived = _derive_context(tmp_path / "automatic", automatic)
    inherited = _load_router().route(derived)["decisions"][0]
    locked = deepcopy(automatic)
    locked["requests"][0]["overrides"] = {"model": "claude-fable-5"}
    refused = _load_router().route(_derive_context(tmp_path / "locked", locked))[
        "decisions"
    ][0]

    # Assert automation inherits while the exact override remains strict.
    assert derived["context"]["mappings"] == []
    assert derived["context"]["main_seat"]["model_capability"] is None
    assert inherited["status"] == "inherit"
    assert inherited["inheritance"]["reason"] == "unavailable_selection_controls"
    assert refused["status"] == "refused"
    assert refused["reason"]["code"] == "unknown_main_seat_ceiling"


def test_context_returns_a_valid_frozen_snapshot_unchanged(tmp_path: Path) -> None:
    """Later routing calls reuse the exact snapshot established on first call."""

    # Freeze the first derived context through the public route Interface.
    first = _derive_context(tmp_path, _runtime_context_request())
    snapshot = _load_router().route(first)["snapshot"]

    # Preserve a deliberately formatted snapshot through the process boundary.
    raw_snapshot = json.dumps(snapshot, indent=3, sort_keys=False).replace("\n", "\r\n")
    raw_requests = json.dumps([_request(request_id="build-2")])
    request = tmp_path / "frozen-context-request.json"
    request.write_text(
        f'{{"schema_version":1,"requests":{raw_requests},"snapshot":{raw_snapshot}}}',
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            "uv",
            "run",
            str(CONTEXT_SCRIPT),
            f"--data={tmp_path / 'model-selector'}",
            str(request),
        ],
        cwd=REPO_ROOT,
        text=False,
        capture_output=True,
        check=False,
    )
    later = json.loads(result.stdout)

    # Assert both the process result and embedded snapshot bytes are exact.
    assert result.returncode == 0
    assert b'"snapshot":' + raw_snapshot.encode() in result.stdout
    assert later["snapshot"] == snapshot


def test_context_refuses_a_frozen_snapshot_with_a_stale_identity(
    tmp_path: Path,
) -> None:
    """Context validates the identity of every snapshot it preserves."""

    # Mutate a valid frozen fact without regenerating its identity.
    first = _derive_context(tmp_path / "first", _runtime_context_request())
    snapshot = _load_router().route(first)["snapshot"]
    snapshot["profile"]["revision"] = "tampered"
    artifact = tmp_path / "stale-snapshot.json"
    artifact.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "requests": [_request()],
                "snapshot": snapshot,
            }
        ),
        encoding="utf-8",
    )

    # Require Context itself to refuse before Route sees the artifact.
    result = _invoke_context(str(artifact))
    refusal = json.loads(result.stdout)
    assert result.returncode == 2
    assert refusal["artifact_refusal"]["code"] == "invalid_context_input"


def test_context_refuses_a_frozen_attestation_for_another_inventory(
    tmp_path: Path,
) -> None:
    """Frozen adapter attestations retain the Harness inventory identity."""

    # Freeze a self-consistent snapshot carrying a contradictory attestation.
    first = _derive_context(tmp_path / "first", _runtime_context_request())
    router = _load_router()
    snapshot = router.route(first)["snapshot"]
    carried = next(
        adapter
        for adapter in snapshot["harness"]["adapter_specs"]
        if adapter.get("inheritance_attestation")
    )
    carried["inheritance_attestation"]["verified"] = "wrong/inventory"
    snapshot = router.freeze_context(snapshot)
    artifact = tmp_path / "wrong-attestation.json"
    artifact.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "requests": [_request()],
                "snapshot": snapshot,
            }
        ),
        encoding="utf-8",
    )

    # Require Context to reject the contradiction despite the valid digest.
    result = _invoke_context(str(artifact))
    assert result.returncode == 2
    assert json.loads(result.stdout)["artifact_refusal"]["code"] == (
        "invalid_context_input"
    )


def test_context_process_refusals_are_machine_readable(tmp_path: Path) -> None:
    """Malformed process input never escapes as a Python traceback."""

    # Exercise each filesystem and JSON failure through the installed process.
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    undecodable = tmp_path / "undecodable.json"
    undecodable.write_bytes(b"\xff")
    invocations = [
        [],
        [str(tmp_path / "absent.json")],
        [str(undecodable)],
        [str(malformed)],
        [str(invalid)],
    ]
    expected = [
        "invalid_arguments",
        "unreadable_artifact",
        "unreadable_artifact",
        "malformed_json",
        "invalid_context_input",
    ]
    for arguments, code in zip(invocations, expected, strict=True):
        result = _invoke_context(*arguments)
        refusal = json.loads(result.stdout)
        assert result.returncode == 2
        assert refusal["artifact_refusal"]["code"] == code
        assert "Traceback" not in result.stderr


def test_context_refuses_a_flag_after_its_artifact_operand(tmp_path: Path) -> None:
    """The process grammar never silently repairs out-of-order arguments."""

    # Put a valid flag after the path its synopsis requires it to precede.
    request = tmp_path / "context-request.json"
    request.write_text(json.dumps(_runtime_context_request()), encoding="utf-8")
    result = _invoke_context(str(request), f"--data={tmp_path}")

    # Assert the grammar refusal stays machine-readable.
    assert result.returncode == 2
    assert json.loads(result.stdout)["artifact_refusal"]["code"] == (
        "invalid_arguments"
    )


def test_context_refuses_inconsistent_main_seat_surface(tmp_path: Path) -> None:
    """The exact main seat cannot silently differ from its invoking Harness."""

    # Contradict the invariant that the runtime contract records twice.
    artifact = _runtime_context_request()
    artifact["runtime"]["main_seat"]["surface"] = "different"
    request = tmp_path / "context-request.json"
    request.write_text(json.dumps(artifact), encoding="utf-8")
    result = _invoke_context(str(request))

    # Assert the cross-field contradiction reaches the stable refusal seam.
    assert result.returncode == 2
    assert json.loads(result.stdout)["artifact_refusal"]["code"] == (
        "invalid_context_input"
    )


def test_context_refuses_an_attestation_for_another_inventory(tmp_path: Path) -> None:
    """One stable runtime identity governs inventory and inheritance."""

    # Contradict the duplicated stable Harness identity in the request.
    artifact = _runtime_context_request()
    artifact["runtime"]["harness"]["inheritance_attestation"]["verified"] = (
        "claude-code/different-surface"
    )
    request = tmp_path / "context-request.json"
    request.write_text(json.dumps(artifact), encoding="utf-8")

    # Refuse the contradiction at Context's public process boundary.
    result = _invoke_context(str(request))
    assert result.returncode == 2
    assert json.loads(result.stdout)["artifact_refusal"]["code"] == (
        "invalid_context_input"
    )


def test_context_schema_consts_do_not_coerce_booleans_and_numbers(
    tmp_path: Path,
) -> None:
    """Schema literals preserve JSON primitive types at the process boundary."""

    # Contradict numeric and boolean constants through Python's equality quirk.
    version = _runtime_context_request()
    version["schema_version"] = True
    attestation = _runtime_context_request()
    attestation["runtime"]["harness"]["inheritance_attestation"][
        "carried_by_default"
    ] = 1
    for index, artifact in enumerate((version, attestation)):
        request = tmp_path / f"const-{index}.json"
        request.write_text(json.dumps(artifact), encoding="utf-8")
        result = _invoke_context(str(request))

        # Refuse each coercive near-match through the same schema boundary.
        assert result.returncode == 2, index
        assert json.loads(result.stdout)["artifact_refusal"]["code"] == (
            "invalid_context_input"
        )


def _automatic_low_snapshot() -> dict[str, Any]:
    """Provide a complete snapshot whose point maps only the low control.

    Automatic requests reach every evidence branch here without an explicit
    deliberation lock, which route must never resolve into inheritance.
    """

    # Reduce the mapped, ordered, and launchable controls to the single value.
    snapshot = _complete_routing_snapshot()
    point = snapshot["mappings"][0]
    native = point["controls"]["low"]
    point["controls"] = {"low": native}
    point["control_capabilities"] = {"low": point["control_capabilities"]["low"]}
    point["native_control_order"] = [native]
    snapshot["harness"]["adapter_specs"][0]["native_controls"] = [native]
    return snapshot


def _carried_control_snapshot() -> dict[str, Any]:
    """Provide a seam that selects the model and inherits the deliberation.

    The frozen main seat carries a native value no configured control mapping
    supplies, so a decision holding that value can only have resolved it from
    the seat itself rather than from the point it launches.
    """

    # Freeze an inherited main-seat control the worker point never maps.
    snapshot = _complete_routing_snapshot()
    seat_native = {"effort": "session-inherited"}
    snapshot["main_seat"]["native_deliberation"] = seat_native

    # Replace the addressable translation with one carried by inheritance.
    adapter = snapshot["harness"]["adapter_specs"][0]
    adapter["adapter_id"] = "codex-carried-subagent"
    adapter["native_controls"] = [seat_native]
    adapter["launch"]["native_control_flags"] = {
        "effort": {"carried_by": "inheritance"}
    }
    adapter["inheritance_attestation"] = {
        "carried_by_default": True,
        "verified": "inventory-3",
    }
    return snapshot


def _ladder_mapping(
    template: dict[str, Any],
    model: str,
    capability: int,
    cash: float | None,
    levels: tuple[str, ...],
    serving_mode: str = "standard",
) -> dict[str, Any]:
    """Copy one complete configured point onto a further rung of the ladder."""

    # Reuse the template's verified native controls so one adapter reaches all.
    point = deepcopy(template)
    point.update(
        {
            "model": model,
            "model_capability": capability,
            "serving_mode": serving_mode,
            "controls": {level: template["controls"][level] for level in levels},
            "control_capabilities": {
                level: template["control_capabilities"][level] for level in levels
            },
        }
    )
    point["commercial"]["cash"] = cash
    return point


def _ladder_snapshot() -> dict[str, Any]:
    """Provide a Harness whose reachable points form a two-dimensional ladder.

    The base point leaves a gap inside its own scale, two models share the
    next capability at different cash, one of them is reached through two
    serving modes, and the capability above that is priced in one mapping and
    unknown in the other.
    """

    # Keep the complete point as the template every further rung is copied from.
    snapshot = _complete_routing_snapshot()
    base = snapshot["mappings"][0]
    template = deepcopy(base)

    # Climb from one sparse scale into equal, cheaper, and unpriced models.
    snapshot["mappings"].extend(
        [
            _ladder_mapping(template, "worker-v3", 85, 5.0, ("medium", "xhigh")),
            _ladder_mapping(template, "worker-v4", 85, 2.0, ("low", "high")),
            _ladder_mapping(
                template, "worker-v4", 85, 2.0, ("low",), serving_mode="priority"
            ),
            _ladder_mapping(template, "worker-v5", 95, None, ("low",)),
            _ladder_mapping(template, "worker-v6", 95, 7.0, ("low",)),
        ]
    )

    # Leave an unmapped level inside the scale the ladder starts on.
    base["controls"] = {level: base["controls"][level] for level in ("low", "high")}
    base["control_capabilities"] = {
        level: base["control_capabilities"][level] for level in ("low", "high")
    }

    # Let the one frozen adapter reach every model and serving mode declared.
    adapter = snapshot["harness"]["adapter_specs"][0]
    adapter["models"] = sorted({point["model"] for point in snapshot["mappings"]})
    adapter["serving_modes"] = ["standard", "priority"]
    return snapshot


def _ladder_candidates(snapshot: dict[str, Any]) -> tuple[Any, ...]:
    """Return every exact point one plain automatic request still reaches."""

    router = _load_router()
    return cast(
        tuple[Any, ...], router._candidate_pool(_request(), snapshot).candidates
    )


def _candidate_at(
    candidates: tuple[Any, ...],
    model: str,
    portable: str,
    serving_mode: str = "standard",
) -> Any:
    """Name one exact candidate on the ladder the way a reader names a rung."""

    return next(
        candidate
        for candidate in candidates
        if candidate.point["model"] == model
        and candidate.point["serving_mode"] == serving_mode
        and candidate.portable == portable
    )


def _rung_of(
    candidates: tuple[Any, ...],
    current: Any,
    direction: Literal["up", "down"] = "up",
) -> tuple[str, str, str] | None:
    """Reduce one resolved Rung to the identity a test can read."""

    rung = _load_router()._adjacent_rung(candidates, current, direction)
    if rung is None:
        return None
    return (rung.point["model"], rung.point["serving_mode"], rung.portable)


def test_adjacent_rung_climbs_the_scale_then_the_cheapest_next_model() -> None:
    """A Rung is the next mapped level, then the next model up by capability."""

    # Read the ladder from the pool one automatic request actually reaches.
    candidates = _ladder_candidates(_ladder_snapshot())

    # Assert the scale is climbed in order with its unmapped level skipped.
    assert _rung_of(candidates, _candidate_at(candidates, "worker-v2", "low")) == (
        "worker-v2",
        "standard",
        "high",
    )

    # Assert an exhausted scale steps to the cheapest mapping one capability
    # up, entered at the lowest portable value that mapping supplies.
    assert _rung_of(candidates, _candidate_at(candidates, "worker-v2", "high")) == (
        "worker-v4",
        "priority",
        "low",
    )

    # Assert a known price is preferred to one the snapshot does not know.
    assert _rung_of(candidates, _candidate_at(candidates, "worker-v4", "high")) == (
        "worker-v6",
        "standard",
        "low",
    )

    # Assert the top of the ladder offers nothing further to climb.
    assert _rung_of(candidates, _candidate_at(candidates, "worker-v6", "low")) is None


def test_adjacent_rung_descends_the_same_ladder_into_the_cheapest_model() -> None:
    """Down is the mirror, except that cost still prefers the cheaper model."""

    # Read the same ladder the upward direction climbs.
    candidates = _ladder_candidates(_ladder_snapshot())
    down: Literal["down"] = "down"

    # Assert the scale descends in order and stops at its own floor.
    assert _rung_of(
        candidates, _candidate_at(candidates, "worker-v2", "high"), down
    ) == (
        "worker-v2",
        "standard",
        "low",
    )
    assert (
        _rung_of(candidates, _candidate_at(candidates, "worker-v2", "low"), down)
        is None
    )

    # Assert a descent enters the lower model at the highest value it maps.
    assert _rung_of(
        candidates, _candidate_at(candidates, "worker-v4", "low", "priority"), down
    ) == ("worker-v2", "standard", "high")

    # Assert the cheaper known price still wins a descending tie.
    assert _rung_of(
        candidates, _candidate_at(candidates, "worker-v6", "low"), down
    ) == (
        "worker-v4",
        "priority",
        "low",
    )


def test_adjacent_rung_never_leaves_the_pool_the_request_reaches() -> None:
    """Both main-seat ceilings bound the ladder before adjacency is read."""

    # Lower the frozen model ceiling beneath every model above the first.
    snapshot = _ladder_snapshot()
    snapshot["main_seat"]["model_capability"] = 80
    candidates = _ladder_candidates(snapshot)

    # Assert an exhausted scale under that ceiling offers no model to climb.
    assert _rung_of(candidates, _candidate_at(candidates, "worker-v2", "high")) is None


def _carried_ladder_snapshot() -> dict[str, Any]:
    """Provide a carried seam with one further enabled model above its own."""

    # Add a stronger model the same inheriting adapter can also launch.
    snapshot = _carried_control_snapshot()
    template = deepcopy(snapshot["mappings"][0])
    snapshot["mappings"].append(
        _ladder_mapping(template, "worker-v3", 85, 2.0, ("low", "high"))
    )
    snapshot["harness"]["adapter_specs"][0]["models"] = ["worker-v2", "worker-v3"]
    return snapshot


def _verified_failure_binding(
    decision: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind an externally verified failure to the exact point that launched."""

    launch = decision["launch"]
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
    return prior, {
        **prior,
        "outcome": "failed",
        "checker": {"kind": "external", "signal": "pytest"},
    }


def _escalation_of(snapshot: dict[str, Any], **changes: Any) -> Any:
    """Route one request twice: once to launch, once to escalate its failure."""

    router = _load_router()
    decision = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [_request(**changes)]}
    )["decisions"][0]
    prior, verified_failure = _verified_failure_binding(decision)
    escalating = _request(
        retry_available=True,
        prior=prior,
        verified_failure=verified_failure,
        **changes,
    )
    return router.route(
        {"schema_version": 1, "context": snapshot, "requests": [escalating]}
    )["decisions"][0]["next_escalation"]


def test_route_selects_an_exact_launchable_point() -> None:
    """The public seam returns a complete Harness-native launch decision."""

    # Route one controlled workload through the public deep-module seam.
    result = _load_router().route(
        {
            "schema_version": 1,
            "context": _complete_routing_snapshot(),
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

    # Assert the complete exact point, translation, and frozen provenance.
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


def test_route_emits_only_parameter_destinations_for_a_complete_point() -> None:
    """Fixed and inherited facts stay exact without becoming arguments."""

    # Declare all destination forms on one concrete launch adapter.
    snapshot = _complete_routing_snapshot()
    adapter = snapshot["harness"]["adapter_specs"][0]
    adapter["launch"] = {
        "model_flag": {"parameter": "-m", "value": "alias-{value}"},
        "surface_flag": {"fixed": "subagent"},
        "serving_mode_flag": {"fixed": "standard"},
        "native_control_flags": {
            "effort": {
                "parameter": "-c",
                "value": "model_reasoning_effort={value}",
            },
            "summary": {"fixed": "auto"},
        },
        "tools_flag": {"carried_by": "inheritance"},
        "policy_flags": {
            "sandbox": {"fixed": "workspace-write"},
            "network": {"carried_by": "inheritance"},
        },
    }
    adapter["inheritance_attestation"] = {
        "carried_by_default": True,
        "verified": "inventory-3",
    }

    # Route through the public seam and inspect only the native launch result.
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert only the two declared parameter destinations are emitted.
    assert decision["launch"]["arguments"] == {
        "-m": "alias-worker-v2",
        "-c": "model_reasoning_effort=low",
    }

    # Make fixed native and policy facts disagree with the selected point.
    for field, value in (("summary", "detailed"), ("sandbox", "read-only")):
        mismatched = deepcopy(snapshot)
        destinations = mismatched["harness"]["adapter_specs"][0]["launch"]
        group = "native_control_flags" if field == "summary" else "policy_flags"
        destinations[group][field] = {"fixed": value}
        refusal = _load_router().route(
            {
                "schema_version": 1,
                "context": mismatched,
                "requests": [_request(overrides={"deliberation": "low"})],
            }
        )["decisions"][0]

        # Assert the mismatched fixed value makes the adapter unreachable.
        assert refusal["status"] == "refused"
        assert refusal["audit"]["exclusions"][0]["code"] == "adapter_unreachable"


def test_route_rejects_carried_facts_that_differ_from_the_main_seat() -> None:
    """A carried destination completes only the seat's exact inherited fact."""

    # Exercise every generalized non-control destination against a mismatch.
    for field in ("model", "surface", "serving_mode", "tools", "policy"):
        snapshot = _complete_routing_snapshot()
        adapter = snapshot["harness"]["adapter_specs"][0]
        adapter["inheritance_attestation"] = {
            "carried_by_default": True,
            "verified": "inventory-3",
        }
        carried = {"carried_by": "inheritance"}
        if field == "model":
            adapter["launch"]["model_flag"] = carried
        elif field == "surface":
            adapter["launch"]["surface_flag"] = carried
            snapshot["main_seat"]["surface"] = "main-seat"
        elif field == "serving_mode":
            adapter["launch"]["serving_mode_flag"] = carried
            snapshot["main_seat"]["serving_mode"] = "fast"
        elif field == "tools":
            adapter["launch"]["tools_flag"] = carried
            snapshot["main_seat"]["tools"] = []
        else:
            adapter["launch"]["policy_flags"]["sandbox"] = carried
            snapshot["main_seat"]["policy"]["sandbox"] = "read-only"

        # Route each complete inherited mismatch through the public seam.
        decision = _load_router().route(
            {
                "schema_version": 1,
                "context": snapshot,
                "requests": [_request(overrides={"deliberation": "low"})],
            }
        )["decisions"][0]

        # Assert each inherited mismatch makes the adapter unreachable.
        assert decision["status"] == "refused", field
        assert decision["audit"]["exclusions"][0]["code"] == ("adapter_unreachable")


def test_route_compares_fixed_and_carried_json_values_by_type() -> None:
    """Boolean and numeric point values never compare as the same JSON fact."""

    # Give both destination forms the numeric counterpart of a boolean point.
    for destination in (
        {"fixed": 1},
        {"carried_by": "inheritance"},
    ):
        snapshot = _complete_routing_snapshot()
        point = snapshot["mappings"][0]
        point["policy"]["toggle"] = True
        adapter = snapshot["harness"]["adapter_specs"][0]
        adapter["policies"] = [deepcopy(point["policy"])]
        adapter["launch"]["policy_flags"]["toggle"] = destination
        adapter["inheritance_attestation"] = {
            "carried_by_default": True,
            "verified": "inventory-3",
        }
        snapshot["main_seat"]["policy"]["toggle"] = 1

        # Reject both mismatches through the public routing seam.
        decision = _load_router().route(
            {
                "schema_version": 1,
                "context": snapshot,
                "requests": [_request(overrides={"deliberation": "low"})],
            }
        )["decisions"][0]
        assert decision["status"] == "refused", destination
        assert decision["audit"]["exclusions"][0]["code"] == ("adapter_unreachable")


def test_route_compares_adapter_facts_as_exact_json_values() -> None:
    """Adapter membership cannot coerce booleans into supported numbers."""

    # Give the point a boolean policy fact and the adapter numeric support.
    snapshot = _complete_routing_snapshot()
    point = snapshot["mappings"][0]
    point["policy"]["toggle"] = True
    adapter = snapshot["harness"]["adapter_specs"][0]
    supported = deepcopy(point["policy"])
    supported["toggle"] = 1
    adapter["policies"] = [supported]
    adapter["launch"]["policy_flags"]["toggle"] = "toggle"

    # Reject the unsupported exact point before argument translation.
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    assert decision["status"] == "refused"
    assert decision["audit"]["exclusions"][0]["code"] == "adapter_unreachable"


def test_route_validates_native_order_as_exact_json_values() -> None:
    """A frozen mapping cannot coerce a native boolean into a number."""

    # Contradict one mapped native value only through Python's equality quirk.
    snapshot = _complete_routing_snapshot()
    point = snapshot["mappings"][0]
    point["controls"] = {"low": {"toggle": True}}
    point["control_capabilities"] = {"low": 1}
    point["native_control_order"] = [{"toggle": 1}]

    # Refuse the structurally valid but cross-field-inexact snapshot.
    response = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )
    assert response["decisions"][0]["status"] == "refused"
    assert response["decisions"][0]["reason"]["code"] == "invalid_snapshot"


def test_context_specializes_every_generalized_model_destination() -> None:
    """Template specialization accepts every schema-valid destination form."""

    # Prepare one shipped selection, template, and exact live runtime.
    context = _load_context_module()
    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    selection = next(
        item
        for item in profile["model_selections"]
        if item["selection_id"] == "claude-opus"
    )
    template = json.loads(
        (MODEL_SELECTOR / "data" / "adapters" / "claude-code-agent.json").read_text(
            encoding="utf-8"
        )
    )
    runtime = _runtime_context_request()["runtime"]
    controls = {"max": {"effort": "max"}}
    canonical = selection["canonical_provider_model_id"]

    # Specialize every valid model destination without assuming a dictionary.
    for destination in (
        "model",
        {"parameter": "model"},
        {"fixed": canonical},
        {"carried_by": "inheritance"},
    ):
        candidate = deepcopy(template)
        candidate["launch"]["model_flag"] = destination
        specialized = context._specialized_adapter(
            candidate,
            selection,
            "standard",
            controls,
            runtime,
        )
        assert specialized is not None, destination

    # Attach an attestation whenever any launch field is carried.
    portable = json.loads(
        (
            MODEL_SELECTOR / "data" / "adapters" / "claude-code-codex-exec.json"
        ).read_text(encoding="utf-8")
    )
    portable["launch"]["tools_flag"] = {"carried_by": "inheritance"}
    codex = next(
        item
        for item in profile["model_selections"]
        if item["selection_id"] == "codex-sol"
    )
    specialized = context._specialized_adapter(
        portable,
        codex,
        "standard",
        controls,
        runtime,
    )
    assert specialized is not None
    assert (
        specialized["inheritance_attestation"]
        == (runtime["harness"]["inheritance_attestation"])
    )


def test_route_inherits_an_empty_mapping_set_before_an_unknown_ceiling() -> None:
    """Unavailable selection data leaves an automatic request on its seat."""

    # Represent a valid context with no comparable or launchable selections.
    snapshot = _complete_routing_snapshot()
    snapshot["mappings"] = []
    snapshot["main_seat"]["model_capability"] = None

    # Route the automatic request through the same public artifact boundary.
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert the unavailable selection controls inherit before ceiling checks.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "unavailable_selection_controls"


def test_route_audits_an_unranked_mapping_before_inheriting() -> None:
    """An incomparable configured model stays visible but never launches."""

    # Keep the mapping complete while withholding only its comparable rank.
    snapshot = _complete_routing_snapshot()
    snapshot["mappings"][0]["model_capability"] = None

    # Resolve the automatic request and retain the unavailable-rank reason.
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert the missing rank remains explicit in the inheritance audit.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "unavailable_selection_controls"
    assert decision["audit"]["exclusions"][0]["code"] == ("capability_rank_unavailable")


def test_route_refuses_an_override_against_an_unranked_empty_pool() -> None:
    """An exact lock never falls through to a generic empty-set refusal."""

    # Keep the matching configured point visible but unavailable to comparison.
    snapshot = _complete_routing_snapshot()
    snapshot["mappings"][0]["model_capability"] = None
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    # Assert an explicit lock receives its override-specific refusal.
    assert decision["status"] == "refused"
    assert decision["reason"]["code"] == "unavailable_override"
    assert decision["audit"]["exclusions"][0]["code"] == ("capability_rank_unavailable")


def test_route_uses_a_complete_harness_adapter_and_point_fingerprint() -> None:
    """Reachability, translation, and identity cover every launch-relevant fact."""

    # Resolve a nominal complete point through its concrete adapter.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    decision = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert every translated launch field and audit identity.
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

    # Add a model whose mismatched tool set makes its adapter unreachable.
    filtered = _complete_routing_snapshot()
    unreachable_point = deepcopy(filtered["mappings"][0])
    unreachable_point.update({"model": "worker-v3", "tools": ["browser"]})
    filtered["mappings"].append(unreachable_point)
    filtered["harness"]["adapter_specs"][0]["models"].append("worker-v3")
    filtered_decision = router.route(
        {
            "schema_version": 1,
            "context": filtered,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert selection and audit share the hard-filter authority.
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

    # Mutate the only point to prove incomplete adapter matches are refused.
    changed_tools = _complete_routing_snapshot()
    changed_tools["mappings"][0]["tools"] = ["shell"]
    unreachable = router.route(
        {
            "schema_version": 1,
            "context": changed_tools,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert no partial launch instruction escapes the adapter filter.
    assert unreachable["status"] == "refused"
    assert unreachable["reason"]["code"] == "unavailable_override"
    assert unreachable["audit"]["exclusions"][0]["code"] == "adapter_unreachable"

    # Collide model and native destinations in an otherwise complete adapter.
    colliding = _complete_routing_snapshot()
    colliding["harness"]["adapter_specs"][0]["launch"]["model_flag"] = (
        "reasoning_effort"
    )
    collision = router.route(
        {
            "schema_version": 1,
            "context": colliding,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert one argument destination can never overwrite another field.
    assert collision["status"] == "refused"
    assert collision["reason"]["code"] == "unavailable_override"
    assert collision["audit"]["exclusions"][0]["code"] == "adapter_unreachable"

    # Resolve launch-policy and non-launch commercial mutations separately.
    changed_policy = _complete_routing_snapshot()
    changed_policy["mappings"][0]["policy"]["sandbox"] = "read-only"
    changed_commercial = _complete_routing_snapshot()
    changed_commercial["mappings"][0]["commercial"]["cash"] = 99.0
    policy_decision = router.route(
        {
            "schema_version": 1,
            "context": changed_policy,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    commercial_decision = router.route(
        {
            "schema_version": 1,
            "context": changed_commercial,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert only launch-relevant changes alter the point fingerprint.
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

    # Remove the lowest mapping and resolve automatic selection again.
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
            "context": missing_automatic,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert automatic routing excludes rather than guesses the missing value.
    assert automatic["status"] == "selected"
    assert automatic["launch"]["portable_deliberation"] == "medium"

    # Supply an unverified max value outside the frozen native order.
    unverified_max = _complete_routing_snapshot()
    unverified_max["mappings"][0]["controls"]["max"] = {
        "effort": "maximum",
        "summary": "detailed",
    }
    max_decision = router.route(
        {
            "schema_version": 1,
            "context": unverified_max,
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )["decisions"][0]

    # Assert invalid native ordering is refused before selection.
    assert max_decision["status"] == "refused"
    assert max_decision["reason"]["code"] == "invalid_snapshot"

    # Lower only the main seat's deliberation ceiling and lock above it.
    deliberation_ceiling = _complete_routing_snapshot()
    deliberation_ceiling["main_seat"]["deliberation_capability"] = 2
    above_deliberation = router.route(
        {
            "schema_version": 1,
            "context": deliberation_ceiling,
            "requests": [_request(overrides={"deliberation": "high"})],
        }
    )["decisions"][0]

    # Assert the deliberation dimension independently enforces authority.
    assert above_deliberation["status"] == "refused"
    assert above_deliberation["reason"]["code"] == "above_main_seat_ceiling"

    # Raise the worker model above the independent main-seat model ceiling.
    model_ceiling = _complete_routing_snapshot()
    model_ceiling["mappings"][0]["model_capability"] = 101
    above_model = router.route(
        {
            "schema_version": 1,
            "context": model_ceiling,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    # Assert the model dimension independently enforces authority.
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

    # Route verdict and execution authority in one deliberately ordered batch.
    verdict = _request(request_id="verdict", authority="verdict", stage="verify")
    execution = _request(request_id="execution")
    decisions = _load_router().route(
        {
            "schema_version": 1,
            "context": _complete_routing_snapshot(),
            "requests": [verdict, execution],
        }
    )["decisions"]

    # Assert order, exact inheritance, and launch-shape discrimination.
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

    # Resolve exact low and high controls before attaching matched evidence.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    snapshot["mappings"][0]["commercial"]["allocated_subscription_cost"] = 1.0
    snapshot["mappings"][0]["controls"] = {
        portable: snapshot["mappings"][0]["controls"][portable]
        for portable in ("low", "high")
    }
    snapshot["mappings"][0]["control_capabilities"] = {"low": 1, "high": 3}
    snapshot["mappings"][0]["native_control_order"] = list(
        snapshot["mappings"][0]["controls"].values()
    )
    snapshot["harness"]["adapter_specs"][0]["native_controls"] = list(
        snapshot["mappings"][0]["controls"].values()
    )
    low = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [
                _request(overrides={"model": "worker-v2", "deliberation": "low"})
            ],
        }
    )["decisions"][0]
    high = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [
                _request(overrides={"model": "worker-v2", "deliberation": "high"})
            ],
        }
    )["decisions"][0]
    observed = {
        "cash": 1.0,
        "rolling_quota": 2.0,
        "weekly_quota": 3.0,
        "allocated_subscription_cost": 1.0,
        "latency": 4.0,
    }
    snapshot["evidence"]["records"] = [
        _measurement_record(low, commercial=dict(observed)),
        _measurement_record(
            high,
            quality=0.9,
            uncertainty={"lower_bound": 0.9, "upper_bound": 0.92},
            commercial=dict(observed),
        ),
    ]

    # Lock only the model and let measured quality choose deliberation.
    result = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    # Assert lower deliberation wins without a monotonic quality assumption.
    assert result["launch"]["model"] == "worker-v2"
    assert result["launch"]["portable_deliberation"] == "low"
    assert result["evidence_class"] == "measurement_based"


def test_route_freezes_max_native_value_in_the_fingerprint() -> None:
    """Max resolves from the snapshot and changes exact-point identity."""

    # Resolve max once, then construct a later valid native maximum.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    first = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
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

    # Reuse the first snapshot and independently route the later context.
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
            "context": changed,
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )

    # Assert reuse is stable while a new native maximum changes identity.
    assert first["decisions"] == reused["decisions"]
    assert first["decisions"][0]["launch"]["native_deliberation"] == {"effort": "xhigh"}
    assert (
        first["decisions"][0]["launch"]["configuration_fingerprint"]
        != later["decisions"][0]["launch"]["configuration_fingerprint"]
    )


def test_route_emits_only_a_bounded_adjacent_escalation() -> None:
    """Only one fully bound, launchable, below-seat retry may escalate."""

    # Resolve the exact prior attempt and bind an externally verified failure.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    selected = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )["decisions"][0]
    prior, verified_failure = _verified_failure_binding(selected)
    request = _request(
        retry_available=True,
        prior=prior,
        verified_failure=verified_failure,
    )
    escalation = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [request]}
    )["decisions"][0]["next_escalation"]

    # Assert the one adjacent step is complete and consumes an existing retry.
    assert selected["launch"]["portable_deliberation"] == "low"
    assert escalation["model"] == "worker-v2"
    assert escalation["portable_deliberation"] == "medium"
    assert escalation["native_deliberation"] == {"effort": "medium"}
    assert escalation["configuration_fingerprint"].startswith("sha256:")
    assert escalation["arguments"]["reasoning_effort"] == "medium"
    assert escalation["consumes_existing_retry"] is True

    # Enumerate retry, point, native-control, and checker binding failures.
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

    # Assert every mismatched predecessor suppresses escalation.
    for mismatch in mismatches:
        changed_request = deepcopy(request)
        changed_request.update(mismatch)
        decision = router.route(
            {
                "schema_version": 1,
                "context": snapshot,
                "requests": [changed_request],
            }
        )["decisions"][0]
        assert decision["next_escalation"] is None, mismatch

    # Assert a request that pinned the deliberation itself climbs nothing.
    assert _escalation_of(snapshot, overrides={"deliberation": "low"}) is None

    # Lower the main-seat ceiling beneath the otherwise valid adjacent step.
    bounded = deepcopy(snapshot)
    bounded["main_seat"]["deliberation_capability"] = 1
    bounded_decision = router.route(
        {"schema_version": 1, "context": bounded, "requests": [request]}
    )["decisions"][0]

    # Assert escalation applies the same complete authority ceiling.
    assert bounded_decision["next_escalation"] is None


def test_route_inherits_without_a_profile_or_discriminating_evidence() -> None:
    """Absence and honest uncertainty never trigger setup or invented facts."""

    # Route independently with absent profile and inheritance-only cold start.
    snapshot = _complete_routing_snapshot()
    snapshot["profile"] = None
    absent = _load_router().route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]
    snapshot = _complete_routing_snapshot()
    snapshot["evidence"]["records"] = []
    snapshot["override_policy"]["cold_start"] = "inherit"
    uncertain = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(reversible=False, checker={"kind": "none"})],
        }
    )["decisions"][0]

    # Assert both safe inheritance reasons remain explicit and distinct.
    assert absent["status"] == "inherit"
    assert absent["inheritance"]["reason"] == "missing_profile"
    assert uncertain["status"] == "inherit"
    assert uncertain["inheritance"]["reason"] == "insufficient_evidence"


def test_route_inherits_when_automatic_execution_lacks_selection_controls() -> None:
    """An inherited Harness still provides fresh-context delegation safely."""

    # Remove every explicit launch adapter while retaining inherited subagents.
    snapshot = _complete_routing_snapshot()
    snapshot["harness"]["adapter_specs"] = []
    decision = _load_router().route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]

    # Preserve delegation without falsely claiming exact launch controls exist.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "unavailable_selection_controls"
    assert "launch" not in decision
    assert decision["audit"]["exclusions"] == [
        {
            "code": "adapter_unreachable",
            "detail": "No active adapter can launch every field of this point.",
            "model": "worker-v2",
            "portable_deliberation": portable,
        }
        for portable in ("low", "medium", "high", "xhigh", "max")
    ]


def test_route_launches_a_deliberation_control_the_harness_carries() -> None:
    """A control the Harness applies by inheritance completes the exact point."""

    # Route automatic execution across a seam that selects only the model.
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": _carried_control_snapshot(),
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert the launch names the seat's exact control and emits no flag for it.
    launch = decision["launch"]
    assert decision["status"] == "selected"
    assert launch["adapter_id"] == "codex-carried-subagent"
    assert launch["native_deliberation"] == {"effort": "session-inherited"}
    assert launch["portable_deliberation"] == "xhigh"
    assert launch["arguments"] == {
        "model": "worker-v2",
        "surface": "subagent",
        "service_tier": "standard",
        "tools": ["shell", "apply_patch"],
        "sandbox": "workspace-write",
        "network": "disabled",
    }


def test_route_binds_carried_evidence_to_the_seat_it_resolved() -> None:
    """The fingerprint follows the frozen seat, and evidence accrues to it."""

    # Route once and feed that decision's own exact measurement back in.
    router = _load_router()
    snapshot = _carried_control_snapshot()
    artifact = {
        "schema_version": 1,
        "context": snapshot,
        "requests": [_request()],
    }
    decision = router.route(deepcopy(artifact))["decisions"][0]
    measured = deepcopy(snapshot)
    measured["evidence"]["records"] = [_measurement_record(decision)]
    remeasured = router.route(
        {"schema_version": 1, "context": measured, "requests": [_request()]}
    )["decisions"][0]

    # Route the same point again after only the inherited seat value moved.
    moved = deepcopy(snapshot)
    moved_native = {"effort": "session-inherited-max"}
    moved["main_seat"]["native_deliberation"] = moved_native
    moved["harness"]["adapter_specs"][0]["native_controls"] = [moved_native]
    moved_decision = router.route(
        {"schema_version": 1, "context": moved, "requests": [_request()]}
    )["decisions"][0]

    # Assert evidence binds to the carried configuration and only to it.
    fingerprint = decision["launch"]["configuration_fingerprint"]
    assert remeasured["evidence_class"] == "measurement_based"
    assert remeasured["launch"]["configuration_fingerprint"] == fingerprint
    assert moved_decision["launch"]["native_deliberation"] == moved_native
    assert moved_decision["launch"]["configuration_fingerprint"] != fingerprint


def test_route_refuses_a_carried_mapping_without_its_attestation() -> None:
    """An unverified claim about a Harness cannot complete a point."""

    # Remove only the declaring session's attestation from the same adapter.
    snapshot = _carried_control_snapshot()
    del snapshot["harness"]["adapter_specs"][0]["inheritance_attestation"]
    decision = _load_router().route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]

    # Assert the mapping alone launches nothing and stays visibly unreachable.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "unavailable_selection_controls"
    assert "launch" not in decision
    assert {exclusion["code"] for exclusion in decision["audit"]["exclusions"]} == {
        "adapter_unreachable"
    }


def test_route_refuses_a_lock_on_a_control_inheritance_carries() -> None:
    """A carried dimension is not one a request can lock."""

    # Lock each dimension separately across the same carried seam.
    router = _load_router()
    snapshot = _carried_control_snapshot()
    locked = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    model_locked = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    # Assert the carried lock refuses while the addressable lock still selects.
    assert locked["status"] == "refused"
    assert locked["reason"]["code"] == "unavailable_override"
    assert {exclusion["code"] for exclusion in locked["audit"]["exclusions"]} == {
        "carried_control_not_selectable"
    }
    assert model_locked["status"] == "selected"
    assert model_locked["launch"]["native_deliberation"] == {
        "effort": "session-inherited"
    }


def test_route_escalates_into_the_next_model_along_a_carried_control() -> None:
    """Where the seat alone decides deliberation, the model is the step."""

    # Route the seam that inherits its control and has a model above it.
    router = _load_router()
    snapshot = _carried_ladder_snapshot()
    decision = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]

    # Assert the cold start still holds the weakest model at the seat's value.
    assert decision["status"] == "selected"
    assert decision["launch"]["model"] == "worker-v2"
    assert decision["launch"]["portable_deliberation"] == "xhigh"

    # Assert the retry the caller owns steps into the next model up, launching
    # at the inherited deliberation it carries rather than a value it claims.
    escalation = _escalation_of(snapshot)
    assert escalation["model"] == "worker-v3"
    assert escalation["adapter_id"] == "codex-carried-subagent"
    assert escalation["portable_deliberation"] == "xhigh"
    assert escalation["native_deliberation"] == {"effort": "session-inherited"}
    assert escalation["configuration_fingerprint"].startswith("sha256:")
    assert "reasoning_effort" not in escalation["arguments"]
    assert escalation["consumes_existing_retry"] is True

    # Assert the same seam with no model above it emits no rung at all.
    assert _escalation_of(_carried_control_snapshot()) is None


def test_route_keeps_the_ladder_inside_an_explicit_model_lock() -> None:
    """A locked model bounds the pool, so no Rung climbs out of it."""

    # Exhaust the first model's scale at the one level it maps.
    snapshot = _ladder_snapshot()
    base = snapshot["mappings"][0]
    base["controls"] = {"low": base["controls"]["low"]}
    base["control_capabilities"] = {"low": base["control_capabilities"]["low"]}

    # Assert the same exhausted scale steps into the next model when free.
    assert _escalation_of(snapshot)["model"] == "worker-v4"

    # Assert the lock leaves that step outside the points the request reaches.
    assert _escalation_of(snapshot, overrides={"model": "worker-v2"}) is None


def test_route_emits_no_rung_under_a_deliberation_lock_in_either_dimension() -> None:
    """A pinned deliberation is the caller's own value, not a rung to leave."""

    # Route a ladder whose next model is reachable at the locked level itself.
    snapshot = _ladder_snapshot()
    locked = {"deliberation": "low"}
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides=locked)],
        }
    )["decisions"][0]

    # Assert the lock holds the exact level it names on the weakest model.
    assert decision["launch"]["model"] == "worker-v2"
    assert decision["launch"]["portable_deliberation"] == "low"

    # Assert the same failure climbs a model when free and nothing when locked.
    assert _escalation_of(snapshot)["model"] == "worker-v2"
    assert _escalation_of(snapshot, overrides=locked) is None


def test_route_cold_starts_the_work_its_contract_promises_a_heuristic() -> None:
    """The documented cold start runs under exactly the guards it states."""

    # Decline unmeasured automatic cold starts in the frozen override policy.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    snapshot["override_policy"]["cold_start"] = "inherit"
    checked = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]
    consequential = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(reversible=False, checker={"kind": "none"})],
        }
    )["decisions"][0]

    # Assert reversible checked work starts weak while the rest still inherits.
    assert checked["status"] == "selected"
    assert checked["evidence_class"] == "heuristic"
    assert checked["launch"]["portable_deliberation"] == "low"
    assert consequential["status"] == "inherit"
    assert consequential["inheritance"]["reason"] == "insufficient_evidence"


def test_route_refuses_a_locked_request_that_could_only_inherit() -> None:
    """An inherited launch carries no controls, so a lock must refuse instead.

    Every graceful inheritance branch delegates without explicit model or
    deliberation arguments. Returning one for a request that locks a dimension
    would silently execute the user's exact instruction on the main seat.
    """

    # Build one controlled snapshot for every inheritance branch a lock reaches.
    router = _load_router()
    absent = _complete_routing_snapshot()
    absent["profile"] = None
    unreachable = _complete_routing_snapshot()
    unreachable["harness"]["adapter_specs"] = []
    cases: list[tuple[str, dict[str, Any], dict[str, Any]]] = [
        ("missing profile with a locked model", absent, {"model": "worker-v2"}),
        ("missing profile with a locked level", absent, {"deliberation": "low"}),
        ("unavailable controls with a lock", unreachable, {"deliberation": "low"}),
    ]

    # Exclude the only candidate's exact evidence beneath the quality floor.
    below_floor = _complete_routing_snapshot()
    locked = _request(overrides={"model": "worker-v2", "deliberation": "low"})
    selected = router.route(
        {"schema_version": 1, "context": below_floor, "requests": [locked]}
    )["decisions"][0]
    below_floor["evidence"]["records"] = [
        _measurement_record(
            selected,
            quality=0.82,
            uncertainty={"lower_bound": 0.8, "upper_bound": 0.84},
        )
    ]
    cases.append(
        (
            "known failing evidence with a lock",
            below_floor,
            {"model": "worker-v2", "deliberation": "low"},
        )
    )

    # Measure one of two locked-level candidates and leave the other unknown.
    mixed = _complete_routing_snapshot()
    second = deepcopy(mixed["mappings"][0])
    second.update({"model": "worker-v3", "model_capability": 80})
    mixed["mappings"].append(second)
    mixed["harness"]["adapter_specs"][0]["models"].append("worker-v3")
    mixed["evidence"]["records"] = [
        _measurement_record(
            router.route({"schema_version": 1, "context": mixed, "requests": [locked]})[
                "decisions"
            ][0]
        )
    ]
    cases.append(("mixed evidence with a locked level", mixed, {"deliberation": "low"}))

    # Assert every locked branch refuses without launching or inheriting.
    for label, snapshot, overrides in cases:
        decision = router.route(
            {
                "schema_version": 1,
                "context": snapshot,
                "requests": [_request(overrides=overrides)],
            }
        )["decisions"][0]
        assert decision["status"] == "refused", label
        assert "launch" not in decision, label
        assert "inheritance" not in decision, label


def test_route_names_the_blocked_lock_in_its_refusal_detail() -> None:
    """A refused lock stays auditable instead of becoming an unexplained stop."""

    # Refuse an explicit model that no configured profile can resolve.
    snapshot = _complete_routing_snapshot()
    snapshot["profile"] = None
    decision = _load_router().route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    # Assert the stable override code and the branch that blocked the lock.
    assert decision["reason"]["code"] == "unavailable_override"
    assert "missing_profile" in decision["reason"]["detail"]


def test_route_still_inherits_when_execution_locks_nothing() -> None:
    """Automatic dimensions keep every documented graceful inheritance branch."""

    # Route the same branches without any explicit field lock.
    router = _load_router()
    absent = _complete_routing_snapshot()
    absent["profile"] = None
    unreachable = _complete_routing_snapshot()
    unreachable["harness"]["adapter_specs"] = []
    expected = {
        "missing_profile": absent,
        "unavailable_selection_controls": unreachable,
    }

    # Assert absence and unavailable controls still delegate with fresh context.
    for reason, snapshot in expected.items():
        decision = router.route(
            {"schema_version": 1, "context": snapshot, "requests": [_request()]}
        )["decisions"][0]
        assert decision["status"] == "inherit", reason
        assert decision["inheritance"]["reason"] == reason
        assert "launch" not in decision


def test_route_refuses_every_unsafe_family_without_launch_arguments() -> None:
    """Invalid, unavailable, unsafe, and empty states fail before launch."""

    # Build one controlled case for every stable unsafe-state family.
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
    verdict = _complete_routing_snapshot()
    verdict["harness"]["inheritance"] = False
    cases.append(
        (verdict, _request(authority="verdict"), "unrepresentable_verdict_inheritance")
    )

    # Assert every family refuses through the public seam without a launch.
    for snapshot, request, expected in cases:
        decision = _load_router().route(
            {"schema_version": 1, "context": snapshot, "requests": [request]}
        )["decisions"][0]
        assert decision["status"] == "refused"
        assert decision["reason"]["code"] == expected
        assert "launch" not in decision


def test_recommend_renders_a_refusal_without_claiming_an_exploration_start() -> None:
    """A refused route remains an honest non-selection in human output."""

    # Adapt an unavailable exact model through the human recommendation seam.
    recommendation = _load_router().recommend(
        {
            "schema_version": 1,
            "context": _complete_routing_snapshot(),
            "requests": [_request(overrides={"model": "missing"})],
        }
    )["recommendations"][0]

    # Assert the banner explains the shared refusal without proposing a launch.
    assert recommendation["decision"]["status"] == "refused"
    assert recommendation["evidence_banner"]["text"] == "🔵 INGEN REKOMMENDATION"
    assert recommendation["evidence_banner"]["classification_reason"] == (
        "unavailable_override"
    )
    assert recommendation["evidence_banner"]["recommendation_kind"] == "no_selection"
    assert recommendation["experiment_brief"] is None


def test_route_derives_a_snapshot_once_and_resolves_exact_aliases() -> None:
    """Current inputs become a reusable snapshot before alias resolution."""

    # Route caller-derived current context through the public freezing seam.
    router = _load_router()
    context = _complete_routing_snapshot()
    context["mappings"][0]["aliases"] = ["worker-latest"]
    original = deepcopy(context)
    frozen = router.freeze_context(context)
    result = router.route(
        {
            "schema_version": 1,
            "context": context,
            "requests": [_request(overrides={"model": "worker-latest"})],
        }
    )

    # Assert the snapshot is frozen before its exact alias resolves.
    assert context == original
    assert result["snapshot"] == frozen
    assert result["snapshot"]["snapshot_identity"].startswith("sha256:")
    assert result["decisions"][0]["launch"]["model"] == "worker-v2"
    assert result["decisions"][0]["launch"]["resolved_alias"] == "worker-latest"


def test_route_refuses_invalid_snapshots_and_ambiguous_aliases() -> None:
    """Unreproducible context and non-exact aliases are never guessed."""

    # Route a structurally incomplete snapshot and one ambiguous alias set.
    invalid = _complete_routing_snapshot()
    invalid.pop("commercial_facts", None)
    invalid.pop("mappings")
    invalid_response = _load_router().route(
        {"schema_version": 1, "context": invalid, "requests": [_request()]}
    )
    ambiguous = _complete_routing_snapshot()
    ambiguous["mappings"][0]["aliases"] = ["worker-latest"]
    duplicate = deepcopy(ambiguous["mappings"][0])
    duplicate["model"] = "worker-v3"
    ambiguous["mappings"].append(duplicate)
    ambiguous_decision = _load_router().route(
        {
            "schema_version": 1,
            "context": ambiguous,
            "requests": [_request(overrides={"model": "worker-latest"})],
        }
    )["decisions"][0]

    # Assert both shared-state failures refuse at their correct boundary.
    assert invalid_response["artifact_refusal"]["code"] == "invalid_snapshot"
    assert invalid_response["decisions"] == []
    assert ambiguous_decision["reason"]["code"] == "ambiguous_override"


def test_route_cli_is_machine_readable_and_does_not_modify_its_input(
    tmp_path: Path,
) -> None:
    """The shipped process seam emits JSON while leaving local state untouched."""

    # Persist one valid canonical artifact and retain its original bytes.
    artifact = tmp_path / "route.json"
    artifact.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "context": _complete_routing_snapshot(),
                "requests": [_request()],
            }
        ),
        encoding="utf-8",
    )
    before = artifact.read_bytes()

    # Execute the packaged script through its declared uv runtime.
    completed = subprocess.run(
        ["uv", "run", str(MODEL_SELECTOR / "scripts" / "route.py"), str(artifact)],
        check=True,
        capture_output=True,
        text=True,
    )

    # Assert machine output and the route's read-only boundary.
    assert json.loads(completed.stdout)["decisions"][0]["status"] == "selected"
    assert completed.stderr == ""
    assert artifact.read_bytes() == before


def test_route_cli_returns_stable_artifact_refusals_without_tracebacks(
    tmp_path: Path,
) -> None:
    """Arguments, paths, JSON, and envelope errors remain machine-readable."""

    # Build one process-boundary artifact for every CLI failure family.
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

    # Assert each failure has the same stable no-traceback process shape.
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


def test_route_rejects_non_finite_numbers_at_direct_and_cli_seams(
    tmp_path: Path,
) -> None:
    """Python-only NaN and infinity values never enter the JSON contract."""

    # Submit every non-finite float through the direct public seam.
    router = _load_router()
    for value in (float("nan"), float("inf"), float("-inf")):
        context = _complete_routing_snapshot()
        context["mappings"][0]["commercial"]["cash"] = value
        response = router.route(
            {"schema_version": 1, "context": context, "requests": [_request()]}
        )
        assert response["artifact_refusal"]["code"] == "invalid_snapshot"

    # Persist Python's permissive NaN token and invoke the machine seam.
    context = _complete_routing_snapshot()
    context["mappings"][0]["commercial"]["cash"] = float("nan")
    artifact = tmp_path / "non-finite.json"
    artifact.write_text(
        json.dumps({"schema_version": 1, "context": context, "requests": [_request()]}),
        encoding="utf-8",
    )
    completed = subprocess.run(
        ["uv", "run", str(MODEL_SELECTOR / "scripts" / "route.py"), str(artifact)],
        check=False,
        capture_output=True,
        text=True,
    )

    # Assert a stable refusal containing only strict JSON numeric syntax.
    assert completed.returncode == 2
    assert json.loads(completed.stdout)["artifact_refusal"]["code"] == (
        "invalid_snapshot"
    )
    assert "NaN" not in completed.stdout
    assert "Infinity" not in completed.stdout


def test_route_and_recommend_refuse_malformed_envelopes_without_exceptions() -> None:
    """Both public seams preserve stable artifact refusals for invalid envelopes."""

    # Prepare malformed shared context and a malformed top-level batch.
    router = _load_router()
    artifacts = [
        {"schema_version": 1, "snapshot": [], "requests": [_request()]},
        {"schema_version": 1, "requests": []},
    ]

    # Resolve both public forms through each invalid envelope.
    for artifact in artifacts:
        routed = router.route(artifact)
        recommended = router.recommend(artifact)

        # Assert the human adapter preserves the compact refusal exactly.
        assert routed["artifact_refusal"]["code"] == "invalid_request"
        assert recommended["artifact_refusal"] == routed["artifact_refusal"]
        assert recommended["recommendations"] == []


def test_route_outputs_conform_to_the_shipped_response_schema() -> None:
    """Every public result family satisfies the versioned response contract."""

    # Produce selected, inherited, refused, and artifact-level responses.
    router = _load_router()
    context = _complete_routing_snapshot()
    missing_profile = deepcopy(context)
    missing_profile["profile"] = None
    responses = [
        router.route(
            {"schema_version": 1, "context": context, "requests": [_request()]}
        ),
        router.route(
            {
                "schema_version": 1,
                "context": missing_profile,
                "requests": [_request()],
            }
        ),
        router.route(
            {
                "schema_version": 1,
                "context": context,
                "requests": [_request(overrides={"model": "missing"})],
            }
        ),
        router.route({"schema_version": 1, "requests": []}),
    ]

    # Resolve the response schema's external request-snapshot reference.
    for response in responses:
        errors = router._schema_errors(
            response,
            router.RESPONSE_SCHEMA,
            router.RESPONSE_SCHEMA,
            "response",
        )
        assert errors == []

    # Prove the validator enforces the refusal branch's empty decision bound.
    invalid_refusal = deepcopy(responses[-1])
    invalid_refusal["decisions"].append(responses[0]["decisions"][0])
    errors = router._schema_errors(
        invalid_refusal,
        router.RESPONSE_SCHEMA,
        router.RESPONSE_SCHEMA,
        "response",
    )
    assert errors


def test_route_labels_stale_measurements_mixed_and_keeps_costs_separate() -> None:
    """Staleness remains visible and commercial dimensions are not collapsed."""

    # Bind stale evidence to one otherwise exact selected configuration.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    selected = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]
    snapshot["evidence"]["records"] = [_measurement_record(selected, stale=True)]
    decision = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["decisions"][0]

    # Assert staleness and each independent commercial fact remain visible.
    assert decision["evidence_class"] == "mixed"
    assert decision["launch"]["commercial"] == {
        "cash": 1.0,
        "rolling_quota": 2.0,
        "weekly_quota": 3.0,
        "allocated_subscription_cost": None,
        "latency": 4.0,
    }

    # Adapt the same stale record through the human recommendation seam.
    recommendation = router.recommend(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"deliberation": "low"})],
        }
    )["recommendations"][0]

    # Assert presentation cannot revive inapplicable evidence.
    assert recommendation["uncertainty"]["status"] == "unknown"


def test_route_requires_exact_representative_evidence_for_measurement_class() -> None:
    """Partial, stale, uncertain, or weak evidence never becomes green."""

    # Derive one exact representative record from a selected launch point.
    router = _load_router()
    snapshot = _automatic_low_snapshot()
    snapshot["evidence"]["records"] = []
    explicit = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )["decisions"][0]
    exact = _measurement_record(explicit)
    snapshot["evidence"]["records"] = [exact]

    # Route the exact record as the positive measurement-based control.
    measured = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert exact applicability alone earns the production evidence class.
    assert measured["status"] == "selected"
    assert measured["evidence_class"] == "measurement_based"

    # Mutate every decision-relevant applicability and quality-floor dimension.
    partial_records = [
        {**exact, "stale": True},
        {**exact, "stage": "verify"},
        {**exact, "channel": "gateway"},
        {**exact, "native_deliberation": {"effort": "medium"}},
        {**exact, "representative": False},
        {**exact, "coverage": {"decision_relevant": False}},
        {**exact, "uncertainty": None},
    ]

    # Assert every partial record remains visibly mixed rather than green.
    for partial in partial_records:
        changed = deepcopy(snapshot)
        changed["evidence"]["records"] = [partial]
        decision = router.route(
            {
                "schema_version": 1,
                "context": changed,
                "requests": [_request()],
            }
        )["decisions"][0]
        assert decision["status"] == "selected"
        assert decision["evidence_class"] == "mixed", partial

    # Keep an exact conservative failure out of heuristic selection.
    below_floor = deepcopy(snapshot)
    below_floor["evidence"]["records"] = [
        {
            **exact,
            "uncertainty": {"lower_bound": 0.82, "upper_bound": 0.96},
        }
    ]
    failing = router.route(
        {
            "schema_version": 1,
            "context": below_floor,
            "requests": [_request()],
        }
    )["decisions"][0]
    assert failing["status"] == "inherit"
    assert failing["inheritance"]["reason"] == "quality_floor_not_cleared"

    # Move the record to an unrelated workload cohort.
    unrelated = deepcopy(snapshot)
    unrelated["evidence"]["records"] = [
        {**exact, "workload_cohort": "typescript-frontend"}
    ]
    heuristic = router.route(
        {
            "schema_version": 1,
            "context": unrelated,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert unrelated evidence remains unknown and heuristic.
    assert heuristic["status"] == "selected"
    assert heuristic["evidence_class"] == "heuristic"


def test_route_keeps_unmeasured_candidates_unknown_beside_measurements() -> None:
    """A measured point cannot dominate a candidate with unknown evidence."""

    # Configure two launchable models at one locked deliberation value.
    router = _load_router()
    context = _automatic_low_snapshot()
    second = deepcopy(context["mappings"][0])
    second.update({"model": "worker-v3", "model_capability": 80})
    context["mappings"].append(second)
    context["harness"]["adapter_specs"][0]["models"].append("worker-v3")

    # Bind representative evidence to only the first candidate.
    first = router.route(
        {
            "schema_version": 1,
            "context": context,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]
    context["evidence"]["records"] = [_measurement_record(first)]

    # Route both models without pretending the unknown candidate is dominated.
    decision = router.route(
        {
            "schema_version": 1,
            "context": context,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert honest inheritance and an explicit missing-evidence audit fact.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "insufficient_evidence"
    assert decision["audit"]["exclusions"][-1]["code"] == "missing_exact_evidence"

    # Adapt the same incomplete coverage without hiding the unknown candidate.
    recommendation = router.recommend(
        {
            "schema_version": 1,
            "context": context,
            "requests": [_request()],
        }
    )["recommendations"][0]
    assert recommendation["uncertainty"]["status"] == "mixed"
    assert {
        candidate["status"] for candidate in recommendation["uncertainty"]["candidates"]
    } == {"measured", "unknown"}


def test_route_excludes_exact_evidence_known_below_the_quality_floor() -> None:
    """A known failing point cannot re-enter selection as a heuristic."""

    # Resolve one exact candidate before attaching failing evidence.
    router = _load_router()
    context = _automatic_low_snapshot()
    request = _request()
    selected = router.route(
        {"schema_version": 1, "context": context, "requests": [request]}
    )["decisions"][0]
    context["evidence"]["records"] = [
        _measurement_record(
            selected,
            quality=0.82,
            uncertainty={"lower_bound": 0.8, "upper_bound": 0.84},
        )
    ]

    # Route again through the same exact point and quality policy.
    decision = router.route(
        {"schema_version": 1, "context": context, "requests": [request]}
    )["decisions"][0]

    # Assert the known failing evidence yields inheritance rather than launch.
    assert decision["status"] == "inherit"
    assert decision["inheritance"]["reason"] == "quality_floor_not_cleared"
    assert decision["audit"]["exclusions"][-1]["code"] == "quality_floor_not_cleared"

    # Adapt the inherited point without discarding its measured interval.
    recommendation = router.recommend(
        {"schema_version": 1, "context": context, "requests": [request]}
    )["recommendations"][0]
    assert recommendation["uncertainty"]["status"] == "measured"
    assert recommendation["uncertainty"]["candidates"][0]["lower_bound"] == 0.8
    assert recommendation["uncertainty"]["candidates"][0]["upper_bound"] == 0.84


def test_route_requires_snapshot_identity_but_freezes_current_context() -> None:
    """Only returned snapshots may bypass current-context derivation."""

    # Submit identical unsigned facts through frozen and current-context fields.
    router = _load_router()
    unsigned = _complete_routing_snapshot()
    refused = router.route(
        {"schema_version": 1, "snapshot": unsigned, "requests": [_request()]}
    )
    derived = router.route(
        {"schema_version": 1, "context": unsigned, "requests": [_request()]}
    )

    # Mutate one returned snapshot without changing its frozen identity.
    tampered = deepcopy(derived["snapshot"])
    tampered["profile"]["revision"] = "profile-8"
    mismatch = router.route(
        {"schema_version": 1, "snapshot": tampered, "requests": [_request()]}
    )

    # Assert only current context is signed and stale signatures are refused.
    assert refused["artifact_refusal"]["code"] == "invalid_snapshot"
    assert refused["decisions"] == []
    assert derived["decisions"][0]["status"] == "selected"
    assert derived["snapshot"]["snapshot_identity"].startswith("sha256:")
    assert mismatch["decisions"][0]["reason"]["code"] == "invalid_snapshot"


def test_route_cold_start_uses_workload_safety_before_economics() -> None:
    """Safe exploration starts weak; unchecked irreversible work starts strong."""

    # Configure weak and strong launchable points without matched measurements.
    router = _load_router()
    snapshot = _complete_routing_snapshot()
    stronger = deepcopy(snapshot["mappings"][0])
    stronger.update({"model": "worker-v3", "model_capability": 90})
    snapshot["mappings"].append(stronger)
    snapshot["harness"]["adapter_specs"][0]["models"].append("worker-v3")

    # Route checked reversible and unchecked irreversible work independently.
    safe = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]
    consequential = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [
                _request(
                    reversible=False,
                    checker={"kind": "none"},
                )
            ],
        }
    )["decisions"][0]

    # Assert workload safety chooses opposite cold-start endpoints.
    assert safe["launch"]["model"] == "worker-v2"
    assert safe["launch"]["portable_deliberation"] == "low"
    assert consequential["launch"]["model"] == "worker-v3"
    assert consequential["launch"]["portable_deliberation"] == "max"
    assert consequential["evidence_class"] == "heuristic"


def test_route_cold_start_filters_by_explicit_workload_requirements() -> None:
    """Cold-start strength follows frozen workload capability facts."""

    # Freeze distinct categorical workload support on weak and strong points.
    snapshot = _complete_routing_snapshot()
    stronger = deepcopy(snapshot["mappings"][0])
    stronger.update(
        {
            "model": "worker-v3",
            "model_capability": 90,
            "capabilities": ["routine-python", "architecture"],
        }
    )
    snapshot["mappings"].append(stronger)
    snapshot["harness"]["adapter_specs"][0]["models"].append("worker-v3")
    artifact = {
        "schema_version": 1,
        "context": snapshot,
        "requests": [
            _request(request_id="routine", required_capabilities=["routine-python"]),
            _request(request_id="architecture", required_capabilities=["architecture"]),
        ],
    }

    # Route routine and architectural requirements through one ordered batch.
    decisions = _load_router().route(artifact)["decisions"]

    # Assert the requirement filter precedes weakest-capable selection.
    assert [decision["launch"]["model"] for decision in decisions] == [
        "worker-v2",
        "worker-v3",
    ]
    assert decisions[1]["audit"]["exclusions"][0]["code"] == (
        "workload_capability_mismatch"
    )


def test_route_uses_pareto_costs_and_only_explicit_shadow_prices() -> None:
    """Separate commercial dimensions prevent an invented universal winner."""

    # Configure two exact points with opposing commercial dimensions.
    router = _load_router()
    snapshot = _automatic_low_snapshot()
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

    # Resolve each exact point before binding representative measurements.
    first_decision = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]
    second_decision = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v3"})],
        }
    )["decisions"][0]
    snapshot["evidence"]["records"] = [
        _measurement_record(
            first_decision,
            quality=0.94,
            uncertainty={"lower_bound": 0.92, "upper_bound": 0.96},
            commercial=deepcopy(first["commercial"]),
        ),
        _measurement_record(
            second_decision,
            quality=0.96,
            uncertainty={"lower_bound": 0.94, "upper_bound": 0.98},
            commercial=deepcopy(second["commercial"]),
        ),
    ]

    # Route without a conversion policy across the two-point frontier.
    ambiguous = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert the frozen objective takes the cheapest measured point.
    assert ambiguous["status"] == "selected"
    assert ambiguous["launch"]["model"] == "worker-v2"
    assert ambiguous["audit"]["decision_policy"] == "cost_first"
    assert len(ambiguous["audit"]["frontier"]) == 2

    # Reverse the objective and take the fastest measured point instead.
    fast = deepcopy(snapshot)
    fast["override_policy"]["objective"] = "time_first"
    hurried = router.route(
        {
            "schema_version": 1,
            "context": fast,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert only the objective changed which of the two points is chosen.
    assert hurried["status"] == "selected"
    assert hurried["launch"]["model"] == "worker-v3"
    assert hurried["audit"]["decision_policy"] == "time_first"

    # Leave both objectives without an order by tying both of their axes.
    tied = deepcopy(snapshot)
    for record in tied["evidence"]["records"]:
        record["commercial"] = {**record["commercial"], "cash": 1.0, "latency": 4.0}

    # Adapt the unresolved measured frontier with its explicit quality rubric.
    unresolved = router.recommend(
        {
            "schema_version": 1,
            "context": tied,
            "requests": [
                _request(
                    rubric={"kind": "binary", "pass_condition": "pytest passes"},
                )
            ],
        }
    )["recommendations"][0]

    # Assert unresolved evidence retains an executable measurement path.
    assert unresolved["decision"]["status"] == "inherit"
    assert unresolved["evidence_banner"]["class"] == "mixed"
    assert "STARTPUNKT" not in unresolved["evidence_banner"]["text"]
    assert unresolved["evidence_banner"]["classification_reason"] == (
        "underdetermined_frontier"
    )
    assert unresolved["evidence_banner"]["missing_evidence"]
    assert unresolved["evidence_banner"]["recommendation_kind"] == "no_selection"
    assert unresolved["uncertainty"]["status"] == "measured"
    assert len(unresolved["uncertainty"]["candidates"]) == 2
    assert {
        candidate["lower_bound"]
        for candidate in unresolved["uncertainty"]["candidates"]
    } == {0.92, 0.94}
    assert unresolved["experiment_brief"]["rubric"] == {
        "kind": "binary",
        "pass_condition": "pytest passes",
    }
    assert unresolved["experiment_brief"]["record_import"]["command"] == (
        "/model-selector record <path>"
    )

    # Make the second point demonstrably worse on quality and every cost axis.
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
            "commercial": deepcopy(dominated["mappings"][1]["commercial"]),
        }
    )
    dominant = router.route(
        {
            "schema_version": 1,
            "context": dominated,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert exact Pareto dominance selects the sole frontier point.
    assert dominant["status"] == "selected"
    assert dominant["launch"]["model"] == "worker-v2"

    # Supply a complete explicit shadow-price policy for every non-cash axis.
    priced = deepcopy(snapshot)
    priced["override_policy"]["shadow_prices"] = {
        "rolling_quota": 1.0,
        "weekly_quota": 0.1,
        "allocated_subscription_cost": 0.1,
        "latency": 0.1,
    }
    selected = router.route(
        {
            "schema_version": 1,
            "context": priced,
            "requests": [_request()],
        }
    )["decisions"][0]

    # Assert only the explicit conversion policy resolves the tradeoff.
    assert selected["status"] == "selected"
    assert selected["launch"]["model"] == "worker-v3"
    assert selected["launch"]["commercial"] == snapshot["mappings"][1]["commercial"]
    assert selected["audit"]["decision_policy"] == "explicit_shadow_prices"

    # Adapt the same measured decision into the detailed human form.
    recommendation = router.recommend(
        {
            "schema_version": 1,
            "context": priced,
            "requests": [_request()],
        }
    )["recommendations"][0]

    # Assert presentation retains the shared point, frontier, and uncertainty.
    assert recommendation["decision"] == selected
    assert recommendation["evidence_banner"]["class"] == "measurement_based"
    assert recommendation["frontier_neighbors"][0]["model"] == "worker-v2"
    assert recommendation["uncertainty"] == {
        "status": "measured",
        "lower_bound": 0.94,
        "upper_bound": 0.98,
    }
    assert recommendation["experiment_brief"] is None


def test_objective_order_resolves_a_subscription_seat_and_names_its_gaps() -> None:
    """An unpriced seat orders by Rung; a half-measured frontier orders not at all."""

    # Configure two exact points a subscription seat exposes no cash for.
    router = _load_router()
    snapshot = _automatic_low_snapshot()
    first = snapshot["mappings"][0]
    second = deepcopy(first)
    second.update({"model": "worker-v3", "model_capability": 80})
    snapshot["mappings"].append(second)
    snapshot["harness"]["adapter_specs"][0]["models"].append("worker-v3")

    # Resolve each exact point before binding representative measurements.
    decisions = [
        router.route(
            {
                "schema_version": 1,
                "context": snapshot,
                "requests": [_request(overrides={"model": model})],
            }
        )["decisions"][0]
        for model in ("worker-v2", "worker-v3")
    ]
    unpriced = {
        "cash": None,
        "rolling_quota": None,
        "weekly_quota": None,
        "allocated_subscription_cost": None,
        "latency": 9.0,
    }
    snapshot["evidence"]["records"] = [
        _measurement_record(decisions[0], commercial=dict(unpriced)),
        _measurement_record(
            decisions[1],
            quality=0.96,
            uncertainty={"lower_bound": 0.94, "upper_bound": 0.98},
            commercial={**unpriced, "latency": 3.0},
        ),
    ]

    # Order a wholly unpriced frontier by the cheaper Rung under the default.
    thrifty = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]

    # Assert the weaker Rung wins without any cash ever being exposed.
    assert thrifty["status"] == "selected"
    assert thrifty["launch"]["model"] == "worker-v2"
    assert thrifty["audit"]["decision_policy"] == "cost_first_rung_order"

    # Reverse the objective and let the measured time decide instead.
    hurried = deepcopy(snapshot)
    hurried["override_policy"]["objective"] = "time_first"
    quickest = router.route(
        {"schema_version": 1, "context": hurried, "requests": [_request()]}
    )["decisions"][0]

    # Assert the faster point wins where nothing separates the two on cash.
    assert quickest["status"] == "selected"
    assert quickest["launch"]["model"] == "worker-v3"
    assert quickest["audit"]["decision_policy"] == "time_first"

    # Price exactly one of the two points and leave the other as it was.
    partial = deepcopy(snapshot)
    partial["evidence"]["records"][1]["commercial"]["cash"] = 2.0
    halved = router.route(
        {"schema_version": 1, "context": partial, "requests": [_request()]}
    )["decisions"][0]

    # Assert a dimension only some points measured orders nothing at all.
    assert halved["status"] == "inherit"
    assert halved["inheritance"]["reason"] == "objective_metrics_missing"
    assert len(halved["audit"]["frontier"]) == 2

    # Withhold the measured time from one point and keep the cash on both.
    timeless = deepcopy(snapshot)
    for record, cash in zip(timeless["evidence"]["records"], (1.0, 2.0)):
        record["commercial"] |= {"cash": cash}
    timeless["evidence"]["records"][0]["commercial"]["latency"] = None
    untimed = router.route(
        {"schema_version": 1, "context": timeless, "requests": [_request()]}
    )["decisions"][0]

    # Assert an unmeasured time leaves even the cash-first order unusable.
    assert untimed["status"] == "inherit"
    assert untimed["inheritance"]["reason"] == "objective_metrics_missing"


def test_recommend_preserves_budget_and_renewal_selection_in_shared_core() -> None:
    """Human economic constraints select through the same exact routing core."""

    # Configure points whose route and renewal cost order is reversed.
    router = _load_router()
    snapshot = _automatic_low_snapshot()
    first = snapshot["mappings"][0]
    first["commercial"].update({"cash": 1.0, "allocated_subscription_cost": 5.0})
    second = deepcopy(first)
    second.update(
        {
            "model": "worker-v3",
            "model_capability": 80,
            "commercial": {
                **first["commercial"],
                "cash": 2.0,
                "allocated_subscription_cost": 2.0,
            },
        }
    )
    snapshot["mappings"].append(second)
    snapshot["harness"]["adapter_specs"][0]["models"].append("worker-v3")

    # Resolve exact fingerprints before adding representative evidence.
    first_decision = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]
    second_decision = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [_request(overrides={"model": "worker-v3"})],
        }
    )["decisions"][0]
    snapshot["evidence"]["records"] = [
        _measurement_record(first_decision),
        _measurement_record(second_decision),
    ]

    # Express route and renewal floors through the shared structured request.
    route_request = _request(
        economics={"decision": "route", "quality_floor": 0.9},
    )
    renew_request = _request(
        request_id="renew",
        economics={"decision": "renew", "quality_floor": 0.9},
    )
    budget_request = _request(
        request_id="budget",
        economics={"decision": "route", "budget": 1.5},
    )
    decision_only_request = _request(
        request_id="decision-only",
        economics={"decision": "route"},
    )

    # Resolve the same economic batch through compact and human forms.
    routed = router.route(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [
                route_request,
                renew_request,
                budget_request,
                decision_only_request,
            ],
        }
    )["decisions"]
    recommended = router.recommend(
        {
            "schema_version": 1,
            "context": snapshot,
            "requests": [
                route_request,
                renew_request,
                budget_request,
                decision_only_request,
            ],
        }
    )["recommendations"]

    # Assert each dimension chooses correctly without presentation drift.
    assert [decision["launch"]["model"] for decision in routed[:3]] == [
        "worker-v2",
        "worker-v3",
        "worker-v2",
    ]
    assert [item["decision"] for item in recommended] == routed
    assert [decision["audit"]["decision_policy"] for decision in routed[:3]] == [
        "quality_floor_cash",
        "quality_floor_allocated_subscription_cost",
        "budget_cash",
    ]
    assert routed[3]["status"] == "inherit"
    assert routed[3]["inheritance"]["reason"] == "objective_metrics_missing"


def test_route_and_recommend_share_selection_but_not_presentation() -> None:
    """Both public forms adapt one exact selection result without semantic drift."""

    # Prepare one heuristic exact-point artifact for both public adapters.
    router = _load_router()
    artifact = {
        "schema_version": 1,
        "context": _complete_routing_snapshot(),
        "requests": [_request(overrides={"deliberation": "low"})],
    }

    # Resolve compact and detailed forms from independent artifact copies.
    route_result = router.route(deepcopy(artifact))
    recommend_result = router.recommend(deepcopy(artifact))
    recommendation = recommend_result["recommendations"][0]

    # Assert shared semantics and the human-only evidence presentation.
    assert recommendation["decision"] == route_result["decisions"][0]
    assert recommendation["evidence_banner"] == {
        "class": "heuristic",
        "text": "🔵 HEURISTISK STARTPUNKT",
        "confidence": "low",
        "classification_reason": "Representative exact-point measurements did not determine the selected point.",
        "missing_evidence": [
            "representative exact-point evidence clearing the quality floor"
        ],
        "recommendation_kind": "exploration_start",
        "production_recommendation": False,
    }
    assert recommendation["frontier_neighbors"] == []
    assert recommendation["uncertainty"]["status"] == "unknown"
    fingerprints = recommendation["experiment_brief"]["configuration_fingerprints"]
    assert fingerprints == [
        route_result["decisions"][0]["launch"]["configuration_fingerprint"]
    ]
    assert recommendation["experiment_brief"]["checker"] == {
        "kind": "external",
        "signal": "pytest",
    }
    assert recommendation["experiment_brief"]["sequential_plan"]
    assert recommendation["experiment_brief"]["parallel_plan"]


def _recommendation_of(snapshot: dict[str, Any], **changes: Any) -> Any:
    """Return the whole recommendation one request actually receives."""

    return _load_router().recommend(
        {
            "schema_version": 1,
            "context": deepcopy(snapshot),
            "requests": [_request(**changes)],
        }
    )["recommendations"][0]


def _brief_of(snapshot: dict[str, Any], **changes: Any) -> Any:
    """Return the experiment brief one recommended request actually receives."""

    return _recommendation_of(snapshot, **changes)["experiment_brief"]


def _brief_rungs(
    snapshot: dict[str, Any], brief: dict[str, Any], **changes: Any
) -> list[tuple[str, str]]:
    """Name every point one brief lists the way a reader names a Rung."""

    router = _load_router()
    pool = router._candidate_pool(_request(**changes), deepcopy(snapshot))
    _, bounded = router._standing_policy(_request(**changes), deepcopy(snapshot), pool)
    by_fingerprint = {
        router._candidate_fingerprint(candidate, snapshot): (
            candidate.point["model"],
            candidate.portable,
        )
        for candidate in bounded.candidates
    }
    return [
        by_fingerprint.get(fingerprint, ("outside-the-bounded-pool", fingerprint))
        for fingerprint in brief["configuration_fingerprints"]
    ]


def test_experiment_brief_names_no_point_a_deliberation_lock_forbids() -> None:
    """A lock is not a Rung, so the brief has nothing to compare (ADR-0146)."""

    # Lock the weakest level on a ladder whose own scale runs further up.
    snapshot = _complete_routing_snapshot()
    locked = {"deliberation": "low"}
    brief = _brief_of(snapshot, overrides=locked)

    # Assert the brief names the launch point alone, as the escalation does.
    assert _brief_rungs(snapshot, brief, overrides=locked) == [("worker-v2", "low")]
    assert _escalation_of(snapshot, overrides=locked) is None


def test_experiment_brief_reaches_the_next_model_along_a_carried_control() -> None:
    """Where the seat carries deliberation, the comparable point is a model."""

    # Recommend the seam that inherits its control and has a model above it.
    snapshot = _carried_ladder_snapshot()
    brief = _brief_of(snapshot)

    # Assert the brief climbs the same Rung the routing escalation climbs.
    assert _brief_rungs(snapshot, brief) == [
        ("worker-v2", "xhigh"),
        ("worker-v3", "xhigh"),
    ]
    assert _escalation_of(snapshot)["model"] == "worker-v3"


def test_experiment_brief_stays_inside_a_cohort_ceiling_when_inherited() -> None:
    """The inherited brief reads the pool the Standing Policy left, too."""

    # Decline the unmeasured cold start so the decision inherits with a brief.
    snapshot = _ladder_snapshot()
    snapshot["override_policy"]["cold_start"] = "inherit"
    snapshot["override_policy"]["standing_policy"] = _standing_policy_fixture(
        {
            "python-refactor": {
                "ceiling": {"model": "worker-v2", "portable_deliberation": "low"}
            }
        }
    )
    unchecked = {"checker": {"kind": "none"}}
    brief = _brief_of(snapshot, **unchecked)

    # Assert the ceiling bounds the brief exactly as it bounds the selection.
    assert _brief_rungs(snapshot, brief, **unchecked) == [("worker-v2", "low")]


def test_experiment_brief_says_plainly_when_it_has_nothing_to_compare() -> None:
    """A brief that reaches one point plans for one point and says so."""

    # Contrast a locked request with the same ladder left free to escalate.
    snapshot = _ladder_snapshot()
    alone = _brief_of(snapshot, overrides={"deliberation": "low"}, retry_available=True)
    paired = _brief_of(snapshot, retry_available=True)

    # Assert both plans state the absence rather than promising a comparison.
    assert len(alone["configuration_fingerprints"]) == 1
    assert "nothing to compare" in alone["sequential_plan"]
    assert "nothing to compare" in alone["parallel_plan"]

    # Assert the run bound keeps its derivation: one point, one owned retry.
    assert alone["run_bound"] == 2

    # Assert a brief that does reach a second point still plans to compare.
    assert len(paired["configuration_fingerprints"]) == 2
    assert "nothing to compare" not in paired["sequential_plan"]
    assert "nothing to compare" not in paired["parallel_plan"]
    assert paired["run_bound"] == 4


def test_a_pinned_deliberation_never_reaches_the_inherited_brief_path() -> None:
    """Neither route to an inherited brief survives a pinned deliberation.

    The inherited path appends from the bounded pool without asking the shared
    resolver, so a lock reaching it would name a point at the level the lock
    forbids (ADR-0146). It carries no guard of its own because nothing reaches
    it under a lock: verdict authority keeps its overrides but inherits for a
    reason that emits no brief, and evidence-driven inheritance resolves an
    exact point as soon as a lock is present. This test fails the day either
    of those two facts changes.
    """

    router = _load_router()

    # Inherit on the one authority whose overrides survive: no brief at all.
    snapshot = _ladder_snapshot()
    verdict = _recommendation_of(
        snapshot, authority="verdict", overrides={"deliberation": "low"}
    )
    assert verdict["decision"]["status"] == "inherit"
    reason = verdict["decision"]["inheritance"]["reason"]
    assert reason == "verdict_authority"
    assert reason not in router.EVIDENCE_INHERITANCE_REASONS
    assert verdict["experiment_brief"] is None

    # Pin the deliberation where the same snapshot would otherwise inherit.
    unmeasured = _ladder_snapshot()
    unmeasured["override_policy"]["cold_start"] = "inherit"
    unchecked = {"checker": {"kind": "none"}}
    locked = _recommendation_of(
        unmeasured, overrides={"deliberation": "low"}, **unchecked
    )

    # Assert the lock resolves an exact point, so the selected guard answers it.
    assert locked["decision"]["status"] == "selected"
    assert len(locked["experiment_brief"]["configuration_fingerprints"]) == 1
    assert "nothing to compare" in locked["experiment_brief"]["sequential_plan"]

    # Assert the very same snapshot does reach the inherited path unlocked.
    free = _recommendation_of(unmeasured, **unchecked)
    assert free["decision"]["status"] == "inherit"
    assert free["decision"]["inheritance"]["reason"] in (
        router.EVIDENCE_INHERITANCE_REASONS
    )
    assert len(free["experiment_brief"]["configuration_fingerprints"]) == 2


def test_route_totally_validates_nested_snapshot_and_request_families() -> None:
    """Malformed nested state becomes detailed refusals rather than exceptions."""

    # Enumerate malformed values across every shared snapshot family.
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

    # Assert malformed shared state receives one schema-valid artifact refusal.
    for family, malformed in snapshot_changes:
        snapshot = _complete_routing_snapshot()
        snapshot[family] = malformed
        response = _load_router().route(
            {"schema_version": 1, "context": snapshot, "requests": [_request()]}
        )
        assert response["artifact_refusal"]["code"] == "invalid_snapshot", family
        assert response["artifact_refusal"]["detail"], family
        assert response["snapshot"] is None, family
        assert response["decisions"] == [], family

    # Enumerate malformed values across every nested request family.
    request_changes: list[tuple[str, Any]] = [
        ("request_id", 7),
        ("checker", []),
        ("overrides", []),
        ("prior", []),
        ("verified_failure", []),
    ]

    # Assert one bad request cannot erase or corrupt its valid batch peer.
    for family, malformed in request_changes:
        invalid_request = _request(request_id="invalid")
        invalid_request[family] = malformed
        decisions = _load_router().route(
            {
                "schema_version": 1,
                "context": _complete_routing_snapshot(),
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
        "escalate exactly one adjacent Rung",
        "strongest plausible enabled configuration",
        "refuse unsafe exploration",
    }
    public_rules = {
        "weakest plausibly capable enabled model",
        "lowest plausibly sufficient supported reasoning control",
        "one adjacent Rung",
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
        "isolated agents run the listed configurations against the same frozen task and checker",
        "the same Rung routing escalates along",
        "there is nothing to compare it against",
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
        "unavailable_selection_controls",
        "locks only that dimension",
        "selected exactly or refused, never inherited",
        "reserved for automatic dimensions",
        "actual spawn capabilities",
        "concrete current-Harness adapter",
        "never interpolates, rounds, or guesses",
        "adjacency does not imply quality ordering",
        "matched evidence may prefer a lower portable level",
        "Missing evidence remains unknown",
        "external checker or declared failure signal",
        "the next model up by `model_capability`",
        "Cash, rolling quota, weekly quota, allocated subscription cost, and latency",
    }

    _assert_contains_all(contract, required_fragments)


def test_route_contract_pins_the_carried_control_and_its_cold_start() -> None:
    """A dimension inheritance decides is stated by the contract, not implied."""

    contract = _read("references/model-routing.md")
    required_fragments = {
        "carried by inheritance",
        "emits no launch argument",
        "different fact from a missing mapping",
        "inheritance_attestation",
        "verified against what the Harness actually does",
        "carried_control_not_selectable",
        "the Harness carries the deliberation control and no adapter addresses it",
        "override_policy.cold_start",
        "Reversible, objectively checked work takes the heuristic",
    }

    _assert_contains_all(contract, required_fragments)


def _load_observations() -> Any:
    """Load the shipped public observation module from its installed path."""

    path = MODEL_SELECTOR / "scripts" / "observations.py"
    spec = importlib.util.spec_from_file_location("model_selector_observations", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _routed_decision(**changes: Any) -> dict[str, Any]:
    """Return one exact selected decision from the shared routing fixtures."""

    decisions = _load_router().route(
        {
            "schema_version": 1,
            "context": _complete_routing_snapshot(),
            "requests": [_request(**changes)],
        }
    )["decisions"]
    return cast(dict[str, Any], decisions[0])


def _attempt(**changes: Any) -> dict[str, Any]:
    """Build one completed routed attempt with an externally judged outcome."""

    attempt = {
        "attempt_id": "build-96",
        "session_identity": "run-4f21",
        "task_identity": "ticket-96",
        "workload_stratum": "initial_build",
        "attempt_index": 1,
        "stage": "build",
        "workload_cohort": "python-refactor",
        "workload_tags": ["python"],
        "harness": {"name": "codex", "inventory_revision": "inventory-3"},
        "benchmark": {
            "key": "orchestrate-ticket-v1",
            "name": "orchestrate-ticket",
            "version": "1",
            "cohort": "python-refactor",
            "tags": ["python"],
        },
        "decision": _routed_decision(),
        "outcome": {
            "result": "pass",
            "authority": "independent_verifier",
            "checker": {"identity": "verify.md", "independent": True},
            "condition": None,
            "scores": {"quality": 1.0},
        },
        "resolution": {"model": "worker-v2", "fallback_from": None},
        "started_at": "2026-08-24T10:00:00Z",
        "completed_at": "2026-08-24T10:04:00Z",
        "measurements": {"tokens": {"input": 1200, "output": 800}, "retries": 0},
        "artifact_hashes": ["sha256:" + "a" * 64],
    }
    attempt.update(changes)
    return attempt


def _attempts(*attempts: dict[str, Any]) -> dict[str, Any]:
    """Wrap completed attempts in the versioned observation request envelope."""

    return {"schema_version": 1, "attempts": list(attempts or (_attempt(),))}


def test_observe_emits_one_importable_observation_from_a_routed_attempt() -> None:
    """A judged attempt keeps its exact point, fallback, identities and metrics."""

    # Observe one completed attempt whose provider resolved a fallback model.
    observations = _load_observations()
    attempt = _attempt(
        resolution={"model": "worker-v2-fallback", "fallback_from": "worker-v2"}
    )
    response = observations.observe(_attempts(attempt))
    observation = response["observations"][0]
    launch = attempt["decision"]["launch"]

    # Assert the exact routed point, the resolved point and the identities.
    assert response["refusals"] == []
    assert (
        observation["configuration_fingerprint"] == launch["configuration_fingerprint"]
    )
    assert observation["routed"]["model"] == launch["model"]
    assert observation["routed"]["native_deliberation"] == launch["native_deliberation"]
    assert observation["routed"]["channel"] == launch["channel"]
    assert observation["routed"]["adapter_id"] == launch["adapter_id"]
    assert observation["resolved"] == {
        "model": "worker-v2-fallback",
        "fallback_from": "worker-v2",
    }
    assert observation["benchmark_key"] == "orchestrate-ticket-v1"
    assert observation["task_id"] == "ticket-96"
    assert observation["session_identity"] == "run-4f21"
    assert observation["workload_stratum"] == "initial_build"
    assert observation["outcome"] == "pass"
    assert observation["outcome_authority"] == "independent_verifier"
    assert (
        observation["provenance"]["snapshot_identity"]
        == (attempt["decision"]["audit"]["snapshot_identity"])
    )
    assert (
        observation["provenance"]["evidence_class"]
        == attempt["decision"]["evidence_class"]
    )
    assert observation["provenance"]["harness"] == "codex"
    assert observation["latency"]["wall_seconds"] == 240.0
    assert observation["tokens"]["input"] == 1200
    assert observation["artifact_hashes"] == attempt["artifact_hashes"]
    assert observations.validate(observation) is None


def test_observe_carries_the_frozen_standing_policy_into_the_observation() -> None:
    """An attempt is judged on the ladder its own run froze, never on today's."""

    # Observe one selected attempt whose frozen decision names its own policy.
    observations = _load_observations()
    attempt = _attempt()
    audited = attempt["decision"]["audit"]["standing_policy"]
    observation = observations.observe(_attempts(attempt))["observations"][0]

    # Assert the block travels whole and drops nothing the evaluation reads.
    assert observation["provenance"]["standing_policy"] == {
        field: audited[field]
        for field in (
            "policy_revision",
            "workload_cohort",
            "starting_rung",
            "current_rung",
            "floor",
            "ceiling",
            "next_rung_up",
        )
    }
    assert observations.validate(observation) is None


def test_run_identity_distinguishes_runs_without_changing_legacy_keys() -> None:
    """An opaque run term separates periods while null preserves old identity."""

    # Emit the same attempt through the legacy and run-scoped identity forms.
    observations = _load_observations()
    legacy = observations.observe(_attempts(_attempt()))["observations"][0]
    scoped = observations.observe(_attempts(_attempt(run_identity="run-opaque-7")))[
        "observations"
    ][0]
    configuration = legacy["configuration_fingerprint"]
    expected = hashlib.sha256(
        f"{configuration}|orchestrate-ticket-v1|ticket-96|null|1".encode()
    ).hexdigest()

    # Keep the historic key and validate the new top-level identity term.
    assert legacy["run_identity"] is None
    assert legacy["run_key"] == expected
    assert scoped["run_identity"] == "run-opaque-7"
    assert scoped["run_key"] != legacy["run_key"]
    assert observations.validate(legacy) is None
    assert observations.validate(scoped) is None


def test_model_selector_observations_is_only_the_shared_library_adapter() -> None:
    """One Library implementation serves the Skill CLI and Orchestrate."""

    # Require the implementation and the four public functions at their seam.
    assert ROUTED_OBSERVATIONS.is_file()
    source = (MODEL_SELECTOR / "scripts" / "observations.py").read_text(
        encoding="utf-8"
    )
    for function in ("observe", "merge", "validate", "record"):
        assert f"def {function}(" not in source
        assert function in source


def test_observe_refuses_every_attempt_no_external_outcome_completed() -> None:
    """A route choice, a refusal and an interrupted run are audit data only."""

    # Observe one undecided, one unlaunched and one interrupted attempt.
    observations = _load_observations()
    undecided = _attempt(attempt_id="build-1", outcome=None)
    unlaunched = _attempt(
        attempt_id="build-2",
        decision={
            "request_id": "build-2",
            "status": "refused",
            "reason": {"code": "empty_safe_candidate_set", "detail": "no point"},
            "audit": _attempt()["decision"]["audit"],
        },
    )
    interrupted = _attempt(attempt_id="build-3", completed_at=None)
    response = observations.observe(_attempts(undecided, unlaunched, interrupted))

    # Assert each refusal names its own stable reason and emits no observation.
    assert response["observations"] == []
    assert [refusal["code"] for refusal in response["refusals"]] == [
        "no_outcome",
        "unlaunched_decision",
        "incomplete_attempt",
    ]


def test_observe_never_lets_a_self_report_establish_an_outcome() -> None:
    """Builder and subagent confidence cannot become measured quality."""

    # Observe one builder self-report and one dependent checker.
    observations = _load_observations()
    self_reported = _attempt(
        attempt_id="build-1",
        outcome={
            "result": "pass",
            "authority": "self_report",
            "checker": {"identity": "builder", "independent": False},
            "condition": None,
            "scores": None,
        },
    )
    dependent = _attempt(
        attempt_id="build-2",
        outcome={
            "result": "pass",
            "authority": "objective_checker",
            "checker": {"identity": "the builder itself", "independent": False},
            "condition": None,
            "scores": None,
        },
    )
    unchecked = _attempt(
        attempt_id="build-3",
        workload_stratum="delegated_execution",
        outcome={
            "result": "pass",
            "authority": "objective_checker",
            "checker": None,
            "condition": None,
            "scores": None,
        },
    )
    response = observations.observe(_attempts(self_reported, dependent, unchecked))

    # Assert no self-graded work reaches the artifact at all.
    assert response["observations"] == []
    assert [refusal["code"] for refusal in response["refusals"]] == [
        "self_reported_outcome",
        "self_reported_outcome",
        "unchecked_outcome",
    ]


def test_observe_accepts_only_declared_signals_and_human_confirmation() -> None:
    """Delegation's decisive outcomes come from a checker, rubric or person."""

    # Observe a frozen rubric, a declared failure signal and a confirmed pass.
    observations = _load_observations()
    rubric = _attempt(
        attempt_id="delegate-1",
        workload_stratum="delegated_execution",
        outcome={
            "result": "pass",
            "authority": "frozen_rubric",
            "checker": {"identity": "rubric-7", "independent": True},
            "condition": None,
            "scores": {"quality": 0.9},
        },
    )
    declared = _attempt(
        attempt_id="delegate-2",
        workload_stratum="delegated_execution",
        outcome={
            "result": "fail",
            "authority": "declared_failure_signal",
            "checker": {"identity": "pytest", "independent": True},
            "condition": None,
            "scores": None,
        },
    )
    confirmed = _attempt(
        attempt_id="delegate-3",
        workload_stratum="delegated_execution",
        outcome={
            "result": "pass",
            "authority": "user_confirmation",
            "checker": {"identity": "user", "independent": True},
            "condition": None,
            "scores": None,
        },
    )
    response = observations.observe(_attempts(rubric, declared, confirmed))

    # Assert all three decisive authorities produce importable observations.
    assert response["refusals"] == []
    assert [observation["outcome"] for observation in response["observations"]] == [
        "pass",
        "fail",
        "pass",
    ]


def test_observe_keeps_workflow_conditions_out_of_model_quality() -> None:
    """Hinders, decisions, dependencies, and tracker faults differ."""

    # Observe every non-model condition the routed workflows can reach.
    observations = _load_observations()
    conditions = {
        "mechanical_hinder": "infra_error",
        "tracker_failure": "infra_error",
        "open_decision": "abstain",
        "discovered_dependency": "abstain",
    }
    attempts = [
        _attempt(
            attempt_id=f"build-{index}",
            attempt_index=index + 1,
            outcome={
                "result": result,
                "authority": "harness",
                "checker": None,
                "condition": condition,
                "scores": None,
            },
        )
        for index, (condition, result) in enumerate(conditions.items())
    ]
    miscounted = _attempt(
        attempt_id="build-99",
        outcome={
            "result": "fail",
            "authority": "independent_verifier",
            "checker": {"identity": "verify.md", "independent": True},
            "condition": "mechanical_hinder",
            "scores": None,
        },
    )
    response = observations.observe(_attempts(*attempts, miscounted))

    # Assert conditions are retained apart from quality and never as failures.
    assert [observation["outcome"] for observation in response["observations"]] == list(
        conditions.values()
    )
    assert [
        observation["non_model_condition"] for observation in response["observations"]
    ] == list(conditions)
    assert [refusal["code"] for refusal in response["refusals"]] == [
        "non_model_condition_outcome"
    ]


def test_observe_leaves_unavailable_metrics_null_and_totals_cheap_first() -> None:
    """A cheap-first policy carries its failed attempt, checker and retry."""

    # Observe a failed cheap attempt and the escalated retry that followed it.
    observations = _load_observations()
    cheap = _attempt(
        attempt_id="build-96",
        outcome={
            "result": "fail",
            "authority": "independent_verifier",
            "checker": {"identity": "verify.md", "independent": True},
            "condition": None,
            "scores": None,
        },
        measurements={
            "rolling_quota": 3.0,
            "wall_seconds": 120.0,
            "cash": None,
            "retries": 0,
        },
    )
    escalated = _attempt(
        attempt_id="amend-96-1",
        workload_stratum="amend",
        attempt_index=2,
        prior_attempt_id="build-96",
        checker_charge={"rolling_quota": 1.0, "wall_seconds": 30.0, "cash": None},
        measurements={"rolling_quota": 5.0, "wall_seconds": 200.0, "retries": 1},
    )
    response = observations.observe(_attempts(cheap, escalated))
    first, second = response["observations"]

    # Assert null metrics and the policy account for all three cases.
    assert first["cost"]["cash"] is None
    assert first["tokens"]["input"] is None
    assert first["quota"]["rolling"] == 3.0
    assert second["policy"]["identity"] == "cheap_first"
    assert second["policy"]["attempts"] == [first["run_key"], second["run_key"]]
    assert second["policy"]["retries"] == 1
    assert second["policy"]["charged"]["rolling_quota"] == 9.0
    assert second["policy"]["charged"]["wall_seconds"] == 350.0
    assert second["policy"]["charged"]["cash"] is None
    assert first["policy"] is None


def test_observe_emits_statistics_rather_than_any_transcript() -> None:
    """Prompts, bodies, diffs, output, secrets and paths cannot enter."""

    # Observe an attempt padded with every forbidden field a caller might hold.
    observations = _load_observations()
    padded = _attempt(
        prompt="the whole brief",
        response="the whole answer",
        reasoning="the whole thinking",
        ticket_body="the whole ticket",
        diff="--- a/x\n+++ b/x",
        terminal_output="pytest ...",
        transcript=["turn one"],
        secret="sk-live-1234567890",
        worktree="/Users/thomas/Projects/skills",
    )
    response = observations.observe(_attempts(padded))
    serialized = json.dumps(response["observations"][0])

    # Assert nothing but the allow-listed statistical fields survives.
    for forbidden in (
        "the whole brief",
        "the whole answer",
        "the whole thinking",
        "the whole ticket",
        "+++ b/x",
        "pytest ...",
        "turn one",
        "sk-live-1234567890",
        "/Users/thomas",
    ):
        assert forbidden not in serialized
    assert set(json.loads(serialized)).isdisjoint(
        {"prompt", "response", "reasoning", "ticket_body", "diff", "transcript"}
    )

    # Assert an absolute path offered as an identity is refused, not trimmed.
    refused = observations.observe(
        _attempts(_attempt(task_identity="/Users/thomas/Projects/skills/tests"))
    )
    assert refused["observations"] == []
    assert refused["refusals"][0]["code"] == "unsanitized_value"
    assert "/Users/thomas" not in json.dumps(refused)


def test_observe_merges_identically_and_never_overwrites_a_conflict() -> None:
    """Repeating an attempt adds nothing; a changed one overwrites nothing."""

    # Merge one produced observation into an empty artifact twice.
    observations = _load_observations()
    produced = observations.observe(_attempts())["observations"]
    first = observations.merge(None, produced)
    again = observations.merge(first["artifact"], produced)

    # Assert the identical repeat is skipped rather than duplicated.
    assert len(first["artifact"]["observations"]) == 1
    assert first["added"] == [produced[0]["run_key"]]
    assert again["added"] == []
    assert again["skipped"] == [produced[0]["run_key"]]
    assert again["artifact"]["observations"] == first["artifact"]["observations"]

    # Merge a different outcome under the same identity.
    conflicting = observations.observe(
        _attempts(
            _attempt(
                outcome={
                    "result": "fail",
                    "authority": "independent_verifier",
                    "checker": {"identity": "verify.md", "independent": True},
                    "condition": None,
                    "scores": None,
                }
            )
        )
    )["observations"]
    clash = observations.merge(first["artifact"], conflicting)

    # Assert the conflict is surfaced while both sources stay as they were.
    assert clash["added"] == []
    assert clash["conflicts"][0]["run_key"] == produced[0]["run_key"]
    assert clash["artifact"]["observations"] == first["artifact"]["observations"]


def _observe_command(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> tuple[dict[str, Any], int]:
    """Run one `observe` command line and return its report and exit status."""

    status = _load_observations().main(argv)
    return cast(dict[str, Any], json.loads(capsys.readouterr().out)), status


def _ledger_rows(directory: Path) -> list[dict[str, Any]]:
    """Return every observation the ledger under *directory* holds."""

    path = directory / "run-observations.jsonl"
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_observe_imports_the_machine_judged_attempt_it_was_asked_to_import(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """One call emits the caller's artifact and files the evidence behind it."""

    # Observe one independently judged attempt with the import asked for.
    source = tmp_path / "attempts.json"
    source.write_text(json.dumps(_attempts()), encoding="utf-8")
    artifact = tmp_path / "artifact.json"
    data = tmp_path / "data"
    report, status = _observe_command(
        [
            "observe",
            str(source),
            f"--artifact={artifact}",
            "--import",
            f"--data={data}",
        ],
        capsys,
    )

    # Assert the artifact is what it always was and the ledger now holds it.
    rows = _ledger_rows(data)
    written = json.loads(artifact.read_text(encoding="utf-8"))
    assert status == 0
    assert [row["run_key"] for row in rows] == report["importable"]
    assert written["observations"] == rows
    assert report["import"]["imported"] == report["importable"]
    assert report["import"]["identically_skipped"] == []
    assert report["import"]["conflicting"] == []
    assert report["import"]["refused"] == []
    assert [
        (answer["workload_cohort"], answer["outcome"])
        for answer in report["import"]["standing_policy"]
    ] == [("python-refactor", "below_threshold")]


def test_observe_repeated_skips_the_row_it_already_filed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An import run twice adds one row and says the second was the same one."""

    # Import the same judged attempt twice into the same evidence directory.
    source = tmp_path / "attempts.json"
    source.write_text(json.dumps(_attempts()), encoding="utf-8")
    data = tmp_path / "data"
    argv = [
        "observe",
        str(source),
        f"--artifact={tmp_path / 'artifact.json'}",
        "--import",
        f"--data={data}",
    ]
    first = _observe_command(argv, capsys)[0]
    again, status = _observe_command(argv, capsys)

    # Assert the ledger holds the one row and the repeat changed nothing.
    rows = _ledger_rows(data)
    assert status == 0
    assert len(rows) == 1
    assert again["import"]["imported"] == []
    assert again["import"]["identically_skipped"] == first["import"]["imported"]


def test_observe_writes_no_ledger_where_no_import_was_asked_for(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The verb a user runs by hand keeps its one side effect: the artifact."""

    # Observe the same judged attempt without the import flag.
    source = tmp_path / "attempts.json"
    source.write_text(json.dumps(_attempts()), encoding="utf-8")
    artifact = tmp_path / "artifact.json"
    data = tmp_path / "data"
    report, status = _observe_command(
        ["observe", str(source), f"--artifact={artifact}"], capsys
    )

    # A ledger directory without the flag is an unsupported option, not a hint.
    refusal, refused_status = _observe_command(
        ["observe", str(source), f"--data={data}"], capsys
    )

    assert status == 0
    assert report["import"] is None
    assert report["importable"]
    assert not data.exists()
    assert refused_status == 2
    assert refusal["artifact_refusal"]["code"] == "invalid_arguments"


def test_observe_imports_no_outcome_only_a_human_established(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A rubric and a person stay the user's own `record`, import or not."""

    # Observe the two authorities no caller may file without a human.
    rubric = _attempt(
        attempt_id="delegate-1",
        workload_stratum="delegated_execution",
        outcome={
            "result": "pass",
            "authority": "frozen_rubric",
            "checker": {"identity": "rubric-7", "independent": True},
            "condition": None,
            "scores": None,
        },
    )
    confirmed = _attempt(
        attempt_id="delegate-2",
        attempt_index=2,
        workload_stratum="delegated_execution",
        outcome={
            "result": "pass",
            "authority": "user_confirmation",
            "checker": {"identity": "user", "independent": True},
            "condition": None,
            "scores": None,
        },
    )
    source = tmp_path / "attempts.json"
    source.write_text(json.dumps(_attempts(rubric, confirmed)), encoding="utf-8")
    artifact = tmp_path / "artifact.json"
    data = tmp_path / "data"
    report, status = _observe_command(
        [
            "observe",
            str(source),
            f"--artifact={artifact}",
            "--import",
            f"--data={data}",
        ],
        capsys,
    )

    # Assert both stay importable by hand and neither reached the ledger.
    assert status == 0
    assert len(report["importable"]) == 2
    assert report["import"]["imported"] == []
    assert _ledger_rows(data) == []


def test_observe_reports_a_ledger_refusal_without_failing_the_caller(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence that cannot be filed stops nothing the caller was doing."""

    # Point the import at a path no ledger directory can be created under.
    source = tmp_path / "attempts.json"
    source.write_text(json.dumps(_attempts()), encoding="utf-8")
    artifact = tmp_path / "artifact.json"
    blocked = tmp_path / "blocked"
    blocked.write_text("", encoding="utf-8")
    report, status = _observe_command(
        [
            "observe",
            str(source),
            f"--artifact={artifact}",
            "--import",
            f"--data={blocked}",
        ],
        capsys,
    )

    # Assert the artifact stands and the refusal is named rather than raised.
    assert status == 0
    assert json.loads(artifact.read_text(encoding="utf-8"))["observations"]
    assert report["import"]["imported"] == []
    assert [
        (refusal["run_key"], refusal["code"]) for refusal in report["import"]["refused"]
    ] == [(report["importable"][0], "automatic_import_failed")]


def test_the_machine_judged_rule_is_the_librarys_and_admits_no_self_report() -> None:
    """One eligibility rule serves both routed callers (issue #222)."""

    # Ask the Library which of every authority it would file without a human.
    observations = _load_observations()
    judged = observations.observe(
        _attempts(
            _attempt(),
            _attempt(
                attempt_id="build-97",
                attempt_index=2,
                outcome={
                    "result": "pass",
                    "authority": "user_confirmation",
                    "checker": {"identity": "user", "independent": True},
                    "condition": None,
                    "scores": None,
                },
            ),
            _attempt(
                attempt_id="build-98",
                attempt_index=3,
                outcome={
                    "result": "abstain",
                    "authority": "harness",
                    "checker": None,
                    "condition": "open_decision",
                    "scores": None,
                },
            ),
        )
    )["observations"]
    eligible = observations.machine_judged(judged)

    # Assert the machine authorities and the non-model conditions, and no more.
    assert [observation["outcome_authority"] for observation in judged] == [
        "independent_verifier",
        "user_confirmation",
        "harness",
    ]
    assert [observation["run_key"] for observation in eligible] == [
        judged[0]["run_key"],
        judged[2]["run_key"],
    ]


def _frontier_point(derived: dict[str, Any], benchmark_key: str) -> dict[str, Any]:
    """Return the single point of the frontier one benchmark key identifies."""

    frontiers = [
        frontier
        for frontier in derived["frontiers"].values()
        if frontier["benchmark_key"] == benchmark_key
    ]
    assert len(frontiers) == 1, derived
    return cast(dict[str, Any], frontiers[0]["points"][0])


def test_record_appends_unseen_observations_and_only_affected_frontiers(
    tmp_path: Path,
) -> None:
    """Explicit import accepts, skips, refuses and rebuilds by eligible set."""

    # Import one artifact into an empty evidence directory.
    observations = _load_observations()
    produced = observations.observe(
        _attempts(
            _attempt(),
            _attempt(
                attempt_id="build-97",
                attempt_index=2,
                task_identity="ticket-97",
                benchmark={
                    "key": "delegation-extract-v1",
                    "name": "delegation-extract",
                    "version": "1",
                    "cohort": None,
                    "tags": [],
                },
            ),
        )
    )["observations"]
    artifact = observations.merge(None, produced)["artifact"]
    first = observations.record(artifact, tmp_path)
    ledger = tmp_path / "run-observations.jsonl"
    frontiers = json.loads((tmp_path / "derived-frontiers.json").read_text("utf-8"))

    # Assert both observations landed and both cohorts were rebuilt once.
    assert sorted(first["accepted"]) == sorted(
        observation["run_key"] for observation in produced
    )
    assert first["rejected"] == []
    assert len(ledger.read_text("utf-8").strip().splitlines()) == 2
    assert first["frontiers_rebuilt"] == [
        {
            "benchmark_key": "delegation-extract-v1",
            "stage": "build",
            "workload_cohort": "python-refactor",
            "workload_tags": ["python"],
        },
        {
            "benchmark_key": "orchestrate-ticket-v1",
            "stage": "build",
            "workload_cohort": "python-refactor",
            "workload_tags": ["python"],
        },
    ]
    assert sorted(
        entry["benchmark_key"] for entry in frontiers["frontiers"].values()
    ) == ["delegation-extract-v1", "orchestrate-ticket-v1"]
    assert not (tmp_path / "config.json").exists()

    # Import the same artifact again, then one changed observation.
    repeated = observations.record(artifact, tmp_path)
    conflicting = deepcopy(artifact)
    conflicting["observations"][0]["outcome"] = "fail"
    clash = observations.record(conflicting, tmp_path)
    kept = json.loads((tmp_path / "derived-frontiers.json").read_text("utf-8"))

    # Assert the repeat changes nothing and the conflict overwrites nothing.
    assert repeated["accepted"] == []
    assert sorted(repeated["skipped"]) == sorted(first["accepted"])
    assert repeated["frontiers_rebuilt"] == []
    assert clash["accepted"] == []
    assert clash["rejected"][0]["code"] == "conflicting_identity"
    assert len(ledger.read_text("utf-8").strip().splitlines()) == 2
    assert kept == frontiers


def test_record_rebuilds_quality_from_judged_model_outcomes_alone(
    tmp_path: Path,
) -> None:
    """Infrastructure and abstained attempts cannot lower a point's quality."""

    # Import one passing attempt, then a hinder and an abstention beside it.
    observations = _load_observations()
    judged = observations.observe(_attempts())["observations"]
    observations.record(observations.merge(None, judged)["artifact"], tmp_path)
    measured = json.loads((tmp_path / "derived-frontiers.json").read_text("utf-8"))
    conditioned = observations.observe(
        _attempts(
            *[
                _attempt(
                    attempt_id=f"build-{index}",
                    attempt_index=index + 2,
                    outcome={
                        "result": result,
                        "authority": "harness",
                        "checker": None,
                        "condition": condition,
                        "scores": None,
                    },
                )
                for index, (condition, result) in enumerate(
                    [
                        ("mechanical_hinder", "infra_error"),
                        ("open_decision", "abstain"),
                    ]
                )
            ]
        )
    )["observations"]
    observations.record(observations.merge(None, conditioned)["artifact"], tmp_path)
    after = json.loads((tmp_path / "derived-frontiers.json").read_text("utf-8"))
    point = _frontier_point(after, "orchestrate-ticket-v1")

    # Assert quality counts only judged model outcomes and keeps the rest apart.
    assert point["runs"] == 1
    assert point["successes"] == 1
    assert point["excluded"] == {"infra_error": 1, "abstain": 1}
    assert (
        point["quality_lower_bound"]
        == (_frontier_point(measured, "orchestrate-ticket-v1")["quality_lower_bound"])
    )
    assert (
        point["quality_upper_bound"]
        == (_frontier_point(measured, "orchestrate-ticket-v1")["quality_upper_bound"])
    )


def _two_candidate_profile() -> bytes:
    """Narrow the fixture to one weak and one strong exactly launchable point.

    A route decision only becomes measurement-based once every launchable
    candidate has exact evidence, so a ledger that closes the loop has to cover
    the whole candidate set. Two points is the smallest set that still has
    something to choose between.
    """

    profile = json.loads(PROFILE_FIXTURE.read_text(encoding="utf-8"))
    kept = []
    for selection in profile["model_selections"]:
        if selection["canonical_provider_model_id"] not in (
            "claude-haiku-4-5-20251001",
            "claude-opus-5",
        ):
            continue
        selection["controls"]["effort"] = {"policy": "explicit", "values": ["max"]}
        selection["controls"]["serving_modes"] = {
            "policy": "explicit",
            "values": ["standard"],
        }
        kept.append(selection)
    profile["model_selections"] = kept
    return json.dumps(profile).encode()


def _judged_attempts(
    decision: dict[str, Any], count: int, result: str, offset: int
) -> list[dict[str, Any]]:
    """Build one externally judged batch of attempts against one exact point."""

    return [
        _attempt(
            attempt_id=f"build-{offset + index}",
            task_identity=f"ticket-{offset + index}",
            harness={
                "name": "claude-code",
                "inventory_revision": "claude-code/agent-tool",
            },
            decision=decision,
            outcome={
                "result": result,
                "authority": "independent_verifier",
                "checker": {"identity": "verify.md", "independent": True},
                "condition": None,
                "scores": None,
            },
        )
        for index in range(count)
    ]


def _import(observations: Any, directory: Path, attempts: list[dict[str, Any]]) -> None:
    """Emit and import one batch, refusing to proceed on any refusal."""

    produced = observations.observe({"schema_version": 1, "attempts": attempts})
    assert produced["refusals"] == [], produced["refusals"]
    report = observations.record(
        observations.merge(None, produced["observations"])["artifact"], directory
    )
    assert report["rejected"] == [], report["rejected"]


def test_the_projected_ledger_reaches_a_measured_decision_with_nothing_written(
    tmp_path: Path,
) -> None:
    """Judged attempts become the next decision's evidence with no user step.

    This is the evidence loop end to end and in one place: a route decision,
    the attempts an external verdict judged, the ledger they were imported
    into, and the next decision over the same profile — with `evidence.records`
    derived from the ledger every time and hand-written nowhere.
    """

    # Route the cold start, whose ledger holds nothing at all yet.
    profile = _two_candidate_profile()
    router = _load_router()
    data = tmp_path / "model-selector"
    cold = _derive_context(tmp_path, _runtime_context_request(), profile)
    weak, strong = router.route(
        {
            "schema_version": 1,
            "context": cold["context"],
            "requests": [
                _request(),
                _request(request_id="route-2", overrides={"model": "claude-opus-5"}),
            ],
        }
    )["decisions"]

    assert cold["context"]["evidence"]["records"] == []
    assert weak["evidence_class"] == "heuristic"
    assert weak["launch"]["model"] == "claude-haiku-4-5-20251001"

    # Import six passes, which the shipped floor is deliberately above.
    observations = _load_observations()
    _import(observations, data, _judged_attempts(weak, 6, "pass", 0))
    six = _derive_context(tmp_path, _runtime_context_request(), profile)
    below = router.route(six)["decisions"][0]
    projected = six["context"]["evidence"]["records"][0]

    # Assert the ledger is read as evidence and the floor still refuses it.
    assert len(six["context"]["evidence"]["records"]) == 1
    assert (
        projected["configuration_fingerprint"]
        == (weak["launch"]["configuration_fingerprint"])
    )
    assert projected["stage"] == "build"
    assert projected["workload_cohort"] == "python-refactor"
    assert projected["representative"] is True
    assert projected["coverage"] == {"decision_relevant": True}
    assert projected["quality"] == 1.0
    assert projected["uncertainty"]["lower_bound"] < 0.7
    assert projected["uncertainty"]["upper_bound"] == 1.0
    assert below["evidence_class"] == "heuristic"
    assert {exclusion["code"] for exclusion in below["audit"]["exclusions"]} == {
        "quality_floor_not_cleared"
    }

    # Cover the whole candidate set, the weak point clearing the floor alone.
    _import(observations, data, _judged_attempts(weak, 4, "pass", 6))
    _import(observations, data, _judged_attempts(strong, 4, "fail", 100))
    measured = _derive_context(tmp_path, _runtime_context_request(), profile)
    decided = router.route(measured)["decisions"][0]
    evidence = measured["context"]["evidence"]

    # Assert the next decision is measured, and says so from the ledger alone.
    assert decided["evidence_class"] == "measurement_based"
    assert decided["launch"]["model"] == "claude-haiku-4-5-20251001"
    assert len(evidence["records"]) == 2
    canonical = json.dumps(
        evidence["records"], sort_keys=True, separators=(",", ":")
    ).encode()
    assert evidence["identity"] == f"sha256:{hashlib.sha256(canonical).hexdigest()}"
    assert evidence["vintage"] == "2026-08-24T10:04:00Z"


def test_a_projection_keeps_every_cohort_and_unnamed_row_apart(
    tmp_path: Path,
) -> None:
    """One fingerprint measured in two Cohorts is two measurements, not one."""

    # Import the same exact point under two stages, one passing and one not.
    observations = _load_observations()
    decision = _routed_decision()
    _import(
        observations,
        tmp_path,
        _judged_attempts(decision, 2, "pass", 0)
        + [
            attempt | {"stage": "rebuild"}
            for attempt in _judged_attempts(decision, 2, "fail", 50)
        ]
        + [
            {
                key: value
                for key, value in attempt.items()
                if key not in ("stage", "workload_cohort", "workload_tags")
            }
            for attempt in _judged_attempts(decision, 2, "pass", 90)
        ],
    )
    projected = observations.projected_evidence(tmp_path)
    derived = json.loads((tmp_path / "derived-frontiers.json").read_text("utf-8"))
    ledger = (tmp_path / "run-observations.jsonl").read_text("utf-8")

    # Assert each stage states its own quality and the unnamed rows state none.
    assert len(ledger.strip().splitlines()) == 6
    assert [
        (record["stage"], record["quality"]) for record in projected["records"]
    ] == [("build", 1.0), ("rebuild", 0.0)]
    assert len(derived["frontiers"]) == 2
    assert sorted(frontier["stage"] for frontier in derived["frontiers"].values()) == [
        "build",
        "rebuild",
    ]
    assert all(
        point["runs"] == 2
        for frontier in derived["frontiers"].values()
        for point in frontier["points"]
    )


def test_a_projected_point_is_priced_by_the_whole_chain_that_reached_it(
    tmp_path: Path,
) -> None:
    """A retry's cost and elapsed time belong to the point its pass landed on."""

    # Import one cheap failure and the escalated retry that finally passed.
    observations = _load_observations()
    cheap = _routed_decision()
    strong = deepcopy(cheap)
    strong["launch"] |= {
        "model": "worker-v3",
        "configuration_fingerprint": "fingerprint-worker-v3",
    }
    failed = _attempt(
        attempt_id="build-96",
        decision=cheap,
        outcome={
            "result": "fail",
            "authority": "independent_verifier",
            "checker": {"identity": "verify.md", "independent": True},
            "condition": None,
            "scores": None,
        },
        run_identity="run-1",
        started_at="2026-08-24T10:00:00Z",
        completed_at="2026-08-24T10:05:00Z",
        measurements={"cash": 1.0, "retries": 0},
    )
    passed = _attempt(
        attempt_id="amend-96-1",
        prior_attempt_id="build-96",
        attempt_index=2,
        workload_stratum="amend",
        stage="amend",
        benchmark={
            "key": "orchestrate-amend",
            "name": "orchestrate-ticket",
            "version": "1",
            "cohort": "python-refactor",
            "tags": ["python"],
        },
        decision=strong,
        run_identity="run-1",
        started_at="2026-08-24T10:05:00Z",
        completed_at="2026-08-24T10:11:00Z",
        measurements={"cash": 4.0, "retries": 1},
    )
    _import(observations, tmp_path, [failed, passed])
    projected = {
        record["configuration_fingerprint"]: record
        for record in observations.projected_evidence(tmp_path)["records"]
    }

    # Assert the escalation is priced in the Cohort its own pass belongs to.
    assert [record["stage"] for record in projected.values()] == ["amend", "build"] or [
        record["stage"] for record in projected.values()
    ] == ["build", "amend"]
    assert projected["fingerprint-worker-v3"]["commercial"]["cash"] == 5.0
    assert projected["fingerprint-worker-v3"]["commercial"]["latency"] == 660.0
    assert projected["fingerprint-worker-v3"]["commercial"]["rolling_quota"] is None
    assert projected[cheap["launch"]["configuration_fingerprint"]]["commercial"] == {
        "cash": None,
        "rolling_quota": None,
        "weekly_quota": None,
        "allocated_subscription_cost": None,
        "latency": None,
    }

    # Assert the ledger holds the links a later reader rebuilds the chain from.
    ledger = [
        json.loads(line)
        for line in (tmp_path / "run-observations.jsonl")
        .read_text("utf-8")
        .splitlines()
    ]
    assert [row["attempt_id"] for row in ledger] == ["build-96", "amend-96-1"]
    assert [row["prior_attempt_id"] for row in ledger] == [None, "build-96"]


def test_a_chain_no_verdict_passed_prices_no_point_at_all(tmp_path: Path) -> None:
    """An unfinished measurement never reads as the cheapest point on a frontier."""

    # Import one task whose only routed attempt was judged a failure.
    observations = _load_observations()
    _import(
        observations,
        tmp_path,
        _judged_attempts(_routed_decision(), 1, "fail", 0)
        + [
            attempt | {"measurements": {"cash": 2.0, "retries": 0}}
            for attempt in _judged_attempts(_routed_decision(), 1, "pass", 7)
        ],
    )
    projected = observations.projected_evidence(tmp_path)["records"]

    # Assert only the chain that passed contributed a cash mean at all.
    assert len(projected) == 1
    assert projected[0]["commercial"]["cash"] == 2.0
    assert projected[0]["quality"] == 0.5


def test_two_runless_sessions_at_one_task_are_two_chains_rather_than_one(
    tmp_path: Path,
) -> None:
    """Unrelated runs at one task never merge into a single charge.

    A row naming no run — a hand recorded observation, a row older than run
    identity — falls back to its session for the chain boundary. Grouping
    those by task alone would read two unrelated attempts as one chain and
    charge both to whichever configuration happened to pass.
    """

    # Import one failed attempt from one session and, at the same task, a
    # later passing attempt from another — neither naming a run.
    observations = _load_observations()
    failed = _attempt(
        attempt_id="build-a",
        session_identity="session-a",
        task_identity="ticket-shared",
        attempt_index=1,
        outcome={
            "result": "fail",
            "authority": "independent_verifier",
            "checker": {"identity": "verify.md", "independent": True},
            "condition": None,
            "scores": None,
        },
        measurements={"cash": 10.0, "retries": 0},
    )
    passed = _attempt(
        attempt_id="build-b",
        session_identity="session-b",
        task_identity="ticket-shared",
        attempt_index=2,
        measurements={"cash": 3.0, "retries": 0},
    )
    _import(observations, tmp_path, [failed, passed])
    projected = observations.projected_evidence(tmp_path)["records"]

    # Assert the pass was charged its own session only, not the other's failure.
    assert len(projected) == 1
    assert projected[0]["commercial"]["cash"] == 3.0


def test_a_damaged_ledger_row_yields_no_evidence_rather_than_a_refusal(
    tmp_path: Path,
) -> None:
    """The ledger is a file Context does not own, so damage in it is not an error.

    It is append-only JSONL a user may hand-write and an interrupted append may
    truncate. A row missing an identity the projection reads must leave the
    route with no evidence, not with a traceback where a decision belongs.
    """

    # A row naming a Cohort but no benchmark names no frontier and no record.
    observations = _load_observations()
    keyless = tmp_path / "keyless"
    keyless.mkdir()
    (keyless / "run-observations.jsonl").write_text(
        json.dumps(
            {
                "run_key": "keyless",
                "stage": "build",
                "workload_cohort": "python-refactor",
                "workload_tags": [],
                "configuration_fingerprint": "sha256:point",
                "outcome": "pass",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    assert observations.projected_evidence(keyless) == {
        "records": [],
        "vintage": None,
    }

    # Derive context over a ledger whose row the reader itself cannot index.
    data = tmp_path / "model-selector"
    data.mkdir(parents=True)
    (data / "run-observations.jsonl").write_text(
        json.dumps({"benchmark_key": "orchestrate-ticket-v1"}) + "\n",
        encoding="utf-8",
    )
    derived = _derive_context(tmp_path, _runtime_context_request())
    routed = _load_router().route(derived)

    # Assert the route still decides, from the shipped seed's own date.
    assert derived["context"]["evidence"]["records"] == []
    assert derived["context"]["evidence"]["vintage"] == "2026-08-23"
    assert routed["decisions"][0]["status"] == "selected"


def test_a_rebuild_discards_a_frontier_written_under_an_older_identity(
    tmp_path: Path,
) -> None:
    """A derived summary is reproducible, so an old shape is dropped, not kept.

    Before a frontier was identified by its whole Cohort it was identified by
    its benchmark key alone. Leaving such an entry beside the new ones would
    put two shapes in one file permanently, the old one never rebuilt and
    readable under no current identity (issue #191).
    """

    # Import one judged attempt over a frontier file of the older shape.
    observations = _load_observations()
    stale = {"points": [{"configuration_fingerprint": "sha256:old", "runs": 3}]}
    (tmp_path / "derived-frontiers.json").write_text(
        json.dumps(
            {"schema_version": 1, "frontiers": {"orchestrate-ticket-v1": stale}}
        ),
        encoding="utf-8",
    )
    _import(observations, tmp_path, _judged_attempts(_routed_decision(), 1, "pass", 0))
    derived = json.loads((tmp_path / "derived-frontiers.json").read_text("utf-8"))

    # Assert only the rebuilt current-shape frontier survives the rebuild.
    assert [entry["benchmark_key"] for entry in derived["frontiers"].values()] == [
        "orchestrate-ticket-v1"
    ]
    assert all("workload_cohort" in entry for entry in derived["frontiers"].values())


def test_observe_carries_the_cohort_the_routed_request_named() -> None:
    """The three identity fields travel with the attempt, or none of them do."""

    # Observe one attempt naming a Cohort, one naming half of it, and one bad.
    observations = _load_observations()
    named, partial = observations.observe(
        _attempts(
            _attempt(workload_tags=["python", "parser", "python"]),
            _attempt(
                attempt_id="build-97",
                task_identity="ticket-97",
                workload_cohort=None,
            ),
        )
    )["observations"]
    refused = observations.observe(_attempts(_attempt(stage=17)))

    # Assert tags normalize, half a Cohort is none, and a malformed one refuses.
    assert named["stage"] == "build"
    assert named["workload_cohort"] == "python-refactor"
    assert named["workload_tags"] == ["parser", "python"]
    assert partial["stage"] is None
    assert partial["workload_cohort"] is None
    assert partial["workload_tags"] is None
    assert refused["observations"] == []
    assert refused["refusals"][0]["code"] == "invalid_attempt"


def test_record_applies_the_same_validation_as_emission(tmp_path: Path) -> None:
    """A hand-written artifact meets exactly the rules emission enforces."""

    # Import an artifact whose observation was never produced by observe.
    observations = _load_observations()
    artifact = observations.merge(
        None, observations.observe(_attempts())["observations"]
    )["artifact"]
    forged = deepcopy(artifact)
    forged["observations"][0]["outcome_authority"] = "self_report"
    forged["observations"][0]["run_key"] = "forged-run-key"
    report = observations.record(forged, tmp_path)

    # Assert import refuses it with emission's own reason and writes nothing.
    assert report["accepted"] == []
    assert report["rejected"][0]["code"] == "self_reported_outcome"
    assert not (tmp_path / "run-observations.jsonl").exists()


def test_observation_cli_writes_only_the_artifact_the_caller_named(
    tmp_path: Path,
) -> None:
    """The process seam is machine-readable and touches no evidence store."""

    # Emit one artifact through the packaged script's declared uv runtime.
    script = str(MODEL_SELECTOR / "scripts" / "observations.py")
    attempts = tmp_path / "attempts.json"
    attempts.write_text(json.dumps(_attempts()), encoding="utf-8")
    artifact = tmp_path / "scratch" / "observations.json"
    completed = subprocess.run(
        ["uv", "run", script, "observe", str(attempts), "--artifact", str(artifact)],
        check=True,
        capture_output=True,
        text=True,
    )
    emitted = json.loads(completed.stdout)

    # Assert the artifact is the only thing written and is reported as such.
    assert emitted["artifact"] == str(artifact)
    assert emitted["importable"] == [
        json.loads(artifact.read_text("utf-8"))["observations"][0]["run_key"]
    ]
    assert completed.stderr == ""
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "attempts.json",
        "scratch",
    ]

    # Run every process-boundary failure family.
    for arguments, code in (
        ([], "invalid_arguments"),
        (["observe", str(tmp_path / "absent.json")], "unreadable_artifact"),
        (["record", str(attempts), "--data", str(tmp_path)], "invalid_artifact"),
    ):
        refused = subprocess.run(
            ["uv", "run", script, *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
        assert refused.returncode == 2
        assert json.loads(refused.stdout)["artifact_refusal"]["code"] == code
        assert "Traceback" not in refused.stderr


def test_the_ledger_purge_counts_rows_for_jsonl_and_bytes_for_the_summary(
    tmp_path: Path,
) -> None:
    """`purge` sizes the two JSONL stores in rows and the JSON summary in bytes.

    The ledger, its frontiers, and the quota store are measurement (ADR-0145,
    ADR-0159): rows that cannot become evidence are removed rather than
    repaired, which is the whole point of the verb.
    """

    observations = _load_observations()
    _import(observations, tmp_path, _judged_attempts(_routed_decision(), 1, "pass", 0))
    (tmp_path / "quota-observations.jsonl").write_text(
        json.dumps({"access_channel_key": "sha256:channel"}) + "\n", encoding="utf-8"
    )
    ledger = tmp_path / "run-observations.jsonl"
    frontiers = tmp_path / "derived-frontiers.json"
    quota = tmp_path / "quota-observations.jsonl"
    assert ledger.exists() and frontiers.exists()

    # A preview reports every path's exact size and writes nothing.
    preview = observations.purge_paths(tmp_path)
    by_path = {entry["path"]: entry for entry in preview}
    assert by_path[str(ledger)] == {
        "path": str(ledger),
        "present": True,
        "unit": "rows",
        "count": 1,
    }
    assert by_path[str(quota)] == {
        "path": str(quota),
        "present": True,
        "unit": "rows",
        "count": 1,
    }
    assert by_path[str(frontiers)] == {
        "path": str(frontiers),
        "present": True,
        "unit": "bytes",
        "count": frontiers.stat().st_size,
    }
    assert ledger.exists(), "a preview must write nothing"

    # Confirmed, purge removes all three and reports exactly what it found.
    removed = observations.purge(tmp_path)
    assert removed == preview
    assert not ledger.exists()
    assert not frontiers.exists()
    assert not quota.exists()


def test_the_ledger_purge_reports_every_absent_path_as_absent(
    tmp_path: Path,
) -> None:
    """An empty data directory purges as a no-op on every path."""

    observations = _load_observations()
    report = observations.purge(tmp_path)
    assert report == [
        {"path": str(tmp_path / "run-observations.jsonl"), "present": False},
        {"path": str(tmp_path / "derived-frontiers.json"), "present": False},
        {"path": str(tmp_path / "quota-observations.jsonl"), "present": False},
    ]
    assert not list(tmp_path.iterdir())


def test_the_observation_cli_purge_previews_without_yes_and_removes_with_it(
    tmp_path: Path,
) -> None:
    """The Skill's own seam reaches the Library's purge without reimplementing it."""

    script = str(MODEL_SELECTOR / "scripts" / "observations.py")
    observations = _load_observations()
    _import(observations, tmp_path, _judged_attempts(_routed_decision(), 1, "pass", 0))

    preview = subprocess.run(
        ["uv", "run", script, "purge", f"--data={tmp_path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert preview.returncode == 0, preview.stdout + preview.stderr
    rendered = json.loads(preview.stdout)
    assert rendered["confirmed"] is False
    assert (tmp_path / "run-observations.jsonl").exists()

    done = subprocess.run(
        ["uv", "run", script, "purge", "--yes", f"--data={tmp_path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["confirmed"] is True
    assert not (tmp_path / "run-observations.jsonl").exists()

    # An unsupported option is refused rather than ignored.
    unsupported = subprocess.run(
        ["uv", "run", script, "purge", "--all", f"--data={tmp_path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert unsupported.returncode == 2
    assert (
        json.loads(unsupported.stdout)["artifact_refusal"]["code"]
        == "invalid_arguments"
    )


def test_evidence_reset_removes_exactly_seven_paths_and_leaves_the_rest_byte_identical(
    tmp_path: Path,
) -> None:
    """The three owning engines' `purge`, run together, are decision 1's set.

    Every other file `references/evidence-ledger.md`'s `## Store` table
    names, and `config.json` and its history, are untouched byte for byte
    (issue #227).
    """

    data = tmp_path / "model-selector"
    data.mkdir()

    observations = _load_observations()
    policy = _load_standing_policy()
    spec = importlib.util.spec_from_file_location(
        "model_selector_capture_for_reset", MODEL_SELECTOR / "scripts" / "capture.py"
    )
    assert spec and spec.loader
    capture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(capture)

    # Populate every file this act removes.
    _import(observations, data, _judged_attempts(_routed_decision(), 1, "pass", 0))
    (data / "quota-observations.jsonl").write_text(
        json.dumps({"access_channel_key": "sha256:channel"}) + "\n", encoding="utf-8"
    )
    policy.move_starting_rung(
        data,
        "orchestrate/amend",
        {"model": "worker-v3", "portable_deliberation": "high"},
        {"kind": "failure_threshold", "run_keys": ["run-1", "run-2"]},
    )
    capture.install(
        data,
        tmp_path / "home",
        ["claude-code"],
        ["uv", "run", "capture.py", "hook"],
    )
    seat = {"model": "worker-v2-2026-05-01", "portable_deliberation": "medium"}
    capture.hook(
        data,
        "SessionStart",
        {"session_id": "session-1", "harness": "claude-code", "seat": seat},
    )
    capture.hook(
        data, "SessionEnd", {"session_id": "session-1", "harness": "claude-code"}
    )

    # Populate every file this act must leave untouched: the profile, and
    # every record type `references/evidence-ledger.md`'s `## Store` table
    # names beyond the three files just written.
    survivors = {
        "config.json": '{"schema_version": 1}\n',
        "config-history.jsonl": '{"revision": 1}\n',
        "source-states.jsonl": '{"source_key": "sha256:s"}\n',
        "access-channel-snapshots.jsonl": '{"key": "sha256:a"}\n',
        "model-versions.jsonl": '{"key": "sha256:m"}\n',
        "alias-bindings.jsonl": '{"provider": "anthropic"}\n',
        "capability-priors.jsonl": '{"key": "sha256:c"}\n',
        "price-schedules.jsonl": '{"key": "sha256:p"}\n',
        "subscription-schedules.jsonl": '{"key": "sha256:sub"}\n',
        "access-mode-availability.jsonl": '{"key": "sha256:mode"}\n',
        "benchmark-definitions.jsonl": '{"key": "sha256:bench"}\n',
        "evaluation-configurations.jsonl": '{"fingerprint": "sha256:eval"}\n',
    }
    for name, content in survivors.items():
        (data / name).write_text(content, encoding="utf-8")
    before = {name: (data / name).read_bytes() for name in survivors}

    removed_paths = {
        "run-observations.jsonl",
        "derived-frontiers.json",
        "quota-observations.jsonl",
        "standing-policy.json",
        "standing-policy-history.jsonl",
    }
    for name in removed_paths:
        assert (data / name).exists(), name
    assert (data / "capture").exists()
    assert (data / "usage-records.jsonl").exists()

    # Confirmed, run every owning engine's purge together.
    observations.purge(data)
    policy.purge(data)
    capture.purge(data)

    # Assert exactly the seven measurement paths are gone.
    for name in removed_paths:
        assert not (data / name).exists(), name
    assert not (data / "capture").exists()
    assert not (data / "usage-records.jsonl").exists()

    # Assert everything else is byte-identical, `config.json` included.
    for name, original in before.items():
        assert (data / name).read_bytes() == original, name


def test_observation_cli_accepts_the_attached_spelling_its_skill_body_writes(
    tmp_path: Path,
) -> None:
    """The engine parses the one flag spelling the Skill body prescribes."""

    # Take the two command lines from the Skill body instead of restating them.
    body = _read("SKILL.md")
    assert "observe --artifact=<path> [--import] [--data=<directory>] <path>" in body
    assert "record --data=<directory> <path>" in body

    # Emit through the process seam with the attached spelling.
    script = str(MODEL_SELECTOR / "scripts" / "observations.py")
    attempts = tmp_path / "attempts.json"
    attempts.write_text(json.dumps(_attempts()), encoding="utf-8")
    artifact = tmp_path / "scratch" / "observations.json"
    emitted = subprocess.run(
        ["uv", "run", script, "observe", f"--artifact={artifact}", str(attempts)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert emitted.returncode == 0, emitted.stdout
    assert json.loads(emitted.stdout)["artifact"] == str(artifact)

    # Import the emitted artifact with the attached spelling as well.
    data = tmp_path / "data"
    imported = subprocess.run(
        ["uv", "run", script, "record", f"--data={data}", str(artifact)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert imported.returncode == 0, imported.stdout
    report = json.loads(imported.stdout)
    assert report["verb"] == "record"
    assert len(report["accepted"]) == 1
    assert (data / "run-observations.jsonl").exists()


def test_observation_contract_separates_public_and_orchestrated_imports() -> None:
    """Delegation stays emission-only while Orchestrate imports at verdict."""

    skill = _read("SKILL.md")
    observe_page = _read("help/observe.md")
    record_page = _read("help/record.md")
    contract = _read("references/run-observations.md")
    public_contract = f"{skill}\n{observe_page}\n{record_page}\n{contract}"
    required_fragments = {
        "caller-owned scratch",
        "Orchestrate",
        "automatically",
        "shared Library",
        "delegation",
        "objective checker",
        "frozen rubric",
        "declared failure signal",
        "explicit user confirmation",
        "self-report",
        "workload stratum",
        "`null`",
        "idempotent",
        "conflicting identity",
        "prompts",
        "transcripts",
        "absolute paths",
        "artifact hashes",
    }

    _assert_contains_all(public_contract, required_fragments)
    assert "| `observe` | `$HERE/help/observe.md` |" in skill
    assert "/model-selector observe --artifact=<path> [--import] <path>" in skill


def test_observation_contract_pins_its_outcome_and_refusal_vocabulary() -> None:
    """An unjudged, self-graded, or unsanitized attempt has a stable answer."""

    contract = _read("references/run-observations.md")
    required_fragments = {
        "no_outcome",
        "unlaunched_decision",
        "incomplete_attempt",
        "self_reported_outcome",
        "unchecked_outcome",
        "non_model_condition_outcome",
        "unsanitized_value",
        "conflicting_identity",
        "initial_build",
        "mechanical_wave_fix",
        "delegated_execution",
        "mechanical_hinder",
        "open_decision",
        "discovered_dependency",
        "tracker_failure",
        "infra_error",
        "abstain",
        "cheap-first",
        "never inferred as zero",
    }

    _assert_contains_all(contract, required_fragments)
    assert "merge_collision" not in contract


STANDING_POLICY: Path = (
    REPO_ROOT / "skills" / "kntnt" / "library" / "scripts" / "standing_policy.py"
)


def _load_standing_policy() -> Any:
    """Load the shared Standing Policy store from its installed Library path."""

    spec = importlib.util.spec_from_file_location(
        "kntnt_standing_policy", STANDING_POLICY
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_damaged_store_is_reported_rather_than_read_as_an_unmoved_cohort(
    tmp_path: Path,
) -> None:
    """A file that will not parse is not the same fact as no file at all.

    Routing keeps working either way, because the shipped default is a whole
    policy — but a damaged store puts every ratcheted Cohort back at its cold
    start, and that is indistinguishable from a Cohort that never moved
    unless the command a human reads says which one it found.
    """

    policy = _load_standing_policy()

    # An absent store is no override and nothing to report.
    assert policy.store_is_damaged(tmp_path) is False

    # A present store that will not parse is reported as damaged.
    (tmp_path / "standing-policy.json").write_text("{not json", encoding="utf-8")
    assert policy.store_is_damaged(tmp_path) is True

    # So is one that parses to something other than a policy.
    (tmp_path / "standing-policy.json").write_text('["cohorts"]', encoding="utf-8")
    assert policy.store_is_damaged(tmp_path) is True

    # A whole store is not damaged, however empty its Cohorts are.
    (tmp_path / "standing-policy.json").write_text(
        json.dumps({"schema_version": 1, "cohorts": {}}), encoding="utf-8"
    )
    assert policy.store_is_damaged(tmp_path) is False


def test_standing_policy_ships_a_working_default_before_any_user_step(
    tmp_path: Path,
) -> None:
    """An empty data directory already answers with the shipped policy."""

    policy = _load_standing_policy()
    effective = policy.effective_policy(tmp_path, "orchestrate/initial_build")

    # Assert the shipped symbolic defaults the contract is written against.
    assert effective == {
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
    assert not list(tmp_path.iterdir()), "reading the policy wrote a user file"


def test_a_threshold_movement_and_a_reset_round_trip_through_the_store(
    tmp_path: Path,
) -> None:
    """A moved Cohort keeps its own revision, its history, and its cause."""

    policy = _load_standing_policy()
    rung = {"model": "worker-v3", "portable_deliberation": "high"}

    # Move one Cohort and read the exact override back through the same seam.
    moved = policy.move_starting_rung(
        tmp_path,
        "orchestrate/amend",
        rung,
        {"kind": "failure_threshold", "run_keys": ["run-1", "run-2"]},
    )
    assert moved["revision"] == 1
    effective = policy.effective_policy(tmp_path, "orchestrate/amend")
    assert effective["starting_rung"] == rung
    assert effective["revision"] == 1
    assert policy.effective_policy(tmp_path, "other")["revision"] == 0

    # Assert the append-only history says what moved the Cohort and from where.
    history = policy.history(tmp_path)
    assert len(history) == 1
    assert history[0]["workload_cohort"] == "orchestrate/amend"
    assert history[0]["from"] == "cold_start"
    assert history[0]["to"] == rung
    assert history[0]["revision_before"] == 0
    assert history[0]["revision_after"] == 1
    assert history[0]["cause"] == {
        "kind": "failure_threshold",
        "run_keys": ["run-1", "run-2"],
    }
    assert history[0]["effective_at"]

    # Reset restores the shipped default and appends exactly one more row.
    removed = policy.reset(tmp_path, "orchestrate/amend")
    assert removed == ["orchestrate/amend"]
    assert policy.effective_policy(tmp_path, "orchestrate/amend")["revision"] == 0
    reset_row = policy.history(tmp_path)[1]
    assert reset_row["cause"] == {"kind": "reset"}
    assert reset_row["to"] == "cold_start"
    assert reset_row["revision_before"] == 1
    assert reset_row["revision_after"] == 0


def _invoke_policy(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Run the shipped Standing Policy CLI exactly as the Skill invokes it."""

    return subprocess.run(
        [sys.executable, str(STANDING_POLICY), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def test_the_policy_cli_shows_the_default_and_resets_only_when_confirmed(
    tmp_path: Path,
) -> None:
    """`show` never writes and `reset` follows the destructive confirmation."""

    policy = _load_standing_policy()
    policy.move_starting_rung(
        tmp_path,
        "orchestrate/amend",
        {"model": "worker-v3", "portable_deliberation": "high"},
        {"kind": "failure_threshold", "run_keys": ["run-1", "run-2"]},
    )

    # The whole store renders the shipped default beside every moved Cohort.
    shown = _invoke_policy("policy", "show", f"--data={tmp_path}")
    assert shown.returncode == 0, shown.stdout + shown.stderr
    rendered = json.loads(shown.stdout)
    assert rendered["default"]["starting_rung"] == "cold_start"
    assert rendered["cohorts"]["orchestrate/amend"]["revision"] == 1
    assert len(rendered["history"]) == 1

    # One Cohort narrows the same page to that Cohort's own effective policy.
    narrowed = json.loads(
        _invoke_policy(
            "policy", "show", "orchestrate/amend", f"--data={tmp_path}"
        ).stdout
    )
    assert narrowed["effective"]["starting_rung"]["model"] == "worker-v3"
    assert "cohorts" not in narrowed

    # An unconfirmed reset changes nothing and says how to confirm it.
    refused = _invoke_policy("policy", "reset", f"--data={tmp_path}")
    assert refused.returncode == 2
    assert json.loads(refused.stdout)["refusal"]["code"] == "unconfirmed_reset"
    assert policy.effective_policy(tmp_path, "orchestrate/amend")["revision"] == 1

    # A confirmed operand-free reset removes every override and records each.
    done = _invoke_policy("policy", "reset", "--yes", f"--data={tmp_path}")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["reset"] == ["orchestrate/amend"]
    assert policy.effective_policy(tmp_path, "orchestrate/amend")["revision"] == 0
    assert len(policy.history(tmp_path)) == 2

    # An unsupported option is refused rather than ignored.
    unsupported = _invoke_policy("policy", "show", "--all", f"--data={tmp_path}")
    assert unsupported.returncode == 2
    assert json.loads(unsupported.stdout)["refusal"]["code"] == "invalid_arguments"


def test_the_policy_store_purge_reports_rows_and_bytes_before_removing_both_files(
    tmp_path: Path,
) -> None:
    """`purge` counts the JSON override in bytes and the JSONL history in rows.

    A Standing Policy override is measurement (ADR-0159): `config reset
    --evidence` discards it and its history outright, rather than restoring
    the shipped default the way `reset` does.
    """

    policy = _load_standing_policy()
    policy.move_starting_rung(
        tmp_path,
        "orchestrate/amend",
        {"model": "worker-v3", "portable_deliberation": "high"},
        {"kind": "failure_threshold", "run_keys": ["run-1", "run-2"]},
    )
    store = tmp_path / "standing-policy.json"
    history = tmp_path / "standing-policy-history.jsonl"

    # A preview reports both exact paths and their size, and writes nothing.
    preview = policy.purge_paths(tmp_path)
    by_path = {entry["path"]: entry for entry in preview}
    assert set(by_path) == {str(store), str(history)}
    assert by_path[str(store)] == {
        "path": str(store),
        "present": True,
        "unit": "bytes",
        "count": store.stat().st_size,
    }
    assert by_path[str(history)] == {
        "path": str(history),
        "present": True,
        "unit": "rows",
        "count": 1,
    }
    assert store.exists() and history.exists()

    # Confirmed, purge removes both files and reports exactly what it found.
    removed = policy.purge(tmp_path)
    assert removed == preview
    assert not store.exists()
    assert not history.exists()
    assert policy.effective_policy(tmp_path, "orchestrate/amend")["revision"] == 0


def test_the_policy_store_purge_reports_an_absent_store_as_absent(
    tmp_path: Path,
) -> None:
    """An empty data directory purges as a no-op on both paths."""

    policy = _load_standing_policy()
    report = policy.purge(tmp_path)
    assert report == [
        {"path": str(tmp_path / "standing-policy.json"), "present": False},
        {"path": str(tmp_path / "standing-policy-history.jsonl"), "present": False},
    ]
    assert not list(tmp_path.iterdir())


def test_the_policy_cli_purge_previews_without_yes_and_removes_with_it(
    tmp_path: Path,
) -> None:
    """Unlike `policy reset`, a purge preview is a success and not a refusal."""

    policy = _load_standing_policy()
    policy.move_starting_rung(
        tmp_path,
        "orchestrate/amend",
        {"model": "worker-v3", "portable_deliberation": "high"},
        {"kind": "failure_threshold", "run_keys": ["run-1", "run-2"]},
    )

    preview = _invoke_policy("purge", f"--data={tmp_path}")
    assert preview.returncode == 0, preview.stdout + preview.stderr
    rendered = json.loads(preview.stdout)
    assert rendered["confirmed"] is False
    assert (tmp_path / "standing-policy.json").exists()

    done = _invoke_policy("purge", "--yes", f"--data={tmp_path}")
    assert done.returncode == 0, done.stdout + done.stderr
    assert json.loads(done.stdout)["confirmed"] is True
    assert not (tmp_path / "standing-policy.json").exists()
    assert not (tmp_path / "standing-policy-history.jsonl").exists()

    # An unsupported option is refused rather than ignored.
    unsupported = _invoke_policy("purge", "--all", f"--data={tmp_path}")
    assert unsupported.returncode == 2
    assert json.loads(unsupported.stdout)["refusal"]["code"] == "invalid_arguments"


def test_the_derivation_freezes_the_standing_policy_into_the_snapshot_identity(
    tmp_path: Path,
) -> None:
    """A policy change is a new snapshot and can never reach a running run."""

    policy = _load_standing_policy()
    shipped = _load_router().route(
        {
            "schema_version": 1,
            "context": _derive_context(tmp_path, _runtime_context_request())["context"],
            "requests": [_request()],
        }
    )

    # The shipped default travels with every snapshot, needing no user step.
    frozen = shipped["snapshot"]["override_policy"]["standing_policy"]
    assert frozen == {
        "schema_version": 1,
        "default": policy.shipped_default(),
        "cohorts": {},
    }

    # Moving one Cohort changes the frozen facts, so the identity moves with it.
    policy.move_starting_rung(
        tmp_path / "model-selector",
        "python-refactor",
        {"model": "claude-sonnet-5", "portable_deliberation": "high"},
        {"kind": "failure_threshold", "run_keys": ["run-1", "run-2"]},
    )
    moved = _load_router().route(
        {
            "schema_version": 1,
            "context": _derive_context(tmp_path, _runtime_context_request())["context"],
            "requests": [_request()],
        }
    )
    frozen_cohorts = moved["snapshot"]["override_policy"]["standing_policy"]["cohorts"]
    assert frozen_cohorts["python-refactor"]["revision"] == 1
    assert (
        moved["snapshot"]["snapshot_identity"]
        != shipped["snapshot"]["snapshot_identity"]
    )


def _bounded_snapshot(**entry: Any) -> dict[str, Any]:
    """Freeze one Cohort override into the shared complete routing snapshot."""

    snapshot = _complete_routing_snapshot()
    snapshot["override_policy"]["standing_policy"] = _standing_policy_fixture(
        {"python-refactor": {"revision": 1, **entry}}
    )
    return snapshot


def test_route_excludes_every_point_outside_the_standing_policy_bounds() -> None:
    """A Rung the policy does not reach is excluded, named, and never climbed."""

    # Cap one Cohort below the seat and take the strongest reachable start.
    router = _load_router()
    snapshot = _bounded_snapshot(
        ceiling={"model": "worker-v2", "portable_deliberation": "high"}
    )
    request = _request(reversible=False, checker={"kind": "none"})
    decision = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [request]}
    )["decisions"][0]

    # Assert the strongest point inside the bounds won and the rest are named.
    assert decision["launch"]["portable_deliberation"] == "high"
    out_of_bounds = {
        exclusion["portable_deliberation"]
        for exclusion in decision["exclusions"]
        if exclusion["code"] == "standing_policy_out_of_bounds"
    }
    assert out_of_bounds == {"xhigh", "max"}

    # Assert the same resolved ceiling bounds the escalation ladder.
    ceiling = _bounded_snapshot(
        ceiling={"model": "worker-v2", "portable_deliberation": "low"}
    )
    selected = router.route(
        {"schema_version": 1, "context": ceiling, "requests": [_request()]}
    )["decisions"][0]
    prior, verified_failure = _verified_failure_binding(selected)
    capped = router.route(
        {
            "schema_version": 1,
            "context": ceiling,
            "requests": [
                _request(
                    retry_available=True,
                    prior=prior,
                    verified_failure=verified_failure,
                )
            ],
        }
    )["decisions"][0]
    assert selected["launch"]["portable_deliberation"] == "low"
    assert capped["next_escalation"] is None


def test_route_starts_an_unmeasured_cohort_at_the_rung_its_policy_names() -> None:
    """A moved Cohort starts where the policy put it, or says why it cannot."""

    # Start the same cold request at a Rung above the cold-start heuristic.
    router = _load_router()
    snapshot = _bounded_snapshot(
        starting_rung={"model": "worker-v2", "portable_deliberation": "high"}
    )
    decision = router.route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]
    assert decision["launch"]["portable_deliberation"] == "high"
    assert decision["audit"]["decision_policy"] == "standing_policy_start"

    # Assert the audit states the policy the decision ran under.
    standing = decision["audit"]["standing_policy"]
    assert standing["policy_revision"] == 1
    assert standing["workload_cohort"] == "python-refactor"
    assert standing["starting_rung"] == {
        "model": "worker-v2",
        "portable_deliberation": "high",
    }
    assert standing["current_rung"] == {
        "model": "worker-v2",
        "portable_deliberation": "high",
    }
    assert standing["floor"] == {"model": "worker-v2", "portable_deliberation": "low"}
    assert standing["ceiling"] == {"model": "worker-v2", "portable_deliberation": "max"}
    assert standing["next_rung_up"] == {
        "model": "worker-v2",
        "portable_deliberation": "xhigh",
    }
    assert standing["start_fallback"] is None

    # A Rung the current profile no longer reaches falls back and says so.
    unreachable = _bounded_snapshot(
        starting_rung={"model": "retired-v1", "portable_deliberation": "high"}
    )
    fallen_back = router.route(
        {"schema_version": 1, "context": unreachable, "requests": [_request()]}
    )["decisions"][0]
    assert fallen_back["launch"]["portable_deliberation"] == "low"
    assert fallen_back["audit"]["decision_policy"] == "cold_start_weakest"
    assert (
        fallen_back["audit"]["standing_policy"]["start_fallback"]
        == "standing_policy_start_unavailable"
    )


def test_the_standing_policy_audit_survives_an_inheritance_with_no_candidate() -> None:
    """An inheritance still names the policy, with its concrete members null."""

    # Remove every mapping so nothing survives to resolve a bound against.
    snapshot = _complete_routing_snapshot()
    snapshot["mappings"] = []
    decision = _load_router().route(
        {"schema_version": 1, "context": snapshot, "requests": [_request()]}
    )["decisions"][0]

    assert decision["status"] == "inherit"
    assert decision["audit"]["standing_policy"] == {
        "policy_revision": 0,
        "workload_cohort": "python-refactor",
        "starting_rung": None,
        "current_rung": None,
        "floor": None,
        "ceiling": None,
        "next_rung_up": None,
        "start_fallback": None,
    }


def test_route_contract_pins_the_standing_policy_and_its_bounds() -> None:
    """The policy routing starts from is stated by the contract, not implied."""

    contract = _read("references/model-routing.md")
    required_fragments = {
        "override_policy.standing_policy",
        "workload_cohort",
        "weakest_enabled",
        "main_seat",
        "cold_start",
        "standing_policy_out_of_bounds",
        "standing_policy_start_unavailable",
        "audit.standing_policy",
        "ratchets up only",
        "compared on the model dimension alone",
        "enters the snapshot identity",
    }

    _assert_contains_all(contract, required_fragments)


def test_the_policy_command_is_documented_where_a_reader_looks_for_it() -> None:
    """`config policy` is one grammar across the body, the pages, and the store."""

    skill = _read("SKILL.md")
    parent = _read("help/config.md")
    page = _read("help/config/policy.md")
    store = _read("references/profile-management.md")

    # The command routes to its three pages and states its own invocation.
    for relative in (
        "config/policy.md",
        "config/policy/show.md",
        "config/policy/reset.md",
    ):
        assert f"| `$HERE/help/{relative}` |" in skill, relative
    assert "config policy [show|reset] [--data=<path>] [<cohort>]" in skill
    assert '"$LIBRARY/scripts/standing_policy.py" policy show' in skill
    assert "policy reset --yes --data=<directory> [<cohort>]" in skill

    # The parent page lists it, and the store says where it lives and why.
    assert "**policy**" in parent
    assert "**show**" in page and "**reset**" in page
    _assert_contains_all(
        store,
        {
            "standing-policy.json",
            "standing-policy-history.jsonl",
            "config.lock",
            "revision 0",
            "kntnt-standing-policy-v1",
        },
    )


def _judged(index: int, result: str, **changes: Any) -> dict[str, Any]:
    """Return one externally judged attempt at the Cohort's own starting Rung."""

    judged: dict[str, Any] = {
        "attempt_id": f"build-{index}",
        "attempt_index": index,
        "run_identity": "run-night-1",
        "started_at": f"2026-08-24T1{index}:00:00Z",
        "completed_at": f"2026-08-24T1{index}:04:00Z",
        "outcome": {
            "result": result,
            "authority": "independent_verifier",
            "checker": {"identity": "verify.md", "independent": True},
            "condition": None,
            "scores": None,
        },
    }
    return _attempt(**(judged | changes))


def _imported(observations: Any, directory: Path, *judged: dict[str, Any]) -> Any:
    """Import externally judged attempts through the one ledger mutation seam."""

    produced = observations.observe(_attempts(*judged))["observations"]
    return observations.record(
        observations.merge(None, produced)["artifact"], directory
    )


def test_record_ratchets_a_cohort_one_rung_up_at_its_failure_threshold(
    tmp_path: Path,
) -> None:
    """Two verified failures in the window move the start and name their runs."""

    # Import two externally verified failures at the Cohort's starting Rung.
    observations = _load_observations()
    policy = _load_standing_policy()
    reported = _imported(observations, tmp_path, _judged(1, "fail"), _judged(2, "fail"))
    evaluated = reported["standing_policy"][0]

    # Assert one move, to the Rung the frozen decision itself named next.
    assert [entry["workload_cohort"] for entry in reported["standing_policy"]] == [
        "python-refactor"
    ]
    assert evaluated["outcome"] == "moved"
    assert evaluated["failures"] == 2
    assert evaluated["window"] == 2
    assert evaluated["threshold"] == {"failures": 2, "window": 4}
    assert sorted(evaluated["run_keys"]) == sorted(reported["accepted"])
    assert evaluated["row"]["to"] == {
        "model": "worker-v2",
        "portable_deliberation": "medium",
    }

    # Assert the store and its history agree with what the report claimed.
    effective = policy.effective_policy(tmp_path, "python-refactor")
    assert effective["starting_rung"] == evaluated["row"]["to"]
    assert effective["revision"] == 1
    history = policy.history(tmp_path)
    assert len(history) == 1
    assert history[0]["cause"]["kind"] == "failure_threshold"
    assert sorted(history[0]["cause"]["run_keys"]) == sorted(reported["accepted"])
    assert history[0]["cause"]["source_run_identity"] == "run-night-1"


def test_the_failure_window_holds_the_last_rows_and_counts_only_failures(
    tmp_path: Path,
) -> None:
    """`fail, pass, pass, pass, fail` is one failure in a window of four."""

    # Import five judged attempts whose oldest failure falls out of the window.
    observations = _load_observations()
    policy = _load_standing_policy()
    reported = _imported(
        observations,
        tmp_path,
        _judged(1, "fail"),
        _judged(2, "pass"),
        _judged(3, "pass"),
        _judged(4, "pass"),
        _judged(5, "fail"),
    )
    evaluated = reported["standing_policy"][0]

    # Assert the window is the last four rows and holds one failure of them.
    assert evaluated["outcome"] == "below_threshold"
    assert evaluated["failures"] == 1
    assert evaluated["window"] == 4
    assert evaluated["row"] is None
    assert policy.effective_policy(tmp_path, "python-refactor")["revision"] == 0
    assert policy.history(tmp_path) == []


def test_only_machine_judged_rows_at_the_starting_rung_reach_the_window(
    tmp_path: Path,
) -> None:
    """An exploration, a retry, a soft judgement and damage teach no policy."""

    # Emit five failures and disqualify four of them, each in its own way.
    observations = _load_observations()
    policy = _load_standing_policy()
    produced = observations.observe(
        _attempts(
            _judged(1, "fail"),
            _judged(2, "fail"),
            _judged(
                3,
                "fail",
                outcome={
                    "result": "fail",
                    "authority": "user_confirmation",
                    "checker": {"identity": "the-user", "independent": True},
                    "condition": None,
                    "scores": None,
                },
            ),
            _judged(4, "fail"),
            _judged(5, "fail"),
        )
    )["observations"]
    produced[0]["provenance"]["exploration"] = True
    produced[1]["routed"]["portable_deliberation"] = "medium"
    produced[4]["provenance"]["standing_policy"]["next_rung_up"] = {"model": ""}
    artifact = observations.merge(None, produced)["artifact"]
    evaluated = observations.record(artifact, tmp_path)["standing_policy"][0]

    # Assert only the one comparable failure was counted, so nothing moved.
    assert evaluated["outcome"] == "below_threshold"
    assert evaluated["failures"] == 1
    assert evaluated["window"] == 1
    assert policy.effective_policy(tmp_path, "python-refactor")["revision"] == 0


def test_a_cohort_at_its_ceiling_records_the_evidence_and_moves_nothing(
    tmp_path: Path,
) -> None:
    """The ladder ends where the frozen decision said it did, not one Rung past."""

    # Import two failures whose own decision found no Rung above the one it ran.
    observations = _load_observations()
    policy = _load_standing_policy()
    produced = observations.observe(_attempts(_judged(1, "fail"), _judged(2, "fail")))[
        "observations"
    ]
    for observation in produced:
        observation["provenance"]["standing_policy"]["next_rung_up"] = None
    artifact = observations.merge(None, produced)["artifact"]
    reported = observations.record(artifact, tmp_path)
    evaluated = reported["standing_policy"][0]

    # Assert the threshold tripped, the evidence landed, and the policy did not.
    assert evaluated["outcome"] == "standing_policy_ceiling_reached"
    assert evaluated["failures"] == 2
    assert len(reported["accepted"]) == 2
    assert policy.effective_policy(tmp_path, "python-refactor")["revision"] == 0
    assert policy.history(tmp_path) == []


def test_evidence_frozen_under_an_older_revision_never_moves_a_policy_again(
    tmp_path: Path,
) -> None:
    """A ratcheted Cohort stays where it is until a person resets it."""

    # Ratchet the Cohort once, then replay a second run frozen before the move.
    observations = _load_observations()
    policy = _load_standing_policy()
    _imported(observations, tmp_path, _judged(1, "fail"), _judged(2, "fail"))
    moved = policy.effective_policy(tmp_path, "python-refactor")
    stale = _imported(observations, tmp_path, _judged(3, "fail"), _judged(4, "fail"))
    evaluated = stale["standing_policy"][0]

    # Assert later evidence is kept and its authority over the policy is not.
    assert evaluated["outcome"] == "stale_policy_context"
    assert evaluated["row"] is None
    assert len(stale["accepted"]) == 2
    assert policy.effective_policy(tmp_path, "python-refactor") == moved
    assert len(policy.history(tmp_path)) == 1

    # Assert the reset a person asks for is the only way back down.
    assert policy.reset(tmp_path, "python-refactor") == ["python-refactor"]
    assert policy.effective_policy(tmp_path, "python-refactor")["revision"] == 0


def _exploring_snapshot(**exploration: Any) -> dict[str, Any]:
    """Freeze a Cohort whose Standing Policy starts a Rung above the floor.

    Exploration steps down, so a Cohort already started at the bottom of its
    own ladder has nowhere to go. The fixture ratchets the shipped Cohort up
    to `high`, which is what a threshold trip leaves behind and the state the
    exploration term exists to buy contrast against.
    """

    snapshot = _complete_routing_snapshot()
    snapshot["override_policy"]["standing_policy"] = _standing_policy_fixture(
        {
            "python-refactor": {
                "revision": 3,
                "starting_rung": {
                    "model": "worker-v2",
                    "portable_deliberation": "high",
                },
                **(
                    {
                        "exploration": {
                            "epsilon": 0.1,
                            "max_per_run": 1,
                            "seed": "kntnt-standing-policy-v1",
                        }
                        | exploration
                    }
                    if exploration
                    else {}
                ),
            }
        }
    )
    return snapshot


def _explorable_request(**changes: Any) -> dict[str, Any]:
    """Build the first routed attempt of retry-owned externally checked work."""

    stated = {
        "retry_available": True,
        "exploration_draw": 0.05,
        "exploration_attempts_used": 0,
    }
    stated.update(changes)
    return _request(**stated)


def _explored(snapshot: dict[str, Any], *requests: dict[str, Any]) -> Any:
    """Route one ordered batch against a frozen exploring snapshot."""

    return _load_router().route(
        {
            "schema_version": 1,
            "context": deepcopy(snapshot),
            "requests": [deepcopy(request) for request in requests],
        }
    )["decisions"]


def test_a_drawn_exploration_launches_one_rung_below_the_production_rung() -> None:
    """The budgeted downward step is taken, named, and priced as exploration."""

    # Route the first attempt of reversible externally checked work.
    decision = _explored(_exploring_snapshot(), _explorable_request())[0]

    # Assert the launch is the Rung below the one production would have taken.
    assert decision["status"] == "selected"
    assert decision["launch"]["portable_deliberation"] == "medium"
    assert decision["audit"]["decision_policy"] == "exploration"
    assert decision["audit"]["exploration"] == {
        "production_rung": {"model": "worker-v2", "portable_deliberation": "high"},
        "selected_rung": {"model": "worker-v2", "portable_deliberation": "medium"},
        "production_decision_policy": "standing_policy_start",
    }

    # Assert the Standing Policy audit still names where the Cohort stands.
    standing = decision["audit"]["standing_policy"]
    assert standing["starting_rung"] == {
        "model": "worker-v2",
        "portable_deliberation": "high",
    }
    assert standing["current_rung"] == {
        "model": "worker-v2",
        "portable_deliberation": "medium",
    }


def test_no_exploration_is_emitted_without_the_facts_that_make_one_safe() -> None:
    """Every eligibility fact is load-bearing on its own."""

    snapshot = _exploring_snapshot()
    ineligible = {
        "an undrawn request": _explorable_request(exploration_draw=None),
        "a draw at epsilon": _explorable_request(exploration_draw=0.1),
        "a spent budget": _explorable_request(exploration_attempts_used=1),
        "irreversible work": _explorable_request(reversible=False),
        "unchecked work": _explorable_request(checker={"kind": "none"}),
        "a retry the caller does not own": _explorable_request(retry_available=False),
        "a Cohort the request never names": _explorable_request(workload_cohort=None),
    }

    # Route each request that misses exactly one fact the term requires. A
    # request naming no Cohort routes under the shipped default and cold starts
    # at its own floor, which is the one case that moves for another reason.
    for named, request in ineligible.items():
        stated = {field: value for field, value in request.items() if value is not None}
        decision = _explored(snapshot, stated)[0]
        assert decision["status"] == "selected", named
        assert decision["audit"]["decision_policy"] != "exploration", named
        assert "exploration" not in decision["audit"], named
        if "workload_cohort" in stated:
            assert decision["launch"]["portable_deliberation"] == "high", named


def test_a_run_frozen_for_speed_and_a_cohort_at_its_floor_explore_nothing() -> None:
    """`--fast` and the inclusive floor each end exploration on their own."""

    # Freeze the same Cohort for the other objective the run could have named.
    fast = _exploring_snapshot()
    fast["override_policy"]["objective"] = "time_first"
    hurried = _explored(fast, _explorable_request())[0]
    assert hurried["audit"]["decision_policy"] == "standing_policy_start"
    assert "exploration" not in hurried["audit"]

    # Start the Cohort at the weakest Rung its own ladder reaches.
    floored = _exploring_snapshot()
    floored["override_policy"]["standing_policy"] = _standing_policy_fixture(
        {
            "python-refactor": {
                "revision": 3,
                "starting_rung": {
                    "model": "worker-v2",
                    "portable_deliberation": "low",
                },
            }
        }
    )
    bottomed = _explored(floored, _explorable_request())[0]
    assert bottomed["launch"]["portable_deliberation"] == "low"
    assert "exploration" not in bottomed["audit"]


def test_a_retry_is_never_moved_down_however_the_draw_fell() -> None:
    """The attempt that exists to escalate is never the one that explores."""

    # Route the amend of a verified failure at the Cohort's production Rung.
    snapshot = _exploring_snapshot()
    first = _explored(snapshot, _explorable_request(exploration_draw=0.9))[0]
    launch = first["launch"]
    attempt = {
        "configuration_fingerprint": launch["configuration_fingerprint"],
        "model": launch["model"],
        "channel": launch["channel"],
        "surface": launch["surface"],
        "serving_mode": launch["serving_mode"],
        "adapter_id": launch["adapter_id"],
        "portable_deliberation": launch["portable_deliberation"],
        "native_deliberation": launch["native_deliberation"],
    }
    amend = _explored(
        snapshot,
        _explorable_request(
            request_id="route-2",
            prior=dict(attempt),
            verified_failure={
                "outcome": "failed",
                "checker": {"kind": "external", "signal": "pytest"},
                **attempt,
            },
        ),
    )[0]

    # Assert the retry stays on production and keeps the Rung above it.
    assert amend["launch"]["portable_deliberation"] == "high"
    assert "exploration" not in amend["audit"]
    assert amend["next_escalation"]["portable_deliberation"] == "xhigh"


def test_one_cohort_spends_its_whole_budget_on_the_first_request_that_draws() -> None:
    """The batch counter caps a Cohort at one accepted attempt per run."""

    # Route two drawn requests of one Cohort in one ordered batch.
    first, second = _explored(
        _exploring_snapshot(),
        _explorable_request(request_id="build-1"),
        _explorable_request(request_id="build-2"),
    )

    # Assert the cap held on the second without the ledger being consulted.
    assert first["audit"]["decision_policy"] == "exploration"
    assert second["audit"]["decision_policy"] == "standing_policy_start"
    assert second["launch"]["portable_deliberation"] == "high"


def test_two_accounts_of_one_cohort_refuse_the_whole_artifact() -> None:
    """A caller holding two counts for one Cohort is refused, not reconciled."""

    # Route one batch whose two requests disagree about what the run has spent.
    answered = _load_router().route(
        {
            "schema_version": 1,
            "context": _exploring_snapshot(),
            "requests": [
                _explorable_request(request_id="build-1", exploration_attempts_used=0),
                _explorable_request(request_id="build-2", exploration_attempts_used=1),
            ],
        }
    )

    # Assert nothing was decided and the refusal names the disagreement.
    assert answered["decisions"] == []
    assert answered["artifact_refusal"]["code"] == "inconsistent_exploration_state"


def test_an_exact_lock_outranks_the_draw_that_would_move_it() -> None:
    """A pinned deliberation is the value the caller asked to run at."""

    # Draw an exploration on a request that pins the dimension it would move.
    decision = _explored(
        _exploring_snapshot(), _explorable_request(overrides={"deliberation": "high"})
    )[0]

    # Assert the lock stands and no downward step was taken under it.
    assert decision["launch"]["portable_deliberation"] == "high"
    assert "exploration" not in decision["audit"]


def test_routing_is_byte_identical_where_epsilon_is_zero_or_no_draw_falls() -> None:
    """The term is inert unless a draw actually lands inside it."""

    # Route one artifact under a zero epsilon and one under the shipped budget.
    silent = _explored(
        _exploring_snapshot(epsilon=0), _explorable_request(exploration_draw=0.0)
    )
    undrawn = _explored(
        _exploring_snapshot(), _explorable_request(exploration_draw=0.5)
    )

    # Compare the decisions byte for byte, the policy block being part of the
    # snapshot identity the two artifacts deliberately differ in.
    def _comparable(decisions: Any) -> str:
        stripped = deepcopy(decisions)
        for decision in stripped:
            decision["audit"]["snapshot_identity"] = "identity"
            decision["audit"]["standing_policy"]["policy_revision"] = 0
        return json.dumps(stripped, sort_keys=True)

    assert _comparable(silent) == _comparable(undrawn)
    assert "exploration" not in silent[0]["audit"]


def test_the_derivation_computes_the_draw_the_route_module_never_makes(
    tmp_path: Path,
) -> None:
    """The draw is an input to the artifact, reproducible from its own facts."""

    # Derive one context request carrying this run's identity and its account.
    artifact = _runtime_context_request()
    artifact["run_identity"] = "run-opaque-7"
    artifact["explored_request_ids"] = {"python-refactor": ["route-0"]}
    derived = _derive_context(tmp_path, artifact)
    request = derived["requests"][0]

    # Assert the draw is the documented hash of the four facts behind it.
    identity = _load_router().freeze_context(derived["context"])["snapshot_identity"]
    material = f"kntnt-standing-policy-v1\n{identity}\nrun-opaque-7\nroute-1".encode()
    expected = (
        int.from_bytes(hashlib.sha256(material).digest()[:7], "big") >> 3
    ) / float(1 << 53)
    assert request["exploration_draw"] == expected
    assert 0.0 <= request["exploration_draw"] < 1.0
    assert request["exploration_attempts_used"] == 1

    # Assert the same request derived twice draws exactly the same number.
    again = _derive_context(tmp_path, artifact)
    assert again["requests"][0]["exploration_draw"] == expected


def test_a_rerouted_batch_starts_from_the_count_its_first_routing_saw(
    tmp_path: Path,
) -> None:
    """A resume reproduces its own decision instead of paying for it twice."""

    # Route one batch whose own request the account already explored.
    artifact = _runtime_context_request()
    artifact["run_identity"] = "run-opaque-7"
    cohort = str(artifact["requests"][0]["workload_cohort"])
    request_id = str(artifact["requests"][0]["request_id"])
    artifact["explored_request_ids"] = {cohort: [request_id]}

    # Assert its own attempt is discounted, leaving the budget where it was.
    derived = _derive_context(tmp_path, artifact)
    assert derived["requests"][0]["exploration_attempts_used"] == 0

    # Assert an unrelated Cohort's spend is untouched by this batch.
    artifact["explored_request_ids"] = {cohort: [request_id, "build-99"]}
    again = _derive_context(tmp_path, artifact)
    assert again["requests"][0]["exploration_attempts_used"] == 1


def test_a_run_that_names_no_identity_composes_no_draw_at_all(
    tmp_path: Path,
) -> None:
    """A dry run's preflight can render no Exploration Attempt."""

    # Derive the same request without the run identity a real plan mints.
    derived = _derive_context(tmp_path, _runtime_context_request())

    # Assert nothing exploration-shaped reached the request.
    assert "exploration_draw" not in derived["requests"][0]
    assert "exploration_attempts_used" not in derived["requests"][0]


def test_an_exploration_tag_travels_from_the_decision_into_its_observation() -> None:
    """The one field #217's window reads is copied by the observe allow-list."""

    # Observe two attempts whose frozen decisions differ only in their policy.
    observations = _load_observations()
    explored = _routed_decision()
    explored["audit"]["decision_policy"] = "exploration"
    explored["audit"]["exploration"] = {
        "production_rung": {"model": "worker-v2", "portable_deliberation": "high"},
        "selected_rung": {"model": "worker-v2", "portable_deliberation": "medium"},
        "production_decision_policy": "standing_policy_start",
    }
    produced = observations.observe(
        _attempts(
            _judged(1, "fail", decision=explored),
            _judged(2, "fail"),
        )
    )["observations"]

    # Assert the tag is copied, and only for the attempt that carried it.
    assert produced[0]["provenance"]["exploration"] is True
    assert produced[1]["provenance"]["exploration"] is False


def test_an_exploration_row_never_moves_the_standing_policy_it_ran_under(
    tmp_path: Path,
) -> None:
    """A purchase of information is not evidence about the production Rung."""

    # Import two verified failures, one of them a tagged Exploration Attempt.
    observations = _load_observations()
    policy = _load_standing_policy()
    explored = _routed_decision()
    explored["audit"]["decision_policy"] = "exploration"
    reported = _imported(
        observations,
        tmp_path,
        _judged(1, "fail", decision=explored),
        _judged(2, "fail"),
    )

    # Assert both rows landed and only the production one entered the window.
    assert len(reported["accepted"]) == 2
    evaluated = reported["standing_policy"][0]
    assert evaluated["outcome"] == "below_threshold"
    assert evaluated["failures"] == 1
    assert policy.effective_policy(tmp_path, "python-refactor")["revision"] == 0
