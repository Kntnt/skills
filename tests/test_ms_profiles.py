"""What the machine can reach, and the fallback that stands in for the answers."""

from __future__ import annotations

import importlib.util
import json
import stat
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
                "tier": None,
                "monthly": 200.0,
                "currency": "USD",
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
    assert profile.channels[0].monthly == 200.0
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


def test_a_channel_is_found_by_provider_and_harness_together(tmp_path: Path) -> None:
    """Who pays depends on where the work runs, not only on whose model it is."""

    profile = profiles.load(_stored(tmp_path, _answers()), CAT)
    opus = catalogue.resolve(CAT, "claude-opus-5")[0]
    astra = catalogue.resolve(CAT, "gpt-6-astra")[0]

    assert profiles.channel_for(profile, opus, "claude-code") is not None
    assert profiles.channel_for(profile, opus, "codex") is None
    assert profiles.channel_for(profile, astra, "claude-code") is None
