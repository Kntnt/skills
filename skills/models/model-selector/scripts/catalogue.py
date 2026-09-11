# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""What models exist, what they cost, and how capable they are.

Every other module in this Skill asks the world a question and this is what
answers it. The facts arrive from two places and one of them is allowed to be
wrong: the seed shipped beside this file is what the Skill knows on the day it
is installed, and `catalogue.json` under the data directory is whatever a later
`update` established. The refreshed file wins per model id, because a fact a
person checked this week outranks a fact this repository froze at release —
except for the fields nobody fetches, which only a release of the seed can
teach, and which a refreshed entry carrying none of them takes from the seed.

Nothing here raises. A catalogue that cannot be read is a catalogue that says
so in `problem` and hands back what it still has, because every caller of this
module is answering a question for a machine that is already mid-task, and a
traceback there costs the caller its work rather than merely its accuracy.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

# The deliberation ladder, weakest first. Index in this tuple is the only
# ordering of effort this Skill has, so it is defined once, here, where the
# models that support a subset of it are parsed.
LEVELS = ("low", "medium", "high", "xhigh", "max")

# The token categories a bill is made of. `reasoning` is last because it is
# the one no provider agrees about: `reasoning_billed_as` says which of the
# others pays for it.
TOKEN_CATEGORIES = ("input", "cache_read", "cache_write", "output", "reasoning")

# How a provider bills reasoning tokens. "separate" and "unknown" name real
# states of knowledge rather than rates, so neither can be priced.
BILLING = ("output", "input", "separate", "unknown")

SEED_FILE = "catalogue-seed.json"
REFRESHED_FILE = "catalogue.json"

# Rate cards are quoted per million tokens by every provider this Skill has
# met, so the unit is fixed and a file saying otherwise is not converted.
PER_MILLION = 1_000_000.0

# The one currency and the one unit every figure here is compared in. Nothing
# in this Skill converts anything, so a card in another currency is not a card
# it can price from — it is a number that would be added to a USD bill as
# though it were dollars. Named here rather than beside the profile because
# the catalogue is the lower layer, and a second copy of a rule is a second
# thing to keep true.
CURRENCY = "USD"
UNIT = "per_mtok"

# Every field one model entry carries, and the subset an agent's fetch may
# write. `capability` is off that subset deliberately: it is a seeded prior
# that measurement refines, and how a published benchmark maps onto its scale
# is not settled. `gateways` is off it too: a gateway's slug for a model is on
# no page the provider publishes, so it is written by the seed and by matching
# against the gateway's own list, and never by a reading of the provider.
MODEL_FIELDS = (
    "id",
    "provider",
    "family",
    "aliases",
    "deliberation",
    "price",
    "long_context_threshold",
    "long_context",
    "reasoning_billed_as",
    "capability",
    "gateways",
    "provider_says",
    "released",
    "source_url",
    "retrieved",
)
SEEDED_FIELDS = ("capability", "gateways")
FETCHED_FIELDS = tuple(name for name in MODEL_FIELDS if name not in SEEDED_FIELDS)

# Every field one plan entry carries. A plan is a whole name, a monthly price
# and the attribution that makes both auditable, and nothing else.
PLAN_FIELDS = ("provider", "name", "monthly_usd", "source_url", "retrieved")


class ContextRule(Protocol):
    """Whatever can say that a kind of work normally runs at repo scale.

    Declared structurally so that this module stays the world's facts alone:
    the answer lives in `data/kinds.json`, which `evidence.KindPriors` reads,
    and neither module has to import the other to agree about it.
    """

    def long_context(self, kind: str) -> bool:
        """Return whether *kind* normally passes a vendor's context threshold."""


@dataclass(frozen=True)
class Price:
    """One model's rate card, per million tokens, in one currency."""

    input: float | None
    cache_read: float | None
    cache_write: float | None
    output: float | None
    currency: str
    unit: str


@dataclass(frozen=True)
class Plan:
    """One subscription a provider sells, under the name it markets it by.

    A whole name and no split. `Claude Max 20x` is one product and `ChatGPT
    Pro 20x` is another, and a file that cut each into a product and a level
    would be inventing a boundary neither provider draws — which is how two
    profiles written a week apart come to disagree about one subscription.

    The price is what the provider lists, in USD per month, and is `None`
    where the provider publishes none that could be reached. It is here rather
    than in a profile because it is a fetched fact like any other, and asking
    a person for it wastes their time and gets a worse answer.
    """

    provider: str
    name: str
    monthly_usd: float | None
    source_url: str | None
    retrieved: str | None


@dataclass(frozen=True)
class Model:
    """One point the Skill can send work to, with everything known about it.

    `gateways` pairs a gateway's name, spelled as a profile spells it, with
    that gateway's own slug for this model: OpenRouter routes `grok-4.6` as
    `x-ai/grok-4.6`, which no string surgery on the provider's name produces.
    Pairs rather than a mapping, so that the model stays a frozen value.
    """

    id: str
    provider: str
    family: str
    aliases: tuple[str, ...]
    deliberation: tuple[str, ...]
    price: Price | None
    long_context_threshold: int | None
    long_context: Price | None
    reasoning_billed_as: str
    capability: float | None
    gateways: tuple[tuple[str, str], ...]
    provider_says: str | None
    released: str | None
    source_url: str | None
    retrieved: str | None


@dataclass(frozen=True)
class Catalogue:
    """Every known model, and why the answer might be thinner than it looks."""

    models: tuple[Model, ...]
    plans: tuple[Plan, ...]
    generated_at: str
    problem: str | None


def load(data_dir: Path, here: Path) -> Catalogue:
    """Merge the shipped seed with the refreshed file, the refreshed one winning.

    A missing or unreadable refreshed file leaves the seed standing and is
    reported in `problem`; only a seed that will not parse empties the answer,
    because at that point the Skill knows nothing at all about the world.
    """

    # The seed is the floor. Without it there is no catalogue to merge into.
    seed, seed_plans, seed_generated, seed_problem = _read(here / "data" / SEED_FILE)
    if seed_problem is not None:
        return Catalogue((), (), "", seed_problem)

    # The refreshed file overrides model by model, so a partial refresh is
    # additive rather than a replacement of everything the seed knew.
    refreshed, refreshed_plans, refreshed_generated, refresh_problem = _read(
        data_dir / REFRESHED_FILE
    )
    seeded: dict[str, Model] = {model.id: model for model in seed}
    merged = dict(seeded)
    for model in refreshed:
        merged[model.id] = _with_seeded_fields(model, seeded.get(model.id))

    generated_at = refreshed_generated or seed_generated
    return Catalogue(
        tuple(merged.values()),
        _merged_plans(seed_plans, refreshed_plans),
        generated_at,
        refresh_problem,
    )


def _with_seeded_fields(model: Model, seeded: Model | None) -> Model:
    """Return a refreshed *model*, the seed filling what nothing fetches.

    A refreshed entry replaces the seeded one whole, which is right for every
    fact `update` reads and wrong for the ones it never does: a catalogue
    refreshed before a release of the seed learned a slug would otherwise
    never learn it (issue #308). So `SEEDED_FIELDS` alone fall back, field by
    field, and only where the refreshed entry carries none — absent, null and
    empty all being none.
    """

    if seeded is None:
        return model
    return replace(
        model,
        capability=seeded.capability if model.capability is None else model.capability,
        gateways=model.gateways or seeded.gateways,
    )


def _merged_plans(seed: Sequence[Plan], refreshed: Sequence[Plan]) -> tuple[Plan, ...]:
    """Return the plans in force, a refreshed provider replacing the seed's whole.

    Models merge entry by entry, a model that existed being a model that still
    exists. A plan is not like that: a provider retires one, and a merge by
    name would go on offering it to somebody choosing how they pay for as long
    as this Skill is installed. So a provider the refreshed file speaks about
    at all is a provider whose plans it states in full.
    """

    spoken = {plan.provider for plan in refreshed}
    return tuple(
        [plan for plan in seed if plan.provider not in spoken] + list(refreshed)
    )


def adopt(
    data_dir: Path, here: Path, path: Path, *, now: str | None = None
) -> dict[str, Any]:
    """Merge what the agent read off the providers' pages into the catalogue.

    `update` is a reading job. The agent holding a web tool opens every
    `source_url` the catalogue carries, writes what it found as one document
    in this catalogue's own shape, and hands the path here. This is the half
    that has to be a script: deciding what may enter the store, merging it
    over what is already known, and replacing the file in one move.

    Every rule is per entry. An entry with nothing to attribute it to, a rate
    card in another currency or another unit, or a deliberation level outside
    the ladder is discarded by name with the reason, and the rest of the
    document is adopted — a single bad row in a page somebody read is not a
    reason to learn nothing from the other twenty. Only a document that is not
    this shape at all is refused whole, nothing being written.

    A model merges field by field over the entry `load` currently answers
    with, so a document carrying a price and nothing else leaves everything
    else standing — `capability` and `gateways` above all, which nothing
    fetches. A provider's plans are replaced whole, as `_merged_plans` explains.
    """

    document, refusal = _offered(path)
    if document is None:
        return {
            "verb": "adopt",
            "data": str(data_dir),
            "source": str(path),
            "refused": refusal,
            "written": None,
            "generated_at": None,
            "models": [],
            "plans": [],
            "discarded": [],
        }

    # What is in force right now, which is what a merge lays the document over
    # and what the report compares against.
    cat = load(data_dir, here)
    known = {model.id: _entry(model) for model in cat.models}
    stored_models, stored_plans = _stored(data_dir / REFRESHED_FILE)

    discarded: list[dict[str, Any]] = []
    adopted = _adopt_models(document["models"], known, stored_models, discarded)
    spoken = _adopt_plans(document["plans"], discarded)

    report: dict[str, Any] = {
        "verb": "adopt",
        "data": str(data_dir),
        "source": str(path),
        "refused": None,
        "written": None,
        "generated_at": None,
        "models": adopted,
        "plans": [
            _plan_change(cat, provider, offered) for provider, offered in spoken.items()
        ],
        "discarded": discarded,
    }
    if not adopted and not spoken:
        return report

    # Through a temporary sibling and an atomic rename: a pass interrupted
    # mid-write leaves the previous catalogue standing rather than half of the
    # new one.
    stamp = now or _now()
    kept = [plan for plan in stored_plans if str(plan.get("provider")) not in spoken]
    data_dir.mkdir(parents=True, exist_ok=True)
    target = data_dir / REFRESHED_FILE
    staged = target.parent / f"{target.name}.tmp"
    staged.write_text(
        json.dumps(
            {
                "generated_at": stamp,
                "models": [stored_models[name] for name in sorted(stored_models)],
                "plans": kept
                + [plan for offered in spoken.values() for plan in offered],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    staged.replace(target)

    report["written"] = str(target)
    report["generated_at"] = stamp
    return report


def _adopt_models(
    entries: list[Any],
    known: Mapping[str, dict[str, Any]],
    stored: dict[str, dict[str, Any]],
    discarded: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge every usable model entry into *stored*, and say what each one did."""

    accounted: list[dict[str, Any]] = []
    for index, entry in enumerate(entries):
        fault = _model_fault(entry)
        if fault is not None:
            discarded.append(
                {"kind": "model", "name": _model_name(entry, index), "reason": fault}
            )
            continue

        # Field by field over what is in force, so that a document saying only
        # what it read leaves everything it did not read exactly as it was.
        identifier = str(entry["id"])
        base = known.get(identifier, {})
        offered = {name: entry[name] for name in FETCHED_FIELDS if name in entry}
        whole = {**dict.fromkeys(MODEL_FIELDS), **base, **offered}
        if _model(whole) is None:
            discarded.append(
                {
                    "kind": "model",
                    "name": identifier,
                    "reason": "names no provider and family, and none is known",
                }
            )
            continue

        stored[identifier] = whole
        changed = sorted(name for name in whole if whole[name] != base.get(name))
        accounted.append(
            {
                "id": identifier,
                "status": _status(base, changed),
                "changed": changed if base else [],
                "ignored": sorted(name for name in entry if name not in FETCHED_FIELDS),
            }
        )

    return accounted


def _plan_change(
    cat: Catalogue, provider: str, offered: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Say what one provider's adopted plan list did to the list it replaced."""

    was = [plan.name for plan in plans_for(cat, provider)]
    names = [str(plan["name"]) for plan in offered]
    return {
        "provider": provider,
        "status": "unchanged" if names == was else "replaced",
        "names": names,
        "was": was,
    }


def _status(base: Mapping[str, Any], changed: Sequence[str]) -> str:
    """Return what one adopted model did to the catalogue."""

    if not base:
        return "added"
    return "changed" if changed else "unchanged"


def _adopt_plans(
    entries: list[Any], discarded: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Return the usable plans per provider, in the order the document holds them.

    A provider is spoken about by its usable entries alone. A provider whose
    every entry was discarded keeps the plans it had rather than losing them
    to a page somebody read badly.
    """

    spoken: dict[str, list[dict[str, Any]]] = {}
    for index, entry in enumerate(entries):
        fault = _plan_fault(entry)
        if fault is not None:
            discarded.append(
                {"kind": "plan", "name": _plan_name(entry, index), "reason": fault}
            )
            continue
        offered = {name: entry.get(name) for name in PLAN_FIELDS}
        spoken.setdefault(str(entry["provider"]), []).append(offered)

    return spoken


def _offered(path: Path) -> tuple[dict[str, list[Any]] | None, str | None]:
    """Read one fetched document, or say why it is not one at all."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"no document at {path}"
    except (OSError, ValueError) as problem:
        return None, f"{path} could not be read: {problem}"

    if not isinstance(raw, dict):
        return None, f"{path} is not a JSON object"
    if "models" not in raw and "plans" not in raw:
        return None, f"{path} carries neither a models list nor a plans list"

    models = raw.get("models", [])
    plans = raw.get("plans", [])
    if not isinstance(models, list) or not isinstance(plans, list):
        return None, f"{path} carries a models or plans member that is not a list"

    return {"models": models, "plans": plans}, None


def _stored(path: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Return what the refreshed file already holds, keyed for merging into.

    An unreadable file is an empty one. The seed is what stands behind it in
    either case, so a refreshed file nothing can parse costs the facts it held
    and never the facts the Skill shipped with.
    """

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}, []

    if not isinstance(raw, dict):
        return {}, []

    entries = raw.get("models")
    plans = raw.get("plans")
    return (
        {
            str(entry["id"]): entry
            for entry in (entries if isinstance(entries, list) else [])
            if isinstance(entry, dict) and _text(entry.get("id"))
        },
        [
            entry
            for entry in (plans if isinstance(plans, list) else [])
            if isinstance(entry, dict)
        ],
    )


def _model_fault(entry: Any) -> str | None:
    """Return why one model entry may not enter the catalogue, or None."""

    if not isinstance(entry, dict):
        return "is not an object"
    if not _text(entry.get("id")):
        return "carries no id"
    if not _text(entry.get("source_url")):
        return "carries no source_url to attribute it to"
    if not _text(entry.get("retrieved")):
        return "carries no retrieved date to attribute it to"

    for member in ("price", "long_context"):
        fault = _card_fault(entry.get(member))
        if fault is not None:
            return f"its {member} {fault}"

    return _ladder_fault(entry.get("deliberation"))


def _card_fault(raw: Any) -> str | None:
    """Return why one rate card may not be priced from, or None.

    Nothing anywhere converts, so a card in another currency is not a cheaper
    card — it is a number that would be added to a dollar bill as though it
    were dollars, and a rate per thousand tokens read as one per million is
    wrong by a factor of a thousand in the direction that wins every ranking.
    """

    if raw is None:
        return None
    if not isinstance(raw, dict):
        return "is not a rate card"

    currency = _text(raw.get("currency")) or CURRENCY
    unit = _text(raw.get("unit")) or UNIT
    if currency != CURRENCY:
        return f"is quoted in {currency} rather than {CURRENCY}, and nothing converts"
    if unit != UNIT:
        return f"is quoted {unit} rather than {UNIT}"
    return None


def _ladder_fault(raw: Any) -> str | None:
    """Return why one deliberation list is not a subset of the ladder, or None."""

    if raw is None:
        return None
    if not isinstance(raw, list):
        return "carries a deliberation that is not a list"

    outside = sorted({str(item) for item in raw} - set(LEVELS))
    if outside:
        return f"names deliberation levels off the ladder: {', '.join(outside)}"
    return None


def _plan_fault(entry: Any) -> str | None:
    """Return why one plan entry may not be offered, or None."""

    if not isinstance(entry, dict):
        return "is not an object"

    for member in ("provider", "name", "source_url", "retrieved"):
        if not _text(entry.get(member)):
            return f"carries no {member}"

    monthly = entry.get("monthly_usd")
    if monthly is not None and _number(monthly) is None:
        return "carries a monthly_usd that is not a number"
    return None


def _model_name(entry: Any, index: int) -> str:
    """Return what a discarded model entry is called in the report."""

    if isinstance(entry, dict) and (identifier := _text(entry.get("id"))):
        return identifier
    return f"models[{index}]"


def _plan_name(entry: Any, index: int) -> str:
    """Return what a discarded plan entry is called in the report."""

    if isinstance(entry, dict):
        named = " ".join(
            part
            for member in ("provider", "name")
            if (part := _text(entry.get(member)))
        )
        if named:
            return named
    return f"plans[{index}]"


def _entry(model: Model) -> dict[str, Any]:
    """Return one model as the refreshed file holds it, every field carried.

    The refreshed entry replaces the seeded one whole, the fields in
    `SEEDED_FIELDS` aside, so a partial entry written here is a fact the Skill
    silently stops knowing.
    """

    return {
        "id": model.id,
        "provider": model.provider,
        "family": model.family,
        "aliases": list(model.aliases),
        "deliberation": list(model.deliberation),
        "price": _priced(model.price),
        "long_context_threshold": model.long_context_threshold,
        "long_context": _priced(model.long_context),
        "reasoning_billed_as": model.reasoning_billed_as,
        "capability": model.capability,
        "gateways": dict(model.gateways),
        "provider_says": model.provider_says,
        "released": model.released,
        "source_url": model.source_url,
        "retrieved": model.retrieved,
    }


def _now() -> str:
    """Return this instant, as the catalogue stamps what it was written at."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def plans_for(cat: Catalogue, provider: str) -> list[Plan]:
    """Return the plans *provider* sells, in the order the catalogue holds them.

    That order is the one they are offered in, and it belongs to whoever wrote
    the facts: a free tier before a paid one is a judgement about the list
    rather than about any entry in it.
    """

    return [plan for plan in cat.plans if plan.provider == provider]


def resolve(cat: Catalogue, token: str) -> list[Model]:
    """Return every model *token* names, newest release first.

    The token is whatever a user or a calling Skill typed: an exact id, an
    alias, or a bare family name that stands for several generations at once.
    An unknown token returns nothing rather than guessing.
    """

    wanted = token.strip().lower()
    if not wanted:
        return []

    # Id, then aliases, then family — one pass, because a token matching more
    # than one of those on the same model still names that model exactly once.
    matched = [
        model
        for model in cat.models
        if wanted == model.id.lower()
        or wanted in model.aliases
        or wanted == model.family.lower()
    ]

    # Newest first, and stable in id order underneath, so that a caller taking
    # `[0]` always takes the same model on the same catalogue.
    matched.sort(key=lambda model: model.id)
    matched.sort(key=lambda model: model.released or "", reverse=True)
    return matched


def cost_usd(
    model: Model,
    tokens: Mapping[str, float | None],
    kind: str,
    rule: ContextRule,
    *,
    rates: Price | None = None,
) -> float | None:
    """Price a token count for one kind of work, or return None where nothing can be.

    Two vendors of the three re-price the *whole* request once it passes a
    context threshold — every token, not the excess — and the jump is large
    enough that ignoring it systematically under-prices exactly the models
    this collection sends the most work to. Nothing here records the context
    size of a request that has not happened yet, so the kind of work stands in
    for it: repo-scale kinds are priced on the long-context card and the rest
    on the standard one. It is an approximation, and it is the honest one,
    because the alternative is quoting a repo-scale job a rate it will never
    actually pay.

    A category the rate card does not cover contributes nothing, which is what
    makes a partially known price still usable. The distinction that matters to
    a caller is between a small bill and no bill at all: an unpriceable model
    returns None so that ranking can rank it last instead of ranking it free.

    `rates` is what the user says they actually pay on the channel this model
    is reached through, and it replaces the catalogue's card whole — the cliff
    included, because a threshold is a fact about the provider's own card and
    not about a gateway that quoted one rate for every size of request.
    """

    price = rates or _card(model, kind, rule)
    if price is None:
        return None

    total = 0.0
    priced = False
    for category in TOKEN_CATEGORIES:
        rate = _rate_for(price, category, model.reasoning_billed_as)
        count = tokens.get(category)
        if rate is None or count is None:
            continue
        total += count * rate / PER_MILLION
        priced = True

    return total if priced else None


def _card(model: Model, kind: str, rule: ContextRule) -> Price | None:
    """Return the rate card this kind of work actually pays on this model."""

    if model.long_context_threshold is None or model.long_context is None:
        return model.price
    return model.long_context if rule.long_context(kind) else model.price


def _rate_for(price: Price, category: str, billing: str) -> float | None:
    """Return the rate that pays for *category*, following the reasoning rule."""

    # Reasoning has no rate of its own anywhere this Skill has looked; it is
    # billed as another category, or it is billed in a way nobody has told us.
    if category == "reasoning":
        if billing == "output":
            return price.output
        if billing == "input":
            return price.input
        return None

    return {
        "input": price.input,
        "cache_read": price.cache_read,
        "cache_write": price.cache_write,
        "output": price.output,
    }[category]


def _read(path: Path) -> tuple[list[Model], list[Plan], str, str | None]:
    """Read one catalogue file into models, plans, its stamp, and what went wrong."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], [], "", f"no catalogue at {path}"
    except (OSError, ValueError) as problem:
        return [], [], "", f"{path} could not be read: {problem}"

    if not isinstance(raw, dict):
        return [], [], "", f"{path} is not a JSON object"

    entries = raw.get("models")
    if not isinstance(entries, list):
        return [], [], "", f"{path} carries no models list"

    models = [model for entry in entries if (model := _model(entry)) is not None]
    offered = raw.get("plans")
    plans = [
        plan
        for entry in (offered if isinstance(offered, list) else [])
        if (plan := _plan(entry)) is not None
    ]
    return models, plans, _text(raw.get("generated_at")) or "", None


def _plan(entry: Any) -> Plan | None:
    """Build one subscription from one JSON entry, or None where it is unusable.

    A plan with no attribution is not offered at all. It would be shown to
    somebody choosing how they pay, with nothing to say where it came from or
    when — which is the state this member of the catalogue exists to end.
    """

    if not isinstance(entry, dict):
        return None

    provider = _text(entry.get("provider"))
    name = _text(entry.get("name"))
    source_url = _text(entry.get("source_url"))
    retrieved = _text(entry.get("retrieved"))
    if not provider or not name or not source_url or not retrieved:
        return None

    return Plan(
        provider, name, _number(entry.get("monthly_usd")), source_url, retrieved
    )


def _model(entry: Any) -> Model | None:
    """Build one model from one JSON entry, or None where it is unusable."""

    if not isinstance(entry, dict):
        return None

    identifier = _text(entry.get("id"))
    provider = _text(entry.get("provider"))
    family = _text(entry.get("family"))
    if not identifier or not provider or not family:
        return None

    billing = _text(entry.get("reasoning_billed_as")) or "unknown"
    return Model(
        id=identifier,
        provider=provider,
        family=family,
        aliases=_aliases(entry.get("aliases"), family),
        deliberation=_deliberation(entry.get("deliberation")),
        price=_price(entry.get("price")),
        long_context_threshold=_count(entry.get("long_context_threshold")),
        long_context=_price(entry.get("long_context")),
        reasoning_billed_as=billing if billing in BILLING else "unknown",
        capability=_fraction(entry.get("capability")),
        gateways=_gateways(entry.get("gateways")),
        provider_says=_text(entry.get("provider_says")),
        released=_text(entry.get("released")),
        source_url=_text(entry.get("source_url")),
        retrieved=_text(entry.get("retrieved")),
    )


def _aliases(raw: Any, family: str) -> tuple[str, ...]:
    """Return the lowercase aliases, with the family always among them."""

    found = [] if not isinstance(raw, list) else [_text(item) for item in raw]
    names = [name.lower() for name in found if name] + [family.lower()]
    return tuple(dict.fromkeys(names))


def _gateways(raw: Any) -> tuple[tuple[str, str], ...]:
    """Return each gateway's slug for a model, dropping what is not one.

    A value that is not an object is no slugs at all, and a slug that is not a
    non-empty string is dropped alone: a hand-edited catalogue costs its own
    bad entry, and a planner never reads a slug nobody wrote.
    """

    if not isinstance(raw, dict):
        return ()
    return tuple(
        (gateway, slug)
        for gateway, value in raw.items()
        if (slug := _text(value)) is not None and _text(gateway) is not None
    )


def _deliberation(raw: Any) -> tuple[str, ...]:
    """Return the supported levels as a subset of LEVELS, in LEVELS order."""

    if not isinstance(raw, list):
        return ()
    named = {_text(item) for item in raw}
    return tuple(level for level in LEVELS if level in named)


def _price(raw: Any) -> Price | None:
    """Build a rate card, treating an absent or malformed one as no card."""

    if not isinstance(raw, dict):
        return None
    return Price(
        input=_number(raw.get("input")),
        cache_read=_number(raw.get("cache_read")),
        cache_write=_number(raw.get("cache_write")),
        output=_number(raw.get("output")),
        currency=_text(raw.get("currency")) or CURRENCY,
        unit=_text(raw.get("unit")) or UNIT,
    )


def _text(raw: Any) -> str | None:
    """Return a non-empty string, or None for anything else including null."""

    return raw if isinstance(raw, str) and raw.strip() else None


def _number(raw: Any) -> float | None:
    """Return a finite float, or None for anything that is not one."""

    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    value = float(raw)
    return value if math.isfinite(value) else None


def _count(raw: Any) -> int | None:
    """Return a whole number of tokens, or None for anything that is not one."""

    value = _number(raw)
    return None if value is None else int(value)


def _fraction(raw: Any) -> float | None:
    """Return a number clamped to 0..1, the scale capability is compared on."""

    value = _number(raw)
    return None if value is None else min(1.0, max(0.0, value))


def default_data() -> Path:
    """Return the directory this Skill keeps its refreshed facts in by default."""

    return Path.home() / ".kntnt" / "model-selector"


def _document(cat: Catalogue) -> dict[str, Any]:
    """Return the whole merged catalogue, in the shape a reader consumes it."""

    return {
        "generated_at": cat.generated_at,
        "problem": cat.problem,
        "models": [
            {
                "id": model.id,
                "provider": model.provider,
                "family": model.family,
                "deliberation": list(model.deliberation),
                "provider_says": model.provider_says,
                "price": _priced(model.price),
                "source_url": model.source_url,
                "retrieved": model.retrieved,
            }
            for model in cat.models
        ],
        "plans": [
            {
                "provider": plan.provider,
                "name": plan.name,
                "monthly_usd": plan.monthly_usd,
                "source_url": plan.source_url,
                "retrieved": plan.retrieved,
            }
            for plan in cat.plans
        ],
    }


def _priced(price: Price | None) -> dict[str, Any] | None:
    """Return one rate card as a reader of the merged catalogue sees it."""

    if price is None:
        return None
    return {
        "input": price.input,
        "cache_read": price.cache_read,
        "cache_write": price.cache_write,
        "output": price.output,
        "currency": price.currency,
        "unit": price.unit,
    }


def _emit(payload: Mapping[str, Any]) -> None:
    """Print one machine-readable answer, as every reader of this Skill's gets it."""

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    """Print the merged catalogue, or adopt what an agent read into it.

    The interview reads the print rather than the two files behind it. Which
    of the two wins, and how a refreshed provider replaces a whole list of
    plans, are rules this module keeps; a second copy of them in prose
    somebody follows by hand is a second thing to keep true.

    A refused document exits 1. Nothing was written, and the agent that fetched
    it is who has to be told so rather than left reading a report as a success.
    """

    parser = argparse.ArgumentParser(
        prog="catalogue.py",
        description=(
            "Print what models and subscriptions this machine knows about, or "
            "adopt a document of fetched facts into them."
        ),
    )
    parser.add_argument("action", nargs="*", metavar="adopt <path>")
    parser.add_argument("--data", default=str(default_data()))
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    data_dir = Path(args.data).expanduser()
    here = Path(__file__).resolve().parent.parent
    if not args.action:
        _emit(_document(load(data_dir, here)))
        return 0

    if len(args.action) != 2 or args.action[0] != "adopt":
        parser.error("the one verb beside the bare form is `adopt <path>`")

    report = adopt(data_dir, here, Path(args.action[1]).expanduser())
    _emit(report)
    return 1 if report["refused"] else 0


if __name__ == "__main__":
    sys.exit(main())
