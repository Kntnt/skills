"""CLI behaviour of the kntnt manager."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"
HARNESS_PATHS = REPO_ROOT / "skills" / "kntnt" / "harness-paths.json"
FAKE_SKILLS = REPO_ROOT / "tests" / "support" / "fake_skills.py"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _skill_md(
    name: str,
    *,
    description: str = "A collection skill.",
    binaries: list[str] | None = None,
    skills: list[str] | None = None,
    externals: list[str] | None = None,
    help_body: str = "",
) -> str:
    lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        "disable-model-invocation: true",
        "metadata:",
        "  internal: true",
        "  kntnt:",
    ]
    for key, values in (
        ("binaries", binaries or []),
        ("skills", skills or []),
        ("externals", externals or []),
    ):
        if values:
            lines.append(f"    {key}:")
            lines.extend(f"      - {value}" for value in values)
    lines.extend(["---", "", f"# {name}", ""])
    if help_body:
        lines.extend(["## Help", "", help_body, ""])
    lines.extend(["## Arguments", "", "- none", ""])
    return "\n".join(lines)


def _catalog(entries: list[dict[str, Any]]) -> str:
    return json.dumps({"origin": "Kntnt/skills", "skills": entries}, indent=2) + "\n"


def _entry(
    name: str,
    category: str,
    *,
    binaries: list[str] | None = None,
    skills: list[str] | None = None,
    externals: list[str] | None = None,
    description: str = "A collection skill.",
) -> dict[str, Any]:
    return {
        "name": name,
        "category": category,
        "description": description,
        "binaries": binaries or [],
        "skills": skills or [],
        "externals": externals or [],
    }


def _world(
    tmp_path: Path, entries: list[dict[str, Any]] | None = None
) -> dict[str, Path]:
    home = tmp_path / "home"
    project = tmp_path / "proj"
    source = tmp_path / "collection"
    here = home / ".claude" / "skills" / "kntnt"
    project.mkdir()
    home.mkdir()

    if entries is None:
        entries = [
            _entry("alpha", "code", binaries=["git"], description="The alpha skill."),
            _entry("beta", "code", skills=["alpha"], description="The beta skill."),
            _entry("gamma", "text", description="The gamma skill."),
        ]

    _write(
        source / "skills" / "kntnt" / "SKILL.md",
        _skill_md("kntnt", description="Manager."),
    )
    _write(source / "skills" / "kntnt" / "catalog.json", _catalog(entries))
    shutil.copy(HARNESS_PATHS, source / "skills" / "kntnt" / "harness-paths.json")

    for entry in entries:
        _write(
            source / "skills" / entry["category"] / entry["name"] / "SKILL.md",
            _skill_md(
                entry["name"],
                description=entry["description"],
                binaries=entry["binaries"],
                skills=entry["skills"],
                externals=entry["externals"],
                help_body=f"Help for {entry['name']}.",
            ),
        )

    dest_scripts = here / "scripts"
    dest_scripts.mkdir(parents=True)
    shutil.copy(KNTNT_PY, dest_scripts / "kntnt.py")
    shutil.copy(HARNESS_PATHS, here / "harness-paths.json")
    _write(here / "catalog.json", _catalog(entries))
    _write(here / "SKILL.md", _skill_md("kntnt", description="Manager."))

    return {"home": home, "project": project, "source": source, "here": here}


def _run(
    world: dict[str, Path], *args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["KNTNT_HOME"] = str(world["home"])
    env["KNTNT_SOURCE"] = str(world["source"])
    env["KNTNT_PROJECT"] = str(world["project"])
    env["KNTNT_HARNESS_PATHS"] = str(HARNESS_PATHS)
    env["KNTNT_TRANSPORT"] = f"uv run {FAKE_SKILLS}"
    script = world["here"] / "scripts" / "kntnt.py"
    return subprocess.run(
        ["uv", "run", str(script), *args],
        cwd=cwd or world["project"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _json(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    assert result.stdout, result.stderr
    payload: dict[str, Any] = json.loads(result.stdout)
    return payload


def _setup(world: dict[str, Path], *harnesses: str) -> None:
    args = ["apply", "setup"]
    for harness in harnesses:
        args.extend(["--harness", harness])
    result = _run(world, *args, "--yes")
    assert result.returncode == 0, result.stderr


def test_status_lists_catalog_skills_as_disabled(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["harness_list"] == "unsatisfied"
    names = [skill["name"] for skill in payload["skills"]]
    assert names == ["alpha", "beta", "gamma"]
    assert {skill["global"] for skill in payload["skills"]} == {"disabled"}
    assert {skill["project"] for skill in payload["skills"]} == {"disabled"}


def test_status_groups_category_on_each_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)

    payload = _json(_run(world, "status"))

    by_name = {skill["name"]: skill["category"] for skill in payload["skills"]}
    assert by_name == {"alpha": "code", "beta": "code", "gamma": "text"}


def test_plan_enable_stops_when_harness_list_is_unsatisfied(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "plan", "enable", "alpha")

    assert result.returncode == 2
    assert "setup" in result.stderr.lower()


def test_apply_setup_records_the_harness_list(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(
        world,
        "apply",
        "setup",
        "--harness",
        "claude-code",
        "--harness",
        "opencode",
        "--yes",
    )

    assert result.returncode == 0, result.stderr
    payload = _json(_run(world, "status"))
    assert payload["harness_list"] == "ok"
    assert payload["harnesses"] == ["claude-code", "opencode"]


def test_plan_enable_without_names_prints_a_picker(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    result = _run(world, "plan", "enable")

    assert result.returncode == 2
    payload = _json(result)
    assert payload["action"] == "pick"
    assert payload["layer"] == "global"
    assert "alpha" in [skill["name"] for skill in payload["categories"]["code"]]


def test_apply_enable_installs_on_every_recorded_harness(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code", "opencode")

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()
    status = _json(_run(world, "status", "alpha"))
    assert status["skills"][0]["global"] == "enabled"


def test_status_sees_opencode_skill_in_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha"))

    status = _json(_run(world, "status", "alpha"))

    assert status["skills"][0]["global"] == "enabled"


def test_help_reads_opencode_skill_from_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(
        dest / "SKILL.md",
        _skill_md("alpha", help_body="Canonical help."),
    )

    result = _run(world, "help", "alpha")

    assert result.returncode == 0, result.stderr
    assert "Canonical help." in result.stdout


def test_apply_enable_is_idempotent(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    first = _run(world, "apply", "enable", "alpha")
    second = _run(world, "apply", "enable", "alpha")

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert _json(second)["changed"] == []


def test_apply_enable_refuses_the_manager(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    result = _run(world, "apply", "enable", "kntnt")

    assert result.returncode == 1
    assert "manager" in result.stderr.lower()


def test_apply_enable_refuses_an_unknown_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    result = _run(world, "apply", "enable", "nope")

    assert result.returncode == 1
    assert "nope" in result.stderr


def test_apply_disable_removes_from_every_recorded_harness(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code", "opencode")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()
    assert not (world["home"] / ".config" / "opencode" / "skills" / "alpha").exists()


def test_apply_enable_project_writes_only_the_project_layer(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    status = _json(_run(world, "status", "gamma"))
    assert status["skills"][0]["global"] == "disabled"
    assert status["skills"][0]["project"] == "enabled"


def test_disable_project_is_noop_when_skill_is_only_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "--project", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    payload = _json(result)
    assert payload["changed"] == []
    assert payload["noop"] == ["alpha"]


def test_project_off_targets_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    result = _run(world, "apply", "enable", "--project=off", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert not (world["project"] / ".claude" / "skills" / "alpha").exists()


def test_setup_adding_a_harness_applies_globally_enabled_skills(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")

    result = _run(
        world,
        "apply",
        "setup",
        "--harness",
        "claude-code",
        "--harness",
        "opencode",
        "--yes",
    )

    assert result.returncode == 0, result.stderr
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()


def test_setup_refuses_to_remove_a_harness_without_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code", "opencode")

    result = _run(world, "apply", "setup", "--harness", "claude-code")

    assert result.returncode == 2
    assert "opencode" in result.stderr
    payload = _json(_run(world, "status"))
    assert payload["harnesses"] == ["claude-code", "opencode"]


def test_setup_yes_removes_collection_skills_from_a_dropped_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code", "opencode")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "setup", "--harness", "claude-code", "--yes")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".config" / "opencode" / "skills" / "alpha").exists()
    assert not (world["home"] / ".config" / "opencode" / "skills" / "kntnt").exists()
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_second_setup_with_the_same_harnesses_is_a_noop(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    result = _run(world, "apply", "setup", "--harness", "claude-code", "--yes")

    assert result.returncode == 0, result.stderr
    assert _json(result)["changed"] == []


def test_missing_harness_list_rebuilds_from_collection_skills_on_disk(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code", "opencode")
    _run(world, "apply", "enable", "alpha")
    list_path = world["home"] / ".config" / "kntnt" / "harnesses.json"
    list_path.unlink()

    payload = _json(_run(world, "status"))

    assert payload["harness_list"] == "ok"
    assert payload["harnesses"] == ["claude-code", "opencode"]


def test_harness_with_only_the_manager_does_not_rebuild_the_list(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    manager = world["home"] / ".config" / "opencode" / "skills" / "kntnt"
    manager.mkdir(parents=True)
    _write(manager / "SKILL.md", _skill_md("kntnt"))

    result = _run(world, "plan", "enable", "alpha")

    assert result.returncode == 2
    assert "setup" in result.stderr.lower()


def test_update_reports_new_catalog_entries_and_leaves_them_disabled(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")

    new_entries = [
        _entry("alpha", "code", binaries=["git"]),
        _entry("delta", "code", description="The delta skill."),
    ]
    _write(world["source"] / "skills" / "kntnt" / "catalog.json", _catalog(new_entries))
    _write(
        world["source"] / "skills" / "code" / "delta" / "SKILL.md",
        _skill_md("delta", description="The delta skill."),
    )

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["new"] == ["delta"]
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()
    status = _json(_run(world, "status"))
    names = [skill["name"] for skill in status["skills"]]
    assert "delta" in names
    delta = next(skill for skill in status["skills"] if skill["name"] == "delta")
    assert delta["global"] == "disabled"


def test_check_reports_an_unsatisfied_binary(tmp_path: Path) -> None:
    world = _world(tmp_path)
    skill = world["project"] / "skill"
    _write(
        skill / "SKILL.md",
        _skill_md("alpha", binaries=["definitely-not-a-binary-kntnt"]),
    )

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 2
    payload = _json(result)
    assert payload["ok"] is False
    assert payload["unsatisfied"][0]["name"] == "definitely-not-a-binary-kntnt"
    assert payload["unsatisfied"][0]["kind"] == "binary"


def test_check_reports_an_unsatisfied_collection_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)
    skill = world["home"] / ".claude" / "skills" / "beta"
    _write(skill / "SKILL.md", _skill_md("beta", skills=["alpha"]))

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 2
    payload = _json(result)
    assert payload["unsatisfied"][0]["name"] == "alpha"
    assert payload["unsatisfied"][0]["kind"] == "skill"
    assert "/kntnt enable alpha" in payload["unsatisfied"][0]["how"]


def test_check_is_ok_when_dependencies_are_present(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "beta")
    beta = world["home"] / ".claude" / "skills" / "beta"

    result = _run(world, "check", "--here", str(beta))

    assert result.returncode == 0, result.stderr
    assert _json(result)["ok"] is True


def test_help_prints_manager_help(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "help")

    assert result.returncode == 0, result.stderr
    assert "enable" in result.stdout
    assert "setup" in result.stdout


def test_help_named_skill_prints_that_skills_help(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "help", "alpha")

    assert result.returncode == 0, result.stderr
    assert "Help for alpha." in result.stdout


def test_missing_catalog_is_fetched_from_the_source(tmp_path: Path) -> None:
    world = _world(tmp_path)
    (world["here"] / "catalog.json").unlink()

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    names = [skill["name"] for skill in _json(result)["skills"]]
    assert names == ["alpha", "beta", "gamma"]
    assert (world["here"] / "catalog.json").is_file()


def test_plan_setup_lists_detected_harnesses(tmp_path: Path) -> None:
    world = _world(tmp_path)
    (world["home"] / ".config" / "opencode").mkdir(parents=True)

    result = _run(world, "plan", "setup")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    ids = {item["id"]: item for item in payload["detected"]}
    assert ids["claude-code"]["present"] is True
    assert ids["opencode"]["present"] is True
    assert ids["claude-code"]["selected"] is True


def test_manager_skill_is_user_invoked_and_not_internal() -> None:
    text = (REPO_ROOT / "skills" / "kntnt" / "SKILL.md").read_text(encoding="utf-8")
    assert "disable-model-invocation: true" in text
    assert "internal: true" not in text
    enable = (REPO_ROOT / "skills" / "kntnt" / "enable.md").read_text(encoding="utf-8")
    assert "scripts/kntnt.py" in enable


def test_check_treats_a_global_skill_as_effective_for_a_project_skill(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "--project", "beta")
    beta = world["project"] / ".claude" / "skills" / "beta"

    result = _run(world, "check", "--here", str(beta))

    assert result.returncode == 0, result.stderr
    assert _json(result)["ok"] is True


def test_update_project_does_not_install_the_manager_in_the_project(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "--project", "alpha")

    result = _run(world, "apply", "update", "--project")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / ".claude" / "skills" / "kntnt").exists()
    assert _json(result)["refreshed"] == ["alpha"]


def test_update_reports_removed_catalog_entries(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _catalog([_entry("alpha", "code", binaries=["git"])]),
    )

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == ["beta", "gamma"]


def test_no_arguments_prints_help(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world)

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("kntnt — manage this collection")
    assert result.stdout == _run(world, "help").stdout


def test_help_says_status_lists_every_catalog_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)

    text = _run(world, "help").stdout

    assert "Enabled or not" in text
    assert "check --here" not in text


def test_update_refreshes_the_catalog_of_the_running_manager(tmp_path: Path) -> None:
    """The transport writes to the recorded Harnesses, not necessarily to $HERE.

    Thomas's shape: the Manager runs from ~/.claude/skills while the Harness
    list holds only opencode, so nothing the transport does can refresh the
    Catalog this Manager reads.
    """

    world = _world(tmp_path)
    _setup(world, "opencode")

    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _catalog(
            [
                _entry("alpha", "code", binaries=["git"]),
                _entry("delta", "code", description="The delta skill."),
            ]
        ),
    )

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["catalog_refreshed"] is True
    shipped = json.loads((world["here"] / "catalog.json").read_text(encoding="utf-8"))
    assert [entry["name"] for entry in shipped["skills"]] == ["alpha", "delta"]
    names = [skill["name"] for skill in _json(_run(world, "status"))["skills"]]
    assert names == ["alpha", "delta"]


def test_update_refreshes_a_sidecar_when_skill_md_is_unchanged(tmp_path: Path) -> None:
    """The transport's own `update` skips these; the manager must not rely on it."""

    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")

    sidecar = world["source"] / "skills" / "code" / "alpha" / "notes.md"
    _write(sidecar, "revised\n")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    installed = world["home"] / ".claude" / "skills" / "alpha" / "notes.md"
    assert installed.read_text(encoding="utf-8") == "revised\n"


def test_apply_disable_refuses_without_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_every_verb_accepts_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _setup(world, "claude-code")

    for args in (
        ("status", "--yes"),
        ("help", "--yes"),
        ("plan", "enable", "alpha", "--yes"),
        ("plan", "disable", "alpha", "--yes"),
        ("plan", "setup", "--yes"),
        ("plan", "update", "--yes"),
        ("apply", "enable", "alpha", "--yes"),
        ("apply", "update", "--yes"),
    ):
        result = _run(world, *args)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "unrecognized arguments" not in result.stderr


def test_collection_skills_are_hidden_from_the_transport() -> None:
    for path in (REPO_ROOT / "skills").glob("*/*/SKILL.md"):
        if path.parent.name == "kntnt":
            continue
        text = path.read_text(encoding="utf-8")
        assert "internal: true" in text, path
        assert "check --here" in text, path
        assert "npx skills add Kntnt/skills" in text, path


def test_agents_md_is_model_invoked() -> None:
    text = (REPO_ROOT / "skills" / "agents" / "agents-md" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "disable-model-invocation" not in text
    assert "name: agents-md" in text


def test_generated_catalog_includes_agents_md() -> None:
    result = subprocess.run(
        ["uv", "run", str(KNTNT_PY), "catalog"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "KNTNT_SOURCE": str(REPO_ROOT)},
        check=False,
    )
    assert result.returncode == 0, result.stderr
    catalog = json.loads(result.stdout)
    names = {entry["name"] for entry in catalog["skills"]}
    assert "agents-md" in names
    entry = next(item for item in catalog["skills"] if item["name"] == "agents-md")
    assert entry["category"] == "agents"
