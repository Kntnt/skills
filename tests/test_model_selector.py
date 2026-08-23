"""Public contracts shipped by the model-selector Skill."""

import hashlib
import json
import re
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
MODEL_SELECTOR: Path = REPO_ROOT / "skills" / "models" / "model-selector"


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
