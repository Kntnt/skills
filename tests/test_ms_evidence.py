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


def _spread(count: int, *, routed: bool, **overrides: Any) -> list[dict[str, Any]]:
    """Provide *count* distinct attempts, all routed or none of them.

    Distinct identities on purpose: two sets filed under one series of names
    would be folded into each other rather than pooled beside each other.
    """

    return [
        _row(
            attempt_id=f"ms-{'routed' if routed else 'span'}-{index:04d}",
            routed=routed,
            **overrides,
        )
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


# What Orchestrate's `observed_measurement` files about a routed attempt: the
# verdict's grade, an elapsed time from the instant `attempt-start` persisted,
# every token category null because a Claude subagent exposes nothing to the
# session that spawned it, and no `cost_usd` key at all (issue #370).
def _observed(**overrides: Any) -> dict[str, Any]:
    """Provide the row a routed run files about one attempt of its own."""

    row = _row(
        **{
            "graded_by": "checker",
            "grade": 1.0,
            "kind": "implement",
            "label": "build",
            "routed": True,
            "tokens": dict.fromkeys(catalogue.TOKEN_CATEGORIES),
            "seconds": 2_400.0,
            "channel": "subscription",
            **overrides,
        }
    )
    row.pop("cost_usd")
    return row


def _attempt(**overrides: Any) -> dict[str, Any]:
    """Provide the row a read of that same builder's transcript files."""

    return _row(
        **{
            "graded_by": "judge",
            "grade": 0.18,
            "kind": "analyze",
            "label": None,
            "routed": False,
            "tokens": {
                "input": 12.0,
                "cache_read": 2_000_000.0,
                "cache_write": 3_400.0,
                "output": 20_000.0,
                "reasoning": 44_000.0,
            },
            "cost_usd": 7.5,
            "seconds": 1_800.0,
            "harness": "claude-code",
            "channel": "subscription",
            "at": "2026-09-06T09:30:00Z",
            **overrides,
        }
    )


def test_one_routed_build_filed_from_both_sides_is_one_priced_row(
    tmp_path: Path,
) -> None:
    """The routed row had a grade and no price; the captured one a price and no verdict.

    Folded under one attempt identity they are one whole build: the checker's
    grade and kind, the counts the transcript exposed, and the price computed
    from them. The elapsed time is whichever side filed first, both figures
    spanning the whole attempt rather than a span inside a session (issue
    #370).
    """

    evidence.append(tmp_path, [_observed()])
    evidence.append(tmp_path, [_attempt()])

    [merged] = evidence.load(tmp_path)
    assert (merged.grade, merged.graded_by, merged.kind) == (
        1.0,
        "checker",
        "implement",
    )
    assert merged.routed is True
    assert merged.tokens["output"] == 20_000.0
    assert merged.tokens["cache_write"] == 3_400.0
    assert merged.cost_usd == 7.5
    assert merged.seconds == 2_400.0


def test_the_opposite_filing_order_leaves_the_same_single_row(
    tmp_path: Path,
) -> None:
    """Which side reaches the store first is a fact about the day.

    It decides nothing but the elapsed time, which is the figure of whichever
    side filed first — the caller's from the launch instant to the verdict,
    the captured one from the builder's first instruction to its last turn.
    """

    evidence.append(tmp_path, [_attempt()])
    evidence.append(tmp_path, [_observed()])

    [merged] = evidence.load(tmp_path)
    assert (merged.grade, merged.graded_by, merged.kind) == (
        1.0,
        "checker",
        "implement",
    )
    assert merged.routed is True
    assert merged.tokens["output"] == 20_000.0
    assert merged.cost_usd == 7.5
    assert merged.seconds == 1_800.0


def test_a_caller_that_measured_no_elapsed_time_takes_the_captured_one(
    tmp_path: Path,
) -> None:
    """A null is an absence, so the one side that measured it fills it."""

    for order in (
        [_observed(seconds=None), _attempt()],
        [_attempt(), _observed(seconds=None)],
    ):
        store = tmp_path / f"order-{len(list(tmp_path.iterdir()))}"
        store.mkdir()
        for row in order:
            evidence.append(store, [row])
        [merged] = evidence.load(store)
        assert merged.seconds == 1_800.0
        assert merged.routed is True


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


def test_a_category_every_row_recorded_as_nought_is_forecast_as_nought(
    tmp_path: Path,
) -> None:
    """Codex reports no cache writes at all, and the vendor never bills them.

    Folded in with a category no row recorded, that reported nought fell
    through to the kind's shipped 208 000 cache-write tokens — about three
    dollars on every `high` attempt of a bill the vendor never sends, on the
    one figure the whole ranking orders by (issue #371).
    """

    measured = {
        "input": 600.0,
        "cache_read": 1_000_000.0,
        "cache_write": 0.0,
        "output": 30_000.0,
        "reasoning": 12_000.0,
    }
    estimator = _estimator(_many(3, 1.0, tokens=measured), tmp_path)

    counted = estimator.tokens("implement", STRONG, "high")

    assert counted["cache_write"] == 0.0
    assert counted["cache_write"] != KINDS.tokens("implement", "high")["cache_write"]
    for category, value in measured.items():
        assert counted[category] == pytest.approx(value), category


def test_a_category_no_row_carries_is_not_one_every_row_measured_as_nought(
    tmp_path: Path,
) -> None:
    """The store keeps the two apart the whole way here, and only this folded them.

    A row carrying no member for a category said nothing about it, and the
    kind's prior scaled to the level asked about is the honest answer. A row
    carrying nought said nought.
    """

    absent = _estimator(
        _many(3, 1.0, tokens={"output": 30_000.0}), tmp_path / "absent"
    ).tokens("implement", STRONG, "high")
    recorded = _estimator(
        _many(3, 1.0, tokens={"output": 30_000.0, "cache_write": 0.0}),
        tmp_path / "recorded",
    ).tokens("implement", STRONG, "high")

    prior = KINDS.tokens("implement", "high")

    assert absent["cache_write"] == pytest.approx(prior["cache_write"])
    assert absent["cache_write"] == pytest.approx(208_000.0 * LADDER["high"]["tokens"])
    assert recorded["cache_write"] == 0.0
    assert absent["output"] == pytest.approx(30_000.0)
    assert recorded["output"] == pytest.approx(30_000.0)


def test_a_row_that_measured_nought_lowers_the_forecast_it_joins(
    tmp_path: Path,
) -> None:
    """A vendor that bills nothing on one attempt in four spends less than on none.

    The geometric mean cannot hold a nought — the logarithm of nought is not a
    number — so the rows that measured a positive amount are pooled exactly as
    they always were and the pooled figure is scaled by their share of the rows
    that recorded the category at all.
    """

    positive = [
        _row(attempt_id=f"ms-paid-{index}", tokens={"cache_write": 40_000.0})
        for index in range(3)
    ]
    free = [_row(attempt_id="ms-free-0", tokens={"cache_write": 0.0})]

    alone = _estimator(list(positive), tmp_path / "alone").tokens(
        "implement", STRONG, "high"
    )["cache_write"]
    mixed = _estimator(positive + free, tmp_path / "mixed").tokens(
        "implement", STRONG, "high"
    )["cache_write"]

    assert alone == pytest.approx(40_000.0)
    assert mixed == pytest.approx(40_000.0 * 3 / 4)
    assert 0.0 < mixed < alone


def test_a_point_that_measured_nought_everywhere_forecasts_nought_everywhere(
    tmp_path: Path,
) -> None:
    """Nothing takes the logarithm of a nought, and no figure comes back negative."""

    estimator = _estimator(
        _many(3, 1.0, tokens=dict.fromkeys(catalogue.TOKEN_CATEGORIES, 0.0)),
        tmp_path,
    )

    for level in evidence.LEVELS:
        counted = estimator.tokens("implement", STRONG, level)
        assert set(counted) == set(catalogue.TOKEN_CATEGORIES)
        assert all(value == 0.0 for value in counted.values()), level


def test_a_row_that_recorded_nothing_is_no_evidence_about_a_category(
    tmp_path: Path,
) -> None:
    """Seventy-five of this store's Opus `implement` rows carry no counts at all.

    They came from a routed run that could see a verdict and no usage. Let them
    into the share the pooled figure is scaled by — a share taken over every
    row of the group rather than over the recording ones — and that point's
    every category is cut by about a third: a forecast of less work on evidence
    of no work (issue #371).
    """

    recording = [
        _row(attempt_id=f"ms-seen-{index}", tokens={"output": 30_000.0})
        for index in range(3)
    ]
    silent = [
        _row(
            attempt_id=f"ms-blind-{index}",
            tokens=dict.fromkeys(catalogue.TOKEN_CATEGORIES),
        )
        for index in range(9)
    ]

    alone = _estimator(list(recording), tmp_path / "alone").tokens(
        "implement", STRONG, "high"
    )
    beside = _estimator(recording + silent, tmp_path / "beside").tokens(
        "implement", STRONG, "high"
    )

    assert alone["output"] == pytest.approx(30_000.0)
    assert beside == pytest.approx(alone)


def test_a_group_that_recorded_nought_answers_rather_than_backing_off(
    tmp_path: Path,
) -> None:
    """A nought is a measurement inside the back-off as well as at the end of it.

    Fall through on *no positive rows* and a store every row of which measured
    nought forecasts the kind's prior, which is the defect being fixed. Only a
    group no row of which recorded the category reaches the group above it, and
    only where neither recorded it does the shipped prior answer.
    """

    for_the_kind = [
        _row(
            attempt_id=f"ms-kind-{index}",
            tokens={"cache_write": 0.0, "output": 30_000.0},
        )
        for index in range(3)
    ]
    for_another = [
        _row(
            attempt_id=f"ms-other-{index}",
            kind="analyze",
            tokens={"cache_write": 50_000.0, "reasoning": 80_000.0},
        )
        for index in range(3)
    ]
    estimator = _estimator(for_the_kind + for_another, tmp_path)

    counted = estimator.tokens("implement", STRONG, "high")
    prior = KINDS.tokens("implement", "high")

    assert counted["cache_write"] == 0.0
    assert counted["output"] == pytest.approx(30_000.0)
    assert counted["reasoning"] == pytest.approx(80_000.0)
    assert counted["input"] == pytest.approx(prior["input"])


def test_an_elapsed_time_of_nought_is_a_clock_that_failed_to_record(
    tmp_path: Path,
) -> None:
    """The same nought is a measurement for tokens and an absence for the clock.

    A vendor really does bill no cache writes; no harness reports an attempt
    that took no time, so a nought there is a start instant that never
    persisted. Read as a measurement it would make the point the fastest thing
    on every list, which is why `_elapsed` keeps the test `_normalised` gives
    up (issue #371).
    """

    estimator = _estimator(
        _many(3, 1.0, tokens={"output": 30_000.0, "cache_write": 0.0}, seconds=0.0),
        tmp_path,
    )

    assert estimator.tokens("implement", STRONG, "high")["cache_write"] == 0.0
    assert estimator.seconds("implement", STRONG, "high") == pytest.approx(
        KINDS.seconds("implement", "high")
    )


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


def test_the_forecast_answers_from_the_routed_rows_where_a_group_has_any(
    tmp_path: Path,
) -> None:
    """A whole build and a span of somebody's own session are different sizes of job.

    Pooled together, seventy-five routed builds carrying a grade and no price
    were forecast from a hundred and thirty non-routed spans of the
    maintainer's own session — median ten minutes and seven dollars — and the
    price the ranking compared against a whole Codex build was the price of a
    span inside a session (issue #370).
    """

    rows = _spread(
        3,
        routed=True,
        tokens={"output": 300_000.0, "cache_read": 9_000_000.0},
        seconds=2_400.0,
    ) + _spread(
        4,
        routed=False,
        tokens={"output": 20_000.0, "cache_read": 500_000.0, "reasoning": 44_000.0},
        seconds=600.0,
    )

    # A second kind's spans, so the model-wide tier the forecast backs off to
    # holds non-routed rows carrying a category the routed rows never did.
    rows += [
        _row(
            attempt_id=f"ms-other-{index:04d}",
            kind="analyze",
            routed=False,
            tokens={"reasoning": 88_000.0},
            seconds=300.0,
        )
        for index in range(3)
    ]
    estimator = _estimator(rows, tmp_path)

    counted = estimator.tokens("implement", STRONG, "high")
    prior = KINDS.tokens("implement", "high")

    assert counted["output"] == pytest.approx(300_000.0)
    assert counted["cache_read"] == pytest.approx(9_000_000.0)
    assert estimator.seconds("implement", STRONG, "high") == pytest.approx(2_400.0)

    # A category the routed rows never measured backs off to the next tier and
    # then to the kind's prior. Taking it from the non-routed rows beside them
    # is the averaging this rule exists to end: a store that has never
    # measured what a routed build spends says so.
    assert counted["reasoning"] == pytest.approx(prior["reasoning"])


def test_a_group_holding_no_routed_row_is_pooled_exactly_as_it_was(
    tmp_path: Path,
) -> None:
    """The filter is a choice made once per group, not a requirement on a row."""

    estimator = _estimator(
        _spread(3, routed=False, tokens={"output": 20_000.0}, seconds=600.0), tmp_path
    )

    assert estimator.tokens("implement", STRONG, "high")["output"] == pytest.approx(
        20_000.0
    )
    assert estimator.seconds("implement", STRONG, "high") == pytest.approx(600.0)


def test_the_chance_of_success_still_reads_every_row_of_a_point(
    tmp_path: Path,
) -> None:
    """There the level and the model are what is being estimated.

    Narrowing its rows too would interact with what counts as measured, and
    the hierarchy already backs off through three tiers of its own.
    """

    rows = _spread(3, routed=True, grade=1.0) + _spread(4, routed=False, grade=0.0)
    estimator = _estimator(rows, tmp_path)

    assert estimator.p_success("implement", STRONG, "high").n == 7.0


def test_the_module_says_why_the_routed_filter_stops_at_the_forecast() -> None:
    """A reader extending it to the chance of success by symmetry would undo it.

    So the reason is written where the restriction is, rather than left for
    the next author to infer from an absence (issue #370).
    """

    stated = " ".join((evidence.Estimator.p_success.__doc__ or "").split())

    assert "routed" in stated
    assert "size of the job" in stated


def test_the_rules_module_says_how_the_routed_fact_reaches_a_row() -> None:
    """Each side files the fact it holds, and the higher authority's stands.

    `_merged` assigns `routed` inside the branch guarded by the two
    authorities, so it travels with the grade exactly as the kind and the
    label do. A module saying it travels with whichever side read the
    transcript would describe a merge this store does not perform (issue
    #370).
    """

    module = ROUTING.read_text(encoding="utf-8")
    [stated] = [
        " ".join(block.split())
        for block in module.split("\n\n")
        if "A Measurement is keyed by" in block
    ]

    for phrase in ("files the routed fact it holds", "higher authority"):
        assert phrase in stated, phrase


def test_the_rules_module_no_longer_says_a_delegated_unit_opens_with_the_line() -> None:
    """The attempt is read from every line of the instruction, not the first.

    A dispatching session hands a builder a pointer to the brief, and a
    Harness puts its own preamble in front of what it hands over; a module
    still saying *opens with* describes the rule that left every routed Claude
    attempt unmeasured (issue #370).
    """

    module = ROUTING.read_text(encoding="utf-8")
    [stated] = [
        " ".join(block.split())
        for block in module.split("\n\n")
        if "A Unit of Work is an instruction" in block
    ]

    assert "opens with" not in stated
    assert "carries a routed attempt's `attempt_id:` line" in stated


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
    for phrase in (
        "normalised",
        "prior",
        "chance of success",
        "(adr-0182)",
        "routed rows of each group",
    ):
        assert phrase in stated, phrase

    # The two fallbacks differ, and a module that flattened them would leave a
    # reader forecasting a cache read of nought for a store that never
    # recorded one.
    assert "category by category" in stated
    assert "whole" in stated

    # And the two things "unmeasured" was folding together: a category no row
    # recorded, which takes the prior, and one every recording row measured as
    # nought, which is a measurement and is priced as one (issue #371).
    assert "recorded it as nought" in stated
    assert "priced as nought" in stated


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


# --- A newer release inherits its family's record (ADR-0215) ---------------------

# Two releases of one family, and a store that holds rows for either or both.
# The family is the fixture's own rather than a seeded one, so that nothing the
# seed ships decides which release is the older.
OLDER: str = "kin-4"
NEWER: str = "kin-5"


def _release(
    identifier: str, released: str, capability: float | None
) -> dict[str, Any]:
    """Provide one release of the fixture family, in the shape the seed writes it."""

    return {
        "id": identifier,
        "provider": "testing",
        "family": "kin",
        "aliases": ["kin"],
        "deliberation": ["low", "medium", "high", "xhigh"],
        "price": {
            "input": 1.0,
            "cache_read": 0.1,
            "cache_write": 1.25,
            "output": 5.0,
            "currency": "USD",
            "unit": "per_mtok",
        },
        "reasoning_billed_as": "output",
        "capability": capability,
        "released": released,
        "source_url": "https://example.invalid/models",
        "retrieved": "2026-09-23",
    }


def _family(tmp_path: Path, *releases: dict[str, Any]) -> Any:
    """Return a catalogue holding *releases*, the two-release family by default.

    The older release carries a capability and the newer one none, which is
    how the catalogue pass admits a release the seed does not name yet.
    """

    shipped = releases or (
        _release(OLDER, "2026-01-01", 0.7),
        _release(NEWER, "2026-06-01", None),
    )
    here = tmp_path / "skill"
    (here / "data").mkdir(parents=True)
    (here / "data" / "catalogue-seed.json").write_text(
        json.dumps({"generated_at": "2026-09-23", "models": list(shipped)}),
        encoding="utf-8",
    )
    return catalogue.load(tmp_path / "data", here)


def _reading(cat: Any, rows: list[dict[str, Any]], data_dir: Path) -> Any:
    """File *rows* in a store of their own and return an estimator over *cat*."""

    evidence.append(data_dir, rows)
    return evidence.Estimator(evidence.load(data_dir), cat, KINDS)


def _own(count: int, grade: float, **overrides: Any) -> list[dict[str, Any]]:
    """Provide *count* rows of the newer release, named apart from the older's."""

    return [
        _row(attempt_id=f"own-{index:04d}", model=NEWER, grade=grade, **overrides)
        for index in range(count)
    ]


# Points across the ladder and across kinds, some of which the stores below
# hold rows at and some of which they do not.
POINTS: tuple[tuple[str, str], ...] = (
    ("implement", "high"),
    ("implement", "low"),
    ("implement", "xhigh"),
    ("design", "high"),
    ("review", "medium"),
)


def _spread_rows(model: str, prefix: str) -> list[dict[str, Any]]:
    """Provide a record of one model at several kinds and levels, graded unevenly."""

    shape = (
        ("implement", "high", 1.0, 9),
        ("implement", "high", 0.0, 3),
        ("implement", "medium", 0.5, 4),
        ("design", "high", 0.0, 2),
        ("review", "low", 1.0, 5),
    )
    return [
        _row(
            attempt_id=f"{prefix}-{index}-{count}",
            model=model,
            kind=kind,
            deliberation=level,
            grade=grade,
        )
        for index, (kind, level, grade, rows) in enumerate(shape)
        for count in range(rows)
    ]


def _before_inheritance(
    estimator: Any, kind: str, model: str, level: str
) -> tuple[float, float]:
    """Return a point's Beta as the hierarchy fitted it before ADR-0215.

    The model's own rows through the three tiers and the sigmoid, and nothing
    else: the arithmetic `main` ran at the commit before this rule, spelt out
    here with the module's own parts so that a model with no older release can
    be held to it exactly.
    """

    exact, by_kind, by_model = estimator._levels(kind, model, level)
    other_levels = [row for row in by_kind if row.deliberation != level]
    other_kinds = [row for row in by_model if row.kind != kind]
    here = estimator._margin(kind, model, level)
    at_model = estimator._mean_margin(other_kinds, model, here)
    at_kind = estimator._mean_margin(other_levels, model, here)
    pooled_model = evidence._posterior_mean(
        other_kinds,
        evidence._sigmoid(evidence.SHARPNESS * at_model),
        evidence.PSEUDO[3],
    )
    pooled_kind = evidence._posterior_mean(
        other_levels,
        evidence._translated(
            pooled_model,
            at_kind - at_model,
            toward=evidence._sigmoid(evidence.SHARPNESS * at_kind),
        ),
        evidence.PSEUDO[2],
    )
    alpha, beta = evidence._posterior(
        exact, evidence._translated(pooled_kind, here - at_kind), evidence.PSEUDO[1]
    )
    return alpha, beta


def test_a_model_with_no_older_release_is_estimated_exactly_as_before(
    tmp_path: Path,
) -> None:
    """With no older release the family's record is the model's own stack.

    Its deepest tier is then empty and passes its prior down unchanged, so the
    Beta is the one the hierarchy gave before a family was read at all, to the
    last bit — at points the store holds rows for and at points it does not.
    The same holds for a model whose older releases hold no row, which is what
    keeps `EXPLORATION_AT_BASE` in `test_ms_selection.py` the sweep the
    commit before this rule drew.
    """

    cat = _family(tmp_path)
    estimator = _reading(cat, _spread_rows(OLDER, "old"), tmp_path / "data")

    for kind, level in POINTS:
        estimate = estimator.p_success(kind, OLDER, level)
        assert (estimate.alpha, estimate.beta) == _before_inheritance(
            estimator, kind, OLDER, level
        )


def test_a_newer_release_with_no_rows_is_estimated_as_its_predecessor(
    tmp_path: Path,
) -> None:
    """At every point its mean is its predecessor's, and less sure of itself.

    The predecessor's stack is the family's record, so the newer release's
    cell is fitted on nothing against a prior that is its predecessor's
    estimate: the same mean, a Beta of only the exact cell's parent weight, so
    a lower tenth percentile wherever the predecessor had rows at the point,
    and no row a caller counts — `family`, a Trial count of nought, an `n` of
    nought.
    """

    cat = _family(tmp_path)
    estimator = _reading(cat, _spread_rows(OLDER, "old"), tmp_path / "data")

    for kind, level in POINTS:
        heir = estimator.p_success(kind, NEWER, level)
        predecessor = estimator.p_success(kind, OLDER, level)
        assert heir.mean == pytest.approx(predecessor.mean, rel=1e-12)
        assert heir.alpha + heir.beta == pytest.approx(evidence.PSEUDO[1])
        assert heir.low <= predecessor.low + 1e-12
        assert heir.basis == "family"
        assert heir.n == 0.0
    assert estimator.rows_for_kind("implement", NEWER) == 0
    measured = estimator.p_success("implement", OLDER, "high")
    assert estimator.p_success("implement", NEWER, "high").low < measured.low


def test_the_older_release_is_untouched_by_the_newer_release_s_rows(
    tmp_path: Path,
) -> None:
    """Nothing flows from a newer release to an older one.

    A lock to the older release by its exact id is answered from its own rows,
    and here it has none: its estimate is the one an empty store gives it.
    """

    cat = _family(tmp_path)
    estimator = _reading(cat, _own(12, 1.0), tmp_path / "data")
    untried = evidence.Estimator([], cat, KINDS)

    for level in ("low", "high"):
        assert estimator.p_success("implement", OLDER, level) == untried.p_success(
            "implement", OLDER, level
        )
    assert estimator.p_success("implement", OLDER, "high").basis == "prior"


def test_three_own_rows_are_a_third_of_the_cell_and_a_dozen_two_thirds(
    tmp_path: Path,
) -> None:
    """The family's record is the cell's prior, at the weight every parent has.

    However many rows the older release holds at the point, what they say
    enters the newer release's cell as a prior worth `PSEUDO[1]`, six. Three
    rows of its own are then three of nine, a third of the cell, and a dozen
    are twelve of eighteen; the rest of the cell is exactly what the family's
    record says of the point with nothing of the release's own.
    """

    cat = _family(tmp_path)
    kin = _many(30, 0.0, model=OLDER)
    record = _reading(cat, kin, tmp_path / "record").p_success(
        "implement", NEWER, "high"
    )
    trial = _reading(cat, [*kin, *_own(evidence.ENOUGH, 1.0)], tmp_path / "trial")
    dozen = _reading(cat, [*kin, *_own(12, 1.0)], tmp_path / "dozen")

    for estimator, own in ((trial, evidence.ENOUGH), (dozen, 12)):
        estimate = estimator.p_success("implement", NEWER, "high")
        weight = estimate.alpha + estimate.beta
        assert weight == pytest.approx(own + evidence.PSEUDO[1])
        assert estimate.mean == pytest.approx(
            (own + evidence.PSEUDO[1] * record.mean) / weight
        )
        assert estimate.basis == "measured"
    assert evidence.ENOUGH / (evidence.ENOUGH + evidence.PSEUDO[1]) == 1 / 3
    assert 12 / (12 + evidence.PSEUDO[1]) == 2 / 3
    assert trial.rows_for_kind("implement", NEWER) == evidence.ENOUGH


def test_the_newest_of_three_releases_inherits_the_rows_of_both_older_ones(
    tmp_path: Path,
) -> None:
    """Every older release is kin, not only the one just before.

    The rows of the oldest release and of the middle one enter the newest
    release's record together, so its estimate is the one it would have if
    all of them had been filed under a single predecessor.
    """

    releases = (
        _release("kin-3", "2025-01-01", 0.7),
        _release(OLDER, "2026-01-01", 0.7),
        _release(NEWER, "2026-06-01", 0.7),
    )
    good = _many(10, 1.0, model="kin-3")
    bad = [
        _row(attempt_id=f"mid-{index}", model=OLDER, grade=0.0) for index in range(10)
    ]
    moved = [{**row, "model": OLDER} for row in good]
    chain = _reading(
        _family(tmp_path / "chain", *releases), [*good, *bad], tmp_path / "a"
    )
    pooled = _reading(
        _family(tmp_path / "pooled", *releases), [*moved, *bad], tmp_path / "b"
    )
    oldest = _reading(_family(tmp_path / "oldest", *releases), good, tmp_path / "c")

    heir = chain.p_success("implement", NEWER, "high")

    assert heir.basis == "family"
    assert heir.mean == pytest.approx(pooled.p_success("implement", NEWER, "high").mean)
    assert heir.mean < oldest.p_success("implement", NEWER, "high").mean


def test_a_release_s_own_rows_at_other_work_inform_its_record_for_this_work(
    tmp_path: Path,
) -> None:
    """The family's stack holds the release's own rows above its cell.

    A predecessor measured once, and failing, is next to nothing beside thirty
    rows of the newer release's own on other work: the estimate for this work
    follows the thirty, as it would with no predecessor at all, rather than
    the one row.
    """

    cat = _family(tmp_path)
    once = [_row(attempt_id="old-once", model=OLDER, grade=0.0)]
    thirty = _own(30, 1.0, kind="design")
    both = _reading(cat, [*once, *thirty], tmp_path / "both")
    own = _reading(cat, thirty, tmp_path / "own")
    kin = _reading(cat, once, tmp_path / "kin")

    mixed = both.p_success("implement", NEWER, "high").mean
    followed = own.p_success("implement", NEWER, "high").mean
    inherited = kin.p_success("implement", NEWER, "high").mean

    assert abs(mixed - followed) < abs(mixed - inherited)
    assert mixed > inherited
    assert both.p_success("implement", NEWER, "high").basis == "pooled"


def test_family_replaces_prior_alone(tmp_path: Path) -> None:
    """`measured` and `pooled` mean what they meant, off the release's own rows.

    One row of its own at the point asked about is too few for either, so a
    release whose family holds rows reads `family`; three rows of its own at
    another kind make it `pooled` as they always did; and a release with
    neither rows nor an older release holding any stays `prior`.
    """

    cat = _family(tmp_path)
    kin = _many(4, 1.0, model=OLDER, kind="review")
    one = _reading(cat, [*kin, *_own(1, 1.0)], tmp_path / "one")
    elsewhere = _reading(cat, [*kin, *_own(3, 1.0, kind="design")], tmp_path / "other")
    alone = _reading(cat, _own(1, 1.0), tmp_path / "alone")

    assert evidence.BASIS == ("measured", "pooled", "family", "prior", "inherit")
    assert one.p_success("implement", NEWER, "high").basis == "family"
    assert elsewhere.p_success("implement", NEWER, "high").basis == "pooled"
    assert alone.p_success("implement", NEWER, "high").basis == "prior"
    assert one.p_success("implement", OLDER, "high").basis == "pooled"


def test_a_release_with_no_seeded_capability_stands_at_its_newest_older_release_s(
    tmp_path: Path,
) -> None:
    """The bottom of the stack is the family's, read here and written nowhere.

    Where the release just before it carries no capability either, the newest
    older release that does is the one it stands at. The catalogue keeps its
    own `None`, and no `catalogue.json` is written, a figure written there
    outranking the seed's own later word.
    """

    three = _family(
        tmp_path / "three",
        _release("kin-3", "2025-01-01", 0.6),
        _release(OLDER, "2026-01-01", 0.9),
        _release(NEWER, "2026-06-01", None),
    )
    gap = _family(
        tmp_path / "gap",
        _release("kin-3", "2025-01-01", 0.6),
        _release(OLDER, "2026-01-01", None),
        _release(NEWER, "2026-06-01", None),
    )
    newest = evidence.Estimator([], three, KINDS)
    skipped = evidence.Estimator([], gap, KINDS)

    for level in ("low", "high"):
        assert newest.p_success("implement", NEWER, level) == newest.p_success(
            "implement", OLDER, level
        )
        assert skipped.p_success("implement", NEWER, level) == skipped.p_success(
            "implement", "kin-3", level
        )
    assert (
        newest.p_success("implement", NEWER, "high").mean
        > skipped.p_success("implement", NEWER, "high").mean
    )
    assert next(model for model in three.models if model.id == NEWER).capability is None
    assert not list(tmp_path.rglob("catalogue.json"))


def test_a_forecast_for_a_release_with_no_rows_is_its_older_release_s(
    tmp_path: Path,
) -> None:
    """Tokens and elapsed time come from the family at the tier they are asked at.

    Read back to the baseline and scaled to the level asked for, as the older
    release's own forecast is, rather than from the kind's shipped prior.
    """

    cat = _family(tmp_path)
    estimator = _reading(
        cat,
        _many(4, 1.0, model=OLDER, seconds=1200.0, tokens={"output": 40_000.0}),
        tmp_path / "data",
    )

    for level in ("low", "xhigh"):
        assert estimator.tokens("implement", NEWER, level) == estimator.tokens(
            "implement", OLDER, level
        )
        assert estimator.seconds("implement", NEWER, level) == pytest.approx(
            estimator.seconds("implement", OLDER, level)
        )
    assert estimator.tokens("implement", NEWER, "high") != KINDS.tokens(
        "implement", "high"
    )


def test_a_forecast_takes_the_release_s_own_rows_before_its_family_s_at_each_tier(
    tmp_path: Path,
) -> None:
    """Own kind, inherited kind, own model, inherited model, then the prior.

    The newer release's own `design` rows answer `design`, and for
    `implement` they are the model tier, which comes after the kind's
    inherited rows: the older release's `implement` rows answer first. One
    `implement` row of its own then answers ahead of both.
    """

    cat = _family(tmp_path)
    kin = _many(4, 1.0, model=OLDER, seconds=1200.0)
    design = _own(4, 1.0, kind="design", seconds=100.0)
    before = _reading(cat, [*kin, *design], tmp_path / "before")
    after = _reading(
        cat,
        [*kin, *design, _row(attempt_id="own-late", model=NEWER, seconds=300.0)],
        tmp_path / "after",
    )

    assert before.seconds("implement", NEWER, "high") == pytest.approx(1200.0)
    assert before.seconds("design", NEWER, "high") == pytest.approx(100.0)
    assert after.seconds("implement", NEWER, "high") == pytest.approx(300.0)


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
