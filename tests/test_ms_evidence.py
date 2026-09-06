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


def test_an_attempt_already_stored_is_skipped_rather_than_duplicated(
    tmp_path: Path,
) -> None:
    """Re-running a filing is how a caller recovers from its own crash."""

    evidence.append(tmp_path, [_row()])
    report = evidence.append(tmp_path, [_row(), _row(attempt_id="ms-new")])

    assert [entry[0] for entry in report.skipped] == ["ms-20260906-000001"]
    assert [entry[0] for entry in report.accepted] == ["ms-new"]
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
