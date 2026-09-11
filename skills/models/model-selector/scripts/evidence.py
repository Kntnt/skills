# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""What actually happened, and what it says about what will happen next.

Two things live here. The store is a JSON Lines ledger of graded attempts,
appended to and never edited, written field by field onto a closed set of
names so that a caller cannot smuggle a key into it and nothing has to be
stripped back out later. A row leaves it only with the model it measured:
`reset --evidence` discards the whole ledger, and a model its maker no longer
lists takes its rows with it (`discard_models`). The estimator is what the store is for: given a kind, a model and a
level of deliberation, how likely is the attempt to come back good, and how
many tokens of each category will it burn getting there.

The estimator is a four-level hierarchy and that is the whole design. Almost
every cell of the (kind x model x deliberation) grid is empty and will stay
empty — a person only ever measures a handful of points — so an estimate for
an unmeasured cell has to be borrowed from the cells around it rather than
invented. Each level is a Beta posterior whose prior mean is the level above
it, so evidence about a model on any kind informs the kind, and evidence about
the kind informs the exact level, and the deepest level that has real rows is
what the answer ends up being made of. `basis` says which level that was, so a
caller can tell a measured answer from a plausible one.

That hierarchy is about success. What an attempt costs is borrowed on the same
principle one tier shallower: a row's token counts and its elapsed time are
divided by the factors of the level they ran at before they are pooled, so a
model's rows for a kind are one sample at the `medium` baseline whatever level
each of them was taken at, and the pooled figure is scaled back up to the level
being asked about. An exact-cell tier in front of that would undo it — the level
holding rows would answer from those rows alone, at whatever baseline they were
taken, and the level beside it would be forecast the same appetite for nothing.

A parent is fitted on the rows its child does not hold, and only on those. It
is a prior for what it can still add, and rows the child is already counting
are not that: counted again at each level, one point's handful of failures
compounds into a confidence about the whole model that the handful never bought.
A level left with no rows of its own passes its own prior down unchanged, which
is the same statement — it knew nothing the child did not.

The bottom of the stack is capability against difficulty, with the level of
deliberation counted as capability the model can be lent: a point far more
capable than the kind is hard usually succeeds, and that is the sigmoid the
whole hierarchy shrinks towards when nothing has ever been measured. The lent
capability is not free — a more deliberate attempt runs longer and reasons
harder, and `data/kinds.json` says by how much — which is what stops the
arithmetic from buying the top of the ladder for every piece of work.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from collections.abc import Collection, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager, suppress
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

from catalogue import LEVELS, TOKEN_CATEGORIES, Catalogue

# The work this Skill knows how to route. A kind outside this set is a kind
# nobody has written a difficulty or a token prior for, so it is rejected at
# the door rather than estimated from nothing.
DEFAULT_DATA_DIR = Path.home() / ".kntnt" / "model-selector"

KINDS = (
    "mechanical",
    "implement",
    "design",
    "debug",
    "review",
    "analyze",
    "prose",
    "converse",
)

# Who decided the grade. Kept as vocabulary rather than as a constraint: a
# caller that files a grade from an unknown judge is still filing evidence.
GRADED_BY = ("checker", "judge", "signal", "user")

# How an estimate was arrived at, strongest first. "inherit" is not produced
# here; it is what a caller reports when it declined to choose at all.
BASIS = ("measured", "pooled", "prior", "inherit")

MEASUREMENTS_FILE = "measurements.jsonl"
KINDS_FILE = "kinds.json"

# Where the Units seen and not yet graded wait. The name is capture's, which
# appends to the file; it is read here as an on-disk contract rather than
# imported, the posture every consumer of this Skill's stores takes.
PENDING_FILE = "pending.jsonl"

# The lock a pass holds while it rewrites the ledger or the pending store:
# grading, and the catalogue pass deleting the rows of a model that is gone.
# A lock older than any pass can legitimately take belonged to a process that
# died. Fifteen minutes is longer than any pass can legitimately take.
LOCK_FILE = "grade.lock"
LOCK_STALE_SECONDS = 900.0

# How much a level's parent is worth, in attempts, when that level is being
# fitted. The key names the parent: a model's own pooled record is worth two
# attempts against the sigmoid it started from, and an exact cell needs six
# attempts of its own before it stops mostly repeating the kind it belongs to.
# Deeper cells shrink harder because they are the ones with the fewest rows.
PSEUDO = {3: 2.0, 2: 4.0, 1: 6.0}

# How many rows a level needs before an answer counts as measured rather than
# as pooled. Three is the point where a run of luck stops being the whole
# sample without demanding a study nobody will ever run.
ENOUGH = 3

# The quantile `low` reports. A tenth percentile is pessimistic enough that an
# untried point cannot present itself as a sure thing, and generous enough
# that three good attempts are allowed to mean something.
LOW_QUANTILE = 0.10

# How sharply capability has to exceed difficulty before success is likely.
# Eight puts the half-way point exactly where the two are equal and saturates
# within about a quarter of the scale either side of it.
SHARPNESS = 8.0

# What a model with no measured capability is assumed to be: exactly as
# capable as the median kind is hard, which is a coin flip and reads as one.
UNKNOWN_CAPABILITY = 0.5

# What a kind with no shipped difficulty is assumed to be. Same reasoning.
UNKNOWN_DIFFICULTY = 0.5

# How far from certainty a mean is held before its log-odds are taken. A cell
# of four failures has a mean the log-odds cannot represent, and a translated
# certainty is a certainty either way, so the clamp costs nothing real.
CERTAINTY = 1e-6

# How far a measurement is carried when it is carried across kinds, and away
# from what the new kind's own difficulty predicts. Moving an estimate between
# deliberation levels of one model is only restating what the shipped level
# table already claims, and moves at the prior's own rate. Moving it between
# kinds is a different and much weaker claim — that rows taken at one difficulty
# predict another they never ran at — and unbounded it turns seven rows of
# failure on hard work into near-certainty on easy work. So a move that leaves
# the estimate further from what the difficulty predicts goes at half the rate
# and stops after this much log-odds. A move that leaves it nearer is the
# conservative direction, asserts nothing the difficulty had not already said,
# and is taken whole.
CROSS_KIND_SHARPNESS = 4.0
CROSS_KIND_LIMIT = 1.5

# How long an attempt at a kind the shipped file does not describe is assumed
# to take. The order of magnitude of a delegated job rather than of a question.
UNKNOWN_SECONDS = 900.0

# The token prior for a kind the shipped file does not describe. Deliberately
# the shape of a small delegated attempt rather than a zero, because a zero
# would price an unknown kind as free and make it win every comparison.
UNKNOWN_TOKENS = {
    "input": 600.0,
    "cache_read": 1_600_000.0,
    "cache_write": 180_000.0,
    "output": 16_000.0,
    "reasoning": 8_000.0,
}

# What one step of deliberation is worth, and what it costs, when the shipped
# file says nothing. The three numbers per level are the same three the file
# carries: how much apparent capability the level buys, how much longer the
# attempt runs, and how much harder it thinks while it runs.
UNKNOWN_DELIBERATION = {
    "capability_bonus": 0.0,
    "tokens": 1.0,
    "reasoning": 1.0,
}


@dataclass(frozen=True)
class Measurement:
    """One graded attempt, as it is stored and as it is read back."""

    attempt_id: str
    at: str
    kind: str
    label: str | None
    model: str
    deliberation: str | None
    harness: str | None
    channel: str | None
    grade: float
    graded_by: str
    tokens: dict[str, float | None]
    cost_usd: float | None
    seconds: float | None
    routed: bool


# Exactly the fields a stored row may carry. Derived from the dataclass rather
# than typed out again, so that the store and the type cannot drift apart.
ALLOWED_FIELDS: frozenset[str] = frozenset(field.name for field in fields(Measurement))


@dataclass(frozen=True)
class Discarded:
    """How many measurement rows and pending Units `discard_models` deleted, per model."""

    rows: dict[str, int]
    units: dict[str, int]


@dataclass(frozen=True)
class AppendReport:
    """What became of each row handed to `append`, and why."""

    accepted: list[tuple[str, str]]
    merged: list[tuple[str, str]]
    rejected: list[tuple[str, str]]


@dataclass(frozen=True)
class Estimate:
    """One belief about one cell: its mean, its floor, and where it came from.

    The Beta those first two are read off travels with them, because a caller
    that means to try this cell rather than rank it needs the distribution and
    not a summary of it.
    """

    mean: float
    low: float
    n: float
    basis: str
    alpha: float
    beta: float

    def draw(self, quantile: float) -> float:
        """Return this cell's success rate read off at one quantile of its Beta.

        The answer is ranked on the means, so nothing read off here decides an
        ordinary call. What spends a quantile is the bounded exploration in
        `selection.py`: on about one reversible call in ten a candidate cheaper
        than the answer is tried where its own posterior says it could still do
        the job. A cell measured a handful of times is wide enough to be tried,
        so the rows that would settle it can be taken; a cell that is
        confidently worse essentially never is, without anybody having had to
        define hopeless.

        Sampling is by inverse transform — a quantile in, a rate out — rather
        than by drawing a Beta variate, because the generator then stays the
        caller's: it decides how many quantiles an experiment spends and on
        what. An exploration spends a fresh one on each candidate it considers,
        which is what leaves the candidates independent of one another rather
        than moved together by a single roll.
        """

        return _beta_quantile(self.alpha, self.beta, quantile)


@dataclass(frozen=True)
class KindPriors:
    """What each kind demands of a model, and what it costs to attempt.

    `notes` is the one sentence that tells each kind from the other seven. It
    buys the arithmetic nothing and is carried anyway, because whoever
    classifies the work — a person reading this Skill, or a caller that cannot
    read it at all — needs the vocabulary and its distinctions from one place.
    """

    difficulties: Mapping[str, float]
    token_priors: Mapping[str, Mapping[str, float]]
    deliberation: Mapping[str, Mapping[str, float]]
    long_contexts: Mapping[str, bool]
    elapsed: Mapping[str, float]
    notes: Mapping[str, str]
    problem: str | None

    def seconds(self, kind: str, deliberation: str | None = None) -> float:
        """Return how long one attempt of this kind is expected to take.

        Scaled up the deliberation ladder by the same factor the token prior
        is, a more deliberate attempt taking longer for the same reason it
        spends more.
        """

        base = self.elapsed.get(kind, UNKNOWN_SECONDS)
        return base * self.factor(deliberation, "seconds")

    def difficulty(self, kind: str) -> float:
        """Return how much intelligence *kind* needs, on the capability scale."""

        return self.difficulties.get(kind, UNKNOWN_DIFFICULTY)

    def long_context(self, kind: str) -> bool:
        """Return whether work of this kind normally runs at repo scale.

        This is what `catalogue.cost_usd` prices a vendor's context cliff from,
        the kind standing in for a context size no unstarted attempt has yet.
        """

        return self.long_contexts.get(kind, False)

    def bonus(self, deliberation: str | None) -> float:
        """Return the apparent capability one level of deliberation buys.

        Deliberation is the other half of the choice this Skill makes, and an
        estimate blind to it would rate a model's cheapest level exactly as
        highly as its most careful one — at which point the answer to *how hard
        should it think* is always *as little as possible*.
        """

        return self._level(deliberation)["capability_bonus"]

    def factor(self, deliberation: str | None, category: str) -> float:
        """Return what one level multiplies one category of cost by.

        The reasoning category has a factor of its own, a more deliberate
        attempt thinking disproportionately harder rather than merely longer;
        every other token category, and the elapsed time with them, scales
        with `tokens`. These are also the two numbers a measurement is divided
        by to read it back to the `medium` baseline, which is what lets a row
        taken at one level say anything about the other four.
        """

        level = self._level(deliberation)
        return level["reasoning"] if category == "reasoning" else level["tokens"]

    def tokens(self, kind: str, deliberation: str | None = None) -> dict[str, float]:
        """Return the per-attempt token prior, scaled to the level asked for.

        A more deliberate attempt runs longer and thinks much harder, so it
        reads and writes proportionally more and reasons disproportionately
        more. That is what makes a level cost something: without it the
        arithmetic would buy the top of the ladder every time, the extra
        capability being free.
        """

        prior = self.token_priors.get(kind, {})
        scaled: dict[str, float] = {}
        for category in TOKEN_CATEGORIES:
            base = float(prior.get(category, UNKNOWN_TOKENS[category]))
            scaled[category] = base * self.factor(deliberation, category)
        return scaled

    def _level(self, deliberation: str | None) -> Mapping[str, float]:
        """Return one level's three numbers, defaulting to a neutral level."""

        if deliberation is None:
            return UNKNOWN_DELIBERATION
        return self.deliberation.get(deliberation, UNKNOWN_DELIBERATION)


def load_kinds(here: Path) -> KindPriors:
    """Read the shipped per-kind difficulties and token priors.

    A file that will not parse leaves every kind on the neutral defaults and
    says so, because an estimator that refuses to run is worse for the caller
    than one that admits it is guessing.
    """

    path = here / "data" / KINDS_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as problem:
        return KindPriors(
            {}, {}, {}, {}, {}, {}, f"{path} could not be read: {problem}"
        )

    entries = raw.get("kinds") if isinstance(raw, dict) else None
    if not isinstance(entries, dict):
        return KindPriors({}, {}, {}, {}, {}, {}, f"{path} carries no kinds object")

    difficulties: dict[str, float] = {}
    token_priors: dict[str, dict[str, float]] = {}
    long_contexts: dict[str, bool] = {}
    elapsed: dict[str, float] = {}
    notes: dict[str, str] = {}
    for kind, entry in entries.items():
        if not isinstance(kind, str) or not isinstance(entry, dict):
            continue
        difficulty = _number(entry.get("difficulty"))
        if difficulty is not None:
            difficulties[kind] = min(1.0, max(0.0, difficulty))
        token_priors[kind] = _token_map(entry.get("tokens"))
        long_contexts[kind] = bool(entry.get("long_context"))
        taken = _number(entry.get("seconds"))
        if taken is not None and taken > 0.0:
            elapsed[kind] = taken
        told = entry.get("note")
        if isinstance(told, str) and told.strip():
            notes[kind] = told.strip()

    return KindPriors(
        difficulties,
        token_priors,
        _deliberation_table(raw.get("deliberation")),
        long_contexts,
        elapsed,
        notes,
        None,
    )


def _deliberation_table(raw: Any) -> dict[str, dict[str, float]]:
    """Return what each level of deliberation buys and costs, as shipped."""

    given = raw if isinstance(raw, dict) else {}
    table: dict[str, dict[str, float]] = {}
    for level in LEVELS:
        entry = given.get(level)
        entry = entry if isinstance(entry, dict) else {}
        table[level] = {
            name: _number(entry.get(name)) or default
            for name, default in UNKNOWN_DELIBERATION.items()
        }
    return table


def append(data_dir: Path, rows: Sequence[Mapping[str, Any]]) -> AppendReport:
    """Add rows to the ledger, reporting what was taken, folded and refused.

    Every row is rebuilt onto the allowed field names rather than written
    through, so a caller's extra keys never reach the file and nothing has to
    be stripped out of it afterwards. An attempt id the store already holds is
    merged into the row it holds rather than added beside it: one attempt is
    one row however many sides of a run file about it, and re-running a filing
    is how a caller recovers from a crash (issue #291).
    """

    report = AppendReport([], [], [])
    held = {row.attempt_id: asdict(row) for row in load(data_dir)}
    folded: dict[str, dict[str, Any]] = {}
    fresh: dict[str, dict[str, Any]] = {}

    for index, row in enumerate(rows):
        attempt_id = _text(row.get("attempt_id")) or f"row {index}"
        problem = _rejection(row)
        if problem is not None:
            report.rejected.append((attempt_id, problem))
            continue

        stored = _stored(row)
        if attempt_id in fresh:
            # Both sides of one attempt arrived in the same call, so the row
            # this call is about to write is the one that is folded into.
            fresh[attempt_id] = _merged(fresh[attempt_id], stored)
            report.merged.append((attempt_id, "folded into the row filed beside it"))
        elif attempt_id in held:
            held[attempt_id] = _merged(held[attempt_id], stored)
            folded[attempt_id] = held[attempt_id]
            report.merged.append((attempt_id, "folded into the row the store held"))
        else:
            fresh[attempt_id] = stored
            report.accepted.append((attempt_id, "appended"))

    if folded:
        _refold(data_dir / MEASUREMENTS_FILE, folded)
    if fresh:
        _append_lines(
            data_dir / MEASUREMENTS_FILE, [_line(row) for row in fresh.values()]
        )
    return report


def _merged(held: Mapping[str, Any], new: Mapping[str, Any]) -> dict[str, Any]:
    """Fold a second filing of one attempt into the row already held.

    Two sides of a run see two halves of one build. A caller's verdict knows
    the grade and the kind of work and nothing about what the attempt spent;
    a read of that builder's own transcript knows what it spent and can only
    grade it from a judge or a signal. Neither is a second attempt, so what is
    kept is the union: every measurement either side actually made, and the
    grade of whichever authority stands higher (issue #291).
    """

    merged = dict(held)

    # What the environment exposed to one side and not the other. A null is an
    # absence rather than a zero everywhere in this store, so a value only ever
    # fills one — nothing measured is overwritten by nothing measured.
    for name in ("cost_usd", "seconds", "harness", "channel"):
        if merged.get(name) is None:
            merged[name] = new.get(name)
    merged["tokens"] = {
        category: (
            counted
            if (counted := _token_counts(held.get("tokens")).get(category)) is not None
            else _token_counts(new.get("tokens")).get(category)
        )
        for category in TOKEN_CATEGORIES
    }

    # The grade of the higher authority, and the reading of the work that came
    # with it. A checker saw the finished work against what was asked for; a
    # judge saw two excerpts of it. Where the two disagree about what the work
    # even was, the kind travels with the grade that is worth more.
    if _authority(new) < _authority(held):
        merged |= {name: new.get(name) for name in ("grade", "graded_by", "kind")}
        merged["routed"] = bool(new.get("routed"))
        merged["label"] = new.get("label")
    if merged.get("label") is None:
        merged["label"] = held.get("label") or new.get("label")

    # The Seat the transcript read is the Seat that ran, whatever was asked
    # for: a launch the environment could not honour serves another point
    # without telling the caller that decided it.
    transcript = _transcript_row(held, new)
    if transcript is not None and held.get("model") and new.get("model"):
        merged["model"] = transcript.get("model")
        merged["deliberation"] = transcript.get("deliberation")

    moments = [
        moment
        for moment in (_text(held.get("at")), _text(new.get("at")))
        if moment is not None
    ]
    if moments:
        merged["at"] = min(moments)
    return merged


def _authority(row: Mapping[str, Any]) -> int:
    """Return where a row's grade stands in `GRADED_BY`, weakest last."""

    graded_by = str(row.get("graded_by") or "")
    return GRADED_BY.index(graded_by) if graded_by in GRADED_BY else len(GRADED_BY)


def _transcript_row(
    held: Mapping[str, Any], new: Mapping[str, Any]
) -> Mapping[str, Any] | None:
    """Return whichever of the two rows read the attempt's own transcript.

    A judge and a signal both grade a Unit that was read off a transcript; a
    checker and a user grade the finished work from outside it. Where exactly
    one of the two rows is such a reading, it is the one that knows which
    point actually ran.
    """

    readings = [
        row for row in (held, new) if row.get("graded_by") in ("judge", "signal")
    ]
    return readings[0] if len(readings) == 1 else None


def _line(row: Mapping[str, Any]) -> str:
    """Return one row as the ledger writes it."""

    return json.dumps(row, separators=(",", ":"), sort_keys=True)


def load(data_dir: Path) -> list[Measurement]:
    """Read every usable row from the ledger, ignoring the rest.

    A line that will not parse is a line somebody's editor mangled, not a
    reason to lose the thousand rows around it.
    """

    path = data_dir / MEASUREMENTS_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return []

    rows: list[Measurement] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except ValueError:
            continue
        if isinstance(raw, dict) and (row := _measurement(raw)) is not None:
            rows.append(row)
    return rows


class Estimator:
    """Beliefs about unmeasured cells, borrowed from the cells around them."""

    def __init__(
        self, rows: Sequence[Measurement], cat: Catalogue, kinds: KindPriors
    ) -> None:
        self._rows = tuple(rows)
        self._kinds = kinds
        self._capability = {model.id: model.capability for model in cat.models}

    def p_success(self, kind: str, model: str, deliberation: str | None) -> Estimate:
        """Return the chance this point comes back good, and how sure that is."""

        exact, by_kind, by_model = self._levels(kind, model, deliberation)

        # What each level knows that the level below it does not. A parent is
        # only a prior for what it can still tell its child, so it is fitted on
        # the rows the child does not already hold: without that the same rows
        # are asserted once per level, and four failures at one point compound
        # into a certainty about the model that four observations cannot buy.
        other_levels = [row for row in by_kind if row.deliberation != deliberation]
        other_kinds = [row for row in by_model if row.kind != kind]

        # Where each level's evidence actually stands. A level's rows ran under
        # their own conditions, not under the ones being asked about: the rows
        # left to the model span every other kind it has attempted, and the ones
        # left to the kind span every other level it was attempted at.
        here = self._margin(kind, model, deliberation)
        at_model = self._mean_margin(other_kinds, model, here)
        at_kind = self._mean_margin(other_levels, model, here)

        # Top down: the sigmoid seeds the model, the model seeds the kind, and
        # the kind seeds the exact cell. Each level is a Beta posterior fitted
        # in its own conditions, and each is translated into the conditions of
        # the level beneath it before it is used there as a prior. Without that
        # translation a model measured on hard work would carry that verdict
        # unchanged onto easy work, and a model measured at one level of
        # deliberation would report the same number for all five of them.
        prior = _sigmoid(SHARPNESS * at_model)
        pooled_model = _posterior_mean(other_kinds, prior, PSEUDO[3])
        pooled_kind = _posterior_mean(
            other_levels,
            _translated(
                pooled_model,
                at_kind - at_model,
                toward=_sigmoid(SHARPNESS * at_kind),
            ),
            PSEUDO[2],
        )
        alpha, beta = _posterior(
            exact, _translated(pooled_kind, here - at_kind), PSEUDO[1]
        )

        basis = "prior"
        if len(exact) >= ENOUGH:
            basis = "measured"
        elif len(by_kind) >= ENOUGH or len(by_model) >= ENOUGH:
            basis = "pooled"

        deepest = exact or by_kind or by_model
        return Estimate(
            mean=alpha / (alpha + beta),
            low=_beta_quantile(alpha, beta, LOW_QUANTILE),
            n=float(len(deepest)),
            basis=basis,
            alpha=alpha,
            beta=beta,
        )

    def tokens(
        self, kind: str, model: str, deliberation: str | None
    ) -> dict[str, float]:
        """Return the per-attempt token count this point is expected to burn.

        Category by category, because a store that measured output and never
        recorded cache reads should not be allowed to report a cache read of
        zero — that is the one error that would understate a bill by two
        orders of magnitude. An unmeasured category falls back to the kind's
        shipped prior instead.

        Every measurement is read at the `medium` baseline and the pooled
        answer scaled to the level asked for, so a model's rows for a kind
        price all five of its levels and the ladder's cost survives having
        been measured at one rung of it.
        """

        _, by_kind, by_model = self._levels(kind, model, deliberation)
        prior = self._kinds.tokens(kind, deliberation)

        counted: dict[str, float] = {}
        for category in TOKEN_CATEGORIES:
            counted[category] = prior[category]
            for group in (by_kind, by_model):
                measured = _geometric_mean(self._normalised(group, category))
                if measured is not None:
                    counted[category] = measured * self._kinds.factor(
                        deliberation, category
                    )
                    break
        return counted

    def seconds(self, kind: str, model: str, deliberation: str | None) -> float:
        """Return how long this point is expected to take to finish an attempt.

        The same two tiers the token forecast backs off through, and the same
        normalisation, over the one measurement a run started for time is
        ordered on. A store with no elapsed time for this point falls back to
        the kind's shipped figure rather than to a zero, a zero being the
        fastest thing on any list.
        """

        _, by_kind, by_model = self._levels(kind, model, deliberation)
        for group in (by_kind, by_model):
            measured = _geometric_mean(self._elapsed(group))
            if measured is not None:
                return measured * self._kinds.factor(deliberation, "seconds")
        return self._kinds.seconds(kind, deliberation)

    def _levels(
        self, kind: str, model: str, deliberation: str | None
    ) -> tuple[list[Measurement], list[Measurement], list[Measurement]]:
        """Return the exact, kind-wide and model-wide rows, in that order."""

        by_model = [row for row in self._rows if row.model == model]
        by_kind = [row for row in by_model if row.kind == kind]
        exact = [row for row in by_kind if row.deliberation == deliberation]
        return exact, by_kind, by_model

    def _normalised(self, rows: Iterable[Measurement], category: str) -> list[float]:
        """Return one category's measurements, each read back to `medium`.

        A row's counts are what its own level of deliberation made of them, so
        dividing by that level's factor is what leaves rows taken at different
        levels one sample — and what lets the level being asked about put its
        own factor back on the pooled figure. A row that ran on a model with no
        effort control ran at factor one and is left alone.
        """

        counted: list[float] = []
        for row in rows:
            value = row.tokens.get(category)
            if value is not None and value > 0.0:
                counted.append(value / self._kinds.factor(row.deliberation, category))
        return counted

    def _elapsed(self, rows: Iterable[Measurement]) -> list[float]:
        """Return every measured runtime, read back to `medium` the same way."""

        return [
            row.seconds / self._kinds.factor(row.deliberation, "seconds")
            for row in rows
            if row.seconds is not None and row.seconds > 0.0
        ]

    def _margin(self, kind: str, model: str, deliberation: str | None) -> float:
        """Return how far this point's capability exceeds what the kind demands.

        The one number every level of the hierarchy is comparable in. Put
        through the sigmoid it is the untried-cell prior; as a difference
        between two cells it is how far a verdict about one has to be moved
        before it says anything about the other.
        """

        capability = self._capability.get(model)
        if capability is None:
            capability = UNKNOWN_CAPABILITY
        return (
            capability + self._kinds.bonus(deliberation) - self._kinds.difficulty(kind)
        )

    def _mean_margin(
        self, rows: Sequence[Measurement], model: str, fallback: float
    ) -> float:
        """Return the conditions a level's rows stand at, on average.

        A level with no rows of its own stands nowhere, so it stands where the
        question does: the fallback makes every translation an identity when
        nothing has been measured, which is what leaves an untouched store
        answering exactly from its priors.
        """

        if not rows:
            return fallback
        return sum(
            self._margin(row.kind, model, row.deliberation) for row in rows
        ) / len(rows)


def _rejection(row: Mapping[str, Any]) -> str | None:
    """Return why *row* may not be stored, or None where it may."""

    if not _text(row.get("attempt_id")):
        return "no attempt_id, so the row cannot be deduplicated"

    kind = row.get("kind")
    if kind not in KINDS:
        return f"kind {kind!r} is not one this Skill routes"

    grade = _number(row.get("grade"))
    if grade is None or not 0.0 <= grade <= 1.0:
        return f"grade {row.get('grade')!r} is not a number in 0..1"

    deliberation = row.get("deliberation")
    if deliberation is not None and deliberation not in LEVELS:
        return f"deliberation {deliberation!r} is not a level"

    # Who judged the work decides how much the grade is worth, so a row that
    # names no recognised authority is a grade with nothing behind it.
    if row.get("graded_by") not in GRADED_BY:
        return f"graded_by {row.get('graded_by')!r} is not an authority"

    return None


def _stored(row: Mapping[str, Any]) -> dict[str, Any]:
    """Copy *row* onto the allowed fields, and onto nothing else."""

    stored: dict[str, Any] = {}
    for field in sorted(ALLOWED_FIELDS):
        if field == "tokens":
            stored[field] = _token_counts(row.get("tokens"))
            continue
        stored[field] = row.get(field)
    stored["routed"] = bool(row.get("routed"))
    return stored


def _append_lines(path: Path, lines: list[str]) -> None:
    """Append complete lines to the ledger, creating it where it is missing."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        for line in lines:
            stream.write(f"{line}\n")


def _refold(path: Path, folded: Mapping[str, dict[str, Any]]) -> None:
    """Rewrite the ledger with each folded row in the place it already had.

    Line by line rather than row by row: a line this module cannot parse is a
    line somebody's editor mangled, and a rewrite that dropped it would lose
    it for good — so everything the fold does not name is carried across
    exactly as it stands. Written through a temporary sibling and an atomic
    rename, as every store here is written, so an interrupted fold leaves the
    ledger it started from rather than half of one.
    """

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return

    kept: list[str] = []
    for line in text.splitlines():
        try:
            raw = json.loads(line)
        except ValueError:
            kept.append(line)
            continue
        identity = _text(raw.get("attempt_id")) if isinstance(raw, dict) else None
        replacement = folded.get(identity) if identity is not None else None
        kept.append(_line(replacement) if replacement is not None else line)

    staged = path.parent / f"{path.name}.tmp"
    staged.write_text("".join(f"{line}\n" for line in kept), encoding="utf-8")
    staged.replace(path)


@contextmanager
def lock(data_dir: Path, name: str = LOCK_FILE) -> Iterator[bool]:
    """Hold one lock for the length of one pass, or yield False.

    Two passes rewriting the same files at once would each write back what
    the other had just changed, so the second one does nothing at all rather
    than doing it twice. A lock older than any pass can legitimately take
    belonged to a process that died and is taken over. Capture appends to the
    pending store without it, which is why a pass that deletes rows for a
    model has to repeat the deletion on every later pass.

    *name* is the lock's file in *data_dir*: the ledger's own by default, and
    `refresh.lock` for the catalogue pass as a whole, which takes the ledger's
    as well where it deletes rows.
    """

    path = data_dir / name
    data_dir.mkdir(parents=True, exist_ok=True)

    with suppress(OSError):
        held = time.time() - path.stat().st_mtime
        if held > LOCK_STALE_SECONDS:
            path.unlink(missing_ok=True)

    try:
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except OSError:
        yield False
        return

    os.close(handle)
    try:
        yield True
    finally:
        path.unlink(missing_ok=True)


def discard_models(data_dir: Path, models: Collection[str]) -> Discarded:
    """Delete every measurement row and pending Unit of *models*, and count them.

    For a model its maker no longer lists: it does not come back, and its
    rows are worth nothing to a selection that can no longer choose it. A row
    or Unit belongs to a model by exact id, which is what the store holds and
    what the estimator matches on. Both files are rewritten as `_refold`
    rewrites the ledger — every line this does not delete carried across as
    it stands, an unparsable one included, through a sibling and an atomic
    rename — and a file holding none of *models* is not rewritten at all. The
    caller holds `lock`.
    """

    wanted = frozenset(models)
    return Discarded(
        _without(data_dir / MEASUREMENTS_FILE, wanted),
        _without(data_dir / PENDING_FILE, wanted),
    )


def _without(path: Path, models: frozenset[str]) -> dict[str, int]:
    """Rewrite one JSON Lines store without the rows of *models*, counting each model's."""

    if not models:
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return {}

    kept: list[str] = []
    deleted: dict[str, int] = {}
    for line in text.splitlines():
        try:
            raw = json.loads(line)
        except ValueError:
            kept.append(line)
            continue
        model = raw.get("model") if isinstance(raw, dict) else None
        if isinstance(model, str) and model in models:
            deleted[model] = deleted.get(model, 0) + 1
            continue
        kept.append(line)

    if deleted:
        staged = path.parent / f"{path.name}.tmp"
        staged.write_text("".join(f"{line}\n" for line in kept), encoding="utf-8")
        staged.replace(path)
    return deleted


def _measurement(raw: Mapping[str, Any]) -> Measurement | None:
    """Build one measurement from one stored line, or None where it is unusable."""

    attempt_id = _text(raw.get("attempt_id"))
    model = _text(raw.get("model"))
    grade = _number(raw.get("grade"))
    if attempt_id is None or model is None or grade is None:
        return None
    if raw.get("kind") not in KINDS or not 0.0 <= grade <= 1.0:
        return None

    deliberation = _text(raw.get("deliberation"))
    return Measurement(
        attempt_id=attempt_id,
        at=_text(raw.get("at")) or "",
        kind=str(raw.get("kind")),
        label=_text(raw.get("label")),
        model=model,
        deliberation=deliberation if deliberation in LEVELS else None,
        harness=_text(raw.get("harness")),
        channel=_text(raw.get("channel")),
        grade=grade,
        graded_by=_text(raw.get("graded_by")) or "signal",
        tokens=_token_counts(raw.get("tokens")),
        cost_usd=_number(raw.get("cost_usd")),
        seconds=_number(raw.get("seconds")),
        routed=bool(raw.get("routed")),
    )


def _posterior(
    rows: Sequence[Measurement], parent_mean: float, weight: float
) -> tuple[float, float]:
    """Return the Beta parameters for *rows* shrunk towards *parent_mean*.

    A grade is a fractional success rather than a coin flip, so an attempt
    graded 0.7 contributes 0.7 to alpha and 0.3 to beta. That is what lets a
    judge's partial credit inform the same arithmetic as a checker's pass.
    """

    successes = sum(row.grade for row in rows)
    failures = sum(1.0 - row.grade for row in rows)
    return successes + weight * parent_mean, failures + weight * (1.0 - parent_mean)


def _posterior_mean(
    rows: Sequence[Measurement], parent_mean: float, weight: float
) -> float:
    """Return just the mean of the posterior `_posterior` describes."""

    alpha, beta = _posterior(rows, parent_mean, weight)
    return alpha / (alpha + beta)


def _sigmoid(x: float) -> float:
    """Return the logistic of *x*, the shape every estimate in here has."""

    return 1.0 / (1.0 + math.exp(-x))


def _translated(mean: float, margin: float, *, toward: float | None = None) -> float:
    """Move a mean by *margin* worth of conditions, in log-odds.

    Log-odds is where the sigmoid is linear, so moving an estimate there says
    what the difference between the two cells is worth and nothing about the
    rest of it: the measurement is kept and only its conditions change. Between
    two levels of one model that is the shipped level table restated, and it
    moves at the prior's own rate, which is what `toward` being None asks for.

    Between two kinds it is an extrapolation to a difficulty the rows never ran
    at, and *toward* is what this kind's own difficulty predicts of this model
    with no rows at all. The damping is asymmetric, because the two directions
    are not the same claim. A move that lands nearer that prediction asserts
    nothing the difficulty did not already say, so there is nothing to protect
    against and it is taken whole; a move that lands further away is the claim
    the damping exists for, and is damped and bounded. Bounding both alike is
    what made a model flawless at trivial work read as near-certain at hard
    work — the cap refused to let the estimate fall as far as the difficulty
    said it should — and it condemned a model on work it had never been asked
    to do for the same reason in reverse.
    """

    held = min(1.0 - CERTAINTY, max(CERTAINTY, mean))
    odds = math.log(held / (1.0 - held))
    whole = _sigmoid(odds + SHARPNESS * margin)
    if toward is None or abs(whole - toward) < abs(held - toward):
        return whole

    shift = CROSS_KIND_SHARPNESS * margin
    return _sigmoid(odds + min(CROSS_KIND_LIMIT, max(-CROSS_KIND_LIMIT, shift)))


def _geometric_mean(values: Sequence[float]) -> float | None:
    """Return the geometric mean, or None where nothing was measured.

    Geometric because token counts span orders of magnitude within one kind:
    one exploratory attempt that read half a repository would drag an
    arithmetic mean past everything else in the sample.
    """

    if not values:
        return None
    return math.exp(sum(math.log(value) for value in values) / len(values))


def _beta_quantile(alpha: float, beta: float, quantile: float) -> float:
    """Return the value below which *quantile* of the Beta mass lies.

    Bisection on the regularised incomplete beta function, at every sample
    size rather than switching to a normal approximation past some count: the
    interesting cells here are the ones with two or three rows, where a normal
    approximation is worst, and fifty bisections of a monotone function cost
    nothing next to the attempt being estimated.
    """

    low, high = 0.0, 1.0
    for _ in range(60):
        middle = (low + high) / 2.0
        if _beta_cdf(alpha, beta, middle) < quantile:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def _beta_cdf(alpha: float, beta: float, x: float) -> float:
    """Return the regularised incomplete beta function I_x(alpha, beta)."""

    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0

    front = math.exp(
        math.lgamma(alpha + beta)
        - math.lgamma(alpha)
        - math.lgamma(beta)
        + alpha * math.log(x)
        + beta * math.log1p(-x)
    )

    # The continued fraction converges quickly only on its own side of the
    # distribution's mode, so the far tail is computed as the near tail of the
    # mirrored distribution.
    if x < (alpha + 1.0) / (alpha + beta + 2.0):
        return front * _beta_fraction(alpha, beta, x) / alpha
    return 1.0 - front * _beta_fraction(beta, alpha, 1.0 - x) / beta


def _beta_fraction(alpha: float, beta: float, x: float) -> float:
    """Evaluate the incomplete beta continued fraction by Lentz's method."""

    tiny = 1e-30
    c = 1.0
    d = 1.0 - (alpha + beta) * x / (alpha + 1.0)
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    fraction = d

    for i in range(1, 200):
        even = 2 * i
        numerator = i * (beta - i) * x / ((alpha + even - 1.0) * (alpha + even))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        fraction *= d * c

        numerator = (
            -(alpha + i)
            * (alpha + beta + i)
            * x
            / ((alpha + even) * (alpha + even + 1.0))
        )
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        step = d * c
        fraction *= step

        if abs(step - 1.0) < 1e-12:
            break

    return fraction


def _token_counts(raw: Any) -> dict[str, float | None]:
    """Return the five token categories, each a number or an admitted absence."""

    given = raw if isinstance(raw, dict) else {}
    return {category: _number(given.get(category)) for category in TOKEN_CATEGORIES}


def _token_map(raw: Any) -> dict[str, float]:
    """Return a shipped token prior, dropping anything that is not a number."""

    given = raw if isinstance(raw, dict) else {}
    counted: dict[str, float] = {}
    for category in TOKEN_CATEGORIES:
        value = _number(given.get(category))
        if value is not None:
            counted[category] = value
    return counted


def _text(raw: Any) -> str | None:
    """Return a non-empty string, or None for anything else including null."""

    return raw if isinstance(raw, str) and raw.strip() else None


def _number(raw: Any) -> float | None:
    """Return a finite float, or None for anything that is not one."""

    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    value = float(raw)
    return value if math.isfinite(value) else None


def summary(data_dir: Path, kind: str | None = None) -> dict[str, Any]:
    """Return what has been measured, grouped by the identity of a measurement.

    A caller that wanted this had to read the whole store and aggregate it by
    hand, which is a large number of lines through somebody's context window
    to answer a question about counts. Kind, model and deliberation are the
    whole of a measurement's identity, so they are the whole of the grouping.
    """

    rows = [row for row in load(data_dir) if kind is None or row.kind == kind]
    groups: dict[tuple[str, str, str | None], list[Measurement]] = {}
    for row in rows:
        groups.setdefault((row.kind, row.model, row.deliberation), []).append(row)

    reported = [
        _group(identity, members)
        for identity, members in sorted(groups.items(), key=_group_order)
    ]
    instants = sorted(row.at for row in rows if row.at)
    return {
        "rows": len(rows),
        "kind": kind,
        "earliest": instants[0] if instants else None,
        "latest": instants[-1] if instants else None,
        "groups": reported,
    }


def _group_order(
    item: tuple[tuple[str, str, str | None], list[Measurement]],
) -> tuple[str, str, str]:
    """Order groups by kind, then model, then position on the scale."""

    kind, model, deliberation = item[0]
    return (kind, model, f"{_position(deliberation):02d}")


def _position(deliberation: str | None) -> int:
    """Return the scale position, with no control at all sorting first."""

    return LEVELS.index(deliberation) + 1 if deliberation in LEVELS else 0


def _group(
    identity: tuple[str, str, str | None], members: list[Measurement]
) -> dict[str, Any]:
    """Return one group's account, stating an unmeasured figure as absent."""

    kind, model, deliberation = identity
    authorities: dict[str, int] = {}
    for row in members:
        authorities[row.graded_by] = authorities.get(row.graded_by, 0) + 1
    return {
        "kind": kind,
        "model": model,
        "deliberation": deliberation,
        "rows": len(members),
        "grade": round(sum(row.grade for row in members) / len(members), 3),
        "graded_by": dict(sorted(authorities.items())),
        "cost_usd": _mean([row.cost_usd for row in members]),
        "seconds": _mean([row.seconds for row in members]),
        "earliest": min(row.at for row in members),
        "latest": max(row.at for row in members),
    }


def _mean(values: Sequence[float | None]) -> float | None:
    """Return the mean of what was measured, or None where nothing was.

    An absence is never a zero here: a zero is a reading, and reading one off
    an unmeasured configuration is what makes it the cheapest thing on offer.
    """

    known = [value for value in values if value is not None]
    return round(sum(known) / len(known), 4) if known else None


def main(argv: Sequence[str] | None = None) -> int:
    """Print the store's own account as JSON, for the `evidence` command."""

    parser = argparse.ArgumentParser(
        prog="evidence.py", description="Report what this machine has measured."
    )
    parser.add_argument("--data")
    parser.add_argument("kind", nargs="?", choices=KINDS)
    args = parser.parse_args(argv)

    data_dir = Path(args.data).expanduser() if args.data else DEFAULT_DATA_DIR
    print(json.dumps(summary(data_dir, args.kind), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
