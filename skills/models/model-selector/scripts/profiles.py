# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""What this machine can reach, and who pays for it.

The catalogue knows every model in the world; this module knows the far
smaller set the person in front of the machine actually has. That set is
answered once, by `/model-selector setup`, and stored as `profile.json` under
the data directory — which means it is also a file a person can hand-edit into
something unreadable at three in the morning.

So a broken profile is not an error here. It is a fallback: every harness this
machine looks like it has, every provider and model the catalogue knows, no
channels, and a `problem` that names both what went wrong and the verb that
fixes it. A caller mid-task gets a worse answer instead of no answer, and the
person gets told once, by whoever reports the problem, rather than by a
traceback in the middle of somebody else's build.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from catalogue import Catalogue, Model

PROFILE_FILE = "profile.json"

# How a channel is paid for. Anything else in the file is not a channel this
# Skill can reason about, so the profile carrying it is treated as invalid.
PAYMENTS = ("subscription", "api")

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


@dataclass(frozen=True)
class Channel:
    """One way of paying one provider on one harness."""

    provider: str
    harness: str
    pay: str
    plan: str | None
    tier: str | None
    monthly: float | None
    currency: str | None
    gateway: str | None


@dataclass(frozen=True)
class Profile:
    """The user's own answers, or the fallback standing in for them."""

    harnesses: tuple[str, ...]
    providers: tuple[str, ...]
    models: tuple[str, ...]
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
    """Read the stored profile, falling back rather than failing.

    Every way the file can disappoint — absent, unreadable, not an object,
    missing a list this Skill routes by — lands in the same place: the widest
    profile the catalogue supports, marked as a fallback and carrying why.
    """

    path = data_dir / PROFILE_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return _fallback(cat, f"no profile at {path}; {REPAIR}")
    except (OSError, ValueError) as problem:
        return _fallback(cat, f"{path} could not be read: {problem}; {REPAIR}")

    if not isinstance(raw, dict):
        return _fallback(cat, f"{path} is not a JSON object; {REPAIR}")

    harnesses = _names(raw.get("harnesses"))
    providers = _names(raw.get("providers"))
    models = _names(raw.get("models"))
    if harnesses is None or providers is None or models is None:
        return _fallback(
            cat, f"{path} is missing harnesses, providers or models; {REPAIR}"
        )

    channels = _channels(raw.get("channels"))
    if channels is None:
        return _fallback(
            cat, f"{path} carries a channel this Skill cannot read; {REPAIR}"
        )

    return Profile(
        harnesses=harnesses,
        providers=providers,
        models=models,
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

    The file names what somebody pays every month, so it is written 0600, and
    it is replaced rather than truncated so that an interrupted write leaves
    the previous answers standing instead of half of the new ones.
    """

    data_dir.mkdir(parents=True, exist_ok=True)
    handle, staged = tempfile.mkstemp(dir=data_dir, prefix=".profile-", suffix=".json")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(_document(p), stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.chmod(staged, 0o600)
        os.replace(staged, data_dir / PROFILE_FILE)
    except OSError:
        Path(staged).unlink(missing_ok=True)
        raise


def _document(p: Profile) -> dict[str, Any]:
    """Return the profile as the JSON object `load` reads back."""

    return {
        "harnesses": list(p.harnesses),
        "providers": list(p.providers),
        "models": list(p.models),
        "channels": [
            {
                "provider": channel.provider,
                "harness": channel.harness,
                "pay": channel.pay,
                "plan": channel.plan,
                "tier": channel.tier,
                "monthly": channel.monthly,
                "currency": channel.currency,
                "gateway": channel.gateway,
            }
            for channel in p.channels
        ],
        "answered_at": p.answered_at,
    }


def _fallback(cat: Catalogue, problem: str) -> Profile:
    """Return the widest profile the catalogue supports, marked as a fallback."""

    providers = dict.fromkeys(model.provider for model in cat.models)
    return Profile(
        harnesses=tuple(detect_harnesses()),
        providers=tuple(providers),
        models=tuple(model.id for model in cat.models),
        channels=(),
        answered_at=None,
        source="fallback",
        problem=problem,
    )


def _names(raw: Any) -> tuple[str, ...] | None:
    """Return a list of names as a tuple, or None where it is not one."""

    if not isinstance(raw, list):
        return None
    names = [item for item in raw if isinstance(item, str) and item.strip()]
    if len(names) != len(raw):
        return None
    return tuple(names)


def _channels(raw: Any) -> tuple[Channel, ...] | None:
    """Return the channels, or None where any of them is unreadable.

    A profile is only worth trusting whole. One channel this Skill cannot read
    is a file somebody edited by hand and got wrong, so the answer is the
    fallback rather than a silently shortened list of ways to pay.
    """

    if raw is None:
        return ()
    if not isinstance(raw, list):
        return None

    channels: list[Channel] = []
    for entry in raw:
        if not isinstance(entry, dict):
            return None
        provider = _text(entry.get("provider"))
        harness = _text(entry.get("harness"))
        pay = _text(entry.get("pay"))
        if provider is None or harness is None or pay not in PAYMENTS:
            return None
        channels.append(
            Channel(
                provider=provider,
                harness=harness,
                pay=pay,
                plan=_text(entry.get("plan")),
                tier=_text(entry.get("tier")),
                monthly=_number(entry.get("monthly")),
                currency=_text(entry.get("currency")),
                gateway=_text(entry.get("gateway")),
            )
        )
    return tuple(channels)


def _text(raw: Any) -> str | None:
    """Return a non-empty string, or None for anything else including null."""

    return raw if isinstance(raw, str) and raw.strip() else None


def _number(raw: Any) -> float | None:
    """Return a float, or None for anything that is not a number."""

    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    return float(raw)
