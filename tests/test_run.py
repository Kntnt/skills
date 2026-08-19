"""CLI behaviour of the orchestrate skill's run engine."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from support.fake_binary import fake_binary_on_path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN = REPO_ROOT / "skills" / "code" / "orchestrate" / "scripts" / "run.py"

# How long any one invocation is given. Generous enough that a cold `uv` never
# trips it, and short enough that a graph the engine walks in circles is a
# failure rather than a suite that never ends.
ENGINE_TIMEOUT = 120

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
# without that label never appears" an assertion rather than a hope. One
# ticket is reachable by number as well, because a blocking edge read out of a
# body names a ticket the scope need not contain; a number the tracker was
# never given fails the call, as a deleted ticket does.
_GH_SCRIPT = """#!/bin/sh
echo "$@" >> "$GH_LOG"
case "$2" in
  view) cat "$GH_ISSUES/$3.json"; exit $? ;;
  edit|close|comment) exit 0 ;;
esac
label=""
while [ $# -gt 0 ]; do
  case "$1" in
    --label) label="$2"; shift 2 ;;
    *) shift ;;
  esac
done
cat "$GH_TICKETS/$label.json"
"""

# A stand-in that logs what git was asked to do and then lets the real git do
# it. Everything the engine reads from the repository has to stay true, so
# this observes rather than substitutes.
_GIT_SPY = """#!/bin/sh
echo "$@" >> "$SPY_LOG"
exec {real} "$@"
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


def _ticket(
    number: int,
    title: str,
    *,
    blocked_by: list[tuple[int, str]] | None = None,
    body: str = "",
    parent: int | None = None,
    claimed_by: list[str] | None = None,
) -> dict[str, Any]:
    """Build a ticket as the tracker answers it, with *blocked_by* as edges.

    Each edge is a ticket number and the state the tracker reports it in, which
    is how the native relation arrives: the blocker's own state travels with
    the edge, so a closed blocker needs no second question. *claimed_by* is the
    logins the tracker has the ticket assigned to, which is how a ticket
    another session is already working announces itself.
    """

    edges = blocked_by or []
    return {
        "number": number,
        "title": title,
        "url": f"https://example.test/issues/{number}",
        "body": body,
        "parent": (
            None
            if parent is None
            else {
                "number": parent,
                "title": "the spec",
                "url": f"https://example.test/issues/{parent}",
                "state": "OPEN",
            }
        ),
        "assignees": [{"login": login} for login in claimed_by or []],
        "blockedBy": {
            "nodes": [{"number": blocker, "state": state} for blocker, state in edges],
            "totalCount": len(edges),
        },
    }


def _tracker(
    tmp_path: Path,
    tickets: dict[str, list[dict[str, Any]]],
    issues: dict[int, dict[str, Any]] | None = None,
) -> dict[str, str]:
    """Stand `gh` up over a tracker holding *tickets*, filed by label.

    *issues* names the tickets reachable by number rather than by label — the
    ones a blocking edge read out of a body can point at from outside the
    scope, and the ones a verb that works a single ticket asks about by name.
    Each is a partial ticket laid over an open, unlabelled, unclaimed one, so
    a test states only the part it is about. A number that is not there is a
    ticket the tracker cannot answer for.
    """

    directory = tmp_path / "tracker"
    directory.mkdir()
    for label, filed in tickets.items():
        (directory / f"{label}.json").write_text(json.dumps(filed), encoding="utf-8")

    folder = tmp_path / "issues"
    folder.mkdir()
    for number, issue in (issues or {}).items():
        default = {"number": number, "state": "OPEN", "labels": [], "assignees": []}
        (folder / f"{number}.json").write_text(
            json.dumps(default | issue), encoding="utf-8"
        )

    env = fake_binary_on_path(tmp_path, "gh", _GH_SCRIPT)
    return env | {
        "GH_TICKETS": str(directory),
        "GH_ISSUES": str(folder),
        "GH_LOG": str(tmp_path / "gh.log"),
    }


def _ready(number: int, **fields: Any) -> dict[str, Any]:
    """Build the answer `gh issue view` gives for a workable ticket."""

    return {"labels": [{"name": "ready-for-agent"}]} | fields


def _gh_calls(env: dict[str, str]) -> str:
    """Return what the tracker was asked to do, one call per line.

    A verb that refuses before touching the tracker leaves no log at all, which
    is the same answer as an empty one and is read as such.
    """

    log = Path(env["GH_LOG"])
    return log.read_text(encoding="utf-8") if log.exists() else ""


def _git_spy(tmp_path: Path) -> dict[str, str]:
    """Log every git command an engine runs, and let it run for real."""

    real = shutil.which("git")
    assert real, "git is required to run this suite"
    env = fake_binary_on_path(tmp_path, "git", _GIT_SPY.format(real=real))
    return env | {"SPY_LOG": str(tmp_path / "git.log")}


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
        timeout=ENGINE_TIMEOUT,
    )


def test_plan_returns_every_ready_for_agent_ticket_and_all_of_them_workable(
    tmp_path: Path,
) -> None:
    """A set with no edge has no ticket waiting on another, so all of it is
    workable at once."""

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
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton")]},
        issues={9: _ready(9)},
    )
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    for args in (
        ("plan", "--yes"),
        ("claim", "--ticket", "9", "--yes"),
        ("record", "--ticket", "9", "--outcome", "done", "--commit", head, "--yes"),
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


def test_plan_separates_the_workable_ticket_from_the_one_that_waits_on_it(
    tmp_path: Path,
) -> None:
    """The edge is what the run must never get wrong: 10 waits for 9."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [9]
    assert plan["blocked"] == [10]
    assert plan["waves"] == [[9], [10]]
    assert plan["never_workable"] == []


def test_plan_offers_every_ticket_whose_blockers_are_met_in_the_same_wave(
    tmp_path: Path,
) -> None:
    """A run is not slower than the graph requires: two roots start together."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph"),
                _ticket(11, "the build", blocked_by=[(9, "OPEN"), (10, "OPEN")]),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [9, 10]
    assert plan["waves"] == [[9, 10], [11]]


def test_plan_does_not_let_a_closed_blocker_block(tmp_path: Path) -> None:
    """The work the edge names already exists, so nothing is waited for."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", blocked_by=[(9, "CLOSED")])]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [10]
    assert plan["blocked"] == []
    assert plan["tickets"][0]["blocked_by"] == []


def test_plan_reads_a_blocked_by_line_where_the_relation_carries_nothing(
    tmp_path: Path,
) -> None:
    """The breakdown writes the edge in the body where the tracker has no
    relation to write it in, and it means the same thing."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph", body="## Blocked by\n\n- #9\n"),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [9]
    assert plan["blocked"] == [10]
    assert plan["tickets"][1]["blocked_by"] == [9]


def test_plan_does_not_let_a_closed_ticket_named_in_the_body_block(
    tmp_path: Path,
) -> None:
    """A body edge names a ticket the scope need not hold, so its state is
    asked for rather than assumed from its absence."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", body="Blocked by: #9")]},
        issues={9: {"state": "CLOSED"}},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [10]


def test_plan_keeps_a_ticket_blocked_by_open_work_outside_the_scope_blocked(
    tmp_path: Path,
) -> None:
    """The blocker is open and carries no label, so the run will never build
    it — calling the ticket workable would build it before its work exists."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", body="Blocked by: #9")]},
        issues={9: {"state": "OPEN"}},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == []
    assert plan["blocked"] == [10]
    assert plan["never_workable"] == [10]


def test_plan_reads_the_body_only_where_the_relation_carries_nothing(
    tmp_path: Path,
) -> None:
    """The relation is the tracker's own answer; a body line is the fallback,
    never a second source added to it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(
                    10,
                    "the graph",
                    blocked_by=[(8, "CLOSED")],
                    body="Blocked by: #9",
                ),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [9, 10]


def test_plan_refuses_a_body_edge_naming_a_ticket_the_tracker_cannot_answer_for(
    tmp_path: Path,
) -> None:
    """An edge whose state nothing can settle makes the whole graph a guess."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", body="Blocked by: #404")]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 1
    assert "404" in result.stderr


def test_plan_refuses_a_body_edge_written_in_another_trackers_terms(
    tmp_path: Path,
) -> None:
    """A run reads one tracker, so `owner/repo#9` is a number it cannot place.
    Passing over it would promote a blocked ticket to the frontier in silence,
    which is the one way this reasoning must never be wrong. The refusal names
    the ticket carrying the reference, so the fix needs no search."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(10, "the graph", body="Blocked by: Kntnt/skills#9")
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 1
    assert "Kntnt/skills#9" in result.stderr
    assert "#10" in result.stderr


def test_plan_with_no_workable_ticket_terminates_rather_than_looping(
    tmp_path: Path,
) -> None:
    """Two tickets waiting on each other resolve no wave at all. The run says
    so and stops; a frontier walked until it empties would never end."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", blocked_by=[(10, "OPEN")]),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["workable"] == []
    assert plan["waves"] == []
    assert plan["blocked"] == [9, 10]
    assert plan["never_workable"] == [9, 10]
    assert "no ticket is workable" in plan["reason"]


def test_plan_under_a_dry_run_shows_the_wave_plan(tmp_path: Path) -> None:
    """The shape of the night is what the dry run is read for."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
            ]
        },
    )

    result = _engine(repo, "plan", "--dry-run", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["dry_run"] is True
    assert plan["waves"] == [[9], [10]]


def test_plan_does_not_offer_a_ticket_another_session_has_claimed(
    tmp_path: Path,
) -> None:
    """A claim is what stops two sessions building the same ticket twice, so a
    claimed ticket leaves the frontier and is named as taken rather than
    dropped."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", claimed_by=["someone"]),
                _ticket(10, "the graph"),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [10]
    assert plan["claimed"] == [9]


def test_plan_stops_where_every_workable_ticket_is_already_claimed(
    tmp_path: Path,
) -> None:
    """Nothing is left for this run to start, and the reason says which."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton", claimed_by=["someone"])]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["workable"] == []
    assert plan["claimed"] == [9]
    assert "claimed" in plan["reason"]


def test_plan_carries_each_tickets_body_and_parent_for_the_brief(
    tmp_path: Path,
) -> None:
    """The brief carries the ticket's fetched body rather than a summary, and
    names the spec whose testing decisions are read before any test."""

    repo = _init_repo(tmp_path / "proj")
    written = "## What to build\n\nThe thing itself, in the words it was filed in.\n"
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", body=written, parent=6)]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["tickets"][0]["body"] == written
    assert plan["tickets"][0]["parent"] == 6


def test_plan_reads_the_parent_from_the_body_where_the_relation_carries_none(
    tmp_path: Path,
) -> None:
    """The breakdown writes the parent in the body where the tracker has no
    relation to write it in, exactly as it writes a blocking edge there."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", body="## Parent\n\n#6\n")]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["tickets"][0]["parent"] == 6


def test_plan_names_the_model_the_building_subagents_run_on(tmp_path: Path) -> None:
    """Mechanical work runs cheaper than judgement work, and the plan is where
    the run says which model builds."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    named = _engine(repo, "plan", "--model", "a-cheaper-model", env=env)
    bare = _engine(repo, "plan", env=env)

    assert named.returncode == 0, named.stderr
    assert json.loads(named.stdout)["model"] == "a-cheaper-model"
    assert json.loads(bare.stdout)["model"] is None


def test_claim_takes_the_ticket_on_the_tracker_before_any_work_starts(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})

    result = _engine(repo, "claim", "--ticket", "9", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["claimed"] is True
    calls = _gh_calls(env)
    assert "issue edit 9 --add-assignee @me" in calls


def test_claim_refuses_a_ticket_another_session_already_has(tmp_path: Path) -> None:
    """The second session started in parallel skips it rather than building it
    a second time, so nothing is written to the tracker at all."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        issues={9: _ready(9, assignees=[{"login": "someone"}])},
    )

    result = _engine(repo, "claim", "--ticket", "9", env=env)

    assert result.returncode == 2
    claim = json.loads(result.stdout)
    assert claim["claimed"] is False
    assert "someone" in claim["reason"]
    assert "--add-assignee" not in _gh_calls(env)


def test_claim_refuses_a_ticket_whose_thinking_is_not_finished(tmp_path: Path) -> None:
    """A ticket without the label is never built, and the claim is the last
    place that can still say so."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        issues={9: {"labels": [{"name": "needs-triage"}]}},
    )

    result = _engine(repo, "claim", "--ticket", "9", env=env)

    assert result.returncode == 2
    claim = json.loads(result.stdout)
    assert claim["claimed"] is False
    assert "ready-for-agent" in claim["reason"]
    assert "--add-assignee" not in _gh_calls(env)


def test_record_closes_a_done_ticket_and_stores_the_commit_that_carries_it(
    tmp_path: Path,
) -> None:
    """Verification passed, so the tracker is brought level with reality — and
    the commit is stored with the outcome, because the outcome without it says
    nothing about where the work is."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    result = _engine(
        repo, "record", "--ticket", "9", "--outcome", "done", "--commit", head, env=env
    )

    assert result.returncode == 0, result.stderr
    recorded = json.loads(result.stdout)
    assert recorded["ticket"] == 9
    assert recorded["outcome"] == "done"
    assert recorded["commit"] == head
    assert recorded["closed"] is True
    calls = _gh_calls(env)
    assert "issue close 9" in calls
    assert f"outcome=done commit={head}" in calls


def test_record_leaves_a_failed_ticket_open_and_does_not_retry_it(
    tmp_path: Path,
) -> None:
    """The conditions of a rerun would be identical and so would the outcome,
    so the failure is written down and the ticket stays open and taken."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})

    result = _engine(repo, "record", "--ticket", "9", "--outcome", "failed", env=env)

    assert result.returncode == 0, result.stderr
    recorded = json.loads(result.stdout)
    assert recorded["outcome"] == "failed"
    assert recorded["closed"] is False
    calls = _gh_calls(env)
    assert "issue close" not in calls
    assert "outcome=failed" in calls


def test_record_refuses_a_done_outcome_that_names_no_commit(tmp_path: Path) -> None:
    """Done without a commit is a ticket closed on nothing."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})

    result = _engine(repo, "record", "--ticket", "9", "--outcome", "done", env=env)

    assert result.returncode == 1
    assert not result.stdout
    assert "commit" in result.stderr
    assert "issue close" not in _gh_calls(env)


def test_record_refuses_a_commit_this_repository_does_not_have(tmp_path: Path) -> None:
    """A commit nothing can resolve is a report nobody can check."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})

    result = _engine(
        repo,
        "record",
        "--ticket",
        "9",
        "--outcome",
        "done",
        "--commit",
        "0" * 40,
        env=env,
    )

    assert result.returncode == 1
    assert "0" * 40 in result.stderr
    assert "issue close" not in _gh_calls(env)


def test_record_refuses_a_ticket_the_tracker_does_not_know(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []})
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    result = _engine(
        repo,
        "record",
        "--ticket",
        "404",
        "--outcome",
        "done",
        "--commit",
        head,
        env=env,
    )

    assert result.returncode == 1
    assert "404" in result.stderr


def test_no_verb_pushes_or_makes_a_worktree(tmp_path: Path) -> None:
    """Nothing leaves the machine while the developer is asleep, and a ceiling
    of one works the branch they were on rather than a worktree beside it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton")]},
        issues={9: _ready(9)},
    ) | _git_spy(tmp_path)
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    for args in (
        ("plan",),
        ("claim", "--ticket", "9"),
        ("record", "--ticket", "9", "--outcome", "done", "--commit", head),
        ("report",),
    ):
        assert _engine(repo, *args, env=env).returncode == 0, args

    ran = Path(env["SPY_LOG"]).read_text(encoding="utf-8")
    assert "push" not in ran
    assert "worktree" not in ran


def test_plan_refuses_a_body_naming_more_than_one_parent(tmp_path: Path) -> None:
    """A ticket has one parent spec. Reading whichever came first would send a
    builder off to read the wrong testing decisions without saying so."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph", body="Parent: #6, #7")]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 1
    assert "#6" in result.stderr and "#7" in result.stderr
