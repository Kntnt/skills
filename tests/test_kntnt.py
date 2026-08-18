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

SHARED_SKILLS = ".agents/skills"


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


def _foreign_skill_md(name: str) -> str:
    """A SKILL.md from outside this collection: no `metadata.kntnt` anywhere.

    The marker is the whole of what tells the sweep which directories are this
    collection's. A skill that carries none is another collection's or the
    user's own, and must survive every Update untouched.
    """

    return "\n".join(
        [
            "---",
            f"name: {name}",
            "description: A skill from somewhere else.",
            "---",
            "",
            f"# {name}",
            "",
        ]
    )


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


# The default Catalog with `gamma` withdrawn from it.
_SURVIVORS = [
    _entry("alpha", "code", binaries=["git"], description="The alpha skill."),
    _entry("beta", "code", skills=["alpha"], description="The beta skill."),
]


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

    # The collection ships the Manager's script, so the origin has to carry it:
    # a refresh that placed a `kntnt` with no `scripts/` would be a Manager
    # nothing could invoke, and Uninstall runs from the copy it is deleting.
    (source / "skills" / "kntnt" / "scripts").mkdir(parents=True)
    shutil.copy(KNTNT_PY, source / "skills" / "kntnt" / "scripts" / "kntnt.py")

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


def _present(world: dict[str, Path], root: str, *harness_dirs: str) -> None:
    """Make Harnesses present under *root* by creating the homes they are found by.

    `root` is `home` for the Global layer and `project` for the Project layer.
    """

    for relative in harness_dirs:
        (world[root] / relative).mkdir(parents=True, exist_ok=True)


def _withdraw(
    world: dict[str, Path], name: str, category: str, remaining: list[dict[str, Any]]
) -> None:
    """Withdraw *name* from the collection: out of the Catalog and off the tree.

    Both halves matter. A source that still carried the skill would let a
    refresh of it succeed by accident, which is precisely what the collection
    cannot count on once a skill is gone.
    """

    _write(world["source"] / "skills" / "kntnt" / "catalog.json", _catalog(remaining))
    shutil.rmtree(world["source"] / "skills" / category / name)


def _publish(
    world: dict[str, Path], entry: dict[str, Any], catalog: list[dict[str, Any]]
) -> None:
    """Publish *entry* at the origin: into its Catalog and onto its tree.

    The mirror of `_withdraw`. The stored snapshot beside the Manager is left
    alone, which is the whole point — a skill the origin carries and the
    snapshot does not is what every fetch-first test is about.
    """

    _write(world["source"] / "skills" / "kntnt" / "catalog.json", _catalog(catalog))
    _write(
        world["source"] / "skills" / entry["category"] / entry["name"] / "SKILL.md",
        _skill_md(entry["name"], description=entry["description"]),
    )


def _snapshot_forgets(world: dict[str, Path], remaining: list[dict[str, Any]]) -> None:
    """Refresh the snapshot beside the Manager behind the Manager's back.

    `catalog.json` is a sidecar of the Manager, so any run of the transport
    that re-copies `kntnt` replaces it — including one whose Update then died,
    and including `npx skills update` invoked by hand. This is that state: the
    file no longer names the withdrawn skill, so a diff against it is empty
    forever and the files it should have taken are stranded (issue #20).
    """

    _write(world["here"] / "catalog.json", _catalog(remaining))


def _unreachable_origin(world: dict[str, Path]) -> None:
    """Make the Catalog fetch fail while the collection tree stays usable.

    Standing in for an offline machine without going near the network: the
    origin is there and its skills are still copyable, but its Catalog cannot
    be read. That is the failure the fallback exists for, and it is the one
    shape of it a test can stage deterministically.
    """

    (world["source"] / "skills" / "kntnt" / "catalog.json").unlink()


def _run(
    world: dict[str, Path],
    *args: str,
    cwd: Path | None = None,
    log: Path | None = None,
    skip: list[str] | None = None,
    refuse: list[str] | None = None,
    installed: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["KNTNT_HOME"] = str(world["home"])
    env["KNTNT_SOURCE"] = str(world["source"])
    env["KNTNT_PROJECT"] = str(world["project"])
    env["KNTNT_HARNESS_PATHS"] = str(HARNESS_PATHS)
    env["KNTNT_TRANSPORT"] = f"uv run {FAKE_SKILLS}"
    env["KNTNT_TRANSPORT_PATHS"] = str(HARNESS_PATHS)

    # `installed` runs the copy the transport placed, resolving `$HERE` and the
    # path table off that directory the way a real invocation does. The fixture
    # keeps the Manager outside every Harness otherwise, so only a test that
    # asks for this shape can watch the Manager delete itself.
    if installed is not None:
        env["KNTNT_HERE"] = str(installed)
        del env["KNTNT_HARNESS_PATHS"]
    if log is not None:
        env["KNTNT_TRANSPORT_LOG"] = str(log)
    if skip is not None:
        env["KNTNT_TRANSPORT_SKIP"] = ",".join(skip)
    if refuse is not None:
        env["KNTNT_TRANSPORT_REFUSE"] = ",".join(refuse)
    script = (installed or world["here"]) / "scripts" / "kntnt.py"
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
    assert {skill["state"] for skill in skills} == {"disabled"}


def test_status_reports_global_and_says_nothing_of_the_project(tmp_path: Path) -> None:
    """Bare Status answers one question: what is Enabled in Global."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "--project", "gamma")

    payload = _json(_run(world, "status"))

    assert payload["reports"] == "global"
    by_name = {skill["name"]: skill for skill in payload["skills"]}
    assert by_name["alpha"]["state"] == "enabled"
    assert by_name["gamma"]["state"] == "disabled"
    assert all("source" not in skill for skill in payload["skills"])
    assert "project" not in payload["directories"]


def test_status_project_reports_the_effective_set_and_its_source(
    tmp_path: Path,
) -> None:
    """With the flag the question is what applies here, and where it comes from."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha", "beta")
    _run(world, "apply", "enable", "--project", "alpha", "gamma")

    payload = _json(_run(world, "status", "--project"))

    assert payload["reports"] == "effective"
    by_name = {skill["name"]: skill for skill in payload["skills"]}
    assert set(by_name) == {"alpha", "beta", "gamma"}
    assert by_name["alpha"]["source"] == "both"
    assert by_name["beta"]["source"] == "global"
    assert by_name["gamma"]["source"] == "project"
    assert {skill["state"] for skill in payload["skills"]} == {"enabled"}


def test_status_project_omits_a_skill_disabled_in_both_layers(tmp_path: Path) -> None:
    """A skill that applies nowhere here is no answer to *what applies here*."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha")

    effective = _json(_run(world, "status", "--project"))["skills"]
    global_form = _json(_run(world, "status"))["skills"]

    assert [skill["name"] for skill in effective] == ["alpha"]
    gamma = next(skill for skill in global_form if skill["name"] == "gamma")
    assert gamma["state"] == "disabled"


def test_status_project_off_is_the_bare_form(tmp_path: Path) -> None:
    """The off form of the flag is its absence, as it is for every other verb."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "--project", "gamma")

    assert _json(_run(world, "status", "--project=off")) == _json(_run(world, "status"))


def test_status_named_skills_narrow_either_form(tmp_path: Path) -> None:
    """Naming skills selects rows; it does not change the shape of one."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "--project", "gamma")

    global_form = _json(_run(world, "status", "alpha"))
    effective = _json(_run(world, "status", "--project", "gamma"))

    assert global_form["skills"] == [
        skill
        for skill in _json(_run(world, "status"))["skills"]
        if skill["name"] == "alpha"
    ]
    assert effective["skills"] == [
        skill
        for skill in _json(_run(world, "status", "--project"))["skills"]
        if skill["name"] == "gamma"
    ]


def test_status_groups_category_on_each_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)

    payload = _json(_run(world, "status"))

    by_name = {skill["name"]: skill["category"] for skill in payload["skills"]}
    assert by_name == {"alpha": "code", "beta": "code", "gamma": "text"}


def test_status_reports_the_directories_it_acted_on(tmp_path: Path) -> None:
    """Targeting is no longer a choice, so the report names places, not a list."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")

    payload = _json(_run(world, "status", "--project"))

    assert payload["directories"]["global"] == [
        str(world["home"] / ".claude" / "skills")
    ]
    assert payload["directories"]["project"] == [
        str(world["project"] / ".claude" / "skills")
    ]
    assert "harness_list" not in payload
    assert "harnesses" not in payload


def test_reported_directories_cover_where_a_universal_harness_really_lands(
    tmp_path: Path,
) -> None:
    """The transport writes a universal Harness's Global files to the canonical tree.

    Reporting the documented path alone would name a directory the file never
    landed in, and the user reads this to learn where the work happened.
    """

    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")

    payload = _json(_run(world, "status"))

    assert payload["directories"]["global"] == sorted(
        [
            str(world["home"] / ".agents" / "skills"),
            str(world["home"] / ".config" / "opencode" / "skills"),
        ]
    )


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
        ("status", "--project"),
    ):
        result = _run(world, *args)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "setup" not in result.stderr.lower()


def test_global_enable_places_the_skill_in_every_detected_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/opencode")

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()
    status = _json(_run(world, "status", "alpha"))
    assert status["skills"][0]["state"] == "enabled"


def test_global_enable_with_nothing_detected_writes_only_the_shared_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / SHARED_SKILLS / "alpha" / "SKILL.md").is_file()
    assert sorted(child.name for child in world["home"].iterdir()) == [".agents"]


def test_project_enable_places_the_skill_in_every_detected_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude", ".crush")

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
    assert (world["project"] / SHARED_SKILLS / "gamma" / "SKILL.md").is_file()
    assert sorted(child.name for child in world["project"].iterdir()) == [".agents"]


def test_project_detection_ignores_an_ordinary_skills_directory(
    tmp_path: Path,
) -> None:
    """`skills/` and `data/` are things a repository has for its own reasons."""

    world = _world(tmp_path)
    _present(world, "project", "skills", "data")

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / "skills" / "gamma").exists()
    assert not (world["project"] / "data" / "skills").exists()
    assert (world["project"] / SHARED_SKILLS / "gamma" / "SKILL.md").is_file()


def test_a_harness_installed_later_is_acted_on_by_the_next_update(
    tmp_path: Path,
) -> None:
    """A recorded list would go stale here; a resolved one repairs itself."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _present(world, "home", ".config/opencode")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()


def test_every_transport_call_names_the_full_detected_set(tmp_path: Path) -> None:
    """Naming a subset is what lets the transport strand a shared directory."""

    world = _world(tmp_path)
    _present(world, "home", ".agents")
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
    _present(world, "home", ".claude", ".config/opencode")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()
    assert not (world["home"] / ".config" / "opencode" / "skills" / "alpha").exists()


def test_status_sees_opencode_skill_in_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha"))

    status = _json(_run(world, "status", "alpha"))

    assert status["skills"][0]["state"] == "enabled"


def test_help_reads_opencode_skill_from_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")
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
    _present(world, "home", ".claude")

    result = _run(world, "plan", "enable")

    assert result.returncode == 2
    payload = _json(result)
    assert payload["action"] == "pick"
    assert payload["layer"] == "global"
    assert "alpha" in [skill["name"] for skill in payload["categories"]["code"]]


def test_apply_enable_is_idempotent(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    first = _run(world, "apply", "enable", "alpha")
    second = _run(world, "apply", "enable", "alpha")

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert _json(second)["intended"] == []


def test_apply_enable_refuses_the_manager(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "enable", "kntnt")

    assert result.returncode == 1
    assert "manager" in result.stderr.lower()


def test_apply_enable_refuses_an_unknown_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "enable", "nope")

    assert result.returncode == 1
    assert "nope" in result.stderr


def test_apply_enable_project_writes_only_the_project_layer(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")

    result = _run(world, "apply", "enable", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    assert _json(_run(world, "status", "gamma"))["skills"][0]["state"] == "disabled"
    effective = _json(_run(world, "status", "--project", "gamma"))["skills"][0]
    assert effective["state"] == "enabled"
    assert effective["source"] == "project"


def test_disable_project_is_noop_when_skill_is_only_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "--project", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    payload = _json(result)
    assert payload["intended"] == []
    assert payload["noop"] == ["alpha"]


def test_project_off_targets_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")

    result = _run(world, "apply", "enable", "--project=off", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert not (world["project"] / ".claude" / "skills" / "alpha").exists()


def test_update_reports_new_catalog_entries_and_leaves_them_disabled(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
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
    assert delta["state"] == "disabled"


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
    _present(world, "home", ".claude")
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
    _present(world, "home", ".claude")
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
    _present(world, "home", ".claude", ".config/opencode")

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["alpha"]
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
    _present(world, "home", ".claude")
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


def test_status_reports_without_a_stored_snapshot(tmp_path: Path) -> None:
    """A Manager with no snapshot beside it still reports, and stays without one.

    Status reads the origin, so a missing snapshot costs it nothing. Writing
    one would give a read verb a write side effect and, worse, hand the next
    Update a baseline it never chose: Update tells new entries from withdrawn
    ones by diffing the snapshot it stored against what the origin now carries,
    and a snapshot laid down by Status flattens that diff.
    """

    world = _world(tmp_path)
    (world["here"] / "catalog.json").unlink()

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    names = [skill["name"] for skill in _json(result)["skills"]]
    assert names == ["alpha", "beta", "gamma"]
    assert not (world["here"] / "catalog.json").exists()


def test_status_lists_a_skill_the_origin_added_after_the_snapshot(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(world, delta, [*_SURVIVORS, delta])

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is True
    row = next(skill for skill in payload["skills"] if skill["name"] == "delta")
    assert row["state"] == "disabled"


def test_status_leaves_out_a_skill_the_origin_no_longer_carries(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    names = [skill["name"] for skill in _json(result)["skills"]]
    assert names == ["alpha", "beta"]


def test_status_does_not_place_a_newly_published_skill_on_disk(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(world, delta, [*_SURVIVORS, delta])

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()


def test_enable_accepts_a_name_only_the_origin_carries(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(world, delta, [*_SURVIVORS, delta])

    result = _run(world, "apply", "enable", "delta")

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["delta"]
    assert (world["home"] / ".claude" / "skills" / "delta" / "SKILL.md").is_file()


def test_status_falls_back_to_the_snapshot_when_the_origin_is_unreachable(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _unreachable_origin(world)

    result = _run(world, "status")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is False
    assert [skill["name"] for skill in payload["skills"]] == ["alpha", "beta", "gamma"]


def test_enable_works_from_the_snapshot_when_the_origin_is_unreachable(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _unreachable_origin(world)

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_update_reports_nothing_changed_when_the_origin_is_unreachable(
    tmp_path: Path,
) -> None:
    """An unreachable origin leaves the snapshot alone and claims no discoveries.

    `new` and `removed` are the difference between the stored copy and the
    collection. With no collection to reach there is no difference to state,
    and an empty pair must not be read as *nothing changed upstream*.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _unreachable_origin(world)

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is False
    assert payload["new"] == []
    assert payload["removed"] == []
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_update_calls_nothing_new_when_there_was_no_snapshot(tmp_path: Path) -> None:
    """With no snapshot there is no *before*, so the collection is not all new.

    Status no longer writes the snapshot it fetched, so a Manager can reach
    Update without one. Reporting every skill as a new entry would bury the
    one that matters under every one that does not.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    (world["here"] / "catalog.json").unlink()

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["new"] == []
    stored = json.loads((world["here"] / "catalog.json").read_text(encoding="utf-8"))
    assert [entry["name"] for entry in stored["skills"]] == ["alpha", "beta", "gamma"]


def test_status_guidance_no_longer_sends_the_user_to_update(tmp_path: Path) -> None:
    """Discovery no longer depends on Update, so the skill body must not say it does."""

    text = (REPO_ROOT / "skills" / "kntnt" / "status.md").read_text(encoding="utf-8")

    assert "/kntnt update" not in text
    assert "catalog_refreshed" in text


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
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
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
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "--project", "alpha")

    result = _run(world, "apply", "update", "--project")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / ".claude" / "skills" / "kntnt").exists()
    assert _json(result)["confirmed"] == ["alpha"]


def test_update_says_nothing_of_a_withdrawn_skill_that_is_not_here(
    tmp_path: Path,
) -> None:
    """The sweep reports what it found, and a skill never Enabled here is not there."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _catalog([_entry("alpha", "code", binaries=["git"])]),
    )

    log = tmp_path / "transport.jsonl"

    result = _run(world, "apply", "update", log=log)

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == []
    assert not [call for call in _calls(log) if call["command"] == "remove"]


def test_update_removes_a_withdrawal_the_snapshot_has_already_forgotten(
    tmp_path: Path,
) -> None:
    """The stranded state of issue #20, recovered by one Update.

    The Catalog beside the Manager has already been refreshed past `gamma` and
    the files are still on disk, which is where a diff runs out of memory. The
    marker in `gamma`'s own frontmatter does not.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)
    _snapshot_forgets(world, _SURVIVORS)

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == [{"name": "gamma", "disk": "removed"}]
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()


def test_update_removes_a_withdrawal_with_no_snapshot_to_compare_against(
    tmp_path: Path,
) -> None:
    """No stored Catalog at all is still no obstacle: the marker is on the skill."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)
    (world["here"] / "catalog.json").unlink()

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["new"] == []
    assert payload["removed"] == [{"name": "gamma", "disk": "removed"}]
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()


def test_update_leaves_a_skill_without_the_marker_alone(tmp_path: Path) -> None:
    """An External or the user's own skill is not this collection's to remove."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    foreign = world["home"] / ".claude" / "skills" / "zeta"
    _write(foreign / "SKILL.md", _foreign_skill_md("zeta"))

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == []
    assert (foreign / "SKILL.md").is_file()


def test_update_survives_a_skill_file_it_cannot_read(tmp_path: Path) -> None:
    """The sweep reads files this collection did not write, so one of them may not read.

    A foreign SKILL.md is an untrusted boundary: it can be any bytes at all.
    Letting one raise would take the whole run down with a traceback and no
    report — the failure shape of issue #5, reintroduced from the other end.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    foreign = world["home"] / ".claude" / "skills" / "zeta" / "SKILL.md"
    foreign.parent.mkdir(parents=True, exist_ok=True)
    foreign.write_bytes(b"---\nname: zeta\ndescription: \xff\xfe not utf-8\n---\n")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == []
    assert foreign.is_file()


def test_update_never_sweeps_the_manager(tmp_path: Path) -> None:
    """`kntnt` is no Catalog entry, and the verb must not delete what runs it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "update")
    manager = world["home"] / ".claude" / "skills" / "kntnt"
    assert manager.is_dir(), "the refresh never placed the Manager"

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == []
    assert (manager / "SKILL.md").is_file()


def test_update_sweeps_nothing_when_the_origin_is_unreachable(tmp_path: Path) -> None:
    """Which files to delete is not a question a fallback list gets to answer."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "gamma")
    _snapshot_forgets(world, _SURVIVORS)
    _unreachable_origin(world)

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is False
    assert payload["removed"] == []
    assert (world["home"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()


def test_update_removes_a_skill_the_collection_has_withdrawn(tmp_path: Path) -> None:
    """A skill that has left the repository must leave the disk."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    assert _json(result)["removed"] == [{"name": "gamma", "disk": "removed"}]


def test_update_never_asks_the_transport_for_a_withdrawn_skill(
    tmp_path: Path,
) -> None:
    """The source no longer carries it, so asking for it is what killed the run."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)
    log = tmp_path / "transport.jsonl"

    result = _run(world, "apply", "update", log=log)

    assert result.returncode == 0, result.stderr
    placements = [call for call in _calls(log) if call["command"] == "add"]
    assert placements, "the refresh itself never ran"
    assert all("gamma" not in call["skills"] for call in placements)


def test_update_with_project_withdraws_only_from_the_project(tmp_path: Path) -> None:
    """The Global copy is another layer's business, and this run is not it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "gamma")
    _run(world, "apply", "enable", "--project", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", "--project")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / ".claude" / "skills" / "gamma").exists()
    assert (world["home"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()


def test_update_refreshes_the_rest_when_a_withdrawal_fails(tmp_path: Path) -> None:
    """A transport that refuses one removal does not get to end the run."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)
    _write(world["source"] / "skills" / "code" / "alpha" / "notes.md", "revised\n")

    result = _run(world, "apply", "update", refuse=["gamma"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["removed"] == [
        {
            "name": "gamma",
            "disk": "failed",
            "directories": [str(world["home"] / ".claude" / "skills")],
        }
    ]
    assert "alpha" in payload["confirmed"]
    installed = world["home"] / ".claude" / "skills" / "alpha" / "notes.md"
    assert installed.read_text(encoding="utf-8") == "revised\n"


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
    _present(world, "home", ".config/opencode")

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
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")

    sidecar = world["source"] / "skills" / "code" / "alpha" / "notes.md"
    _write(sidecar, "revised\n")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    installed = world["home"] / ".claude" / "skills" / "alpha" / "notes.md"
    assert installed.read_text(encoding="utf-8") == "revised\n"


def test_apply_disable_refuses_without_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_every_verb_accepts_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    for args in (
        ("status", "--yes"),
        ("help", "--yes"),
        ("plan", "enable", "alpha", "--yes"),
        ("plan", "disable", "alpha", "--yes"),
        ("plan", "update", "--yes"),
        ("plan", "uninstall", "--yes"),
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


def test_catalog_generation_rejects_a_skill_without_the_collection_marker(
    tmp_path: Path,
) -> None:
    """The marker is how Update tells a withdrawal from an External on disk.

    A shipped skill that carried none could never be swept, which is the bug
    of issue #20 reintroduced one skill at a time, so generation is where it
    has to fail.
    """

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _foreign_skill_md("alpha"),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "alpha" in result.stderr
    assert "metadata.kntnt" in result.stderr


def test_enable_confirms_each_placement_against_the_disk(tmp_path: Path) -> None:
    """A clean run says what it did and says the disk was read to know it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "enable", "alpha")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["intended"] == ["alpha"]
    assert payload["confirmed"] == ["alpha"]
    assert payload["failed"] == []


def test_enable_reports_a_placement_the_transport_did_not_make(tmp_path: Path) -> None:
    """A transport that exits zero and writes nothing is not a success."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "enable", "alpha", skip=["alpha"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["intended"] == ["alpha"]
    assert payload["confirmed"] == []
    assert payload["failed"] == [
        {
            "name": "alpha",
            "directories": [str(world["home"] / ".claude" / "skills")],
        }
    ]


def test_enable_project_reports_a_placement_the_transport_did_not_make(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude")

    result = _run(world, "apply", "enable", "--project", "gamma", skip=["gamma"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["confirmed"] == []
    assert payload["failed"][0]["directories"] == [
        str(world["project"] / ".claude" / "skills")
    ]


def test_disable_reports_a_removal_the_transport_did_not_make(tmp_path: Path) -> None:
    """The reported defect: removal claimed, files still there, exit 0."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "disable", "alpha", "--yes", skip=["alpha"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["intended"] == ["alpha"]
    assert payload["confirmed"] == []
    assert payload["failed"] == [
        {
            "name": "alpha",
            "directories": [str(world["home"] / ".claude" / "skills")],
        }
    ]
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_disable_project_reports_a_removal_the_transport_did_not_make(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "--project", "gamma")

    result = _run(
        world, "apply", "disable", "--project", "gamma", "--yes", skip=["gamma"]
    )

    assert result.returncode != 0
    payload = _json(result)
    assert payload["confirmed"] == []
    assert payload["failed"][0]["directories"] == [
        str(world["project"] / ".claude" / "skills")
    ]


def test_a_partly_applied_verb_reports_both_sets_and_still_fails(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "enable", "alpha", "beta", skip=["beta"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["intended"] == ["alpha", "beta"]
    assert payload["confirmed"] == ["alpha"]
    assert [item["name"] for item in payload["failed"]] == ["beta"]
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_a_failed_removal_names_only_the_directory_it_survived_in(
    tmp_path: Path,
) -> None:
    """Where to look is the point, so the Harness that agrees is not named."""

    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "enable", "alpha")
    shutil.rmtree(world["home"] / ".config" / "crush" / "skills" / "alpha")

    result = _run(world, "apply", "disable", "alpha", "--yes", skip=["alpha"])

    assert result.returncode != 0
    assert _json(result)["failed"][0]["directories"] == [
        str(world["home"] / ".claude" / "skills")
    ]


def test_update_reports_a_refresh_that_never_landed(tmp_path: Path) -> None:
    """Update reaches a Harness installed since the last Enable, or says so."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _present(world, "home", ".config/crush")

    result = _run(world, "apply", "update", skip=["alpha"])

    assert result.returncode != 0
    payload = _json(result)
    assert "alpha" in payload["intended"]
    assert [item["name"] for item in payload["failed"]] == ["alpha"]
    assert payload["failed"][0]["directories"] == [
        str(world["home"] / ".config" / "crush" / "skills")
    ]


def test_a_verb_that_changes_nothing_is_clean(tmp_path: Path) -> None:
    """Nothing intended is nothing to verify; an inert transport cannot fail."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")

    result = _run(world, "apply", "enable", "alpha", skip=["alpha"])

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["intended"] == []
    assert payload["confirmed"] == []
    assert payload["failed"] == []
    assert payload["noop"] == ["alpha"]


def test_the_change_verbs_tell_the_user_when_a_change_did_not_take(
    tmp_path: Path,
) -> None:
    """The payload is half of it; the skill body has to show the failure."""

    for name in ("enable.md", "disable.md", "update.md"):
        text = (REPO_ROOT / "skills" / "kntnt" / name).read_text(encoding="utf-8")
        assert "`failed`" in text, name
        assert "`directories`" in text, name


def test_a_failed_removal_names_the_shared_tree_a_universal_harness_reads(
    tmp_path: Path,
) -> None:
    """The installation the defect was found on: shared tree, exit 0.

    The transport clears each Harness's own path and skips the shared one, so
    the report has to name the directory the files are actually left in.
    """

    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")
    _write(
        world["home"] / ".agents" / "skills" / "alpha" / "SKILL.md", _skill_md("alpha")
    )

    result = _run(world, "apply", "disable", "alpha", "--yes", skip=["alpha"])

    assert result.returncode != 0
    assert _json(result)["failed"][0]["directories"] == [
        str(world["home"] / ".agents" / "skills")
    ]


def _install_manager(world: dict[str, Path]) -> None:
    """Put the Manager on disk the way a Global refresh does.

    `kntnt` reaches a Harness through the transport like any other skill, so a
    test with something to uninstall has to have run the verb that places it.
    """

    _run(world, "apply", "update", "--yes")


def test_uninstall_removes_every_enabled_skill_and_the_manager(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "enable", "alpha", "beta")
    _install_manager(world)

    result = _run(world, "apply", "uninstall", "--yes")

    assert result.returncode == 0, result.stderr
    for harness in (".claude", ".config/crush"):
        skills = world["home"] / harness / "skills"
        assert sorted(path.name for path in skills.iterdir()) == []


def test_uninstall_reports_every_name_it_took_off_the_disk(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)

    payload = _json(_run(world, "apply", "uninstall", "--yes"))

    assert payload["intended"] == ["alpha", "kntnt"]
    assert payload["confirmed"] == ["alpha", "kntnt"]
    assert payload["failed"] == []
    assert payload["directories"] == [str(world["home"] / ".claude" / "skills")]


def test_uninstall_removes_the_manager_last(tmp_path: Path) -> None:
    """The Manager is what re-runs the verb when the first pass leaves work."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)
    log = tmp_path / "calls.jsonl"

    _run(world, "apply", "uninstall", "--yes", log=log)

    removals = [call for call in _calls(log) if call["command"] == "remove"]
    assert [call["skills"] for call in removals] == [["alpha"], ["kntnt"]]


def test_uninstall_with_nothing_enabled_still_removes_the_manager(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _install_manager(world)

    payload = _json(_run(world, "apply", "uninstall", "--yes"))

    assert payload["intended"] == ["kntnt"]
    assert payload["confirmed"] == ["kntnt"]
    assert not (world["home"] / ".claude" / "skills" / "kntnt").exists()


def test_uninstall_refuses_without_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)

    result = _run(world, "apply", "uninstall")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha").exists()
    assert (world["home"] / ".claude" / "skills" / "kntnt").exists()


def test_uninstall_leaves_a_project_copy_where_it_is(tmp_path: Path) -> None:
    """A Skill in a working directory travels with that repository."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "enable", "alpha")
    _run(world, "apply", "enable", "--project", "gamma")
    _install_manager(world)

    result = _run(world, "apply", "uninstall", "--yes")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()


def test_uninstall_has_no_project_form(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _install_manager(world)

    for args in (
        ("plan", "uninstall", "--project"),
        ("apply", "uninstall", "--project", "--yes"),
    ):
        result = _run(world, *args)
        assert result.returncode != 0, args
        assert (world["home"] / ".claude" / "skills" / "kntnt").exists()


def test_plan_uninstall_names_what_will_go_and_from_where(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)

    payload = _json(_run(world, "plan", "uninstall"))

    assert payload["action"] == "uninstall"
    assert payload["layer"] == "global"
    assert payload["skills"] == ["alpha", "kntnt"]
    assert payload["directories"] == [str(world["home"] / ".claude" / "skills")]
    assert (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_uninstall_says_whether_the_list_it_worked_from_is_current(
    tmp_path: Path,
) -> None:
    """Nothing is left to re-run afterwards, so a stale list is said aloud."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)
    _unreachable_origin(world)

    plan = _json(_run(world, "plan", "uninstall"))
    apply = _json(_run(world, "apply", "uninstall", "--yes"))

    assert plan["catalog_refreshed"] is False
    assert apply["catalog_refreshed"] is False


def test_uninstall_keeps_the_manager_when_a_skill_is_left_behind(
    tmp_path: Path,
) -> None:
    """The Manager is the only verb that can finish what this run could not."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)

    result = _run(world, "apply", "uninstall", "--yes", skip=["alpha"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["intended"] == ["alpha"]
    assert payload["confirmed"] == []
    assert payload["failed"] == [
        {
            "name": "alpha",
            "directories": [str(world["home"] / ".claude" / "skills")],
        }
    ]
    assert (world["home"] / ".claude" / "skills" / "kntnt" / "SKILL.md").is_file()


def test_uninstall_keeps_the_manager_when_the_transport_refuses_a_name(
    tmp_path: Path,
) -> None:
    """A refusal takes the batch down, so nothing left — nor may the Manager."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha", "beta")
    _install_manager(world)
    log = tmp_path / "calls.jsonl"

    result = _run(world, "apply", "uninstall", "--yes", refuse=["beta"], log=log)

    assert result.returncode != 0
    payload = _json(result)
    assert [item["name"] for item in payload["failed"]] == ["alpha", "beta"]
    assert (world["home"] / ".claude" / "skills" / "kntnt").exists()
    assert ["kntnt"] not in [call["skills"] for call in _calls(log)]


def test_uninstall_survives_deleting_the_manager_it_is_running(tmp_path: Path) -> None:
    """`$HERE` goes with the Manager; the run still has a removal to verify."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "enable", "alpha")
    _install_manager(world)
    installed = world["home"] / ".claude" / "skills" / "kntnt"

    result = _run(world, "apply", "uninstall", "--yes", installed=installed)

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["alpha", "kntnt"]
    assert not installed.exists()


def test_uninstall_tells_the_user_what_it_does_not_touch() -> None:
    """No payload can carry every working directory; the body has to say it."""

    text = (REPO_ROOT / "skills" / "kntnt" / "uninstall.md").read_text(encoding="utf-8")

    assert "`failed`" in text
    assert "`directories`" in text
    assert "Project" in text


def test_help_lists_the_uninstall_verb(tmp_path: Path) -> None:
    """Help is the only place the way out is discovered."""

    world = _world(tmp_path)

    text = _run(world, "help").stdout

    assert "uninstall" in text
