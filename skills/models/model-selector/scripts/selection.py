# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""The decision, and the one entry point a machine calls to get it.

A caller arrives mid-task with a piece of work and its own seat, and leaves
with one model, one level of deliberation, and a way to start them. Everything
this Skill knows feeds that one JSON object: the catalogue says what exists and
what it costs, the profile says what this machine can reach, the evidence store
says what has actually worked, and `launch` says how to start what was chosen.

The posture matters more than the arithmetic. This runs inside somebody else's
turn, so there is no refusal and no non-zero exit a caller could read as
*stop* — only a malformed command line fails. Where nothing can be chosen the
answer is `inherit`: keep working in the seat you already have. A routing
service that can block the work it was asked about is worse than no routing
service, because the work is what matters and the routing is an optimisation.

The work itself is never passed in. A caller names its kind and nothing more,
because that is the whole of what the arithmetic reads, and a brief accepted
here would be a brief somebody expects to have been recorded.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import catalogue
import evidence
import launch
import profiles
from catalogue import LEVELS, Catalogue, Model
from evidence import KINDS, Estimate, Estimator, KindPriors
from profiles import Profile

# How wide a pool the caller wants to consider. `limited` stays with the
# provider the caller is already paying for this turn, `callable` adds
# everything this machine can actually start, `all` ignores reachability.
SCOPES = ("limited", "callable", "all")

STAKES = ("reversible", "high")

# What finishing the work is counted in. Money is what a run spends whether or
# not anybody is watching it; time is what the person waiting on it spends
# instead, and asking for one is not the same as asking for the other.
OBJECTIVES = ("cost", "time")

# What `high` stakes demands before cost is allowed to decide anything. Below
# this, a cheap attempt is a cheap way of not getting the work done.
FLOOR = 0.8

# Where the data directory sits when the caller does not say.
DEFAULT_DATA = Path(".kntnt") / "model-selector"

# The provider a harness pays for itself, used as the floor of `limited` when
# the caller named no seat. opencode is deliberately absent: it fronts
# whatever the user configured, so it implies no provider of its own.
HARNESS_PROVIDER = {"claude-code": "anthropic", "codex": "openai"}


@dataclass(frozen=True)
class Point:
    """One model at one level of deliberation — the unit being chosen between.

    `deliberation` is None for a model with no effort control at all, which
    has exactly one point rather than one per level.
    """

    model: Model
    deliberation: str | None


@dataclass(frozen=True)
class Scored:
    """One candidate point with everything the ranking needs to compare it."""

    point: Point
    estimate: Estimate
    tokens: dict[str, float]
    cost_usd: float | None
    expected_usd: float | None
    seconds: float
    expected_seconds: float


def main(argv: Sequence[str] | None = None) -> int:
    """Print one answer as JSON and exit 0, whatever the state of the machine."""

    args = _parse(argv)
    try:
        answer = _answer(args)
    except Exception as failure:  # noqa: BLE001 - a machine entry point is fail-open by contract
        # A broad catch, on purpose. This is a machine entry point inside
        # somebody else's turn: an unhandled failure here would end their work
        # over an optimisation, so every failure becomes `inherit` instead.
        answer = _inherit(args, f"the selector failed: {failure!r}")

    print(json.dumps(answer))
    return 0


def _answer(args: argparse.Namespace) -> dict[str, Any]:
    """Build the answer, from the world through the evidence to one point."""

    data_dir = _data_dir(args.data)
    here = Path(__file__).resolve().parent.parent
    cat = catalogue.load(data_dir, here)
    profile = profiles.load(data_dir, cat)
    kinds = evidence.load_kinds(here)
    estimator = Estimator(evidence.load(data_dir), cat, kinds)

    harness = _harness(args.harness, profile)
    seat_model, _ = _seat(args.seat)
    notes = [profile.problem] if profile.source == "fallback" else []

    # The pool, then the two locks, in that order: a lock narrows what scope
    # admitted rather than reaching past it, except where it names a model
    # scope never offered, which is a caller saying it knows better.
    pool = _pool(args.scope, cat, profile, seat_model, harness, args.repo)
    pool = _locked_to_model(pool, cat, args.model, notes)
    pool = _locked_to_deliberation(pool, args.deliberation, notes)
    if not pool:
        return _inherit(args, _why_nothing(cat, profile, notes))

    scored = [_score(point, args.kind, estimator, kinds) for point in pool]
    ranked = _ranked(scored, args.stakes, args.objective)
    ranked = _after(ranked, args.after, notes)
    if not ranked:
        return _inherit(args, _why_nothing(cat, profile, notes))
    best = ranked[0]

    return _report(best, ranked[1:], args, profile, cat, harness, notes)


def _after(
    ranked: Sequence[Scored], failed: str | None, notes: list[str | None]
) -> list[Scored]:
    """Return one step up from a point that just failed, best first.

    Escalation is a second question rather than a second answer, so it is asked
    the way the first one was and answered from the same ranked pool: keep the
    candidates strictly likelier to finish the work than the one that failed,
    and the existing order — the cost of finishing — picks among them. Nothing
    is appended above the top of the ladder: where the failed point was already
    the likeliest thing available, the caller is told so and offered it again,
    because there is no step and pretending otherwise would spend a retry on
    the same seat under a different name.
    """

    if failed is None:
        return list(ranked)

    model, level = _seat(failed)
    beaten = [
        row
        for row in ranked
        if row.point.model.id == model and row.point.deliberation == level
    ]
    if not beaten:
        notes.append(f"nothing here matches the failed point {failed!r}")
        return list(ranked)

    floor = beaten[0].estimate.mean
    stepped = [row for row in ranked if row.estimate.mean > floor]
    if not stepped:
        notes.append(f"{failed!r} is already the likeliest point this request reaches")
        return list(ranked)

    notes.append(f"one step up from {failed!r}, which failed")
    return stepped


def _report(
    best: Scored,
    rest: Sequence[Scored],
    args: argparse.Namespace,
    profile: Profile,
    cat: Catalogue,
    harness: str,
    notes: Sequence[str | None],
) -> dict[str, Any]:
    """Render one ranked pool as the answer a caller acts on."""

    started = launch.plan(
        best.point.model,
        best.point.deliberation,
        harness,
        profile,
        cat,
        repo=args.repo,
    )
    channel = profiles.channel_for(profile, best.point.model, harness)
    total = sum(best.tokens.values())

    return {
        "ok": True,
        "kind": args.kind,
        "model": best.point.model.id,
        "deliberation": best.point.deliberation,
        "channel": _channel(channel),
        "launch": {
            "how": started.how,
            "subagent_type": started.subagent_type,
            "command": list(started.command) if started.command else None,
            "note": started.note,
        },
        "basis": best.estimate.basis,
        "confidence": round(best.estimate.low, 3),
        "expected": {
            "cost_usd": None if best.cost_usd is None else round(best.cost_usd, 4),
            "p_success": round(best.estimate.mean, 3),
            "tokens": round(total),
            "seconds": round(best.seconds),
            "runs": round(best.estimate.n, 1),
        },
        "alternatives": _alternatives(best, rest, args.n),
        "attempt_id": _attempt_id(),
        "note": _note([*notes, started.note]),
    }


def _inherit(args: argparse.Namespace, why: str) -> dict[str, Any]:
    """Return the answer that declines to route, naming the caller's own seat."""

    seat_model, seat_level = _seat(args.seat)
    return {
        "ok": True,
        "kind": args.kind,
        "model": seat_model,
        "deliberation": seat_level,
        "channel": None,
        "launch": {
            "how": "inherit",
            "subagent_type": None,
            "command": None,
            "note": why,
        },
        "basis": "inherit",
        "confidence": 0.0,
        "expected": {
            "cost_usd": None,
            "p_success": None,
            "tokens": None,
            "seconds": None,
            "runs": 0.0,
        },
        "alternatives": [],
        "attempt_id": _attempt_id(),
        "note": why,
    }


def _pool(
    scope: str,
    cat: Catalogue,
    profile: Profile,
    seat_model: str | None,
    harness: str,
    repo: str | None,
) -> list[Point]:
    """Return every point the scope admits, before any lock narrows it."""

    source = cat.models if scope == "all" else _enabled(cat, profile)
    points = [
        Point(model, level)
        for model in source
        for level in (model.deliberation or (None,))
    ]
    if scope == "all":
        return points

    # `limited` is the provider the caller is already paying for this turn.
    # Where neither the seat nor the harness names one, nothing is excluded:
    # a floor nobody can compute is not a reason to narrow the answer.
    floor = _provider_floor(cat, seat_model, harness)
    near = [point for point in points if floor is None or point.model.provider == floor]
    if scope == "limited":
        return near

    reachable = [
        point
        for point in points
        if point not in near and _reachable(point, harness, profile, cat, repo)
    ]
    return near + reachable


def _enabled(cat: Catalogue, profile: Profile) -> list[Model]:
    """Return the catalogue models the profile says this machine has."""

    wanted = set(profile.models)
    return [model for model in cat.models if model.id in wanted]


def _provider_floor(cat: Catalogue, seat_model: str | None, harness: str) -> str | None:
    """Return the provider `limited` stays with, or None where there is none."""

    if seat_model is not None:
        matched = catalogue.resolve(cat, seat_model)
        if matched:
            return matched[0].provider
    return HARNESS_PROVIDER.get(harness)


def _reachable(
    point: Point, harness: str, profile: Profile, cat: Catalogue, repo: str | None
) -> bool:
    """Return whether this machine can start this point and say who pays for it."""

    started = launch.plan(
        point.model, point.deliberation, harness, profile, cat, repo=repo
    )
    if started.how == "inherit":
        return False
    return profiles.channel_for(profile, point.model, harness) is not None


def _locked_to_model(
    pool: Sequence[Point], cat: Catalogue, token: str | None, notes: list[str | None]
) -> list[Point]:
    """Narrow the pool to a locked model, without ever emptying it.

    An unrecognised lock is a typo or a model this machine has never heard of.
    Either way the caller still needs an answer, so the lock is reported as
    unrecognised and the pool stands.
    """

    if token is None:
        return list(pool)

    matched = catalogue.resolve(cat, token)
    if not matched:
        notes.append(f"the model lock {token!r} matched nothing in the catalogue")
        return list(pool)

    kept = [point for point in pool if point.model.id == matched[0].id]
    if kept:
        if len({point.model.id for point in pool if _among(point, matched)}) > 1:
            notes.append(
                f"the lock {token!r} names several models; {matched[0].id} is newest"
            )
        return kept

    # The lock named something the scope never offered. A caller naming a
    # model explicitly outranks the scope it also named, so the point is
    # admitted and the widening is said out loud.
    notes.append(
        f"the lock {token!r} names {matched[0].id}, which this scope did not offer"
    )
    return [Point(matched[0], level) for level in matched[0].deliberation]


def _locked_to_deliberation(
    pool: Sequence[Point], level: str | None, notes: list[str | None]
) -> list[Point]:
    """Narrow the pool to one level, or to the nearest each model supports."""

    if level is None:
        return list(pool)

    kept = [point for point in pool if point.deliberation == level]
    if kept:
        return kept

    nearest = [Point(model, _nearest(model, level)) for model in _models(pool)]
    if nearest:
        offered = ", ".join(
            sorted({point.deliberation or "no effort control" for point in nearest})
        )
        notes.append(f"no candidate supports {level!r}; using {offered} instead")
    return nearest


def _score(point: Point, kind: str, estimator: Estimator, kinds: KindPriors) -> Scored:
    """Attach the estimate, the token forecast and both bills to one point.

    The second bill is the one that decides. What a caller pays to finish the
    work is what every attempt costs divided by the share of attempts that
    succeed, plus what each failure costs to notice and brief again — and that
    last term is why a candidate expected to fail three times in four is not
    the economical answer merely because its tokens are cheap.
    """

    estimate = estimator.p_success(kind, point.model.id, point.deliberation)
    tokens = estimator.tokens(kind, point.model.id, point.deliberation)
    cost = catalogue.cost_usd(point.model, tokens, kind, kinds)
    probability = max(estimate.mean, 1e-6)
    expected = (
        None
        if cost is None
        else (cost + kinds.overhead(kind) * (1.0 - estimate.mean)) / probability
    )
    taken = estimator.seconds(kind, point.model.id, point.deliberation)
    return Scored(point, estimate, tokens, cost, expected, taken, taken / probability)


def _ranked(scored: Sequence[Scored], stakes: str, objective: str) -> list[Scored]:
    """Order the pool best first, under the rule the stakes call for.

    The objective chooses which quantity *finishing* is counted in. Money is
    the default because it is what a run spends whether or not anybody is
    watching; time is what a person waiting on the answer is spending instead,
    and it is theirs to ask for.
    """

    if stakes == "high":
        confident = [row for row in scored if row.estimate.mean >= FLOOR]
        if confident:
            return sorted(confident, key=_cost_key)
        return sorted(scored, key=_quality_key)
    if objective == "time":
        return sorted(scored, key=_time_key)
    return sorted(scored, key=_value_key)


def _value_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by the cost of finishing, the default for reversible work."""

    return (row.expected_usd is None, row.expected_usd or 0.0, *_tiebreak(row))


def _time_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by the time to finish, for a run somebody is waiting on."""

    return (False, row.expected_seconds, *_tiebreak(row))


def _cost_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by cost alone, once the success floor has already been met."""

    return (row.cost_usd is None, row.cost_usd or 0.0, *_tiebreak(row))


def _quality_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by success alone, for high stakes nothing clears the floor for."""

    return (row.cost_usd is None, -row.estimate.mean, *_tiebreak(row))


def _tiebreak(row: Scored) -> tuple[float, float, int, str]:
    """Break a tie on the better outcome, then the cheaper bill, then the id."""

    return (
        -row.estimate.mean,
        row.cost_usd or 0.0,
        _position(row.point.deliberation),
        row.point.model.id,
    )


def _alternatives(
    best: Scored, rest: Sequence[Scored], count: int
) -> list[dict[str, Any]]:
    """Return the next best points, one per model, in ranked order.

    One per model, because a caller reading three levels of the same model has
    been told the same thing three times and still does not know what else it
    could have run.
    """

    seen = {best.point.model.id}
    listed: list[dict[str, Any]] = []
    for row in rest:
        if len(listed) >= max(count, 0):
            break
        if row.point.model.id in seen:
            continue
        seen.add(row.point.model.id)
        listed.append(
            {
                "model": row.point.model.id,
                "deliberation": row.point.deliberation,
                "cost_usd": None if row.cost_usd is None else round(row.cost_usd, 4),
                "p_success": round(row.estimate.mean, 3),
            }
        )
    return listed


def _channel(channel: profiles.Channel | None) -> dict[str, Any] | None:
    """Return who pays for the chosen point, or None where nobody has said."""

    if channel is None:
        return None
    return {
        "provider": channel.provider,
        "pay": channel.pay,
        "plan": channel.plan,
        "harness": channel.harness,
    }


def _why_nothing(cat: Catalogue, profile: Profile, notes: Sequence[str | None]) -> str:
    """Say why the pool came out empty, in the most specific terms available."""

    if not cat.models:
        return cat.problem or "the catalogue is empty"
    if not profile.models:
        return profile.problem or "the profile enables no models"
    return _note(notes) or "no candidate model was left after the locks"


def _note(notes: Sequence[str | None]) -> str | None:
    """Fold the accumulated notes into one line, or None where there are none."""

    said = [note for note in notes if note]
    return "; ".join(dict.fromkeys(said)) if said else None


def _among(point: Point, matched: Sequence[Model]) -> bool:
    """Return whether this point's model is one the lock resolved to."""

    return any(point.model.id == model.id for model in matched)


def _models(pool: Sequence[Point]) -> list[Model]:
    """Return the distinct models in a pool, in the order they first appear."""

    seen: dict[str, Model] = {}
    for point in pool:
        seen.setdefault(point.model.id, point.model)
    return list(seen.values())


def _nearest(model: Model, level: str) -> str | None:
    """Return the supported level closest to the one that was asked for.

    None where the model has no effort control, that model's one point being
    as near the requested level as it is ever going to get.
    """

    if not model.deliberation:
        return None
    wanted = LEVELS.index(level)
    return min(
        model.deliberation,
        key=lambda supported: (
            abs(LEVELS.index(supported) - wanted),
            LEVELS.index(supported),
        ),
    )


def _position(level: str | None) -> int:
    """Return where a level sits on the scale, with no control below all of it."""

    return LEVELS.index(level) if level is not None else -1


def _seat(seat: str | None) -> tuple[str | None, str | None]:
    """Split `model@level` into its two halves, either of which may be absent."""

    if not seat:
        return None, None
    model, _, level = seat.partition("@")
    return (model or None), (level or None)


def _harness(named: str | None, profile: Profile) -> str:
    """Return the harness to plan against: the caller's, else the first detected."""

    if named:
        return named
    if profile.harnesses:
        return profile.harnesses[0]
    detected = profiles.detect_harnesses()
    return detected[0] if detected else ""


def _data_dir(named: str | None) -> Path:
    """Return the data directory, defaulting under a home this may not have."""

    if named:
        return Path(named).expanduser()
    try:
        return Path.home() / DEFAULT_DATA
    except RuntimeError:
        return Path.cwd() / DEFAULT_DATA


def _attempt_id() -> str:
    """Mint the id the caller files its measurement under."""

    day = datetime.now(UTC).strftime("%Y%m%d")
    return f"ms-{day}-{uuid.uuid4().hex[:6]}"


def _parse(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command line. The only thing in this Skill that may fail."""

    parser = argparse.ArgumentParser(
        prog="selection.py",
        description="Choose a model for one piece of delegated work.",
    )
    parser.add_argument("--kind", choices=KINDS, default="implement")
    parser.add_argument("--scope", choices=SCOPES, default="callable")
    parser.add_argument("--harness")
    parser.add_argument("--seat")
    parser.add_argument("--model")
    parser.add_argument("--deliberation", choices=LEVELS)
    parser.add_argument("--stakes", choices=STAKES, default="reversible")
    parser.add_argument("--after")
    parser.add_argument("--objective", choices=OBJECTIVES, default="cost")
    parser.add_argument("--repo")
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--data")
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
