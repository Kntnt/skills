"""Owned cross-Harness integrations shipped by the Collection Library."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, cast

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
LIBRARY: Path = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts"

OWNER = "kntnt.model-selector.capture"
COMMAND = ["uv", "run", "/skills/model-selector/scripts/capture.py", "hook"]


def _load() -> Any:
    """Load the shipped integration module from its installed path."""

    path = LIBRARY / "integrations.py"
    spec = importlib.util.spec_from_file_location("kntnt_integrations", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _settings(root: Path) -> dict[str, Any]:
    loaded = (root / ".claude" / "settings.json").read_text(encoding="utf-8")
    return cast(dict[str, Any], json.loads(loaded))


def _codex_hooks(root: Path) -> dict[str, Any]:
    loaded = (root / ".codex" / "hooks.json").read_text(encoding="utf-8")
    return cast(dict[str, Any], json.loads(loaded))


def test_every_supported_harness_installs_its_own_shape(tmp_path: Path) -> None:
    """Each adapter writes the integration its own Harness actually reads."""

    module = _load()
    for harness in ("claude-code", "codex", "opencode"):
        root = tmp_path / harness
        result = module.install(OWNER, harness, root, COMMAND)
        assert result["status"] == "installed", result
        assert result["harness"] == harness

    assert _settings(tmp_path / "claude-code")["hooks"]["SessionStart"]
    assert _codex_hooks(tmp_path / "codex")["hooks"]["Stop"]
    plugin = tmp_path / "opencode" / ".config" / "opencode" / "plugins"
    assert list(plugin.glob("*.js"))


def test_an_unsupported_harness_reports_an_unsatisfied_capability(
    tmp_path: Path,
) -> None:
    """A Harness whose lifecycle cannot carry the contract is never called healthy."""

    module = _load()
    result = module.install(OWNER, "cursor", tmp_path, COMMAND)

    assert result["status"] == "unsatisfied"
    assert result["capability"]
    assert not any(tmp_path.iterdir())


def test_installation_is_idempotent(tmp_path: Path) -> None:
    """Installing twice converges on the same disk state rather than doubling."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    first = _settings(tmp_path)
    module.install(OWNER, "claude-code", tmp_path, COMMAND)

    assert _settings(tmp_path) == first
    entries = _settings(tmp_path)["hooks"]["SessionStart"]
    assert len(entries) == 1


def test_installation_preserves_an_unrelated_hook(tmp_path: Path) -> None:
    """Another owner's hook is left exactly as it was."""

    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    theirs: dict[str, Any] = {
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command", "command": "their-own-thing"}]}
            ]
        },
        "model": "opus",
    }
    settings.write_text(json.dumps(theirs), encoding="utf-8")

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    after = _settings(tmp_path)

    assert after["model"] == "opus"
    assert theirs["hooks"]["SessionStart"][0] in after["hooks"]["SessionStart"]


def test_removal_takes_only_what_this_owner_installed(tmp_path: Path) -> None:
    """Removal is surgical: unrelated hooks and settings survive it."""

    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    theirs: dict[str, Any] = {
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command", "command": "their-own-thing"}]}
            ]
        },
        "model": "opus",
    }
    settings.write_text(json.dumps(theirs), encoding="utf-8")

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    result = module.remove(OWNER, "claude-code", tmp_path)

    assert result["status"] == "removed"
    after = _settings(tmp_path)
    assert after["model"] == "opus"
    assert after["hooks"]["SessionStart"] == theirs["hooks"]["SessionStart"]


def test_removal_is_idempotent_and_verified_from_disk(tmp_path: Path) -> None:
    """Removing what is not there is a converged state rather than a failure."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    module.remove(OWNER, "claude-code", tmp_path)
    again = module.remove(OWNER, "claude-code", tmp_path)

    assert again["status"] == "removed"
    assert again["entries"] == 0
    assert module.health(OWNER, "claude-code", tmp_path)["status"] == "absent"


def test_removal_reports_a_harness_it_could_not_clear(tmp_path: Path) -> None:
    """Partial external state is reported per Harness, never as a clean removal."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    settings = tmp_path / ".claude" / "settings.json"
    settings.write_text("{not json", encoding="utf-8")

    result = module.remove(OWNER, "claude-code", tmp_path)

    assert result["status"] == "failed"
    assert result["detail"]


def test_health_reports_each_harness_separately(tmp_path: Path) -> None:
    """Health is per Harness, and an uninstalled one is absent rather than broken."""

    module = _load()
    module.install(OWNER, "opencode", tmp_path, COMMAND)

    assert module.health(OWNER, "opencode", tmp_path)["status"] == "healthy"
    assert module.health(OWNER, "codex", tmp_path)["status"] == "absent"
    assert module.health(OWNER, "cursor", tmp_path)["status"] == "unsatisfied"


def test_repair_restores_an_integration_removed_behind_our_back(
    tmp_path: Path,
) -> None:
    """Installing again after external damage converges rather than duplicating."""

    module = _load()
    module.install(OWNER, "codex", tmp_path, COMMAND)
    (tmp_path / ".codex" / "hooks.json").unlink()

    result = module.install(OWNER, "codex", tmp_path, COMMAND)

    assert result["status"] == "installed"
    assert module.health(OWNER, "codex", tmp_path)["status"] == "healthy"


def test_the_owner_is_carried_in_what_is_written(tmp_path: Path) -> None:
    """Every installed entry names its owner, so removal never has to guess."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    written = json.dumps(_settings(tmp_path))

    assert OWNER in written


def test_every_supported_harness_survives_a_whole_lifecycle(tmp_path: Path) -> None:
    """Install, repair, install again, remove, remove again — for each of them."""

    module = _load()
    for harness in ("claude-code", "codex", "opencode"):
        root = tmp_path / harness
        assert module.install(OWNER, harness, root, COMMAND)["status"] == "installed"
        assert module.install(OWNER, harness, root, COMMAND)["status"] == "installed"
        assert module.health(OWNER, harness, root)["status"] == "healthy"

        first = module.remove(OWNER, harness, root)
        second = module.remove(OWNER, harness, root)

        assert first["status"] == "removed", harness
        assert second["status"] == "removed", harness
        assert module.health(OWNER, harness, root)["status"] == "absent", harness


def test_removal_leaves_no_empty_leavings_of_ours(tmp_path: Path) -> None:
    """An event nobody else uses goes with our entry rather than staying empty."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    module.remove(OWNER, "claude-code", tmp_path)

    assert "hooks" not in _settings(tmp_path)
