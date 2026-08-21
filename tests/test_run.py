"""CLI behaviour of the orchestrate skill's run engine."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from support.fake_binary import fake_binary_on_path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN = REPO_ROOT / "skills" / "code" / "orchestrate" / "scripts" / "run.py"


def _run() -> ModuleType:
    """Import the run engine as a module.

    Almost everything here drives the engine as the skill does, through its
    command line. Registry detection is the exception: what it has to answer
    is a fact about this repository, and no invocation in a repository built
    for a test can ask that question of the one the suite runs in.
    """

    # The loader API answers with optionals, so both are narrowed before use:
    # a missing script is a broken checkout and has to say which file.
    spec = importlib.util.spec_from_file_location("kntnt_run", RUN)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import the run engine from {RUN}")

    # Execute the script under its own module object and hand that back. It is
    # registered first because the engine's dataclasses resolve their own
    # annotations through the module they were declared in.
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# How long any one invocation is given. Generous enough that a cold `uv` never
# trips it, and short enough that a graph the engine walks in circles is a
# failure rather than a suite that never ends.
ENGINE_TIMEOUT = 120

# The five lists a report accounts for its scope with. Named once, because
# what a test about the account asserts is a ticket's place across all five —
# and a sixth list nobody read would be exactly the silence they guard against.
_ACCOUNT = ("done", "failed", "conflicted", "stranded", "never_on_frontier")

_GIT_ENV = {
    key: value for key, value in os.environ.items() if not key.startswith("GIT_")
}
_GIT_ENV["GIT_AUTHOR_NAME"] = "Test"
_GIT_ENV["GIT_AUTHOR_EMAIL"] = "test@example.com"
_GIT_ENV["GIT_COMMITTER_NAME"] = "Test"
_GIT_ENV["GIT_COMMITTER_EMAIL"] = "test@example.com"

# The stand-in tracker answers with the tickets filed under the label and the
# state it was asked for, and knows no other way to reach a ticket. A ticket
# the engine comes back with is therefore one it asked for by label, and a
# query carrying no label finds no file and fails the call — which is what
# makes "a ticket without that label never appears" an assertion rather than a
# hope. State is part of that key because the open scope and the tickets a run
# closed are two different questions asked of the same label. One ticket is
# reachable by number as well, because a blocking edge read out of a body
# names a ticket the scope need not contain; a number the tracker was never
# given fails the call, as a deleted ticket does. It also answers who the run
# is authenticated as, which is how a claim of this developer's own is told
# from another session's; a tracker given no login cannot say.
_GH_SCRIPT = """#!/bin/sh
echo "$@" >> "$GH_LOG"
if [ "$1" = "api" ]; then
  [ -n "$GH_LOGIN" ] || exit 1
  printf '%s\\n' "$GH_LOGIN"
  exit 0
fi
case "$2" in
  view) cat "$GH_ISSUES/$3.json"; exit $? ;;
  edit|close|comment) exit 0 ;;
esac
label=""
state="open"
while [ $# -gt 0 ]; do
  case "$1" in
    --label) label="$2"; shift 2 ;;
    --state) state="$2"; shift 2 ;;
    *) shift ;;
  esac
done
cat "$GH_TICKETS/$label.$state.json"
"""

# The marker `record` writes an outcome in, stated here as the contract rather
# than imported: what one verb writes on a ticket is what the next run reads
# back off it, and a test that built the marker from the engine's own constant
# would pass on both halves being wrong together.
MARKER = "kntnt-orchestrate"

# What the run calls the state it keeps in the session's scratch directory,
# and the directory of its own it keeps it in, stated here for the same
# reason: a test that asked the engine where it wrote would be asking the
# thing under test to grade itself.
STATE_FILE = "kntnt-orchestrate.json"
STATE_HOME = "kntnt-orchestrate"

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


def _recorded(
    outcome: str, commit: str | None = None, collided_with: list[int] | None = None
) -> dict[str, Any]:
    """Build the comment a run leaves on a ticket when it records *outcome*.

    *collided_with* is the other half of a conflicted outcome: the tickets whose
    work this one collided with, which is the pair that names the blocking edge
    the ticket breakdown was missing.
    """

    named = f" commit={commit}" if commit else ""
    against = (
        f" collided-with={','.join(str(number) for number in collided_with)}"
        if collided_with
        else ""
    )
    return {
        "body": f"<!-- {MARKER} outcome={outcome}{named}{against} --> what happened"
    }


def _wrote(env: dict[str, str], number: int) -> str:
    """Return the last note the run left on ticket *number*, as the tracker got
    it.

    Read back off the call rather than built here, so a test that feeds a note
    to the verb that reads it is feeding it the note the verb that writes it
    actually wrote.
    """

    prefix = f"issue comment {number} --body "
    written = [
        line.removeprefix(prefix)
        for line in _gh_calls(env).splitlines()
        if line.startswith(prefix)
    ]
    return written[-1]


def _remark(author: str, written: str, body: str) -> dict[str, Any]:
    """Build a comment on a ticket as the tracker answers for it.

    The half of a thread a person wrote: attributed and dated, which is what
    tells a builder what came after what.
    """

    return {"author": {"login": author}, "createdAt": written, "body": body}


def _ticket(
    number: int,
    title: str,
    *,
    blocked_by: list[tuple[int, str]] | None = None,
    body: str = "",
    parent: int | None = None,
    claimed_by: list[str] | None = None,
    comments: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a ticket as the tracker answers it, with *blocked_by* as edges.

    Each edge is a ticket number and the state the tracker reports it in, which
    is how the native relation arrives: the blocker's own state travels with
    the edge, so a closed blocker needs no second question. *claimed_by* is the
    logins the tracker has the ticket assigned to, which is how a ticket
    another session is already working announces itself, and *comments* is
    where an outcome a run recorded is read back from.
    """

    edges = blocked_by or []
    return {
        "comments": comments or [],
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
    closed: list[dict[str, Any]] | None = None,
    login: str = "me",
) -> dict[str, str]:
    """Stand `gh` up over a tracker holding *tickets*, filed by label.

    *issues* names the tickets reachable by number rather than by label — the
    ones a blocking edge read out of a body can point at from outside the
    scope, the ones a verb that works a single ticket asks about by name, and
    the ones a run is aimed at. Each is a partial ticket laid over an open,
    unlabelled, unclaimed one that the tracker files no children under, so a
    test states only the part it is about. A number that is not there is a
    ticket the tracker cannot answer for.

    *closed* holds the tickets the tracker answers for the ready label in its
    closed state, which is where a ticket a run closed as done has gone.

    *login* is who the tracker says the run is authenticated as, so a claim
    holding that login is this developer's own and one holding another is
    somebody else's. Empty is a tracker that cannot say.
    """

    directory = tmp_path / "tracker"
    directory.mkdir()
    for label, filed in tickets.items():
        (directory / f"{label}.open.json").write_text(
            json.dumps(filed), encoding="utf-8"
        )
        (directory / f"{label}.closed.json").write_text(
            json.dumps(closed if label == "ready-for-agent" and closed else []),
            encoding="utf-8",
        )

    folder = tmp_path / "issues"
    folder.mkdir()
    for number, issue in (issues or {}).items():
        default = {
            "number": number,
            "state": "OPEN",
            "labels": [],
            "assignees": [],
            "comments": [],
            "subIssues": {"nodes": [], "totalCount": 0},
        }
        (folder / f"{number}.json").write_text(
            json.dumps(default | issue), encoding="utf-8"
        )

    env = fake_binary_on_path(tmp_path, "gh", _GH_SCRIPT)
    return env | {
        "GH_TICKETS": str(directory),
        "GH_ISSUES": str(folder),
        "GH_LOG": str(tmp_path / "gh.log"),
        "GH_LOGIN": login,
    }


def _refile(
    env: dict[str, str], state: str, tickets: list[dict[str, Any]]
) -> dict[str, str]:
    """Refile the ready label's *state* half with *tickets*, and return *env*.

    The tracker as it stands after a run has written to it. The stand-in `gh`
    accepts a write and changes nothing, so a test that goes on to read the
    tracker back says here what that write left behind.
    """

    directory = Path(env["GH_TICKETS"])
    (directory / f"ready-for-agent.{state}.json").write_text(
        json.dumps(tickets), encoding="utf-8"
    )
    return env


def _refile_issue(
    env: dict[str, str], number: int, issue: dict[str, Any]
) -> dict[str, str]:
    """Lay *issue* over the ticket the tracker answers for by number.

    The stand-in `gh` accepts a write and changes nothing, so a test that goes
    on to read a ticket back says here what that write left on it.
    """

    path = Path(env["GH_ISSUES"]) / f"{number}.json"
    stored = json.loads(path.read_text(encoding="utf-8"))
    path.write_text(json.dumps(stored | issue), encoding="utf-8")
    return env


def _ready(number: int, **fields: Any) -> dict[str, Any]:
    """Build the answer `gh issue view` gives for a workable ticket."""

    return {"labels": [{"name": "ready-for-agent"}]} | fields


def _children(*numbers: int) -> dict[str, Any]:
    """Build the sub-issue relation the tracker files a spec's children under.

    This is the relation a `Parent` line in a body stands in for, and it is
    what tells a reference naming a spec from one naming a ticket.
    """

    nodes = [{"number": number, "state": "OPEN"} for number in numbers]
    return {"subIssues": {"nodes": nodes, "totalCount": len(nodes)}}


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


def test_plan_works_the_default_branch_like_any_other_branch(
    tmp_path: Path,
) -> None:
    """A run works the branch the developer left it on, and which branch that
    is is not the Skill's to second-guess (ADR-0064)."""

    repo = _init_repo(tmp_path / "proj", branch="main")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert plan["reason"] is None
    assert plan["branch"] == "main"
    assert plan["default_branch"] == "main"
    assert [entry["number"] for entry in plan["tickets"]] == [9]
    assert plan["workable"] == [9]


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
    assert report["never_on_frontier"] == [9, 10]


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
        ("park", "--ticket", "9", "--yes"),
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


def test_plan_works_a_repository_that_cannot_name_its_default_branch(
    tmp_path: Path,
) -> None:
    """Nothing is gated on which branch is the default any more, so a
    repository naming its default neither main nor master, and with no remote
    to ask, is worked rather than refused — and the plan still says that
    nothing could tell."""

    repo = _init_repo(tmp_path / "proj", initial="trunk", branch="work")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})
    _git(repo, "branch", "-D", "trunk")

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert plan["reason"] is None
    assert plan["default_branch"] is None
    assert [entry["number"] for entry in plan["tickets"]] == [9]


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
    assert result.stderr.startswith("error:")


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


def test_plan_carries_what_has_been_said_on_a_ticket_since_it_was_filed(
    tmp_path: Path,
) -> None:
    """A ticket is a thread and the body is only its first post. Triage answers
    the body's open questions in a comment, and the brief is filled in from the
    plan — so the plan is where the rest of the thread has to arrive, in filing
    order, each entry attributed and dated."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(
                    10,
                    "the graph",
                    body="## What triage must decide\n\nWhich seam it goes behind.\n",
                    comments=[
                        _remark("maintainer", "2026-01-02T09:00:00Z", "The engine's."),
                        _remark(
                            "reviewer", "2026-01-03T11:30:00Z", "Agreed, and\ntested."
                        ),
                    ],
                )
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["tickets"][0]["thread"] == [
        {
            "author": "maintainer",
            "created_at": "2026-01-02T09:00:00Z",
            "body": "The engine's.",
        },
        {
            "author": "reviewer",
            "created_at": "2026-01-03T11:30:00Z",
            "body": "Agreed, and\ntested.",
        },
    ]


def test_plan_leaves_the_runs_own_notes_out_of_a_tickets_thread(
    tmp_path: Path,
) -> None:
    """An outcome marker, a rebuild note, and an amend note are the engine
    talking to its next self, and a builder that reads them learns only that
    this ticket has been here before. They are left out, what a person wrote
    stays, and every reading the engine makes of a comment answers exactly as
    it did."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(
                    10,
                    "the graph",
                    comments=[
                        _remark(
                            "maintainer", "2026-01-02T09:00:00Z", "Behind the seam."
                        ),
                        {"body": f"<!-- {MARKER} rebuild --> built once more"},
                        {"body": f"<!-- {MARKER} amend --> amended once"},
                        _recorded("failed"),
                    ],
                )
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert [entry["body"] for entry in plan["tickets"][0]["thread"]] == [
        "Behind the seam."
    ]
    assert plan["tickets"][0]["outcome"] == "failed"


def test_plan_carries_an_empty_thread_for_a_ticket_nobody_has_written_on(
    tmp_path: Path,
) -> None:
    """A ticket whose thread is empty is briefed exactly as it was briefed
    before there was a thread to brief from."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(10, "the graph")]})

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["tickets"][0]["thread"] == []


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
    assert result.stderr.startswith("error:")


def test_a_run_at_a_ceiling_of_one_pushes_nothing_and_makes_no_worktree(
    tmp_path: Path,
) -> None:
    """Nothing leaves the machine while the developer is asleep, and a ceiling
    of one works the branch they were on rather than a working tree beside it:
    the run reads what git has open, and opens none of its own."""

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
        ("park", "--ticket", "9"),
        ("record", "--ticket", "9", "--outcome", "done", "--commit", head),
        ("report",),
    ):
        assert _engine(repo, *args, env=env).returncode == 0, args

    ran = [
        line.split()
        for line in Path(env["SPY_LOG"]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert "push" not in [called[0] for called in ran]
    assert ["worktree", "add"] not in [called[:2] for called in ran]


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


def test_plan_does_not_offer_a_ticket_whose_outcome_is_already_recorded(
    tmp_path: Path,
) -> None:
    """A failure is written down and never retried, so the next plan must not
    hand the same ticket back — the conditions of a rerun would be identical
    and so would the outcome. It stays in the account rather than vanishing."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("failed")]),
                _ticket(10, "the graph"),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [10]
    assert plan["recorded"] == [9]
    assert plan["tickets"][0]["outcome"] == "failed"
    assert plan["tickets"][1]["outcome"] is None


def test_plan_carries_the_commit_a_recorded_outcome_named(tmp_path: Path) -> None:
    """An outcome without the commit it was recorded on says nothing about
    where the work is."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("conflicted", head)]),
                _ticket(10, "the graph"),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["tickets"][0]["outcome"] == "conflicted"
    assert plan["tickets"][0]["commit"] == head


def test_plan_strands_the_tickets_waiting_on_a_failure_rather_than_dropping_them(
    tmp_path: Path,
) -> None:
    """This is the outcome a naive loop drops without saying so: 10 waits on a
    ticket that failed and 11 waits on 10, so neither is workable and neither
    may go missing from the account."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("failed")]),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
                _ticket(11, "the build", blocked_by=[(10, "OPEN")]),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["workable"] == []
    assert plan["recorded"] == [9]
    assert plan["stranded"] == [10, 11]
    assert plan["never_workable"] == []
    assert [entry["number"] for entry in plan["tickets"]] == [9, 10, 11]


def test_plan_leaves_a_ticket_the_failure_does_not_reach_workable(
    tmp_path: Path,
) -> None:
    """Stranding follows the edges and stops there: an unrelated ticket is
    still the run's to start."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("failed")]),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
                _ticket(11, "the unrelated one"),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["workable"] == [11]
    assert plan["stranded"] == [10]


def test_plan_reads_back_the_outcome_that_record_wrote(tmp_path: Path) -> None:
    """The two halves meet here: what `record` writes on a ticket is what the
    next `plan` reads off it. A test that built the marker for itself would
    pass on both halves being wrong together."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})
    assert (
        _engine(repo, "record", "--ticket", "9", "--outcome", "failed", env=env)
    ).returncode == 0

    # Take the note the tracker was asked to write, and put it back on the
    # ticket as the comment the tracker would now be answering with.
    written = [
        line for line in _gh_calls(env).splitlines() if line.startswith("issue comment")
    ]
    note = written[0].split("--body ", 1)[1]
    second = tmp_path / "second"
    second.mkdir()
    env = _tracker(
        second,
        {"ready-for-agent": [_ticket(9, "the skeleton", comments=[{"body": note}])]},
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["tickets"][0]["outcome"] == "failed"
    assert plan["workable"] == []


def test_report_accounts_for_every_ticket_in_scope_exactly_once(
    tmp_path: Path,
) -> None:
    """The five outcomes are the whole account: a ticket the run silently drops
    is one the developer will not know to pick up."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(10, "the failure", comments=[_recorded("failed")]),
                _ticket(11, "behind it", blocked_by=[(10, "OPEN")]),
                _ticket(12, "the collision", comments=[_recorded("conflicted", head)]),
                _ticket(13, "never reached", claimed_by=["someone"]),
            ]
        },
        closed=[_ticket(9, "the skeleton", comments=[_recorded("done", head)])],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["done"] == [9]
    assert report["failed"] == [10]
    assert report["conflicted"] == [12]
    assert report["stranded"] == [11]
    assert report["never_on_frontier"] == [13]

    # Every ticket in scope, once and once only, across the five.
    accounted = [number for outcome in _ACCOUNT for number in report[outcome]]
    in_scope = [entry["number"] for entry in report["tickets"]]
    assert sorted(accounted) == in_scope == [9, 10, 11, 12, 13]
    assert len(set(accounted)) == len(accounted)


def test_report_names_the_commit_a_closed_ticket_was_recorded_on(
    tmp_path: Path,
) -> None:
    """A done ticket has left the open scope, so the report finds it among the
    tickets this machine's runs closed and reports the commit with it."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        closed=[_ticket(9, "the skeleton", comments=[_recorded("done", head)])],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["done"] == [9]
    assert report["tickets"][0]["commit"] == head
    assert "--assignee @me" in _gh_calls(env)


def test_report_leaves_out_a_closed_ticket_no_run_recorded(tmp_path: Path) -> None:
    """A ticket somebody closed by hand carries no marker of this engine's and
    was never this run's to account for, so it is in none of the five lists —
    accounting for it under any of them would be a report nobody can check."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        closed=[_ticket(9, "closed by a person")],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["tickets"] == []
    assert all(report[outcome] == [] for outcome in _ACCOUNT)


def test_report_accounts_for_a_ticket_recorded_failed_and_later_closed(
    tmp_path: Path,
) -> None:
    """A ticket this run recorded failed, and a person or a commit trailer then
    closed, is still this run's: the run claimed it, built it, and wrote an
    outcome on it. It is reported under the outcome that stands on it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        closed=[_ticket(9, "the failure", comments=[_recorded("failed")])],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["failed"] == [9]
    assert [entry["number"] for entry in report["tickets"]] == [9]
    assert [number for outcome in _ACCOUNT for number in report[outcome]] == [9]


def test_report_reads_a_closed_tickets_outcome_as_it_now_stands(
    tmp_path: Path,
) -> None:
    """A ticket recorded failed and then recorded done is a done ticket, the
    last marker being the outcome as it stands — and it is in one of the five
    lists rather than in two of them."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        closed=[
            _ticket(
                9,
                "the skeleton",
                comments=[_recorded("failed"), _recorded("done", head)],
            )
        ],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["done"] == [9]
    assert [entry["number"] for entry in report["tickets"]] == [9]
    assert [number for outcome in _ACCOUNT for number in report[outcome]] == [9]


def test_plan_strands_nothing_behind_a_ticket_that_passed(tmp_path: Path) -> None:
    """Done is work that exists, so nothing strands behind it. A ticket reopened
    after a run closed it still carries that outcome and is never offered
    again, which leaves what waits on it waiting on work no wave will build —
    not stranded behind a failure, which is a different thing to go and fix."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("done", head)]),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["recorded"] == [9]
    assert plan["stranded"] == []
    assert plan["blocked"] == [9, 10]
    assert plan["never_workable"] == [10]


def test_plan_offers_back_the_ticket_an_interrupted_run_left_claimed(
    tmp_path: Path,
) -> None:
    """An interrupted run costs the remaining tickets, not the finished ones.
    The ticket it was on is still claimed by this developer and carries no
    outcome, which is what an interruption looks like from the tracker."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", claimed_by=["me"]),
                _ticket(10, "the graph"),
            ]
        },
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["resuming"] == [9]
    assert plan["claimed"] == []
    assert plan["workable"] == [9, 10]


def test_plan_leaves_a_claim_this_run_never_took_where_it_is(tmp_path: Path) -> None:
    """Two sessions of one developer's authenticate as the same person, so a
    claim carrying that login is not by itself an interrupted run. A run
    holding state of its own that never took the claim leaves it alone."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
    )
    assert _engine(repo, "plan", "--state-dir", str(scratch), env=env).returncode == 0

    # A second session of this developer's claims 9 while the first is reading.
    _refile(
        env,
        "open",
        [_ticket(9, "the skeleton", claimed_by=["me"]), _ticket(10, "the graph")],
    )

    result = _engine(repo, "plan", "--state-dir", str(scratch), env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["resuming"] == []
    assert plan["claimed"] == [9]
    assert plan["workable"] == [10]


def test_plan_writes_the_run_state_to_the_directory_the_harness_provides(
    tmp_path: Path,
) -> None:
    """The state is written under the directory the harness keeps this
    session's scratch in, and the plan names the file so the developer can go
    and look at it. Under rather than in: a subagent's cleanup glob at the root
    of that directory deleted the engine's own state file mid-run, and the
    run's own things live where no subagent is sent (ADR-0071)."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton", claimed_by=["me"])]},
    )

    result = _engine(repo, "plan", "--state-dir", str(scratch), env=env)

    assert result.returncode == 0, result.stderr
    written = scratch / STATE_HOME / STATE_FILE
    assert json.loads(result.stdout)["state"] == str(written)
    assert not (scratch / STATE_FILE).exists()
    state = json.loads(written.read_text(encoding="utf-8"))
    assert state["branch"] == "work"
    assert state["label"] == "ready-for-agent"
    assert state["login"] == "me"
    assert state["claimed"] == [9]


def test_a_run_given_no_state_directory_plans_the_same_and_writes_nothing(
    tmp_path: Path,
) -> None:
    """A harness with no per-session directory to offer is not an error: the
    state is an optimisation, and the tracker is what the plan is read off."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["state"] is None
    assert plan["workable"] == [9]
    assert not list(tmp_path.rglob(STATE_FILE))


def test_a_state_file_nothing_can_read_is_rebuilt_rather_than_stopping_the_run(
    tmp_path: Path,
) -> None:
    """A half-written file from a run somebody killed says nothing, and a run
    that stopped over it would have made the state a source of truth."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    (scratch / STATE_HOME).mkdir(parents=True)
    (scratch / STATE_HOME / STATE_FILE).write_text('{"branch": "wo', encoding="utf-8")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton", claimed_by=["me"])]},
    )

    result = _engine(repo, "plan", "--state-dir", str(scratch), env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["resuming"] == [9]
    assert json.loads((scratch / STATE_HOME / STATE_FILE).read_text(encoding="utf-8"))[
        "claimed"
    ] == [9]


def test_claim_takes_a_ticket_this_developer_already_holds(tmp_path: Path) -> None:
    """The claim an interrupted run left is this run's own, so claiming it again
    is the same claim rather than a collision with somebody else."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        issues={9: _ready(9, assignees=[{"login": "me"}])},
    )

    result = _engine(repo, "claim", "--ticket", "9", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["claimed"] is True


def test_plan_refuses_where_a_claim_exists_and_nothing_can_say_whose_it_is(
    tmp_path: Path,
) -> None:
    """Told nothing about who it is, a run cannot tell its own interrupted claim
    from another session's, and either guess builds the wrong thing."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton", claimed_by=["someone"])]},
        login="",
    )

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 1
    assert "who" in result.stderr


def test_no_verb_takes_a_resume_flag(tmp_path: Path) -> None:
    """The ordinary invocation is the resume, so there is no flag to remember
    or forget."""

    repo = _init_repo(tmp_path / "proj")

    result = _engine(repo, "plan", "--resume")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_every_verb_accepts_a_state_directory(tmp_path: Path) -> None:
    """The flag reaches every verb, as `--yes` does, so the skill passes the
    session's scratch directory to whatever it calls."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton")]},
        issues={9: _ready(9)},
    )
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    for args in (
        ("plan",),
        ("claim", "--ticket", "9"),
        ("park", "--ticket", "9"),
        ("record", "--ticket", "9", "--outcome", "done", "--commit", head),
        ("report",),
    ):
        result = _engine(repo, *args, "--state-dir", str(scratch), env=env)
        assert result.returncode == 0, f"{args}: {result.stderr}"
        assert "unrecognized arguments" not in result.stderr


def test_report_names_the_commit_the_runs_work_sits_on(tmp_path: Path) -> None:
    """The account of a night is read as a diff, and the commit the run's first
    recorded work sits on top of is where that diff starts."""

    repo = _init_repo(tmp_path / "proj")
    before = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "one.txt").write_text("one\n", encoding="utf-8")
    _git(repo, "add", "one.txt")
    _git(repo, "commit", "-m", "the skeleton")
    first = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        closed=[_ticket(9, "the skeleton", comments=[_recorded("done", first)])],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["base"] == before


def _interrupted_run(tmp_path: Path, scratch: Path) -> tuple[Path, dict[str, str]]:
    """Play a run that recorded #9 done and was interrupted while holding #10.

    The stand-in tracker accepts a write and changes nothing, so what the run
    wrote is refiled here: #9 closed and recorded, #10 claimed and carrying no
    outcome, #11 never started.
    """

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph"),
                _ticket(11, "the build"),
            ]
        },
        issues={9: _ready(9), 10: _ready(10)},
    )

    for args in (
        ("plan",),
        ("claim", "--ticket", "9"),
        ("record", "--ticket", "9", "--outcome", "done", "--commit", head),
        ("claim", "--ticket", "10"),
    ):
        result = _engine(repo, *args, "--state-dir", str(scratch), env=env)
        assert result.returncode == 0, f"{args}: {result.stderr}"

    _refile(
        env,
        "open",
        [_ticket(10, "the graph", claimed_by=["me"]), _ticket(11, "the build")],
    )
    _refile(env, "closed", [_ticket(9, "the skeleton", comments=[_recorded("done")])])
    return repo, env


def test_re_invoking_continues_the_run_rather_than_restarting_it(
    tmp_path: Path,
) -> None:
    """The developer re-invokes exactly as before: what is done stays done, and
    what the interruption left claimed is picked up rather than skipped."""

    scratch = tmp_path / "scratch"
    repo, env = _interrupted_run(tmp_path, scratch)

    result = _engine(repo, "plan", "--state-dir", str(scratch), env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [entry["number"] for entry in plan["tickets"]] == [10, 11]
    assert plan["resuming"] == [10]
    assert plan["workable"] == [10, 11]


def test_a_run_whose_state_was_deleted_reaches_the_same_account(
    tmp_path: Path,
) -> None:
    """A new session, a cleared scratch directory, or a machine restart leaves
    no state to read, and the run rebuilds it from the tracker and the branch
    rather than starting over. That is what makes the invocation idempotent."""

    scratch = tmp_path / "scratch"
    repo, env = _interrupted_run(tmp_path, scratch)
    remembered = _engine(repo, "plan", "--state-dir", str(scratch), env=env)
    accounted = _engine(repo, "report", "--state-dir", str(scratch), env=env)

    shutil.rmtree(scratch)
    rebuilt = _engine(repo, "plan", "--state-dir", str(scratch), env=env)
    again = _engine(repo, "report", "--state-dir", str(scratch), env=env)

    assert rebuilt.returncode == remembered.returncode, rebuilt.stderr
    assert rebuilt.stdout == remembered.stdout
    assert again.stdout == accounted.stdout
    assert (scratch / STATE_HOME / STATE_FILE).exists()


def test_a_dry_run_leaves_no_state_behind(tmp_path: Path) -> None:
    """A dry run starts nothing, and a run that had left its memory behind
    would have started something after all."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--dry-run", "--state-dir", str(scratch), env=env)

    assert result.returncode == 2, result.stderr
    assert json.loads(result.stdout)["state"] is None
    assert not (scratch / STATE_HOME / STATE_FILE).exists()


def test_claim_refuses_a_claim_in_this_developers_name_the_run_never_took(
    tmp_path: Path,
) -> None:
    """The last gate answers as the plan does: a run holding state of its own
    that never took this claim is looking at another session's work, whatever
    login the tracker has against it."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={9: _ready(9, assignees=[{"login": "me"}])},
    )
    assert _engine(repo, "plan", "--state-dir", str(scratch), env=env).returncode == 0

    result = _engine(
        repo, "claim", "--ticket", "9", "--state-dir", str(scratch), env=env
    )

    assert result.returncode == 2
    claim = json.loads(result.stdout)
    assert claim["claimed"] is False
    assert "did not start" in claim["reason"]
    assert "--add-assignee" not in _gh_calls(env)


def test_the_run_state_names_the_commit_the_work_sits_on(tmp_path: Path) -> None:
    """The branch is the other half of what a run remembers, and it is read off
    the branch rather than off the file, so a rebuilt state cannot disagree
    with the history it describes."""

    repo = _init_repo(tmp_path / "proj")
    before = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "one.txt").write_text("one\n", encoding="utf-8")
    _git(repo, "add", "one.txt")
    _git(repo, "commit", "-m", "the skeleton")
    first = _git(repo, "rev-parse", "HEAD").stdout.strip()
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("failed", first)]),
                _ticket(10, "the graph"),
            ]
        },
    )

    assert _engine(repo, "plan", "--state-dir", str(scratch), env=env).returncode == 0

    state = json.loads((scratch / STATE_HOME / STATE_FILE).read_text(encoding="utf-8"))
    assert state["base"] == before


def test_plan_given_a_ticket_reference_works_that_ticket_alone(
    tmp_path: Path,
) -> None:
    """The developer aims the run at one ticket, and the rest of the tracker is
    neither planned nor named."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
        issues={9: _ready(9)},
    )

    result = _engine(repo, "plan", "--scope", "#9", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["scope"] == [{"reference": "#9", "kind": "ticket", "number": 9}]
    assert [entry["number"] for entry in plan["tickets"]] == [9]
    assert plan["workable"] == [9]
    assert "the graph" not in result.stdout


def test_a_ticket_reference_does_not_lift_the_tickets_blocking_edges(
    tmp_path: Path,
) -> None:
    """Naming a ticket says which ticket to work, never that the work it waits
    on already exists. A blocker outside the scope is work the run cannot
    reach, and the ticket is reported rather than built on top of nothing."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
            ]
        },
        issues={10: _ready(10)},
    )

    result = _engine(repo, "plan", "--scope", "10", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["workable"] == []
    assert plan["never_workable"] == [10]


def test_plan_given_a_spec_reference_works_that_specs_children(
    tmp_path: Path,
) -> None:
    """A spec scopes the run to its children, so tickets of an unrelated effort
    in the same tracker are left alone."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", parent=6),
                _ticket(10, "the graph", parent=6),
                _ticket(41, "another effort", parent=7),
            ]
        },
        issues={6: _children(9, 10)},
    )

    result = _engine(repo, "plan", "--scope", "#6", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["scope"] == [{"reference": "#6", "kind": "spec", "number": 6}]
    assert [entry["number"] for entry in plan["tickets"]] == [9, 10]
    assert plan["workable"] == [9, 10]
    assert "another effort" not in result.stdout


def test_plan_given_a_spec_reference_reads_a_parent_named_only_in_a_body(
    tmp_path: Path,
) -> None:
    """The tracker's own relation is the source where it carries one, and the
    body is the same fallback for a parent as it is for a blocking edge."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", body="## Parent\n\n#6\n"),
                _ticket(41, "another effort"),
            ]
        },
        issues={6: _ready(6)},
    )

    result = _engine(repo, "plan", "--scope", "6", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [aim["kind"] for aim in plan["scope"]] == ["spec"]
    assert [entry["number"] for entry in plan["tickets"]] == [9]


def test_plan_reads_a_reference_the_tracker_files_children_under_as_a_spec(
    tmp_path: Path,
) -> None:
    """A spec carrying the label is still a spec: what has children is scoped
    to them, and is never itself built."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(6, "the spec"),
                _ticket(9, "the skeleton", parent=6),
            ]
        },
        issues={6: _ready(6, **_children(9))},
    )

    result = _engine(repo, "plan", "--scope", "6", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [aim["kind"] for aim in plan["scope"]] == ["spec"]
    assert [entry["number"] for entry in plan["tickets"]] == [9]


def test_plan_refuses_a_reference_the_tracker_cannot_answer_for(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--scope", "#404", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert "404" in result.stderr
    assert result.stderr.startswith("error:")


def test_plan_refuses_a_reference_that_names_no_ticket(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--scope", "the graph", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert "the graph" in result.stderr
    assert result.stderr.startswith("error:")


def test_plan_refuses_a_reference_written_in_another_trackers_terms(
    tmp_path: Path,
) -> None:
    """A run reads one repository's tracker and cannot tell a reference in it
    from one somewhere else, which is why a body edge written this way is
    refused too."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--scope", "kntnt/skills#9", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert "kntnt/skills#9" in result.stderr
    assert result.stderr.startswith("error:")


def test_plan_given_several_ticket_references_works_exactly_those_tickets(
    tmp_path: Path,
) -> None:
    """A run is aimed at as many references as the developer named, and its
    scope is the union of what they resolve to."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph"),
                _ticket(41, "another effort"),
            ]
        },
        issues={9: _ready(9), 10: _ready(10)},
    )

    result = _engine(repo, "plan", "--scope", "#9 #10", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["scope"] == [
        {"reference": "#9", "kind": "ticket", "number": 9},
        {"reference": "#10", "kind": "ticket", "number": 10},
    ]
    assert [entry["number"] for entry in plan["tickets"]] == [9, 10]
    assert plan["workable"] == [9, 10]
    assert "another effort" not in result.stdout


def test_plan_given_a_spec_and_a_ticket_works_the_union_of_the_two(
    tmp_path: Path,
) -> None:
    """Each reference is resolved on its own: a spec brings its children and a
    ticket brings itself, and the run works both sets rather than one of
    them."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", parent=6),
                _ticket(10, "the graph", parent=6),
                _ticket(41, "another effort"),
                _ticket(42, "a third effort"),
            ]
        },
        issues={6: _children(9, 10), 41: _ready(41)},
    )

    result = _engine(repo, "plan", "--scope", "#6 #41", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [aim["kind"] for aim in plan["scope"]] == ["spec", "ticket"]
    assert [entry["number"] for entry in plan["tickets"]] == [9, 10, 41]
    assert "a third effort" not in result.stdout


def test_a_ticket_named_twice_or_beside_its_own_spec_is_the_same_scope(
    tmp_path: Path,
) -> None:
    """The scope is a set, so naming a ticket twice — or naming it beside the
    spec that holds it — names what one of them named, and is not an error."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", parent=6),
                _ticket(10, "the graph", parent=6),
            ]
        },
        issues={6: _children(9, 10), 9: _ready(9)},
    )

    result = _engine(repo, "plan", "--scope", "#6 #9 #9", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [aim["number"] for aim in plan["scope"]] == [6, 9]
    assert [entry["number"] for entry in plan["tickets"]] == [9, 10]
    assert plan["workable"] == [9, 10]


def test_a_scope_of_several_references_still_waits_on_the_edges_between_them(
    tmp_path: Path,
) -> None:
    """A scope narrows the set and never the rules (ADR-0053): a named ticket
    blocked by another named ticket waits for it, and the two are laid out in
    the waves the graph puts them in rather than started together."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph", blocked_by=[(9, "OPEN")]),
            ]
        },
        issues={9: _ready(9), 10: _ready(10)},
    )

    result = _engine(repo, "plan", "--scope", "#9 #10", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["waves"] == [[9], [10]]
    assert plan["workable"] == [9]


def test_plan_refuses_the_whole_scope_where_one_reference_reads_as_nothing(
    tmp_path: Path,
) -> None:
    """Dropping the reference nobody can read would work a scope the developer
    did not name, so the invocation is refused rather than narrowed to the rest
    of it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
        issues={9: _ready(9), 10: _ready(10)},
    )

    result = _engine(repo, "plan", "--scope", "#9 banana #10", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert "banana" in result.stderr
    assert result.stderr.startswith("error:")


def test_plan_refuses_a_whole_scope_the_tracker_answers_for_only_in_part(
    tmp_path: Path,
) -> None:
    """A reference the tracker does not know is refused wherever it stands, and
    the references beside it settle nothing about it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton")]},
        issues={9: _ready(9)},
    )

    result = _engine(repo, "plan", "--scope", "#9 #404", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert "404" in result.stderr
    assert result.stderr.startswith("error:")


def test_plan_refuses_a_qualified_reference_named_beside_readable_ones(
    tmp_path: Path,
) -> None:
    """A run reads one repository's tracker whatever else was named beside the
    reference written in another's terms."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
        issues={9: _ready(9), 10: _ready(10)},
    )

    result = _engine(repo, "plan", "--scope", "#9 kntnt/skills#10", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert "kntnt/skills#10" in result.stderr
    assert result.stderr.startswith("error:")


def test_a_scope_of_several_references_holding_no_ticket_names_them_all(
    tmp_path: Path,
) -> None:
    """A run says why it has nothing to work in the terms it was asked in, and
    a run aimed at several references was asked in all of them."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(41, "another effort")]},
        issues={9: {}, 10: {}},
    )

    result = _engine(repo, "plan", "--scope", "#9 #10", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert "#9, #10" in plan["reason"]
    assert plan["tickets"] == []


def test_a_dry_run_honours_the_scope_it_was_given(tmp_path: Path) -> None:
    """The plan a dry run is read off is the plan a run would work, so the two
    have to be aimed at the same tickets."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
        issues={9: _ready(9)},
    )

    result = _engine(repo, "plan", "--dry-run", "--scope", "#9", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert "dry run" in plan["reason"]
    assert [entry["number"] for entry in plan["tickets"]] == [9]
    assert plan["waves"] == [[9]]


def test_report_accounts_for_the_scope_the_run_was_aimed_at(tmp_path: Path) -> None:
    """A run aimed at one spec reports that spec's children and nothing else,
    or the report would account for work the run never had."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", parent=6),
                _ticket(41, "another effort", parent=7),
            ]
        },
        issues={6: _children(9)},
    )

    result = _engine(repo, "report", "--scope", "#6", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["scope"] == [{"reference": "#6", "kind": "spec", "number": 6}]
    assert [entry["number"] for entry in report["tickets"]] == [9]
    assert report["never_on_frontier"] == [9]


def test_report_accounts_for_a_scope_of_several_references(tmp_path: Path) -> None:
    """The report reads the run that was aimed, so a scope of several
    references accounts for the union of what they named and for nothing
    else."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", parent=6),
                _ticket(41, "another effort", parent=7),
                _ticket(42, "a third effort"),
            ]
        },
        issues={6: _children(9), 42: _ready(42)},
    )

    result = _engine(repo, "report", "--scope", "#6 #42", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert [aim["number"] for aim in report["scope"]] == [6, 42]
    assert [entry["number"] for entry in report["tickets"]] == [9, 42]
    assert report["never_on_frontier"] == [9, 42]
    assert "another effort" not in result.stdout


def test_a_scoped_plan_leaves_a_claim_outside_its_scope_where_it_is(
    tmp_path: Path,
) -> None:
    """A run aimed at part of the graph revises only what it read about. A
    claim an earlier, wider plan of this run took is still this run's own
    afterwards, or the next bare invocation would read it as a stranger's."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", claimed_by=["me"]),
                _ticket(10, "the graph"),
            ]
        },
        issues={10: _ready(10)},
    )
    assert _engine(repo, "plan", "--state-dir", str(scratch), env=env).returncode == 0

    result = _engine(
        repo, "plan", "--scope", "10", "--state-dir", str(scratch), env=env
    )

    assert result.returncode == 0, result.stderr
    state = json.loads((scratch / STATE_HOME / STATE_FILE).read_text(encoding="utf-8"))
    assert state["claimed"] == [9]


def test_plan_refuses_a_reference_that_says_nothing(tmp_path: Path) -> None:
    """An empty reference is a reference nobody can read, and reading it as a
    bare invocation would work the whole tracker under an argument that asked
    for part of it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--scope", "", env=env)

    assert result.returncode != 0
    assert not result.stdout
    assert result.stderr.startswith("error:")


def test_a_ticket_reference_does_not_re_offer_a_ticket_already_recorded(
    tmp_path: Path,
) -> None:
    """Naming a ticket says which ticket to work. It does not say that what a
    run has already written on that ticket has stopped being true, so a
    recorded outcome settles a named ticket exactly as it settles any other
    (ADR-0053)."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", comments=[_recorded("failed")])
            ]
        },
        issues={9: _ready(9)},
    )

    result = _engine(repo, "plan", "--scope", "#9", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["recorded"] == [9]
    assert plan["workable"] == []


def test_a_scoped_plan_forgets_a_claim_the_label_no_longer_holds_open(
    tmp_path: Path,
) -> None:
    """The note is the claims a run holds now. A claim the tracker has finished
    with is pruned by an aimed plan exactly as a bare one prunes it, or the
    note would only ever grow."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", claimed_by=["me"]),
                _ticket(10, "the graph"),
            ]
        },
        issues={10: _ready(10)},
    )
    assert _engine(repo, "plan", "--state-dir", str(scratch), env=env).returncode == 0

    # The tracker as it stands once 9 has been closed by hand.
    _refile(env, "open", [_ticket(10, "the graph")])

    result = _engine(
        repo, "plan", "--scope", "10", "--state-dir", str(scratch), env=env
    )

    assert result.returncode == 0, result.stderr
    state = json.loads((scratch / STATE_HOME / STATE_FILE).read_text(encoding="utf-8"))
    assert state["claimed"] == []


def test_plan_caps_how_many_tickets_are_started_at_once(tmp_path: Path) -> None:
    """The ceiling is what keeps concurrent test suites from overloading the
    machine and failing for the wrong reason. It caps what starts, and nothing
    else: the whole frontier stays workable and is worked a ceiling at a
    time."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(10, "the graph"),
                _ticket(11, "the report"),
            ]
        },
    )

    result = _engine(repo, "plan", "--at-once", "2", env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["at_once"] == 2
    assert plan["workable"] == [9, 10, 11]
    assert plan["starting"] == [9, 10]


def test_a_ceiling_above_one_gives_each_ticket_its_own_working_tree(
    tmp_path: Path,
) -> None:
    """Isolation is not an independent choice the developer makes separately:
    more than one ticket at a time is more than one working tree, and exactly
    one needs none."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton"), _ticket(10, "the graph")]},
    )

    alone = _engine(repo, "plan", env=env)
    together = _engine(repo, "plan", "--at-once", "2", env=env)

    assert alone.returncode == 0, alone.stderr
    assert together.returncode == 0, together.stderr
    assert json.loads(alone.stdout)["at_once"] == 1
    assert json.loads(alone.stdout)["worktrees"] is False
    assert json.loads(alone.stdout)["starting"] == [9]
    assert json.loads(together.stdout)["worktrees"] is True


def test_plan_refuses_a_ceiling_that_would_start_nothing(tmp_path: Path) -> None:
    """A ceiling below one is a run that works no ticket at all, which is not a
    run the developer can have meant."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})

    result = _engine(repo, "plan", "--at-once", "0", env=env)

    assert result.returncode == 1
    assert not result.stdout
    assert "at once" in result.stderr


def test_isolate_gives_a_ticket_a_working_tree_of_its_own(tmp_path: Path) -> None:
    """Two tickets built at once cannot share one working tree, and the
    developer's own is not a place to build in either: it is where they left
    it and stays there."""

    repo = _init_repo(tmp_path / "proj")

    result = _engine(repo, "isolate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    answer = json.loads(result.stdout)
    worktree = Path(answer["worktree"])
    assert worktree.is_dir()
    assert answer["branch"] != "work"
    assert _git(worktree, "branch", "--show-current").stdout.strip() == answer["branch"]
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_isolate_returns_the_working_tree_an_interrupted_run_already_made(
    tmp_path: Path,
) -> None:
    """The invocation is the resume here as everywhere else: a ticket picked up
    again goes on in the working tree it was left in rather than in a second
    one beside it."""

    repo = _init_repo(tmp_path / "proj")

    first = _engine(repo, "isolate", "--ticket", "9")
    second = _engine(repo, "isolate", "--ticket", "9")

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert json.loads(first.stdout) == json.loads(second.stdout)


def test_integrate_merges_a_ticket_and_takes_its_working_tree_away(
    tmp_path: Path,
) -> None:
    """The developer comes back to one branch and a tidy machine: the work is
    on the branch they were on, and what it was built in is gone."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    answer = json.loads(result.stdout)
    assert answer["merged"] is True
    assert answer["commit"] == _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert (repo / "graph.py").read_text(encoding="utf-8") == "edges\n"
    assert not worktree.exists()
    assert "kntnt-orchestrate" not in _git(repo, "branch", "--list").stdout


def _collided(repo: Path) -> dict[int, Path]:
    """Build two tickets over the same file and put the first on the branch.

    What is left is the collision every repair starts from: #9 merged into the
    run branch, and #10 standing in a working tree of its own with work that
    will not merge on top of it.
    """

    trees = {}
    for number, written in ((9, "nine\n"), (10, "ten\n")):
        tree = Path(
            json.loads(_engine(repo, "isolate", "--ticket", str(number)).stdout)[
                "worktree"
            ]
        )
        (tree / "graph.py").write_text(written, encoding="utf-8")
        _git(tree, "add", "graph.py")
        _git(tree, "commit", "-m", f"build #{number}")
        trees[number] = tree
    assert _engine(repo, "integrate", "--ticket", "9").returncode == 0

    return trees


def test_integrate_keeps_the_working_tree_of_a_ticket_it_could_not_merge(
    tmp_path: Path,
) -> None:
    """Two tickets that touched the same code collide at the merge. The run
    branch is left as it was rather than half-merged, and the losing ticket's
    working tree stands so the collision can be repaired from it."""

    repo = _init_repo(tmp_path / "proj")
    trees = _collided(repo)

    result = _engine(repo, "integrate", "--ticket", "10")

    assert result.returncode == 2, result.stderr
    answer = json.loads(result.stdout)
    assert answer["merged"] is False
    assert answer["collisions"] == ["graph.py"]
    assert answer["worktree"] == str(trees[10])
    assert trees[10].is_dir()
    assert (repo / "graph.py").read_text(encoding="utf-8") == "nine\n"
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_integrate_refuses_work_a_working_tree_never_committed(
    tmp_path: Path,
) -> None:
    """A builder that stopped mid-ticket leaves work only its working tree
    holds. Merging the branch and sweeping the tree away would take that work
    with it without saying so."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "README.md").write_text("half a ticket\n", encoding="utf-8")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 1
    assert "never committed" in result.stderr
    assert worktree.is_dir()


def test_integrate_refuses_a_file_a_working_tree_never_added(tmp_path: Path) -> None:
    """A file written and never added is the half of a stopped ticket's work
    the merge cannot carry, and taking the working tree away would destroy it
    outright rather than leave it somewhere to be found."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("never added\n", encoding="utf-8")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 1
    assert "never committed" in result.stderr
    assert (worktree / "graph.py").is_file()


def test_integrate_merges_into_the_default_branch(tmp_path: Path) -> None:
    """A run ends on the branch it started on, so a run started on the default
    branch integrates there like anywhere else (ADR-0064)."""

    repo = _init_repo(tmp_path / "proj", branch="main")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["merged"] is True
    assert (repo / "graph.py").read_text(encoding="utf-8") == "edges\n"
    assert not worktree.exists()


def test_integrate_merges_where_nothing_can_say_which_branch_is_the_default(
    tmp_path: Path,
) -> None:
    """No answer about the default branch gates a merge any more, so a
    repository that can name no default is merged into rather than refused."""

    repo = _init_repo(tmp_path / "proj", initial="trunk", branch="work")
    _git(repo, "branch", "-D", "trunk")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["merged"] is True
    assert (repo / "graph.py").read_text(encoding="utf-8") == "edges\n"
    assert not worktree.exists()


def test_a_failed_tickets_working_tree_stays_where_the_run_left_it(
    tmp_path: Path,
) -> None:
    """The machine ends tidy except for the failures, which stay inspectable —
    so the report says where the work of one stands."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton")]},
        issues={9: _ready(9)},
    )
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    assert (
        _engine(
            repo, "record", "--ticket", "9", "--outcome", "failed", env=env
        ).returncode
        == 0
    )
    _refile(env, "open", [_ticket(9, "the skeleton", comments=[_recorded("failed")])])

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["failed"] == [9]
    assert report["tickets"][0]["worktree"] == str(worktree)
    assert worktree.is_dir()


def test_report_names_the_tickets_a_stopped_run_never_attempted(
    tmp_path: Path,
) -> None:
    """A suite that fails on the integrated branch stops the run rather than
    spending the remaining hours building on broken code. What the run never
    got to is named rather than dropped: a ticket dropped in silence is one the
    developer would not know to pick up."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(10, "the graph", blocked_by=[(9, "CLOSED")]),
                _ticket(11, "the report"),
            ]
        },
        closed=[_ticket(9, "the skeleton", comments=[_recorded("done", head)])],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["done"] == [9]
    assert report["never_on_frontier"] == [10, 11]
    accounted = (
        report["done"]
        + report["failed"]
        + report["conflicted"]
        + report["stranded"]
        + report["never_on_frontier"]
    )
    assert sorted(accounted) == [9, 10, 11]
    assert len(accounted) == len(set(accounted))


def test_integrate_names_the_ticket_a_collision_was_with(tmp_path: Path) -> None:
    """A collision that is not repaired names a blocking edge the ticket
    breakdown was missing, and it takes both tickets to name it. The files
    alone would leave the developer to work out whose work is on the other
    side of them."""

    repo = _init_repo(tmp_path / "proj")
    _collided(repo)

    result = _engine(repo, "integrate", "--ticket", "10")

    assert result.returncode == 2, result.stderr
    answer = json.loads(result.stdout)
    assert answer["collisions"] == ["graph.py"]
    assert answer["collided_with"] == [9]


def test_integrate_leaves_out_a_merge_the_losing_branch_already_carries(
    tmp_path: Path,
) -> None:
    """An earlier wave's ticket that touched the same file is not what this one
    collided with: the losing branch was cut after that merge, so the two share
    it as common ground. Naming it would report a blocking edge that is not
    missing, and the pair is read for exactly the ones that are."""

    repo = _init_repo(tmp_path / "proj")

    # An earlier wave puts #8 on the branch, over the file all three touch.
    early = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "8").stdout)["worktree"]
    )
    (early / "graph.py").write_text("eight\n", encoding="utf-8")
    _git(early, "add", "graph.py")
    _git(early, "commit", "-m", "build #8")
    assert _engine(repo, "integrate", "--ticket", "8").returncode == 0

    # #9 and #10 are cut from the branch as it then stands, and collide.
    trees = {}
    for number, written in ((9, "eight\nnine\n"), (10, "eight\nten\n")):
        tree = Path(
            json.loads(_engine(repo, "isolate", "--ticket", str(number)).stdout)[
                "worktree"
            ]
        )
        (tree / "graph.py").write_text(written, encoding="utf-8")
        _git(tree, "add", "graph.py")
        _git(tree, "commit", "-m", f"build #{number}")
        trees[number] = tree
    assert _engine(repo, "integrate", "--ticket", "9").returncode == 0

    result = _engine(repo, "integrate", "--ticket", "10")

    assert result.returncode == 2, result.stderr
    answer = json.loads(result.stdout)
    assert answer["collisions"] == ["graph.py"]
    assert answer["collided_with"] == [9]


def test_integrate_merges_a_ticket_repaired_on_its_own_branch(
    tmp_path: Path,
) -> None:
    """The cheap repair is settled on the losing ticket's own branch, so the
    branch the developer comes back to is never half-merged and never carries
    an unverified resolution. Once the run branch is in that ticket's branch,
    the second integration cannot collide."""

    repo = _init_repo(tmp_path / "proj")
    trees = _collided(repo)
    assert _engine(repo, "integrate", "--ticket", "10").returncode == 2

    # The repair, as the subagent makes it: the run branch merged into the
    # ticket's branch, settled there, and committed.
    subprocess.run(
        ["git", "merge", "work"],
        cwd=trees[10],
        env=_GIT_ENV,
        text=True,
        capture_output=True,
        check=False,
    )
    (trees[10] / "graph.py").write_text("nine\nten\n", encoding="utf-8")
    _git(trees[10], "add", "graph.py")
    _git(trees[10], "commit", "--no-edit")

    result = _engine(repo, "integrate", "--ticket", "10")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["merged"] is True
    assert (repo / "graph.py").read_text(encoding="utf-8") == "nine\nten\n"
    assert not trees[10].exists()


def test_rebuild_discards_the_losing_tickets_working_tree_and_branch(
    tmp_path: Path,
) -> None:
    """Where the repair does not verify, the ticket is built again from
    scratch on top of the integrated branch — so what it was built in the
    first time goes, and the branch it collided with is left exactly as it
    was."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )
    trees = _collided(repo)
    assert _engine(repo, "integrate", "--ticket", "10").returncode == 2

    result = _engine(repo, "rebuild", "--ticket", "10", env=env)

    assert result.returncode == 0, result.stderr
    answer = json.loads(result.stdout)
    assert answer["rebuilt"] is True
    assert not trees[10].exists()
    assert "kntnt-orchestrate" not in _git(repo, "branch", "--list").stdout
    assert (repo / "graph.py").read_text(encoding="utf-8") == "nine\n"
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert "rebuild" in _gh_calls(env)


def test_a_ticket_is_rebuilt_at_most_once(tmp_path: Path) -> None:
    """A rebuild is the one rerun a collision buys, and the tracker is what
    bounds it: the note the first rebuild left on the ticket is what refuses
    the second, so a collision that keeps coming back is recorded rather than
    built over and over."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )
    _collided(repo)
    assert _engine(repo, "rebuild", "--ticket", "10", env=env).returncode == 0
    note = _wrote(env, 10)
    assert f"<!-- {MARKER} rebuild -->" in note
    _refile_issue(env, 10, _ready(10, comments=[{"body": note}]))

    # The ticket, built afresh on the integrated branch, collides again.
    rebuilt = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "10").stdout)["worktree"]
    )
    (rebuilt / "graph.py").write_text("ten again\n", encoding="utf-8")
    _git(rebuilt, "add", "graph.py")
    _git(rebuilt, "commit", "-m", "build #10 again")

    result = _engine(repo, "rebuild", "--ticket", "10", env=env)

    assert result.returncode == 2, result.stderr
    answer = json.loads(result.stdout)
    assert answer["rebuilt"] is False
    assert "already" in answer["reason"]
    assert "a collision buys" in answer["reason"]
    assert rebuilt.is_dir()


def test_rebuild_refuses_a_ticket_that_has_no_working_tree_to_discard(
    tmp_path: Path,
) -> None:
    """A ceiling of one merges nothing, so nothing can collide and there is
    nothing to rebuild on top of."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )

    result = _engine(repo, "rebuild", "--ticket", "10", env=env)

    assert result.returncode == 1
    assert "no working tree" in result.stderr
    assert _gh_calls(env) == ""


def test_amend_writes_the_bound_on_the_ticket_the_moment_it_is_spent(
    tmp_path: Path,
) -> None:
    """A failed verification buys one amend, and the note is the bound: the
    ticket carries it from the moment the amend starts, so a run interrupted
    mid-amend comes back and finds the bound where it left it (ADR-0069).
    Nothing is discarded and nothing is made — the amender works the tree the
    first builder worked, which is why a ceiling of one, with no working tree
    at all, is amended exactly like any other ticket."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )

    result = _engine(repo, "amend", "--ticket", "10", env=env)

    assert result.returncode == 0, result.stderr
    answer = json.loads(result.stdout)
    assert answer["amended"] is True
    assert answer["reason"] is None
    assert f"<!-- {MARKER} amend -->" in _wrote(env, 10)


def test_a_ticket_is_amended_at_most_once(tmp_path: Path) -> None:
    """The amend is bounded exactly as the rebuild is, and by the same thing:
    the note the first amend left on the ticket is what refuses the second, so
    a ticket whose verdict keeps failing is recorded rather than built over and
    over through the night."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )
    assert _engine(repo, "amend", "--ticket", "10", env=env).returncode == 0
    _refile_issue(env, 10, _ready(10, comments=[{"body": _wrote(env, 10)}]))

    result = _engine(repo, "amend", "--ticket", "10", env=env)

    assert result.returncode == 2, result.stderr
    answer = json.loads(result.stdout)
    assert answer["amended"] is False
    assert "already" in answer["reason"]


def test_the_amend_and_the_rebuild_are_bounds_a_ticket_spends_separately(
    tmp_path: Path,
) -> None:
    """The two answer different failures at different moments — the rebuild a
    collision at integration, the amend a verdict before it — so spending one
    leaves the other where it was, and a collided ticket's repair story does
    not depend on whether its verifier had earlier found a typo (ADR-0069)."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )
    trees = _collided(repo)
    assert _engine(repo, "amend", "--ticket", "10", env=env).returncode == 0
    amended = _wrote(env, 10)
    _refile_issue(env, 10, _ready(10, comments=[{"body": amended}]))

    result = _engine(repo, "rebuild", "--ticket", "10", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["rebuilt"] is True
    assert not trees[10].exists()

    # With both notes standing, neither bound is left for this ticket to spend.
    rebuilt = _wrote(env, 10)
    _refile_issue(env, 10, _ready(10, comments=[{"body": amended}, {"body": rebuilt}]))
    assert _engine(repo, "amend", "--ticket", "10", env=env).returncode == 2


def test_record_stores_the_ticket_a_conflicted_outcome_collided_with(
    tmp_path: Path,
) -> None:
    """The pair is what the developer fixes the ticket breakdown from, so it is
    written where they will look for it."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )

    result = _engine(
        repo,
        "record",
        "--ticket",
        "10",
        "--outcome",
        "conflicted",
        "--collided-with",
        "9",
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["collided_with"] == [9]
    assert "collided-with=9" in _gh_calls(env)
    assert "#9" in _gh_calls(env)


def test_record_refuses_a_collision_named_against_another_outcome(
    tmp_path: Path,
) -> None:
    """Only a collision has a ticket on the other side of it. A failure or a
    pass recorded against one would state something that did not happen."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )

    result = _engine(
        repo,
        "record",
        "--ticket",
        "10",
        "--outcome",
        "failed",
        "--collided-with",
        "9",
        env=env,
    )

    assert result.returncode == 1
    assert "conflicted" in result.stderr
    assert _gh_calls(env) == ""


def test_report_accounts_for_a_conflicted_ticket_with_the_one_it_hit(
    tmp_path: Path,
) -> None:
    """A collision that was not repaired is reported together with the ticket
    it collided with — that pair is the blocking edge the breakdown missed, and
    it is how this run improves the next one."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton"),
                _ticket(
                    10,
                    "the graph",
                    comments=[_recorded("conflicted", collided_with=[9])],
                ),
            ]
        },
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["conflicted"] == [10]
    entry = next(entry for entry in report["tickets"] if entry["number"] == 10)
    assert entry["collided_with"] == [9]


def test_no_verb_pushes_while_the_developer_is_asleep(tmp_path: Path) -> None:
    """Isolating and integrating are git of a kind the earlier verbs never ran,
    and nothing leaves the machine in either."""

    repo = _init_repo(tmp_path / "proj")
    env = _git_spy(tmp_path)
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9", env=env).stdout)[
            "worktree"
        ]
    )
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")

    assert _engine(repo, "integrate", "--ticket", "9", env=env).returncode == 0

    ran = Path(env["SPY_LOG"]).read_text(encoding="utf-8").splitlines()
    assert "push" not in [line.split()[0] for line in ran if line.strip()]


def test_plan_refuses_a_working_tree_that_holds_uncommitted_work(
    tmp_path: Path,
) -> None:
    """A run commits where the developer left off, so work they had not
    committed would land inside a ticket's own commit. Asked on the default
    branch, which is now worked like any other, so the tree is the only thing
    left that a plan refuses about the state it starts in."""

    repo = _init_repo(tmp_path / "proj", branch="main")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})
    (repo / "README.md").write_text("half a thought\n", encoding="utf-8")

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert "committed" in plan["reason"]
    assert "branch" not in plan["reason"]
    assert [entry["number"] for entry in plan["tickets"]] == [9]


def test_plan_refuses_a_working_tree_holding_a_file_nothing_tracks(
    tmp_path: Path,
) -> None:
    """A file written and never added is the half of that work a merge cannot
    carry, and above a ceiling of one it stops one with nothing to collide
    over."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})
    (repo / "notes.txt").write_text("mine, not a ticket's\n", encoding="utf-8")

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert "committed" in plan["reason"]


def test_plan_works_a_tree_whose_only_changes_the_repository_ignores(
    tmp_path: Path,
) -> None:
    """What the repository ignores is not work, and a run that refused over a
    cache directory would refuse every repository that has one."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})
    (repo / ".gitignore").write_text("build/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore what is built")
    (repo / "build").mkdir()
    (repo / "build" / "out.txt").write_text("generated\n", encoding="utf-8")

    result = _engine(repo, "plan", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["ready"] is True


def test_a_dry_run_reads_the_scope_from_a_working_tree_that_holds_work(
    tmp_path: Path,
) -> None:
    """A dry run starts nothing whatever the tree holds, so it answers with
    the scope rather than with a refusal about a run nobody asked to start."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": [_ticket(9, "the skeleton")]})
    (repo / "README.md").write_text("half a thought\n", encoding="utf-8")

    result = _engine(repo, "plan", "--dry-run", env=env)

    assert result.returncode == 2, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is False
    assert plan["reason"] == "dry run: nothing is started"
    assert [entry["number"] for entry in plan["tickets"]] == [9]


def test_record_refuses_a_done_outcome_while_the_working_tree_holds_work(
    tmp_path: Path,
) -> None:
    """A ticket closed on a commit that does not carry its work is a report
    nobody can check, and at a ceiling of one nothing else asks the
    question — the ticket has no working tree of its own to be refused
    over."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})
    (repo / "graph.py").write_text("never committed\n", encoding="utf-8")

    result = _engine(
        repo,
        "record",
        "--ticket",
        "9",
        "--outcome",
        "done",
        "--commit",
        "HEAD",
        env=env,
    )

    assert result.returncode == 1
    assert "committed" in result.stderr
    assert "issue close" not in _gh_calls(env)


def test_record_writes_a_failure_from_a_working_tree_that_still_holds_work(
    tmp_path: Path,
) -> None:
    """A failed ticket's work is left where it stands on purpose, so the tree
    holding it is the state that outcome is recorded from."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})
    (repo / "graph.py").write_text("half a ticket\n", encoding="utf-8")

    result = _engine(repo, "record", "--ticket", "9", "--outcome", "failed", env=env)

    assert result.returncode == 0, result.stderr
    assert "issue comment 9" in _gh_calls(env)


def test_isolate_does_not_adopt_a_working_tree_another_branch_left(
    tmp_path: Path,
) -> None:
    """A tree is named for its ticket and a branch for its run, and it is the
    branch that says whose it is: adopting one an interrupted run left on
    another branch would build this run's ticket on top of that branch's
    work."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("another branch's work\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "build #9 elsewhere")
    _git(repo, "checkout", "-b", "other")

    result = _engine(repo, "isolate", "--ticket", "9")

    assert result.returncode == 1
    assert str(worktree) in result.stderr
    assert worktree.is_dir()
    assert (worktree / "graph.py").is_file()


def test_integrate_leaves_a_working_tree_another_branch_holds_alone(
    tmp_path: Path,
) -> None:
    """What a run merges is what it built, and a tree cut from another branch
    is neither."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("another branch's work\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "build #9 elsewhere")
    _git(repo, "checkout", "-b", "other")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 1
    assert not (repo / "graph.py").exists()
    assert worktree.is_dir()


def test_isolate_still_resumes_the_working_tree_this_branchs_run_made(
    tmp_path: Path,
) -> None:
    """The invocation is the resume, and narrowing what counts as this run's
    tree must not cost the run the tree it made itself."""

    repo = _init_repo(tmp_path / "proj")

    first = _engine(repo, "isolate", "--ticket", "9")
    second = _engine(repo, "isolate", "--ticket", "9")

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert json.loads(first.stdout) == json.loads(second.stdout)


def test_report_asks_only_for_what_was_closed_since_the_branch_left_the_default(
    tmp_path: Path,
) -> None:
    """Every ticket a run ever finished stays closed, labelled, and assigned,
    so the question grows for the life of the project. The fork point is
    earlier than anything this run recorded and later than everything the
    project finished before the branch existed."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []})
    fork = _git(repo, "merge-base", "HEAD", "main").stdout.strip()
    day = _git(repo, "show", "--no-patch", "--format=%cs", fork).stdout.strip()

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    asked = [line for line in _gh_calls(env).splitlines() if "--state closed" in line]
    assert len(asked) == 1
    assert f"closed:>={day}" in asked[0]


def test_report_asks_the_whole_closed_question_where_no_default_can_be_told(
    tmp_path: Path,
) -> None:
    """A repository naming its default neither main nor master, and no remote
    to ask, has no fork point to bound anything by — so the question is asked
    whole and the full-page guard is what still answers for it."""

    repo = _init_repo(tmp_path / "proj", initial="trunk", branch="work")
    env = _tracker(tmp_path, {"ready-for-agent": []})
    _git(repo, "branch", "-D", "trunk")

    result = _engine(repo, "report", env=env)

    assert result.returncode == 0, result.stderr
    asked = [line for line in _gh_calls(env).splitlines() if "--state closed" in line]
    assert len(asked) == 1
    assert "closed:>=" not in asked[0]


def test_report_refuses_a_closed_list_that_may_have_been_truncated(
    tmp_path: Path,
) -> None:
    """The bound narrows the question; it does not answer it. A closed half
    that still comes back a full page is a report nobody can check, and says
    so rather than accounting for part of a run."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        closed=[
            _ticket(number, "one of many", comments=[_recorded("done", "abc123")])
            for number in range(200)
        ],
    )

    result = _engine(repo, "report", env=env)

    assert result.returncode == 1
    assert "200" in result.stderr


def test_isolate_refuses_a_ticket_whose_branch_an_earlier_run_left_behind(
    tmp_path: Path,
) -> None:
    """A branch with no working tree holding it is work an earlier run left,
    and a run that cut a second one over it would build this ticket on top of
    that work without saying so. The branch name is stated here as the
    contract rather than imported.

    The refusal is pinned by what only the engine says. Cutting the tree would
    fail on its own — git will not open a second branch of that name — with an
    error naming the same branch and exiting the same way, so a test reading
    only the name and the code cannot tell the guard from its absence."""

    repo = _init_repo(tmp_path / "proj")
    _git(repo, "branch", "kntnt-orchestrate/work/9")

    result = _engine(repo, "isolate", "--ticket", "9")

    assert result.returncode == 1
    assert "kntnt-orchestrate/work/9" in result.stderr
    assert "look at what is on it, then delete it" in result.stderr
    assert _git(repo, "worktree", "list").stdout.count("\n") == 1


def test_integrate_names_a_working_tree_it_could_not_take_away(
    tmp_path: Path,
) -> None:
    """The machine ends tidy, and where it cannot the run says so: a tree
    reported gone that is still there is one nobody goes back to look at."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")
    _git(repo, "worktree", "lock", str(worktree))

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    answer = json.loads(result.stdout)
    assert answer["merged"] is True
    assert answer["worktree"] == str(worktree)
    assert worktree.is_dir()
    assert "kntnt-orchestrate/work/9" in _git(repo, "branch", "--list").stdout


def test_integrate_says_what_stopped_a_merge_that_left_no_conflicted_file(
    tmp_path: Path,
) -> None:
    """A merge can fail without a collision — a file standing in the run
    branch's own working tree that the merge would have written over. There is
    no conflicted file to name and no ticket on the other side of it, so what
    stopped it has to speak for itself rather than pass as a collision with
    nothing in it."""

    repo = _init_repo(tmp_path / "proj")
    worktree = Path(
        json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)["worktree"]
    )
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")
    (repo / "graph.py").write_text("somebody else's, never added\n", encoding="utf-8")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 2, result.stderr
    answer = json.loads(result.stdout)
    assert answer["merged"] is False
    assert answer["collisions"] == []
    assert answer["collided_with"] == []
    assert "graph.py" in answer["reason"]
    assert answer["worktree"] == str(worktree)


def _registry(repo: Path, directory: str, *records: str) -> None:
    """File a directory of records named by number, as this collection keeps them."""

    (repo / directory).mkdir(parents=True, exist_ok=True)
    for record in records:
        (repo / directory / record).write_text("a record\n", encoding="utf-8")
    _git(repo, "add", directory)
    _git(repo, "commit", "-m", f"file {directory}")


def test_isolate_reserves_a_number_no_other_ticket_in_the_wave_holds(
    tmp_path: Path,
) -> None:
    """Two tickets built at once each read the registry for its next free
    number, read the same answer, and create two records under one number.
    Git merges both sides without a conflict and no gate ever says so, so the
    run hands the numbers out before the wave builds (ADR-0071)."""

    repo = _init_repo(tmp_path / "proj")
    _registry(repo, "docs/adr", "0001-the-first.md", "0002-the-second.md")

    first = json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)
    second = json.loads(_engine(repo, "isolate", "--ticket", "10").stdout)

    assert first["reservations"] == [{"directory": "docs/adr", "number": "0003"}]
    assert second["reservations"] == [{"directory": "docs/adr", "number": "0004"}]


def test_isolate_gives_a_ticket_back_the_number_it_already_holds(
    tmp_path: Path,
) -> None:
    """The invocation is the resume here as everywhere else: a ticket picked up
    again holds the number its brief was filled in from, and a ticket isolated
    beside it never holds that one."""

    repo = _init_repo(tmp_path / "proj")
    _registry(repo, "docs/adr", "0001-the-first.md")

    first = json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)
    beside = json.loads(_engine(repo, "isolate", "--ticket", "10").stdout)
    again = json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)

    assert first["reservations"] == [{"directory": "docs/adr", "number": "0002"}]
    assert again["reservations"] == first["reservations"]
    assert beside["reservations"] == [{"directory": "docs/adr", "number": "0003"}]


def test_isolate_reserves_nothing_in_a_repository_that_numbers_nothing(
    tmp_path: Path,
) -> None:
    """A repository keeping no records named by number has nothing to hand out,
    which is an answer and not a refusal."""

    repo = _init_repo(tmp_path / "proj")

    result = _engine(repo, "isolate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["reservations"] == []


def test_the_registries_the_engine_finds_are_the_ones_this_repository_keeps() -> None:
    """The detection is deterministic and unconfigured, so what it answers for
    this repository is what this repository actually keeps: the decision
    records under `docs/adr`, and nothing else in the tree."""

    found = _run().numbered_registries(REPO_ROOT)
    records = sorted((REPO_ROOT / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md"))

    assert set(found) == {"docs/adr"}
    assert found["docs/adr"] == int(records[-1].name[:4])


def test_isolate_gives_a_ticket_a_scratch_directory_of_its_own(
    tmp_path: Path,
) -> None:
    """Two subagents in sibling working trees chose the same log path for the
    same gate, and one nearly read the other's exit status as its own. A path
    they cannot both name is what stops that (ADR-0071)."""

    repo = _init_repo(tmp_path / "proj")

    first = json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)
    second = json.loads(_engine(repo, "isolate", "--ticket", "10").stdout)

    assert Path(first["scratch"]).is_dir()
    assert Path(second["scratch"]).is_dir()
    assert first["scratch"] != second["scratch"]
    assert Path(first["scratch"]) != Path(first["worktree"])
    assert Path(first["scratch"]).parent == Path(first["worktree"]).parent


def test_integrate_takes_away_what_isolate_gave_a_merged_ticket(
    tmp_path: Path,
) -> None:
    """The machine ends tidy: a ticket whose work is on the branch is finished
    with the scratch it was given as it is finished with the tree."""

    repo = _init_repo(tmp_path / "proj")
    answer = json.loads(_engine(repo, "isolate", "--ticket", "9").stdout)
    worktree = Path(answer["worktree"])
    (worktree / "graph.py").write_text("edges\n", encoding="utf-8")
    _git(worktree, "add", "graph.py")
    _git(worktree, "commit", "-m", "read the blocking edges")

    result = _engine(repo, "integrate", "--ticket", "9")

    assert result.returncode == 0, result.stderr
    assert not Path(answer["scratch"]).exists()


def test_a_rebuilt_ticket_reserves_afresh_rather_than_keeping_a_spent_number(
    tmp_path: Path,
) -> None:
    """A rebuild throws the first try away and builds on top of the work it
    collided with — which may have taken the number the first try was holding,
    so the second try reads the registry as it now stands."""

    repo = _init_repo(tmp_path / "proj")
    _registry(repo, "docs/adr", "0001-the-first.md")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(10, "the graph")]},
        issues={10: _ready(10)},
    )
    _collided(repo)
    held = json.loads(_engine(repo, "isolate", "--ticket", "10").stdout)
    assert _engine(repo, "integrate", "--ticket", "10").returncode == 2
    assert _engine(repo, "rebuild", "--ticket", "10", env=env).returncode == 0

    again = json.loads(_engine(repo, "isolate", "--ticket", "10").stdout)

    assert held["reservations"] == [{"directory": "docs/adr", "number": "0003"}]
    assert again["reservations"] == [{"directory": "docs/adr", "number": "0002"}]


def test_a_state_file_left_at_the_old_place_is_carried_into_the_new_one(
    tmp_path: Path,
) -> None:
    """A run interrupted before the state moved goes on where it left off: the
    old file is read once and rewritten where the new one lives, rather than
    read as no state at all and its claims handed back as somebody else's."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    (scratch / STATE_FILE).write_text(
        json.dumps(
            {
                "branch": "work",
                "label": "ready-for-agent",
                "login": "me",
                "claimed": [],
                "base": _git(repo, "rev-parse", "HEAD").stdout.strip(),
            }
        ),
        encoding="utf-8",
    )
    env = _tracker(
        tmp_path,
        {
            "ready-for-agent": [
                _ticket(9, "the skeleton", claimed_by=["me"]),
                _ticket(10, "the graph"),
            ]
        },
    )

    result = _engine(repo, "plan", "--state-dir", str(scratch), env=env)

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["resuming"] == []
    assert plan["claimed"] == [9]
    assert not (scratch / STATE_FILE).exists()
    assert (scratch / STATE_HOME / STATE_FILE).exists()


def test_park_returns_a_ticket_to_the_human_loop(tmp_path: Path) -> None:
    """ADR-0070: the ready label is a claim triage can get wrong, and the swap
    is the tracker saying truthfully that the thinking is not finished."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(tmp_path, {"ready-for-agent": []}, issues={9: _ready(9)})

    result = _engine(repo, "park", "--ticket", "9", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["parked"] is True
    calls = _gh_calls(env)
    assert "issue edit 9 --remove-label ready-for-agent --add-label needs-info" in calls


def test_park_releases_the_claim_this_run_holds(tmp_path: Path) -> None:
    """A parked ticket has left the scope, so a claim of this run's own goes
    with the label rather than standing over work nobody will do."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        issues={9: _ready(9, assignees=[{"login": "me"}])},
        login="me",
    )

    result = _engine(repo, "park", "--ticket", "9", env=env)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["parked"] is True
    assert "--remove-assignee @me" in _gh_calls(env)


def test_park_leaves_a_claim_that_is_not_this_runs(tmp_path: Path) -> None:
    """The open question is the ticket's whoever holds it, so the label still
    moves — but another session's claim is not this run's to release."""

    repo = _init_repo(tmp_path / "proj")
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        issues={9: _ready(9, assignees=[{"login": "someone"}])},
        login="me",
    )

    result = _engine(repo, "park", "--ticket", "9", env=env)

    assert result.returncode == 0, result.stderr
    calls = _gh_calls(env)
    assert "--remove-label ready-for-agent --add-label needs-info" in calls
    assert "--remove-assignee" not in calls


def test_park_refuses_a_ticket_that_carries_a_recorded_outcome(
    tmp_path: Path,
) -> None:
    """A settled ticket is nobody's to park: what a run recorded on it is the
    account the report reads, and the swap would take the ticket out of it."""

    repo = _init_repo(tmp_path / "proj")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    env = _tracker(
        tmp_path,
        {"ready-for-agent": []},
        issues={9: _ready(9, comments=[_recorded("done", head)])},
    )

    result = _engine(repo, "park", "--ticket", "9", env=env)

    assert result.returncode == 2
    parked = json.loads(result.stdout)
    assert parked["parked"] is False
    assert "settled" in parked["reason"]
    assert "issue edit" not in _gh_calls(env)


def test_park_takes_the_ticket_out_of_what_the_run_remembers_claiming(
    tmp_path: Path,
) -> None:
    """A parked ticket is no longer this run's claim, so a later invocation
    does not go looking for it as work an interruption left behind."""

    repo = _init_repo(tmp_path / "proj")
    scratch = tmp_path / "scratch"
    env = _tracker(
        tmp_path,
        {"ready-for-agent": [_ticket(9, "the skeleton")]},
        issues={9: _ready(9)},
    )
    assert _engine(repo, "plan", "--state-dir", str(scratch), env=env).returncode == 0
    assert (
        _engine(
            repo, "claim", "--ticket", "9", "--state-dir", str(scratch), env=env
        ).returncode
        == 0
    )

    result = _engine(
        repo, "park", "--ticket", "9", "--state-dir", str(scratch), env=env
    )

    assert result.returncode == 0, result.stderr
    state = json.loads((scratch / STATE_HOME / STATE_FILE).read_text(encoding="utf-8"))
    assert state["claimed"] == []
