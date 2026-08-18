# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Manage which collection skills are Enabled on which Harnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, cast

ORIGIN = "Kntnt/skills"
MANAGER = "kntnt"
UNIVERSAL_PROJECT = ".agents/skills"
CANONICAL_GLOBAL = "~/.agents/skills"

# What a verb exits with when the disk does not show the change it made. The
# payload is still emitted: the user has to be told which skills and where.
EXIT_CHANGE_FAILED = 1
BINARY_HOW = {
    "uv": "install uv from https://docs.astral.sh/uv/",
    "git": "install git",
    "gh": "install GitHub CLI (gh) from https://cli.github.com/",
}

# A Capability is a Dependency on the Harness itself. No script can test one:
# this file cannot know which Harness invoked it, let alone what that Harness
# can do. So the checker reports the Capabilities a skill requires and the
# agent — which is the Harness — answers. Every name a skill may declare is
# defined here, so a typo is a refusal rather than a silently skipped check.
CAPABILITIES = {
    "subagents": {
        "confirm": "you can spawn subagents that work in their own context window",
        "how": "run this skill in a harness that can spawn subagents",
    },
}


class ManagerError(RuntimeError):
    """A user-facing manager failure with an exit code."""

    def __init__(self, message: str, code: int = 1) -> None:
        super().__init__(message)
        self.code = code


def fail(message: str, code: int = 1) -> int:
    """Print an error to stderr and return an exit code."""

    print(f"error: {message}", file=sys.stderr)
    return code


# What a dry run costs, carried in the payload rather than left to be guessed
# at: the Sandbox has an npm cache of its own, so the first dry run in a
# session downloads the transport afresh. An unexplained pause in a command
# whose whole promise is that nothing happens is the moment somebody reaches
# for the interrupt (ADR-0042).
DRY_RUN_NOTE = (
    "a dry run has an npm cache of its own, so the transport is downloaded "
    "afresh and this takes longer than the run it previews"
)

# The Sandbox this run is executing against, or None when the run is real.
# Held for the run because every payload a dry run emits has to say so, and
# which verb composed it is beside the point: the Sandbox is a fact about the
# run rather than about the verb.
_SANDBOX: Path | None = None


def emit(payload: dict[str, Any]) -> None:
    """Print *payload* as JSON, saying where a dry run read its outcome from."""

    if _SANDBOX is not None:
        payload = {
            **payload,
            "dry_run": {"sandbox": str(_SANDBOX), "note": DRY_RUN_NOTE},
        }

    print(json.dumps(payload, indent=2))


def home() -> Path:
    """Return the home used to resolve Global harness paths."""

    return Path(os.environ.get("KNTNT_HOME", str(Path.home())))


def here() -> Path:
    """Return the installed manager directory."""

    override = os.environ.get("KNTNT_HERE")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent


def project_root() -> Path:
    """Return the Project directory (cwd, unless tests override)."""

    override = os.environ.get("KNTNT_PROJECT")
    if override:
        return Path(override)
    return Path.cwd()


def collection_source() -> str:
    """Return the collection origin the transport and Catalog fetch use."""

    return os.environ.get("KNTNT_SOURCE", ORIGIN)


# The path table this run resolves every directory through. Held for the run
# because Uninstall deletes the Manager, and this file with it, while the same
# run still has to verify that removal and name the directories it happened in.
_HARNESS_PATHS: dict[str, dict[str, str]] | None = None


def harness_paths() -> dict[str, dict[str, str]]:
    """Load harness id → path templates, once per run."""

    global _HARNESS_PATHS

    if _HARNESS_PATHS is None:
        override = os.environ.get("KNTNT_HARNESS_PATHS")
        path = Path(override) if override else here() / "harness-paths.json"
        _HARNESS_PATHS = cast(
            dict[str, dict[str, str]], json.loads(path.read_text(encoding="utf-8"))
        )

    return _HARNESS_PATHS


def expand_path(template: str, *, global_layer: bool) -> Path:
    """Resolve a harness path template against home or the Project."""

    if template.startswith("~/"):
        return home() / template[2:]
    if global_layer:
        return home() / template
    return project_root() / template


def layer_dir(harness: str, *, global_layer: bool) -> Path | None:
    """Return the skills directory for *harness* in the targeted layer."""

    spec = harness_paths().get(harness)
    if spec is None:
        return None
    key = "global" if global_layer else "project"
    template = spec.get(key)
    if not template:
        return None
    return expand_path(template, global_layer=global_layer)


def is_universal(harness: str) -> bool:
    """True when the transport installs *harness* into the shared .agents/skills tree."""

    spec = harness_paths().get(harness)
    return spec is not None and spec.get("project") == UNIVERSAL_PROJECT


def skill_dirs(harness: str, *, global_layer: bool) -> list[Path]:
    """Return directories where *harness* may hold a skill in this layer.

    The transport treats a harness whose project path is `.agents/skills` as
    universal and writes Global files to `~/.agents/skills`, ignoring that
    harness's documented globalSkillsDir.
    """

    dirs: list[Path] = []
    primary = layer_dir(harness, global_layer=global_layer)
    if primary is not None:
        dirs.append(primary)
    if global_layer and is_universal(harness):
        canonical = expand_path(CANONICAL_GLOBAL, global_layer=True)
        if canonical not in dirs:
            dirs.append(canonical)
    return dirs


def parse_yaml_scalar(raw: str) -> Any:
    """Parse a YAML scalar used in skill frontmatter."""

    if raw in {"true", "True"}:
        return True
    if raw in {"false", "False"}:
        return False
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
        return raw[1:-1]
    return raw


def _next_significant(lines: list[str], start: int) -> tuple[int, str] | None:
    """Return (indent, stripped) of the next non-empty, non-comment line."""

    for raw in lines[start:]:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        return indent, raw.strip()
    return None


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse a restricted YAML subset: maps, lists of scalars, scalars."""

    lines = text.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    index = 0

    while index < len(lines):
        raw = lines[index]
        if not raw.strip() or raw.strip().startswith("#"):
            index += 1
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1]

        if stripped.startswith("- "):
            if isinstance(container, list):
                container.append(parse_yaml_scalar(stripped[2:].strip()))
            index += 1
            continue

        if ":" not in stripped:
            index += 1
            continue

        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if not isinstance(container, dict):
            index += 1
            continue

        if rest:
            container[key] = parse_yaml_scalar(rest)
            index += 1
            continue

        nxt = _next_significant(lines, index + 1)
        if nxt is not None and nxt[1].startswith("- ") and nxt[0] > indent:
            nested_list: list[Any] = []
            container[key] = nested_list
            stack.append((indent, nested_list))
        else:
            nested_map: dict[str, Any] = {}
            container[key] = nested_map
            stack.append((indent, nested_map))
        index += 1

    return root


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Return the YAML frontmatter of a SKILL.md, or an empty dict."""

    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    return parse_simple_yaml(text[4:end])


DEP_KINDS = ("binaries", "skills", "externals", "capabilities")

# The frontmatter block a collection skill declares its Dependencies in, under
# `metadata`. It is also this collection's mark on a skill it installed: no
# other collection has reason to write the key, and it travels in the skill's
# own SKILL.md rather than in anything the Manager keeps beside itself.
METADATA_BLOCK = "kntnt"


def collection_block(frontmatter: dict[str, Any]) -> dict[str, Any] | None:
    """Return this collection's frontmatter block, or None where there is none."""

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        return None
    block = metadata.get(METADATA_BLOCK)
    return block if isinstance(block, dict) else None


def skill_deps(frontmatter: dict[str, Any]) -> dict[str, list[str]]:
    """Read Dependency lists from a skill's frontmatter."""

    block = collection_block(frontmatter)
    if block is None:
        return {key: [] for key in DEP_KINDS}
    result: dict[str, list[str]] = {}
    for key in DEP_KINDS:
        values = block.get(key, [])
        result[key] = [str(item) for item in values] if isinstance(values, list) else []
    return result


def carries_marker(skill_dir: Path) -> bool:
    """True when the skill installed at *skill_dir* came from this collection.

    Provenance is read off the skill's own frontmatter and off nothing else.
    Every file the Manager keeps beside itself is a sidecar the transport
    overwrites whenever it re-copies `kntnt`, so a record held there can forget
    that a skill was ever ours; the marker in the skill's own SKILL.md cannot
    (issue #20). Answers rather than raises, whatever it meets on the way.
    """

    # A layer holds skills this collection did not write, so the file is an
    # untrusted boundary: any bytes at all, no read permission, or no file
    # there. None of that can claim to be ours, and none of it may take the
    # run down — a traceback in place of the report is the failure of #5.
    try:
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False

    return collection_block(parse_frontmatter(text)) is not None


def capability_notes(names: list[str]) -> list[dict[str, str]]:
    """Describe each required Capability so the agent can answer for itself."""

    notes: list[dict[str, str]] = []
    for name in names:
        note = CAPABILITIES.get(name)
        if note is None:
            raise ManagerError(f"unknown capability '{name}'")
        notes.append({"name": name, **note})
    return notes


# What no Digest may see, on the producing side and the consuming side alike.
# The generator walks a working tree carrying the maintainer's own bytecode
# cache; the consumer walks an installed directory carrying the one running the
# skill created. Neither has a git to ask which files are the collection's, so
# the two can agree only through this list (ADR-0041). A pattern ending in `/`
# is a directory name skipped wherever it occurs; any other matches a filename.
DIGEST_IGNORE = ("__pycache__/", "*.pyc")


def digest_ignores(relative: str) -> bool:
    """True when a path below a skill directory is an artefact, not a file we ship."""

    # Match each pattern against the part of the path its shape names: a
    # directory anywhere along the way, or the filename at the end of it.
    parts = relative.split("/")
    for pattern in DIGEST_IGNORE:
        if pattern.endswith("/"):
            if pattern[:-1] in parts[:-1]:
                return True
        elif fnmatch(parts[-1], pattern):
            return True

    return False


def directory_digest(directory: Path) -> str:
    """Digest a skill directory over its sorted relative paths and file contents.

    The one freshness question the manager can answer honestly is whether two
    directories hold the same files, so paths and contents both go in: a
    rename, an edit, an added file and a removed file each change the value.
    The Catalog carries this for a skill as the collection ships it, and the
    same call over an installed copy is what any comparison stands on — which
    is why the ignore list above has to be the only one either side applies.
    """

    # Sort by the relative path rather than by the absolute one, so that where
    # the directory sits cannot reach the value the two sides compare.
    files = sorted(
        (path.relative_to(directory).as_posix(), path)
        for path in directory.rglob("*")
        if path.is_file()
    )

    # Hash the files the collection ships and pass the artefacts by. A NUL
    # after each path and a fixed-width digest of its contents keep the stream
    # unambiguous: no arrangement of names and bytes can imitate another.
    digest = hashlib.sha256()
    for relative, path in files:
        if digest_ignores(relative):
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())

    return digest.hexdigest()


# The Catalog this run reasons from, and whether the origin supplied it. Held
# for the run because a single invocation reads the Catalog many times over.
_CATALOG: tuple[dict[str, Any], bool] | None = None


def fetch_catalog() -> dict[str, Any]:
    """Load the Catalog from the collection origin. Never invent it."""

    source = collection_source()
    local = Path(source)
    if local.is_dir():
        candidate = local / "skills" / MANAGER / "catalog.json"
        if candidate.is_file():
            return cast(
                dict[str, Any], json.loads(candidate.read_text(encoding="utf-8"))
            )
        raise ManagerError(f"Catalog missing at {candidate}")

    url = (
        f"https://raw.githubusercontent.com/{source}/main/skills/{MANAGER}/catalog.json"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return cast(dict[str, Any], json.loads(response.read().decode("utf-8")))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ManagerError(f"Catalog could not be fetched from {url}") from exc


def write_catalog(catalog: dict[str, Any]) -> None:
    """Store *catalog* beside the Manager that is running."""

    path = here() / "catalog.json"
    path.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def stored_catalog() -> dict[str, Any] | None:
    """Return the snapshot stored beside the Manager, or None if absent."""

    path = here() / "catalog.json"
    if not path.is_file():
        return None
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def resolve_catalog() -> tuple[dict[str, Any], bool]:
    """Return the Catalog to reason from and whether the origin supplied it.

    The collection is what the repository ships, not what a snapshot recorded
    the last time someone ran Update, so the origin is asked first and every
    verb reasons from the answer. A fetch that fails must not take a read verb
    with it: the snapshot is the fallback, and the boolean is how the caller
    tells the user which of the two they are looking at. With neither — no
    origin and no snapshot — there is no Catalog to invent, and the fetch's own
    error stands.

    The answer is cached because a single invocation reads the Catalog many
    times over and the origin is to be asked once per run, not once per reader.
    """

    global _CATALOG

    if _CATALOG is None:
        try:
            _CATALOG = (fetch_catalog(), True)
        except ManagerError:
            stored = stored_catalog()
            if stored is None:
                raise
            _CATALOG = (stored, False)

    return _CATALOG


def load_catalog() -> dict[str, Any]:
    """Return the Catalog every verb reasons from."""

    return resolve_catalog()[0]


def catalog_from_origin() -> bool:
    """True when the Catalog in hand was fetched rather than read off disk.

    Named for what it reports rather than for the payload field it feeds. The
    field kept Update's name, `catalog_refreshed`, so that a reader meets one
    shape everywhere; a *refresh* is what Update then does with the answer, and
    is not what a verb that only reports has established.
    """

    return resolve_catalog()[1]


def skills_of(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the skill entries of *catalog*."""

    skills = catalog.get("skills", [])
    if not isinstance(skills, list):
        raise ManagerError("Catalog is corrupt")
    return [entry for entry in skills if isinstance(entry, dict)]


def names_of(catalog: dict[str, Any]) -> set[str]:
    """Return every skill name in *catalog*."""

    return {str(entry["name"]) for entry in skills_of(catalog) if "name" in entry}


def catalog_skills() -> list[dict[str, Any]]:
    """Return the Catalog's skill entries."""

    return skills_of(load_catalog())


def catalog_names() -> set[str]:
    """Return every Catalog skill name."""

    return names_of(load_catalog())


def is_project_detectable(template: str) -> bool:
    """True when a Project template names a hidden directory of the Harness's own.

    `skills`, `data/skills`, and `agent/skills` are things a repository has for
    its own reasons. Reading one of those as a Harness would write this
    collection into someone else's source tree, so such a Harness is not
    detected in the Project layer at all.
    """

    return template.startswith(".")


def detected_harnesses(*, global_layer: bool) -> list[str]:
    """Return the Harnesses present in this layer.

    Present means the Harness has a home here — the parent of its skills
    directory is on disk — not that it already holds skills. A Harness
    installed after the last Enable is therefore detected on the next run.
    """

    key = "global" if global_layer else "project"
    found: list[str] = []

    # A Harness qualifies only where it documents a path for this layer, and in
    # the Project layer only where that path is its own to claim.
    for harness, spec in harness_paths().items():
        template = spec.get(key)
        if not template:
            continue
        if not global_layer and not is_project_detectable(template):
            continue
        if expand_path(template, global_layer=global_layer).parent.is_dir():
            found.append(harness)

    return found


def shared_harness() -> str:
    """Return the harness id that reads the shared skills directory in both layers.

    The transport writes by agent id, so naming the shared directory means
    naming an agent that reads exactly it and nothing else. Several do, they
    all write the same files to the same place, and the first in a stable order
    is as good as any.
    """

    for harness, spec in sorted(harness_paths().items()):
        if (
            spec.get("global") == CANONICAL_GLOBAL
            and spec.get("project") == UNIVERSAL_PROJECT
        ):
            return harness
    raise ManagerError("no harness reads the shared skills directory")


def target_harnesses(*, global_layer: bool) -> list[str]:
    """Return every Harness this invocation acts on, never a subset of them.

    With nothing detected the answer is the shared skills directory alone. The
    transport's own fallback — every agent it knows of — would create skills
    directories for Harnesses the user has never installed.
    """

    return detected_harnesses(global_layer=global_layer) or [shared_harness()]


def layer_dirs(harnesses: list[str], *, global_layer: bool) -> list[Path]:
    """Return every directory *harnesses* could hold a skill in, each of them once.

    The union of the Harnesses' directories rather than the per-Harness
    grouping, because several Harness ids share one directory: every universal
    Harness has its Global files written to the canonical tree. A walk that
    iterated Harnesses would arrive at that tree once per id and do its work
    there as many times — which for a walk that reads each SKILL.md it finds
    is that many reads of every file in it.

    Whoever needs to know which Harness a directory belongs to walks the
    Harnesses itself: `skill_state` counts how many of them agree a skill is
    present, and `contradicting_dirs` names the ones that disagree. Everything
    else wants this.
    """

    directories = {
        directory
        for harness in harnesses
        for directory in skill_dirs(harness, global_layer=global_layer)
    }
    return sorted(directories, key=str)


def target_dirs(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return the skills directories *harnesses* resolve to, for a payload.

    These are `skill_dirs`, not the documented path alone: a universal Harness
    has its Global files written to the canonical tree rather than to the
    directory its own entry names, so naming only the latter would report a
    place the file never landed in. Reporting both keeps the payload to what
    Status actually looked in.
    """

    return [
        str(directory) for directory in layer_dirs(harnesses, global_layer=global_layer)
    ]


def skill_present_at(directory: Path, name: str) -> bool:
    """True when *name* is on disk in *directory*.

    The manager's one notion of presence. Status decides Enabled with it and a
    change is confirmed with it, so no verb can report what Status contradicts.
    """

    return (directory / name / "SKILL.md").is_file()


def skill_state(name: str, harnesses: list[str], *, global_layer: bool) -> str:
    """Return enabled, disabled, or partial for *name* in one layer."""

    if not harnesses:
        return "disabled"
    present = 0
    checked = 0
    for harness in harnesses:
        directories = skill_dirs(harness, global_layer=global_layer)
        if not directories:
            continue
        checked += 1
        if any(skill_present_at(directory, name) for directory in directories):
            present += 1
    if checked == 0 or present == 0:
        return "disabled"
    if present == checked:
        return "enabled"
    return "partial"


def enabled_names(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return Catalog skills Enabled in *layer* on any targeted Harness."""

    names: list[str] = []
    for entry in catalog_skills():
        name = str(entry["name"])
        if skill_state(name, harnesses, global_layer=global_layer) != "disabled":
            names.append(name)
    return names


def run_transport(args: list[str], *, internal: bool = False) -> None:
    """Run the transport. Skill files move only through this call."""

    raw = os.environ.get("KNTNT_TRANSPORT", "npx --yes skills")
    command = [*shlex.split(raw), *args]
    env = os.environ.copy()
    if internal:
        env["INSTALL_INTERNAL_SKILLS"] = "1"
    result = subprocess.run(
        command,
        cwd=project_root(),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ManagerError(detail or f"transport failed: {' '.join(args)}")


# The variables a Sandbox redirects. `HOME` is what the transport resolves the
# Global layer and its own npm cache through — measured rather than assumed,
# and the property the whole of `--dry-run` stands on (ADR-0042) — and the
# three of ours are how this script resolves that same layer, the Project, and
# the Manager a verb writes beside.
SANDBOX_ENV = ("HOME", "KNTNT_HOME", "KNTNT_PROJECT", "KNTNT_HERE")

# The two homes a Sandbox holds, under the root it is made at. Both stand
# whichever layer is being run: the transport resolves a Project against the
# directory it is invoked in and its own cache against the home, so a Sandbox
# with only the layer's own base would leave the other reaching out of it.
SANDBOX_HOME = "home"
SANDBOX_PROJECT = "project"


def sandbox_path(path: Path, root: Path, *, global_layer: bool) -> Path:
    """Return where *path* lands inside the Sandbox at *root*.

    The layer decides both ends of the move — Global is rooted at the home and
    a Project at the working directory, and the Sandbox holds a counterpart of
    each — so both are worked out here rather than passed in. Where a layer
    lives is then one expression in one place instead of a pair of values
    every caller has to carry and keep matched.
    """

    base = home() if global_layer else project_root()
    replacement = root / (SANDBOX_HOME if global_layer else SANDBOX_PROJECT)

    try:
        return replacement / path.relative_to(base)
    except ValueError:
        raise ManagerError(
            f"{path} is outside {base} and cannot be sandboxed"
        ) from None


def seed_skills(source: Path, destination: Path) -> None:
    """Copy this collection's own skills out of *source* and into *destination*.

    The Manager and every skill carrying the marker, and nothing else. Without
    the seed a dry run would report installing what the user already has, which
    is the failure mode of a preview that starts from an empty world; with more
    than the seed it would absorb a defect worth seeing, since no verb of this
    collection touches another collection's files (ADR-0042).
    """

    for entry in sorted(source.iterdir()):
        if not (entry / "SKILL.md").is_file():
            continue
        if entry.name != MANAGER and not carries_marker(entry):
            continue
        shutil.copytree(entry, destination / entry.name)


def seed_manager(root: Path, directories: list[Path], *, global_layer: bool) -> Path:
    """Return the Manager a sandboxed run resolves its own directory to.

    A Manager installed in the layer being run is already in the Sandbox, put
    there with the directory it sits in, and pointing at that copy is what lets
    a dry run of Uninstall delete the Manager the way the real run would. One
    installed anywhere else — a Global Manager applying a Project, a checkout
    under test — is copied in, because a verb that writes beside the Manager,
    as Update does when it stores the Catalog, has to write inside the Sandbox.
    """

    installed = here()
    if installed.parent in directories:
        return sandbox_path(installed, root, global_layer=global_layer)

    copy = root / MANAGER
    shutil.copytree(installed, copy)
    return copy


def seed_sandbox(root: Path, *, global_layer: bool) -> dict[str, str]:
    """Fill the Sandbox at *root* with this collection's files, and say where it is.

    Returns the environment the verb is then run under: both of the Sandbox's
    homes, whichever layer is being applied, and the Manager it resolves its
    own directory to.
    """

    sandbox_home = root / SANDBOX_HOME
    sandbox_project = root / SANDBOX_PROJECT
    sandbox_home.mkdir()
    sandbox_project.mkdir()

    # Every directory the layer covers is recreated, whether or not this
    # collection has anything in it. A Harness is Detected by its directory
    # being there (ADR-0035), so a Sandbox missing one would resolve a
    # different set of targets than the run it is standing in for.
    directories = layer_dirs(
        target_harnesses(global_layer=global_layer), global_layer=global_layer
    )
    for directory in directories:
        target = sandbox_path(directory, root, global_layer=global_layer)
        target.mkdir(parents=True, exist_ok=True)
        if directory.is_dir():
            seed_skills(directory, target)

    return {
        "HOME": str(sandbox_home),
        "KNTNT_HOME": str(sandbox_home),
        "KNTNT_PROJECT": str(sandbox_project),
        "KNTNT_HERE": str(seed_manager(root, directories, global_layer=global_layer)),
    }


@contextmanager
def sandbox(*, global_layer: bool) -> Iterator[None]:
    """Run a verb against a temporary home seeded with this collection, then discard it.

    The verb inside is the verb itself: the same code, the same transport
    calls, and the same reading of the disk afterwards, so what it reports is
    an outcome rather than a description of intent (ADR-0042). The redirection
    is the environment, because that is what this script resolves every
    directory through and what the transport inherits from it.
    """

    global _SANDBOX

    # Seeded before anything is redirected, since the seed is read from the
    # world as it is now, and the Sandbox is announced only once it stands.
    root = Path(tempfile.mkdtemp(prefix="kntnt-dry-run-"))
    restore = {name: os.environ.get(name) for name in SANDBOX_ENV}
    try:
        os.environ.update(seed_sandbox(root, global_layer=global_layer))
        _SANDBOX = root
        yield
    finally:
        # Put the environment back as it was, whether the verb returned or
        # raised, and take the Sandbox with it: what a dry run leaves behind
        # is a report and nothing else.
        _SANDBOX = None
        for name, value in restore.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        shutil.rmtree(root, ignore_errors=True)


def contradicting_dirs(
    name: str, harnesses: list[str], *, global_layer: bool, expect_present: bool
) -> list[str]:
    """Return the directories where *name* contradicts the intended change."""

    directories: set[str] = set()

    # A Harness that agrees contributes nothing, even where one of its own
    # directories is empty: that is what the canonical tree does to a universal
    # Harness on a placement that did take effect.
    for harness in harnesses:
        presence = {
            directory: skill_present_at(directory, name)
            for directory in skill_dirs(harness, global_layer=global_layer)
        }
        if any(presence.values()) == expect_present:
            continue
        directories.update(
            str(directory)
            for directory, present in presence.items()
            if present != expect_present
        )

    return sorted(directories)


def verified_outcome(
    names: list[str], harnesses: list[str], *, global_layer: bool, expect_present: bool
) -> dict[str, Any]:
    """Report which of *names* the disk agrees were changed.

    The transport's exit code says only that it did not throw; a run that does
    nothing looks exactly like one that did the work (issue #7). Success is
    therefore the presence test Status uses, run again over the same layer and
    the same directories: a placement is confirmed where the skill is now
    Enabled, a removal where it is now Disabled. Whatever fails that is named,
    with the directories that contradict it, so the user knows where to look.
    """

    wanted = "enabled" if expect_present else "disabled"
    confirmed: list[str] = []
    failed: list[dict[str, Any]] = []

    # Ask the disk about each name, and name the directories behind a no.
    for name in names:
        if skill_state(name, harnesses, global_layer=global_layer) == wanted:
            confirmed.append(name)
            continue
        failed.append(
            {
                "name": name,
                "directories": contradicting_dirs(
                    name,
                    harnesses,
                    global_layer=global_layer,
                    expect_present=expect_present,
                ),
            }
        )

    return {"intended": list(names), "confirmed": confirmed, "failed": failed}


def outcome_exit_code(outcome: dict[str, Any]) -> int:
    """Return the exit code a verified outcome earns.

    One rule for every verb: a change the disk does not show fails the run,
    including a run where other skills succeeded. The payload is emitted
    either way — an exit code names neither the skill nor the directory.
    """

    return EXIT_CHANGE_FAILED if outcome["failed"] else 0


def add_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Enable *names* on *harnesses* in the targeted layer, and verify it."""

    # Nothing to place is not a call: the transport refuses an empty selection.
    if names and harnesses:
        args = ["add", collection_source()]
        for name in names:
            args.extend(["--skill", name])
        for harness in harnesses:
            args.extend(["--agent", harness])
        if global_layer:
            args.append("--global")
        args.append("--yes")
        run_transport(args, internal=True)

    return verified_outcome(
        names, harnesses, global_layer=global_layer, expect_present=True
    )


def remove_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Disable *names* on *harnesses* in the targeted layer, and verify it."""

    # Nothing to remove is not a call: the transport refuses an empty selection.
    if names and harnesses:
        args = ["remove", *names]
        for harness in harnesses:
            args.extend(["--agent", harness])
        if global_layer:
            args.append("--global")
        args.append("--yes")
        run_transport(args, internal=True)

    return verified_outcome(
        names, harnesses, global_layer=global_layer, expect_present=False
    )


def removal_outcome(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Remove *names* and report the outcome, whatever the transport did.

    The transport takes the whole call down when it declines one name, so a
    removal that has to carry on regardless — Update's withdrawals, Uninstall
    deciding whether the Manager may go — reads that failure off the disk
    rather than raising it. What the run intended is unchanged either way;
    only the split between confirmed and failed differs.
    """

    try:
        return remove_skills(names, harnesses, global_layer=global_layer)
    except ManagerError:
        return verified_outcome(
            names, harnesses, global_layer=global_layer, expect_present=False
        )


def withdrawn_names(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return this collection's skills in this layer that the Catalog no longer names.

    Withdrawal is resolved from what the disk says wrote each skill, never from
    what a stored Catalog remembers the collection once shipped. That memory is
    a sidecar the transport replaces whenever it re-copies the Manager — a
    failed Update or a hand-run `npx skills update` is enough — and once it has
    forgotten a name, nothing can establish the skill was ever ours and the
    files are stranded for good (issue #20).

    Two things are never swept, whatever the Catalog says. The Manager is not a
    Catalog entry, so judging it by the Catalog alone would delete the verb
    doing the sweeping; and a skill with no marker belongs to another
    collection or to the user, which is not this collection's to remove.
    """

    catalog = catalog_names()
    withdrawn: set[str] = set()

    # Every directory the layer could hold a skill in, asked what wrote it.
    for directory in layer_dirs(harnesses, global_layer=global_layer):
        if not directory.is_dir():
            continue
        for entry in directory.iterdir():
            name = entry.name
            if name == MANAGER or name in catalog or name in withdrawn:
                continue
            if carries_marker(entry):
                withdrawn.add(name)

    return sorted(withdrawn)


def withdraw_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> list[dict[str, Any]]:
    """Take the skills the collection has withdrawn off the disk.

    A skill that has left the Catalog can no longer be updated, supported, or
    reasoned about, so it is removed without asking (ADR-0037). It goes through
    Disable's own removal — the collection has one way to delete skill files —
    and each name is reported with what the disk then showed: `removed` where
    the files are gone, `failed` with the directories they survive in. A
    failure is one skill's, not the run's: whatever else Update had to do still
    happens.

    *names* is what `withdrawn_names` swept off this layer, so every one of
    them was on disk when it looked. There is no verdict for a skill that was
    never here, because there is no such name to give one to.
    """

    outcome = removal_outcome(names, harnesses, global_layer=global_layer)

    # Every name was on disk when the sweep looked, so each one has an outcome
    # to report rather than a reason it was skipped.
    failed = {str(item["name"]): item["directories"] for item in outcome["failed"]}
    report: list[dict[str, Any]] = []
    for name in names:
        if name in failed:
            report.append({"name": name, "disk": "failed", "directories": failed[name]})
        else:
            report.append({"name": name, "disk": "removed"})

    return report


def require_yes(yes: bool, deletion: str) -> None:
    """Refuse a deletion the user has not been asked about.

    Where a subcommand deletes files the user is choosing to delete, `--yes` is
    the gate rather than a convenience (ADR-0029): the confirmation belongs to
    the skill, because a script run non-interactively cannot prompt, and the
    flag is how the skill asserts that it happened. One sentence for every such
    verb, so the two halves cannot drift apart.
    """

    if not yes:
        raise ManagerError(f"{deletion}; confirm first, then pass --yes", 2)


def parse_layer(value: str) -> bool:
    """True when the command targets Global."""

    if value in {"on", "true", "1"}:
        return False
    if value in {"off", "false", "0"}:
        return True
    raise ManagerError(f"unknown --project value '{value}'")


def validate_names(names: list[str]) -> list[str]:
    """Reject the Manager and unknown Catalog names."""

    known = catalog_names()
    cleaned: list[str] = []
    for name in names:
        if name == MANAGER:
            raise ManagerError("kntnt is the Manager; it is always Enabled")
        if name not in known:
            raise ManagerError(f"unknown skill '{name}'")
        if name not in cleaned:
            cleaned.append(name)
    return cleaned


def effective_row(global_state: str, project_state: str) -> dict[str, str] | None:
    """Return the state and source a skill has here, or None where it has neither.

    Only a layer that carries the skill can be its source, so a skill Disabled
    in both is no answer to *what applies here* and gets no row at all. Enabled
    in a carrying layer is Enabled here, that layer having put the skill in
    every Harness it detected; only where every carrying layer is partial is
    the answer partial. The two are never merged Harness by Harness: each layer
    detects its own set, so their union would answer a question nobody asked.
    """

    carrying = {
        layer: state
        for layer, state in (("global", global_state), ("project", project_state))
        if state != "disabled"
    }
    if not carrying:
        return None

    return {
        "state": "enabled" if "enabled" in carrying.values() else "partial",
        "source": "both" if len(carrying) == 2 else next(iter(carrying)),
    }


def status_payload(names: list[str], *, effective: bool) -> dict[str, Any]:
    """Build the Status report for *names*, or every Catalog skill.

    Two questions, one shape. Without the project flag Status answers *what
    does this machine have*: every Catalog skill with its Global `state`,
    Disabled ones included, because the Catalog still carries them. With the
    flag it answers *what applies in this working directory*: the Effective
    set — everything Enabled in Global plus everything Enabled in this Project
    — each row naming its `source` as global, project, or both. A skill
    Disabled in both layers is no answer to the second question, so that form
    leaves it out. `reports` says which of the two was answered, because a
    reader must never have to guess.

    Either form is only as current as the list it was built from, so
    `catalog_refreshed` says whether that list came from the origin or from the
    snapshot the origin could not be reached to replace. Same field, same
    meaning, as the one Update reports.
    """

    # Global is read either way; the Project only where it is part of the answer.
    global_targets = target_harnesses(global_layer=True)
    project_targets = target_harnesses(global_layer=False) if effective else []

    # Skill names select rows out of the Catalog; naming none selects them all.
    wanted = (
        validate_names(names)
        if names
        else [str(entry["name"]) for entry in catalog_skills()]
    )
    by_name = {str(entry["name"]): entry for entry in catalog_skills()}

    # Every row carries what the Catalog knows about a skill; the two forms
    # differ only in what they add to that and in which skills earn a row.
    skills: list[dict[str, Any]] = []
    for name in wanted:
        entry = by_name[name]
        row = {
            "name": name,
            "category": entry.get("category", ""),
            "description": entry.get("description", ""),
            "capabilities": entry.get("capabilities", []),
        }
        global_state = skill_state(name, global_targets, global_layer=True)
        if not effective:
            skills.append({**row, "state": global_state})
            continue
        applies = effective_row(
            global_state, skill_state(name, project_targets, global_layer=False)
        )
        if applies is not None:
            skills.append({**row, **applies})

    # Name only the layers the report covers, so the directories are the places
    # the states just reported were read from and nowhere else.
    directories = {"global": target_dirs(global_targets, global_layer=True)}
    if effective:
        directories["project"] = target_dirs(project_targets, global_layer=False)

    return {
        "reports": "effective" if effective else "global",
        "catalog_refreshed": catalog_from_origin(),
        "directories": directories,
        "skills": skills,
    }


def picker_payload(
    names: list[str], *, global_layer: bool, action: str
) -> dict[str, Any]:
    """Group Catalog skills by Category for an interactive Enable/Disable."""

    harnesses = target_harnesses(global_layer=global_layer)
    categories: dict[str, list[dict[str, Any]]] = {}
    for entry in catalog_skills():
        name = str(entry["name"])
        if names and name not in names:
            continue
        state = skill_state(name, harnesses, global_layer=global_layer)
        if action == "disable" and state == "disabled":
            continue
        category = str(entry.get("category") or "other")
        categories.setdefault(category, []).append(
            {
                "name": name,
                "description": entry.get("description", ""),
                "capabilities": entry.get("capabilities", []),
                "enabled": state == "enabled",
            }
        )
    return {
        "action": "pick",
        "layer": "global" if global_layer else "project",
        "categories": categories,
    }


def cmd_status(names: list[str], *, global_layer: bool) -> int:
    """Print Status and return 0.

    Status reads two layers and changes neither, so the project flag selects
    the question rather than a target: Global alone, or what applies here.
    """

    emit(status_payload(names, effective=not global_layer))
    return 0


def cmd_plan_enable(names: list[str], *, global_layer: bool) -> int:
    """Print an Enable picker or a plan for the named skills."""

    if not names:
        emit(picker_payload([], global_layer=global_layer, action="enable"))
        return 2
    wanted = validate_names(names)
    harnesses = target_harnesses(global_layer=global_layer)
    emit(
        {
            "action": "enable",
            "layer": "global" if global_layer else "project",
            "skills": wanted,
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_plan_disable(names: list[str], *, global_layer: bool) -> int:
    """Print a Disable picker or a plan for the named skills."""

    if not names:
        emit(picker_payload([], global_layer=global_layer, action="disable"))
        return 2
    wanted = validate_names(names)
    harnesses = target_harnesses(global_layer=global_layer)
    emit(
        {
            "action": "disable",
            "layer": "global" if global_layer else "project",
            "skills": wanted,
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_apply_enable(names: list[str], *, global_layer: bool) -> int:
    """Enable the named skills in the targeted layer."""

    wanted = validate_names(names)
    if not wanted:
        raise ManagerError("name at least one skill to enable", 2)
    harnesses = target_harnesses(global_layer=global_layer)
    already = {
        name
        for name in wanted
        if skill_state(name, harnesses, global_layer=global_layer) == "enabled"
    }
    changing = [name for name in wanted if name not in already]
    outcome = add_skills(changing, harnesses, global_layer=global_layer)
    emit(
        {
            **outcome,
            "noop": [name for name in wanted if name in already],
            "layer": "global" if global_layer else "project",
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return outcome_exit_code(outcome)


def cmd_apply_disable(names: list[str], *, global_layer: bool, yes: bool) -> int:
    """Disable the named skills in the targeted layer."""

    wanted = validate_names(names)
    if not wanted:
        raise ManagerError("name at least one skill to disable", 2)

    require_yes(yes, "disabling deletes these skills' files")

    harnesses = target_harnesses(global_layer=global_layer)
    changing: list[str] = []
    noop: list[str] = []
    for name in wanted:
        state = skill_state(name, harnesses, global_layer=global_layer)
        if state == "disabled":
            noop.append(name)
            continue
        changing.append(name)
    outcome = remove_skills(changing, harnesses, global_layer=global_layer)
    emit(
        {
            **outcome,
            "noop": noop,
            "layer": "global" if global_layer else "project",
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return outcome_exit_code(outcome)


def cmd_plan_uninstall() -> int:
    """Print what Uninstall will take off this machine."""

    harnesses = target_harnesses(global_layer=True)
    emit(
        {
            "action": "uninstall",
            "layer": "global",
            "skills": [*enabled_names(harnesses, global_layer=True), MANAGER],
            "catalog_refreshed": catalog_from_origin(),
            "directories": target_dirs(harnesses, global_layer=True),
        }
    )
    return 0


def cmd_apply_uninstall(*, yes: bool) -> int:
    """Take this collection off the machine: the Global set, then the Manager.

    Global only, and no `--project` to say otherwise. A Skill in a working
    directory is checked into that repository and travels with it, so whether
    it stays is that project's decision rather than this machine's (ADR-0040).

    `catalog_refreshed` matters more here than anywhere else: the set to
    remove is every Catalog skill Enabled in Global, so a Catalog read off
    the snapshot rather than the origin may leave a skill the collection has
    since withdrawn behind — and once the Manager is gone there is no verb
    left to finish the job.
    """

    require_yes(yes, "uninstalling deletes this collection's files")

    harnesses = target_harnesses(global_layer=True)
    directories = target_dirs(harnesses, global_layer=True)

    # Which list the run worked from is part of the report, and the Catalog is
    # read while the snapshot it may have come from is still on disk.
    refreshed = catalog_from_origin()

    outcome = removal_outcome(
        enabled_names(harnesses, global_layer=True), harnesses, global_layer=True
    )

    # The Manager goes last, and only where the rest of the collection really
    # left: it is the one skill that can be asked to finish the job, and a
    # machine holding skills with no verb left to remove them is worse off than
    # one whose Manager outlives them by a run.
    if not outcome["failed"]:
        manager = removal_outcome([MANAGER], harnesses, global_layer=True)
        outcome = {
            "intended": [*outcome["intended"], *manager["intended"]],
            "confirmed": [*outcome["confirmed"], *manager["confirmed"]],
            "failed": manager["failed"],
        }

    emit(
        {
            **outcome,
            "catalog_refreshed": refreshed,
            "layer": "global",
            "directories": directories,
        }
    )
    return outcome_exit_code(outcome)


def cmd_plan_update(*, global_layer: bool) -> int:
    """Print which Enabled skills Update will refresh."""

    harnesses = target_harnesses(global_layer=global_layer)
    refresh = enabled_names(harnesses, global_layer=global_layer)
    if global_layer:
        refresh = [MANAGER, *refresh]
    emit(
        {
            "action": "update",
            "layer": "global" if global_layer else "project",
            "refresh": refresh,
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_apply_update(*, global_layer: bool) -> int:
    """Refresh this collection, report new Catalog entries, re-check Dependencies."""

    harnesses = target_harnesses(global_layer=global_layer)

    # What changed is the difference between the snapshot this Manager stored
    # and what the origin carries now, so the old half is read off the file
    # itself: the shared loader is already holding the new one.
    stored = stored_catalog()

    # Update is the collection's one writer of the snapshot. Every verb reasons
    # from the origin; storing what it returned is what leaves a usable
    # fallback for the next run that cannot reach it, and what the comparison
    # above is made against next time.
    refreshed = catalog_from_origin()
    if refreshed:
        write_catalog(load_catalog())

    current_names = catalog_names()

    # A Manager with no snapshot has no *before*, and a run with no *before*
    # has discovered nothing: calling the whole collection new would bury the
    # one entry that matters under every entry that does not.
    old_names = names_of(stored) if stored is not None else current_names
    new_names = [name for name in sorted(current_names) if name not in old_names]

    # Only the reporting half rests on that comparison. What has been
    # withdrawn is asked of the disk (ADR-0037), and only where the origin
    # answered: deleting files on the strength of a fallback list is the one
    # thing a stale Catalog must never be allowed to do.
    withdrawn = (
        withdrawn_names(harnesses, global_layer=global_layer) if refreshed else []
    )
    withdrawals = withdraw_skills(withdrawn, harnesses, global_layer=global_layer)

    desired = enabled_names(harnesses, global_layer=global_layer)
    refresh = [MANAGER, *desired] if global_layer else list(desired)

    # The transport's own `update` compares SKILL.md and skips a skill whose
    # SKILL.md is unchanged, leaving sidecars — catalog.json, helper documents,
    # scripts — frozen at the revision that last touched SKILL.md. `add`
    # re-copies the whole directory and is idempotent, so it is the refresh.
    outcome = add_skills(refresh, harnesses, global_layer=global_layer)

    unsatisfied: list[dict[str, str]] = []
    capabilities: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    seen_capabilities: set[tuple[str, str]] = set()
    for directory in layer_dirs(harnesses, global_layer=global_layer):
        for name in desired:
            skill_dir = directory / name
            if not skill_present_at(directory, name):
                continue
            for item in unsatisfied_at(skill_dir):
                key = (item["kind"], item["name"], item["how"])
                if key in seen:
                    continue
                seen.add(key)
                unsatisfied.append(item)
            for note in capabilities_at(skill_dir):
                pair = (name, note["name"])
                if pair in seen_capabilities:
                    continue
                seen_capabilities.add(pair)
                capabilities.append({"skill": name, **note})

    emit(
        {
            **outcome,
            "new": new_names,
            "removed": withdrawals,
            "catalog_refreshed": refreshed,
            "unsatisfied": unsatisfied,
            "capabilities": capabilities,
            "layer": "global" if global_layer else "project",
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )

    # ADR-0036's one rule reaches both halves of the run: a withdrawal whose
    # files are still there is as much a change the disk does not show as a
    # refresh that never landed.
    if any(item["disk"] == "failed" for item in withdrawals):
        return EXIT_CHANGE_FAILED

    return outcome_exit_code(outcome)


def declared_deps_at(skill_dir: Path) -> dict[str, list[str]]:
    """Return the Dependency lists declared in *skill_dir*/SKILL.md."""

    path = skill_dir / "SKILL.md"
    if not path.is_file():
        raise ManagerError(f"no SKILL.md at {skill_dir}")
    return skill_deps(parse_frontmatter(path.read_text(encoding="utf-8")))


def capabilities_at(skill_dir: Path) -> list[dict[str, str]]:
    """Return the Capabilities *skill_dir* requires of the running Harness."""

    return capability_notes(declared_deps_at(skill_dir)["capabilities"])


def unsatisfied_at(skill_dir: Path) -> list[dict[str, str]]:
    """Return Unsatisfied Dependencies declared in *skill_dir*/SKILL.md.

    Capabilities are absent by design: only the agent can answer those.
    """

    deps = declared_deps_at(skill_dir)
    missing: list[dict[str, str]] = []

    for binary in deps["binaries"]:
        if shutil.which(binary) is None:
            missing.append(
                {
                    "name": binary,
                    "kind": "binary",
                    "how": BINARY_HOW.get(binary, f"install {binary}"),
                }
            )

    for name in deps["skills"]:
        if not skill_is_effective(name):
            missing.append(
                {
                    "name": name,
                    "kind": "skill",
                    "how": f"/kntnt enable {name}",
                }
            )

    for name in deps["externals"]:
        if not skill_is_effective(name):
            missing.append(
                {
                    "name": name,
                    "kind": "external",
                    "how": f"add the External '{name}' with the transport (npx skills add)",
                }
            )

    return missing


def skill_is_effective(name: str) -> bool:
    """True when *name* is present in Global or this Project (the Effective union)."""

    for global_layer in (True, False):
        for harness in target_harnesses(global_layer=global_layer):
            if any(
                skill_present_at(directory, name)
                for directory in skill_dirs(harness, global_layer=global_layer)
            ):
                return True
    return False


def cmd_check(skill_dir: Path) -> int:
    """Refuse when a Dependency at *skill_dir* is Unsatisfied.

    `capabilities` is the unfinished half of the check: each entry is a
    Dependency this script cannot test, handed to the agent to answer. Exit 0
    with a non-empty list therefore means "nothing missing that I can see",
    not "go ahead".
    """

    capabilities = capabilities_at(skill_dir)
    missing = unsatisfied_at(skill_dir)
    if missing:
        emit({"ok": False, "unsatisfied": missing, "capabilities": capabilities})
        return 2
    emit({"ok": True, "unsatisfied": [], "capabilities": capabilities})
    return 0


def find_skill_md(name: str) -> Path | None:
    """Locate a SKILL.md for *name* on disk or in a local collection source."""

    for global_layer in (True, False):
        for harness in target_harnesses(global_layer=global_layer):
            for directory in skill_dirs(harness, global_layer=global_layer):
                candidate = directory / name / "SKILL.md"
                if candidate.is_file():
                    return candidate

    source = Path(collection_source())
    if source.is_dir():
        if name == MANAGER:
            candidate = source / "skills" / MANAGER / "SKILL.md"
            if candidate.is_file():
                return candidate
        matches = list((source / "skills").glob(f"*/{name}/SKILL.md"))
        if matches:
            return matches[0]
    return None


def help_section(text: str) -> str:
    """Return the Help section of a SKILL.md, or the whole body after frontmatter."""

    marker = "## Help"
    start = text.find(marker)
    if start < 0:
        end = text.find("\n---", 3)
        return text[end + 4 :].strip() if end >= 0 else text.strip()
    rest = text[start:]
    next_heading = rest.find("\n## ", 1)
    if next_heading >= 0:
        rest = rest[:next_heading]
    return rest.strip()


def read_manpage(path: Path) -> str:
    """Read a shipped manpage, or name the file a truncated install is missing."""

    # A half-copied install is the one way a manpage can be absent, and the
    # user can act on that only if the file that should be there is named.
    if not path.is_file():
        raise ManagerError(f"missing help file '{path}'; run the transport again")

    return path.read_text(encoding="utf-8").rstrip("\n")


def subcommand_manpage(name: str) -> Path | None:
    """Return the manpage the manager ships for *name*, if *name* is a verb of it.

    Matched against what is on disk rather than a list held here, so the set of
    documented verbs is the set of files under `help/` and cannot drift from it.
    Globbing also settles the name: a user-supplied string never reaches a path.
    """

    return next(
        (path for path in (here() / "help").glob("*.md") if path.stem == name), None
    )


def help_text(name: str | None) -> str:
    """Return the help for *name*: the manager's, a subcommand's, or a skill's."""

    # Bare help, and the manager's own name, both mean the manager's manpage.
    if not name or name == MANAGER:
        return read_manpage(here() / "help.md")

    # The manager documents its own verbs; every skill documents itself. A verb
    # answers first, so a skill can never take a subcommand's name out of use.
    verb = subcommand_manpage(name)
    if verb is not None:
        return read_manpage(verb)

    if name not in catalog_names():
        raise ManagerError(f"unknown subcommand or skill '{name}'")

    # A Disabled skill has no files here, so its description is all there is.
    path = find_skill_md(name)
    if path is None:
        entry = next(
            (item for item in catalog_skills() if item.get("name") == name), None
        )
        description = entry.get("description", "") if entry else ""
        return f"{name}\n\n{description}\n\nEnable this skill to read its full help."

    # Every collection skill ships its manpage beside its SKILL.md; one that
    # does not is older than that contract, and its Help section stands in.
    manpage = path.parent / "help.md"
    if manpage.is_file():
        return read_manpage(manpage)

    return help_section(path.read_text(encoding="utf-8"))


def cmd_help(name: str | None) -> int:
    """Print help for the manager, one of its subcommands, or one skill."""

    print(help_text(name))
    return 0


# The frontmatter parser reads a restricted YAML subset with no block scalars,
# so `description: >` yields this indicator as the value. Generation is where
# that has to fail: past it the character ships as the skill's whole help text.
BLOCK_SCALARS = frozenset({">", "|", ">-", "|-", ">+", "|+"})


def generate_catalog(source: Path) -> dict[str, Any]:
    """Build a Catalog from SKILL.md files under *source*/skills."""

    entries: list[dict[str, Any]] = []
    skills_root = source / "skills"
    for skill_md in sorted(skills_root.glob("*/*/SKILL.md")):
        category = skill_md.parent.parent.name
        frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = str(frontmatter.get("name") or skill_md.parent.name)
        if name == MANAGER:
            continue
        deps = skill_deps(frontmatter)
        description = str(frontmatter.get("description") or "")

        # Generation is where a misspelt Capability has to fail. Past this
        # point the name would ride into the Catalog and only surface when a
        # user ran the skill. The same is true of the two fields the Catalog
        # exists to carry — the transport installs by directory name, and
        # the description is a skill's entire help until it is Enabled — and
        # of the marker, which is how Update tells a withdrawal of ours from
        # another collection's skill once this one has stopped shipping it.
        capability_notes(deps["capabilities"])
        if collection_block(frontmatter) is None:
            raise ManagerError(
                f"{skill_md}: no metadata.kntnt block; a skill without the "
                "marker cannot be removed when the collection withdraws it"
            )
        if name != skill_md.parent.name:
            raise ManagerError(
                f"{skill_md}: name '{name}' is not the directory "
                f"'{skill_md.parent.name}'; the transport installs by directory"
            )
        if not description:
            raise ManagerError(f"{skill_md}: description is empty")
        if description in BLOCK_SCALARS:
            raise ManagerError(
                f"{skill_md}: description '{description}' is a YAML block "
                "scalar, which the frontmatter parser does not support; "
                "write it on one line"
            )
        entries.append(
            {
                "name": name,
                "category": category,
                "description": description,
                "digest": directory_digest(skill_md.parent),
                "binaries": deps["binaries"],
                "skills": deps["skills"],
                "externals": deps["externals"],
                "capabilities": deps["capabilities"],
            }
        )
    return {"origin": ORIGIN, "skills": entries}


def cmd_catalog(*, write: bool) -> int:
    """Print a generated Catalog from a local collection source."""

    source = Path(collection_source())
    if not source.is_dir():
        raise ManagerError(
            "KNTNT_SOURCE must be a local collection to generate the Catalog"
        )
    catalog = generate_catalog(source)
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if write:
        path = here() / "catalog.json"
        path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


def add_project_flag(parser: argparse.ArgumentParser) -> None:
    """Add the --project flag that defaults to Global."""

    parser.add_argument("--project", choices=("on", "off"), default="off")


def add_yes_flag(parser: argparse.ArgumentParser) -> None:
    """Add --yes to a verb.

    Every verb takes it, so passing the user's flag through is never a crash.
    It only carries meaning where something is asked or deleted.
    """

    parser.add_argument("--yes", action="store_true")


def add_dry_run_flag(parser: argparse.ArgumentParser) -> None:
    """Add --dry-run to a verb.

    Every subparser takes it, including the ones with nothing to do with it:
    the agent's forwarding is prose and therefore unreliable, and a forwarded
    flag must never be the thing that breaks a run (ADR-0029).
    """

    parser.add_argument("--dry-run", action="store_true")


def normalize_argv(argv: list[str]) -> list[str]:
    """Turn bare `--project` into `--project on` so it cannot steal a skill name."""

    normalized: list[str] = []
    for arg in argv:
        if arg == "--project":
            normalized.extend(["--project", "on"])
        elif arg.startswith("--project="):
            normalized.extend(["--project", arg.split("=", 1)[1]])
        else:
            normalized.append(arg)
    return normalized


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the manager CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Report Enabled and Disabled.")
    status.add_argument("skills", nargs="*")
    add_project_flag(status)
    add_yes_flag(status)
    add_dry_run_flag(status)

    help_cmd = sub.add_parser("help", help="Print help.")
    help_cmd.add_argument("skill", nargs="?")
    add_yes_flag(help_cmd)
    add_dry_run_flag(help_cmd)

    check = sub.add_parser("check", help="Refuse when a Dependency is Unsatisfied.")
    check.add_argument("--here", required=True, type=Path)
    add_dry_run_flag(check)

    catalog = sub.add_parser(
        "catalog", help="Generate the Catalog from a local source."
    )
    catalog.add_argument("--write", action="store_true")
    add_dry_run_flag(catalog)

    plan = sub.add_parser("plan", help="Print a JSON plan and stop.")
    plan_sub = plan.add_subparsers(dest="verb", required=True)
    plan_enable = plan_sub.add_parser("enable")
    plan_enable.add_argument("skills", nargs="*")
    add_project_flag(plan_enable)
    add_yes_flag(plan_enable)
    add_dry_run_flag(plan_enable)
    plan_disable = plan_sub.add_parser("disable")
    plan_disable.add_argument("skills", nargs="*")
    add_project_flag(plan_disable)
    add_yes_flag(plan_disable)
    add_dry_run_flag(plan_disable)
    plan_update = plan_sub.add_parser("update")
    add_project_flag(plan_update)
    add_yes_flag(plan_update)
    add_dry_run_flag(plan_update)

    # Uninstall takes no --project: it acts on this machine, and a working
    # directory's copies are that repository's to keep or drop (ADR-0040).
    plan_uninstall = plan_sub.add_parser("uninstall")
    add_yes_flag(plan_uninstall)
    add_dry_run_flag(plan_uninstall)

    apply = sub.add_parser("apply", help="Apply a plan.")
    apply_sub = apply.add_subparsers(dest="verb", required=True)
    apply_enable = apply_sub.add_parser("enable")
    apply_enable.add_argument("skills", nargs="*")
    add_project_flag(apply_enable)
    add_yes_flag(apply_enable)
    add_dry_run_flag(apply_enable)
    apply_disable = apply_sub.add_parser("disable")
    apply_disable.add_argument("skills", nargs="*")
    add_project_flag(apply_disable)
    add_yes_flag(apply_disable)
    add_dry_run_flag(apply_disable)
    apply_update = apply_sub.add_parser("update")
    add_project_flag(apply_update)
    add_yes_flag(apply_update)
    add_dry_run_flag(apply_update)
    apply_uninstall = apply_sub.add_parser("uninstall")
    add_yes_flag(apply_uninstall)
    add_dry_run_flag(apply_uninstall)

    return parser.parse_args(argv)


def dry_run_layer(args: argparse.Namespace) -> bool:
    """Return the layer a changing verb's Sandbox has to stand in for.

    Uninstall takes no `--project` and clears this machine (ADR-0040), so its
    Sandbox is a home; every other verb previews the layer it was aimed at.
    """

    verb: str = args.verb
    return True if verb == "uninstall" else parse_layer(args.project)


def dispatch(args: argparse.Namespace) -> int:
    """Run the parsed command, in a Sandbox where the run is a dry run."""

    # Apply is where skill files move, and a Sandbox is what those moves
    # happen in instead. Every other command takes the flag and has nothing to
    # do with it, bar Catalog, which honours it where it writes.
    if args.dry_run and args.command == "apply":
        with sandbox(global_layer=dry_run_layer(args)):
            return run_command(args)

    return run_command(args)


def run_command(args: argparse.Namespace) -> int:
    """Run the parsed command against whatever home is in force."""

    if args.command == "status":
        return cmd_status(args.skills, global_layer=parse_layer(args.project))
    if args.command == "help":
        return cmd_help(args.skill)
    if args.command == "check":
        return cmd_check(args.here)
    # Catalog's `--write` is the one write this script makes outside a layer,
    # so it is the one place besides Apply where the flag has anything to
    # honour. A flag that was accepted while the file was rewritten anyway
    # would state something false about what happened (ADR-0029).
    if args.command == "catalog":
        return cmd_catalog(write=args.write and not args.dry_run)
    if args.command == "plan":
        if args.verb == "uninstall":
            return cmd_plan_uninstall()
        if args.verb == "update":
            return cmd_plan_update(global_layer=parse_layer(args.project))
        global_layer = parse_layer(args.project)
        if args.verb == "enable":
            return cmd_plan_enable(args.skills, global_layer=global_layer)
        return cmd_plan_disable(args.skills, global_layer=global_layer)
    if args.verb == "uninstall":
        return cmd_apply_uninstall(yes=args.yes)
    if args.verb == "update":
        return cmd_apply_update(global_layer=parse_layer(args.project))
    global_layer = parse_layer(args.project)
    if args.verb == "enable":
        return cmd_apply_enable(args.skills, global_layer=global_layer)
    return cmd_apply_disable(args.skills, global_layer=global_layer, yes=args.yes)


def main(argv: list[str] | None = None) -> int:
    """Dispatch a manager command. Return an exit code."""

    raw = normalize_argv(list(sys.argv[1:] if argv is None else argv))
    if not raw:
        raw = ["help"]
    args = parse_args(raw)
    try:
        return dispatch(args)
    except ManagerError as exc:
        return fail(str(exc), exc.code)


if __name__ == "__main__":
    raise SystemExit(main())
