# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Plan, record, and report an unattended run over the tracker's tickets."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

# The label that says the thinking behind a ticket is finished. A ticket
# without it is never planned, never claimed, and never built.
READY_LABEL = "ready-for-agent"

# How many tickets one tracker query asks for. The tracker pages at thirty by
# default, which is no scope at all; a page that comes back full is not
# trusted to be the whole set, since a scope silently missing tickets is a run
# that leaves work behind without saying so.
TICKET_PAGE = 200

# The outcomes a run records against a ticket. Stranded and never-on-the-
# frontier are read off the graph rather than recorded, so neither is one.
OUTCOMES = ("done", "failed", "conflicted")

# What the tracker calls a ticket that is finished. A blocker in this state
# names work that already exists, so it blocks nothing.
CLOSED = "CLOSED"

# The line the ticket breakdown writes an edge on where the tracker has no
# native relation to write it in: a heading or a sentence opening `Blocked by`,
# optionally marked up as one.
BLOCKED_BY_LINE = re.compile(
    r"^\s*(?:#{1,6}\s+)?\**blocked[ -]by\**\s*:?", re.IGNORECASE
)

# A line that continues the edge list under such a heading. Anything else ends
# it, so a `#12` further down the body is prose and not an edge.
EDGE_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")

# A ticket reference in a body: a bare number in this repository's tracker.
TICKET_REFERENCE = re.compile(r"(?<![0-9A-Za-z_/-])#(\d+)")

# The same reference written in a tracker's own terms, `owner/repo#12`. A run
# reads one repository's tracker and cannot tell such a reference in it from
# one somewhere else, so an edge written this way is refused rather than read
# — reading it would invent an edge, and dropping it would call a blocked
# ticket workable without saying so.
QUALIFIED_REFERENCE = re.compile(r"[\w.-]+/[\w.-]+#\d+")


class RunError(RuntimeError):
    """A git or tracker command the engine depends on failed."""


def fail(message: str, code: int = 1) -> int:
    """Print an error to stderr and return an exit code."""

    print(f"error: {message}", file=sys.stderr)
    return code


def emit(payload: dict[str, Any]) -> None:
    """Print one verb's JSON answer."""

    print(json.dumps(payload, indent=2))


def _capture(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a command in *cwd* without raising on a non-zero exit."""

    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def _output(cwd: Path, *args: str) -> str:
    """Run a command in *cwd* and return stdout. Raise RunError on failure."""

    result = _capture(cwd, *args)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RunError(detail or f"{' '.join(args)} failed")
    return result.stdout


def git(cwd: Path, *args: str) -> str:
    """Run git in *cwd* and return stdout."""

    return _output(cwd, "git", *args)


def git_ok(cwd: Path, *args: str) -> bool:
    """Return True when a git command exits 0."""

    return _capture(cwd, "git", *args).returncode == 0


def gh(cwd: Path, *args: str) -> str:
    """Run gh in *cwd* and return stdout."""

    return _output(cwd, "gh", *args)


def current_branch(cwd: Path) -> str:
    """Return the branch the run would work on."""

    name = git(cwd, "branch", "--show-current").strip()
    if not name:
        raise RunError("detached HEAD")

    return name


def default_branch(cwd: Path) -> str | None:
    """Return the repository's default branch, or None where it cannot be told.

    None is not a licence to work anywhere: it is the answer that stops a run
    from calling the branch in hand the default and refusing under a reason
    that is not true.
    """

    # What the remote calls its default settles it wherever there is one.
    try:
        ref = git(cwd, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").strip()
        if ref.startswith("refs/remotes/origin/"):
            return ref.removeprefix("refs/remotes/origin/")
    except RunError:
        pass

    # No remote to ask: the conventional names are the only other evidence.
    for candidate in ("main", "master"):
        if git_ok(cwd, "show-ref", "--verify", "--quiet", f"refs/heads/{candidate}"):
            return candidate

    return None


@dataclass
class Ticket:
    """One ticket in scope, as the tracker describes it.

    `blocked_by` holds the tickets that still block this one — a blocker the
    tracker reports closed names work that already exists and is left out, so
    the list is what remains to be waited for rather than the whole history of
    the edge.
    """

    number: int
    title: str
    url: str
    blocked_by: list[int]


@dataclass
class Plan:
    """What a run would work, and whether it may start.

    `ready` answers the second question alone: false with a `reason` means no
    work starts, while the scope is reported either way, so a dry run reads
    the tickets off a plan that refuses exactly as it reads them off one that
    does not.

    The scope is reported four ways over the same tickets. `waves` is the shape
    of the night, wave one being `workable`; `blocked` is everything else, and
    `never_workable` the part of it no wave holds because it waits on a cycle
    or on work outside the run.
    """

    verb: str
    ready: bool
    reason: str | None
    dry_run: bool
    branch: str
    default_branch: str | None
    label: str
    tickets: list[dict[str, Any]]
    workable: list[int]
    blocked: list[int]
    waves: list[list[int]]
    never_workable: list[int]


def still_blocks(state: str) -> bool:
    """Whether a blocker the tracker reports in *state* is work yet to exist."""

    return state.upper() != CLOSED


def body_edges(body: str) -> list[int]:
    """Return the tickets a `Blocked by` line in *body* names.

    The breakdown writes edges here where the tracker offers no relation to
    write them in.
    """

    # Take the text an edge can be written in: the rest of each `Blocked by`
    # line, and the list under it. The first line that is neither blank nor a
    # list item ends that list, or a ticket mentioned anywhere further down the
    # body would become an edge nobody wrote.
    lines = body.splitlines()
    written: list[str] = []
    for index, line in enumerate(lines):
        opening = BLOCKED_BY_LINE.match(line)
        if not opening:
            continue
        written.append(line[opening.end() :])
        for following in lines[index + 1 :]:
            if not following.strip():
                continue
            if not EDGE_LIST_ITEM.match(following):
                break
            written.append(following)

    # An edge nothing can read is never passed over in silence.
    for line in written:
        qualified = QUALIFIED_REFERENCE.search(line)
        if qualified:
            raise RunError(
                f"a `Blocked by` line names {qualified.group()}, and a run reads "
                "one repository's tracker: write the edge as #number"
            )

    return [
        int(number) for line in written for number in TICKET_REFERENCE.findall(line)
    ]


def ticket_state(cwd: Path, number: int, states: dict[int, str]) -> str:
    """Return the state the tracker reports ticket *number* in, remembering it.

    A body edge can name a ticket the scope does not hold, and its absence
    settles nothing: an open ticket outside the scope blocks, a closed one does
    not. So the tracker is asked, once per number, and *states* is what makes
    it once.
    """

    if number in states:
        return states[number]

    try:
        output = gh(cwd, "issue", "view", str(number), "--json", "number,state")
        state = str(json.loads(output)["state"]).upper()
    except (RunError, json.JSONDecodeError, KeyError) as exc:
        raise RunError(
            f"#{number} is named as a blocker, but the tracker cannot say "
            f"whether it is open or closed: {exc}"
        ) from exc

    states[number] = state
    return state


def unmet_blockers(
    cwd: Path, item: dict[str, Any], states: dict[int, str]
) -> list[int]:
    """Return the tickets still blocking *item*, as the tracker describes it.

    The tracker's own relation is the source wherever it carries an edge, and
    the body is read only where it carries none — a fallback, never a second
    source added to the first.
    """

    # The relation carries each blocker's state with it, so nothing is asked.
    nodes = item["blockedBy"]["nodes"]
    if nodes:
        return sorted(
            {int(node["number"]) for node in nodes if still_blocks(str(node["state"]))}
        )

    # A body edge is a bare number, so the state behind it is asked for.
    return sorted(
        number
        for number in set(body_edges(str(item["body"])))
        if still_blocks(ticket_state(cwd, number, states))
    )


def waves_of(tickets: list[Ticket]) -> tuple[list[list[int]], list[int]]:
    """Lay *tickets* out in waves, and name the ones no wave can hold.

    A wave is the tickets whose blockers are all settled by the waves before
    it, so wave one is the frontier. Waves stop as soon as one comes back
    empty, which is what a cycle or a blocker outside the scope produces: the
    tickets left over are workable in no wave of this run, and the walk ends
    rather than turning over a frontier that never grows.
    """

    waiting = {ticket.number: set(ticket.blocked_by) for ticket in tickets}
    settled: set[int] = set()
    waves: list[list[int]] = []
    while waiting:
        wave = sorted(
            number for number, blockers in waiting.items() if blockers <= settled
        )
        if not wave:
            break

        waves.append(wave)
        settled.update(wave)
        for number in wave:
            del waiting[number]

    return waves, sorted(waiting)


def tickets_in_scope(cwd: Path) -> list[Ticket]:
    """Return the open tickets carrying the ready label, oldest first.

    Ordered by number rather than by whatever order the tracker answers in, so
    that a plan is the same plan on two invocations with nothing changed.
    """

    # Ask the tracker for the whole scope, and for it by label: a ticket
    # without that label is unfinished thinking and is never worked.
    output = gh(
        cwd,
        "issue",
        "list",
        "--label",
        READY_LABEL,
        "--state",
        "open",
        "--json",
        "number,title,url,body,blockedBy",
        "--limit",
        str(TICKET_PAGE),
    )

    # The tracker is a boundary: an unreadable answer, or a full page that may
    # be hiding the rest of the scope, has to name itself rather than pass as
    # a plan somebody would act on.
    try:
        listed = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RunError(f"the tracker returned no readable ticket list: {exc}") from exc
    if len(listed) >= TICKET_PAGE:
        raise RunError(
            f"the tracker returned a full page of {TICKET_PAGE} tickets, "
            "so the scope cannot be read completely"
        )

    # Every ticket in scope is open, the query having asked for open ones, so
    # an edge that points into the scope costs the tracker no second question.
    states = {int(item["number"]): "OPEN" for item in listed}
    tickets = [
        Ticket(
            number=int(item["number"]),
            title=str(item["title"]),
            url=str(item["url"]),
            blocked_by=unmet_blockers(cwd, item, states),
        )
        for item in listed
    ]
    return sorted(tickets, key=lambda ticket: ticket.number)


def build_plan(cwd: Path, *, dry_run: bool) -> Plan:
    """Gather what a run in *cwd* would work, and whether it may start."""

    # The graph is the shape of the night: wave one is what may start now, and
    # everything else is waiting on work inside it or on work outside the run.
    branch = current_branch(cwd)
    default = default_branch(cwd)
    tickets = tickets_in_scope(cwd)
    waves, never_workable = waves_of(tickets)
    workable = waves[0] if waves else []
    frontier = set(workable)
    plan = Plan(
        verb="plan",
        ready=True,
        reason=None,
        dry_run=dry_run,
        branch=branch,
        default_branch=default,
        label=READY_LABEL,
        tickets=[asdict(ticket) for ticket in tickets],
        workable=workable,
        blocked=[ticket.number for ticket in tickets if ticket.number not in frontier],
        waves=waves,
        never_workable=never_workable,
    )

    # A run works the branch the developer left it on, so the default branch
    # is the one place an unattended night must never land — and a default
    # nothing can name is a refusal too, not a branch to guess at.
    if dry_run:
        plan.ready = False
        plan.reason = "dry run: nothing is started"
    elif default is None:
        plan.ready = False
        plan.reason = (
            "cannot tell which branch is the default; "
            "name it with `git remote set-head origin --auto`"
        )
    elif branch == default:
        plan.ready = False
        plan.reason = f"on the default branch '{branch}'"
    elif not tickets:
        plan.ready = False
        plan.reason = f"no open ticket carries '{READY_LABEL}'"
    elif not workable:
        plan.ready = False
        plan.reason = (
            "no ticket is workable: every ticket in scope waits on work "
            "this run cannot reach"
        )

    return plan


def cmd_plan(cwd: Path, *, dry_run: bool) -> int:
    """Print the plan, and answer whether work may start."""

    try:
        plan = build_plan(cwd, dry_run=dry_run)
    except RunError as exc:
        return fail(str(exc))

    emit(asdict(plan))
    return 0 if plan.ready else 2


def cmd_record(args: argparse.Namespace) -> int:
    """Print the outcome recorded against one ticket.

    Nothing outlives the call yet: run state is what remembers an outcome, and
    it arrives with the verb that has outcomes to remember.
    """

    emit(
        {
            "verb": "record",
            "ticket": args.ticket,
            "outcome": args.outcome,
            "commit": args.commit,
        }
    )
    return 0


def cmd_report(cwd: Path) -> int:
    """Print the run report: the tickets in scope, and what was recorded."""

    try:
        tickets = tickets_in_scope(cwd)
    except RunError as exc:
        return fail(str(exc))

    emit(
        {
            "verb": "report",
            "label": READY_LABEL,
            "tickets": [asdict(ticket) for ticket in tickets],
            "recorded": [],
        }
    )
    return 0


def add_yes_flag(parser: argparse.ArgumentParser) -> None:
    """Add --yes to a verb.

    No question is asked here — a script has no terminal to ask one in — but
    every verb takes the flag, so the skill can pass the user's own arguments
    straight through without turning `--yes` into a crash (ADR-0029).
    """

    parser.add_argument("--yes", action="store_true")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the run CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="verb", required=True)

    plan = sub.add_parser("plan", help="Print what a run would work.")
    plan.add_argument("--dry-run", action="store_true")
    add_yes_flag(plan)

    record = sub.add_parser("record", help="Record one ticket's outcome.")
    record.add_argument("--ticket", required=True, type=int)
    record.add_argument("--outcome", required=True, choices=OUTCOMES)
    record.add_argument("--commit")
    add_yes_flag(record)

    add_yes_flag(sub.add_parser("report", help="Print the consolidated report."))

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Dispatch one verb. Return an exit code."""

    args = parse_args(argv if argv is not None else sys.argv[1:])
    cwd = Path.cwd()
    if args.verb == "plan":
        return cmd_plan(cwd, dry_run=args.dry_run)
    if args.verb == "record":
        return cmd_record(args)
    return cmd_report(cwd)


if __name__ == "__main__":
    raise SystemExit(main())
