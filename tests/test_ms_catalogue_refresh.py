"""The pass that keeps the catalogue current from three structured sources.

Every test here is built from payloads recorded on the maintainer's machine on
2026-09-11 and stored under `tests/support/model_selector_refresh/`: Claude
Code's `initialize` control response, Codex's `app-server` exchange ending in
`model/list`, the header of the models cache that exchange left behind, and
OpenRouter's public `GET /api/v1/models`. Account identifiers were redacted and
nothing else was touched, so a parser that reads them reads the shapes the
tools actually emit. A change in either CLI shows up when the fixtures are
recorded again; no test here reaches a network or starts a real harness.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
SHIPPED: Path = REPO_ROOT / "skills" / "models" / "model-selector"
FIXTURES: Path = REPO_ROOT / "tests" / "support" / "model_selector_refresh"

# The instant the recorded exchanges were taken at, give or take a minute. The
# Codex cache the exchange left behind says it was fetched 43 seconds before.
NOW = datetime(2026, 9, 11, 14, 3, 8, tzinfo=UTC)
TODAY = "2026-09-11"
CACHE_AGE = timedelta(seconds=43)


def _module(stem: str) -> Any:
    """Load one shipped module under the plain name its siblings import it by.

    `refresh` imports `profiles` and `launch` inside the function, so both are
    registered here before it runs: under xdist a worker that has not loaded
    them would otherwise resolve the lazy import against nothing.
    """

    if stem in sys.modules:
        return sys.modules[stem]
    spec = importlib.util.spec_from_file_location(stem, SCRIPTS / f"{stem}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[stem] = module
    spec.loader.exec_module(module)
    return module


catalogue = _module("catalogue")
profiles = _module("profiles")
launch = _module("launch")
evidence = _module("evidence")


# --- The recorded payloads ---------------------------------------------------


def _lines(name: str) -> list[dict[str, Any]]:
    """Return one recorded newline-delimited exchange, one message per line."""

    text = (FIXTURES / name).read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _claude_messages() -> list[dict[str, Any]]:
    """Return Claude Code's recorded answer to `initialize`."""

    return _lines("claude-initialize.jsonl")


def _claude_models(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the model list inside a recorded Claude answer, for editing."""

    for message in messages:
        if message.get("type") == "control_response":
            models: list[dict[str, Any]] = message["response"]["response"]["models"]
            return models
    raise AssertionError("the recording holds no control response")


def _codex_pages() -> list[dict[str, Any]]:
    """Return the `result` of each recorded `model/list` page."""

    return [
        message["result"]
        for message in _lines("codex-app-server.jsonl")
        if message.get("id") == 1
    ]


def _openrouter() -> dict[str, Any]:
    """Return OpenRouter's recorded model list, whole."""

    payload: dict[str, Any] = json.loads(
        (FIXTURES / "openrouter-models.json").read_text(encoding="utf-8")
    )
    return payload


def _openrouter_entry(payload: dict[str, Any], slug: str) -> dict[str, Any]:
    """Return one entry of an OpenRouter payload, for editing in place."""

    for entry in payload["data"]:
        if entry["id"] == slug:
            found: dict[str, Any] = entry
            return found
    raise AssertionError(f"{slug} is not in the recording")


def _stamp(instant: datetime) -> str:
    """Return an instant the way Codex writes `fetched_at`."""

    return instant.isoformat().replace("+00:00", "Z")


Reader = Callable[[datetime, float], Any]


def _readers(
    *,
    claude: list[dict[str, Any]] | None = None,
    codex: list[dict[str, Any]] | None = None,
    openrouter: dict[str, Any] | None = None,
    cache_age: timedelta = CACHE_AGE,
    overrides: Mapping[str, Reader] | None = None,
) -> dict[str, Reader]:
    """Return readers replaying the recordings through the shipped parsers."""

    claude_messages = _claude_messages() if claude is None else claude
    codex_pages = _codex_pages() if codex is None else codex
    payload = _openrouter() if openrouter is None else openrouter

    readers: dict[str, Reader] = {
        "claude": lambda started, seconds: catalogue.claude_reading(claude_messages),
        "codex": lambda started, seconds: catalogue.codex_reading(
            codex_pages, _stamp(started - cache_age), started
        ),
        "openrouter": lambda started, seconds: catalogue.openrouter_reading([payload]),
    }
    readers.update(overrides or {})
    return readers


# --- The machine a pass runs on ------------------------------------------------


CHANNELS = {
    "anthropic": {
        "provider": "anthropic",
        "harness": "claude-code",
        "pay": "subscription",
        "plan": "Claude Max 20x",
        "gateway": None,
        "rates": None,
    },
    "openai": {
        "provider": "openai",
        "harness": "codex",
        "pay": "subscription",
        "plan": "ChatGPT Pro 20x",
        "gateway": None,
        "rates": None,
    },
    "spacexai": {
        "provider": "spacexai",
        "harness": "opencode",
        "pay": "api",
        "plan": None,
        "gateway": "openrouter",
        "rates": None,
    },
}


def _here(tmp_path: Path, *, drop: tuple[str, ...] = ()) -> Path:
    """Write a copy of the shipped seed with the named models left out."""

    seed = json.loads(
        (SHIPPED / "data" / "catalogue-seed.json").read_text(encoding="utf-8")
    )
    seed["models"] = [entry for entry in seed["models"] if entry["id"] not in drop]
    here = tmp_path / "skill"
    (here / "data").mkdir(parents=True)
    (here / "data" / "catalogue-seed.json").write_text(
        json.dumps(seed), encoding="utf-8"
    )
    return here


def _machine(
    tmp_path: Path, *makers: str, drop: tuple[str, ...] = ()
) -> tuple[Path, Path, Path]:
    """Return a seed, a data directory holding a profile choosing *makers*, and an agents directory."""

    here = _here(tmp_path, drop=drop)
    data = tmp_path / "data"
    data.mkdir()
    chosen = makers or ("anthropic", "openai", "spacexai")
    (data / "profile.json").write_text(
        json.dumps(
            {
                "harnesses": ["claude-code", "codex", "opencode"],
                "makers": list(chosen),
                "channels": [CHANNELS[maker] for maker in chosen],
                "answered_at": "2026-09-06T09:12:00Z",
            }
        ),
        encoding="utf-8",
    )
    assert profiles.load(data, catalogue.load(data, here)).source == "file"
    return here, data, tmp_path / "agents"


def _pass(
    here: Path,
    data: Path,
    agents: Path,
    *,
    now: datetime = NOW,
    **readers: Any,
) -> dict[str, Any]:
    """Run one pass over the recordings, or over what a test put in their place."""

    report: dict[str, Any] = catalogue.refresh(
        data, here, agents, now=now, readers=_readers(**readers)
    )
    return report


def _model(here: Path, data: Path, identifier: str) -> Any:
    """Return one model of the merged catalogue, or None where it has none."""

    for model in catalogue.load(data, here).models:
        if model.id == identifier:
            return model
    return None


def _journal(data: Path) -> list[dict[str, Any]]:
    """Return every row the passes have journalled, oldest first."""

    path = data / "catalogue-journal.jsonl"
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _rows(data: Path, at: datetime) -> list[dict[str, Any]]:
    """Return the rows one pass journalled, by the instant it ran at."""

    return [row for row in _journal(data) if row["at"] == _stamp(at)]


def _day(created: int) -> str:
    """Return the UTC date of an OpenRouter `created`."""

    return datetime.fromtimestamp(created, UTC).date().isoformat()


# --- The parsers, against what the tools actually emitted ----------------------


def test_the_recorded_claude_list_parses_into_its_models_skipping_default() -> None:
    """The `default` entry names a model the other entries name too."""

    reading = catalogue.claude_reading(_claude_messages())

    assert reading.outcome == "complete"
    listed = {offer.id: offer for offer in reading.listed}
    assert sorted(listed) == [
        "claude-fable-5-1",
        "claude-haiku-4-5-20251001",
        "claude-opus-5",
        "claude-sonnet-5",
    ]
    assert listed["claude-opus-5"].family == "opus"
    assert listed["claude-opus-5"].aliases == ("opus",)
    assert listed["claude-opus-5"].levels == catalogue.LEVELS
    assert listed["claude-haiku-4-5-20251001"].levels is None


def test_a_claude_answer_that_is_not_a_success_is_unreadable() -> None:
    """Only a `success` carrying `models` is a complete Claude list."""

    failed = [
        {
            "type": "control_response",
            "response": {
                "subtype": "error",
                "request_id": "x",
                "error": "not logged in",
            },
        }
    ]

    reading = catalogue.claude_reading(failed)

    assert reading.outcome == "unreadable"
    assert "not logged in" in (reading.reason or "")
    assert reading.listed == ()


def test_the_recorded_codex_list_parses_skipping_hidden_models() -> None:
    """Hidden entries are the vendor's own, and are never offered."""

    reading = catalogue.codex_reading(_codex_pages(), _stamp(NOW - CACHE_AGE), NOW)

    assert reading.outcome == "complete"
    listed = {offer.id: offer for offer in reading.listed}
    assert sorted(listed) == [
        "gpt-5.3-codex-spark",
        "gpt-5.5",
        "gpt-5.6-luna",
        "gpt-5.6-sol",
        "gpt-5.6-terra",
        "gpt-6-astra",
    ]
    assert listed["gpt-6-astra"].family == "astra"
    assert listed["gpt-5.3-codex-spark"].family == "spark"
    assert listed["gpt-5.5"].family == "gpt-5.5"
    assert listed["gpt-5.5"].aliases == ()


def test_codex_s_ultra_is_dropped_from_the_levels_it_lists() -> None:
    """`ultra` is an execution mode, off the ladder, and never enters an entry."""

    reading = catalogue.codex_reading(_codex_pages(), _stamp(NOW - CACHE_AGE), NOW)
    astra = next(offer for offer in reading.listed if offer.id == "gpt-6-astra")

    assert astra.levels == catalogue.LEVELS


def test_a_codex_list_served_from_a_cache_older_than_its_ttl_is_incomplete() -> None:
    """A cache older than the pass minus 300 seconds is Codex's bundled fallback."""

    stale = catalogue.codex_reading(
        _codex_pages(), _stamp(NOW - timedelta(seconds=301)), NOW
    )
    fresh = catalogue.codex_reading(
        _codex_pages(), _stamp(NOW - timedelta(seconds=299)), NOW
    )
    absent = catalogue.codex_reading(_codex_pages(), None, NOW)

    assert stale.outcome == "incomplete"
    assert "fetched_at" in (stale.reason or "")
    assert fresh.outcome == "complete"
    assert absent.outcome == "incomplete"
    assert len(stale.listed) == len(fresh.listed)


def test_a_codex_list_whose_pagination_broke_is_incomplete() -> None:
    """A failure part-way through the pages leaves what was read, marked so."""

    reading = catalogue.codex_reading(
        _codex_pages(), _stamp(NOW - CACHE_AGE), NOW, failure="page 2 did not arrive"
    )

    assert reading.outcome == "incomplete"
    assert "page 2" in (reading.reason or "")


def test_an_openrouter_read_short_of_its_total_count_is_incomplete() -> None:
    """A collected count that does not add up is a truncated read."""

    payload = _openrouter()
    truncated = {**payload, "data": payload["data"][:-1]}

    assert catalogue.openrouter_reading([payload]).outcome == "complete"
    reading = catalogue.openrouter_reading([truncated])
    assert reading.outcome == "incomplete"
    assert str(payload["total_count"]) in (reading.reason or "")


def test_openrouter_pages_are_collected_until_the_total_adds_up() -> None:
    """Two pages whose entries sum to `total_count` are one complete read."""

    payload = _openrouter()
    half = len(payload["data"]) // 2
    first = {
        "data": payload["data"][:half],
        "total_count": payload["total_count"],
        "links": {"next": "/api/v1/models?offset=1"},
    }
    second = {
        "data": payload["data"][half:],
        "total_count": payload["total_count"],
        "links": {"next": None},
    }

    reading = catalogue.openrouter_reading([first, second])

    assert reading.outcome == "complete"
    assert len(reading.entries) == payload["total_count"]


# --- What one pass adds and updates --------------------------------------------


def test_a_pass_adds_a_claude_model_the_catalogue_lacked_with_a_derived_identity(
    tmp_path: Path,
) -> None:
    """Id, family, alias, provider, release date and billing are all derived."""

    here, data, agents = _machine(tmp_path, drop=("claude-sonnet-5",))
    assert _model(here, data, "claude-sonnet-5") is None

    _pass(here, data, agents)

    sonnet = _model(here, data, "claude-sonnet-5")
    created = _openrouter_entry(_openrouter(), "anthropic/claude-sonnet-5")["created"]
    assert sonnet is not None
    assert (sonnet.provider, sonnet.family) == ("anthropic", "sonnet")
    assert "sonnet" in sonnet.aliases
    assert sonnet.released == _day(created)
    assert sonnet.reasoning_billed_as == "output"
    assert sonnet.deliberation == catalogue.LEVELS
    assert sonnet.capability is None
    assert sonnet.price == catalogue.Price(2.0, 0.2, 2.5, 10.0, "USD", "per_mtok")
    assert sonnet.long_context_threshold is None
    assert sonnet.gateways == (("openrouter", "anthropic/claude-sonnet-5"),)
    assert sonnet.source_url == "https://openrouter.ai/anthropic/claude-sonnet-5"
    assert sonnet.retrieved == TODAY
    added = [row for row in _journal(data) if row["model"] == "claude-sonnet-5"]
    assert added == [
        {
            "at": _stamp(NOW),
            "source": "claude",
            "model": "claude-sonnet-5",
            "field": "model",
            "old": None,
            "new": "claude-sonnet-5",
        }
    ]


def test_a_new_model_s_entry_is_complete_in_the_stored_file(tmp_path: Path) -> None:
    """A partial entry would silently lose what the seed would have supplied."""

    here, data, agents = _machine(tmp_path, drop=("claude-sonnet-5",))

    _pass(here, data, agents)

    stored = json.loads((data / "catalogue.json").read_text(encoding="utf-8"))
    entry = next(
        model for model in stored["models"] if model["id"] == "claude-sonnet-5"
    )
    assert set(entry) == set(catalogue.MODEL_FIELDS)
    assert entry["provider_says"] is None
    assert catalogue._model_fault(entry) is None


def test_models_of_an_unchosen_maker_are_left_out(tmp_path: Path) -> None:
    """Nothing is added or repriced for a maker the profile does not choose."""

    here, data, agents = _machine(tmp_path, "anthropic")
    consulted: list[str] = []

    def codex(started: datetime) -> Any:
        consulted.append("codex")
        return catalogue.codex_reading(
            _codex_pages(), _stamp(started - CACHE_AGE), started
        )

    _pass(here, data, agents, overrides={"codex": codex})

    identifiers = {model.id for model in catalogue.load(data, here).models}
    assert "gpt-5.5" not in identifiers
    assert "grok-4.5" not in identifiers
    sol = _model(here, data, "gpt-5.6-sol")
    assert sol.price.input == 4.0
    assert consulted == []
    assert all(row["model"].startswith("claude-") for row in _journal(data))


def test_the_grok_models_offered_are_the_standard_ones_with_a_deliberation_control(
    tmp_path: Path,
) -> None:
    """Variants, multi-agent specials and models with no effort control are not added."""

    here, data, agents = _machine(tmp_path, "spacexai")
    payload = _openrouter()
    template = _openrouter_entry(payload, "x-ai/grok-4.6")
    for slug in ("x-ai/grok-9:batch", "x-ai/grok-9-multi-agent"):
        payload["data"].append(
            {**copy.deepcopy(template), "id": slug, "canonical_slug": slug}
        )
    payload["total_count"] += 2

    _pass(here, data, agents, openrouter=payload)

    groks = sorted(
        model.id
        for model in catalogue.load(data, here).models
        if model.provider == "spacexai"
    )
    assert groks == ["grok-4.3", "grok-4.5", "grok-4.6"]
    grok = _model(here, data, "grok-4.3")
    assert grok.family == "grok"
    assert grok.gateways == (("openrouter", "x-ai/grok-4.3"),)
    assert grok.deliberation == ("low", "medium", "high")
    assert grok.long_context_threshold == 200000


def test_a_grok_lock_still_takes_the_newest_release_after_older_ones_arrive_dated(
    tmp_path: Path,
) -> None:
    """`grok-4.6` shipped undated; the pass dates it before 4.3 and 4.5 outrank it."""

    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents)

    assert catalogue.resolve(catalogue.load(data, here), "grok")[0].id == "grok-4.6"
    created = _openrouter_entry(_openrouter(), "x-ai/grok-4.6")["created"]
    assert _model(here, data, "grok-4.6").released == _day(created)


def test_a_changed_openrouter_price_updates_the_catalogue_and_is_journalled(
    tmp_path: Path,
) -> None:
    """A price row carries the whole card before and after."""

    here, data, agents = _machine(tmp_path)
    _pass(here, data, agents)
    before = catalogue._priced(_model(here, data, "claude-opus-5").price)

    payload = _openrouter()
    _openrouter_entry(payload, "anthropic/claude-opus-5")["pricing"]["prompt"] = (
        "0.000006"
    )
    later = NOW + timedelta(days=1)
    _pass(here, data, agents, now=later, openrouter=payload)

    assert _model(here, data, "claude-opus-5").price.input == 6.0
    rows = _rows(data, later)
    assert rows == [
        {
            "at": _stamp(later),
            "source": "openrouter",
            "model": "claude-opus-5",
            "field": "price",
            "old": before,
            "new": {**before, "input": 6.0},
        }
    ]


def test_openrouter_s_price_replaces_the_seed_s_where_the_two_differ(
    tmp_path: Path,
) -> None:
    """On 2026-09-11 OpenRouter listed Sol at half the seed's figure, and it stands."""

    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents)

    sol = _model(here, data, "gpt-5.6-sol")
    assert sol.price == catalogue.Price(2.0, 0.2, 2.5, 10.0, "USD", "per_mtok")
    assert sol.long_context == catalogue.Price(4.0, 0.4, 5.0, 15.0, "USD", "per_mtok")
    assert any(
        row["model"] == "gpt-5.6-sol" and row["field"] == "price"
        for row in _journal(data)
    )


def test_a_second_pass_over_unchanged_sources_journals_nothing_and_moves_retrieved(
    tmp_path: Path,
) -> None:
    """Re-verifying a fact moves its date; it is no change, `gpt-5.3-codex-spark` included."""

    here, data, agents = _machine(tmp_path)
    _pass(here, data, agents)
    assert _rows(data, NOW)

    later = NOW + timedelta(days=1)
    _pass(here, data, agents, now=later)

    assert _rows(data, later) == []
    assert _model(here, data, "claude-opus-5").retrieved == "2026-09-12"


def test_a_noisy_price_string_is_stored_exactly_and_journals_nothing_twice(
    tmp_path: Path,
) -> None:
    """`0.0000002` per token is 0.2 per million, and float arithmetic says otherwise."""

    assert float("0.0000002") * 1_000_000 != 0.2
    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents)
    later = NOW + timedelta(days=1)
    _pass(here, data, agents, now=later)

    luna = _model(here, data, "gpt-5.6-luna")
    assert luna.price.input == 0.2
    assert luna.price.cache_read == 0.02
    assert [row for row in _rows(data, later) if row["model"] == "gpt-5.6-luna"] == []


def test_haiku_is_matched_by_normalisation_and_the_slug_is_written_back(
    tmp_path: Path,
) -> None:
    """A dated id loses its date, and a hyphen between digits becomes a dot."""

    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents)

    haiku = _model(here, data, "claude-haiku-4-5-20251001")
    assert haiku.gateways == (("openrouter", "anthropic/claude-haiku-4.5"),)
    assert haiku.deliberation == ()
    rows = [
        row for row in _journal(data) if row["model"] == "claude-haiku-4-5-20251001"
    ]
    assert {
        "field": "gateways",
        "old": {},
        "new": {"openrouter": "anthropic/claude-haiku-4.5"},
    }.items() <= next(row for row in rows if row["field"] == "gateways").items()


def test_the_normalisation_rules_match_the_examples_they_were_written_from() -> None:
    """Prefix by provider, drop a trailing date, and dot a hyphen between digits."""

    assert (
        catalogue.openrouter_slug("anthropic", "claude-fable-5-1")
        == "anthropic/claude-fable-5.1"
    )
    assert (
        catalogue.openrouter_slug("anthropic", "claude-haiku-4-5-20251001")
        == "anthropic/claude-haiku-4.5"
    )
    assert catalogue.openrouter_slug("openai", "gpt-6-astra") == "openai/gpt-6-astra"
    assert catalogue.openrouter_slug("spacexai", "grok-4.6") == "x-ai/grok-4.6"


def test_a_new_codex_model_with_no_openrouter_match_is_added_unpriced(
    tmp_path: Path,
) -> None:
    """Its attribution is Codex's own documentation, and the journal says why it has no price."""

    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents)

    spark = _model(here, data, "gpt-5.3-codex-spark")
    assert spark is not None
    assert spark.price is None
    assert spark.family == "spark"
    assert spark.released == TODAY
    assert (
        spark.source_url
        == "https://learn.chatgpt.com/docs/app-server#list-models-modellist"
    )
    assert spark.retrieved == TODAY
    notes = [
        row
        for row in _journal(data)
        if row["model"] == "gpt-5.3-codex-spark" and row.get("note")
    ]
    assert notes == [
        {
            "at": _stamp(NOW),
            "source": "openrouter",
            "model": "gpt-5.3-codex-spark",
            "field": "price",
            "old": None,
            "new": None,
            "note": "no price source",
        }
    ]


def test_an_existing_model_that_loses_its_match_is_journalled_once(
    tmp_path: Path,
) -> None:
    """The row marks the change of state, and a pass that finds it unchanged is silent."""

    here, data, agents = _machine(tmp_path)
    _pass(here, data, agents)
    payload = _openrouter()
    payload["data"] = [
        entry for entry in payload["data"] if entry["id"] != "openai/gpt-5.6-terra"
    ]
    payload["total_count"] -= 1
    price = catalogue._priced(_model(here, data, "gpt-5.6-terra").price)

    second, third = NOW + timedelta(days=1), NOW + timedelta(days=2)
    _pass(here, data, agents, now=second, openrouter=payload)
    _pass(here, data, agents, now=third, openrouter=payload)

    terra = [
        row
        for row in _journal(data)
        if row["model"] == "gpt-5.6-terra" and row["at"] != _stamp(NOW)
    ]
    assert terra == [
        {
            "at": _stamp(second),
            "source": "openrouter",
            "model": "gpt-5.6-terra",
            "field": "price",
            "old": price,
            "new": price,
            "note": "no price source",
        }
    ]
    assert _model(here, data, "gpt-5.6-terra").retrieved == TODAY


def test_an_alias_the_catalogue_holds_survives_a_list_offering_another(
    tmp_path: Path,
) -> None:
    """Aliases are a union, and what a list adds is journalled."""

    here, data, agents = _machine(tmp_path)
    messages = _claude_messages()
    for entry in _claude_models(messages):
        if entry["value"] == "fable":
            entry["value"] = "fablo"

    _pass(here, data, agents, claude=messages)

    fable = _model(here, data, "claude-fable-5-1")
    assert {"fable", "claude-fable-5-1", "claude-fable-5.1", "fablo"} <= set(
        fable.aliases
    )
    rows = [
        row
        for row in _journal(data)
        if row["model"] == "claude-fable-5-1" and row["field"] == "aliases"
    ]
    assert len(rows) == 1
    assert "fablo" in rows[0]["new"] and "fablo" not in rows[0]["old"]
    assert rows[0]["source"] == "claude"


def test_levels_a_harness_list_reports_replace_the_catalogue_s(tmp_path: Path) -> None:
    """Where the list reports levels for a model they win; where it reports none, nothing moves."""

    here, data, agents = _machine(tmp_path)
    messages = _claude_messages()
    for entry in _claude_models(messages):
        if entry["value"] == "sonnet":
            entry["supportedEffortLevels"] = ["low", "high"]

    _pass(here, data, agents, claude=messages)

    assert _model(here, data, "claude-sonnet-5").deliberation == ("low", "high")
    assert _model(here, data, "claude-haiku-4-5-20251001").deliberation == ()
    row = next(
        row
        for row in _journal(data)
        if row["model"] == "claude-sonnet-5" and row["field"] == "deliberation"
    )
    assert (row["source"], row["old"], row["new"]) == (
        "claude",
        list(catalogue.LEVELS),
        ["low", "high"],
    )


# --- A source that cannot be read, or is read short ------------------------------


def test_an_unreadable_claude_list_adds_nothing_while_openrouter_still_prices_claude(
    tmp_path: Path,
) -> None:
    """Only what the source governs is left alone."""

    here, data, agents = _machine(tmp_path, drop=("claude-sonnet-5",))
    payload = _openrouter()
    _openrouter_entry(payload, "anthropic/claude-opus-5")["pricing"]["prompt"] = (
        "0.000006"
    )
    unreadable = {
        "claude": lambda started, seconds: catalogue.unreadable(
            "claude", "claude is not on the PATH"
        )
    }

    report = _pass(here, data, agents, openrouter=payload, overrides=unreadable)

    assert _model(here, data, "claude-sonnet-5") is None
    assert _model(here, data, "claude-opus-5").price.input == 6.0
    assert report["sources"]["claude"]["outcome"] == "unreadable"
    assert report["sources"]["claude"]["reason"] == "claude is not on the PATH"
    stored = json.loads((data / "refresh.json").read_text(encoding="utf-8"))
    assert stored["sources"]["claude"] == report["sources"]["claude"]


def test_an_unreadable_openrouter_changes_no_price_and_adds_undated_models_quietly(
    tmp_path: Path,
) -> None:
    """A model a harness lists is still added, with no date and no price-source row."""

    here, data, agents = _machine(tmp_path)
    unreadable = {
        "openrouter": lambda started, seconds: catalogue.unreadable(
            "openrouter", "HTTP 503"
        )
    }

    report = _pass(here, data, agents, overrides=unreadable)

    assert _model(here, data, "gpt-5.6-sol").price.input == 4.0
    assert _model(here, data, "grok-4.5") is None
    added = _model(here, data, "gpt-5.5")
    assert added is not None
    assert added.released is None
    assert added.price is None
    assert not [row for row in _journal(data) if row.get("note")]
    assert report["sources"]["openrouter"] == {
        "outcome": "unreadable",
        "reason": "HTTP 503",
        "changes": 0,
    }


def test_a_truncated_openrouter_read_changes_nothing_it_governs(tmp_path: Path) -> None:
    """An incomplete price list is no evidence about any price."""

    here, data, agents = _machine(tmp_path)
    payload = _openrouter()
    _openrouter_entry(payload, "anthropic/claude-opus-5")["pricing"]["prompt"] = (
        "0.000006"
    )
    payload["data"] = payload["data"][:-1]

    report = _pass(here, data, agents, openrouter=payload)

    assert _model(here, data, "claude-opus-5").price.input == 5.0
    assert _model(here, data, "grok-4.5") is None
    assert report["sources"]["openrouter"]["outcome"] == "incomplete"
    assert not [row for row in _journal(data) if row["source"] == "openrouter"]


def test_an_incomplete_codex_list_still_adds_models_and_updates_levels(
    tmp_path: Path,
) -> None:
    """A bundled fallback is a positive list, though never evidence of absence."""

    here, data, agents = _machine(tmp_path)

    report = _pass(here, data, agents, cache_age=timedelta(seconds=3600))

    assert report["sources"]["codex"]["outcome"] == "incomplete"
    assert _model(here, data, "gpt-5.5") is not None


def test_no_makers_chosen_writes_the_outcome_and_nothing_else(tmp_path: Path) -> None:
    """A missing or old-shape profile reads no source and writes only `refresh.json`."""

    here = _here(tmp_path)
    called: list[str] = []
    for name, profile in (
        ("missing", None),
        ("old", {"harnesses": ["codex"], "models": ["gpt-5.6-sol"]}),
    ):
        data = tmp_path / name
        data.mkdir()
        if profile is not None:
            (data / "profile.json").write_text(json.dumps(profile), encoding="utf-8")
        before = sorted(path.name for path in data.iterdir())

        def never(started: datetime, seconds: float) -> Any:
            called.append("read")
            raise AssertionError("a source was read")

        report = catalogue.refresh(
            data,
            here,
            tmp_path / "agents",
            now=NOW,
            readers=dict.fromkeys(("claude", "codex", "openrouter"), never),
        )

        assert called == []
        assert report["outcome"] == "no makers chosen"
        assert sorted(path.name for path in data.iterdir()) == sorted(
            [*before, "refresh.json"]
        )
        assert json.loads((data / "refresh.json").read_text(encoding="utf-8")) == {
            "at": _stamp(NOW),
            "outcome": "no makers chosen",
        }
    assert not (tmp_path / "agents").exists()


# --- What a pass leaves behind -------------------------------------------------


def test_a_pass_that_changed_the_catalogue_resyncs_the_agent_definitions(
    tmp_path: Path,
) -> None:
    """A Claude model the pass added has its definitions in the directory it was given."""

    here, data, agents = _machine(tmp_path, drop=("claude-sonnet-5",))

    report = _pass(here, data, agents)

    assert (agents / "kntnt-sonnet-high.md").is_file()
    assert "kntnt-sonnet-high.md" in report["definitions"]["written"]


def test_a_pass_writes_nothing_outside_the_directories_it_was_given(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The real agents directory is a default for a person, never for a test."""

    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents)

    assert list(home.iterdir()) == []
    assert {path.name for path in data.iterdir()} == {
        "profile.json",
        "catalogue.json",
        "catalogue-journal.jsonl",
        "refresh.json",
    }


def test_the_journal_subcommand_prints_the_last_pass_and_a_week_of_changes_and_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Status reads; it moves no marker and rewrites no file."""

    here, data, agents = _machine(tmp_path)
    _pass(here, data, agents, now=NOW - timedelta(days=10))
    payload = _openrouter()
    _openrouter_entry(payload, "anthropic/claude-opus-5")["pricing"]["prompt"] = (
        "0.000006"
    )
    _pass(here, data, agents, now=NOW, openrouter=payload)
    snapshot = {path.name: path.read_bytes() for path in data.iterdir()}
    capsys.readouterr()

    shown = catalogue.journal(data, 7, now=NOW + timedelta(hours=1))

    assert shown["last_pass"]["at"] == _stamp(NOW)
    assert shown["last_pass"]["sources"]["openrouter"]["outcome"] == "complete"
    assert {row["at"] for row in shown["journal"]} == {_stamp(NOW)}
    assert any(row["model"] == "claude-opus-5" for row in shown["journal"])
    assert catalogue.main(["journal", f"--data={data}", "--days=7"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["last_pass"]["at"] == _stamp(NOW)
    assert {path.name: path.read_bytes() for path in data.iterdir()} == snapshot


def test_the_journal_subcommand_says_when_no_pass_has_run(tmp_path: Path) -> None:
    """An empty directory is no pass yet, not an error."""

    shown = catalogue.journal(tmp_path, 7, now=NOW)

    assert shown["last_pass"] is None
    assert shown["journal"] == []
    assert list(tmp_path.iterdir()) == []


# --- Reaching the three sources, and nothing else --------------------------------


def _replaying(recording: str, argv_log: Path) -> str:
    """Return a stand-in harness that answers each request from a recording.

    Each line the pass sends is answered with every recorded line up to and
    including the one answering it — by `id` for JSON-RPC, by the one control
    response for the control protocol — and a notification the pass did not ask
    for is passed along in between, as the real tools do. The argv it was
    started with is written beside it, for the test to read.
    """

    return f"""#!{sys.executable}
import json, sys, time
from pathlib import Path
Path({str(argv_log)!r}).write_text(json.dumps(sys.argv[1:]))
recorded = [json.loads(line) for line in Path({recording!r}).read_text().splitlines() if line.strip()]
for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request and request.get("type") != "control_request":
        continue
    while recorded:
        message = recorded.pop(0)
        print(json.dumps(message), flush=True)
        if message.get("id") == request.get("id") or message.get("type") == "control_response":
            break
time.sleep(60)
"""


def _install(tmp_path: Path, name: str, script: str) -> str:
    """Put one stand-in on a `PATH` of its own, and return that `PATH`."""

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    executable = bin_dir / name
    executable.write_text(script, encoding="utf-8")
    executable.chmod(0o755)
    return str(bin_dir)


def test_the_claude_list_is_read_over_the_control_protocol_without_a_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The exchange is `initialize` and nothing that could start a model."""

    argv_log = tmp_path / "claude-argv.json"
    monkeypatch.setenv(
        "PATH",
        _install(
            tmp_path,
            "claude",
            _replaying(str(FIXTURES / "claude-initialize.jsonl"), argv_log),
        ),
    )

    reading = catalogue.read_claude(NOW)

    assert reading.outcome == "complete", reading.reason
    assert len(reading.listed) == 4
    assert json.loads(argv_log.read_text()) == list(catalogue.CLAUDE_LIST_ARGV[1:])
    assert "--safe-mode" in catalogue.CLAUDE_LIST_ARGV
    assert "--no-session-persistence" in catalogue.CLAUDE_LIST_ARGV
    assert (
        catalogue.CLAUDE_LIST_ARGV[catalogue.CLAUDE_LIST_ARGV.index("--tools") + 1]
        == ""
    )


def test_the_codex_list_is_read_over_json_rpc_and_its_cache_is_checked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`model/list` with hidden entries included, then the cache's `fetched_at`."""

    argv_log = tmp_path / "codex-argv.json"
    monkeypatch.setenv(
        "PATH",
        _install(
            tmp_path,
            "codex",
            _replaying(str(FIXTURES / "codex-app-server.jsonl"), argv_log),
        ),
    )
    home = tmp_path / "codex-home"
    home.mkdir()
    monkeypatch.setenv("CODEX_HOME", str(home))
    started = datetime.now(UTC)
    (home / "models_cache.json").write_text(
        json.dumps({"fetched_at": _stamp(started - CACHE_AGE)}), encoding="utf-8"
    )

    reading = catalogue.read_codex(started)

    assert reading.outcome == "complete", reading.reason
    assert len(reading.listed) == 6
    assert json.loads(argv_log.read_text()) == list(catalogue.CODEX_LIST_ARGV[1:])

    (home / "models_cache.json").write_text(
        json.dumps({"fetched_at": _stamp(started - timedelta(hours=2))}),
        encoding="utf-8",
    )
    assert catalogue.read_codex(started).outcome == "incomplete"


def test_a_harness_that_never_answers_is_stopped_at_the_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A `claude` waiting for a login is killed and reported unreadable."""

    silent = f"#!{sys.executable}\nimport time\ntime.sleep(60)\n"
    monkeypatch.setenv("PATH", _install(tmp_path, "claude", silent))
    monkeypatch.setattr(catalogue, "EXCHANGE_SECONDS", 1.0)

    reading = catalogue.read_claude(NOW)

    assert reading.outcome == "unreadable"
    assert "1" in (reading.reason or "")


def test_a_harness_that_is_not_installed_is_unreadable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No binary is no list, said by name."""

    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))

    assert catalogue.read_claude(NOW).outcome == "unreadable"
    assert catalogue.read_codex(NOW).outcome == "unreadable"


def test_openrouter_is_read_from_its_one_address_and_a_foreign_next_link_is_not_followed() -> (
    None
):
    """Pagination is followed on OpenRouter's own host, and nowhere else."""

    payload = _openrouter()
    half = len(payload["data"]) // 2
    pages = {
        catalogue.OPENROUTER_MODELS_URL: {
            "data": payload["data"][:half],
            "total_count": payload["total_count"],
            "links": {"next": "/api/v1/models?cursor=2"},
        },
        "https://openrouter.ai/api/v1/models?cursor=2": {
            "data": payload["data"][half:],
            "total_count": payload["total_count"],
            "links": {"next": None},
        },
    }
    asked: list[str] = []

    def fetch(url: str, timeout: float) -> bytes:
        asked.append(url)
        return json.dumps(pages[url]).encode()

    reading = catalogue.read_openrouter(NOW, fetch=fetch)

    assert reading.outcome == "complete"
    assert asked == [
        catalogue.OPENROUTER_MODELS_URL,
        "https://openrouter.ai/api/v1/models?cursor=2",
    ]

    pages[catalogue.OPENROUTER_MODELS_URL]["links"]["next"] = (
        "https://elsewhere.example/models"
    )
    asked.clear()
    reading = catalogue.read_openrouter(NOW, fetch=fetch)
    assert reading.outcome == "incomplete"
    assert asked == [catalogue.OPENROUTER_MODELS_URL]


def test_openrouter_that_cannot_be_fetched_is_unreadable() -> None:
    """A failed first page is no list at all."""

    def fetch(url: str, timeout: float) -> bytes:
        raise OSError("connection refused")

    reading = catalogue.read_openrouter(NOW, fetch=fetch)

    assert reading.outcome == "unreadable"
    assert "connection refused" in (reading.reason or "")


def test_the_pass_reads_exactly_the_three_sources() -> None:
    """No other reader is wired in, and none of them names a prompt or a model."""

    assert set(catalogue.READERS) == {"claude", "codex", "openrouter"}
    assert catalogue.OPENROUTER_MODELS_URL == "https://openrouter.ai/api/v1/models"
    assert catalogue.CODEX_LIST_ARGV == ("codex", "app-server", "--listen", "stdio://")
    assert "--model" not in catalogue.CLAUDE_LIST_ARGV


# --- The validator the pass and `adopt` both go through --------------------------


def _adopted(tmp_path: Path, entry: dict[str, Any]) -> dict[str, Any]:
    """Adopt one fetched model entry over the shipped seed, and return the report."""

    document = tmp_path / "fetched.json"
    document.write_text(json.dumps({"models": [entry]}), encoding="utf-8")
    report: dict[str, Any] = catalogue.adopt(
        tmp_path / "data", SHIPPED, document, now="2026-09-11T00:00:00Z"
    )
    return report


@pytest.mark.parametrize("member", [-1.0, "2.0", float("inf"), float("nan"), True])
def test_the_validator_refuses_a_price_member_that_is_not_a_finite_non_negative_number(
    tmp_path: Path, member: Any
) -> None:
    """A plausible wrong number is the validator's to catch where it can."""

    entry = {
        "id": "claude-opus-5",
        "price": {
            "input": member,
            "cache_read": 0.5,
            "cache_write": 6.25,
            "output": 25.0,
            "currency": "USD",
            "unit": "per_mtok",
        },
        "source_url": "https://example.com",
        "retrieved": "2026-09-11",
    }

    report = _adopted(tmp_path, entry)

    assert report["models"] == []
    assert report["discarded"][0]["name"] == "claude-opus-5"
    assert "input" in report["discarded"][0]["reason"]


def test_the_validator_accepts_a_null_price_member_as_unknown(tmp_path: Path) -> None:
    """Null is a state of knowledge, not a malformed number."""

    entry = {
        "id": "grok-4.6",
        "price": {
            "input": 2.0,
            "cache_write": None,
            "currency": "USD",
            "unit": "per_mtok",
        },
        "source_url": "https://example.com",
        "retrieved": "2026-09-11",
    }

    assert _adopted(tmp_path, entry)["discarded"] == []


def test_adopting_a_partial_price_keeps_every_category_it_omits(tmp_path: Path) -> None:
    """Omitted and null both leave the standing figure; the long-context card merges the same way."""

    entry = {
        "id": "gpt-5.6-sol",
        "price": {"input": 3.0, "output": None, "currency": "USD", "unit": "per_mtok"},
        "long_context": {"output": 31.0},
        "source_url": "https://example.com",
        "retrieved": "2026-09-11",
    }

    _adopted(tmp_path, entry)

    sol = _model(SHIPPED, tmp_path / "data", "gpt-5.6-sol")
    assert sol.price == catalogue.Price(3.0, 0.4, 5.0, 20.0, "USD", "per_mtok")
    assert sol.long_context == catalogue.Price(8.0, 0.8, 10.0, 31.0, "USD", "per_mtok")


def test_per_million_conversion_is_decimal_and_rounded_to_six_places() -> None:
    """The one conversion the pass makes is exact."""

    assert catalogue.per_million("0.0000002") == 0.2
    assert catalogue.per_million("0.000000125") == 0.125
    assert catalogue.per_million("0.0000000000001") == 0.0
    assert Decimal(str(catalogue.per_million("0.00001"))) == Decimal(10)


# --- A model gone from its maker's list ------------------------------------------

DAY = timedelta(days=1)
GONE = "gpt-5.6-luna"


def _codex_without(model: str = GONE, *, hidden: bool = False) -> list[dict[str, Any]]:
    """Return the recorded Codex pages with *model* dropped, or marked hidden."""

    pages = copy.deepcopy(_codex_pages())
    for page in pages:
        if hidden:
            for entry in page["data"]:
                if entry["model"] == model:
                    entry["hidden"] = True
        else:
            page["data"] = [entry for entry in page["data"] if entry["model"] != model]
    return pages


def _failing(reason: str) -> Reader:
    """Return a reader whose source could not be read at all."""

    return lambda started, seconds: catalogue.unreadable("codex", reason)


def _measured(
    data: Path, model: str, count: int, *, grade: float = 1.0, first: int = 0
) -> None:
    """Append *count* measurement rows for *model*, in the shape the ledger holds."""

    evidence.append(
        data,
        [
            {
                "attempt_id": f"{model}-{first + index}",
                "at": "2026-09-10T10:00:00Z",
                "kind": "implement",
                "label": None,
                "model": model,
                "deliberation": "high",
                "harness": "codex",
                "channel": None,
                "grade": grade,
                "graded_by": "signal",
                "tokens": {"output": 1000.0},
                "cost_usd": None,
                "seconds": 60.0,
                "routed": False,
            }
            for index in range(count)
        ],
    )


def _waiting(data: Path, model: str, *units: str, failure: str | None = None) -> None:
    """Append pending Units for *model*, each carrying `last_failure` where given."""

    with (data / "pending.jsonl").open("a", encoding="utf-8") as stream:
        for unit in units:
            row: dict[str, Any] = {"unit_id": unit, "model": model}
            if failure is not None:
                row["last_failure"] = failure
                row["attempts"] = 1
            stream.write(json.dumps(row, sort_keys=True) + "\n")


def _ledger(data: Path) -> list[str]:
    """Return the model of every measurement row, in ledger order."""

    return [row.model for row in evidence.load(data)]


def _queued(data: Path) -> list[str]:
    """Return the model of every pending Unit, in queue order."""

    path = data / "pending.jsonl"
    if not path.exists():
        return []
    return [
        json.loads(line)["model"]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _lifecycle(data: Path) -> dict[str, Any]:
    """Return what `lifecycle.json` holds per model, or nothing where it is absent."""

    path = data / "lifecycle.json"
    if not path.exists():
        return {}
    held: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))["models"]
    return held


def _days(
    here: Path,
    data: Path,
    agents: Path,
    count: int,
    *,
    first: datetime = NOW,
    **readers: Any,
) -> list[dict[str, Any]]:
    """Run one pass a day on *count* consecutive days, and return their reports."""

    return [
        _pass(here, data, agents, now=first + index * DAY, **readers)
        for index in range(count)
    ]


def _removals(data: Path) -> list[dict[str, Any]]:
    """Return every removal the journal holds."""

    return [row for row in _journal(data) if row["field"] == "removed"]


def test_a_model_missing_from_three_complete_lists_on_three_days_is_removed_with_its_evidence(
    tmp_path: Path,
) -> None:
    """Its entry, every measurement row and every pending Unit go, and the journal says so."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 3)
    _measured(data, "gpt-5.6-sol", 2)
    _waiting(data, GONE, "u1", "u2")
    _waiting(data, "gpt-5.6-sol", "u3")

    _days(here, data, agents, 2, codex=_codex_without())
    assert _model(here, data, GONE) is not None
    assert _ledger(data).count(GONE) == 3

    _pass(here, data, agents, now=NOW + 2 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is None
    assert _ledger(data) == ["gpt-5.6-sol", "gpt-5.6-sol"]
    assert _queued(data) == ["gpt-5.6-sol"]
    days = [(NOW + index * DAY).date().isoformat() for index in range(3)]
    assert _removals(data) == [
        {
            "at": _stamp(NOW + 2 * DAY),
            "source": "codex",
            "model": GONE,
            "field": "removed",
            "old": None,
            "new": {"absent_days": days, "rows_deleted": 3, "units_dropped": 2},
        }
    ]
    record = _lifecycle(data)[GONE]
    assert record["absent_days"] == days
    assert (record["rows_deleted"], record["units_dropped"]) == (3, 2)


def test_a_failed_read_breaks_the_run_of_absent_days(tmp_path: Path) -> None:
    """Absent, unreadable, absent, absent: a quota running out is no observation."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 1)

    _pass(here, data, agents, now=NOW, codex=_codex_without())
    _pass(
        here,
        data,
        agents,
        now=NOW + DAY,
        overrides={"codex": _failing("the weekly quota ran out")},
    )
    _days(here, data, agents, 2, first=NOW + 2 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is not None
    assert _ledger(data) == [GONE]
    assert _removals(data) == []


def test_a_day_on_which_the_list_shows_the_model_resets_the_run(tmp_path: Path) -> None:
    """Absent, present, absent, absent removes nothing."""

    here, data, agents = _machine(tmp_path)

    _pass(here, data, agents, now=NOW, codex=_codex_without())
    _pass(here, data, agents, now=NOW + DAY)
    _days(here, data, agents, 2, first=NOW + 2 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is not None
    assert _removals(data) == []


def test_a_day_with_no_complete_read_breaks_the_run(tmp_path: Path) -> None:
    """Two absent days, a day read only from Codex's bundled list, then an absent day."""

    here, data, agents = _machine(tmp_path)

    _days(here, data, agents, 2, codex=_codex_without())
    _pass(
        here,
        data,
        agents,
        now=NOW + 2 * DAY,
        codex=_codex_without(),
        cache_age=timedelta(hours=2),
    )
    _pass(here, data, agents, now=NOW + 3 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is not None
    assert _removals(data) == []


def test_a_day_with_no_pass_at_all_breaks_the_run(tmp_path: Path) -> None:
    """Three absent passes on days that are not consecutive are not three days in a row."""

    here, data, agents = _machine(tmp_path)

    _days(here, data, agents, 2, codex=_codex_without())
    _pass(here, data, agents, now=NOW + 3 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is not None


def test_three_failed_runs_of_a_model_its_list_still_shows_remove_nothing(
    tmp_path: Path,
) -> None:
    """Failing to run is channel health, and never a signal that a model is gone."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 3, grade=0.0)
    _waiting(data, GONE, "u1", "u2", failure="exited-nonzero")

    _days(here, data, agents, 3)

    assert _model(here, data, GONE) is not None
    assert _ledger(data) == [GONE, GONE, GONE]
    assert _queued(data) == [GONE, GONE]
    assert _removals(data) == []
    assert _lifecycle(data) == {}


def test_presence_is_judged_on_the_version_identifier_each_list_names(
    tmp_path: Path,
) -> None:
    """`claude-opus-5[1m]` is `claude-opus-5`, and `x-ai/grok-4.6` is `grok-4.6`."""

    here, data, agents = _machine(tmp_path)
    before = {model.id for model in catalogue.load(data, here).models}

    _days(here, data, agents, 3)

    after = {model.id for model in catalogue.load(data, here).models}
    assert {"claude-opus-5", "grok-4.6"} <= after
    assert before <= after
    assert _removals(data) == []
    assert _lifecycle(data) == {}


def test_a_model_the_codex_list_returns_marked_hidden_is_present(
    tmp_path: Path,
) -> None:
    """Deletion cannot be undone, so only a model the list no longer returns is absent."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 1)

    _days(here, data, agents, 3, codex=_codex_without(hidden=True))

    assert _model(here, data, GONE) is not None
    assert _ledger(data) == [GONE]


def test_a_family_alias_moved_to_a_successor_does_not_keep_the_old_release(
    tmp_path: Path,
) -> None:
    """`opus` naming `claude-opus-6` counts `claude-opus-5` absent, and its definitions go."""

    here, data, agents = _machine(tmp_path)
    _pass(here, data, agents, now=NOW - DAY)
    assert "claude-opus-5" in (agents / "kntnt-opus-high.md").read_text(
        encoding="utf-8"
    )

    succeeded = _claude_messages()
    for entry in _claude_models(succeeded):
        if entry["resolvedModel"] == "claude-opus-5[1m]":
            entry["resolvedModel"] = "claude-opus-6[1m]"
    _days(here, data, agents, 3, claude=succeeded)

    assert _model(here, data, "claude-opus-5") is None
    assert _model(here, data, "claude-opus-6") is not None
    named = [path.read_text(encoding="utf-8") for path in agents.glob("kntnt-*.md")]
    assert named
    assert not any("claude-opus-5" in text for text in named)
    assert "claude-opus-6" in (agents / "kntnt-opus-high.md").read_text(
        encoding="utf-8"
    )


def test_a_removed_model_gone_from_every_file_leaves_no_definitions_of_its_family(
    tmp_path: Path,
) -> None:
    """A family with no release remaining has its definitions removed."""

    here, data, agents = _machine(tmp_path)
    _pass(here, data, agents, now=NOW - DAY)
    assert (agents / "kntnt-sonnet-high.md").is_file()
    dropped = _claude_messages()
    models = _claude_models(dropped)
    models[:] = [entry for entry in models if entry["value"] != "sonnet"]

    reports = _days(here, data, agents, 3, claude=dropped)

    assert _model(here, data, "claude-sonnet-5") is None
    assert not list(agents.glob("kntnt-sonnet-*.md"))
    assert "kntnt-sonnet-high.md" in reports[-1]["definitions"]["removed"]


def test_a_removed_seed_model_stays_removed_across_a_reload_and_an_adopt(
    tmp_path: Path,
) -> None:
    """The mask hides the seed's copy, and an `adopt` rewriting `catalogue.json` keeps it."""

    here, data, agents = _machine(tmp_path)
    _days(here, data, agents, 3, codex=_codex_without())
    assert _model(here, data, GONE) is None

    document = tmp_path / "fetched.json"
    document.write_text(
        json.dumps(
            {
                "models": [
                    {
                        "id": "gpt-5.6-sol",
                        "price": {"input": 3.0},
                        "source_url": "https://example.com",
                        "retrieved": "2026-09-14",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    assert catalogue.adopt(data, here, document)["written"] is not None

    assert _model(here, data, GONE) is None
    assert GONE in _lifecycle(data)
    assert _model(here, data, "gpt-5.6-sol").price.input == 3.0


def test_a_row_filed_for_a_removed_model_after_its_removal_is_deleted_by_the_next_pass(
    tmp_path: Path,
) -> None:
    """Capture appends without a lock, so every pass clears the ids it removed."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 2)
    _days(here, data, agents, 3, codex=_codex_without())
    _measured(data, GONE, 1, first=10)
    _waiting(data, GONE, "late")

    _pass(here, data, agents, now=NOW + 3 * DAY, codex=_codex_without())

    assert _ledger(data) == []
    assert _queued(data) == []
    record = _lifecycle(data)[GONE]
    assert (record["rows_deleted"], record["units_dropped"]) == (3, 1)
    assert len(_removals(data)) == 1


def test_a_pass_that_chooses_no_maker_still_clears_the_rows_of_removed_models(
    tmp_path: Path,
) -> None:
    """Nothing is read, but a row capture filed after the removal still goes."""

    here, data, agents = _machine(tmp_path)
    _days(here, data, agents, 3, codex=_codex_without())
    _measured(data, GONE, 2)
    (data / "profile.json").unlink()

    report = _pass(here, data, agents, now=NOW + 3 * DAY)

    assert report["outcome"] == "no makers chosen"
    assert _ledger(data) == []
    assert _lifecycle(data)[GONE]["rows_deleted"] == 2


def test_a_removed_model_re_added_by_its_list_is_an_ordinary_model_again(
    tmp_path: Path,
) -> None:
    """The re-add ends the removal: its rows are kept, and `lifecycle.json` forgets it."""

    here, data, agents = _machine(tmp_path)
    _days(here, data, agents, 3, codex=_codex_without())
    assert _model(here, data, GONE) is None

    _pass(here, data, agents, now=NOW + 3 * DAY)
    assert _model(here, data, GONE) is not None
    assert GONE not in _lifecycle(data)
    _measured(data, GONE, 1)
    _waiting(data, GONE, "after")

    _pass(here, data, agents, now=NOW + 4 * DAY)

    assert _ledger(data) == [GONE]
    assert _queued(data) == [GONE]
    assert GONE not in _lifecycle(data)


def test_a_removed_model_re_added_through_adopt_is_forgotten_in_the_same_operation(
    tmp_path: Path,
) -> None:
    """A pass running before the next refresh never deletes a row filed after the re-add."""

    here, data, agents = _machine(tmp_path)
    _days(here, data, agents, 3, codex=_codex_without())
    document = tmp_path / "fetched.json"
    document.write_text(
        json.dumps(
            {
                "models": [
                    {
                        "id": GONE,
                        "provider": "openai",
                        "family": "luna",
                        "source_url": "https://example.com",
                        "retrieved": "2026-09-14",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    catalogue.adopt(data, here, document)

    assert _model(here, data, GONE) is not None
    assert GONE not in _lifecycle(data)


def test_with_the_lock_busy_the_model_is_removed_and_its_rows_wait_for_the_next_pass(
    tmp_path: Path,
) -> None:
    """The catalogue entry goes at once; the rows go when a pass gets the lock."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 2)
    _waiting(data, GONE, "u1")
    _days(here, data, agents, 2, codex=_codex_without())

    with evidence.lock(data) as held:
        assert held is True
        _pass(here, data, agents, now=NOW + 2 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is None
    assert _ledger(data) == [GONE, GONE]
    assert _removals(data)[0]["new"]["rows_deleted"] == 0

    _pass(here, data, agents, now=NOW + 3 * DAY, codex=_codex_without())

    assert _ledger(data) == []
    assert _queued(data) == []
    record = _lifecycle(data)[GONE]
    assert (record["rows_deleted"], record["units_dropped"]) == (2, 1)


def test_the_first_absent_read_on_the_third_day_removes_the_model(
    tmp_path: Path,
) -> None:
    """Each day is judged on the reads made so far that day."""

    here, data, agents = _machine(tmp_path)
    _days(here, data, agents, 2, codex=_codex_without())

    _pass(here, data, agents, now=NOW + 2 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is None


def test_a_day_any_complete_read_showed_the_model_is_not_absent(
    tmp_path: Path,
) -> None:
    """Shown in the morning and missing in the evening is a day it was present."""

    here, data, agents = _machine(tmp_path)
    _days(here, data, agents, 2, codex=_codex_without())
    _pass(here, data, agents, now=NOW + 2 * DAY)

    _pass(
        here,
        data,
        agents,
        now=NOW + 2 * DAY + timedelta(hours=6),
        codex=_codex_without(),
    )
    _pass(here, data, agents, now=NOW + 3 * DAY, codex=_codex_without())

    assert _model(here, data, GONE) is not None


def test_a_grok_model_adopt_left_without_a_slug_is_present_by_the_slug_the_pass_writes(
    tmp_path: Path,
) -> None:
    """The slug write-back runs before presence is judged."""

    here, data, agents = _machine(tmp_path)
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-09-10T00:00:00Z",
                "models": [
                    {
                        **dict.fromkeys(catalogue.MODEL_FIELDS),
                        "id": "grok-4.5",
                        "provider": "spacexai",
                        "family": "grok",
                        "aliases": [],
                        "deliberation": ["low", "high"],
                        "reasoning_billed_as": "output",
                        "source_url": "https://example.com",
                        "retrieved": "2026-09-10",
                    }
                ],
                "plans": [],
            }
        ),
        encoding="utf-8",
    )

    _pass(here, data, agents)

    assert "grok-4.5" not in _lifecycle(data)
    assert dict(_model(here, data, "grok-4.5").gateways) == {
        "openrouter": "x-ai/grok-4.5"
    }


def test_a_grok_model_missing_from_openrouter_s_complete_list_is_removed(
    tmp_path: Path,
) -> None:
    """For Grok, its maker's list is OpenRouter's public one."""

    here, data, agents = _machine(tmp_path)
    payload = _openrouter()
    payload["data"] = [
        entry for entry in payload["data"] if entry["id"] != "x-ai/grok-4.6"
    ]
    payload["total_count"] = len(payload["data"])

    _days(here, data, agents, 3, openrouter=payload)

    assert _model(here, data, "grok-4.6") is None
    assert _removals(data)[0]["source"] == "openrouter"


def test_the_journal_subcommand_shows_every_removal_with_its_dates_and_counts(
    tmp_path: Path,
) -> None:
    """Status reports the removal, its three dates, and rows and Units as two numbers."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 2)
    _waiting(data, GONE, "u1")
    _days(here, data, agents, 3, codex=_codex_without())
    _measured(data, GONE, 1, first=10)
    _pass(here, data, agents, now=NOW + 3 * DAY, codex=_codex_without())
    days = [(NOW + index * DAY).date().isoformat() for index in range(3)]

    recent = catalogue.journal(data, 7, now=NOW + 3 * DAY)
    later = catalogue.journal(data, 7, now=NOW + 30 * DAY)

    removal = [row for row in recent["journal"] if row["field"] == "removed"]
    assert removal[0]["new"] == {
        "absent_days": days,
        "rows_deleted": 2,
        "units_dropped": 1,
    }
    for shown in (recent, later):
        assert shown["removed"] == [
            {
                "model": GONE,
                "absent_days": days,
                "removed_at": _stamp(NOW + 2 * DAY),
                "rows_deleted": 3,
                "units_dropped": 1,
            }
        ]
    assert later["journal"] == []


# --- The bounds a pass runs within (#312) ------------------------------------------
#
# The pass runs by itself once a day, so nothing may make it outlive its
# welcome: one pass at a time, one scheduled attempt a day, thirty seconds a
# source and three hundred for the whole, and a pass past its deadline writes
# nothing but the marker that says so.

SOURCES = ("claude", "codex", "openrouter")


def _never(started: datetime, seconds: float) -> Any:
    raise AssertionError("a source was read")


def _marker(data: Path) -> dict[str, Any]:
    marker: dict[str, Any] = json.loads(
        (data / "refresh-marker.json").read_text(encoding="utf-8")
    )
    return marker


def _files(*directories: Path) -> dict[str, bytes]:
    """Return every file under *directories* but the marker, by path, with its bytes."""

    return {
        str(path): path.read_bytes()
        for directory in directories
        if directory.exists()
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path.name != "refresh-marker.json"
    }


def _gone(pid: int) -> bool:
    """Return whether process *pid* no longer runs, waiting up to ten seconds.

    A killed process lingers as a zombie until whatever inherited it reaps
    it, and under a loaded suite that can take a moment; a zombie runs
    nothing, so it counts as gone.
    """

    for _ in range(100):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        state = subprocess.run(
            ["ps", "-o", "stat=", "-p", str(pid)],
            capture_output=True,
            text=True,
            check=False,
            cwd="/",
        ).stdout.strip()
        if not state or state.startswith("Z"):
            return True
        time.sleep(0.1)
    return False


def test_a_pass_started_while_another_holds_the_lock_does_nothing(
    tmp_path: Path,
) -> None:
    """Hand-started or scheduled, it reads nothing, writes nothing, and leaves no marker."""

    here, data, agents = _machine(tmp_path)
    before = _files(data)

    with evidence.lock(data, catalogue.REFRESH_LOCK) as taken:
        assert taken
        for scheduled in (False, True):
            report = catalogue.run(
                data,
                here,
                agents,
                scheduled=scheduled,
                now=NOW,
                readers=dict.fromkeys(SOURCES, _never),
            )
            assert report == {"ran": False, "reason": "locked"}

    assert _files(data) == before
    assert not (data / "refresh-marker.json").exists()


def test_a_hand_started_pass_finding_the_lock_busy_says_so_and_exits_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, data, agents = _machine(tmp_path)
    monkeypatch.setattr(catalogue, "READERS", dict.fromkeys(SOURCES, _never))

    with evidence.lock(data, catalogue.REFRESH_LOCK):
        code = catalogue.main(["refresh", f"--data={data}", f"--agents={agents}"])

    assert code == 0
    assert json.loads(capsys.readouterr().out) == {"ran": False, "reason": "locked"}


def test_a_second_scheduled_attempt_on_the_same_day_does_nothing(
    tmp_path: Path,
) -> None:
    """The marker holds the UTC day, when the pass ended, and the bound it hit."""

    here, data, agents = _machine(tmp_path)

    first = catalogue.run(
        data, here, agents, scheduled=True, now=NOW, readers=_readers()
    )

    assert first["outcome"] == "ran"
    marker = _marker(data)
    assert marker["date"] == TODAY
    assert marker["bound_hit"] is None
    assert datetime.fromisoformat(marker["ended_at"]).tzinfo is not None
    before = _files(data, agents)

    second = catalogue.run(
        data,
        here,
        agents,
        scheduled=True,
        now=NOW + timedelta(hours=6),
        readers=dict.fromkeys(SOURCES, _never),
    )

    assert second == {"ran": False, "reason": "already ran today"}
    assert _files(data, agents) == before
    assert _marker(data) == marker


def test_the_next_day_s_scheduled_attempt_runs(tmp_path: Path) -> None:
    here, data, agents = _machine(tmp_path)
    catalogue.run(data, here, agents, scheduled=True, now=NOW, readers=_readers())

    report = catalogue.run(
        data, here, agents, scheduled=True, now=NOW + DAY, readers=_readers()
    )

    assert report["outcome"] == "ran"
    assert _marker(data)["date"] == (NOW + DAY).date().isoformat()


def test_a_hand_started_pass_runs_on_a_day_the_scheduled_pass_already_ran(
    tmp_path: Path,
) -> None:
    """The daily marker gates only the scheduled entry point."""

    here, data, agents = _machine(tmp_path)
    catalogue.run(data, here, agents, scheduled=True, now=NOW, readers=_readers())
    marker = _marker(data)

    later = NOW + timedelta(hours=1)
    report = catalogue.run(data, here, agents, now=later, readers=_readers())

    assert report["outcome"] == "ran"
    stored = json.loads((data / "refresh.json").read_text(encoding="utf-8"))
    assert stored["at"] == _stamp(later)
    assert _marker(data) == marker


def test_the_scheduled_entry_point_on_the_command_line_is_gated_by_the_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, data, agents = _machine(tmp_path)
    monkeypatch.setattr(catalogue, "READERS", dict.fromkeys(SOURCES, _never))
    (data / "refresh-marker.json").write_text(
        json.dumps(
            {
                "date": datetime.now(UTC).date().isoformat(),
                "ended_at": datetime.now(UTC).isoformat(),
                "bound_hit": None,
            }
        ),
        encoding="utf-8",
    )

    code = catalogue.main(
        ["refresh", "--scheduled", f"--data={data}", f"--agents={agents}"]
    )

    assert code == 0
    assert json.loads(capsys.readouterr().out) == {
        "ran": False,
        "reason": "already ran today",
    }


def test_a_source_past_its_deadline_is_stopped_with_its_process_group_and_keeps_its_facts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The harness and what it started are killed; the source changes nothing it governs."""

    here, data, agents = _machine(tmp_path, "anthropic", drop=("claude-sonnet-5",))
    child = tmp_path / "child.pid"
    hanging = f"#!/bin/sh\nsleep 60 &\necho $! > '{child}'\nexec sleep 60\n"
    # The stand-in's own `sleep` has to resolve, or the harness exits at once
    # instead of hanging with a child in its group.
    bin_dir = _install(tmp_path, "claude", hanging)
    monkeypatch.setenv("PATH", os.pathsep.join((bin_dir, "/bin", "/usr/bin")))
    # Long enough for a loaded suite to start the stand-in and its child.
    monkeypatch.setattr(catalogue, "EXCHANGE_SECONDS", 4.0)

    report = catalogue.run(
        data,
        here,
        agents,
        scheduled=True,
        now=NOW,
        readers=_readers(overrides={"claude": catalogue.read_claude}),
    )

    claude = report["sources"]["claude"]
    assert claude["outcome"] == "unreadable"
    assert "deadline" in claude["reason"]
    assert report["bound_hit"] == "source:claude"
    assert _marker(data)["bound_hit"] == "source:claude"
    stored = json.loads((data / "refresh.json").read_text(encoding="utf-8"))
    assert "deadline" in stored["sources"]["claude"]["reason"]
    assert _model(here, data, "claude-sonnet-5") is None
    assert all(row["source"] != "claude" for row in _journal(data))
    assert child.exists(), "the stand-in never started its child"
    assert _gone(int(child.read_text(encoding="utf-8")))


def test_the_whole_deadline_stops_a_source_in_flight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A source is given the lesser of its own deadline and what the pass has left."""

    here, data, agents = _machine(tmp_path, "anthropic")
    silent = f"#!{sys.executable}\nimport time\ntime.sleep(60)\n"
    monkeypatch.setenv("PATH", _install(tmp_path, "claude", silent))
    monkeypatch.setattr(catalogue, "PASS_SECONDS", 1.0)
    before = _files(data)

    started = time.monotonic()
    report = catalogue.run(
        data,
        here,
        agents,
        scheduled=True,
        now=NOW,
        readers=_readers(overrides={"claude": catalogue.read_claude}),
    )

    assert time.monotonic() - started < 10
    assert report["bound_hit"] == "whole-pass"
    assert _marker(data)["bound_hit"] == "whole-pass"
    assert _files(data) == before


def test_a_pass_past_its_whole_deadline_before_applying_writes_nothing_but_its_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No catalogue, journal, pass report, lifecycle, deletion or definition moves."""

    here, data, agents = _machine(tmp_path)
    _measured(data, GONE, 2)
    _days(here, data, agents, 2, codex=_codex_without())
    before = _files(data, agents)
    monkeypatch.setattr(catalogue, "PASS_SECONDS", 0.5)

    def slow(started: datetime, seconds: float) -> Any:
        time.sleep(0.6)
        return catalogue.claude_reading(_claude_messages())

    report = catalogue.run(
        data,
        here,
        agents,
        scheduled=True,
        now=NOW + 2 * DAY,
        readers=_readers(codex=_codex_without(), overrides={"claude": slow}),
    )

    assert report["outcome"] == catalogue.PAST_DEADLINE
    assert report["bound_hit"] == "whole-pass"
    assert _files(data, agents) == before
    assert _model(here, data, GONE) is not None
    assert _ledger(data).count(GONE) == 2
    assert _marker(data)["bound_hit"] == "whole-pass"


def test_a_pass_whose_deadline_passes_while_it_is_applying_finishes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Applying is local and bounded, so nothing interrupts it once it has begun."""

    here, data, agents = _machine(tmp_path, drop=("claude-sonnet-5",))
    monkeypatch.setattr(catalogue, "PASS_SECONDS", 2.0)
    synced = launch.sync_definitions

    def slow_sync(*arguments: Any, **options: Any) -> Any:
        time.sleep(2.3)
        return synced(*arguments, **options)

    monkeypatch.setattr(launch, "sync_definitions", slow_sync)

    report = catalogue.run(data, here, agents, now=NOW, readers=_readers())

    assert report["outcome"] == "ran"
    assert report["bound_hit"] is None
    assert (agents / "kntnt-sonnet-high.md").is_file()
    stored = json.loads((data / "refresh.json").read_text(encoding="utf-8"))
    assert stored["at"] == _stamp(NOW)


def test_a_sigterm_to_a_running_pass_releases_its_lock(tmp_path: Path) -> None:
    """A `bootout` that arrives mid-pass leaves no stale lock and no marker."""

    here, data, agents = _machine(tmp_path)
    previous = signal.getsignal(signal.SIGTERM)

    def terminated(started: datetime, seconds: float) -> Any:
        assert (data / catalogue.REFRESH_LOCK).exists()
        os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(5)
        raise AssertionError("the pass outlived its SIGTERM")

    with pytest.raises(SystemExit):
        catalogue.run(
            data,
            here,
            agents,
            scheduled=True,
            now=NOW,
            readers=_readers(overrides={"claude": terminated}),
        )

    assert not (data / catalogue.REFRESH_LOCK).exists()
    assert not (data / "refresh-marker.json").exists()
    assert signal.getsignal(signal.SIGTERM) is previous


def _paged() -> dict[str, dict[str, Any]]:
    """Return OpenRouter's recorded list split over two pages on its own host."""

    payload = _openrouter()
    half = len(payload["data"]) // 2
    return {
        catalogue.OPENROUTER_MODELS_URL: {
            "data": payload["data"][:half],
            "total_count": payload["total_count"],
            "links": {"next": "/api/v1/models?cursor=2"},
        },
        "https://openrouter.ai/api/v1/models?cursor=2": {
            "data": payload["data"][half:],
            "total_count": payload["total_count"],
            "links": {"next": None},
        },
    }


def test_openrouter_gives_every_page_what_remains_of_its_one_budget() -> None:
    pages = _paged()
    given: list[float] = []

    def fetch(url: str, timeout: float) -> bytes:
        given.append(timeout)
        time.sleep(0.2)
        return json.dumps(pages[url]).encode()

    reading = catalogue.read_openrouter(NOW, 5.0, fetch=fetch)

    assert reading.outcome == "complete"
    assert given[0] <= 5.0
    assert given[1] <= given[0] - 0.2


def test_openrouter_past_its_budget_between_pages_is_incomplete_and_names_the_deadline() -> (
    None
):
    pages = _paged()

    def fetch(url: str, timeout: float) -> bytes:
        time.sleep(0.3)
        return json.dumps(pages[url]).encode()

    reading = catalogue.read_openrouter(NOW, 0.2, fetch=fetch)

    assert reading.outcome == "incomplete"
    assert "deadline" in (reading.reason or "")
    assert reading.timed_out


def test_openrouter_timing_out_on_its_first_page_is_unreadable_and_names_the_deadline() -> (
    None
):
    def fetch(url: str, timeout: float) -> bytes:
        raise TimeoutError("timed out")

    reading = catalogue.read_openrouter(NOW, 0.2, fetch=fetch)

    assert reading.outcome == "unreadable"
    assert "deadline" in (reading.reason or "")
    assert reading.timed_out
