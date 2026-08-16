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
from dataclasses import asdict, dataclass, field
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
JSON_VERSION_RE = re.compile(r'("version"\s*:\s*")([^"]+)(")')
TOML_VERSION_RE = re.compile(r'^(version\s*=\s*")([^"]+)(")', re.MULTILINE)


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


@dataclass
class Plan:
    """Facts the calling skill shows, then feeds to apply."""

    mode: str
    ready: bool
    reason: str | None = None
    branch: str | None = None
    default_branch: str | None = None
    dirty: bool = False
    stage_rule: str = "tracked"
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


def status_paths(cwd: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (staged, tracked unstaged, untracked) paths from porcelain."""

    staged: list[str] = []
    tracked: list[str] = []
    untracked: list[str] = []
    for line in git(cwd, "status", "--porcelain", "-uall").splitlines():
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
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


def build_plan(cwd: Path, mode: str) -> Plan:
    """Gather plan facts for *mode* in *cwd*."""

    staged, tracked, untracked = status_paths(cwd)
    dirty = bool(staged or tracked)
    stage_rule = "staged" if staged else "tracked"
    branch = current_branch(cwd)
    plan = Plan(
        mode=mode,
        ready=True,
        branch=branch,
        default_branch=default_branch(cwd),
        dirty=dirty,
        stage_rule=stage_rule,
        staged=staged,
        tracked=tracked,
        untracked=untracked,
        unpushed=unpushed_count(cwd),
        last_tag=last_tag(cwd),
        gh=shutil.which("gh") is not None,
    )

    if mode == "commit":
        if not dirty:
            plan.ready = False
            plan.reason = "nothing to commit"
        return plan

    if mode == "push":
        if not _origin_url(cwd):
            plan.ready = False
            plan.reason = "no origin remote"
        elif not dirty and plan.unpushed == 0:
            plan.ready = False
            plan.reason = "everything up-to-date"
        return plan

    plan.commits = commit_subjects(cwd, plan.last_tag)
    plan.unreleased_empty = unreleased_is_empty(cwd / "CHANGELOG.md")
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
    return not any(line.startswith("- ") or line.startswith("* ") for line in body.splitlines())


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
    plugin = cwd / ".claude-plugin" / "plugin.json"
    if plugin.is_file():
        version = json_version(plugin)
        if version:
            found.append((".claude-plugin/plugin.json", version))
    return found


def json_version(path: Path) -> str | None:
    """Return the top-level version string from a JSON file."""

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    value = data.get("version")
    return value if isinstance(value, str) else None


def toml_version(path: Path) -> str | None:
    """Return a ``version = "…"`` assignment from a TOML file."""

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("version") and "=" in stripped:
            _, _, raw = stripped.partition("=")
            return raw.strip().strip('"').strip("'")
    return None


def stage(cwd: Path, include: list[str]) -> None:
    """Stage tracked changes, or the existing index, plus any --include paths."""

    staged, tracked, _untracked = status_paths(cwd)
    if not staged:
        if tracked:
            git(cwd, "add", "-u")
    for path in include:
        git(cwd, "add", "--", path)


def apply_commit(cwd: Path, message: str, include: list[str]) -> str:
    """Stage and commit. Return the new SHA. Raise GitError if nothing to commit."""

    stage(cwd, include)
    staged, _tracked, _untracked = status_paths(cwd)
    if not staged:
        raise GitError("nothing to commit")
    git(cwd, "commit", "-m", message)
    return git(cwd, "rev-parse", "--short", "HEAD").strip()


def apply_push(cwd: Path, message: str, include: list[str]) -> str:
    """Commit when dirty, then push the current branch. Return a summary."""

    staged, tracked, _untracked = status_paths(cwd)
    parts: list[str] = []
    if staged or tracked or include:
        sha = apply_commit(cwd, message, include)
        parts.append(sha)
    try:
        git(cwd, "rev-parse", "--abbrev-ref", "@{upstream}")
        has_upstream = True
    except GitError:
        has_upstream = False
    if has_upstream:
        git(cwd, "push")
    else:
        git(cwd, "push", "-u", "origin", "HEAD")
    parts.append("pushed")
    return " ".join(parts)


def bump_version_files(cwd: Path, version: str) -> list[Path]:
    """Write *version* into every detected conventional location. Return paths."""

    written: list[Path] = []
    for relative, _current in detect_versions(cwd):
        path = cwd / relative
        original = path.read_text(encoding="utf-8")
        if path.suffix == ".toml":
            updated, count = TOML_VERSION_RE.subn(rf"\g<1>{version}\g<3>", original, count=1)
        else:
            updated, count = JSON_VERSION_RE.subn(rf"\g<1>{version}\g<3>", original, count=1)
        if count != 1:
            raise GitError(f"could not bump version in {relative}")
        path.write_text(updated, encoding="utf-8")
        written.append(path)
    return written


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
    body = re.sub(r"^(#{3,6})(?= )", lambda m: m[1][1:], match["body"], flags=re.MULTILINE)
    return body.strip()


def apply_release(cwd: Path, message: str, version: str, include: list[str]) -> str:
    """Bump, promote changelog, commit, tag, push, and publish."""

    if not VERSION_RE.match(version):
        raise GitError(f"'{version}' is not a major.minor.patch version")

    # Release only from the default branch, with a free tag name.
    branch = current_branch(cwd)
    default = default_branch(cwd)
    if branch != default:
        raise GitError(f"not on the default branch (on {branch}, default is {default})")
    tag = f"v{version}"
    if git(cwd, "tag", "-l", tag).strip():
        raise GitError(f"tag {tag} already exists")

    # Refuse when there is no user-facing Unreleased body to ship.
    changelog = cwd / "CHANGELOG.md"
    if unreleased_is_empty(changelog) is not False:
        raise GitError("nothing to release")

    # Write the version and promote the changelog before staging.
    bump_version_files(cwd, version)
    date = datetime.date.today().isoformat()
    new_text = promote_changelog(changelog.read_text(encoding="utf-8"), version, date)
    changelog.write_text(new_text, encoding="utf-8")

    git(cwd, "add", "--", "CHANGELOG.md")
    for relative, _current in detect_versions(cwd):
        git(cwd, "add", "--", relative)
    sha = apply_commit(cwd, message, include)

    # Tag the release commit and publish the branch, tag, and notes.
    git(cwd, "tag", "-a", tag, "-m", tag)
    git(cwd, "push", "-u", "origin", "HEAD")
    git(cwd, "push", "origin", tag)
    parts = [sha, tag, "pushed"]
    if shutil.which("gh") and "github.com" in _origin_url(cwd):
        notes = extract_release_notes(new_text, version)
        created = subprocess.run(
            ["gh", "release", "create", tag, "--title", tag, "--notes", notes],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        if created.returncode != 0:
            detail = (created.stderr or created.stdout).strip()
            raise GitError(f"tag pushed; gh release failed: {detail}")
        parts.append("released")
    return " ".join(parts)


def _origin_url(cwd: Path) -> str:
    """Return the origin URL, or empty when origin is missing."""

    try:
        return git(cwd, "remote", "get-url", "origin").strip()
    except GitError:
        return ""


def cmd_plan(cwd: Path, mode: str) -> int:
    """Print a JSON plan and return 0, or 2 when there is nothing to do."""

    try:
        plan = build_plan(cwd, mode)
    except GitError as exc:
        return fail(str(exc))
    print(json.dumps(asdict(plan), indent=2))
    if not plan.ready:
        return 2
    return 0


def cmd_apply(cwd: Path, args: argparse.Namespace) -> int:
    """Apply *args.mode* and print a one-line result."""

    message = args.message.strip()
    if not message:
        return fail("message is empty")
    try:
        if args.mode == "commit":
            result = apply_commit(cwd, message, args.include)
        elif args.mode == "push":
            result = apply_push(cwd, message, args.include)
        else:
            if not args.version:
                return fail("--version is required for release")
            result = apply_release(cwd, message, args.version, args.include)
    except GitError as exc:
        text = str(exc)
        if text == "nothing to commit":
            return fail(text, 2)
        return fail(text)
    print(result)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the ship CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="Print a JSON plan and stop.")
    plan.add_argument("mode", choices=("commit", "push", "release"))
    apply = sub.add_parser("apply", help="Apply a plan.")
    apply.add_argument("mode", choices=("commit", "push", "release"))
    apply.add_argument("--message", required=True)
    apply.add_argument("--version")
    apply.add_argument("--include", action="append", default=[])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Dispatch plan or apply. Return an exit code."""

    args = parse_args(argv if argv is not None else sys.argv[1:])
    cwd = Path.cwd()
    if args.command == "plan":
        return cmd_plan(cwd, args.mode)
    return cmd_apply(cwd, args)


if __name__ == "__main__":
    raise SystemExit(main())
