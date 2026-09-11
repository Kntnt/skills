"""What the interview may write down, and what it has to say out loud about it."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"


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
profiles = _module("profiles")
launch = _module("launch")
setup_apply = _module("setup_apply")

OPENROUTER = {
    "input": 0.9915,
    "cache_read": 0.9915,
    "cache_write": 0.9915,
    "output": 6.174,
    "currency": "USD",
    "unit": "per_mtok",
}


def _answers(*channels: dict[str, Any]) -> dict[str, Any]:
    """Provide one profile in the shape the interview assembles it."""

    return {
        "harnesses": ["claude-code", "codex", "opencode"],
        "providers": ["anthropic", "openai", "spacexai"],
        "models": ["claude-opus-5", "gpt-5.6-luna", "grok-4.6"],
        "channels": list(channels),
        "answered_at": "2026-09-06T13:35:00Z",
    }


def _applied(tmp_path: Path, answers: dict[str, Any]) -> dict[str, Any]:
    """Apply one assembled profile into a directory of this test's own."""

    supplied = tmp_path / "profile-in.json"
    supplied.write_text(json.dumps(answers), encoding="utf-8")
    report: dict[str, Any] = setup_apply.apply(
        supplied, tmp_path / "data", tmp_path / "agents"
    )
    return report


def _subscription(**overrides: Any) -> dict[str, Any]:
    """Provide one subscription channel, payable by default."""

    channel: dict[str, Any] = {
        "provider": "anthropic",
        "harness": "claude-code",
        "pay": "subscription",
        "plan": "Claude Max 20x",
        "gateway": None,
        "rates": None,
    }
    channel.update(overrides)
    return channel


def test_a_plan_the_catalogue_markets_is_written_without_comment(
    tmp_path: Path,
) -> None:
    """The whole point of offering the catalogue's names is that they come back."""

    report = _applied(tmp_path, _answers(_subscription()))

    assert report["ok"] is True
    assert report["notes"] == []
    assert profiles.load(tmp_path / "data", catalogue.load(tmp_path, SCRIPTS.parent))


def test_a_plan_that_came_from_nowhere_is_noticed_rather_than_recorded_quietly(
    tmp_path: Path,
) -> None:
    """An interview has to be able to tell that its own vocabulary fell short.

    An answer the user typed because no option fitted arrives indistinguishable
    from one they picked. `Codex Pro 5x` is a real example: it was recorded as
    though it had been chosen, and nothing anywhere said that the list offered
    could not express it.
    """

    report = _applied(tmp_path, _answers(_subscription(plan="Codex Pro 5x")))

    # Noticed, and still written: the user is who knows what they pay, and a
    # catalogue that has fallen behind is not grounds for refusing an answer.
    assert report["ok"] is True
    assert any("Codex Pro 5x" in note for note in report["notes"])
    assert any("update" in note for note in report["notes"])


def test_a_provider_whose_plans_the_catalogue_lacks_draws_no_complaint(
    tmp_path: Path,
) -> None:
    """A list this Skill does not hold is a gap in the catalogue, not a wrong answer."""

    answers = _answers(
        _subscription(provider="spacexai", harness="opencode", plan="SuperGrok Heavy")
    )

    report = _applied(tmp_path, answers)

    assert report["ok"] is True
    assert report["notes"] == []


def test_a_rate_card_the_arithmetic_cannot_read_is_refused_by_name(
    tmp_path: Path,
) -> None:
    """Nothing here converts, so a card in kronor is not a card at all.

    Refused rather than noted: a note would leave the profile written and every
    later answer priced from kronor added to dollars, which is the one failure
    a person cannot see in the output.
    """

    kronor = {"input": 9.0, "output": 60.0, "currency": "SEK", "unit": "per_mtok"}
    answers = _answers(
        _subscription(provider="spacexai", harness="opencode", pay="api", rates=kronor)
    )

    report = _applied(tmp_path, answers)

    assert report["ok"] is False
    assert any("SEK" in problem for problem in report["problems"])
    assert not (tmp_path / "data" / "profile.json").exists()


def test_a_gateway_priced_from_the_provider_s_own_page_is_noticed(
    tmp_path: Path,
) -> None:
    """A gateway prices differently, and the catalogue holds only list prices.

    Recorded without a card, the channel is silently billed at the provider's
    own rates — the arrangement whose ratio was wrong by more than a factor of
    two on this machine, in whatever currency it was read.
    """

    answers = _answers(
        _subscription(
            provider="spacexai",
            harness="opencode",
            pay="api",
            plan=None,
            gateway="openrouter",
        )
    )

    report = _applied(tmp_path, answers)

    assert report["ok"] is True
    assert any("openrouter" in note for note in report["notes"])


def test_the_rate_card_a_gateway_channel_carries_survives_being_written(
    tmp_path: Path,
) -> None:
    """The written profile is the only record of it, so the round trip is the test."""

    answers = _answers(
        _subscription(
            provider="spacexai",
            harness="opencode",
            pay="api",
            plan=None,
            gateway="openrouter",
            rates=OPENROUTER,
        )
    )

    report = _applied(tmp_path, answers)

    assert report["ok"] is True
    assert report["notes"] == []

    stored = json.loads((tmp_path / "data" / "profile.json").read_text("utf-8"))
    assert stored["channels"][0]["rates"] == OPENROUTER


SKILL_DIR: Path = SCRIPTS.parent


def _objective(data: Path, agents: Path, objective: str, capsys: Any) -> dict[str, Any]:
    """Set the standing objective through the writer `objective` hands it to."""

    assert (
        setup_apply.main(
            [f"--data={data}", f"--agents={agents}", f"--objective={objective}"]
        )
        == 0
    )
    report: dict[str, Any] = json.loads(capsys.readouterr().out)
    return report


def test_the_standing_objective_is_written_on_its_own(
    tmp_path: Path, capsys: Any
) -> None:
    """Setting time or cost touches neither the profile nor the agent definitions."""

    data = tmp_path / "data"
    agents = tmp_path / "agents"
    assert _applied(tmp_path, _answers(_subscription()))["ok"] is True
    profile = (data / "profile.json").read_bytes()
    defined = sorted((path.name, path.read_bytes()) for path in agents.iterdir())

    for objective in ("time", "cost"):
        report = _objective(data, agents, objective, capsys)

        assert report["ok"] is True
        assert report["objective"] == objective
        written = json.loads((data / "objective.json").read_text(encoding="utf-8"))
        assert written == {"objective": objective}
        assert (data / "profile.json").read_bytes() == profile
        assert (
            sorted((path.name, path.read_bytes()) for path in agents.iterdir())
            == defined
        )


def test_setting_the_objective_on_a_machine_nobody_interviewed_writes_that_alone(
    tmp_path: Path, capsys: Any
) -> None:
    """No profile is conjured and no agents directory is created by the one answer."""

    data = tmp_path / "data"
    agents = tmp_path / "agents"

    _objective(data, agents, "time", capsys)

    assert [path.name for path in data.iterdir()] == ["objective.json"]
    assert not agents.exists()


def test_an_objective_outside_the_vocabulary_is_refused_by_the_command_line(
    tmp_path: Path,
) -> None:
    """The words are the ones `--objective` already has, and no new one."""

    try:
        setup_apply.main([f"--data={tmp_path}", "--objective=fast"])
    except SystemExit as stopped:
        assert stopped.code == 2
    else:
        raise AssertionError("an objective nobody defined was accepted")
    assert not (tmp_path / "objective.json").exists()


def test_setup_and_update_leave_the_standing_objective_where_it_was(
    tmp_path: Path, capsys: Any
) -> None:
    """The choice survives the interview, the sync, and the adoption of new facts."""

    data = tmp_path / "data"
    agents = tmp_path / "agents"
    _objective(data, agents, "time", capsys)
    held = (data / "objective.json").read_bytes()

    # `setup`: a profile operand written and the definitions synced.
    assert _applied(tmp_path, _answers(_subscription()))["ok"] is True
    assert (data / "objective.json").read_bytes() == held

    # `update`: the facts adopted, then the definitions synced with no operand.
    fetched = tmp_path / "fetched.json"
    fetched.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "provider": "anthropic",
                        "name": "Claude Max 20x",
                        "monthly_usd": 200.0,
                        "source_url": "https://example.test/pricing",
                        "retrieved": "2026-09-11",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    adopted = catalogue.adopt(data, SKILL_DIR, fetched)
    assert adopted["refused"] is None
    assert (data / "catalogue.json").exists()
    assert (data / "objective.json").read_bytes() == held
    assert setup_apply.apply(None, data, agents)["ok"] is True
    assert (data / "objective.json").read_bytes() == held


def test_reset_names_and_removes_the_standing_objective() -> None:
    """The standing choice is an answer the user gave, so `reset` discards it."""

    body = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    section = body.partition("\n## Reset\n")[2].partition("\n## ")[0]
    page = (SKILL_DIR / "help" / "reset.md").read_text(encoding="utf-8")

    assert section.count("objective.json") >= 2, "previewed and removed"
    assert "objective.json" in page
