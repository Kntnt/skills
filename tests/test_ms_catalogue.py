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
    """What was read this week outranks what the release froze."""

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
    """What the user says they pay outranks what the catalogue holds.

    The catalogue holds the price OpenRouter publishes, which is the charge
    through OpenRouter and a different arrangement's bill through any other
    gateway, so the card the user records replaces it.
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

    The context cliff is a fact about the catalogue's card, the threshold
    OpenRouter publishes with its price. A channel that carries its own card
    has already said what the tokens cost, and a second card applied on top of
    it would be this Skill inventing a threshold its source never mentioned.
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


def test_load_returns_the_seed_s_plans_even_when_catalogue_json_holds_plans(
    tmp_path: Path,
) -> None:
    """Plans ship with the collection, and nothing on this machine replaces them.

    No structured source lists what a provider sells, and the agent reading
    pages that once refreshed them is retired (ADR-0194). A `catalogue.json`
    an older release wrote may still carry plans; they are left unread, so
    the plans in force are the ones the release shipped.
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

    assert [plan.name for plan in catalogue.plans_for(cat, "testing")] == ["Old Plan"]
    assert [plan.name for plan in catalogue.plans_for(cat, "other")] == ["Untouched"]


def _card(**overrides: Any) -> dict[str, Any]:
    """Provide one rate card, in the units this Skill compares and never converts."""

    card = {
        "input": 10.0,
        "cache_read": 1.0,
        "cache_write": 12.5,
        "output": 50.0,
        "currency": "USD",
        "unit": "per_mtok",
    }
    card.update(overrides)
    return card


def _attributed(**overrides: Any) -> dict[str, Any]:
    """Provide one entry as the catalogue pass writes it: attributed and dated."""

    entry = _model(source_url="https://example.test/models", retrieved="2026-09-06")
    entry.update(overrides)
    return entry


def test_the_validator_refuses_a_card_in_another_currency() -> None:
    """Nothing here converts, so a card in euros would be added to a dollar bill."""

    fault = catalogue._model_fault(_attributed(price=_card(currency="EUR")))

    assert fault is not None
    assert "EUR" in fault


def test_the_validator_refuses_a_card_quoted_in_another_unit() -> None:
    """A rate per thousand tokens read as a rate per million is off by a thousand."""

    fault = catalogue._model_fault(_attributed(price=_card(unit="per_ktok")))

    assert fault is not None
    assert "per_ktok" in fault


def test_the_validator_refuses_a_deliberation_level_outside_the_ladder() -> None:
    """The ladder is the only ordering of effort this Skill has, so it is closed."""

    fault = catalogue._model_fault(_attributed(deliberation=["low", "extreme"]))

    assert fault is not None
    assert "extreme" in fault


def test_the_validator_refuses_an_entry_with_nothing_to_attribute_it_to() -> None:
    """A fact nothing can attribute is worse than no fact."""

    fault = catalogue._model_fault(_model())

    assert fault is not None
    assert "source_url" in fault


def test_the_catalogue_has_no_verb_that_adopts_a_document() -> None:
    """`update` is retired, and the half of it that was a script goes with it.

    The catalogue pass is the one writer of `catalogue.json` (ADR-0194), and
    it goes through the validator on its own path, so nothing is left that
    would hand `adopt` a document.
    """

    for name in ("adopt", "_adopt_models", "_adopt_plans", "_merged_plans"):
        assert not hasattr(catalogue, name), name
    for name in ("FETCHED_FIELDS", "PLAN_FIELDS", "_plan_fault", "_offered"):
        assert not hasattr(catalogue, name), name
    try:
        catalogue.main(["adopt", "/nowhere/fetched.json", "--data=/nowhere"])
    except SystemExit as stopped:
        assert stopped.code == 2
    else:
        raise AssertionError("`adopt` is still accepted")


def test_no_model_carries_a_provider_s_own_prose() -> None:
    """Prose never becomes a number, and nothing ranks on it (ADR-0194).

    `provider_says` was the provider's one-line positioning of a model, shown
    in the interview and fetched by `update`. Nothing reads it any more, so the
    seed, the loaded catalogue and its print carry it nowhere.
    """

    seed = json.loads((SHIPPED / "data" / "catalogue-seed.json").read_text("utf-8"))
    cat = catalogue.load(Path("/nowhere"), SHIPPED)

    assert "provider_says" not in catalogue.MODEL_FIELDS
    assert not [entry["id"] for entry in seed["models"] if "provider_says" in entry]
    assert not [model.id for model in cat.models if hasattr(model, "provider_says")]
    assert not [
        entry["id"]
        for entry in catalogue._document(cat)["models"]
        if "provider_says" in entry
    ]


def test_gateways_and_capability_are_the_fields_the_seed_keeps() -> None:
    """A gateway's slug is matched, not read off any page (issue #308)."""

    assert "gateways" in catalogue.MODEL_FIELDS
    assert catalogue.SEEDED_FIELDS == ("capability", "gateways")


def test_the_shipped_seed_carries_the_openrouter_slug_for_grok_alone() -> None:
    """The one gateway route this collection ships knowing is Grok's through OpenRouter."""

    cat = catalogue.load(Path("/nowhere"), SHIPPED)

    slugged = {model.id: model.gateways for model in cat.models if model.gateways}

    assert slugged == {"grok-4.6": (("openrouter", "x-ai/grok-4.6"),)}


def _seed_entry(identifier: str) -> dict[str, Any]:
    """Return one entry of the shipped seed exactly as the file holds it."""

    seed = json.loads((SHIPPED / "data" / "catalogue-seed.json").read_text("utf-8"))
    return next(entry for entry in seed["models"] if entry["id"] == identifier)


def _refreshed(data: Path, entry: dict[str, Any]) -> None:
    """Write a refreshed catalogue holding one entry, as `update` leaves it."""

    data.mkdir(parents=True, exist_ok=True)
    (data / "catalogue.json").write_text(
        json.dumps({"generated_at": "2026-09-10T00:00:00Z", "models": [entry]}),
        encoding="utf-8",
    )


def test_a_refreshed_entry_carrying_no_gateways_keeps_the_seed_s(
    tmp_path: Path,
) -> None:
    """A machine that ran `update` before the seed knew a slug still learns it.

    The refreshed entry otherwise replaces the seeded one whole, so a slug the
    seed gained in a release would never reach a catalogue refreshed before it.
    Absent, null and empty all count as not carrying one.
    """

    carried: object
    for carried in ("absent", None, {}):
        entry = _seed_entry("grok-4.6")
        entry["price"] = _card(input=3.0)
        if carried == "absent":
            entry.pop("gateways", None)
        else:
            entry["gateways"] = carried
        data = tmp_path / f"data-{carried}"
        _refreshed(data, entry)

        grok = catalogue.resolve(catalogue.load(data, SHIPPED), "grok-4.6")[0]

        assert grok.price is not None and grok.price.input == 3.0
        assert grok.gateways == (("openrouter", "x-ai/grok-4.6"),), carried


def test_a_refreshed_entry_carrying_no_capability_keeps_the_seed_s(
    tmp_path: Path,
) -> None:
    """Capability, which nothing fetches, falls back the same way."""

    entry = _seed_entry("grok-4.6")
    entry["capability"] = None
    data = tmp_path / "data"
    _refreshed(data, entry)

    grok = catalogue.resolve(catalogue.load(data, SHIPPED), "grok-4.6")[0]

    assert grok.capability == 0.7


def test_a_refreshed_entry_that_carries_its_own_gateways_keeps_them(
    tmp_path: Path,
) -> None:
    """The fallback fills an absence; it does not overrule what was written."""

    entry = _seed_entry("grok-4.6")
    entry["gateways"] = {"elsewhere": "grok/4.6"}
    data = tmp_path / "data"
    _refreshed(data, entry)

    grok = catalogue.resolve(catalogue.load(data, SHIPPED), "grok-4.6")[0]

    assert grok.gateways == (("elsewhere", "grok/4.6"),)


def test_a_malformed_gateways_value_is_dropped_rather_than_raised(
    tmp_path: Path,
) -> None:
    """A hand-edited catalogue costs its own bad slug and nothing more."""

    here = _here(
        tmp_path,
        [
            _model(gateways="openrouter"),
            _model(
                id="test-two",
                family="two",
                gateways={"openrouter": 3, "elsewhere": "two/1", "blank": " "},
            ),
        ],
    )

    cat = catalogue.load(tmp_path / "data", here)

    assert catalogue.resolve(cat, "test-one")[0].gateways == ()
    assert catalogue.resolve(cat, "test-two")[0].gateways == (("elsewhere", "two/1"),)


# What the retired unattended pass went by: its module, the store it kept, the
# member that told it how to read a body, the file that told it when to run,
# and the constant that bounded its network time (issue #293). A shipped file
# still carrying one of these names describes a mechanism this collection no
# longer has, and it describes it to whoever next reads that file — which is
# how a comment justifying a timeout came to cite a module nothing ships.
RETIRED_NAMES: tuple[str, ...] = (
    "refresh.py",
    "source-states",
    "source_states",
    "reads_as",
    "refresh-cadences",
    "refresh cadence",
    "SOURCE_STATE",
    "BUDGET_SECONDS",
)

# The one place a retired name is still owed. `capture.reset --evidence` can
# only remove a file it knows the name of, so the store the pass kept has to
# stay written down there for as long as somebody's data directory might hold
# one.
RETIRED_NAME_EXEMPTIONS: tuple[tuple[str, str], ...] = (
    ("skills/models/model-selector/scripts/capture.py", '"source-states.jsonl",'),
)


def _shipped_lines() -> list[tuple[str, int, str]]:
    """Every line of every text file this collection ships, located."""

    located: list[tuple[str, int, str]] = []
    for path in sorted((REPO_ROOT / "skills").rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        relative = path.relative_to(REPO_ROOT).as_posix()
        located.extend(
            (relative, number, line)
            for number, line in enumerate(text.splitlines(), start=1)
        )
    return located


def test_no_shipped_file_names_the_retired_unattended_refresh() -> None:
    """A file that still names the pass tells a reader it is still there.

    The pass was removed because it fetched pages it could not interpret and
    had never learned a fact (ADR-0185). Removing the module is only half of
    that: prose elsewhere in the collection went on asserting, in the present
    tense, that session end reached the network and was bounded by a constant
    inside the deleted module — which contradicts what the same collection now
    tells the user in `help.md` and in `docs/rules/routing.md`. The names are
    checked rather than the word *refresh*, which the Manager uses for its own
    unrelated transaction on nearly every page it ships (issue #293).
    """

    offending = [
        f"{path}:{number}: {line.strip()}"
        for path, number, line in _shipped_lines()
        for name in RETIRED_NAMES
        if name in line and (path, line.strip()) not in RETIRED_NAME_EXEMPTIONS
    ]

    assert not offending, "the retired pass is still named in:\n" + "\n".join(offending)


def test_the_shipped_seed_promises_no_refresh_of_what_it_carries() -> None:
    """The seed's own prose is read by whoever wonders where a figure comes from.

    Nothing fetches `capability`: it is a seeded prior refined by measurement,
    and how a published benchmark maps onto its scale is undecided, so a note
    saying a refresh replaces it from one names a mechanism that does not
    exist and promises an accuracy nobody is delivering. The daily catalogue
    pass is what renews a figure here, a script reading three structured
    sources (ADR-0191, ADR-0193), and it never fetches `capability`; the plans
    change only with a release of the collection (ADR-0194).
    """

    seed = json.loads((SHIPPED / "data" / "catalogue-seed.json").read_text("utf-8"))

    offending = [note for note in seed["notes"] if "refresh" in note.lower()]

    assert not offending, "the seed still promises a refresh:\n" + "\n".join(offending)


# Where a person or an agent is told how to use this Skill: every file it
# ships, the collection's rule on routing, and the README that lists its
# verbs. `update` was retired, so none of them may name it as this Skill's
# verb — neither the slash form nor the backticked word nor a heading — and
# none may hand a document to `catalogue.py adopt` (ADR-0194).
UPDATE_SWEEP: tuple[Path, ...] = (
    REPO_ROOT / "docs" / "rules" / "routing.md",
    REPO_ROOT / "README.md",
)
RETIRED_UPDATE_FORMS: tuple[str, ...] = (
    "/model-selector update",
    "model-selector update",
    "`update`",
    "## Update",
    "catalogue.py adopt",
    'catalogue.py" adopt',
    "`adopt`",
)


def test_no_shipped_file_tells_anybody_to_run_the_retired_update() -> None:
    """A verb a page names is a verb somebody runs, and this one no longer exists."""

    files = [
        path
        for path in sorted(SHIPPED.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    ]
    offending = [
        f"{path.relative_to(REPO_ROOT)}:{number}: {form}"
        for path in [*files, *UPDATE_SWEEP]
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        )
        for form in RETIRED_UPDATE_FORMS
        if form in line
    ]

    assert not (SHIPPED / "help" / "update.md").exists()
    assert not offending, "`update` is still named in:\n" + "\n".join(offending)


def _section(heading: str) -> str:
    """Return one `## ` section of the Skill's own body."""

    body = (SHIPPED / "SKILL.md").read_text(encoding="utf-8")
    return body.partition(f"\n## {heading}\n")[2].partition("\n## ")[0]


def test_setup_reads_no_page_and_ends_by_running_the_pass_by_hand() -> None:
    """A fresh machine has a current catalogue straight away, not the next morning.

    Setup runs the pass the way a person would, without `--scheduled`, so the
    daily marker is not consulted and the pass's own lock is taken. It runs
    whether the profile was written or the review declined, and not after the
    writer refused one.
    """

    setup = _section("Setup")

    assert 'catalogue.py" refresh [--data=<directory>]' in setup
    assert "refresh --scheduled" not in setup
    assert "declined" in setup
    assert "refused" in setup
    assert "page" not in setup
    assert "thirty days" not in setup


def test_status_reports_the_pass_rather_than_the_age_of_the_facts() -> None:
    """The plans' `retrieved` dates are a release's, so their age says nothing."""

    status = _section("Status")

    assert "journal --data=<directory> --days=7" in status
    assert "retrieved" not in status
    assert "thirty days" not in status
