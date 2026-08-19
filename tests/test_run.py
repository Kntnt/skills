"""CLI behaviour of the orchestrate skill's run engine."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from support.fake_binary import fake_binary_on_path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN = REPO_ROOT / "skills" / "code" / "orchestrate" / "scripts" / "run.py"

_GIT_ENV = {
    key: value for key, value in os.environ.items() if not key.startswith("GIT_")
}
_GIT_ENV["GIT_AUTHOR_NAME"] = "Test"
_GIT_ENV["GIT_AUTHOR_EMAIL"] = "test@example.com"
_GIT_ENV["GIT_COMMITTER_NAME"] = "Test"
_GIT_ENV["GIT_COMMITTER_EMAIL"] = "test@example.com"

# The stand-in tracker answers with the tickets filed under the label it was
# asked for, and knows no other way to reach a ticket. A ticket the engine
# comes back with is therefore one it asked for by label, and a query carrying
# no label finds no file and fails the call — which is what makes "a ticket
# without that label never appears" an assertion rather than a hope.
_GH_SCRIPT = """#!/bin/sh
echo "$@" >> "$GH_LOG"
label=""
while [ $# -gt 0 ]; do
  case "$1" in
    --label) label="$2"; shift 2 ;;
    *) shift ;;
  esac
done
cat "$GH_TICKETS/$label.json"
"""


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=_GIT_ENV,
        text=True,
        capture_output=True,
        check=True,
    )


def _init_repo(path: Path, branch: str = "work", initial: str = "main") -> Path:
    """Build a repository defaulting to *initial*, checked out on *branch*."""

    path.mkdir()
    _git(path, "init", "-b", initial)
    _git(path, "config", "user.name", "Test")
    _git(path, "config", "user.email", "test@example.com")
    (path / "README.md").write_text("hello\n", encoding="utf-8")
    _git(path, "add", "README.md")
    _git(path, "commit", "-m", "init")
    if branch != initial:
        _git(path, "checkout", "-b", branch)
    return path


def _ticket(number: int, title: str) -> dict[str, Any]:
    return {
        "number": number,
        "title": title,
        "url": f"https://example.test/issues/{number}",
    }


def _tracker(
    tmp_path: Path, tickets: dict[str, list[dict[str, Any]]]
) -> dict[str, str]:
    """Stand `gh` up over a tracker holding *tickets*, filed by label."""

    directory = tmp_path / "tracker"
    directory.mkdir()
    for label, filed in tickets.items():
        (directory / f"{label}.json").write_text(json.dumps(filed), encoding="utf-8")

    env = fake_binary_on_path(tmp_path, "gh", _GH_SCRIPT)
    return env | {"GH_TICKETS": str(directory), "GH_LOG": str(tmp_path / "gh.log")}


def _engine(
    cwd: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    merged = dict(_GIT_ENV)
    if env:
        merged.update(env)
    return subprocess.run(
        ["uv", "run", str(RUN), *args],
        cwd=cwd,
        env=merged,
        text=True,
        capture_output=True,
        check=False,
    )


def test_plan_returns_every_ready_for_agent_ticket_and_all_of_them_workable(
    tmp_path: Path,
) -> None:
    """No edges are read yet, so a set with no edges is workable in full."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert plan["reason"] is None
    assert [entry["number"] for entry in plan["tickets"]] == [9, 10]
    assert plan["workable"] == [9, 10]


def test_plan_never_returns_a_ticket_that_does_not_carry_the_label(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [_ticket(9, "the skeleton")],
            "needs-triage": [_ticket(41, "unfinished thinking")],
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [entry["number"] for entry in plan["tickets"]] == [9]
    assert "unfinished thinking" not in result.stdout


def test_plan_refuses_on_the_default_branch_and_still_shows_the_scope(
    tmp_path: Path,
) -> None:
    """A dry run is read off a refused plan, so the scope has to survive it."""

    repo = _init_repo(tmp_path / "proj", branch="main")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert "main" in plan["reason"]
    assert plan["branch"] == "main"
    assert plan["default_branch"] == "main"
    assert [entry["number"] for entry in plan["tickets"]] == [9]


def test_plan_with_no_labelled_ticket_stops_rather_than_returning_work(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []})

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert "ready-for-agent" in plan["reason"]
    assert plan["tickets"] == []
    assert plan["workable"] == []


def test_record_emits_the_outcome_and_the_commit_it_was_given(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")

    result = _engine(
        repo, "record", "--ticket", "9", "--outcome", "done", "--commit", "abc1234"
    )

    assert result.returncode == 0, result.stderr
    recorded = json.loads(result.stdout)
    assert recorded["ticket"] == 9
    assert recorded["outcome"] == "done"
    assert recorded["commit"] == "abc1234"


def test_record_refuses_an_outcome_it_does_not_know(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")

    result = _engine(repo, "record", "--ticket", "9", "--outcome", "probably-fine")

    assert result.returncode != 0
    assert not result.stdout


def test_report_accounts_for_the_tickets_in_scope(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert [entry["number"] for entry in report["tickets"]] == [9, 10]
    assert report["recorded"] == []


def test_every_verb_accepts_yes(tmp_path: Path) -> None:
    """ADR-0029: the flag reaches every verb, including those that ask nothing."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    for args in (
        ("plan", "--yes"),
        ("record", "--ticket", "9", "--outcome", "done", "--yes"),
        ("report", "--yes"),
    ):
        result = _engine(repo, *args, env=env)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "unrecognized arguments" not in result.stderr


def test_plan_under_a_dry_run_shows_the_scope_and_starts_nothing(
    tmp_path: Path,
) -> None:
    """The flag is the engine's decision, not the agent's reading of it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--dry-run", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["dry_run"] is True
    assert plan["ready"] is False
    assert "dry run" in plan["reason"]
    assert [entry["number"] for entry in plan["tickets"]] == [9]


def test_plan_refuses_when_it_cannot_tell_which_branch_is_the_default(
    tmp_path: Path,
) -> None:
    """A repository naming its default neither main nor master, and no remote
    to ask, must be told so rather than have the branch in hand called the
    default and refused under a reason that is not true."""

    repo = _init_repo(tmp_path / "proj", initial="trunk", branch="work")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})
    _git(repo, "branch", "-D", "trunk")

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["default_branch"] is None
    assert "cannot tell which branch is the default" in plan["reason"]


def test_plan_refuses_a_ticket_list_that_may_have_been_truncated(
    tmp_path: Path,
) -> None:
    """A full page is no proof of a full scope, and a scope silently missing
    tickets is a run that leaves work behind without saying so. The page size
    is the engine's, and stated here as the contract rather than imported."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(number, "one of many") for number in range(200)]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 1
    assert "200" in result.stderr
