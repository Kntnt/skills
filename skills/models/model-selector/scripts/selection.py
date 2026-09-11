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

What is ranked is the chance of finishing first and the price second. Among
the candidates the evidence says will finish, the one whose price per finished
job is lowest is taken — its price divided by its chance of success, since a
point that fails is paid for again — and where any of them has been measured
doing this kind of work the answer is chosen among those alone. No point below
`FLOOR` is taken for being cheap, and among those above it the order is on
price divided by the chance of success; nor is an estimate nobody has tested
taken over one somebody has. `_ranked` states that rule, and `_explored` states
the one exception to reading it off the means: a bounded share of reversible
calls tries the boundary instead, because a store that only ever runs its
favourite never learns that a cheaper point would have done.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
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
from profiles import OBJECTIVES, Profile

# How wide a pool the caller wants to consider. `limited` stays with the
# provider the caller is already paying for this turn, `callable` adds
# everything this machine can actually start — through an adapter where the
# caller is a Harness, and through an installed Bridge command where it is a
# process — and `all` ignores reachability.
SCOPES = ("limited", "callable", "all")

STAKES = ("reversible", "high")

# What finishing the work is counted in where the caller names nothing and the
# user has set nothing. The order is the caller's `--objective`, else the
# user's standing choice, else this: running out of quota mid-week stops
# everything, while a slower job is only slower. The vocabulary, `OBJECTIVES`,
# is the profile module's, the standing choice being one of the user's answers.
DEFAULT_OBJECTIVE = "cost"

# What every call demands before price is allowed to decide anything. Below
# this, a cheap attempt is a cheap way of not getting the work done.
FLOOR = 0.8

# What share of the calls that may explore actually do. It is a probability per
# call rather than a counter, so no particular call is the one that explores and
# over time about a tenth of them are. Low enough that exploring costs a run
# almost nothing, high enough that the store still fills with rows about the
# points the answer keeps stepping over.
EXPLORATION = 0.1

# The two dimensions of a point, one of which an exploration moves. A row that
# moved both at once would say nothing about either, and the coin gives each
# dimension half the explorations.
DIMENSIONS = ("deliberation", "model")

# Where the data directory sits when the caller does not say.
DEFAULT_DATA = Path(".kntnt") / "model-selector"

# The provider a harness pays for itself, used as the floor of `limited` when
# the caller named no seat. opencode is deliberately absent: it fronts
# whatever the user configured, so it implies no provider of its own.
HARNESS_PROVIDER = {"claude-code": "anthropic", "codex": "openai"}

# What a caller calls itself when it is a script rather than a Harness. It can
# spawn no subagent, so every point it is offered is a Bridge command it has to
# run — which is what makes `callable` a narrower question for it than for a
# Harness, and why it appears in no provider table above.
PROCESS = "process"

# What is said when a process caller has candidates and no way to start any of
# them. More specific than the locks the empty pool is otherwise blamed on: the
# models are enabled and paid for, and the machine has nothing installed to
# reach them with.
NOTHING_STARTABLE = "nothing on this machine can start a process for any candidate"


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
    seconds: float


@dataclass(frozen=True)
class Objective:
    """What this call's finishing is counted in, and who said so.

    `source` is `caller` where the request named it, `standing` where the
    user's standing choice did, and `default` where neither did. `problem`
    names a standing choice that was there and could not be read, which counts
    as none and is said in the answer's note rather than refused.
    """

    name: str
    source: str
    problem: str | None = None


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
    if args.kinds:
        return _vocabulary(here)
    objective = _objective(args.objective, data_dir)
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
    pool = _pool(args.scope, cat, profile, seat_model, harness, args.repo, notes)
    pool = _locked_to_model(pool, cat, args.model, notes)
    pool = _locked_to_deliberation(pool, args.deliberation, notes)
    if not pool:
        return _inherit(args, _why_nothing(cat, profile, notes), objective)

    # Rank on what the evidence holds, then — where this request is one the
    # boundary may be tried on — replace the answer with one point beyond it,
    # which is the only way an estimate nobody retries is ever corrected.
    scored = [
        _score(point, args.kind, estimator, kinds, _paid(profile, point, harness))
        for point in pool
    ]
    ranked = _ranked(scored, objective.name)
    explored: str | None = None
    if _explorable(args):
        ranked, explored = _explored(scored, ranked, args, objective.name, notes)

    ranked = _after(ranked, args.after, objective.name, notes)
    if not ranked:
        return _inherit(args, _why_nothing(cat, profile, notes), objective)
    best = ranked[0]

    return _report(
        best, ranked[1:], args, profile, cat, harness, explored, objective, notes
    )


def _objective(asked: str | None, data_dir: Path) -> Objective:
    """Return what this call ranks on: the caller's, the user's, or the default.

    The standing choice is read only where the caller named nothing, because
    a caller's `--objective` wins and a file it does not need is no business of
    that call. A file that cannot be read is treated as absent, and its reason
    travels to the note: the call is answered on the default, never refused.
    """

    if asked is not None:
        return Objective(asked, "caller")
    standing, problem = profiles.standing_objective(data_dir)
    if standing is not None:
        return Objective(standing, "standing")
    return Objective(DEFAULT_OBJECTIVE, "default", problem)


def _vocabulary(here: Path) -> dict[str, Any]:
    """Return the closed vocabulary a caller classifies its own work into.

    The eight kinds and the sentence that tells each from the others, which is
    what this Skill's own `## Arguments` gives a person. A machine caller reads
    no Skill body and may not reach into this Skill's data, so the list it has
    to classify against comes back through the entry point it already calls
    (issue #292). The vocabulary is the constant rather than the file: a kind
    the shipped data has lost its note for is still a kind, and is still
    offered.
    """

    kinds = evidence.load_kinds(here)
    return {
        "ok": True,
        "kinds": [{"kind": kind, "note": kinds.notes.get(kind, "")} for kind in KINDS],
    }


def _explorable(args: argparse.Namespace) -> bool:
    """Return whether this request is one the boundary may be tried on.

    Three requests are answered rather than explored. High stakes wants the
    best point the evidence knows of rather than a row about a cheaper one,
    there being nothing behind it to catch a wrong answer. A model or a
    deliberation lock is the user's own instruction, and an instruction is not
    a dimension to vary. And a caller naming the point that just failed is
    asking for the step up from it, which is a second question rather than an
    experiment.
    """

    return (
        args.stakes != "high"
        and args.model is None
        and args.deliberation is None
        and args.after is None
    )


def _explored(
    scored: Sequence[Scored],
    ranked: Sequence[Scored],
    args: argparse.Namespace,
    objective: str,
    notes: list[str | None],
) -> tuple[list[Scored], str | None]:
    """Return the answer, either as ranked or with one dimension of it moved.

    A pool ranked on its means answers the same question the same way for ever.
    The moment the store holds good rows for one point that point wins every
    call, so nothing cheaper is ever tried, so no estimate but its own is ever
    corrected — and a cheaper point that would in fact have done the job stays
    undiscoverable. So a bounded share of the calls that may be explored buys a
    row instead of the answer: about one in ten, drawn per call rather than
    counted, so that nothing has to remember what the last call did and
    `--seed` still reproduces which calls those were.

    One coin decides whether this call explores and a second decides which
    dimension it moves, because an exploration that moved the model and the
    level at once would come back with a row saying nothing about either. Each
    candidate beyond the boundary is then drawn once from its own posterior,
    cheapest first, and the first draw to clear the floor is taken: a candidate
    with few rows behind it has a wide posterior and therefore gets tried, a
    candidate confidently worse essentially never does, and nothing has to
    define which is which. Where no draw clears, the best of them is taken
    anyway — the coin has already spent this call on the experiment, and coming
    back with the answer would spend it on nothing.

    The dissent is reported because an exploration is how this call was spent
    and never a claim about the world: a reader who finds a weaker point chosen
    has to be able to tell a deliberate experiment from an error at a glance
    (ADR-0182).
    """

    rng = random.Random(args.seed)
    if rng.random() >= EXPLORATION:
        return list(ranked), None

    dimension = DIMENSIONS[0] if rng.random() < 0.5 else DIMENSIONS[1]
    plain = ranked[0]
    beyond = _beyond(scored, plain, dimension, objective)
    if not beyond:
        return list(ranked), None

    chosen = _tried(beyond, rng)
    notes.append(
        f"explored the {dimension} dimension, where the evidence would have "
        f"chosen {_named(plain.point)}"
    )
    return [chosen, *[row for row in ranked if row is not chosen]], dimension


def _beyond(
    scored: Sequence[Scored], plain: Scored, dimension: str, objective: str
) -> list[Scored]:
    """Return every point one dimension away from the answer and cheaper than it.

    On `deliberation` that is the answer's own model at each of its other
    levels; on `model` it is every other model, taken at the answer's level or
    at the nearest level that model supports. Only the cheaper ones are
    candidates: the answer is already the point the evidence vouches for with
    the lowest price per finished job — measured for the kind where anything
    measured clears the floor — so what a row is worth buying about is whether
    something below it, often a point nothing has measured yet, would have done.
    """

    if dimension == "deliberation":
        beside = [
            row
            for row in scored
            if row.point.model.id == plain.point.model.id
            and row.point.deliberation != plain.point.deliberation
        ]
    else:
        beside = [
            _alongside(rows, plain.point.deliberation)
            for rows in _elsewhere(scored, plain.point.model.id)
        ]

    cheaper = [row for row in beside if _below(row, plain, objective)]
    return sorted(cheaper, key=lambda row: _order(row, objective))


def _tried(beyond: Sequence[Scored], rng: random.Random) -> Scored:
    """Return the cheapest candidate whose own draw clears the floor.

    Every candidate is drawn once, in the fixed order it arrives in, so that a
    seed reproduces the whole experiment rather than merely its first step.
    """

    drawn = [(row, row.estimate.draw(rng.random())) for row in beyond]
    for row, chance in drawn:
        if chance >= FLOOR:
            return row
    return max(drawn, key=lambda tried: tried[1])[0]


def _elsewhere(scored: Sequence[Scored], model_id: str) -> list[list[Scored]]:
    """Return the points of every model but one, grouped and in pool order."""

    grouped: dict[str, list[Scored]] = {}
    for row in scored:
        if row.point.model.id != model_id:
            grouped.setdefault(row.point.model.id, []).append(row)
    return list(grouped.values())


def _alongside(rows: Sequence[Scored], level: str | None) -> Scored:
    """Return one model's point at a level, or at the nearest it supports.

    Where the answer carries no level at all its model has no effort control,
    so there is no level to be near and the other model is taken at the bottom
    of its own ladder.
    """

    at = [row for row in rows if row.point.deliberation == level]
    if at:
        return at[0]
    if level is None:
        return min(rows, key=lambda row: _position(row.point.deliberation))
    wanted = _nearest(rows[0].point.model, level)
    near = [row for row in rows if row.point.deliberation == wanted]
    return near[0] if near else rows[0]


def _below(row: Scored, plain: Scored, objective: str) -> bool:
    """Return whether one point is cheaper than the answer, in the caller's terms.

    A point nothing can price is never cheaper than one that can be priced. An
    absence read as a nought is how an unmeasured configuration becomes the
    cheapest thing on the frontier by having nothing behind it.
    """

    if objective == "time":
        return row.seconds < plain.seconds
    if row.cost_usd is None or plain.cost_usd is None:
        return False
    return row.cost_usd < plain.cost_usd


def _order(row: Scored, objective: str) -> tuple[float, str, int]:
    """Return the fixed order candidates are drawn and taken in, cheapest first."""

    price = row.seconds if objective == "time" else (row.cost_usd or 0.0)
    return (price, row.point.model.id, _position(row.point.deliberation))


def _after(
    ranked: Sequence[Scored],
    failed: str | None,
    objective: str,
    notes: list[str | None],
) -> list[Scored]:
    """Return one step up from a point that just failed, best first.

    Escalation is a second question rather than a second answer, so it is asked
    the way the first one was and answered from the same pool: keep the
    candidates strictly likelier to finish the work than the one that failed,
    and where any of those has been measured for the kind and clears the floor,
    step to the one of them with the lowest price per finished job — a failure
    is answered with a point the evidence has seen doing the work before it is
    answered with a cheaper guess. Where none has, the step is the likelier
    point with the lowest price per finished job, measured or not and with no
    floor. Either way every candidate is ordered on its price divided by its
    chance of success, or on its elapsed time divided by it where the caller
    asked for time. Nothing is appended above the top of the ladder:
    where the failed point was already the likeliest thing available, the
    caller is told so and offered it again, because there is no step and
    pretending otherwise would spend a retry on the same seat under a
    different name.
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
    order = _time_key if objective == "time" else _cost_key
    stepped = sorted(stepped, key=order)
    vouched = [row for row in stepped if _vouched(row)]
    if not vouched:
        return stepped
    return [vouched[0], *[row for row in stepped if row is not vouched[0]]]


def _report(
    best: Scored,
    rest: Sequence[Scored],
    args: argparse.Namespace,
    profile: Profile,
    cat: Catalogue,
    harness: str,
    explored: str | None,
    objective: Objective,
    notes: Sequence[str | None],
) -> dict[str, Any]:
    """Render one ranked pool as the answer a caller acts on.

    It names the objective it ranked on and where that came from, because two
    callers asking the same question with no `--objective` are answered on
    whatever the user last set, and a reader has to be able to see which.
    """

    started = launch.plan(
        best.point.model,
        best.point.deliberation,
        harness,
        profile,
        cat,
        repo=args.repo,
        read_only=args.read_only,
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
        "explored": explored,
        "objective": objective.name,
        "objective_source": objective.source,
        "confidence": round(best.estimate.low, 3),
        "expected": {
            "cost_usd": _rounded_cost(best.cost_usd),
            "p_success": round(best.estimate.mean, 3),
            "tokens": round(total),
            "seconds": round(best.seconds),
            "per_success_cost_usd": _rounded_cost(_per_success_cost(best)),
            "per_success_seconds": round(_per_success_seconds(best)),
            "runs": round(best.estimate.n, 1),
        },
        "alternatives": _alternatives(best, rest, args.n),
        "attempt_id": _attempt_id(),
        "note": _note([*notes, objective.problem, started.note]),
    }


def _inherit(
    args: argparse.Namespace, why: str, objective: Objective | None = None
) -> dict[str, Any]:
    """Return the answer that declines to route, naming the caller's own seat.

    It still names the objective the call would have ranked on, so a caller
    reading any answer finds the same members in it.
    """

    held = objective or _objective(args.objective, _data_dir(args.data))
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
        "explored": None,
        "objective": held.name,
        "objective_source": held.source,
        "confidence": 0.0,
        "expected": {
            "cost_usd": None,
            "p_success": None,
            "tokens": None,
            "seconds": None,
            "per_success_cost_usd": None,
            "per_success_seconds": None,
            "runs": 0.0,
        },
        "alternatives": [],
        "attempt_id": _attempt_id(),
        "note": _note([why, held.problem]),
    }


def _pool(
    scope: str,
    cat: Catalogue,
    profile: Profile,
    seat_model: str | None,
    harness: str,
    repo: str | None,
    notes: list[str | None],
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

    # `callable` is what this caller can actually start, and what that means
    # depends on what the caller is. A Harness starts the points of its own
    # provider natively, so those are admitted and the rest are tested against
    # the adapters. A process starts every point the same way, by running a
    # Bridge command, so every point takes the same test — the floor's own
    # included, a seat being no evidence that the CLI behind it is installed
    # (issue #301).
    if harness == PROCESS:
        startable = [
            point
            for point in points
            if _reachable(point, harness, profile, cat, repo, started_here=True)
        ]
        if not startable and points:
            notes.append(NOTHING_STARTABLE)
        return startable

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
    point: Point,
    harness: str,
    profile: Profile,
    cat: Catalogue,
    repo: str | None,
    *,
    started_here: bool = False,
) -> bool:
    """Return whether this machine can start this point and say who pays for it.

    Two tests where an adapter does the starting: something plans a way in, and
    the profile carries a channel that says who pays for it. `started_here` adds
    the third, for a caller that starts what it is given itself: the binary the
    plan would run has to be on this machine. Without it an unreachable point
    wins, degrades to `inherit` at launch, and reaches the grader as no judge
    rather than as no CLI — a machine reporting a judge it could not run instead
    of choosing one it could (issue #301).

    The binary tested is the head of the argv the plan already carries, so
    nothing here keeps a second list of CLI names to fall out of date. The test
    is a `PATH` lookup and nothing more — no process is started and no network
    is touched — which is the same probes-only stance the harness markers are
    detected under, and which this has to keep because selection runs inside
    somebody else's turn.
    """

    started = launch.plan(
        point.model, point.deliberation, harness, profile, cat, repo=repo
    )
    if started.how == "inherit":
        return False
    if profiles.channel_for(profile, point.model, harness) is None:
        return False
    if not started_here:
        return True
    if started.command is None:
        return False
    return shutil.which(started.command[0]) is not None


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


def _paid(profile: Profile, point: Point, harness: str) -> catalogue.Price | None:
    """Return the rate card the channel that pays for this point carries.

    A gateway prices the same model differently from the provider whose model
    it is, and the catalogue holds the provider's own list price alone. Where
    the user has said what they pay, that is what the comparison is made on.
    """

    channel = profiles.channel_for(profile, point.model, harness)
    return channel.rates if channel is not None else None


def _score(
    point: Point,
    kind: str,
    estimator: Estimator,
    kinds: KindPriors,
    rates: catalogue.Price | None,
) -> Scored:
    """Attach the estimate, the token forecast, the bill and the clock to one point.

    All four are what the evidence holds about the point as it stands, and all
    four are per attempt. Nothing here is divided by anything: what one attempt
    costs and how likely it is to finish are two facts about the point, and the
    keys `_ranked` orders on are where one is divided by the other.
    """

    estimate = estimator.p_success(kind, point.model.id, point.deliberation)
    tokens = estimator.tokens(kind, point.model.id, point.deliberation)
    cost = catalogue.cost_usd(point.model, tokens, kind, kinds, rates=rates)
    taken = estimator.seconds(kind, point.model.id, point.deliberation)
    return Scored(point, estimate, tokens, cost, taken)


def _ranked(scored: Sequence[Scored], objective: str) -> list[Scored]:
    """Order the pool best first: the floor decides who is in, then price decides.

    The requirement is that the job gets done, and that among what gets it done
    the cheapest is chosen. A point that fails is paid for again, and a point
    at 0.5 needs two attempts on average, so what a finished job costs is the
    price of one attempt divided by the chance of success. So the candidates
    the evidence believes in — those whose posterior mean clears the floor —
    are ordered on that figure, and the rest fall in behind them ordered on
    their chances, which is all a pool that can promise nothing has left to
    offer. No point below `FLOOR` is taken for being cheap, and among those
    above it the order is on price divided by the chance of success: the
    division reads the chance as the expected number of attempts, never as an
    exchange rate between chance and money (ADR-0188).

    A mean is not the same claim for every point, though. Where a point has been
    measured doing this kind of work, its mean is what this machine saw; where
    it has not, its mean is a prior or a verdict carried over from other work,
    and on the means alone that estimate wins whenever it looks cheaper. So the
    points measured for the kind that clear the floor go first, ordered on
    price per finished job, and everything else follows exactly as it would
    have without them.
    Nothing is filtered out: the alternatives and a named failure read the same
    list, and whether a cheaper, untried point would have done is what the
    explored calls find out (ADR-0187).

    The objective chooses which price is read, and either is divided by the
    same chance. It is the caller's where the caller names one, else the
    user's standing choice, else money: money because it is what a run spends
    whether or not anybody is watching, and running out of quota stops
    everything while a slower job is only slower; time is what a person
    waiting on the answer is spending instead, and it is theirs to ask for.
    """

    order = _time_key if objective == "time" else _cost_key
    clears = [row for row in scored if row.estimate.mean >= FLOOR]
    under = [row for row in scored if row.estimate.mean < FLOOR]
    whole = sorted(clears, key=order) + sorted(under, key=_quality_key)
    vouched = [row for row in whole if _vouched(row)]
    return vouched + [row for row in whole if not _vouched(row)]


def _vouched(row: Scored) -> bool:
    """Return whether this point's own rows for the kind clear the floor.

    Measured is the estimator's word for it — enough rows in the exact kind,
    model and deliberation — so a model's rows at other levels or of other
    kinds leave a point pooled, however good they were.
    """

    return row.estimate.basis == "measured" and row.estimate.mean >= FLOOR


def _time_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by the clock a finished job takes, for a run somebody is waiting on.

    One attempt's elapsed time divided by the chance of success, because an
    attempt that fails is waited on again.
    """

    return (False, _per_success_seconds(row), *_tiebreak(row))


def _cost_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by price per finished job: one attempt's price over its chance.

    An attempt that fails is paid for again, so a point at 0.82 costs about
    1.22 attempts per job and one at 0.98 about 1.02. An unpriced point still
    sorts behind every priced one.
    """

    return (row.cost_usd is None, _per_success_cost(row) or 0.0, *_tiebreak(row))


def _per_success_cost(row: Scored) -> float | None:
    """Return one attempt's price divided by its chance, or None where unpriced.

    The posterior mean never reaches nought, so the division needs no guard.
    """

    if row.cost_usd is None:
        return None
    return row.cost_usd / row.estimate.mean


def _per_success_seconds(row: Scored) -> float:
    """Return one attempt's elapsed time divided by its chance of success."""

    return row.seconds / row.estimate.mean


def _quality_key(row: Scored) -> tuple[bool, float, float, float, int, str]:
    """Rank by chances alone, for a pool nothing in which clears the floor."""

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
    could have run. Ranked order puts the entries that clear the floor first,
    ordered on price per finished job, so each entry carries that figure beside
    its per-attempt price, and the elapsed time per finished job beside it.
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
                "cost_usd": _rounded_cost(row.cost_usd),
                "p_success": round(row.estimate.mean, 3),
                "per_success_cost_usd": _rounded_cost(_per_success_cost(row)),
                "per_success_seconds": round(_per_success_seconds(row)),
            }
        )
    return listed


def _rounded_cost(cost: float | None) -> float | None:
    """Round a dollar figure the way the answer reports every one, keeping a null."""

    return None if cost is None else round(cost, 4)


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


def _named(point: Point) -> str:
    """Spell one point the way a caller names one on a command line."""

    if point.deliberation is None:
        return point.model.id
    return f"{point.model.id}@{point.deliberation}"


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
    parser.add_argument("--kinds", action="store_true")
    parser.add_argument("--scope", choices=SCOPES, default="callable")
    parser.add_argument("--harness")
    parser.add_argument("--seat")
    parser.add_argument("--model")
    parser.add_argument("--deliberation", choices=LEVELS)
    parser.add_argument("--stakes", choices=STAKES, default="reversible")
    parser.add_argument("--after")
    parser.add_argument("--objective", choices=OBJECTIVES)
    parser.add_argument("--repo")
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--data")
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
