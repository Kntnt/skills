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


def test_route_selects_an_exact_launchable_point() -> None:
    """The public seam returns a complete Harness-native launch decision."""

    result = _load_router().route(
        {
            "schema_version": 1,
            "snapshot": _routing_snapshot(),
            "requests": [
                {
                    "request_id": "build-1",
                    "authority": "execution",
                    "stage": "build",
                    "workload": "Change the Python parser",
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
        "reasoning_effort": "low",
    }
    assert result["decisions"][0]["launch"]["native_deliberation"] == {"effort": "low"}
    assert result["snapshot"]["profile"]["revision"] == "profile-7"


def _request(**changes: Any) -> dict[str, Any]:
    """Build one valid execution request with explicit variations."""

    request = {
        "request_id": "route-1",
        "authority": "execution",
        "stage": "build",
        "workload": "Change the Python parser",
        "workload_tags": ["python"],
        "reversible": True,
        "checker": {"kind": "external", "signal": "pytest"},
        "overrides": {},
    }
    request.update(changes)
    return request


def test_route_preserves_batch_order_and_inherits_the_verdict_seat() -> None:
    """Every request produces one same-position discriminated decision."""

    verdict = _request(request_id="verdict", authority="verdict", stage="verify")
    execution = _request(request_id="execution")
    decisions = _load_router().route(
        {
            "schema_version": 1,
            "snapshot": _routing_snapshot(),
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

    result = _load_router().route(
        {
            "schema_version": 1,
            "snapshot": _routing_snapshot(),
            "requests": [_request(overrides={"model": "worker-v2"})],
        }
    )["decisions"][0]

    assert result["launch"]["model"] == "worker-v2"
    assert result["launch"]["portable_deliberation"] == "low"
    assert result["evidence_class"] == "measurement_based"


def test_route_freezes_max_native_value_in_the_fingerprint() -> None:
    """Max resolves from the snapshot and changes exact-point identity."""

    router = _load_router()
    snapshot = _routing_snapshot()
    first = router.route(
        {
            "schema_version": 1,
            "snapshot": snapshot,
            "requests": [_request(overrides={"deliberation": "max"})],
        }
    )
    changed = _routing_snapshot()
    changed["mappings"][0]["controls"]["max"] = {"effort": "maximum"}
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
    """Checked reversible failure permits one same-model adjacent step."""

    request = _request(
        prior={"configuration_fingerprint": "previous", "portable_deliberation": "low"},
        verified_failure={"signal": "pytest", "configuration_fingerprint": "previous"},
    )
    decision = _load_router().route(
        {"schema_version": 1, "snapshot": _routing_snapshot(), "requests": [request]}
    )["decisions"][0]

    assert decision["next_escalation"] == {
        "model": "worker-v2",
        "portable_deliberation": "medium",
        "consumes_existing_retry": True,
    }


def test_route_inherits_without_a_profile_or_discriminating_evidence() -> None:
    """Absence and honest uncertainty never trigger setup or invented facts."""

    snapshot = _routing_snapshot()
    snapshot["profile"] = None
    absent = _load_router().route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]
    snapshot = _routing_snapshot()
    snapshot["evidence"]["records"] = []
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
    invalid = _routing_snapshot()
    invalid["profile"]["valid"] = False
    cases.append((invalid, _request(), "invalid_profile"))
    cases.append(
        (
            _routing_snapshot(),
            _request(overrides={"deliberation": "auto"}),
            "invalid_request",
        )
    )
    cases.append(
        (
            _routing_snapshot(),
            _request(overrides={"model": "missing"}),
            "unavailable_override",
        )
    )
    unavailable = _routing_snapshot()
    unavailable["mappings"][0]["controls"].pop("xhigh")
    cases.append(
        (
            unavailable,
            _request(overrides={"deliberation": "xhigh"}),
            "unavailable_override",
        )
    )
    unknown = _routing_snapshot()
    unknown["main_seat"]["capability"] = None
    cases.append((unknown, _request(), "unknown_main_seat_ceiling"))
    above = _routing_snapshot()
    above["mappings"][0]["capability"] = 101
    cases.append(
        (above, _request(overrides={"model": "worker-v2"}), "above_main_seat_ceiling")
    )
    unreachable = _routing_snapshot()
    unreachable["harness"]["adapters"] = []
    cases.append((unreachable, _request(), "empty_safe_candidate_set"))
    verdict = _routing_snapshot()
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

    context = _routing_snapshot()
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

    invalid = _routing_snapshot()
    invalid.pop("commercial_facts", None)
    invalid.pop("mappings")
    invalid_decision = _load_router().route(
        {"schema_version": 1, "snapshot": invalid, "requests": [_request()]}
    )["decisions"][0]
    ambiguous = _routing_snapshot()
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
                "snapshot": _routing_snapshot(),
                "requests": [_request()],
            }
        ),
        encoding="utf-8",
    )
    before = artifact.read_bytes()
    completed = subprocess.run(
        [str(MODEL_SELECTOR / "scripts" / "route.py"), str(artifact)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(completed.stdout)["decisions"][0]["status"] == "selected"
    assert completed.stderr == ""
    assert artifact.read_bytes() == before


def test_route_labels_stale_measurements_mixed_and_keeps_costs_separate() -> None:
    """Staleness remains visible and commercial dimensions are not collapsed."""

    snapshot = _routing_snapshot()
    snapshot["evidence"]["records"][0]["stale"] = True
    decision = _load_router().route(
        {"schema_version": 1, "snapshot": snapshot, "requests": [_request()]}
    )["decisions"][0]

    assert decision["evidence_class"] == "mixed"
    assert decision["launch"]["commercial"] == {
        "cash": 1.0,
        "rolling_quota": 2.0,
        "weekly_quota": 3.0,
        "allocated_subscription_cost": None,
        "latency": 4.0,
    }


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
