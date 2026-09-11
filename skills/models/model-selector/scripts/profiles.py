# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Whose models this machine may be sent to, and who pays for them.

The catalogue knows every model in the world; this module knows which makers
the person in front of the machine wants models from, and how they pay for
each. Every model a chosen maker offers is then eligible, a model the catalogue
gains later included, and no single model is chosen or left out within a maker
(ADR-0190). The answers are given once, by `/model-selector setup`, and stored
as `profile.json` under the data directory — which means it is also a file a
person can hand-edit into something unreadable at three in the morning.

So a broken profile is not an error here. It is a stand-in: every harness this
machine looks like it has, no maker, no channels, and a `problem` that names
both what went wrong and the verb that fixes it. With no maker chosen nothing
is eligible, so a caller mid-task gets its own seat back instead of no answer —
never the whole catalogue, a pool nobody chose — and the person gets told
once, by whoever reports the problem, rather than by a traceback in the middle
of somebody else's build. A profile an older release wrote, with a list of
models and no makers, is read the same way rather than translated.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from catalogue import CURRENCY, UNIT, Catalogue, Model, Price

PROFILE_FILE = "profile.json"

# Where the user's standing choice between time and cost is kept. Beside the
# profile rather than inside it: `write` replaces the profile whole on every
# `setup`, which would drop it, and a profile holding nothing but an objective
# is not one `load` can read.
OBJECTIVE_FILE = "objective.json"

# What finishing the work is counted in. Money is what a run spends whether or
# not anybody is watching it; time is what the person waiting on it spends
# instead, and asking for one is not the same as asking for the other.
OBJECTIVES = ("cost", "time")

# How a channel is paid for. Anything else in the file is not a channel this
# Skill can reason about, so the profile carrying it is treated as invalid.
PAYMENTS = ("subscription", "api")

# The two lists a profile carried before makers replaced them. Found beside
# `makers`, they are a file written half by an older release or edited by hand,
# and a profile is only worth trusting whole.
RETIRED = ("providers", "models")

# The directory each harness leaves in a home directory, and the name this
# Skill knows that harness by. Probes only: no process is started and no
# network is touched, because detection runs inside somebody else's turn.
HARNESS_MARKERS = (
    (Path(".claude"), "claude-code"),
    (Path(".codex"), "codex"),
    (Path(".config") / "opencode", "opencode"),
)

# What a person has to run to replace a fallback with real answers. Named in
# every `problem` this module writes, because a diagnosis without the verb
# that fixes it is a diagnosis nobody acts on.
REPAIR = "run `/model-selector setup` to answer these questions again"

# What `_rates` answers with where a card is present and unusable, which is
# neither a card nor the absence of one. A sentinel rather than an exception,
# because nothing in this module raises at a caller mid-task.
_UNREADABLE = Price(None, None, None, None, "", "")


@dataclass(frozen=True)
class Channel:
    """One way of paying one provider on one harness.

    `plan` is the subscription under the whole name the provider markets it
    by — `Claude Max 20x`, not a product and a level in two fields. There is
    nothing here for what the plan costs per month: that is a fetched fact the
    catalogue holds, and a copy of it in somebody's answers is a second thing
    to keep true that no decision ever reads.

    `rates` is what the user pays per token on this channel, where they pay
    per token at all. The catalogue holds one list price per model from the
    provider's own page, which is the wrong bill for a gateway — and a gateway
    is exactly the arrangement that has nowhere else to be recorded.
    """

    provider: str
    harness: str
    pay: str
    plan: str | None
    gateway: str | None
    rates: Price | None


@dataclass(frozen=True)
class Profile:
    """The user's own answers, or the stand-in that chooses nothing for them.

    `makers` are catalogue provider ids — `anthropic`, `openai`, `spacexai` —
    and every model a chosen maker offers is eligible. The stand-in's `source`
    is `fallback` and it chooses none.
    """

    harnesses: tuple[str, ...]
    makers: tuple[str, ...]
    channels: tuple[Channel, ...]
    answered_at: str | None
    source: str
    problem: str | None


def detect_harnesses() -> list[str]:
    """Return the harnesses this machine looks like it has, sorted.

    Filesystem probes and nothing else. A machine with no home directory at
    all detects nothing rather than raising, because this runs inside a turn
    that belongs to somebody else's work.
    """

    try:
        home = Path.home()
    except RuntimeError:
        return []

    found = {name for marker, name in HARNESS_MARKERS if (home / marker).is_dir()}
    return sorted(found)


def load(data_dir: Path, cat: Catalogue) -> Profile:
    """Read the stored profile, standing in for it rather than failing.

    Every way the file can disappoint — absent, unreadable, not an object, in
    the shape an older release wrote, or naming a maker or a channel this
    Skill cannot route by — lands in the same place: a stand-in choosing no
    maker, marked as a fallback and carrying why.
    """

    path = data_dir / PROFILE_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return _fallback(f"no profile at {path}; {REPAIR}")
    except (OSError, ValueError) as problem:
        return _fallback(f"{path} could not be read: {problem}; {REPAIR}")

    if not isinstance(raw, dict):
        return _fallback(f"{path} is not a JSON object; {REPAIR}")

    if "makers" not in raw:
        return _fallback(
            f"{path} is from before makers were chosen and names none; {REPAIR}"
        )

    harnesses = _names(raw.get("harnesses"))
    makers = _names(raw.get("makers"))
    if harnesses is None or makers is None:
        return _fallback(f"{path} is missing harnesses or makers; {REPAIR}")

    unreadable = _unchoosable(raw, makers, cat)
    if unreadable is not None:
        return _fallback(f"{path} {unreadable}; {REPAIR}")

    channels, unreadable = _channels(raw.get("channels"))
    if channels is None:
        return _fallback(f"{path} {unreadable}; {REPAIR}")

    return Profile(
        harnesses=harnesses,
        makers=tuple(dict.fromkeys(makers)),
        channels=channels,
        answered_at=_text(raw.get("answered_at")),
        source="file",
        problem=None,
    )


def channel_for(p: Profile, model: Model, harness: str) -> Channel | None:
    """Return the channel that pays for *model*, preferring *harness*'s own.

    The harness a channel names is the one the model is reached through, and
    that is frequently not the harness doing the asking: a Claude Code session
    reaches an OpenAI model by running the Codex CLI, and it is the Codex
    subscription that pays for those tokens. Matching on the asking harness
    alone therefore said no provider was payable outside the seat's own, which
    silently removed every bridged model from the pool the moment a profile
    existed — and made an answered interview worse than none.

    So the exact harness wins where the profile has one, because that is where
    the two arrangements differ when a provider is reached two ways at once,
    and any channel for the provider answers where it has not. A profile with
    no channel at all for a point is not a profile that forbids it; it is one
    that cannot say what the point costs to reach, which is a judgement the
    caller makes rather than this lookup.
    """

    for channel in p.channels:
        if channel.provider == model.provider and channel.harness == harness:
            return channel
    for channel in p.channels:
        if channel.provider == model.provider:
            return channel
    return None


def write(data_dir: Path, p: Profile) -> None:
    """Store the profile atomically, readable only by its owner.

    The file names what somebody pays for their tokens, so it is written 0600,
    and it is replaced rather than truncated so that an interrupted write
    leaves the previous answers standing instead of half of the new ones.
    """

    _replace(data_dir, PROFILE_FILE, _document(p))


def standing_objective(data_dir: Path) -> tuple[str | None, str | None]:
    """Return the objective the user set, and why it could not be read.

    Both are None where nothing is set. A file that is there and cannot be
    read, or that names a word other than one of `OBJECTIVES`, answers None
    with the reason: whoever reads it treats it as absent and says so, because
    a standing choice is a preference and never a reason to refuse a call.
    """

    path = data_dir / OBJECTIVE_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, None
    except (OSError, ValueError) as problem:
        return None, f"the standing objective at {path} cannot be read ({problem})"

    held = raw.get("objective") if isinstance(raw, dict) else None
    if held not in OBJECTIVES:
        return None, (
            f"the standing objective at {path} names neither "
            f"{' nor '.join(OBJECTIVES)}, so it cannot be read"
        )
    return str(held), None


def write_objective(data_dir: Path, objective: str) -> Path:
    """Store the user's standing objective atomically, and nothing beside it."""

    return _replace(data_dir, OBJECTIVE_FILE, {"objective": objective})


def _replace(data_dir: Path, name: str, document: dict[str, Any]) -> Path:
    """Write one of the user's answer files whole, readable only by its owner."""

    data_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(name).stem
    handle, staged = tempfile.mkstemp(dir=data_dir, prefix=f".{stem}-", suffix=".json")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.chmod(staged, 0o600)
        os.replace(staged, data_dir / name)
    except OSError:
        Path(staged).unlink(missing_ok=True)
        raise
    return data_dir / name


def _document(p: Profile) -> dict[str, Any]:
    """Return the profile as the JSON object `load` reads back."""

    return {
        "harnesses": list(p.harnesses),
        "makers": list(p.makers),
        "channels": [
            {
                "provider": channel.provider,
                "harness": channel.harness,
                "pay": channel.pay,
                "plan": channel.plan,
                "gateway": channel.gateway,
                "rates": _card(channel.rates),
            }
            for channel in p.channels
        ],
        "answered_at": p.answered_at,
    }


def _fallback(problem: str) -> Profile:
    """Return the stand-in for answers nobody gave: no maker, and no channel.

    With no maker chosen nothing is eligible, so every call not locked to a
    model inherits the caller's own seat and says why. The whole catalogue is
    what this used to stand in with, and that is a pool nobody chose.
    """

    return Profile(
        harnesses=tuple(detect_harnesses()),
        makers=(),
        channels=(),
        answered_at=None,
        source="fallback",
        problem=problem,
    )


def _unchoosable(
    raw: dict[str, Any], makers: tuple[str, ...], cat: Catalogue
) -> str | None:
    """Say why the makers cannot be trusted, or None where they can.

    None chosen is a choice nothing answers, a maker the catalogue holds no
    model of is a typo, and a list the makers replaced still standing beside
    them is a file written half by an older release.
    """

    leftover = [field for field in RETIRED if field in raw]
    if leftover:
        return f"carries {' and '.join(leftover)} beside makers, which replaced them"
    if not makers:
        return "chooses no maker"
    known = {model.provider for model in cat.models}
    unknown = [name for name in makers if name not in known]
    if unknown:
        return (
            f"chooses {', '.join(repr(name) for name in unknown)}, "
            "which the catalogue holds no model of"
        )
    return None


def _names(raw: Any) -> tuple[str, ...] | None:
    """Return a list of names as a tuple, or None where it is not one."""

    if not isinstance(raw, list):
        return None
    names = [item for item in raw if isinstance(item, str) and item.strip()]
    if len(names) != len(raw):
        return None
    return tuple(names)


def _channels(raw: Any) -> tuple[tuple[Channel, ...] | None, str | None]:
    """Return the channels, or None and why none of them can be trusted.

    A profile is only worth trusting whole. One channel this Skill cannot read
    is a file somebody edited by hand and got wrong, so the answer is the
    stand-in rather than a silently shortened list of ways to pay.

    The reason travels with the refusal because it is the only thing anybody
    can act on: *a rate card in SEK* names the edit to make, where *a channel
    this Skill cannot read* sends somebody through the whole file looking.
    """

    if raw is None:
        return (), None
    if not isinstance(raw, list):
        return None, "carries a channels member that is not a list"

    channels: list[Channel] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            return None, f"carries a channel {index} that is not an object"
        provider = _text(entry.get("provider"))
        harness = _text(entry.get("harness"))
        pay = _text(entry.get("pay"))
        if provider is None or harness is None or pay not in PAYMENTS:
            return (
                None,
                f"carries a channel {index} that names no provider, no harness, or no way of paying",
            )
        rates = _rates(entry.get("rates"))
        if rates is _UNREADABLE:
            return (
                None,
                f"carries a rate card on channel {index} that is not a readable card in {CURRENCY} {UNIT}",
            )
        channels.append(
            Channel(
                provider=provider,
                harness=harness,
                pay=pay,
                plan=_text(entry.get("plan")),
                gateway=_text(entry.get("gateway")),
                rates=rates,
            )
        )
    return tuple(channels), None


def _rates(raw: Any) -> Price | None:
    """Return the channel's own rate card, absent, or the marker for unusable.

    Every figure this Skill compares is USD and nothing anywhere converts, so
    a card in another currency would be added to a USD bill without a word
    said. That is worse than the stand-in, which at least announces itself, so
    it joins the states that invalidate a profile rather than the ones that
    are quietly dropped.
    """

    if raw is None:
        return None
    if not isinstance(raw, dict):
        return _UNREADABLE

    card = Price(
        input=_number(raw.get("input")),
        cache_read=_number(raw.get("cache_read")),
        cache_write=_number(raw.get("cache_write")),
        output=_number(raw.get("output")),
        currency=_text(raw.get("currency")) or CURRENCY,
        unit=_text(raw.get("unit")) or UNIT,
    )
    if card.currency != CURRENCY or card.unit != UNIT:
        return _UNREADABLE
    return card


def _card(rates: Price | None) -> dict[str, Any] | None:
    """Return one channel's rate card as the JSON object `load` reads back."""

    if rates is None:
        return None
    return {
        "input": rates.input,
        "cache_read": rates.cache_read,
        "cache_write": rates.cache_write,
        "output": rates.output,
        "currency": rates.currency,
        "unit": rates.unit,
    }


def _text(raw: Any) -> str | None:
    """Return a non-empty string, or None for anything else including null."""

    return raw if isinstance(raw, str) and raw.strip() else None


def _number(raw: Any) -> float | None:
    """Return a float, or None for anything that is not a number."""

    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    return float(raw)
