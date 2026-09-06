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
person checked this week outranks a fact this repository froze at release.

Nothing here raises. A catalogue that cannot be read is a catalogue that says
so in `problem` and hands back what it still has, because every caller of this
module is answering a question for a machine that is already mid-task, and a
traceback there costs the caller its work rather than merely its accuracy.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
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
class Model:
    """One point the Skill can send work to, with everything known about it."""

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
    provider_says: str | None
    released: str | None
    source_url: str | None
    retrieved: str | None


@dataclass(frozen=True)
class Catalogue:
    """Every known model, and why the answer might be thinner than it looks."""

    models: tuple[Model, ...]
    generated_at: str
    problem: str | None


def load(data_dir: Path, here: Path) -> Catalogue:
    """Merge the shipped seed with the refreshed file, the refreshed one winning.

    A missing or unreadable refreshed file leaves the seed standing and is
    reported in `problem`; only a seed that will not parse empties the answer,
    because at that point the Skill knows nothing at all about the world.
    """

    # The seed is the floor. Without it there is no catalogue to merge into.
    seed, seed_generated, seed_problem = _read(here / "data" / SEED_FILE)
    if seed_problem is not None:
        return Catalogue((), "", seed_problem)

    # The refreshed file overrides model by model, so a partial refresh is
    # additive rather than a replacement of everything the seed knew.
    refreshed, refreshed_generated, refresh_problem = _read(data_dir / REFRESHED_FILE)
    merged: dict[str, Model] = {model.id: model for model in seed}
    for model in refreshed:
        merged[model.id] = model

    generated_at = refreshed_generated or seed_generated
    return Catalogue(tuple(merged.values()), generated_at, refresh_problem)


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
    model: Model, tokens: Mapping[str, float | None], kind: str, rule: ContextRule
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
    """

    price = _card(model, kind, rule)
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


def _read(path: Path) -> tuple[list[Model], str, str | None]:
    """Read one catalogue file into models, its stamp, and what went wrong."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], "", f"no catalogue at {path}"
    except (OSError, ValueError) as problem:
        return [], "", f"{path} could not be read: {problem}"

    if not isinstance(raw, dict):
        return [], "", f"{path} is not a JSON object"

    entries = raw.get("models")
    if not isinstance(entries, list):
        return [], "", f"{path} carries no models list"

    models = [model for entry in entries if (model := _model(entry)) is not None]
    return models, _text(raw.get("generated_at")) or "", None


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
        currency=_text(raw.get("currency")) or "USD",
        unit=_text(raw.get("unit")) or "per_mtok",
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
