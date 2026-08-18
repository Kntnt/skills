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
MANAGER_DIR = REPO_ROOT / "skills" / "kntnt"
FAKE_SKILLS = REPO_ROOT / "tests" / "support" / "fake_skills.py"
UV_CACHE = Path(os.environ.get("UV_CACHE_DIR") or Path.home() / ".cache" / "uv")

SHARED_SKILLS = ".agents/skills"

# Every key a Select row carries, and no other. Pinned as a set because the two
# the design withdrew — a `state` and a `source` — are absences rather than
# values, and an absence is only testable against the whole shape.
_ROW_KEYS = {
    "name",
    "description",
    "capabilities",
    "checked",
    "incomplete",
    "freshness",
    "requires",
    "unsatisfied",
    "locked",
}


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
# A three-deep chain: `delta` needs `beta`, which needs `alpha`. The shape a
# closure has to collapse into one question rather than three (issue #28).
_CHAIN = [
    _entry("alpha", "code", description="The alpha skill."),
    _entry("beta", "code", skills=["alpha"], description="The beta skill."),
    _entry("delta", "code", skills=["beta"], description="The delta skill."),
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
    _ship_manpages(here)
    _ship_manpages(source / "skills" / "kntnt")

    return {"home": home, "project": project, "source": source, "here": here}


def _ship_manpages(manager: Path) -> None:
    """Give *manager* the help files the collection ships beside its script.

    Help is a file the manager prints rather than a string it holds, so a
    fixture without these files is a manager that cannot answer at all.
    """

    shutil.copy(MANAGER_DIR / "help.md", manager / "help.md")
    shutil.copytree(MANAGER_DIR / "help", manager / "help", dirs_exist_ok=True)


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


def _store_snapshot(world: dict[str, Path]) -> None:
    """Store the Catalog the origin now carries as the snapshot beside the Manager.

    The mirror of `_snapshot_forgets`: a Manager whose stored copy is exactly
    what the last Update fetched, which is the state a fallback is read in —
    and the only one in which the snapshot carries Digests at all.
    """

    _write(
        world["here"] / "catalog.json",
        (world["source"] / "skills" / "kntnt" / "catalog.json").read_text(
            encoding="utf-8"
        ),
    )


def _unreachable_origin(world: dict[str, Path]) -> None:
    """Make the Catalog fetch fail while the collection tree stays usable.

    Standing in for an offline machine without going near the network: the
    origin is there and its skills are still copyable, but its Catalog cannot
    be read. That is the failure the fallback exists for, and it is the one
    shape of it a test can stage deterministically.
    """

    (world["source"] / "skills" / "kntnt" / "catalog.json").unlink()


def _env(world: dict[str, Path]) -> dict[str, str]:
    """Build the environment the manager and the transport are both run with.

    The isolated home, project, and collection are what makes a run a test run,
    and the transport reads its own path table from a variable of its own.

    `HOME` is redirected as well as the manager's own variable, because the
    transport resolves the Global layer through it exactly as the real one
    does. A Sandbox redirects that same variable and nothing else would carry
    the redirection to the stand-in (ADR-0042). `uv` keeps its cache where it
    was: it is what runs the stand-in rather than anything the collection
    installs, and a cache under the isolated home would be a change to that
    home that no verb made.
    """

    env = os.environ.copy()
    env["HOME"] = str(world["home"])
    env["UV_CACHE_DIR"] = str(UV_CACHE)
    env["KNTNT_HOME"] = str(world["home"])
    env["KNTNT_SOURCE"] = str(world["source"])
    env["KNTNT_PROJECT"] = str(world["project"])
    env["KNTNT_TRANSPORT_PATHS"] = str(HARNESS_PATHS)
    return env


def _run(
    world: dict[str, Path],
    *args: str,
    cwd: Path | None = None,
    log: Path | None = None,
    skip: list[str] | None = None,
    refuse: list[str] | None = None,
    installed: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    env = _env(world)
    env["KNTNT_HARNESS_PATHS"] = str(HARNESS_PATHS)
    env["KNTNT_TRANSPORT"] = f"uv run {FAKE_SKILLS}"

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


def _transport_add(
    world: dict[str, Path], name: str, *, home: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Add *name* globally through the stand-in transport, as the manager does.

    A test about what `add` does to a directory calls the transport itself
    rather than a verb: which skills a verb hands it is a separate question
    with tests of its own, and one that is going to keep changing. *home*
    redirects the home the transport writes the Global layer into, which is
    what a Sandbox does to it.
    """

    env = _env(world)
    if home is not None:
        env["HOME"] = str(home)

    return subprocess.run(
        [
            "uv",
            "run",
            str(FAKE_SKILLS),
            "add",
            str(world["source"]),
            "--skill",
            name,
            "--agent",
            "claude-code",
            "--global",
            "--yes",
        ],
        cwd=world["project"],
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


def _rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every row of a Select list, the grouping flattened away."""

    return [row for rows in payload["categories"].values() for row in rows]


def _checked(payload: dict[str, Any]) -> dict[str, bool]:
    """Return each row's checkbox by skill name."""

    return {row["name"]: row["checked"] for row in _rows(payload)}


def _row(payload: dict[str, Any], name: str) -> dict[str, Any]:
    """Return the row *name* has in a Select list."""

    return next(row for row in _rows(payload) if row["name"] == name)


def _digested_catalog(world: dict[str, Path]) -> str:
    """Generate a Catalog from the origin's own tree, Digests and all.

    `_entry` writes the shape a hand-authored Catalog has and carries no
    Digest, which is what most of the suite wants: freshness that cannot be
    established is reported as unknown. A test about Deviating needs the real
    generator instead, because only the digest it computes matches the files.
    """

    result = _run(world, "catalog")
    assert result.returncode == 0, result.stderr
    return result.stdout


def _digested_world(
    tmp_path: Path, entries: list[dict[str, Any]] | None = None
) -> dict[str, Path]:
    """Build a world whose origin Catalog carries the Digests the disk is judged by.

    The Digest is what tells a Skill that has moved from one that has not, so a
    test about which Skills a verb refreshes needs the generated Catalog rather
    than the hand-authored one every other fixture is built on.
    """

    world = _world(tmp_path, entries)
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json", _digested_catalog(world)
    )
    return world


def test_select_lists_every_catalog_skill_unchecked(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["action"] == "select"
    assert _checked(payload) == {"alpha": False, "beta": False, "gamma": False}


def test_select_lists_global_and_says_nothing_of_the_project(tmp_path: Path) -> None:
    """Bare Select lists one layer: what is Enabled on this machine."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")
    _run(world, "apply", "select", "--project", "gamma")

    payload = _json(_run(world, "plan", "select"))

    assert payload["layer"] == "global"
    assert _checked(payload) == {"alpha": True, "beta": False, "gamma": False}
    assert payload["directories"] == [str(world["home"] / ".claude" / "skills")]


def test_select_project_lists_the_project_layer_alone(tmp_path: Path) -> None:
    """There is no Effective form: with the flag the list is this Project's."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha", "beta")
    _run(world, "apply", "select", "--project", "gamma")

    payload = _json(_run(world, "plan", "select", "--project"))

    assert payload["layer"] == "project"
    assert _checked(payload) == {"alpha": False, "beta": False, "gamma": True}
    assert payload["directories"] == [str(world["project"] / ".claude" / "skills")]


def test_select_project_marks_a_skill_already_enabled_in_global(
    tmp_path: Path,
) -> None:
    """This layer holds no copy to uncheck, so the row says where the copy is."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")

    payload = _json(_run(world, "plan", "select", "--project"))

    assert _row(payload, "alpha")["checked"] is False
    assert _row(payload, "alpha")["in_global"] is True
    assert _row(payload, "beta")["in_global"] is False


def test_select_carries_no_effective_form_and_no_partial_state(
    tmp_path: Path,
) -> None:
    """A skill is Enabled or Disabled; incompleteness is a fact about the disk."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    payload = _json(_run(world, "plan", "select"))

    assert "reports" not in payload
    assert "effective" not in json.dumps(payload)
    assert "partial" not in json.dumps(payload)
    assert all(set(row) == _ROW_KEYS for row in _rows(payload))


def test_select_project_off_is_the_bare_form(tmp_path: Path) -> None:
    """The off form of the flag is its absence, as it is for every other verb."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")
    _run(world, "apply", "select", "--project", "gamma")

    assert _json(_run(world, "plan", "select", "--project=off")) == _json(
        _run(world, "plan", "select")
    )


def test_plan_select_takes_no_skill_names(tmp_path: Path) -> None:
    """The list is the whole of the plan half; the answer arrives at Apply."""

    world = _world(tmp_path)

    result = _run(world, "plan", "select", "alpha")

    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr


def test_select_groups_the_rows_by_category(tmp_path: Path) -> None:
    """Related skills are read together, so the grouping is the payload's (ADR-0015)."""

    world = _world(tmp_path)

    payload = _json(_run(world, "plan", "select"))

    assert {
        category: [row["name"] for row in rows]
        for category, rows in payload["categories"].items()
    } == {"code": ["alpha", "beta"], "text": ["gamma"]}


def test_select_carries_the_description_of_every_row(tmp_path: Path) -> None:
    """A row is judged on the row: nothing about it is looked up elsewhere."""

    world = _world(tmp_path)

    payload = _json(_run(world, "plan", "select"))

    assert _row(payload, "alpha")["description"] == "The alpha skill."
    assert _row(payload, "gamma")["description"] == "The gamma skill."


def test_select_reports_the_directories_the_layer_covers(tmp_path: Path) -> None:
    """Targeting is no longer a choice, so the list names places, not a list."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")

    payload = _json(_run(world, "plan", "select", "--project"))

    assert payload["directories"] == [str(world["project"] / ".claude" / "skills")]
    assert "harness_list" not in payload
    assert "harnesses" not in payload


def test_select_shows_an_incomplete_skill_checked_and_marks_it(
    tmp_path: Path,
) -> None:
    """Partial is a fact about the disk, never a third thing anyone chose."""

    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "select", "alpha")
    shutil.rmtree(world["home"] / ".config" / "crush" / "skills" / "alpha")

    payload = _json(_run(world, "plan", "select"))

    assert _row(payload, "alpha")["checked"] is True
    assert _row(payload, "alpha")["incomplete"] is True
    assert _row(payload, "beta")["incomplete"] is False


def test_confirming_the_list_repairs_an_incomplete_skill(tmp_path: Path) -> None:
    """The answer did not change, and the disk it describes is made true."""

    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "select", "alpha")
    shutil.rmtree(world["home"] / ".config" / "crush" / "skills" / "alpha")

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["alpha"]
    assert payload["confirmed"] == ["alpha"]
    assert (
        world["home"] / ".config" / "crush" / "skills" / "alpha" / "SKILL.md"
    ).is_file()
    assert _row(_json(_run(world, "plan", "select")), "alpha")["incomplete"] is False


def test_select_reports_a_hand_edited_skill_as_deviating(tmp_path: Path) -> None:
    """The Digest answers the one freshness question honestly (ADR-0041)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _digested_catalog(world),
    )
    _run(world, "apply", "select", "alpha")

    assert _row(_json(_run(world, "plan", "select")), "alpha")["freshness"] == "current"

    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    payload = _json(_run(world, "plan", "select"))

    assert _row(payload, "alpha")["freshness"] == "deviating"
    assert _row(payload, "beta")["freshness"] == "unknown"


def test_confirming_the_list_re_copies_a_deviating_skill(tmp_path: Path) -> None:
    """Which is why the offer says the local changes go with it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _digested_catalog(world),
    )
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    assert _json(result)["placed"] == ["alpha"]
    source = world["source"] / "skills" / "code" / "alpha" / "SKILL.md"
    assert installed.read_bytes() == source.read_bytes()


def test_a_snapshot_list_reports_no_skill_deviating_or_current(
    tmp_path: Path,
) -> None:
    """Those digests describe the collection as of the last Update (ADR-0041)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    catalog = _digested_catalog(world)
    _write(world["source"] / "skills" / "kntnt" / "catalog.json", catalog)
    _run(world, "apply", "select", "alpha")
    _write(world["here"] / "catalog.json", catalog)
    _unreachable_origin(world)

    payload = _json(_run(world, "plan", "select"))

    assert payload["catalog_refreshed"] is False
    assert {row["freshness"] for row in _rows(payload)} == {"unknown"}


def test_a_snapshot_list_re_copies_nothing_on_the_strength_of_it(
    tmp_path: Path,
) -> None:
    """No refresh is offered from a list the collection did not answer with."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    catalog = _digested_catalog(world)
    _write(world["source"] / "skills" / "kntnt" / "catalog.json", catalog)
    _run(world, "apply", "select", "alpha")
    _write(world["here"] / "catalog.json", catalog)
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")
    _unreachable_origin(world)

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    assert _json(result)["placed"] == []
    assert installed.read_text(encoding="utf-8") == "hand edited\n"


def test_select_closes_by_counting_what_the_catalog_no_longer_names(
    tmp_path: Path,
) -> None:
    """A skill of ours the collection has withdrawn is Update's to take off."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    payload = _json(_run(world, "plan", "select"))

    assert payload["withdrawn"] == ["gamma"]
    assert "gamma" not in _checked(payload)


def test_select_counts_no_skill_that_is_not_this_collection_s(
    tmp_path: Path,
) -> None:
    """The marker is the whole of what says a directory was written by us."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["home"] / ".claude" / "skills" / "stranger" / "SKILL.md",
        _foreign_skill_md("stranger"),
    )

    assert _json(_run(world, "plan", "select"))["withdrawn"] == []


def test_one_answer_places_and_removes_in_the_same_run(tmp_path: Path) -> None:
    """Changing several skills is one reply, and one report covers both ways."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "beta", "gamma", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["beta", "gamma"]
    assert payload["removed"] == ["alpha"]
    assert payload["intended"] == ["beta", "gamma", "alpha"]
    assert payload["confirmed"] == ["beta", "gamma", "alpha"]
    assert payload["failed"] == []
    assert _checked(_json(_run(world, "plan", "select"))) == {
        "alpha": False,
        "beta": True,
        "gamma": True,
    }


def test_select_locks_a_row_whose_dependency_is_unchecked(tmp_path: Path) -> None:
    """The structure between Skills is visible before the user answers."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    row = _row(_json(_run(world, "plan", "select")), "beta")

    assert row["requires"] == ["alpha"]
    assert row["unsatisfied"] == ["alpha"]
    assert row["locked"] is True


def test_select_unlocks_a_row_whose_dependency_is_checked(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    row = _row(_json(_run(world, "plan", "select")), "beta")

    assert row["requires"] == ["alpha"]
    assert row["unsatisfied"] == []
    assert row["locked"] is False


def test_select_resolves_a_chain_to_the_whole_closure(tmp_path: Path) -> None:
    """Three levels resolve to one set, so one question can cover all of it."""

    world = _world(tmp_path, _CHAIN)
    _present(world, "home", ".claude")

    row = _row(_json(_run(world, "plan", "select")), "delta")

    assert row["requires"] == ["alpha", "beta"]
    assert row["unsatisfied"] == ["alpha", "beta"]
    assert row["locked"] is True


def test_select_leaves_a_checked_row_unlocked_and_names_what_it_lacks(
    tmp_path: Path,
) -> None:
    """A Dependency missing under a checked skill is a break to report, not a lock."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "beta", "--yes")

    row = _row(_json(_run(world, "plan", "select")), "beta")

    assert row["checked"] is True
    assert row["unsatisfied"] == ["alpha"]
    assert row["locked"] is False


def test_select_project_counts_a_global_dependency_as_satisfied(
    tmp_path: Path,
) -> None:
    """A Project row is judged against what the Harness will load (ADR-0013)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")

    row = _row(_json(_run(world, "plan", "select", "--project")), "beta")

    assert row["unsatisfied"] == []
    assert row["locked"] is False


def test_apply_select_reports_a_dependency_the_answer_leaves_out(
    tmp_path: Path,
) -> None:
    """The answer stands; what it leaves Unsatisfied is reported."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "beta")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["beta"]
    assert payload["unsatisfied"] == {"beta": ["alpha"]}


def test_apply_select_reports_nothing_when_the_answer_carries_the_closure(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "alpha", "beta")

    assert result.returncode == 0, result.stderr
    assert _json(result)["unsatisfied"] == {}


def test_unchecking_a_dependency_is_reported_and_not_blocked(tmp_path: Path) -> None:
    """The user is told what they have broken; they are not overruled."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "beta")

    result = _run(world, "apply", "select", "beta", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["removed"] == ["alpha"]
    assert payload["unsatisfied"] == {"beta": ["alpha"]}
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_apply_select_reads_what_a_dependency_lacks_off_the_disk(
    tmp_path: Path,
) -> None:
    """A Dependency the transport never placed is absent, whatever the answer said."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "alpha", "beta", skip=["alpha"])

    payload = _json(result)
    assert [item["name"] for item in payload["failed"]] == ["alpha"]
    assert payload["unsatisfied"] == {"beta": ["alpha"]}


def test_apply_select_project_counts_a_global_dependency_as_satisfied(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--project", "beta")

    assert result.returncode == 0, result.stderr
    assert _json(result)["unsatisfied"] == {}


def test_a_dependency_cycle_in_the_catalog_does_not_take_the_run_down(
    tmp_path: Path,
) -> None:
    """The Catalog is fetched at every invocation, so a cycle in it is survivable."""

    world = _world(
        tmp_path,
        [
            _entry("alpha", "code", skills=["beta"], description="The alpha skill."),
            _entry("beta", "code", skills=["alpha"], description="The beta skill."),
        ],
    )
    _present(world, "home", ".claude")

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    assert _row(_json(result), "alpha")["requires"] == ["beta"]


def test_select_settles_the_closure_before_anything_is_written(
    tmp_path: Path,
) -> None:
    """One question for the whole closure, asked before the run (issue #28)."""

    text = (REPO_ROOT / "skills" / "kntnt" / "steps" / "select.md").read_text(
        encoding="utf-8"
    )

    assert "`requires`" in text
    assert "`unsatisfied`" in text
    assert "`locked`" in text
    assert "one question" in text
    assert "--yes" in text

    # The closure is resolved before the write and never against the user: a
    # step that re-checked what they unchecked would overrule the answer it
    # was asked to carry out (ADR-0047).
    assert "the user did not just uncheck" in text
    assert "reported, not refused" in text


def test_select_on_enables_a_skill_and_opens_no_list(tmp_path: Path) -> None:
    """A machine is set up without a human at the list (ADR-0043)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "--on", "alpha")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["alpha"]
    assert "categories" not in payload
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_select_off_disables_a_skill_and_opens_no_list(tmp_path: Path) -> None:
    """The mirror of `--on`, and gated the same way a deletion always is."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--off", "alpha", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["removed"] == ["alpha"]
    assert "categories" not in payload
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_select_on_leaves_the_skills_it_does_not_name_alone(tmp_path: Path) -> None:
    """Naming one Skill can never silently Disable another (ADR-0043)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--on", "gamma")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["gamma"]
    assert payload["removed"] == []
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_select_off_leaves_the_skills_it_does_not_name_alone(tmp_path: Path) -> None:
    """Unchecking one Skill is not an answer about any other."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")

    result = _run(world, "apply", "select", "--off", "gamma", "--yes")

    assert result.returncode == 0, result.stderr
    assert _json(result)["removed"] == ["gamma"]
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_select_on_leaves_a_deviating_skill_it_did_not_name_alone(
    tmp_path: Path,
) -> None:
    """Keeping the state it had includes keeping the edit somebody made to it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _digested_catalog(world),
    )
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    result = _run(world, "apply", "select", "--on", "gamma")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["gamma"]
    assert "alpha" in payload["noop"]
    assert installed.read_text(encoding="utf-8") == "hand edited\n"


def test_select_on_leaves_an_incomplete_skill_it_did_not_name_alone(
    tmp_path: Path,
) -> None:
    """A delta answers for the names it carries and for no others (ADR-0043)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "select", "alpha")
    shutil.rmtree(world["home"] / ".config" / "crush" / "skills" / "alpha")

    result = _run(world, "apply", "select", "--on", "gamma")

    assert result.returncode == 0, result.stderr
    assert _json(result)["placed"] == ["gamma"]
    assert not (world["home"] / ".config" / "crush" / "skills" / "alpha").exists()


def test_select_takes_more_than_one_on_and_more_than_one_off(tmp_path: Path) -> None:
    """One invocation carries the whole delta, however many names it names."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")

    result = _run(
        world,
        "apply",
        "select",
        "--on",
        "beta",
        "--off",
        "alpha",
        "--off",
        "gamma",
        "--yes",
    )

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["beta"]
    assert payload["removed"] == ["alpha", "gamma"]


def test_select_refuses_a_delta_and_a_whole_answer_in_one_invocation(
    tmp_path: Path,
) -> None:
    """Names are the whole set; `--on` and `--off` are a change to it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "alpha", "--on", "beta")

    assert result.returncode != 0
    assert "--on" in result.stderr
    assert "whole answer" in result.stderr
    assert not (world["home"] / ".claude" / "skills" / "beta").exists()


def test_select_off_refuses_without_yes(tmp_path: Path) -> None:
    """A delta that deletes files is gated like any other (ADR-0029)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--off", "alpha")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_select_on_refuses_an_unknown_skill(tmp_path: Path) -> None:
    """A delta names Catalog skills; a typo is a refusal, never a silent miss."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "--on", "nosuch")

    assert result.returncode != 0
    assert "nosuch" in result.stderr


def test_select_on_resolves_the_whole_closure_before_it_writes(
    tmp_path: Path,
) -> None:
    """`--on release --yes` Enables `push` and `commit` as well (issue #29)."""

    world = _world(tmp_path, _CHAIN)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "--on", "delta", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["alpha", "beta", "delta"]
    assert payload["unsatisfied"] == {}


def test_select_off_stands_against_a_dependency_the_same_run_would_add(
    tmp_path: Path,
) -> None:
    """What the user unchecked stays unchecked; what it lacks is reported."""

    world = _world(tmp_path, _CHAIN)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "--on", "delta", "--off", "beta", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["alpha", "delta"]
    assert payload["unsatisfied"] == {"delta": ["beta"]}


def test_select_project_on_leaves_a_global_dependency_where_it_is(
    tmp_path: Path,
) -> None:
    """Global's copy Satisfies it, and a second one buys nothing (ADR-0013)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--project", "--on", "beta")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == ["beta"]
    assert payload["unsatisfied"] == {}
    assert not (world["project"] / ".claude" / "skills" / "alpha").exists()


def test_select_as_is_enables_nothing_that_was_not_enabled(tmp_path: Path) -> None:
    """An unattended run can never inject instructions nobody read (ADR-0043)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--as-is", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == []
    assert payload["removed"] == []
    assert "categories" not in payload
    assert not (world["home"] / ".claude" / "skills" / "beta").exists()


def test_select_as_is_repairs_an_incomplete_skill(tmp_path: Path) -> None:
    """Putting what the user has into good order needs no list to read."""

    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "select", "alpha")
    shutil.rmtree(world["home"] / ".config" / "crush" / "skills" / "alpha")

    result = _run(world, "apply", "select", "--as-is", "--yes")

    assert result.returncode == 0, result.stderr
    assert _json(result)["placed"] == ["alpha"]
    assert (
        world["home"] / ".config" / "crush" / "skills" / "alpha" / "SKILL.md"
    ).is_file()


def test_select_as_is_refreshes_a_deviating_skill(tmp_path: Path) -> None:
    """Putting what the user has into good order is what the flag is for."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json",
        _digested_catalog(world),
    )
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    result = _run(world, "apply", "select", "--as-is", "--yes")

    assert result.returncode == 0, result.stderr
    assert _json(result)["placed"] == ["alpha"]
    source = world["source"] / "skills" / "code" / "alpha" / "SKILL.md"
    assert installed.read_bytes() == source.read_bytes()


def test_select_as_is_refreshes_nothing_from_the_snapshot_and_says_why(
    tmp_path: Path,
) -> None:
    """Those digests describe the collection as of the last Update (ADR-0041)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    catalog = _digested_catalog(world)
    _write(world["source"] / "skills" / "kntnt" / "catalog.json", catalog)
    _run(world, "apply", "select", "alpha")
    _write(world["here"] / "catalog.json", catalog)
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")
    _unreachable_origin(world)

    result = _run(world, "apply", "select", "--as-is", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["placed"] == []
    assert payload["catalog_refreshed"] is False
    assert installed.read_text(encoding="utf-8") == "hand edited\n"


def test_select_names_the_delta_forms_in_its_steps(tmp_path: Path) -> None:
    """The list is suppressed where there is nobody to read it (issue #29)."""

    text = (REPO_ROOT / "skills" / "kntnt" / "steps" / "select.md").read_text(
        encoding="utf-8"
    )

    assert "`--on`" in text
    assert "`--off`" in text
    assert "--as-is" in text
    assert "open no list" in text


def test_the_manager_has_no_status_enable_or_disable_verb(tmp_path: Path) -> None:
    """Three verbs and a transcription step became one gesture (ADR-0043)."""

    world = _world(tmp_path)
    manager = REPO_ROOT / "skills" / "kntnt"

    for args in (
        ("status",),
        ("status", "--project"),
        ("plan", "enable", "alpha"),
        ("plan", "disable", "alpha"),
        ("apply", "enable", "alpha"),
        ("apply", "disable", "alpha", "--yes"),
    ):
        assert _run(world, *args).returncode != 0, args

    body = (manager / "SKILL.md").read_text(encoding="utf-8")
    for verb in ("status", "enable", "disable"):
        assert f"`{verb}`" not in body, verb
        assert f"{verb}|" not in body, verb
        assert not (manager / "steps" / f"{verb}.md").exists(), verb
        assert not (manager / "help" / f"{verb}.md").exists(), verb


def test_select_points_at_update_for_what_it_cannot_take_off(tmp_path: Path) -> None:
    """The closing line is the only place a withdrawn skill can be acted on."""

    text = (REPO_ROOT / "skills" / "kntnt" / "steps" / "select.md").read_text(
        encoding="utf-8"
    )

    assert "`withdrawn`" in text
    assert "/kntnt update" in text


def test_reported_directories_cover_where_a_universal_harness_really_lands(
    tmp_path: Path,
) -> None:
    """The transport writes a universal Harness's Global files to the canonical tree.

    Reporting the documented path alone would name a directory the file never
    landed in, and the user reads this to learn where the work happened.
    """

    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")

    payload = _json(_run(world, "plan", "select"))

    assert payload["directories"] == sorted(
        [
            str(world["home"] / ".agents" / "skills"),
            str(world["home"] / ".config" / "opencode" / "skills"),
        ]
    )


def test_a_directory_two_harnesses_share_is_resolved_once(tmp_path: Path) -> None:
    """Every universal Harness's Global files land in one canonical tree.

    Two of them present means that tree is reached twice over, and a walk that
    took it twice would do its work there twice — for Update's sweep, that is
    every SKILL.md in it read once per Harness id rather than once per run.
    """

    world = _world(tmp_path)
    _present(world, "home", ".codex", ".cursor")

    payload = _json(_run(world, "plan", "select"))

    assert payload["directories"] == sorted(
        [
            str(world["home"] / ".agents" / "skills"),
            str(world["home"] / ".codex" / "skills"),
            str(world["home"] / ".cursor" / "skills"),
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
        ("plan", "select"),
        ("plan", "select", "--project"),
        ("plan", "update"),
    ):
        result = _run(world, *args)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "setup" not in result.stderr.lower()


def test_a_checked_skill_is_placed_in_every_detected_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/opencode")

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()
    assert _row(_json(_run(world, "plan", "select")), "alpha")["checked"] is True


def test_a_checked_skill_with_nothing_detected_writes_the_shared_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / SHARED_SKILLS / "alpha" / "SKILL.md").is_file()
    assert sorted(child.name for child in world["home"].iterdir()) == [".agents"]


def test_a_project_answer_places_the_skill_in_every_detected_harness(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude", ".crush")

    result = _run(world, "apply", "select", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()
    assert (world["project"] / ".crush" / "skills" / "gamma" / "SKILL.md").is_file()


def test_a_project_answer_with_nothing_detected_writes_the_shared_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)

    result = _run(world, "apply", "select", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / SHARED_SKILLS / "gamma" / "SKILL.md").is_file()
    assert sorted(child.name for child in world["project"].iterdir()) == [".agents"]


def test_project_detection_ignores_an_ordinary_skills_directory(
    tmp_path: Path,
) -> None:
    """`skills/` and `data/` are things a repository has for its own reasons."""

    world = _world(tmp_path)
    _present(world, "project", "skills", "data")

    result = _run(world, "apply", "select", "--project", "gamma")

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
    _run(world, "apply", "select", "alpha")
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

    result = _run(world, "apply", "select", "alpha", log=log)

    assert result.returncode == 0, result.stderr
    expected = _harnesses_reading("~/.agents/skills", global_layer=True)
    assert len(expected) > 1
    assert set(_calls(log)[0]["agents"]) == expected


def test_an_unchecked_skill_leaves_every_detected_directory(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/opencode")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--yes")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()
    assert not (world["home"] / ".config" / "opencode" / "skills" / "alpha").exists()


def test_select_sees_opencode_skill_in_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha"))

    payload = _json(_run(world, "plan", "select"))

    assert _row(payload, "alpha")["checked"] is True


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


def test_plan_select_prints_the_list_and_writes_nothing(tmp_path: Path) -> None:
    """Reading is never a side-effecting act: the list half touches no file."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    before = _tree(world["home"])

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["action"] == "select"
    assert payload["layer"] == "global"
    assert "alpha" in [row["name"] for row in payload["categories"]["code"]]
    assert _tree(world["home"]) == before


def test_an_answer_that_changes_nothing_writes_nothing(tmp_path: Path) -> None:
    """Someone who opened the list to read it must be able to leave unchanged."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    first = _run(world, "apply", "select", "alpha")
    log = tmp_path / "transport.jsonl"
    second = _run(world, "apply", "select", "alpha", log=log)

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    payload = _json(second)
    assert payload["intended"] == []
    assert payload["placed"] == []
    assert payload["removed"] == []
    assert payload["noop"] == ["alpha"]
    assert not log.exists()


def test_apply_select_refuses_the_manager(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "kntnt")

    assert result.returncode == 1
    assert "manager" in result.stderr.lower()


def test_apply_select_refuses_an_unknown_skill(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "nope")

    assert result.returncode == 1
    assert "nope" in result.stderr


def test_apply_select_project_writes_only_the_project_layer(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")

    result = _run(world, "apply", "select", "--project", "gamma")

    assert result.returncode == 0, result.stderr
    assert (world["project"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    assert _row(_json(_run(world, "plan", "select")), "gamma")["checked"] is False
    project = _json(_run(world, "plan", "select", "--project"))
    assert _row(project, "gamma")["checked"] is True


def test_select_project_cannot_uncheck_a_skill_only_global_carries(
    tmp_path: Path,
) -> None:
    """This layer holds no copy of it, and there is no subtractive overlay."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--project", "--yes")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    payload = _json(result)
    assert payload["intended"] == []
    assert payload["removed"] == []


def test_project_off_targets_global(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")

    result = _run(world, "apply", "select", "--project=off", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert not (world["project"] / ".claude" / "skills" / "alpha").exists()


def test_update_reports_new_catalog_entries_and_leaves_them_disabled(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

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
    listing = _json(_run(world, "plan", "select"))
    assert "delta" in _checked(listing)
    assert _checked(listing)["delta"] is False


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
    assert "/kntnt select" in payload["unsatisfied"][0]["how"]
    assert "alpha" in payload["unsatisfied"][0]["how"]


def test_check_is_ok_when_dependencies_are_present(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "beta")
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

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["alpha"]
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert (
        world["home"] / ".config" / "opencode" / "skills" / "alpha" / "SKILL.md"
    ).is_file()


def test_select_names_the_capabilities_a_row_needs_of_the_harness(
    tmp_path: Path,
) -> None:
    """The user learns before choosing that a skill may refuse to work here."""

    world = _world(tmp_path, [_entry("alpha", "agents", capabilities=["subagents"])])

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    assert _row(_json(result), "alpha")["capabilities"] == ["subagents"]


def test_update_reports_capabilities_per_skill(tmp_path: Path) -> None:
    world = _world(tmp_path, [_entry("alpha", "agents", capabilities=["subagents"])])
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    capabilities = _json(result)["capabilities"]
    assert [item["skill"] for item in capabilities] == ["alpha"]
    assert capabilities[0]["name"] == "subagents"


def test_help_prints_the_manpage_the_manager_ships(tmp_path: Path) -> None:
    """The manager's help is a file beside it, not a string inside its script."""

    world = _world(tmp_path)

    result = _run(world, "help")

    assert result.returncode == 0, result.stderr
    shipped = (REPO_ROOT / "skills" / "kntnt" / "help.md").read_text(encoding="utf-8")
    assert result.stdout.strip() == shipped.strip()


def test_help_named_subcommand_prints_that_subcommands_manpage(
    tmp_path: Path,
) -> None:
    """`/kntnt help <command>` is how a verb of the manager is read about."""

    world = _world(tmp_path)

    result = _run(world, "help", "uninstall")

    assert result.returncode == 0, result.stderr
    shipped = (REPO_ROOT / "skills" / "kntnt" / "help" / "uninstall.md").read_text(
        encoding="utf-8"
    )
    assert result.stdout.strip() == shipped.strip()


def test_help_named_skill_prefers_the_manpage_beside_it(tmp_path: Path) -> None:
    """A skill that ships `help.md` is read from that file, not from its Steps."""

    world = _world(tmp_path)
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha", help_body="Generated help."))
    _write(dest / "help.md", "# alpha\n\nThe alpha manpage.\n")

    result = _run(world, "help", "alpha")

    assert result.returncode == 0, result.stderr
    assert "The alpha manpage." in result.stdout
    assert "Generated help." not in result.stdout


def test_help_named_skill_prints_that_skills_help(tmp_path: Path) -> None:
    world = _world(tmp_path)

    result = _run(world, "help", "alpha")

    assert result.returncode == 0, result.stderr
    assert "Help for alpha." in result.stdout


def test_select_lists_without_a_stored_snapshot(tmp_path: Path) -> None:
    """A Manager with no snapshot beside it still lists, and stays without one.

    Select reads the origin, so a missing snapshot costs it nothing. Writing
    one would give a reading gesture a write side effect and, worse, hand the
    next Update a baseline it never chose: Update tells new entries from
    withdrawn ones by diffing the snapshot it stored against what the origin
    now carries, and a snapshot laid down by Select flattens that diff.
    """

    world = _world(tmp_path)
    (world["here"] / "catalog.json").unlink()

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    assert sorted(_checked(_json(result))) == ["alpha", "beta", "gamma"]
    assert not (world["here"] / "catalog.json").exists()


def test_select_lists_a_skill_the_origin_added_after_the_snapshot(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(world, delta, [*_SURVIVORS, delta])

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is True
    assert _row(payload, "delta")["checked"] is False


def test_select_leaves_out_a_skill_the_origin_no_longer_carries(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    assert sorted(_checked(_json(result))) == ["alpha", "beta"]


def test_select_does_not_place_a_newly_published_skill_on_disk(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(world, delta, [*_SURVIVORS, delta])

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()


def test_select_accepts_a_name_only_the_origin_carries(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(world, delta, [*_SURVIVORS, delta])

    result = _run(world, "apply", "select", "delta")

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["delta"]
    assert (world["home"] / ".claude" / "skills" / "delta" / "SKILL.md").is_file()


def test_select_falls_back_to_the_snapshot_when_the_origin_is_unreachable(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _unreachable_origin(world)

    result = _run(world, "plan", "select")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is False
    assert sorted(_checked(payload)) == ["alpha", "beta", "gamma"]


def test_select_works_from_the_snapshot_when_the_origin_is_unreachable(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _unreachable_origin(world)

    result = _run(world, "apply", "select", "alpha")

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
    _run(world, "apply", "select", "alpha")
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


def test_select_says_which_catalog_the_list_came_from(tmp_path: Path) -> None:
    """Discovery is the list itself, so the body has to declare the list's source."""

    text = (REPO_ROOT / "skills" / "kntnt" / "steps" / "select.md").read_text(
        encoding="utf-8"
    )

    assert "catalog_refreshed" in text
    assert "deviating" in text


def test_manager_skill_is_user_invoked_and_not_internal() -> None:
    text = (REPO_ROOT / "skills" / "kntnt" / "SKILL.md").read_text(encoding="utf-8")
    assert "disable-model-invocation: true" in text
    assert "internal: true" not in text
    select = (REPO_ROOT / "skills" / "kntnt" / "steps" / "select.md").read_text(
        encoding="utf-8"
    )
    assert "scripts/kntnt.py" in select


def test_check_treats_a_global_skill_as_effective_for_a_project_skill(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")
    _run(world, "apply", "select", "--project", "beta")
    beta = world["project"] / ".claude" / "skills" / "beta"

    result = _run(world, "check", "--here", str(beta))

    assert result.returncode == 0, result.stderr
    assert _json(result)["ok"] is True


def test_update_project_does_not_install_the_manager_in_the_project(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "--project", "alpha")

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
    _run(world, "apply", "select", "gamma")
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
    _run(world, "apply", "select", "gamma")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "gamma")
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
    _run(world, "apply", "select", "gamma")
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
    _run(world, "apply", "select", "gamma")
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
    _run(world, "apply", "select", "gamma")
    _run(world, "apply", "select", "--project", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", "--project")

    assert result.returncode == 0, result.stderr
    assert not (world["project"] / ".claude" / "skills" / "gamma").exists()
    assert (world["home"] / ".claude" / "skills" / "gamma" / "SKILL.md").is_file()


def test_update_refreshes_the_rest_when_a_withdrawal_fails(tmp_path: Path) -> None:
    """A transport that refuses one removal does not get to end the run."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
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
    assert result.stdout.startswith("# kntnt")
    assert result.stdout == _run(world, "help").stdout


def test_help_says_select_lists_every_catalog_skill(tmp_path: Path) -> None:
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
    assert sorted(_checked(_json(_run(world, "plan", "select")))) == [
        "alpha",
        "delta",
    ]


def test_update_refreshes_a_sidecar_when_skill_md_is_unchanged(tmp_path: Path) -> None:
    """The transport's own `update` skips these; the manager must not rely on it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    sidecar = world["source"] / "skills" / "code" / "alpha" / "notes.md"
    _write(sidecar, "revised\n")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    installed = world["home"] / ".claude" / "skills" / "alpha" / "notes.md"
    assert installed.read_text(encoding="utf-8") == "revised\n"


def test_update_leaves_a_skill_whose_digest_matches_alone(tmp_path: Path) -> None:
    """A Skill already byte-identical to the collection is no work (ADR-0028)."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    log = tmp_path / "transport.jsonl"

    result = _run(world, "apply", "update", log=log)

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["current"] == ["alpha"]
    assert payload["intended"] == ["kntnt"]
    assert all("alpha" not in call["skills"] for call in _calls(log))


def test_update_refreshes_a_skill_whose_digest_deviates(tmp_path: Path) -> None:
    """A refresh discards the local edit that made the Skill Deviate (ADR-0041)."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["intended"] == ["kntnt", "alpha"]
    assert payload["confirmed"] == ["kntnt", "alpha"]
    assert payload["current"] == []
    source = world["source"] / "skills" / "code" / "alpha" / "SKILL.md"
    assert installed.read_bytes() == source.read_bytes()


def test_update_refreshes_the_manager_whatever_the_digests_say(tmp_path: Path) -> None:
    """It is no Catalog entry, and the verb that repairs the rest has to reach itself."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "update")
    log = tmp_path / "transport.jsonl"

    result = _run(world, "apply", "update", log=log)

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["kntnt"]
    assert [call["skills"] for call in _calls(log)] == [["kntnt"]]


def test_update_reports_what_moved_apart_from_what_did_not(tmp_path: Path) -> None:
    """*Twelve of twelve refreshed* said the same thing whatever had happened."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "beta")
    installed = world["home"] / ".claude" / "skills" / "beta" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["intended"] == ["kntnt", "beta"]
    assert payload["current"] == ["alpha"]


def test_a_refreshed_skill_is_the_files_the_collection_ships(tmp_path: Path) -> None:
    """Withdrawn upstream is gone, changed is replaced, added is present — after one call."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    upstream = world["source"] / "skills" / "code" / "alpha"
    _write(upstream / "gone.md", "carried once\n")
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json", _digested_catalog(world)
    )
    _run(world, "apply", "select", "alpha")

    (upstream / "gone.md").unlink()
    _write(upstream / "notes.md", "added upstream\n")
    _write(
        upstream / "SKILL.md",
        _skill_md(
            "alpha",
            description="The alpha skill.",
            binaries=["git"],
            help_body="Revised help for alpha.",
        ),
    )
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json", _digested_catalog(world)
    )

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["kntnt", "alpha"]
    assert _tree(world["home"] / ".claude" / "skills" / "alpha") == _tree(upstream)


def test_update_re_checks_a_skill_it_did_not_refresh(tmp_path: Path) -> None:
    """A Dependency is the layer's business, and the layer is not only what moved."""

    world = _digested_world(
        tmp_path,
        [
            _entry(
                "alpha",
                "agents",
                binaries=["definitely-not-a-binary-kntnt"],
                capabilities=["subagents"],
            )
        ],
    )
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["current"] == ["alpha"]
    assert [item["name"] for item in payload["unsatisfied"]] == [
        "definitely-not-a-binary-kntnt"
    ]
    assert [item["skill"] for item in payload["capabilities"]] == ["alpha"]


def test_update_reports_a_gated_refresh_that_never_landed(tmp_path: Path) -> None:
    """The Digest decides what is copied; the disk still decides what is reported."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")
    _present(world, "home", ".config/crush")

    result = _run(world, "apply", "update", skip=["alpha"])

    assert result.returncode != 0
    payload = _json(result)
    assert [item["name"] for item in payload["failed"]] == ["alpha"]
    assert payload["current"] == [], "a Skill that never landed is not current"


def test_update_sweeps_a_withdrawal_with_everything_else_current(
    tmp_path: Path,
) -> None:
    """The sweep asks the disk what this collection wrote, and no Digest gates it."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)
    _write(
        world["source"] / "skills" / "kntnt" / "catalog.json", _digested_catalog(world)
    )

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["removed"] == [{"name": "gamma", "disk": "removed"}]
    assert payload["current"] == ["alpha"]
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()


def test_update_refreshes_nothing_from_the_snapshot_and_says_so(
    tmp_path: Path,
) -> None:
    """The files move through the origin the Catalog could not be read from (ADR-0041)."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _store_snapshot(world)
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")
    _unreachable_origin(world)
    log = tmp_path / "transport.jsonl"

    result = _run(world, "apply", "update", log=log)

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is False
    assert payload["intended"] == []
    assert payload["current"] == []
    assert not log.exists(), "the transport was asked for files it could not fetch"
    assert installed.read_text(encoding="utf-8") == "hand edited\n"


def test_plan_update_names_only_what_it_would_refresh(tmp_path: Path) -> None:
    """The plan is what the user confirms, so it cannot promise a refresh of everything."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "beta")
    installed = world["home"] / ".claude" / "skills" / "beta" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    payload = _json(_run(world, "plan", "update"))

    assert payload["refresh"] == ["kntnt", "beta"]
    assert payload["current"] == ["alpha"]
    assert payload["catalog_refreshed"] is True


def test_plan_update_promises_no_refresh_from_the_snapshot(tmp_path: Path) -> None:
    """Nothing can be fetched, so there is nothing to plan and nothing to confirm."""

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _store_snapshot(world)
    _unreachable_origin(world)

    payload = _json(_run(world, "plan", "update"))

    assert payload["catalog_refreshed"] is False
    assert payload["refresh"] == []
    assert payload["current"] == []


def test_the_transport_empties_a_skill_directory_before_it_copies(
    tmp_path: Path,
) -> None:
    """`add` replaces a skill's directory rather than merging into it.

    A file the collection does not carry is gone after a re-`add` — verified
    against the real transport, and ADR-0028 is where the double's obligation
    to model it is written down.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha"
    stray = installed / "notes" / "stray.md"
    _write(stray, "left behind\n")

    result = _transport_add(world, "alpha")

    assert result.returncode == 0, result.stderr
    assert not stray.exists()
    assert (installed / "SKILL.md").is_file()


def test_the_transport_discards_a_hand_edit_to_a_file_of_the_skill(
    tmp_path: Path,
) -> None:
    """The other half of the postcondition: the collection's bytes, not the edit.

    This half holds through the copy rather than through the wipe — the source
    is written over whatever is there — so it would survive the wipe being
    lost. Both halves together are what lets a refresh promise the skill on
    disk is the skill the collection ships, so both are pinned.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")

    result = _transport_add(world, "alpha")

    assert result.returncode == 0, result.stderr
    source = world["source"] / "skills" / "code" / "alpha" / "SKILL.md"
    assert installed.read_bytes() == source.read_bytes()


def test_unchecking_refuses_without_yes(tmp_path: Path) -> None:
    """The flag is the gate where the answer deletes files (ADR-0029)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_an_answer_that_only_places_needs_no_gate(tmp_path: Path) -> None:
    """Nothing is deleted, so there is nothing for the flag to stand in for."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    assert (world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()


def test_every_verb_accepts_yes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")

    for args in (
        ("help", "--yes"),
        ("plan", "select", "--yes"),
        ("plan", "update", "--yes"),
        ("plan", "uninstall", "--yes"),
        ("apply", "select", "alpha", "--yes"),
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


def test_every_collection_skill_ships_a_manpage_and_prints_it() -> None:
    """Help lives with the skill: a file it prints, not prose it regenerates."""

    for path in (REPO_ROOT / "skills").glob("*/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        assert (path.parent / "help.md").is_file(), path
        assert "`$HERE/help.md`" in text, path
        assert "--help" in text, path
        assert "Arguments and Steps" not in text, path


def test_the_manager_separates_steps_from_manpages() -> None:
    """One rule everywhere: `help.md` is the manpage, `steps/` is the instructions."""

    manager = REPO_ROOT / "skills" / "kntnt"
    verbs = ("help", "select", "update", "uninstall")

    assert (manager / "help.md").is_file()
    for verb in verbs:
        assert (manager / "steps" / f"{verb}.md").is_file(), verb
        assert (manager / "help" / f"{verb}.md").is_file(), verb
        if verb != "help":
            assert not (manager / f"{verb}.md").exists(), verb

    text = (manager / "SKILL.md").read_text(encoding="utf-8")
    assert "$HERE/steps/" in text


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
    assert json.loads(result.stdout) == json.loads(shipped), (
        "run `KNTNT_SOURCE=. uv run skills/kntnt/scripts/kntnt.py catalog --write`"
    )


def test_the_generated_catalog_digests_each_skill_directory(tmp_path: Path) -> None:
    """The Digest is generated with the Catalog, so nothing has to be bumped."""

    world = _world(tmp_path)

    before = _json(_run(world, "catalog"))
    _write(world["source"] / "skills" / "code" / "alpha" / "extra.md", "more\n")
    after = _json(_run(world, "catalog"))

    digests_before = {entry["name"]: entry["digest"] for entry in before["skills"]}
    digests_after = {entry["name"]: entry["digest"] for entry in after["skills"]}
    assert all(len(digest) == 64 for digest in digests_before.values())
    assert digests_after["alpha"] != digests_before["alpha"]
    assert digests_after["beta"] == digests_before["beta"]


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


def test_select_confirms_each_placement_against_the_disk(tmp_path: Path) -> None:
    """A clean run says what it did and says the disk was read to know it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "alpha")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["intended"] == ["alpha"]
    assert payload["confirmed"] == ["alpha"]
    assert payload["failed"] == []


def test_select_reports_a_placement_the_transport_did_not_make(
    tmp_path: Path,
) -> None:
    """A transport that exits zero and writes nothing is not a success."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    result = _run(world, "apply", "select", "alpha", skip=["alpha"])

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


def test_select_project_reports_a_placement_the_transport_did_not_make(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude")

    result = _run(world, "apply", "select", "--project", "gamma", skip=["gamma"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["confirmed"] == []
    assert payload["failed"][0]["directories"] == [
        str(world["project"] / ".claude" / "skills")
    ]


def test_select_reports_a_removal_the_transport_did_not_make(tmp_path: Path) -> None:
    """The reported defect: removal claimed, files still there, exit 0."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "--yes", skip=["alpha"])

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


def test_select_project_reports_a_removal_the_transport_did_not_make(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "--project", "gamma")

    result = _run(world, "apply", "select", "--project", "--yes", skip=["gamma"])

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

    result = _run(world, "apply", "select", "alpha", "beta", skip=["beta"])

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
    _run(world, "apply", "select", "alpha")
    shutil.rmtree(world["home"] / ".config" / "crush" / "skills" / "alpha")

    result = _run(world, "apply", "select", "--yes", skip=["alpha"])

    assert result.returncode != 0
    assert _json(result)["failed"][0]["directories"] == [
        str(world["home"] / ".claude" / "skills")
    ]


def test_update_reports_a_refresh_that_never_landed(tmp_path: Path) -> None:
    """Update reaches a Harness installed since the last Enable, or says so."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")

    result = _run(world, "apply", "select", "alpha", skip=["alpha"])

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["intended"] == []
    assert payload["confirmed"] == []
    assert payload["failed"] == []
    assert payload["noop"] == ["alpha"]
    assert payload["placed"] == []
    assert payload["removed"] == []


def test_the_change_verbs_tell_the_user_when_a_change_did_not_take(
    tmp_path: Path,
) -> None:
    """The payload is half of it; the skill body has to show the failure."""

    for name in ("select.md", "update.md"):
        text = (REPO_ROOT / "skills" / "kntnt" / "steps" / name).read_text(
            encoding="utf-8"
        )
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

    result = _run(world, "apply", "select", "--yes", skip=["alpha"])

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
    _run(world, "apply", "select", "alpha", "beta")
    _install_manager(world)

    result = _run(world, "apply", "uninstall", "--yes")

    assert result.returncode == 0, result.stderr
    for harness in (".claude", ".config/crush"):
        skills = world["home"] / harness / "skills"
        assert sorted(path.name for path in skills.iterdir()) == []


def test_uninstall_reports_every_name_it_took_off_the_disk(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")
    _run(world, "apply", "select", "--project", "gamma")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha")
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
    _run(world, "apply", "select", "alpha", "beta")
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
    _run(world, "apply", "select", "alpha")
    _install_manager(world)
    installed = world["home"] / ".claude" / "skills" / "kntnt"

    result = _run(world, "apply", "uninstall", "--yes", installed=installed)

    assert result.returncode == 0, result.stderr
    assert _json(result)["confirmed"] == ["alpha", "kntnt"]
    assert not installed.exists()


def test_uninstall_tells_the_user_what_it_does_not_touch() -> None:
    """No payload can carry every working directory; the body has to say it."""

    text = (REPO_ROOT / "skills" / "kntnt" / "steps" / "uninstall.md").read_text(
        encoding="utf-8"
    )

    assert "`failed`" in text
    assert "`directories`" in text
    assert "Project" in text


def test_help_lists_the_uninstall_verb(tmp_path: Path) -> None:
    """Help is the only place the way out is discovered."""

    world = _world(tmp_path)

    text = _run(world, "help").stdout

    assert "uninstall" in text


def _tree(root: Path) -> dict[str, bytes]:
    """Snapshot every file under *root*, so a run can be shown to have left it alone."""

    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_the_transport_writes_where_home_points(tmp_path: Path) -> None:
    """The real transport honours an overridden HOME, and the double has to too.

    That property is the whole of what makes a Sandbox possible (ADR-0042), so
    a double that resolved its home some other way would let a dry run pass
    the suite while writing into the user's real home.
    """

    world = _world(tmp_path)
    elsewhere = tmp_path / "elsewhere"

    result = _transport_add(world, "alpha", home=elsewhere)

    assert result.returncode == 0, result.stderr
    assert (elsewhere / ".claude" / "skills" / "alpha" / "SKILL.md").is_file()
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_dry_run_leaves_every_directory_of_the_layer_alone(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    before = _tree(world["home"])

    result = _run(world, "apply", "select", "alpha", "--dry-run")

    assert result.returncode == 0, result.stderr
    assert _tree(world["home"]) == before


def test_dry_run_reports_an_outcome_read_from_the_sandbox(tmp_path: Path) -> None:
    """What comes back is the verb's own outcome, not a description of intent."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    payload = _json(_run(world, "apply", "select", "alpha", "--dry-run"))

    assert payload["intended"] == ["alpha"]
    assert payload["confirmed"] == ["alpha"]
    assert payload["failed"] == []
    assert payload["noop"] == []


def test_dry_run_makes_the_transport_calls_the_real_run_makes(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    dry = tmp_path / "dry.jsonl"
    real = tmp_path / "real.jsonl"

    _run(world, "apply", "select", "alpha", "--dry-run", log=dry)
    _run(world, "apply", "select", "alpha", log=real)

    assert _calls(dry) == _calls(real)


def test_dry_run_says_it_downloads_the_transport_afresh(tmp_path: Path) -> None:
    """An unexplained pause is when a user reaches for the interrupt."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    payload = _json(_run(world, "apply", "select", "alpha", "--dry-run"))

    note = payload["dry_run"]["note"]
    assert "download" in note
    assert "longer" in note


def test_dry_run_starts_from_the_collection_files_the_layer_holds(
    tmp_path: Path,
) -> None:
    """Seeded with what is here, so a preview reports the run and not the world."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    before = _tree(world["home"])

    payload = _json(_run(world, "apply", "select", "--yes", "--dry-run"))

    assert payload["confirmed"] == ["alpha"]
    assert _tree(world["home"]) == before


def test_dry_run_reports_a_skill_already_enabled_as_no_work(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    payload = _json(_run(world, "apply", "select", "alpha", "--dry-run"))

    assert payload["noop"] == ["alpha"]
    assert payload["intended"] == []


def test_dry_run_leaves_a_skill_that_is_not_ours_out_of_the_sandbox(
    tmp_path: Path,
) -> None:
    """Only this collection's files are seeded; another's is nothing to copy."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _write(
        world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md",
        _foreign_skill_md("alpha"),
    )

    payload = _json(_run(world, "apply", "select", "alpha", "--dry-run"))

    assert payload["intended"] == ["alpha"]
    assert payload["noop"] == []


def test_dry_run_update_writes_neither_the_skills_nor_the_stored_catalog(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude", ".config/crush")
    _run(world, "apply", "select", "alpha")
    _install_manager(world)
    delta = _entry("delta", "code", description="The delta skill.")
    _publish(
        world,
        delta,
        [*_SURVIVORS, _entry("gamma", "text", description="The gamma skill."), delta],
    )
    before = _tree(world["home"])
    stored = (world["here"] / "catalog.json").read_bytes()

    payload = _json(_run(world, "apply", "update", "--dry-run"))

    assert payload["new"] == ["delta"]
    assert "alpha" in payload["confirmed"]
    assert _tree(world["home"]) == before
    assert (world["here"] / "catalog.json").read_bytes() == stored


def test_dry_run_uninstall_keeps_the_collection_on_the_machine(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _install_manager(world)
    before = _tree(world["home"])

    payload = _json(_run(world, "apply", "uninstall", "--yes", "--dry-run"))

    assert payload["confirmed"] == ["alpha", "kntnt"]
    assert _tree(world["home"]) == before


def test_dry_run_project_leaves_the_working_directory_alone(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _present(world, "project", ".claude")
    before = _tree(world["project"])

    payload = _json(_run(world, "apply", "select", "--project", "alpha", "--dry-run"))

    assert payload["confirmed"] == ["alpha"]
    assert _tree(world["project"]) == before


def test_dry_run_takes_the_sandbox_with_it(tmp_path: Path) -> None:
    """A dry run leaves a report behind and nothing else."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")

    payload = _json(_run(world, "apply", "select", "alpha", "--dry-run"))

    assert not Path(payload["dry_run"]["sandbox"]).exists()


def test_dry_run_catalog_prints_the_catalog_and_writes_nothing(
    tmp_path: Path,
) -> None:
    """The one write outside a layer honours the flag rather than ignoring it."""

    world = _world(tmp_path)
    _publish(
        world,
        _entry("delta", "code", description="The delta skill."),
        [*_SURVIVORS, _entry("gamma", "text", description="The gamma skill.")],
    )
    stored = (world["here"] / "catalog.json").read_bytes()

    result = _run(world, "catalog", "--write", "--dry-run")

    assert result.returncode == 0, result.stderr
    assert "delta" in json.dumps(json.loads(result.stdout))
    assert (world["here"] / "catalog.json").read_bytes() == stored


def test_every_subparser_accepts_dry_run(tmp_path: Path) -> None:
    """A forwarded flag must never be the thing that breaks a run (ADR-0029)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    gamma = world["source"] / "skills" / "text" / "gamma"

    for args in (
        ("help", "--dry-run"),
        ("check", "--here", str(gamma), "--dry-run"),
        ("catalog", "--dry-run"),
        ("plan", "select", "--dry-run"),
        ("plan", "update", "--dry-run"),
        ("plan", "uninstall", "--dry-run"),
        ("apply", "select", "alpha", "--dry-run"),
        ("apply", "select", "--yes", "--dry-run"),
        ("apply", "update", "--dry-run"),
        ("apply", "uninstall", "--yes", "--dry-run"),
    ):
        result = _run(world, *args)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "unrecognized arguments" not in result.stderr


def test_help_documents_the_dry_run_flag(tmp_path: Path) -> None:
    world = _world(tmp_path)

    text = _run(world, "help").stdout

    assert "--dry-run" in text


def test_every_changing_verb_forwards_the_dry_run_flag() -> None:
    """The agent's forwarding is prose, so the prose has to say it."""

    for verb in ("select", "update", "uninstall"):
        text = (REPO_ROOT / "skills" / "kntnt" / "steps" / f"{verb}.md").read_text(
            encoding="utf-8"
        )
        assert "--dry-run" in text, verb
