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

SHARED_GLOBAL = ".agents/skills"
SHARED_PROJECT = ".agents/skills"


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
    capabilities: list[str] | None = None,
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
        ("capabilities", capabilities or []),
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
    capabilities: list[str] | None = None,
    description: str = "A collection skill.",
) -> dict[str, Any]:
    return {
        "name": name,
        "category": category,
        "description": description,
        "binaries": binaries or [],
        "skills": skills or [],
        "externals": externals or [],
        "capabilities": capabilities or [],
    }


def _world(
    tmp_path: Path, entries: list[dict[str, Any]] | None = None
) -> dict[str, Path]:
    """Build an isolated home, project, collection source, and manager.

    The manager sits outside both the home and the project on purpose: where it
    was installed says nothing about which Harnesses are present, and a fixture
    that put it in one of their directories would detect that Harness for free.
    """

    home = tmp_path / "home"
    project = tmp_path / "proj"
    source = tmp_path / "collection"
    here = tmp_path / "manager"
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
                capabilities=entry.get("capabilities", []),
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


def _present(world: dict[str, Path], *harness_dirs: str) -> None:
    """Make Harnesses present in the Global layer by creating their homes."""

    for relative in harness_dirs:
        (world["home"] / relative).mkdir(parents=True, exist_ok=True)


def _present_here(world: dict[str, Path], *harness_dirs: str) -> None:
    """Make Harnesses present in the Project layer."""

    for relative in harness_dirs:
        (world["project"] / relative).mkdir(parents=True, exist_ok=True)


def _run(
    world: dict[str, Path], *args: str, cwd: Path | None = None, log: Path | None = None
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["KNTNT_HOME"] = str(world["home"])
    env["KNTNT_SOURCE"] = str(world["source"])
    env["KNTNT_PROJECT"] = str(world["project"])
    env["KNTNT_HARNESS_PATHS"] = str(HARNESS_PATHS)
    env["KNTNT_TRANSPORT"] = f"uv run {FAKE_SKILLS}"
    if log is not None:
        env["KNTNT_TRANSPORT_LOG"] = str(log)
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


def _calls(log: Path) -> list[dict[str, Any]]:
    """Read the transport log written by the fake transport."""

    if not log.is_file():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def _harnesses_reading(template: str, *, global_layer: bool) -> set[str]:
    """Return every harness id whose layer directory is *template*."""

    table = json.loads(HARNESS_PATHS.read_text(encoding="utf-8"))
    key = "global" if global_layer else "project"
    return {harness for harness, spec in table.items() if spec.get(key) == template}


def test_status_lists_catalog_skills_as_disabled(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    skills = _json(result)["skills"]
    assert [skill["name"] for skill in skills] == ["alpha", "beta", "gamma"]
    assert {skill["global"] for skill in skills} == {"disabled"}
    assert {skill["project"] for skill in skills} == {"disabled"}


def test_status_groups_category_on_each_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)

    payload = _json(_run(world, "status"))

    by_name = {skill["name"]: skill["category"] for skill in payload["skills"]}
    assert by_name == {"alpha": "code", "beta": "code", "gamma": "text"}


def test_status_reports_the_directories_it_acted_on(tmp_path: Path) -> None:
    """Targeting is no longer a choice, so the report names places, not a list."""

    world = _world(tmp_path)
    _present(world, ".claude")
    _present_here(world, ".claude")

    payload = _json(_run(world, "status"))

    assert payload["directories"]["global"] == [
        str(world["home"] / ".claude" / "skills")
    ]
    assert payload["directories"]["project"] == [
        str(world["project"] / ".claude" / "skills")
    ]
    assert "harness_list" not in payload
    assert "harnesses" not in payload


def test_the_manager_has_no_setup_verb(tmp_path: Path) -> None:
    world = _world(tmp_path)

    plan = _run(world, "plan", "setup")
    apply = _run(world, "apply", "setup", "--harness", "claude-code", "--yes")

    assert plan.returncode != 0
    assert apply.returncode != 0
    assert "setup" not in _run(world, "help").stdout


def test_no_command_asks_for_setup_when_nothing_is_detected(tmp_path: Path) -> None:
    """The failure state went with the concept: there is nothing left to record."""

    world = _world(tmp_path)

    for args in (
        ("plan", "enable", "alpha"),
        ("plan", "disable", "alpha"),
        ("plan", "update"),
        ("status",),
    ):
        result = _run(world, *args)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "setup" not in result.stderr.lower()


def test_global_enable_places_the_skill_in_every_detected_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, ".claude", ".config/opencode")

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()
    status = _json(_run(world, "status", "alpha"))
    assert status["skills"][0]["global"] == "enabled"


def test_global_enable_with_nothing_detected_writes_only_the_shared_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / SHARED_GLOBAL / "alpha" / "SKILL.md").is_file()
    assert sorted(child.name for child in world["home"].iterdir()) == [".agents"]


def test_project_enable_places_the_skill_in_every_detected_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present_here(world, ".claude", ".crush")

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()
    assert (world["project"] / ".crush" / "skills" / "gamma" / "SKILL.md").is_file()


def test_project_enable_with_nothing_detected_writes_only_the_shared_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / SHARED_PROJECT / "gamma" / "SKILL.md").is_file()
    assert sorted(child.name for child in world["project"].iterdir()) == [".agents"]


def test_project_detection_ignores_an_ordinary_skills_directory(
    tmp_path: Path,
) -> None:
    """`skills/` and `data/` are things a repository has for its own reasons."""

    world = _world(tmp_path)
    _present_here(world, "skills", "data")

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / "skills" / "gamma").exists()
    assert not (world["project"] / "data" / "skills").exists()
    assert (world["project"] / SHARED_PROJECT / "gamma" / "SKILL.md").is_file()


def test_a_harness_installed_later_is_acted_on_by_the_next_update(
    tmp_path: Path,
) -> None:
    """A recorded list would go stale here; a resolved one repairs itself."""

    world = _world(tmp_path)
    _present(world, ".claude")
    _run(world, "apply", "enable", "alpha")
    _present(world, ".config/opencode")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()


def test_every_transport_call_names_the_full_detected_set(tmp_path: Path) -> None:
    """Naming a subset is what lets the transport strand a shared directory."""

    world = _world(tmp_path)
    _present(world, ".agents")
    log = tmp_path / "transport.jsonl"

    result = _run(world, "apply", "enable", "alpha", log=log)

    assert result.returncode == 0, result.stderr
    expected = _harnesses_reading("~/.agents/skills", global_layer=True)
    assert len(expected) > 1
    assert set(_calls(log)[0]["agents"]) == expected


def test_disable_removes_the_skill_from_every_detected_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, ".claude", ".config/opencode")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()
    assert not (world["home"] / ".config" / "opencode" / "skills" / "alpha").exists()


def test_status_sees_opencode_skill_in_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, ".config/opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha"))

    status = _json(_run(world, "status", "alpha"))

    assert status["skills"][0]["global"] == "enabled"


def test_help_reads_opencode_skill_from_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, ".config/opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(
        dest / "SKILL.md",
        _skill_md("alpha", help_body="Canonical help."),
    )

    result = _run(world, "help", "alpha")

    assert result.returncode == 0, result.stderr
    assert "Canonical help." in result.stdout


def test_plan_enable_without_names_prints_a_picker(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")

    result = _run(world, "plan", "enable")

    assert result.returncode == 2
    payload = _json(result)
    assert payload["action"] == "pick"
    assert payload["layer"] == "global"
    assert "alpha" in [skill["name"] for skill in payload["categories"]["code"]]


def test_apply_enable_is_idempotent(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
    first = _run(world, "apply", "enable", "alpha")
    second = _run(world, "apply", "enable", "alpha")

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert _json(second)["changed"] == []


def test_apply_enable_refuses_the_manager(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")

    result = _run(world, "apply", "enable", "kntnt")

    assert result.returncode == 1
    assert "manager" in result.stderr.lower()


def test_apply_enable_refuses_an_unknown_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")

    result = _run(world, "apply", "enable", "nope")

    assert result.returncode == 1
    assert "nope" in result.stderr


def test_apply_enable_project_writes_only_the_project_layer(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
    _present_here(world, ".claude")

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    status = _json(_run(world, "status", "gamma"))
    assert status["skills"][0]["global"] == "disabled"
    assert status["skills"][0]["project"] == "enabled"


def test_disable_project_is_noop_when_skill_is_only_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
    _present_here(world, ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "--project", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    payload = _json(result)
    assert payload["changed"] == []
    assert payload["noop"] == ["alpha"]


def test_project_off_targets_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
    _present_here(world, ".claude")

    result = _run(world, "apply", "enable", "--project=off", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert not (world["project"] / ".claude" / "skills" / "alpha").exists()


def test_update_reports_new_catalog_entries_and_leaves_them_disabled(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
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
    _present(world, ".claude")
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
    _present(world, ".claude")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "beta")
    beta = world["home"] / ".claude" / "skills" / "beta"

    result = _run(world, "check", "--here", str(beta))

    assert result.returncode == 0, result.stderr
    assert _json(result)["ok"] is True


def test_check_hands_a_required_capability_to_the_agent(tmp_path: Path) -> None:
    """No script can test a Capability, so `check` reports it instead of judging it."""

    world = _world(tmp_path)
    skill = world["project"] / "skill"
    _write(skill / "SKILL.md", _skill_md("alpha", capabilities=["subagents"]))

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["ok"] is True
    assert payload["unsatisfied"] == []
    note = payload["capabilities"][0]
    assert note["name"] == "subagents"
    assert note["confirm"] and note["how"]


def test_check_reports_capabilities_alongside_an_unsatisfied_binary(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    skill = world["project"] / "skill"
    _write(
        skill / "SKILL.md",
        _skill_md(
            "alpha",
            binaries=["definitely-not-a-binary-kntnt"],
            capabilities=["subagents"],
        ),
    )

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 2
    payload = _json(result)
    assert payload["unsatisfied"][0]["kind"] == "binary"
    assert payload["capabilities"][0]["name"] == "subagents"


def test_check_rejects_an_unknown_capability(tmp_path: Path) -> None:
    """A misspelt Capability must refuse, not pass as a check that never runs."""

    world = _world(tmp_path)
    skill = world["project"] / "skill"
    _write(skill / "SKILL.md", _skill_md("alpha", capabilities=["telepathy"]))

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 1
    assert "telepathy" in result.stderr


def test_capabilities_do_not_gate_where_a_skill_is_installed(tmp_path: Path) -> None:
    """ADR-0030: one desired set; the skill is Enabled everywhere and refuses at runtime."""

    world = _world(
        tmp_path,
        [_entry("alpha", "agents", capabilities=["subagents"])],
    )
    _present(world, ".claude", ".config/opencode")

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert _json(result)["changed"] == ["alpha"]
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()


def test_status_names_the_capabilities_a_skill_needs(tmp_path: Path) -> None:
    world = _world(tmp_path, [_entry("alpha", "agents", capabilities=["subagents"])])

    result = _run(world, "status", "alpha")

    assert result.returncode == 0, result.stderr
    assert _json(result)["skills"][0]["capabilities"] == ["subagents"]


def test_update_reports_capabilities_per_skill(tmp_path: Path) -> None:
    world = _world(tmp_path, [_entry("alpha", "agents", capabilities=["subagents"])])
    _present(world, ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    capabilities = _json(result)["capabilities"]
    assert [item["skill"] for item in capabilities] == ["alpha"]
    assert capabilities[0]["name"] == "subagents"


def test_help_prints_manager_help(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "help")

    assert result.returncode == 0, result.stderr
    assert "enable" in result.stdout
    assert "disable" in result.stdout


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
    _present(world, ".claude")
    _present_here(world, ".claude")
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
    _present_here(world, ".claude")
    _run(world, "apply", "enable", "--project", "alpha")

    result = _run(world, "apply", "update", "--project")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / ".claude" / "skills" / "kntnt").exists()
    assert _json(result)["refreshed"] == ["alpha"]


def test_update_reports_removed_catalog_entries(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
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
    """The transport writes to the detected Harnesses, not necessarily to $HERE.

    Nothing says the Manager being run is installed in a directory this
    invocation targets, so the Catalog it reads has to be refreshed directly or
    Status goes on reporting the snapshot it shipped with.
    """

    world = _world(tmp_path)
    _present(world, ".config/opencode")

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
    _present(world, ".claude")
    _run(world, "apply", "enable", "alpha")

    sidecar = world["source"] / "skills" / "code" / "alpha" / "notes.md"
    _write(sidecar, "revised\n")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    installed = world["home"] / ".claude" / "skills" / "alpha" / "notes.md"
    assert installed.read_text(encoding="utf-8") == "revised\n"


def test_apply_disable_refuses_without_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_every_verb_accepts_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, ".claude")

    for args in (
        ("status", "--yes"),
        ("help", "--yes"),
        ("plan", "enable", "alpha", "--yes"),
        ("plan", "disable", "alpha", "--yes"),
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


def test_shipped_catalog_matches_the_generated_one() -> None:
    """The Catalog is generated; a hand-edited one would drift from the skills."""

    result = subprocess.run(
        ["uv", "run", str(KNTNT_PY), "catalog"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "KNTNT_SOURCE": str(REPO_ROOT)},
        check=False,
    )
    assert result.returncode == 0, result.stderr
    shipped = (REPO_ROOT / "skills" / "kntnt" / "catalog.json").read_text(
        encoding="utf-8"
    )
    assert json.loads(result.stdout) == json.loads(shipped)


def test_delegation_requires_subagents_and_says_so() -> None:
    """The Claude-only model ladder is gone; the harness requirement is declared."""

    path = REPO_ROOT / "skills" / "agents" / "delegation" / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    assert "capabilities:" in text
    assert "- subagents" in text
    assert "`capabilities`" in text

    mode = (path.parent / "mode.md").read_text(encoding="utf-8")
    assert "haiku" not in mode
    assert "Claude Code" not in mode


def test_catalog_generation_rejects_a_name_that_is_not_the_directory(
    tmp_path: Path,
) -> None:
    """The transport installs by directory, so a Catalog name that differs cannot resolve."""

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "delta" / "SKILL.md",
        _skill_md("epsilon"),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "epsilon" in result.stderr
    assert "delta" in result.stderr


def test_catalog_generation_rejects_an_empty_description(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _skill_md("alpha", description=""),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "description" in result.stderr
    assert "alpha" in result.stderr


def test_catalog_generation_rejects_a_folded_description(tmp_path: Path) -> None:
    """parse_simple_yaml has no block scalars, so a folded description ships as '>'."""

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _skill_md("alpha", description=">"),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "alpha" in result.stderr
