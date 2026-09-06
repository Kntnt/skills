"""World facts the model-selector Skill answers from: models, aliases, prices."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
SHIPPED: Path = REPO_ROOT / "skills" / "models" / "model-selector"

# The measured Claude Code session this Skill's priors are calibrated on. Kept
# here as the one real token mix the pricing arithmetic is checked against,
# because a cost model that treats cache reads as incidental is wrong by two
# orders of magnitude and nothing smaller than a real session shows it.
SESSION = {
    "input": 558.0,
    "cache_write": 903149.0,
    "cache_read": 27790393.0,
    "output": 32791.0,
    "reasoning": 16750.0,
}


class Rule:
    """Stand in for the kinds table, the only thing that says this about a kind."""

    def __init__(self, *long_context: str) -> None:
        self._long = frozenset(long_context)

    def long_context(self, kind: str) -> bool:
        """Return whether *kind* normally passes a vendor's context threshold."""

        return kind in self._long


SHORT = Rule()
LONG = Rule("implement")


def _module(stem: str, name: str | None = None) -> Any:
    """Load one shipped module under the name its siblings import it by.

    Registered in `sys.modules` before it executes, so that a module importing
    a sibling by plain name finds the same object this test is holding.
    """

    registered = name or stem
    if registered in sys.modules:
        return sys.modules[registered]
    spec = importlib.util.spec_from_file_location(registered, SCRIPTS / f"{stem}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[registered] = module
    spec.loader.exec_module(module)
    return module


catalogue = _module("catalogue")


def _model(**overrides: Any) -> dict[str, Any]:
    """Provide one catalogue entry, in the shape the shipped seed writes it."""

    entry: dict[str, Any] = {
        "id": "test-one",
        "provider": "testing",
        "family": "one",
        "aliases": ["one"],
        "deliberation": ["low", "high"],
        "price": {
            "input": 10.0,
            "cache_read": 1.0,
            "cache_write": 12.5,
            "output": 50.0,
            "currency": "USD",
            "unit": "per_mtok",
        },
        "reasoning_billed_as": "output",
        "capability": 0.8,
        "provider_says": None,
        "released": "2026-01-01",
        "source_url": None,
        "retrieved": None,
    }
    entry.update(overrides)
    return entry


def _here(tmp_path: Path, models: list[dict[str, Any]] | str) -> Path:
    """Write a shipped-seed directory, or an unparsable file where given a string."""

    here = tmp_path / "skill"
    (here / "data").mkdir(parents=True)
    seed = here / "data" / "catalogue-seed.json"
    if isinstance(models, str):
        seed.write_text(models, encoding="utf-8")
    else:
        seed.write_text(
            json.dumps({"generated_at": "2026-01-01T00:00:00Z", "models": models}),
            encoding="utf-8",
        )
    return here


def test_load_returns_the_seed_alone_when_nothing_has_been_refreshed(
    tmp_path: Path,
) -> None:
    """A data directory with no refreshed file leaves the shipped facts standing."""

    here = _here(tmp_path, [_model()])

    cat = catalogue.load(tmp_path / "data", here)

    assert [model.id for model in cat.models] == ["test-one"]
    assert cat.problem is not None
    assert "catalogue.json" in cat.problem


def test_a_refreshed_model_replaces_the_seed_entry_of_the_same_id(
    tmp_path: Path,
) -> None:
    """What a person checked this week outranks what the release froze."""

    here = _here(tmp_path, [_model(), _model(id="test-two", family="two")])
    data = tmp_path / "data"
    data.mkdir()
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-09-01T00:00:00Z",
                "models": [
                    _model(capability=0.31),
                    _model(id="test-three", family="three"),
                ],
            }
        ),
        encoding="utf-8",
    )

    cat = catalogue.load(data, here)

    assert cat.problem is None
    assert cat.generated_at == "2026-09-01T00:00:00Z"
    assert {model.id for model in cat.models} == {"test-one", "test-two", "test-three"}
    assert catalogue.resolve(cat, "test-one")[0].capability == 0.31


def test_an_unparsable_seed_yields_an_empty_catalogue_rather_than_an_exception(
    tmp_path: Path,
) -> None:
    """Nothing in this Skill raises; a seed that will not parse says so instead."""

    here = _here(tmp_path, "{not json at all")

    cat = catalogue.load(tmp_path / "data", here)

    assert cat.models == ()
    assert cat.problem is not None


def test_resolve_matches_id_alias_and_family_and_returns_the_newest_first(
    tmp_path: Path,
) -> None:
    """A family alias names a generation, so the answer is ordered by release."""

    here = _here(
        tmp_path,
        [
            _model(id="test-old", released="2024-01-01"),
            _model(id="test-new", released="2026-06-01"),
        ],
    )
    cat = catalogue.load(tmp_path / "data", here)

    assert [model.id for model in catalogue.resolve(cat, "one")] == [
        "test-new",
        "test-old",
    ]
    assert [model.id for model in catalogue.resolve(cat, "TEST-OLD")] == ["test-old"]
    assert catalogue.resolve(cat, "nothing-like-this") == []


def test_cost_prices_the_measured_session_with_cache_reads_dominating() -> None:
    """The bill is mostly cache reads, and pricing that ignores them is wrong."""

    model = catalogue.load(Path("/nowhere"), SHIPPED)
    opus = catalogue.resolve(model, "claude-opus-5")[0]

    total = catalogue.cost_usd(opus, SESSION, "implement", LONG)
    cache_read_only = catalogue.cost_usd(
        opus, {"cache_read": SESSION["cache_read"]}, "implement", LONG
    )

    assert total is not None and cache_read_only is not None
    assert cache_read_only / total > 0.5


def test_reasoning_is_priced_by_the_category_the_provider_bills_it_as(
    tmp_path: Path,
) -> None:
    """Reasoning has no rate of its own, so it borrows the one it is billed at."""

    here = _here(
        tmp_path,
        [
            _model(id="test-out", reasoning_billed_as="output"),
            _model(id="test-in", reasoning_billed_as="input"),
            _model(id="test-sep", reasoning_billed_as="separate"),
        ],
    )
    cat = catalogue.load(tmp_path / "data", here)
    tokens = {"reasoning": 1_000_000.0}

    priced = {
        model.id: catalogue.cost_usd(model, tokens, "implement", SHORT)
        for model in cat.models
    }

    assert priced["test-out"] == 50.0
    assert priced["test-in"] == 10.0
    assert priced["test-sep"] is None


def test_a_category_the_card_does_not_cover_is_absent_rather_than_free(
    tmp_path: Path,
) -> None:
    """An unpriceable point returns None so that ranking can rank it last."""

    here = _here(
        tmp_path,
        [
            _model(
                id="test-partial",
                price={"output": 50.0, "currency": "USD", "unit": "per_mtok"},
            ),
            _model(id="test-unpriced", price=None),
        ],
    )
    cat = catalogue.load(tmp_path / "data", here)
    partial, unpriced = (
        catalogue.resolve(cat, "test-partial")[0],
        catalogue.resolve(cat, "test-unpriced")[0],
    )

    assert catalogue.cost_usd(partial, {"cache_read": 1e6}, "implement", SHORT) is None
    assert (
        catalogue.cost_usd(
            partial, {"cache_read": 1e6, "output": 1e6}, "implement", SHORT
        )
        == 50.0
    )
    assert catalogue.cost_usd(unpriced, SESSION, "implement", SHORT) is None


def test_a_kind_that_runs_at_repo_scale_is_priced_on_the_long_context_card(
    tmp_path: Path,
) -> None:
    """A vendor cliff re-prices the whole request, so the kind has to select it."""

    here = _here(
        tmp_path,
        [
            _model(
                id="test-cliff",
                long_context_threshold=272_000,
                long_context={
                    "input": 20.0,
                    "cache_read": 2.0,
                    "cache_write": None,
                    "output": 75.0,
                    "currency": "USD",
                    "unit": "per_mtok",
                },
            ),
            _model(id="test-flat"),
        ],
    )
    cat = catalogue.load(tmp_path / "data", here)
    cliff = catalogue.resolve(cat, "test-cliff")[0]
    flat = catalogue.resolve(cat, "test-flat")[0]
    tokens = {"cache_read": 1_000_000.0}

    assert cliff.long_context_threshold == 272_000
    assert catalogue.cost_usd(cliff, tokens, "implement", SHORT) == 1.0
    assert catalogue.cost_usd(cliff, tokens, "implement", LONG) == 2.0
    assert catalogue.cost_usd(flat, tokens, "implement", LONG) == 1.0


def test_the_shipped_seed_parses_into_the_models_it_names() -> None:
    """The file this Skill installs with has to load through its own loader."""

    cat = catalogue.load(Path("/nowhere"), SHIPPED)

    assert len(cat.models) == 9
    assert all(
        level in catalogue.LEVELS
        for model in cat.models
        for level in model.deliberation
    )
    assert all(model.family in model.aliases for model in cat.models)

    # One shipped model has no effort control at all, which is a real state
    # rather than a gap: the loader has to carry it as an empty tuple, and
    # everything downstream has to read that as one point rather than none.
    haiku = catalogue.resolve(cat, "haiku")[0]
    assert haiku.deliberation == ()


def test_a_channel_rate_card_replaces_the_one_the_catalogue_holds() -> None:
    """What the user says they pay outranks what the provider publishes.

    A gateway prices the same model differently from the provider whose model
    it is, and the catalogue holds one list price per model from that
    provider's own page. Pricing a gateway channel from it is not an
    approximation but a different arrangement's bill.
    """

    model = catalogue._model(_model())
    assert model is not None
    paid = catalogue.Price(0.9915, 0.9915, 0.9915, 6.174, "USD", "per_mtok")

    listed = catalogue.cost_usd(model, SESSION, "implement", SHORT)
    theirs = catalogue.cost_usd(model, SESSION, "implement", SHORT, rates=paid)

    assert listed is not None and theirs is not None
    assert round(theirs, 4) == round(
        (558.0 + 903149.0 + 27790393.0) * 0.9915 / 1e6
        + (32791.0 + 16750.0) * 6.174 / 1e6,
        4,
    )
    assert theirs < listed


def test_a_channel_rate_card_prices_repo_scale_work_at_the_same_rates() -> None:
    """A rate the user quoted is what they pay, at every size of request.

    The context cliff is a fact about a provider's own card. A channel that
    carries its own card has already said what the tokens cost, and a second
    card applied on top of it would be this Skill inventing a threshold its
    source never mentioned.
    """

    cliff = catalogue._model(
        _model(
            long_context_threshold=272_000,
            long_context={
                "input": 20.0,
                "cache_read": 2.0,
                "cache_write": 25.0,
                "output": 100.0,
                "currency": "USD",
                "unit": "per_mtok",
            },
        )
    )
    assert cliff is not None
    paid = catalogue.Price(1.0, 1.0, 1.0, 1.0, "USD", "per_mtok")
    tokens = {"cache_read": 1_000_000.0}

    assert catalogue.cost_usd(cliff, tokens, "implement", LONG) == 2.0
    assert catalogue.cost_usd(cliff, tokens, "implement", LONG, rates=paid) == 1.0


def test_the_shipped_seed_holds_the_plans_each_provider_markets(tmp_path: Path) -> None:
    """The tiers an interview offers are world facts, dated and attributed.

    A vocabulary kept as prose in a reference file cannot be refreshed, cannot
    say where it came from, and drifts the moment a provider renames a plan or
    adds a multiplier. These are the same kind of fact as a price and carry the
    same two members.
    """

    cat = catalogue.load(Path("/nowhere"), SHIPPED)

    priced = {model.provider for model in cat.models}
    assert {plan.provider for plan in cat.plans} == priced
    assert all(plan.source_url and plan.retrieved for plan in cat.plans)

    # The two plans this machine actually pays for, spelled whole. Neither was
    # offerable from the hand-written table these replace.
    named = {plan.name for plan in cat.plans}
    assert "Claude Max 20x" in named
    assert "ChatGPT Pro 20x" in named


def test_plans_for_answers_with_one_provider_s_plans_in_the_order_held() -> None:
    """The interview asks per provider, so the lookup is per provider.

    The order is the file's, which is the order the plans are offered in: the
    author of the facts is who knows that a free tier precedes a paid one.
    """

    cat = catalogue.load(Path("/nowhere"), SHIPPED)

    anthropic = catalogue.plans_for(cat, "anthropic")

    assert [plan.name for plan in anthropic] == [
        plan.name for plan in cat.plans if plan.provider == "anthropic"
    ]
    assert anthropic[0].name == "Claude Free"
    assert catalogue.plans_for(cat, "nobody") == []


def test_a_refreshed_plan_list_replaces_the_seed_plans_of_that_provider(
    tmp_path: Path,
) -> None:
    """A retired plan has to be able to disappear, which a merge by name cannot do.

    Models merge entry by entry because a model that existed still exists. A
    plan that a provider stopped selling is an option this Skill would go on
    offering forever, and offering a wrong list is the defect being fixed.
    """

    here = _here(tmp_path, [_model()])
    seed = json.loads((here / "data" / "catalogue-seed.json").read_text("utf-8"))
    seed["plans"] = [
        {
            "provider": "testing",
            "name": "Old Plan",
            "monthly_usd": 10.0,
            "source_url": "https://example.test/pricing",
            "retrieved": "2026-01-01",
        },
        {
            "provider": "other",
            "name": "Untouched",
            "monthly_usd": 5.0,
            "source_url": "https://example.test/other",
            "retrieved": "2026-01-01",
        },
    ]
    (here / "data" / "catalogue-seed.json").write_text(json.dumps(seed), "utf-8")
    data = tmp_path / "data"
    data.mkdir()
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-09-01T00:00:00Z",
                "models": [],
                "plans": [
                    {
                        "provider": "testing",
                        "name": "New Plan",
                        "monthly_usd": 12.0,
                        "source_url": "https://example.test/pricing",
                        "retrieved": "2026-09-01",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    cat = catalogue.load(data, here)

    assert [plan.name for plan in catalogue.plans_for(cat, "testing")] == ["New Plan"]
    assert [plan.name for plan in catalogue.plans_for(cat, "other")] == ["Untouched"]
