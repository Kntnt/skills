# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""What models exist, what they cost, and how capable they are.

Every other module in this Skill asks the world a question and this is what
answers it. The facts arrive from two places and one of them is allowed to be
wrong: the seed shipped beside this file is what the Skill knows on the day it
is installed, and `catalogue.json` under the data directory is whatever a later
catalogue pass or `update` established. The refreshed file wins per model id,
because a fact read this week outranks a fact this repository froze at
release — except for the fields `update` never reads — `capability`, which
nothing fetches, and `gateways`, which only the seed and the catalogue pass's
matching write — and which a refreshed entry carrying none of them takes from
the seed. A model its maker stopped listing is removed by the catalogue pass,
and `lifecycle.json` beside the refreshed file masks the seed's copy of it, so
that no later load or release of the seed brings it back.

Nothing here raises. A catalogue that cannot be read is a catalogue that says
so in `problem` and hands back what it still has, because every caller of this
module is answering a question for a machine that is already mid-task, and a
traceback there costs the caller its work rather than merely its accuracy.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import select
import signal
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Protocol, Self

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

    A model the catalogue pass removed is masked out of the seed, since the
    seed goes on carrying whatever it was released with. The mask covers the
    seed's copy alone: an entry for that id in the refreshed file shows
    through it, a re-added model being an ordinary one.

    A missing or unreadable refreshed file leaves the seed standing and is
    reported in `problem`; only a seed that will not parse empties the answer,
    because at that point the Skill knows nothing at all about the world.
    """

    # The seed is the floor. Without it there is no catalogue to merge into.
    seed, seed_plans, seed_generated, seed_problem = _read(here / "data" / SEED_FILE)
    if seed_problem is not None:
        return Catalogue((), (), "", seed_problem)

    # The refreshed file overrides model by model, so a refresh that says
    # nothing about a model leaves the seed's copy standing. Only a removal
    # recorded in `lifecycle.json` takes the seed's copy away.
    refreshed, refreshed_plans, refreshed_generated, refresh_problem = _read(
        data_dir / REFRESHED_FILE
    )
    masked = _removed(_lifecycle(data_dir))
    seeded: dict[str, Model] = {model.id: model for model in seed}
    merged = {
        identifier: model
        for identifier, model in seeded.items()
        if identifier not in masked
    }
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
    """Return a refreshed *model*, the seed filling what `update` never reads.

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

    Models merge entry by entry, because a refresh that says nothing about a
    model is no evidence that it is gone; that is established only by its
    maker's own list, and the catalogue pass records it in `lifecycle.json`.
    Plans have no such list: a provider retires one, and a merge by name would
    go on offering it to somebody choosing how they pay for as long as this
    Skill is installed. So a provider the refreshed file speaks about at all is
    a provider whose plans it states in full.
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
    else standing — `capability` and `gateways` above all, which no reading of
    a page supplies — and a rate card merges category by category, so a card
    carrying one figure keeps every other. A provider's plans are replaced
    whole, as `_merged_plans` explains.
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

    # A removed model this document brings back is an ordinary model again,
    # and forgetting its removal in the same operation is what stops a pass
    # running before the next refresh from deleting the rows filed since.
    _forget_removals(data_dir, [entry["id"] for entry in adopted])

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
        for member in ("price", "long_context"):
            if isinstance(offered.get(member), dict):
                offered[member] = _merged_card(base.get(member), offered[member])
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


def _merged_card(standing: Any, offered: Mapping[str, Any]) -> dict[str, Any]:
    """Lay one offered rate card over the standing one, category by category.

    A category the offer omits, or states as null, keeps the standing figure:
    a page read for its input price is no evidence that the cached rate
    beside it stopped existing.
    """

    held = standing if isinstance(standing, dict) else {}
    card = {
        category: held.get(category)
        for category in ("input", "cache_read", "cache_write", "output")
    }
    card["currency"] = held.get("currency") or CURRENCY
    card["unit"] = held.get("unit") or UNIT
    card.update({key: value for key, value in offered.items() if value is not None})
    return card


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

    # Null is a state of knowledge — the provider publishes no such rate — and
    # anything else has to be a rate somebody could actually be billed.
    for member in ("input", "cache_read", "cache_write", "output"):
        value = raw.get(member)
        if value is None:
            continue
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            return f"carries an {member} that is not a finite, non-negative number"
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

    The catalogue's card is the price OpenRouter publishes, which is the
    charge itself on an OpenRouter channel. `rates` is what the user says they
    actually pay on the channel this model is reached through, and it still
    replaces the catalogue's card whole — the cliff included, because a rate a
    user recorded is one rate for every size of request.
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


# --- The pass that keeps the catalogue current -------------------------------
#
# Three structured sources, read by a script with no agent and no model call
# (ADR-0191). The harness lists say which Claude and GPT models this account
# is offered and at which levels; OpenRouter's public list says what every
# model costs, when it was released, and which Grok models exist at all.

# Where each source's facts are published. The two harness lists are spoken to
# over their own stdio protocols, exactly as recorded on 2026-09-11; nothing in
# either exchange is a prompt, so neither can start a model.
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_HOST = "openrouter.ai"
CLAUDE_LIST_ARGV = (
    "claude",
    "-p",
    "--input-format",
    "stream-json",
    "--output-format",
    "stream-json",
    "--verbose",
    "--safe-mode",
    "--no-session-persistence",
    "--tools",
    "",
    "--permission-mode",
    "dontAsk",
    "--permission-prompts",
    "none",
)
CLAUDE_REQUEST_ID = "refresh-init"
CODEX_LIST_ARGV = ("codex", "app-server", "--listen", "stdio://")

# How long one exchange may take before its process group is killed and the
# source reported unreadable: a `claude` waiting for a login never answers.
EXCHANGE_SECONDS = 30.0

# Codex answers `model/list` from a cache it refreshes after 300 seconds, and
# from a list bundled with the binary where the refresh fails. A cache older
# than that before the pass began is the bundled list speaking.
CODEX_CACHE_TTL = 300
CODEX_CACHE_FILE = "models_cache.json"

# The first-party documentation of each harness list, which is what a model
# the list establishes is attributed to where OpenRouter carries no page.
HARNESS_DOCS = {
    "claude": "https://code.claude.com/docs/en/agent-sdk/typescript",
    "codex": "https://learn.chatgpt.com/docs/app-server#list-models-modellist",
}

# Which maker each harness list speaks for. Grok has no harness list of its
# own: it is reached only through OpenRouter, so OpenRouter says what it offers.
HARNESS_MAKERS = {"claude": "anthropic", "codex": "openai"}
GATEWAY_MAKER = "spacexai"

# How OpenRouter spells each maker, and how its per-token categories map onto
# the catalogue's. A category the catalogue has no field for is ignored.
OPENROUTER_PREFIXES = {
    "anthropic": "anthropic/",
    "openai": "openai/",
    "spacexai": "x-ai/",
}
OPENROUTER_CATEGORIES = (
    ("prompt", "input"),
    ("completion", "output"),
    ("input_cache_read", "cache_read"),
    ("input_cache_write", "cache_write"),
)
PRICED = ("input", "cache_read", "cache_write", "output")

# Six places per million tokens is a millionth of a cent per token, finer than
# any price published, and coarse enough that float noise never journals.
_PLACES = Decimal("0.000001")

JOURNAL_FILE = "catalogue-journal.jsonl"
PASS_FILE = "refresh.json"

# Where a model's run of absent days and its removal are kept. Apart from
# `catalogue.json`, which `adopt` rewrites whole, and apart from the evidence,
# which `reset --evidence` discards: this is catalogue state.
LIFECYCLE_FILE = "lifecycle.json"

# How many consecutive UTC days a model must be missing from its maker's
# complete list before it is gone. Deletion cannot be undone, and a vendor's
# list is occasionally wrong for a day.
GONE_AFTER_DAYS = 3

# Which list says whether a model of each maker still exists. The two harness
# lists speak for the makers they list; Grok is reached only through
# OpenRouter, so OpenRouter's public list is its maker's list.
PRESENCE_SOURCES = (
    ("claude", "anthropic"),
    ("codex", "openai"),
    ("openrouter", "spacexai"),
)
NO_MAKERS = "no makers chosen"
NO_PRICE_SOURCE = "no price source"
OUTCOMES = ("complete", "incomplete", "unreadable")


@dataclass(frozen=True)
class Offer:
    """One model a harness list offers, with what that list says about it.

    `levels` is None where the list reports no levels for the model, which is
    different from reporting an empty set: Haiku's absent field leaves the
    catalogue's levels standing.
    """

    id: str
    provider: str
    family: str
    aliases: tuple[str, ...]
    levels: tuple[str, ...] | None


@dataclass(frozen=True)
class Reading:
    """What one source said, and whether it said all of it.

    `complete` is a whole answer. `incomplete` is a positive answer that may
    be missing entries, and never evidence that something is gone. An
    `unreadable` source changes nothing it governs.

    `returned` is the version identifier of every entry a harness list
    returned, hidden ones included, which is what presence is judged on:
    `listed` leaves hidden entries out, and a model the list still returns
    is not a model that is gone.
    """

    source: str
    outcome: str
    reason: str | None
    listed: tuple[Offer, ...] = ()
    entries: tuple[Mapping[str, Any], ...] = ()
    returned: tuple[str, ...] = ()


def unreadable(source: str, reason: str) -> Reading:
    """Return the reading of a source that could not be read, and why."""

    return Reading(source, "unreadable", reason)


def per_million(raw: Any) -> float | None:
    """Return a per-token price string as USD per million tokens, or None.

    Decimal rather than float, rounded to six places, because `0.0000002` per
    token is 0.2 per million and float arithmetic says 0.19999999999999998 —
    a difference the journal would otherwise record as a price change on
    every pass.
    """

    if isinstance(raw, bool) or not isinstance(raw, (str, int, float)):
        return None
    try:
        value = Decimal(str(raw))
    except InvalidOperation:
        return None
    if not value.is_finite():
        return None
    return float((value * 1_000_000).quantize(_PLACES))


def openrouter_slug(provider: str, identifier: str) -> str | None:
    """Return the OpenRouter id a harness id normalises to, or None.

    Prefix by maker, drop a trailing `-YYYYMMDD`, and turn a hyphen between two
    digits into a dot: `claude-haiku-4-5-20251001` is `anthropic/claude-haiku-4.5`.
    """

    prefix = OPENROUTER_PREFIXES.get(provider)
    if prefix is None:
        return None
    name = re.sub(r"-\d{8}$", "", identifier)
    return prefix + re.sub(r"(?<=\d)-(?=\d)", ".", name)


def claude_reading(messages: Sequence[Any]) -> Reading:
    """Read Claude Code's answer to `initialize` into the models it offers.

    Complete where the control response is a `success` carrying `models`. The
    `default` entry names a model another entry names too, and is skipped; a
    bracketed serving selector such as `[1m]` is not a different model.
    """

    answer = next(
        (
            message
            for message in messages
            if isinstance(message, dict) and message.get("type") == "control_response"
        ),
        None,
    )
    if answer is None:
        return unreadable("claude", "Claude Code sent no control response")

    response = answer.get("response")
    if not isinstance(response, dict) or response.get("subtype") != "success":
        said = response.get("error") if isinstance(response, dict) else None
        return unreadable(
            "claude", f"Claude Code did not answer `initialize` with success: {said}"
        )

    body = response.get("response")
    models = body.get("models") if isinstance(body, dict) else None
    if not isinstance(models, list):
        return unreadable(
            "claude", "Claude Code's answer to `initialize` carries no models"
        )

    offers: dict[str, Offer] = {}
    returned: dict[str, None] = {}
    for entry in models:
        if not isinstance(entry, dict):
            continue
        value = _text(entry.get("value"))
        resolved = _text(entry.get("resolvedModel"))
        if resolved and value != "default":
            returned[_unbracketed(resolved)] = None
        if not value or not resolved or value == "default":
            continue
        identifier = _unbracketed(resolved)
        family = _unbracketed(value).lower()
        levels = _levels(entry.get("supportedEffortLevels"))
        held = offers.get(identifier)
        aliases = (*held.aliases, family) if held is not None else (family,)
        offers[identifier] = Offer(
            identifier,
            "anthropic",
            held.family if held is not None else family,
            tuple(dict.fromkeys(aliases)),
            levels if held is None or held.levels is None else held.levels,
        )

    return Reading(
        "claude", "complete", None, tuple(offers.values()), returned=tuple(returned)
    )


def codex_reading(
    pages: Sequence[Any],
    fetched_at: str | None,
    started: datetime,
    failure: str | None = None,
) -> Reading:
    """Read the pages of Codex's `model/list` into the models it offers.

    Hidden entries are skipped. The list is incomplete where paging broke off
    or where the models cache is older than the pass minus its TTL, which is
    Codex answering from the list bundled with the binary.
    """

    if (
        not pages
        or not isinstance(pages[0], dict)
        or not isinstance(pages[0].get("data"), list)
    ):
        return unreadable("codex", failure or "Codex's `model/list` answered no data")

    offers: dict[str, Offer] = {}
    returned: dict[str, None] = {}
    for page in pages:
        data = page.get("data") if isinstance(page, dict) else None
        for entry in data if isinstance(data, list) else []:
            if not isinstance(entry, dict):
                continue
            identifier = _text(entry.get("model")) or _text(entry.get("id"))
            if not identifier:
                continue
            returned[identifier] = None
            if entry.get("hidden") is True:
                continue
            efforts = entry.get("supportedReasoningEfforts")
            named = (
                [
                    item.get("reasoningEffort") if isinstance(item, dict) else item
                    for item in efforts
                ]
                if isinstance(efforts, list)
                else None
            )
            offers[identifier] = Offer(
                identifier, "openai", _gpt_family(identifier), (), _levels(named)
            )

    listed = tuple(offers.values())
    every = tuple(returned)
    if failure is not None:
        return Reading("codex", "incomplete", failure, listed, returned=every)
    stale = _stale(fetched_at, started)
    if stale is not None:
        return Reading("codex", "incomplete", stale, listed, returned=every)
    return Reading("codex", "complete", None, listed, returned=every)


def openrouter_reading(pages: Sequence[Any], failure: str | None = None) -> Reading:
    """Collect the entries of OpenRouter's model list, and say whether all arrived.

    Where `total_count` is present the collected count must equal it, or the
    read is incomplete — and an incomplete price list changes no price.
    """

    if (
        not pages
        or not isinstance(pages[0], dict)
        or not isinstance(pages[0].get("data"), list)
    ):
        return unreadable(
            "openrouter", failure or "OpenRouter's model list carries no data"
        )

    entries = tuple(
        entry
        for page in pages
        if isinstance(page, dict) and isinstance(page.get("data"), list)
        for entry in page["data"]
        if isinstance(entry, dict) and _text(entry.get("id"))
    )
    if failure is not None:
        return Reading("openrouter", "incomplete", failure, entries=entries)

    total = pages[-1].get("total_count") if isinstance(pages[-1], dict) else None
    if isinstance(total, int) and not isinstance(total, bool) and len(entries) != total:
        return Reading(
            "openrouter",
            "incomplete",
            f"collected {len(entries)} models where OpenRouter's total_count names {total}",
            entries=entries,
        )
    return Reading("openrouter", "complete", None, entries=entries)


def read_claude(started: datetime) -> Reading:
    """Ask Claude Code which models this account is offered, generating nothing."""

    request = {
        "type": "control_request",
        "request_id": CLAUDE_REQUEST_ID,
        "request": {"subtype": "initialize"},
    }
    try:
        with _Exchange(CLAUDE_LIST_ARGV) as talk:
            talk.send(request)
            answer = talk.receive(_answers_initialize)
    except FileNotFoundError:
        return unreadable("claude", "claude is not on the PATH")
    except TimeoutError:
        return unreadable(
            "claude", f"claude did not answer within {EXCHANGE_SECONDS:g} seconds"
        )
    except (EOFError, OSError) as problem:
        return unreadable("claude", f"claude could not be read: {problem}")
    return claude_reading([answer])


def _answers_initialize(message: dict[str, Any]) -> bool:
    """Return whether *message* is Claude Code's answer to this pass's `initialize`."""

    response = message.get("response")
    return (
        message.get("type") == "control_response"
        and isinstance(response, dict)
        and response.get("request_id") == CLAUDE_REQUEST_ID
    )


def _answering(number: int) -> Callable[[dict[str, Any]], bool]:
    """Return the test for the JSON-RPC response to request *number*."""

    def answers(message: dict[str, Any]) -> bool:
        return message.get("id") == number

    return answers


def read_codex(started: datetime) -> Reading:
    """Ask Codex which models this account is offered, following every page."""

    pages: list[Any] = []
    failure: str | None = None
    try:
        with _Exchange(CODEX_LIST_ARGV) as talk:
            talk.send(
                {
                    "id": 0,
                    "method": "initialize",
                    "params": {
                        "clientInfo": {
                            "name": "model_selector_refresh",
                            "version": "1",
                        },
                        "capabilities": {},
                    },
                }
            )
            opened = talk.receive(lambda message: message.get("id") == 0)
            if "result" not in opened:
                return unreadable(
                    "codex", f"Codex refused `initialize`: {opened.get('error')}"
                )
            talk.send({"method": "initialized", "params": {}})

            cursor: Any = None
            for number in range(1, 51):
                params: dict[str, Any] = {"limit": 100, "includeHidden": True}
                if cursor:
                    params["cursor"] = cursor
                talk.send({"id": number, "method": "model/list", "params": params})
                try:
                    answer = talk.receive(_answering(number))
                except (TimeoutError, EOFError) as problem:
                    if not pages:
                        raise
                    failure = f"page {number} of `model/list` did not arrive: {problem or 'deadline'}"
                    break
                result = answer.get("result")
                if not isinstance(result, dict):
                    if not pages:
                        return unreadable(
                            "codex",
                            f"Codex refused `model/list`: {answer.get('error')}",
                        )
                    failure = f"page {number} of `model/list` was refused: {answer.get('error')}"
                    break
                pages.append(result)
                cursor = result.get("nextCursor")
                if not cursor:
                    break
            else:
                failure = "`model/list` was still paging after 50 pages"
    except FileNotFoundError:
        return unreadable("codex", "codex is not on the PATH")
    except TimeoutError:
        return unreadable(
            "codex", f"codex did not answer within {EXCHANGE_SECONDS:g} seconds"
        )
    except (EOFError, OSError) as problem:
        return unreadable("codex", f"codex could not be read: {problem}")

    return codex_reading(pages, _codex_fetched_at(), started, failure)


def read_openrouter(
    started: datetime, fetch: Callable[[str], bytes] | None = None
) -> Reading:
    """Read OpenRouter's public model list, following `links.next` on its own host."""

    get = fetch or _fetch
    url: str | None = OPENROUTER_MODELS_URL
    pages: list[Any] = []
    seen: set[str] = set()
    failure: str | None = None
    while url is not None:
        seen.add(url)
        try:
            page = json.loads(get(url))
        except (OSError, ValueError) as problem:
            if not pages:
                return unreadable("openrouter", f"{url} could not be read: {problem}")
            failure = f"{url} could not be read: {problem}"
            break
        pages.append(page)

        links = page.get("links") if isinstance(page, dict) else None
        following = _text(links.get("next")) if isinstance(links, dict) else None
        if following is None:
            break
        target = urllib.parse.urljoin(OPENROUTER_MODELS_URL, following)
        parsed = urllib.parse.urlparse(target)
        if parsed.scheme != "https" or parsed.netloc != OPENROUTER_HOST:
            failure = f"OpenRouter's next page points off its own host, at {target}"
            break
        if target in seen:
            failure = f"OpenRouter's next page repeats {target}"
            break
        url = target

    return openrouter_reading(pages, failure)


# The three readers a pass consults, and nothing else.
READERS: Mapping[str, Callable[[datetime], Reading]] = {
    "claude": read_claude,
    "codex": read_codex,
    "openrouter": read_openrouter,
}


def refresh(
    data_dir: Path,
    here: Path,
    agents: Path,
    *,
    now: datetime | None = None,
    readers: Mapping[str, Callable[[datetime], Reading]] | None = None,
) -> dict[str, Any]:
    """Bring the catalogue up to date with the three sources, journalling every change.

    What each source governs is the whole of what it can change. The harness
    lists add the Claude and GPT models of a chosen maker, and set their
    aliases and levels. OpenRouter sets prices, release dates and the slug it
    routes each model by, and says which Grok models are offered. A source
    that cannot be read changes nothing it governs, and an incomplete
    OpenRouter list changes nothing at all. A missing, old-shape or damaged
    profile chooses no maker, so nothing is read and only `refresh.json` is
    written, saying so.

    A model missing from its maker's complete list on three consecutive UTC
    days is gone: its entry is removed, the seed's copy masked, and every
    measurement row and pending Unit of it deleted. Only a complete read is an
    observation, so a failed or partial one breaks the run rather than
    extending it, and a failure to run a model is never one at all. Every
    pass, one choosing no maker included, deletes whatever rows have been
    filed since for the models it removed.

    Each entry is checked by the same validator `adopt` uses before it is
    written, and the stored file is written whole, the plans carried through,
    so `load` never falls back to the seed by accident. After any write the
    generated agent definitions in *agents* are brought into line.
    """

    # Imported here: both import this module, and a module-level import would
    # be a cycle.
    import launch
    import profiles

    started = (now or datetime.now(UTC)).astimezone(UTC)
    stamp = _instant(started)
    today = started.date().isoformat()
    cat = load(data_dir, here)
    profile = profiles.load(data_dir, cat)
    makers = frozenset(profile.makers) if profile.source != "fallback" else frozenset()
    previous = _last_pass(data_dir / PASS_FILE)
    seen = _seen_today(previous, today)
    records = _lifecycle(data_dir)
    held = _document_of(records)
    if not makers:
        report: dict[str, Any] = {"at": stamp, "outcome": NO_MAKERS}
        if seen:
            report["present"] = {"day": today, "models": sorted(seen)}
        if _removed(records):
            report["lifecycle"] = _settle_lifecycle(data_dir, records, held, {})
        _replace_json(data_dir / PASS_FILE, report)
        return report

    consulted = [source for source, maker in HARNESS_MAKERS.items() if maker in makers]
    consulted.append("openrouter")
    readings = {
        source: _consult((readers or READERS).get(source), source, started)
        for source in consulted
    }

    step = _Pass(
        {model.id: _entry(model) for model in cat.models},
        makers,
        stamp,
        today,
        frozenset(previous.get("unmatched") or ())
        if isinstance(previous.get("unmatched"), list)
        else frozenset(),
    )
    for source, reading in readings.items():
        if source in HARNESS_MAKERS and reading.outcome != "unreadable":
            step.listed(source, reading)
    gateway = readings["openrouter"]
    if gateway.outcome == "complete":
        if GATEWAY_MAKER in makers:
            step.offered_through_gateway(gateway)
        step.priced(gateway)

    # Presence is judged on the entries as this pass leaves them, so a slug
    # the matching above just wrote back is the slug a Grok model is found by.
    stored_models, stored_plans = _stored(data_dir / REFRESHED_FILE)
    _forget(records, stored_models)
    shown, lacking = _presence(readings, makers, step.entries)
    gone = _observed(
        records,
        shown,
        lacking,
        seen,
        today,
        (started - timedelta(days=1)).date().isoformat(),
    )
    changed, discarded = step.settled()
    rows = [row for row in step.rows if row["model"] not in gone]
    report = {
        "at": stamp,
        "outcome": "ran",
        "sources": {},
        "changes": 0,
        "written": None,
        "definitions": None,
        "discarded": discarded,
        "unmatched": sorted(
            step.unmatched if gateway.outcome == "complete" else step.unmatched_before
        ),
        "present": {"day": today, "models": sorted(seen)},
    }

    written = False
    if changed or gone:
        stored_models.update(changed)
        for identifier in gone:
            stored_models.pop(identifier, None)
        try:
            _replace_json(
                data_dir / REFRESHED_FILE,
                {
                    "generated_at": stamp,
                    "models": [stored_models[name] for name in sorted(stored_models)],
                    "plans": stored_plans,
                },
            )
        except OSError as problem:
            report["problem"] = f"the catalogue could not be written: {problem}"
        else:
            written = True
            report["written"] = str(data_dir / REFRESHED_FILE)

    # A removal is recorded only once the entry is out of the file; until then
    # its three absent days stand, and the next pass removes it.
    removed_now = gone if written else {}
    for identifier, days in removed_now.items():
        records[identifier] = {
            "absent_days": days,
            "removed_at": stamp,
            "rows_deleted": 0,
            "units_dropped": 0,
        }
    if written:
        _forget(records, stored_models)
    report["lifecycle"] = _settle_lifecycle(data_dir, records, held, removed_now)
    for identifier, days in removed_now.items():
        rows.append(
            {
                "at": stamp,
                "source": lacking[identifier],
                "model": identifier,
                "field": "removed",
                "old": None,
                "new": {
                    "absent_days": days,
                    "rows_deleted": records[identifier]["rows_deleted"],
                    "units_dropped": records[identifier]["units_dropped"],
                },
            }
        )

    report["sources"] = {
        source: {
            "outcome": reading.outcome,
            "reason": reading.reason,
            "changes": sum(1 for row in rows if row["source"] == source),
        }
        for source, reading in readings.items()
    }
    report["changes"] = len(rows)

    if written:
        try:
            if rows:
                with (data_dir / JOURNAL_FILE).open(
                    "a", encoding="utf-8"
                ) as journal_stream:
                    for row in rows:
                        journal_stream.write(json.dumps(row, sort_keys=True) + "\n")
        except OSError as problem:
            report["problem"] = f"the journal could not be written: {problem}"
        try:
            synced = launch.sync_definitions(
                agents, launch.definitions(profile, load(data_dir, here))
            )
        except OSError as problem:
            report["definitions"] = {
                "directory": str(agents),
                "problem": str(problem),
            }
        else:
            report["definitions"] = {
                "directory": str(agents),
                "written": synced.written,
                "unchanged": synced.unchanged,
                "removed": synced.removed,
            }

    try:
        _replace_json(data_dir / PASS_FILE, report)
    except OSError as problem:
        report["problem"] = f"{data_dir / PASS_FILE} could not be written: {problem}"
    return report


def _presence(
    readings: Mapping[str, Reading],
    makers: frozenset[str],
    entries: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Return which catalogue models their maker's complete list shows, and which it lacks.

    Each maps a model id to the source that said so. A model is judged only
    where its maker is chosen and its maker's list was read completely, and
    only on the version identifier the list names: a Claude entry's
    `resolvedModel` without its bracketed serving selector, a Codex entry's
    `model`, and OpenRouter's full id, which a Grok model matches by its id or
    by its OpenRouter slug. An alias never establishes presence — a family
    alias moves to each new release, and matching on it would keep a replaced
    release present for ever.
    """

    shown: dict[str, str] = {}
    lacking: dict[str, str] = {}
    for source, maker in PRESENCE_SOURCES:
        reading = readings.get(source)
        if maker not in makers or reading is None or reading.outcome != "complete":
            continue
        names = (
            frozenset(str(entry["id"]) for entry in reading.entries)
            if source == "openrouter"
            else frozenset(reading.returned)
        )
        for identifier, entry in entries.items():
            if entry.get("provider") != maker:
                continue
            gateways = entry.get("gateways")
            slug = (
                _text(gateways.get("openrouter"))
                if source == "openrouter" and isinstance(gateways, dict)
                else None
            )
            if identifier in names or (slug is not None and slug in names):
                shown[identifier] = source
            else:
                lacking[identifier] = source
    return shown, lacking


def _observed(
    records: dict[str, dict[str, Any]],
    shown: Mapping[str, str],
    lacking: Mapping[str, str],
    seen: set[str],
    today: str,
    yesterday: str,
) -> dict[str, list[str]]:
    """Record one pass's observations, and return each model now gone with its absent days.

    A day is absent where a complete read that day lacked the model and none
    showed it, so a model shown by any read today is never absent today, and
    *seen* carries that across the passes of one day. Absent days count only
    while they are consecutive: a day with no complete read leaves a gap, and
    a gap starts the run again. A run no pass can extend any more is dropped.
    """

    for identifier in shown:
        seen.add(identifier)
        if identifier in records and not _is_removal(records[identifier]):
            del records[identifier]

    gone: dict[str, list[str]] = {}
    for identifier in lacking:
        if identifier in seen or _is_removal(records.get(identifier)):
            continue
        held = records.get(identifier) or {}
        days = [day for day in held.get("absent_days") or [] if isinstance(day, str)]
        if not days or days[-1] != today:
            days = [*days, today] if days and days[-1] == yesterday else [today]
        days = days[-GONE_AFTER_DAYS:]
        records[identifier] = {"absent_days": days}
        if len(days) >= GONE_AFTER_DAYS:
            gone[identifier] = days

    for identifier in list(records):
        held = records[identifier]
        days = held.get("absent_days") or []
        if not _is_removal(held) and (not days or str(days[-1]) < yesterday):
            del records[identifier]
    return gone


def _settle_lifecycle(
    data_dir: Path,
    records: dict[str, dict[str, Any]],
    held: str,
    removed_now: Mapping[str, list[str]],
) -> dict[str, Any]:
    """Delete the rows of every removed model, then write `lifecycle.json` where it moved.

    The deletion runs under the ledger's lock. Where another pass holds it,
    the removal stands and its rows wait for the next pass that gets the lock;
    `lifecycle.json` keeps each removed model's running counts, which is what
    status reports.
    """

    import evidence  # Imported here: it imports this module.

    removed = sorted(
        identifier for identifier in records if _is_removal(records[identifier])
    )
    outcome: dict[str, Any] = {
        "removed": sorted(removed_now),
        "lock": None,
        "rows_deleted": 0,
        "units_dropped": 0,
    }
    if removed:
        try:
            with evidence.lock(data_dir) as taken:
                outcome["lock"] = "held" if taken else "busy"
                deleted = evidence.discard_models(data_dir, removed) if taken else None
        except OSError as problem:
            outcome["problem"] = (
                f"the rows of removed models could not be deleted: {problem}"
            )
            deleted = None
        if deleted is not None:
            for identifier in removed:
                record = records[identifier]
                rows = deleted.rows.get(identifier, 0)
                units = deleted.units.get(identifier, 0)
                record["rows_deleted"] = int(record.get("rows_deleted") or 0) + rows
                record["units_dropped"] = int(record.get("units_dropped") or 0) + units
                outcome["rows_deleted"] += rows
                outcome["units_dropped"] += units

    path = data_dir / LIFECYCLE_FILE
    if _document_of(records) != held and (records or path.exists()):
        try:
            _replace_json(path, {"models": records})
        except OSError as problem:
            outcome["problem"] = f"{path} could not be written: {problem}"
    return outcome


def _forget(records: dict[str, dict[str, Any]], present: Collection[str]) -> None:
    """Drop the removal of every model `catalogue.json` holds again.

    A re-added model is an ordinary one: its mask, its removal record and its
    absence history all go at once, and no pass deletes anything for it again.
    """

    for identifier in [name for name in records if name in present]:
        if _is_removal(records[identifier]):
            del records[identifier]


def _forget_removals(data_dir: Path, identifiers: Sequence[str]) -> None:
    """Forget the removal of every model in *identifiers*, rewriting `lifecycle.json` if any."""

    records = _lifecycle(data_dir)
    held = _document_of(records)
    _forget(records, frozenset(identifiers))
    if _document_of(records) != held:
        _replace_json(data_dir / LIFECYCLE_FILE, {"models": records})


def _lifecycle(data_dir: Path) -> dict[str, dict[str, Any]]:
    """Return `lifecycle.json`'s record per model, an unreadable file holding none."""

    try:
        raw = json.loads((data_dir / LIFECYCLE_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    models = raw.get("models") if isinstance(raw, dict) else None
    if not isinstance(models, dict):
        return {}
    return {
        str(identifier): dict(record)
        for identifier, record in models.items()
        if isinstance(record, dict)
    }


def _removed(records: Mapping[str, Mapping[str, Any]]) -> frozenset[str]:
    """Return the ids whose record is a removal."""

    return frozenset(
        identifier for identifier, record in records.items() if _is_removal(record)
    )


def _is_removal(record: Mapping[str, Any] | None) -> bool:
    """Return whether one lifecycle record says its model was removed."""

    return record is not None and _text(record.get("removed_at")) is not None


def _document_of(records: Mapping[str, Any]) -> str:
    """Return *records* as one comparable string, to tell whether a pass moved them."""

    return json.dumps(records, sort_keys=True)


def _seen_today(previous: Mapping[str, Any], today: str) -> set[str]:
    """Return the models an earlier pass today saw in a complete list.

    Carried in `refresh.json` beside `unmatched` rather than in
    `lifecycle.json`: it is what the passes of one day saw, and says nothing
    about a model once the day is over.
    """

    present = previous.get("present")
    if not isinstance(present, dict) or present.get("day") != today:
        return set()
    models = present.get("models")
    return {str(model) for model in models} if isinstance(models, list) else set()


def journal(
    data_dir: Path, days: int, *, now: datetime | None = None
) -> dict[str, Any]:
    """Return the last pass's outcomes, the journal rows of the last *days* days, and every removal.

    Reads and writes nothing else: `/model-selector status` shows this, and a
    report that moved a marker would change what the next report says. A
    removal is shown for as long as `lifecycle.json` records it, however old,
    with the rows and Units deleted for it so far, since later passes go on
    deleting what capture files for it.
    """

    until = (now or datetime.now(UTC)).astimezone(UTC)
    since = until - timedelta(days=days)
    last: Any = None
    problem: str | None = None
    path = data_dir / PASS_FILE
    try:
        last = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        last = None
    except (OSError, ValueError) as failure:
        problem = f"{path} could not be read: {failure}"

    rows: list[dict[str, Any]] = []
    try:
        lines = (data_dir / JOURNAL_FILE).read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        at = _parsed_instant(row.get("at")) if isinstance(row, dict) else None
        if at is not None and since <= at <= until:
            rows.append(row)

    return {
        "days": days,
        "last_pass": last if isinstance(last, dict) else None,
        "problem": problem,
        "journal": rows,
        "removed": [
            {
                "model": identifier,
                "absent_days": record.get("absent_days"),
                "removed_at": record.get("removed_at"),
                "rows_deleted": record.get("rows_deleted", 0),
                "units_dropped": record.get("units_dropped", 0),
            }
            for identifier, record in sorted(_lifecycle(data_dir).items())
            if _is_removal(record)
        ],
    }


class _Pass:
    """The working state of one pass: the entries it is changing and what it said.

    Every change goes through `set`, which is where the journal row is made,
    so a field that moved and a row that says so cannot come apart. A model
    this pass added journals only its `model` row, and its `no price source`
    row where OpenRouter was read and had no match.
    """

    def __init__(
        self,
        known: dict[str, dict[str, Any]],
        makers: frozenset[str],
        stamp: str,
        today: str,
        unmatched_before: frozenset[str],
    ) -> None:
        self.known = known
        self.entries = {identifier: dict(entry) for identifier, entry in known.items()}
        self.makers = makers
        self.stamp = stamp
        self.today = today
        self.unmatched_before = unmatched_before
        self.unmatched: set[str] = set()
        self.added: set[str] = set()
        self.rows: list[dict[str, Any]] = []

    def note(
        self,
        source: str,
        model: str,
        field: str,
        old: Any,
        new: Any,
        note: str | None = None,
    ) -> None:
        """Journal one change, unless it is a field of a model this pass added."""

        if model in self.added and field != "model" and note is None:
            return
        row: dict[str, Any] = {
            "at": self.stamp,
            "source": source,
            "model": model,
            "field": field,
            "old": old,
            "new": new,
        }
        if note is not None:
            row["note"] = note
        self.rows.append(row)

    def set(self, source: str, model: str, field: str, value: Any) -> None:
        """Set one field, journalling it where the value actually moved."""

        entry = self.entries[model]
        if _same(field, entry.get(field), value):
            return
        self.note(source, model, field, entry.get(field), value)
        entry[field] = value

    def add(self, source: str, entry: dict[str, Any]) -> None:
        """Enter a model the catalogue lacked, and journal that it came."""

        self.entries[entry["id"]] = entry
        self.added.add(entry["id"])
        self.note(source, entry["id"], "model", None, entry["id"])

    def listed(self, source: str, reading: Reading) -> None:
        """Add or update every model one harness list offers for its maker."""

        maker = HARNESS_MAKERS[source]
        if maker not in self.makers:
            return
        for offer in reading.listed:
            if offer.id not in self.entries:
                self.add(source, _new_entry(offer, source, self.today))
                continue
            entry = self.entries[offer.id]
            if entry.get("provider") != maker:
                continue
            held = list(entry.get("aliases") or [])
            merged = held + [alias for alias in offer.aliases if alias not in held]
            self.set(source, offer.id, "aliases", merged)
            if offer.levels is not None:
                self.set(source, offer.id, "deliberation", list(offer.levels))

    def offered_through_gateway(self, reading: Reading) -> None:
        """Add or update every standard Grok model OpenRouter lists with a level control."""

        prefix = OPENROUTER_PREFIXES[GATEWAY_MAKER]
        for entry in reading.entries:
            slug = str(entry["id"])
            if (
                not slug.startswith(prefix)
                or ":" in slug
                or slug.endswith("-multi-agent")
            ):
                continue
            levels = _openrouter_levels(entry)
            if not levels:
                continue
            identifier = slug[len(prefix) :]
            if identifier not in self.entries:
                self.add(
                    "openrouter",
                    {
                        **dict.fromkeys(MODEL_FIELDS),
                        "id": identifier,
                        "provider": GATEWAY_MAKER,
                        "family": "grok",
                        "aliases": [],
                        "deliberation": list(levels),
                        "reasoning_billed_as": "output",
                        "gateways": {"openrouter": slug},
                        "source_url": f"https://openrouter.ai/{slug}",
                        "retrieved": self.today,
                    },
                )
                continue
            if self.entries[identifier].get("provider") == GATEWAY_MAKER:
                self.set("openrouter", identifier, "deliberation", list(levels))

    def priced(self, reading: Reading) -> None:
        """Price every model of a chosen maker that matches an OpenRouter entry."""

        every = {str(entry["id"]): entry for entry in reading.entries}
        standard = {slug: entry for slug, entry in every.items() if ":" not in slug}
        for identifier, entry in self.entries.items():
            if entry.get("provider") not in self.makers:
                continue
            held = entry.get("gateways")
            written = _text(held.get("openrouter")) if isinstance(held, dict) else None
            slug = written or openrouter_slug(str(entry.get("provider")), identifier)
            match = (every if written else standard).get(slug or "")
            if slug is None or match is None:
                self.unpriced(identifier)
                continue
            self.matched(identifier, slug, match)

    def unpriced(self, identifier: str) -> None:
        """Record a model with no OpenRouter entry, journalling only the change of state."""

        entry = self.entries[identifier]
        self.unmatched.add(identifier)
        if identifier in self.added:
            entry["released"] = entry.get("released") or self.today
        if identifier not in self.unmatched_before:
            price = entry.get("price")
            self.note("openrouter", identifier, "price", price, price, NO_PRICE_SOURCE)

    def matched(self, identifier: str, slug: str, match: Mapping[str, Any]) -> None:
        """Take price, threshold, release date and slug from one OpenRouter entry."""

        entry = self.entries[identifier]
        gateways = dict(entry.get("gateways") or {})
        if gateways.get("openrouter") != slug:
            self.set(
                "openrouter", identifier, "gateways", {**gateways, "openrouter": slug}
            )

        listed = match.get("pricing")
        pricing: Mapping[str, Any] = listed if isinstance(listed, dict) else {}
        base = _openrouter_card(pricing, entry.get("price"))
        self.set("openrouter", identifier, "price", base)

        override = next(
            (
                item
                for item in pricing.get("overrides") or []
                if isinstance(item, dict)
                and _whole(item.get("min_prompt_tokens")) is not None
            ),
            None,
        )
        if override is not None:
            self.set(
                "openrouter",
                identifier,
                "long_context_threshold",
                _whole(override["min_prompt_tokens"]),
            )
            self.set(
                "openrouter",
                identifier,
                "long_context",
                _openrouter_card(override, base),
            )

        created = _whole(match.get("created"))
        if entry.get("released") is None and created is not None:
            self.set(
                "openrouter",
                identifier,
                "released",
                datetime.fromtimestamp(created, UTC).date().isoformat(),
            )

        entry["source_url"] = f"https://openrouter.ai/{slug}"
        entry["retrieved"] = self.today

    def settled(self) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
        """Return every entry this pass changed that the validator accepts, and what it refused.

        A refused entry keeps what it had, and the rows about it are withdrawn,
        a change that did not happen being no change to journal.
        """

        changed: dict[str, dict[str, Any]] = {}
        discarded: list[dict[str, str]] = []
        for identifier, entry in self.entries.items():
            if entry == self.known.get(identifier):
                continue
            fault = _model_fault(entry)
            if fault is None and _model(entry) is None:
                fault = "names no provider and family"
            if fault is not None:
                discarded.append({"model": identifier, "reason": fault})
                self.rows = [row for row in self.rows if row["model"] != identifier]
                continue
            changed[identifier] = entry
        return changed, discarded


class _Exchange:
    """One newline-delimited JSON conversation with a harness over its stdio.

    The process runs in a group of its own, and leaving the block kills that
    group, so a harness that goes on waiting — for a login, for a prompt that
    never comes — outlives neither the exchange nor its deadline.
    """

    def __init__(self, argv: Sequence[str]) -> None:
        self._deadline = time.monotonic() + EXCHANGE_SECONDS
        self._buffer = b""
        # The home directory, which nothing in this collection removes; the
        # exchange itself reads and writes nothing there.
        self._process = subprocess.Popen(
            list(argv),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=_quiet_directory(),
            start_new_session=True,
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *raised: object) -> None:
        self.close()

    def send(self, message: Mapping[str, Any]) -> None:
        """Write one message as one line."""

        stream = self._process.stdin
        assert stream is not None
        stream.write((json.dumps(message) + "\n").encode("utf-8"))
        stream.flush()

    def receive(self, wanted: Callable[[dict[str, Any]], bool]) -> dict[str, Any]:
        """Return the first message *wanted* accepts, skipping every other line."""

        while True:
            line = self._line()
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if isinstance(message, dict) and wanted(message):
                return message

    def _line(self) -> bytes:
        stream = self._process.stdout
        assert stream is not None
        while b"\n" not in self._buffer:
            left = self._deadline - time.monotonic()
            if left <= 0:
                raise TimeoutError
            ready, _, _ = select.select([stream], [], [], left)
            if not ready:
                raise TimeoutError
            chunk = os.read(stream.fileno(), 1 << 16)
            if not chunk:
                raise EOFError("the harness closed its output")
            self._buffer += chunk
        line, _, self._buffer = self._buffer.partition(b"\n")
        return line

    def close(self) -> None:
        """Stop the harness and everything it started."""

        for signal_number in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(self._process.pid, signal_number)
            except ProcessLookupError:
                break
            try:
                self._process.wait(timeout=2)
                break
            except subprocess.TimeoutExpired:
                continue
        for stream in (self._process.stdin, self._process.stdout):
            if stream is not None:
                stream.close()


def _consult(
    reader: Callable[[datetime], Reading] | None, source: str, started: datetime
) -> Reading:
    """Run one reader, turning any failure of its own into an unreadable source."""

    if reader is None:
        return unreadable(source, "no reader is wired for this source")
    try:
        return reader(started)
    except Exception as failure:  # noqa: BLE001 - one source failing must not cost the other two
        return unreadable(source, f"the reader failed: {failure!r}")


def _new_entry(offer: Offer, source: str, today: str) -> dict[str, Any]:
    """Return the complete record of a model a harness list established.

    Attributed to that list's own documentation until OpenRouter matches it,
    unpriced, and with no capability: that is a seeded prior and nothing here
    seeds it.
    """

    return {
        **dict.fromkeys(MODEL_FIELDS),
        "id": offer.id,
        "provider": offer.provider,
        "family": offer.family,
        "aliases": list(offer.aliases),
        "deliberation": list(offer.levels or ()),
        "reasoning_billed_as": "output",
        "gateways": {},
        "source_url": HARNESS_DOCS[source],
        "retrieved": today,
    }


def _openrouter_card(pricing: Mapping[str, Any], standing: Any) -> dict[str, Any]:
    """Return a rate card from OpenRouter's per-token prices, over *standing*.

    A category OpenRouter omits keeps what *standing* has, so a partial
    listing never costs the catalogue a figure. A price that will not convert
    is carried as given, for the validator to refuse by name.
    """

    held = standing if isinstance(standing, dict) else {}
    card: dict[str, Any] = {category: held.get(category) for category in PRICED}
    for theirs, ours in OPENROUTER_CATEGORIES:
        raw = pricing.get(theirs)
        if raw is None:
            continue
        converted = per_million(raw)
        card[ours] = raw if converted is None else converted
    card["currency"] = CURRENCY
    card["unit"] = UNIT
    return card


def _openrouter_levels(entry: Mapping[str, Any]) -> tuple[str, ...]:
    """Return the ladder levels an OpenRouter entry's reasoning block supports."""

    reasoning = entry.get("reasoning")
    efforts = (
        reasoning.get("supported_efforts") if isinstance(reasoning, dict) else None
    )
    return _levels(efforts) or ()


def _levels(raw: Any) -> tuple[str, ...] | None:
    """Return the ladder levels a list names, in ladder order, or None for no list.

    A level off the ladder — Codex's `ultra`, OpenRouter's `none` — is dropped
    rather than refused, since the list is the harness's and not the catalogue's.
    """

    if not isinstance(raw, list):
        return None
    named = {item for item in raw if isinstance(item, str)}
    return tuple(level for level in LEVELS if level in named)


def _gpt_family(identifier: str) -> str:
    """Return a GPT model's family: its last segment where alphabetic, else the id."""

    head, _, last = identifier.rpartition("-")
    return last if head and last.isalpha() else identifier


def _unbracketed(name: str) -> str:
    """Return a Claude model name without a bracketed serving selector such as `[1m]`."""

    return re.sub(r"\[[^\]]*\]$", "", name)


def _stale(fetched_at: str | None, started: datetime) -> str | None:
    """Return why a Codex list came from its bundled fallback, or None where it is fresh."""

    fetched = _parsed_instant(fetched_at)
    if fetched is None:
        return "Codex's models cache carries no readable fetched_at, so the list is its bundled one"
    if fetched < started - timedelta(seconds=CODEX_CACHE_TTL):
        return (
            f"Codex's models cache was fetched_at {fetched_at}, more than "
            f"{CODEX_CACHE_TTL} seconds before the pass, so the list is its bundled one"
        )
    return None


def _codex_fetched_at() -> str | None:
    """Return the `fetched_at` of the models cache in the `CODEX_HOME` Codex used."""

    named = os.environ.get("CODEX_HOME")
    try:
        home = Path(named) if named else Path.home() / ".codex"
        raw = json.loads((home / CODEX_CACHE_FILE).read_text(encoding="utf-8"))
    except (RuntimeError, OSError, ValueError):
        return None
    return _text(raw.get("fetched_at")) if isinstance(raw, dict) else None


def _fetch(url: str) -> bytes:
    """GET one OpenRouter page, unauthenticated, within the exchange deadline."""

    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "kntnt-model-selector"},
    )
    with urllib.request.urlopen(request, timeout=EXCHANGE_SECONDS) as response:
        body: bytes = response.read()
    return body


def _quiet_directory() -> Path:
    """Return the working directory an exchange is started in."""

    try:
        return Path.home()
    except RuntimeError:
        return Path(tempfile.gettempdir())


def _same(field: str, old: Any, new: Any) -> bool:
    """Return whether two values of *field* are the same fact.

    Rate cards compare category by category at six places, so a float read
    back from JSON never differs from the Decimal it was rounded from.
    """

    if field in ("price", "long_context"):
        return bool(_rounded_card(old) == _rounded_card(new))
    return bool(old == new)


def _rounded_card(card: Any) -> Any:
    """Return a rate card with every number at six places, for comparison."""

    if not isinstance(card, dict):
        return card
    return {
        key: float(Decimal(repr(value)).quantize(_PLACES))
        if isinstance(value, float | int)
        and not isinstance(value, bool)
        and math.isfinite(value)
        else value
        for key, value in card.items()
    }


def _whole(raw: Any) -> int | None:
    """Return a whole number, or None for anything else."""

    if (
        isinstance(raw, bool)
        or not isinstance(raw, (int, float))
        or not math.isfinite(raw)
    ):
        return None
    return int(raw)


def _instant(moment: datetime) -> str:
    """Return a UTC instant the way this Skill stamps what it wrote."""

    return moment.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parsed_instant(raw: Any) -> datetime | None:
    """Return an ISO instant as an aware UTC datetime, or None."""

    if not isinstance(raw, str):
        return None
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return (
        parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)
    )


def _last_pass(path: Path) -> dict[str, Any]:
    """Return what the previous pass wrote, or nothing where there is none."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return raw if isinstance(raw, dict) else {}


def _replace_json(path: Path, document: Mapping[str, Any]) -> None:
    """Write one JSON document whole, through a sibling and an atomic rename."""

    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.parent / f"{path.name}.tmp"
    staged.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    staged.replace(path)


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


def _agents(named: str | None) -> Path:
    """Return the agents directory a pass resyncs, Claude Code's own by default.

    The default is for a person or a scheduler running the pass; a test names
    a directory of its own.
    """

    if named:
        return Path(named).expanduser()
    try:
        return Path.home() / ".claude" / "agents"
    except RuntimeError:
        return Path.cwd() / ".claude" / "agents"


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
    parser.add_argument("action", nargs="*", metavar="adopt <path> | refresh | journal")
    parser.add_argument("--data", default=str(default_data()))
    parser.add_argument("--agents")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    data_dir = Path(args.data).expanduser()
    here = Path(__file__).resolve().parent.parent
    if not args.action:
        _emit(_document(load(data_dir, here)))
        return 0

    if args.action == ["refresh"]:
        _emit(refresh(data_dir, here, _agents(args.agents)))
        return 0
    if args.action == ["journal"]:
        _emit(journal(data_dir, args.days))
        return 0

    if len(args.action) != 2 or args.action[0] != "adopt":
        parser.error(
            "the verbs beside the bare form are `adopt <path>`, `refresh` and `journal`"
        )

    report = adopt(data_dir, here, Path(args.action[1]).expanduser())
    _emit(report)
    return 1 if report["refused"] else 0


if __name__ == "__main__":
    sys.exit(main())
