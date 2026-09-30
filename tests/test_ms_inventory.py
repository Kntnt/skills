"""The profile inventory reports choices without performing selection."""

from __future__ import annotations

import importlib.util
import json
import os
import socket
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

import pytest

SCRIPTS = (
    Path(__file__).resolve().parent.parent / "skills/models/model-selector/scripts"
)


def _module(stem: str) -> Any:
    """Load the script and its siblings as they are loaded when run locally."""

    if stem in sys.modules:
        return sys.modules[stem]
    spec = importlib.util.spec_from_file_location(stem, SCRIPTS / f"{stem}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[stem] = module
    spec.loader.exec_module(module)
    return module


def _inventory() -> Any:
    """Expose the local reader without importing a selection or launch engine."""

    _module("catalogue")
    _module("profiles")
    return _module("inventory")


def _store(tmp_path: Path, *, families: Any = None) -> tuple[Path, Path]:
    """Store deliberately unordered releases and independent profile choices."""

    here = tmp_path / "skill"
    data = tmp_path / "store"
    (here / "data").mkdir(parents=True)
    data.mkdir()
    models = [
        ("gpt-6-sol", "openai", "Sol", "2026-01-01"),
        ("grok-5", "spacexai", "grok", "2026-09-01"),
        ("gpt-6-luna", "openai", "luna", "2026-02-01"),
        ("claude-opus-5", "anthropic", "opus", "2026-05-01"),
        ("gpt-6.1-sol", "openai", "sol", "2026-09-01"),
        ("claude-sonnet-5", "anthropic", "sonnet", "2026-08-01"),
    ]
    (here / "data/catalogue-seed.json").write_text(
        json.dumps(
            {
                "models": [
                    {
                        "id": identifier,
                        "provider": provider,
                        "family": family,
                        "released": released,
                        "deliberation": ["low", "high"],
                    }
                    for identifier, provider, family, released in models
                ]
            }
        ),
        encoding="utf-8",
    )
    profile = {
        "harnesses": ["codex", "claude-code", "codex"],
        "makers": ["openai", "anthropic"],
        "channels": [],
    }
    if families is not None:
        profile["families"] = families
    (data / "profile.json").write_text(json.dumps(profile), encoding="utf-8")
    return data, here


def test_list_reports_only_selected_harnesses_and_latest_selected_series(
    tmp_path: Path,
) -> None:
    """One row per series excludes old releases, other series and Makers."""

    data, here = _store(tmp_path, families={"openai": ["SOL"], "anthropic": ["sonnet"]})

    assert _inventory().read(data, here) == (
        "Harnesses:\n"
        "  claude-code\n"
        "  codex\n"
        "Models:\n"
        "  Claude:\n"
        "    sonnet: claude-sonnet-5\n"
        "  GPT:\n"
        "    sol: gpt-6.1-sol"
    )


@pytest.mark.parametrize("relocated", [False, True])
def test_script_lists_actual_local_data_at_default_or_relocated_directory(
    tmp_path: Path, relocated: bool
) -> None:
    """The body can run a real reader instead of inferring session choices."""

    data, _ = _store(tmp_path, families={"openai": ["sol"], "anthropic": ["sonnet"]})
    home = tmp_path / "home"
    home.mkdir()
    if not relocated:
        (home / ".kntnt").mkdir()
        data.rename(home / ".kntnt/model-selector")
        data = home / ".kntnt/model-selector"
    env = {**os.environ, "HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1"}

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "inventory.py"),
            *([f"--data={data}"] if relocated else []),
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Harnesses:\n  claude-code\n  codex\nModels:" in result.stdout
    assert "  GPT:\n    sol: gpt-" in result.stdout
    assert "luna" not in result.stdout


@pytest.mark.parametrize(
    "contents",
    [
        None,
        "{broken",
        '{"models": []}',
        '{"harnesses": ["codex"], "makers": ["openai"], "channels": [], "families": 7}',
    ],
)
def test_invalid_profile_lists_no_detected_harness_or_catalogue_models(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, contents: str | None
) -> None:
    """A fallback is a diagnosis, never an inventory somebody selected."""

    data, here = _store(tmp_path)
    (data / "profile.json").unlink()
    if contents is not None:
        (data / "profile.json").write_text(contents, encoding="utf-8")
    _inventory()
    monkeypatch.setattr(
        _module("profiles"), "detect_harnesses", lambda: ["detected-only"]
    )

    result = _inventory().read(data, here)

    assert "No configured models can be listed" in result
    assert "/model-selector setup" in result
    assert "detected-only" not in result
    assert "Harnesses:" not in result
    assert "gpt-" not in result


def test_missing_selected_series_is_reported_without_admitting_other_series(
    tmp_path: Path,
) -> None:
    """A catalogue gap retains the choice and still lists the other selections."""

    data, here = _store(
        tmp_path,
        families={"openai": ["sol", "missing"], "anthropic": ["absent"]},
    )

    assert _inventory().read(data, here) == (
        "Harnesses:\n"
        "  claude-code\n"
        "  codex\n"
        "Models:\n"
        "  Claude:\n"
        "    absent: no catalogue release\n"
        "  GPT:\n"
        "    missing: no catalogue release\n"
        "    sol: gpt-6.1-sol"
    )


@pytest.mark.parametrize(
    ("families", "expected"),
    [
        (None, {"claude-opus-5", "claude-sonnet-5", "gpt-6-luna", "gpt-6.1-sol"}),
        ({"openai": ["sol"]}, {"claude-opus-5", "claude-sonnet-5", "gpt-6.1-sol"}),
    ],
)
def test_legacy_and_explicit_profiles_share_permissions_and_follow_new_releases(
    tmp_path: Path, families: Any, expected: set[str]
) -> None:
    """Omitted choices stay broad, explicit choices stay narrow as releases arrive."""

    data, here = _store(tmp_path, families=families)
    inventory = _inventory()
    original_profile = (data / "profile.json").read_bytes()

    result = inventory.read(data, here)

    assert {
        line.split(": ")[1] for line in result.splitlines() if line.startswith("    ")
    } == expected
    cat = _module("catalogue").load(data, here)
    profile = _module("profiles").load(data, cat)
    assert {
        (model.provider, model.family.lower())
        for model in cat.models
        if _module("profiles").allows(profile, model)
    } == {
        (model.provider, model.family.lower())
        for model in cat.models
        if model.id in expected
    }

    # A later local refresh adds a release without replacing profile choices.
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "models": [
                    {
                        "id": "gpt-next-sol",
                        "provider": "openai",
                        "family": "SOL",
                        "released": "2026-10-01",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    updated = inventory.read(data, here)

    assert "sol: gpt-next-sol" in updated
    assert "gpt-6.1-sol" not in updated
    assert "luna: gpt-6-luna" in updated if families is None else "luna" not in updated
    assert (data / "profile.json").read_bytes() == original_profile


def test_inventory_uses_shared_release_ties_and_displays_unknown_maker_ids(
    tmp_path: Path,
) -> None:
    """Date beats version-looking ids, equal dates use the shared lexical tie."""

    data, here = _store(tmp_path)
    (data / "profile.json").write_text(
        json.dumps(
            {"harnesses": [], "makers": ["testing", "spacexai"], "channels": []}
        ),
        encoding="utf-8",
    )
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "models": [
                    {
                        "id": identifier,
                        "provider": "testing",
                        "family": "series",
                        "released": released,
                    }
                    for identifier, released in [
                        ("test-99", None),
                        ("test-b", "2026-10-01"),
                        ("test-a", "2026-10-01"),
                    ]
                ]
            }
        ),
        encoding="utf-8",
    )

    assert _inventory().read(data, here) == (
        "Harnesses:\nModels:\n  Grok:\n    grok: grok-5\n  testing:\n    series: test-a"
    )


def test_list_reads_only_profile_and_catalogue_and_has_no_effects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Deny process/network boundaries and unrelated reads; retain every file."""

    data, here = _store(tmp_path, families={"openai": ["sol"]})
    inventory = _inventory()
    for name in (
        "objective.json",
        "measurements.jsonl",
        "pending.jsonl",
        "quota.json",
        "refresh.json",
    ):
        (data / name).write_text("must stay unread and unchanged", encoding="utf-8")
    agents = tmp_path / "home/.claude/agents"
    agents.mkdir(parents=True)
    (agents / "model-selector-sol.md").write_text(
        "existing definition", encoding="utf-8"
    )
    before = {
        path: (path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_mode)
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    original_open = Path.open
    permitted = {
        data / name for name in ("profile.json", "catalogue.json", "lifecycle.json")
    }
    permitted.add(here / "data/catalogue-seed.json")

    def read_only(path: Path, mode: str = "r", *args: Any, **kwargs: Any) -> Any:
        """Fail at the filesystem boundary on any unrelated read or write."""

        assert path in permitted, f"unrelated read: {path}"
        assert mode in ("r", "rb"), f"write: {path}"
        return original_open(path, mode, *args, **kwargs)

    def forbidden(*args: Any, **kwargs: Any) -> Any:
        """A local inventory may never start a process or reach the network."""

        pytest.fail("inventory crossed a process, network or selection boundary")

    # Public routing, usage and definition seams stay unused even if loaded.
    for stem in ("evidence", "quota", "launch"):
        _module(stem)
    for stem, name in (
        ("selection", "main"),
        ("launch", "plan"),
        ("launch", "definitions"),
        ("launch", "sync_definitions"),
        ("quota", "accounts"),
        ("evidence", "load"),
    ):
        module = _module(stem)
        monkeypatch.setattr(module, name, forbidden)
    with monkeypatch.context() as effects:
        effects.setattr(Path, "open", read_only)
        effects.setattr(subprocess, "Popen", forbidden)
        effects.setattr(socket.socket, "connect", forbidden)
        effects.setattr(urllib.request, "urlopen", forbidden)
        result = inventory.read(data, here)

    assert "sol: gpt-6.1-sol" in result
    assert {
        path: (path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_mode)
        for path in tmp_path.rglob("*")
        if path.is_file()
    } == before
