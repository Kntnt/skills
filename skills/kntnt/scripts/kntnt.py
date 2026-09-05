# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Manage which collection skills are Enabled on which Harnesses."""

from __future__ import annotations

import argparse
import ctypes
import fcntl
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
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, cast

import yaml

ORIGIN = "Kntnt/skills"
MANAGER = "kntnt"
UNIVERSAL_PROJECT = ".agents/skills"
CANONICAL_GLOBAL = "~/.agents/skills"

# Directory-relative sentinel used when Linux receives absolute paths.
AT_FDCWD = -100

# Platform flags that request an atomic exchange rather than replacement.
RENAME_EXCHANGE = 2
RENAME_SWAP = 2

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

# Domain-separate approval identities from every other Digest in the Manager.
UPDATE_APPROVAL_VERSION: int = 1

BINARY_HOW = {
    "uv": "install uv from https://docs.astral.sh/uv/",
    "git": "install git",
    "gh": "install GitHub CLI (gh) from https://cli.github.com/",
    "pdftotext": "install Poppler so pdftotext is available on PATH",
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


@dataclass(frozen=True)
class Publication:
    """One verified candidate and the physical target it may replace."""

    name: str
    candidate: Path
    target: Path


@dataclass(frozen=True)
class Withdrawal:
    """One physical active target omitted by the selected generation."""

    name: str
    target: Path


@dataclass(frozen=True)
class PreparedWithdrawal:
    """One withdrawal and the adjacent path retaining its old tree."""

    name: str
    target: Path
    backup: Path


@dataclass(frozen=True)
class PublishedTree:
    """One active target exchanged by the current publication transaction."""

    target: Path
    backup: Path
    active_before: bool
    active_after: bool


@dataclass(frozen=True)
class RollbackFailure:
    """One old tree a failed publication could not restore."""

    backup: Path
    detail: str


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


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Return the YAML frontmatter of a SKILL.md, or an empty dict.

    A file with no frontmatter and one whose fence is never closed both answer
    empty: neither states anything about the skill. Malformed YAML inside a
    closed fence is a different thing — it states something unreadable — and
    raises `yaml.YAMLError` for the caller to decide about (ADR-0060).
    """

    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}

    # The fence may hold any YAML document at all, since `carries_marker`
    # reads files the collection did not write: a list, a bare scalar, or
    # nothing between the fences is not a declaration and answers as none.
    frontmatter = yaml.safe_load(text[4:end])
    if isinstance(frontmatter, dict):
        return cast(dict[str, Any], frontmatter)
    return {}


DEP_KINDS = ("binaries", "skills", "externals", "capabilities")

# The prefix every key a collection skill writes under `metadata` carries. It
# is how a skill declares its Dependencies, and it is also this collection's
# mark on a skill it installed: no other collection has reason to write a key
# under this name, and it travels in the skill's own SKILL.md rather than in
# anything the Manager keeps beside itself. The specification allows `metadata`
# one level of string values and nothing else, so the namespace is spelled into
# the key rather than built out of a map underneath it (issue #52).
METADATA_PREFIX = "kntnt."

# What a YAML value is, said the way the author of the file spelled it. A
# refusal that named Python's type for it would answer in a language nobody
# wrote the frontmatter in, and `NoneType` for a key left empty is the worst
# of them.
YAML_TYPES = {
    type(None): "null",
    bool: "a boolean",
    int: "a number",
    float: "a number",
    str: "a string",
    list: "a list",
    dict: "a mapping",
}


def yaml_type(value: Any) -> str:
    """Name *value*'s YAML type for a message an author has to act on."""

    return YAML_TYPES.get(type(value), "a value")


def collection_block(frontmatter: dict[str, Any]) -> dict[str, Any] | None:
    """Return this collection's `metadata` keys unprefixed, or None where there are none.

    Any key at all under the prefix carries the marker, so a skill with no
    Dependencies is marked by writing its four lists empty rather than by an
    empty map that only means something to a parser reading the block whole.

    Values come back as the file spelled them. Coercing them here would answer
    a question this function is not asked: it says whether a skill is ours, on
    behalf of `carries_marker`, which reads files the collection did not write
    and may not raise about any of them. What a value is has to be refused
    somewhere that can refuse (issue #48).
    """

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        return None

    # The keys come from a file the collection did not write, where a key is
    # whatever YAML made of it, so each is read as text to compare at all.
    block = {
        str(key)[len(METADATA_PREFIX) :]: value
        for key, value in metadata.items()
        if str(key).startswith(METADATA_PREFIX)
    }

    return block or None


def value_fault(block: dict[str, Any]) -> str | None:
    """Say what is wrong with the first non-string value in *block*, or None.

    The specification allows `metadata` string values and nothing else, so a
    value of any other shape is a file to send back rather than one to read
    through `str()`: coercion is what put a Python repr where a Dependency
    list belonged, and it warns nobody because a string is a legal value
    (ADR-0061).
    """

    for key, value in block.items():
        if not isinstance(value, str):
            return (
                f"metadata.{METADATA_PREFIX}{key} is {yaml_type(value)}, not a "
                "string; metadata holds strings, and a list of names is one "
                "string with spaces between them"
            )

    return None


def marker_fault(frontmatter: dict[str, Any]) -> str | None:
    """Say why this skill's marker cannot be read, or None when it can.

    Three conditions rather than one, because the single message the first
    two shared described only the first of them and said something false
    about a file whose block was visibly there (issue #48).
    """

    # A `metadata` that is not a mapping has nowhere to hang a key, so it
    # reaches the same empty block as a skill that declares nothing at all.
    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return (
            f"metadata is {yaml_type(metadata)}, not a mapping; the "
            f"'{METADATA_PREFIX}' keys that mark a skill as this "
            "collection's have nowhere to be"
        )

    # No key under the prefix is the one condition the single message was
    # about: a skill carrying no mark of this collection at all.
    block = collection_block(frontmatter)
    if block is None:
        return (
            f"no metadata.{METADATA_PREFIX}* key; a skill without the marker "
            "cannot be removed when the collection withdraws it"
        )

    return value_fault(block)


def skill_deps(frontmatter: dict[str, Any]) -> dict[str, list[str]]:
    """Read Dependency lists from a skill's frontmatter.

    Each list is one space-separated string, as the specification's own
    `allowed-tools` is and for the same reason: a value `metadata` can hold.

    Raises:
        ManagerError: a `kntnt.` key holds something other than a string.
            Reading it anyway would answer with a Dependency list nobody
            declared, which is worse than not answering (issue #48).
    """

    block = collection_block(frontmatter) or {}
    fault = value_fault(block)
    if fault is not None:
        raise ManagerError(fault)

    return {key: block.get(key, "").split() for key in DEP_KINDS}


def carries_marker(skill_dir: Path) -> bool:
    """True when the skill installed at *skill_dir* came from this collection.

    Provenance is read off the skill's own frontmatter and off nothing else.
    Every file the Manager keeps beside itself is a sidecar the transport
    overwrites whenever it re-copies `kntnt`, so a record held there can forget
    that a skill was ever ours; the marker in the skill's own SKILL.md cannot
    (issue #20). Answers rather than raises, whatever it meets on the way.
    """

    # A layer holds skills this collection did not write, so the file is an
    # untrusted boundary: any bytes at all, no read permission, no file there,
    # or a fence around something that is not YAML. None of that can claim to
    # be ours, and none of it may take the run down — a traceback in place of
    # the report is the failure of #5.
    try:
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        return collection_block(parse_frontmatter(text)) is not None
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return False


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
MANAGER_DIGEST_IGNORE = frozenset({"catalog.json"})


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


def directory_digest(directory: Path, *, ignored: frozenset[str] = frozenset()) -> str:
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
        if path.is_file() and path.relative_to(directory).as_posix() not in ignored
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


def manager_digest(directory: Path) -> str:
    """Digest a Manager tree without its recursively generated Catalog."""

    # Break the Catalog's self-reference while covering every other shipped
    # file.
    return directory_digest(directory, ignored=MANAGER_DIGEST_IGNORE)


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


def write_catalog_file(path: Path, catalog: dict[str, Any]) -> None:
    """Store *catalog* at *path* in one move.

    Written to a sibling and renamed over the target, because a write in place
    is what leaves a half-written snapshot behind when a run is interrupted —
    and the reader treats a damaged one as no snapshot at all, so an in-place
    write can silently cost the user their fallback. A rename within one
    directory is atomic: what survives is the old file or the new one.
    """

    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    encoded = text.encode("utf-8")

    # An identical snapshot is no write, preserving the Manager tree's identity.
    try:
        if path.read_bytes() == encoded:
            return
    except OSError:
        pass

    # Sibling rather than a temporary directory: `replace` is only atomic
    # within one filesystem, and the directory the file lands in is the one
    # place guaranteed to be on it.
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def write_catalog(catalog: dict[str, Any]) -> None:
    """Store *catalog* beside the Manager that is running, in one move."""

    write_catalog_file(here() / "catalog.json", catalog)


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


def run_transport(
    args: list[str],
    *,
    internal: bool = False,
    cwd: Path | None = None,
    environment: dict[str, str] | None = None,
) -> None:
    """Run the transport. Skill files move only through this call."""

    raw = os.environ.get("KNTNT_TRANSPORT", "npx --yes skills")
    command = [*shlex.split(raw), *args]
    env = os.environ.copy()
    if environment is not None:
        env.update(environment)
    if internal:
        env["INSTALL_INTERNAL_SKILLS"] = "1"
    result = subprocess.run(
        command,
        cwd=cwd or project_root(),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ManagerError(detail or f"transport failed: {' '.join(args)}")


def transport_args(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> list[str]:
    """Build the one transport invocation that acquires *names*."""

    args = ["add", collection_source()]
    for name in names:
        args.extend(["--skill", name])
    for harness in harnesses:
        args.extend(["--agent", harness])
    if global_layer:
        args.append("--global")
    args.append("--yes")
    return args


def staging_environment(root: Path) -> dict[str, str]:
    """Create and return the homes an isolated transport acquisition uses."""

    staging_home = root / SANDBOX_HOME
    staging_project = root / SANDBOX_PROJECT
    staging_home.mkdir()
    staging_project.mkdir()
    return {
        "HOME": str(staging_home),
        "KNTNT_HOME": str(staging_home),
        "KNTNT_PROJECT": str(staging_project),
    }


def staged_skill_dirs(
    root: Path, harness: str, *, global_layer: bool
) -> list[tuple[Path, Path]]:
    """Pair possible staged skill directories with their active counterparts."""

    return [
        (
            sandbox_path(directory, root, global_layer=global_layer),
            directory,
        )
        for directory in skill_dirs(harness, global_layer=global_layer)
    ]


def local_source_skill(name: str) -> Path | None:
    """Return *name* in a local Collection origin, when this run has one."""

    source = Path(collection_source())
    if not source.is_dir():
        return None
    if name == MANAGER:
        candidate = source / "skills" / MANAGER
        return candidate if (candidate / "SKILL.md").is_file() else None
    for skill_md in source.glob("skills/*/*/SKILL.md"):
        if skill_md.parent.name == name:
            return skill_md.parent
    return None


def required_digest(value: Any, subject: str) -> str:
    """Return one valid SHA-256 Digest or refuse the selected Catalog."""

    try:
        decoded = bytes.fromhex(value) if isinstance(value, str) else b""
    except ValueError:
        decoded = b""
    if len(decoded) != hashlib.sha256().digest_size:
        raise ManagerError(f"{subject} carries no valid Digest")
    return cast(str, value)


def expected_candidate_digest(name: str) -> str:
    """Return the source-of-truth Digest available for a staged candidate."""

    source = local_source_skill(name)
    if source is not None:
        return manager_digest(source) if name == MANAGER else directory_digest(source)
    if name == MANAGER:
        return required_digest(
            load_catalog().get("manager_digest"), "selected Catalog Manager"
        )
    entry = catalog_entries().get(name, {})
    return required_digest(entry.get("digest"), f"selected Catalog entry '{name}'")


def validate_manager_candidate(candidate: Path) -> None:
    """Reject a staged Manager that cannot serve its own public entrypoints."""

    required = (
        "SKILL.md",
        "agents/openai.yaml",
        "catalog.json",
        "harness-paths.json",
        "help.md",
        "help/help.md",
        "help/select.md",
        "help/uninstall.md",
        "help/update.md",
        "library/references/changelog.md",
        "library/references/delivery.md",
        "library/scripts/integrations.py",
        "library/scripts/languages.py",
        "library/scripts/ship.py",
        "scripts/kntnt.py",
        "steps/help.md",
        "steps/select.md",
        "steps/uninstall.md",
        "steps/update.md",
    )
    missing = [
        relative for relative in required if not (candidate / relative).is_file()
    ]
    if missing:
        raise ManagerError(f"staged Manager is missing {', '.join(missing)}")

    # Verify every shipped interface is readable before checking structured
    # data and executable helpers more deeply.
    contents = {
        relative: (candidate / relative).read_text(encoding="utf-8")
        for relative in required
    }
    catalog = json.loads(contents["catalog.json"])
    if not isinstance(catalog, dict) or not isinstance(catalog.get("skills"), list):
        raise ManagerError("staged Manager carries a corrupt Catalog")
    if not isinstance(catalog.get(FEATURES, []), list):
        raise ManagerError("staged Manager carries a corrupt Catalog")
    validate_staged_features(candidate, catalog)
    paths = json.loads(contents["harness-paths.json"])
    if not isinstance(paths, dict):
        raise ManagerError("staged Manager carries a corrupt harness path table")
    agent = yaml.safe_load(contents["agents/openai.yaml"])
    if not isinstance(agent, dict):
        raise ManagerError("staged Manager carries a corrupt agent declaration")

    # Every Python helper is part of the runtime contract, not an opaque
    # sidecar.
    for relative, content in contents.items():
        if relative.endswith(".py"):
            compile(content, str(candidate / relative), "exec")

    # The acquired Manager must carry the same Catalog that selected this run.
    if catalog != load_catalog():
        raise ManagerError("staged Manager carries another Collection Catalog")


def validate_staged_features(candidate: Path, catalog: dict[str, Any]) -> None:
    """Refuse a staged Manager that cannot run the Features its own Catalog names.

    A Feature ships inside the Manager rather than travelling as its own skill
    directory (ADR-0173), so a truncated Manager is the one way a Feature's
    files can be missing while its Catalog row goes on offering it. The list is
    read from the staged Catalog rather than written here, because a hardcoded
    one would grow with every Feature and would refuse a Manager from a
    collection shipping different ones.
    """

    for entry in features_of(catalog):
        name = str(entry.get("name") or "")
        directory = candidate / FEATURES / name
        body = directory / "FEATURE.md"
        if not name or not body.is_file():
            raise ManagerError(
                f"staged Manager offers the Feature '{name}' and does not carry it"
            )
        declared = (
            collection_block(parse_frontmatter(body.read_text(encoding="utf-8"))) or {}
        ).get("integrations")
        script = directory / str(declared or "")
        if not declared or not script.is_file():
            raise ManagerError(
                f"staged Manager's Feature '{name}' declares no script it carries"
            )


def validate_candidate(name: str, candidate: Path, expected_digest: str) -> str:
    """Return a candidate's Digest after validating its readable contract."""

    try:
        if not candidate.is_dir():
            raise ManagerError(f"transport did not acquire '{name}'")
        frontmatter = parse_frontmatter(
            (candidate / "SKILL.md").read_text(encoding="utf-8")
        )
        if frontmatter.get("name") != name:
            raise ManagerError(f"staged '{name}' declares another name")
        digest = (
            manager_digest(candidate)
            if name == MANAGER
            else directory_digest(candidate)
        )
        if digest != expected_digest:
            raise ManagerError(f"staged '{name}' differs from the selected Collection")
        if name == MANAGER:
            write_catalog_file(candidate / "catalog.json", load_catalog())
            validate_manager_candidate(candidate)
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        yaml.YAMLError,
        SyntaxError,
    ) as exc:
        raise ManagerError(f"staged '{name}' could not be verified: {exc}") from exc

    return digest


def physical_target(target: Path) -> Path:
    """Resolve a logical skill path to the physical publication target."""

    return target.resolve(strict=False)


def acquisition_targets(
    root: Path,
    names: list[str],
    harnesses: list[str],
    *,
    global_layer: bool,
) -> list[Publication]:
    """Validate staged files and map them to every physical active target."""

    publications: dict[Path, Publication] = {}
    for name in names:
        expected = expected_candidate_digest(name)
        candidates: dict[Path, Path] = {}
        for harness in harnesses:
            found = [
                (staged / name, active / name)
                for staged, active in staged_skill_dirs(
                    root, harness, global_layer=global_layer
                )
                if (staged / name).is_dir()
            ]
            if not found:
                raise ManagerError(f"transport did not acquire '{name}' for {harness}")
            for candidate, target in found:
                candidates[candidate] = physical_target(target)

        # Every transport output must be the same verified Collection tree.
        digests = {
            validate_candidate(name, candidate, expected) for candidate in candidates
        }
        if len(digests) != 1:
            raise ManagerError(f"transport acquired mixed generations of '{name}'")
        source = next(iter(candidates))
        for target in candidates.values():
            publications[target] = Publication(name, source, target)

        # The running Manager may sit outside the layer's Detected Harnesses.
        if name == MANAGER:
            target = physical_target(here())
            publications[target] = Publication(name, source, target)

    return [
        publication
        for _, publication in sorted(
            publications.items(), key=lambda item: str(item[0])
        )
    ]


def withdrawal_targets(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> list[Withdrawal]:
    """Map withdrawn logical paths to their distinct physical active trees."""

    withdrawals: dict[Path, Withdrawal] = {}
    for name in names:
        for harness in harnesses:
            for directory in skill_dirs(harness, global_layer=global_layer):
                logical = directory / name
                if not logical.is_dir():
                    continue
                target = physical_target(logical)
                withdrawals[target] = Withdrawal(name, target)

    return [
        withdrawal
        for _, withdrawal in sorted(withdrawals.items(), key=lambda item: str(item[0]))
    ]


@contextmanager
def publication_locks(parents: list[Path]) -> Iterator[None]:
    """Serialize Collection publishers by locking their stable parent dirs."""

    descriptors: list[int] = []
    try:
        for parent in sorted(set(parents), key=str):
            descriptor = os.open(parent, os.O_RDONLY)
            descriptors.append(descriptor)
            fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        for descriptor in reversed(descriptors):
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)


def atomic_exchange(first: Path, second: Path) -> None:
    """Atomically exchange two non-empty directory entries on macOS or Linux."""

    library = ctypes.CDLL(None, use_errno=True)
    first_raw = os.fsencode(first)
    second_raw = os.fsencode(second)
    if sys.platform == "darwin":
        operation = library.renamex_np
        operation.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        operation.restype = ctypes.c_int
        result = operation(first_raw, second_raw, RENAME_SWAP)
    elif sys.platform.startswith("linux"):
        operation = library.renameat2
        operation.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        operation.restype = ctypes.c_int
        result = operation(AT_FDCWD, first_raw, AT_FDCWD, second_raw, RENAME_EXCHANGE)
    else:
        raise ManagerError(
            f"atomic directory publication is unsupported on {sys.platform}"
        )
    if result != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), str(second))


def remove_publication_tree(path: Path) -> None:
    """Remove one private staging or backup tree after a transaction."""

    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink():
        path.unlink()
    else:
        shutil.rmtree(path)


def rollback_publications(
    published: list[PublishedTree],
) -> list[RollbackFailure]:
    """Restore every old tree already exchanged by a failed transaction."""

    failures: list[RollbackFailure] = []
    for publication in reversed(published):
        try:
            if publication.active_before and publication.active_after:
                atomic_exchange(publication.backup, publication.target)
            elif publication.active_after:
                os.replace(publication.target, publication.backup)
            else:
                os.replace(publication.backup, publication.target)
        except OSError as exc:
            failures.append(
                RollbackFailure(publication.backup, f"{publication.target}: {exc}")
            )
    return failures


def publish_candidates(
    publications: list[Publication], withdrawals: list[Withdrawal] | None = None
) -> None:
    """Publish one complete generation, rolling every changed target back."""

    withdrawals = withdrawals or []
    created: list[Path] = []
    prepared: list[Publication] = []
    retired: list[PreparedWithdrawal] = []
    published: list[PublishedTree] = []
    preserved: set[Path] = set()
    try:
        # Create only the missing layer roots needed by a fully verified
        # acquisition.
        for publication in publications:
            missing: list[Path] = []
            parent = publication.target.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            created.extend(reversed(missing))
            publication.target.parent.mkdir(parents=True, exist_ok=True)

        parents = [publication.target.parent for publication in publications]
        parents.extend(withdrawal.target.parent for withdrawal in withdrawals)
        with publication_locks(parents):
            # Prepare every same-filesystem candidate before the first exchange.
            for publication in publications:
                if publication.target.exists() and not publication.target.is_dir():
                    raise ManagerError(
                        f"publication target '{publication.target}' is not a directory"
                    )
                candidate_digest = directory_digest(publication.candidate)
                if (
                    publication.target.is_dir()
                    and directory_digest(publication.target) == candidate_digest
                ):
                    continue
                staging = Path(
                    tempfile.mkdtemp(
                        prefix=f".{publication.target.name}.kntnt-stage-",
                        dir=publication.target.parent,
                    )
                )
                staging.rmdir()
                prepared.append(
                    Publication(publication.name, staging, publication.target)
                )
                shutil.copytree(
                    publication.candidate, staging, copy_function=shutil.copy2
                )
                if directory_digest(staging) != candidate_digest:
                    raise ManagerError(
                        f"staging copy for '{publication.target.name}' "
                        "could not be verified"
                    )

            # Reserve every rollback path before the active generation moves.
            for withdrawal in withdrawals:
                if not withdrawal.target.is_dir():
                    continue
                backup = Path(
                    tempfile.mkdtemp(
                        prefix=f".{withdrawal.target.name}.kntnt-retired-",
                        dir=withdrawal.target.parent,
                    )
                )
                backup.rmdir()
                retired.append(
                    PreparedWithdrawal(withdrawal.name, withdrawal.target, backup)
                )

            # Exchange each complete directory entry without an unreadable
            # interval.
            for publication in prepared:
                replaced = publication.target.exists()
                if replaced:
                    atomic_exchange(publication.candidate, publication.target)
                else:
                    os.replace(publication.candidate, publication.target)
                published.append(
                    PublishedTree(
                        publication.target,
                        publication.candidate,
                        active_before=replaced,
                        active_after=True,
                    )
                )

            # Remove omissions only while their old trees remain available to
            # roll back.
            for omission in retired:
                os.replace(omission.target, omission.backup)
                published.append(
                    PublishedTree(
                        omission.target,
                        omission.backup,
                        active_before=True,
                        active_after=False,
                    )
                )
    except (ManagerError, OSError) as exc:
        rollback_failures = rollback_publications(published)
        detail = f"publication failed: {exc}"
        if rollback_failures:
            preserved = {failure.backup for failure in rollback_failures}
            detail += "; rollback failed: " + "; ".join(
                failure.detail for failure in rollback_failures
            )
        raise ManagerError(detail) from exc
    finally:
        for publication in prepared:
            if publication.candidate not in preserved:
                remove_publication_tree(publication.candidate)
        for omission in retired:
            if omission.backup not in preserved:
                remove_publication_tree(omission.backup)
        for directory in reversed(created):
            try:
                directory.rmdir()
            except OSError:
                pass


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

    try:
        # Acquire and verify the complete generation before any active tree
        # moves.
        if names and harnesses:
            with tempfile.TemporaryDirectory(prefix="kntnt-acquire-") as temporary:
                root = Path(temporary)
                environment = staging_environment(root)
                run_transport(
                    transport_args(names, harnesses, global_layer=global_layer),
                    internal=True,
                    cwd=root / SANDBOX_PROJECT,
                    environment=environment,
                )
                publications = acquisition_targets(
                    root, names, harnesses, global_layer=global_layer
                )
                publish_candidates(publications)
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

    return verified_outcome(
        names, harnesses, global_layer=global_layer, expect_present=True
    )


def teardown_integrations(
    names: list[str], directories: list[Path]
) -> list[dict[str, Any]]:
    """Ask every skill in *names* that owns Harness integrations to remove them.

    A skill's files are what removes a skill's integrations, so this runs while
    those files are still on disk — after them, nothing is left that knows what
    was installed or where. The declaration is the skill's own
    `metadata.kntnt.integrations`, naming a script inside its directory, and the
    contract is one word: `remove-integrations`, answered with JSON. The Manager
    learns no Harness's hook format that way, and a second skill needing the
    same thing declares it the same way (ADR-0012).

    A teardown that fails is reported and never raised. External state this
    collection does not own cannot be allowed to hold up the removal of files
    it does own, and a partial removal reported is a partial removal the user
    can finish by hand.

    Which layer may ask this at all is not decided here. `removal_integrations`
    is the gate, and every caller reaches this through it.
    """

    reported: list[dict[str, Any]] = []
    for name in names:
        for directory in directories:
            skill = directory / name
            body = skill / "SKILL.md"
            if not body.exists():
                continue
            try:
                declared = (
                    collection_block(
                        parse_frontmatter(body.read_text(encoding="utf-8"))
                    )
                    or {}
                ).get("integrations")
            except OSError:
                continue
            if not isinstance(declared, str) or not declared.strip():
                continue

            # A declaration is a path inside the skill, and only inside it: a
            # skill cannot name somebody else's script for the Manager to run.
            script = (skill / declared).resolve()
            if not script.is_relative_to(skill.resolve()):
                reported.append(
                    {
                        "name": name,
                        "status": "failed",
                        "detail": f"{declared} points outside the skill's own directory",
                        "removed": [],
                    }
                )
                continue

            reported.append(_teardown(name, script))
    return reported


def stage_integration_owners(root: Path, withdrawals: list[Withdrawal]) -> list[Path]:
    """Copy withdrawn owners so teardown can run after publication succeeds."""

    staged: list[Path] = []
    for index, withdrawal in enumerate(withdrawals):
        destination = root / "retired-integrations" / str(index)
        try:
            shutil.copytree(
                withdrawal.target,
                destination / withdrawal.name,
                symlinks=True,
            )
        except OSError as exc:
            raise ManagerError(
                f"could not stage integrations owned by '{withdrawal.name}': {exc}"
            ) from exc
        staged.append(destination)

    return staged


def _teardown(name: str, script: Path) -> dict[str, Any]:
    """Run one skill's declared teardown and read what it says it removed.

    From `home()` rather than from wherever the Manager was invoked. The same
    run that asks this may have just replaced the Manager's own installed
    tree, and a directory unlinked under a running process is one no launcher
    can start from — the failure arriving before the declared script is
    reached at all (issue #257). This seam hands the script everything it
    needs on the command line, so it has no working directory of its own to
    want, and the home Global paths resolve against is what no run of this
    collection removes.

    Where no home can be resolved at all, `Path.home()` raises `RuntimeError`
    rather than the `OSError` a missing directory would be, so the caught
    failure covers both: an unresolvable home is reported per skill like every
    other failure of this call, never raised (ADR-0090).
    """

    if not script.exists():
        return {
            "name": name,
            "status": "failed",
            "detail": f"{script.name} is declared but not installed",
            "removed": [],
        }
    try:
        completed = subprocess.run(
            ["uv", "run", "--quiet", str(script), "remove-integrations"],
            cwd=home(),
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return {"name": name, "status": "failed", "detail": str(exc), "removed": []}

    if completed.returncode != 0:
        return {
            "name": name,
            "status": "failed",
            "detail": (completed.stderr or completed.stdout).strip()[:200],
            "removed": [],
        }
    try:
        answered = json.loads(completed.stdout)
        removed = answered.get("removed", []) if isinstance(answered, dict) else []
    except ValueError:
        removed = []
    return {"name": name, "status": "removed", "detail": None, "removed": removed}


# What a Project-layer placement leaves out. An owned entry is keyed by owner
# inside a Harness's own configuration, so a Global and a Project Enable of
# the same Skill would write and remove one another's single entry —
# measurement is a property of the machine, not of a working directory
# (issue #223 decision 4).
PROJECT_LAYER_INTEGRATIONS_NOTE = (
    "the Project layer installs no integration; only a Global Enable does"
)

# The other half of that same sentence, and a second thing to say rather than
# a widening of the first: a run that installed none and a run that removed
# none are different answers. Every owned entry a Project-layer run can reach
# belongs to a Global Enable, because that layer installs none of its own, so
# tearing one down there would take away what the other layer still describes.
PROJECT_LAYER_REMOVAL_NOTE = (
    "the Project layer removes no integration; only a Global Disable does"
)


def install_integrations(
    names: list[str], directories: list[Path], harnesses: list[str]
) -> list[dict[str, Any]]:
    """Ask every skill in *names* that owns Harness integrations to install them.

    The mirror of `teardown_integrations`: the same declaration
    (`metadata.kntnt.integrations`), the same per-skill script, the other
    word (issue #223 decision 1). It runs after a placement or a refresh has
    landed the skill's files, so the script it declares is there to run.

    Detected Harnesses are the Manager's own to resolve and pass, because a
    script may not sniff which Harness invoked it (ADR-0030) and the Manager
    already knows what this machine has (issue #223 decision 2); which of
    those a supported adapter actually exists for is the declared script's
    own answer to give back; every Detected Harness is handed on regardless
    of size. Install, repair, and refresh stay the same convergence over
    whatever is on disk (ADR-0090), so asking an already-installed skill
    again changes nothing, and a failed installation is reported per skill
    and never raised, exactly as a failed teardown is.
    """

    reported: list[dict[str, Any]] = []
    for name in names:
        for directory in directories:
            skill = directory / name
            body = skill / "SKILL.md"
            if not body.exists():
                continue
            try:
                declared = (
                    collection_block(
                        parse_frontmatter(body.read_text(encoding="utf-8"))
                    )
                    or {}
                ).get("integrations")
            except OSError:
                continue
            if not isinstance(declared, str) or not declared.strip():
                continue

            # A declaration is a path inside the skill, and only inside it, the
            # same rule teardown enforces for the same reason.
            script = (skill / declared).resolve()
            if not script.is_relative_to(skill.resolve()):
                reported.append(
                    {
                        "name": name,
                        "status": "failed",
                        "detail": f"{declared} points outside the skill's own directory",
                        "installed": [],
                    }
                )
                continue

            reported.append(_install(name, script, harnesses))
    return reported


def _install(name: str, script: Path, harnesses: list[str]) -> dict[str, Any]:
    """Run one skill's declared install and read what it says it installed.

    From `home()`, and answering an unresolvable one per skill, for the reasons
    `_teardown` states. Neither word takes a layer between here and the script:
    the Project layer reaches neither of them at all (ADR-0160), so what each
    resolves against is the machine's own home and never a working directory.
    """

    if not script.exists():
        return {
            "name": name,
            "status": "failed",
            "detail": f"{script.name} is declared but not installed",
            "installed": [],
        }
    try:
        completed = subprocess.run(
            [
                "uv",
                "run",
                "--quiet",
                str(script),
                "install-integrations",
                *[f"--harness={harness}" for harness in harnesses],
            ],
            cwd=home(),
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return {"name": name, "status": "failed", "detail": str(exc), "installed": []}

    if completed.returncode != 0:
        return {
            "name": name,
            "status": "failed",
            "detail": (completed.stderr or completed.stdout).strip()[:200],
            "installed": [],
        }
    try:
        answered = json.loads(completed.stdout)
        installed = answered.get("installed", []) if isinstance(answered, dict) else []
        unsupported = (
            answered.get("unsupported") if isinstance(answered, dict) else None
        )
    except ValueError:
        installed, unsupported = [], None
    report = {
        "name": name,
        "status": "installed",
        "detail": None,
        "installed": installed,
    }
    if unsupported:
        report["unsupported"] = unsupported
    return report


def placement_integrations(
    names: list[str],
    directories: list[Path],
    harnesses: list[str],
    *,
    global_layer: bool,
) -> dict[str, Any]:
    """Report what an Enabled skill's own install call did, or why none ran.

    Capture installs from the Global layer alone (issue #223 decision 4), so
    a Project-layer placement attempts nothing and names the reason in this
    report's one `note` line rather than silently doing nothing.
    """

    if not global_layer:
        return {"attempted": [], "note": PROJECT_LAYER_INTEGRATIONS_NOTE}
    return {
        "attempted": install_integrations(names, directories, harnesses),
        "note": None,
    }


def removal_integrations(
    names: list[str], directories: list[Path], *, global_layer: bool
) -> dict[str, Any]:
    """Report what a departing skill's own teardown did, or why none ran.

    The mirror of `placement_integrations`, gating the same layer for the same
    reason (ADR-0160). A Project-layer run cannot be removing anything a
    Project-layer run installed, because that layer installs nothing: whatever
    it could reach inside a Harness's own configuration was put there by a
    Global Enable that is still standing, and taking it away would leave that
    Enable describing a machine state that no longer exists.

    The directories come from the caller and are never resolved here. The two
    callers hold different ones: an uncheck hands the run's own layer, while a
    withdrawal hands the copies staged in a temporary directory, its files
    having already left every layer by the time it asks.
    """

    if not global_layer:
        return unattempted_removal(global_layer=global_layer)
    return {"attempted": teardown_integrations(names, directories), "note": None}


def unattempted_removal(*, global_layer: bool) -> dict[str, Any]:
    """Return the answer of a run that tore no integration down in this layer.

    The gate's own `note` without any records beside it. A Project-layer run
    has that sentence to give for itself, and a run that failed before its
    teardown could run has the same answer to carry rather than none at all —
    neither of them may ask a skill anything to arrive at it (issue #258).
    """

    return {
        "attempted": [],
        "note": None if global_layer else PROJECT_LAYER_REMOVAL_NOTE,
    }


def with_records(
    answer: dict[str, Any], records: list[dict[str, Any]]
) -> dict[str, Any]:
    """Return one integration answer with more records of the same kind in it.

    A Feature owns exactly what ADR-0090 gave a Skill and nothing else, so what
    its script did belongs under the key every other owned integration is
    reported under rather than in a second place a reader has to know about
    (ADR-0173). The `note` is untouched: it says what this layer does, which is
    the same sentence whoever the owner was.
    """

    if not records:
        return answer
    return {**answer, "attempted": [*answer.get("attempted", []), *records]}


def joined_integrations(
    first: dict[str, Any], second: dict[str, Any]
) -> dict[str, Any]:
    """Return two teardown answers as the one answer a verb reports.

    Uninstall tears down twice — the collection's skills, then the Manager —
    and both are one run's account of what left this machine's Harnesses. The
    note is a fact about the layer rather than about either half, so the two
    cannot disagree about it and the first that has one carries it.
    """

    return {
        "attempted": [*first["attempted"], *second["attempted"]],
        "note": first["note"] or second["note"],
    }


def remove_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Disable *names* on *harnesses* in the targeted layer, and verify it.

    What a skill installed outside its own directory has already gone by the
    time this runs: `removal_outcome` asks for it first, because the files
    that know how to remove it are the files this is about to delete.
    """

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


def failed_placement_outcome(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Report a refresh transaction that published none of its candidates."""

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
    removal that has to carry on regardless — an ordinary Disable or Uninstall
    deciding whether the Manager may go — reads that failure off the disk
    rather than raising it. What the run intended is unchanged either way;
    only the split between confirmed and failed differs.

    Where that split leaves a failure, the transport's own account of it goes
    to the user on stderr, which is the only place it is told.
    """

    # What a skill installed outside its own directory goes first, because the
    # files that know how to remove it are the files the transport is about to
    # delete — and the answer is held out here, outside the call that can
    # raise. A run that pulled a Skill's hooks out of a Harness and then met a
    # refusal has changed the machine, and an exception carrying that away
    # unreported is the one outcome not available (ADR-0036, issue #258).
    integrations = removal_integrations(
        names,
        layer_dirs(harnesses, global_layer=global_layer),
        global_layer=global_layer,
    )

    try:
        outcome = remove_skills(names, harnesses, global_layer=global_layer)
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

    # What a skill installed outside its own directory is reported beside what
    # the disk says of the files: a Harness this run could not clear is state
    # the user is left with, and silence about it is the one thing that would
    # make it theirs without their knowing (ADR-0036).
    return {**outcome, "removed_integrations": integrations}


def withdrawal_report(
    names: list[str],
    harnesses: list[str],
    *,
    global_layer: bool,
    integrations: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Report each withdrawn name from the active installation on disk."""

    outcome = verified_outcome(
        names, harnesses, global_layer=global_layer, expect_present=False
    )
    failed = {str(item["name"]): item["directories"] for item in outcome["failed"]}
    report: list[dict[str, Any]] = [
        (
            {"name": name, "disk": "failed", "directories": failed[name]}
            if name in failed
            else {"name": name, "disk": "removed"}
        )
        for name in names
    ]

    # Keep each external result beside the file removal owned by that Skill.
    by_name: dict[str, list[dict[str, Any]]] = {}
    for answer in integrations or []:
        by_name.setdefault(str(answer["name"]), []).append(answer)
    for item in report:
        name = str(item["name"])
        if name in by_name:
            item["integrations"] = by_name[name]

    return report


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


def refresh_outcome(
    names: list[str],
    withdrawn: list[str],
    harnesses: list[str],
    *,
    global_layer: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    """Acquire and publish the complete selected Collection generation.

    Three things come back: what the disk says of the placements, one report
    per withdrawal carrying that Skill's own teardown records, and the whole
    teardown answer — whose `note` has nowhere to sit in a per-Skill list and
    is the one thing a Project-layer run has to say for itself (issue #258).
    """

    # The gate's own answer for this layer, asking no skill anything, so a
    # failure before the teardown runs still carries the note the payload
    # needs and no run tears anything down twice.
    integrations = unattempted_removal(global_layer=global_layer)
    try:
        with tempfile.TemporaryDirectory(prefix="kntnt-acquire-") as temporary:
            root = Path(temporary)
            publications: list[Publication] = []
            if names and harnesses:
                environment = staging_environment(root)
                run_transport(
                    transport_args(names, harnesses, global_layer=global_layer),
                    internal=True,
                    cwd=root / SANDBOX_PROJECT,
                    environment=environment,
                )
                publications = acquisition_targets(
                    root, names, harnesses, global_layer=global_layer
                )

            # Preserve integration owners without changing external state before
            # every active filesystem target has committed.
            withdrawals = withdrawal_targets(
                withdrawn, harnesses, global_layer=global_layer
            )
            integration_owners = stage_integration_owners(root, withdrawals)
            publish_candidates(publications, withdrawals)

            # Publication has no remaining failure point, so external teardown
            # cannot leave a rolled-back tree without the integrations it owns.
            integrations = removal_integrations(
                withdrawn, integration_owners, global_layer=global_layer
            )
    except ManagerError as exc:
        relay_transport(str(exc))
        return (
            failed_placement_outcome(names, harnesses, global_layer=global_layer),
            withdrawal_report(withdrawn, harnesses, global_layer=global_layer),
            integrations,
        )

    return (
        verified_outcome(
            names, harnesses, global_layer=global_layer, expect_present=True
        ),
        withdrawal_report(
            withdrawn,
            harnesses,
            global_layer=global_layer,
            integrations=integrations["attempted"],
        ),
        integrations,
    )


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
    """Reject the Manager and unknown Catalog names.

    Both entry types answer here, because the list is answered as one checked
    set: the user reads two groups and writes one sentence, and a name is
    unknown only where neither group carries it. A Feature and a Skill may
    never share a name — Catalog generation refuses that — so nothing here has
    to decide which of the two a name meant (ADR-0173).
    """

    known = catalog_names() | feature_names()
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


# The Catalog's second entry type, and the one place a Feature's name is
# written. A Feature is not a Skill: no Harness loads it, the transport never
# moves it, and it has no directory in a skills tree. What it has is the one
# thing ADR-0090 gave a Skill — an owned integration it installs into a
# Harness's own configuration — and nothing else. So it ships inside the
# Manager, which is always installed, and Enabling it is exactly the install
# word the Manager already says at the seam where a Skill's files land
# (ADR-0173).
FEATURES = "features"

# What a Project-layer answer cannot reach, in the same voice its two siblings
# above use. A Feature owns nothing but Harness Integrations, and the Project
# layer installs and removes none of those: a Feature offered there would be a
# checkbox that could never change anything.
PROJECT_LAYER_FEATURES_NOTE = (
    "a Feature owns only Harness Integrations, which the Project layer neither "
    "installs nor removes; Features are chosen in the Global layer"
)


def features_of(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the Feature entries of *catalog*.

    A Catalog with no `features` key at all is one this collection published
    before Features existed, and reads as a collection shipping none — never as
    a corrupt Catalog, because a Manager newer than the Catalog it fetched is
    the ordinary state of a machine between two releases.
    """

    features = catalog.get(FEATURES, [])
    if not isinstance(features, list):
        raise ManagerError("Catalog is corrupt")
    return [entry for entry in features if isinstance(entry, dict)]


def catalog_features() -> list[dict[str, Any]]:
    """Return the Catalog's Feature entries."""

    return features_of(load_catalog())


def feature_entries() -> dict[str, dict[str, Any]]:
    """Return the Catalog's Features by name, in the order the Catalog lists them."""

    return {
        str(entry["name"]): entry for entry in catalog_features() if "name" in entry
    }


def feature_names() -> set[str]:
    """Return every Catalog Feature name."""

    return set(feature_entries())


def feature_dir(name: str) -> Path:
    """Return the directory a Feature ships in, inside the installed Manager."""

    return here() / FEATURES / name


def feature_script(name: str) -> Path | None:
    """Return the script a Feature declares, or None where it declares none.

    Read off the Feature's own `FEATURE.md` the same way a Skill's is read off
    its `SKILL.md`, and held to the same rule: a declaration is a path inside
    the Feature's own directory and never a way out of it.
    """

    directory = feature_dir(name)
    body = directory / "FEATURE.md"
    if not body.is_file():
        return None
    try:
        declared = (
            collection_block(parse_frontmatter(body.read_text(encoding="utf-8"))) or {}
        ).get("integrations")
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    if not isinstance(declared, str) or not declared.strip():
        return None
    script = (directory / declared).resolve()
    if not script.is_relative_to(directory.resolve()) or not script.is_file():
        return None
    return script


def run_feature(name: str, word: str, harnesses: list[str]) -> dict[str, Any]:
    """Say one word to one Feature's own script and read what it answers.

    The same call shape a Skill's declared integrations get, for the same
    reasons: from `home()`, with the Detected Harnesses handed in because a
    script may not sniff which Harness invoked it (ADR-0030), and answered per
    Feature rather than raised, because a Feature that could not be installed
    must not cost the user the report of the run that installed everything else.
    """

    script = feature_script(name)
    if script is None:
        return {
            "name": name,
            "status": "failed",
            "detail": f"the Feature '{name}' declares no readable script",
            "installed": [],
            "removed": [],
            "harnesses": [],
        }
    try:
        completed = subprocess.run(
            [
                "uv",
                "run",
                "--quiet",
                str(script),
                word,
                *[f"--harness={harness}" for harness in harnesses],
            ],
            cwd=home(),
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return {
            "name": name,
            "status": "failed",
            "detail": str(exc),
            "installed": [],
            "removed": [],
            "harnesses": [],
        }
    if completed.returncode != 0:
        return {
            "name": name,
            "status": "failed",
            "detail": (completed.stderr or completed.stdout).strip()[:200],
            "installed": [],
            "removed": [],
            "harnesses": [],
        }
    try:
        answered = json.loads(completed.stdout)
    except ValueError:
        answered = {}
    if not isinstance(answered, dict):
        answered = {}

    status = {"install-integrations": "installed", "remove-integrations": "removed"}
    report: dict[str, Any] = {
        "name": name,
        "status": status.get(word, "reported"),
        "detail": None,
        "installed": answered.get("installed", []),
        "removed": answered.get("removed", []),
        "harnesses": answered.get("harnesses", []),
    }
    unsupported = answered.get("unsupported")
    if unsupported:
        report["unsupported"] = unsupported
    return report


def feature_records(name: str, harnesses: list[str]) -> list[dict[str, Any]]:
    """Return what each Harness holds of one Feature right now."""

    answered = run_feature(name, "health", harnesses)
    records = answered.get("harnesses") or []
    return [record for record in records if isinstance(record, dict)]


def state_of_records(records: list[dict[str, Any]]) -> str:
    """Return enabled, disabled, or partial for one Feature's own health.

    The three words `skill_state` answers in, so a row reads the same whichever
    kind of entry it names. `healthy` and `gated` are both present — a gated
    integration is written and waiting on the Harness's own trust review, never
    absent — and everything else is not.
    """

    if not records:
        return "disabled"
    present = sum(
        1 for record in records if str(record.get("status")) in {"healthy", "gated"}
    )
    if present == 0:
        return "disabled"
    return "enabled" if present == len(records) else "partial"


def feature_state(name: str, harnesses: list[str], *, global_layer: bool) -> str:
    """Return enabled, disabled, or partial for one Feature in one layer.

    A Feature is a property of the machine rather than of a working directory,
    for the reason ADR-0160 already gave capture: an owned entry is keyed by
    owner inside a Harness's own configuration, so a Project-layer Enable and a
    Global one would write and remove each other's single entry. The Project
    layer therefore holds no Feature at all, and says so rather than reporting
    the machine's state as its own.
    """

    if not global_layer:
        return "disabled"
    return state_of_records(feature_records(name, harnesses))


def feature_serves(entry: dict[str, Any], harnesses: list[str]) -> list[str]:
    """Return the Detected Harnesses one Feature declares it can serve."""

    declared = {str(harness) for harness in entry.get("harnesses", [])}
    return [harness for harness in harnesses if harness in declared]


def feature_freshness(name: str, digest: str) -> str:
    """Say whether the Feature installed beside the Manager is the one shipped.

    The same three words `installed_freshness` answers in, over the one copy a
    Feature has: it ships inside the Manager, so there is never more than one.
    """

    directory = feature_dir(name)
    if not digest or not directory.is_dir():
        return "unknown"
    return "current" if directory_digest(directory) == digest else "deviating"


def enabled_feature_names(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return the Catalog Features this machine holds an integration of."""

    if not global_layer:
        return []
    return [
        str(entry["name"])
        for entry in catalog_features()
        if feature_state(str(entry["name"]), harnesses, global_layer=True) != "disabled"
    ]


def feature_rows(harnesses: list[str], *, global_layer: bool) -> list[dict[str, Any]]:
    """Build the second group of the list the user reads and answers.

    Every field a Skill's row carries that means the same thing here, plus the
    two a Feature has of its own: what it writes and where, which has to be
    readable before the row is checked rather than after, and which of the
    Detected Harnesses it can actually serve. A Feature no Detected Harness can
    serve is locked and says why, in the Capability vocabulary a Skill's
    Harness requirement is already said in (ADR-0030) — reported, never hidden.
    """

    if not global_layer:
        return []

    rows: list[dict[str, Any]] = []
    for entry in catalog_features():
        name = str(entry["name"])
        declared = [str(harness) for harness in entry.get("harnesses", [])]
        serves = feature_serves(entry, harnesses)
        records = feature_records(name, serves) if serves else []
        state = state_of_records(records)
        details = [str(record["detail"]) for record in records if record.get("detail")]
        rows.append(
            {
                "name": name,
                "category": str(entry.get("category") or "other"),
                "description": str(entry.get("description", "")),
                "writes": [str(line) for line in entry.get("writes", [])],
                "capabilities": entry.get("capabilities", []),
                "harnesses": declared,
                "serves": serves,
                "checked": state != "disabled",
                "incomplete": state == "partial",
                "freshness": feature_freshness(name, catalog_digest(entry)),
                "locked": not serves,
                "capability": None
                if serves
                else (
                    "no Detected Harness of this machine is one this Feature can "
                    f"serve; it serves {', '.join(declared) or 'no Harness'}"
                ),
                "detail": " ".join(details) or None,
            }
        )
    return rows


def feature_change(
    answer: list[str], harnesses: list[str], *, global_layer: bool
) -> tuple[list[str], list[str], list[str]]:
    """Split the Catalog's Features into what the answer installs, removes, and leaves.

    The Project layer changes none of them, so every Feature is left alone
    there and the payload's own note says why rather than a row pretending
    otherwise.

    A Feature is never *carried* the way a Skill is. What `carried` protects is
    a local edit a re-copy would overwrite, and a Feature has no copy in a
    layer to edit: what it owns is an entry inside a Harness's own
    configuration, where installing again is the same convergence as installing
    once. So an Enabled Feature that is not fully healthy is repaired by any
    run that reaches it, which is what an unattended `--as-is` promises.
    """

    if not global_layer:
        return [], [], [str(entry["name"]) for entry in catalog_features()]

    place: list[str] = []
    remove: list[str] = []
    noop: list[str] = []

    for entry in catalog_features():
        name = str(entry["name"])
        serves = feature_serves(entry, harnesses)
        state = feature_state(name, serves, global_layer=True)
        if name not in answer:
            if state != "disabled":
                remove.append(name)
            continue
        if not serves or state == "enabled":
            noop.append(name)
        else:
            place.append(name)

    return place, remove, noop


def feature_outcome(
    place: list[str], remove: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Install and tear down the answered Features, and verify both off the disk.

    The transport's own contract, applied to a kind of entry the transport
    never touches: the word a Feature was told is not the evidence it did
    anything, so each one is asked afterwards what its Harnesses actually hold
    (ADR-0003). A Feature that could not be brought to the answered state is
    named with the Harnesses it was asked about, which is where to look.
    """

    if not global_layer:
        return {
            "intended": [],
            "confirmed": [],
            "failed": [],
            "placed": [],
            "removed": [],
            "installed_integrations": [],
            "removed_integrations": [],
            "note": PROJECT_LAYER_FEATURES_NOTE,
        }

    entries = feature_entries()
    installed = [
        run_feature(
            name,
            "install-integrations",
            feature_serves(entries.get(name, {}), harnesses),
        )
        for name in place
    ]
    torn_down = [run_feature(name, "remove-integrations", []) for name in remove]

    confirmed: list[str] = []
    failed: list[dict[str, Any]] = []
    for name, wanted in [(name, "enabled") for name in place] + [
        (name, "disabled") for name in remove
    ]:
        serves = feature_serves(entries.get(name, {}), harnesses)
        if feature_state(name, serves, global_layer=True) == wanted:
            confirmed.append(name)
        else:
            failed.append({"name": name, "harnesses": serves})

    return {
        "intended": [*place, *remove],
        "confirmed": confirmed,
        "failed": failed,
        "placed": place,
        "removed": remove,
        "installed_integrations": installed,
        "removed_integrations": torn_down,
        "note": None,
    }


def unattempted_features(*, global_layer: bool) -> dict[str, Any]:
    """Return the answer of a run that changed no Feature in this layer."""

    return {
        "intended": [],
        "confirmed": [],
        "failed": [],
        "placed": [],
        "removed": [],
        "installed_integrations": [],
        "removed_integrations": [],
        "note": None if global_layer else PROJECT_LAYER_FEATURES_NOTE,
    }


def teardown_features(harnesses: list[str]) -> dict[str, Any]:
    """Take every Enabled Feature's integrations off this machine.

    Uninstall's own use, and the one seam where leaving them would be worst: a
    hook naming a script inside a Manager that has just been deleted is an
    entry the Harness runs at every session and nothing answers.
    """

    return feature_outcome(
        [],
        enabled_feature_names(harnesses, global_layer=True),
        harnesses,
        global_layer=True,
    )


def select_payload(*, global_layer: bool) -> dict[str, Any]:
    """Build the list the user reads and answers in one gesture.

    Two groups rather than one: the Catalog's Skills, and under them the
    Catalog's Features, which are the entries that install nothing a Harness
    loads and only write into a Harness's own configuration (ADR-0173). A
    Feature's row carries what it writes and where, because a row that edits a
    file the user owns and reads has to say so before it is checked.

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
        "features": feature_rows(harnesses, global_layer=global_layer),
        "features_note": None if global_layer else PROJECT_LAYER_FEATURES_NOTE,
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
    answer = [
        *enabled_names(harnesses, global_layer=global_layer),
        *enabled_feature_names(harnesses, global_layer=global_layer),
    ]

    # Only Skills are ever carried. A Feature has no copy in a layer for a
    # re-copy to overwrite, so the edit this protects cannot exist for one
    # (ADR-0173), and `feature_change` converges an Enabled Feature that is
    # not healthy whichever form the run arrived in.
    carried = (
        frozenset()
        if as_is
        else frozenset(enabled_names(harnesses, global_layer=global_layer))
        - frozenset(on)
    )

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


def update_approval_identity(payload: dict[str, Any]) -> str:
    """Identify one complete Update payload under the approval contract."""

    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    prefix = f"kntnt-update-plan-v{UPDATE_APPROVAL_VERSION}\0".encode()
    return hashlib.sha256(prefix + canonical).hexdigest()


def resolve_update_plan(*, global_layer: bool) -> tuple[list[str], dict[str, Any]]:
    """Resolve Update's targets and complete content-bound plan together."""

    # Resolve the exact target state and Catalog difference the plan describes.
    harnesses = target_harnesses(global_layer=global_layer)
    refresh, current = refresh_change(
        enabled_names(harnesses, global_layer=global_layer),
        harnesses,
        global_layer=global_layer,
    )
    new = new_entry_names(stored_catalog())
    refreshed = catalog_from_origin()

    # Withdrawals are safe to name only when the origin answered; the stored
    # Catalog cannot establish what the Collection has stopped shipping.
    remove = withdrawn_names(harnesses, global_layer=global_layer) if refreshed else []

    # Assemble every mutation and target the agent renders before confirmation.
    payload: dict[str, Any] = {
        "action": "update",
        "layer": "global" if global_layer else "project",
        "refresh": refresh,
        "current": current,
        "new": new,
        "enable": new,
        "remove": remove,
        "catalog_refreshed": refreshed,
        "directories": target_dirs(harnesses, global_layer=global_layer),
    }

    # Bind both possible answers to distinct complete plans; a response may
    # accept the offered Enablements or leave every new entry Disabled.
    without_enablement = {**payload, "enable": []}
    payload["approval"] = update_approval_identity(payload)
    payload["approval_without_enablement"] = update_approval_identity(
        without_enablement
    )
    return harnesses, payload


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
    """Make the targeted layer hold exactly the entries the answer checked.

    Skills and Features are answered together and reported apart: a Skill's
    outcome is about files in a layer and a Feature's is about entries in a
    Harness's own configuration, so the run carries the Features' own
    `intended`, `confirmed`, `failed`, `placed`, and `removed` under `features`
    rather than folding two different kinds of evidence into one list
    (ADR-0173). What each Feature's own script did is reported beside every
    other owned integration, under the keys those already have.

    Both halves of the answer are one verb's work, so both are reported
    together: `intended`, `confirmed`, and `failed` cover the run, and
    `placed` and `removed` say which way each intended name went (ADR-0036).
    Each half's Harness Integrations answer beside it — `integrations` for
    what a placement installed, `removed_integrations` for what an uncheck
    tore down — so one key means one thing across every verb (issue #258).

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
    feature_place, feature_remove, feature_noop = feature_change(
        answer, harnesses, global_layer=global_layer
    )

    # Unchecking deletes files the user chose to delete, and a script cannot
    # prompt, so the flag is that half of the answer's gate (ADR-0029). An
    # unchecked Feature deletes no file and still changes a Harness's own
    # configuration, which is the user's file too, so it is gated in its own
    # words rather than under a sentence about files that would be false.
    if remove:
        require_yes(yes, "unchecking these skills deletes their files")
    if feature_remove:
        require_yes(
            yes,
            "unchecking these Features takes what they wrote back out of your "
            "Harnesses' own configuration",
        )

    # The removals are read off the disk rather than raised, because the
    # placements have already landed by then: a transport that refuses one name
    # must not cost the user the report of what the same run did place.
    placed = add_skills(place, harnesses, global_layer=global_layer)
    removed = removal_outcome(remove, harnesses, global_layer=global_layer)
    features = feature_outcome(
        feature_place, feature_remove, harnesses, global_layer=global_layer
    )
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
            "noop": [*noop, *feature_noop],
            "features": {**features, "noop": feature_noop},
            "integrations": with_records(
                placement_integrations(
                    placed["confirmed"],
                    directories,
                    harnesses,
                    global_layer=global_layer,
                ),
                features["installed_integrations"],
            ),
            "removed_integrations": with_records(
                removed["removed_integrations"], features["removed_integrations"]
            ),
            "unsatisfied": unsatisfied_on_disk(harnesses, global_layer=global_layer),
            "layer": "global" if global_layer else "project",
            "catalog_refreshed": catalog_from_origin(),
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )

    # One rule across both entry types: a change the disk does not show fails
    # the run, whichever kind of entry failed to make it.
    return outcome_exit_code({"failed": [*outcome["failed"], *features["failed"]]})


def cmd_plan_uninstall() -> int:
    """Print what Uninstall will take off this machine."""

    harnesses = target_harnesses(global_layer=True)
    emit(
        {
            "action": "uninstall",
            "layer": "global",
            "skills": [*enabled_names(harnesses, global_layer=True), MANAGER],
            "features": enabled_feature_names(harnesses, global_layer=True),
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

    # The Features go first, while the Manager they ship inside is still on
    # disk to run them: a hook naming a script inside a deleted Manager is an
    # entry the Harness runs at every session and nothing answers (ADR-0173).
    features = feature_outcome(
        [],
        enabled_feature_names(harnesses, global_layer=True),
        harnesses,
        global_layer=True,
    )

    collection = removal_outcome(
        enabled_names(harnesses, global_layer=True), harnesses, global_layer=True
    )
    integrations = with_records(
        collection["removed_integrations"], features["removed_integrations"]
    )
    outcome = {key: collection[key] for key in ("intended", "confirmed", "failed")}

    # The Manager goes last, and only where the rest of the collection really
    # left: it is the one skill that can be asked to finish the job, and a
    # machine holding skills with no verb left to remove them is worse off than
    # one whose Manager outlives them by a run.
    if not outcome["failed"] and not features["failed"]:
        manager = removal_outcome([MANAGER], harnesses, global_layer=True)
        integrations = joined_integrations(
            integrations, manager["removed_integrations"]
        )
        outcome = {
            "intended": [*outcome["intended"], *manager["intended"]],
            "confirmed": [*outcome["confirmed"], *manager["confirmed"]],
            "failed": manager["failed"],
        }

    emit(
        {
            **outcome,
            # Both teardowns, under the key every verb's removal answers
            # under: this one places nothing, so `integrations` — which means
            # a placement everywhere else — never appears here (issue #258).
            "removed_integrations": integrations,
            "features": features,
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

    _, payload = resolve_update_plan(global_layer=global_layer)
    emit(payload)
    return 0


def cmd_apply_update(*, global_layer: bool, yes: bool, approval: str | None) -> int:
    """Refresh this collection, Enable what is new where the offer is answered.

    The offer is the one question Update asks, and `--yes` is how an answer
    reaches a script that cannot prompt (ADR-0029). Answered, the entries the
    collection has added since the last run are Enabled in the layer being
    updated and named in the report; unanswered, nothing new is placed — a run
    nobody answered has been told nothing (ADR-0007).
    """

    harnesses, plan = resolve_update_plan(global_layer=global_layer)

    # A direct Apply call carries no evidence that the current interaction
    # authorized a Global mutation, whatever surrounding mission invoked it.
    if global_layer and _SANDBOX is None:
        if approval is None:
            raise ManagerError(
                "global update requires the current plan's approval; run plan "
                "update and obtain a new user confirmation first",
                2,
            )
        approval_key = "approval" if yes else "approval_without_enablement"
        if approval != plan[approval_key]:
            raise ManagerError(
                "the approved global update plan changed; run plan update, show "
                "the complete new plan, and obtain a new user confirmation",
                2,
            )

    # What changed is the difference between the snapshot this Manager stored
    # and what the origin carries now, so the old half is read off the file
    # itself: the shared loader is already holding the new one.
    new_names = cast(list[str], plan["new"])

    # Every verb reasons from the origin, and whether it answered is what the
    # rest of the run is gated on: what may be deleted as Withdrawn, and
    # whether the snapshot below is worth writing at all.
    refreshed = cast(bool, plan["catalog_refreshed"])

    # The answer to the offer, and the whole of what a run places beyond a
    # refresh. Every name it adds is in the report, which is what makes an
    # unattended Update's one power — Enabling what the user pointed it at —
    # legible after the fact (ADR-0007).
    adopted = new_names if yes else []

    # What has been withdrawn is asked of the disk (ADR-0037), and only where
    # the origin answered. Its removal waits until acquisition and publication
    # succeed, so a failed replacement leaves the complete old Collection.
    withdrawn = cast(list[str], plan["remove"])

    desired = enabled_names(harnesses, global_layer=global_layer)
    refresh = cast(list[str], plan["refresh"])
    current = cast(list[str], plan["current"])

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
    # A refusal here is read rather than raised so the run can report the
    # failed replacement while leaving every active tree as it was. Omitted
    # Skills join the same rollback set rather than being removed afterward.
    outcome, withdrawals, withdrawn_integrations = refresh_outcome(
        place,
        withdrawn,
        harnesses,
        global_layer=global_layer,
    )

    # A refreshed Manager is a refreshed Feature: a Feature ships inside it, so
    # the script a Harness's hook table names and the prose a Feature's block
    # carries both come from the tree this run has just replaced. Re-converging
    # every Enabled Feature is what keeps a Harness from going on reading last
    # release's block; installing again is the same convergence as installing
    # once, so a Feature already correct costs nothing (ADR-0173).
    #
    # Only Enabled ones. A Feature new in this Catalog is not adopted here even
    # under `--yes`, unlike a new Skill: a Feature writes into files the user
    # owns and reads, and an unattended run must never place instructions the
    # user has not read (ADR-0043). It is offered by `select`, where what it
    # writes is on the row beside the checkbox.
    features = feature_outcome(
        enabled_feature_names(harnesses, global_layer=global_layer),
        [],
        harnesses,
        global_layer=global_layer,
    )

    # Update is the collection's one writer of the snapshot, and what holds it
    # back is any failed replacement. The difference against this file is the
    # whole of what makes an entry new, so a failed run must leave the prior
    # snapshot beside the prior readable Manager (ADR-0007).
    unplaced = {item["name"] for item in outcome["failed"]} & set(adopted)
    if refreshed and not global_layer and not outcome["failed"] and not unplaced:
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

            # A declaration this Manager cannot read is one of the layer's
            # Unsatisfied Dependencies rather than a refusal, because the run
            # is past the point where it may stop talking: the withdrawals
            # above are already deleted and the placements already made
            # (ADR-0036). Update reaches Skills a refresh could not repair —
            # one the origin was unreachable for, one a hand edit left with no
            # frontmatter at all — and each of those is exactly what has to be
            # reported (ADR-0068).
            fault = declaration_fault_at(skill_dir)
            if fault is not None:
                item = unreadable_declaration(skill_dir, fault)
                key = (item["kind"], item["name"], item["how"])
                if key not in seen:
                    seen.add(key)
                    unsatisfied.append(item)
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
            "integrations": with_records(
                placement_integrations(
                    outcome["confirmed"],
                    layer_dirs(harnesses, global_layer=global_layer),
                    harnesses,
                    global_layer=global_layer,
                ),
                features["installed_integrations"],
            ),
            "features": features,
            # The withdrawal teardown's own records already sit beside each
            # withdrawal in `removed`, so what is left to carry here is the
            # answer's `note` — the sentence a Project-layer run has for a
            # user who would otherwise believe their machine-wide integration
            # went with the files (issue #258).
            "removed_integrations": {**withdrawn_integrations, "attempted": []},
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


def declaration_fault_at(skill_dir: Path) -> str | None:
    """Say why the Dependency declaration at *skill_dir* cannot be read, or None.

    `carries_marker` asks the same predicate a different question. It reads
    directories the collection did not write, so no readable block there means
    *not ours*, and a stranger's skill legitimately declares nothing this
    Manager checks. Here the caller is a Skill of this collection asking about
    itself — nothing else invokes the checker — so the two states come apart
    and no readable declaration means *ours, and unreadable* (ADR-0068).
    """

    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return f"no SKILL.md at {skill_dir}"
    return marker_fault(parse_frontmatter(path.read_text(encoding="utf-8")))


def unreadable_declaration(skill_dir: Path, fault: str) -> dict[str, str]:
    """Describe an unreadable declaration as the Unsatisfied Dependency it is.

    The one shape every Unsatisfied Dependency is reported in, because the
    instruction each Skill carries is to emit what the checker said: an entry
    of another shape would reach the user through no documented channel, and
    the fault has to reach them to be acted on. Nothing here is a Dependency
    by name, so what is Unsatisfied is the declaration itself.

    The fault travels whole and framed rather than alone. `marker_fault` is
    written for the sweep, which asks the same question to decide whether a
    Skill can be withdrawn, so its sentence names a consequence that is not
    this reader's — true, and beside the point in front of somebody whose
    Skill just refused to run.
    """

    return {
        "name": skill_dir.name,
        "kind": "declaration",
        "how": (
            f"this Manager cannot read what the skill declares ({fault}); "
            "refresh this machine with '/kntnt update', which brings the "
            "Manager and every Enabled Skill to one revision of the collection"
        ),
    }


def declared_deps_at(skill_dir: Path) -> dict[str, list[str]]:
    """Return the Dependency lists declared in *skill_dir*/SKILL.md.

    Raises:
        ManagerError: the declaration cannot be read. Answering four empty
            lists is the answer a Skill genuinely requiring nothing gets, so a
            Manager meeting a shape it does not know reported nothing missing
            and handed the agent no Capability to confirm — both halves of the
            gate gone, without a word, for every Skill of a collection that had
            moved on (issue #68). A declaration that cannot be read is not a
            declaration of nothing (ADR-0068).
    """

    fault = declaration_fault_at(skill_dir)
    if fault is not None:
        raise ManagerError(fault)
    path = skill_dir / "SKILL.md"
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

    Exit 0 with both lists empty is the strongest thing this gate says, so it
    is never what an unreadable declaration earns: nothing missing that I can
    see is a claim about a declaration that was read (ADR-0068).
    """

    # A declaration this Manager cannot read is refused the way an Unsatisfied
    # Dependency is refused, and not raised: exit 2 with the reason on stdout
    # is the one non-zero answer every Skill's body documents a response to,
    # so the fault reaches the user rather than an empty stop (ADR-0068).
    fault = declaration_fault_at(skill_dir)
    if fault is not None:
        emit(
            {
                "ok": False,
                "unsatisfied": [unreadable_declaration(skill_dir, fault)],
                "capabilities": [],
            }
        )
        return 2

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


def synopsis_of(page: Path) -> str:
    """Return the `## SYNOPSIS` section of *page*, verbatim and whole.

    A syntax error prints a synopsis the collection ships rather than one
    composed here, and takes the section entire rather than the line it wants
    (ADR-0059). Anything rebuilt from the parser would be a second grammar,
    free to drift from the page the pointer at the end of the error leads to.
    """

    text = read_manpage(page)
    heading = "\n## SYNOPSIS\n"
    if heading not in text:
        raise ManagerError(f"'{page}' ships no Synopsis; run the transport again")

    return text.partition(heading)[2].partition("\n## ")[0].strip("\n")


def addressed_verb(argv: list[str]) -> str:
    """Return the word an invocation addressed.

    `plan` and `apply` are the two halves of one verb, so what the user
    addressed is the verb under them; everything else addresses itself.
    """

    if argv[0] in ("plan", "apply") and len(argv) > 1 and not argv[1].startswith("-"):
        return argv[1]

    return argv[0]


def addressed_page(argv: list[str]) -> tuple[Path, str]:
    """Return the manpage an invocation addressed and where to read it in full.

    A verb the manager documents answers with its own page. Anything else —
    an internal subcommand, or a word that is no subcommand at all — answers
    with the manager's own, and nothing is published to make the first case
    fit: `manpage`, `check`, and `catalog` are nobody's verbs (ADR-0046).
    """

    verb = addressed_verb(argv)
    page = subcommand_manpage(verb)
    if page is None:
        return here() / "help.md", "/kntnt --help"

    return page, f"/kntnt help {verb}"


def syntax_error(problem: str, argv: list[str]) -> ManagerError:
    """Answer a syntax error with the error, the synopsis, and the pointer.

    And with nothing else (ADR-0059): no guess at which verb was meant, no
    half of a run, and nothing done with the rest of a line whose first word
    was wrong. One shape for both halves of the grammar, so the difference
    between two refusals is never something only the source explains.
    """

    page, pointer = addressed_page(argv)

    return ManagerError(f"{problem}\n\n{synopsis_of(page)}\n\nsee '{pointer}'", 2)


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
        description = str(frontmatter.get("description") or "")

        # Generation is where a misspelt Capability has to fail. Past this
        # point the name would ride into the Catalog and only surface when a
        # user ran the skill. The same is true of the two fields the Catalog
        # exists to carry — the transport installs by directory name, and
        # the description is a skill's entire help until it is Enabled — and
        # of the marker, which is how Update tells a withdrawal of ours from
        # another collection's skill once this one has stopped shipping it.
        # The marker is asked first because everything below reads through
        # it, and because it is the one refusal `carries_marker` cannot make
        # on its own: this gate is the whole of what keeps a skill the sweep
        # could never withdraw off a user's disk (issue #48).
        fault = marker_fault(frontmatter)
        if fault is not None:
            raise ManagerError(f"{skill_md}: {fault}")
        deps = skill_deps(frontmatter)
        capability_notes(deps["capabilities"])
        if name != skill_md.parent.name:
            raise ManagerError(
                f"{skill_md}: name '{name}' is not the directory "
                f"'{skill_md.parent.name}'; the transport installs by directory"
            )
        if not description:
            raise ManagerError(f"{skill_md}: description is empty")
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
    manager = skills_root / MANAGER
    return {
        "origin": ORIGIN,
        "manager_digest": manager_digest(manager),
        "skills": entries,
        FEATURES: generate_features(manager, {entry["name"] for entry in entries}),
    }


# What a Feature's row has to say before it is checked, read from the Feature's
# own page rather than from a metadata string: these are sentences a person
# writes and a person reads, and `metadata` holds strings with spaces in them
# (ADR-0061), which a list of sentences is not.
WRITES_HEADING = "## Writes"


def feature_writes(text: str) -> list[str]:
    """Return the bullets under a Feature's `## Writes` heading.

    One line per thing the Feature writes and where. Select puts these in front
    of the user in the single question it asks before writing anything, because
    a row that edits a file the user owns and reads has to say so before it is
    checked rather than after (ADR-0173).
    """

    lines = text.splitlines()
    try:
        start = lines.index(WRITES_HEADING) + 1
    except ValueError:
        return []

    bullets: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif bullets and line.startswith("  ") and line.strip():
            bullets[-1] = f"{bullets[-1]} {line.strip()}"
    return bullets


def generate_features(manager: Path, skill_names: set[str]) -> list[dict[str, Any]]:
    """Build the Catalog's Feature entries from the `FEATURE.md` files inside the Manager.

    A Feature ships inside the Manager because it has nothing a Harness loads:
    what it owns is an entry in a Harness's own configuration, and the Manager
    is the one directory always on the machine to run it from (ADR-0173). So
    generation reads `skills/kntnt/features/*/FEATURE.md` rather than a second
    tree of its own.

    Everything a Skill's generation refuses, this refuses too, for the same
    reasons — an unreadable declaration, a name that is not the directory, an
    empty description, a Capability nothing defines — plus the two a Feature
    has of its own: a Harness it claims to serve that this collection has no
    path for, and a name a Skill already carries, which would make the one
    checked set the list is answered as ambiguous.
    """

    entries: list[dict[str, Any]] = []
    for feature_md in sorted((manager / FEATURES).glob("*/FEATURE.md")):
        text = feature_md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        name = str(frontmatter.get("name") or feature_md.parent.name)
        fault = marker_fault(frontmatter)
        if fault is not None:
            raise ManagerError(f"{feature_md}: {fault}")

        block = collection_block(frontmatter) or {}
        deps = {
            key: str(block.get(key, "")).split() for key in ("binaries", "capabilities")
        }
        capability_notes(deps["capabilities"])
        harnesses = str(block.get("harnesses", "")).split()
        description = str(frontmatter.get("description") or "")

        if name != feature_md.parent.name:
            raise ManagerError(
                f"{feature_md}: name '{name}' is not the directory "
                f"'{feature_md.parent.name}'; a Feature is addressed by its directory"
            )
        if name in skill_names:
            raise ManagerError(
                f"{feature_md}: '{name}' is also a Skill; the list is answered as "
                "one checked set, so a name has to mean one entry"
            )
        if not description:
            raise ManagerError(f"{feature_md}: description is empty")
        if not harnesses:
            raise ManagerError(
                f"{feature_md}: metadata.{METADATA_PREFIX}harnesses is empty; a "
                "Feature that serves no Harness can never be Enabled anywhere"
            )
        unknown = [name for name in harnesses if name not in harness_paths()]
        if unknown:
            raise ManagerError(
                f"{feature_md}: no Harness is named '{unknown[0]}' in the harness "
                "path table"
            )
        declared = str(block.get("integrations", ""))
        if not declared or not (feature_md.parent / declared).is_file():
            raise ManagerError(
                f"{feature_md}: metadata.{METADATA_PREFIX}integrations names no "
                "script inside this Feature; a Feature that installs nothing is "
                "nothing to Enable"
            )
        writes = feature_writes(text)
        if not writes:
            raise ManagerError(
                f"{feature_md}: no '{WRITES_HEADING}' bullets; a Feature's row has "
                "to say what it writes and where before it is checked"
            )

        entries.append(
            {
                "name": name,
                "category": str(block.get("category") or "other"),
                "description": description,
                "digest": directory_digest(feature_md.parent),
                "binaries": deps["binaries"],
                "capabilities": deps["capabilities"],
                "harnesses": harnesses,
                "writes": writes,
            }
        )
    return entries


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
    """Add --yes to a verb that asks something answerable yes or no.

    To those verbs and no others. A flag with no function on this verb is not
    a flag of this verb (ADR-0059), so the ones that ask nothing refuse it
    rather than accepting it and doing nothing with it.
    """

    parser.add_argument("--yes", action="store_true")


def add_dry_run_flag(parser: argparse.ArgumentParser) -> None:
    """Add --dry-run to a subcommand that acts on it.

    The changing verbs preview themselves in a Sandbox, and Catalog honours
    the flag where it writes. Nothing else has a use for it, and a use is the
    only way anything holds a flag under ADR-0059.
    """

    parser.add_argument("--dry-run", action="store_true")


def add_approval_flag(parser: argparse.ArgumentParser) -> None:
    """Add the opaque plan approval accepted only by Update's Apply half."""

    parser.add_argument("--approval")


def normalize_argv(argv: list[str]) -> list[str]:
    """Turn bare `--project` into the argv pair argparse reads it as.

    Written attached or bare, the flag is one token; argparse wants the value as
    an argument of its own, and without this a bare `--project` would swallow the
    skill name that follows it.
    """

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
    """Parse the manager CLI, strictly.

    An unknown subcommand and a disallowed flag are both errors, and both are
    answered in the manager's own terms rather than with argparse's usage dump
    (ADR-0059). The parser still does the deciding — what a subcommand is, and
    which flags it declared — so there is no second table here to disagree
    with it.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    # Help takes no flags at all. It changes nothing, asks nothing, and writes
    # nothing, so every flag the manager carries would mean nothing here.
    help_cmd = sub.add_parser("help", help="Print help.")
    help_cmd.add_argument("subcommand", nargs="?")

    # Not a verb the user types: Select is what runs it, for a row the user
    # asked to read in full before answering the list (ADR-0044). The rule
    # binds it and the two below all the same — a surface strict where
    # somebody is looking and lax where nobody is, is the seam again.
    manpage = sub.add_parser("manpage", help="Print one skill's manpage.")
    manpage.add_argument("skill")

    check = sub.add_parser("check", help="Refuse when a Dependency is Unsatisfied.")
    check.add_argument("--here", required=True, type=Path)

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
    add_approval_flag(apply_update)
    apply_uninstall = apply_sub.add_parser("uninstall")
    add_yes_flag(apply_uninstall)
    add_dry_run_flag(apply_uninstall)

    # A word that is no subcommand is where parsing stops. Nothing after it is
    # read: a mistyped verb used to run Help with the rest of the line as its
    # arguments, and a line meant for Update carries flags that would mean
    # something to whatever the typo landed on.
    if argv:
        verbs = {"plan": plan_sub.choices, "apply": apply_sub.choices}
        if argv[0] not in sub.choices:
            raise syntax_error(f"unknown subcommand '{argv[0]}'", argv)
        verb = addressed_verb(argv)
        if argv[0] in verbs and verb != argv[0] and verb not in verbs[argv[0]]:
            raise syntax_error(f"unknown subcommand '{verb}'", argv)

    # Whatever the subparser did not declare, it does not take. Argparse would
    # answer this with `unrecognized arguments` and its own usage, which names
    # neither the verb the user addressed nor where to read what it does take.
    args, extras = parser.parse_known_args(argv)
    if extras:
        stray = next((item for item in extras if item.startswith("-")), extras[0])
        raise syntax_error(f"{addressed_verb(argv)} takes no '{stray}'", argv)

    return args


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
    # happen in instead. The only other subcommand that declares the flag is
    # Catalog, which honours it itself, where it writes.
    if args.command == "apply" and args.dry_run:
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
    # honour — and honouring it is the only reason Catalog keeps a flag no
    # other internal subcommand does (ADR-0059).
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
        return cmd_apply_update(
            global_layer=parse_layer(args.project),
            yes=args.yes,
            approval=args.approval,
        )
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

    # A help flag after a public verb addresses that verb's shipped manpage.
    if (
        len(raw) == 2
        and raw[1] in ("--help", "-h")
        and subcommand_manpage(raw[0]) is not None
    ):
        raw = ["help", raw[0]]

    # Bare `/kntnt` and a top-level help flag address the Manager's own page.
    elif not raw or raw[0] in ("--help", "-h"):
        raw = ["help", *raw[1:]]

    try:
        return dispatch(parse_args(raw))
    except ManagerError as exc:
        return fail(str(exc), exc.code)


if __name__ == "__main__":
    raise SystemExit(main())
