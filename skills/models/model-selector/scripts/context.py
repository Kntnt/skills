# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Derive complete routing context from persisted selections and runtime facts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

import route

# Derive routing-owned scales without creating a second source of truth.
PORTABLE_RANKS: dict[str, int] = {
    level: rank for rank, level in enumerate(route.PORTABLE_LEVELS, start=1)
}

# Load the immutable schemas and defaults relative to the installed Skill.
SKILL_ROOT: Path = Path(__file__).resolve().parent.parent
CONTEXT_SCHEMA: dict[str, Any] = json.loads(
    (SKILL_ROOT / "references" / "context-request.schema.json").read_text(
        encoding="utf-8"
    )
)
PROFILE_SCHEMA: dict[str, Any] = json.loads(
    (SKILL_ROOT / "references" / "profile.schema.json").read_text(encoding="utf-8")
)
ADAPTER_TEMPLATE_SCHEMA: dict[str, Any] = json.loads(
    (SKILL_ROOT / "references" / "adapter-template.schema.json").read_text(
        encoding="utf-8"
    )
)
ROUTING_DEFAULTS: dict[str, Any] = json.loads(
    (SKILL_ROOT / "data" / "routing-defaults.json").read_text(encoding="utf-8")
)

# Extend the routing validator with the three schemas this adapter owns.
route.SCHEMAS_BY_ID.update(
    {
        CONTEXT_SCHEMA["$id"]: CONTEXT_SCHEMA,
        PROFILE_SCHEMA["$id"]: PROFILE_SCHEMA,
        ADAPTER_TEMPLATE_SCHEMA["$id"]: ADAPTER_TEMPLATE_SCHEMA,
    }
)


def _canonical_digest(value: Any) -> str:
    """Hash one JSON value through the routing contract's canonical form."""

    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _schema_error(value: Any, schema: dict[str, Any], path: str) -> str | None:
    """Return the first violation found by the shared schema interpreter."""

    errors = route._schema_errors(value, schema, schema, path)
    return errors[0] if errors else None


def _read_seed() -> list[dict[str, Any]]:
    """Read the immutable shipped seed without consulting network state."""

    return [
        cast(dict[str, Any], json.loads(line))
        for line in (SKILL_ROOT / "data" / "seed-evidence.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]


def _read_templates() -> list[dict[str, Any]]:
    """Read validated adapter templates in deterministic identifier order."""

    templates = [
        cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
        for path in sorted((SKILL_ROOT / "data" / "adapters").glob("*.json"))
    ]
    for template in templates:
        if error := _schema_error(
            template, ADAPTER_TEMPLATE_SCHEMA, "adapter_template"
        ):
            raise ValueError(error)
    return sorted(templates, key=lambda item: item["adapter_template_id"])


def migrate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Isolate in-memory migration while version 1 is the only documented shape.

    The detached value protects persisted bytes from both current normalization
    and a later version-specific transformation.
    """

    return deepcopy(profile)


def _read_profile(data_directory: Path) -> dict[str, Any] | None:
    """Return one valid normalized profile or the missing-profile state."""

    try:
        raw = json.loads((data_directory / "config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    profile = migrate_profile(raw)
    return None if _schema_error(profile, PROFILE_SCHEMA, "profile") else profile


def _selection_aliases(selection: dict[str, Any]) -> list[str]:
    """Return exact configured aliases without fuzzy identity matching."""

    canonical = selection["canonical_provider_model_id"]
    return [
        value
        for field in ("requested_model_id", "provider_release_id", "resolved_target")
        if isinstance((value := selection.get(field)), str) and value != canonical
    ]


def _selection_matches(selection: dict[str, Any], model: str) -> bool:
    """Match a main-seat model against canonical configured identity facts."""

    return model == selection[
        "canonical_provider_model_id"
    ] or model in _selection_aliases(selection)


def _seed_models(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index model-version and model-reference seed rows by canonical ID."""

    return {
        record["canonical_model_id"]: record
        for record in records
        if record.get("record_type") in {"model_version_seed", "model_reference_seed"}
    }


def _version_key(identifier: str) -> tuple[int, ...]:
    """Order dotted benchmark versions without importing packaging machinery."""

    final = identifier.rsplit(":", 1)[-1]
    return tuple(int(part) for part in re.findall(r"\d+", final))


def _active_benchmarks(records: list[dict[str, Any]]) -> set[str]:
    """Keep only the newest version of every benchmark definition."""

    latest: dict[str, str] = {}
    for record in records:
        if record.get("record_type") != "benchmark_definition_seed":
            continue
        identifier = cast(str, record["seed_id"])
        definition = identifier.rsplit(":", 1)[0]
        if definition not in latest or _version_key(identifier) > _version_key(
            latest[definition]
        ):
            latest[definition] = identifier
    return set(latest.values())


def _capability_ranks(
    records: list[dict[str, Any]],
    model_seeds: dict[str, dict[str, Any]],
    candidates: list[str],
    main_model: str,
) -> tuple[dict[str, float | None], float | None]:
    """Rank comparable models from one newest maximally covering benchmark."""

    # Resolve canonical model IDs to the identities carried by evaluation rows.
    seed_ids = {
        model: cast(str, seed["seed_id"]) for model, seed in model_seeds.items()
    }
    main_seed_id = seed_ids.get(main_model)
    if main_seed_id is None:
        return {}, None

    # Retain maximum scores per model within every non-superseded benchmark.
    scores: dict[str, dict[str, float]] = {}
    active = _active_benchmarks(records)
    for record in records:
        benchmark = record.get("benchmark_seed_id")
        model_seed_id = record.get("model_seed_id")
        score = record.get("score")
        if (
            record.get("record_type") != "evaluation_prior_seed"
            or benchmark not in active
            or not isinstance(model_seed_id, str)
            or not isinstance(score, (int, float))
            or isinstance(score, bool)
        ):
            continue
        held = scores.setdefault(cast(str, benchmark), {})
        held[model_seed_id] = max(float(score), held.get(model_seed_id, float("-inf")))

    # Select the widest shared comparison, using newest version to break ties.
    choices = [
        benchmark
        for benchmark, benchmark_scores in scores.items()
        if main_seed_id in benchmark_scores
    ]
    if not choices:
        return {}, None
    selected = max(
        choices,
        key=lambda benchmark: (
            sum(seed_ids.get(model) in scores[benchmark] for model in candidates),
            _version_key(benchmark),
        ),
    )
    selected_scores = scores[selected]
    ranks = {
        model: selected_scores.get(seed_ids.get(model, "")) for model in candidates
    }
    return ranks, selected_scores[main_seed_id]


def _policy_values(policy: dict[str, Any], supported: list[str]) -> list[str]:
    """Expand a persisted control policy against one model's supported values."""

    if policy["policy"] == "explicit":
        requested = policy["values"] or []
        return [value for value in supported if value in requested]
    return list(supported)


def _portable_controls(
    selection: dict[str, Any],
    seed: dict[str, Any],
    template: dict[str, Any] | None,
    main_seat: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, int], list[dict[str, Any]]]:
    """Resolve exact native controls and their portable ordinal ranks."""

    # A carried adapter exposes exactly the main seat's inherited control.
    if template is not None and template["deliberation_source"] == "carried":
        portable = cast(str, main_seat["portable_deliberation"])
        native = cast(dict[str, Any], deepcopy(main_seat["native_deliberation"]))
        return {portable: native}, {portable: PORTABLE_RANKS[portable]}, [native]

    # Intersect the model seed, persisted policy, and template's portable scale.
    supported = [
        value
        for value in seed.get("supported_controls", {}).get("effort", [])
        if value in PORTABLE_RANKS
    ]
    if not supported:
        default = seed.get("default_configuration", {}).get("effort") or "medium"
        supported = [default] if default in PORTABLE_RANKS else ["medium"]
    if template is not None:
        admitted = set(template.get("supported_deliberation", PORTABLE_RANKS))
        supported = [value for value in supported if value in admitted]
    supported = _policy_values(selection["controls"]["effort"], supported)
    controls = {value: {"effort": value} for value in supported}
    capabilities = {value: PORTABLE_RANKS[value] for value in supported}
    return controls, capabilities, list(controls.values())


def _serving_modes(selection: dict[str, Any], seed: dict[str, Any]) -> list[str]:
    """Expand one selection into every admitted model serving mode."""

    policy = selection["controls"]["serving_modes"]
    if policy["policy"] == "explicit":
        return cast(list[str], policy["values"] or [])
    supported = cast(
        list[str], seed.get("supported_controls", {}).get("serving_modes", [])
    )
    if not supported:
        default = seed.get("default_configuration", {}).get("serving_mode")
        supported = [default or "standard"]
    return _policy_values(policy, supported)


def _specialized_adapter(
    template: dict[str, Any],
    selection: dict[str, Any],
    mode: str,
    controls: dict[str, dict[str, Any]],
    runtime: dict[str, Any],
) -> dict[str, Any] | None:
    """Specialize one shipped template into a concrete route adapter."""

    # Refuse family aliases the Agent tool does not accept.
    model_value = selection["canonical_provider_model_id"]
    if template["model_source"] == "family_alias":
        model_value = cast(str, selection["family"]).removeprefix("claude-")
        if model_value not in template.get("accepted_model_aliases", []):
            return None
    if mode not in template["serving_modes"] or not controls:
        return None

    # Bind dynamic model identity while leaving the template immutable on disk.
    launch = deepcopy(template["launch"])
    launch["model_flag"]["value"] = model_value
    adapter = {
        "adapter_id": template["adapter_template_id"],
        "channel": selection["channel_id"],
        "harness": template["harness"],
        "surface": template["surface"],
        "models": [selection["canonical_provider_model_id"]],
        "serving_modes": [mode],
        "native_controls": list(controls.values()),
        "tool_sets": [[]],
        "policies": [{}],
        "launch": launch,
    }
    if template["deliberation_source"] == "carried":
        attestation = runtime["harness"].get("inheritance_attestation")
        if not runtime["harness"]["inheritance"] or attestation is None:
            return None
        adapter["native_controls"] = [
            deepcopy(runtime["main_seat"]["native_deliberation"])
        ]
        adapter["inheritance_attestation"] = deepcopy(attestation)
    if route._schema_errors(
        adapter,
        route.REQUEST_SCHEMA["$defs"]["adapter"],
        route.REQUEST_SCHEMA,
        "adapter",
    ):
        return None
    return adapter


def _commercial() -> dict[str, None]:
    """Represent every per-attempt commercial dimension as unmeasured."""

    return {dimension: None for dimension in route.COMMERCIAL_DIMENSIONS}


def _main_channel(profile: dict[str, Any], harness: str, model: str) -> str:
    """Resolve the session's channel only from its exact configured selection."""

    selection = next(
        (
            item
            for item in profile["model_selections"]
            if item["harness_surface"] == harness and _selection_matches(item, model)
        ),
        None,
    )
    return "unconfigured" if selection is None else cast(str, selection["channel_id"])


def _derive_context(
    runtime: dict[str, Any],
    profile: dict[str, Any] | None,
) -> dict[str, Any]:
    """Derive one complete current routing context without persistent writes."""

    # Freeze stable seed facts and the exact runtime seat supplied by the
    # caller.
    records = _read_seed()
    manifest = next(
        record for record in records if record["record_type"] == "seed_manifest"
    )
    model_seeds = _seed_models(records)
    runtime_harness = runtime["harness"]
    runtime_seat = runtime["main_seat"]
    evidence_records: list[dict[str, Any]] = []
    evidence = {
        "identity": _canonical_digest(evidence_records),
        "vintage": manifest["as_of"],
        "records": evidence_records,
    }

    # Missing or invalid configuration is a normal inheritance context.
    if profile is None:
        ranks: dict[str, float | None] = {}
        main_rank = None
        selections: list[dict[str, Any]] = []
    else:
        selections = [
            selection
            for selection in profile["model_selections"]
            if selection["enabled"] is True
            and selection["validation_status"] == "validated"
        ]
        candidate_models = [
            cast(str, selection["canonical_provider_model_id"])
            for selection in selections
        ]
        configured_main = next(
            (
                selection["canonical_provider_model_id"]
                for selection in profile["model_selections"]
                if _selection_matches(selection, runtime_seat["model"])
            ),
            None,
        )
        if configured_main is None:
            ranks, main_rank, selections = {}, None, []
        else:
            ranks, main_rank = _capability_ranks(
                records,
                model_seeds,
                candidate_models,
                cast(str, configured_main),
            )
            if main_rank is None:
                selections = []

    # Specialize every enabled validated selection and serving mode in order.
    templates = _read_templates()
    adapters: list[dict[str, Any]] = []
    mappings: list[dict[str, Any]] = []
    for selection in selections:
        canonical = cast(str, selection["canonical_provider_model_id"])
        seed = model_seeds.get(canonical) or {
            "supported_controls": {"effort": [], "serving_modes": []},
            "default_configuration": {
                "effort": "medium",
                "serving_mode": "standard",
            },
        }
        template = next(
            (
                item
                for item in templates
                if item["harness"] == runtime_harness["name"]
                and selection["harness_surface"] in item["covers"]
            ),
            None,
        )
        controls, control_capabilities, native_order = _portable_controls(
            selection, seed, template, runtime_seat
        )
        for mode in _serving_modes(selection, seed):
            adapter = (
                None
                if template is None
                else _specialized_adapter(template, selection, mode, controls, runtime)
            )
            if adapter is not None:
                adapters.append(adapter)
            mappings.append(
                {
                    "model": canonical,
                    "aliases": _selection_aliases(selection),
                    "channel": selection["channel_id"],
                    "surface": template["surface"]
                    if template is not None
                    else selection["harness_surface"],
                    "serving_mode": mode,
                    "model_capability": ranks.get(canonical),
                    "controls": controls,
                    "control_capabilities": control_capabilities,
                    "native_control_order": native_order,
                    "tools": [],
                    "policy": {},
                    "capabilities": [],
                    "commercial": _commercial(),
                    "enabled": True,
                }
            )

    # Complete the seat and Harness shapes consumed by the pure route module.
    channel = runtime_seat.get("channel")
    if channel is None and profile is not None:
        channel = _main_channel(
            profile,
            cast(str, runtime_harness["name"]),
            cast(str, runtime_seat["model"]),
        )
    main_seat = {
        "model": runtime_seat["model"],
        "channel": channel or "unconfigured",
        "surface": runtime_harness["surface"],
        "serving_mode": runtime_seat["serving_mode"],
        "adapter_id": f"{runtime_harness['name']}-main-seat",
        "native_deliberation": deepcopy(runtime_seat["native_deliberation"]),
        "portable_deliberation": runtime_seat["portable_deliberation"],
        "model_capability": main_rank,
        "deliberation_capability": PORTABLE_RANKS[
            runtime_seat["portable_deliberation"]
        ],
        "tools": deepcopy(runtime_seat["tools"]),
        "policy": deepcopy(runtime_seat["policy"]),
    }
    return {
        "snapshot_version": 1,
        "profile": None
        if profile is None
        else {"revision": str(profile["revision"]), "valid": True},
        "evidence": evidence,
        "harness": {
            "name": runtime_harness["name"],
            "surface": runtime_harness["surface"],
            "inventory_revision": runtime_harness["inventory_revision"],
            "inheritance": runtime_harness["inheritance"],
            "adapter_specs": adapters,
        },
        "main_seat": main_seat,
        "mappings": mappings,
        "override_policy": deepcopy(ROUTING_DEFAULTS),
    }


def derive(artifact: Any, data_directory: Path) -> dict[str, Any]:
    """Validate one request without turning absent configuration into setup.

    Invalid request or contradictory runtime facts raise ``ValueError`` for the
    process adapter to report as ``invalid_context_input``.
    """

    if error := _schema_error(artifact, CONTEXT_SCHEMA, "context_request"):
        raise ValueError(error)

    # Refuse contradictory duplicates of the active Harness surface.
    if "runtime" in artifact and (
        artifact["runtime"]["main_seat"]["surface"]
        != artifact["runtime"]["harness"]["surface"]
    ):
        raise ValueError("runtime main_seat.surface must equal harness.surface")
    requests = deepcopy(artifact["requests"])
    if "snapshot" in artifact:
        return {
            "schema_version": 1,
            "requests": requests,
            "snapshot": deepcopy(artifact["snapshot"]),
        }
    profile = _read_profile(data_directory)
    return {
        "schema_version": 1,
        "requests": requests,
        "context": _derive_context(artifact["runtime"], profile),
    }


def _refusal(code: str, detail: str) -> dict[str, Any]:
    """Build a machine-readable process refusal with no partial context."""

    return {
        "schema_version": 1,
        "requests": [],
        "artifact_refusal": {"code": code, "detail": detail},
    }


def _skip_json_whitespace(content: str, index: int) -> int:
    """Advance to the next byte-bearing JSON token."""

    while index < len(content) and content[index] in " \t\r\n":
        index += 1
    return index


def _raw_object_member(content: str, target: str) -> str | None:
    """Recover one top-level JSON value with its original internal bytes."""

    # Walk only validated JSON tokens so strings cannot impersonate member keys.
    decoder = json.JSONDecoder()
    index = _skip_json_whitespace(content, 0)
    if index >= len(content) or content[index] != "{":
        return None
    index += 1
    matched: str | None = None
    while True:
        index = _skip_json_whitespace(content, index)
        if index >= len(content) or content[index] == "}":
            return matched
        key, index = decoder.raw_decode(content, index)
        index = _skip_json_whitespace(content, index)
        if not isinstance(key, str) or index >= len(content) or content[index] != ":":
            return None
        value_start = _skip_json_whitespace(content, index + 1)
        _, value_end = decoder.raw_decode(content, value_start)
        if key == target:
            matched = content[value_start:value_end]
        index = _skip_json_whitespace(content, value_end)
        if index >= len(content) or content[index] not in ",}":
            return None
        if content[index] == "}":
            return matched
        index += 1


def _render_response(response: dict[str, Any], raw_snapshot: str | None) -> str:
    """Keep a validated frozen snapshot byte-exact inside its new envelope."""

    if "snapshot" not in response or raw_snapshot is None:
        return json.dumps(response, sort_keys=True, separators=(",", ":"))
    requests = json.dumps(response["requests"], sort_keys=True, separators=(",", ":"))
    return f'{{"schema_version":1,"requests":{requests},"snapshot":{raw_snapshot}}}'


def _arguments(argv: list[str]) -> tuple[Path, Path] | None:
    """Parse the public attached-value grammar without repairing invalid forms."""

    data_directory = Path.home() / ".kntnt" / "model-selector"
    data_seen = False
    paths: list[str] = []
    for argument in argv:
        if argument.startswith("--data=") and len(argument) > len("--data="):
            if data_seen or paths:
                return None
            data_seen = True
            data_directory = Path(argument.removeprefix("--data=")).expanduser()
        elif argument.startswith("-"):
            return None
        else:
            paths.append(argument)
    return (data_directory, Path(paths[0])) if len(paths) == 1 else None


def main(argv: list[str] | None = None) -> int:
    """Emit a route artifact on exit 0 or one stable refusal on exit 2."""

    # Refuse malformed process input before reading configuration or seed data.
    raw_snapshot: str | None = None
    arguments = _arguments(sys.argv[1:] if argv is None else argv)
    if arguments is None:
        response = _refusal(
            "invalid_arguments",
            "Context accepts [--data=<path>] followed by exactly one artifact path.",
        )
    else:
        data_directory, artifact_path = arguments
        try:
            content = artifact_path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            response = _refusal("unreadable_artifact", str(error))
        else:
            try:
                artifact = json.loads(content)
            except json.JSONDecodeError as error:
                response = _refusal("malformed_json", str(error))
            else:
                raw_snapshot = _raw_object_member(content, "snapshot")
                try:
                    response = derive(artifact, data_directory)
                except ValueError as error:
                    response = _refusal("invalid_context_input", str(error))
    print(_render_response(response, raw_snapshot))
    return 2 if "artifact_refusal" in response else 0


if __name__ == "__main__":
    raise SystemExit(main())
