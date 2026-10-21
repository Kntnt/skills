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


def test_plan_commit_works_on_a_branch_without_commits(tmp_path: Path) -> None:
    """A first commit can be planned before the branch has any history."""

    # Arrange a repository whose branch has no commits yet.
    repo = tmp_path / "proj"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    (repo / "README.md").write_text("hello\n", encoding="utf-8")

    # Act through the same CLI the commit Skill calls.
    result = _ship(repo, "plan", "commit")

    # Assert the first change is ready with an empty history.
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert plan["dirty"] is True
    assert "README.md" in plan["untracked"]
    assert plan["commits"] == []
    assert plan["commit_count"] == 0
    assert plan["last_tag"] is None


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


RELEASED_CHANGELOG = """# Changelog

## [Unreleased]

## [0.2.0] – 2026-02-02

### Added

- A shipped thing.

## [0.1.0] – 2026-01-01

### Added

- An older thing.
"""


def _github_repo(tmp_path: Path) -> tuple[Path, Path]:
    """Return a released Project on a GitHub origin, and where its pushes land.

    The origin reads as GitHub, which is what the engine checks before it calls
    `gh`, while its push URL is a local bare repository, so a test can see what
    reached the remote without a network.
    """

    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(RELEASED_CHANGELOG, encoding="utf-8")
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Release 0.2.0")
    remote = _bare_remote(tmp_path)
    _git(repo, "remote", "add", "origin", "git@github.com:example/proj.git")
    _git(repo, "remote", "set-url", "--push", "origin", str(remote))
    _git(repo, "push", "origin", "main")
    return repo, remote


def _tag_locally(repo: Path, version: str = "0.2.0") -> None:
    _git(repo, "tag", "-a", f"v{version}", "-m", f"v{version}")


def _release_assets_command(repo: Path, script: str) -> None:
    command = repo / "bin" / "build-release-assets"
    command.parent.mkdir(exist_ok=True)
    command.write_text(script, encoding="utf-8")
    command.chmod(0o755)
    _git(repo, "add", "bin/build-release-assets")
    _git(repo, "commit", "-m", "Build release assets")


def _recording_gh(tmp_path: Path) -> tuple[dict[str, str], Path]:
    """Stand in for gh, recording each call's arguments as one record."""

    log = tmp_path / "gh.log"
    env = fake_binary_on_path(
        tmp_path,
        "gh",
        '#!/bin/sh\nprintf \'%s\\037\' "$@" >> "$GH_LOG"\nprintf \'\\036\' >> "$GH_LOG"\n',
    )
    return env | {"GH_LOG": str(log)}, log


def _gh_calls(log: Path) -> list[list[str]]:
    """Return every recorded gh call as its list of arguments."""

    if not log.exists():
        return []
    records = log.read_text(encoding="utf-8").split("\036")[:-1]
    return [record.split("\037")[:-1] for record in records]


def _remote_has_tag(remote: Path, tag: str = "v0.2.0") -> bool:
    return _git(remote, "tag", "-l", tag).stdout.strip() == tag


def test_plan_release_reports_the_release_assets_command(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    _release_assets_command(repo, "#!/bin/sh\n")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["build"] == {
        "command": "bin/build-release-assets",
        "directory": "release-assets",
    }


def test_apply_tag_creates_the_tag_without_pushing_it(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)

    result = _ship(repo, "apply", "tag", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    assert "v0.2.0" in result.stdout
    assert _git(repo, "tag", "-l", "v0.2.0").stdout.strip() == "v0.2.0"
    assert not _remote_has_tag(remote)


def test_apply_publish_creates_the_release_with_notes_and_every_asset_at_once(
    tmp_path: Path,
) -> None:
    repo, remote = _github_repo(tmp_path)
    # The build sees HEAD carrying the version's tag, which is what lets a
    # build check the Project's version against it.
    _release_assets_command(
        repo,
        "#!/bin/sh\n"
        "git describe --exact-match --tags HEAD > release-assets/tag.txt\n"
        "echo pdf > release-assets/book.pdf\n"
        "echo epub > release-assets/book.epub\n",
    )
    stale = repo / "release-assets" / "old.zip"
    stale.parent.mkdir()
    stale.write_text("from an earlier build", encoding="utf-8")
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("released v0.2.0")
    calls = _gh_calls(log)
    assert len(calls) == 1
    call = calls[0]
    assert call[:3] == ["release", "create", "v0.2.0"]
    assert "--verify-tag" in call
    notes = call[call.index("--notes") + 1]
    assert "- A shipped thing." in notes
    assert "## Added" in notes
    assert "An older thing" not in notes
    attached = [Path(arg).name for arg in call if Path(arg).is_absolute()]
    assert attached == ["book.epub", "book.pdf", "tag.txt"]
    assert (repo / "release-assets" / "tag.txt").read_text().strip() == "v0.2.0"
    assert not stale.exists()
    assert _remote_has_tag(remote)


def test_apply_publish_without_a_build_attaches_no_stale_asset(
    tmp_path: Path,
) -> None:
    repo, remote = _github_repo(tmp_path)
    stale = repo / "release-assets" / "old.zip"
    stale.parent.mkdir()
    stale.write_text("from a build by hand", encoding="utf-8")
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode == 0, result.stderr
    calls = _gh_calls(log)
    assert len(calls) == 1
    assert "old.zip" not in "".join(calls[0])
    assert not any(Path(arg).is_absolute() for arg in calls[0])
    assert stale.exists()
    assert _remote_has_tag(remote)


def test_apply_publish_no_build_neither_builds_nor_attaches(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    marker = tmp_path / "ran"
    _release_assets_command(repo, f"#!/bin/sh\ntouch {marker}\n")
    stale = repo / "release-assets" / "old.zip"
    stale.parent.mkdir()
    stale.write_text("from a build by hand", encoding="utf-8")
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(
        repo, "apply", "publish", "--no-build", "--version", "0.2.0", env=env
    )

    assert result.returncode == 0, result.stderr
    assert not marker.exists()
    calls = _gh_calls(log)
    assert len(calls) == 1
    assert not any(Path(arg).is_absolute() for arg in calls[0])
    assert stale.exists()
    assert _remote_has_tag(remote)


def test_apply_publish_publishes_nothing_when_the_build_fails(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    _release_assets_command(
        repo, "#!/bin/sh\necho half > release-assets/half.zip\nexit 3\n"
    )
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "bin/build-release-assets" in result.stderr
    assert "locally" in result.stderr
    assert not log.exists()
    assert not _remote_has_tag(remote)
    assert _git(repo, "tag", "-l", "v0.2.0").stdout.strip() == "v0.2.0"


def test_apply_publish_reports_the_pushed_tag_when_gh_fails(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    _tag_locally(repo)
    env = fake_binary_on_path(tmp_path, "gh", "#!/bin/sh\necho refused >&2\nexit 1\n")

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "refused" in result.stderr
    assert "pushed without a GitHub release" in result.stderr
    assert _remote_has_tag(remote)


def test_apply_publish_refuses_to_empty_tracked_files(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    marker = tmp_path / "ran"
    _release_assets_command(repo, f"#!/bin/sh\ntouch {marker}\n")
    tracked = repo / "release-assets" / "kept.txt"
    tracked.parent.mkdir()
    tracked.write_text("committed", encoding="utf-8")
    _git(repo, "add", "release-assets/kept.txt")
    _git(repo, "commit", "-m", "Track a file in release-assets")
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "release-assets" in result.stderr
    assert tracked.read_text(encoding="utf-8") == "committed"
    assert not marker.exists()
    assert not log.exists()
    assert not _remote_has_tag(remote)


def test_apply_publish_fails_when_the_command_leaves_nothing(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    _release_assets_command(repo, "#!/bin/sh\n")
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "release-assets" in result.stderr
    assert not log.exists()
    assert not _remote_has_tag(remote)


def test_apply_publish_refuses_a_directory_in_release_assets(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    _release_assets_command(
        repo, "#!/bin/sh\nmkdir release-assets/nested\necho x > release-assets/a.zip\n"
    )
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "nested" in result.stderr
    assert not log.exists()
    assert not _remote_has_tag(remote)


def test_apply_publish_refuses_a_tag_that_is_not_on_head(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    _tag_locally(repo)
    (repo / "README.md").write_text("fixed after tagging\n", encoding="utf-8")
    _git(repo, "commit", "-am", "Fix after tagging")
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "HEAD" in result.stderr
    assert not log.exists()
    assert not _remote_has_tag(remote)


def test_apply_publish_refuses_without_the_tag(tmp_path: Path) -> None:
    repo, remote = _github_repo(tmp_path)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "no tag v0.2.0" in result.stderr
    assert not log.exists()
    assert not _remote_has_tag(remote)


def test_apply_publish_pushes_the_tag_when_origin_is_not_github(
    tmp_path: Path,
) -> None:
    repo, remote = _github_repo(tmp_path)
    _git(repo, "remote", "set-url", "origin", str(remote))
    marker = tmp_path / "ran"
    _release_assets_command(repo, f"#!/bin/sh\ntouch {marker}\n")
    _tag_locally(repo)
    env, log = _recording_gh(tmp_path)

    result = _ship(repo, "apply", "publish", "--version", "0.2.0", env=env)

    assert result.returncode != 0
    assert "not GitHub" in result.stderr
    assert not marker.exists()
    assert not log.exists()
    assert _remote_has_tag(remote)


WORDPRESS_PLUGIN = """<?php
/**
 * Plugin Name:       Demo
 * Version:           0.1.0
 * Requires PHP:      8.3
 */

// Version: not a header, just a comment further down.
"""


def test_apply_bump_writes_a_wordpress_plugin_header(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "demo.php").write_text(WORDPRESS_PLUGIN, encoding="utf-8")
    (repo / "helpers.php").write_text("<?php\n// Version: 9.9.9\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "Add plugin")

    plan = json.loads(_ship(repo, "plan", "release").stdout)
    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert plan["version_files"] == ["demo.php:0.1.0"]
    assert result.returncode == 0, result.stderr
    assert (repo / "demo.php").read_text(encoding="utf-8") == WORDPRESS_PLUGIN.replace(
        " * Version:           0.1.0", " * Version:           0.2.0"
    )
    assert (repo / "helpers.php").read_text(encoding="utf-8") == (
        "<?php\n// Version: 9.9.9\n"
    )


def test_apply_bump_writes_the_cargo_package_version(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    cargo = (
        "[package]\n"
        'name = "demo"\n'
        'version = "0.1.0"\n'
        "\n"
        "[dependencies.serde]\n"
        'version = "0.1.0"\n'
    )
    (repo / "Cargo.toml").write_text(cargo, encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "Add crate")

    plan = json.loads(_ship(repo, "plan", "release").stdout)
    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert plan["version_files"] == ["Cargo.toml:0.1.0"]
    assert result.returncode == 0, result.stderr
    assert (repo / "Cargo.toml").read_text(encoding="utf-8") == cargo.replace(
        'name = "demo"\nversion = "0.1.0"', 'name = "demo"\nversion = "0.2.0"'
    )


def test_apply_bump_writes_a_version_file(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "Add version file")

    plan = json.loads(_ship(repo, "plan", "release").stdout)
    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert plan["version_files"] == ["VERSION:0.1.0"]
    assert result.returncode == 0, result.stderr
    assert (repo / "VERSION").read_text(encoding="utf-8") == "0.2.0\n"


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
        f" becoming a verb a session may decide to run (ADR-0180). See"
        f" {STANDARD}."
    )
    assert "git push" not in text, (
        f"{body}: this skill commits and stops. Pushing is `/push`, a skill of"
        f" its own that declares this one — a body that pushed as well would"
        f" publish work on a step the user confirmed as a commit, and the body"
        f" is the whole of what the agent executes (ADR-0177). See {STANDARD}."
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
        f" `[Unreleased]` rather than belonging to one consumer (ADR-0177)."
        f" See {STANDARD}."
    )


def test_push_follows_commit_then_pushes() -> None:
    body = REPO_ROOT / "skills" / "code" / "push" / "SKILL.md"
    text = body.read_text(encoding="utf-8")

    assert "disable-model-invocation: true" in text, (
        f"{body}: this skill writes to a remote, so it carries"
        f" `disable-model-invocation: true` and is reached only when the user"
        f" types it. The field is what keeps a verb the user asks for from"
        f" becoming a verb a session may decide to run (ADR-0180). See"
        f" {STANDARD}."
    )
    assert "../commit/SKILL.md" in text, (
        f"{body}: the body follows the commit skill rather than restating its"
        f" steps. That skill is what this one declares in `kntnt.skills`, and a"
        f" second copy of the commit sequence is a copy that drifts from the"
        f" one the suite checks (ADR-0177). See {STANDARD}."
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
        f" for (ADR-0180). See {STANDARD}."
    )
    assert "../push/SKILL.md" in text, (
        f"{body}: the body follows the push skill rather than restating it."
        f" That skill is what this one declares in `kntnt.skills`, and it is"
        f" what carries the commit before the tag is cut (ADR-0177). See"
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
        f" offered (ADR-0176). See {STANDARD}."
    )
