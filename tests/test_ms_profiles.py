"""What the machine can reach, and the fallback that stands in for the answers."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
from dataclasses import replace
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
profiles = _module("profiles")

CAT = catalogue.load(Path("/nowhere"), SHIPPED)


def _answers(**overrides: Any) -> dict[str, Any]:
    """Provide one profile in the shape `setup` writes it."""

    document: dict[str, Any] = {
        "harnesses": ["claude-code"],
        "providers": ["anthropic"],
        "models": ["claude-opus-5"],
        "channels": [
            {
                "provider": "anthropic",
                "harness": "claude-code",
                "pay": "subscription",
                "plan": "Claude Max 20x",
                "gateway": None,
            }
        ],
        "answered_at": "2026-09-01T10:00:00Z",
    }
    document.update(overrides)
    return document


def _stored(tmp_path: Path, document: Any) -> Path:
    """Write a profile file, taking a string as the way to write a broken one."""

    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "profile.json"
    path.write_text(
        document if isinstance(document, str) else json.dumps(document),
        encoding="utf-8",
    )
    return tmp_path


def test_detection_probes_the_filesystem_and_nothing_else(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Detection runs inside somebody else's turn, so it only ever looks."""

    (tmp_path / ".claude").mkdir()
    (tmp_path / ".config" / "opencode").mkdir(parents=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

    assert profiles.detect_harnesses() == ["claude-code", "opencode"]


def test_an_absent_profile_falls_back_to_the_whole_catalogue(tmp_path: Path) -> None:
    """A machine nobody has answered for still gets a routable answer."""

    profile = profiles.load(tmp_path, CAT)

    assert profile.source == "fallback"
    assert profile.models == tuple(model.id for model in CAT.models)
    assert profile.channels == ()
    assert profile.problem is not None
    assert "setup" in profile.problem


def test_a_broken_profile_falls_back_rather_than_raising(tmp_path: Path) -> None:
    """The file is hand-editable, so unreadable is a state rather than a crash."""

    for broken in ("{not json", json.dumps(["a", "list"]), json.dumps({"models": 7})):
        data_dir = _stored(tmp_path / f"case-{abs(hash(broken))}", broken)

        profile = profiles.load(data_dir, CAT)

        assert profile.source == "fallback"
        assert profile.problem is not None


def test_one_unreadable_channel_invalidates_the_whole_profile(tmp_path: Path) -> None:
    """A profile is only worth trusting whole; half a payment story is not."""

    data_dir = _stored(
        tmp_path,
        _answers(channels=[{"provider": "anthropic", "harness": "claude-code"}]),
    )

    profile = profiles.load(data_dir, CAT)

    assert profile.source == "fallback"


def test_a_written_profile_reads_back_as_the_answers_it_was_given(
    tmp_path: Path,
) -> None:
    """The round trip is the contract between `setup` and everything else."""

    data_dir = _stored(tmp_path, _answers())

    profile = profiles.load(data_dir, CAT)

    assert profile.source == "file"
    assert profile.problem is None
    assert profile.models == ("claude-opus-5",)
    assert profile.channels[0].plan == "Claude Max 20x"
    assert profile.channels[0].rates is None
    assert profile.answered_at == "2026-09-01T10:00:00Z"


def test_writing_is_atomic_and_readable_only_by_its_owner(tmp_path: Path) -> None:
    """The file names what somebody pays every month."""

    data_dir = tmp_path / "fresh"
    original = profiles.load(_stored(tmp_path / "source", _answers()), CAT)

    profiles.write(data_dir, original)

    written = data_dir / "profile.json"
    assert stat.S_IMODE(written.stat().st_mode) == 0o600
    assert not list(data_dir.glob(".profile-*"))
    assert profiles.load(data_dir, CAT) == original


def test_a_channel_is_found_by_provider_first_and_by_harness_where_it_can(
    tmp_path: Path,
) -> None:
    """Who pays follows the provider; where the work runs only breaks a tie.

    This test once asserted the opposite — that a channel answers for its own
    harness alone — and that is what removed every bridged model from the pool
    the moment somebody answered the interview. A subscription pays for its
    provider whichever harness invokes it.
    """

    profile = profiles.load(_stored(tmp_path, _answers()), CAT)
    opus = catalogue.resolve(CAT, "claude-opus-5")[0]
    astra = catalogue.resolve(CAT, "gpt-6-astra")[0]

    # One channel, for Anthropic, and it pays for Anthropic from either seat.
    assert profiles.channel_for(profile, opus, "claude-code") is not None
    assert profiles.channel_for(profile, opus, "codex") is not None

    # A provider the profile names no channel for is still unpayable.
    assert profiles.channel_for(profile, astra, "claude-code") is None


def test_a_bridged_provider_is_paid_for_by_the_harness_that_reaches_it(
    tmp_path: Path,
) -> None:
    """A channel belongs to the harness the model is reached through.

    A Claude Code session reaches an OpenAI model by running the Codex CLI, and
    it is the Codex subscription that pays for those tokens. Matching a channel
    on the asking harness alone answered None for every bridged model, which
    removed all of them from the pool the moment a profile existed — an
    answered interview leaving the caller worse off than an unanswered one.
    """

    cat = catalogue.load(tmp_path, SHIPPED)
    astra = next(model for model in cat.models if model.id == "gpt-6-astra")
    opus = next(model for model in cat.models if model.id == "claude-opus-5")
    codex = profiles.Channel(
        provider="openai",
        harness="codex",
        pay="subscription",
        plan="ChatGPT Pro 20x",
        gateway=None,
        rates=None,
    )
    direct = profiles.Channel(
        provider="openai",
        harness="claude-code",
        pay="api",
        plan=None,
        gateway=None,
        rates=None,
    )
    profile = profiles.Profile(
        harnesses=("claude-code", "codex"),
        providers=("anthropic", "openai"),
        models=(astra.id, opus.id),
        channels=(codex,),
        answered_at="2026-09-06",
        source="file",
        problem=None,
    )

    # The bridged provider is payable from the seat that runs the bridge.
    assert profiles.channel_for(profile, astra, "claude-code") == codex

    # A provider the profile says nothing about is still unpayable.
    assert profiles.channel_for(profile, opus, "claude-code") is None

    # Where the same provider is reached two ways, the asking harness wins:
    # that is the whole reason a channel names a harness at all.
    both = replace(profile, channels=(codex, direct))
    assert profiles.channel_for(both, astra, "claude-code") == direct
    assert profiles.channel_for(both, astra, "codex") == codex


def test_a_gateway_channel_carries_the_rate_card_the_user_actually_pays(
    tmp_path: Path,
) -> None:
    """A gateway prices differently, and the catalogue holds no gateway rates.

    It holds one list price per model, from the provider's own page. Without
    somewhere for the user's own card to live, a gateway arrangement is either
    recorded at the wrong rates or left out of the profile altogether — and a
    provider left out is a provider never recommended.
    """

    data_dir = _stored(
        tmp_path,
        _answers(
            providers=["anthropic", "spacexai"],
            models=["claude-opus-5", "grok-4.6"],
            harnesses=["claude-code", "opencode"],
            channels=[
                {
                    "provider": "spacexai",
                    "harness": "opencode",
                    "pay": "api",
                    "plan": None,
                    "gateway": "openrouter",
                    "rates": {
                        "input": 0.9915,
                        "cache_read": 0.9915,
                        "cache_write": 0.9915,
                        "output": 6.174,
                        "currency": "USD",
                        "unit": "per_mtok",
                    },
                }
            ],
        ),
    )

    profile = profiles.load(data_dir, CAT)

    assert profile.source == "file"
    rates = profile.channels[0].rates
    assert rates is not None
    assert (rates.input, rates.output) == (0.9915, 6.174)

    # The card survives the round trip, or the answers are lost on the next
    # write of a profile nobody edited.
    profiles.write(tmp_path / "again", profile)
    assert profiles.load(tmp_path / "again", CAT) == profile


def test_a_rate_card_this_skill_cannot_price_from_invalidates_the_profile(
    tmp_path: Path,
) -> None:
    """Silence about a card is worse than the fallback, which says it is one.

    Every figure this Skill compares is USD, nothing converts, and a card in
    another currency would be added to a USD bill without a word. A card that
    is not an object at all is the same failure with less to read.
    """

    for card in ({"input": 9.0, "output": 60.0, "currency": "SEK"}, "nine kronor"):
        data_dir = _stored(
            tmp_path / str(card)[:8],
            _answers(
                channels=[
                    {
                        "provider": "anthropic",
                        "harness": "claude-code",
                        "pay": "api",
                        "plan": None,
                        "gateway": None,
                        "rates": card,
                    }
                ]
            ),
        )

        profile = profiles.load(data_dir, CAT)

        assert profile.source == "fallback"
        assert profile.problem is not None
