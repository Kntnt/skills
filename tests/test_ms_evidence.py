"""The measurement store, and the hierarchy that borrows from it."""

from __future__ import annotations

import importlib.util
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
SHIPPED: Path = REPO_ROOT / "skills" / "models" / "model-selector"
ROUTING: Path = REPO_ROOT / "docs" / "rules" / "routing.md"


def _module(stem: str, name: str | None = None) -> Any:
    """Load one shipped module under the name its siblings import it by."""

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
evidence = _module("evidence")

CAT = catalogue.load(Path("/nowhere"), SHIPPED)
KINDS = evidence.load_kinds(SHIPPED)
LADDER: dict[str, dict[str, float]] = json.loads(
    (SHIPPED / "data" / "kinds.json").read_text(encoding="utf-8")
)["deliberation"]

STRONG = "claude-opus-5"
WEAK = "claude-sonnet-5"


def _row(**overrides: Any) -> dict[str, Any]:
    """Provide one measurement in the shape a caller files it."""

    row: dict[str, Any] = {
        "attempt_id": "ms-20260906-000001",
        "at": "2026-09-06T09:00:00Z",
        "kind": "implement",
        "label": "ticket 42",
        "model": STRONG,
        "deliberation": "high",
        "harness": "claude-code",
        "channel": "anthropic/subscription",
        "grade": 1.0,
        "graded_by": "checker",
        "tokens": {"cache_read": 2_000_000.0, "output": 20_000.0},
        "cost_usd": 1.5,
        "seconds": 900.0,
        "routed": True,
    }
    row.update(overrides)
    return row


def _many(count: int, grade: float, **overrides: Any) -> list[dict[str, Any]]:
    """Provide *count* distinct attempts that were all graded the same."""

    return [
        _row(attempt_id=f"ms-2026-{index:04d}", grade=grade, **overrides)
        for index in range(count)
    ]


def _estimator(rows: list[dict[str, Any]], data_dir: Path) -> Any:
    """File the rows and hand back an estimator reading them."""

    evidence.append(data_dir, rows)
    return evidence.Estimator(evidence.load(data_dir), CAT, KINDS)


def test_a_row_is_rebuilt_onto_the_allowed_fields_and_nothing_else(
    tmp_path: Path,
) -> None:
    """A caller's extra key never reaches the file, so nothing has to strip it."""

    report = evidence.append(tmp_path, [_row(secret="do not store me", cost_usd=None)])

    stored = json.loads((tmp_path / "measurements.jsonl").read_text().splitlines()[0])
    assert [entry[0] for entry in report.accepted] == ["ms-20260906-000001"]
    assert set(stored) == set(evidence.ALLOWED_FIELDS)
    assert stored["tokens"]["cache_write"] is None


def test_a_row_outside_the_vocabulary_is_rejected_with_its_reason(
    tmp_path: Path,
) -> None:
    """Evidence the estimator cannot use is worse than no evidence at all."""

    report = evidence.append(
        tmp_path,
        [
            _row(attempt_id="a", kind="vibes"),
            _row(attempt_id="b", grade=1.4),
            _row(attempt_id="c", deliberation="extreme"),
            _row(attempt_id="d"),
        ],
    )

    assert [entry[0] for entry in report.rejected] == ["a", "b", "c"]
    assert [entry[0] for entry in report.accepted] == ["d"]
    assert all(reason for _, reason in report.rejected)


# What Orchestrate files at the boundary that established an attempt's outcome:
# the verdict's grade, the role's kind, and no tokens at all, because the
# harness it dispatched on exposes none to it (issue #291).
def _checker(**overrides: Any) -> dict[str, Any]:
    """Provide the row a caller's own verdict files about one attempt."""

    return _row(
        graded_by="checker",
        grade=1.0,
        kind="implement",
        label="build",
        routed=True,
        tokens=dict.fromkeys(catalogue.TOKEN_CATEGORIES),
        cost_usd=None,
        seconds=None,
        channel=None,
        **overrides,
    )


# What the capture pass files about the same attempt, having read the
# transcript that build actually ran in: what it spent, and the weaker grade
# whatever decided it could establish.
def _captured(**overrides: Any) -> dict[str, Any]:
    """Provide the row a transcript read files about one attempt."""

    return _row(
        graded_by="judge",
        grade=0.18,
        kind="analyze",
        label=None,
        routed=False,
        tokens={"cache_read": 2_000_000.0, "output": 20_000.0},
        cost_usd=1.5,
        seconds=900.0,
        harness="claude-code",
        channel="subscription",
        at="2026-09-06T09:30:00Z",
        **overrides,
    )


def test_an_attempt_filed_twice_is_merged_into_one_row(tmp_path: Path) -> None:
    """Every routed build was counted twice: once graded, once costed.

    One side holds the verdict and no cost, the other the cost and a weaker
    grade. Folding them leaves one row carrying the verdict's grade, the
    role's kind, and the tokens the transcript exposed (issue #291).
    """

    evidence.append(tmp_path, [_checker()])
    report = evidence.append(tmp_path, [_captured(), _row(attempt_id="ms-new")])

    assert [entry[0] for entry in report.merged] == ["ms-20260906-000001"]
    assert [entry[0] for entry in report.accepted] == ["ms-new"]
    held = {row.attempt_id: row for row in evidence.load(tmp_path)}
    assert len(held) == 2
    merged = held["ms-20260906-000001"]
    assert (merged.grade, merged.graded_by) == (1.0, "checker")
    assert (merged.kind, merged.label, merged.routed) == ("implement", "build", True)
    assert merged.tokens["output"] == 20_000.0
    assert (merged.cost_usd, merged.seconds) == (1.5, 900.0)
    assert merged.channel == "subscription"
    assert merged.at == "2026-09-06T09:00:00Z"


def test_the_merge_does_not_depend_on_which_side_filed_first(
    tmp_path: Path,
) -> None:
    """Capture runs at a session's end and the verdict lands mid-run.

    Which of them reaches the store first is a fact about the day rather than
    about the attempt, so it decides nothing about the row.
    """

    evidence.append(tmp_path, [_captured()])
    report = evidence.append(tmp_path, [_checker()])

    assert [entry[0] for entry in report.merged] == ["ms-20260906-000001"]
    held = evidence.load(tmp_path)
    assert len(held) == 1
    assert (held[0].grade, held[0].graded_by) == (1.0, "checker")
    assert held[0].kind == "implement"
    assert held[0].tokens["output"] == 20_000.0
    assert held[0].at == "2026-09-06T09:00:00Z"


def test_the_seat_that_ran_is_the_one_the_transcript_read(tmp_path: Path) -> None:
    """The transcript is what actually ran, whatever the router asked for."""

    evidence.append(tmp_path, [_checker(model=WEAK, deliberation="low")])
    evidence.append(tmp_path, [_captured(model=STRONG, deliberation="high")])

    held = evidence.load(tmp_path)
    assert (held[0].model, held[0].deliberation) == (STRONG, "high")


def test_two_subagents_are_two_attempts(tmp_path: Path) -> None:
    """A merge folds one attempt filed twice, never two attempts into one."""

    report = evidence.append(
        tmp_path,
        [_captured(attempt_id="build-1"), _captured(attempt_id="build-2")],
    )

    assert report.merged == []
    assert len(evidence.load(tmp_path)) == 2


def test_a_filing_repeated_after_a_crash_changes_nothing(tmp_path: Path) -> None:
    """Re-running a filing is how a caller recovers from its own crash."""

    evidence.append(tmp_path, [_checker()])
    before = (tmp_path / "measurements.jsonl").read_text(encoding="utf-8")
    report = evidence.append(tmp_path, [_checker()])

    assert [entry[0] for entry in report.merged] == ["ms-20260906-000001"]
    assert (tmp_path / "measurements.jsonl").read_text(encoding="utf-8") == before


def test_a_merge_never_loses_the_line_beside_it(tmp_path: Path) -> None:
    """The ledger is rewritten to fold one row, not to sweep the rest.

    A line somebody's editor mangled is still not a reason to lose the
    thousand rows around it, and a rewrite is where that would happen.
    """

    evidence.append(tmp_path, [_checker(), _row(attempt_id="ms-second")])
    path = tmp_path / "measurements.jsonl"
    path.write_text(
        path.read_text(encoding="utf-8") + "{half a line\n", encoding="utf-8"
    )

    evidence.append(tmp_path, [_captured()])

    assert "{half a line" in path.read_text(encoding="utf-8")
    assert len(evidence.load(tmp_path)) == 2


def test_a_mangled_line_is_skipped_rather_than_losing_the_ledger(
    tmp_path: Path,
) -> None:
    """One line somebody's editor broke is not a reason to lose the rest."""

    evidence.append(tmp_path, [_row(), _row(attempt_id="ms-second")])
    path = tmp_path / "measurements.jsonl"
    path.write_text(path.read_text() + "{half a line\n", encoding="utf-8")

    assert len(evidence.load(tmp_path)) == 2


def test_the_hierarchy_backs_off_to_the_deepest_level_that_has_rows(
    tmp_path: Path,
) -> None:
    """An unmeasured cell is borrowed from its neighbours, and says so."""

    estimator = _estimator(_many(4, 0.9, deliberation="high"), tmp_path)

    exact = estimator.p_success("implement", STRONG, "high")
    sibling = estimator.p_success("implement", STRONG, "low")
    other_kind = estimator.p_success("debug", STRONG, "high")
    other_model = estimator.p_success("implement", WEAK, "high")

    assert exact.basis == "measured"
    assert sibling.basis == "pooled"
    assert other_kind.basis == "pooled"
    assert other_model.basis == "prior"
    assert exact.mean > sibling.mean > other_model.mean
    assert exact.n == 4.0


def test_evidence_moves_a_cell_off_the_prior_it_was_assumed_at(
    tmp_path: Path,
) -> None:
    """Evidence outranks a flattering prior, in both directions.

    The weak model measured succeeding is estimated above what it was assumed
    to be, and the strong model measured failing falls below the weak model
    nobody has tried at all. Neither ordering holds on the priors alone, which
    is the point of storing anything.

    What six good rows do not do is overtake a stronger model's untried prior,
    because a cell shrinks towards its parent at `PSEUDO[1]` attempts' worth of
    weight and its rows are counted once rather than once per level: six rows
    are worth six. Whether that weight is the right one is a separate question
    from this one, and it is asked of `PSEUDO` rather than of the hierarchy.
    """

    untouched = _estimator([], tmp_path / "none")
    working = _estimator(_many(6, 0.9, model=WEAK), tmp_path / "a")
    failing = _estimator(_many(8, 0.05, model=STRONG), tmp_path / "b")

    assumed = untouched.p_success("implement", WEAK, "high")
    measured_good = working.p_success("implement", WEAK, "high")
    measured_bad = failing.p_success("implement", STRONG, "high")
    untried_weak = failing.p_success("implement", WEAK, "high")

    assert measured_good.mean > assumed.mean
    assert measured_good.low > assumed.low
    assert measured_bad.mean < untried_weak.mean


def test_backing_off_a_level_keeps_what_the_level_was_worth(tmp_path: Path) -> None:
    """Measuring a model at one level must not flatten the other four.

    The pooled kind-wide mean describes the level its rows ran at. Read
    unadjusted it is the same number for every level of that model, which
    silently deletes the deliberation signal the moment a cell has evidence —
    and the cheapest level then wins every comparison by default.
    """

    estimator = _estimator(_many(6, 0.6, deliberation="high"), tmp_path)

    ladder = [
        estimator.p_success("implement", STRONG, level).mean
        for level in ("low", "medium", "high", "xhigh", "max")
    ]

    assert ladder == sorted(ladder)
    assert ladder[0] < ladder[2] < ladder[-1]
    assert estimator.p_success("implement", STRONG, "high").basis == "measured"
    assert estimator.p_success("implement", STRONG, "low").basis == "pooled"


def test_backing_off_a_kind_translates_the_verdict_to_the_new_difficulty(
    tmp_path: Path,
) -> None:
    """Failing hard work says something about easy work, not everything.

    A model with nothing but failures on the hardest kind it was ever given
    would otherwise carry that verdict unchanged onto the easiest one, where
    it means far less. The translated estimate sits between the two: below
    what the model's untouched prior claims, and well above its own record on
    the work that beat it.
    """

    weak = "claude-haiku-4-5-20251001"
    estimator = _estimator(_many(4, 0.0, model=weak, kind="design"), tmp_path)
    untouched = evidence.Estimator([], CAT, KINDS)

    hard = estimator.p_success("design", weak, None).mean
    easy = estimator.p_success("mechanical", weak, None).mean
    prior = untouched.p_success("mechanical", weak, None).mean

    assert hard < easy < prior
    assert easy > hard * 4


def test_a_level_of_deliberation_is_worth_something_and_costs_something() -> None:
    """Otherwise the answer to *how hard should it think* is always *barely*."""

    estimator = evidence.Estimator([], CAT, KINDS)

    low = estimator.p_success("implement", STRONG, "low")
    high = estimator.p_success("implement", STRONG, "high")
    cheap = estimator.tokens("implement", STRONG, "low")
    dear = estimator.tokens("implement", STRONG, "high")

    assert high.mean > low.mean
    assert dear["reasoning"] > cheap["reasoning"] * 2
    assert dear["cache_read"] > cheap["cache_read"]


def test_a_category_no_row_measured_falls_back_to_the_prior_not_to_zero(
    tmp_path: Path,
) -> None:
    """A zero for cache reads would understate a bill by two orders of magnitude."""

    estimator = _estimator(
        _many(3, 1.0, tokens={"output": 30_000.0, "cache_read": None}), tmp_path
    )

    counted = estimator.tokens("implement", STRONG, "high")
    prior = KINDS.tokens("implement", "high")

    assert counted["output"] == pytest.approx(30_000.0)
    assert counted["cache_read"] == prior["cache_read"]
    assert all(value > 0.0 for value in counted.values())


def test_a_measured_row_is_scaled_to_the_level_it_is_forecast_at(
    tmp_path: Path,
) -> None:
    """A row taken at one level is a row about every level of that model.

    Read as it stands it forecasts one appetite for the whole ladder, at which
    point the most deliberate level costs exactly what the cheapest does and
    wins every comparison that reads success and cost together.
    """

    measured = {"cache_read": 2_300_000.0, "output": 20_000.0, "reasoning": 44_000.0}
    estimator = _estimator(
        _many(3, 1.0, deliberation="high", tokens=measured, seconds=1_200.0), tmp_path
    )

    counted = estimator.tokens("implement", STRONG, "max")

    for category, value in measured.items():
        rung = "reasoning" if category == "reasoning" else "tokens"
        expected = value / LADDER["high"][rung] * LADDER["max"][rung]
        assert counted[category] == pytest.approx(expected)
    assert estimator.seconds("implement", STRONG, "max") == pytest.approx(
        1_200.0 / LADDER["high"]["tokens"] * LADDER["max"]["tokens"]
    )


def test_rows_at_two_levels_are_forecast_from_one_baseline(tmp_path: Path) -> None:
    """Normalised, a model's rows for a kind are one sample whatever level ran.

    Which is why the exact cell stops being a tier of its own for cost: kept in
    front of the rest, the level that happens to have rows answers from those
    rows alone, and the level beside it answers from a different sample at a
    baseline nobody reconciled.
    """

    rows = [
        _row(
            attempt_id=f"ms-low-{index}",
            deliberation="low",
            tokens={"cache_read": 900_000.0},
            seconds=600.0,
        )
        for index in range(3)
    ] + [
        _row(
            attempt_id="ms-max-1",
            deliberation="max",
            tokens={"cache_read": 3_600_000.0},
            seconds=2_400.0,
        )
    ]
    estimator = _estimator(rows, tmp_path)

    read = statistics.geometric_mean(
        [900_000.0 / LADDER["low"]["tokens"]] * 3
        + [3_600_000.0 / LADDER["max"]["tokens"]]
    )
    taken = statistics.geometric_mean(
        [600.0 / LADDER["low"]["tokens"]] * 3 + [2_400.0 / LADDER["max"]["tokens"]]
    )

    for level in evidence.LEVELS:
        counted = estimator.tokens("implement", STRONG, level)
        assert counted["cache_read"] == pytest.approx(read * LADDER[level]["tokens"])
        assert estimator.seconds("implement", STRONG, level) == pytest.approx(
            taken * LADDER[level]["tokens"]
        )
    assert estimator.p_success("implement", STRONG, "low").basis == "measured"
    assert estimator.p_success("implement", STRONG, "max").basis == "pooled"


def test_the_ladder_survives_the_measurement_of_two_of_its_rungs(
    tmp_path: Path,
) -> None:
    """What a level costs is a ratio, and the ratio is the shipped one."""

    rows = [
        _row(
            attempt_id="ms-high-1",
            deliberation="high",
            tokens={"cache_read": 2_000_000.0, "reasoning": 40_000.0},
            seconds=1_100.0,
        ),
        _row(
            attempt_id="ms-xhigh-1",
            deliberation="xhigh",
            tokens={"cache_read": 2_600_000.0, "reasoning": 90_000.0},
            seconds=1_600.0,
        ),
    ]
    estimator = _estimator(rows, tmp_path)

    at_high = estimator.tokens("implement", STRONG, "high")
    at_max = estimator.tokens("implement", STRONG, "max")

    assert at_max["cache_read"] == pytest.approx(
        at_high["cache_read"] * LADDER["max"]["tokens"] / LADDER["high"]["tokens"]
    )
    assert at_max["reasoning"] == pytest.approx(
        at_high["reasoning"] * LADDER["max"]["reasoning"] / LADDER["high"]["reasoning"]
    )
    assert estimator.seconds("implement", STRONG, "max") == pytest.approx(
        estimator.seconds("implement", STRONG, "high")
        * LADDER["max"]["tokens"]
        / LADDER["high"]["tokens"]
    )


def test_a_row_taken_without_a_level_is_neither_divided_nor_multiplied(
    tmp_path: Path,
) -> None:
    """A model with no effort control ran at factor one and is read at factor one."""

    estimator = _estimator(
        _many(
            3,
            1.0,
            deliberation=None,
            tokens={"cache_read": 1_100_000.0},
            seconds=700.0,
        ),
        tmp_path,
    )

    assert estimator.tokens("implement", STRONG, None)["cache_read"] == pytest.approx(
        1_100_000.0
    )
    assert estimator.seconds("implement", STRONG, None) == pytest.approx(700.0)
    assert estimator.tokens("implement", STRONG, "max")["cache_read"] == pytest.approx(
        1_100_000.0 * LADDER["max"]["tokens"]
    )


def test_the_rules_module_pools_appetite_the_way_the_estimator_does() -> None:
    """The chance of success and what an attempt costs no longer back off alike.

    `p_success` fits the exact (kind, model, deliberation) cell before the kind
    and the model, the level of deliberation being the condition it estimates.
    `tokens` and `seconds` have no such cell: `_normalised` and `_elapsed`
    divide a row by the factors of the level it ran at, so a model's rows for a
    kind are one sample at the `medium` baseline and the level asked for puts
    its own factors back on the pooled figure. A module still saying appetite
    backs off the same way the chance of success does hands a reader the
    opposite of the arithmetic beneath it (issue #300).
    """

    module = ROUTING.read_text(encoding="utf-8")
    collapsed = " ".join(module.split()).lower()

    assert "backs off the same way" not in collapsed

    written = [
        " ".join(block.split()).lower()
        for block in module.split("\n\n")
        if "appetite" in block.lower()
    ]
    assert len(written) == 1
    stated = written[0]

    # What is pooled, in the order the estimator pools it, and the citation the
    # rule has always answered to.
    for phrase in ("normalised", "prior", "chance of success", "(adr-0182)"):
        assert phrase in stated, phrase

    # The two fallbacks differ, and a module that flattened them would leave a
    # reader forecasting a cache read of nought for a store that never
    # recorded one.
    assert "category by category" in stated
    assert "whole" in stated


def test_the_shipped_note_says_the_ladder_is_applied_to_measurements_too() -> None:
    """A factor documented as the prior's alone is a factor nobody applies twice."""

    shipped = json.loads((SHIPPED / "data" / "kinds.json").read_text(encoding="utf-8"))

    assert "measured" in shipped["deliberation_note"]


def test_the_prior_ranks_a_capable_model_above_a_weak_one_on_a_hard_kind() -> None:
    """With nothing measured, capability against difficulty is the whole answer."""

    estimator = evidence.Estimator([], CAT, KINDS)

    hard = [
        estimator.p_success("design", model, "high").mean
        for model in (STRONG, WEAK, "claude-haiku-4-5-20251001")
    ]
    easy = estimator.p_success("mechanical", "claude-haiku-4-5-20251001", None)

    assert hard == sorted(hard, reverse=True)
    assert easy.mean > 0.5
    assert easy.basis == "prior"


def test_the_shipped_kinds_file_describes_every_kind_this_skill_routes() -> None:
    """A kind with no difficulty and no token prior is a kind priced from nothing."""

    assert KINDS.problem is None
    for kind in evidence.KINDS:
        assert 0.0 <= KINDS.difficulty(kind) <= 1.0
        assert all(value > 0.0 for value in KINDS.tokens(kind).values())
    assert KINDS.long_context("implement") and not KINDS.long_context("converse")


def test_drawing_at_uniform_quantiles_samples_the_posterior_reported(
    tmp_path: Path,
) -> None:
    """A sample that is not this cell's own belief is a wager on a fiction.

    Both halves of the estimate are checked against the same sample, and the
    tenth percentile is the sharper of the two: `low` is arrived at by bisecting
    the incomplete beta function, so an agreement between it and the draws is
    two independent routes to one distribution rather than one route twice.
    """

    estimator = _estimator(_many(5, 0.8, deliberation="high"), tmp_path)
    estimate = estimator.p_success("implement", STRONG, "high")
    rng = random.Random(4)

    drawn = sorted(estimate.draw(rng.random()) for _ in range(20_000))

    assert abs(statistics.fmean(drawn) - estimate.mean) < 0.01
    assert abs(drawn[2_000] - estimate.low) < 0.01


def test_a_draw_rises_with_the_quantile_it_is_asked_for(tmp_path: Path) -> None:
    """The quantile is the whole of the sampling, so it has to order the answers.

    Which is what lets one quantile be spent across several correlated cells:
    a caller that shares it between a model's levels is saying they move
    together, and that only means anything if the direction is common.
    """

    estimate = _estimator(_many(4, 0.7), tmp_path).p_success(
        "implement", STRONG, "high"
    )

    ladder = [estimate.draw(quantile) for quantile in (0.05, 0.25, 0.5, 0.75, 0.95)]

    assert ladder == sorted(ladder)
    assert ladder[0] < estimate.mean < ladder[-1]


def test_a_handful_of_failures_at_one_point_is_worth_one_handful(
    tmp_path: Path,
) -> None:
    """Rows counted once per level are the same rows asserted three times.

    A model measured at exactly one point leaves both parent levels holding no
    rows of their own, so each contributes its prior and nothing else, and what
    reaches the cell is its own rows against a prior worth `PSEUDO[1]` of them.
    That is an arithmetic identity rather than a tendency, so it is asserted as
    one: counted three times instead, four failures reach a confidence about
    the whole model that four observations never bought.
    """

    measured = _estimator(_many(4, 0.0, deliberation="high"), tmp_path)
    untried = _estimator([], tmp_path / "empty")

    heard = measured.p_success("implement", STRONG, "high")
    prior = untried.p_success("implement", STRONG, "high")

    weight = evidence.PSEUDO[1]
    assert heard.mean == pytest.approx(weight * prior.mean / (weight + 4))


# --- Discarding the rows of a model that is gone -------------------------------


def _unit_line(unit_id: str, model: str | None) -> str:
    """Return one pending Unit as capture appends it, carrying only what matters here."""

    return json.dumps(
        {"unit_id": unit_id, "model": model, "last_failure": "no-judge"},
        sort_keys=True,
    )


def test_discarding_a_model_deletes_its_rows_and_units_and_nothing_else(
    tmp_path: Path,
) -> None:
    """Matched by exact id, so a model whose id another one extends is untouched."""

    evidence.append(
        tmp_path,
        [
            _row(attempt_id="a1", model="gpt-5.6-luna"),
            _row(attempt_id="a2", model="gpt-5.6-luna-pro"),
            _row(attempt_id="a3", model="gpt-5.6-luna", grade=0.0),
            _row(attempt_id="a4", model=STRONG),
        ],
    )
    (tmp_path / "pending.jsonl").write_text(
        "".join(
            f"{line}\n"
            for line in (
                _unit_line("u1", "gpt-5.6-luna"),
                _unit_line("u2", STRONG),
                _unit_line("u3", "gpt-5.6-luna"),
            )
        ),
        encoding="utf-8",
    )

    gone = evidence.discard_models(tmp_path, ["gpt-5.6-luna"])

    assert gone.rows == {"gpt-5.6-luna": 2}
    assert gone.units == {"gpt-5.6-luna": 2}
    assert [row.attempt_id for row in evidence.load(tmp_path)] == ["a2", "a4"]
    waiting = (tmp_path / "pending.jsonl").read_text(encoding="utf-8").splitlines()
    assert [json.loads(line)["unit_id"] for line in waiting] == ["u2"]


def test_discarding_carries_every_line_it_cannot_parse_across(tmp_path: Path) -> None:
    """A mangled line is somebody's, and a rewrite that dropped it would lose it."""

    good = json.dumps(_row(attempt_id="a1", model="gpt-5.6-luna"))
    kept = json.dumps(_row(attempt_id="a2"))
    (tmp_path / "measurements.jsonl").write_text(
        f"{good}\n{{not json\n{kept}\n", encoding="utf-8"
    )
    (tmp_path / "pending.jsonl").write_text(
        f"{_unit_line('u1', 'gpt-5.6-luna')}\n[half\n", encoding="utf-8"
    )

    evidence.discard_models(tmp_path, ["gpt-5.6-luna"])

    assert (tmp_path / "measurements.jsonl").read_text(encoding="utf-8") == (
        f"{{not json\n{kept}\n"
    )
    assert (tmp_path / "pending.jsonl").read_text(encoding="utf-8") == "[half\n"
    assert not list(tmp_path.glob("*.tmp"))


def test_discarding_a_model_nothing_holds_rewrites_nothing(tmp_path: Path) -> None:
    """An empty directory stays empty, and a store with no such rows is not touched."""

    empty = tmp_path / "empty"
    empty.mkdir()
    assert evidence.discard_models(empty, ["gpt-5.6-luna"]).rows == {}
    assert list(empty.iterdir()) == []

    evidence.append(tmp_path, [_row(attempt_id="a1")])
    before = (tmp_path / "measurements.jsonl").stat().st_mtime_ns
    gone = evidence.discard_models(tmp_path, ["gpt-5.6-luna"])

    assert (gone.rows, gone.units) == ({}, {})
    assert (tmp_path / "measurements.jsonl").stat().st_mtime_ns == before


def test_the_ledger_lock_admits_one_holder_and_takes_over_a_stale_one(
    tmp_path: Path,
) -> None:
    """Grading and the catalogue pass both rewrite these files, under one lock."""

    import os

    with evidence.lock(tmp_path) as first, evidence.lock(tmp_path) as second:
        assert (first, second) == (True, False)
    assert not (tmp_path / "grade.lock").exists()

    stale = tmp_path / "grade.lock"
    stale.write_text("", encoding="utf-8")
    os.utime(stale, (0, 0))
    with evidence.lock(tmp_path) as held:
        assert held is True
