# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Derive complete routing context from persisted selections and runtime facts."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, NamedTuple, cast

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
ROUTING_DEFAULTS["portable_levels"] = list(route.PORTABLE_LEVELS)

# Extend the routing validator with the three schemas this adapter owns.
route.SCHEMAS_BY_ID.update(
    {
        CONTEXT_SCHEMA["$id"]: CONTEXT_SCHEMA,
        PROFILE_SCHEMA["$id"]: PROFILE_SCHEMA,
        ADAPTER_TEMPLATE_SCHEMA["$id"]: ADAPTER_TEMPLATE_SCHEMA,
    }
)


def _observations() -> Any:
    """Load the Skill's own observation seam beside the routing module.

    Context reads the evidence ledger through exactly the module the public
    `observe` and `record` commands run on, rather than reimplementing the
    projection here: the ledger has one reading, and two would be two answers
    to the same question about the same file.
    """

    path = SKILL_ROOT / "scripts" / "observations.py"
    spec = importlib.util.spec_from_file_location("model_selector_observations", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{path} is not a loadable observation seam")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _standing_policy() -> Any:
    """Load the shared Standing Policy store from the installed Library.

    The store is Library-owned because the import that moves it and the two
    Model Selector surfaces that read it are three callers of one file, and a
    peer Skill's `scripts/` is not an interface any of them may reach into.
    The candidates are the repository, an installed Manager sibling, and a
    Skill-local fallback, exactly as the observation seam resolves its own.
    """

    candidates = (
        SKILL_ROOT.parent.parent / "kntnt/library/scripts/standing_policy.py",
        SKILL_ROOT.parent / "kntnt/library/scripts/standing_policy.py",
        SKILL_ROOT / "library/scripts/standing_policy.py",
    )
    for candidate in candidates:
        if not candidate.exists():
            continue
        spec = importlib.util.spec_from_file_location(
            "kntnt_standing_policy", candidate
        )
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    raise RuntimeError(
        "the Standing Policy store is missing; install or update the Manager"
    )


OBSERVATIONS: Any = _observations()
STANDING_POLICY: Any = _standing_policy()


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


def _profile_references_are_valid(profile: dict[str, Any]) -> bool:
    """Accept only unambiguous channel references from every selection."""

    channel_ids = [channel["channel_id"] for channel in profile["access_channels"]]
    return len(channel_ids) == len(set(channel_ids)) and all(
        selection["channel_id"] in channel_ids
        for selection in profile["model_selections"]
    )


class StoredProfile(NamedTuple):
    """One reading of `config.json` in exactly one of three states.

    A validated profile carries `profile`. An absent one carries neither
    member, absence being the file not existing and nothing else. A profile
    that was read and rejected carries `rejection`, saying what rejected it
    and naming the interview that writes a current one (ADR-0165).
    """

    profile: dict[str, Any] | None = None
    rejection: str | None = None


def _rejected(cause: str) -> StoredProfile:
    """Reject a stored profile with its cause and the one way back."""

    return StoredProfile(
        rejection=f"{cause} Re-run `/model-selector setup` to write a current profile."
    )


def _read_profile(data_directory: Path) -> StoredProfile:
    """Read the stored profile as valid, absent, or present and rejected.

    Version 1 is the only documented shape and nothing migrates an older one
    into it: the profile is a short interview `setup` recreates, and the
    shapes that predate the contract diverge too far to bridge without
    inventing facts (ADR-0165).
    """

    # An unreadable or undecodable file was still configured by somebody, so
    # only its non-existence is the absent state.
    try:
        raw = json.loads((data_directory / "config.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return StoredProfile()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return _rejected(
            f"config.json could not be read: {type(error).__name__}: {error}."
        )

    # A value of the wrong kind never reaches the contract to be judged by it.
    if not isinstance(raw, dict):
        return _rejected("config.json does not hold a JSON object.")

    # Name the failing path and constraint the shared interpreter reports, so
    # a stale shape reads differently from a corrupted file.
    profile = cast(dict[str, Any], raw)
    if error_detail := _schema_error(profile, PROFILE_SCHEMA, "profile"):
        return _rejected(
            f"config.json does not match the current profile contract: {error_detail}."
        )

    # The contract judges each selection alone, so the relationship between
    # them is the one thing left to reject the profile as a whole on.
    if not _profile_references_are_valid(profile):
        return _rejected(
            "config.json holds a model selection that does not resolve to"
            " exactly one configured access channel."
        )

    return StoredProfile(profile=profile)


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
        benchmark_scores = scores.setdefault(cast(str, benchmark), {})
        benchmark_scores[model_seed_id] = max(
            float(score), benchmark_scores.get(model_seed_id, float("-inf"))
        )

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
            sum(seed_ids.get(model) in scores[benchmark] for model in set(candidates)),
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
    seed: dict[str, Any] | None,
    template: dict[str, Any] | None,
    main_seat: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, int],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    """Resolve exact native controls and their portable ordinal ranks."""

    # A carried adapter exposes exactly the main seat's inherited control.
    if template is not None and template["deliberation_source"] == "carried":
        portable = cast(str, main_seat["portable_deliberation"])
        native = cast(dict[str, Any], deepcopy(main_seat["native_deliberation"]))
        controls = {portable: native}
        return controls, {portable: PORTABLE_RANKS[portable]}, [native], controls

    # Resolve only controls verified as supported for the selected model.
    supported = [
        value
        for value in (seed or {}).get("supported_controls", {}).get("effort", [])
        if value in PORTABLE_RANKS
    ]
    if seed is not None and not supported:
        default = seed.get("default_configuration", {}).get("effort") or "medium"
        supported = [default] if default in PORTABLE_RANKS else ["medium"]
    policy = selection["controls"]["effort"]
    mapped = _policy_values(policy, supported)

    # Admit adapters only for values verified by seed and template evidence.
    launchable = list(mapped)
    if template is not None:
        admitted = set(template.get("supported_deliberation", PORTABLE_RANKS))
        launchable = [value for value in launchable if value in admitted]
    controls = {value: {"effort": value} for value in mapped}
    capabilities = {value: PORTABLE_RANKS[value] for value in mapped}
    adapter_controls = {value: controls[value] for value in launchable}
    return controls, capabilities, list(controls.values()), adapter_controls


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


def _specialized_destination(destination: Any, value: str) -> Any:
    """Bind a dynamic string while preserving fixed and carried destinations."""

    # Turn every parameter form into a concrete adapter translation.
    if isinstance(destination, str):
        return {"parameter": destination, "value": value}
    if isinstance(destination, dict) and "parameter" in destination:
        specialized = deepcopy(destination)
        template = specialized.get("value", "{value}")
        specialized["value"] = cast(str, template).replace("{value}", value)
        return specialized
    return deepcopy(destination)


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

    # Require a selected template mode with at least one launchable control.
    if mode not in template["serving_modes"] or not controls:
        return None

    # Bind dynamic model identity while leaving the template immutable on disk.
    launch = deepcopy(template["launch"])
    launch["model_flag"] = _specialized_destination(
        launch["model_flag"], cast(str, model_value)
    )

    # Build the concrete adapter around the specialized launch translation.
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

    # Bind every carried destination to the live session attestation.
    if route._carries_launch_value({"launch": launch}):
        attestation = runtime["harness"].get("inheritance_attestation")
        if not runtime["harness"]["inheritance"] or attestation is None:
            return None
        adapter["inheritance_attestation"] = deepcopy(attestation)

    # Replace a carried deliberation mapping with the exact main-seat value.
    if template["deliberation_source"] == "carried":
        adapter["native_controls"] = [
            deepcopy(runtime["main_seat"]["native_deliberation"])
        ]

    # Keep only concrete adapters admitted by the shared routing schema.
    if route._schema_errors(
        adapter,
        route.REQUEST_SCHEMA["$defs"]["adapter"],
        route.REQUEST_SCHEMA,
        "adapter",
    ):
        return None

    return adapter


def _evidence(data_directory: Path, seed_vintage: str) -> dict[str, Any]:
    """Return the routing evidence the ledger states, ready to be frozen.

    The records are the ledger's own projection, which is what closes the loop
    between one run and the next: an attempt an external verdict judged becomes
    a record the route module classifies, with nothing written by hand in
    between. An absent, unreadable, or empty ledger is simply no evidence, and
    the routing rules answer that with inheritance rather than with an error.
    """

    # Read the ledger as a file this command does not own. It is append-only
    # JSONL a user may hand-write and an interrupted append may truncate, so it
    # can be absent, unreadable, not JSON, or a row missing an identity the
    # projection reads by name — and none of that is a reason to refuse a route
    # the routing rules can answer without any evidence at all.
    try:
        projected = OBSERVATIONS.projected_evidence(data_directory)
    except (OSError, UnicodeDecodeError, ValueError, KeyError):
        projected = {"records": [], "vintage": None}

    # Admit only records the shared routing schema accepts, so one damaged
    # ledger row refuses itself instead of the whole artifact it sits in.
    records = [
        record
        for record in projected["records"]
        if not route._schema_errors(
            record,
            route.REQUEST_SCHEMA["$defs"]["evidence_record"],
            route.REQUEST_SCHEMA,
            "evidence_record",
        )
    ]

    # Date the evidence by exactly the records it holds. Where a row was
    # dropped, the projection's instant may belong to it, so the shipped seed's
    # date is what can still be defended.
    complete = len(records) == len(projected["records"])
    vintage = projected["vintage"] if records and complete else None
    return {
        "identity": route._canonical_digest(records),
        "vintage": vintage or seed_vintage,
        "records": records,
    }


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


def _profile_state(stored: StoredProfile) -> dict[str, Any] | None:
    """Represent the reading as the frozen state routing discriminates on.

    A validated profile is its revision; a rejected one is what rejected it,
    carrying no revision at all because a profile can fail the contract on
    that very member and no trustworthy value exists to put there. An absent
    profile is the null state it always was.
    """

    if stored.profile is not None:
        return {"revision": str(stored.profile["revision"])}
    return None if stored.rejection is None else {"rejection": stored.rejection}


def _derive_context(
    runtime: dict[str, Any],
    stored: StoredProfile,
    data_directory: Path,
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
    evidence = _evidence(data_directory, cast(str, manifest["as_of"]))

    # An absent or rejected profile is a normal inheritance context; neither
    # state withholds the evidence the ledger holds independently of it.
    profile = stored.profile
    if profile is None:
        ranks: dict[str, float | None] = {}
        main_rank = None
        selections: list[dict[str, Any]] = []
    else:
        # Retain only enabled selections whose persisted identity was validated.
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

        # Resolve the live main seat against exact configured model identities.
        configured_main = next(
            (
                selection["canonical_provider_model_id"]
                for selection in profile["model_selections"]
                if _selection_matches(selection, runtime_seat["model"])
            ),
            None,
        )

        # Withhold selection when the main seat has no comparable benchmark.
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
        # Resolve the selection's seed or its explicitly unknown audit seed.
        canonical = cast(str, selection["canonical_provider_model_id"])
        seed = model_seeds.get(canonical)
        audit_seed = seed or {
            "supported_controls": {"effort": [], "serving_modes": []},
            "default_configuration": {
                "effort": "medium",
                "serving_mode": "standard",
            },
        }

        # Match the selected Harness surface to one shipped adapter template.
        template = next(
            (
                item
                for item in templates
                if item["harness"] == runtime_harness["name"]
                and selection["harness_surface"] in item["covers"]
            ),
            None,
        )

        # Freeze only supported mappings while retaining unknown selections.
        controls, control_capabilities, native_order, adapter_controls = (
            _portable_controls(selection, seed, template, runtime_seat)
        )

        # Emit every selected serving mode as an independently auditable point.
        for mode in _serving_modes(selection, audit_seed):
            # Specialize the reachable adapter without changing its template.
            adapter = (
                None
                if template is None
                else _specialized_adapter(
                    template,
                    selection,
                    mode,
                    adapter_controls,
                    runtime,
                )
            )

            # Retain only adapters that can represent the verified controls.
            if adapter is not None:
                adapters.append(adapter)

            # Preserve the configured point even when no adapter can launch it.
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
        "profile": _profile_state(stored),
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
        "override_policy": deepcopy(ROUTING_DEFAULTS)
        | {
            "objective": runtime["objective"],
            "standing_policy": STANDING_POLICY.frozen_policy(data_directory),
        },
    }


def _exploration_draw(
    seed: str, snapshot_identity: str, run_identity: str, request_id: str
) -> float:
    """Draw one request's exploration number from facts that cannot move.

    Routing is deterministic and a reused snapshot reproduces its decisions
    (ADR-0083, ADR-0085), so the draw is derived here and carried into the
    request rather than made inside the route module. The four facts are the
    Cohort's policy seed, the frozen context, the run, and the request, joined
    by a single newline; the digest's first 53 bits over `2^53` are the value,
    which is every bit a float can hold without rounding.
    """

    material = f"{seed}\n{snapshot_identity}\n{run_identity}\n{request_id}"
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return (int.from_bytes(digest[:7], "big") >> 3) / float(1 << 53)


def _spent(explored: Any, batch: set[str]) -> dict[str, int]:
    """Count each Cohort's spent budget, discounting the batch being routed.

    A request the account already explored and that this batch routes again is
    the same attempt reaching `route` a second time, so counting it would move
    the batch off the count its first routing saw and answer it at a different
    Rung. Discounting it is what makes a resume reproduce its own decision
    (ADR-0151).
    """

    if not isinstance(explored, dict):
        return {}
    spent: dict[str, int] = {}
    for cohort, named in explored.items():
        if isinstance(named, list):
            spent[cohort] = len({str(name) for name in named} - batch)
    return spent


def _with_exploration(
    requests: list[dict[str, Any]],
    snapshot_identity: str,
    standing_policy: dict[str, Any],
    run_identity: Any,
    explored: Any,
) -> list[dict[str, Any]]:
    """Write this run's exploration facts into each request that can carry them.

    A request naming no Cohort has no policy to draw against and a caller
    naming no run has no account to spend from — a dry run being exactly that —
    so both leave the requests as they arrived.
    """

    if not isinstance(run_identity, str) or not run_identity:
        return requests
    spent = _spent(explored, {str(request["request_id"]) for request in requests})
    for request in requests:
        cohort = request.get("workload_cohort")
        if not isinstance(cohort, str):
            continue
        entry = standing_policy["cohorts"].get(cohort, standing_policy["default"])
        request["exploration_draw"] = _exploration_draw(
            str(entry["exploration"]["seed"]),
            snapshot_identity,
            run_identity,
            str(request["request_id"]),
        )
        request["exploration_attempts_used"] = spent.get(cohort, 0)
    return requests


def derive(artifact: Any, data_directory: Path) -> dict[str, Any]:
    """Validate one request without turning absent configuration into setup.

    Invalid request or contradictory runtime facts raise ``ValueError`` for the
    process adapter to report as ``invalid_context_input``.
    """

    # Reject structural input before reading any nested runtime facts.
    if error := _schema_error(artifact, CONTEXT_SCHEMA, "context_request"):
        raise ValueError(error)

    # Refuse contradictory duplicates of the active Harness identity.
    if "runtime" in artifact and (
        artifact["runtime"]["main_seat"]["surface"]
        != artifact["runtime"]["harness"]["surface"]
    ):
        raise ValueError("runtime main_seat.surface must equal harness.surface")
    if "runtime" in artifact:
        harness = artifact["runtime"]["harness"]
        attestation = harness.get("inheritance_attestation")
        if (
            attestation is not None
            and attestation["verified"] != harness["inventory_revision"]
        ):
            raise ValueError(
                "runtime inheritance attestation must equal inventory revision"
            )

    # Preserve request order only after validating a reusable snapshot itself.
    requests = deepcopy(artifact["requests"])
    run_identity = artifact.get("run_identity")
    explored = artifact.get("explored_request_ids")
    if "snapshot" in artifact:
        if error := route._snapshot_error(artifact["snapshot"]):
            raise ValueError(error)
        snapshot = deepcopy(artifact["snapshot"])
        return {
            "schema_version": 1,
            "requests": _with_exploration(
                requests,
                str(snapshot["snapshot_identity"]),
                snapshot["override_policy"]["standing_policy"],
                run_identity,
                explored,
            ),
            "snapshot": snapshot,
        }

    # Derive current facts from optional validated local configuration.
    stored = _read_profile(data_directory)
    context = _derive_context(artifact["runtime"], stored, data_directory)

    # Freeze the context here to reach the identity the draw is derived from.
    # The identity `route` computes later is the same function of the same
    # facts, so the two never disagree and no second freezing rule exists.
    return {
        "schema_version": 1,
        "requests": _with_exploration(
            requests,
            str(route.freeze_context(context)["snapshot_identity"]),
            context["override_policy"]["standing_policy"],
            run_identity,
            explored,
        ),
        "context": context,
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

    # Parse the strict attached-value grammar before reading any artifact.
    raw_snapshot: str | None = None
    arguments = _arguments(sys.argv[1:] if argv is None else argv)
    if arguments is None:
        response = _refusal(
            "invalid_arguments",
            "Context accepts [--data=<path>] followed by exactly one artifact path.",
        )
    else:
        # Read the UTF-8 artifact without consulting configuration on failure.
        data_directory, artifact_path = arguments
        try:
            content = artifact_path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            response = _refusal("unreadable_artifact", str(error))
        else:
            # Parse JSON before recovering any raw snapshot member bytes.
            try:
                artifact = json.loads(content)
            except json.JSONDecodeError as error:
                response = _refusal("malformed_json", str(error))
            else:
                # Derive or validate Context while preserving the snapshot.
                raw_snapshot = _raw_object_member(content, "snapshot")
                try:
                    response = derive(artifact, data_directory)
                except ValueError as error:
                    response = _refusal("invalid_context_input", str(error))

    # Emit exactly one machine-readable response and its corresponding status.
    print(_render_response(response, raw_snapshot))
    return 2 if "artifact_refusal" in response else 0


if __name__ == "__main__":
    raise SystemExit(main())
