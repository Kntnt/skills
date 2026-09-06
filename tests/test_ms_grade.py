"""Grading the Units of Work the model-selector Skill captured."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"

NOW = datetime(2026, 9, 6, 12, 0, 0, tzinfo=UTC)


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


# In dependency order, so a module importing a sibling by plain name finds the
# same object these tests are holding.
catalogue = _module("catalogue")
_module("profiles")
evidence = _module("evidence")
grade = _module("grade")


class _Judge:
    """Stand in for the one model call, recording exactly what it was sent."""

    def __init__(self, *answers: str | None) -> None:
        self.answers = list(answers)
        self.prompts: list[str] = []
        self.seconds: list[float] = []

    def __call__(self, prompt: str, seconds: float) -> str | None:
        self.prompts.append(prompt)
        self.seconds.append(seconds)
        return self.answers.pop(0) if self.answers else None


def _never(prompt: str, seconds: float) -> str | None:
    """Provide a judge that fails the test if the pass ever calls it."""

    raise AssertionError("the pass asked a model, which it may not do here")


def _unit(**overrides: Any) -> dict[str, Any]:
    """Provide one pending Unit, in the shape capture writes it."""

    base: dict[str, Any] = {
        "unit_id": "unit-one",
        "session": "0123456789abcdef",
        "harness": "claude-code",
        "started_at": "2026-09-06T10:00:00.000Z",
        "ended_at": "2026-09-06T10:05:00.000Z",
        "seconds": 300.0,
        "model": "claude-opus-5",
        "deliberation": "high",
        "tokens": {
            "input": 10.0,
            "cache_read": 120000.0,
            "cache_write": 3400.0,
            "output": 5000.0,
            "reasoning": 250.0,
        },
        "tool_calls": 9,
        "changing_tool_calls": 4,
        "delegated": False,
        "signals": {
            "retried": False,
            "tests_ran": False,
            "tests_passed": False,
            "interrupted": False,
            "errored": False,
        },
        "instruction_excerpt": "make the thing work",
        "result_excerpt": "It works now, and the suite is green.",
    }
    return {**base, **overrides}


def _signals(**flags: bool) -> dict[str, bool]:
    """Provide one Unit's free signals, every flag false but the named ones."""

    base = {
        "retried": False,
        "tests_ran": False,
        "tests_passed": False,
        "interrupted": False,
        "errored": False,
    }
    return {**base, **flags}


def _queue(tmp_path: Path, *rows: dict[str, Any]) -> Path:
    """Write one pending store and return the data directory holding it."""

    data = tmp_path / "data"
    data.mkdir(exist_ok=True)
    (data / "pending.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return data


def _waiting(data: Path) -> list[dict[str, Any]]:
    """Return every Unit still pending under *data*."""

    path = data / "pending.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _verdict(kind: str = "implement", value: int = 80) -> str:
    """Provide one judge's answer, as a bridge hands a model's words back."""

    return json.dumps({"kind": kind, "grade": value, "reason": "did the work"})


# --- The free signals decide first -------------------------------------------


def test_an_interrupted_unit_with_no_result_is_dropped_rather_than_scored_zero(
    tmp_path: Path,
) -> None:
    """Nothing was established about the model, and a zero says otherwise.

    An attempt somebody stopped is not the event that an attempt which did
    nothing useful is, and recording them identically is a measurement error
    no sample size corrects.
    """

    data = _queue(
        tmp_path, _unit(signals=_signals(interrupted=True), result_excerpt="")
    )

    report = grade.grade_pending(data, judge=_never, now=NOW)

    assert report["dropped"] == 1
    assert evidence.load(data) == []
    assert _waiting(data) == []


def test_an_errored_unit_with_no_result_is_dropped_too(tmp_path: Path) -> None:
    """A Harness that failed the turn is not a model that failed the work."""

    data = _queue(tmp_path, _unit(signals=_signals(errored=True), result_excerpt=""))

    grade.grade_pending(data, judge=_never, now=NOW)

    assert evidence.load(data) == []


def test_an_interrupted_unit_that_still_produced_a_result_is_judged(
    tmp_path: Path,
) -> None:
    """Something came back, so there is something to grade."""

    data = _queue(tmp_path, _unit(signals=_signals(interrupted=True)))
    judge = _Judge(_verdict(value=40))

    grade.grade_pending(data, judge=judge, now=NOW)

    rows = evidence.load(data)
    assert len(judge.prompts) == 1
    assert rows[0].grade == 0.4
    assert rows[0].graded_by == "judge"


def test_an_instruction_given_again_grades_the_answer_that_preceded_it(
    tmp_path: Path,
) -> None:
    """A free signal, so no model is asked and nothing is spent."""

    data = _queue(tmp_path, _unit(signals=_signals(retried=True)))

    grade.grade_pending(data, judge=_never, now=NOW)

    row = evidence.load(data)[0]
    assert row.grade == grade.RETRIED_GRADE
    assert row.graded_by == "signal"
    assert row.model == "claude-opus-5"
    assert row.deliberation == "high"


def test_tests_that_ran_and_passed_grade_the_unit_without_asking_anybody(
    tmp_path: Path,
) -> None:
    """The closest thing to an external checker an ordinary session contains."""

    data = _queue(tmp_path, _unit(signals=_signals(tests_ran=True, tests_passed=True)))

    grade.grade_pending(data, judge=_never, now=NOW)

    row = evidence.load(data)[0]
    assert row.grade == grade.TESTS_PASSED_GRADE
    assert row.graded_by == "signal"


def test_a_unit_with_no_model_behind_it_is_dropped(tmp_path: Path) -> None:
    """A measurement with nothing to attribute is not a measurement."""

    data = _queue(tmp_path, _unit(model=None, signals=_signals(retried=True)))

    report = grade.grade_pending(data, judge=_never, now=NOW)

    assert report["dropped"] == 1
    assert evidence.load(data) == []


def test_a_signal_graded_unit_claims_only_what_the_signals_support(
    tmp_path: Path,
) -> None:
    """Two kinds, because the free signals support exactly two."""

    data = _queue(
        tmp_path,
        _unit(
            unit_id="unit-built", changing_tool_calls=4, signals=_signals(retried=True)
        ),
        _unit(
            unit_id="unit-read", changing_tool_calls=0, signals=_signals(retried=True)
        ),
    )

    grade.grade_pending(data, judge=_never, now=NOW)

    kinds = {row.attempt_id: row.kind for row in evidence.load(data)}
    assert kinds == {"unit-built": "implement", "unit-read": "analyze"}


# --- The judge, and what it is sent ------------------------------------------


def test_the_judge_is_sent_the_units_two_ends_and_nothing_that_identifies_it(
    tmp_path: Path,
) -> None:
    """A judge told which model wrote the answer is grading the model."""

    data = _queue(tmp_path, _unit())
    judge = _Judge(_verdict())

    grade.grade_pending(data, judge=judge, now=NOW)

    sent = judge.prompts[0]
    assert "make the thing work" in sent
    assert "It works now" in sent
    assert "9" in sent and "4" in sent
    assert "300" in sent

    for absent in (
        "claude-opus-5",
        "high",
        "claude-code",
        "0123456789abcdef",
        "unit-one",
    ):
        assert absent not in sent, absent


def test_the_judge_is_offered_the_whole_kind_vocabulary(tmp_path: Path) -> None:
    """It classifies as well as grades, so it has to see what the kinds are."""

    data = _queue(tmp_path, _unit())
    judge = _Judge(_verdict())

    grade.grade_pending(data, judge=judge, now=NOW)

    for kind in evidence.KINDS:
        assert kind in judge.prompts[0], kind


def test_a_judged_unit_becomes_a_measurement_on_the_judges_own_terms(
    tmp_path: Path,
) -> None:
    """Its kind, its number out of a hundred, and nothing of the caller's."""

    data = _queue(tmp_path, _unit())

    grade.grade_pending(data, judge=_Judge(_verdict("debug", 65)), now=NOW)

    row = evidence.load(data)[0]
    assert row.kind == "debug"
    assert row.grade == 0.65
    assert row.graded_by == "judge"
    assert row.routed is False
    assert row.attempt_id == "unit-one"
    assert _waiting(data) == []


def test_a_verdict_wrapped_in_a_bridges_own_event_stream_is_still_read(
    tmp_path: Path,
) -> None:
    """A bridge wraps a model's words in its own JSON; the object is looked for."""

    data = _queue(tmp_path, _unit())
    wrapped = (
        '{"type":"item.started"}\n'
        '{"type":"item.completed","text":"' + _verdict().replace('"', '\\"') + '"}\n'
    )

    grade.grade_pending(data, judge=_Judge(wrapped), now=NOW)

    assert evidence.load(data)[0].grade == 0.8


def test_a_kind_the_judge_invented_falls_back_rather_than_reaching_the_store(
    tmp_path: Path,
) -> None:
    """The vocabulary is closed, and a grade is still worth keeping."""

    data = _queue(tmp_path, _unit())
    answer = json.dumps({"kind": "refactoring", "grade": 70, "reason": "fine"})

    grade.grade_pending(data, judge=_Judge(answer), now=NOW)

    row = evidence.load(data)[0]
    assert row.kind == "implement"
    assert row.grade == 0.7


# --- When the judge cannot be reached ----------------------------------------


def test_a_unit_no_model_could_be_reached_for_waits_for_the_next_pass(
    tmp_path: Path,
) -> None:
    """A grader that cannot run must lose nothing and must claim nothing."""

    data = _queue(tmp_path, _unit())

    report = grade.grade_pending(data, judge=_Judge(None), now=NOW)

    assert report["waiting"] == 1
    assert evidence.load(data) == []
    assert _waiting(data)[0]["attempts"] == 1


def test_an_unparseable_answer_is_a_failed_attempt_rather_than_a_number(
    tmp_path: Path,
) -> None:
    """Nothing is invented out of an answer nobody could read."""

    data = _queue(tmp_path, _unit())

    grade.grade_pending(data, judge=_Judge("I would rather not say."), now=NOW)

    assert evidence.load(data) == []
    assert _waiting(data)[0]["attempts"] == 1


def test_three_failed_attempts_settle_the_unit_and_stop_retrying_it(
    tmp_path: Path,
) -> None:
    """Waiting forever is its own kind of lost measurement."""

    data = _queue(tmp_path, _unit())

    for _ in range(3):
        grade.grade_pending(data, judge=_Judge(None), now=NOW)

    assert _waiting(data) == []
    assert evidence.load(data) == []


# --- The budget, and it is a hard one ----------------------------------------


def test_the_budget_stops_the_pass_and_leaves_the_rest_pending(
    tmp_path: Path,
) -> None:
    """One call at a time, and everything above the line waits."""

    data = _queue(
        tmp_path,
        _unit(unit_id="unit-one"),
        _unit(unit_id="unit-two"),
        _unit(unit_id="unit-three"),
    )
    judge = _Judge(_verdict(), _verdict(), _verdict())

    report = grade.grade_pending(data, budget=1, judge=judge, now=NOW)

    assert len(judge.prompts) == 1
    assert report["judged"] == 1
    assert [row["unit_id"] for row in _waiting(data)] == ["unit-two", "unit-three"]


def test_a_unit_left_below_the_budget_line_is_not_charged_an_attempt(
    tmp_path: Path,
) -> None:
    """This pass's own thrift is not a failure of the Unit's."""

    data = _queue(tmp_path, _unit(unit_id="unit-one"), _unit(unit_id="unit-two"))

    grade.grade_pending(data, budget=1, judge=_Judge(_verdict()), now=NOW)

    assert "attempts" not in _waiting(data)[0]


def test_a_days_worth_of_gradings_already_bought_stops_the_pass_entirely(
    tmp_path: Path,
) -> None:
    """A hard limit rather than a guideline."""

    data = _queue(tmp_path, _unit())
    evidence.append(
        data,
        [
            {
                "attempt_id": f"old-{index}",
                "at": grade._stamp(NOW - timedelta(hours=2)),
                "kind": "implement",
                "model": "claude-opus-5",
                "deliberation": "high",
                "grade": 0.5,
                "graded_by": "judge",
                "tokens": {},
                "routed": False,
            }
            for index in range(grade.DAILY_JUDGE_LIMIT)
        ],
    )

    report = grade.grade_pending(data, judge=_never, now=NOW)

    assert report["capped"] is True
    assert len(_waiting(data)) == 1


def test_gradings_older_than_a_day_do_not_count_against_the_limit(
    tmp_path: Path,
) -> None:
    """The cap is a rate rather than a total."""

    data = _queue(tmp_path, _unit())
    evidence.append(
        data,
        [
            {
                "attempt_id": f"old-{index}",
                "at": grade._stamp(NOW - timedelta(days=3)),
                "kind": "implement",
                "model": "claude-opus-5",
                "deliberation": "high",
                "grade": 0.5,
                "graded_by": "judge",
                "tokens": {},
                "routed": False,
            }
            for index in range(grade.DAILY_JUDGE_LIMIT)
        ],
    )

    report = grade.grade_pending(data, judge=_Judge(_verdict()), now=NOW)

    assert report["capped"] is False
    assert report["judged"] == 1


# --- Two copies must not both grade ------------------------------------------


def test_a_second_pass_holding_no_lock_does_nothing_at_all(tmp_path: Path) -> None:
    """Both would read the same queue and both would buy the same judgement."""

    data = _queue(tmp_path, _unit())

    with grade._lock(data) as first, grade._lock(data) as second:
        assert first is True
        assert second is False


def test_a_lock_left_by_a_dead_process_is_taken_over(tmp_path: Path) -> None:
    """A crash must not stop a machine grading anything ever again."""

    import os

    data = _queue(tmp_path, _unit())
    stale = data / "grade.lock"
    stale.write_text("", encoding="utf-8")
    os.utime(stale, (0, 0))

    with grade._lock(data) as held:
        assert held is True


# --- What a session's end actually pays for ----------------------------------


def test_the_session_end_pass_asks_no_model_and_hands_the_rest_over(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """The free half is local arithmetic; the judging happens elsewhere."""

    data = _queue(
        tmp_path, _unit(), _unit(unit_id="unit-two", signals=_signals(retried=True))
    )
    started: list[list[str]] = []

    def popen(command: list[str], **options: Any) -> Any:
        started.append(command)
        assert options["cwd"] == grade._safe_home()
        assert options["start_new_session"] is True
        return object()

    monkeypatch.setattr(subprocess, "Popen", popen)

    report = grade.hook_pass(data)

    assert report["graded"] == 1
    assert report["judged"] == 0
    assert report["pending"] == 1
    assert report["dispatched"] is True
    assert started[0][:2] == ["uv", "run"]
    assert "--once" in started[0]


def test_nothing_is_dispatched_when_nothing_is_left_to_judge(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """A pass that spends nothing starts nothing."""

    data = _queue(tmp_path, _unit(signals=_signals(retried=True)))

    def popen(command: list[str], **options: Any) -> Any:
        raise AssertionError("the pass started a process it did not need")

    monkeypatch.setattr(subprocess, "Popen", popen)

    assert grade.hook_pass(data)["dispatched"] is False


def test_the_grader_records_that_it_ran_where_status_reads_it(
    tmp_path: Path,
) -> None:
    """Reported by `status` and by nothing else."""

    data = _queue(tmp_path, _unit(signals=_signals(retried=True)))

    grade.grade_pending(data, judge=_never, now=NOW)

    state = json.loads((data / "grader.json").read_text(encoding="utf-8"))
    assert state["last_run_at"] == grade._stamp(NOW)
    assert state["graded"] == 1


def test_the_module_never_lets_a_failure_reach_its_caller(tmp_path: Path) -> None:
    """Grading is a side effect of finished work and never a failure of it."""

    blocked = tmp_path / "blocked"
    blocked.write_text("not a directory", encoding="utf-8")

    assert grade.main(["--once", "--data", str(blocked)]) == 0
