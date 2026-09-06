# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Write the answers `setup` gathered, and make the machine able to act on them.

The interview belongs to the conversation: only a person can say which
harnesses they use, which providers they pay, and how. This is the other half
of it — the half that has to be a script, because writing a profile means
validating it against the catalogue, replacing a file atomically, and then
regenerating the agent definitions that make a chosen point startable at all.

Nothing here asks anything. It is handed a profile as JSON, it says whether
that profile is one this machine can act on, and where it is, it writes it and
brings `~/.claude/agents/` into line with it. A profile it cannot act on is
reported field by field and nothing is written, because half a profile is
worse than the fallback: the fallback at least says it is one.

The report names the directory it wrote definitions into and, where it had to
create that directory, says why that matters. Claude Code reads the agents
directory when a session starts, so definitions written into a directory that
did not exist a moment ago reach the sessions started from now on rather than
the one running this.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import catalogue
import launch
import profiles
from catalogue import CURRENCY, UNIT, Catalogue, Price
from profiles import PAYMENTS, Channel, Profile

# Where Claude Code reads the subagent definitions this Skill generates. It is
# the one directory outside its own data this Skill ever writes into, and it
# writes only files carrying its own prefix.
AGENTS_DIRECTORY = Path(".claude") / "agents"

# What a caller has to know about a directory that did not exist until now.
# Said in the report rather than left for somebody to discover from a subagent
# the running session cannot name.
CREATED_NOTE = (
    "the agents directory did not exist and was created; Claude Code reads it "
    "when a session starts, so these definitions are available to sessions "
    "started from now on rather than to one already running"
)

# What `_rates` answers with where a card was supplied and refused, which is
# neither a card nor the absence of one. The complaint is already in the list
# by then, so the marker only has to stop the channel being written.
_REFUSED = Price(None, None, None, None, "", "")


def _now() -> str:
    """Return this instant, as a profile dates the answers it holds."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _text(raw: Any) -> str | None:
    """Return a non-empty string, or None for anything else including null."""

    return raw if isinstance(raw, str) and raw.strip() else None


def _number(raw: Any) -> float | None:
    """Return a float, or None for anything that is not a number."""

    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    return float(raw)


def _names(raw: Any, field: str, problems: list[str]) -> tuple[str, ...]:
    """Return one list of names, complaining where it is not one."""

    if not isinstance(raw, list):
        problems.append(f"{field} is missing or is not a list")
        return ()
    named = [name for item in raw if (name := _text(item)) is not None]
    if len(named) != len(raw):
        problems.append(f"{field} holds something that is not a name")
    return tuple(dict.fromkeys(named))


def _channels(
    raw: Any, harnesses: Sequence[str], problems: list[str]
) -> tuple[Channel, ...]:
    """Return the ways of paying, complaining about each one that cannot be read."""

    if raw is None:
        return ()
    if not isinstance(raw, list):
        problems.append("channels is not a list")
        return ()

    read: list[Channel] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            problems.append(f"channel {index} is not an object")
            continue
        provider = _text(entry.get("provider"))
        harness = _text(entry.get("harness"))
        pay = _text(entry.get("pay"))
        if provider is None or harness is None:
            problems.append(f"channel {index} names no provider or no harness")
            continue
        if pay not in PAYMENTS:
            problems.append(
                f"channel {index} pays by {pay!r}, which is not one of {PAYMENTS}"
            )
            continue
        if harness not in harnesses:
            problems.append(
                f"channel {index} pays on {harness!r}, which the profile does not use"
            )
            continue
        rates = _rates(entry.get("rates"), index, problems)
        if rates is _REFUSED:
            continue
        read.append(
            Channel(
                provider=provider,
                harness=harness,
                pay=pay,
                plan=_text(entry.get("plan")),
                gateway=_text(entry.get("gateway")),
                rates=rates,
            )
        )
    return tuple(read)


def _rates(raw: Any, index: int, problems: list[str]) -> Price | None:
    """Return one channel's own rate card, complaining where it is not one.

    Refused rather than dropped. Every figure this Skill compares is USD and
    nothing anywhere converts, so a card in another currency would be added to
    a USD bill with nothing said — the one kind of wrong answer a person
    reading the output cannot see.
    """

    if raw is None:
        return None
    if not isinstance(raw, dict):
        problems.append(f"channel {index} carries a rate card that is not an object")
        return _REFUSED

    currency = _text(raw.get("currency")) or CURRENCY
    unit = _text(raw.get("unit")) or UNIT
    if currency != CURRENCY or unit != UNIT:
        problems.append(
            f"channel {index} carries a rate card in {currency} {unit}; "
            f"this Skill compares {CURRENCY} {UNIT} and converts nothing, so a "
            f"rate card is asked for and recorded in {CURRENCY}"
        )
        return _REFUSED

    return Price(
        input=_number(raw.get("input")),
        cache_read=_number(raw.get("cache_read")),
        cache_write=_number(raw.get("cache_write")),
        output=_number(raw.get("output")),
        currency=currency,
        unit=unit,
    )


def _noticed(channels: Sequence[Channel], cat: Catalogue) -> list[str]:
    """Return what is worth saying about answers this Skill could not offer.

    Not problems. Each one is a profile worth writing that the catalogue
    cannot account for, and the person who saw the screen is the record of
    what they pay — but an interview that cannot tell a chosen answer from a
    typed one cannot tell that its own vocabulary fell short, which is how a
    list missing the plan somebody actually pays for goes on being offered.
    """

    said: list[str] = []
    for channel in channels:
        offered = {plan.name for plan in catalogue.plans_for(cat, channel.provider)}
        if channel.plan is not None and offered and channel.plan not in offered:
            said.append(
                f"{channel.plan!r} is not a plan the catalogue holds for "
                f"{channel.provider}; it is recorded as given, and "
                f"`/model-selector update` is what brings the plans up to date"
            )
        if channel.gateway is not None and channel.rates is None:
            said.append(
                f"the {channel.provider} channel through {channel.gateway} carries "
                f"no rate card, so it is priced at {channel.provider}'s own list "
                f"price; a gateway prices differently"
            )
    return said


def validate(raw: Any, cat: Catalogue) -> tuple[Profile | None, list[str]]:
    """Return the profile *raw* describes, or the reasons it describes none.

    Validated against the catalogue rather than against a schema: a model id
    nothing in the catalogue answers to is a typo that would silently narrow
    every future answer, and a provider nobody sells is a channel that can
    never pay for anything.
    """

    problems: list[str] = []
    if not isinstance(raw, dict):
        return None, ["the profile is not a JSON object"]
    if not cat.models:
        return None, [
            cat.problem or "the catalogue is empty, so nothing can be validated"
        ]

    harnesses = _names(raw.get("harnesses"), "harnesses", problems)
    providers = _names(raw.get("providers"), "providers", problems)
    models = _names(raw.get("models"), "models", problems)
    channels = _channels(raw.get("channels"), harnesses, problems)

    known_models = {model.id for model in cat.models}
    known_providers = {model.provider for model in cat.models}
    problems += [
        f"the catalogue holds no model {name!r}"
        for name in models
        if name not in known_models
    ]
    problems += [
        f"the catalogue holds no provider {name!r}"
        for name in providers
        if name not in known_providers
    ]
    problems += [
        f"channel {index} pays {channel.provider!r}, which the catalogue does not know"
        for index, channel in enumerate(channels)
        if channel.provider not in known_providers
    ]

    if not harnesses:
        problems.append("the profile names no harness, so nothing can be started")
    if not models:
        problems.append("the profile enables no model, so nothing can be chosen")
    if problems:
        return None, problems

    return (
        Profile(
            harnesses=harnesses,
            providers=providers,
            models=models,
            channels=channels,
            answered_at=_text(raw.get("answered_at")) or _now(),
            source="file",
            problem=None,
        ),
        [],
    )


def apply(path: Path | None, data_dir: Path, agents: Path) -> dict[str, Any]:
    """Write one supplied profile and sync the definitions, or only sync.

    Without a profile this is the second half alone, which is what `update`
    runs: the generated definitions say of themselves that `update` rewrites
    this directory, and a catalogue that has just gained or lost a model has
    changed which of them ought to exist. The profile in force is whatever is
    on disk, including the fallback where there is none — a machine nobody has
    interviewed still needs the subagents an answer will name.
    """

    here = Path(__file__).resolve().parent.parent
    cat = catalogue.load(data_dir, here)

    if path is None:
        profile = profiles.load(data_dir, cat)
    else:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as problem:
            return {
                "ok": False,
                "notes": [],
                "problems": [f"{path} could not be read: {problem}"],
            }

        validated, problems = validate(raw, cat)
        if validated is None:
            return {"ok": False, "notes": [], "problems": problems}
        profiles.write(data_dir, validated)
        profile = validated

    synced = launch.sync_definitions(agents, launch.definitions(profile, cat))

    return {
        "ok": True,
        "problems": [],
        "notes": _noticed(profile.channels, cat),
        "profile": {
            "path": str(data_dir / profiles.PROFILE_FILE),
            "answered_at": profile.answered_at,
            "harnesses": list(profile.harnesses),
            "providers": list(profile.providers),
            "models": len(profile.models),
            "channels": len(profile.channels),
        },
        "definitions": {
            "directory": str(agents),
            "written": synced.written,
            "unchanged": synced.unchanged,
            "removed": synced.removed,
            "created_directory": synced.created_directory,
        },
        "note": CREATED_NOTE if synced.created_directory else None,
    }


def _agents_directory(named: str | None) -> Path:
    """Return where the generated definitions go, under a home this may not have."""

    if named:
        return Path(named).expanduser()
    try:
        return Path.home() / AGENTS_DIRECTORY
    except RuntimeError:
        return Path.cwd() / AGENTS_DIRECTORY


def _data_dir(named: str | None) -> Path:
    """Return the data directory, defaulting under a home this may not have."""

    if named:
        return Path(named).expanduser()
    try:
        return Path.home() / ".kntnt" / "model-selector"
    except RuntimeError:
        return Path.cwd() / ".kntnt" / "model-selector"


def _parse(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command line. The only thing in this Skill that may fail."""

    parser = argparse.ArgumentParser(
        prog="setup_apply.py",
        description="Write the profile `setup` gathered and sync the agent definitions.",
    )
    parser.add_argument("--data")
    parser.add_argument("--agents")
    parser.add_argument("path", nargs="?")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Apply one profile, print what happened, and exit 0."""

    args = _parse(argv)
    try:
        report = apply(
            Path(args.path).expanduser() if args.path else None,
            _data_dir(args.data),
            _agents_directory(args.agents),
        )
    except Exception as failure:  # noqa: BLE001 - a report is never worth a traceback
        report = {
            "ok": False,
            "notes": [],
            "problems": [f"the profile could not be applied: {failure!r}"],
        }

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
