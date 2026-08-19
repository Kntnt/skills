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

# How long a verb waits for the origin, in seconds. The files are a small JSON
# list and a Markdown page, so a link that works answers well inside this; a
# link that is dropped rather than refused is the case the number is for. For
# the Catalog the wait buys nothing the fallback — reported in
# `catalog_refreshed` — does not already give, and for a manpage, which has no
# stored copy behind it, a short wait is the difference between being told and
# being kept waiting to be told.
ORIGIN_TIMEOUT = 5

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


def relay_transport(message: str) -> None:
    """Write the transport's own account of a failure to stderr, verbatim.

    The mirrors below read a transport failure off the disk rather than
    raising it, which costs the user the one thing only the transport knows:
    why it declined. That belongs on stderr — the channel the manager's own
    errors already use — and never in the payload, which ADR-0036 fixes as a
    statement about the disk in one shape every verb carries.

    Whole and unedited, under a line naming whose words these are. The same
    text reaches the user in full wherever the failure is not swallowed, so a
    cap here would make one path quieter than the other for no reason, and
    the manager has no standing to summarise prose it cannot interpret.
    """

    print(f"the transport said:\n{message}", file=sys.stderr)


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

        # The path table is required data with no fallback, so a damaged one is
        # a truncated install: name the file, because that is what the user can
        # act on.
        try:
            _HARNESS_PATHS = cast(
                dict[str, dict[str, str]], json.loads(path.read_text(encoding="utf-8"))
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ManagerError(
                f"could not read the harness path table '{path}'; "
                "run the transport again"
            ) from exc

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


def origin_text(relative: str, what: str) -> str:
    """Read one file of the collection from the origin, wherever the origin is.

    A local path is a collection checked out; anything else is `owner/repo` at
    GitHub. How the origin is addressed lives here alone, so the Catalog and a
    skill's manpage are fetched by one scheme and fail with one pair of
    messages: *missing at* a path that is there, *could not be fetched* from a
    host that is not. *what* names the thing for those messages.
    """

    source = collection_source()
    local = Path(source)

    # A checked-out collection: a file that is not there is that origin's way
    # of being unreachable, and the path is what the user can act on.
    if local.is_dir():
        candidate = local / relative
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
        raise ManagerError(f"{what} missing at {candidate}")

    url = f"https://raw.githubusercontent.com/{source}/main/{relative}"
    try:
        with urllib.request.urlopen(url, timeout=ORIGIN_TIMEOUT) as response:
            return cast(bytes, response.read()).decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ManagerError(f"{what} could not be fetched from {url}") from exc


def fetch_catalog() -> dict[str, Any]:
    """Load the Catalog from the collection origin. Never invent it.

    Corrupt is its own answer rather than *could not be fetched*: the origin
    replied, and a reader told the file was unreachable would go looking in
    the wrong place for it.
    """

    raw = origin_text(f"skills/{MANAGER}/catalog.json", "Catalog")
    try:
        return cast(dict[str, Any], json.loads(raw))
    except json.JSONDecodeError as exc:
        raise ManagerError("Catalog at the origin is corrupt") from exc


def write_catalog(catalog: dict[str, Any]) -> None:
    """Store *catalog* beside the Manager that is running, in one move.

    Written to a sibling and renamed over the target, because a write in place
    is what leaves a half-written snapshot behind when a run is interrupted —
    and the reader treats a damaged one as no snapshot at all, so an in-place
    write can silently cost the user their fallback. A rename within one
    directory is atomic: what survives is the old file or the new one.
    """

    path = here() / "catalog.json"
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"

    # Sibling rather than a temporary directory: `replace` is only atomic
    # within one filesystem, and the directory the file lands in is the one
    # place guaranteed to be on it.
    temporary = path.with_name(f"{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def stored_catalog() -> dict[str, Any] | None:
    """Return the snapshot stored beside the Manager, or None where there is none.

    Damaged counts as absent. The file is a sidecar the transport replaces
    whenever it re-copies the Manager and an interrupted Update can leave half
    written, so unreadable bytes are a state the run has to survive: raising
    here would take down every verb, including the Update that rewrites the
    file. A run with no snapshot has no *before* and reports nothing new, which
    is what `new_entry_names` already says of a Manager that has never stored
    one, and where the origin cannot be reached either the fetch's own error
    stands rather than a Catalog being invented.
    """

    path = here() / "catalog.json"

    # The snapshot is not necessarily anything the Manager wrote, so it is read
    # as an untrusted boundary: any bytes at all, no read permission, or no
    # file there. None of it may reach the caller as an exception.
    try:
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None


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


def new_entry_names(stored: dict[str, Any] | None) -> list[str]:
    """Return the Catalog entries the collection has added since *stored*.

    A Manager with no snapshot has no *before*, and a run with no *before* has
    discovered nothing: calling the whole collection new would bury the one
    entry that matters under every entry that does not. A Catalog read off the
    snapshot is that snapshot, so it answers with nothing new — which is the
    honest answer rather than a claim that the collection published nothing.
    """

    current = catalog_names()
    old = names_of(stored) if stored is not None else current
    return sorted(name for name in current if name not in old)


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


def seed_layer(root: Path, *, global_layer: bool) -> list[Path]:
    """Recreate one layer's directories inside the Sandbox at *root*, and fill them.

    Every directory the layer covers is recreated, whether or not this
    collection has anything in it. A Harness is Detected by its directory
    being there (ADR-0035), so a Sandbox missing one would resolve a different
    set of targets than the run it is standing in for. The answer is the
    directories as they are outside the Sandbox, which is what the Manager's
    own seeding is then decided against.
    """

    directories = layer_dirs(
        target_harnesses(global_layer=global_layer), global_layer=global_layer
    )
    for directory in directories:
        target = sandbox_path(directory, root, global_layer=global_layer)
        target.mkdir(parents=True, exist_ok=True)
        if directory.is_dir():
            seed_skills(directory, target)

    return directories


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

    # The layer being previewed, and Global with it where that layer is a
    # Project. What Satisfies a Project's Dependency is Global's copy as much
    # as its own (ADR-0013), so a Sandbox holding only the working directory
    # reads a machine with nothing on it and offers a second copy of every
    # Dependency the user already has. Global runs the other way: it reads no
    # Project, and one seeded for it would be a directory the real run never
    # looked in.
    directories = seed_layer(root, global_layer=global_layer)
    if not global_layer:
        seed_layer(root, global_layer=True)

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


def placement_outcome(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Place *names* and report the outcome, whatever the transport did.

    The mirror of `removal_outcome`, for the half of a run that puts files
    there. Update deletes what the collection has Withdrawn before it places
    anything, so a transport failure that escaped would cost the user the
    report of a deletion that has already happened — a change the disk shows
    and nothing says (ADR-0036).

    A refusal is every name failing, and not the presence test the other
    mirror re-reads the disk for. The transport declines the whole call before
    anything moves, so nothing in the batch landed; and presence cannot answer
    a refresh in any case, the files it would have replaced being already
    there. Absence, which is what a removal is verified by, has no such
    problem. The directories named are the ones the layer covers, because
    where to look is the whole use the user has for them.

    The reason goes to the user even so, on stderr rather than in the payload.
    Every name failing is the condition the other mirror guards on, so here it
    always holds.
    """

    try:
        return add_skills(names, harnesses, global_layer=global_layer)
    except ManagerError as exc:
        relay_transport(str(exc))
        return {
            "intended": list(names),
            "confirmed": [],
            "failed": [
                {
                    "name": name,
                    "directories": target_dirs(harnesses, global_layer=global_layer),
                }
                for name in names
            ],
        }


def removal_outcome(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Remove *names* and report the outcome, whatever the transport did.

    The transport takes the whole call down when it declines one name, so a
    removal that has to carry on regardless — Update's withdrawals, Uninstall
    deciding whether the Manager may go — reads that failure off the disk
    rather than raising it. What the run intended is unchanged either way;
    only the split between confirmed and failed differs.

    Where that split leaves a failure, the transport's own account of it goes
    to the user on stderr, which is the only place it is told.
    """

    try:
        return remove_skills(names, harnesses, global_layer=global_layer)
    except ManagerError as exc:
        outcome = verified_outcome(
            names, harnesses, global_layer=global_layer, expect_present=False
        )

        # Only a failure has a why to explain. A transport that exited
        # non-zero having removed the files anyway is exactly what reading the
        # disk exists to absorb, and that run is clean: printing somebody
        # else's error over it would be telling the user about nothing.
        if outcome["failed"]:
            relay_transport(str(exc))
        return outcome


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
    """True when the command targets Global.

    `off` is Global and `on` is the Project, and those two are the whole of the
    flag (ADR-0038). Nothing else can arrive: `add_project_flag` declares the
    choices, and `normalize_argv` has already turned the bare flag and the
    `--project=` form into one of them before argparse reads it.
    """

    return value == "off"


def joined(base: list[str], extra: list[str]) -> list[str]:
    """Return *base* followed by each name of *extra* it does not already carry."""

    return [*base, *(name for name in extra if name not in base)]


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


def installed_freshness(name: str, digest: str, directories: list[Path]) -> str:
    """Say whether the copies of *name* on disk are the files *digest* names.

    `deviating` where any copy differs, `current` where every copy agrees, and
    `unknown` where there is nothing to establish it from — no copy on disk, or
    no Digest to compare against. Never *out of date*: the comparison sees two
    states and no history, so it cannot name a direction (ADR-0041).
    """

    copies = [
        directory / name
        for directory in directories
        if skill_present_at(directory, name)
    ]
    if not digest or not copies:
        return "unknown"
    if any(directory_digest(copy) != digest for copy in copies):
        return "deviating"
    return "current"


def catalog_digest(entry: dict[str, Any]) -> str:
    """Return the Digest *entry* carries, or nothing where none may be trusted.

    A Catalog read off the stored snapshot carries digests that describe the
    collection as of the last Update, so a verdict made from them would be a
    claim about a revision the collection may already have left. Nothing
    Deviates and nothing is current on such a list, and no refresh is offered
    on the strength of it (ADR-0041), which is what the empty answer buys.
    """

    if not catalog_from_origin():
        return ""
    return str(entry.get("digest") or "")


def catalog_entries() -> dict[str, dict[str, Any]]:
    """Return the Catalog's skills by name, in the order the Catalog lists them."""

    return {str(entry["name"]): entry for entry in catalog_skills()}


def dependencies_of(name: str, entries: dict[str, dict[str, Any]]) -> list[str]:
    """Return the collection Skills *name* declares, as the Catalog carries them.

    Only names the Catalog itself carries. A `skills` entry naming something
    this collection does not ship has no row to check and no entry to walk; a
    Dependency outside the Catalog is the checker's to answer when the Skill is
    used (ADR-0012).
    """

    entry = entries.get(name)
    if entry is None:
        return []
    declared = entry.get("skills", [])
    return [str(item) for item in declared if str(item) in entries]


def dependency_closure(name: str, entries: dict[str, dict[str, Any]]) -> list[str]:
    """Return every collection Skill *name* needs, Dependencies before dependents.

    The whole chain rather than the first link, because the user is asked one
    question for the whole closure: `release` pulling in `push` and `commit` is
    a single yes rather than three (ADR-0047). The order is the order the
    Skills would be checked in, so the rendering can read the list out as what
    it is about to add.
    """

    resolved: list[str] = []

    def walk(current: str, ancestors: tuple[str, ...]) -> None:
        for dependency in dependencies_of(current, entries):
            # The Catalog is fetched from the origin at every invocation, so a
            # cycle in it is an authoring mistake this run has to survive
            # rather than a state the caller has already ruled out.
            if dependency in ancestors:
                continue

            walk(dependency, (*ancestors, dependency))
            if dependency not in resolved:
                resolved.append(dependency)

    walk(name, (name,))
    return resolved


def unsatisfied_among(requires: list[str], satisfied: set[str]) -> list[str]:
    """Return the members of *requires* that nothing in *satisfied* supplies."""

    return [name for name in requires if name not in satisfied]


def satisfying_names(harnesses: list[str], *, global_layer: bool) -> set[str]:
    """Return the Skills that Satisfy a Dependency for a Skill in this layer.

    What Satisfies one is what the Harness will load, so a Project is judged by
    its own copies and Global's together: a Dependency already Enabled on the
    machine wants no second copy in the working directory (ADR-0013).
    """

    satisfied = set(enabled_names(harnesses, global_layer=global_layer))
    if not global_layer:
        satisfied.update(
            enabled_names(target_harnesses(global_layer=True), global_layer=True)
        )
    return satisfied


def unsatisfied_on_disk(
    harnesses: list[str], *, global_layer: bool
) -> dict[str, list[str]]:
    """Name, per Skill the layer now holds, the Dependencies it is left without.

    Read off the disk rather than off the answer, because a placement the
    transport did not make leaves a Skill without that Dependency whatever the
    answer said, and a report of the answer would call that run clean
    (ADR-0036). Reported and never blocked: unchecking a Skill that a checked
    one depends on is the user's to do, and the manager says what it left
    Unsatisfied rather than putting the Dependency back (ADR-0047).
    """

    entries = catalog_entries()
    enabled = enabled_names(harnesses, global_layer=global_layer)
    satisfied = satisfying_names(harnesses, global_layer=global_layer)

    lacking = {
        name: unsatisfied_among(dependency_closure(name, entries), satisfied)
        for name in enabled
    }
    return {name: names for name, names in lacking.items() if names}


def select_payload(*, global_layer: bool) -> dict[str, Any]:
    """Build the list the user reads and answers in one gesture.

    One row per Catalog skill, grouped by Category so related skills are read
    together (ADR-0015), and everything a row is judged on carried on the row:
    the checkbox, the one-line description, the Capabilities the skill wants of
    the harness, whether its files reached only some of the layer's Detected
    Harnesses, whether they are the files the collection ships, and the whole
    chain of collection Skills it needs — resolved here so that the rendering
    names what would be added rather than walking the graph itself (ADR-0047).

    One layer, and no Effective form: without the flag the list is Global, and
    with it the Project layer alone (ADR-0038). There is no `partial` state
    either — incompleteness is a fact about the disk that confirming the list
    repairs, never a third thing an answer could select (ADR-0043).
    """

    harnesses = target_harnesses(global_layer=global_layer)
    directories = layer_dirs(harnesses, global_layer=global_layer)

    # A Project row says where else the skill is already Enabled: this layer
    # holds no copy of a Global one to uncheck, and checking the row would put
    # a second copy in the working directory (ADR-0013).
    global_targets = [] if global_layer else target_harnesses(global_layer=True)

    entries = catalog_entries()
    satisfied = satisfying_names(harnesses, global_layer=global_layer)
    categories: dict[str, list[dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []

    for name, entry in entries.items():
        state = skill_state(name, harnesses, global_layer=global_layer)
        row: dict[str, Any] = {
            "name": name,
            "description": entry.get("description", ""),
            "capabilities": entry.get("capabilities", []),
            "checked": state != "disabled",
            "incomplete": state == "partial",
            "freshness": installed_freshness(name, catalog_digest(entry), directories),
        }
        if not global_layer:
            row["in_global"] = (
                skill_state(name, global_targets, global_layer=True) != "disabled"
            )

        categories.setdefault(str(entry.get("category") or "other"), []).append(row)
        rows.append(row)

    # The closure is resolved here and not by the rendering, so a row names the
    # whole chain it needs rather than the first link of it (ADR-0047). A row
    # is locked where the user cannot yet have it; a checked Skill whose
    # Dependency has gone is a break to report, and locking it would say the
    # user may not have what they already do.
    for row in rows:
        requires = dependency_closure(str(row["name"]), entries)
        row["requires"] = requires
        row["unsatisfied"] = unsatisfied_among(requires, satisfied)
        row["locked"] = bool(row["unsatisfied"]) and not row["checked"]

    return {
        "action": "select",
        "layer": "global" if global_layer else "project",
        "catalog_refreshed": catalog_from_origin(),
        "directories": target_dirs(harnesses, global_layer=global_layer),
        "categories": categories,
        "withdrawn": withdrawn_names(harnesses, global_layer=global_layer),
    }


def delta_answer(
    on: list[str],
    off: list[str],
    harnesses: list[str],
    *,
    as_is: bool,
    global_layer: bool,
) -> tuple[list[str], frozenset[str]]:
    """Resolve a delta into the whole checked set, and what it only carried.

    `--on` and `--off` never mean *make this the whole set*. The base is what
    the layer already holds, so a Skill nobody named keeps the state it had and
    a script that mentions one name cannot silently Disable another (ADR-0043).

    What a named Skill needs comes with it, resolved to the whole closure
    before anything is written (ADR-0047) and minus whatever already Satisfies
    it, so a Project gains no second copy of a Dependency Global supplies
    (ADR-0013). `--off` is applied last and stands: a name the user took off is
    off however the same run arrived at it, and what that leaves Unsatisfied is
    reported rather than repaired behind them.

    The second answer is the Skills the base carried and the delta never named.
    Keeping the state they had is a fact about their files and not only about
    their checkbox: re-copying a Deviating one would overwrite an edit under a
    command that named something else, and the offer that says so is the list's
    (ADR-0041), which this form does not open. `--as-is` carries nothing,
    because there the set already on disk is itself the answer given.
    """

    # What the delta is resolved against: the Catalog it may name Skills from,
    # the Dependencies this layer already Satisfies, and the set on disk.
    entries = catalog_entries()
    satisfied = satisfying_names(harnesses, global_layer=global_layer)
    answer = enabled_names(harnesses, global_layer=global_layer)
    carried = frozenset() if as_is else frozenset(answer) - frozenset(on)

    # Each named Skill brings the chain it cannot work without, ahead of
    # itself, so the order is the order the Skills would be checked in.
    for name in on:
        for required in dependency_closure(name, entries):
            if required not in answer and required not in satisfied:
                answer.append(required)
        if name not in answer:
            answer.append(name)

    return [name for name in answer if name not in off], carried


def select_change(
    answer: list[str],
    harnesses: list[str],
    directories: list[Path],
    *,
    carried: frozenset[str] = frozenset(),
    global_layer: bool,
) -> tuple[list[str], list[str], list[str]]:
    """Split the Catalog into what the answer places, removes, and leaves alone.

    A checked skill is placed wherever the layer does not already hold exactly
    the files the collection ships: a Disabled one is Enabled, an incomplete
    one repaired, a Deviating one re-copied — which is why the confirmation has
    to say in the same breath that a local edit goes with it (ADR-0041).

    Checked and already those files is no work, and an unchecked skill this
    layer does not carry is no work either. An answer that is all no work
    leaves both lists empty, and reading is never a side-effecting act.

    *carried* names the skills the answer holds without answering for them —
    what a delta found on disk and never mentioned. Nothing is written for one
    of those, whatever the disk shows, so the repair and the re-copy stay where
    the offer to make them was given.
    """

    place: list[str] = []
    remove: list[str] = []
    noop: list[str] = []

    for entry in catalog_skills():
        name = str(entry["name"])
        state = skill_state(name, harnesses, global_layer=global_layer)

        # Unchecked is Disabled here, and only here: a Project holds no copy of
        # a skill Enabled in Global, so there is nothing of it to remove.
        if name not in answer:
            if state != "disabled":
                remove.append(name)
            continue

        # Carried and never named: the run has no answer about this skill, so
        # it writes none — the state it had includes the files it had.
        if name in carried:
            noop.append(name)
            continue

        freshness = installed_freshness(name, catalog_digest(entry), directories)
        if state == "enabled" and freshness != "deviating":
            noop.append(name)
        else:
            place.append(name)

    return place, remove, noop


def refresh_change(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> tuple[list[str], list[str]]:
    """Split the Enabled Skills into what a refresh copies and what it leaves alone.

    A Skill whose Digest matches the Catalog's is already byte-identical to
    what the collection ships, so re-copying it would move nothing while the
    report went on saying *twelve of twelve refreshed* — equally true of a
    machine where everything had changed and one where nothing had (ADR-0028).
    Everything else is refreshed: Deviating because the files are not the
    collection's, incomplete because the layer is missing a copy, and unknown
    because nothing establishes either. An open question is one Update answers
    by fetching, which is where this parts company with Select: Select is being
    told *this is the set*, and re-copying on no evidence would discard a local
    edit under a command that never named the Skill, while Update was pointed
    at the collection and fetching is the whole of what it was asked for.

    Nothing at all is refreshed from a Catalog read off the snapshot. The files
    move through the transport from the same origin that Catalog could not be
    fetched from, so there is nothing to copy, and gating on digests describing
    a revision the collection may already have left would be theatre in front
    of a fetch that cannot happen (ADR-0041).

    The Manager leads whatever is left, whatever any Digest says. It is no
    Catalog entry, so no Digest describes it, and the verb that repairs
    everything else has to be able to reach itself. Global only: an Update of a
    Project places no Manager in the working directory.
    """

    # The load-bearing half of the fallback rule. Without it the empty Digests
    # a snapshot Catalog answers with would read as unknown, and unknown is
    # refreshed — a fallback would fetch everything rather than nothing.
    if not catalog_from_origin():
        return [], []

    entries = catalog_entries()
    directories = layer_dirs(harnesses, global_layer=global_layer)
    refresh = [MANAGER] if global_layer else []
    current: list[str] = []

    # *names* is Catalog order, and the split keeps it, so the report reads in
    # the order the list the user answered was printed in.
    for name in names:
        state = skill_state(name, harnesses, global_layer=global_layer)
        freshness = installed_freshness(
            name, catalog_digest(entries.get(name, {})), directories
        )
        if state == "enabled" and freshness == "current":
            current.append(name)
        else:
            refresh.append(name)

    return refresh, current


def cmd_plan_select(*, global_layer: bool) -> int:
    """Print the list the user reads and answers. Nothing is written."""

    emit(select_payload(global_layer=global_layer))
    return 0


def cmd_apply_select(
    names: list[str],
    *,
    on: list[str],
    off: list[str],
    as_is: bool,
    global_layer: bool,
    yes: bool,
) -> int:
    """Make the targeted layer hold exactly the skills the answer checked.

    Both halves of the answer are one verb's work, so both are reported
    together: `intended`, `confirmed`, and `failed` cover the run, and
    `placed` and `removed` say which way each intended name went (ADR-0036).

    The answer arrives in one of two forms and never both. Skill names are the
    whole checked set, which is how the list is answered; `--as-is`, `--on`,
    and `--off` change the set the layer already holds, which is how a machine
    with nobody at the list is set up. `--as-is` names nothing and is the whole
    of `select --yes`: it Enables nothing that was not already Enabled and
    refreshes what Deviates and repairs what is incomplete, so an unattended
    run can never place instructions the user has not read (ADR-0043).
    """

    # Read together, the two forms would leave the Skills nobody named in a
    # state neither of them chose: the whole-set form removes them and the
    # delta keeps them.
    is_delta = as_is or bool(on) or bool(off)
    if is_delta and names:
        raise ManagerError(
            "skill names are the whole answer, and --as-is, --on, and --off "
            "change the set on disk; give one form or the other"
        )

    harnesses = target_harnesses(global_layer=global_layer)
    directories = layer_dirs(harnesses, global_layer=global_layer)
    answer, carried = (
        delta_answer(
            validate_names(on),
            validate_names(off),
            harnesses,
            as_is=as_is,
            global_layer=global_layer,
        )
        if is_delta
        else (validate_names(names), frozenset())
    )
    place, remove, noop = select_change(
        answer, harnesses, directories, carried=carried, global_layer=global_layer
    )

    # Unchecking deletes files the user chose to delete, and a script cannot
    # prompt, so the flag is that half of the answer's gate (ADR-0029).
    if remove:
        require_yes(yes, "unchecking these skills deletes their files")

    # The removals are read off the disk rather than raised, because the
    # placements have already landed by then: a transport that refuses one name
    # must not cost the user the report of what the same run did place.
    placed = add_skills(place, harnesses, global_layer=global_layer)
    removed = removal_outcome(remove, harnesses, global_layer=global_layer)
    outcome = {
        "intended": [*placed["intended"], *removed["intended"]],
        "confirmed": [*placed["confirmed"], *removed["confirmed"]],
        "failed": [*placed["failed"], *removed["failed"]],
    }

    emit(
        {
            **outcome,
            "placed": place,
            "removed": remove,
            "noop": noop,
            "unsatisfied": unsatisfied_on_disk(harnesses, global_layer=global_layer),
            "layer": "global" if global_layer else "project",
            "catalog_refreshed": catalog_from_origin(),
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
    """Print what Update will refresh, what it will leave alone, and what is new.

    The plan is what the user confirms, so it is the same split the run makes
    rather than a list of everything Enabled: a plan promising to refresh
    twelve skills ahead of a run that copies two describes a different verb.

    The new Catalog entries are here for the same reason. Apply is where they
    are Enabled, and the offer to Enable them has to be answerable before that
    — nothing reaches the disk ahead of the question it belongs to (ADR-0047).
    """

    harnesses = target_harnesses(global_layer=global_layer)
    refresh, current = refresh_change(
        enabled_names(harnesses, global_layer=global_layer),
        harnesses,
        global_layer=global_layer,
    )
    emit(
        {
            "action": "update",
            "layer": "global" if global_layer else "project",
            "refresh": refresh,
            "current": current,
            "new": new_entry_names(stored_catalog()),
            "catalog_refreshed": catalog_from_origin(),
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_apply_update(*, global_layer: bool, yes: bool) -> int:
    """Refresh this collection, Enable what is new where the offer is answered.

    The offer is the one question Update asks, and `--yes` is how an answer
    reaches a script that cannot prompt (ADR-0029). Answered, the entries the
    collection has added since the last run are Enabled in the layer being
    updated and named in the report; unanswered, nothing new is placed — a run
    nobody answered has been told nothing (ADR-0007).
    """

    harnesses = target_harnesses(global_layer=global_layer)

    # What changed is the difference between the snapshot this Manager stored
    # and what the origin carries now, so the old half is read off the file
    # itself: the shared loader is already holding the new one.
    stored = stored_catalog()
    new_names = new_entry_names(stored)

    # Every verb reasons from the origin, and whether it answered is what the
    # rest of the run is gated on: what may be deleted as Withdrawn, and
    # whether the snapshot below is worth writing at all.
    refreshed = catalog_from_origin()

    # The answer to the offer, and the whole of what a run places beyond a
    # refresh. Every name it adds is in the report, which is what makes an
    # unattended Update's one power — Enabling what the user pointed it at —
    # legible after the fact (ADR-0007).
    adopted = new_names if yes else []

    # Only the reporting half rests on the comparison above. What has been
    # withdrawn is asked of the disk (ADR-0037), and only where the origin
    # answered: deleting files on the strength of a fallback list is the one
    # thing a stale Catalog must never be allowed to do.
    withdrawn = (
        withdrawn_names(harnesses, global_layer=global_layer) if refreshed else []
    )
    withdrawals = withdraw_skills(withdrawn, harnesses, global_layer=global_layer)

    desired = enabled_names(harnesses, global_layer=global_layer)
    refresh, current = refresh_change(desired, harnesses, global_layer=global_layer)

    # An adopted entry is a placement like any other, so it joins the refresh
    # rather than travelling beside it: one transport call, one reading of the
    # disk, and one `intended`/`confirmed`/`failed` account of both (ADR-0036).
    # The re-check covers it for the same reason: what a skill lacks is the
    # layer's business from the moment the skill is in the layer.
    place = joined(refresh, adopted)
    recheck = joined(desired, adopted)

    # The transport's own `update` compares SKILL.md and skips a skill whose
    # SKILL.md is unchanged, leaving sidecars — catalog.json, helper documents,
    # scripts — frozen at the revision that last touched SKILL.md. `add`
    # re-copies the whole directory and is idempotent, so it is the refresh —
    # and it is why the Digest may gate it: what is skipped here is skipped for
    # being the collection's own files already, not for one file agreeing.
    # A refusal here is read rather than raised: the withdrawals above have
    # already been deleted, and the run has to report them.
    outcome = placement_outcome(place, harnesses, global_layer=global_layer)

    # Update is the collection's one writer of the snapshot, and what holds it
    # back is exactly what the offer is about. The difference against this file
    # is the whole of what makes an entry new, so a run that set out to Enable
    # one and did not place it must leave the file as it was: reported once and
    # gone before the user could act on it is the failure this guards
    # (ADR-0007). Nothing else holds it back. A refresh that did not land is
    # found again by its Digest on the next run, and a withdrawal that did not
    # land is found again by asking the disk — neither reads this file, so
    # freezing it for their sake would only leave the fallback describing an
    # older collection than the one the origin just answered with.
    unplaced = {item["name"] for item in outcome["failed"]} & set(adopted)
    if refreshed and not unplaced:
        write_catalog(load_catalog())

    unsatisfied: list[dict[str, str]] = []
    capabilities: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    seen_capabilities: set[tuple[str, str]] = set()
    for directory in layer_dirs(harnesses, global_layer=global_layer):
        for name in recheck:
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
            "enabled": adopted,
            "current": current,
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
                    "how": f"check '{name}' in /kntnt select",
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


def enabled_manpage(name: str) -> Path | None:
    """Locate the manpage of *name* where a layer holds it, Global or Project.

    Both layers answer, and Global before Project only because something has to
    come first: the question is what a Skill does, and any copy of it says so.
    A directory of that name is read as that skill's without asking the marker,
    which is the manager's one notion of presence — the same one the checkbox
    on the row is computed from, so the help and the checkbox cannot disagree.
    """

    for global_layer in (True, False):
        for harness in target_harnesses(global_layer=global_layer):
            for directory in skill_dirs(harness, global_layer=global_layer):
                candidate = directory / name / "help.md"
                if candidate.is_file():
                    return candidate
    return None


def fetch_manpage(category: str, name: str) -> str:
    """Read *name*'s manpage from the collection origin. Never invent it.

    The path is derivable rather than published: `category` is a Catalog field
    and the origin serves a skill's files where the repository ships them, so
    reading about a Skill nobody has Enabled costs the collection nothing.
    """

    return origin_text(
        f"skills/{category}/{name}/help.md", f"help for '{name}'"
    ).rstrip("\n")


def skill_manpage(name: str) -> str:
    """Return one collection skill's manpage, from disk or from the origin.

    This is what Select reads a row about, so it answers for a Skill the user
    has Enabled and one they are only considering alike (ADR-0044) — and it
    answers with the file the collection ships either way, or says it could not.
    """

    # The Catalog settles the name before any of it reaches a path, so a string
    # typed at the list can never address a file of its own choosing.
    entry = catalog_entries().get(name)
    if entry is None:
        raise ManagerError(f"unknown skill '{name}'")

    path = enabled_manpage(name)
    if path is not None:
        return read_manpage(path)

    category = str(entry.get("category") or "")
    if not category:
        raise ManagerError(f"the Catalog gives '{name}' no Category to fetch help from")

    return fetch_manpage(category, name)


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
    """Return the manager's own manpage, or the manpage of one of its verbs.

    A skill's help is not reached here (ADR-0044): one the user has answers
    `--help` itself, and one they do not is read about in Select. So an
    unknown name is refused with both routes named rather than looked for in
    the Catalog, which keeps Help answerable with no origin to reach.
    """

    # Bare help, and the manager's own name, both mean the manager's manpage.
    if not name or name == MANAGER:
        return read_manpage(here() / "help.md")

    verb = subcommand_manpage(name)
    if verb is None:
        raise ManagerError(
            f"unknown subcommand '{name}'; the manager documents its own verbs — "
            f"a skill of this collection answers '/{name} --help' itself, and "
            "'/kntnt select' reads the help of one you do not have"
        )

    return read_manpage(verb)


def cmd_help(name: str | None) -> int:
    """Print help for the manager or one of its subcommands."""

    print(help_text(name))
    return 0


def cmd_manpage(name: str) -> int:
    """Print one collection skill's manpage, whether or not it is Enabled."""

    print(skill_manpage(name))
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


def add_delta_flags(parser: argparse.ArgumentParser) -> None:
    """Add the answer form that names Skills instead of listing them.

    `--on` and `--off` each take one Skill and may be given as often as the
    answer has names, so a whole delta is one invocation. `--as-is` is the
    delta that names nothing — the answer is the set the layer already holds —
    and it is what `select --yes` comes down to once there is no list to open.
    """

    parser.add_argument("--on", action="append", default=[], metavar="SKILL")
    parser.add_argument("--off", action="append", default=[], metavar="SKILL")
    parser.add_argument("--as-is", action="store_true")


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


def refuse_project_on_uninstall(argv: list[str]) -> None:
    """Refuse `uninstall --project` in the verb's own terms, ahead of the parser.

    *argv* is what `normalize_argv` has already been over, so `--project=on`
    has become two arguments and the flag is always a word of its own.

    Uninstall declares no `--project`, so argparse would refuse this anyway —
    with `unrecognized arguments`, which says the flag is unknown where what
    the user has to learn is that the verb clears the machine. A meaningless
    flag is tolerated and a misleading one is refused (ADR-0029), and this is
    the misleading one: forwarded silently it would let a user believe they had
    scoped the run to a Project while it emptied their home. The check sits
    ahead of the parser so that the parser stays permissive for everything it
    does accept.
    """

    uninstalling = argv[0] in ("plan", "apply") and argv[1:2] == ["uninstall"]
    if uninstalling and "--project" in argv[2:]:
        raise ManagerError(
            "uninstall takes no --project: it clears this collection off this "
            "machine and never reaches a Project, whose own copies are checked "
            "into that repository and stay",
            2,
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the manager CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    help_cmd = sub.add_parser("help", help="Print help.")
    help_cmd.add_argument("subcommand", nargs="?")
    add_yes_flag(help_cmd)
    add_dry_run_flag(help_cmd)

    # Not a verb the user types: Select is what runs it, for a row the user
    # asked to read in full before answering the list (ADR-0044).
    manpage = sub.add_parser("manpage", help="Print one skill's manpage.")
    manpage.add_argument("skill")
    add_yes_flag(manpage)
    add_dry_run_flag(manpage)

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

    # Select's plan half takes no skill names: it is the list the user reads
    # before there is an answer to plan, and the answer arrives at Apply.
    plan_select = plan_sub.add_parser("select")
    add_project_flag(plan_select)
    add_yes_flag(plan_select)
    add_dry_run_flag(plan_select)
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

    # The names are the whole answer, so no names is the answer that checked
    # nothing — which Apply can read as such, having no list form to confuse
    # it with. The delta flags are the other answer form, for the run with
    # nobody at the list, and the two are refused together.
    apply_select = apply_sub.add_parser("select")
    apply_select.add_argument("skills", nargs="*")
    add_delta_flags(apply_select)
    add_project_flag(apply_select)
    add_yes_flag(apply_select)
    add_dry_run_flag(apply_select)
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

    if args.command == "help":
        return cmd_help(args.subcommand)
    if args.command == "manpage":
        return cmd_manpage(args.skill)
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
        return cmd_plan_select(global_layer=parse_layer(args.project))
    if args.verb == "uninstall":
        return cmd_apply_uninstall(yes=args.yes)
    if args.verb == "update":
        return cmd_apply_update(global_layer=parse_layer(args.project), yes=args.yes)
    return cmd_apply_select(
        args.skills,
        on=args.on,
        off=args.off,
        as_is=args.as_is,
        global_layer=parse_layer(args.project),
        yes=args.yes,
    )


def main(argv: list[str] | None = None) -> int:
    """Dispatch a manager command. Return an exit code."""

    raw = normalize_argv(list(sys.argv[1:] if argv is None else argv))
    if not raw:
        raw = ["help"]
    try:
        refuse_project_on_uninstall(raw)
        return dispatch(parse_args(raw))
    except ManagerError as exc:
        return fail(str(exc), exc.code)


if __name__ == "__main__":
    raise SystemExit(main())
