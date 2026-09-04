"""The Manager asking a Skill to take its own Harness integrations away."""

from __future__ import annotations

import importlib.util
import json
import sys
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

# The mirror stand-in: answers `install-integrations` with the same per-Harness
# shape `install()` in the Collection Library's own `integrations.py` reports.
INSTALL_SCRIPT = """#!/usr/bin/env python3
import json, sys
from pathlib import Path

Path(sys.argv[0]).parent.joinpath("ran.json").write_text(json.dumps(sys.argv[1:]))
harnesses = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--harness=")]
json.dump(
    {
        "installed": [
            {"harness": harness, "status": "installed", "entries": 3, "detail": None}
            for harness in harnesses
        ],
        "unsupported": {"count": 0, "supported": ["claude-code", "codex", "opencode"]},
    },
    sys.stdout,
)
"""


def _manager() -> ModuleType:
    """Import the Manager's script as a module."""

    spec = importlib.util.spec_from_file_location("kntnt_teardown", KNTNT_PY)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _skill(
    directory: Path,
    name: str,
    *,
    integrations: str | None,
    script_body: str = TEARDOWN_SCRIPT,
) -> Path:
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
        script.write_text(script_body, encoding="utf-8")
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
    _skill(layer, "brief", integrations=None)

    assert manager.teardown_integrations(["brief"], [layer]) == []


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


# --- The mirror word: an Enabled Skill is asked to install its own (#223) ---


def test_a_skill_that_owns_integrations_is_asked_to_install_them(
    tmp_path: Path,
) -> None:
    """The install runs after the Skill's files have already landed."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    skill = _skill(
        layer,
        "model-selector",
        integrations="scripts/capture.py",
        script_body=INSTALL_SCRIPT,
    )

    reported = manager.install_integrations(
        ["model-selector"], [layer], ["claude-code", "codex"]
    )

    assert reported[0]["name"] == "model-selector"
    assert reported[0]["status"] == "installed"
    assert [entry["harness"] for entry in reported[0]["installed"]] == [
        "claude-code",
        "codex",
    ]
    ran = json.loads((skill / "scripts" / "ran.json").read_text(encoding="utf-8"))
    assert ran == ["install-integrations", "--harness=claude-code", "--harness=codex"]


def test_a_skill_declaring_no_integration_is_never_asked_to_install(
    tmp_path: Path,
) -> None:
    """Most Skills own nothing of the Harness, and nothing is executed for them."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    _skill(layer, "brief", integrations=None)

    assert manager.install_integrations(["brief"], [layer], ["claude-code"]) == []


def test_an_install_that_fails_is_reported_and_never_fatal(tmp_path: Path) -> None:
    """A failed installation is reported per Skill and per Harness, never raised."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    skill = _skill(layer, "model-selector", integrations="scripts/capture.py")
    (skill / "scripts" / "capture.py").write_text(
        "import sys\nsys.exit(3)\n", encoding="utf-8"
    )

    reported = manager.install_integrations(
        ["model-selector"], [layer], ["claude-code"]
    )

    assert reported[0]["status"] == "failed"
    assert reported[0]["name"] == "model-selector"


def test_a_missing_install_script_is_reported_rather_than_executed(
    tmp_path: Path,
) -> None:
    """A declaration pointing nowhere is a fault to say, not a crash."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    skill = _skill(layer, "model-selector", integrations="scripts/capture.py")
    (skill / "scripts" / "capture.py").unlink()

    reported = manager.install_integrations(
        ["model-selector"], [layer], ["claude-code"]
    )

    assert reported[0]["status"] == "failed"


def test_the_install_declaration_may_not_escape_the_skill(tmp_path: Path) -> None:
    """The same rule the removal word is held to, held here too."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    _skill(layer, "model-selector", integrations="../../elsewhere.py")

    reported = manager.install_integrations(
        ["model-selector"], [layer], ["claude-code"]
    )

    assert reported[0]["status"] == "failed"
    assert "outside" in reported[0]["detail"]


def test_installing_twice_asks_the_same_convergent_word_again(tmp_path: Path) -> None:
    """Install, repair, and refresh are the same convergence over what is on
    disk (ADR-0090), so asking an already-installed Skill again is answered."""

    manager = _manager()
    layer = tmp_path / "skills"
    layer.mkdir()
    _skill(
        layer,
        "model-selector",
        integrations="scripts/capture.py",
        script_body=INSTALL_SCRIPT,
    )

    first = manager.install_integrations(["model-selector"], [layer], ["claude-code"])
    second = manager.install_integrations(["model-selector"], [layer], ["claude-code"])

    assert first[0]["status"] == second[0]["status"] == "installed"
