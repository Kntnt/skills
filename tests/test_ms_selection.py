"""The decision itself: what is chosen, and what is said when nothing can be."""

from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SKILL: Path = REPO_ROOT / "skills" / "models" / "model-selector"
SCRIPTS: Path = SKILL / "scripts"
SELECT: Path = SCRIPTS / "selection.py"

# How many draws a distribution is read off. Large enough that a candidate
# winning a tenth of the time is not going to be absent by luck, small enough
# that the whole file still runs in a couple of seconds.
DRAWS: int = 200

# The flags that hold a pool to what a fixture profile enables: the caller's
# own provider, and the Harness that says which provider that is.
LIMITED: tuple[str, ...] = ("--scope=limited", "--harness=claude-code")


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
    """Write a profile that pays for Anthropic work in Claude Code."""

    document: dict[str, Any] = {
        "harnesses": ["claude-code"],
        "providers": ["anthropic"],
        "models": ["claude-sonnet-5", "claude-opus-5"],
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


def _winners(capsys: pytest.CaptureFixture[str], flags: Sequence[str]) -> Counter[str]:
    """Return how often each model wins, one call per seed."""

    return Counter(
        _answer(capsys, *flags, f"--seed={seed}")["model"] for seed in range(DRAWS)
    )


def _mean(data_dir: Path, kind: str, model: str, level: str | None) -> float:
    """Return the posterior mean the shipped estimator holds for one point."""

    evidence = _module("evidence")
    cat = _module("catalogue").load(data_dir, SKILL)
    kinds = evidence.load_kinds(SKILL)
    estimator = evidence.Estimator(evidence.load(data_dir), cat, kinds)
    beheld: float = estimator.p_success(kind, model, level).mean
    return beheld


def test_an_empty_data_directory_still_answers_and_exits_zero(tmp_path: Path) -> None:
    """This runs inside somebody else's turn, so there is no way to say stop."""

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
    assert answer["model"]


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

    answer = _answer(capsys, f"--data={tmp_path}", "--model=gpt-9-imaginary")

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
    _profile(tmp_path, models=["claude-sonnet-5", "claude-sonnet-6"])

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
    """An unpriceable model must not read as a free one and win everything."""

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
    _profile(tmp_path, models=["claude-sonnet-5", "test-unpriced"])

    answers = [
        _answer(
            capsys, f"--data={tmp_path}", "--scope=limited", "--n=3", f"--seed={seed}"
        )
        for seed in range(DRAWS)
    ]

    assert {answer["model"] for answer in answers} == {"claude-sonnet-5"}
    for answer in answers:
        listed = {row["model"]: row for row in answer["alternatives"]}
        assert listed["test-unpriced"]["cost_usd"] is None


def test_high_stakes_buys_the_cheapest_point_that_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A cheap attempt below the floor is a cheap way of not getting the work done.

    The floor is read off the difference between the two requests rather than
    off one answer: high stakes is decided and always clears it, reversible
    work is drawn and regularly does not, and every point a draw took below the
    floor was cheaper than the one the floor bought. That last is the whole of
    what the floor is for, and no single seeded draw states it.
    """

    seat = [f"--data={tmp_path}", "--harness=claude-code", "--seat=claude-opus-5@high"]

    careful = _answer(capsys, "--kind=mechanical", "--stakes=high", *seat)
    drawn = [
        _answer(capsys, "--kind=mechanical", *seat, f"--seed={seed}")
        for seed in range(DRAWS)
    ]
    under = [row for row in drawn if row["expected"]["p_success"] < select.FLOOR]

    assert careful["expected"]["p_success"] >= select.FLOOR
    assert under
    assert all(
        careful["expected"]["cost_usd"] > row["expected"]["cost_usd"] for row in under
    )


def test_a_profile_that_enables_nothing_inherits_the_callers_own_seat(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Where nothing can be chosen the answer is to keep the seat you have."""

    _profile(tmp_path, models=[], providers=[])

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

    answer = _answer(capsys, f"--data={tmp_path}", "--model=haiku", "--scope=all")

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


def test_two_candidates_whose_posteriors_overlap_each_win_a_share_of_the_calls(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A pool ranked on its means answers the same way for ever, and never learns."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-haiku-4-5-20251001"])
    _store(
        tmp_path,
        ("mechanical", "claude-sonnet-5", "low", 1.0, 3),
        ("mechanical", "claude-haiku-4-5-20251001", None, 1.0, 2),
        ("mechanical", "claude-haiku-4-5-20251001", None, 0.0, 1),
    )

    winners = _winners(capsys, LIMITED + (f"--data={tmp_path}", "--kind=mechanical"))

    assert set(winners) == {"claude-sonnet-5", "claude-haiku-4-5-20251001"}
    assert min(winners.values()) >= DRAWS // 10


def test_a_candidate_that_is_confidently_worse_essentially_never_wins(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Nobody defines hopeless; two posteriors that no longer overlap do it."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-haiku-4-5-20251001"])
    _store(
        tmp_path,
        ("implement", "claude-sonnet-5", "high", 1.0, 12),
        ("implement", "claude-haiku-4-5-20251001", None, 0.0, 12),
    )

    winners = _winners(capsys, LIMITED + (f"--data={tmp_path}", "--kind=implement"))

    assert set(winners) == {"claude-sonnet-5"}


def test_a_candidate_nothing_has_measured_still_wins_now_and_then(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """It is the only way a store ever learns that something cheaper sufficed."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-haiku-4-5-20251001"])
    _store(tmp_path, ("mechanical", "claude-sonnet-5", "low", 1.0, 6))

    winners = _winners(capsys, LIMITED + (f"--data={tmp_path}", "--kind=mechanical"))

    assert winners["claude-haiku-4-5-20251001"] > 0


def test_the_same_seed_draws_the_same_answer_twice(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller that has to reproduce a decision says which draw it wants."""

    first = _answer(capsys, f"--data={tmp_path}", "--scope=all", "--seed=11")
    again = _answer(capsys, f"--data={tmp_path}", "--scope=all", "--seed=11")

    assert (first["model"], first["deliberation"]) == (
        again["model"],
        again["deliberation"],
    )


def test_drawing_never_disturbs_the_generator_the_rest_of_the_process_shares(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A routing call inside somebody else's turn reseeds nothing of theirs."""

    before = random.getstate()

    _answer(capsys, f"--data={tmp_path}", "--scope=all", "--seed=3")

    assert random.getstate() == before


def test_high_stakes_is_decided_on_the_means_rather_than_drawn(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Irreversible or unchecked work wants the best estimate, not a wager."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-opus-5"])
    _store(
        tmp_path,
        ("implement", "claude-opus-5", "high", 1.0, 6),
        ("implement", "claude-sonnet-5", "high", 0.5, 6),
    )

    winners = _winners(
        capsys,
        LIMITED + (f"--data={tmp_path}", "--kind=implement", "--stakes=high"),
    )

    assert len(winners) == 1


def test_a_locked_request_is_an_instruction_rather_than_a_distribution(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A user who names a model or a level is not offering one to gamble on."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-opus-5"])

    locked = _winners(capsys, LIMITED + (f"--data={tmp_path}", "--deliberation=high"))

    assert len(locked) == 1


def test_an_escalation_after_a_failure_is_a_step_up_rather_than_a_gamble(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller whose attempt just failed is asking for the step, not a roll."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-opus-5"])

    stepped = _winners(
        capsys,
        LIMITED + (f"--data={tmp_path}", "--after=claude-sonnet-5@low"),
    )

    assert len(stepped) == 1


def test_the_reported_success_rate_is_the_posterior_mean_and_not_the_draw(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The draw is how the choice was made, never a claim about the world."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-haiku-4-5-20251001"])
    _store(
        tmp_path,
        ("mechanical", "claude-sonnet-5", "low", 1.0, 3),
        ("mechanical", "claude-haiku-4-5-20251001", None, 0.5, 4),
    )

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

    for answer in answers:
        assert answer["expected"]["p_success"] == round(
            _mean(tmp_path, "mechanical", answer["model"], answer["deliberation"]), 3
        )


def test_a_draw_that_dissents_from_the_means_names_what_they_would_have_chosen(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A reader seeing a weaker model chosen can tell a sample from an error."""

    _profile(tmp_path, models=["claude-sonnet-5", "claude-haiku-4-5-20251001"])
    _store(
        tmp_path,
        ("mechanical", "claude-sonnet-5", "low", 1.0, 3),
        ("mechanical", "claude-haiku-4-5-20251001", None, 1.0, 2),
        ("mechanical", "claude-haiku-4-5-20251001", None, 0.0, 1),
    )

    flags = LIMITED + (f"--data={tmp_path}", "--kind=mechanical")
    notes = [_answer(capsys, *flags, f"--seed={seed}")["note"] for seed in range(DRAWS)]
    dissented = [note for note in notes if note and "would have chosen" in note]

    assert dissented
    assert all("claude-" in note for note in dissented)
