"""CLI behaviour of the Collection Library's ship engine."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from support.contract import STANDARD
from support.fake_binary import fake_binary_on_path

REPO_ROOT = Path(__file__).resolve().parent.parent
SHIP = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts" / "ship.py"

_GIT_ENV = {
    key: value for key, value in os.environ.items() if not key.startswith("GIT_")
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


def _ship(
    cwd: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    merged = dict(_GIT_ENV)
    if env:
        merged.update(env)
    return subprocess.run(
        ["uv", "run", str(SHIP), *args],
        cwd=cwd,
        env=merged,
        text=True,
        capture_output=True,
        check=False,
    )


def _bare_remote(tmp_path: Path, name: str = "remote.git") -> Path:
    remote = tmp_path / name
    _git(tmp_path, "init", "--bare", "-b", "main", str(remote))
    return remote


CHANGELOG = """# Changelog

## [Unreleased]

### Added

- A new greeting.

## [0.1.0] – 2026-01-01
"""


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
    assert plan["commits"]


def test_plan_commit_is_ready_when_only_untracked(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "notes.md").write_text("keep\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert "notes.md" in plan["untracked"]


def test_plan_commit_exits_when_tree_is_clean(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 2
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["reason"] == "nothing to commit"
    assert plan["commits"] == []
    assert plan["commit_count"] == 1
    assert len(result.stdout) < 1000


def test_plan_commit_full_restores_inventory_and_preserves_clean_keys(
    tmp_path: Path,
) -> None:
    """The full override restores commits without changing the plan shape."""
    repo = _init_repo(tmp_path / "proj")

    bounded = _ship(repo, "plan", "commit")
    full = _ship(repo, "plan", "--full", "commit")

    bounded_plan = json.loads(bounded.stdout)
    full_plan = json.loads(full.stdout)
    assert set(bounded_plan) == set(full_plan)
    assert bounded_plan["commits"] == []
    assert full_plan["commit_count"] == len(full_plan["commits"]) == 1


def test_plan_push_excerpt_has_exact_head_and_tail(tmp_path: Path) -> None:
    """The bounded push projection keeps the three oldest and newest subjects."""
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    for index in range(8):
        (repo / "README.md").write_text(f"change {index}\n", encoding="utf-8")
        _git(repo, "add", "README.md")
        _git(repo, "commit", "-m", f"change {index}")

    plan = json.loads(_ship(repo, "plan", "push").stdout)
    assert [item["subject"] for item in plan["commits"]] == [
        "init",
        "change 0",
        "change 1",
        "change 5",
        "change 6",
        "change 7",
    ]


def test_plan_apply_rejects_full(tmp_path: Path) -> None:
    """The inventory override belongs exclusively to the plan verb."""
    repo = _init_repo(tmp_path / "proj")
    # Arrange and act through the CLI parser to verify the verb boundary.
    result = _ship(repo, "apply", "push", "--full")
    # Assert argparse rejects the plan-only option.
    assert result.returncode == 2


def test_plan_push_bounds_commits_and_full_restores_inventory(tmp_path: Path) -> None:
    """Bounded push output preserves the complete inventory under --full."""
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    for index in range(8):
        (repo / "README.md").write_text(f"change {index}\n", encoding="utf-8")
        _git(repo, "add", "README.md")
        _git(repo, "commit", "-m", f"change {index}")

    bounded = _ship(repo, "plan", "push")
    full = _ship(repo, "plan", "--full", "push")

    assert bounded.returncode == 0
    bounded_plan = json.loads(bounded.stdout)
    full_plan = json.loads(full.stdout)
    assert bounded_plan["commit_count"] == len(full_plan["commits"]) == 9
    assert len(bounded_plan["commits"]) == 6
    assert [item["subject"] for item in full_plan["commits"]] == [
        "init",
        *[f"change {index}" for index in range(8)],
    ]
    assert {
        key: value for key, value in bounded_plan.items() if key not in {"commits"}
    } == {key: value for key, value in full_plan.items() if key not in {"commits"}}


def test_plan_commit_proposes_gitignore_when_missing(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["gitignore_proposal"] is not None
    assert ".DS_Store" in plan["gitignore_proposal"]


def test_plan_commit_omits_gitignore_when_present(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / ".gitignore").write_text(".env\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["gitignore_proposal"] is None


def test_plan_commit_gitignore_includes_stack_entries(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text("{}\n", encoding="utf-8")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert "node_modules/" in plan["gitignore_proposal"]


def test_apply_commit_commits_tracked_changes(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "apply", "commit", "--message", "Update greeting")

    assert result.returncode == 0, result.stderr
    log = _git(repo, "log", "-1", "--format=%s").stdout.strip()
    assert log == "Update greeting"
    status = _git(repo, "status", "--porcelain").stdout
    assert status == ""


def test_apply_commit_includes_untracked_files(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "notes.md").write_text("keep\n", encoding="utf-8")

    result = _ship(repo, "apply", "commit", "--message", "Add notes")

    assert result.returncode == 0, result.stderr
    files = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines()
    assert "notes.md" in files


def test_apply_commit_stages_unstaged_tracked_files(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "one.txt").write_text("one\n", encoding="utf-8")
    (repo / "two.txt").write_text("two\n", encoding="utf-8")
    _git(repo, "add", "one.txt", "two.txt")
    _git(repo, "commit", "-m", "add files")
    (repo / "one.txt").write_text("ONE\n", encoding="utf-8")
    (repo / "two.txt").write_text("TWO\n", encoding="utf-8")
    _git(repo, "add", "one.txt")

    result = _ship(repo, "apply", "commit", "--message", "Change both")

    assert result.returncode == 0, result.stderr
    one = _git(repo, "show", "HEAD:one.txt").stdout
    two = _git(repo, "show", "HEAD:two.txt").stdout
    assert one == "ONE\n"
    assert two == "TWO\n"


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


def test_plan_push_exits_when_up_to_date(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")

    result = _ship(repo, "plan", "push")

    assert result.returncode == 2
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["reason"] == "everything up-to-date"


def test_apply_push_pushes_without_committing(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    (repo / "README.md").write_text("shared\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "Share greeting")
    (repo / "scratch.md").write_text("dirty\n", encoding="utf-8")

    result = _ship(repo, "apply", "push")

    assert result.returncode == 0, result.stderr
    assert "pushed" in result.stdout
    remote_head = _git(remote, "log", "-1", "--format=%s").stdout.strip()
    assert remote_head == "Share greeting"
    status = _git(repo, "status", "--porcelain").stdout
    assert "scratch.md" in status


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
    for index in range(7):
        (repo / "README.md").write_text(f"release change {index}\n", encoding="utf-8")
        _git(repo, "add", "README.md")
        _git(repo, "commit", "-m", f"release change {index}")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["last_tag"] == "v0.1.0"
    assert plan["current_version"] == "0.1.0"
    assert "package.json:0.1.0" in plan["version_files"]
    assert plan["unreleased_empty"] is False
    assert plan["build"] is None
    subjects = [c["subject"] for c in plan["commits"]]
    assert subjects == [
        "Greet better",
        *[f"release change {index}" for index in range(7)],
    ]
    assert len(plan["commits"]) == plan["commit_count"] == 8


def test_plan_commit_dirty_tree_keeps_complete_inventory(tmp_path: Path) -> None:
    """A ready commit plan retains every changelog-baseline commit."""
    repo = _init_repo(tmp_path / "proj")
    # Arrange a span longer than the bounded excerpt and leave the tree dirty.
    expected = ["init"]
    for index in range(8):
        (repo / "README.md").write_text(f"change {index}\n", encoding="utf-8")
        _git(repo, "add", "README.md")
        _git(repo, "commit", "-m", f"change {index}")
        expected.append(f"change {index}")
    (repo / "pending.md").write_text("pending\n", encoding="utf-8")

    # Act and assert that the ready plan keeps every subject in order.
    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0
    plan = json.loads(result.stdout)
    assert [item["subject"] for item in plan["commits"]] == expected
    assert plan["commit_count"] == len(expected)


def test_plan_release_detects_zip_script(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    scripts = repo / "scripts"
    scripts.mkdir()
    (scripts / "build-zip.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["build"]["command"] == "scripts/build-zip.sh"


def test_plan_release_detects_make_zip_target(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "Makefile").write_text("zip:\n\techo zip\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["build"]["command"] == "make zip"


def test_plan_release_detects_npm_zip_script(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text(
        '{"version": "0.1.0", "scripts": {"build:zip": "true"}}\n',
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["build"]["command"] == "npm run build:zip"


def test_apply_bump_writes_version_and_promotes_changelog(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text('{"version": "0.1.0"}\n', encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "package.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add package")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    assert "0.2.0" in result.stdout
    package = json.loads((repo / "package.json").read_text(encoding="utf-8"))
    assert package["version"] == "0.2.0"
    changelog = (repo / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.2.0]" in changelog
    assert "## [Unreleased]" in changelog
    assert _git(repo, "tag", "-l", "v0.2.0").stdout.strip() == ""


def test_apply_bump_refuses_empty_unreleased(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n", encoding="utf-8"
    )
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")

    result = _ship(repo, "apply", "bump", "--version", "0.1.0")

    assert result.returncode == 1
    assert "nothing to release" in result.stderr


def test_apply_bump_refuses_existing_tag(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "tag", "-a", "v0.2.0", "-m", "v0.2.0")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 1
    assert "already exists" in result.stderr


def test_apply_bump_refuses_when_not_on_default_branch(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "checkout", "-b", "feature")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 1
    assert "default branch" in result.stderr


def test_apply_tag_creates_and_pushes_tag(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")

    result = _ship(repo, "apply", "tag", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    assert "v0.2.0" in result.stdout
    assert _git(repo, "tag", "-l", "v0.2.0").stdout.strip() == "v0.2.0"
    assert _git(remote, "tag", "-l", "v0.2.0").stdout.strip() == "v0.2.0"


def test_apply_publish_creates_github_release(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "remote", "add", "origin", "git@github.com:example/proj.git")
    log = tmp_path / "gh.log"
    env = fake_binary_on_path(tmp_path, "gh", '#!/bin/sh\necho "$@" >> "$GH_LOG"\n')

    result = _ship(
        repo,
        "apply",
        "publish",
        "--version",
        "0.2.0",
        env=env | {"GH_LOG": str(log)},
    )

    assert result.returncode == 0, result.stderr
    assert "released" in result.stdout
    recorded = log.read_text(encoding="utf-8")
    assert "release create v0.2.0" in recorded


def test_apply_publish_uploads_asset_when_release_exists(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    asset = repo / "proj.zip"
    asset.write_text("zip", encoding="utf-8")
    _git(repo, "remote", "add", "origin", "https://github.com/example/proj.git")
    log = tmp_path / "gh.log"
    env = fake_binary_on_path(
        tmp_path,
        "gh",
        "#!/bin/sh\n"
        'echo "$@" >> "$GH_LOG"\n'
        'if [ "$1" = release ] && [ "$2" = view ]; then exit 0; fi\n',
    )

    result = _ship(
        repo,
        "apply",
        "publish",
        "--version",
        "0.2.0",
        "--asset",
        str(asset),
        env=env | {"GH_LOG": str(log)},
    )

    assert result.returncode == 0, result.stderr
    assert "uploaded" in result.stdout
    recorded = log.read_text(encoding="utf-8")
    assert "release upload v0.2.0" in recorded


def test_apply_bump_ignores_a_nested_version_key(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "composer.json").write_text(
        "{\n"
        '  "name": "acme/demo",\n'
        '  "extra": {\n'
        '    "pinned": { "version": "9.9.9" }\n'
        "  },\n"
        '  "version": "0.1.0"\n'
        "}\n",
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "composer.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add composer manifest")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    composer = json.loads((repo / "composer.json").read_text(encoding="utf-8"))
    assert composer["version"] == "0.2.0"
    assert composer["extra"]["pinned"]["version"] == "9.9.9"


def test_plan_release_ignores_a_version_scheme_setting(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "pyproject.toml").write_text(
        "[project]\n"
        'name = "demo"\n'
        'dynamic = ["version"]\n'
        "\n"
        "[tool.setuptools_scm]\n"
        'version_scheme = "post-release"\n',
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["version_files"] == []
    assert plan["current_version"] != "post-release"


def test_apply_bump_writes_the_pyproject_project_version(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "pyproject.toml").write_text(
        "[build-system]\n"
        'requires = ["hatchling"]\n'
        "\n"
        "[project]\n"
        'name = "demo"\n'
        'version = "0.1.0"\n',
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "pyproject.toml", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add pyproject")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    assert 'version = "0.2.0"' in (repo / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires = ["hatchling"]' in (repo / "pyproject.toml").read_text(
        encoding="utf-8"
    )


def test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text('{"version": "0.1.0"}\n', encoding="utf-8")
    ambiguous = (
        "{\n"
        '  "name": "acme/demo",\n'
        '  "extra": {\n'
        '    "pinned": { "version": "0.1.0" }\n'
        "  },\n"
        '  "version": "0.1.0"\n'
        "}\n"
    )
    (repo / "composer.json").write_text(ambiguous, encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "package.json", "composer.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add manifests")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode != 0
    assert "composer.json" in result.stderr
    assert (repo / "package.json").read_text(encoding="utf-8") == (
        '{"version": "0.1.0"}\n'
    )
    assert (repo / "composer.json").read_text(encoding="utf-8") == ambiguous
    assert "## [0.2.0]" not in (repo / "CHANGELOG.md").read_text(encoding="utf-8")


def test_apply_publish_passes_changelog_notes_with_shifted_headings(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n"
        "\n"
        "## [Unreleased]\n"
        "\n"
        "## [0.2.0] – 2026-02-02\n"
        "\n"
        "### Added\n"
        "\n"
        "- A shipped thing.\n"
        "\n"
        "## [0.1.0] – 2026-01-01\n"
        "\n"
        "### Added\n"
        "\n"
        "- An older thing.\n",
        encoding="utf-8",
    )
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "remote", "add", "origin", "git@github.com:example/proj.git")
    log = tmp_path / "gh.log"
    env = fake_binary_on_path(tmp_path, "gh", '#!/bin/sh\necho "$@" >> "$GH_LOG"\n')

    result = _ship(
        repo,
        "apply",
        "publish",
        "--version",
        "0.2.0",
        env=env | {"GH_LOG": str(log)},
    )

    assert result.returncode == 0, result.stderr
    recorded = log.read_text(encoding="utf-8")
    assert "- A shipped thing." in recorded
    assert "## Added" in recorded
    assert "An older thing" not in recorded


def test_plan_commit_reports_a_non_ascii_path_unescaped(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "skäl.md").write_text("reason\n", encoding="utf-8")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["untracked"] == ["skäl.md"]
    assert plan["tracked"] == ["README.md"]


def test_plan_commit_reports_a_renamed_path_once(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "gammal fil.txt").write_text("content\n", encoding="utf-8")
    _git(repo, "add", "gammal fil.txt")
    _git(repo, "commit", "-m", "Add a file")
    _git(repo, "mv", "gammal fil.txt", "ny fil.txt")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["staged"] == ["ny fil.txt"]
    assert plan["tracked"] == []
    assert plan["untracked"] == []


def test_commit_skill_does_not_push() -> None:
    body = REPO_ROOT / "skills" / "code" / "commit" / "SKILL.md"
    text = body.read_text(encoding="utf-8")

    assert "disable-model-invocation: true" in text, (
        f"{body}: this skill writes to the repository, so it carries"
        f" `disable-model-invocation: true` and is reached only when the user"
        f" types it. The field is what keeps a verb the user asks for from"
        f" becoming a verb a session may decide to run (ADR-0066). See"
        f" {STANDARD}."
    )
    assert "git push" not in text, (
        f"{body}: this skill commits and stops. Pushing is `/push`, a skill of"
        f" its own that declares this one — a body that pushed as well would"
        f" publish work on a step the user confirmed as a commit, and the body"
        f" is the whole of what the agent executes (ADR-0046). See {STANDARD}."
    )
    assert "$LIBRARY/scripts/ship.py" in text, (
        f"{body}: the body calls the Collection Library's `scripts/ship.py`"
        f" rather than running git itself. Every deterministic step lives"
        f" behind the engine's command line, which is the skill's only seam"
        f" and the only part of it a test can hold (ADR-0050). See {STANDARD}."
    )
    assert "$LIBRARY/references/changelog.md" in text, (
        f"{body}: the body follows the Collection Library's changelog"
        f" reference, so the same procedure serves every Skill that reconciles"
        f" `[Unreleased]` rather than belonging to one consumer (ADR-0076)."
        f" See {STANDARD}."
    )


def test_push_follows_commit_then_pushes() -> None:
    body = REPO_ROOT / "skills" / "code" / "push" / "SKILL.md"
    text = body.read_text(encoding="utf-8")

    assert "disable-model-invocation: true" in text, (
        f"{body}: this skill writes to a remote, so it carries"
        f" `disable-model-invocation: true` and is reached only when the user"
        f" types it. The field is what keeps a verb the user asks for from"
        f" becoming a verb a session may decide to run (ADR-0066). See"
        f" {STANDARD}."
    )
    assert "../commit/SKILL.md" in text, (
        f"{body}: the body follows the commit skill rather than restating its"
        f" steps. That skill is what this one declares in `kntnt.skills`, and a"
        f" second copy of the commit sequence is a copy that drifts from the"
        f" one the suite checks (ADR-0012). See {STANDARD}."
    )
    assert "apply push" in text, (
        f"{body}: the push itself is `ship.py apply push`, not a git command in"
        f" the prose. Every deterministic step lives behind the engine's"
        f" command line, which is the skill's only seam (ADR-0050). See"
        f" {STANDARD}."
    )


def test_release_follows_push_after_bump() -> None:
    body = REPO_ROOT / "skills" / "code" / "release" / "SKILL.md"
    text = body.read_text(encoding="utf-8")

    assert "disable-model-invocation: true" in text, (
        f"{body}: this skill tags and publishes, so it carries"
        f" `disable-model-invocation: true` and is reached only when the user"
        f" types it. A release starting itself is not a trade any argument pays"
        f" for (ADR-0066). See {STANDARD}."
    )
    assert "../push/SKILL.md" in text, (
        f"{body}: the body follows the push skill rather than restating it."
        f" That skill is what this one declares in `kntnt.skills`, and it is"
        f" what carries the commit before the tag is cut (ADR-0012). See"
        f" {STANDARD}."
    )
    for verb in ("apply bump", "apply tag", "apply publish"):
        assert verb in text, (
            f"{body}: the body reaches `ship.py {verb}` rather than doing that"
            f" step in prose. Every deterministic step lives behind the"
            f" engine's command line, which is the skill's only seam and the"
            f" only part of it a test can hold (ADR-0050). See {STANDARD}."
        )
    assert "--no-build" in text, (
        f"{body}: `--no-build` is in this skill's `argument-hint`, so the body"
        f" says what it does. A flag advertised in one place and absent from"
        f" another is a grammar that disagrees with itself, and the body is the"
        f" half the agent executes — it would refuse the flag its own hint"
        f" offered (ADR-0059). See {STANDARD}."
    )
