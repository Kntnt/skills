# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Plan, claim, record, and report an unattended run over the tracker's tickets."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable
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
DONE = "done"
FAILED = "failed"
CONFLICTED = "conflicted"
OUTCOMES = (DONE, FAILED, CONFLICTED)

# What each recorded outcome says on the ticket it is recorded against. The
# machine-readable half is the marker; this is the half a developer reads.
NOTES = {
    DONE: (
        "Recorded by an unattended run: built and then verified independently "
        "against this ticket's acceptance criteria."
    ),
    FAILED: (
        "Recorded by an unattended run: verification did not pass. The ticket "
        "is not retried — a rerun would have identical conditions."
    ),
    CONFLICTED: (
        "Recorded by an unattended run: this ticket's work collided with "
        "another ticket's and the collision was not repaired."
    ),
}

# The marker every recorded outcome carries, so what a run wrote on a ticket
# is machine-readable and not only prose somebody has to interpret.
MARKER = "kntnt-orchestrate"

# The same marker read back off a ticket. A recorded outcome outlives the
# session that produced it because the tracker is where it was written, which
# is what lets one run's record change the next run's plan without either of
# them sharing any memory (ADR-0051).
RECORDED_OUTCOME = re.compile(
    rf"<!--\s*{MARKER}\s+outcome=(\S+?)(?:\s+commit=(\S+?))?\s*-->"
)

# Who a claim assigns the ticket to. The tracker's own relation for "somebody
# is on this" is the claim: it needs no label created and no convention
# agreed, and a ticket a human has taken is one an unattended run must leave
# alone for exactly the same reason.
CLAIM_ASSIGNEE = "@me"

# What a run calls the state it keeps in the session's scratch directory. One
# file per session, named rather than generated, so a re-invocation in that
# same session finds what the last one left (ADR-0052).
STATE_FILE = "kntnt-orchestrate.json"

# What the tracker calls a ticket that is finished. A blocker in this state
# names work that already exists, so it blocks nothing.
CLOSED = "CLOSED"

# The line the ticket breakdown writes an edge on where the tracker has no
# native relation to write it in: a heading or a sentence opening `Blocked by`,
# optionally marked up as one.
BLOCKED_BY_LINE = re.compile(
    r"^\s*(?:#{1,6}\s+)?\**blocked[ -]by\**\s*:?", re.IGNORECASE
)

# The line the breakdown names a ticket's parent spec on, written the same two
# ways: a heading with the reference under it, or a sentence carrying it.
PARENT_LINE = re.compile(r"^\s*(?:#{1,6}\s+)?\**parent\b\**\s*:?", re.IGNORECASE)

# A line that continues the list under such a heading: an item, or a reference
# standing on its own line. Anything else ends it, so a `#12` further down the
# body is prose and not an edge.
EDGE_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")

# A ticket reference in a body: a bare number in this repository's tracker.
TICKET_REFERENCE = re.compile(r"(?<![0-9A-Za-z_/-])#(\d+)")

# A line holding references and nothing else, which is how the breakdown
# writes a single reference under a heading.
BARE_REFERENCE = re.compile(r"^(?:\s*#\d+\s*,?)+$")

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

    `body` is the ticket as it was filed, carried whole because the brief a
    building subagent gets carries the body and never a summary of it, and
    `parent` is the spec whose testing decisions are read before any test.
    `claimed_by` is who the tracker has it assigned to: non-empty means a
    session or a person already has it, and the logins are what tells a claim
    this run left behind from one somebody else took.

    `outcome` is what a run has already recorded against this ticket, read back
    off the tracker, with `commit` the commit that outcome named. Both are None
    where nothing has been recorded. A ticket carrying an outcome is settled:
    it is never offered again, and what waits on it is stranded rather than
    workable.
    """

    number: int
    title: str
    url: str
    body: str
    parent: int | None
    claimed_by: list[str]
    blocked_by: list[int]
    outcome: str | None
    commit: str | None


@dataclass
class RunState:
    """What one run remembers of itself between invocations.

    It is remembered, never relied on: every answer this engine gives is read
    off the tracker and the branch, and the same answer comes back where this
    is absent (ADR-0051). What it buys is the one thing the tracker cannot
    say — which of the claims standing in this developer's name are this run's
    own, an interrupted run and a session running in parallel being the same
    login on the same ticket.

    `branch` and `label` are what the state is of: a scratch directory outlives
    a checkout, and a document describing another branch describes another run.
    `login` is who the tracker last said this run claims as, kept so a verb
    that needs it does not ask again. `claimed` is the tickets this run has
    taken and not yet recorded an outcome against. `base` is the commit its
    work sits on top of, which is the branch's half of the same account and is
    worked out afresh every time rather than read back, so a state that is gone
    cannot make it disagree with the branch it describes.
    """

    branch: str
    label: str
    login: str | None
    claimed: list[int]
    base: str


def state_file(directory: str | None) -> Path | None:
    """Return the file the run's state lives in, or None where there is none.

    The harness knows where this session's scratch directory is and the engine
    does not, so the directory is passed in. None is not an error: the state is
    an optimisation, and a harness that offers no such directory costs a run
    nothing but the tracker call the state would have saved.
    """

    return Path(directory).expanduser() / STATE_FILE if directory else None


def read_state(path: Path | None, branch: str) -> RunState | None:
    """Return what the run remembered of itself, or None where nothing does.

    The file is a boundary like any other: a session killed mid-write, a hand
    edit, or a scratch directory carried over to another branch all produce
    something this cannot read, and each is answered the same way — as no state
    at all, which is a state the engine already knows how to work from.
    """

    if path is None:
        return None

    try:
        stored = json.loads(path.read_text(encoding="utf-8"))
        if stored["branch"] != branch or stored["label"] != READY_LABEL:
            return None
        return RunState(
            branch=str(stored["branch"]),
            label=str(stored["label"]),
            login=None if stored["login"] is None else str(stored["login"]),
            claimed=[int(number) for number in stored["claimed"]],
            base=str(stored["base"]),
        )
    except (OSError, TypeError, ValueError, KeyError):
        return None


def write_state(path: Path | None, state: RunState) -> str | None:
    """Store *state* and return where, or None where it was not stored.

    A scratch directory that cannot be written to is not a reason to stop: the
    run goes on reading the tracker, and the next invocation rebuilds what this
    one could not leave behind.
    """

    if path is None:
        return None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(state), indent=2) + "\n", encoding="utf-8")
    except OSError:
        return None

    return str(path)


def remembered_state(path: Path | None, cwd: Path) -> RunState | None:
    """Return what the run remembered, for a verb that has not read the branch.

    The branch is what says whether a document describes this run, and a verb
    working one ticket has no other reason to ask for it — so a repository that
    cannot answer is read as no state, which is a state the engine works from.
    """

    if path is None:
        return None

    try:
        return read_state(path, current_branch(cwd))
    except RunError:
        return None


def _amend_claims(
    path: Path | None, cwd: Path, change: Callable[[set[int]], set[int]]
) -> None:
    """Put the run's remembered claims through *change*, where it remembers any.

    Only a verb that has read the whole scope writes the document; this one
    amends the document that is already there, and does nothing where there is
    none. A file written from a verb that knows about one ticket would say the
    run's other claims are somebody else's, which is the one thing the state is
    kept to prevent.
    """

    state = remembered_state(path, cwd)
    if state is None:
        return

    state.claimed = sorted(change(set(state.claimed)))
    write_state(path, state)


def remember_claim(path: Path | None, cwd: Path, number: int) -> None:
    """Add ticket *number* to what the run remembers claiming."""

    _amend_claims(path, cwd, lambda claims: claims | {number})


def forget_claim(path: Path | None, cwd: Path, number: int) -> None:
    """Drop ticket *number* from what the run remembers claiming.

    A recorded ticket is settled, and a settled ticket is not one that a
    re-invocation picks up where this run left off.
    """

    _amend_claims(path, cwd, lambda claims: claims - {number})


def my_login(cwd: Path, remembered: RunState | None) -> str:
    """Return who the tracker has this run authenticated as.

    Asked only where a claim in scope makes it matter, and remembered across
    the verbs of one run. A run told nothing about who it is cannot tell its
    own interrupted claim from another session's, and neither guess is one an
    unattended night may make: it stops instead.
    """

    if remembered and remembered.login:
        return remembered.login

    try:
        login = gh(cwd, "api", "user", "--jq", ".login").strip()
    except RunError as exc:
        raise RunError(
            "a ticket in scope is claimed, and the tracker cannot say who this "
            f"run would be claiming as: {exc}"
        ) from exc
    if not login:
        raise RunError(
            "a ticket in scope is claimed, and the tracker named nobody when "
            "asked who this run would be claiming as"
        )

    return login


@dataclass
class Plan:
    """What a run would work, and whether it may start.

    `ready` answers the second question alone: false with a `reason` means no
    work starts, while the scope is reported either way, so a dry run reads
    the tickets off a plan that refuses exactly as it reads them off one that
    does not.

    The scope is reported over the same tickets several ways. `recorded` is
    what a run has already settled and `stranded` what waits on a settled
    failure; neither is laid out in a wave, because neither can be worked.
    `waves` is the shape of what remains as the graph dictates it; `blocked` is
    everything outside wave one, and `never_workable` the part of it no wave
    holds because it waits on a cycle or on work outside the run. `claimed`
    cuts across all of that: a ticket somebody already has is not this run's to
    start, so `workable` is wave one less whatever is claimed. `resuming` is
    the other half of that reading — the tickets this run itself claimed and
    was interrupted before recording, which are in `workable` like any other,
    the claim on them being already its own.

    `model` is the model the building subagents run on, and `state` is where
    the run left what it remembers of itself, both carried here because the
    plan is where the run says what it is about to do.
    """

    verb: str
    ready: bool
    reason: str | None
    dry_run: bool
    model: str | None
    state: str | None
    branch: str
    default_branch: str | None
    label: str
    tickets: list[dict[str, Any]]
    workable: list[int]
    claimed: list[int]
    resuming: list[int]
    recorded: list[int]
    stranded: list[int]
    blocked: list[int]
    waves: list[list[int]]
    never_workable: list[int]


def still_blocks(state: str) -> bool:
    """Whether a blocker the tracker reports in *state* is work yet to exist."""

    return state.upper() != CLOSED


def references_under(body: str, opening: re.Pattern[str], heading: str) -> list[int]:
    """Return the tickets named under each *opening* line in *body*.

    The breakdown writes both a ticket's blocking edges and its parent this
    way, where the tracker offers no relation to write them in.
    """

    # Take the text a reference can be written in: the rest of each opening
    # line, and the list under it. The first line that is neither blank, a list
    # item, nor a reference standing alone ends that list, or a ticket
    # mentioned anywhere further down the body would become one nobody wrote.
    lines = body.splitlines()
    written: list[str] = []
    for index, line in enumerate(lines):
        found = opening.match(line)
        if not found:
            continue
        written.append(line[found.end() :])
        for following in lines[index + 1 :]:
            if not following.strip():
                continue
            if not EDGE_LIST_ITEM.match(following) and not BARE_REFERENCE.match(
                following
            ):
                break
            written.append(following)

    # A reference nothing can read is never passed over in silence.
    for line in written:
        qualified = QUALIFIED_REFERENCE.search(line)
        if qualified:
            raise RunError(
                f"a `{heading}` line names {qualified.group()}, and a run reads "
                "one repository's tracker: write it as #number"
            )

    return [
        int(number) for line in written for number in TICKET_REFERENCE.findall(line)
    ]


def body_edges(body: str) -> list[int]:
    """Return the tickets a `Blocked by` line in *body* names."""

    return references_under(body, BLOCKED_BY_LINE, "Blocked by")


def body_parent(body: str) -> int | None:
    """Return the spec a `Parent` line in *body* names, if it names one.

    A ticket has one parent. Two named under that heading is a ticket nobody
    can read, and picking whichever came first would send a builder off to
    read the wrong spec without saying so.
    """

    named = references_under(body, PARENT_LINE, "Parent")
    if len(named) > 1:
        raise RunError(
            "a `Parent` line names more than one ticket "
            f"({', '.join(f'#{number}' for number in named)}): a ticket has one parent"
        )

    return named[0] if named else None


def holders_of(item: dict[str, Any]) -> list[str]:
    """Return who the tracker has *item* assigned to, which is who claims it."""

    return [str(holder["login"]) for holder in item["assignees"]]


def recorded_against(item: dict[str, Any]) -> tuple[str | None, str | None]:
    """Return the outcome a run recorded on *item*, and the commit it named.

    The tracker is a boundary and a comment is prose anybody can write, so only
    an outcome this engine knows how to record is read back — a marker naming
    anything else is somebody else's writing and settles nothing. The last one
    wins, that being the outcome as it now stands.
    """

    # Read every marker and keep the last, that being the outcome as it stands.
    outcome: str | None = None
    commit: str | None = None
    for comment in item["comments"]:
        found = RECORDED_OUTCOME.search(str(comment["body"]))
        if found and found.group(1) in OUTCOMES:
            outcome, commit = found.group(1), found.group(2)

    return outcome, commit


def ticket_view(cwd: Path, number: int, fields: str) -> dict[str, Any]:
    """Return what the tracker says about ticket *number*.

    Raises a RunError carrying what the tracker said, for the caller to put in
    the terms of whatever it was about to do with the answer.
    """

    output = gh(cwd, "issue", "view", str(number), "--json", fields)
    try:
        answer: dict[str, Any] = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RunError(str(exc)) from exc

    return answer


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
        state = str(ticket_view(cwd, number, "number,state")["state"]).upper()
    except (RunError, KeyError) as exc:
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


def parent_of(item: dict[str, Any]) -> int | None:
    """Return the spec *item* belongs to, as the tracker describes it.

    The tracker's own relation is the source wherever it carries one, and the
    body is read only where it carries none — the same fallback, and the same
    order, as a blocking edge.
    """

    native = item["parent"]
    if native:
        return int(native["number"])

    return body_parent(str(item["body"]))


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


def stranded_behind(tickets: list[Ticket]) -> list[int]:
    """Return the tickets waiting, however far back, on one that did not pass.

    This is the outcome a naive loop drops without saying so. A ticket whose
    blocker failed cannot be worked — the work it builds on does not exist —
    and it is not blocked in the ordinary sense either, because nothing left in
    the run will ever unblock it. It comes back stranded instead: out of the
    frontier, and still in the account.
    """

    # Walk the edges the other way round, so a settled ticket names what waited
    # on it rather than the other way about.
    dependents: dict[int, list[int]] = {}
    for ticket in tickets:
        for blocker in ticket.blocked_by:
            dependents.setdefault(blocker, []).append(ticket.number)

    # Stranding spreads from the tickets that did not pass, transitively: done
    # is work that exists and holds nothing back behind it. A ticket carrying
    # an outcome of its own is settled by that outcome and is never restated as
    # stranded.
    recorded = {ticket.number for ticket in tickets if ticket.outcome}
    stranded: set[int] = set()
    spreading = [
        ticket.number for ticket in tickets if ticket.outcome not in (None, DONE)
    ]
    while spreading:
        for dependent in dependents.get(spreading.pop(), []):
            if dependent not in recorded and dependent not in stranded:
                stranded.add(dependent)
                spreading.append(dependent)

    return sorted(stranded)


def listed_tickets(cwd: Path, *query: str) -> list[dict[str, Any]]:
    """Return what the tracker answers a ticket query with.

    The page size is asked for here rather than by the caller, because it is
    what the guard below is written against: a caller free to choose its own
    limit is a caller that can switch that guard off without meaning to.
    """

    # Every query is by label, a ticket without one being unfinished thinking.
    output = gh(
        cwd,
        "issue",
        "list",
        "--label",
        READY_LABEL,
        "--limit",
        str(TICKET_PAGE),
        *query,
    )

    # The tracker is a boundary: an unreadable answer, or a full page that may
    # be hiding the rest of the scope, has to name itself rather than pass as a
    # plan somebody would act on.
    try:
        listed: list[dict[str, Any]] = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RunError(f"the tracker returned no readable ticket list: {exc}") from exc
    if len(listed) >= TICKET_PAGE:
        raise RunError(
            f"the tracker returned a full page of {TICKET_PAGE} tickets, "
            "so the scope cannot be read completely"
        )

    return listed


def ticket_from(
    item: dict[str, Any],
    *,
    blocked_by: list[int],
    outcome: str | None,
    commit: str | None,
) -> Ticket:
    """Build one ticket out of what the tracker answered about it.

    Everything readable straight off that answer is read here. What costs the
    tracker a second question, or a judgement about the graph, is settled by
    the caller and passed in.
    """

    return Ticket(
        number=int(item["number"]),
        title=str(item["title"]),
        url=str(item["url"]),
        body=str(item["body"]),
        parent=parent_of(item),
        claimed_by=holders_of(item),
        blocked_by=blocked_by,
        outcome=outcome,
        commit=commit,
    )


def tickets_in_scope(cwd: Path) -> list[Ticket]:
    """Return the open tickets carrying the ready label, oldest first.

    Ordered by number rather than by whatever order the tracker answers in, so
    that a plan is the same plan on two invocations with nothing changed.
    """

    # Ask the tracker for the whole scope, and for it by label: a ticket
    # without that label is unfinished thinking and is never worked.
    listed = listed_tickets(
        cwd,
        "--state",
        "open",
        "--json",
        "number,title,url,body,parent,assignees,blockedBy,comments",
    )

    # Every ticket in scope is open, the query having asked for open ones, so
    # an edge that points into the scope costs the tracker no second question.
    states = {int(item["number"]): "OPEN" for item in listed}

    # A body that cannot be read stops the plan, and says which ticket to go
    # and fix — the reference alone would leave the scope to be searched by
    # hand for whichever ticket carries it.
    tickets = []
    for item in listed:
        number = int(item["number"])
        try:
            outcome, commit = recorded_against(item)
            tickets.append(
                ticket_from(
                    item,
                    blocked_by=unmet_blockers(cwd, item, states),
                    outcome=outcome,
                    commit=commit,
                )
            )
        except RunError as exc:
            raise RunError(f"#{number}: {exc}") from exc

    return sorted(tickets, key=lambda ticket: ticket.number)


def tickets_recorded_done(cwd: Path) -> list[Ticket]:
    """Return the tickets a run closed as done, oldest first.

    Done is the one outcome that takes a ticket out of the open scope, so the
    report would lose exactly the tickets it most needs to name if it read that
    scope alone. They are found by the claim that started them and the marker
    that ended them: a ticket closed by hand carries neither and was never this
    run's to account for, and counting it done would be a report nobody can
    check.
    """

    # Ask for the closed half of the scope, narrowed to the tickets this
    # machine's runs took: without that the query is every ticket the label has
    # ever closed, which grows past a page and can only refuse.
    listed = listed_tickets(
        cwd,
        "--state",
        "closed",
        "--assignee",
        CLAIM_ASSIGNEE,
        "--json",
        "number,title,url,body,parent,assignees,comments",
    )

    # No edge is read off a finished ticket. There is nothing left for it to
    # wait for, and asking the tracker about a blocker named in its body is a
    # question whose answer could only ever fail the report.
    tickets = []
    for item in listed:
        number = int(item["number"])
        outcome, commit = recorded_against(item)
        if outcome != DONE:
            continue
        try:
            tickets.append(
                ticket_from(item, blocked_by=[], outcome=outcome, commit=commit)
            )
        except RunError as exc:
            raise RunError(f"#{number}: {exc}") from exc

    return sorted(tickets, key=lambda ticket: ticket.number)


def run_base(cwd: Path, tickets: list[Ticket]) -> str:
    """Return the commit this run's work sits on top of.

    This is the branch's half of a run's account: what the night added is the
    diff from here to the head. It is worked out from the branch every time
    rather than read back from what a run remembered, so a session whose
    scratch directory is gone answers exactly as the session that did the work
    did — the commit all of this run's recorded work descends from. Where the
    run has recorded nothing yet there is no work to sit on, and the head is
    where its first ticket will land.
    """

    # A commit a run recorded on another branch is not this branch's history,
    # and a branch that does not hold it can say nothing about where work began.
    recorded = [ticket.commit for ticket in tickets if ticket.commit]
    on_branch = [
        commit
        for commit in recorded
        if git_ok(cwd, "merge-base", "--is-ancestor", commit, "HEAD")
    ]
    if not on_branch:
        return git(cwd, "rev-parse", "HEAD").strip()

    # What they all descend from is the oldest of them where the run committed
    # one ticket after another, and an earlier commit where the branch forked
    # and came back — either way a base the whole run is contained by.
    oldest = git(cwd, "merge-base", "--octopus", *on_branch).strip()

    # A run whose first recorded commit is the repository's root sits on that
    # commit itself: there is nothing before it to name.
    try:
        return git(cwd, "rev-parse", "--verify", f"{oldest}^").strip()
    except RunError:
        return oldest


def build_plan(
    cwd: Path, *, dry_run: bool, model: str | None, state_path: Path | None
) -> Plan:
    """Gather what a run in *cwd* would work, and whether it may start."""

    # What earlier waves of this run wrote down is where the plan starts, not
    # where it ends: a ticket already settled is never offered again, and what
    # waits on a settled failure is stranded rather than worked on top of code
    # that was never built.
    branch = current_branch(cwd)
    default = default_branch(cwd)
    remembered = read_state(state_path, branch)
    tickets = tickets_in_scope(cwd)
    recorded = [ticket.number for ticket in tickets if ticket.outcome]
    stranded = stranded_behind(tickets)

    # The graph is the shape of what is left: wave one is what may start now,
    # and everything else waits on work inside it or on work outside the run.
    settled = set(recorded).union(stranded)
    waves, never_workable = waves_of(
        [ticket for ticket in tickets if ticket.number not in settled]
    )
    frontier = set(waves[0]) if waves else set()

    # A claim standing in this run's own name, over a ticket it took and never
    # recorded, is where an interruption left off: the run picks it up rather
    # than treating it as taken. Every other claim is somebody else's session
    # or a person, and leaves the frontier without leaving the account, so
    # nothing disappears by being taken.
    held = [ticket for ticket in tickets if ticket.claimed_by and not ticket.outcome]
    login = my_login(cwd, remembered) if held else None
    resuming = [
        ticket.number
        for ticket in held
        if ticket.claimed_by == [login]
        and (remembered is None or ticket.number in remembered.claimed)
    ]
    claimed = [ticket.number for ticket in held if ticket.number not in resuming]
    workable = sorted(frontier.difference(claimed))

    plan = Plan(
        verb="plan",
        ready=True,
        reason=None,
        dry_run=dry_run,
        model=model,
        state=None,
        branch=branch,
        default_branch=default,
        label=READY_LABEL,
        tickets=[asdict(ticket) for ticket in tickets],
        workable=workable,
        claimed=claimed,
        resuming=resuming,
        recorded=recorded,
        stranded=stranded,
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
    elif not frontier:
        plan.ready = False
        plan.reason = (
            "no ticket is workable: every ticket in scope is already recorded, "
            "stranded behind a failure, or waiting on work this run cannot reach"
        )
    elif not workable:
        plan.ready = False
        plan.reason = (
            "every workable ticket is already claimed, so another run or a "
            "person has all the work this one could start"
        )

    # A run that may start leaves what it remembers of itself where this
    # session's scratch is, written from here because this is the verb that has
    # read the whole scope. A run that may not starts nothing, and a dry run
    # that left a file behind would have started something after all. A login
    # nothing asked for this time is the one already remembered.
    if plan.ready:
        plan.state = write_state(
            state_path,
            RunState(
                branch=branch,
                label=READY_LABEL,
                login=login or (remembered.login if remembered else None),
                claimed=resuming,
                base=run_base(cwd, tickets),
            ),
        )

    return plan


def cmd_plan(
    cwd: Path, *, dry_run: bool, model: str | None, state_path: Path | None
) -> int:
    """Print the plan, and answer whether work may start."""

    try:
        plan = build_plan(cwd, dry_run=dry_run, model=model, state_path=state_path)
    except RunError as exc:
        return fail(str(exc))

    emit(asdict(plan))
    return 0 if plan.ready else 2


def claim_refusal(
    number: int,
    ticket: dict[str, Any],
    mine: str | None,
    remembered: RunState | None,
) -> str | None:
    """Return why *ticket* may not be claimed, or None where it may.

    This is the last gate before a subagent is briefed, so it asks the tracker
    itself rather than trusting a plan that may be minutes old — the whole
    point of a claim is the session that started while this one was reading.
    That is also why a claim in this run's own name is not enough on its own:
    an interrupted run of this developer's and one they started in parallel
    leave the same login behind, and only a claim the run remembers taking is
    its own to pick up. Where it remembers nothing there is nothing to tell
    them apart by, and the claim is read as the interrupted one it usually is.
    """

    if str(ticket["state"]).upper() == CLOSED:
        return f"#{number} is closed"

    if READY_LABEL not in [str(label["name"]) for label in ticket["labels"]]:
        return f"#{number} does not carry '{READY_LABEL}'"

    holders = holders_of(ticket)
    if not holders:
        return None

    if holders != [mine]:
        return f"#{number} is already claimed by {', '.join(holders)}"

    if remembered and number not in remembered.claimed:
        return f"#{number} is claimed by a run this one did not start"

    return None


def cmd_claim(cwd: Path, number: int, state_path: Path | None) -> int:
    """Take one ticket on the tracker, before any work on it starts."""

    try:
        ticket = ticket_view(cwd, number, "number,state,labels,assignees")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")

    # Who this run is only matters where somebody already holds the ticket,
    # that being the one question a login answers, so an unclaimed ticket costs
    # the tracker nothing to take.
    holders = holders_of(ticket)
    remembered = remembered_state(state_path, cwd)
    try:
        mine = my_login(cwd, remembered) if holders else None
    except RunError as exc:
        return fail(str(exc))

    # A refusal is an answer and not a breakage: the second session started in
    # parallel reads it, skips the ticket, and works the next one.
    refusal = claim_refusal(number, ticket, mine, remembered)
    if refusal:
        emit({"verb": "claim", "ticket": number, "claimed": False, "reason": refusal})
        return 2

    # A ticket this run already holds is already claimed, and asking the
    # tracker to assign it again would write nothing it does not already say.
    if not holders:
        try:
            gh(cwd, "issue", "edit", str(number), "--add-assignee", CLAIM_ASSIGNEE)
        except RunError as exc:
            return fail(f"#{number} could not be claimed: {exc}")

    remember_claim(state_path, cwd, number)
    emit({"verb": "claim", "ticket": number, "claimed": True, "reason": None})
    return 0


def outcome_note(outcome: str, commit: str | None) -> str:
    """Render what is written on a ticket when its outcome is recorded.

    One line, carrying a marker a later run can read the outcome back out of
    and prose the developer reading the ticket can read instead.
    """

    named = f" commit={commit}" if commit else ""
    return f"<!-- {MARKER} outcome={outcome}{named} --> {NOTES[outcome]}"


def cmd_record(
    cwd: Path, number: int, outcome: str, named: str | None, state_path: Path | None
) -> int:
    """Store ticket *number*'s *outcome* and the commit that carries it.

    The tracker is the store, because it is the one place an outcome outlives
    the session that produced it and the one place the developer will look.
    """

    # Both halves of a done outcome are settled before the tracker is touched:
    # a ticket closed on a commit nothing can resolve is a report nobody can
    # check, which is the one thing an unattended run may not produce.
    if outcome == DONE and not named:
        return fail(f"recording #{number} done needs the commit that carries it")

    commit = None
    if named:
        try:
            commit = git(cwd, "rev-parse", "--verify", f"{named}^{{commit}}").strip()
        except RunError:
            return fail(f"this repository has no commit {named}")

    # The tracker is asked for the ticket before anything is written to it, so
    # a number it cannot answer for is refused rather than half-recorded.
    try:
        ticket_view(cwd, number, "number,state")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")

    # Done is the only outcome that closes a ticket, and the Skill records it
    # only where a separate subagent has verified the work — so there is no
    # path from a builder's own report to a closed ticket.
    note = outcome_note(outcome, commit)
    try:
        if outcome == DONE:
            gh(cwd, "issue", "close", str(number), "--comment", note)
        else:
            gh(cwd, "issue", "comment", str(number), "--body", note)
    except RunError as exc:
        return fail(f"#{number} could not be recorded: {exc}")

    forget_claim(state_path, cwd, number)

    emit(
        {
            "verb": "record",
            "ticket": number,
            "outcome": outcome,
            "commit": commit,
            "closed": outcome == DONE,
        }
    )
    return 0


def cmd_report(cwd: Path) -> int:
    """Print the consolidated report: every ticket in scope, and its outcome.

    One report rather than a running commentary, and every ticket in scope in
    it exactly once — a ticket the run drops in silence is one the developer
    will not know to pick up. The five outcomes partition the scope by
    construction: what a run recorded, then what a recorded failure stranded,
    then everything left, which is everything this run never had on its
    frontier — held by a cycle, by work outside the run, by another session's
    claim, or by the run stopping before its wave came round.
    """

    # The scope is asked for twice, because done is the one outcome that takes
    # a ticket out of the open one by closing it.
    try:
        branch = current_branch(cwd)
        open_scope = tickets_in_scope(cwd)
        tickets = sorted(
            open_scope + tickets_recorded_done(cwd), key=lambda ticket: ticket.number
        )
        base = run_base(cwd, tickets)
    except RunError as exc:
        return fail(str(exc))

    # Stranding is read off the open scope alone: a ticket that is finished has
    # no unmet blocker left to strand anything behind.
    recorded = {
        outcome: [ticket.number for ticket in tickets if ticket.outcome == outcome]
        for outcome in OUTCOMES
    }
    stranded = stranded_behind(open_scope)
    accounted = set(stranded).union(*recorded.values())

    emit(
        {
            "verb": "report",
            "label": READY_LABEL,
            "branch": branch,
            "base": base,
            "tickets": [asdict(ticket) for ticket in tickets],
            "done": recorded[DONE],
            "failed": recorded[FAILED],
            "conflicted": recorded[CONFLICTED],
            "stranded": stranded,
            "never_on_frontier": [
                ticket.number for ticket in tickets if ticket.number not in accounted
            ],
        }
    )
    return 0


def add_shared_flags(parser: argparse.ArgumentParser) -> None:
    """Add the flags every verb takes to one of them.

    No question is asked here — a script has no terminal to ask one in — but
    every verb takes `--yes`, so the skill can pass the user's own arguments
    straight through without turning it into a crash (ADR-0029). `--state-dir`
    is on every verb for the other half of the same reason: the harness knows
    where this session's scratch directory is and the engine does not, and a
    verb that could not be told would be a verb whose part of the run is
    forgotten. There is no flag for resuming, because the ordinary invocation
    is the resume (ADR-0052).
    """

    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--state-dir")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the run CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="verb", required=True)

    plan = sub.add_parser("plan", help="Print what a run would work.")
    plan.add_argument("--dry-run", action="store_true")
    plan.add_argument("--model")
    add_shared_flags(plan)

    claim = sub.add_parser("claim", help="Take one ticket before working it.")
    claim.add_argument("--ticket", required=True, type=int)
    add_shared_flags(claim)

    record = sub.add_parser("record", help="Record one ticket's outcome.")
    record.add_argument("--ticket", required=True, type=int)
    record.add_argument("--outcome", required=True, choices=OUTCOMES)
    record.add_argument("--commit")
    add_shared_flags(record)

    add_shared_flags(sub.add_parser("report", help="Print the consolidated report."))

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Dispatch one verb. Return an exit code."""

    args = parse_args(argv if argv is not None else sys.argv[1:])
    cwd = Path.cwd()
    state_path = state_file(args.state_dir)
    if args.verb == "plan":
        return cmd_plan(
            cwd, dry_run=args.dry_run, model=args.model, state_path=state_path
        )
    if args.verb == "claim":
        return cmd_claim(cwd, args.ticket, state_path)
    if args.verb == "record":
        return cmd_record(cwd, args.ticket, args.outcome, args.commit, state_path)
    return cmd_report(cwd)


if __name__ == "__main__":
    raise SystemExit(main())
