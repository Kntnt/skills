"""CLI behaviour of the kntnt manager."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"
HARNESS_PATHS = REPO_ROOT / "skills" / "kntnt" / "harness-paths.json"
MANAGER_DIR = REPO_ROOT / "skills" / "kntnt"
MODEL_SELECTOR_DIR = REPO_ROOT / "skills" / "models" / "model-selector"
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
    body: str = "",
) -> str:
    lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        "disable-model-invocation: true",
        "metadata:",
        '  kntnt.internal: "true"',
    ]

    # Every list is written, empty or not: the four keys are what carries the
    # marker, and a skill declaring nothing still has to be recognisably ours.
    for key, values in (
        ("binaries", binaries or []),
        ("skills", skills or []),
        ("externals", externals or []),
        ("capabilities", capabilities or []),
    ):
        lines.append(f'  kntnt.{key}: "{" ".join(values)}"')
    lines.extend(["---", "", f"# {name}", ""])
    if body:
        lines.extend([body, ""])
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


def _skill_md_with_metadata(name: str, metadata: str) -> str:
    """A SKILL.md whose `metadata` block is written out verbatim.

    `_skill_md` writes the shape the collection ships, which is the one shape
    none of the marker's refusals is about. *metadata* is the whole block,
    newline-terminated, and may be empty.
    """

    return (
        "---\n"
        f"name: {name}\n"
        "description: A collection skill.\n"
        "disable-model-invocation: true\n"
        f"{metadata}"
        "---\n"
        "\n"
        f"# {name}\n"
    )


def _manpage(name: str) -> str:
    """The manpage the origin ships for *name*, as ADR-0044 has every skill do."""

    return f"# {name}\n\nThe {name} manpage, from the collection.\n"


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

    # Shared resources travel inside the Manager rather than as Catalog Skills.
    shutil.copytree(MANAGER_DIR / "library", source / "skills" / "kntnt" / "library")

    # Every collection skill ships its manpage beside its SKILL.md (ADR-0044),
    # so the origin carries one too: it is what Select reads a skill's help
    # from when nobody has that skill installed.
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
            ),
        )
        _write(
            source / "skills" / entry["category"] / entry["name"] / "help.md",
            _manpage(entry["name"]),
        )

    dest_scripts = here / "scripts"
    dest_scripts.mkdir(parents=True)
    shutil.copy(KNTNT_PY, dest_scripts / "kntnt.py")
    shutil.copy(HARNESS_PATHS, here / "harness-paths.json")
    _write(here / "catalog.json", _catalog(entries))
    _write(here / "SKILL.md", _skill_md("kntnt", description="Manager."))
    _ship_manpages(here)
    _ship_manpages(source / "skills" / "kntnt")

    # The running Manager has the same Library its refreshed copy will carry.
    shutil.copytree(MANAGER_DIR / "library", here / "library")

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
    _write(
        world["source"] / "skills" / entry["category"] / entry["name"] / "help.md",
        _manpage(entry["name"]),
    )


def _publish_delta(world: dict[str, Path]) -> None:
    """Publish `delta` at the origin, leaving `alpha` the only entry beside it.

    The arrange every test of the offer shares: one entry the stored snapshot
    has never seen, in a Catalog whose other name that snapshot already carries.
    """

    _publish(
        world,
        _entry("delta", "code", description="The delta skill."),
        [_entry("alpha", "code", binaries=["git"]), _entry("delta", "code")],
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
    grumble: list[str] | None = None,
    installed: Path | None = None,
    paths: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    env = _env(world)
    env["KNTNT_HARNESS_PATHS"] = str(paths or HARNESS_PATHS)
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
    if grumble is not None:
        env["KNTNT_TRANSPORT_GRUMBLE"] = ",".join(grumble)
    script = (installed or world["here"]) / "scripts" / "kntnt.py"

    # Every fixture is a fresh copy of the script at a path `uv` has not seen,
    # so it provisions the environment the PEP 723 block declares and says so
    # on stderr. `--quiet` leaves the fixture reading the script's own output.
    return subprocess.run(
        ["uv", "run", "--quiet", str(script), *args],
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
    """The list is the whole of the plan half; the answer arrives at Apply.

    Refused in the manager's own terms, as every syntax error is: what the
    parser did not declare is named, with the verb's synopsis under it and the
    pointer to its page, rather than argparse's usage dump (ADR-0059).
    """

    world = _world(tmp_path)

    result = _run(world, "plan", "select", "alpha")

    assert result.returncode == 2
    assert "unrecognized arguments" not in result.stderr
    assert "select takes no 'alpha'" in result.stderr


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


def test_the_steps_relay_the_reason_and_still_distrust_the_transport() -> None:
    """The two readings of one sentence, told apart (issues #46, #65).

    *Whatever the transport reported* meant do not take its word for success.
    Once there is a message to hand on it also reads as never mind what it
    said, which is the opposite of what the step now has to do with it. All
    three verbs that can print the message are pinned here, so they cannot
    drift apart again.
    """

    steps = REPO_ROOT / "skills" / "kntnt" / "steps"
    for name in ("update.md", "select.md", "uninstall.md"):
        text = (steps / name).read_text(encoding="utf-8")

        assert "the transport said:" in text
        assert "whether or not the transport claimed otherwise" in text
        assert "whatever the transport reported" not in text
        assert (
            "pass on as it stands whatever the script printed to stderr under "
            "`the transport said:`" in text
        )


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
    """`--on=release --yes` Enables `push` and `commit` as well (issue #29)."""

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


def test_manpage_reads_opencode_skill_from_transport_canonical_dir(
    tmp_path: Path,
) -> None:
    world = _world(tmp_path)
    _present(world, "home", ".config/opencode")
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha"))
    _write(dest / "help.md", "# alpha\n\nThe canonical copy's manpage.\n")

    result = _run(world, "manpage", "alpha")

    assert result.returncode == 0, result.stderr
    assert "The canonical copy's manpage." in result.stdout


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


def test_an_unknown_project_value_is_refused_by_the_parser(tmp_path: Path) -> None:
    """`on` and `off` are the whole of the flag, and argparse is what says so."""

    world = _world(tmp_path)

    result = _run(world, "plan", "select", "--project=sometimes")

    assert result.returncode == 2
    assert "invalid choice" in result.stderr


def test_update_reports_a_new_catalog_entry_and_leaves_it_disabled_unanswered(
    tmp_path: Path,
) -> None:
    """The offer is reported either way; only an answer puts files anywhere."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")

    _publish_delta(world)

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["new"] == ["delta"]
    assert payload["enabled"] == [], "an unanswered offer Enables nothing"
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()
    listing = _json(_run(world, "plan", "select"))
    assert "delta" in _checked(listing)
    assert _checked(listing)["delta"] is False


def test_update_enables_a_new_catalog_entry_when_yes_answers_the_offer(
    tmp_path: Path,
) -> None:
    """ADR-0007: the offer is a question, and `--yes` answers every question yes."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _publish_delta(world)

    result = _run(world, "apply", "update", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["new"] == ["delta"]
    assert payload["enabled"] == ["delta"]
    assert "delta" in payload["intended"]
    assert "delta" in payload["confirmed"]
    assert (world["home"] / ".claude" / "skills" / "delta" / "SKILL.md").is_file()


def test_update_enables_a_new_catalog_entry_in_the_layer_it_was_aimed_at(
    tmp_path: Path,
) -> None:
    """The offer belongs to the layer being updated, as every other placement does."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "--project", "alpha")
    _publish_delta(world)

    result = _run(world, "apply", "update", "--project", "--yes")

    assert result.returncode == 0, result.stderr
    assert _json(result)["enabled"] == ["delta"]
    assert (world["project"] / ".claude" / "skills" / "delta" / "SKILL.md").is_file()
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()


def test_update_reports_a_new_entry_that_never_landed(tmp_path: Path) -> None:
    """A new entry is placed by the path every placement takes, disk and all."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _publish_delta(world)

    result = _run(world, "apply", "update", "--yes", skip=["delta"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["enabled"] == ["delta"]
    assert [item["name"] for item in payload["failed"]] == ["delta"]


def test_update_re_checks_what_a_newly_enabled_skill_needs(tmp_path: Path) -> None:
    """A skill Enabled by the offer is as much the layer's business as any other."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    entries = [
        _entry("alpha", "code"),
        _entry(
            "delta",
            "agents",
            binaries=["definitely-not-a-binary-kntnt"],
            capabilities=["subagents"],
            description="The delta skill.",
        ),
    ]
    _write(world["source"] / "skills" / "kntnt" / "catalog.json", _catalog(entries))
    _write(
        world["source"] / "skills" / "agents" / "delta" / "SKILL.md",
        _skill_md(
            "delta",
            description="The delta skill.",
            binaries=["definitely-not-a-binary-kntnt"],
            capabilities=["subagents"],
        ),
    )

    result = _run(world, "apply", "update", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["enabled"] == ["delta"]
    assert [item["name"] for item in payload["unsatisfied"]] == [
        "definitely-not-a-binary-kntnt"
    ]
    assert [item["skill"] for item in payload["capabilities"]] == ["delta"]


def test_update_enables_nothing_new_where_there_was_no_snapshot(
    tmp_path: Path,
) -> None:
    """No *before* is no discovery, so `--yes` has nothing to say yes to."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    (world["here"] / "catalog.json").unlink()

    result = _run(world, "apply", "update", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["new"] == []
    assert payload["enabled"] == []
    assert not (world["home"] / ".claude" / "skills" / "alpha").exists()


def test_update_enables_nothing_new_when_the_origin_is_unreachable(
    tmp_path: Path,
) -> None:
    """A fallback Catalog is the snapshot itself, so it can carry nothing new."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _unreachable_origin(world)

    result = _run(world, "apply", "update", "--yes")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["catalog_refreshed"] is False
    assert payload["new"] == []
    assert payload["enabled"] == []


def test_plan_update_reports_the_new_entries_the_question_is_about(
    tmp_path: Path,
) -> None:
    """The question is asked before the write, so the plan carries what it names."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _publish_delta(world)

    result = _run(world, "plan", "update")

    assert result.returncode == 0, result.stderr
    assert _json(result)["new"] == ["delta"]
    stored = json.loads((world["here"] / "catalog.json").read_text(encoding="utf-8"))
    assert "delta" not in [entry["name"] for entry in stored["skills"]], (
        "a plan writes nothing, the snapshot included"
    )
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()


def test_the_update_body_asks_the_offer_and_names_what_answers_it() -> None:
    """The question lives in the body: a script run non-interactively cannot ask."""

    steps = (REPO_ROOT / "skills" / "kntnt" / "steps" / "update.md").read_text(
        encoding="utf-8"
    )
    assert "`new`" in steps, "the body has to name the entries the question is about"
    assert "`enabled`" in steps, "and what the run then Enabled"
    assert "--yes" in steps, "and the flag that carries the answer to the script"
    options = _options("update")
    option = options.partition("**--yes**")[2].partition("\n\n**")[0]
    assert "enable" in option.lower(), "the manpage documents what the flag now does"


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


def test_check_refuses_a_declaration_it_cannot_read(tmp_path: Path) -> None:
    """The shape a previous release wrote must not read as *requires nothing*.

    ADR-0061 moved the four Dependency lists into one flat prefixed namespace,
    and a Manager that predates it finds no `kntnt.` key in the shape that
    replaced it. `check` answered that with exit 0 and two empty lists, which
    is what a skill genuinely requiring nothing answers with — so the binary
    half of the gate reported nothing missing and the Capability half handed
    the agent nothing to confirm, and the skill ran (issue #68).
    """

    world = _world(tmp_path)
    skill = world["project"] / "skill"
    _write(
        skill / "SKILL.md",
        _skill_md_with_metadata(
            "alpha",
            "metadata:\n"
            "  internal: true\n"
            "  kntnt:\n"
            "    binaries:\n"
            "      - definitely-not-a-binary-kntnt\n"
            "    capabilities:\n"
            "      - subagents\n",
        ),
    )

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 2, result.stdout
    payload = _json(result)
    assert payload["ok"] is False
    assert payload["capabilities"] == []
    entry = payload["unsatisfied"][0]
    assert entry["kind"] == "declaration"
    assert "metadata" in entry["how"], "the fault reaches the user, not just a stop"
    assert "/kntnt update" in entry["how"], "and so does the remedy for it"


def test_check_refuses_every_declaration_it_cannot_read(tmp_path: Path) -> None:
    """The gate refuses each form generation refuses, and for the same reason.

    Generation is the gate on an unreadable marker in the repository; nothing
    was the gate on one already installed. The two lists are deliberately the
    same, minus the values `skill_deps` could already refuse: whatever shape
    leaves this Manager without a readable declaration, the answer is a refusal
    rather than four empty lists (issue #68).
    """

    forms = (
        ("no metadata at all", ""),
        ("a metadata that is not a mapping", "metadata: hello\n"),
        ("a metadata holding no kntnt. key", 'metadata:\n  internal: "true"\n'),
        (
            "the nested block ADR-0061 replaced",
            "metadata:\n  kntnt:\n    binaries: git\n",
        ),
    )

    for index, (label, metadata) in enumerate(forms):
        root = tmp_path / f"form{index}"
        root.mkdir()
        world = _world(root)
        skill = world["project"] / "skill"
        _write(skill / "SKILL.md", _skill_md_with_metadata("alpha", metadata))

        result = _run(world, "check", "--here", str(skill))

        assert result.returncode == 2, f"{label}: {result.stdout}"
        payload = _json(result)
        assert payload["ok"] is False, label
        assert payload["unsatisfied"][0]["kind"] == "declaration", label


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


def test_help_no_longer_answers_for_a_skill(tmp_path: Path) -> None:
    """`/kntnt help <skill>` is withdrawn: it asked the user the wrong question.

    Knowing which collection a skill arrived from is the fact the route made
    the user hold, and both replacements are named where the refusal is read.
    """

    world = _world(tmp_path)

    result = _run(world, "help", "alpha")

    assert result.returncode != 0
    assert "--help" in result.stderr
    assert "select" in result.stderr


def test_manpage_of_an_enabled_skill_is_read_from_disk(tmp_path: Path) -> None:
    """A skill the user has answers out of its own files, origin or no origin."""

    world = _world(tmp_path)
    dest = world["home"] / ".agents" / "skills" / "alpha"
    _write(dest / "SKILL.md", _skill_md("alpha"))
    _write(dest / "help.md", "# alpha\n\nThe Enabled copy's manpage.\n")

    result = _run(world, "manpage", "alpha")

    assert result.returncode == 0, result.stderr
    assert "The Enabled copy's manpage." in result.stdout
    assert "from the collection" not in result.stdout


def test_manpage_of_a_skill_not_enabled_comes_from_the_origin(
    tmp_path: Path,
) -> None:
    """Deciding whether to Enable something never means installing it first."""

    world = _world(tmp_path)

    result = _run(world, "manpage", "alpha")

    assert result.returncode == 0, result.stderr
    assert "The alpha manpage, from the collection." in result.stdout


def test_manpage_writes_nothing_in_either_layer(tmp_path: Path) -> None:
    """Reading is never a side-effecting act, on this route as on the list."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    before = (_tree(world["home"]), _tree(world["project"]), _tree(world["here"]))

    result = _run(world, "manpage", "alpha")

    assert result.returncode == 0, result.stderr
    assert (_tree(world["home"]), _tree(world["project"]), _tree(world["here"])) == (
        before
    )


def test_manpage_says_the_collection_could_not_be_reached(tmp_path: Path) -> None:
    """No copy on disk and no origin is a thing to say, not a page to invent.

    A checked-out collection is unreachable by the file not being there, which
    is how `_unreachable_origin` stages the same failure for the Catalog. The
    remote half of that branch is one network call and stays untested here.
    """

    world = _world(tmp_path)
    (world["source"] / "skills" / "code" / "alpha" / "help.md").unlink()

    result = _run(world, "manpage", "alpha")

    assert result.returncode != 0
    assert not result.stdout.strip()
    assert "alpha" in result.stderr
    assert "help.md" in result.stderr


def test_manpage_refuses_a_name_the_catalog_does_not_carry(tmp_path: Path) -> None:
    """The Catalog settles the name, so nothing typed at the list reaches a path."""

    world = _world(tmp_path)

    result = _run(world, "manpage", "../../etc/passwd")

    assert result.returncode != 0
    assert not result.stdout.strip()


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


def test_update_reports_the_withdrawal_it_made_when_a_refresh_is_refused(
    tmp_path: Path,
) -> None:
    """A transport that refuses a placement does not get to hide a deletion."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", refuse=["alpha"])

    assert result.returncode != 0
    payload = _json(result)
    assert payload["removed"] == [{"name": "gamma", "disk": "removed"}]
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    assert {item["name"] for item in payload["failed"]} == {"kntnt", "alpha"}
    assert payload["confirmed"] == []


def test_a_refused_placement_relays_what_the_transport_said(tmp_path: Path) -> None:
    """The reason a placement was declined is the transport's alone (issue #46).

    Reading the refusal instead of raising it is what keeps the payload — and
    with it the report of the withdrawal the same run already made — but it
    leaves the user told which skills did not land and never why. The words go
    to stderr, where the manager's own errors go, so the payload on stdout
    stays a statement about the disk (ADR-0036).
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", refuse=["alpha"])

    assert result.returncode != 0
    assert "the transport said:" in result.stderr
    assert "error: skills alpha refused" in result.stderr


def test_the_relayed_reason_never_reaches_the_payload(tmp_path: Path) -> None:
    """Two channels, and nothing crossing between them (issue #46).

    The message is somebody else's prose and the payload is the run's own
    account of the disk. A field carrying the one into the other would grow a
    case in every verb's steps, so what has to hold is that the payload gains
    no key and loses none on the run that prints it.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", refuse=["alpha"])

    assert "error: skills alpha refused" in result.stderr
    assert set(_json(result)) == {
        "intended",
        "confirmed",
        "failed",
        "new",
        "enabled",
        "current",
        "removed",
        "catalog_refreshed",
        "unsatisfied",
        "capabilities",
        "layer",
        "directories",
    }
    assert "refused" not in result.stdout


def test_a_refused_removal_relays_what_the_transport_said(tmp_path: Path) -> None:
    """The other mirror, which has swallowed the reason since long before #36."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", refuse=["gamma"])

    assert result.returncode != 0
    assert "the transport said:" in result.stderr
    assert "error: skills gamma refused" in result.stderr


def test_a_removal_the_disk_confirms_says_nothing_the_transport_said(
    tmp_path: Path,
) -> None:
    """A transport that grumbled while doing the job is what the disk absorbs.

    Only a failure has a why to explain. Where the removal is confirmed off
    the disk the run is clean, and a clean run that printed somebody's error
    would be telling the user about nothing at all.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha", "gamma")
    _withdraw(world, "gamma", "text", _SURVIVORS)

    result = _run(world, "apply", "update", grumble=["gamma"])

    assert result.returncode == 0, result.stderr
    assert not (world["home"] / ".claude" / "skills" / "gamma").exists()
    assert _json(result)["removed"] == [{"name": "gamma", "disk": "removed"}]
    assert "the transport said:" not in result.stderr
    assert "ledger" not in result.stderr


def test_an_entry_that_did_not_land_is_still_on_offer(tmp_path: Path) -> None:
    """The offer is the difference against the snapshot, so a failure must not spend it."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _store_snapshot(world)
    _publish_delta(world)
    assert _json(_run(world, "plan", "update"))["new"] == ["delta"]

    failed = _run(world, "apply", "update", "--yes", refuse=["delta"])

    assert failed.returncode != 0
    assert _json(_run(world, "plan", "update"))["new"] == ["delta"]


def test_the_stored_catalog_is_untouched_when_an_entry_did_not_land(
    tmp_path: Path,
) -> None:
    """The mechanism behind the offer standing, asserted on the file itself."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _store_snapshot(world)
    _publish_delta(world)

    _run(world, "apply", "update", "--yes", refuse=["delta"])

    stored = json.loads((world["here"] / "catalog.json").read_text(encoding="utf-8"))
    assert "delta" not in [entry["name"] for entry in stored["skills"]]


def test_an_offer_the_user_declined_is_not_made_twice(tmp_path: Path) -> None:
    """Asked and answered: the entry is `select`'s from then on (ADR-0007)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    _store_snapshot(world)
    _publish_delta(world)

    assert _json(_run(world, "apply", "update"))["new"] == ["delta"]

    assert _json(_run(world, "plan", "update"))["new"] == []
    assert not (world["home"] / ".claude" / "skills" / "delta").exists()


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
            body="Revised upstream.",
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


def test_update_reports_a_declaration_it_cannot_read(tmp_path: Path) -> None:
    """The re-check names an unreadable declaration; it neither hides it nor eats the report.

    ADR-0068 makes an unreadable declaration a refusal rather than four empty
    lists, and Update re-checks every Skill the layer holds — including one the
    origin could not be reached to repair. A refusal raised there would cost
    the user the account of what the same run already deleted and placed, which
    is the one thing ADR-0036 does not allow a verb to lose, so it is reported
    in the payload like any other Unsatisfied Dependency (issue #68).
    """

    world = _digested_world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    installed = world["home"] / ".claude" / "skills" / "alpha" / "SKILL.md"
    installed.write_text("hand edited\n", encoding="utf-8")
    _unreachable_origin(world)

    result = _run(world, "apply", "update")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    entry = next(
        item for item in payload["unsatisfied"] if item["kind"] == "declaration"
    )
    assert entry["name"] == "alpha"
    assert "/kntnt update" in entry["how"]


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


def test_a_verb_takes_yes_only_where_it_can_ask_something(tmp_path: Path) -> None:
    """The inversion of `test_every_verb_accepts_yes`, for the same reason.

    The flag answers a question, so a subcommand that asks none has nothing
    for it to answer and refuses it rather than swallowing it (ADR-0059).
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    gamma = world["source"] / "skills" / "text" / "gamma"

    for args in (
        ("help",),
        ("manpage", "alpha"),
        ("check", "--here", str(gamma)),
        ("catalog",),
    ):
        result = _run(world, *args, "--yes")
        assert result.returncode == 2, f"{args}: {result.stderr}"
        assert "takes no '--yes'" in result.stderr, args

    for invocation in (
        ("plan", "select", "--yes"),
        ("plan", "update", "--yes"),
        ("plan", "uninstall", "--yes"),
        ("apply", "select", "alpha", "--yes"),
        ("apply", "update", "--yes"),
    ):
        result = _run(world, *invocation)
        assert result.returncode == 0, f"{invocation}: {result.stderr}"
        assert "unrecognized arguments" not in result.stderr


def test_collection_skills_are_hidden_from_the_transport() -> None:
    """Under the collection's own key, which is where the spec puts it.

    `metadata` holds one flat namespace shared with every other collection, so
    the flag says whose it is rather than trusting `internal` to be nobody
    else's (issue #52).
    """

    for path in (REPO_ROOT / "skills").glob("*/*/SKILL.md"):
        if path.parent.name == "kntnt":
            continue
        text = path.read_text(encoding="utf-8")
        assert 'kntnt.internal: "true"' in text, (
            f'{path}: every skill declares `kntnt.internal: "true"`, which is'
            f" how it is kept out of ordinary discovery by a reader elsewhere."
            f" The flag is prefixed like every other key of ours because"
            f" `metadata` is one flat namespace and a bare `internal` is a key"
            f" any collection may claim (ADR-0061). See {STANDARD}."
        )


def test_a_skill_runs_the_checker_exactly_when_it_has_something_to_check() -> None:
    """ADR-0012: a Skill with nothing to declare calls no checker.

    The check reads the Skill's own Dependency lists, so on a Skill whose four
    lists are empty it can only ever report an empty one — and running it would
    mean declaring `uv` for the sole purpose of letting the check that proves
    there are no Dependencies execute. The Catalog carries those lists, so it
    is what decides which Skill owes the preamble, and the absence is asserted
    as firmly as the presence: a preamble added back by habit is a Dependency
    nobody declared.
    """

    catalog = json.loads((MANAGER_DIR / "catalog.json").read_text(encoding="utf-8"))
    declares = {
        entry["name"]: any(
            entry[kind] for kind in ("binaries", "skills", "externals", "capabilities")
        )
        for entry in catalog["skills"]
    }

    for path in (REPO_ROOT / "skills").glob("*/*/SKILL.md"):
        if path.parent.name == "kntnt":
            continue
        text = path.read_text(encoding="utf-8")
        assert path.parent.name in declares, (
            f"{path}: the Catalog carries no entry for this skill, so nothing"
            f" says which dependencies it declares. Regenerate the Catalog"
            f" (CONTRIBUTING.md) and run this again. See {STANDARD}."
        )
        if declares[path.parent.name]:
            assert "check --here" in text, (
                f"{path}: this skill declares dependencies, so its body opens"
                f" with the preamble that runs the checker before it does any"
                f" work — a skill owns its dependencies and refuses without"
                f" them rather than installing them (ADR-0012). See {STANDARD}."
            )
            assert "npx skills add Kntnt/skills" in text, (
                f"{path}: the preamble names `npx skills add Kntnt/skills` as"
                f" the fix where no checker is found, so a user meeting the"
                f" refusal is told what to do about it (ADR-0012). See"
                f" {STANDARD}."
            )
        else:
            assert "check --here" not in text, (
                f"{path}: this skill declares no dependency at all, so it calls"
                f" no checker: the call could only ever report an empty list,"
                f" and making it would itself require `uv` — a dependency"
                f" nobody declared (ADR-0012). See {STANDARD}."
            )


def test_every_collection_skill_ships_a_manpage_and_prints_it() -> None:
    """Help lives with the skill: a file it prints, not prose it regenerates.

    The route is read out of the `## Help` section rather than out of the body
    at large. Both tokens it names are named again by the refusal clause every
    body has to carry, so a body read whole answers yes for a skill whose
    `## Help` section was deleted outright — and a skill that can no longer be
    asked what it does is the failure this exists to catch. Asserting the route
    inside the section requires the heading and pins the route to it at once.
    """

    for path in _skill_bodies():
        text = path.read_text(encoding="utf-8")
        assert (path.parent / "help.md").is_file(), (
            f"{path}: every skill ships a `help.md` beside its `SKILL.md`."
            f" Help lives with the skill, so a skill in front of a user can be"
            f" asked what it does without knowing which collection it came"
            f" from (ADR-0044). See {STANDARD}."
        )

        marker = "\n## Help\n"
        assert marker in text, (
            f"{path}: every body carries a `## Help` section, which is where"
            f" the route into the manpage lives. A skill is asked what it does"
            f" by name, so the answer is a section of the body rather than one"
            f" skill's habit (ADR-0044). See {STANDARD}."
        )
        section = text.partition(marker)[2].partition("\n## ")[0]

        assert "`$HERE/help.md`" in section, (
            f"{path}: the `## Help` section prints `$HERE/help.md` verbatim"
            f" rather than summarising it. The manpage is a file a reviewer can"
            f" diff, not prose an agent regenerates each time (ADR-0044,"
            f" ADR-0045). See {STANDARD}."
        )
        assert "--help" in section, (
            f"{path}: the `## Help` section routes `--help` to the manpage,"
            f" which is how every skill of this collection is asked what it"
            f" does (ADR-0044). See {STANDARD}."
        )
        assert "Arguments and Steps" not in text, (
            f"{path}: the body carries only what the agent executes, so its"
            f" sections are the ones it acts on rather than a heading pairing"
            f" two of them (ADR-0046). See {STANDARD}."
        )


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


def test_every_manpage_carries_the_sections_the_standard_requires() -> None:
    """Every page has the conventional core in its conventional order.

    A manpage is written for a reader deciding whether to enable the skill,
    which is a reader who may not have it yet. Presence and order are what this
    check can hold; usefulness remains review judgement.
    """

    for page in _manpages():
        text = page.read_text(encoding="utf-8")
        positions: list[int] = []
        for heading in _MANPAGE_SECTIONS:
            marker = f"\n{heading}\n"
            assert marker in text, (
                f"{page}: this manpage carries no `{heading}`. Every manpage of"
                f" the collection carries {_the_sections()}, while optional"
                f" conventional sections appear only where they have content"
                f" (ADR-0044). See {STANDARD}."
            )
            positions.append(text.index(marker))

        assert positions == sorted(positions), (
            f"{page}: the required sections are not in manpage order. The page"
            f" starts with {_the_sections()}, with relevant optional sections"
            f" between `## DESCRIPTION` and `## DEPENDENCIES`. See {STANDARD}."
        )


def test_every_manpage_uses_a_conventional_title_name_and_heading_case() -> None:
    """Markdown title metadata and `NAME` make each page identifiable."""

    for page in _manpages():
        text = page.read_text(encoding="utf-8")
        name = _manpage_name(page)
        name_lines = _section(text, "## NAME", page).strip().splitlines()

        assert text.startswith(f"# {name}\n"), (
            f"{page}: the top-level title is not `# {name}`, the Markdown"
            f" equivalent of the title metadata a roff manpage carries. See"
            f" {STANDARD}."
        )
        assert len(name_lines) == 1 and name_lines[0].startswith(f"{name} - "), (
            f"{page}: `NAME` is one line in the form `{name} - concise"
            f" summary`, which is the conventional indexed identity of a"
            f" manpage. See {STANDARD}."
        )
        assert not name_lines[0].endswith("."), (
            f"{page}: the `NAME` summary is a phrase and carries no final"
            f" period. See {STANDARD}."
        )

        for heading in (line for line in text.splitlines() if line.startswith("## ")):
            assert heading == heading.upper(), (
                f"{page}: `{heading}` is not an uppercase manpage section"
                f" heading. Sentence case is reserved for subsections. See"
                f" {STANDARD}."
            )


def test_every_manpage_synopsis_and_options_describe_the_same_flags() -> None:
    """An absent `OPTIONS` section means the page accepts no option."""

    for manpage in _manpages():
        page = manpage.read_text(encoding="utf-8")
        synopsis = _flags(_section(page, "## SYNOPSIS", manpage))
        options = _optional_section(page, "## OPTIONS")
        documented = _flags(options)

        assert synopsis == documented, (
            f"{manpage}: `SYNOPSIS` names {sorted(synopsis)} while `OPTIONS`"
            f" names {sorted(documented)}. They are one grammar. See"
            f" {STANDARD}."
        )
        assert bool(options) == bool(documented), (
            f"{manpage}: an `OPTIONS` section exists without an option. Omit"
            f" an empty conventional section instead of explaining its"
            f" absence. See {STANDARD}."
        )


def test_every_manpage_documents_the_invocation_envelope() -> None:
    """Every addressed help page exposes context without making it an option."""

    # Hold the context surface and the minimum explanation every page carries.
    suffix = "[**--** *INSTRUCTION*]"
    required = (
        "Contextual Instruction",
        "Conversation Context",
        "Redundant but applicable guidance is valid",
        "Before the first side effect, the Skill uses available read-only checks",
        "exact partial outcome",
        "reserved separator",
        "syntax refusal",
        "context refusal",
    )

    # Discover every page so future command paths inherit the same contract.
    for manpage in _manpages():
        # Read the two public sections that expose the Envelope.
        text = manpage.read_text(encoding="utf-8")
        synopsis = _section(text, "## SYNOPSIS", manpage)
        envelope = _section(text, "## INVOCATION ENVELOPE", manpage)

        # Keep the separator visible as a suffix and absent from the option set.
        forms = [line for line in synopsis.splitlines() if line]
        assert forms and all(line.endswith(suffix) for line in forms), (
            f"{manpage}: every formal form exposes the optional context suffix"
            f" so callers can distinguish guidance from strict grammar"
            f" (ADR-0078). See {STANDARD}."
        )
        assert all(phrase in envelope for phrase in required), (
            f"{manpage}: the envelope section does not explain the complete"
            f" caller-visible contract required by ADR-0078. See {STANDARD}."
        )
        assert "**--**" not in _optional_section(text, "## OPTIONS"), (
            f"{manpage}: the reserved separator is not an option and therefore"
            f" never belongs in `## OPTIONS` (ADR-0078). See {STANDARD}."
        )


# The two Markdown files every skill ships at its root: the body the harness
# loads and the skill-level manpage. A skill with subcommands may additionally
# carry their manpages under `help/`; other Markdown is agent reference material.
_ALWAYS_IN_THE_ROOT = frozenset({"SKILL.md", "help.md"})


def test_what_a_skill_opens_on_demand_lives_under_references() -> None:
    """ADR-0063: the spec's directory says what a flat root cannot.

    The on-demand files are discovered rather than listed, because a list
    maintained by hand goes stale without saying so: a skill it never gained
    an entry for has its placement held to nothing at all. A skill ships its
    body, its manpages, its engine where it has one, and the files its body
    opens when the situation arises. Subcommand manpages are a user-facing
    tree under `help/`; every other Markdown file beyond the two root files is
    one of the last kind, whether or not anybody remembered to write it down.
    """

    for directory in _shipped_skills():
        for path in sorted(directory.rglob("*.md")):
            if path.parent == directory and path.name in _ALWAYS_IN_THE_ROOT:
                continue
            if directory / "help" in path.parents:
                continue
            assert directory / "references" in path.parents, (
                f"{path}: this is neither the body nor a manpage, so it is a"
                f" file the body opens only when the situation arises, and it"
                f" belongs under `references/` — the specification's own"
                f" directory for it, which is what tells a reader it is not the"
                f" manpage a user is meant to read (ADR-0063). See {STANDARD}."
            )


def test_a_skills_python_helpers_live_under_scripts() -> None:
    """The local resource shape separates helpers from instructions."""

    for directory in _shipped_skills():
        for path in sorted(directory.rglob("*.py")):
            assert directory / "scripts" in path.parents, (
                f"{path}: an executable helper used only by this Skill belongs"
                f" under its `scripts/`, mirroring the Collection Library's"
                f" resource structure (ADR-0063, ADR-0076). See {STANDARD}."
            )


def test_the_paths_the_collection_publishes_are_left_where_they_are() -> None:
    """ADR-0063's three deviations, each a published address rather than layout.

    A manpage is fetched at `skills/<category>/<name>/help.md` and the Catalog
    at `skills/kntnt/catalog.json` (ADR-0044); the Manager's `steps/` is what
    the agent carries out rather than what it consults (ADR-0046).
    """

    for directory in _shipped_skills():
        assert (directory / "help.md").is_file(), (
            f"{directory}: a manpage is fetched at"
            f" `skills/<category>/<name>/help.md`, so it stays in the skill's"
            f" root rather than moving under `references/` with the files a"
            f" body opens on demand (ADR-0044, ADR-0063). See {STANDARD}."
        )

    manager = REPO_ROOT / "skills" / "kntnt"
    assert (manager / "help.md").is_file()
    assert (manager / "catalog.json").is_file()
    assert (manager / "harness-paths.json").is_file()
    assert (manager / "steps").is_dir()
    assert (manager / "help").is_dir()


def test_the_collection_library_separates_references_from_scripts() -> None:
    """Shared implementation has one owner and mirrors a Skill's resources."""

    library = REPO_ROOT / "skills" / "kntnt" / "library"

    # Hold the shared destinations and the absence of their old local copies.
    assert (library / "references" / "changelog.md").is_file()
    assert (library / "scripts" / "ship.py").is_file()
    assert not (
        REPO_ROOT / "skills" / "code" / "commit" / "references" / "changelog.md"
    ).exists()
    assert not (
        REPO_ROOT / "skills" / "code" / "commit" / "scripts" / "ship.py"
    ).exists()


def test_the_collection_library_carries_one_delivery_contract() -> None:
    """Several Skills deliver a Text Artifact, so the rule has one owner.

    Delivery is stated once, in the Library, rather than in whichever Skill
    happened to need it first: a copy under one consumer would make that Skill
    the implementation owner of its peers, and a copy under each would make one
    rule several things to keep true (ADR-0076, ADR-0091).
    """

    library = REPO_ROOT / "skills" / "kntnt" / "library"

    # Hold the shared destination and the absence of any private copy of it.
    assert (library / "references" / "delivery.md").is_file(), (
        f"{library / 'references' / 'delivery.md'}: the Output Target and"
        f" In-place Editing contract is read by every Skill that delivers a"
        f" Text Artifact, so it belongs to the Collection Library"
        f" (ADR-0076). See {STANDARD}."
    )
    private = [
        directory
        for directory in _shipped_skills()
        if (directory / "references" / "delivery.md").exists()
    ]
    assert private == [], (
        f"{private}: the delivery contract has several consumers, so a local"
        f" copy makes one Skill the implementation owner of its peers"
        f" (ADR-0076). See {STANDARD}."
    )


def test_the_shared_delivery_contract_binds_no_consumers_grammar() -> None:
    """A shared contract states behaviour, never a consumer's flag spelling.

    Each editorial Skill declares its own Formal Invocation, and a flag written
    into the shared document would either be a second copy of that grammar or a
    name a later Skill is not free to choose (ADR-0091).
    """

    contract = (
        REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "delivery.md"
    ).read_text(encoding="utf-8")

    # Match a long-option spelling, never the reserved standalone separator.
    flags = sorted(set(re.findall(r"(?<![\w-])--[A-Za-z][\w-]*", contract)))
    assert flags == [], (
        f"{flags}: the shared delivery contract names a consumer's flag"
        f" spelling, which binds a grammar the consuming Skill owns"
        f" (ADR-0091). See {STANDARD}."
    )

    # Hold the domain vocabulary and the collision sequence it is read for.
    assert "Output Target" in contract
    assert "In-place Editing" in contract
    assert "`my-file.md`, `my-file-2.md`, `my-file-3.md`" in contract


def test_the_collection_library_carries_the_editorial_base_contract() -> None:
    """One statement of what a first draft has to be, read from both sides.

    Write drafts against the base contract and Redline reviews against the same
    document, so it belongs to neither of them. A copy under one would make that
    Skill the owner of its peer's rules, and a copy under each would let a
    requirement and its review disagree about what was required (ADR-0076,
    ADR-0095).
    """

    editorial = REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "editorial"

    assert (editorial / "base.md").is_file(), (
        f"{editorial / 'base.md'}: the normative outcomes a first draft has to"
        f" meet are stated once, in the Collection Library, because the Skill"
        f" that writes and the Skill that reviews read the same statement"
        f" (ADR-0076, ADR-0095). See {STANDARD}."
    )

    private = [
        directory
        for directory in _shipped_skills()
        if (directory / "references" / "editorial").exists()
    ]
    assert private == [], (
        f"{private}: the editorial contract has several consumers, so a local"
        f" copy makes one Skill the implementation owner of its peers"
        f" (ADR-0076, ADR-0095). See {STANDARD}."
    )

    contract = (editorial / "base.md").read_text(encoding="utf-8")

    # Match a long-option spelling, never the reserved standalone separator.
    flags = sorted(set(re.findall(r"(?<![\w-])--[A-Za-z][\w-]*", contract)))
    assert flags == [], (
        f"{flags}: the shared base contract names a consumer's flag spelling,"
        f" which binds a grammar the consuming Skill owns (ADR-0095). See"
        f" {STANDARD}."
    )

    # Hold the register baseline and the thing that overrides it, which is the
    # pair a genre resource is written against.
    assert "newspaper" in contract and "magazine" in contract, (
        f"{editorial / 'base.md'}: the base contract states the register"
        f" baseline a draft starts from (ADR-0095). See {STANDARD}."
    )
    assert "genre, audience, and purpose" in contract.lower(), (
        f"{editorial / 'base.md'}: the base contract states that genre,"
        f" audience, and purpose override the register baseline, or a letter"
        f" comes out as a news article (ADR-0095). See {STANDARD}."
    )


def test_the_general_genre_ships_beside_the_contract_it_extends() -> None:
    """An unspecified content type still gets a complete genre contract.

    `general` is the default, so it is the genre a Skill loads when nobody
    selected one. The set of installed genres is the directory itself, which is
    what makes adding one a single-resource addition (ADR-0095).
    """

    genres = (
        REPO_ROOT
        / "skills"
        / "kntnt"
        / "library"
        / "references"
        / "editorial"
        / "genres"
    )

    assert (genres / "general.md").is_file(), (
        f"{genres / 'general.md'}: `general` is the default genre, so it ships"
        f" as a resource with a complete contract rather than as the absence of"
        f" one (ADR-0095). See {STANDARD}."
    )


def test_a_review_extension_is_addressable_apart_from_the_base_half() -> None:
    """A Skill that only writes must not pay for the guidance it cannot use.

    The review half of a genre or technique is a file of its own beside the
    base half, `<name>.review.md`, rather than a section inside it: a Skill
    resolving a genre by name loads the base half and stops, and a reviewing
    Skill asks for the extension by its own name (ADR-0095).
    """

    editorial = REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "editorial"
    resources = [
        path for path in sorted(editorial.rglob("*.md")) if path.name != "README.md"
    ]

    # A glob that matched nothing would pass every assertion below it.
    assert resources

    for path in resources:
        if path.name.endswith(".review.md"):
            base = path.with_name(path.name[: -len(".review.md")] + ".md")
            assert base.is_file(), (
                f"{path}: a review extension extends a base half, and"
                f" {base.name} is not there to extend (ADR-0095). See"
                f" {STANDARD}."
            )
            continue
        assert "\n## Review\n" not in path.read_text(encoding="utf-8"), (
            f"{path}: the review half sits inside the base half, so a Skill"
            f" that only writes loads it too. Write it as"
            f" `{path.stem}.review.md` beside this file (ADR-0095). See"
            f" {STANDARD}."
        )


# The editorial resources, and the genres and techniques a user selects among
# by name. A Skill resolves a selection against the directory itself, so these
# names are no registry anything reads at run time (ADR-0095): they are the
# floor the suite holds the Collection to, so that a resource renamed or gone
# is caught here rather than by the user who meets a refusal instead of a
# draft.
EDITORIAL = REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "editorial"
INSTALLED_GENRES = ("general", "article", "report", "press-release")
INSTALLED_TECHNIQUES = ("abt", "pac")

# The resources shipped with review guidance of their own. `general` is the
# default genre and carries none yet, and a base half standing alone is a
# complete resource (ADR-0095).
REVIEWED_RESOURCES = (
    "genres/article",
    "genres/report",
    "genres/press-release",
    "techniques/abt",
    "techniques/pac",
)


def _editorial_resources() -> list[Path]:
    """Every genre and technique base half, review extensions excluded."""

    resources = [
        path
        for directory in ("genres", "techniques")
        for path in sorted((EDITORIAL / directory).glob("*.md"))
        if not path.name.endswith(".review.md")
    ]

    # A glob that matched nothing would pass every assertion over it.
    assert resources
    return resources


def test_the_genres_and_techniques_a_user_selects_ship_in_the_library() -> None:
    """Selection is worth having only where there is something to select.

    Genre is more than its default and technique more than none because these
    resources sit beside the base contract, where every Skill that reads the
    contract reaches them on the same terms (ADR-0076). The directory is the
    installed set, so a name with no file is a refusal rather than a default
    quietly supplied in its place (ADR-0095).
    """

    for name in INSTALLED_GENRES:
        path = EDITORIAL / "genres" / f"{name}.md"
        assert path.is_file(), (
            f"{path}: `{name}` is a genre this Collection installs, and the"
            f" directory is what a Skill resolves a selection against. Absent"
            f" here, the value is refused wherever anybody selects it"
            f" (ADR-0095). See {STANDARD}."
        )

    for name in INSTALLED_TECHNIQUES:
        path = EDITORIAL / "techniques" / f"{name}.md"
        assert path.is_file(), (
            f"{path}: `{name}` is a technique this Collection installs, and a"
            f" technique applies because it was selected. Absent here, there"
            f" is nothing to select and nothing states its arc (ADR-0095). See"
            f" {STANDARD}."
        )


def test_each_selectable_resource_carries_its_review_guidance_beside_it() -> None:
    """Diagnostics ship with the requirement they diagnose, and separately.

    A resource whose base half states requirements and whose review half is
    missing leaves a reviewing Skill to invent the diagnostics, which is how a
    review acquires a target the writer was never told about. The extension is
    a file of its own so that a Skill which only writes never loads it
    (ADR-0095).
    """

    for name in REVIEWED_RESOURCES:
        base = EDITORIAL / f"{name}.md"
        extension = EDITORIAL / f"{name}.review.md"
        assert base.is_file(), (
            f"{base}: the base half is what a draft is written against, and"
            f" the review half below extends it (ADR-0095). See {STANDARD}."
        )
        assert extension.is_file(), (
            f"{extension}: `{name}` states requirements and ships no review"
            f" guidance for them, leaving a reviewing Skill to invent its own"
            f" diagnostics for rules somebody else wrote (ADR-0095). See"
            f" {STANDARD}."
        )


def test_a_genre_or_technique_says_what_it_is_before_it_says_what_it_asks() -> None:
    """Listing what is installed reads the top of a file and stops.

    The directory is the installed set, so anything showing a user what they
    may select opens each resource and reads its name and its opening
    paragraph. A file that begins with its rules makes that a choice between
    showing nothing and loading everything (ADR-0095).
    """

    for path in _editorial_resources():
        lines = path.read_text(encoding="utf-8").splitlines()

        assert lines and re.fullmatch(r"# \S.*", lines[0]), (
            f"{path}: a resource opens with `# <Name>`, which is what names it"
            f" wherever the installed set is shown (ADR-0095). See {STANDARD}."
        )

        # The summary is whatever prose stands between the title and the first
        # section heading.
        summary: list[str] = []
        for line in lines[1:]:
            if line.startswith("## "):
                break
            summary.append(line)
        assert any(line.strip() for line in summary), (
            f"{path}: the title is followed straight by a section, so a Skill"
            f" showing what is installed has nothing to show but the name"
            f" (ADR-0095). See {STANDARD}."
        )


def test_a_genre_or_technique_binds_no_consumers_grammar() -> None:
    """A shared resource states an outcome, never a flag spelling.

    Every editorial Skill declares its own Formal Invocation, so an option
    named in a resource all of them read is either a second copy of that
    grammar or a name the next Skill is not free to choose (ADR-0091,
    ADR-0095).
    """

    for path in sorted(EDITORIAL.rglob("*.md")):
        if path.name == "README.md":
            continue

        # Match a long-option spelling, never the reserved separator.
        flags = sorted(
            set(
                re.findall(
                    r"(?<![\w-])--[A-Za-z][\w-]*", path.read_text(encoding="utf-8")
                )
            )
        )
        assert flags == [], (
            f"{flags}: {path} names a consumer's flag spelling, which binds a"
            f" grammar the consuming Skill owns (ADR-0095). See {STANDARD}."
        )


def test_no_editorial_resource_pins_a_rule_to_one_installed_language() -> None:
    """The editorial half is language-independent, and the split is the point.

    What a genre or a technique asks for holds in every language the
    Collection installs; what writing well in one language takes lives in that
    language's own resource, which is the only place a Skill looks for it
    (ADR-0087, ADR-0095). A rule here naming one language would be applied to
    drafts written in the others.
    """

    languages = REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "languages"
    codes = sorted(
        path.stem for path in languages.glob("*.md") if path.name != "README.md"
    )

    # A rename in the languages directory must not silently empty this check.
    assert codes

    for path in sorted(EDITORIAL.rglob("*.md")):
        if path.name == "README.md":
            continue

        text = path.read_text(encoding="utf-8")
        named = [code for code in codes if re.search(rf"\b{re.escape(code)}\b", text)]
        assert named == [], (
            f"{named}: {path} pins a rule to a single Language Resource. The"
            f" editorial contract is language-independent, and guidance true"
            f" of one language belongs in that language's resource (ADR-0087,"
            f" ADR-0095). See {STANDARD}."
        )


def _base_contract_section(name: str) -> str:
    """The body of one `## ` section of the shared base contract.

    Where a rule stands in that document is part of the rule: a requirement
    about what may be claimed, filed under `Words`, has been put away from the
    requirement it qualifies and from the reader who needs it (ADR-0095).
    """

    text = (EDITORIAL / "base.md").read_text(encoding="utf-8")
    for section in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        heading, _, body = section.partition("\n")
        if heading.strip() == name:
            return body

    return ""


def test_the_base_contract_makes_circumstantial_detail_a_claim() -> None:
    """The shape an invented fact takes when it reads as prose.

    A duration, a manner, a motive, an absence, a state of affairs given as
    background: each asserts something about the case the text reports, and
    each survives a writer's own reading precisely because it does not look
    like an assertion. Unstated, the requirement that every claim be supported
    is read as covering figures and attributions alone, which is the form every
    Source Fidelity failure the Claude-family evaluation found actually took
    (issue #138).
    """

    claims = _base_contract_section("Claims")

    # A contract reworded out of this heading would leave nothing to judge and
    # would pass every assertion below it.
    assert claims, (
        f"{EDITORIAL / 'base.md'}: the contract states what a claim owes its"
        f" reader under `## Claims`, and there is no such section to read"
        f" (ADR-0095). See {STANDARD}."
    )

    lowered = claims.lower()

    assert "circumstantial detail" in lowered, (
        f"{EDITORIAL / 'base.md'}: the `Claims` section requires support for"
        f" every claim and never says that circumstantial detail about the"
        f" reported case is one, so the detail that reads as prose is the"
        f" detail a draft invents (issue #138). See {STANDARD}."
    )

    unnamed = [
        form
        for form in ("duration", "manner", "motive", "absence", "background")
        if form not in lowered
    ]
    assert unnamed == [], (
        f"{unnamed}: forms circumstantial detail takes that the `Claims`"
        f" section does not name, each of them observed as an unsupported fact"
        f" in a delivered draft (issue #138). See {STANDARD}."
    )


def test_the_base_contract_settles_a_stated_length_against_the_material() -> None:
    """A length that was asked for, and material too thin to reach it.

    Both fixtures that failed Source Fidelity stated a word count their
    material could not fill, and the drafts reached it by supplying detail the
    brief did not carry. Nothing said which of the two gives way. The rule is
    therefore stated beside the requirement it protects, and it settles the
    conflict in one direction: the length gives way, and the shortfall is named
    rather than filled (issue #138).
    """

    claims = _base_contract_section("Claims").lower()

    assert claims

    for clause in (
        "never a licence to add to it",
        "the length the material supports",
        "what further material would close",
    ):
        assert clause in claims, (
            f"{EDITORIAL / 'base.md'}: the `Claims` section leaves a stated"
            f" length free to license material the source does not carry,"
            f" which is the conflict every observed failure was decided the"
            f" wrong way round ({clause!r} unstated, issue #138). See"
            f" {STANDARD}."
        )


def test_write_ships_in_the_editorial_category_and_invokes_no_peer() -> None:
    """Running an editorial pipeline stays the user's separate choice.

    Write produces one first draft and stops. Invoking Redline or Proofread
    from inside it would make the pipeline the default and the single draft the
    exception, and would spend a reviewing Skill's context on every draft
    whether or not anybody wanted one reviewed (ADR-0088).
    """

    body = REPO_ROOT / "skills" / "editorial" / "write" / "SKILL.md"

    assert body.is_file(), (
        f"{body}: Write ships in the Collection's editorial category. See {STANDARD}."
    )

    # The pointer shape a Skill follows a declared peer Dependency through.
    nested = re.compile(r"\$HERE/\.\./([A-Za-z0-9_-]+)/SKILL\.md")
    called = sorted(set(nested.findall(body.read_text(encoding="utf-8"))))
    assert called == [], (
        f"{called}: Write invokes a peer Skill, which turns one first draft"
        f" into an editorial pipeline nobody asked for (ADR-0088). See"
        f" {STANDARD}."
    )

    assert '\n  kntnt.skills: ""\n' in body.read_text(encoding="utf-8"), (
        f"{body}: Write declares a Skill Dependency, and it invokes no peer"
        f" (ADR-0088). See {STANDARD}."
    )


def test_write_loads_only_what_a_first_draft_is_written_against() -> None:
    """Concision is the point of the wave, and it is a loading rule.

    Write loads the base contract, the selected genre, the composition scope of
    the resolved Language Resource, and the optional technique. Review,
    anti-slop, and mechanics guidance belong to the Skills contracted to act on
    them, and a Skill that loads guidance it may not act on has spent the
    context the split was made to save (ADR-0095).
    """

    directory = REPO_ROOT / "skills" / "editorial" / "write"
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(directory.rglob("*.md"))
    )

    assert "$LIBRARY/references/editorial/base.md" in text, (
        f"{directory}: Write never reaches the base contract, so nothing says"
        f" what its draft is written against (ADR-0095). See {STANDARD}."
    )
    assert "--scope=composition" in text, (
        f"{directory}: Write never asks the resolver for the composition"
        f" scope, which is the language-specific guidance a draft is written"
        f" with (ADR-0087, ADR-0095). See {STANDARD}."
    )
    for scope in ("review", "anti-slop", "mechanics"):
        assert f"--scope={scope}" not in text, (
            f"{directory}: Write asks for the {scope} scope, which belongs to"
            f" the Skills contracted to act on it (ADR-0087, ADR-0095). See"
            f" {STANDARD}."
        )


def test_write_accounts_for_what_it_did_with_the_material() -> None:
    """A run reporting its own fidelity has made a claim about the draft.

    Every Source Fidelity failure the Claude-family evaluation found shipped
    under a report saying that every claim traced to the brief. So the account
    is answerable to the contract the draft is written under: it says where the
    material stopped when the draft is short of a stated length, and asserts
    nothing about the draft that the run has not established. It remains an
    account and never a second pass — Write still stops at the first draft
    (ADR-0088, issue #138).
    """

    directory = REPO_ROOT / "skills" / "editorial" / "write"
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(directory.rglob("*.md"))
    )

    assert "short of a stated length" in text, (
        f"{directory}: nothing tells a run to say where the material stopped"
        f" when the draft comes in under a length the brief asked for, which"
        f" is the one moment a draft is under pressure to invent (issue #138)."
        f" See {STANDARD}."
    )

    assert "fidelity it has not established" in text, (
        f"{directory}: the run's account may still report the draft as"
        f" faithful without having checked, which is what every failing run"
        f" did (issue #138). See {STANDARD}."
    )

    # The account says what the run did with the material; it never reviews the
    # draft it has just written (ADR-0088).
    assert "perform neither, and offer neither as a next step" in text, (
        f"{directory}: Write no longer stops at the first draft, so the"
        f" account of a run has become the review pass this Skill does not"
        f" have (ADR-0088). See {STANDARD}."
    )


# The Skill this wave's mechanical pass ships as, read at the one seam a test
# has: the body is the whole of what the agent executes (ADR-0046).
PROOFREAD = REPO_ROOT / "skills" / "editorial" / "proofread" / "SKILL.md"


def test_proofread_reads_only_the_mechanics_scope_of_a_language_resource() -> None:
    """Scoping buys frugality, and the body is where it is spent or wasted.

    A Language Resource carries four scopes and the resolver returns only the
    ones a caller asks for (ADR-0087). Proofread may act on mechanics alone, so
    a body asking for composition, review, or anti-slop guidance would be
    paying context for rules it is contracted not to apply — and holding rules
    it may not act on is how a mechanical pass drifts into a rewrite.
    """

    text = PROOFREAD.read_text(encoding="utf-8")

    assert "$LIBRARY/scripts/languages.py" in text, (
        f"{PROOFREAD}: the body resolves its language through the Collection"
        f" Library's resolver rather than reading the resources itself. The"
        f" selection is deterministic and shared by every editorial Skill,"
        f" which is why it is a script and not prose (ADR-0087, ADR-0076). See"
        f" {STANDARD}."
    )
    assert "--scope=mechanics" in text, (
        f"{PROOFREAD}: the body asks the resolver for no scope, so it either"
        f" loads nothing language-specific or loads the resource whole. It"
        f" asks for `mechanics`, which is the one scope it may act on"
        f" (ADR-0087). See {STANDARD}."
    )
    for scope in ("composition", "review", "anti-slop"):
        assert f"--scope={scope}" not in text, (
            f"{PROOFREAD}: the body asks the resolver for the `{scope}` scope,"
            f" which this Skill is contracted not to apply. A caller asks for"
            f" the scopes it can act on and is given those and no others"
            f" (ADR-0087). See {STANDARD}."
        )


def test_proofread_delivers_through_the_shared_output_contract() -> None:
    """The rule has one owner, and a consumer follows it rather than repeating it.

    Where a result goes, when a source file may be replaced by it, and what
    happens when nothing changed are stated once in the Collection Library
    (ADR-0091). A Skill restating them in its own body is a second copy free to
    drift from the one every other Skill delivers by.
    """

    text = PROOFREAD.read_text(encoding="utf-8")

    assert "$LIBRARY/references/delivery.md" in text, (
        f"{PROOFREAD}: the body delivers its Text Artifact without following"
        f" the Collection Library's delivery contract, so the Output Target,"
        f" In-place Editing, its refusals, and the no-change status are this"
        f" Skill's own account of rules it shares with its peers (ADR-0091,"
        f" ADR-0076). See {STANDARD}."
    )
    assert "`my-file-2.md`" not in text, (
        f"{PROOFREAD}: the body spells out the shared collision sequence"
        f" instead of following the contract that owns it, which is one rule"
        f" made into two things to keep true (ADR-0091). See {STANDARD}."
    )


# The Skill this wave's editorial review ships as, read at the one seam a test
# has: the body is the whole of what the agent executes (ADR-0046).
REDLINE = REPO_ROOT / "skills" / "editorial" / "redline" / "SKILL.md"

# Its manpage, and the brief a correcting subagent is started from. The brief
# is a file only this Skill opens, so it lives under the Skill's `references/`
# (ADR-0063), and it is the whole of what reaches a subagent that has no
# history of its own to fall back on.
REDLINE_HELP = REDLINE.parent / "help.md"
REDLINE_CORRECTION = REDLINE.parent / "references" / "correction.md"

# The shared catalogue of machine-sounding prose, and the seven patterns the
# specification requires it to carry.
ANTI_SLOP = (
    REPO_ROOT
    / "skills"
    / "kntnt"
    / "library"
    / "references"
    / "editorial"
    / "anti-slop.md"
)
SLOP_PATTERNS = (
    "false contrast",
    "empty opening",
    "importance inflation",
    "vague attribution",
    "synonym cycling",
    "robotic rhythm",
    "generic conclusion",
)


def test_redline_reviews_a_text_artifact_that_nothing_here_wrote() -> None:
    """Provenance is an optimisation, never an entry condition (ADR-0088).

    Redline takes any Text Artifact — Write's, a human's, or one produced
    somewhere else entirely. Handoff Metadata is read where a recognized map
    exists and is never required and never created where it is absent, or a
    reviewing Skill would only be usable as the second stage of a pipeline.
    """

    assert REDLINE.is_file(), (
        f"{REDLINE}: Redline ships in the Collection's editorial category. See"
        f" {STANDARD}."
    )

    text = REDLINE.read_text(encoding="utf-8")

    assert "never creates" in text or "never created" in text, (
        f"{REDLINE}: the body does not say that Handoff Metadata is never"
        f" created where a Text Artifact carries none. Requiring or writing it"
        f" would make provenance an entry condition instead of a shortcut"
        f" (ADR-0088). See {STANDARD}."
    )
    assert "kntnt" in text and "frontmatter" in text, (
        f"{REDLINE}: the body never says which frontmatter is this"
        f" collection's, so unrelated document fields read as configuration"
        f" (ADR-0088). See {STANDARD}."
    )


def test_redline_loads_the_contract_it_reviews_against() -> None:
    """A review is only as good as the document it is read against.

    Redline reads the base contract and its review extension, the selected
    genre and technique with theirs, the shared anti-slop catalogue, and the
    three scopes of the resolved Language Resource it may act on. Mechanics
    belong to the closing Proofread pass, which resolves them itself
    (ADR-0087, ADR-0095).
    """

    text = REDLINE.read_text(encoding="utf-8")

    for pointer in (
        "$LIBRARY/references/editorial/base.md",
        "$LIBRARY/references/editorial/base.review.md",
        "$LIBRARY/references/editorial/anti-slop.md",
    ):
        assert pointer in text, (
            f"{REDLINE}: the body never reaches `{pointer}`, so part of what"
            f" the review is read against is not loaded (ADR-0095). See"
            f" {STANDARD}."
        )

    for scope in ("composition", "review", "anti-slop"):
        assert f"--scope={scope}" in text, (
            f"{REDLINE}: the body never asks the resolver for the `{scope}`"
            f" scope, which is language-specific guidance this Skill is"
            f" contracted to apply (ADR-0087). See {STANDARD}."
        )
    assert "--scope=mechanics" not in text, (
        f"{REDLINE}: the body asks for the `mechanics` scope, which belongs to"
        f" the closing Proofread pass and is resolved there. A caller asks for"
        f" the scopes it can act on and is given those and no others"
        f" (ADR-0087). See {STANDARD}."
    )
    assert ".review.md" in text.replace("base.review.md", ""), (
        f"{REDLINE}: the body loads no review extension for the selected genre"
        f" or technique, so the diagnostic half of those resources is written"
        f" for a reader that never opens it (ADR-0095). See {STANDARD}."
    )


def test_redline_leaves_source_fidelity_to_the_skill_that_owns_it() -> None:
    """A reviewing Skill has no source material, and says nothing about it.

    Redline reviews the Text Artifact against its editorial contract. It never
    compares the artifact with source material and never reports that source
    verification was unavailable, because a caveat about material nobody
    supplied is noise in every run that was never a Write run (ADR-0088).
    """

    text = REDLINE.read_text(encoding="utf-8")

    assert "source material" in text, (
        f"{REDLINE}: the body says nothing about source material, so nothing"
        f" stops a review from asking for material it was never given"
        f" (ADR-0088). See {STANDARD}."
    )
    assert "Source Fidelity" in text, (
        f"{REDLINE}: the body never names Source Fidelity as somebody else's"
        f" contract, and the boundary is what keeps this Skill usable where no"
        f" Write invocation and no material exist (ADR-0088). See {STANDARD}."
    )


def test_redline_invokes_proofread_once_and_declares_what_it_needs() -> None:
    """The mechanical pass is last, and both requirements are hard.

    Proofread is a declared Skill Dependency followed through its public
    `SKILL.md` rather than through its private files (ADR-0076), and subagents
    are a hard Capability whatever Correction Budget is in force, so the Skill
    has one honest availability contract rather than one per invocation.
    """

    text = REDLINE.read_text(encoding="utf-8")

    assert "$HERE/../proofread/SKILL.md" in text, (
        f"{REDLINE}: the body never follows Proofread's public `SKILL.md`, so"
        f" the closing mechanical pass is either absent or performed by"
        f" Redline itself (ADR-0088, ADR-0076). See {STANDARD}."
    )
    assert '\n  kntnt.skills: "proofread"\n' in text, (
        f"{REDLINE}: Proofread is invoked and not declared, so Select cannot"
        f" show what Redline needs before it is Enabled (ADR-0088). See"
        f" {STANDARD}."
    )
    assert '\n  kntnt.capabilities: "subagents"\n' in text, (
        f"{REDLINE}: subagents are a hard Capability of this Skill whatever"
        f" the Correction Budget in force is, a conditional declaration being"
        f" an availability contract that changes with the invocation"
        f" (ADR-0062). See {STANDARD}."
    )


def test_redline_delivers_through_the_shared_output_contract() -> None:
    """The rule has one owner, and a consumer follows it rather than repeating it.

    Where a result goes, when a source file may be replaced by it, and what
    happens when nothing changed are stated once in the Collection Library
    (ADR-0091). A Skill restating them in its own body is a second copy free
    to drift from the one every other Skill delivers by.
    """

    text = REDLINE.read_text(encoding="utf-8")

    assert "$LIBRARY/references/delivery.md" in text, (
        f"{REDLINE}: the body delivers its Text Artifact without following the"
        f" Collection Library's delivery contract, so the Output Target,"
        f" In-place Editing, its refusals, and the no-change status are this"
        f" Skill's own account of rules it shares with its peers (ADR-0091,"
        f" ADR-0076). See {STANDARD}."
    )
    assert "`my-file-2.md`" not in text, (
        f"{REDLINE}: the body spells out the shared collision sequence instead"
        f" of following the contract that owns it, which is one rule made into"
        f" two things to keep true (ADR-0091). See {STANDARD}."
    )


def test_the_correction_budget_is_any_non_negative_integer_defaulting_to_one() -> None:
    """One correction and one chance to verify it is the ordinary review.

    The budget is a ceiling on delegated corrections rather than a quota to
    reach: `0` reviews and reports without correcting, the default `1` buys
    one correction and the re-review that verifies it, and a higher number
    bounds a longer loop explicitly (ADR-0107). Every surface a caller reads
    says the same range and the same default, and the release that accepted
    zero alone is gone from all of them.
    """

    body = REDLINE.read_text(encoding="utf-8")
    manpage = REDLINE_HELP.read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    for path, text in ((REDLINE, body), (REDLINE_HELP, manpage)):
        assert "non-negative integer" in text, (
            f"{path}: the Correction Budget's range is not stated, so what"
            f" `--max` accepts is left to be discovered by refusal"
            f" (ADR-0107). See {STANDARD}."
        )
        assert (
            "release accepts" not in text and "release does not accept" not in text
        ), (
            f"{path}: the budget is still documented against what one release"
            f" accepts, which is the half-built Skill this one has left"
            f" (ADR-0107). See {STANDARD}."
        )

    assert "defaults to `1`" in body, (
        f"{REDLINE}: the body does not default the Correction Budget to `1`,"
        f" so an ordinary review either corrects nothing or corrects without"
        f" a bound nobody wrote down (ADR-0107). See {STANDARD}."
    )
    assert "`1`" in _optional_section(manpage, "## OPTIONS"), (
        f"{REDLINE_HELP}: the `--max` option does not state its default, which"
        f" is what a reader deciding whether to name it needs (ADR-0107). See"
        f" {STANDARD}."
    )
    assert "zero alone" not in readme, (
        f"{REPO_ROOT / 'README.md'}: the `### redline` section still says the"
        f" Correction Budget accepts zero alone. The README is where somebody"
        f" decides whether they want the Skill, and it is describing a release"
        f" that has been outrun (ADR-0107). See {STANDARD}."
    )


def test_each_correction_is_delegated_to_a_subagent_that_carries_no_history() -> None:
    """A repair is attempted by somebody the last attempt cannot have framed.

    Fresh means no earlier findings and no earlier attempts, and the brief is
    the whole of what reaches the subagent: the complete current Text
    Artifact, the complete current findings, the resolved editorial
    parameters, and the requirement to preserve what the findings do not
    concern (ADR-0107). A summary of any of those is this session's reading
    of the text, which is the very thing the fresh subagent exists to be
    without.
    """

    body = REDLINE.read_text(encoding="utf-8")

    assert REDLINE_CORRECTION.is_file(), (
        f"{REDLINE_CORRECTION}: a correcting subagent is started from a brief"
        f" this Skill alone opens, which belongs under its `references/`"
        f" (ADR-0063, ADR-0107). See {STANDARD}."
    )
    assert "references/correction.md" in body, (
        f"{REDLINE}: the body never reaches the correction brief, so what a"
        f" fresh subagent receives is left to the session that dispatches it"
        f" (ADR-0107). See {STANDARD}."
    )

    brief = REDLINE_CORRECTION.read_text(encoding="utf-8")
    for phrase, missing in (
        ("complete", "the complete current Text Artifact"),
        ("finding", "the complete current findings"),
        ("preserve", "the requirement to preserve unaffected material"),
    ):
        assert phrase in brief.lower(), (
            f"{REDLINE_CORRECTION}: the brief does not carry {missing}, so a"
            f" subagent with no history of its own repairs something other"
            f" than the text as it now stands (ADR-0107). See {STANDARD}."
        )
    for parameter in ("genre", "technique", "language"):
        assert parameter in brief.lower(), (
            f"{REDLINE_CORRECTION}: the brief passes on no {parameter}, so the"
            f" repair is made against a contract other than the one the review"
            f" found the text wanting against (ADR-0107). See {STANDARD}."
        )
    assert "fresh" in body.lower(), (
        f"{REDLINE}: the body does not say that each correction goes to a"
        f" fresh subagent, so one context accumulates every round's framing"
        f" and the previous attempt biases the next (ADR-0107). See"
        f" {STANDARD}."
    )


def test_a_correction_is_verified_by_review_rather_than_by_its_own_report() -> None:
    """The one reader who cannot check a repair is the agent that made it.

    Every returned text is reviewed again against everything the first review
    was read against, and the budget falls by exactly one per correction, so a
    round that returned nothing usable still costs what it spent (ADR-0107).
    """

    body = REDLINE.read_text(encoding="utf-8")

    assert "reviewed again" in body or "review it again" in body, (
        f"{REDLINE}: the body never reviews a corrected text again, so a"
        f" correction is accepted on the report of whoever made it"
        f" (ADR-0107). See {STANDARD}."
    )
    assert "once per correction" in body, (
        f"{REDLINE}: the body does not say the budget falls once per"
        f" correction, so the bound a caller named is not the bound the loop"
        f" keeps (ADR-0107). See {STANDARD}."
    )


def test_the_correction_loop_stops_on_each_of_its_three_conditions() -> None:
    """A loop with one exit is a loop that spends everything it is given.

    It stops when no findings remain, leaving the rest of the budget unspent
    so clean text is not rewritten for the sake of a number; it stops when a
    correction makes no relevant progress, saying what remains rather than
    repeating a no-op round; and it stops when the budget is spent, delivering
    the text with the findings that are left (ADR-0107). The closing
    mechanical pass happens once after the loop whatever stopped it, and
    nothing substantive follows it.
    """

    body = REDLINE.read_text(encoding="utf-8")

    assert "unspent" in body, (
        f"{REDLINE}: the body never leaves budget unspent, so a clean text is"
        f" corrected again to use up a number the caller named as a ceiling"
        f" (ADR-0107). See {STANDARD}."
    )
    assert "no relevant progress" in body, (
        f"{REDLINE}: the body has no stop for a correction that changed"
        f" nothing the findings named, so the loop repeats a round already"
        f" shown to achieve nothing (ADR-0107). See {STANDARD}."
    )
    assert "budget is spent" in body or "budget is exhausted" in body, (
        f"{REDLINE}: the body never stops on the spent budget, so the bound"
        f" the caller named bounds nothing (ADR-0107). See {STANDARD}."
    )
    assert "$HERE/../proofread/SKILL.md" in body, (
        f"{REDLINE}: the closing mechanical pass is gone from the body"
        f" (ADR-0088). See {STANDARD}."
    )

    loop = body.index("Correction Budget", body.index("## Steps"))
    proofread = body.index("$HERE/../proofread/SKILL.md")
    assert loop < proofread, (
        f"{REDLINE}: the mechanical pass is invoked before the correction loop"
        f" it is meant to close, so a correction can put mechanical errors"
        f" back into a text already cleaned of them (ADR-0088, ADR-0107). See"
        f" {STANDARD}."
    )


def test_the_anti_slop_catalogue_is_shared_rather_than_one_skills_property() -> None:
    """Two Skills apply this pass, so neither owns the other's rules.

    The catalogue is a condensed adaptation the collection owns, which is what
    keeps an external Skill out of the dependency lists, and it ships in the
    Collection Library because a peer applying the pass alone must read it
    without reaching into Redline's own files (ADR-0076, ADR-0101).
    """

    assert ANTI_SLOP.is_file(), (
        f"{ANTI_SLOP}: the anti-slop catalogue has more than one consumer, so"
        f" it belongs to the Collection Library rather than to the Skill that"
        f" happened to need it first (ADR-0076, ADR-0101). See {STANDARD}."
    )

    catalogue = ANTI_SLOP.read_text(encoding="utf-8").lower()
    missing = [pattern for pattern in SLOP_PATTERNS if pattern not in catalogue]
    assert missing == [], (
        f"{missing}: the anti-slop catalogue does not carry these patterns,"
        f" which are the ones the collection undertook to catch (ADR-0101)."
        f" See {STANDARD}."
    )

    assert "MIT" in ANTI_SLOP.read_text(encoding="utf-8"), (
        f"{ANTI_SLOP}: the catalogue adapts a substantial part of an upstream"
        f" MIT-licensed catalogue and ships without the upstream notice its"
        f" terms require (ADR-0101). See {STANDARD}."
    )

    private = sorted(
        path
        for directory in _shipped_skills()
        for path in directory.rglob("*.md")
        if "anti-slop" in path.name
    )
    assert private == [], (
        f"{private}: a Skill ships its own copy of the anti-slop catalogue,"
        f" which makes one consumer the implementation owner of the other's"
        f" rules (ADR-0076, ADR-0101). See {STANDARD}."
    )


# The Skill that applies the anti-slop pass alone, read at the one seam a test
# has: the body is the whole of what the agent executes (ADR-0046). Its
# manpage, and the brief its correcting subagents are started from.
UNSLOP = REPO_ROOT / "skills" / "editorial" / "unslop" / "SKILL.md"
UNSLOP_HELP = UNSLOP.parent / "help.md"
UNSLOP_CORRECTION = UNSLOP.parent / "references" / "correction.md"


def _unslop() -> str:
    """Every Markdown file the Skill ships, concatenated.

    A rule about what this Skill may load or reach is a rule about all of its
    files: a pointer the body never writes reaches just as far from the brief
    a subagent is started from.
    """

    paths = sorted(UNSLOP.parent.rglob("*.md"))

    # A directory that is not there would leave every assertion over it with
    # nothing to judge and pass regardless.
    assert paths, (
        f"{UNSLOP.parent}: the Skill that applies the anti-slop pass alone"
        f" ships in the Collection's editorial category (ADR-0112). See"
        f" {STANDARD}."
    )
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def _unslop_field(name: str) -> str:
    """Return one of the Skill's frontmatter fields, as the file writes it."""

    body = UNSLOP.read_text(encoding="utf-8")
    frontmatter = body.partition("---\n")[2].partition("\n---\n")[0]
    for line in frontmatter.splitlines():
        if line.startswith(f"{name}:"):
            return line.partition(":")[2].strip()
    return ""


def test_unslop_loads_only_the_lens_it_applies() -> None:
    """Reading no more than it may act on is the whole point of the split.

    One lens applied alone loads the shared catalogue and the resolved
    language's anti-slop scope, and nothing else: no base contract, no genre,
    no technique, and none of the composition, review, or mechanics scopes.
    A Skill holding rules it is contracted not to apply is a Skill one round
    away from applying them, which is how a single pass becomes the whole
    editorial contract nobody asked for (ADR-0087, ADR-0112).
    """

    body = UNSLOP.read_text(encoding="utf-8")
    shipped = _unslop()

    assert "$LIBRARY/references/editorial/anti-slop.md" in body, (
        f"{UNSLOP}: the body never reaches the shared anti-slop catalogue, so"
        f" the one pass this Skill exists to apply is applied from memory"
        f" (ADR-0101, ADR-0112). See {STANDARD}."
    )
    assert "--scope=anti-slop" in body, (
        f"{UNSLOP}: the body never asks the resolver for the `anti-slop`"
        f" scope, which is where a language's own slop words, phrases,"
        f" punctuation, and constructions live (ADR-0087). See {STANDARD}."
    )
    for scope in ("composition", "review", "mechanics"):
        assert f"--scope={scope}" not in shipped, (
            f"{UNSLOP.parent}: the Skill asks the resolver for the `{scope}`"
            f" scope, which belongs to the Skills contracted to act on it. A"
            f" caller asks for the scopes it can act on and is given those and"
            f" no others (ADR-0087, ADR-0112). See {STANDARD}."
        )
    for pointer in (
        "editorial/base.md",
        "editorial/base.review.md",
        "editorial/genres/",
        "editorial/techniques/",
    ):
        assert pointer not in shipped, (
            f"{UNSLOP.parent}: the Skill reaches `{pointer}`, which is part of"
            f" the editorial contract it selects none of. Typing the whole"
            f" contract to get one lens is the gesture this Skill exists to"
            f" replace (ADR-0112). See {STANDARD}."
        )

    hint = _unslop_field("argument-hint")
    for option in ("--language=", "--max=", "--output=", "--in-place"):
        assert option in hint, (
            f"{UNSLOP}: `argument-hint` offers no `{option}`, and the four"
            f" editorial options this Skill resolves are spelled as its peers"
            f" spell them (ADR-0112). See {STANDARD}."
        )
    for option in ("--genre", "--technique"):
        assert option not in hint, (
            f"{UNSLOP}: `argument-hint` offers `{option}`, which selects part"
            f" of an editorial contract this Skill never loads. A flag"
            f" accepted here would be a flag with no work to do (ADR-0112)."
            f" See {STANDARD}."
        )


def test_unslop_reads_the_shared_catalogue_without_reaching_into_a_peer() -> None:
    """A peer's private files are not an interface, whoever needs them.

    The catalogue lives in the Collection Library precisely so a second
    consumer can apply the pass without the Skill that needed it first
    becoming the implementation owner of its rules (ADR-0076, ADR-0101).
    """

    body = UNSLOP.read_text(encoding="utf-8")
    shipped = _unslop()

    assert "$LIBRARY" in body, (
        f"{UNSLOP}: the body defines no Collection Library, so the shared"
        f" catalogue and the language resources are reached from wherever the"
        f" session happens to look (ADR-0076). See {STANDARD}."
    )
    for peer in ("redline", "write", "proofread"):
        assert f"../{peer}/" not in shipped, (
            f"{UNSLOP.parent}: the Skill reads `{peer}`'s own files. A Skill"
            f" may follow a declared Dependency's public `SKILL.md` and never"
            f" its `references/` or its `scripts/` (ADR-0076). See {STANDARD}."
        )

    private = sorted(
        path
        for path in UNSLOP.parent.rglob("*.md")
        if "anti-slop" in path.name or "slop" in path.stem
    )
    assert private == [], (
        f"{private}: the Skill ships a catalogue of its own beside the shared"
        f" one, which is the second copy the Library exists to prevent"
        f" (ADR-0076, ADR-0101). See {STANDARD}."
    )


def test_unslop_runs_no_mechanical_pass_and_names_the_separate_gesture() -> None:
    """One pass was asked for, and one pass is what comes back.

    Redline closes with a mechanical pass because it has just applied a whole
    editorial contract. This Skill applied one lens, so it proofreads nothing,
    declares no Dependency on a proofreading peer, and says on its own page
    which gesture a reader wants for mechanical errors instead (ADR-0112).
    """

    body = UNSLOP.read_text(encoding="utf-8")

    assert '\n  kntnt.skills: ""\n' in body, (
        f"{UNSLOP}: the Skill declares a Dependency on a peer Skill. It calls"
        f" none — a Skill that ran a mechanical pass would be delivering work"
        f" its caller did not ask for (ADR-0112). See {STANDARD}."
    )
    assert "$HERE/../proofread/SKILL.md" not in body, (
        f"{UNSLOP}: the body invokes the mechanical pass. This Skill was asked"
        f" for one pass and gives one pass (ADR-0112). See {STANDARD}."
    )

    manpage = UNSLOP_HELP.read_text(encoding="utf-8")
    assert "proofread" in manpage, (
        f"{UNSLOP_HELP}: the page never names the separate gesture for"
        f" mechanical errors, so a reader whose text still has typos after"
        f" this pass is left to discover that it was never going to fix them"
        f" (ADR-0112). See {STANDARD}."
    )


def test_unslop_declares_the_subagents_and_the_runtime_it_needs() -> None:
    """Availability is one contract, not one per invocation.

    Every correction goes to a subagent, so subagents are a hard Capability
    whatever Correction Budget an invocation names, and the shared resolver
    the language is settled through needs the Collection's normal runtime
    (ADR-0062, ADR-0107).
    """

    body = UNSLOP.read_text(encoding="utf-8")

    assert '\n  kntnt.capabilities: "subagents"\n' in body, (
        f"{UNSLOP}: subagents are a hard Capability of this Skill whatever the"
        f" Correction Budget in force is, a conditional declaration being an"
        f" availability contract that changes with the invocation (ADR-0062)."
        f" See {STANDARD}."
    )
    assert '\n  kntnt.binaries: "uv"\n' in body, (
        f"{UNSLOP}: the Skill runs the Collection's resolver and declares none"
        f" of the runtime it takes to run it (ADR-0062). See {STANDARD}."
    )
    assert 'check --here="$HERE"' in body, (
        f"{UNSLOP}: the dependency lists are not empty and the body calls no"
        f" checker, so an Unsatisfied Dependency is met as a failure rather"
        f" than as a refusal. See {STANDARD}."
    )

    compatibility = _unslop_field("compatibility")
    for requirement in ("uv", "subagents"):
        assert requirement in compatibility, (
            f"{UNSLOP}: `compatibility` does not name {requirement!r}, and it"
            f" is the one field a reader outside this collection knows to look"
            f" at (ADR-0062). See {STANDARD}."
        )


def test_unslop_is_started_by_a_person_rather_than_by_a_model() -> None:
    """*This text reads like AI* is a judgement a person makes.

    A model reaching for this pass unasked would be rewriting a text on its
    own reading of how the text sounds, which is exactly the call the author
    is entitled to make. Both files say so, because Codex reads only the
    sidecar and the harness reads only the frontmatter (ADR-0094, ADR-0112).
    """

    body = UNSLOP.read_text(encoding="utf-8")

    assert "\ndisable-model-invocation: true\n" in body, (
        f"{UNSLOP}: the frontmatter leaves this Skill open to a model starting"
        f" it, so a text is unslopped because something judged that it sounded"
        f" wrong rather than because anybody asked (ADR-0094, ADR-0112). See"
        f" {STANDARD}."
    )

    sidecar = (UNSLOP.parent / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "allow_implicit_invocation: false" in sidecar, (
        f"{UNSLOP.parent / 'agents' / 'openai.yaml'}: the sidecar leaves this"
        f" Skill implicitly invocable, and it is the only copy of that"
        f" decision Codex reads (ADR-0094). See {STANDARD}."
    )


def test_unslop_carries_the_collections_one_correction_budget_contract() -> None:
    """One loop contract in the Collection, reused rather than restated.

    The budget is any non-negative integer defaulting to one; each correction
    goes to a subagent started fresh with the complete text and the complete
    findings; the budget falls once per correction; the returned text is
    reviewed again rather than accepted on its own report; and the loop stops
    on clean text, on no relevant progress, and on the spent budget
    (ADR-0107). The brief carries no genre and no technique, because this
    Skill resolves neither (ADR-0112).
    """

    body = UNSLOP.read_text(encoding="utf-8")

    for phrase, missing in (
        ("non-negative integer", "the range the budget accepts"),
        ("defaults to `1`", "the default an ordinary invocation gets"),
        ("once per correction", "the decrement the caller's bound depends on"),
        ("unspent", "the early stop that leaves clean text alone"),
        ("no relevant progress", "the stop for a round that changed nothing"),
        ("budget is spent", "the stop that carries findings to a person"),
        ("fresh", "the subagent that carries no earlier round's framing"),
    ):
        assert phrase in body, (
            f"{UNSLOP}: the body does not carry {missing}, so this Skill's"
            f" loop is a second set of semantics beside the one the Collection"
            f" already has (ADR-0107, ADR-0112). See {STANDARD}."
        )
    assert "reviewed again" in body or "review it again" in body, (
        f"{UNSLOP}: the body never reviews a corrected text again, so a"
        f" correction is accepted on the report of whoever made it"
        f" (ADR-0107). See {STANDARD}."
    )

    assert UNSLOP_CORRECTION.is_file(), (
        f"{UNSLOP_CORRECTION}: a correcting subagent is started from a brief"
        f" this Skill alone opens, which belongs under its `references/`"
        f" (ADR-0063, ADR-0107). See {STANDARD}."
    )
    assert "references/correction.md" in body, (
        f"{UNSLOP}: the body never reaches the correction brief, so what a"
        f" fresh subagent receives is left to the session that dispatches it"
        f" (ADR-0107). See {STANDARD}."
    )

    brief = UNSLOP_CORRECTION.read_text(encoding="utf-8").lower()
    for phrase, missing in (
        ("complete", "the complete current Text Artifact"),
        ("finding", "the complete current findings"),
        ("preserve", "the requirement to preserve unaffected material"),
        ("language", "the resolved language"),
    ):
        assert phrase in brief, (
            f"{UNSLOP_CORRECTION}: the brief does not carry {missing}, so a"
            f" subagent with no history of its own repairs something other"
            f" than the text as it now stands (ADR-0107). See {STANDARD}."
        )
    for parameter in ("genre", "technique"):
        assert parameter not in brief, (
            f"{UNSLOP_CORRECTION}: the brief passes on a {parameter}, which"
            f" this Skill resolves nowhere and loads nothing for. A correction"
            f" made against a contract the review never applied is a change"
            f" nobody asked for (ADR-0112). See {STANDARD}."
        )


def test_unslop_resolves_the_language_and_leaves_the_map_as_it_found_it() -> None:
    """One parameter, the Collection's own precedence, and no metadata written.

    The language falls through the Formal Invocation, a recognized Kntnt map,
    the Contextual Instruction, the Conversation Context, inference, and then
    the language of the supplied text. A map may supply that one value; no map
    is created and none is brought into line with what the run resolved,
    because this Skill resolves nothing a map records (ADR-0088, ADR-0112).
    """

    body = UNSLOP.read_text(encoding="utf-8")

    for level in (
        "Formal Invocation",
        "Contextual Instruction",
        "Conversation Context",
    ):
        assert level in body, (
            f"{UNSLOP}: the body names no {level} in its language precedence,"
            f" so the order this Collection resolves a parameter in is this"
            f" Skill's own (ADR-0088). See {STANDARD}."
        )
    assert "kntnt" in body and "frontmatter" in body, (
        f"{UNSLOP}: the body never says which frontmatter is this"
        f" collection's, so unrelated document fields read as configuration"
        f" (ADR-0088). See {STANDARD}."
    )
    assert "created or synchronized" in body, (
        f"{UNSLOP}: the body does not say that no Kntnt map is created or"
        f" synchronized. This Skill resolves one value of the three a map"
        f" carries, so writing one would record a configuration it never"
        f" settled (ADR-0088, ADR-0112). See {STANDARD}."
    )
    assert "$LIBRARY/scripts/languages.py" in body, (
        f"{UNSLOP}: the body resolves its language through something other"
        f" than the Collection Library's resolver, which is deterministic and"
        f" shared by every editorial Skill (ADR-0087, ADR-0076). See"
        f" {STANDARD}."
    )


def test_unslop_delivers_shared_and_judges_only_the_text_in_front_of_it() -> None:
    """Two contracts this Skill consumes rather than restates.

    Where a result goes, when a source may be replaced, and what an unchanged
    run returns are stated once in the Collection Library (ADR-0091). Source
    material is somebody else's contract, and a caveat about material nobody
    supplied is noise in every run that was never a Write run (ADR-0088).
    """

    body = UNSLOP.read_text(encoding="utf-8")

    assert "$LIBRARY/references/delivery.md" in body, (
        f"{UNSLOP}: the body delivers its Text Artifact without following the"
        f" Collection Library's delivery contract, so the Output Target,"
        f" In-place Editing, its refusals, and the no-change status are this"
        f" Skill's own account of rules it shares with its peers (ADR-0091,"
        f" ADR-0076). See {STANDARD}."
    )
    assert "`my-file-2.md`" not in body, (
        f"{UNSLOP}: the body spells out the shared collision sequence instead"
        f" of following the contract that owns it, which is one rule made into"
        f" two things to keep true (ADR-0091). See {STANDARD}."
    )
    assert "source material" in body, (
        f"{UNSLOP}: the body says nothing about source material, so nothing"
        f" stops a pass from asking for material it was never given"
        f" (ADR-0088). See {STANDARD}."
    )
    assert "Source Fidelity" in body, (
        f"{UNSLOP}: the body never names Source Fidelity as somebody else's"
        f" contract, and the boundary is what keeps this Skill usable where no"
        f" Write invocation and no material exist (ADR-0088). See {STANDARD}."
    )


def test_the_unslop_manpage_names_the_patterns_a_finding_may_be() -> None:
    """A reader deciding whether to run this needs to know what it looks for.

    The seven patterns are the whole of what a finding may be here, and the
    page that describes the Skill is where somebody outside the run reads
    them. They are applied by what they do in the target language rather than
    matched as English strings (ADR-0101, ADR-0112).
    """

    manpage = UNSLOP_HELP.read_text(encoding="utf-8").lower()

    missing = [pattern for pattern in SLOP_PATTERNS if pattern not in manpage]
    assert missing == [], (
        f"{missing}: the page does not name these patterns, and they are the"
        f" whole of what this Skill finds (ADR-0101, ADR-0112). See"
        f" {STANDARD}."
    )
    assert "semantic" in manpage, (
        f"{UNSLOP_HELP}: the page does not say that the catalogue's English"
        f" examples are applied as semantic patterns in the target language,"
        f" which is what makes one compact catalogue work on every language"
        f" the Collection installs (ADR-0101). See {STANDARD}."
    )


def test_the_base_contracts_review_extension_restates_no_base_rule() -> None:
    """A requirement and its diagnostic must not both claim to state the rule.

    The extension holds diagnostics, examples, edge cases, ambiguity
    resolution, and minimum-safe-correction guidance for requirements the base
    half already states. A sentence carried over from the base half is one
    rule made into two things to keep true, free to drift the moment either is
    edited (ADR-0095).
    """

    editorial = REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "editorial"
    extension = editorial / "base.review.md"

    assert extension.is_file(), (
        f"{extension}: the base contract ships without the review extension"
        f" the reviewing Skills read it through (ADR-0095). See {STANDARD}."
    )

    review = extension.read_text(encoding="utf-8")

    # The same rule the base half is held to: a shared document naming a
    # consumer's flag would bind a grammar the consuming Skill owns.
    flags = sorted(set(re.findall(r"(?<![\w-])--[A-Za-z][\w-]*", review)))
    assert flags == [], (
        f"{flags}: the review extension names a consumer's flag spelling,"
        f" which binds a grammar the consuming Skill owns (ADR-0095). See"
        f" {STANDARD}."
    )

    # A sentence long enough to be a rule rather than a turn of phrase.
    base = (editorial / "base.md").read_text(encoding="utf-8")
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", base)
        if len(sentence.strip()) >= 40
    ]
    assert sentences

    carried = sorted(sentence for sentence in sentences if sentence in review)
    assert carried == [], (
        f"{carried}: the review extension repeats the base half word for word."
        f" Anything a draft has to meet is a base rule and belongs where the"
        f" writing Skill will see it; the extension says how a failure is"
        f" recognised and repaired (ADR-0095). See {STANDARD}."
    )


def test_a_skill_reads_shared_implementation_only_from_the_collection_library() -> None:
    """A peer Skill is a Dependency, never an implementation owner."""

    # Match an installed-layout pointer into any peer except the Manager.
    peer_implementation = re.compile(
        r"\$HERE/\.\./(?!kntnt/)[A-Za-z0-9_-]+/(?:references|scripts)/"
    )

    # Hold every body to the same ownership direction.
    for body in _skill_bodies():
        assert peer_implementation.search(body.read_text(encoding="utf-8")) is None, (
            f"{body}: shared references and scripts belong to the Collection"
            f" Library, so a Skill never reads another Skill's implementation"
            f" (ADR-0076). See {STANDARD}."
        )


def test_every_distributed_markdown_dependency_is_available_to_an_installed_reader() -> (
    None
):
    """A distributed document needs no repository-only context.

    Three pointer shapes carry the collection: `$HERE/<path>`, resolved from
    the directory holding `SKILL.md`; `$LIBRARY/<path>`, resolved from the
    Manager's Collection Library; and a Markdown link, resolved from the file
    it sits in. All are followed here so a rename cannot leave one dangling in
    somebody's session.

    `$HERE/../kntnt/scripts/kntnt.py` is the one pointer not followed. It is
    the checker as an installed skill sees it, every skill a sibling of the
    Manager; the source tree groups by category instead, and the body already
    reads that path as one that may be absent.
    """

    here = re.compile(r"\$HERE/([A-Za-z0-9_./-]+\.(?:md|py))")
    library = re.compile(r"\$LIBRARY/([A-Za-z0-9_./-]+\.(?:md|py))")
    link = re.compile(r"\]\(([A-Za-z0-9_./-]+\.md)\)")
    citation = re.compile(r"ADR-\d{4}")

    pointers = 0
    citations: dict[str, list[str]] = {}
    for path in sorted((REPO_ROOT / "skills").rglob("*.md")):
        root = next(p for p in path.parents if (p / "SKILL.md").is_file())
        text = path.read_text(encoding="utf-8")
        for match in citation.findall(text):
            citations.setdefault(match, []).append(str(path.relative_to(REPO_ROOT)))
        for target in here.findall(text):
            if target.startswith("../kntnt/"):
                continue
            assert (root / target).is_file(), (
                f"{path}: `$HERE/{target}` resolves to nothing. `$HERE` is the"
                f" directory holding `SKILL.md`, and a pointer that dangles is"
                f" a file an agent is told to open mid-run and cannot. See"
                f" {STANDARD}."
            )
            pointers += 1
        for target in library.findall(text):
            assert (MANAGER_DIR / "library" / target).is_file(), (
                f"{path}: `$LIBRARY/{target}` resolves to nothing. `$LIBRARY`"
                f" is the Collection Library shipped inside the Manager, and"
                f" a pointer that dangles is a file an agent is told to open"
                f" mid-run and cannot. See {STANDARD}."
            )
            pointers += 1
        for target in link.findall(text):
            assert (path.parent / target).is_file(), (
                f"{path}: the link `{target}` resolves to nothing. A Markdown"
                f" link is resolved from the file it sits in, so a move is"
                f" finished only when every file pointing at it agrees. See"
                f" {STANDARD}."
            )
            pointers += 1

    assert pointers
    assert citations == {}, (
        f"{citations}: an installed reader receives the Skill and the"
        f" Collection Library, not this repository's ADR directory. Carry the"
        f" operational rule and necessary rationale in distributed resources"
        f" instead. See {STANDARD}."
    )


def test_select_is_where_a_skill_is_read_about_before_it_is_enabled() -> None:
    """The route `/kntnt help <skill>` was withdrawn in favour of (ADR-0044).

    Prose is what carries it, so prose is where it has to be pinned: a list
    that never offers the help is a list nobody can ask for it from.
    """

    manager = REPO_ROOT / "skills" / "kntnt"
    steps = (manager / "steps" / "select.md").read_text(encoding="utf-8")
    page = (manager / "help" / "select.md").read_text(encoding="utf-8")

    assert 'scripts/kntnt.py" manpage' in steps
    assert "read in full" in page


def test_the_manager_documents_its_own_verbs_and_no_skill() -> None:
    """A withdrawn route left standing in the prose is one users keep trying."""

    withdrawn = (
        "help <skill>",
        "one collection skill",
        "named collection skill",
        "collection skill's help",
    )
    manager = REPO_ROOT / "skills" / "kntnt"
    for path in (
        manager / "SKILL.md",
        manager / "help.md",
        manager / "help" / "help.md",
        manager / "steps" / "help.md",
    ):
        text = path.read_text(encoding="utf-8")
        for phrase in withdrawn:
            assert phrase not in text, f"{path}: {phrase}"


def test_agents_md_is_model_invoked() -> None:
    text = (REPO_ROOT / "skills" / "agents" / "agents-md" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "disable-model-invocation: false" in text, (
        f"{REPO_ROOT / 'skills' / 'agents' / 'agents-md' / 'SKILL.md'}: a model"
        f" invokes this skill on its own, and it says so in the field rather"
        f" than by leaving the field out — an absent field is a decision nobody"
        f" wrote, and the Codex sidecar beside it has to agree with something"
        f" (ADR-0018). See {STANDARD}."
    )
    assert "name: agents-md" in text, (
        f"{REPO_ROOT / 'skills' / 'agents' / 'agents-md' / 'SKILL.md'}: `name`"
        f" is the skill's directory name exactly, and the description is the"
        f" only hook a harness has for reaching it (ADR-0019). See {STANDARD}."
    )


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
    assert 'kntnt.capabilities: "subagents"' in text, (
        f"{path}: this skill is meaningless where subagents cannot be spawned,"
        f" so it declares `subagents` as a Capability. A harness requirement is"
        f" a fourth kind of dependency the skill refuses on, never a row in a"
        f" per-harness matrix (ADR-0030). See {STANDARD}."
    )
    assert "`capabilities`" in text, (
        f"{path}: the body answers the checker's `capabilities` list itself."
        f" No script can: the agent is the harness, so exit 0 with a non-empty"
        f" list means nothing a script could see is missing rather than"
        f" go-ahead (ADR-0030). See {STANDARD}."
    )

    mode = (path.parent / "references" / "mode.md").read_text(encoding="utf-8")
    assert "haiku" not in mode, (
        f"{path.parent / 'references' / 'mode.md'}: the mode text names no"
        f" model from one vendor's ladder. It is written into a committed"
        f" `AGENTS.md` that agents of any harness read (ADR-0026), and the"
        f" collection is one set across harnesses (ADR-0005) — so it tells the"
        f" reader to pick from its own ladder. See {STANDARD}."
    )
    assert "Claude Code" not in mode, (
        f"{path.parent / 'references' / 'mode.md'}: the mode text names no"
        f" single harness. It is written into a committed `AGENTS.md` that"
        f" agents of any harness read (ADR-0026), and an instruction addressed"
        f" to one of them is an instruction the rest cannot act on (ADR-0005)."
        f" See {STANDARD}."
    )


def test_delegation_routes_execution_without_changing_the_main_seat() -> None:
    """The standing mode delegates only execution through model-selector route.

    Delegation's public contract is the instruction copied unchanged to session,
    Project, and user contexts. Hold the authority boundary at that seam rather
    than duplicating model-selector's routing tests here.
    """

    directory = REPO_ROOT / "skills" / "agents" / "delegation"
    skill = (directory / "SKILL.md").read_text(encoding="utf-8")
    help_page = (directory / "help.md").read_text(encoding="utf-8")
    mode = (directory / "references" / "mode.md").read_text(encoding="utf-8")
    persistence = (directory / "references" / "persist.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    catalog = json.loads(
        (REPO_ROOT / "skills" / "kntnt" / "catalog.json").read_text(encoding="utf-8")
    )

    assert 'kntnt.skills: "model-selector"' in skill
    assert "model-selector" in skill.partition("compatibility:")[2].partition("\n")[0]
    assert "model-selector" in help_page
    assert (
        "model-selector"
        in readme.partition("### delegation")[2].partition("### commit")[0]
    )
    entry = next(item for item in catalog["skills"] if item["name"] == "delegation")
    assert entry["skills"] == ["model-selector"]

    required_mode_fragments = {
        "do this yourself",
        "before Route is consulted",
        "understanding, diagnosis, decisions, briefing, verification and the final answer",
        "main seat",
        "only the execution subagent",
        "public `/model-selector route` Interface",
        "real execution brief",
        "reversibility, consequence, context and tool demand",
        "independent checker or declared failure signal",
        "Keep the user's access profile and model inventory out of persistent mode context",
        "explicit execution-model instruction locks only the model dimension",
        "explicit `low`, `medium`, `high`, `xhigh`, or `max` deliberation instruction locks only the deliberation dimension",
        "refuse it rather than replacing it",
        "exact Harness-native launch controls",
        "without explicit model or deliberation overrides",
        "Route optimization was unavailable",
        "no subagent is launched",
        "starts no setup, research, evaluation, profile writes, or ledger writes",
        "objective main-agent verification or the declared failure signal",
        "never the execution subagent's self-confidence",
        "strongest safe permitted point",
        "brief + fresh-context reading + report",
        "After you have decided to delegate",
    }
    missing = sorted(
        fragment for fragment in required_mode_fragments if fragment not in mode
    )
    assert not missing, (
        f"{directory / 'references' / 'mode.md'}: delegation must route only chosen"
        f" execution through the public contract while preserving main-seat ownership;"
        f" missing {missing}."
    )

    assert {"--model", "--deliberation"}.isdisjoint(_flags(_hint(directory)))
    assert "config.json" not in mode

    # Keep project and user persistence as one refreshable mode contract.
    required_persistence_fragments = {
        "`project` and `user` keep the mode as a managed block",
        "{the entire content of $HERE/references/mode.md, verbatim}",
        "`on` over an existing block rewrites it from the current `mode.md`",
        "`off` removes the whole block, both markers included, and nothing else",
        "lines between the second comment and the closing marker differ",
        (
            "`status` reports it and names `/delegation on --project` or"
            " `/delegation on --user` as the fix"
        ),
    }
    missing_persistence = sorted(
        fragment
        for fragment in required_persistence_fragments
        if fragment not in persistence
    )
    assert not missing_persistence, (
        f"{directory / 'references' / 'persist.md'}: persistent delegation must"
        f" copy one authoritative mode verbatim, refresh it, remove it exactly, and"
        f" diagnose stale copies; missing {missing_persistence}."
    )


def test_delegation_keeps_predictably_noisy_tool_output_out_of_main_context() -> None:
    """The mode delegates noisy tool work before its raw result reaches the main agent."""

    path = REPO_ROOT / "skills" / "agents" / "delegation" / "references" / "mode.md"
    mode = path.read_text(encoding="utf-8")

    required_fragments = {
        "Narrow at the source first.",
        "predictably large and mostly irrelevant",
        "the main agent does not need the raw material",
        "expected main-context saving exceeds the cost",
        "complete tool call",
        "bounded extraction",
        "direct answer",
        "minimal supporting evidence",
        "material anomalies or uncertainty",
        "truncation or incomplete coverage",
        "bounded semantic extraction",
        "understanding, diagnosis, decisions, briefing, verification and the final answer",
        "same-model context isolation",
        "Post-hoc summarisation in the main context cannot recover context already spent",
    }
    missing = sorted(
        fragment for fragment in required_fragments if fragment not in mode
    )
    assert not missing, (
        f"{path}: delegation mode must keep predictably noisy tool output out of the"
        f" main context before the call, with a bounded task-shaped report; missing"
        f" contract fragments: {missing}."
    )


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


def test_catalog_generation_accepts_a_folded_description(tmp_path: Path) -> None:
    """A real YAML parser folds the block, so a description may run over lines.

    The subset had no block scalars and yielded the indicator itself, so
    generation refused `description: >` to keep a lone `>` out of the Catalog
    (issue #51). There is nothing left to refuse: the value arrives folded.
    """

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        "---\n"
        "name: alpha\n"
        "description: >\n"
        "  A collection skill whose description\n"
        "  runs over two lines.\n"
        "disable-model-invocation: true\n"
        "metadata:\n"
        '  kntnt.internal: "true"\n'
        '  kntnt.binaries: ""\n'
        "---\n"
        "\n"
        "# alpha\n",
    )

    result = _run(world, "catalog")

    assert result.returncode == 0, result.stderr
    entry = next(item for item in _json(result)["skills"] if item["name"] == "alpha")
    assert (
        entry["description"]
        == "A collection skill whose description runs over two lines.\n"
    )


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


def test_catalog_generation_rejects_metadata_that_is_not_a_mapping(
    tmp_path: Path,
) -> None:
    """`metadata: hello` is a file that says something, not one that says nothing.

    It reaches the same empty block as a skill carrying no `metadata` at all,
    and the message the two shared told this author the marker was missing
    when what is wrong is the line the keys would have hung under (issue #48).
    """

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _skill_md_with_metadata("alpha", "metadata: hello\n"),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "alpha" in result.stderr
    assert "not a mapping" in result.stderr


def test_catalog_generation_rejects_a_marker_value_that_is_not_a_string(
    tmp_path: Path,
) -> None:
    """A YAML list under `kntnt.binaries` is what habit writes after ADR-0061.

    The marker is there, so the skill passes the test for one, and the value
    is then read by a reader that wants a string. Coercing it lands a Python
    repr in the Catalog's `binaries`, which is the silent wrong answer
    ADR-0061 refused to let any other reader give (issue #48).
    """

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _skill_md_with_metadata(
            "alpha", "metadata:\n  kntnt.binaries:\n    - git\n    - uv\n"
        ),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "alpha" in result.stderr
    assert "kntnt.binaries" in result.stderr
    assert "not a string" in result.stderr


def test_catalog_generation_is_the_gate_on_every_unreadable_marker(
    tmp_path: Path,
) -> None:
    """Nothing else keeps one off a user's disk.

    Generation refuses and `CONTRIBUTING.md` step 4 regenerates the Catalog
    before anything ships: that pair is the whole of the guarantee about this
    repository, and it has to hold for every form. It was never a guarantee
    about a machine holding two revisions of the collection at once, which is
    what the gate now answers for itself (ADR-0068). The predicate underneath
    also feeds `carries_marker`, which may not raise and so can never report —
    a skill that reached a machine with an unreadable marker is one the sweep
    could not withdraw (issue #48).
    """

    forms = (
        ("no metadata at all", ""),
        ("a metadata that is not a mapping", "metadata: hello\n"),
        ("a metadata holding no kntnt. key", 'metadata:\n  internal: "true"\n'),
        ("a list value", "metadata:\n  kntnt.binaries:\n    - git\n"),
        ("an empty value, read as null", "metadata:\n  kntnt.binaries:\n"),
        ("a bare boolean", "metadata:\n  kntnt.internal: true\n"),
        ("a mapping value", 'metadata:\n  kntnt.binaries:\n    git: ""\n'),
    )

    for index, (label, metadata) in enumerate(forms):
        root = tmp_path / f"form{index}"
        root.mkdir()
        world = _world(root)
        _write(
            world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
            _skill_md_with_metadata("alpha", metadata),
        )

        result = _run(world, "catalog")

        assert result.returncode == 1, f"{label}: {result.stdout}"
        assert "alpha" in result.stderr, label


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


def test_uninstall_refuses_project_by_the_path_every_flag_is_refused_by(
    tmp_path: Path,
) -> None:
    """One error path, not two: the bespoke message for this flag is gone.

    A special case in the code for one flag is the seam ADR-0059 exists to
    remove — a difference between two refusals only somebody reading the
    source can account for. The reason the verb has no project form stays in
    `help/uninstall.md`, which the pointer at the end of the error leads to.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _install_manager(world)

    for args in (
        ("plan", "uninstall", "--project"),
        ("apply", "uninstall", "--project", "--yes"),
        ("apply", "uninstall", "--project=on", "--yes"),
    ):
        result = _run(world, *args)
        assert result.returncode == 2, args
        assert "unrecognized arguments" not in result.stderr, args
        assert "uninstall takes no '--project'" in result.stderr, args
        assert _synopsis(MANAGER_DIR / "help" / "uninstall.md") in result.stderr, args
        assert "/kntnt help uninstall" in result.stderr, args
        assert "never reaches a Project" not in result.stderr, args
        assert (world["home"] / ".claude" / "skills" / "kntnt").exists(), args


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


def test_a_project_dry_run_reads_the_global_layer(tmp_path: Path) -> None:
    """A Dependency Global supplies wants no second copy in the Project (ADR-0013)."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")

    payload = _json(
        _run(
            world, "apply", "select", "--project", "--on", "beta", "--yes", "--dry-run"
        )
    )

    assert payload["placed"] == ["beta"]


def test_a_project_dry_run_leaves_the_global_layer_alone(tmp_path: Path) -> None:
    """Seeing Global is not touching it: the Sandbox holds a copy of both layers."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _present(world, "project", ".claude")
    _run(world, "apply", "select", "alpha")
    before = _tree(world["home"])

    _run(world, "apply", "select", "--project", "--on", "beta", "--yes", "--dry-run")

    assert _tree(world["home"]) == before


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


def test_a_subparser_takes_dry_run_only_where_it_acts_on_it(tmp_path: Path) -> None:
    """The inversion of `test_every_subparser_accepts_dry_run` (ADR-0059).

    That test pinned the tolerance this record withdrew: every subparser took
    the flag, including the three with nothing to do with it, so that a flag
    the agent forwarded on its own could never break a run. It is inverted
    rather than deleted, so the reversal is visible where the old promise was
    — the same invocations, now split by whether the subcommand has a use for
    the flag. `catalog` keeps it by honouring it where it writes.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    _run(world, "apply", "select", "alpha")
    gamma = world["source"] / "skills" / "text" / "gamma"

    for args in (
        ("help",),
        ("manpage", "alpha"),
        ("check", "--here", str(gamma)),
    ):
        result = _run(world, *args, "--dry-run")
        assert result.returncode == 2, f"{args}: {result.stderr}"
        assert "takes no '--dry-run'" in result.stderr, args

    for invocation in (
        ("catalog", "--dry-run"),
        ("plan", "select", "--dry-run"),
        ("plan", "update", "--dry-run"),
        ("plan", "uninstall", "--dry-run"),
        ("apply", "select", "alpha", "--dry-run"),
        ("apply", "select", "--yes", "--dry-run"),
        ("apply", "update", "--dry-run"),
        ("apply", "uninstall", "--yes", "--dry-run"),
    ):
        result = _run(world, *invocation)
        assert result.returncode == 0, f"{invocation}: {result.stderr}"
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


def test_a_damaged_stored_catalog_is_not_a_traceback(tmp_path: Path) -> None:
    """A snapshot half-written by an interrupted Update must not take a verb down."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    (world["here"] / "catalog.json").write_text('{"skills": [', encoding="utf-8")

    result = _run(world, "plan", "update")

    assert "Traceback" not in result.stderr, result.stderr
    assert result.returncode == 0, result.stderr


def test_a_damaged_stored_catalog_reports_nothing_new(tmp_path: Path) -> None:
    """No readable snapshot is no *before*, so the run has discovered nothing."""

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    (world["here"] / "catalog.json").write_text("not json at all", encoding="utf-8")

    payload = _json(_run(world, "plan", "update"))

    assert payload["new"] == []
    assert payload["catalog_refreshed"] is True


def test_a_damaged_path_table_names_the_file(tmp_path: Path) -> None:
    """The path table has no fallback, so it fails with the manager's own message."""

    world = _world(tmp_path)
    table = tmp_path / "harness-paths.json"
    table.write_text("{", encoding="utf-8")

    result = _run(world, "plan", "select", paths=table)

    assert "Traceback" not in result.stderr, result.stderr
    assert "harness-paths.json" in result.stderr
    assert result.returncode == 1


# The flag table settled once every verb existed: where a flag is accepted it
# always means the same thing, and a verb with no use for one does not take it
# (ADR-0059). Every subcommand the script has is a row, because the rule has no
# exceptions — the three nobody types are as strict as the four that are typed.
# The two classes are checked differently and are one table on purpose: a verb
# a user meets is held to its manpage as well as to the parser, so the
# documented grammar and the parser cannot drift apart, and an internal
# subcommand is held to the parser alone rather than being published as user
# documentation to satisfy the check (ADR-0046).
_FLAG_TABLE = {
    "help": frozenset[str](),
    "select": frozenset({"--project", "--yes", "--dry-run"}),
    "update": frozenset({"--project", "--yes", "--dry-run"}),
    "uninstall": frozenset({"--yes", "--dry-run"}),
    "manpage": frozenset[str](),
    "check": frozenset[str](),
    "catalog": frozenset({"--dry-run"}),
}

# The rows a user types, which are the rows that ship a manpage.
_USER_FACING = ("help", "select", "update", "uninstall")

_FLAGS = ("--project", "--yes", "--dry-run")


def _invocations(world: dict[str, Path]) -> dict[str, tuple[tuple[str, ...], ...]]:
    """Return, per table row, every invocation of the parser that reaches it.

    A user-facing verb has two: the plan half and the apply half are separate
    subparsers, and a flag the verb takes has to survive both.
    """

    return {
        "help": (("help",),),
        "select": (("plan", "select"), ("apply", "select")),
        "update": (("plan", "update"), ("apply", "update")),
        "uninstall": (("plan", "uninstall"), ("apply", "uninstall")),
        "manpage": (("manpage", "alpha"),),
        "check": (
            ("check", "--here", str(world["source"] / "skills" / "text" / "gamma")),
        ),
        "catalog": (("catalog",),),
    }


def _synopsis(page: Path) -> str:
    """Return the `## SYNOPSIS` section of a shipped manpage, verbatim and whole."""

    text = page.read_text(encoding="utf-8")
    assert "\n## SYNOPSIS\n" in text, page
    return text.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0].strip("\n")


def _options(verb: str) -> str:
    """Return one verb's optional `OPTIONS` section, and nothing after it."""

    text = (REPO_ROOT / "skills" / "kntnt" / "help" / f"{verb}.md").read_text(
        encoding="utf-8"
    )
    if "\n## OPTIONS\n" not in text:
        return ""

    return text.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]


def test_each_manpage_documents_exactly_the_flags_its_verb_takes() -> None:
    """A flag accepted and ignored teaches the user that flags sometimes lie."""

    for verb in _USER_FACING:
        options = _options(verb)
        for flag in _FLAGS:
            assert (flag in _flags(options)) == (flag in _FLAG_TABLE[verb]), (
                verb,
                flag,
            )


def test_the_parser_takes_exactly_the_flags_the_table_allows(tmp_path: Path) -> None:
    """The other half of the one table: the parser, held to the same row.

    A verb documented to take a flag it would reject is the failure ADR-0029
    was written against, and strictness re-opens it wherever the two disagree.
    So the same table drives both, and the internal subcommands are in it: the
    rule binds every subcommand the script has.
    """

    world = _world(tmp_path)
    invocations = _invocations(world)

    for name, allowed in _FLAG_TABLE.items():
        for invocation in invocations[name]:
            for flag in _FLAGS:
                result = _run(world, *invocation, flag)
                refused = f"takes no '{flag}'" in result.stderr
                assert refused == (flag not in allowed), (
                    invocation,
                    flag,
                    result.stderr,
                )
                assert "unrecognized arguments" not in result.stderr, (invocation, flag)


def test_an_internal_subcommand_is_not_published_as_a_manpage() -> None:
    """Strictness is satisfied by the parser, never by documenting a non-verb.

    `manpage`, `check`, and `catalog` are in the flag table because the rule
    has no exceptions, and a page under `help/` would make them read as verbs
    a user is invited to type (ADR-0046).
    """

    for name in _FLAG_TABLE:
        published = (MANAGER_DIR / "help" / f"{name}.md").is_file()
        assert published == (name in _USER_FACING), name


def test_help_takes_no_flags_and_says_so(tmp_path: Path) -> None:
    """`/kntnt help --yes` is an error, not a page with a note above it.

    The refusal is the script's, so the prose that routes the invocation hands
    the flag on rather than answering for it (ADR-0059).
    """

    steps = (REPO_ROOT / "skills" / "kntnt" / "steps" / "help.md").read_text(
        encoding="utf-8"
    )

    assert "no flags" in steps
    assert _options("help") == ""

    # `--help` is how the verb is reached (`SKILL.md` routes it here), so the
    # steps have to exempt it or `/kntnt --help` is met with a complaint about
    # the very argument that asked for the page.
    assert "--help" in steps

    world = _world(tmp_path)
    result = _run(world, "help", "--yes")

    assert result.returncode == 2
    assert result.stdout == ""


def test_an_unknown_subcommand_is_refused_with_the_managers_own_synopsis(
    tmp_path: Path,
) -> None:
    """`/kntnt sel` is an error, and never a guess at which verb was meant.

    The synopsis is the manager's own, taken whole off the page it ships, so
    nothing here is a second grammar free to drift from the first (ADR-0059).
    """

    world = _world(tmp_path)

    result = _run(world, "sel")

    assert result.returncode == 2
    assert "sel" in result.stderr
    assert _synopsis(MANAGER_DIR / "help.md") in result.stderr
    assert "--help" in result.stderr
    assert "unrecognized arguments" not in result.stderr
    assert "invalid choice" not in result.stderr
    assert result.stdout == ""


def test_nothing_after_an_unknown_subcommand_is_read(tmp_path: Path) -> None:
    """A line whose first word was wrong carries flags meant for another verb.

    So the rest of it is neither run as arguments to something else nor
    reported back: the unknown word is the whole of what the error names.
    """

    world = _world(tmp_path)

    result = _run(world, "updat", "--yes")

    assert result.returncode == 2
    named = result.stderr.splitlines()[0]
    assert "updat" in named
    assert "--yes" not in named
    assert result.stdout == ""


def test_a_flag_a_verb_does_not_take_is_refused_with_that_verbs_synopsis(
    tmp_path: Path,
) -> None:
    """The same shape as an unknown subcommand: error, synopsis, pointer."""

    world = _world(tmp_path)

    result = _run(world, "help", "--yes")

    assert result.returncode == 2
    assert "--yes" in result.stderr
    assert _synopsis(MANAGER_DIR / "help" / "help.md") in result.stderr
    assert "/kntnt help help" in result.stderr
    assert "unrecognized arguments" not in result.stderr
    assert result.stdout == ""


def test_the_route_into_help_is_not_a_flag_on_a_verb(tmp_path: Path) -> None:
    """`--help` and `-h` reach Help, and bare `/kntnt` still does (ADR-0027)."""

    world = _world(tmp_path)
    shipped = (MANAGER_DIR / "help.md").read_text(encoding="utf-8").strip()

    for args in ((), ("--help",), ("-h",)):
        result = _run(world, *args)

        assert result.returncode == 0, (args, result.stderr)
        assert result.stdout.strip() == shipped, args


def test_each_manager_subcommand_routes_help_flags_to_its_manpage(
    tmp_path: Path,
) -> None:
    """A help flag after a public verb addresses that verb, not the Manager."""

    world = _world(tmp_path)

    for verb in _USER_FACING:
        shipped = (MANAGER_DIR / "help" / f"{verb}.md").read_text(encoding="utf-8")
        for flag in ("--help", "-h"):
            result = _run(world, verb, flag)

            assert result.returncode == 0, (
                f"/kntnt {verb} {flag} failed instead of printing that verb's"
                f" manpage: {result.stderr} (ADR-0077). See {STANDARD}."
            )
            assert result.stdout.strip() == shipped.strip(), (
                f"/kntnt {verb} {flag} did not print help/{verb}.md verbatim"
                f" (ADR-0077). See {STANDARD}."
            )
            assert result.stderr == "", (
                f"/kntnt {verb} {flag} printed the page but also diagnosed a"
                f" help route as an error (ADR-0077). See {STANDARD}."
            )


def test_the_dependency_gate_is_invoked_with_no_flag_in_every_skill() -> None:
    """`check --here` runs first in every skill that has anything to check.

    Under strict syntax a stray flag on that call would kill the skill before
    it did anything, so the call sites are pinned here and the drift is caught
    in the suite rather than in a broken `/commit`.
    """

    gates: dict[str, str] = {}
    for path in (REPO_ROOT / "skills").glob("*/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        if "check --here" in text:
            gates[path.parent.name] = text

    assert {"agents-md", "delegation", "commit", "push", "release"} <= set(gates)
    for name, text in gates.items():
        assert 'check --here="$HERE"`' in text, (
            f'{name}: the checker is invoked as `check --here="$HERE"` and'
            f" with no flag on it. Under strict syntax a stray flag there is"
            f" refused rather than ignored, which would kill the skill before"
            f" it did anything (ADR-0059). See {STANDARD}."
        )


def test_the_manager_hands_an_unknown_subcommand_to_the_script() -> None:
    """The fallback to the help step was the tolerance in the other half.

    A typo answered by silently running Help is how everything after it became
    Help's arguments, so the step is gone and the script answers instead — and
    the agent prints what comes back rather than authoring a refusal.
    """

    steps = (
        (MANAGER_DIR / "SKILL.md")
        .read_text(encoding="utf-8")
        .partition("\n## Steps\n")[2]
    )

    assert 'scripts/kntnt.py" <subcommand>' in steps
    assert "steps/help.md" not in steps


def test_no_verb_accepts_force(tmp_path: Path) -> None:
    """`--force` was proposed for both changing verbs and dropped in design.

    The Digest answers *does this need doing* and `--yes` answers *ask me
    nothing*, so nothing was left for a third flag to mean.
    """

    world = _world(tmp_path)

    for args in (
        ("plan", "select", "--force"),
        ("apply", "select", "alpha", "--force"),
        ("plan", "update", "--force"),
        ("apply", "update", "--force", "--yes"),
        ("apply", "uninstall", "--force", "--yes"),
    ):
        result = _run(world, *args)
        assert result.returncode != 0, args
        assert "--force" in result.stderr, args


# The skills' half of strict syntax. A skill has no parser for the grammar its
# user types — `agents-md` and `delegation` have no script at all, and the
# others hand a settled command line to an engine rather than the user's own —
# so the agent is the only thing that can refuse, and the rule has to be stated
# where that agent reads it (ADR-0059). What follows is prose held to the
# behaviour, which is the only seam a script-less skill has (ADR-0046).


def _shipped_skills() -> list[Path]:
    """Every collection skill's directory. The Manager is no entry of its own."""

    directories = sorted(p.parent for p in (REPO_ROOT / "skills").glob("*/*/SKILL.md"))
    assert directories
    return directories


def _skill_bodies() -> list[Path]:
    """Every `SKILL.md` the collection ships, the Manager's own included.

    The Manager sits a level above the categories, so the glob that finds a
    Catalog skill cannot see it — and it is a Skill by the collection's own
    definition, so a rule about what a body carries is a rule about its body
    too.
    """

    return [*(d / "SKILL.md" for d in _shipped_skills()), MANAGER_DIR / "SKILL.md"]


def _root_manpages() -> list[Path]:
    """Every root page whose Envelope contract its own Skill executes."""

    return [*(d / "help.md" for d in _shipped_skills()), MANAGER_DIR / "help.md"]


def _manpages() -> list[Path]:
    """Every manpage the collection ships, found rather than listed.

    Every Skill ships its root page and a Skill with subcommands ships their
    page tree under `help/`. The Manager follows the same user-facing shape;
    its separate `steps/` tree is agent procedure and therefore excluded.
    """

    pages = [
        *_root_manpages(),
        *(
            page
            for d in _shipped_skills()
            for page in sorted((d / "help").rglob("*.md"))
        ),
        *sorted((MANAGER_DIR / "help").rglob("*.md")),
    ]
    assert pages
    return pages


# The fixed core every manpage carries. Further conventional sections are
# selected by content, with Dependencies retained as a local product rule.
_MANPAGE_SECTIONS = (
    "## NAME",
    "## SYNOPSIS",
    "## DESCRIPTION",
    "## DEPENDENCIES",
    "## SEE ALSO",
)


def _the_sections() -> str:
    """The required set as prose, so a message and the standard cannot drift."""

    quoted = [f"`{heading}`" for heading in _MANPAGE_SECTIONS]
    return f"{', '.join(quoted[:-1])}, and {quoted[-1]}"


def _section(text: str, heading: str, where: Path) -> str:
    """Return one `## ` section of a Markdown file, and nothing after it."""

    marker = f"\n{heading}\n"
    assert marker in text, (
        f"{where} carries no `{heading}` section, so the rule read out of it"
        f" cannot be checked at all. Every manpage carries {_the_sections()},"
        f" while `## POSITIONAL ARGUMENTS`, `## OPTIONS`, `## DIAGNOSTICS`, and"
        f" other conventional sections appear only where they have useful"
        f" content. See {STANDARD}."
    )
    return text.partition(marker)[2].partition("\n## ")[0]


def _optional_section(text: str, heading: str) -> str:
    """Return an optional `## ` section, or an empty string when omitted."""

    marker = f"\n{heading}\n"
    if marker not in text:
        return ""

    return text.partition(marker)[2].partition("\n## ")[0]


def _command_entries(page: Path) -> dict[str, str]:
    """Return immediate command names and descriptions from one manpage."""

    # Split the Commands section into the tagged terms and prose that follow.
    text = page.read_text(encoding="utf-8")
    commands = _section(text, "## COMMANDS", page)
    paragraphs = [part.strip() for part in commands.strip().split("\n\n")]
    entries: dict[str, str] = {}

    # A command is a tagged term followed by its short description paragraph.
    for index, paragraph in enumerate(paragraphs):
        match = re.match(r"^\*\*([a-z][a-z-]*)\*\*(?:\s|$)", paragraph)
        if match is None:
            continue
        assert index + 1 < len(paragraphs), (
            f"{page}: `{match.group(1)}` has no short description after its"
            f" tagged term. Every immediate subcommand carries one"
            f" (ADR-0077). See {STANDARD}."
        )
        description = paragraphs[index + 1]
        assert not description.startswith("**"), (
            f"{page}: `{match.group(1)}` is followed by another tagged term"
            f" instead of its short description (ADR-0077). See {STANDARD}."
        )
        entries[match.group(1)] = description

    return entries


def _command_groups() -> list[tuple[Path, Path]]:
    """Return each command-list page and the directory it must describe."""

    # Inspect every user-facing help tree, including nested command paths.
    groups: list[tuple[Path, Path]] = []
    owners = [*_shipped_skills(), MANAGER_DIR]

    # The root page lists immediate children; a command with children lists its own.
    for owner in owners:
        help_directory = owner / "help"
        if not help_directory.is_dir():
            continue
        groups.append((owner / "help.md", help_directory))
        for directory in sorted(
            path for path in help_directory.rglob("*") if path.is_dir()
        ):
            if not any(directory.glob("*.md")):
                continue
            relative = directory.relative_to(help_directory)
            parent = help_directory / relative.with_suffix(".md")
            groups.append((parent, directory))

    return groups


_MODEL_SELECTOR_MANPAGES = frozenset(
    {
        "chart.md",
        "compare.md",
        "config.md",
        "config/add.md",
        "config/edit.md",
        "config/history.md",
        "config/remove.md",
        "config/reset.md",
        "config/show.md",
        "capture.md",
        "observe.md",
        "recommend.md",
        "record.md",
        "route.md",
        "setup.md",
        "status.md",
        "update.md",
    }
)


def test_model_selector_ships_and_routes_one_manpage_per_subcommand() -> None:
    """Every accepted command path has a deterministic `--help` target."""

    # Compare the complete accepted command set with the shipped page tree.
    help_directory = MODEL_SELECTOR_DIR / "help"
    actual = {
        str(path.relative_to(help_directory)) for path in help_directory.rglob("*.md")
    }
    skill = (MODEL_SELECTOR_DIR / "SKILL.md").read_text(encoding="utf-8")
    help_section = _section(skill, "## Help", MODEL_SELECTOR_DIR / "SKILL.md")

    assert actual == _MODEL_SELECTOR_MANPAGES, (
        f"{MODEL_SELECTOR_DIR}: the subcommand page tree is {sorted(actual)},"
        f" but the accepted command paths are"
        f" {sorted(_MODEL_SELECTOR_MANPAGES)} (ADR-0077). See {STANDARD}."
    )
    assert "--help" in help_section, (
        f"{MODEL_SELECTOR_DIR / 'SKILL.md'}: subcommand pages exist but the"
        f" Help section has no direct `--help` route to them (ADR-0077). See"
        f" {STANDARD}."
    )

    # Hold every file to an explicit deterministic route in the Skill body.
    for relative in _MODEL_SELECTOR_MANPAGES:
        assert f"`$HERE/help/{relative}`" in help_section, (
            f"{MODEL_SELECTOR_DIR / 'SKILL.md'}: the Help section does not"
            f" route the `{relative}` manpage (ADR-0077). See {STANDARD}."
        )


def test_every_command_page_lists_all_immediate_subcommands_with_descriptions() -> None:
    """A command tree is discoverable without guessing names from prose."""

    groups = _command_groups()
    assert groups, "no command page tree was found, so this check judged nothing"

    # Each parent page names exactly the pages immediately below it.
    for page, directory in groups:
        expected = {path.stem for path in directory.glob("*.md")}
        entries = _command_entries(page)

        assert set(entries) == expected, (
            f"{page}: `COMMANDS` lists {sorted(entries)}, while the immediate"
            f" command pages are {sorted(expected)}. A parent lists every"
            f" immediate child and no nested grandchild (ADR-0077). See"
            f" {STANDARD}."
        )
        assert all(entries.values()), (
            f"{page}: every immediate subcommand carries a short description"
            f" after its tagged term (ADR-0077). See {STANDARD}."
        )


def _manpage_name(page: Path) -> str:
    """Return the invocation name a shipped page documents."""

    if page == MANAGER_DIR / "help.md":
        return "kntnt"

    if page.parent == MANAGER_DIR / "help":
        return f"kntnt {page.stem}"

    for directory in _shipped_skills():
        help_directory = directory / "help"
        if help_directory in page.parents:
            relative = page.relative_to(help_directory).with_suffix("")
            command = " ".join(relative.parts)
            return f"{directory.name} {command}"

    return page.parent.name


def _hint(directory: Path) -> str:
    """Return one skill's `argument-hint`, which is the grammar the harness shows."""

    for line in (directory / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("argument-hint:"):
            return line.partition(":")[2].strip().strip("\"'")
    raise AssertionError(
        f"{directory}: every skill declares an `argument-hint`. It is the"
        f" grammar the harness shows a user before anything is typed, and one"
        f" of the three places the flags a skill takes are named — the manpage's"
        f" `## SYNOPSIS` and `## OPTIONS` being the others (ADR-0059). See"
        f" {STANDARD}."
    )


def _flags(text: str) -> set[str]:
    """Every long flag named in a piece of prose, `--help` excepted.

    `--help` is the route into the manpage rather than a flag on a form, so it
    is documented nowhere and belongs to no row of the grammar.
    """

    return {word for word in re.findall(r"--[a-z][a-z-]*", text)} - {"--help"}


def test_every_skill_exposes_the_invocation_envelope_before_its_grammar() -> None:
    """Every caller meets the same envelope before Skill-specific parsing.

    The suffix is caller-neutral and reserved across the Collection, so a
    future Skill discovered by the body glob must expose it in the harness
    hint and separate it before either help routing or formal validation.
    """

    # Discover every body so a future Skill cannot omit the shared first step.
    for body in _skill_bodies():
        # Read only the body surface the harness executes.
        text = body.read_text(encoding="utf-8")
        envelope = _section(text, "## Invocation Envelope", body)

        # Hold exposure, ordering, and the boundary into deterministic parsers.
        assert _hint(body.parent).endswith("[-- <instruction>]"), (
            f"{body}: the harness hint omits the optional Contextual"
            f" Instruction suffix required by ADR-0078. See {STANDARD}."
        )
        assert text.index("\n## Invocation Envelope\n") < text.index("\n## Help\n"), (
            f"{body}: Envelope splitting must precede help routing and formal"
            f" validation (ADR-0078). See {STANDARD}."
        )
        assert "before help routing or formal validation" in envelope.lower(), (
            f"{body}: the executable Envelope section does not state its"
            f" required ordering (ADR-0078). See {STANDARD}."
        )
        assert "`## INVOCATION ENVELOPE` section of `$HERE/help.md`" in envelope, (
            f"{body}: a directly installed Skill must read its executable"
            f" Envelope contract from its own root manpage (ADR-0078). See"
            f" {STANDARD}."
        )
        assert "Pass only the Formal Invocation to scripts" in envelope, (
            f"{body}: scripts and nested parsers receive only Formal Invocation"
            f" input (ADR-0078). See {STANDARD}."
        )


def test_invocation_envelope_defines_the_reserved_separator_without_inference() -> None:
    """The shared executable contract distinguishes context from formal data.

    These are worked inputs from issue #87 rather than a parser reimplemented
    in the test: prose is the public seam for a Skill whose agent performs the
    split, and every body above follows this one discovered reference.
    """

    # Discover every executable root contract, including the Manager's.
    for root in _root_manpages():
        text = _section(
            root.read_text(encoding="utf-8"), "## INVOCATION ENVELOPE", root
        )

        # Pin every separator distinction to literal issue examples.
        for phrase in (
            "same line",
            "after blank lines",
            "must contain non-whitespace text",
            "including later `--` tokens",
            "Without the separator",
            "`--force`",
            "`foo--bar`",
            "`` `--` ``",
            '`"--"`',
            "Redundant but applicable guidance is valid",
        ):
            # Refuse the loss of an accepted or rejected separator distinction.
            assert phrase in text, (
                f"{root}: the executable Envelope omits {phrase!r}, so it no"
                f" longer distinguishes an issue #87 syntax case (ADR-0078)."
                f" See {STANDARD}."
            )


def test_invocation_envelope_carries_worked_split_outcomes() -> None:
    """Concrete payloads pin the agent-executed split at the prose seam."""

    # Keep independent, worked outcomes for every syntax case in issue #87.
    cases = (
        "| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |",
        r"| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |",
        "| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |",
        "| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |",
        "| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |",
        '| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |',
        "| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |",
    )

    # Hold each Skill's locally executable examples to the independent outcomes.
    for root in _root_manpages():
        text = _section(
            root.read_text(encoding="utf-8"), "## INVOCATION ENVELOPE", root
        )

        # A missing row removes the expected result, not a descriptive word.
        for case in cases:
            # Refuse a scenario whose independently worked outcome disappeared.
            assert case in text, (
                f"{root}: worked Envelope outcomes omit `{case}`, leaving that"
                f" issue #87 split unpinned at the executable prose seam"
                f" (ADR-0078). See {STANDARD}."
            )


def test_skill_standard_requires_every_invocation_envelope_surface() -> None:
    """Contributors meet the contract before discovered checks enforce it."""

    # Read the contributor-facing source of the rules asserted by this suite.
    standard = (REPO_ROOT / STANDARD).read_text(encoding="utf-8")

    # Hold all five authored surfaces and the separator's non-option status.
    for phrase in (
        "`[-- <instruction>]`",
        "`## Invocation Envelope`",
        "`## INVOCATION ENVELOPE` section of the Skill's own `$HERE/help.md`",
        "`[**--** *INSTRUCTION*]`",
        "`## INVOCATION ENVELOPE`",
        "separator, not an option",
    ):
        # Keep each asserted rule discoverable before this test reports it.
        assert phrase in standard, (
            f"{STANDARD}: the contributor standard omits {phrase!r}, so an"
            f" author meets the Envelope rule only after this suite fails"
            f" (ADR-0078)."
        )


def test_nested_skill_calls_propagate_only_relevant_context_explicitly() -> None:
    """A nested Envelope is constructed at the call, never blindly forwarded."""

    # Discover peer body references in every shipped Skill's executable prose.
    nested_skill = re.compile(r"\$HERE/\.\./([A-Za-z0-9_-]+)/SKILL\.md")
    calls = [
        (body, target, paragraph)
        for body in _skill_bodies()
        for paragraph in body.read_text(encoding="utf-8").split("\n\n")
        for target in nested_skill.findall(paragraph)
    ]
    assert calls, "No nested Skill calls were discovered at the documented seam"

    # Hold selective propagation at each concrete nested call.
    for body, target, call in calls:
        # Require both Envelope parts and the relevance filter at the call site.
        assert "Formal Invocation" in call, (
            f"{body}: the nested call to {target} does not construct an"
            f" explicit Formal Invocation (ADR-0078). See {STANDARD}."
        )
        assert "Contextual Instruction" in call, (
            f"{body}: context propagation into nested Skill {target} is"
            f" implicit rather than an explicit inner Envelope (ADR-0078)."
            f" See {STANDARD}."
        )
        assert "relevant" in call, (
            f"{body}: nested Skill {target} could receive the outer"
            f" instruction blindly instead of only relevant guidance"
            f" (ADR-0078). See {STANDARD}."
        )


def test_manager_help_passes_only_formal_arguments_to_its_script() -> None:
    """The help adapter never hands the Contextual Instruction to argparse."""

    # Read the adapter that turns the Manager's help route into script input.
    steps = (MANAGER_DIR / "steps" / "help.md").read_text(encoding="utf-8")

    # Refuse the old whole-payload wording and require the new parser boundary.
    assert "Formal Invocation arguments" in steps, (
        f"{MANAGER_DIR / 'steps' / 'help.md'}: the Manager must pass only Formal"
        f" Invocation input to its parser (ADR-0078). See {STANDARD}."
    )
    assert "Every other argument the user gave" not in steps, (
        f"{MANAGER_DIR / 'steps' / 'help.md'}: whole-payload forwarding would"
        f" leak Contextual Instruction into argparse (ADR-0078). See {STANDARD}."
    )


def test_every_skill_answers_a_form_its_grammar_forbids_with_its_own_synopsis() -> None:
    """One failure behaviour per skill, and no error text authored by an agent.

    An undeclared flag, an invalid combination, and an incomplete form are the
    same refusal, in the shape every refusal in this collection has: what was
    wrong, the synopsis of what was addressed, and where to read the page in
    full. The synopsis is the one shipped in `help.md`, never a second grammar
    composed on the spot to answer with.
    """

    for directory in _shipped_skills():
        skill = (directory / "SKILL.md").read_text(encoding="utf-8")
        page = (directory / "help.md").read_text(encoding="utf-8")

        assert "`## SYNOPSIS` section of `$HERE/help.md`" in skill, (
            f"{directory}: an invalid form is answered with the `## SYNOPSIS`"
            f" section of `$HERE/help.md`, printed verbatim. A skill has no"
            f" parser — the agent reading these files is the whole of the"
            f" enforcement — so a refusal composed on the spot is a second"
            f" grammar, free to drift from the one the page documents"
            f" (ADR-0059). See {STANDARD}."
        )
        assert f"`/{directory.name} --help` for the page in full" in skill, (
            f"{directory}: the refusal closes by pointing at"
            f" `/{directory.name} --help`, so a user given one line of synopsis"
            f" is told where the rest of the page is (ADR-0059). See"
            f" {STANDARD}."
        )
        assert "refused rather than ignored" in page, (
            f"{directory}: the manpage says a flag with no work to do is"
            f" refused rather than ignored. The strictness is documented as"
            f" well as performed, or a reader meets it first as an error"
            f" (ADR-0059). See {STANDARD}."
        )


def test_a_skills_hint_and_manpage_agree_on_the_flags_it_takes() -> None:
    """The defence ADR-0059 names: one grammar, read by both halves.

    Strictness re-opens ADR-0029's failure wherever the documented grammar and
    the thing that enforces it disagree, and for a skill the enforcer reads the
    same files the user does. So a flag advertised in the hint and missing from
    the page, or the other way round, is a failure here rather than a refusal
    in somebody's session.
    """

    for directory in _shipped_skills():
        manpage = directory / "help.md"
        page = manpage.read_text(encoding="utf-8")
        documented = _flags(_optional_section(page, "## OPTIONS"))

        assert _flags(_hint(directory)) == documented, (
            f"{directory}: `argument-hint` names"
            f" {sorted(_flags(_hint(directory)))} and the manpage's"
            f" `## OPTIONS` names {sorted(documented)}. The two are one set:"
            f" the skill has no parser, so a flag advertised in one and missing"
            f" from the other is a grammar disagreeing with itself, and the"
            f" refusal lands in a user's session instead of here (ADR-0059)."
            f" See {STANDARD}."
        )
        assert _flags(_section(page, "## SYNOPSIS", manpage)) == documented, (
            f"{manpage}: `## SYNOPSIS` names"
            f" {sorted(_flags(_section(page, '## SYNOPSIS', manpage)))} and"
            f" `## OPTIONS` names {sorted(documented)}. The synopsis is what a"
            f" refusal quotes verbatim, so a flag missing from it is a flag the"
            f" user is refused for without being shown (ADR-0059). See"
            f" {STANDARD}."
        )


def test_no_hint_form_offers_a_combination_its_synopsis_forbids() -> None:
    """The aggregate flag set is blind to which flags may appear together.

    `argument-hint` is one line and may collapse forms the manpage spells out
    separately, so the two are not held to the same count of forms. What is
    held is that a combination the harness advertises is one the page allows:
    the hint's alternatives are separated by ` | `, and each one's flags have
    to fit inside a single `## SYNOPSIS` form. Comparing the three surfaces as
    one set of names cannot see this — a hint offering a scope flag and a
    confirmation flag alongside a status form that writes nothing passes that
    check, and did — and the user meets the disagreement as a refusal for a
    form the harness itself told them to type.
    """

    for directory in _shipped_skills():
        manpage = directory / "help.md"
        synopsis = _section(manpage.read_text(encoding="utf-8"), "## SYNOPSIS", manpage)
        allowed = [_flags(line) for line in synopsis.splitlines() if line.strip()]

        assert allowed, (
            f"{manpage}: `## SYNOPSIS` names no form, so this check judged"
            f" nothing. See {STANDARD}."
        )

        for form in _hint(directory).split(" | "):
            offered = _flags(form)
            assert any(offered <= permitted for permitted in allowed), (
                f"{directory}: the `argument-hint` form `{form.strip()}` offers"
                f" {sorted(offered)}, and no `## SYNOPSIS` form allows that"
                f" combination — the page permits"
                f" {[sorted(permitted) for permitted in allowed]}. The hint may"
                f" collapse forms the page separates, but never widen one: a"
                f" flag is refused where it has no work to do on the form it"
                f" was given with (ADR-0059). See {STANDARD}."
            )


def test_no_form_of_delegations_grammar_carries_yes_and_status_at_once() -> None:
    """`--yes` answers a confirmation, and `status` never asks for one.

    The flag is only ever acted on where a persistent scope is written, so
    `/delegation status --yes` reads as a flag that does nothing — the case
    ADR-0059 settled, and one the command-path grammar leaves exactly as it
    found it (ADR-0109).
    """

    directory = DELEGATION_DIR
    forms = _delegation_forms()

    assert any("--yes" in form for form in forms), (
        f"{directory}: no form of the grammar names `--yes`, so this check"
        f" judged nothing. See {STANDARD}."
    )
    assert any("status" in form for form in forms), (
        f"{directory}: no form of the grammar names `status`, so this check"
        f" judged nothing. See {STANDARD}."
    )
    for form in forms:
        assert not ("--yes" in form and "status" in form), (
            f"{directory}: the form `{form}` offers `--yes` on `status`, which"
            f" writes nothing and so asks nothing. A flag with no work to do is"
            f" refused rather than ignored, and a grammar that advertises one"
            f" teaches that flags sometimes do nothing (ADR-0059). See"
            f" {STANDARD}."
        )


def test_delegation_refuses_an_incomplete_form_rather_than_asking() -> None:
    """`/delegation --user` with no command path prints the synopsis and stops.

    Its two halves disagreed: the arguments asked for `on`, `off`, or `status`
    while step 1 stopped. The half the agent executes is the true one (ADR-0046),
    and `--yes` settles it beyond consistency — a question with three outcomes
    has no answer under the flag (ADR-0029), so *ask* needs a special case
    there and *error* needs none. The form is now a scope flag with no command
    path, and it is refused for the same reason (ADR-0109).
    """

    directory = REPO_ROOT / "skills" / "agents" / "delegation"
    skill = (directory / "SKILL.md").read_text(encoding="utf-8")
    page = (directory / "help.md").read_text(encoding="utf-8")

    incomplete = [
        line
        for line in _section(skill, "## Arguments", directory / "SKILL.md").splitlines()
        if "no command path" in line
    ]
    assert incomplete, (
        f"{directory}: the parse rules no longer name the incomplete form, so"
        f" this check judged nothing. See {STANDARD}."
    )
    for line in incomplete:
        assert "ask" not in line.lower(), (
            f"{directory}: `{line.strip()}` answers an incomplete form by"
            f" asking. A question with three outcomes has no answer under"
            f" `--yes` (ADR-0029), so the incomplete form is refused with the"
            f" synopsis like every other invalid one (ADR-0059). See"
            f" {STANDARD}."
        )

    assert "changes nothing and asks" not in page, (
        f"{directory / 'help.md'}: the manpage still documents the incomplete"
        f" form as asking, which is the half the agent does not execute. Where"
        f" the two halves disagree the body is the true one (ADR-0046). See"
        f" {STANDARD}."
    )
    diagnostics = _section(page, "## DIAGNOSTICS", directory / "help.md").lower()
    assert "prints the synopsis" in diagnostics, (
        f"{directory / 'help.md'}: `DIAGNOSTICS` says the incomplete form prints the"
        f" synopsis. A reader who has not run the skill cannot tell a refusal"
        f" from a no-op unless the page names what the refusal does, and the"
        f" refusal with the synopsis is what the body performs (ADR-0059). See"
        f" {STANDARD}."
    )


# The Skill whose mode is addressed through a command path, the pages that
# path answers to, and the `--`-prefixed spelling it no longer has. The
# spellings went rather than becoming aliases: two spellings for one form are
# the ambiguity ADR-0103 removes, and an alias would keep it (issue #115).
BRIEF_DIR = REPO_ROOT / "skills" / "agents" / "brief"
BRIEF_COMMANDS = frozenset({"on.md", "off.md", "status.md"})
FLAG_SPELLING = re.compile(r"--(?:on|off|status)\b")

# The name the Skill answered to before ADR-0113, in both the spellings it was
# written in: the command's own `tldr` and the standing mode's `TL;DR`.
FORMER_NAME = re.compile(r"(?i)tl;?dr")

# The shipped surfaces the former name may not survive on. Records and released
# changelog entries are deliberately outside it: a record's decision stands and
# an entry is an account of what shipped, so neither is rewritten (ADR-0075).
SHIPPED_TEXT = frozenset({".md", ".json", ".yaml", ".yml", ".py", ".txt"})


def _shipped_surfaces() -> list[Path]:
    """Every file a user of this collection reads the Skill's name from."""

    return [
        *sorted(
            path
            for path in (REPO_ROOT / "skills").rglob("*")
            if path.is_file() and path.suffix in SHIPPED_TEXT
        ),
        REPO_ROOT / "README.md",
        REPO_ROOT / "CONTEXT.md",
    ]


def test_the_reframing_skill_answers_to_brief_on_every_shipped_surface() -> None:
    """One name for the command and for the standing mode it carries.

    `tldr` named the bare form and nothing else. The standing mode adopts a
    perspective for later replies and deliberately revisits nothing, so under
    the old name `on` read as *turn the too-long-didn't-read on* and promised
    a summary that never arrived. A Skill has no parser — the agent reading
    these files is the whole of the enforcement — so a surface left spelling
    the old name is a second name the Skill still answers to (ADR-0113).
    """

    assert BRIEF_DIR.is_dir(), (
        f"{BRIEF_DIR}: the Skill's directory is its name under its Category,"
        f" and the rename is not done while the old one is what exists"
        f" (ADR-0113). See {STANDARD}."
    )
    assert not (REPO_ROOT / "skills" / "agents" / "tldr").exists(), (
        f"{REPO_ROOT / 'skills' / 'agents' / 'tldr'}: the old directory is"
        f" still here, so the collection ships the Skill under two names"
        f" (ADR-0113). See {STANDARD}."
    )

    body = (BRIEF_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "\nname: brief\n" in body, (
        f"{BRIEF_DIR / 'SKILL.md'}: the `name` frontmatter is what every"
        f" reader outside this collection resolves the Skill by, so it spells"
        f" the name the directory does (ADR-0113). See {STANDARD}."
    )

    persistence = (BRIEF_DIR / "references" / "persist.md").read_text(encoding="utf-8")
    for marker in ("<!-- kntnt:brief -->", "<!-- /kntnt:brief -->"):
        assert marker in persistence, (
            f"{BRIEF_DIR / 'references' / 'persist.md'}: the managed block's"
            f" markers name the Skill, and the Skill writes and reads only the"
            f" one spelling — a second accepted marker is a compatibility"
            f" branch that never leaves the file (ADR-0113). See {STANDARD}."
        )

    surfaces = _shipped_surfaces()

    # A glob that matched nothing would pass the loop below without reading a
    # single surface, which is the one outcome this check exists to catch.
    assert len(surfaces) > 2

    for path in surfaces:
        found = sorted(set(FORMER_NAME.findall(path.read_text(encoding="utf-8"))))
        assert not found, (
            f"{path}: {found} spells the name the Skill and its standing mode"
            f" no longer answer to. Every shipped surface names it `brief`,"
            f" the records and the released changelog entries excepted"
            f" (ADR-0113). See {STANDARD}."
        )


def _brief_readme_section() -> str:
    """The README's own entry for `/brief`, which states the forms it accepts."""

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    return readme.partition("\n### brief\n")[2].partition("\n### ")[0]


def test_brief_ships_and_routes_one_manpage_per_command_path() -> None:
    """`on`, `off`, and `status` each answer to their own help route.

    A command path is exactly what a page under `help/` answers to (ADR-0077),
    so the three pages are what make these tokens a path rather than operands —
    and what lets a refusal quote the grammar the invalid form violated rather
    than the whole Skill's.
    """

    help_directory = BRIEF_DIR / "help"
    assert help_directory.is_dir(), (
        f"{BRIEF_DIR}: the mode is addressed through a command path, and every"
        f" public command path has an addressable manpage under `help/`"
        f" (ADR-0077, ADR-0103). See {STANDARD}."
    )

    actual = {
        str(page.relative_to(help_directory)) for page in help_directory.rglob("*.md")
    }
    assert actual == set(BRIEF_COMMANDS), (
        f"{BRIEF_DIR}: the command page tree is {sorted(actual)}, while the"
        f" accepted command paths are {sorted(BRIEF_COMMANDS)} (ADR-0077,"
        f" ADR-0103). See {STANDARD}."
    )

    body = BRIEF_DIR / "SKILL.md"
    help_section = _section(body.read_text(encoding="utf-8"), "## Help", body)
    for relative in sorted(BRIEF_COMMANDS):
        assert f"`$HERE/help/{relative}`" in help_section, (
            f"{body}: the `## Help` section does not route the `{relative}`"
            f" manpage. `/<skill> <command-path> --help` prints the most"
            f" specific recognized path's page verbatim (ADR-0077). See"
            f" {STANDARD}."
        )
    assert "-h" in help_section, (
        f"{body}: `-h` is the identical short route into an addressed page,"
        f" so the command paths answer to it too (ADR-0077). See {STANDARD}."
    )


def test_brief_spells_its_mode_as_a_command_path_and_never_as_a_flag() -> None:
    """No `--`-prefixed spelling survives anywhere the Skill is described.

    The flag spellings go rather than becoming aliases. Two spellings for one
    form is the ambiguity ADR-0103 exists to remove, and a Skill has no parser
    — the agent reading these files is the whole of the enforcement — so a
    spelling left standing on any surface is a spelling that is accepted.
    """

    surfaces = sorted(BRIEF_DIR.rglob("*.md"))

    # A glob that matched nothing would pass the loop below without reading a
    # single surface, which is the one outcome this check exists to catch.
    assert surfaces

    for path in surfaces:
        found = sorted(set(FLAG_SPELLING.findall(path.read_text(encoding="utf-8"))))
        assert not found, (
            f"{path}: {found} is a `--`-prefixed spelling of a command path."
            f" `on`, `off`, and `status` are reached as a command path and by"
            f" no second spelling, the flags having gone rather than become"
            f" aliases (ADR-0103). See {STANDARD}."
        )

    section = _brief_readme_section()
    assert section.strip(), (
        f"{REPO_ROOT / 'README.md'}: the `### brief` section could not be"
        f" found, so this check judged nothing. See {STANDARD}."
    )
    assert not FLAG_SPELLING.findall(section), (
        f"{REPO_ROOT / 'README.md'}: the `### brief` section still writes a"
        f" `--`-prefixed spelling of a command path (ADR-0103). See"
        f" {STANDARD}."
    )
    for form in ("/brief on", "/brief status"):
        assert form in section, (
            f"{REPO_ROOT / 'README.md'}: the `### brief` section does not state"
            f" the `{form}` form. The README is where somebody decides whether"
            f" they want the Skill, so it states the forms it accepts"
            f" (ADR-0103). See {STANDARD}."
        )


def test_brief_accepts_no_unseparated_text_after_its_name_or_command_path() -> None:
    """The free-text operand is gone, and the separator is the one channel.

    `/brief` was the only Skill in the collection whose formal grammar accepted
    free text, which is what forced its mode onto flags in the first place.
    The Invocation Envelope's reserved separator now carries what the operand
    carried, so the operand is a second unseparated channel for one thing and
    goes with the ambiguity it caused (ADR-0078, ADR-0103).
    """

    body = BRIEF_DIR / "SKILL.md"
    text = body.read_text(encoding="utf-8")
    arguments = _section(text, "## Arguments", body)
    page = (BRIEF_DIR / "help.md").read_text(encoding="utf-8")

    assert "\n## POSITIONAL ARGUMENTS\n" not in page, (
        f"{BRIEF_DIR / 'help.md'}: the page still documents a positional"
        f" argument. The Skill takes no operand, and an empty conventional"
        f" section is omitted rather than filled (ADR-0103). See {STANDARD}."
    )

    unseparated = (
        "A token that is neither a recognized command path nor a declared flag"
    )
    assert unseparated in arguments, (
        f"{body}: the argument prose does not refuse unseparated text after"
        f" the Skill name or a command path. Anything not carried by a"
        f" recognized token is an invalid form rather than an instruction"
        f" (ADR-0103). See {STANDARD}."
    )


def test_brief_reads_its_replacement_answer_from_the_contextual_instruction() -> None:
    """What the operand did is not lost, and the body says where it went.

    Widening the range, naming a language, narrowing the subject, and
    constraining the output are each a choice the Skill's contract leaves
    open, which is exactly what a Contextual Instruction is permitted to
    settle — so the step that settles the range and the step that writes the
    replacement answer read it, and an instruction that would widen the Skill
    takes the Envelope's context refusal rather than a syntax refusal.
    """

    body = BRIEF_DIR / "SKILL.md"
    text = body.read_text(encoding="utf-8")
    arguments = _section(text, "## Arguments", body)
    steps = _section(text, "## Steps", body)

    for phrase in (
        "widen the range",
        "name a language",
        "narrow the subject",
        "constrain the output",
    ):
        assert phrase in arguments, (
            f"{body}: the argument prose does not say that a request to"
            f" {phrase} arrives through the Contextual Instruction. The"
            f" operand carried it before, and a capability whose channel is"
            f" unwritten is a capability nobody can reach (ADR-0078,"
            f" ADR-0103). See {STANDARD}."
        )

    for marker in ("settle the range", "replacement answer"):
        reading = [line for line in steps.splitlines() if marker in line]
        assert reading, (
            f"{body}: no step names {marker!r}, so this check judged nothing."
            f" See {STANDARD}."
        )
        for line in reading:
            assert "Contextual Instruction" in line, (
                f"{body}: the step `{line.strip()[:60]}...` no longer reads the"
                f" Contextual Instruction. It is where the free-form tail's"
                f" work went, so a step that does not read it silently drops"
                f" what the user asked for (ADR-0103). See {STANDARD}."
            )


# The other Skill whose mode is addressed through a command path, the pages
# that path answers to, and the spellings it no longer has. Its scope became a
# flag and the session, being the default, lost its name with them: one intent
# has one spelling where a scope word, a state word, six aliases, and a free
# order gave it a dozen (issue #116).
DELEGATION_DIR = REPO_ROOT / "skills" / "agents" / "delegation"
DELEGATION_COMMANDS = frozenset({"on.md", "off.md", "status.md"})
ALIAS_SPELLING = re.compile(r"--(?:on|off|status|session)\b")
SCOPE_OPERAND = re.compile(r"(?<![-\w])(?:session|project|user)\b")


def _delegation_readme_section() -> str:
    """The README's own entry for `/delegation`, which states the forms it takes."""

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    return readme.partition("\n### delegation\n")[2].partition("\n### ")[0]


def _delegation_forms() -> list[str]:
    """Every form the Skill's grammar surfaces write, hint and synopsis alike."""

    forms = list(_hint(DELEGATION_DIR).split(" | "))
    pages = [
        DELEGATION_DIR / "help.md",
        *sorted((DELEGATION_DIR / "help").rglob("*.md")),
    ]
    for page in pages:
        section = _section(page.read_text(encoding="utf-8"), "## SYNOPSIS", page)
        forms.extend(line for line in section.splitlines() if line.strip())
    return forms


def test_delegation_ships_and_routes_one_manpage_per_command_path() -> None:
    """`on`, `off`, and `status` each answer to their own help route.

    A command path is exactly what a page under `help/` answers to (ADR-0077),
    so the three pages are what make these tokens a path rather than operands,
    and what lets a refusal quote the grammar the invalid form violated rather
    than the whole Skill's (ADR-0109).
    """

    help_directory = DELEGATION_DIR / "help"
    assert help_directory.is_dir(), (
        f"{DELEGATION_DIR}: the mode is addressed through a command path, and"
        f" every public command path has an addressable manpage under `help/`"
        f" (ADR-0077, ADR-0109). See {STANDARD}."
    )

    actual = {
        str(page.relative_to(help_directory)) for page in help_directory.rglob("*.md")
    }
    assert actual == set(DELEGATION_COMMANDS), (
        f"{DELEGATION_DIR}: the command page tree is {sorted(actual)}, while"
        f" the accepted command paths are {sorted(DELEGATION_COMMANDS)}"
        f" (ADR-0077, ADR-0109). See {STANDARD}."
    )

    body = DELEGATION_DIR / "SKILL.md"
    help_section = _section(body.read_text(encoding="utf-8"), "## Help", body)
    for relative in sorted(DELEGATION_COMMANDS):
        assert f"`$HERE/help/{relative}`" in help_section, (
            f"{body}: the `## Help` section does not route the `{relative}`"
            f" manpage. `/<skill> <command-path> --help` prints the most"
            f" specific recognized path's page verbatim (ADR-0077). See"
            f" {STANDARD}."
        )
    assert "-h" in help_section, (
        f"{body}: `-h` is the identical short route into an addressed page,"
        f" so the command paths answer to it too (ADR-0077). See {STANDARD}."
    )


def test_delegation_spells_its_mode_as_a_command_path_and_never_as_a_flag() -> None:
    """No `--`-prefixed spelling survives anywhere the Skill is described.

    The alias set goes rather than being deprecated. Two spellings for one form
    is the defect, a period in which both work is the defect with a schedule
    attached, and a Skill has no parser — the agent reading these files is the
    whole of the enforcement — so a spelling left standing on any surface is a
    spelling that is accepted (ADR-0109).
    """

    surfaces = sorted(DELEGATION_DIR.rglob("*.md"))

    # A glob that matched nothing would pass the loop below without reading a
    # single surface, which is the one outcome this check exists to catch.
    assert surfaces

    for path in surfaces:
        found = sorted(set(ALIAS_SPELLING.findall(path.read_text(encoding="utf-8"))))
        assert not found, (
            f"{path}: {found} is a `--`-prefixed spelling of a command path or"
            f" of the unnamed default scope. `on`, `off`, and `status` are"
            f" reached as a command path and by no second spelling, and the"
            f" session scope has no spelling at all (ADR-0109). See"
            f" {STANDARD}."
        )

    section = _delegation_readme_section()
    assert section.strip(), (
        f"{REPO_ROOT / 'README.md'}: the `### delegation` section could not be"
        f" found, so this check judged nothing. See {STANDARD}."
    )
    assert not ALIAS_SPELLING.findall(section), (
        f"{REPO_ROOT / 'README.md'}: the `### delegation` section still writes"
        f" a `--`-prefixed spelling of a command path (ADR-0109). See"
        f" {STANDARD}."
    )
    for form in ("/delegation on", "/delegation status"):
        assert form in section, (
            f"{REPO_ROOT / 'README.md'}: the `### delegation` section does not"
            f" state the `{form}` form. The README is where somebody decides"
            f" whether they want the Skill, so it states the forms it accepts"
            f" (ADR-0109). See {STANDARD}."
        )


def test_delegation_takes_its_scope_as_a_flag_and_never_as_an_operand() -> None:
    """The scope is a flag, and the default scope is not nameable.

    `--project` and `--user` name the two persistent scopes; the session is
    what giving neither selects, and the bare invocation is the only way to
    write a session toggle. That removes the last pair of spellings for one
    thing, at the cost of a user no longer being able to write the default
    scope for emphasis (ADR-0109).
    """

    forms = _delegation_forms()

    # A surface list that came back empty would leave the loop below judging
    # nothing, which is the one outcome this check exists to catch.
    assert forms

    for form in forms:
        found = sorted(set(SCOPE_OPERAND.findall(form)))
        assert not found, (
            f"{DELEGATION_DIR}: the form `{form.strip()}` writes {found} as a"
            f" bare operand. A scope is named by a flag or not at all, and the"
            f" session is the unnamed default (ADR-0097, ADR-0109). See"
            f" {STANDARD}."
        )

    page = (DELEGATION_DIR / "help.md").read_text(encoding="utf-8")
    assert {"--project", "--user"} <= _flags(_optional_section(page, "## OPTIONS")), (
        f"{DELEGATION_DIR / 'help.md'}: `## OPTIONS` no longer declares both"
        f" scope flags, so the two persistent scopes have no spelling at all"
        f" (ADR-0109). See {STANDARD}."
    )


def test_delegation_accepts_no_unseparated_free_text_and_interrogates_nothing() -> None:
    """Prose stops being a form, and the interrogation clause goes with it.

    The Skill answered *is it on?* as `status` while asking about anything
    wider, so its formal grammar accepted free text at one narrow width and
    interrogated it above that. The reserved separator carries instructions
    collection-wide (ADR-0078), so an unrecognized bare token is refused like
    any other invalid form (ADR-0109).
    """

    body = DELEGATION_DIR / "SKILL.md"
    text = body.read_text(encoding="utf-8")
    arguments = _section(text, "## Arguments", body)
    page = (DELEGATION_DIR / "help.md").read_text(encoding="utf-8")

    unseparated = (
        "A token that is neither a recognized command path nor a declared flag"
    )
    assert unseparated in arguments, (
        f"{body}: the argument prose does not refuse unseparated text after"
        f" the Skill name or a command path. Anything not carried by a"
        f" recognized token is an invalid form rather than an instruction"
        f" (ADR-0109). See {STANDARD}."
    )
    assert "Prose is not a form" not in text, (
        f"{body}: the interrogation clause is still in the body. Prose is not"
        f" a form at any width, so nothing is asked about in place of the"
        f" grammar (ADR-0109). See {STANDARD}."
    )
    assert "Unseparated text is not an instruction" in page, (
        f"{DELEGATION_DIR / 'help.md'}: `DIAGNOSTICS` does not say that"
        f" unseparated text is refused rather than read as guidance"
        f" (ADR-0109). See {STANDARD}."
    )


def test_delegation_reports_every_scope_when_no_scope_flag_is_given() -> None:
    """`status` keeps the reach it had when the scope was an operand.

    Nothing about what the Skill does moves here. The one behaviour the new
    grammar could quietly have lost is the report that covers all three scopes,
    because the form that produced it was a bare `status` with no scope word
    beside it (ADR-0109).
    """

    body = DELEGATION_DIR / "SKILL.md"
    arguments = _section(body.read_text(encoding="utf-8"), "## Arguments", body)

    assert "`status` with no scope flag reports all three scopes." in arguments, (
        f"{body}: the parse rules no longer say that `status` without a scope"
        f" flag reports every scope. The scope became a flag; what `status`"
        f" reaches did not (ADR-0109). See {STANDARD}."
    )


def test_delegation_reports_checked_observations_and_imports_none() -> None:
    """Routed delegation may leave evidence, and only a checked outcome may.

    The mode is copied verbatim into session, Project, and user contexts, so
    what it says about evidence is the whole of delegation's observation
    contract: an unchecked subjective success is not a measurement, and nothing
    reaches the ledger until the user asks for it (issue #96).
    """

    path = REPO_ROOT / "skills" / "agents" / "delegation" / "references" / "mode.md"
    mode = path.read_text(encoding="utf-8")

    required_fragments = {
        "/model-selector observe",
        "/model-selector record",
        "caller-owned scratch",
        "objective checker, frozen rubric, declared failure signal, or explicit user confirmation",
        "unchecked subjective success",
        "never a checker",
        "unavailable measurement stays `null`",
        "no prompt, response, reasoning, source content, diff, terminal output, secret, or absolute path",
    }
    missing = sorted(
        fragment for fragment in required_fragments if fragment not in mode
    )
    assert not missing, (
        f"{path}: routed delegation reports a sanitized observation artifact"
        f" whose decisive outcomes are externally established, and imports"
        f" nothing on the user's behalf (issue #96); missing {missing}."
    )
