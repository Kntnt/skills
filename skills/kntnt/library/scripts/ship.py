# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Plan and apply commit, push, and release for the commit/push/release skills."""

from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Final
from urllib.parse import urlparse

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
JSON_VERSION_RE = re.compile(r'("version"\s*:\s*")([^"]+)(")')
TOML_VERSION_RE = re.compile(r'^(version\s*=\s*")([^"]+)(")', re.MULTILINE)
WORDPRESS_VERSION_RE = re.compile(r"^([ \t/*#@]*Version:[ \t]*)(\S+)", re.MULTILINE)
VERSION_FILE_RE = re.compile(r"\A(\s*)(\S+)")

# WordPress reads a plugin's header from the first 8 KiB of its main file.
WORDPRESS_HEADER_LENGTH: Final = 8192

RELEASE_ASSETS_COMMAND: Final = "bin/build-release-assets"
RELEASE_ASSETS_DIR: Final = "release-assets"
COMMIT_EXCERPT_HEAD: Final = 3
COMMIT_EXCERPT_TAIL: Final = 3

GITIGNORE_BASE = """# OS
.DS_Store
Thumbs.db

# Editors
.idea/
.vscode/
*.swp
*~

# Environment
.env
.env.*
!.env.example

# Claude local
.claude/settings.local.json
"""


class GitError(RuntimeError):
    """A git command failed."""


def fail(message: str, code: int = 1) -> int:
    """Print an error to stderr and return an exit code."""

    print(f"error: {message}", file=sys.stderr)
    return code


def git(cwd: Path, *args: str) -> str:
    """Run git in *cwd* and return stdout. Raise GitError on failure."""

    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise GitError(detail or f"git {' '.join(args)} failed")
    return result.stdout


def git_ok(cwd: Path, *args: str) -> bool:
    """Return True when a git command exits 0."""

    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def _gh(cwd: Path, *args: str) -> str:
    """Run gh in *cwd* and return stdout. Raise GitError on failure."""

    result = subprocess.run(
        ["gh", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise GitError(detail or f"gh {' '.join(args)} failed")
    return result.stdout


@dataclass
class Plan:
    """Facts the calling skill shows, then feeds to apply.

    ``commit_count`` always reports the complete changelog-baseline span,
    including when ``commits`` contains only an excerpt.
    """

    mode: str
    ready: bool
    reason: str | None = None
    branch: str | None = None
    default_branch: str | None = None
    dirty: bool = False
    stage_rule: str = "all"
    staged: list[str] = field(default_factory=list)
    tracked: list[str] = field(default_factory=list)
    untracked: list[str] = field(default_factory=list)
    unpushed: int | None = 0
    last_tag: str | None = None
    current_version: str | None = None
    version_files: list[str] = field(default_factory=list)
    unreleased_empty: bool | None = None
    gh: bool = False
    commits: list[dict[str, str]] = field(default_factory=list)
    commit_count: int = 0
    gitignore_proposal: str | None = None
    build: dict[str, str] | None = None


def status_paths(cwd: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (staged, tracked unstaged, untracked) paths from porcelain.

    Reads the NUL-separated form: git C-quotes any path with a byte outside
    ASCII in its default output, and these paths are shown to the user to
    confirm before a commit, so they have to arrive as themselves.
    """

    staged: list[str] = []
    tracked: list[str] = []
    untracked: list[str] = []

    # A rename or copy spends a second field on the original path. Walk the
    # fields by index so that one can be consumed rather than parsed as an
    # entry of its own.
    fields = git(cwd, "status", "--porcelain", "-z", "-uall").split("\0")
    index = 0
    while index < len(fields):
        entry = fields[index]
        index += 1
        if len(entry) < 4:
            continue
        code = entry[:2]
        path = entry[3:]
        if "R" in code or "C" in code:
            index += 1

        if code == "??":
            untracked.append(path)
        elif code[0] != " " and code[0] != "?":
            staged.append(path)
            if code[1] != " ":
                tracked.append(path)
        else:
            tracked.append(path)

    return staged, tracked, untracked


def current_branch(cwd: Path) -> str:
    """Return the current branch name."""

    name = git(cwd, "branch", "--show-current").strip()
    if not name:
        raise GitError("detached HEAD")
    return name


def default_branch(cwd: Path) -> str:
    """Return the default branch, preferring origin/HEAD."""

    try:
        ref = git(cwd, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").strip()
        if ref.startswith("refs/remotes/origin/"):
            return ref.removeprefix("refs/remotes/origin/")
    except GitError:
        pass
    for candidate in ("main", "master"):
        if git_ok(cwd, "show-ref", "--verify", "--quiet", f"refs/heads/{candidate}"):
            return candidate
    return current_branch(cwd)


def unpushed_count(cwd: Path) -> int | None:
    """Commits not in the upstream, or None when this branch has no upstream."""

    try:
        git(cwd, "rev-parse", "--abbrev-ref", "@{upstream}")
    except GitError:
        return None
    log = git(cwd, "rev-list", "--count", "@{upstream}..HEAD").strip()
    return int(log or "0")


def last_tag(cwd: Path) -> str | None:
    """Return the latest v* tag, or None."""

    try:
        tag = git(cwd, "describe", "--tags", "--abbrev=0", "--match", "v*").strip()
    except GitError:
        return None
    return tag or None


def commit_subjects(cwd: Path, since: str | None) -> list[dict[str, str]]:
    """Return oldest-first subjects since *since*, or the whole history."""

    # An unborn branch has no history to list.
    if not git_ok(cwd, "rev-parse", "--verify", "--quiet", "HEAD"):
        return []

    fmt = "%h\t%s"
    if since:
        output = git(cwd, "log", f"{since}..HEAD", "--reverse", f"--format={fmt}")
    else:
        output = git(cwd, "log", "--reverse", f"--format={fmt}")
    commits: list[dict[str, str]] = []
    for line in output.splitlines():
        sha, _, subject = line.partition("\t")
        if sha:
            commits.append({"sha": sha, "subject": subject})
    return commits


def gitignore_proposal(cwd: Path) -> str | None:
    """Return a proposed .gitignore, or None when one already exists."""

    if (cwd / ".gitignore").is_file():
        return None

    parts = [GITIGNORE_BASE]
    if (cwd / "package.json").is_file():
        parts.append("node_modules/\ndist/\n")
    if (cwd / "composer.json").is_file():
        parts.append("/vendor/\n")
    if (cwd / "pyproject.toml").is_file() or (cwd / "requirements.txt").is_file():
        parts.append(
            "__pycache__/\n*.py[cod]\n.venv/\n.mypy_cache/\n.pytest_cache/\n.ruff_cache/\n"
        )
    return "\n".join(part.rstrip() for part in parts) + "\n"


def detect_build(cwd: Path) -> dict[str, str] | None:
    """Return the release-assets command and its directory, or None.

    One convention covers every kind of Project, whatever its language: an
    executable `bin/build-release-assets` leaves the files to attach in
    `release-assets/`. A Project without it attaches nothing.
    """

    if (cwd / RELEASE_ASSETS_COMMAND).is_file():
        return {"command": RELEASE_ASSETS_COMMAND, "directory": RELEASE_ASSETS_DIR}
    return None


def build_plan(cwd: Path, mode: str, full_inventory: bool = False) -> Plan:
    """Gather plan facts for *mode* and project commits when requested."""

    staged, tracked, untracked = status_paths(cwd)
    dirty = bool(staged or tracked or untracked)
    branch = current_branch(cwd)
    tag = last_tag(cwd)
    commits = commit_subjects(cwd, tag)
    plan = Plan(
        mode=mode,
        ready=True,
        branch=branch,
        default_branch=default_branch(cwd),
        dirty=dirty,
        staged=staged,
        tracked=tracked,
        untracked=untracked,
        unpushed=unpushed_count(cwd),
        last_tag=tag,
        gh=shutil.which("gh") is not None,
        commits=commits,
        commit_count=len(commits),
        gitignore_proposal=gitignore_proposal(cwd),
        unreleased_empty=unreleased_is_empty(cwd / "CHANGELOG.md"),
    )

    if mode == "commit":
        if not dirty:
            plan.ready = False
            plan.reason = "nothing to commit"
        if not plan.ready and not full_inventory:
            plan.commits = []
        return plan

    if mode == "push":
        if not _origin_url(cwd):
            plan.ready = False
            plan.reason = "no origin remote"
        elif not dirty and plan.unpushed == 0:
            plan.ready = False
            plan.reason = "everything up-to-date"
        if not full_inventory and not plan.ready:
            plan.commits = []
        elif (
            not full_inventory
            and len(plan.commits) > COMMIT_EXCERPT_HEAD + COMMIT_EXCERPT_TAIL
        ):
            plan.commits = (
                plan.commits[:COMMIT_EXCERPT_HEAD] + plan.commits[-COMMIT_EXCERPT_TAIL:]
            )
        return plan

    plan.build = detect_build(cwd)
    locations = detect_versions(cwd)
    plan.version_files = [f"{path}:{version}" for path, version in locations]
    if locations:
        plan.current_version = locations[0][1]
    elif plan.last_tag and plan.last_tag.startswith("v"):
        plan.current_version = plan.last_tag[1:]
    return plan


def unreleased_is_empty(changelog: Path) -> bool | None:
    """True when [Unreleased] has no bullets; None when the file is missing."""

    if not changelog.is_file():
        return None
    text = changelog.read_text(encoding="utf-8")
    body = unreleased_body(text)
    if body is None:
        return None
    return not any(line.startswith(("- ", "* ")) for line in body.splitlines())


def unreleased_body(text: str) -> str | None:
    """Return the [Unreleased] section body, or None if the heading is absent."""

    marker = "## [Unreleased]"
    start = text.find(marker)
    if start < 0:
        return None
    rest = text[start + len(marker) :]
    next_heading = rest.find("\n## ")
    if next_heading >= 0:
        rest = rest[:next_heading]
    return rest


def detect_versions(cwd: Path) -> list[tuple[str, str]]:
    """Find conventional version locations relative to *cwd*."""

    found: list[tuple[str, str]] = []
    package = cwd / "package.json"
    if package.is_file():
        version = json_version(package)
        if version:
            found.append(("package.json", version))
    composer = cwd / "composer.json"
    if composer.is_file():
        version = json_version(composer)
        if version:
            found.append(("composer.json", version))
    pyproject = cwd / "pyproject.toml"
    if pyproject.is_file():
        version = toml_version(pyproject)
        if version:
            found.append(("pyproject.toml", version))
    cargo = cwd / "Cargo.toml"
    if cargo.is_file():
        version = toml_version(cargo)
        if version:
            found.append(("Cargo.toml", version))
    plugin = cwd / ".claude-plugin" / "plugin.json"
    if plugin.is_file():
        version = json_version(plugin)
        if version:
            found.append((".claude-plugin/plugin.json", version))
    for main_file in wordpress_plugin_files(cwd):
        version = wordpress_reader(main_file.read_text(encoding="utf-8"))
        if version:
            found.append((main_file.name, version))
    version_file = cwd / "VERSION"
    if version_file.is_file():
        version = version_file_reader(version_file.read_text(encoding="utf-8"))
        if version:
            found.append(("VERSION", version))
    return found


def wordpress_plugin_files(cwd: Path) -> list[Path]:
    """Return the PHP files at the root that carry a WordPress plugin header.

    WordPress recognises a plugin's main file by a `Plugin Name:` header in its
    first 8 KiB, so that is the test here too. A file that is not UTF-8 is not
    one this can rewrite safely, and is passed over.
    """

    found: list[Path] = []
    for path in sorted(cwd.glob("*.php")):
        try:
            head = path.read_text(encoding="utf-8")[:WORDPRESS_HEADER_LENGTH]
        except (OSError, UnicodeDecodeError):
            continue
        if "Plugin Name:" in head:
            found.append(path)
    return found


def wordpress_reader(text: str) -> str | None:
    """Return the `Version:` of a WordPress plugin header in *text*, or None."""

    head = text[:WORDPRESS_HEADER_LENGTH]
    if "Plugin Name:" not in head:
        return None
    match = WORDPRESS_VERSION_RE.search(head)
    return match[2] if match else None


def version_file_reader(text: str) -> str | None:
    """Return the version a `VERSION` file holds: its first word, or None."""

    words = text.split()
    return words[0] if words else None


def version_format(
    relative: str,
) -> tuple[Callable[[str], str | None], re.Pattern[str]]:
    """Return the reader and the rewrite pattern for a version location."""

    if relative == "VERSION":
        return version_file_reader, VERSION_FILE_RE
    if relative.endswith(".toml"):
        return toml_reader, TOML_VERSION_RE
    if relative.endswith(".php"):
        return wordpress_reader, WORDPRESS_VERSION_RE
    return json_reader, JSON_VERSION_RE


def json_version(path: Path) -> str | None:
    """Return the top-level version string from a JSON file."""

    return json_reader(path.read_text(encoding="utf-8"))


def json_reader(text: str) -> str | None:
    """Return the top-level version string from JSON *text*."""

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    value = data.get("version")
    return value if isinstance(value, str) else None


def toml_version(path: Path) -> str | None:
    """Return the declared version from a TOML file."""

    return toml_reader(path.read_text(encoding="utf-8"))


def toml_reader(text: str) -> str | None:
    """Return the declared version from TOML *text*, or None.

    Reads `[project]` first, then `[tool.poetry]` — the two places a Python
    project's own version conventionally lives — and then Cargo's `[package]`.
    A dynamic or workspace-inherited version is absent from all three, which
    is the correct answer: there is nothing here to bump.
    """

    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None

    tool = data.get("tool")
    poetry = tool.get("poetry") if isinstance(tool, dict) else None
    for table in (data.get("project"), poetry, data.get("package")):
        if isinstance(table, dict):
            value = table.get("version")
            if isinstance(value, str):
                return value
    return None


def apply_commit(cwd: Path, message: str) -> str:
    """Stage the working tree and commit. Return the new SHA."""

    git(cwd, "add", "-A")
    staged, _tracked, _untracked = status_paths(cwd)
    if not staged:
        raise GitError("nothing to commit")
    git(cwd, "commit", "-m", message)
    return git(cwd, "rev-parse", "--short", "HEAD").strip()


def apply_push(cwd: Path) -> str:
    """Push the current branch. Return a summary."""

    if not _origin_url(cwd):
        raise GitError("no origin remote")
    try:
        git(cwd, "rev-parse", "--abbrev-ref", "@{upstream}")
        has_upstream = True
    except GitError:
        has_upstream = False
    if has_upstream:
        git(cwd, "push")
    else:
        git(cwd, "push", "-u", "origin", "HEAD")
    return "pushed"


def _confirm_version(path: Path, updated: str, version: str, relative: str) -> None:
    """Raise unless *updated* reads back as *version* through the reader.

    The reader is the authority on where a version lives, so running it over
    the rewritten text is what proves the write hit that same place. It is the
    only check that also catches the ambiguous case, where a nested key holds
    the identical string and no value match can tell the two apart.
    """

    reader, _pattern = version_format(relative)
    if reader(updated) != version:
        raise GitError(f"could not bump version in {relative}")


def _rewrite_version(
    text: str, pattern: re.Pattern[str], current: str, version: str, relative: str
) -> str:
    """Return *text* with the assignment holding *current* set to *version*.

    Matching on the value rather than on the first occurrence is what keeps a
    nested `"version"` in some unrelated block from being rewritten instead of
    the real one. When no match carries *current*, or the result no longer
    reads back as *version*, this refuses: for a command that goes on to tag
    and publish, a wrong version written quietly is worse than a stopped run.
    """

    for match in pattern.finditer(text):
        if match[2] != current:
            continue
        return f"{text[: match.start(2)]}{version}{text[match.end(2) :]}"
    raise GitError(f"could not bump version in {relative}")


def bump_version_files(cwd: Path, version: str) -> list[Path]:
    """Write *version* into every detected conventional location. Return paths.

    Resolves every file before writing any of them, so a file this cannot
    rewrite unambiguously aborts the whole bump instead of leaving the project
    half-bumped for the caller to unpick by hand.
    """

    # Resolve first, write second — every failure mode has to land before the
    # first byte is written.
    resolved: list[tuple[Path, str]] = []
    for relative, current in detect_versions(cwd):
        path = cwd / relative
        _reader, pattern = version_format(relative)
        updated = _rewrite_version(
            path.read_text(encoding="utf-8"), pattern, current, version, relative
        )
        _confirm_version(path, updated, version, relative)
        resolved.append((path, updated))

    for path, updated in resolved:
        path.write_text(updated, encoding="utf-8")
    return [path for path, _updated in resolved]


def promote_changelog(text: str, version: str, date: str) -> str:
    """Turn [Unreleased] into a dated version heading and open a fresh one."""

    heading = "## [Unreleased]"
    if heading not in text:
        raise GitError("no ## [Unreleased] heading")
    return text.replace(heading, f"{heading}\n\n## [{version}] – {date}", 1)


def extract_release_notes(text: str, version: str) -> str:
    """Return the body of ``## [version]`` with headings shifted up one level."""

    pattern = re.compile(
        r"^## \[" + re.escape(version) + r"\][^\n]*\n(?P<body>.*?)"
        r"(?=^## \[|^\[[^\]]+\]:\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        return ""
    body = re.sub(
        r"^(#{3,6})(?= )", lambda m: m[1][1:], match["body"], flags=re.MULTILINE
    )
    return body.strip()


def _require_version(version: str) -> str:
    """Return the v-prefixed tag, or raise when *version* is not SemVer."""

    if not VERSION_RE.match(version):
        raise GitError(f"'{version}' is not a major.minor.patch version")
    return f"v{version}"


def _require_default_branch(cwd: Path) -> None:
    """Raise when HEAD is not the default branch."""

    branch = current_branch(cwd)
    default = default_branch(cwd)
    if branch != default:
        raise GitError(f"not on the default branch (on {branch}, default is {default})")


def apply_bump(cwd: Path, version: str) -> str:
    """Bump version files and promote the changelog. Return the version."""

    tag = _require_version(version)
    _require_default_branch(cwd)
    if git(cwd, "tag", "-l", tag).strip():
        raise GitError(f"tag {tag} already exists")
    changelog = cwd / "CHANGELOG.md"
    if unreleased_is_empty(changelog) is not False:
        raise GitError("nothing to release")

    bump_version_files(cwd, version)
    date = datetime.datetime.now(tz=datetime.UTC).date().isoformat()
    new_text = promote_changelog(changelog.read_text(encoding="utf-8"), version, date)
    changelog.write_text(new_text, encoding="utf-8")
    return version


def apply_tag(cwd: Path, version: str) -> str:
    """Create an annotated tag on HEAD, locally. Return the tag name.

    The tag stays local until `apply publish` has built the release assets:
    a build can then check the Project's version against the tag HEAD carries,
    and a failed build leaves nothing on the remote to take back.
    """

    tag = _require_version(version)
    if git(cwd, "tag", "-l", tag).strip():
        raise GitError(f"tag {tag} already exists")
    git(cwd, "tag", "-a", tag, "-m", tag)
    return tag


def apply_publish(cwd: Path, version: str, build: bool = True) -> str:
    """Build the release assets, push the tag, and create the GitHub release.

    The release is created with its notes and every asset in one `gh` call, so
    no reader of GitHub ever sees the version without its files. A failed
    build raises before anything leaves the machine: the tag stays local and
    no release exists. Without GitHub the tag is still pushed, a Project being
    versioned by its tag alone, and the missing release is the error.
    Without *build*, or without `bin/build-release-assets`, the release
    carries no files, whatever an earlier build left in `release-assets/`.
    """

    tag = _require_version(version)
    tag_ref = f"refs/tags/{tag}^{{commit}}"
    if not git_ok(cwd, "rev-parse", "--verify", "--quiet", tag_ref):
        raise GitError(f"no tag {tag}; create it with apply tag first")
    # Assets are built from HEAD, so a tag elsewhere would publish files that
    # were not built from the commit the release names.
    if git(cwd, "rev-parse", tag_ref) != git(cwd, "rev-parse", "HEAD"):
        raise GitError(f"tag {tag} does not point at HEAD")
    unavailable = _github_unavailable(cwd)

    assets: list[Path] = []
    if build and not unavailable and (cwd / RELEASE_ASSETS_COMMAND).is_file():
        try:
            assets = _build_release_assets(cwd)
        except GitError as exc:
            raise GitError(
                f"{exc}; {tag} is tagged locally only and nothing is published"
            ) from exc

    git(cwd, "push", "origin", tag)
    if unavailable:
        raise GitError(f"{unavailable}; {tag} is pushed without a GitHub release")

    notes = ""
    changelog = cwd / "CHANGELOG.md"
    if changelog.is_file():
        notes = extract_release_notes(changelog.read_text(encoding="utf-8"), version)
    try:
        _gh(
            cwd,
            "release",
            "create",
            tag,
            "--verify-tag",
            "--title",
            tag,
            "--notes",
            notes,
            *(str(asset) for asset in assets),
        )
    except GitError as exc:
        raise GitError(f"{exc}; {tag} is pushed without a GitHub release") from exc
    if not assets:
        return f"released {tag}"
    return f"released {tag} with " + ", ".join(asset.name for asset in assets)


def _build_release_assets(cwd: Path) -> list[Path]:
    """Build the release assets afresh and return every file, sorted.

    Empties `release-assets/` and runs `bin/build-release-assets`, so nothing
    from an earlier build rides along. Refuses before running anything when
    git tracks a file in that directory: emptying it would then destroy
    committed work rather than build output.
    """

    command = cwd / RELEASE_ASSETS_COMMAND
    if git(cwd, "ls-files", "--", RELEASE_ASSETS_DIR).strip():
        raise GitError(
            f"{RELEASE_ASSETS_DIR}/ holds files git tracks; refusing to empty it"
        )

    directory = cwd / RELEASE_ASSETS_DIR
    shutil.rmtree(directory, ignore_errors=True)
    directory.mkdir()

    # The command's own output is progress for whoever watches the release,
    # so it goes to stderr and stdout stays this verb's one-line result.
    try:
        built = subprocess.run([str(command)], cwd=cwd, stdout=sys.stderr, check=False)
    except OSError as exc:
        raise GitError(f"cannot run {RELEASE_ASSETS_COMMAND}: {exc}") from exc
    if built.returncode != 0:
        raise GitError(
            f"{RELEASE_ASSETS_COMMAND} failed with exit code {built.returncode}"
        )

    entries = sorted(directory.iterdir())
    nested = [entry.name for entry in entries if not entry.is_file()]
    if nested:
        raise GitError(
            f"{RELEASE_ASSETS_DIR}/ must hold only files, not {', '.join(nested)}"
        )
    if not entries:
        raise GitError(
            f"{RELEASE_ASSETS_COMMAND} left nothing in {RELEASE_ASSETS_DIR}/"
        )
    return entries


def _github_unavailable(cwd: Path) -> str | None:
    """Return why no GitHub release can be made, or None when one can."""

    if not shutil.which("gh"):
        return "gh not available"
    if "github" not in _remote_host(_origin_url(cwd)):
        return "origin is not GitHub"
    return None


def _origin_url(cwd: Path) -> str:
    """Return the origin URL, or empty when origin is missing."""

    try:
        return git(cwd, "remote", "get-url", "origin").strip()
    except GitError:
        return ""


def _remote_host(url: str) -> str:
    """Return the host of a git remote URL."""

    if not url:
        return ""
    if url.startswith("git@"):
        return url[4:].split(":", 1)[0]
    return urlparse(url).hostname or ""


def cmd_plan(cwd: Path, mode: str, full_inventory: bool = False) -> int:
    """Print a compact or complete JSON plan and return its readiness status."""

    try:
        plan = build_plan(cwd, mode, full_inventory)
    except GitError as exc:
        return fail(str(exc))
    print(json.dumps(asdict(plan), indent=2))
    if not plan.ready:
        return 2
    return 0


def cmd_apply(cwd: Path, args: argparse.Namespace) -> int:
    """Apply *args.mode* and print a one-line result."""

    try:
        if args.mode == "commit":
            message = args.message.strip()
            if not message:
                return fail("message is empty")
            result = apply_commit(cwd, message)
        elif args.mode == "push":
            result = apply_push(cwd)
        elif args.mode == "bump":
            result = apply_bump(cwd, args.version)
        elif args.mode == "tag":
            result = apply_tag(cwd, args.version)
        else:
            result = apply_publish(cwd, args.version, build=not args.no_build)
    except GitError as exc:
        text = str(exc)
        if text == "nothing to commit":
            return fail(text, 2)
        return fail(text)
    print(result)
    return 0


def add_yes_flag(parser: argparse.ArgumentParser) -> None:
    """Add --yes to a verb.

    The confirmation lives in the skill, not here — nothing in this script can
    prompt. Accepting the flag on every verb means the skill can pass the user's
    own arguments straight through without turning `--yes` into a crash.
    """

    parser.add_argument("--yes", action="store_true")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the ship CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Print a JSON plan and stop.")
    plan.add_argument("mode", choices=("commit", "push", "release"))
    plan.add_argument("--full", dest="full_inventory", action="store_true")
    add_yes_flag(plan)

    apply = sub.add_parser("apply", help="Apply a plan.")
    apply_sub = apply.add_subparsers(dest="mode", required=True)

    commit = apply_sub.add_parser("commit", help="Stage everything and commit.")
    commit.add_argument("--message", required=True)
    add_yes_flag(commit)

    add_yes_flag(apply_sub.add_parser("push", help="Push the current branch."))

    bump = apply_sub.add_parser("bump", help="Bump versions and promote the changelog.")
    bump.add_argument("--version", required=True)
    add_yes_flag(bump)

    tag = apply_sub.add_parser("tag", help="Tag HEAD locally.")
    tag.add_argument("--version", required=True)
    add_yes_flag(tag)

    publish = apply_sub.add_parser(
        "publish",
        help="Build the release assets, push the tag, and create the GitHub release.",
    )
    publish.add_argument("--version", required=True)
    publish.add_argument(
        "--no-build", action="store_true", help="Attach no release assets."
    )
    add_yes_flag(publish)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Dispatch plan or apply. Return an exit code."""

    args = parse_args(argv if argv is not None else sys.argv[1:])
    cwd = Path.cwd()
    if args.command == "plan":
        return cmd_plan(cwd, args.mode, args.full_inventory)
    return cmd_apply(cwd, args)


if __name__ == "__main__":
    raise SystemExit(main())
