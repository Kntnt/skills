"""CLI behaviour of the commit skill's ship engine."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SHIP = REPO_ROOT / "skills" / "code" / "commit" / "scripts" / "ship.py"

_GIT_ENV = {
    key: value
    for key, value in os.environ.items()
    if not key.startswith("GIT_")
}
_GIT_ENV["GIT_AUTHOR_NAME"] = "Test"
_GIT_ENV["GIT_AUTHOR_EMAIL"] = "test@example.com"
_GIT_ENV["GIT_COMMITTER_NAME"] = "Test"
_GIT_ENV["GIT_COMMITTER_EMAIL"] = "test@example.com"


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=_GIT_ENV,
        text=True,
        capture_output=True,
        check=True,
    )


def _init_repo(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "-b", "main")
    _git(path, "config", "user.name", "Test")
    _git(path, "config", "user.email", "test@example.com")
    (path / "README.md").write_text("hello\n", encoding="utf-8")
    _git(path, "add", "README.md")
    _git(path, "commit", "-m", "init")
    return path


def _ship(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", str(SHIP), *args],
        cwd=cwd,
        env=_GIT_ENV,
        text=True,
        capture_output=True,
        check=False,
    )


def test_plan_commit_reports_tracked_dirty_file(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["mode"] == "commit"
    assert plan["ready"] is True
    assert plan["dirty"] is True
    assert "README.md" in plan["tracked"]


def test_plan_commit_exits_when_tree_is_clean(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 2
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["reason"] == "nothing to commit"


def test_apply_commit_commits_tracked_changes(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "apply", "commit", "--message", "Update greeting")

    assert result.returncode == 0, result.stderr
    log = _git(repo, "log", "-1", "--format=%s").stdout.strip()
    assert log == "Update greeting"
    status = _git(repo, "status", "--porcelain").stdout
    assert status == ""


def test_apply_commit_leaves_untracked_files_out(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")
    (repo / "scratch.tmp").write_text("nope\n", encoding="utf-8")

    result = _ship(repo, "apply", "commit", "--message", "Update greeting")

    assert result.returncode == 0, result.stderr
    files = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines()
    assert "scratch.tmp" not in files
    status = _git(repo, "status", "--porcelain").stdout
    assert "scratch.tmp" in status


def test_apply_commit_includes_named_untracked_file(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")
    (repo / "notes.md").write_text("keep\n", encoding="utf-8")

    result = _ship(
        repo, "apply", "commit", "--message", "Add notes", "--include", "notes.md"
    )

    assert result.returncode == 0, result.stderr
    files = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines()
    assert "notes.md" in files


def test_apply_commit_keeps_existing_index(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "one.txt").write_text("one\n", encoding="utf-8")
    (repo / "two.txt").write_text("two\n", encoding="utf-8")
    _git(repo, "add", "one.txt", "two.txt")
    _git(repo, "commit", "-m", "add files")
    (repo / "one.txt").write_text("ONE\n", encoding="utf-8")
    (repo / "two.txt").write_text("TWO\n", encoding="utf-8")
    _git(repo, "add", "one.txt")

    result = _ship(repo, "apply", "commit", "--message", "Change one")

    assert result.returncode == 0, result.stderr
    one = _git(repo, "show", "HEAD:one.txt").stdout
    two = _git(repo, "show", "HEAD:two.txt").stdout
    assert one == "ONE\n"
    assert two == "two\n"


def _bare_remote(tmp_path: Path, name: str = "remote.git") -> Path:
    remote = tmp_path / name
    _git(tmp_path, "init", "--bare", "-b", "main", str(remote))
    return remote


def test_plan_push_is_ready_when_branch_has_no_upstream(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))

    result = _ship(repo, "plan", "push")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert plan["unpushed"] is None


def test_plan_push_is_ready_when_unpushed(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    (repo / "README.md").write_text("pushed once\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "local only")

    result = _ship(repo, "plan", "push")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert plan["unpushed"] == 1
    assert plan["dirty"] is False


def test_apply_push_commits_and_pushes(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    (repo / "README.md").write_text("shared\n", encoding="utf-8")

    result = _ship(repo, "apply", "push", "--message", "Share greeting")

    assert result.returncode == 0, result.stderr
    assert "pushed" in result.stdout
    remote_head = _git(remote, "log", "-1", "--format=%s").stdout.strip()
    assert remote_head == "Share greeting"


CHANGELOG = """# Changelog

## [Unreleased]

### Added

- A new greeting.

## [0.1.0] – 2026-01-01
"""


def test_plan_release_lists_commits_and_version(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text('{"version": "0.1.0"}\n', encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "package.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add package")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    (repo / "README.md").write_text("hello there\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "Greet better")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["last_tag"] == "v0.1.0"
    assert plan["current_version"] == "0.1.0"
    assert "package.json:0.1.0" in plan["version_files"]
    assert plan["unreleased_empty"] is False
    subjects = [c["subject"] for c in plan["commits"]]
    assert "Greet better" in subjects


def test_apply_release_bumps_tags_and_pushes(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    (repo / "package.json").write_text('{"version": "0.1.0"}\n', encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "package.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add package")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")

    result = _ship(
        repo,
        "apply",
        "release",
        "--message",
        "Release 0.2.0: A new greeting",
        "--version",
        "0.2.0",
    )

    assert result.returncode == 0, result.stderr
    package = json.loads((repo / "package.json").read_text(encoding="utf-8"))
    assert package["version"] == "0.2.0"
    changelog = (repo / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.2.0]" in changelog
    assert "## [Unreleased]" in changelog
    tag = _git(repo, "tag", "-l", "v0.2.0").stdout.strip()
    assert tag == "v0.2.0"
    remote_tag = _git(remote, "tag", "-l", "v0.2.0").stdout.strip()
    assert remote_tag == "v0.2.0"


def test_apply_release_refuses_empty_unreleased(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n", encoding="utf-8"
    )
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")

    result = _ship(
        repo,
        "apply",
        "release",
        "--message",
        "Release 0.1.0: nothing",
        "--version",
        "0.1.0",
    )

    assert result.returncode == 1
    assert "nothing to release" in result.stderr


def test_apply_release_refuses_existing_tag(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "tag", "-a", "v0.2.0", "-m", "v0.2.0")

    result = _ship(
        repo,
        "apply",
        "release",
        "--message",
        "Release 0.2.0: A new greeting",
        "--version",
        "0.2.0",
    )

    assert result.returncode == 1
    assert "already exists" in result.stderr


def test_commit_skill_does_not_push() -> None:
    text = (REPO_ROOT / "skills" / "code" / "commit" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "disable-model-invocation: true" in text
    assert "git push" not in text
    assert "scripts/ship.py" in text


def test_push_and_release_call_the_commit_engine() -> None:
    for name in ("push", "release"):
        text = (REPO_ROOT / "skills" / "code" / name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "disable-model-invocation: true" in text
        assert "../commit/scripts/ship.py" in text


def test_apply_release_refuses_when_not_on_default_branch(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "checkout", "-b", "feature")

    result = _ship(
        repo,
        "apply",
        "release",
        "--message",
        "Release 0.2.0: A new greeting",
        "--version",
        "0.2.0",
    )

    assert result.returncode == 1
    assert "default branch" in result.stderr

