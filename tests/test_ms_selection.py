"""The decision itself: what is chosen, and what is said when nothing can be."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import time
from collections.abc import Sequence
from datetime import UTC, datetime
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

# The distinctive words of the note the band writes, so that a test asserting
# the line is there and one asserting it is absent read the same string.
BAND: str = "the evidence cannot tell from"

# What `explored` carries where the call was a Trial rather than an ordinary
# exploration, stated here rather than read off the module so that a test
# asserting a Trial and one asserting there was none read the same string.
TRIAL: str = "trial"

# The exploration as it stood at the commit this ticket's work starts from,
# digested over `SEEDS` seeds of the `_boundary` fixture by `_replayed`. A
# Trial is settled before the generator is touched, so a pool owing none has to
# draw exactly what it drew before, and this is the sweep that says it did. The
# base commit is named in this ticket's commit message.
EXPLORATION_AT_BASE: str = (
    "5ac25d3fadd3a2c5d68aee6412b727e969ef50f967be2302c5bf891c52c47b07"
)

# The retired rule's own sentences, whitespace-collapsed before matching so
# that a line break falling inside one of them hides nothing. Each states, as
# the contract in force, an answer read off a draw over the whole pool rather
# than off the means, or the cost the expected-cost arithmetic used to rank on
# (issue #288), or the floor as the only thing ever standing between a cheap
# point and the answer, which the band falsifies wherever nothing measured
# clears it (issue #372). The identifiers the expected-cost arithmetic went by
# are deliberately absent: a list naming them would itself be a surface
# carrying them.
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
    "is taken for being cheap",
    "is never chosen for being cheap",
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


for _dependency in ("catalogue", "profiles", "evidence", "launch", "quota"):
    _module(_dependency)

# Registered under a name of its own: this module's file name is the standard
# library's `select`, and shadowing that inside a test run would reach far
# beyond this file.
select = _module("selection", "ms_selection")
quota = sys.modules["quota"]

# How many rows of its own a model needs for a kind before it stops being owed
# a Trial, read off the module because it is the same threshold that decides
# when a cell stops being pooled and a test writing a three of its own would
# stop agreeing with the rule the moment the rule moved.
ENOUGH: int = sys.modules["evidence"].ENOUGH


@pytest.fixture(autouse=True)
def elsewhere(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point every test in this module at a home of its own, and return it.

    The entry point is run in process here, so anything inside it that asks
    for a home gets the machine the suite happens to be running on unless
    something moves it: the data directory's own fallback, the harness probes,
    and the two trees the quota guard reads. None of this module's subjects is
    about that machine, so all of them are pointed at a temporary tree, and a
    test that wants the guard to see a figure writes it under the tree this
    hands back (issue #373).
    """

    home = tmp_path / "home"
    home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("KNTNT_HOME", raising=False)
    return home


def _answer(capsys: pytest.CaptureFixture[str], *flags: str) -> dict[str, Any]:
    """Run the entry point in process and return the one object it printed."""

    assert select.main(list(flags)) == 0
    printed = capsys.readouterr().out.strip().splitlines()
    assert len(printed) == 1
    parsed: dict[str, Any] = json.loads(printed[0])
    return parsed


def _profile(data_dir: Path, **overrides: Any) -> None:
    """Write a profile that chooses Anthropic and pays for it in Claude Code.

    Every model Anthropic offers is therefore eligible, and every one of them
    is a candidate too: each seeded Anthropic family holds one release, so the
    rule keeping only a family's newest release takes nothing out of this pool
    until a fixture adds a second release to one of them. A test that needs a
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

    Sonnet's sixty good rows are what put the bound it draws at about 0.9276,
    over the unpriced model's prior of about 0.9105 and over every other prior
    in this pool, so nothing here is owed a Trial and the answer this test
    reads is the ranked one rather than a point being tried (issue #374).
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
    _store(tmp_path, ("implement", "claude-sonnet-5", "high", 1.0, 60))

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


def _measured_nought(data_dir: Path) -> None:
    """Write a store in which one point recorded nought in every token category.

    Codex reports `cache_write: 0` on every attempt it exposes usage for, and a
    vendor that bills nothing for a category has reported nothing rather than
    hidden it. Taken to its limit — every category recorded as nought — the
    point prices at 0.00 USD.

    Sonnet's sixty good rows are what put the bound it draws at about 0.9276,
    above every prior in this pool — the highest of them Fable's 0.9002, and the
    point Fable would be tried at, `high` like the answer, 0.8808 — so no model
    here is owed a Trial and the answer this fixture is read for is the ranked
    one. The rows are the same recorded nought whatever their number, so the
    price under test is untouched by how many there are (issue #374).
    """

    catalogue = _module("catalogue")
    _profile(data_dir)
    lines = [
        json.dumps(
            {
                "attempt_id": f"ms-free-{index}",
                "at": "2026-09-01T00:00:00Z",
                "kind": "implement",
                "model": "claude-sonnet-5",
                "deliberation": "high",
                "grade": 1.0,
                "graded_by": "checker",
                "routed": True,
                "tokens": dict.fromkeys(catalogue.TOKEN_CATEGORIES, 0.0),
                "seconds": 900.0,
            }
        )
        for index in range(60)
    ]
    (data_dir / "measurements.jsonl").write_text(
        "".join(f"{line}\n" for line in lines), encoding="utf-8"
    )


def test_a_forecast_of_nought_is_a_real_price_and_not_a_null_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A recorded nought exists, so what it prices at is a price.

    This is the far edge of the rule that a category measured as nought is
    forecast as nought: a point whose every recorded category measured nought
    prices at 0.00 USD and sorts ahead of every other priced point. That is the
    answer rather than a defect, and no floor, epsilon or guard is added
    against it — the rule that an unmeasured configuration never becomes the
    cheapest thing on a frontier governs a measurement that does not exist,
    and this one does (issue #371).

    The store is this test's own and owes no Trial, so the answer read here is
    the ranked one rather than a point being tried (issue #374).
    """

    _measured_nought(tmp_path)
    ranked = _ranking(tmp_path, "implement")

    free = {select._named(row.point): row for row in ranked}["claude-sonnet-5@high"]
    priced = [row for row in ranked if row.cost_usd is not None]

    assert free.cost_usd == 0.0
    assert select._per_success_cost(free) == 0.0

    # Every point Sonnet's own rows answer for prices at nought, so what has to
    # hold is that each of them is ahead of every point carrying a real bill.
    dearer = [row for row in priced if row.cost_usd > 0.0]
    assert dearer
    assert select._cost_key(min(priced, key=select._cost_key))[1] == 0.0
    assert all(select._cost_key(free) < select._cost_key(row) for row in dearer)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "high")
    assert answer["expected"]["cost_usd"] == 0.0
    assert answer["expected"]["per_success_cost_usd"] == 0.0
    assert all(row["cost_usd"] > 0.0 for row in answer["alternatives"])


def test_the_answer_is_the_cheapest_point_that_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Where measured points clear the floor, none below it is taken for being cheap.

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


def test_where_nothing_clears_the_floor_the_band_decides(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A pool that cannot promise the work is done is ordered by the band."""

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


def test_an_answer_ranked_on_the_band_still_carries_the_total(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Where nothing clears the floor the band decides, and the answer says both."""

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


def test_with_no_likelier_point_clearing_the_floor_the_step_is_read_per_success(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The step drawn over the band is ordered on the same total as the rest.

    Sonnet at `low` failed. Both likelier points are measured and neither
    clears the floor, so the step is the band drawn around the best of them.
    Sonnet at `medium` is the cheapest attempt among them and finishes about
    half the time; Sonnet at `high` costs a little more and finishes about two
    times in three, which makes it the cheaper finished job.
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


def _measured_beside_unowed_prior(data_dir: Path) -> None:
    """Write `_measured_beside_prior`'s case with no model in the pool owed a Trial.

    A store of one test's own, because the shape that test is about — a cheaper
    untested point beside a dearer measured one — is also the shape that owes a
    Trial, and the shared helper cannot be given rows without moving the four
    other tests that replay it (issue #374).

    Opus at `high` has two hundred good `mechanical` rows and at `low` ten bad
    ones, so it is the answer and the bound it draws is about 0.9735 — above
    Sonnet's prior of about 0.9689 at `high` and far above the Haiku point, so
    neither is owed a Trial on its mean. Fable's three failing rows are
    `ENOUGH` to take it off one on its count. Sonnet is still untested at every
    level, still clears the floor at each, and still finishes a job for less
    than the answer does, which is the whole of what this test is about.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("mechanical", "claude-opus-5", "high", 1.0, 200),
        ("mechanical", "claude-opus-5", "low", 0.0, 10),
        ("mechanical", FABLE, "high", 0.0, 3),
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

    _measured_beside_unowed_prior(tmp_path)
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


def test_where_no_measured_point_clears_the_floor_the_band_answers(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Measured points go first whether or not one of them can promise the work.

    Opus's own `mechanical` rows all failed, so nothing measured clears the
    floor. That used to hand the answer back to the whole pool, and an estimate
    nobody had tested took it on arithmetic. Now the one measured point is the
    only one its own bound admits, so it is the answer, and a cheaper estimate
    that clears the floor is offered beside it rather than chosen (ADR-0204).
    """

    _profile(tmp_path)
    _store(tmp_path, ("mechanical", "claude-opus-5", "high", 0.0, 10))

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--stakes=high"
    )
    estimated = _point(
        capsys,
        (*LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--stakes=high"),
        "claude-sonnet-5",
        "low",
    )

    assert estimated["basis"] == "prior"
    assert estimated["expected"]["p_success"] >= select.FLOOR
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["basis"] == "measured"
    assert answer["expected"]["p_success"] < select.FLOOR
    assert BAND in (answer["note"] or "")
    assert "claude-opus-5@high" in (answer["note"] or "")


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


# The rule this section covers: every point measured for the kind leads the
# answer, and where none of them clears the floor a band drawn around the best
# of them decides which one is taken (ADR-0204).

# Every level the default deliberation ceiling admits, for a fixture that has
# to measure one model everywhere rather than at one rung of the ladder.
UNDER_CEILING: tuple[str, ...] = ("low", "medium", "high", "xhigh")


def _timed(data_dir: Path, model: str, seconds: float) -> None:
    """Write an elapsed time onto every stored row of one model.

    `_store` writes a grade and nothing else, so every point of a store it
    shaped forecasts the kind's shipped elapsed figure scaled by its own level.
    Two models at one level are then equally fast per attempt, and the likelier
    of them is always the faster finished job — which no fixture can shape into
    an untested point that is the slower one. A row carries its own `seconds`,
    and this is how a fixture says so.
    """

    path = data_dir / "measurements.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    for row in rows:
        if row["model"] == model:
            row["seconds"] = seconds
    path.write_text("".join(f"{json.dumps(row)}\n" for row in rows), encoding="utf-8")


def _ranking(
    data_dir: Path,
    kind: str,
    objective: str = "cost",
    scope: str = "limited",
    harness: str = "claude-code",
) -> list[Any]:
    """Return the whole ranked pool one call reads its answer off.

    `alternatives` carries one entry per model, so it can never show two points
    of one model in the order the rule put them, and a test reading it would be
    reading a summary of the list rather than the list. The order itself is
    read here, through the same module the suite already imports and off the
    same pool the entry point builds.
    """

    catalogue = _module("catalogue")
    profiles = _module("profiles")
    evidence = _module("evidence")

    cat = catalogue.load(data_dir, SKILL)
    profile = profiles.load(data_dir, cat)
    kinds = evidence.load_kinds(SKILL)
    estimator = evidence.Estimator(evidence.load(data_dir), cat, kinds)
    pool = [
        point
        for point in select._pool(scope, cat, profile, None, harness, None, [])
        if select._admitted(point.deliberation, select.DEFAULT_MAX_DELIBERATION)
    ]
    scored = [
        select._score(
            point, kind, estimator, kinds, select._paid(profile, point, harness)
        )
        for point in pool
    ]
    return list(select._ranked(scored, objective))


def _spelt(ranked: Sequence[Any]) -> list[str]:
    """Spell a ranked pool the way a caller names each of its points."""

    return [select._named(row.point) for row in ranked]


def _made(model: Any, level: str | None, mean: float, low: float, cost: float) -> Any:
    """Return one measured point made rather than stored, for a unit check.

    A tie on the highest mean is what the band's own order has to settle, and
    two stored cells landing on the same posterior to the last bit is not
    something a fixture can arrange.
    """

    evidence = _module("evidence")
    estimate = evidence.Estimate(
        mean=mean, low=low, n=9.0, basis="measured", alpha=1.0, beta=1.0
    )
    return select.Scored(select.Point(model, level), estimate, {}, cost, 100.0)


def _replay(data_dir: Path) -> None:
    """Write the store that replays the `implement` case of 2026-09-19.

    On the maintainer's machine that day, `gpt-6-astra` at `high` won a day of
    work at 16.74 USD per finished job with no rows of its own, over
    `claude-opus-5` at `high` at 7.01 USD with 142 of them, because the first
    cleared the floor on `sigmoid(SHARPNESS × (capability + bonus −
    difficulty))` and the second missed it on measurements. Clearing 0.8 that
    way at `high` takes a seeded capability of about 0.873, and Opus is seeded
    at 0.87: three thousandths of a seeded number decided the run.

    The shape is what is replayed here rather than the models. Opus at `high`
    is measured at about 0.76 and does not clear the floor; Fable at `medium`
    has no row at all, clears it at about 0.83 on its prior, and costs more per
    finished job. The rows carry an elapsed time of their own so that the same
    case can be asked on the clock: without one, two points at one level are
    equally fast per attempt and the likelier is always the faster job.
    """

    _profile(data_dir)
    _store(data_dir, ("implement", "claude-opus-5", "high", 0.75, 20))
    _timed(data_dir, "claude-opus-5", 600.0)


def _cheapest_measured(data_dir: Path) -> None:
    """Write a store whose cheapest measured point is junk the band shuts out.

    Luna is measured at every level the ceiling admits and finishes about a
    fifth of the time, which its price still makes the cheapest and the fastest
    finished job in the pool. Opus at `high` is measured at about 0.76, and its
    tenth percentile is far above anything Luna reads — so the evidence can
    tell the two apart, and dividing the price by the chance is not on its own
    what keeps the cheap junk from winning.

    Fable, Astra and Sol each carry `ENOUGH` failing rows of their own, which is
    what leaves nothing in this pool owed a Trial. Opus's own mean has to stay
    below the floor for the band to be what decides the answer, so the bound it
    draws stays near 0.65 and can never be lifted over a prior of 0.88: the
    three models whose tried point reads above that bound are taken off a Trial
    on their count instead, and every other model here with no rows for the kind
    is below it already at the level it would be tried at. The rows are failures
    so that Opus at `high` stays the best measured point and goes on being the
    one the band is drawn around, and they move neither the cheapest nor the
    quickest finished job in the pool, both of which are still Luna at `low`
    (issue #374).
    """

    _bridged(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "high", 0.75, 20),
        *[("implement", "gpt-5.6-luna", level, 0.21, 20) for level in UNDER_CEILING],
        ("implement", FABLE, "high", 0.0, ENOUGH),
        ("implement", "gpt-6-astra", "high", 0.0, ENOUGH),
        ("implement", "gpt-5.6-sol", "high", 0.0, ENOUGH),
    )
    _timed(data_dir, "gpt-5.6-luna", 200.0)


def _indistinguishable(data_dir: Path) -> None:
    """Write a store whose best measured point is not the one the band takes.

    Nothing here clears the floor. Opus at `high` reads about 0.76 with a tenth
    percentile of about 0.65, and Sonnet at `high` about 0.71 — inside that
    bound, so the evidence cannot tell the two apart, and Sonnet is less than
    half the price per finished job. Fable at `high` reads about 0.39, well
    below the bound, so the band leaves it behind however it is priced.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "high", 0.75, 20),
        ("implement", "claude-sonnet-5", "high", 0.75, 20),
        ("implement", FABLE, "high", 0.1, 10),
    )


def _unmeasured_kind(data_dir: Path) -> None:
    """Write a store holding no row at all for the kind the call asks about.

    Sonnet's rows are every one of them `design`, so a `mechanical` call finds
    nothing measured to prefer and is answered by the rule that stood before
    the measured points were given the front of the list.
    """

    _profile(data_dir)
    _store(data_dir, ("design", "claude-sonnet-5", "high", 1.0, 20))


@pytest.mark.parametrize(
    ("objective", "total"),
    (("cost", "per_success_cost_usd"), ("time", "per_success_seconds")),
)
def test_the_estimate_that_won_the_replayed_case_is_tried_rather_than_answered(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], objective: str, total: str
) -> None:
    """The replay of the `implement` case of 2026-09-19, which is now a Trial.

    An estimate nobody had tested cleared the floor and a point with 142 rows
    behind it did not, so the measured-first preference never engaged and the
    estimate won a day of work on arithmetic, as though something had watched it
    do the job. The two rules released together answer that shape differently:
    the ranking puts the measured point first, and the Trial then tries the
    untested model on purpose — three reversible jobs of the kind at whatever
    they cost — so the model that won that day is tried and says it was tried,
    rather than taken for the answer (issue #374).

    That is forced rather than chosen. The band's bound is the drawer's own
    `Estimate.low`, which is never above its own mean, so wherever no measured
    point clears the floor while an untested one does — the antecedent this test
    asserts of its own store — the untested point is necessarily at or above the
    band and is therefore necessarily owed a Trial. No store keeps this
    scenario and owes none, so the ranking-only claim this test used to make is
    covered where the Trial is suppressed instead:
    `test_where_no_measured_point_clears_the_floor_the_band_answers` asks it at
    high stakes, which `_explorable` never tries the boundary on, and
    `test_every_measured_point_leads_the_pool_the_alternatives_are_read_from`
    reads the ranked order itself, below the Trial.
    """

    _replay(tmp_path)
    flags = (
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=implement",
        f"--objective={objective}",
        "--seed=0",
    )

    answer = _answer(capsys, *flags)
    untested = _point(capsys, flags, FABLE, "medium")
    measured = _point(capsys, flags, "claude-opus-5", "high")

    assert untested["basis"] == "prior"
    assert untested["expected"]["p_success"] >= select.FLOOR
    assert measured["basis"] == "measured"
    assert measured["expected"]["p_success"] < select.FLOOR
    assert untested["expected"][total] > measured["expected"][total]

    assert (answer["model"], answer["deliberation"]) == (FABLE, "high")
    assert answer["explored"] == TRIAL
    assert answer["basis"] == "prior"
    assert "claude-opus-5@high" in (answer["note"] or "")


@pytest.mark.parametrize(
    ("objective", "total"),
    (("cost", "per_success_cost_usd"), ("time", "per_success_seconds")),
)
def test_the_cheapest_measured_point_is_left_outside_the_band(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], objective: str, total: str
) -> None:
    """Measured-first on its own would answer with the cheapest junk in the pool.

    Luna finishes about a fifth of the time and is still the cheapest and the
    fastest finished job here, because its price is small enough to survive
    being divided by that. The band is what stops it: its mean is far below the
    bound the best measured point carries, so the evidence can tell the two
    apart and the cheap point is never among the candidates price orders.

    The store is this test's own, and nothing in its pool is owed a Trial, so
    the answer read here is the ranked one rather than a point being tried
    (issue #374).
    """

    _cheapest_measured(tmp_path)
    flags = (
        "--scope=callable",
        "--harness=claude-code",
        f"--data={tmp_path}",
        "--kind=implement",
        f"--objective={objective}",
        "--seed=0",
    )

    answer = _answer(capsys, *flags)
    cheap = _point(capsys, flags, "gpt-5.6-luna", "low")
    ranked = _ranking(tmp_path, "implement", objective, "callable")

    priced = [row for row in ranked if row.cost_usd is not None]
    lowest = min(priced, key=lambda row: select._per_success_cost(row) or 0.0)
    quickest = min(priced, key=select._per_success_seconds)
    assert select._named(lowest.point) == "gpt-5.6-luna@low"
    assert select._named(quickest.point) == "gpt-5.6-luna@low"
    assert cheap["basis"] == "measured"
    assert cheap["expected"]["p_success"] < 0.25

    assert answer["explored"] is None
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["basis"] == "measured"
    assert BAND in (answer["note"] or "")
    assert "claude-opus-5@high" in (answer["note"] or "")
    # The bound the band was drawn at is the named point's own, read off the
    # estimator through a locked call rather than off `confidence`, which is
    # always the answer's own tenth percentile and never the band's.
    bound = _point(capsys, flags, "claude-opus-5", "high")["confidence"]
    assert cheap["expected"]["p_success"] < bound


@pytest.mark.parametrize(
    ("objective", "chosen"),
    (("cost", "claude-sonnet-5@high"), ("time", "claude-opus-5@high")),
)
def test_the_band_is_ordered_on_what_the_call_was_ranked_on(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], objective: str, chosen: str
) -> None:
    """Inside the band the objective decides, exactly as it does above the floor.

    Sonnet at `high` is the cheaper finished job of the two the evidence cannot
    tell apart, and Opus at `high` the faster one, so the same store answers
    with a different point under each objective.
    """

    _indistinguishable(tmp_path)

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=implement",
        f"--objective={objective}",
        "--seed=0",
    )

    assert answer["explored"] is None
    assert f"{answer['model']}@{answer['deliberation']}" == chosen
    assert answer["basis"] == "measured"
    assert answer["expected"]["p_success"] < select.FLOOR


def test_every_measured_point_leads_the_pool_the_alternatives_are_read_from(
    tmp_path: Path,
) -> None:
    """A mean resting on rows outranks a mean resting on arithmetic, everywhere.

    The whole list is read rather than its first entry, because `alternatives`
    carries one entry per model and cannot show two points of one model in the
    order the rule put them.
    """

    _indistinguishable(tmp_path)
    ranked = _ranking(tmp_path, "implement")

    measured = [
        index for index, row in enumerate(ranked) if row.estimate.basis == "measured"
    ]
    other = [
        index for index, row in enumerate(ranked) if row.estimate.basis != "measured"
    ]
    assert measured and other
    assert max(measured) < min(other)


def test_the_ranked_order_is_the_band_then_the_rest_of_what_was_measured(
    tmp_path: Path,
) -> None:
    """The whole order, on a pool no measured point of which clears the floor.

    The band first, ordered on price per finished job; then the measured points
    the band left behind, on chance alone; then every point that is not
    measured, in exactly the order the rule before this one gave it — nothing
    here clears the floor, so that is chance alone as well.
    """

    _indistinguishable(tmp_path)

    ranked = _ranking(tmp_path, "implement")

    assert _spelt(ranked) == [
        "claude-sonnet-5@high",
        "claude-opus-5@high",
        "claude-fable-5-1@high",
        "claude-opus-5@xhigh",
        "claude-sonnet-5@xhigh",
        "claude-opus-5@medium",
        "claude-sonnet-5@medium",
        "claude-opus-5@low",
        "claude-sonnet-5@low",
        "claude-fable-5-1@xhigh",
        "claude-fable-5-1@medium",
        "claude-fable-5-1@low",
        HAIKU,
    ]
    assert not [row for row in ranked if row.estimate.mean >= select.FLOOR]
    band = select._band(ranked)
    assert band is not None
    inside = ranked[:2]
    assert all(row.estimate.mean >= band[1] for row in inside)
    assert select._per_success_cost(inside[0]) < select._per_success_cost(inside[1])
    assert ranked[2].estimate.mean < band[1]


def test_the_band_is_drawn_over_the_rows_it_is_handed_and_nothing_else(
    tmp_path: Path,
) -> None:
    """One statement of the band answers both the plain answer and the step up.

    It reads no store: handed the whole pool it names the best measured point
    in it, handed the points a step up is choosing between it names the best of
    those, and handed rows none of which is measured it names nothing.
    """

    _indistinguishable(tmp_path)
    ranked = _ranking(tmp_path, "implement")

    whole = select._band(ranked)
    assert whole is not None
    assert select._named(whole[0].point) == "claude-opus-5@high"
    assert whole[1] == whole[0].estimate.low

    stepped = [row for row in ranked if row.point.model.id != "claude-opus-5"]
    narrower = select._band(stepped)
    assert narrower is not None
    assert select._named(narrower[0].point) == "claude-sonnet-5@high"
    assert narrower[1] == narrower[0].estimate.low

    assert (
        select._band([row for row in ranked if row.estimate.basis != "measured"])
        is None
    )
    assert select._band([]) is None


def test_the_band_breaks_a_tie_on_the_highest_mean_the_same_way_every_run(
    tmp_path: Path,
) -> None:
    """Two measured points on one mean have to resolve to the same one, always."""

    cat = _module("catalogue").load(tmp_path, SKILL)
    by_id = {model.id: model for model in cat.models}
    tied = [
        _made(by_id["claude-sonnet-5"], "high", mean=0.5, low=0.3, cost=2.0),
        _made(by_id["claude-opus-5"], "high", mean=0.5, low=0.4, cost=1.0),
    ]

    for handed in (tied, list(reversed(tied))):
        found = select._band(handed)
        assert found is not None
        assert found[0].point.model.id == "claude-opus-5"
        assert found[1] == 0.4


@pytest.mark.parametrize("objective", ("cost", "time"))
def test_with_nothing_measured_for_the_kind_the_pool_is_ranked_as_it_was(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], objective: str
) -> None:
    """A pool holding no measured point is answered by the rule that stood before.

    The floor decides who is in and the price per finished job orders them, and
    the band never enters it — there is nothing measured for it to be drawn
    around, so no line about one is written either.
    """

    _unmeasured_kind(tmp_path)
    flags = (
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=mechanical",
        f"--objective={objective}",
        "--seed=0",
    )

    answer = _answer(capsys, *flags)
    ranked = _ranking(tmp_path, "mechanical", objective)

    assert not [row for row in ranked if row.estimate.basis == "measured"]
    clears = [row for row in ranked if row.estimate.mean >= select.FLOOR]
    assert clears
    total = (
        select._per_success_seconds if objective == "time" else select._per_success_cost
    )
    first = min(clears, key=lambda row: (row.cost_usd is None, total(row) or 0.0))
    assert (answer["model"], answer["deliberation"]) == (
        first.point.model.id,
        first.point.deliberation,
    )
    assert answer["basis"] != "measured"
    assert BAND not in (answer["note"] or "")


def test_a_step_up_takes_a_measured_point_over_a_cheaper_estimate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A failure is answered with the evidence before it is answered with a guess.

    Nothing measured above the failed point clears the floor, so before this
    rule the step was the likelier point with the lowest price per finished
    job, measured or not — which here is Sonnet at `medium`, an estimate with
    no row of its own. The step is now the measured point the band admits.
    """

    _indistinguishable(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    answer = _answer(capsys, *flags, "--after=claude-fable-5-1@low")
    guess = _point(capsys, flags, "claude-sonnet-5", "medium")
    failed = _point(capsys, flags, FABLE, "low")

    assert guess["basis"] != "measured"
    assert guess["expected"]["p_success"] > failed["expected"]["p_success"]
    assert (
        guess["expected"]["per_success_cost_usd"]
        < answer["expected"]["per_success_cost_usd"]
    )
    assert "one step up" in (answer["note"] or "")
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "high")
    assert answer["basis"] == "measured"


def test_the_band_decides_the_step_up_where_no_measured_point_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A step up is decided the same way, and says so in the same words.

    Every measured point here is likelier than the failed one and none of them
    clears the floor, so the band decides the step, and the note names the
    point it was drawn around rather than the point that was taken.
    """

    _indistinguishable(tmp_path)

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--kind=implement",
        "--after=claude-fable-5-1@high",
    )

    assert "one step up" in (answer["note"] or "")
    assert (answer["model"], answer["deliberation"]) == ("claude-sonnet-5", "high")
    assert BAND in (answer["note"] or "")
    assert "claude-opus-5@high" in (answer["note"] or "")


def test_the_band_note_is_written_once_in_one_answer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """One line, once, naming the point the band was drawn around.

    Produced in one place off the list the answer was read from, so neither
    the pool the deliberation ceiling was measured against nor the step up
    writes a second copy of it.
    """

    _indistinguishable(tmp_path)
    note = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )["note"]

    assert note is not None
    assert note.count(BAND) == 1
    assert "claude-opus-5@high" in note


def test_a_band_of_one_still_says_that_the_band_decided(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The line is about which branch answered, not about how wide it was."""

    _under(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["basis"] == "measured"
    assert BAND in (answer["note"] or "")
    assert "claude-opus-5@high" in (answer["note"] or "")


def test_no_band_line_where_a_measured_point_cleared_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The floor keeps its whole meaning wherever the measurements can promise."""

    _clearing(tmp_path)

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", "--seed=0"
    )

    assert answer["expected"]["p_success"] >= select.FLOOR
    assert BAND not in (answer["note"] or "")


def test_no_band_line_on_a_call_that_was_spent_exploring(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An exploration was not decided by the band, and never claims it was."""

    _indistinguishable(tmp_path)

    answers = _over_seeds(capsys, (*LIMITED, f"--data={tmp_path}", "--kind=implement"))
    explored = [answer for answer in answers if answer["explored"] is not None]

    assert explored
    for answer in explored:
        assert BAND not in (answer["note"] or "")


def test_the_judge_is_a_measured_reviewer_even_where_none_clears_the_floor(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The grader asks the same ranking, so the band picks its judge too.

    Fable at `high` has twenty `review` rows of its own and finishes about
    three times in four, which does not clear the high-stakes floor. Opus at
    `high` has no row, clears the floor on its prior and costs half as much per
    finished job — and is no longer the judge, a reviewer this machine has
    watched doing the work being the one it grades with.
    """

    _bridged(tmp_path)
    _store(tmp_path, ("review", FABLE, "high", 0.7, 20))
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
    watched = _answer(capsys, *grader, f"--model={FABLE}", "--deliberation=high")

    assert prior["basis"] == "prior"
    assert prior["expected"]["p_success"] >= select.FLOOR
    assert watched["basis"] == "measured"
    assert watched["expected"]["p_success"] < select.FLOOR
    assert (
        prior["expected"]["per_success_cost_usd"]
        < watched["expected"]["per_success_cost_usd"]
    )
    assert (answer["model"], answer["deliberation"]) == (FABLE, "high")
    assert answer["basis"] == "measured"
    assert answer["expected"]["p_success"] < select.FLOOR


def test_exploring_still_compares_one_attempt_at_a_time(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The exploration reads none of this, and a seed still says which calls it is.

    A point the evidence undervalues would never be retried if the exploration
    judged it on the evidence's own mean, which is the reason ADR-0188 gives
    for keeping these comparisons per attempt. So which calls explore is the
    coin alone, and the candidates are still the points cheaper than the answer
    for one attempt, drawn in that order.
    """

    _boundary(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=implement")

    answers = {seed: _answer(capsys, *flags, f"--seed={seed}") for seed in range(DRAWS)}
    coin = {
        seed
        for seed in range(DRAWS)
        if random.Random(seed).random() < select.EXPLORATION
    }
    assert coin
    assert {seed for seed, answer in answers.items() if answer["explored"]} == coin

    ranked = _ranking(tmp_path, "implement")
    plain = ranked[0]
    for dimension in select.DIMENSIONS:
        beyond = select._beyond(ranked, plain, dimension, "cost")
        assert beyond
        prices = [row.cost_usd for row in beyond]
        assert prices == sorted(prices)
        assert all(price < plain.cost_usd for price in prices)


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


def _owing(data_dir: Path) -> None:
    """Write a store one model of which is owed a Trial, at a dearer point.

    Opus at `high` has twenty good `mechanical` rows and at `low` ten bad ones,
    so it is the answer and the band it draws is its own bound of about 0.796.
    Sonnet and Haiku have three failing rows each: enough rows of their own
    that neither is owed a Trial, and low enough means that neither would be
    owed one anyway. Fable has no row for the kind at all, its prior reads
    about 0.994 — well above the band — and it finishes an attempt for about
    1.06 against the answer's 0.67, so the one point owed a Trial here is also
    the dear one.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("mechanical", "claude-opus-5", "high", 1.0, 20),
        ("mechanical", "claude-opus-5", "low", 0.0, 10),
        ("mechanical", "claude-sonnet-5", "high", 0.0, 3),
        ("mechanical", HAIKU, None, 0.0, 3),
    )


def _settled(data_dir: Path, *extra: tuple[str, str, str | None, float, int]) -> None:
    """Write `_owing`'s store again with rows added, the fixture being replaced whole."""

    _store(
        data_dir,
        ("mechanical", "claude-opus-5", "high", 1.0, 20),
        ("mechanical", "claude-opus-5", "low", 0.0, 10),
        ("mechanical", "claude-sonnet-5", "high", 0.0, 3),
        ("mechanical", HAIKU, None, 0.0, 3),
        *extra,
    )


def _shaped(model_id: str, levels: Sequence[str]) -> dict[str, Any]:
    """Return a priced Anthropic model supporting exactly the levels named."""

    return {
        "id": model_id,
        "provider": "anthropic",
        "family": model_id,
        "aliases": [model_id],
        "deliberation": list(levels),
        "price": {
            "input": 3.0,
            "cache_read": 0.3,
            "cache_write": 3.75,
            "output": 15.0,
            "currency": "USD",
            "unit": "per_mtok",
        },
        "reasoning_billed_as": "output",
        "capability": 0.95,
        "released": "2026-09-01",
    }


def _replayed(answers: Sequence[dict[str, Any]]) -> str:
    """Digest one seed sweep: which calls explored, on what, and in what order.

    A thousand seeds are too many to write down and the point of writing them
    down is that none of them moved, so what is kept is a digest over the whole
    sweep — each seed's `explored`, the point it answered, and the whole order
    of the pool that answer was read off.
    """

    spelt = []
    for seed, answer in enumerate(answers):
        listed = ",".join(
            f"{row['model']}@{row['deliberation']}" for row in answer["alternatives"]
        )
        spelt.append(
            f"{seed}|{answer['explored']}|{answer['model']}"
            f"@{answer['deliberation']}|{listed}"
        )
    return hashlib.sha256("\n".join(spelt).encode("utf-8")).hexdigest()


def test_a_model_with_no_rows_for_the_kind_is_tried_however_dear_it_is(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A Trial buys the rows that make a point judgeable, at whatever it costs.

    The downhill exploration reaches a cheaper point about one call in ten and
    a dearer one never, so a model the ranking shuts out of every plain answer
    has no route to the three rows that would let it be judged on its own
    (issue #374). The Trial is that route: no price cap is consulted, and here
    the point tried finishes an attempt for more than half again what the
    answer does.
    """

    _owing(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=mechanical")

    answers = [_answer(capsys, *flags, f"--seed={seed}") for seed in range(DRAWS)]
    tried = _point(capsys, flags, FABLE, "high")
    plain = _point(capsys, flags, "claude-opus-5", "high")

    assert tried["expected"]["cost_usd"] > plain["expected"]["cost_usd"]
    for answer in answers:
        assert (answer["model"], answer["deliberation"]) == (FABLE, "high")
        assert answer["explored"] == TRIAL
        assert answer["basis"] == "prior"
        assert "claude-opus-5@high" in (answer["note"] or "")


def test_a_trial_takes_the_nearest_level_the_tried_model_supports(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A model with a shallower ladder is tried where its own ladder reaches.

    The answer sits at `high` and the model owed the Trial offers `low` alone,
    so `low` is where it is tried — the nearest-level rule an exploration of
    the model dimension already follows, asked again rather than restated.
    """

    _profile(tmp_path)
    _refresh(tmp_path, _shaped("test-shallow", ["low"]))
    _settled(tmp_path, ("mechanical", FABLE, "high", 0.0, 3))

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--seed=0"
    )

    assert (answer["model"], answer["deliberation"]) == ("test-shallow", "low")
    assert answer["explored"] == TRIAL


def test_a_trial_ends_once_the_store_holds_enough_rows_for_the_kind(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Three rows of its own take a model off the Trial and onto its own record.

    The boundary is read at both sides of `ENOUGH`, and the row that crosses it
    is taken at another level, because what ends a Trial is the model's rows
    for the kind wherever on the ladder they were taken.
    """

    _owing(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--seed=0")

    _settled(tmp_path, ("mechanical", FABLE, "high", 1.0, ENOUGH - 1))
    short = _answer(capsys, *flags)

    _settled(
        tmp_path,
        ("mechanical", FABLE, "high", 1.0, ENOUGH - 1),
        ("mechanical", FABLE, "low", 1.0, 1),
    )
    full = _answer(capsys, *flags)

    assert (short["model"], short["deliberation"]) == (FABLE, "high")
    assert short["explored"] == TRIAL
    assert (full["model"], full["deliberation"]) == ("claude-opus-5", "high")
    assert full["explored"] is None


def test_rows_at_any_level_count_towards_the_kind_the_trial_is_owed_for(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A Trial ends on three rows spread across the ladder, one of them at the point tried.

    The count is the model's rows for the kind rather than the cell's, and
    `Estimate.n` is not it: that reads the deepest group holding anything, so
    this model, with one row at the level being asked about and two elsewhere,
    reports one run while the store holds the three that end its Trial. A Trial
    counted off that figure would never end.
    """

    _owing(tmp_path)
    _settled(
        tmp_path,
        *[("mechanical", FABLE, level, 1.0, 1) for level in ("high", "low", "medium")],
    )

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--seed=0"
    )
    spread = _point(
        capsys,
        (*LIMITED, f"--data={tmp_path}", "--kind=mechanical"),
        FABLE,
        "high",
    )

    assert spread["expected"]["runs"] == 1
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert answer["explored"] is None


def test_a_model_below_the_band_is_left_to_the_downhill_exploration(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A Trial tries a model that might be the answer, never one that cannot be.

    Two stores holding the same models, differing only in how many good rows
    the measured point has and therefore in where the bound it draws falls.
    Sonnet is untested for the kind in both. Where its prior sits above that
    bound it is owed a Trial; where the bound has risen past its prior it is
    not, and the call is answered as it would have been without the rule — the
    road such a model keeps being the downhill exploration, which is cheap by
    construction.
    """

    below = tmp_path / "below"
    above = tmp_path / "above"
    for data_dir, rows in ((below, 200), (above, 20)):
        _profile(data_dir)
        _store(
            data_dir,
            ("mechanical", "claude-opus-5", "high", 1.0, rows),
            ("mechanical", "claude-opus-5", "low", 0.0, 10),
            ("mechanical", FABLE, "high", 0.0, 3),
            ("mechanical", HAIKU, None, 0.0, 3),
        )

    quiet = _answer(
        capsys, *LIMITED, f"--data={below}", "--kind=mechanical", "--seed=0"
    )
    owed = _answer(capsys, *LIMITED, f"--data={above}", "--kind=mechanical", "--seed=0")
    ranked = _ranking(below, "mechanical")
    drawn = select._band(ranked)
    sonnet = next(
        row for row in ranked if select._named(row.point) == "claude-sonnet-5@high"
    )

    assert drawn is not None
    assert sonnet.estimate.mean < drawn[1]
    assert (quiet["model"], quiet["deliberation"]) == ("claude-opus-5", "high")
    assert quiet["explored"] is None
    assert (owed["model"], owed["deliberation"]) == ("claude-sonnet-5", "high")
    assert owed["explored"] == TRIAL


def test_a_kind_with_no_measured_point_owes_no_trial(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without a measured point there is no band, and without a band no Trial.

    The ranking already lets an untested point be the plain answer where the
    pool holds nothing measured for the kind, so there is no door here for a
    Trial to open.
    """

    _unmeasured_kind(tmp_path)

    answers = [
        _answer(
            capsys,
            *LIMITED,
            f"--data={tmp_path}",
            "--kind=mechanical",
            f"--seed={seed}",
        )
        for seed in range(DRAWS)
    ]

    assert select._band(_ranking(tmp_path, "mechanical")) is None
    assert {answer["explored"] for answer in answers} <= {None, *select.DIMENSIONS}


def test_a_trial_in_progress_is_taken_before_one_not_yet_begun(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """One model at a time per kind, and the one already part-way is that model.

    Two models are owed here and the ranked list reaches Sonnet's point first,
    so Sonnet is tried while neither has a row. A single row for Fable makes
    Fable's the Trial in progress, and it is taken over the earlier-ranked
    point until its three rows are in — which is what keeps one Trial from
    becoming three models with one row each.
    """

    fresh = tmp_path / "fresh"
    begun = tmp_path / "begun"
    shared = (
        ("mechanical", "claude-opus-5", "high", 1.0, 20),
        ("mechanical", "claude-opus-5", "low", 0.0, 10),
        ("mechanical", HAIKU, None, 0.0, 3),
    )
    for data_dir in (fresh, begun):
        _profile(data_dir)
    _store(fresh, *shared)
    _store(begun, *shared, ("mechanical", FABLE, "high", 1.0, 1))

    neither = _answer(
        capsys, *LIMITED, f"--data={fresh}", "--kind=mechanical", "--seed=0"
    )
    started = _answer(
        capsys, *LIMITED, f"--data={begun}", "--kind=mechanical", "--seed=0"
    )
    again = _answer(
        capsys, *LIMITED, f"--data={begun}", "--kind=mechanical", "--seed=7"
    )

    assert (neither["model"], neither["deliberation"]) == ("claude-sonnet-5", "high")
    assert neither["explored"] == TRIAL
    assert (started["model"], started["deliberation"]) == (FABLE, "high")
    assert started["explored"] == TRIAL
    assert (again["model"], again["deliberation"]) == (FABLE, "high")


def test_the_answers_own_model_is_never_the_model_owed_a_trial(
    tmp_path: Path,
) -> None:
    """A Trial is a point tried instead of the answer, so it is never the answer's.

    No pool the ranking produces can put an unmeasured point first while the
    band is non-empty, so this guard is unreachable through a fixture and is
    held at the unit level instead: a pool built by hand whose first point is
    its model's, with no rows behind that model at all, still yields no Trial
    of it. A note saying the evidence would have chosen the point just chosen
    would say nothing.
    """

    evidence = _module("evidence")
    cat = _module("catalogue").load(tmp_path, SKILL)
    kinds = evidence.load_kinds(SKILL)
    estimator = evidence.Estimator([], cat, kinds)
    by_id = {model.id: model for model in cat.models}
    first = select.Scored(
        select.Point(by_id["claude-sonnet-5"], "high"),
        evidence.Estimate(
            mean=0.99, low=0.9, n=0.0, basis="prior", alpha=1.0, beta=1.0
        ),
        {},
        1.0,
        100.0,
    )
    beside = _made(by_id["claude-sonnet-5"], "low", mean=0.9, low=0.5, cost=0.5)
    measured = _made(by_id["claude-opus-5"], "high", mean=0.8, low=0.4, cost=2.0)
    ranked = [first, beside, measured]

    owed = select._owed(ranked, ranked, "mechanical", estimator)

    assert estimator.rows_for_kind("mechanical", "claude-sonnet-5") == 0
    assert owed is not None
    assert owed.point.model.id == "claude-opus-5"


@pytest.mark.parametrize(
    "asked",
    (
        ("--stakes=high",),
        ("--model=claude-sonnet-5",),
        ("--deliberation=low",),
        ("--after=claude-opus-5@low",),
    ),
)
def test_the_three_requests_that_are_never_explored_are_never_trials(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], asked: tuple[str, ...]
) -> None:
    """A Trial is an experiment, and the same three requests refuse one.

    High stakes wants the best point the evidence knows of, a lock is an
    instruction rather than a dimension to vary, and a caller naming the point
    that just failed is asking for the step up. `_explorable` already says so,
    and a Trial asks it rather than stating it a second time.
    """

    _owing(tmp_path)

    answers = [
        _answer(
            capsys,
            *LIMITED,
            f"--data={tmp_path}",
            "--kind=mechanical",
            *asked,
            f"--seed={seed}",
        )
        for seed in range(DRAWS)
    ]

    assert {answer["explored"] for answer in answers} == {None}


def test_a_point_above_the_deliberation_ceiling_is_never_tried(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The ceiling narrowed the pool, and the Trial's candidates are that pool.

    Asked with no ceiling of its own the Trial takes Fable at `high`; asked
    under a `medium` ceiling every answer is a point that ceiling admits,
    because the points above it were never in the pool the call ranked.
    Nothing in the Trial reads the ceiling to arrive at that.
    """

    _owing(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=mechanical")

    open_call = _answer(capsys, *flags, "--seed=0")
    capped = [
        _answer(capsys, *flags, "--max-deliberation=medium", f"--seed={seed}")
        for seed in range(DRAWS)
    ]

    assert (open_call["model"], open_call["deliberation"]) == (FABLE, "high")
    assert open_call["explored"] == TRIAL
    assert {answer["deliberation"] for answer in capped} <= {None, "low", "medium"}
    assert TRIAL in {answer["explored"] for answer in capped}


def test_a_model_the_ceiling_leaves_no_point_for_is_never_tried(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A model reaching no level under the ceiling has no point to be tried at.

    It is not excluded from the Trial: it is absent from the pool the Trial's
    candidates are the points of, which is the same thing arrived at without
    the rule having to know the ceiling exists.
    """

    _profile(tmp_path)
    _refresh(tmp_path, _shaped("test-deep", ["max"]))
    _settled(tmp_path, ("mechanical", FABLE, "high", 0.0, 3))

    answers = [
        _answer(
            capsys,
            *LIMITED,
            f"--data={tmp_path}",
            "--kind=mechanical",
            EVERY,
            f"--seed={seed}",
        )
        for seed in range(DRAWS)
    ]

    for answer in answers:
        assert "test-deep" not in _named_in(answer)
        assert answer["explored"] != TRIAL


def test_a_point_the_pool_never_held_is_never_given_a_trial(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Every filter on the pool is a filter on the Trial, for free.

    One store asked twice. Where the scope admits the whole catalogue the Trial
    goes to the earliest-ranked point owed one among it; where the call is held
    to the maker paying for this turn those points are not in the pool it
    ranked, nothing left in it is owed a Trial, and none is given.
    """

    _profile(tmp_path)
    _settled(tmp_path, ("mechanical", FABLE, "high", 0.0, 3))
    flags = (f"--data={tmp_path}", "--kind=mechanical", "--harness=claude-code", EVERY)

    wide = _answer(capsys, *flags, "--scope=all", "--seed=0")
    narrow = [
        _answer(capsys, *flags, "--scope=limited", f"--seed={seed}")
        for seed in range(DRAWS)
    ]

    assert wide["explored"] == TRIAL
    assert wide["model"] == "grok-4.6"
    for answer in narrow:
        assert "grok-4.6" not in _named_in(answer)
        assert answer["explored"] != TRIAL


def test_an_unpriceable_point_is_tried_where_it_is_the_model_owed_a_trial(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """No price cap means a point with no price at all is a candidate like any other.

    The downhill exploration excludes such a point on purpose — an absence read
    as a nought would make it the cheapest thing on the frontier — but a Trial
    consults no price, so the one model owed one here is tried although nothing
    can say what it costs.
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
    _store(
        tmp_path,
        ("implement", "claude-sonnet-5", "high", 1.0, 20),
        ("implement", FABLE, "high", 0.0, 3),
    )

    answer = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=implement", EVERY, "--seed=0"
    )

    assert (answer["model"], answer["deliberation"]) == ("test-unpriced", "high")
    assert answer["explored"] == TRIAL
    assert answer["expected"]["cost_usd"] is None


def test_while_a_trial_is_owed_every_reversible_call_is_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Three consecutive jobs, rather than three calls in thirty.

    The one-in-ten coin is not tossed at all while a model is owed a Trial, so
    no seed leaves a plain answer among these; once the store holds that
    model's three rows the coin comes back and the ordinary mixture of plain
    and explored answers returns.
    """

    _owing(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", "--kind=mechanical")

    owed = [_answer(capsys, *flags, f"--seed={seed}") for seed in range(DRAWS)]

    _settled(tmp_path, ("mechanical", FABLE, "high", 1.0, ENOUGH))
    done = [_answer(capsys, *flags, f"--seed={seed}") for seed in range(DRAWS)]

    assert {answer["explored"] for answer in owed} == {TRIAL}
    assert [answer for answer in done if answer["explored"] is None]
    assert {answer["explored"] for answer in done} <= {None, *select.DIMENSIONS}


def test_a_trial_says_it_was_one_and_what_the_evidence_would_have_chosen(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A reader must tell a deliberate Trial from a routing fault at a glance.

    The note names the call as a Trial, names the point being tried and says
    what the evidence would have chosen — the duty ADR-0184 gives the
    exploration note — and it never calls `trial` a dimension, a Trial being a
    point tried instead of the answer rather than one axis of it moved.
    """

    _owing(tmp_path)
    tried = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--kind=mechanical", "--seed=0"
    )

    _boundary(tmp_path)
    ordinary = [
        answer
        for answer in _over_seeds(
            capsys, (*LIMITED, f"--data={tmp_path}", "--kind=implement")
        )
        if answer["explored"] is not None
    ]

    note = tried["note"] or ""
    assert tried["explored"] == TRIAL
    assert TRIAL in note
    assert f"{FABLE}@high" in note
    assert "would have chosen" in note
    assert "claude-opus-5@high" in note
    assert f"{TRIAL} dimension" not in note

    assert ordinary
    for answer in ordinary:
        assert answer["explored"] in select.DIMENSIONS
        assert f"{answer['explored']} dimension" in (answer["note"] or "")


def test_no_trial_owed_leaves_the_exploration_exactly_as_it_was(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A call owing no Trial draws what it drew before, on every seed.

    `_boundary` holds `ENOUGH` rows for every model in its pool, so nothing
    there is ever owed a Trial and the generator is untouched. Which seeds
    explored, which dimension each moved, which point each answered and the
    whole order of the pool behind it are read against the sweep the module
    produced before this rule existed.
    """

    _boundary(tmp_path)

    answers = _over_seeds(
        capsys, (*LIMITED, f"--data={tmp_path}", "--kind=implement", EVERY)
    )

    assert {answer["explored"] for answer in answers} <= {None, *select.DIMENSIONS}
    assert _replayed(answers) == EXPLORATION_AT_BASE


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


# Every flag either bridge uses to grant or withhold permission. An answer
# carries the ones the caller's own level named and no others.
PERMISSION_FLAGS: frozenset[str] = frozenset(
    {
        "-s",
        "--sandbox",
        "--approve-for-me",
        "--dangerously-bypass-approvals-and-sandbox",
        "--permission-mode",
    }
)


def test_a_caller_s_own_permission_level_reaches_the_command_it_is_handed(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A delegated start inherits the level its caller is running at.

    The caller states it, nothing here reads it off anything, and it arrives
    in the launch spelled the way the CLI being started spells it — which is
    what lets a builder commit and reach the network without its caller
    editing the command it was given.
    """

    _profile(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude"))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=process",
        "--kind=implement",
        "--permissions=bypass",
    )

    command = answer["launch"]["command"] or []
    assert command[command.index("--permission-mode") + 1] == "bypassPermissions"


def test_an_answer_asked_for_without_a_level_names_no_permission_flag(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Silence leaves the decision to the started CLI's own configuration."""

    _profile(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude"))

    answer = _answer(
        capsys, f"--data={tmp_path}", "--harness=process", "--kind=implement"
    )

    command = answer["launch"]["command"] or []
    assert not PERMISSION_FLAGS.intersection(command)


def test_a_permission_level_nothing_here_knows_is_answered_and_named(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Never a refusal: there is no answer a caller may read as *start nothing*.

    A caller that could not read its own level, or read one this vocabulary
    does not hold, still gets a launch. What it also gets is the value back in
    the note, so the mismatch is visible where the decision is read.
    """

    _profile(tmp_path)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude"))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=process",
        "--kind=implement",
        "--permissions=paranoid",
    )

    assert answer["ok"] is True
    assert not PERMISSION_FLAGS.intersection(answer["launch"]["command"] or [])
    assert "paranoid" in (answer["note"] or "")


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


# --- Which models are eligible: the makers chosen, and nothing narrower ------


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


def test_a_chosen_makers_models_are_candidates_and_an_unchosen_makers_are_not(
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


def _deepest(data_dir: Path) -> None:
    """Write a store whose likeliest point, by far, is Opus at `max`.

    Only Opus at `max` ever finished, and every other model Anthropic offers
    has failed, so the band is drawn around Opus at `max`, the only point its
    own bound admits — which is the case in which the top of the ladder used
    to win unasked. Opus at `xhigh` has failed too, so a step up from it has nowhere
    likelier to go but `max`.
    """

    _profile(data_dir)
    _store(
        data_dir,
        ("implement", "claude-opus-5", "low", 0.0, 8),
        ("implement", "claude-opus-5", "xhigh", 0.0, 8),
        ("implement", "claude-opus-5", "max", 1.0, 8),
        ("implement", "claude-sonnet-5", "high", 0.0, 8),
        ("implement", FABLE, "high", 0.0, 8),
        ("implement", HAIKU, None, 0.0, 8),
    )


def _levels_named(answer: dict[str, Any]) -> set[str | None]:
    """Return every level the answer names, chosen or offered beside it."""

    return {
        answer["deliberation"],
        *(row["deliberation"] for row in answer["alternatives"]),
    }


def test_with_no_deliberation_ceiling_given_nothing_above_xhigh_is_chosen(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The top of the ladder is never reached for unasked (issue #323).

    Nothing clears the floor, so the band decides, and the band around Opus
    at `max` admits that point alone. The deliberation ceiling defaults to
    `xhigh`, so `max` is not in the pool at all, and the note says the
    ceiling is why the answer is not the point the evidence would have taken.
    """

    _deepest(tmp_path)

    answer = _answer(capsys, *LIMITED, f"--data={tmp_path}", EVERY, "--stakes=high")

    assert "max" not in _levels_named(answer)
    assert answer["launch"]["how"] != "inherit"
    assert "deliberation ceiling" in answer["note"]


def test_a_call_that_explores_stays_under_the_deliberation_ceiling(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An exploration moves within the pool, and `max` is not in it."""

    _deepest(tmp_path)

    answers = [
        _answer(capsys, *LIMITED, f"--data={tmp_path}", EVERY, f"--seed={seed}")
        for seed in range(DRAWS)
    ]

    assert any(answer["explored"] for answer in answers)
    for answer in answers:
        assert "max" not in _levels_named(answer)


def test_a_step_up_from_xhigh_does_not_climb_past_the_deliberation_ceiling(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The only likelier point is `max`, so the ceiling is why there is no step.

    Every other level of every model Anthropic offers has failed outright, and
    Opus at `xhigh` finished some of the time, so without the ceiling the step
    up is `max` and nothing else.
    """

    _profile(tmp_path)
    _store(
        tmp_path,
        ("implement", "claude-opus-5", "low", 0.0, 8),
        ("implement", "claude-opus-5", "medium", 0.0, 8),
        ("implement", "claude-opus-5", "high", 0.0, 8),
        ("implement", "claude-opus-5", "xhigh", 0.6, 20),
        ("implement", "claude-opus-5", "max", 1.0, 20),
        *(
            ("implement", model, level, 0.0, 8)
            for model in ("claude-sonnet-5", FABLE)
            for level in ("low", "medium", "high", "xhigh", "max")
        ),
        ("implement", HAIKU, None, 0.0, 8),
    )
    free = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--after=claude-opus-5@xhigh",
        "--max-deliberation=max",
    )
    assert (free["model"], free["deliberation"]) == ("claude-opus-5", "max")

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        EVERY,
        "--after=claude-opus-5@xhigh",
    )

    assert "max" not in _levels_named(answer)
    assert "deliberation ceiling 'xhigh' ruled out claude-opus-5@max" in answer["note"]


def test_a_ceiling_at_max_admits_the_whole_ladder_and_a_lower_one_narrows_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--max-deliberation` moves the ceiling in either direction."""

    _deepest(tmp_path)
    flags = (*LIMITED, f"--data={tmp_path}", EVERY, "--stakes=high")

    opened = _answer(capsys, *flags, "--max-deliberation=max")
    lowered = _answer(capsys, *flags, "--max-deliberation=high")

    assert (opened["model"], opened["deliberation"]) == ("claude-opus-5", "max")
    assert "deliberation ceiling" not in (opened["note"] or "")
    assert not {"xhigh", "max"} & _levels_named(lowered)
    assert "deliberation ceiling 'high'" in lowered["note"]


def test_the_ceiling_compares_positions_so_a_level_above_max_is_excluded() -> None:
    """A level nobody has named yet sits above `max`, and the default keeps it out.

    The ladder is passed in rather than patched into the catalogue, which
    silently drops a level its own ladder lacks and would leave the rule
    unexercised (issue #323).
    """

    ladder = ("low", "medium", "high", "xhigh", "max", "beyond")
    ceiling = select.DEFAULT_MAX_DELIBERATION

    assert ceiling == "xhigh"
    assert select._admitted("xhigh", ceiling, ladder)
    assert not select._admitted("max", ceiling, ladder)
    assert not select._admitted("beyond", ceiling, ladder)
    assert not select._admitted("beyond", "max", ladder)
    assert select._admitted(None, "low", ladder)


def test_a_deliberation_lock_at_max_lifts_the_ceiling_and_says_so(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The user named the level, and an explicit choice outranks the default."""

    _deepest(tmp_path)

    answer = _answer(
        capsys,
        *LIMITED,
        f"--data={tmp_path}",
        "--model=claude-opus-5",
        "--deliberation=max",
    )

    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "max")
    assert (
        "deliberation lock 'max' lifted the deliberation ceiling 'xhigh'"
        in answer["note"]
    )

    unlocked_model = _answer(
        capsys, *LIMITED, f"--data={tmp_path}", "--deliberation=max"
    )

    assert unlocked_model["deliberation"] == "max"
    assert "lifted the deliberation ceiling" in unlocked_model["note"]


def _ladder_with_a_gap(data_dir: Path, *levels: str) -> None:
    """Add one Anthropic model supporting only the levels given."""

    _refresh(
        data_dir,
        {
            "id": "test-gapped",
            "provider": "anthropic",
            "family": "gapped",
            "aliases": ["gapped"],
            "deliberation": list(levels),
            "price": {
                "input": 3.0,
                "cache_read": 0.3,
                "cache_write": 3.75,
                "output": 15.0,
            },
            "reasoning_billed_as": "output",
            "capability": 0.8,
            "released": "2026-09-01",
        },
    )
    _profile(data_dir)


def test_a_lock_under_the_ceiling_never_falls_back_to_a_level_above_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The nearest supported level is looked for at or below the ceiling.

    The model supports `low` and `xhigh`, so `high` is nearest to `xhigh`; with
    the ceiling at `high` the fallback is `low` instead.
    """

    _ladder_with_a_gap(tmp_path, "low", "xhigh")
    flags = (f"--data={tmp_path}", "--harness=claude-code", "--model=test-gapped")

    open_ladder = _answer(
        capsys, *flags, "--deliberation=high", "--max-deliberation=max"
    )
    capped = _answer(capsys, *flags, "--deliberation=high", "--max-deliberation=high")

    assert (open_ladder["model"], open_ladder["deliberation"]) == (
        "test-gapped",
        "xhigh",
    )
    assert (capped["model"], capped["deliberation"]) == ("test-gapped", "low")


def test_a_model_lock_alone_is_still_held_to_the_ceiling(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A model re-admitted from the catalogue is filtered like any other point.

    With no valid profile the pool is empty, so the lock reaches past it and
    admits every level of the model it names — `max` among them.
    """

    _store(tmp_path, ("implement", "claude-opus-5", "max", 1.0, 8))

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--model=claude-opus-5",
    )

    assert answer["basis"] != "inherit"
    assert answer["model"] == "claude-opus-5"
    assert answer["deliberation"] != "max"


def test_a_point_with_no_effort_control_is_admitted_under_any_ceiling(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A model with no levels has nothing to hold against a ceiling."""

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--model=haiku",
        "--scope=all",
        "--max-deliberation=low",
    )

    assert answer["model"] == HAIKU
    assert answer["deliberation"] is None
    assert answer["launch"]["how"] != "inherit"


def test_a_ceiling_that_empties_the_pool_inherits_and_names_the_ceiling(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Never a refusal: the caller keeps its own seat and is told why."""

    _ladder_with_a_gap(tmp_path, "max")

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--seat=claude-opus-5@high",
        "--model=test-gapped",
    )

    assert answer["launch"]["how"] == "inherit"
    assert (answer["model"], answer["deliberation"]) == ("claude-opus-5", "high")
    assert "deliberation ceiling 'xhigh' admits no candidate" in answer["note"]


# --- the quota guard ------------------------------------------------------

# The two Harnesses the fixture profile pays a subscription on, and the model
# each one's plan pays for. Named rather than derived, so a test asserting that
# one maker's points went says which channel paid for them.
CLAUDE_CODE: str = "claude-code"
CODEX: str = "codex"

# The week, in seconds, which is what a fixture divides to place a window at a
# share of its own length.
WEEK: int = 10080 * 60

# A call that reaches both makers: a process caller with both CLIs installed
# and a profile paying for each, which is the only shape in which holding one
# channel back leaves something on the other to answer with. High stakes so
# that no call here is spent exploring, exploration being the one other thing
# that moves the top of a ranking.
ASKED: tuple[str, ...] = ("--harness=process", "--stakes=high", "--kind=implement")


def _window(
    home: Path,
    harness: str,
    *,
    used: float,
    elapsed: float,
    age: float = 60.0,
    window: int = 10080,
) -> None:
    """Put one Harness's weekly window at a used share and a share elapsed.

    Written where the guard reads that harness: the file this collection's
    status line writes, for Claude Code, and a session log of Codex's own, for
    Codex. Both are under the home every test in this module is pointed at, and
    neither is under the directory `--data` names.
    """

    moment = time.time()
    resets = int(moment + (1.0 - elapsed) * WEEK)
    if harness == CODEX:
        day = datetime.now(UTC).strftime("%Y/%m/%d")
        logs = home / ".codex" / "sessions" / day
        logs.mkdir(parents=True, exist_ok=True)
        taken = datetime.fromtimestamp(moment - age, UTC).isoformat()
        (logs / "rollout-fixture.jsonl").write_text(
            json.dumps(
                {
                    "timestamp": taken.replace("+00:00", "Z"),
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {"total_token_usage": {"total_tokens": 47535}},
                        "rate_limits": {
                            "limit_id": "codex",
                            "primary": {
                                "used_percent": used,
                                "window_minutes": window,
                                "resets_at": resets,
                            },
                            "secondary": None,
                            "plan_type": "pro",
                        },
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return

    data = home / ".kntnt" / "model-selector"
    data.mkdir(parents=True, exist_ok=True)
    (data / "quota.json").write_text(
        json.dumps(
            {
                "channels": {
                    harness: {
                        "used_percent": used,
                        "resets_at": resets,
                        "window_minutes": window,
                        "written_at": int(moment - age),
                    }
                }
            }
        ),
        encoding="utf-8",
    )


def _reaching_both(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *groups: tuple[str, str, Any, float, int],
) -> tuple[str, ...]:
    """Set up the call that reaches both makers, and return its flags."""

    _bridged(tmp_path)
    if groups:
        _store(tmp_path, *groups)
    monkeypatch.setenv("PATH", path_holding(tmp_path, "claude", "codex"))
    return (f"--data={tmp_path}", *ASKED)


def test_a_channel_running_ahead_of_its_week_is_left_out_of_the_answer(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """Every point the held-back channel pays for goes, and another answers.

    The guard narrows the pool before anything reads it, so the models are
    absent from the alternatives as well as from the answer — a pool that still
    held them and merely ranked something above them would read the same off
    the chosen model alone.
    """

    asked = _reaching_both(tmp_path, monkeypatch)
    _window(elsewhere, CODEX, used=95.0, elapsed=0.5)

    answer = _answer(capsys, *asked, EVERY)

    assert _named_in(answer) == ANTHROPIC
    assert answer["channel"]["harness"] == CLAUDE_CODE


def test_ninety_per_cent_holds_a_channel_back_whatever_the_pace(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """Behind the week and nearly out of it is still nearly out of it."""

    asked = _reaching_both(tmp_path, monkeypatch)
    _window(elsewhere, CODEX, used=90.0, elapsed=0.99)

    assert _named_in(_answer(capsys, *asked, EVERY)) == ANTHROPIC


def test_a_channel_below_both_thresholds_is_held_back_by_neither(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """A window running to time is not a reason to narrow anybody's answer."""

    asked = _reaching_both(tmp_path, monkeypatch)
    _window(elsewhere, CODEX, used=55.0, elapsed=0.5)
    _window(elsewhere, CLAUDE_CODE, used=10.0, elapsed=0.5)

    assert _named_in(_answer(capsys, *asked, EVERY)) == ANTHROPIC | OPENAI


def test_the_guard_never_empties_the_pool(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """Where every candidate's channel would go, nothing goes.

    A guard that answered `inherit` because both subscriptions are busy has
    stopped the work over an optimisation, and this Skill answers every call it
    can parse. So the answer is exactly the one the ranking gives with no
    figure on the machine at all.
    """

    asked = _reaching_both(tmp_path, monkeypatch)
    unguarded = _answer(capsys, *asked, EVERY)

    _window(elsewhere, CODEX, used=95.0, elapsed=0.5)
    _window(elsewhere, CLAUDE_CODE, used=95.0, elapsed=0.5)
    answer = _answer(capsys, *asked, EVERY)

    assert _named_in(answer) == ANTHROPIC | OPENAI
    assert (answer["model"], answer["deliberation"]) == (
        unguarded["model"],
        unguarded["deliberation"],
    )
    assert "quota guard" not in (answer["note"] or "")


def test_a_locked_model_is_answered_though_its_channel_is_held_back(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """A `--model` is the user naming what they want, and the guard holds nothing."""

    asked = _reaching_both(tmp_path, monkeypatch)
    _window(elsewhere, CODEX, used=95.0, elapsed=0.5)

    answer = _answer(capsys, *asked, "--model=gpt-5.6-luna")

    assert answer["model"] == "gpt-5.6-luna"
    assert "quota guard" not in (answer["note"] or "")


def test_the_note_names_the_guard_and_the_point_it_ruled_out(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """Judged against the same call ranked without the guard, and not otherwise.

    A reader who finds a dearer point chosen has to be able to tell the guard
    at work from the ranking's own verdict, so the comparison is against the
    answer this call would have given with every channel admitted.
    """

    measured = ("implement", "gpt-5.6-luna", "low", 1.0, 20)
    asked = _reaching_both(tmp_path, monkeypatch, measured)

    # The same call, first with every channel admitted: what the guard has to
    # be judged against is this answer, not a point named in the test.
    plain = _answer(capsys, *asked)
    assert plain["channel"]["harness"] == CODEX

    _window(elsewhere, CODEX, used=95.0, elapsed=0.5)
    answer = _answer(capsys, *asked)

    ruled_out = f"{plain['model']}@{plain['deliberation']}"
    assert answer["model"] != plain["model"]
    assert f"the quota guard ruled out {ruled_out}" in answer["note"]


def test_a_guard_that_changed_nothing_says_nothing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
) -> None:
    """The channel is held back and the answer was never going to be on it.

    The note is about what the guard cost this call, so a guard that took away
    points the ranking had already beaten is a line nobody needs to read.
    """

    measured = ("implement", "claude-haiku-4-5-20251001", None, 1.0, 20)
    asked = _reaching_both(tmp_path, monkeypatch, measured)

    plain = _answer(capsys, *asked, EVERY)
    assert plain["channel"]["harness"] == CLAUDE_CODE

    _window(elsewhere, CODEX, used=95.0, elapsed=0.5)
    answer = _answer(capsys, *asked, EVERY)

    assert answer["model"] == plain["model"]
    assert _named_in(answer) == ANTHROPIC
    assert "quota guard" not in (answer["note"] or "")


def _damage(home: Path, condition: str) -> None:
    """Leave one of the five ways a figure can fail to be one, for both sources."""

    data = home / ".kntnt" / "model-selector"
    logs = home / ".codex" / "sessions" / datetime.now(UTC).strftime("%Y/%m/%d")
    if condition == "absent":
        return
    if condition == "unreadable":
        (data / "quota.json").mkdir(parents=True)
        logs.mkdir(parents=True, exist_ok=True)
        (logs / "rollout-fixture.jsonl").mkdir()
        return
    if condition == "another shape":
        data.mkdir(parents=True, exist_ok=True)
        (data / "quota.json").write_text('{"channels": []}', encoding="utf-8")
        logs.mkdir(parents=True, exist_ok=True)
        (logs / "rollout-fixture.jsonl").write_text("not json\n", encoding="utf-8")
        return
    if condition == "stale":
        _window(home, CLAUDE_CODE, used=99.0, elapsed=0.5, age=25 * 3600.0)
        _window(home, CODEX, used=99.0, elapsed=0.5, age=25 * 3600.0)
        return
    _window(home, CLAUDE_CODE, used=99.0, elapsed=1.5)
    _window(home, CODEX, used=99.0, elapsed=1.5)


@pytest.mark.parametrize(
    "condition", ["absent", "unreadable", "another shape", "stale", "reset"]
)
def test_no_figure_is_no_guard_and_is_said_nowhere(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    elsewhere: Path,
    condition: str,
) -> None:
    """Each of the five, on both sources, with exit 0 and nothing said.

    A figure the machine has not got is the ordinary state of a machine, so
    none of these is a problem to report: the call is answered exactly as it
    would be with nothing written anywhere.
    """

    asked = _reaching_both(tmp_path, monkeypatch)
    _damage(elsewhere, condition)

    answer = _answer(capsys, *asked, EVERY)

    assert answer["ok"] is True
    assert _named_in(answer) == ANTHROPIC | OPENAI
    assert "quota" not in (answer["note"] or "")


# --- Only the newest release of a family is a candidate ----------------------

# The maker whose seeded catalogue holds exactly one model, so that a profile
# choosing it alone puts one family in the pool and the releases a fixture adds
# to it are the whole of what is ranked. Its seeded release carries no date,
# which makes it the undated half of the tie the rule has to settle as well.
XAI: str = "spacexai"
SEEDED_GROK: str = "grok-4.6"

# The levels the seeded Grok supports, so that a release a fixture adds sits on
# the same ladder rather than differing from it by accident.
GROK_LEVELS: tuple[str, ...] = ("low", "medium", "high", "xhigh")

# What every Grok call here asks with: the family's own maker reached through
# the opencode bridge, high stakes so that no answer is spent exploring, and
# every alternative listed so that a release left in the pool is seen.
GROK_ASKED: tuple[str, ...] = (
    "--harness=claude-code",
    "--kind=implement",
    "--stakes=high",
    EVERY,
)


def _grok(data_dir: Path, *releases: dict[str, Any]) -> None:
    """Choose xAI alone, paid through OpenRouter, and add releases of Grok.

    A Claude Code caller reaches them over the opencode bridge, so nothing has
    to be on the `PATH` for the whole family to be in the pool at once.
    """

    _profile(
        data_dir,
        harnesses=["claude-code", "opencode"],
        makers=[XAI],
        channels=[
            {
                "provider": XAI,
                "harness": "opencode",
                "pay": "api",
                "gateway": "openrouter",
            }
        ],
    )
    _refresh(data_dir, *releases)


def _release(
    identifier: str,
    released: str | None = None,
    levels: Sequence[str] = GROK_LEVELS,
    gateways: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return one release of the Grok family, routed as the seeded one is."""

    return {
        "id": identifier,
        "provider": XAI,
        "family": "grok",
        "aliases": ["grok"],
        "deliberation": list(levels),
        "price": {"input": 3.0, "cache_read": 0.3, "cache_write": 3.75, "output": 15.0},
        "reasoning_billed_as": "output",
        "capability": 0.8,
        "gateways": (
            {"openrouter": f"x-ai/{identifier}"} if gateways is None else gateways
        ),
        "released": released,
    }


def _three_releases(data_dir: Path) -> None:
    """Write the family at three releases, every one of them admitted.

    The seeded `grok-4.6` carries no date, and the two added ones do, so the
    newest is unambiguous and the oldest is the undated case at the same time.
    """

    _grok(data_dir, _release("grok-5", "2026-02-01"), _release("grok-6", "2026-08-01"))


def test_the_answer_is_the_newest_release_of_the_family(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A maker that goes on listing every release it ever shipped offers one."""

    _three_releases(tmp_path)

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert answer["model"] == "grok-6"


def test_no_release_a_newer_one_replaced_is_offered_beside_the_answer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An alternative is a point the caller may run, so an older release is none.

    Reading the chosen model alone would pass on a pool that still held the
    older releases and merely ranked the newest above them.
    """

    _three_releases(tmp_path)

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert _named_in(answer) == {"grok-6"}
    assert answer["alternatives"] == []


def test_no_exploration_ever_names_a_release_a_newer_one_replaced(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The rule narrows the pool the exploration draws its candidates from.

    An exploration buys a row about a point somebody might run again, and a
    row about a replaced release is a row nothing will ever read.
    """

    _three_releases(tmp_path)

    answers = [
        _answer(
            capsys,
            f"--data={tmp_path}",
            "--harness=claude-code",
            "--kind=implement",
            EVERY,
            f"--seed={seed}",
        )
        for seed in range(DRAWS)
    ]

    assert {model for answer in answers for model in _named_in(answer)} == {"grok-6"}


def test_a_step_up_after_a_failure_never_names_a_release_a_newer_one_replaced(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The escalation is answered from the same pool, so it holds one release."""

    _three_releases(tmp_path)

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--kind=implement",
        "--after=grok-6@low",
        EVERY,
    )

    assert _named_in(answer) == {"grok-6"}


def test_where_the_newest_release_has_no_way_in_the_next_one_stands_for_the_family(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The comparison is made among the releases this call could actually use.

    `gateways` is a per-model field, so a release the gateway its channel pays
    through records no slug for has no route and never entered the pool. Held
    against it, the family would vanish rather than be represented.
    """

    _grok(
        tmp_path,
        _release("grok-5", "2026-02-01"),
        _release("grok-6", "2026-08-01", gateways={}),
    )

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert answer["model"] == "grok-5"
    assert _named_in(answer) == {"grok-5"}


def test_where_the_newest_release_is_above_the_ceiling_the_family_still_stands(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The ceiling is one of the gates the comparison is made among.

    A release supporting no level at or below the ceiling is not one this call
    could use, and a pool holding only that family would be emptied by a rule
    applied before the ceiling rather than after it.
    """

    _grok(tmp_path, _release("grok-7", "2026-08-01", levels=("max",)))

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert answer["model"] == SEEDED_GROK
    assert answer["launch"]["how"] != "inherit"


def test_a_dated_release_beats_an_undated_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Most seeded entries carry no date, so the undated case is the common one."""

    _grok(tmp_path, _release("grok-5", "2026-02-01"))

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert _named_in(answer) == {"grok-5"}


def test_two_releases_dated_the_same_day_resolve_to_the_smaller_id(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A tie is settled on the id as the catalogue spells it, and lexically.

    Lexically rather than numerically, because a numeric reading would be this
    module inferring a succession the catalogue never stated.
    """

    _grok(
        tmp_path,
        _release("grok-7.0", "2026-05-01"),
        _release("grok-7.1", "2026-05-01"),
    )

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert _named_in(answer) == {"grok-7.0"}


def test_the_release_chosen_never_depends_on_the_order_the_catalogue_was_read_in(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Two fields decide it, so the same catalogue in either order decides alike."""

    first = _release("grok-7.0", "2026-05-01")
    second = _release("grok-7.1", "2026-05-01")
    ascending, descending = tmp_path / "ascending", tmp_path / "descending"
    _grok(ascending, first, second)
    _grok(descending, second, first)

    answer = _answer(capsys, f"--data={ascending}", *GROK_ASKED)
    reversed_answer = _answer(capsys, f"--data={descending}", *GROK_ASKED)

    assert _named_in(answer) == _named_in(reversed_answer) == {"grok-7.0"}


def test_a_family_alias_and_an_unlocked_call_name_the_same_release_on_a_tie(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """One order decides which release is newest, so the two can never disagree.

    A lock resolving a family alias one way and the pool keeping the other
    release is a user asking for `grok` and being told the newest Grok is one
    the same catalogue would not have offered them.
    """

    _grok(
        tmp_path,
        _release("grok-7.0", "2026-05-01"),
        _release("grok-7.1", "2026-05-01"),
    )

    unlocked = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)
    aliased = _answer(capsys, f"--data={tmp_path}", "--model=grok", *GROK_ASKED)

    assert unlocked["model"] == aliased["model"] == "grok-7.0"
    assert _named_in(unlocked) == {"grok-7.0"}
    assert "newest" in aliased["note"]


def test_models_of_different_families_are_untouched_by_one_another(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A family is what the catalogue says it is, whatever two ids have in common.

    `gpt-5.6-sol` and `gpt-6-astra` share a maker and most of a name and are
    two version lines, so neither replaces the other and both stay.
    """

    _profile(
        tmp_path,
        harnesses=["codex"],
        makers=["openai"],
        channels=[
            {
                "provider": "openai",
                "harness": "codex",
                "pay": "subscription",
                "plan": "ChatGPT Pro",
            }
        ],
    )

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=codex",
        "--scope=limited",
        "--kind=implement",
        "--stakes=high",
        EVERY,
    )

    assert _named_in(answer) == OPENAI


def test_an_exact_id_lock_on_a_replaced_release_is_answered_with_that_release(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A lock is never overridden, and the rule runs after it rather than before.

    Every gate admitted this release, so the answer says nothing about the
    lock and nothing about a scope that did not offer the model.
    """

    _three_releases(tmp_path)

    answer = _answer(
        capsys, f"--data={tmp_path}", f"--model={SEEDED_GROK}", *GROK_ASKED
    )

    assert answer["model"] == SEEDED_GROK
    note = answer["note"] or ""
    assert "lock" not in note
    assert "did not offer" not in note


def test_no_note_composed_from_the_pool_names_a_release_the_rule_removed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The unceiled pool the ceiling is measured against is narrowed too.

    `_ceiling_ruled_out` names the point at the top of that pool, so a pool
    left holding the replaced release tells a caller the ceiling cost it a
    point it could never have been offered in the first place.
    """

    _grok(
        tmp_path,
        _release("grok-old", "2026-01-01", levels=("low", "xhigh", "max")),
        _release("grok-new", "2026-08-01", levels=("low", "xhigh")),
    )
    _store(tmp_path, ("implement", "grok-old", "max", 1.0, 30))

    answer = _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert answer["model"] == "grok-new"
    assert "grok-old" not in (answer["note"] or "")


def test_a_failed_point_a_newer_release_replaced_is_answered_as_any_unknown_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """No step is invented for a release the pool does not hold.

    The caller's own token is echoed back, which is the caller's word rather
    than a point this Skill composed from the pool.
    """

    _three_releases(tmp_path)

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--kind=implement",
        f"--after={SEEDED_GROK}@low",
        EVERY,
    )

    assert "nothing here matches the failed point" in answer["note"]
    assert answer["model"] == "grok-6"


def test_the_same_failure_locked_to_that_release_still_steps_up_within_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller wanting the step up from a release it chose says so with a lock."""

    _three_releases(tmp_path)

    answer = _answer(
        capsys,
        f"--data={tmp_path}",
        "--harness=claude-code",
        "--kind=implement",
        f"--model={SEEDED_GROK}",
        f"--after={SEEDED_GROK}@low",
        EVERY,
    )

    assert answer["model"] == SEEDED_GROK
    assert answer["deliberation"] != "low"
    assert "one step up from" in answer["note"]


def test_one_order_decides_which_release_is_newest_and_every_caller_goes_by_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Two opposite tie-breaks for one notion is what this collapses into one.

    The family alias, the pool and the subagent file name all answer *which
    release of this family is the newest*, and a tie is where they used to
    disagree: `resolve` took the smaller id and `definitions` the greater.
    """

    _grok(
        tmp_path,
        _release("grok-7.0", "2026-05-01"),
        _release("grok-7.1", "2026-05-01"),
    )
    catalogue = _module("catalogue")
    launch = _module("launch")
    cat = catalogue.load(tmp_path, SKILL)
    tied = [model for model in cat.models if model.family == "grok"]
    pool = [select.Point(model, "low") for model in tied]

    assert catalogue.newest_first(tied)[0].id == "grok-7.0"
    assert {point.model.id for point in select._newest_releases(pool)} == {"grok-7.0"}
    assert "newest_first" in " ".join((launch.definitions.__doc__ or "").split())


def test_the_rule_removes_nothing_this_machine_has_stored(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A replaced release keeps its entry and its rows; it is simply not chosen.

    Rows are evidence of a version that does not change, and the user may lock
    the release they were taken at for as long as its maker offers it.
    """

    _three_releases(tmp_path)
    _store(tmp_path, ("implement", SEEDED_GROK, "low", 1.0, 30))
    (tmp_path / "pending.jsonl").write_text(
        json.dumps({"attempt_id": "ms-fixture-pending", "model": SEEDED_GROK}) + "\n",
        encoding="utf-8",
    )
    before = {
        path.name: path.read_bytes()
        for path in sorted(tmp_path.iterdir())
        if path.is_file()
    }

    _answer(capsys, f"--data={tmp_path}", *GROK_ASKED)

    assert {
        path.name: path.read_bytes()
        for path in sorted(tmp_path.iterdir())
        if path.is_file()
    } == before
