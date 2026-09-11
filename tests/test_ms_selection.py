"""The decision itself: what is chosen, and what is said when nothing can be."""

from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
from support.fake_binary import path_holding

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SKILL: Path = REPO_ROOT / "skills" / "models" / "model-selector"
SCRIPTS: Path = SKILL / "scripts"
SELECT: Path = SCRIPTS / "selection.py"

# How many seeds a per-call probability is read off. The band in the ticket is
# stated over exactly this many, and it is wide enough that a tenth measured
# over them is a tenth rather than a run of luck.
SEEDS: int = 1000

# How many seeds a property asserted of every answer is read over. Enough that
# a rule broken by one answer in fifty is caught, few enough to stay quick.
DRAWS: int = 200

# The flags that hold a pool to the maker a fixture profile chooses: the
# caller's own provider, and the Harness that says which provider that is.
LIMITED: tuple[str, ...] = ("--scope=limited", "--harness=claude-code")

# Every model Anthropic offers in the shipped catalogue, which is the pool a
# fixture profile choosing Anthropic alone ranks. Named here rather than read
# off the catalogue, so that a fixture whose premise rests on the two models
# nothing else in it measures says which two those are.
FABLE: str = "claude-fable-5-1"
HAIKU: str = "claude-haiku-4-5-20251001"

# Both stakes a caller may declare, stated here rather than read off the module
# so that a rule meant to hold at either is asked at each by name.
STAKES_ASKED: tuple[str, ...] = ("reversible", "high")

# The retired rule's own sentences, whitespace-collapsed before matching so
# that a line break falling inside one of them hides nothing. Each states, as
# the contract in force, an answer read off a draw over the whole pool rather
# than off the means, or the cost the expected-cost arithmetic used to rank on
# (issue #288). The identifiers that arithmetic went by are deliberately absent:
# a list naming them would itself be a surface carrying them.
RETIRED: tuple[str, ...] = (
    "ranking on a draw",
    "ranked on a draw",
    "rather than on a mean",
    "one quantile spent",
    "tickets in one lottery",
    "rather than from a wager",
    "decides rather than draws",
    "decided rather than drawn",
    "the cost of finishing",
    "per expected failure",
)


def _surfaces() -> list[Path]:
    """Every file that says in prose how the answer is arrived at.

    The engine and the Skill that fronts it, the runner that asks it and
    renders what came back, the module where the rule is written down for the
    collection, and the page a reader meets first. A rule stated in a docstring
    binds a reader exactly as the page spelling it out does, so the scan takes
    the scripts and their shipped data as well as the prose beside them.
    """

    trees = [
        REPO_ROOT / "skills" / "models" / "model-selector",
        REPO_ROOT / "skills" / "code" / "orchestrate",
    ]
    found = [
        path
        for tree in trees
        for path in sorted(tree.rglob("*"))
        if path.suffix in {".py", ".md", ".json"}
    ]
    return [
        *found,
        REPO_ROOT / "docs" / "rules" / "routing.md",
        REPO_ROOT / "README.md",
    ]


@pytest.fixture(params=_surfaces(), ids=lambda path: str(path.relative_to(REPO_ROOT)))
def subject(request: pytest.FixtureRequest) -> Path:
    """One shipped surface of the choosing rule."""

    surface: Path = request.param
    return surface


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


for _dependency in ("catalogue", "profiles", "evidence", "launch"):
    _module(_dependency)

# Registered under a name of its own: this module's file name is the standard
# library's `select`, and shadowing that inside a test run would reach far
# beyond this file.
select = _module("selection", "ms_selection")


def _answer(capsys: pytest.CaptureFixture[str], *flags: str) -> dict[str, Any]:
    """Run the entry point in process and return the one object it printed."""

    assert select.main(list(flags)) == 0
    printed = capsys.readouterr().out.strip().splitlines()
    assert len(printed) == 1
    parsed: dict[str, Any] = json.loads(printed[0])
    return parsed


def _profile(data_dir: Path, **overrides: Any) -> None:
    """Write a profile that chooses Anthropic and pays for it in Claude Code.

    Every model Anthropic offers is therefore eligible. A test that needs a
    smaller pool shapes it by the makers it chooses or by a lock, never by a
    list of models, which a profile no longer carries.
    """

    document: dict[str, Any] = {
        "harnesses": ["claude-code"],
        "makers": ["anthropic"],
        "channels": [
            {
                "provider": "anthropic",
                "harness": "claude-code",
                "pay": "subscription",
                "plan": "Claude Max 20x",
            }
        ],
        "answered_at": None,
    }
    document.update(overrides)
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "profile.json").write_text(json.dumps(document), encoding="utf-8")


def _refresh(data_dir: Path, *models: dict[str, Any]) -> None:
    """Add models to the catalogue the way a refresh would."""

    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "catalogue.json").write_text(
        json.dumps({"generated_at": "2026-09-06T00:00:00Z", "models": list(models)}),
        encoding="utf-8",
    )


def _store(data_dir: Path, *groups: tuple[str, str, str | None, float, int]) -> None:
    """Write a store from (kind, model, level, grade, rows) groups.

    Every row of a group is the same graded attempt under a different id, which
    is what a run of identical outcomes looks like in the real ledger and the
    only thing the success posterior reads.
    """

    lines: list[str] = []
    for index, (kind, model, level, grade, rows) in enumerate(groups):
        for row in range(rows):
            lines.append(
                json.dumps(
                    {
                        "attempt_id": f"ms-fixture-{index}-{row}",
                        "at": "2026-09-01T00:00:00Z",
                        "kind": kind,
                        "model": model,
                        "deliberation": level,
                        "grade": grade,
                        "graded_by": "checker",
                        "routed": True,
                    }
                )
            )

    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "measurements.jsonl").write_text(
        "".join(f"{line}\n" for line in lines), encoding="utf-8"
    )


def _clearing(data_dir: Path) -> None:
    """Write a store whose cheapest clearing point is not its likeliest.

    Sonnet at `high` clears the floor at about 0.87 for USD 1.50, Opus clears
    it everywhere and reads near 0.98 at `max` for four times the money, and
    the fastest point that clears is Opus at `low` — three different answers
    to three different questions off one store. Fable and Haiku, the other two
    models Anthropic offers, have failed the work, so neither is a fourth.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "low", 1.0, 20),
        ("implement", "claude-sonnet-5", "high", 1.0, 30),
        ("implement", "claude-sonnet-5", "low", 0.0, 10),
        ("implement", FABLE, "high", 0.0, 10),
        ("implement", HAIKU, None, 0.0, 10),
    )


def _boundary(data_dir: Path) -> None:
    """Write a store whose one clearing point has a boundary on both dimensions.

    Only Opus at `xhigh` clears the floor, so the answer has three cheaper
    levels of its own model below it and cheaper models beside it: Sonnet at
    the same level, and Haiku, which has no level at all and is taken at its
    one point — which is what makes every exploration of either dimension find
    something to try. Fable has failed at `xhigh` and costs more than the
    answer, so it clears nothing and is never tried.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "xhigh", 1.0, 20),
        ("implement", "claude-opus-5", "low", 0.0, 10),
        ("implement", "claude-sonnet-5", "high", 0.0, 10),
        ("implement", FABLE, "xhigh", 0.0, 10),
        ("implement", HAIKU, None, 0.0, 10),
    )


def _under(data_dir: Path) -> None:
    """Write a store no point of which clears the floor.

    Every model Anthropic offers has rows here, and only Opus at `high` ever
    finished, so the prior of an untried model is not left to clear it.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "low", 0.0, 8),
        ("implement", "claude-opus-5", "high", 1.0, 8),
        ("implement", "claude-sonnet-5", "high", 0.0, 8),
        ("implement", FABLE, "high", 0.0, 8),
        ("implement", HAIKU, None, 0.0, 8),
    )


def _bridged(data_dir: Path, **overrides: Any) -> None:
    """Write a profile that chooses both makers and can bridge to either.

    The profile a process caller is answered against: two Bridges the machine
    might have, every model each maker offers, and a channel saying who pays
    for each. What separates the two makers in these tests is therefore never
    the profile but the `PATH`, which is the fact under test.
    """

    document: dict[str, Any] = {
        "harnesses": ["claude-code", "codex"],
        "makers": ["anthropic", "openai"],
        "channels": [
            {
                "provider": "anthropic",
                "harness": "claude-code",
                "pay": "subscription",
                "plan": "Claude Max 20x",
            },
            {
                "provider": "openai",
                "harness": "codex",
                "pay": "subscription",
                "plan": "ChatGPT Pro",
            },
        ],
    }
    document.update(overrides)
    _profile(data_dir, **document)


def _named_in(answer: dict[str, Any]) -> set[str]:
    """Return every model the answer names, chosen or offered beside it.

    A point excluded from the pool is absent from both, and reading the chosen
    model alone would pass on a pool that still held the excluded point and
    merely ranked something else above it.
    """

    return {answer["model"], *(row["model"] for row in answer["alternatives"])}


def _over_seeds(
    capsys: pytest.CaptureFixture[str], flags: Sequence[str]
) -> list[dict[str, Any]]:
    """Return one answer per seed of the band criterion 1 is read over."""

    return [_answer(capsys, *flags, f"--seed={seed}") for seed in range(SEEDS)]


# Enough alternatives that every model in any fixture pool is listed beside the
# answer, so that `_named_in` reads the whole pool rather than its top three.
EVERY: str = "--n=20"

# Every model each maker in the shipped catalogue offers. Named here rather
# than read off the catalogue, because a test that took its pool from the data
# under test would pass just as well on a catalogue that had lost a model.
ANTHROPIC: frozenset[str] = frozenset(
    {"claude-fable-5-1", "claude-opus-5", "claude-sonnet-5", HAIKU}
)
OPENAI: frozenset[str] = frozenset(
    {"gpt-6-astra", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"}
)


# The eight kinds, stated here rather than imported: a caller outside this
# Skill classifies work into exactly this vocabulary, and a test that read it
# off the module under test would pass on both halves being wrong together.
VOCABULARY: tuple[str, ...] = (
    "mechanical",
    "implement",
    "design",
    "debug",
    "review",
    "analyze",
    "prose",
    "converse",
)


def test_the_vocabulary_is_printed_for_a_caller_that_has_to_classify_work(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A machine caller cannot read this Skill's prose, so it asks for the list.

    Orchestrate classifies every ticket it routes and may not reach into this
    Skill's data directory to learn what it may classify it as, so the eight
    kinds and the sentence that tells them apart come back through the same
    entry point the answer does (issue #292).
    """

    answered = _answer(capsys, "--kinds")

    assert answered["ok"] is True
    assert [entry["kind"] for entry in answered["kinds"]] == list(VOCABULARY)
    assert all(entry["note"].strip() for entry in answered["kinds"])
    told = {entry["kind"]: entry["note"] for entry in answered["kinds"]}
    assert "already decided" in told["mechanical"]
    assert "for a person to read" in told["prose"]


def test_an_empty_data_directory_still_answers_and_exits_zero(tmp_path: Path) -> None:
    """This runs inside somebody else's turn, so there is no way to say stop.

    Nobody has chosen a maker, so nothing is eligible and the answer is to keep
    the seat the caller has; with no `--seat` named, that answer names no
    model, and its note says what to run.
    """

    # The working directory is the repository, which nothing in this run
    # replaces; the script's own directory is what puts its siblings on the path.
    finished = subprocess.run(
        [sys.executable, str(SELECT), f"--data={tmp_path}", "--kind=implement"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    answer = json.loads(finished.stdout)
    assert finished.returncode == 0
    assert answer["ok"] is True
    assert answer["attempt_id"].startswith("ms-")
    assert answer["basis"] == "inherit"
    assert answer["launch"]["how"] == "inherit"
    assert answer["model"] is None
    assert "/model-selector setup" in answer["note"]


def test_a_malformed_command_line_is_the_only_thing_that_fails(
    tmp_path: Path,
) -> None:
    """A closed vocabulary is rejected at the door rather than guessed at."""

    with pytest.raises(SystemExit) as refused:
        select.main([f"--data={tmp_path}", "--kind=vibes"])

    assert refused.value.code != 0


def test_the_shipped_priors_send_easy_work_cheap_and_hard_work_deep(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The priors are the answer on a machine that has measured nothing yet.

    Asked at high stakes, which is a decided request rather than a drawn one.
    What is read here is what the priors hold, and a store this empty has
    posteriors wide enough that a draw would answer differently every call —
    so a drawn request would be reading the die rather than the priors.
    """

    _profile(tmp_path)
    seat = [
        "--harness=claude-code",
        "--seat=claude-opus-5@xhigh",
        "--stakes=high",
        f"--data={tmp_path}",
    ]

    mechanical = _answer(capsys, "--kind=mechanical", *seat)
    design = _answer(capsys, "--kind=design", *seat)

    assert mechanical["model"] != design["model"]
    assert mechanical["expected"]["cost_usd"] < design["expected"]["cost_usd"]
    assert design["model"] in ("claude-opus-5", "claude-fable-5-1")
    assert design["deliberation"] in ("high", "xhigh", "max")
    assert design["expected"]["cost_usd"] < 10.0
    assert mechanical["basis"] == "prior"


def test_an_unrecognised_model_lock_never_empties_the_pool(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A typo still needs an answer, and gets one with the lock reported."""

    _profile(tmp_path)
    answer = _answer(
        capsys, f"--data={tmp_path}", "--harness=claude-code", "--model=gpt-9-imaginary"
    )

    assert answer["ok"] is True
    assert answer["model"]
    assert answer["launch"]["how"] != "inherit"
    assert "gpt-9-imaginary" in answer["note"]


def test_a_family_lock_takes_the_newest_model_and_says_so(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A family names a generation, and the answer is one point rather than a set."""

    _refresh(
        tmp_path,
        {
            "id": "claude-sonnet-6",
            "provider": "anthropic",
            "family": "sonnet",
            "aliases": ["sonnet"],
            "deliberation": ["low", "high"],
            "price": {
                "input": 3.0,
                "cache_read": 0.3,
                "cache_write": 3.75,
                "output": 15.0,
            },
            "reasoning_billed_as": "output",
            "capability": 0.8,
            "released": "2026-08-01",
        },
    )
    _profile(tmp_path)

    answer = _answer(capsys, f"--data={tmp_path}", "--model=sonnet", "--scope=limited")

    assert answer["model"] == "claude-sonnet-6"
    assert "newest" in answer["note"]


def test_a_deliberation_lock_no_candidate_supports_falls_to_the_nearest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The lock is honoured as closely as the candidates allow, and the gap is said."""

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--model=grok",
        "--deliberation=max",
        "--scope=all",
    )

    assert answer["model"] == "grok-4.6"
    assert answer["deliberation"] == "xhigh"
    assert "max" in answer["note"]


def test_a_point_that_cannot_be_priced_is_ranked_last_but_stays_eligible(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An unpriceable model must not read as a free one and win everything.

    Both it and Sonnet clear the floor, so price is what is left to order them
    on and the one nothing can price has to lose it — on the answer, and on the
    calls that explore, where a point nothing can price is never cheaper than
    the answer. A null cost is a null cost: read as a nought it would make the
    model nothing is known about the cheapest thing on the frontier by having
    nothing behind it.
    """

    _refresh(
        tmp_path,
        {
            "id": "test-unpriced",
            "provider": "anthropic",
            "family": "unpriced",
            "aliases": ["unpriced"],
            "deliberation": ["high"],
            "price": None,
            "reasoning_billed_as": "unknown",
            "capability": 0.99,
            "released": "2026-09-01",
        },
    )
    _profile(tmp_path)
    _store(tmp_path, ("implement", "claude-sonnet-5", "high", 1.0, 20))

    answers = [
        _answer(
            capsys, f"--data={tmp_path}", "--scope=limited", EVERY, f"--seed={seed}"
        )
        for seed in range(DRAWS)
    ]

    assert "test-unpriced" not in {answer["model"] for answer in answers}
    assert {answer["model"] for answer in answers if answer["explored"] is None} == {
        "claude-sonnet-5"
    }
    for answer in answers:
        listed = {row["model"]: row for row in answer["alternatives"]}
        assert listed["test-unpriced"]["cost_usd"] is None
        assert listed["test-unpriced"]["per_success_cost_usd"] is None
        assert listed["test-unpriced"]["per_success_seconds"] is not None


def test_the_answer_is_the_cheapest_point_that_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """No point below the floor is taken for being cheap.

    The floor is what the job getting done means here, and among the points
    that clear it the order is on price divided by the chance of success — so
    the answer is neither the likeliest point on the table nor the cheapest
    point on it. On this store the cheapest attempt that clears the floor is
    also the cheapest finished job, so the answer is the one the per-attempt
    order gave before the division was introduced.
    """

    _clearing(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    assert answer["explored"] is None
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "high")
    assert answer["expected"]["p_success"] >= select.FLOOR
    beaten = {row["model"]: row for row in answer["alternatives"]}
    assert beaten["claude-opus-5"]["p_success"] > answer["expected"]["p_success"]
    assert beaten["claude-opus-5"]["cost_usd"] > answer["expected"]["cost_usd"]


def test_where_nothing_clears_the_floor_the_likeliest_point_is_taken(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A pool that cannot promise the work is done is ranked on doing it."""

    _under(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    assert answer["explored"] is None
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["expected"]["p_success"] < select.FLOOR
    for row in answer["alternatives"]:
        assert row["p_success"] <= answer["expected"]["p_success"]


def test_a_run_ordered_on_time_takes_the_fastest_point_that_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The floor is the same floor; what orders the survivors is the caller's."""

    _clearing(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0")

    fastest = _answer(capsys, *flags, "--objective=time")
    cheapest = _answer(capsys, *flags)

    assert fastest["explored"] is None
    assert (fastest["model"], fastest["deliberation"]) == ("claude-opus-5", "low")
    assert fastest["expected"]["p_success"] >= select.FLOOR
    assert fastest["expected"]["seconds"] < cheapest["expected"]["seconds"]
    assert fastest["expected"]["cost_usd"] > cheapest["expected"]["cost_usd"]


def _finishing(data_dir: Path) -> None:
    """Write a store whose cheapest attempt is not its cheapest finished job.

    Opus at `low` and at `medium` both clear the floor on rows of their own.
    `low` is the cheaper attempt, by the money and by the clock, and it finishes
    about 0.82 of the time; `medium` costs about 1.14 times as much and takes
    about 1.11 times as long, and finishes about 0.98 of the time. That gap in
    chance is wider than the gap in price, so `medium` is the cheaper finished
    job on both counts.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "low", 0.8, 40),
        ("implement", "claude-opus-5", "medium", 1.0, 40),
    )


def _point(
    capsys: pytest.CaptureFixture[str], flags: Sequence[str], model: str, level: str
) -> dict[str, Any]:
    """Return the answer locked to one point, which is what the store says of it.

    A model with no effort control has one point and no level to lock, so its
    lock is the model's alone.
    """

    locks = [f"--model={model}"]
    if level is not None:
        locks.append(f"--deliberation={level}")
    return _answer(capsys, *flags, *locks)


@pytest.mark.parametrize(
    ("objective", "attempt"),
    (("cost", "cost_usd"), ("time", "seconds")),
)
def test_the_answer_is_the_point_that_finishes_the_job_for_the_least(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], objective: str, attempt: str
) -> None:
    """A point that fails is paid for again, so its price is read per success.

    Both points clear the floor, so neither is a lower chance bought with
    price. The cheaper attempt succeeds about 0.82 of the time and needs about
    1.22 attempts per finished job; the dearer one, at about 0.98, needs about
    1.02. What a finished job costs is the price divided by the chance of
    success, and on that the dearer attempt is the cheaper job — in money and
    in elapsed time alike.
    """

    _finishing(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0")

    answer = _answer(capsys, *flags, f"--objective={objective}")
    cheap = _point(capsys, flags, "claude-opus-5", "low")
    sure = _point(capsys, flags, "claude-opus-5", "medium")

    assert select.FLOOR <= cheap["expected"]["p_success"] < 0.85
    assert sure["expected"]["p_success"] > 0.95
    assert cheap["expected"][attempt] < sure["expected"][attempt]
    total = f"per_success_{attempt}"
    assert sure["expected"][total] < cheap["expected"][total]
    assert answer["explored"] is None
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "medium")
    assert answer["expected"][total] == sure["expected"][total]


def test_the_answer_carries_the_total_it_was_ranked_on(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Beside what one attempt costs, the answer says what a finished job costs.

    Both figures are the per-attempt ones divided by the chance of success,
    rounded as their per-attempt figures are: the money to four places and the
    clock to whole seconds.
    """

    _finishing(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    expected = answer["expected"]
    chance = expected["p_success"]
    assert expected["per_success_cost_usd"] == pytest.approx(
        expected["cost_usd"] / chance, rel=1e-3
    )
    assert expected["per_success_cost_usd"] == round(
        expected["per_success_cost_usd"], 4
    )
    assert isinstance(expected["per_success_seconds"], int)
    assert expected["per_success_seconds"] == pytest.approx(
        expected["seconds"] / chance, abs=1
    )
    for row in answer["alternatives"]:
        assert row["per_success_cost_usd"] == pytest.approx(
            row["cost_usd"] / row["p_success"], rel=1e-3
        )
        assert isinstance(row["per_success_seconds"], int)


def test_an_answer_ranked_on_its_chances_still_carries_the_total(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Where nothing clears the floor the answer is ranked on chance, and says both."""

    _under(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    assert answer["expected"]["p_success"] < select.FLOOR
    assert answer["expected"]["per_success_cost_usd"] > answer["expected"]["cost_usd"]
    assert answer["expected"]["per_success_seconds"] > answer["expected"]["seconds"]


def test_an_inheriting_answer_carries_no_total(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Nothing was priced, so nothing is divided, and the members are still there."""

    answer = _answer(capsys, f"--data={tmp_path}", "--seat=claude-opus-5@xhigh")

    assert answer["basis"] == "inherit"
    assert answer["expected"]["per_success_cost_usd"] is None
    assert answer["expected"]["per_success_seconds"] is None


def test_an_explored_answer_carries_the_total_of_the_point_it_tried(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The figures describe the point that was run, not the one stepped over."""

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    answers = _over_seeds(capsys, flags)
    explored = [answer for answer in answers if answer["explored"] is not None]

    assert explored
    for answer in explored[:20]:
        point = _point(capsys, flags, answer["model"], answer["deliberation"])
        for member in ("per_success_cost_usd", "per_success_seconds"):
            assert answer["expected"][member] == point["expected"][member]


def test_the_step_up_is_the_likelier_point_that_finishes_for_the_least(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A failure is answered on the same total the first answer was.

    Both Opus points are measured, clear the floor, and are likelier than the
    Sonnet point that failed. `low` is the cheaper attempt and `medium` the
    cheaper finished job, so the step is `medium`.
    """

    _finishing(tmp_path)

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=implement",
        "--after=claude-sonnet-5@low",
    )

    assert "one step up" in (answer["note"] or "")
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "medium")


def test_with_nothing_measured_to_step_to_the_step_is_still_read_per_success(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The floorless step is ordered on the same total as the rest.

    Sonnet at `low` failed. Nothing measured above it clears the floor, so
    every likelier point is a candidate. Sonnet at `medium` is the cheapest
    attempt among them and finishes about half the time; Sonnet at `high` costs
    a little more and finishes about two times in three, which makes it the
    cheaper finished job.
    """

    _profile(tmp_path)
    _store(
        tmp_path,
        ("implement", "claude-sonnet-5", "low", 0.0, 10),
        ("implement", "claude-sonnet-5", "medium", 0.5, 20),
        ("implement", "claude-sonnet-5", "high", 0.7, 20),
    )
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    answer = _answer(capsys, *flags, "--after=claude-sonnet-5@low")
    medium = _point(capsys, flags, "claude-sonnet-5", "medium")
    high = _point(capsys, flags, "claude-sonnet-5", "high")

    assert medium["expected"]["cost_usd"] < high["expected"]["cost_usd"]
    assert (
        high["expected"]["per_success_cost_usd"]
        < (medium["expected"]["per_success_cost_usd"])
    )
    assert high["expected"]["p_success"] < select.FLOOR
    assert "one step up" in (answer["note"] or "")
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "high")


def _priced(model_id: str, scale: float) -> dict[str, Any]:
    """Return a one-level Anthropic model whose rate card is Sonnet's times a scale.

    Every row of the fixture that uses it is `implement` at `high`, and none
    carries a token count, so each model's forecast is the kind's own and what
    separates their bills is the scale alone.
    """

    return {
        "id": model_id,
        "provider": "anthropic",
        "family": model_id,
        "aliases": [model_id],
        "deliberation": ["high"],
        "price": {
            "input": 2.0 * scale,
            "cache_read": 0.2 * scale,
            "cache_write": 2.5 * scale,
            "output": 10.0 * scale,
            "currency": "USD",
            "unit": "per_mtok",
        },
        "reasoning_billed_as": "output",
        "capability": 0.9,
        "released": "2026-09-01",
    }


def test_the_alternatives_that_clear_the_floor_are_listed_per_success(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The list a caller reads its fallbacks off is ordered on the same total.

    Three models clear the floor. `test-sure` is the answer on any reading.
    Of the other two, `test-shaky` is the cheaper attempt and succeeds about
    0.82 of the time, `test-steady` costs about a tenth more and succeeds about
    0.98 of the time — so it is the cheaper finished job and is listed first.
    """

    _refresh(
        tmp_path,
        _priced("test-sure", 1.0),
        _priced("test-shaky", 1.1),
        _priced("test-steady", 1.2),
    )
    _profile(tmp_path)
    _store(
        tmp_path,
        ("implement", "test-sure", "high", 1.0, 40),
        ("implement", "test-shaky", "high", 0.8, 40),
        ("implement", "test-steady", "high", 1.0, 40),
    )

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    listed = answer["alternatives"]
    assert answer["model"] == "test-sure"
    assert [row["model"] for row in listed] == ["test-steady", "test-shaky"]
    assert all(row["p_success"] >= select.FLOOR for row in listed)
    assert listed[1]["cost_usd"] < listed[0]["cost_usd"]
    assert listed[0]["per_success_cost_usd"] < listed[1]["per_success_cost_usd"]


def _measured_beside_prior(data_dir: Path) -> None:
    """Write a store whose one measured clearing point is not its cheapest.

    Opus at `high` has twenty good `mechanical` rows of its own, and at `low`
    ten bad ones. Sonnet has no row at all, and the shipped priors put every
    level of it above the floor on work this easy for a fraction of Opus's
    price — so ranked on the means alone, an estimate nothing on this machine
    has ever tested would win every call.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("mechanical", "claude-opus-5", "high", 1.0, 20),
        ("mechanical", "claude-opus-5", "low", 0.0, 10),
    )


@pytest.mark.parametrize("stakes", STAKES_ASKED)
def test_a_measured_point_that_clears_the_floor_outranks_a_cheaper_prior(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], stakes: str
) -> None:
    """An estimate the evidence has never seen doing the work is not the answer.

    High stakes wants the best point the evidence knows of, and a reversible
    call's ordinary answer is the same answer: where a point measured for the
    kind clears the floor, the answer is chosen among those alone. Finding out
    whether the cheaper, untried point would do is exploration's job.
    """

    _measured_beside_prior(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=mechanical", f"--stakes={stakes}")

    answers = [_answer(capsys, *flags, f"--seed={seed}") for seed in range(DRAWS)]
    plain = [answer for answer in answers if answer["explored"] is None]

    assert plain
    for answer in plain:
        assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
        assert answer["basis"] == "measured"


def test_a_verdict_carried_from_a_harder_kind_does_not_outrank_a_measured_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Rows of another kind make a point pooled for this one, never measured.

    Sonnet has only `design` rows, every one of them good, and carried down to
    `mechanical` its estimate clears the floor for less than Opus costs. Opus
    has measured `mechanical` rows that clear it too, and those are the only
    evidence here about the work actually being asked for.
    """

    _profile(tmp_path)
    _store(
        tmp_path,
        ("design", "claude-sonnet-5", "high", 1.0, 20),
        ("mechanical", "claude-opus-5", "high", 1.0, 20),
    )

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--stakes=high"
    )
    carried = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=mechanical",
        "--model=claude-sonnet-5",
        "--deliberation=low",
    )

    assert carried["basis"] == "pooled"
    assert carried["expected"]["p_success"] >= select.FLOOR
    assert carried["expected"]["cost_usd"] < answer["expected"]["cost_usd"]
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["basis"] == "measured"


def test_where_no_measured_point_clears_the_floor_the_whole_pool_is_ranked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Measured points go first only where one of them can promise the work.

    Opus's own `mechanical` rows all failed, so nothing measured clears the
    floor and the answer is what it always was: of the points whose estimate
    clears it, prior or not, the one with the lowest price per finished job.
    """

    _profile(tmp_path)
    _store(tmp_path, ("mechanical", "claude-opus-5", "high", 0.0, 10))

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--stakes=high"
    )

    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "low")
    assert answer["basis"] == "prior"
    assert answer["expected"]["p_success"] >= select.FLOOR


def test_an_explored_answer_can_still_name_a_point_with_no_rows_of_its_own(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An untried point is still tried, on the calls spent on trying things."""

    _measured_beside_prior(tmp_path)

    answers = _over_seeds(capsys, (*LIMITED, f"--data={tmp_path}", "--kind=mechanical"))
    explored = [answer for answer in answers if answer["explored"] is not None]

    assert any(answer["basis"] == "prior" for answer in explored)


def test_the_alternatives_still_offer_the_point_nothing_has_measured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Measured points are ranked first, and nothing else is filtered out."""

    _measured_beside_prior(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--stakes=high"
    )

    assert answer["model"] == "claude-opus-5"
    assert "claude-sonnet-5" in {row["model"] for row in answer["alternatives"]}


def test_the_step_up_prefers_a_measured_point_that_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A failure is answered with the evidence, not with a cheaper guess.

    Every level of Sonnet is likelier than the Opus point that failed and
    cheaper than Opus at `high`, and none of them has a row. The step is the
    measured point that clears the floor.
    """

    _measured_beside_prior(tmp_path)

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=mechanical",
        "--after=claude-opus-5@low",
    )

    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["basis"] == "measured"
    assert "one step up" in (answer["note"] or "")


def test_a_failed_point_nothing_has_measured_is_still_found_and_stepped_from(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller may have run an unmeasured point, and may name it when it fails.

    Sonnet at `low` has no row, and its prior is likelier than anything Opus
    has measured here, so no measured point is a step up from it and the step
    is the likelier point with the lowest price per finished job: the next
    level of Sonnet.
    """

    _measured_beside_prior(tmp_path)

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=mechanical",
        "--after=claude-sonnet-5@low",
    )

    assert "nothing here matches" not in (answer["note"] or "")
    assert "one step up" in (answer["note"] or "")
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "medium")


def test_where_no_measured_point_steps_up_the_step_is_the_likelier_one_that_finishes_for_the_least(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """With no measured point to prefer, the step is the likelier point with the
    lowest price per finished job.

    Haiku, the cheapest model Anthropic offers, has failed this kind as often
    as the Opus point did, so it is no likelier and is not a step up from it.
    """

    _profile(tmp_path)
    _store(
        tmp_path,
        ("mechanical", "claude-opus-5", "low", 0.0, 10),
        ("mechanical", HAIKU, None, 0.0, 10),
    )

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=mechanical",
        "--after=claude-opus-5@low",
    )

    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "low")
    assert answer["basis"] == "prior"


def test_a_profile_whose_makers_reach_nothing_inherits_the_callers_own_seat(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Where nothing can be chosen the answer is to keep the seat you have.

    The one maker chosen is not the caller's own, and nothing this Harness has
    reaches it, so no point is eligible and reachable at once.
    """

    _profile(tmp_path, makers=["openai"], channels=[])

    answer = _answer(capsys, f"--data={tmp_path}", "--seat=claude-opus-5@xhigh")

    assert answer["ok"] is True
    assert answer["basis"] == "inherit"
    assert answer["launch"]["how"] == "inherit"
    assert answer["model"] == "claude-opus-5"
    assert answer["deliberation"] == "xhigh"
    assert answer["note"]


def test_a_model_with_no_effort_control_is_answered_with_a_null_level(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """One point rather than five, and the answer says so rather than inventing one."""

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--model=haiku",
        "--scope=all",
    )

    assert answer["model"] == "claude-haiku-4-5-20251001"
    assert answer["deliberation"] is None
    assert answer["launch"]["subagent_type"] == "kntnt-haiku"


def test_the_answer_carries_the_channel_that_pays_for_the_chosen_point(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller reading the answer can see who is being billed for it."""

    _profile(tmp_path)

    answer = _answer(capsys, f"--data={tmp_path}", "--harness=claude-code")

    assert answer["channel"] == {
        "provider": "anthropic",
        "pay": "subscription",
        "plan": "Claude Max 20x",
        "harness": "claude-code",
    }


def test_about_a_tenth_of_reversible_calls_explore_and_no_high_stakes_call_does(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A store that only ever runs its favourite never learns a cheaper point sufficed.

    So a bounded share of reversible calls buys the row instead of the answer.
    It is a probability per call rather than a counter, so no particular call is
    the one that explores; what is asserted is the share over many calls. High
    stakes wants the best estimate on the table and never explores at all.
    """

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    reversible = _over_seeds(capsys, flags)
    careful = _over_seeds(capsys, (*flags, "--stakes=high"))

    explored = [answer for answer in reversible if answer["explored"] is not None]
    assert SEEDS * 0.07 <= len(explored) <= SEEDS * 0.13
    assert not [answer for answer in careful if answer["explored"] is not None]


def test_an_exploration_moves_exactly_one_dimension_and_names_which(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A row that moved two things at once says nothing about either of them."""

    _boundary(tmp_path)

    answers = _over_seeds(capsys, (*LIMITED, f"--data={tmp_path}", "--kind=implement"))

    plain = {
        (answer["model"], answer["deliberation"])
        for answer in answers
        if answer["explored"] is None
    }
    assert len(plain) == 1
    model, level = plain.pop()

    explored = [answer for answer in answers if answer["explored"] is not None]
    assert {answer["explored"] for answer in explored} == {"model", "deliberation"}
    for answer in explored:
        if answer["explored"] == "model":
            # Held at the answer's level, except by a model with no effort
            # control, whose one point has no level to hold.
            assert answer["model"] != model
            assert answer["deliberation"] in (level, None)
            if answer["deliberation"] is None:
                assert answer["model"] == HAIKU
        else:
            assert answer["model"] == model
            assert answer["deliberation"] != level


def test_the_same_seed_returns_the_same_answer_twice(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller that has to reproduce a decision says which one it wants.

    Asked of a seed that explores and of one that does not, because a seed
    reproducing only the calls that took the answer would reproduce nothing
    about the calls that did not.
    """

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    twice = [
        [_answer(capsys, *flags, f"--seed={seed}") for _ in range(2)]
        for seed in (11, 31)
    ]

    assert [pair[0]["explored"] for pair in twice] == [None, "deliberation"]
    for first, again in twice:
        first.pop("attempt_id")
        again.pop("attempt_id")
        assert first == again


def test_exploring_never_disturbs_the_generator_the_rest_of_the_process_shares(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A routing call inside somebody else's turn reseeds nothing of theirs."""

    _profile(tmp_path)
    before = random.getstate()

    _answer(capsys, f"--data={tmp_path}", "--scope=all", "--seed=3")

    assert random.getstate() == before


def test_a_lock_is_an_instruction_rather_than_a_boundary_to_try(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A user who names a model or a level is not offering one to experiment on."""

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    locked = [
        _answer(capsys, *flags, lock, f"--seed={seed}")
        for lock in ("--model=claude-opus-5", "--deliberation=xhigh")
        for seed in range(DRAWS)
    ]

    assert locked
    assert all(answer["explored"] is None for answer in locked)


def test_an_escalation_after_a_failure_is_a_step_up_rather_than_an_experiment(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller whose attempt just failed is asking for the step, not for a row."""

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    stepped = [
        _answer(capsys, *flags, "--after=claude-opus-5@low", f"--seed={seed}")
        for seed in range(DRAWS)
    ]

    assert all(answer["explored"] is None for answer in stepped)
    assert len({answer["model"] for answer in stepped}) == 1


def test_an_exploration_names_what_the_evidence_would_have_chosen(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A reader seeing a weaker point chosen can tell an experiment from an error."""

    _boundary(tmp_path)

    answers = _over_seeds(capsys, (*LIMITED, f"--data={tmp_path}", "--kind=implement"))
    explored = [answer for answer in answers if answer["explored"] is not None]

    assert explored
    for answer in explored:
        assert "would have chosen" in answer["note"]
        assert "claude-opus-5@xhigh" in answer["note"]
        assert answer["explored"] in answer["note"]


def test_no_shipped_surface_still_says_the_answer_is_ranked_on_a_draw(
    subject: Path,
) -> None:
    """A docstring is a surface of the contract, and this contract changed.

    The answer used to be read off one draw from each candidate's posterior,
    and the prose beside the arithmetic said so — that ranking on a draw is
    what lets a store correct itself, that the overlap between two posteriors
    settles how often each is chosen, that one quantile spent across a model's
    levels keeps them from holding a ticket apiece. None of that is true of an
    engine that ranks on the means and buys its correcting rows on a bounded
    share of calls instead, so a surface still asserting it tells a reader the
    opposite of what the code beneath it does (issue #288).
    """

    text = " ".join(subject.read_text(encoding="utf-8").split()).lower()
    assert [phrase for phrase in RETIRED if phrase in text] == []


def test_the_quantile_a_cell_is_read_at_says_what_now_spends_it() -> None:
    """The method's only caller is the exploration, so its prose answers to that.

    A surface emptied of the retired claim and left saying nothing is the same
    stranded surface one edit later: the next reader still has to work out from
    the call sites what a draw is for.
    """

    evidence = _module("evidence")
    prose = " ".join((evidence.Estimate.draw.__doc__ or "").split()).lower()

    assert "explor" in prose


def test_an_explored_answer_reports_the_rate_measured_and_not_the_draw(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An exploration is how the call was spent, never a claim about the world.

    What picked the point was a draw that cleared the floor; what the store
    believes about it is its posterior mean, which on this store is below the
    floor, the one point clearing it being the answer. A point beyond the
    answer may also clear the floor on an estimate nothing has measured, and
    what is reported for it is still that mean. Reporting the draw would tell a
    caller the evidence backs a point it does not, and the caller could not
    tell that from an answer the evidence really does back.
    """

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    answers = _over_seeds(capsys, flags)
    explored = [answer for answer in answers if answer["explored"] is not None]
    points = {(answer["model"], answer["deliberation"]) for answer in explored}

    assert points
    for model, level in points:
        locked = _point(capsys, flags, model, level)
        rate = locked["expected"]["p_success"]
        assert rate < select.FLOOR
        for answer in explored:
            if (answer["model"], answer["deliberation"]) == (model, level):
                assert answer["expected"]["p_success"] == rate


def test_a_process_asking_for_an_anthropic_model_is_handed_a_command(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A script cannot spawn a subagent, so the native path is not its path.

    The grader is the caller that proves it: it is a process rather than a
    Harness, and an answer naming a subagent only an agent inside Claude Code
    can start would leave it with no judge at all.

    The `PATH` is named rather than inherited, because what the answer is here
    depends on it: a process is offered only the points something installed on
    this machine can start, and the machine under a test is whichever one the
    suite happens to be running on.
    """

    _profile(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude"))

    answer = _answer(capsys, f"--data={tmp_path}", "--harness=process", "--kind=review")

    assert answer["launch"]["how"] == "bridge-command"
    assert (answer["launch"]["command"] or [])[0] == "claude"
    assert answer["model"].startswith("claude-")


def test_a_read_only_answer_carries_a_bridge_that_grants_no_tool(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The caller says the work writes nothing; the launch is what says how."""

    _profile(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude"))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=process",
        "--kind=review",
        "--read-only",
    )

    command = answer["launch"]["command"] or []
    assert command[command.index("--tools") + 1] == ""


def test_the_same_answer_asked_for_without_it_keeps_its_tools(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every other caller is a builder, and a builder that cannot write is idle."""

    _profile(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude"))

    answer = _answer(capsys, f"--data={tmp_path}", "--harness=process", "--kind=review")

    assert "--tools" not in (answer["launch"]["command"] or [])


def test_the_ask_the_grader_makes_lands_on_a_judge_strong_enough_to_grade(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Grading is review work nothing checks, and the bar is what picks the judge.

    Asked as the easiest kind there is, the cheapest model on the machine
    cleared the high-stakes floor and graded a build the verifier had passed
    at 0.18. Asked as what it is, over the shipped priors and an empty store,
    the floor admits only a model that can actually read a unit of work.

    The machine is named rather than inherited: both makers are chosen, so
    every model each offers is eligible, each is paid for, and both CLIs are
    installed, so the pool the floor picks out of is the whole of what a judge
    could be — which is what makes the cheapest of them being refused mean
    anything.
    """

    _bridged(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude", "codex"))
    asked = (
        f"--data={tmp_path}",
        "--kind=review",
        "--stakes=high",
        "--harness=process",
        "--read-only",
    )

    answer = _answer(capsys, *asked)

    assert answer["expected"]["p_success"] >= select.FLOOR
    assert answer["model"] != "gpt-5.6-luna"
    assert _named_in(_answer(capsys, *asked, EVERY)) == ANTHROPIC | OPENAI


def test_the_judge_is_a_measured_reviewer_where_one_clears_the_floor(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The grader asks the same ranking, so it too prefers what was measured.

    Fable at `high` has twenty good `review` rows of its own. Opus at `high`
    has none, and its prior clears the floor for less money — which is the
    judge an empty store picks. A store that has watched a reviewer do the
    work grades with that reviewer rather than with an estimate.
    """

    _bridged(tmp_path)
    _store(tmp_path, ("review", "claude-fable-5-1", "high", 1.0, 20))
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude", "codex"))

    grader = (
        f"--data={tmp_path}",
        "--kind=review",
        "--scope=callable",
        "--stakes=high",
        "--harness=process",
        "--read-only",
    )

    answer = _answer(capsys, *grader)
    prior = _answer(capsys, *grader, "--model=claude-opus-5", "--deliberation=high")

    assert prior["basis"] == "prior"
    assert prior["expected"]["p_success"] >= select.FLOOR
    assert prior["expected"]["cost_usd"] < answer["expected"]["cost_usd"]
    assert (answer["model"], answer["deliberation"]) == ("claude-fable-5-1", "high")
    assert answer["basis"] == "measured"


@pytest.mark.parametrize(
    ("installed", "answered"),
    (("claude", ANTHROPIC), ("codex", OPENAI)),
    ids=("claude", "codex"),
)
def test_a_process_never_answers_a_point_no_bridge_here_can_start(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    installed: str,
    answered: frozenset[str],
) -> None:
    """`callable` for a process is what this machine can start, and no more.

    A Harness reaches a point through an adapter, so what admits one is the
    adapter existing. A process reaches every point by running a Bridge
    command, so what admits one is that command being installed here — and a
    point admitted without that test comes back as a command that fails in
    somebody else's terminal, reported by then as no judge rather than as no
    CLI (issue #301).
    """

    _bridged(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, installed))

    answer = _answer(
        capsys, f"--data={tmp_path}", "--harness=process", "--kind=review", EVERY
    )

    assert _named_in(answer) == answered
    assert (answer["launch"]["command"] or [])[0] == installed


def test_a_process_that_names_a_seat_is_held_to_the_same_test(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A seat says which provider is already being paid for, not which CLI is here.

    The seat gives `callable` a provider floor, and a floor admitted unfiltered
    would put back exactly the points this machine cannot start — so the floor's
    own points take the test with every other.
    """

    _bridged(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "codex"))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=process",
        "--seat=claude-sonnet-5@high",
        "--kind=review",
        EVERY,
    )

    assert _named_in(answer) == OPENAI


@pytest.mark.parametrize("missing", ("bridge", "channel"))
def test_an_installed_binary_alone_does_not_make_a_point_startable(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    missing: str,
) -> None:
    """The binary is the third test and never a replacement for the first two.

    A machine with both CLIs installed still cannot start a point no Bridge
    plans a command for, and still cannot say who would pay for one the profile
    carries no channel for. Either absence is disqualifying on its own.
    """

    without = (
        {"harnesses": ["codex"]}
        if missing == "bridge"
        else {
            "channels": [
                {
                    "provider": "openai",
                    "harness": "codex",
                    "pay": "subscription",
                    "plan": "ChatGPT Pro",
                }
            ]
        }
    )
    _bridged(tmp_path, **without)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude", "codex"))

    answer = _answer(
        capsys, f"--data={tmp_path}", "--harness=process", "--kind=review", EVERY
    )

    assert _named_in(answer) == OPENAI


def test_a_machine_that_can_start_nothing_says_that_rather_than_naming_a_judge(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty pool is answered with the seat, and with the reason it is empty.

    The reason matters because of who reads it. The grader takes `inherit` for
    no judge and files the attempt as ungraded, so a machine with neither CLI
    installed reports a judge that could not be reached; the note is the only
    place that can say the machine, rather than the evidence, is what is
    missing.
    """

    _bridged(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=process",
        "--kind=review",
        "--seat=claude-opus-5@high",
    )

    assert answer["launch"]["how"] == "inherit"
    assert answer["basis"] == "inherit"
    assert answer["model"] == "claude-opus-5"
    assert "nothing on this machine can start a process" in (answer["note"] or "")


@pytest.mark.parametrize("harness", ("claude-code", "codex", "process"))
@pytest.mark.parametrize("scope", ("limited", "all"))
def test_the_other_two_scopes_never_read_this_machine_for_binaries(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    harness: str,
    scope: str,
) -> None:
    """Only `callable` claims to be about what can be started, so only it is.

    `limited` is the provider already being paid for this turn and `all` is the
    catalogue whether or not anything can reach it, and neither statement has
    ever depended on what is installed here. Each answers the same under both
    machines.
    """

    _bridged(tmp_path)
    flags = (
        f"--data={tmp_path}",
        f"--scope={scope}",
        f"--harness={harness}",
        "--kind=review",
        "--seed=1",
    )

    monkeypatch.setenv("PATH", path_holding(tmp_path / "equipped", "claude", "codex"))
    equipped = _answer(capsys, *flags)
    monkeypatch.setenv("PATH", path_holding(tmp_path / "bare"))
    bare = _answer(capsys, *flags)

    assert bare["basis"] != "inherit"
    assert (bare["model"], bare["deliberation"]) == (
        equipped["model"],
        equipped["deliberation"],
    )


def test_a_harness_keeps_the_pool_it_had_before_binaries_were_asked_about(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """What a real Harness admits is unchanged, and the same hole is left in it.

    A Harness plans a bridge to another provider on the profile's own account of
    itself, with no binary consulted, and that is still what it does: the same
    gap one step over is a ticket of its own rather than something to widen this
    fix into.
    """

    _bridged(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--scope=callable",
        "--kind=review",
        EVERY,
    )

    assert OPENAI <= _named_in(answer)


# The three places that each state what `callable` admits: the option a person
# reads, the body the agent running the Skill reads, and the rule binding every
# Skill in the collection that routes work.
SCOPE_SURFACES: tuple[Path, ...] = (
    SKILL / "help.md",
    SKILL / "SKILL.md",
    REPO_ROOT / "docs" / "rules" / "routing.md",
)


@pytest.mark.parametrize("surface", SCOPE_SURFACES, ids=lambda path: path.name)
def test_every_account_of_callable_says_what_it_means_for_a_process(
    surface: Path,
) -> None:
    """A rule stated in three places is stated in all three or falsified in two.

    `callable` used to mean one thing, so one sentence about a Harness said the
    whole of it. It means something narrower for a caller that starts what it is
    given itself, and a page still giving only the Harness account promises a
    pool wider than the one the engine will offer.
    """

    text = " ".join(surface.read_text(encoding="utf-8").split()).lower()
    sentences = text.split(". ")

    assert [
        sentence
        for sentence in sentences
        if "callable" in sentence and "process" in sentence and "`path`" in sentence
    ]


setup_apply = _module("setup_apply")

# The flags every standing-objective test asks with: a store where the cheapest
# finished job and the quickest one are two different points.
STANDING: tuple[str, ...] = (*LIMITED, "--kind=implement", "--seed=0")


def _stand(capsys: pytest.CaptureFixture[str], data_dir: Path, objective: str) -> None:
    """Set the standing objective as `/model-selector objective` does, then clear stdout."""

    assert setup_apply.main([f"--data={data_dir}", f"--objective={objective}"]) == 0
    capsys.readouterr()


def _pointed(answer: dict[str, Any]) -> tuple[str, str | None]:
    """Return the point an answer names."""

    return answer["model"], answer["deliberation"]


def test_the_standing_choice_orders_an_answer_asked_for_no_objective(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """After `objective time` a bare call ranks on time, after `objective cost` on cost."""

    _clearing(tmp_path)
    flags = (*STANDING, f"--data={tmp_path}")
    on_time = _answer(capsys, *flags, "--objective=time")
    on_cost = _answer(capsys, *flags, "--objective=cost")
    assert _pointed(on_time) != _pointed(on_cost)

    _stand(capsys, tmp_path, "time")
    timed = _answer(capsys, *flags)
    _stand(capsys, tmp_path, "cost")
    costed = _answer(capsys, *flags)

    assert _pointed(timed) == _pointed(on_time)
    assert (timed["objective"], timed["objective_source"]) == ("time", "standing")
    assert _pointed(costed) == _pointed(on_cost)
    assert (costed["objective"], costed["objective_source"]) == ("cost", "standing")


@pytest.mark.parametrize(("standing", "asked"), (("time", "cost"), ("cost", "time")))
def test_an_explicit_objective_outranks_the_standing_choice(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], standing: str, asked: str
) -> None:
    """The caller's `--objective` wins in both directions, so `--fast` still means time."""

    _clearing(tmp_path)
    flags = (*STANDING, f"--data={tmp_path}")
    _stand(capsys, tmp_path, standing)

    inherited = _answer(capsys, *flags)
    answer = _answer(capsys, *flags, f"--objective={asked}")

    assert _pointed(answer) != _pointed(inherited)
    assert (answer["objective"], answer["objective_source"]) == (asked, "caller")
    assert (inherited["objective"], inherited["objective_source"]) == (
        standing,
        "standing",
    )


def test_with_nothing_set_an_answer_ranks_on_cost(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Running out of quota stops everything, while a slower job is only slower."""

    _clearing(tmp_path)
    flags = (*STANDING, f"--data={tmp_path}")

    answer = _answer(capsys, *flags)
    on_cost = _answer(capsys, *flags, "--objective=cost")

    assert _pointed(answer) == _pointed(on_cost)
    assert (answer["objective"], answer["objective_source"]) == ("cost", "default")
    assert not (tmp_path / "objective.json").exists()


# The sentences that tied ranking on time to the caller asking for it,
# whitespace-collapsed and lowered before matching. A call is ranked on time
# where the caller asks, and equally where the user's standing choice says so,
# so a surface still naming the caller as the only way there states the rule
# ADR-0189 replaced (issue #307).
CALLER_ONLY_TIME: tuple[str, ...] = (
    "where the caller asked for time",
    "where the caller asks for time",
    "caller asked for time",
    "in the caller's terms",
)


def test_no_shipped_surface_ties_ranking_on_time_to_the_caller(
    subject: Path,
) -> None:
    """Time is reached from the caller's `--objective` or the standing choice alike."""

    text = " ".join(subject.read_text(encoding="utf-8").split()).lower()
    assert [phrase for phrase in CALLER_ONLY_TIME if phrase in text] == []


def test_a_step_up_is_ordered_on_time_wherever_the_call_is_ranked_on_time() -> None:
    """The step is asked the way the first answer was, whatever set its objective."""

    selection = _module("selection")
    prose = " ".join((selection._after.__doc__ or "").split()).lower()

    assert "where the call is ranked on time" in prose


@pytest.mark.parametrize(
    "held",
    ("{not json", '{"objective": "fast"}', '{"objective": 1}', '["time"]', "{}"),
)
def test_a_standing_choice_nothing_can_read_is_the_default_said_out_loud(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], held: str
) -> None:
    """An unreadable file is treated as absent, named in the note, and never refused."""

    _clearing(tmp_path)
    (tmp_path / "objective.json").write_text(held, encoding="utf-8")
    flags = (*STANDING, f"--data={tmp_path}")

    answer = _answer(capsys, *flags)

    assert answer["ok"] is True
    assert _pointed(answer) == _pointed(_answer(capsys, *flags, "--objective=cost"))
    assert (answer["objective"], answer["objective_source"]) == ("cost", "default")
    assert "objective.json" in (answer["note"] or "")


def test_an_inheriting_answer_names_its_objective_and_where_it_came_from(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The answer that keeps the caller's seat carries both members as well."""

    flags = (f"--data={tmp_path}", "--seat=claude-opus-5@xhigh")

    defaulted = _answer(capsys, *flags)
    asked = _answer(capsys, *flags, "--objective=time")
    _stand(capsys, tmp_path, "time")
    standing = _answer(capsys, *flags)
    (tmp_path / "objective.json").write_text("{not json", encoding="utf-8")
    unreadable = _answer(capsys, *flags)

    assert {row["basis"] for row in (defaulted, asked, standing, unreadable)} == {
        "inherit"
    }
    assert (defaulted["objective"], defaulted["objective_source"]) == (
        "cost",
        "default",
    )
    assert (asked["objective"], asked["objective_source"]) == ("time", "caller")
    assert (standing["objective"], standing["objective_source"]) == ("time", "standing")
    assert (unreadable["objective"], unreadable["objective_source"]) == (
        "cost",
        "default",
    )
    assert "objective.json" in unreadable["note"]


def test_the_vocabulary_answer_carries_no_objective(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`--kinds` ranks nothing, so it has nothing to say it ranked on."""

    answer = _answer(capsys, "--kinds")

    assert "objective" not in answer
    assert "objective_source" not in answer


# --- Which models are eligible: every model a chosen maker offers ------------


def _makers(data_dir: Path, *channels: dict[str, Any]) -> None:
    """Write a profile choosing Anthropic and xAI, on three Harnesses.

    OpenAI is not chosen, yet the machine could reach it: Codex is one of the
    Harnesses, and the channels passed in may pay for it. Whatever keeps its
    models out of the pool is therefore the choice of makers and nothing else.
    """

    _profile(
        data_dir,
        harnesses=["claude-code", "codex", "opencode"],
        makers=["anthropic", "spacexai"],
        channels=list(channels),
    )


ANTHROPIC_CHANNEL: dict[str, Any] = {
    "provider": "anthropic",
    "harness": "claude-code",
    "pay": "subscription",
    "plan": "Claude Max 20x",
}
XAI_CHANNEL: dict[str, Any] = {
    "provider": "spacexai",
    "harness": "opencode",
    "pay": "api",
}
OPENAI_CHANNEL: dict[str, Any] = {
    "provider": "openai",
    "harness": "codex",
    "pay": "subscription",
    "plan": "ChatGPT Pro",
}


def test_every_model_a_chosen_maker_offers_that_a_channel_reaches_is_a_candidate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Nothing new has to be enabled by hand; no model of an unchosen maker is in.

    A model the catalogue gains later is eligible the moment it is there,
    because what is chosen is its maker. OpenAI is reachable and paid for on
    this machine and still never offered, because nobody chose it.
    """

    _makers(tmp_path, ANTHROPIC_CHANNEL, XAI_CHANNEL, OPENAI_CHANNEL)

    answer = _answer(
        capsys, f"--data={tmp_path}", "--harness=claude-code", "--kind=review", EVERY
    )

    assert _named_in(answer) == ANTHROPIC | {"grok-4.6"}
    assert not _named_in(answer) & OPENAI


def test_a_chosen_maker_no_channel_reaches_is_not_a_candidate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Choosing a maker says whose models are wanted, never who pays for them.

    xAI is chosen and nothing pays for it, so Grok is out. Anthropic has no
    channel either, and is in: it is the caller's own provider, and the seat
    already in hand needs no channel to reach its own models.
    """

    _makers(tmp_path)

    answer = _answer(
        capsys, f"--data={tmp_path}", "--harness=claude-code", "--kind=review", EVERY
    )

    assert _named_in(answer) == ANTHROPIC


def test_the_whole_catalogue_is_still_the_scope_that_asks_for_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--scope=all` ignores reachability and the makers alike, on a valid profile."""

    _makers(tmp_path, ANTHROPIC_CHANNEL)

    answer = _answer(
        capsys, f"--data={tmp_path}", "--scope=all", "--kind=review", EVERY
    )

    assert OPENAI <= _named_in(answer)


def _stored_as(data_dir: Path, state: str) -> None:
    """Leave no profile, one in the old shape, or one of four kinds of damage."""

    old = {
        "harnesses": ["claude-code"],
        "providers": ["anthropic"],
        "models": ["claude-opus-5"],
        "channels": [ANTHROPIC_CHANNEL],
    }
    shapes: dict[str, Any] = {
        "old-shape": old,
        "unknown-maker": {**old, "makers": ["anthropic", "mistral"]},
        "leftover-list": {**old, "makers": ["anthropic"]},
        "bad-channel": {
            "harnesses": ["claude-code"],
            "makers": ["anthropic"],
            "channels": [{"provider": "anthropic"}],
        },
        "unreadable": "{not json",
    }
    data_dir.mkdir(parents=True, exist_ok=True)
    if state == "missing":
        return
    shape = shapes[state]
    (data_dir / "profile.json").write_text(
        shape if isinstance(shape, str) else json.dumps(shape), encoding="utf-8"
    )


NO_VALID_PROFILE: tuple[str, ...] = (
    "missing",
    "old-shape",
    "unknown-maker",
    "leftover-list",
    "bad-channel",
    "unreadable",
)


@pytest.mark.parametrize("scope", ("limited", "callable", "all"))
@pytest.mark.parametrize("state", NO_VALID_PROFILE)
def test_without_a_valid_profile_an_unlocked_call_inherits_and_names_setup(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], state: str, scope: str
) -> None:
    """No maker is chosen, so nothing is eligible, the caller's own provider included.

    A profile in the old shape is not translated: a list of model ids says
    nothing about makers, and the user answers the interview again. The whole
    catalogue is no pool to fall back on either, being wider than anyone chose.
    """

    _stored_as(tmp_path, state)

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--seat=claude-opus-5@xhigh",
        f"--scope={scope}",
    )

    assert answer["basis"] == "inherit"
    assert answer["launch"]["how"] == "inherit"
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "xhigh")
    assert "/model-selector setup" in answer["note"]


@pytest.mark.parametrize("state", ("missing", "old-shape", "unknown-maker"))
def test_without_a_valid_profile_a_model_lock_is_still_answered(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], state: str
) -> None:
    """A model the user named is honoured as it always was, profile or none."""

    _stored_as(tmp_path, state)

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--seat=claude-opus-5@xhigh",
        "--model=sonnet",
        "--deliberation=high",
    )

    assert answer["basis"] != "inherit"
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "high")
    assert answer["launch"]["subagent_type"] == "kntnt-sonnet-high"


def test_without_a_valid_profile_a_deliberation_lock_alone_inherits(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A level says how hard to think, never which model; so no model is chosen."""

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--seat=claude-opus-5@xhigh",
        "--deliberation=high",
    )

    assert answer["basis"] == "inherit"
    assert "/model-selector setup" in answer["note"]
