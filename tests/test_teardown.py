"""The Manager asking a Skill to take its own Harness integrations away."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"

TEARDOWN_SCRIPT = """#!/usr/bin/env python3
import json, sys
from pathlib import Path

Path(sys.argv[0]).parent.joinpath("ran.json").write_text(json.dumps(sys.argv[1:]))
json.dump(
    {"removed": [{"harness": "claude-code", "status": "removed"}]}, sys.stdout
)
"""


def _manager() -> ModuleType:
    """Import the Manager's script as a module."""

    spec = importlib.util.spec_from_file_location("kntnt_manager", KNTNT_PY)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _skill(directory: Path, name: str, *, integrations: str | None) -> Path:
    """Write one installed skill, optionally declaring an owned integration."""

    skill = directory / name
    (skill / "scripts").mkdir(parents=True)
    declared = f'  kntnt.integrations: "{integrations}"\n' if integrations else ""
    (skill / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        "description: A collection skill.\n"
        "metadata:\n"
        '  kntnt.internal: "true"\n'
        f"{declared}"
        "---\n\n"
        f"# {name}\n",
        encoding="utf-8",
    )
    if integrations:
        script = skill / integrations
        script.write_text(TEARDOWN_SCRIPT, encoding="utf-8")
        script.chmod(0o755)
    return skill


def test_a_skill_that_owns_integrations_is_asked_to_remove_them(
    tmp_path: Path,
) -> None:
    """The teardown runs while the Skill's own files are still there to run it."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    skill = _skill(layer, "model-selector", integrations="scripts/capture.py")

    reported = manager.teardown_integrations(["model-selector"], [layer])

    assert reported[0]["name"] == "model-selector"
    assert reported[0]["status"] == "removed"
    ran = json.loads((skill / "scripts" / "ran.json").read_text(encoding="utf-8"))
    assert ran == ["remove-integrations"]


def test_a_skill_declaring_no_integration_is_not_run_at_all(tmp_path: Path) -> None:
    """Most Skills own nothing of the Harness, and nothing is executed for them."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    _skill(layer, "tldr", integrations=None)

    assert manager.teardown_integrations(["tldr"], [layer]) == []


def test_a_teardown_that_fails_is_reported_and_never_fatal(tmp_path: Path) -> None:
    """Partial external state is reported per Skill rather than raised."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    skill = _skill(layer, "model-selector", integrations="scripts/capture.py")
    (skill / "scripts" / "capture.py").write_text(
        "import sys\nsys.exit(3)\n", encoding="utf-8"
    )

    reported = manager.teardown_integrations(["model-selector"], [layer])

    assert reported[0]["status"] == "failed"
    assert reported[0]["name"] == "model-selector"


def test_a_missing_teardown_script_is_reported_rather_than_executed(
    tmp_path: Path,
) -> None:
    """A declaration pointing nowhere is a fault to say, not a crash."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    skill = _skill(layer, "model-selector", integrations="scripts/capture.py")
    (skill / "scripts" / "capture.py").unlink()

    reported = manager.teardown_integrations(["model-selector"], [layer])

    assert reported[0]["status"] == "failed"


def test_the_teardown_declaration_may_not_escape_the_skill(tmp_path: Path) -> None:
    """A path that climbs out of the Skill's own directory is refused."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    _skill(layer, "model-selector", integrations="../../elsewhere.py")

    reported = manager.teardown_integrations(["model-selector"], [layer])

    assert reported[0]["status"] == "failed"
    assert "outside" in reported[0]["detail"]
