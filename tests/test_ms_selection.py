"""The decision itself: what is chosen, and what is said when nothing can be."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
SELECT: Path = SCRIPTS / "selection.py"


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
    """The priors are the answer on a machine that has measured nothing yet."""

    seat = ["--harness=claude-code", "--seat=claude-opus-5@xhigh", f"--data={tmp_path}"]

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

    answer = _answer(capsys, f"--data={tmp_path}", "--scope=limited", "--n=3")
    alternatives = {row["model"]: row for row in answer["alternatives"]}

    assert answer["model"] == "claude-sonnet-5"
    assert alternatives["test-unpriced"]["cost_usd"] is None


def test_high_stakes_buys_the_cheapest_point_that_clears_the_floor(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A cheap attempt below the floor is a cheap way of not getting the work done."""

    seat = [f"--data={tmp_path}", "--harness=claude-code", "--seat=claude-opus-5@high"]

    reversible = _answer(capsys, "--kind=mechanical", *seat)
    careful = _answer(capsys, "--kind=mechanical", "--stakes=high", *seat)

    assert reversible["expected"]["p_success"] < 0.8
    assert careful["expected"]["p_success"] >= 0.8
    assert careful["expected"]["cost_usd"] > reversible["expected"]["cost_usd"]


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
