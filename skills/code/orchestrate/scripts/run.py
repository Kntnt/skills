# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Plan, claim, record, and report an unattended run over the tracker's tickets."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, TypedDict, cast

# The label that says the thinking behind a ticket is finished. A ticket
# without it is never planned, never claimed, and never built.
READY_LABEL = "ready-for-agent"

# Completed tickets keep a neutral discovery label after readiness and an
# active claim stop being truthful descriptions of their lifecycle.
HISTORICAL_LABEL: str = "orchestrated"

# GitHub renders the neutral discovery state with its conventional purple.
HISTORICAL_LABEL_COLOR: str = "6f42c1"

# Repository label discovery is bounded independently of ticket pagination.
REPOSITORY_LABEL_PAGE: int = 100

# The label a parked ticket goes back under: the triage vocabulary's own word
# for thinking that is not finished. The ready label is a claim, and a ticket
# whose text still defers a decision to a human is one triage got wrong — the
# swap is the tracker made truthful again (ADR-0070).
INFO_LABEL = "needs-info"

# How many tickets one tracker query asks for. The tracker pages at thirty by
# default, which is no scope at all; a page that comes back full is not
# trusted to be the whole set, since a scope silently missing tickets is a run
# that leaves work behind without saying so.
TICKET_PAGE = 200

# Approval identities have their own domain so equal JSON in another feature
# can never authorize an Orchestrate run.
APPROVAL_VERSION: int = 1

# The outcomes a run records against a ticket and that settle it: a settled
# ticket is never offered again. Stranded and never-on-the-frontier are read
# off the graph rather than recorded, so neither is one.
DONE = "done"
FAILED = "failed"
CONFLICTED = "conflicted"
OUTCOMES = (DONE, FAILED, CONFLICTED)

# The one recordable outcome that settles nothing. A builder that finds its
# ticket depends on open work the graph does not name stops, and the run
# writes the missing edge rather than a failure (ADR-0073). The edge on the
# tracker is the whole of the memory the mechanism needs — the ticket is
# offered again when its blocker has a done Ticket Resolution — which is why
# read back off a ticket never include this one.
BLOCKED = "blocked"

# Everything the record verb accepts: the outcomes that settle a ticket, and
# the one that corrects the graph instead.
RECORDABLE = (*OUTCOMES, BLOCKED)

# A fresh verdict after the first amend may reveal new bounded information,
# but a second continuation is terminal rather than an open-ended repair loop.
AMEND_LIMIT: int = 2

# Each amend's append-only lifecycle. The builder and verifier dispatches are
# recorded before they start; their terminal verdict is recorded before the
# run integrates or spends the continuation.
AMEND_BUILDING: str = "building"
AMEND_VERIFYING: str = "verifying"
AMEND_PASSED: str = "passed"
AMEND_FAILED: str = "failed"
AMEND_LEGACY: str = "legacy"
AMEND_PHASES: tuple[str, ...] = (
    AMEND_BUILDING,
    AMEND_VERIFYING,
    AMEND_PASSED,
    AMEND_FAILED,
)

# The only legal moves through the two-attempt repair path. Repeating the
# current move is handled separately as an idempotent replay.
AMEND_TRANSITIONS: dict[tuple[int, str] | None, tuple[tuple[int, str], ...]] = {
    None: ((1, AMEND_BUILDING),),
    (1, AMEND_BUILDING): ((1, AMEND_VERIFYING),),
    (1, AMEND_VERIFYING): ((1, AMEND_PASSED), (1, AMEND_FAILED)),
    (1, AMEND_FAILED): ((2, AMEND_BUILDING),),
    (1, AMEND_LEGACY): ((2, AMEND_BUILDING),),
    (2, AMEND_BUILDING): ((2, AMEND_VERIFYING),),
    (2, AMEND_VERIFYING): ((2, AMEND_PASSED), (2, AMEND_FAILED)),
}

# Appended to an unsuccessful outcome's note. The note is append-only and can
# never be corrected in place (ADR-0051), and a later Reconciliation cannot
# reach back into it, so what limits its claim to the attempt it records has
# to be true from the moment it is written and stay true of a ticket that is
# never reconciled. It therefore points a reader at the rest of the thread
# rather than promising a Reconciliation is there (ADR-0079, issue #112).
RESOLUTION_ELSEWHERE = (
    "This records that attempt only; if the ticket's current resolution "
    "differs, that is established elsewhere in this thread."
)

# What each recorded outcome says on the ticket it is recorded against. The
# machine-readable half is the marker; this is the half a developer reads.
NOTES = {
    DONE: (
        "Recorded by an unattended run: built and then verified independently "
        "against this ticket's acceptance criteria."
    ),
    FAILED: (
        "Recorded by an unattended run: verification did not pass. Numbered "
        "amend markers show how far the bounded two-amend repair path ran; no "
        f"further automatic attempt is made. {RESOLUTION_ELSEWHERE}"
    ),
    CONFLICTED: (
        "Recorded by an unattended run: this ticket's work collided with "
        "another ticket's and the collision was not repaired. "
        f"{RESOLUTION_ELSEWHERE}"
    ),
    BLOCKED: (
        "Recorded by an unattended run: the builder found this ticket depends "
        "on open work the graph did not name. The corrected edge is now on "
        "the tracker, the claim is released, and the ticket is offered again "
        "when its blocker has a done Ticket Resolution."
    ),
}

# What a run writes on a ticket it is about to build a second time. A rebuild
# is the one rerun a collision buys, and this note is what bounds it: the
# ticket carries it from the moment the first rebuild starts, so a second
# collision on the same ticket is recorded rather than built over again.
REBUILD_NOTE = (
    "Recorded by an unattended run: this ticket's work collided with work "
    "already on the branch, the repair did not verify, and the ticket is "
    "being built once more on top of the integrated branch."
)

# A phase that dispatches a builder or records a failed verifier retains the
# complete verdict that determines what the run may do when it resumes.
AMEND_VERDICT_HEADING: str = "\n\nVerifier verdict:\n\n"

# The marker every recorded outcome carries, so what a run wrote on a ticket
# is machine-readable and not only prose somebody has to interpret.
MARKER = "kntnt-orchestrate"

# The same marker read back off a ticket. A recorded outcome outlives the
# session that produced it because the tracker is where it was written, which
# is what lets one run's record change the next run's plan without either of
# them sharing any memory (ADR-0051).
RECORDED_OUTCOME = re.compile(
    rf"<!--\s*{MARKER}\s+outcome=(\S+?)(?:\s+commit=(\S+?))?"
    rf"(?:\s+collided-with=([\d,]+))?(?:\s+contract-base=(\S+?))?\s*-->"
)

# Reconciliation is a distinct fact from the run outcome it follows. Keeping
# its own marker preserves the unsuccessful attempt while letting projections
# answer where the ticket's requested work stands now (ADR-0079).
RECORDED_RECONCILIATION: re.Pattern[str] = re.compile(
    rf"<!--\s*{MARKER}\s+reconciliation=done\s+commit=(\S+?)\s*-->"
)

# GitHub's closing-keyword grammar is the strongest repository-local evidence
# that a commit completed one ticket. The repository half is deliberately
# absent: Orchestrate reads one repository and only accepts bare references.
CLOSING_REFERENCE: re.Pattern[str] = re.compile(
    r"(?im)^\s*(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)\b"
)

# The same marker read back for the one thing that is not an outcome: whether
# this ticket has already had its one rebuild. It is read off the tracker for
# exactly the reason an outcome is — a run that was interrupted mid-rebuild
# must find the bound where it left it (ADR-0055).
RECORDED_REBUILD = re.compile(rf"<!--\s*{MARKER}\s+rebuild\s*-->")

# The same marker read back for verifier-informed amendments. Number and phase
# reconstruct the exact lifecycle; the optional pair retains the legacy marker
# as attempt one with an unknown historical phase.
RECORDED_AMEND: re.Pattern[str] = re.compile(
    rf"<!--\s*{MARKER}\s+amend"
    rf"(?:=([1-{AMEND_LIMIT}])\s+phase=({'|'.join(AMEND_PHASES)}))?\s*-->"
)

# The same marker on the note a blocked outcome leaves. Owned by the engine so
# it never reaches a brief as thread, and never read back as an outcome: a
# blocked ticket is not settled, the corrected edge on the tracker being the
# whole of the memory the mechanism needs (ADR-0073).
RECORDED_BLOCKED = re.compile(rf"<!--\s*{MARKER}\s+blocked-by=[\d,]+\s*-->")

# The same marker again, on the merge a run makes when it brings a ticket onto
# the branch. It is what lets the branch say whose work a file carries, which
# is how a collision names the ticket on the other side of it rather than only
# the files the two tickets both touched.
MERGED_TICKET = re.compile(
    rf"<!--\s*{MARKER}\s+merged=(\d+)(?:\s+regenerated=(\S+))?\s*-->"
)

# A collision repair is run-owned history too, but remains distinct from the
# integration markers used to account for tickets on the run branch.
REPAIRED_TICKET = re.compile(rf"<!--\s*{MARKER}\s+repair=(\d+)\s*-->")

# The same marker once more, on the merge a resume makes to bring the run
# branch into a preserved ticket branch. That merge is the engine's own
# scaffolding rather than anything a builder wrote, and the marker is what says
# so: a subject line is prose, and prose is not what durable history is read
# back from (ADR-0148).
BROUGHT_FORWARD = re.compile(rf"<!--\s*{MARKER}\s+brought-forward=(\d+)\s*-->")

# Every marker that says a commit is the run's own rather than a builder's.
# The declared commit-role walk reads these, so an engine-made commit whose
# marker is missing here is read as work the ticket declared (ADR-0148).
RUN_OWNED: tuple[re.Pattern[str], ...] = (
    MERGED_TICKET,
    REPAIRED_TICKET,
    BROUGHT_FORWARD,
)

# Where a repository says which of its files are generated and what regenerates
# each. It is read rather than inferred: a file is generated because the
# repository declares it so, never because the engine recognised its name or
# its shape (ADR-0106). A repository that declares nothing has no collision
# settled this way, and every collision takes the repair path as before.
GENERATED_DECLARATION = ".kntnt-orchestrate/generated.json"

# Who a claim assigns the ticket to. The tracker's own relation for "somebody
# is on this" is the claim: it needs no label created and no convention
# agreed, and a ticket a human has taken is one an unattended run must leave
# alone for exactly the same reason.
CLAIM_ASSIGNEE = "@me"

# What a run calls the state it keeps in the session's scratch directory. One
# file per session, named rather than generated, so a re-invocation in that
# same session finds what the last one left (ADR-0052).
STATE_FILE = "kntnt-orchestrate.json"

# What it calls the other half of that state, and the half ADR-0052's account
# does not cover: the frozen routing context, the invocation's own field locks,
# and every exact decision made under them. The tracker and the branch can
# rebuild what a run claimed and recorded; neither can reproduce the profile
# revision, evidence vintage, prices, aliases, and Harness mappings a decision
# was made from, so those live in a file of their own and are never inferred
# (ADR-0085).
ROUTING_FILE = "kntnt-orchestrate-routing.json"

# The directory it keeps that file in, under the one the harness gives. A
# subagent's cleanup glob at the root of a shared scratch directory deleted the
# state of the very run that dispatched it, so the run's own things live one
# level down, where no subagent is ever sent (ADR-0071).
STATE_HOME = "kntnt-orchestrate"

# The version of model-selector's public route response this engine reads. The
# Interface is the only cross-Skill seam, and a response from another version
# of it is refused rather than guessed at (ADR-0083).
ROUTE_SCHEMA_VERSION = 1

# What one public decision can be: an exact launch, a safe inheritance, or a
# role that may not launch at all. The first two may start work; the third
# never does.
ROUTE_SELECTED = "selected"
ROUTE_INHERIT = "inherit"
ROUTE_REFUSED = "refused"
ROUTE_ACCEPTABLE = (ROUTE_SELECTED, ROUTE_INHERIT)

# The whole of the portable deliberation scale, which is what `--deliberation`
# locks and the only vocabulary either side of the seam shares. Native names
# and numeric budgets stay inside model-selector's verified mappings.
DELIBERATION_LEVELS = ("low", "medium", "high", "xhigh", "max")

# How Orchestrate names the requests it sends, and therefore how a decision
# finds its way back to the role and the ticket it was made for. The names are
# this Skill's own — it writes the requests — and the engine reads them so a
# claim, an amend, and the account can each ask whether the thing about to run
# was routed at all. A wave's fix carries one further name beside its own, for
# the single escalated round a changed-nothing fix buys (ADR-0110).
ROUTE_REQUEST = re.compile(
    r"^(?:(?P<role>build|repair|rebuild)-(?P<ticket>\d+)"
    r"|amend-(?P<amended>\d+)-(?P<attempt>\d+)"
    r"|wave-fix-(?P<wave>\d+)(?P<escalated>-escalated)?)\Z"
)

# What that further decision is named: the wave's own fix request with this
# suffix. There is exactly one such name per wave and no name at all for a
# second, and the engine refuses a second under it, the escalation being one
# round rather than a ladder (ADR-0110).
WAVE_FIX_ESCALATION = "-escalated"

# The stable reason model-selector inherits under where no complete adapter on
# the active Harness can express a safe point. A run every one of whose
# decisions came back that way has one fact about its Harness rather than one
# fact per ticket, and says it once (ADR-0110).
INHERITED_FOR_NO_ADAPTER = "unavailable_selection_controls"

# Where a run keeps the routed attempts an external verdict has judged, and
# where the sanitized artifact model-selector makes of them is written. Both
# sit in the run's own scratch, are named by the engine so a report and an
# import mean the same two files, and neither is ever a repository file
# (ADR-0089).
ATTEMPTS_FILE = "kntnt-orchestrate-attempts.json"
OBSERVATION_FILE = "kntnt-orchestrate-observations.json"

# Where a caller polls the current non-authoritative run dashboard.
PROGRESS_FILE: str = "kntnt-orchestrate-progress.json"

# The complete live phases a session or engine transition may publish.
PROGRESS_PHASES: tuple[str, ...] = (
    "preflight",
    "isolate",
    "build",
    "verify",
    "amend",
    "integrate",
    "note",
    "wave_verdict",
)

# Durable flake evidence belongs to the Skill rather than to any repository.
# The run-local selection sits beside the rest of the session account so the
# final report names this run's records without mistaking older ones for them.
FLAKE_HOME = Path(".kntnt/orchestrate")
FLAKE_LEDGER = "flakes.jsonl"
RUN_FLAKES_FILE = "kntnt-orchestrate-flakes.json"

# The version of model-selector's public observation contract this engine
# writes. It is versioned separately from the route response because the two
# are different documents and neither is a reading of the other.
OBSERVATION_SCHEMA_VERSION = 1

# What each building role is as workload. An initial build and a mechanical
# wave fix are different work rather than the same work twice, and an amend is
# a second attempt at the first one's, so evidence keeps them apart.
OBSERVED_STRATA: dict[str, str] = {
    "build": "initial_build",
    "amend": "amend",
    "repair": "collision_repair",
    "rebuild": "rebuild",
    "wave-fix": "mechanical_wave_fix",
}

# The namespace this Skill's Cohorts are named under. A ledger is shared with
# every other routed caller, so an Orchestrate initial build has to be nameable
# apart from anybody else's work of the same kind.
OBSERVED_COHORT_PREFIX = "orchestrate/"

# Which independent verdict establishes each role's outcome. A builder's own
# report establishes nothing, so the checker an observation names is always the
# brief of the session that judged it and never the one that did the work.
OBSERVED_CHECKERS: dict[str, str] = {
    "build": "verify.md",
    "amend": "verify.md",
    "rebuild": "verify.md",
    "repair": "repaired.md",
    "wave-fix": "wave.md",
}

# How this run's own vocabulary reaches the evidence contract's. The first two
# are verdicts on the work; the rest are conditions of the environment and of
# the workflow, which the ledger keeps apart from quality because none of them
# says the configuration did the work badly.
OBSERVED_OUTCOMES: dict[str, tuple[str, str | None, str]] = {
    "pass": ("pass", None, "independent_verifier"),
    "fail": ("fail", None, "independent_verifier"),
    "hinder": ("infra_error", "mechanical_hinder", "harness"),
    "tracker-failure": ("infra_error", "tracker_failure", "tracker"),
    "parked": ("abstain", "open_decision", "tracker"),
    "blocked": ("abstain", "discovered_dependency", "tracker"),
}

# The four things a report can say about a ticket's Time to Verified Pass.
# Only the first carries a number; the other three are the three different
# silences an absent measurement can be, kept apart so a reader never has to
# guess which one a missing value was (ADR-0147).
NOT_STARTED: str = "not_started"
VERIFIED_PASS: str = "verified_pass"
INCOMPLETE: str = "incomplete"
NOT_PASSED: str = "not_passed"


# Machine judgements and non-model conditions may enter the ledger unattended.
AUTOMATIC_AUTHORITIES: frozenset[str] = frozenset(
    {"independent_verifier", "objective_checker", "declared_failure_signal"}
)

# What a Cohort's Standing Policy evaluation came to when the ledger actually
# moved it, and the one command that puts it back. The run reports both rather
# than leaving a developer to find out at the next freeze that a Cohort now
# starts a Rung higher (ADR-0149).
POLICY_MOVED: str = "moved"
POLICY_RESET_COMMAND: str = "/model-selector config policy reset"

# The roles that are never routed. A verdict inherits the complete main seat
# exactly, so a decision made for one is refused at this seam rather than left
# for a paragraph to forbid: what cannot be persisted cannot reach a verifier
# (ADR-0085).
VERDICT_ROLES = ("verify", "amend-verify", "repair-verify", "wave-check")

# What a run calls the working trees it builds tickets in, and the branches it
# builds them on. They live under the repository's own git directory: a
# developer who comes back mid-run finds their working tree exactly as they
# left it, and `git status` says nothing about a run in progress (ADR-0054).
WORKTREE_HOME = "kntnt-orchestrate"

# What a ticket's own scratch directory is called, beside the working tree it
# belongs to. Two subagents that cannot name the same path cannot read each
# other's logs or clear away each other's files (ADR-0071).
SCRATCH_SUFFIX = ".scratch"

# Where the numbers a ticket was reserved are kept, beside the same working
# tree. They are the run's account rather than the ticket's, so they sit
# outside the scratch directory a subagent is told it may write in.
RESERVED_SUFFIX = ".reserved.json"

# The lock every reservation is produced under, beside the reservations it
# guards. One file per repository rather than per run, because two sessions
# working the same repository reach the same allocation window from different
# processes, and the tracker's claim keeps them off the same ticket but not
# off the same number. The kernel releases it with the process that holds it,
# so a run killed mid-allocation strands nothing.
ALLOCATION_LOCK = "allocation.lock"

# What a record in a numbered registry is named: four digits and a hyphen,
# which is the pattern this collection's own registries share. It is how a
# directory of records is recognised without anybody configuring one.
RECORD_NAME = re.compile(r"^(\d{4})-")

# The ceiling at which a run works one ticket at a time: the default, the
# floor below which a ceiling would start nothing, and the point isolation
# begins above. It is the run that needs no integration at all — the work
# lands straight on the branch, with nothing to merge and no working tree to
# make (ADR-0054).
ONE_AT_A_TIME = 1

# What the tracker calls a ticket that is closed. Closure changes which facts
# must be projected, but does not itself establish that requested work exists.
CLOSED = "CLOSED"

# The line the ticket breakdown writes an edge on where the tracker has no
# native relation to write it in: a heading or a sentence opening `Blocked by`,
# optionally marked up as one.
BLOCKED_BY_LINE = re.compile(
    r"^\s*(?:#{1,6}\s+)?\**blocked[ -]by\**\s*:?", re.IGNORECASE
)

# The line a ticket declares itself a Solo Ticket on, written the same two ways
# as the edge above: a heading with the reason under it, or a sentence carrying
# it. It names nobody, because what it excludes is every ticket that could add
# a new instance of what it is rewriting — instances that do not exist when the
# ticket is written, which is why no edge can say this (ADR-0099).
SOLO_LINE = re.compile(r"^\s*(?:#{1,6}\s+)?\**builds[ -]alone\**\s*:?", re.IGNORECASE)

# The line the breakdown names a ticket's parent spec on, written the same two
# ways: a heading with the reference under it, or a sentence carrying it.
PARENT_LINE = re.compile(r"^\s*(?:#{1,6}\s+)?\**parent\b\**\s*:?", re.IGNORECASE)

# The ordered commit roles a ticket may declare, using the same heading or
# sentence shape as the other body-line declarations.
COMMIT_ROLES_LINE = re.compile(
    r"^\s*(?:#{1,6}\s+)?\**commit[ -]roles\**\s*: ?|"
    r"^\s*#{1,6}\s+\**commit[ -]roles\**\s*$",
    re.IGNORECASE,
)

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

# What a run was aimed at, written the way a developer writes a reference: a
# bare number, marked up as one or not.
SCOPE_REFERENCE = re.compile(r"^#?(\d+)$")

# The two things a reference can name. A spec scopes the run to its children
# and is never itself built; a ticket scopes it to itself.
SPEC = "spec"
TICKET = "ticket"


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


def git_result(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run git in *cwd* and return the whole result, exit code and all.

    For the callers that act on a git command's failure rather than stopping
    at it: a merge that collides is an answer, and so is a working tree that
    will not go.
    """

    return _capture(cwd, "git", *args)


def git_ok(cwd: Path, *args: str) -> bool:
    """Return True when a git command exits 0."""

    return git_result(cwd, *args).returncode == 0


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

    None means there is nothing to bound the closed half of a report by
    (ADR-0058), which is all the answer is asked for. It gates nothing: a run
    works the branch the developer left it on either way (ADR-0064).
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


def default_branch_reference(cwd: Path) -> str | None:
    """Return the authoritative default-branch ref used for landed work."""

    # Prefer the remote-tracking ref itself, because a local branch may carry
    # work that has not reached the repository other maintainers can observe.
    try:
        reference = git(
            cwd,
            "symbolic-ref",
            "--quiet",
            "refs/remotes/origin/HEAD",
        ).strip()
        if reference.startswith("refs/remotes/origin/") and git_ok(
            cwd,
            "show-ref",
            "--verify",
            "--quiet",
            reference,
        ):
            return reference
    except RunError:
        pass

    # A configured origin establishes a publication boundary even when its
    # default ref is unavailable locally; uncertainty refuses reconciliation.
    if git_ok(cwd, "remote", "get-url", "origin"):
        return None

    # Repositories without a remote retain the local fallback used by tests
    # and by work that has no publication boundary.
    return default_branch(cwd)


def worktree_home(cwd: Path) -> Path:
    """Return the directory a run keeps its ticket working trees in.

    The git directory rather than the repository beside it, because a working
    tree there would show up as untracked files in the developer's own — and
    in whatever a builder is about to commit (ADR-0054).
    """

    common = Path(git(cwd, "rev-parse", "--git-common-dir").strip())
    return (cwd / common).resolve() / WORKTREE_HOME


def worktree_branch(run_branch: str, number: int) -> str:
    """Return the branch ticket *number* is built on in *run_branch*'s run."""

    return f"{WORKTREE_HOME}/{run_branch}/{number}"


def open_worktrees(cwd: Path, run_branch: str) -> dict[int, str]:
    """Return the working tree *run_branch*'s run has open per ticket.

    Git's own account of its working trees is the source: a run that made one
    and was interrupted, and one whose ticket failed and whose tree was left
    to be inspected, are the same fact on disk and are read the same way.

    A tree is named for its ticket and a branch for the run that made it, so
    it is the branch that says whose it is. A tree standing at this ticket's
    path on another run's branch is another branch's work, and adopting it
    would build this run's ticket on top of it.
    """

    # Find the trees this run made: those under its own directory, named for a
    # ticket, on the branch this run cuts for it. Git writes one block per
    # tree; a block with no branch line is a detached head this never makes.
    home = worktree_home(cwd)
    found: dict[int, str] = {}
    standing: Path | None = None
    for line in git(cwd, "worktree", "list", "--porcelain").splitlines():
        if line.startswith("worktree "):
            standing = Path(line.removeprefix("worktree ").strip()).resolve()
        elif line.startswith("branch ") and standing is not None:
            branch = line.removeprefix("branch ").strip().removeprefix("refs/heads/")
            if (
                standing.parent == home
                and standing.name.isdigit()
                and branch == worktree_branch(run_branch, int(standing.name))
            ):
                found[int(standing.name)] = str(standing)

    return found


def numbered_registries(cwd: Path) -> dict[str, int]:
    """Return each directory of numbered records, with the highest number in it.

    A registry is found rather than configured: a directory holding files named
    by a four-digit prefix is one, wherever in the tree it sits. It is read off
    the repository's index of tracked files, which keeps the answer the same
    however the tree is walked and leaves out everything git ignores.
    """

    # The whole repository rather than the directory the verb was run from: a
    # registry the run cannot see is one two tickets go on colliding in.
    top = Path(git(cwd, "rev-parse", "--show-toplevel").strip())

    # Every tracked file named by a number puts its directory on the list, and
    # the highest number in that directory is what the next one is read from.
    highest: dict[str, int] = {}
    for tracked in git(top, "ls-files").splitlines():
        record = PurePosixPath(tracked)
        numbered = RECORD_NAME.match(record.name)
        if numbered is not None:
            directory = str(record.parent)
            highest[directory] = max(highest.get(directory, 0), int(numbered.group(1)))

    return highest


@contextmanager
def allocation_lock(home: Path) -> Iterator[None]:
    """Hold the lock a wave's overlapping isolations take turns under.

    A caller that finds it taken waits: the work behind it is bounded and
    short, and a refusal would turn solved contention into a ticket with
    nowhere to build. Closing the file releases it, as does the death of the
    process.
    """

    home.mkdir(parents=True, exist_ok=True)
    with (home / ALLOCATION_LOCK).open("a") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        yield


def reserved_numbers(home: Path, number: int) -> list[dict[str, str]]:
    """Return what isolate reserved ticket *number*, or nothing where it has none.

    The file is a boundary like any other, and a file that cannot be read is
    read as no reservation: the ticket is given fresh numbers rather than the
    run stopping over a directory somebody emptied.
    """

    try:
        stored = json.loads(
            (home / f"{number}{RESERVED_SUFFIX}").read_text(encoding="utf-8")
        )
        return [
            {"directory": str(held["directory"]), "number": str(held["number"])}
            for held in stored
        ]
    except (OSError, TypeError, ValueError, KeyError):
        return []


def numbers_in_flight(home: Path) -> dict[str, int]:
    """Return the highest number any reservation holds, registry by registry.

    Read off the reservation files under *home* rather than off any list of
    open working trees, because such a list is read before the reservations
    it stands for: two isolations started together each list the trees before
    the other opened its own, and a list read in one session never carries
    another session's trees at all. The files are whoever has reserved,
    however they came to.
    """

    # Every reservation on disk counts, a stale one included: it merely
    # raises the floor, and an unused number expires as a gap the numbering
    # already allows. The digit check keeps a hand-copied file from stopping
    # the run, in the same spirit as reading an unreadable one as nothing.
    taken: dict[str, int] = {}
    for reservation in home.glob(f"*{RESERVED_SUFFIX}"):
        ticket = reservation.name.removesuffix(RESERVED_SUFFIX)
        if ticket.isdigit():
            for held in reserved_numbers(home, int(ticket)):
                directory = held["directory"]
                taken[directory] = max(taken.get(directory, 0), int(held["number"]))

    return taken


def allocate(cwd: Path, number: int) -> dict[str, Any]:
    """Give ticket *number* the scratch and the record numbers it may take.

    Both are the ticket's for as long as its working tree is: made beside it,
    read back where the ticket is picked up again, and taken away with it. The
    reservation is stored rather than worked out afresh because the answer a
    brief was filled in from has to be the answer still when the next ticket
    asks — two tickets that each read a registry for its next free number read
    the same one, and git merges the two records they write without a word
    (ADR-0071). And it is produced under an advisory file lock, together with
    the reads it is derived from, because the allocation is itself that same
    read-then-write one level up: four isolate calls overlapping in one wave
    read the same state and reserved the same number.
    """

    home = worktree_home(cwd)

    # The scratch is made rather than merely named: a subagent told to write in
    # a directory nothing created writes somewhere else instead.
    scratch = home / f"{number}{SCRATCH_SUFFIX}"
    scratch.mkdir(parents=True, exist_ok=True)

    # The whole read-modify-write happens with the lock held.
    with allocation_lock(home):
        # A ticket already holding numbers keeps them, under contention
        # exactly as without it. One arriving new takes the next past both
        # the registry's highest and whatever any reservation holds, so a
        # wave's reservations are disjoint however its isolations overlap. A
        # reservation nobody uses expires as a gap, which the numbering
        # allows: next free is one above the highest, never the lowest hole
        # (ADR-0067).
        held = reserved_numbers(home, number)
        if not held:
            taken = numbers_in_flight(home)
            held = [
                {
                    "directory": directory,
                    "number": f"{max(highest, taken.get(directory, 0)) + 1:04d}",
                }
                for directory, highest in sorted(numbered_registries(cwd).items())
            ]
            (home / f"{number}{RESERVED_SUFFIX}").write_text(
                json.dumps(held, indent=2) + "\n", encoding="utf-8"
            )

    return {"scratch": str(scratch), "reservations": held}


def discard_allocation(cwd: Path, number: int) -> None:
    """Take back what isolate gave ticket *number* beside its working tree.

    The scratch and the reservation live exactly as long as that tree does: a
    ticket whose work is on the branch is finished with both, and one being
    built again from nothing has to read the registry as it now stands rather
    than hold a number the work it collided with has since taken.
    """

    home = worktree_home(cwd)
    shutil.rmtree(home / f"{number}{SCRATCH_SUFFIX}", ignore_errors=True)
    (home / f"{number}{RESERVED_SUFFIX}").unlink(missing_ok=True)


@dataclass
class Remark:
    """One thing a person wrote on a ticket after filing it.

    Attributed and dated because the brief renders the thread in filing order
    and a builder has to be able to tell what came after what — a comment
    answering a question the body leaves open is only the answer once you can
    see it was written later. `author` is empty where the tracker has forgotten
    who wrote it, an account since deleted still having filed requirement.
    """

    author: str
    created_at: str
    body: str


@dataclass(frozen=True)
class AmendState:
    """The latest append-only verifier-informed amend phase on a ticket.

    `attempt` is one or two. `phase` identifies the next safe action, and
    `verdict` retains the complete verifier output needed by a resumed builder.
    Legacy markers expose an unknown historical phase and no persisted verdict.
    """

    attempt: int
    phase: str
    verdict: str | None


@dataclass(frozen=True)
class TicketResolution:
    """A ticket's current resolution and the provenance that established it.

    `outcome` is the current projection used for scheduling and reporting.
    `commit` carries that projection's implementation. `run_outcome` preserves
    the unattended attempt even when Reconciliation later projects done, and
    `is_reconciled` identifies that external-completion path.
    """

    outcome: str | None
    commit: str | None
    run_outcome: str | None
    is_reconciled: bool


@dataclass
class Ticket:
    """One ticket in scope, as the tracker describes it.

    `blocked_by` holds the tickets whose current Ticket Resolution does not
    establish the work this one needs. A closed failed or conflicted blocker
    therefore remains in the list until Reconciliation resolves it done.

    `body` is the ticket as it was filed and `thread` is what has been said on
    it since, oldest first. Both are carried whole, because the brief a
    building subagent gets carries the ticket as the tracker now holds it and
    never a summary of it — a requirement a maintainer answered in a comment is
    requirement, and a builder given only the body would be answering questions
    that were settled hours ago. `parent` is the spec whose testing decisions
    are read before any test.
    `claimed_by` is who the tracker has it assigned to: non-empty means a
    session or a person already has it, and the logins are what tells a claim
    this run left behind from one somebody else took.

    `resolution` keeps the current scheduling projection and its provenance in
    one domain value. A failed or conflicted resolution strands dependents; a
    done resolution unblocks them. `collided_with` is the other half of a
    conflicted Run Outcome — the tickets whose work this one collided with,
    which is the pair that names the blocking edge the ticket breakdown missed.
    `amends_spent` is the append-only verification-repair bound: zero before an
    amend, one after the first marker, and two after the continuation marker.
    `amend_state` identifies the exact current builder, verifier, or verdict
    phase and retains the verdict a resumed amend builder needs.

    `builds_alone` is the ticket's own declaration that it shares its wave with
    nobody: a repository-wide invariant it rewrites is a rule every shipped
    file is under, including the files a concurrent sibling has not written yet
    (ADR-0099).

    `worktree` is the one thing here the tracker cannot say and the repository
    can: where this ticket's work stands, for as long as a working tree of its
    own holds it. It is None for a ticket built straight on the branch, and for
    one whose tree was taken away when its work was merged — which leaves it
    naming exactly the failures the machine kept for the developer to look at.
    """

    number: int
    title: str
    url: str
    body: str
    thread: list[Remark]
    parent: int | None
    claimed_by: list[str]
    blocked_by: list[int]
    resolution: TicketResolution
    collided_with: list[int]
    amends_spent: int
    amend_state: AmendState | None
    builds_alone: bool = False
    commit_contract: list[dict[str, Any]] | None = None
    contract_base: str | None = None
    worktree: str | None = None


def ticket_details(
    ticket: Ticket, timing: dict[int, dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Return the established flat public representation of *ticket*.

    `timing` is the run's own Time to Verified Pass account where the caller
    has one. A ticket absent from it launched no routed attempt in this run,
    which is a fact about the run rather than a gap in the report, so it is
    stated as `not_started` rather than left out.
    """

    # The domain groups resolution provenance, while the public engine contract
    # retains its established top-level fields for callers and renderers.
    details = asdict(ticket)
    resolution = cast(dict[str, Any], details.pop("resolution"))
    if timing is None:
        return details | resolution
    measured = timing.get(
        ticket.number,
        {
            "time_to_verified_pass_seconds": None,
            "time_to_verified_pass_status": NOT_STARTED,
        },
    )
    return details | resolution | measured


@dataclass
class ProgressState:
    """Session-supplied dashboard values no ticket transition can derive."""

    wave: int
    ticket: int | None
    amendments_spent: int
    tickets_completed: int
    tickets_remaining: int


class ApprovalPayload(TypedDict):
    """The complete plan surface one caller authorizes."""

    branch: str
    default_branch: str | None
    scope: list[dict[str, Any]] | None
    at_once: int
    worktrees: bool
    model: str | None
    deliberation: str | None
    waves: list[list[int]]
    solo: list[int]


@dataclass
class RunState:
    """What one run remembers of itself between invocations.

    Its ordinary account is remembered rather than relied on: the tracker and
    branch can reproduce it when this state is absent (ADR-0051). Its declared
    commit contracts and their claim boundaries are relied-on projections: a
    declared ticket requires readable state to begin and enforce its contract,
    while a checking verb with absent or unreadable state deliberately follows
    the undeclared path (ADR-0138).

    `branch` and `label` are what the state is of: a scratch directory outlives
    a checkout, and a document describing another branch describes another run.
    `login` is who the tracker last said this run claims as, kept so a verb
    that needs it does not ask again. `claimed` is the tickets this run has
    taken and not yet recorded an outcome against. `base` is the commit its
    work sits on top of, which is the branch's half of the same account and is
    worked out afresh every time rather than read back, so a state that is gone
    cannot make it disagree with the branch it describes. `starting` is the
    frontier the last plan cut to the ceiling, kept so the preflight that
    follows can be held to routing that frontier and not some other set.

    `contracts` projects the tracker declarations, and `contract_bases` holds
    the claim boundaries that the branch can no longer establish after work
    begins. `progress` remembers the session-supplied dashboard values that a
    ticket transition cannot derive, so deleting the dashboard never makes it
    an input. The frozen routing account is separately relied on and lives in
    a file of its own rather than in this one (ADR-0085).
    """

    branch: str
    label: str
    login: str | None
    claimed: list[int]
    base: str
    starting: list[int]
    contracts: dict[int, list[dict[str, Any]]]
    contract_bases: dict[int, str]
    progress: ProgressState | None = None
    approval_expected: str | None = None
    approval_identity: str | None = None
    approval_payload: ApprovalPayload | None = None
    approval_met: bool | None = None


def state_file(directory: str | None) -> Path | None:
    """Return the file the run's state lives in, or None where there is none.

    The harness knows where this session's scratch directory is and the engine
    does not, so the directory is passed in. None is not an error: the state is
    an optimisation, and a harness that offers no such directory costs a run
    nothing but the tracker call the state would have saved.

    It resolves into a subdirectory of that directory rather than its root,
    which the run shares with every subagent it dispatches (ADR-0071).
    """

    return Path(directory).expanduser() / STATE_HOME / STATE_FILE if directory else None


@dataclass
class RouteRecord:
    """One public route decision, and the role of this run's it was made for.

    `decision` is model-selector's own answer, kept whole and never
    interpreted: this Skill consumes the Interface and owns none of the
    selection rules behind it (ADR-0083). What the engine adds is the reading
    of the request name it chose itself — which `role` the decision governs and,
    where the role belongs to one ticket, which ticket — so a claim, an amend,
    and the account can each find the decision that covers what is about to run.

    `stage`, `workload_cohort`, and `workload_tags` are the same reading again:
    the Cohort the decision was made for, computed once here and frozen with
    the decision, so the observation a later verdict writes names the Cohort
    the request named rather than one reconstructed from a response that never
    echoed it.
    """

    request_id: str
    role: str
    ticket: int | None
    decision: dict[str, Any]
    stage: str
    workload_cohort: str
    workload_tags: list[str]

    @property
    def acceptable(self) -> bool:
        """Say whether this decision may launch work at all."""

        return str(self.decision["status"]) in ROUTE_ACCEPTABLE


@dataclass
class Routing:
    """The frozen routing account: the half of a run nothing can rebuild.

    Every other answer this engine gives is a reading of the tracker and the
    branch, and comes back the same where a run's own memory is gone
    (ADR-0051). This one does not. `snapshot` is the context model-selector
    froze before the first claim — profile revision, evidence identity and
    vintage, Harness inventory, main seat, native mappings, commercial facts,
    and override policy — and the current versions of all of that are a
    different context, not a recovered one. `model` and `deliberation` are the
    invocation's own field locks, frozen beside it because a resume that
    changed them would be a second run reporting as the first. `fast` is the
    third of them and the run's objective: set, the night is routed to the
    fastest configuration that holds quality rather than the cheapest one, and
    a resume that added or dropped it would be routing the rest of the work
    against a different objective than the half already built. `decisions` is
    every exact decision made under that context, in the order they were made,
    which is what the outcome account is audited from. `attempts` is what an
    external verdict later established about those decisions, kept beside them
    because an outcome and the decision it judges are one fact, and because
    nothing else holds either once the session that reached them is gone.
    """

    snapshot: dict[str, Any]
    model: str | None
    deliberation: str | None
    decisions: list[RouteRecord]
    fast: bool = False
    attempts: list[dict[str, Any]] = field(default_factory=list)
    run_identity: str = ""

    @property
    def identity(self) -> str:
        """Return the identity the snapshot is named by."""

        return str(self.snapshot["snapshot_identity"])

    @property
    def main_seat(self) -> dict[str, Any]:
        """Return the seat every verdict inherits, exactly as it was frozen."""

        return cast(dict[str, Any], self.snapshot["main_seat"])

    def decided(self, request_id: str) -> RouteRecord | None:
        """Return the latest decision made for *request_id*, or None."""

        made = [record for record in self.decisions if record.request_id == request_id]
        return made[-1] if made else None


def routing_details(routing: Routing | None) -> dict[str, Any] | None:
    """Return the public shape of a frozen routing account, or None.

    The identity and the main seat are hoisted out of the snapshot they are
    part of, because those two are what a report renders and what a verdict
    inherits, and neither reader should have to know the snapshot's own shape
    to reach them.
    """

    if routing is None:
        return None

    return {
        "snapshot_identity": routing.identity,
        "main_seat": routing.main_seat,
        "model": routing.model,
        "deliberation": routing.deliberation,
        "fast": routing.fast,
        "run_identity": routing.run_identity or None,
        "routing_capability": routing_capability(routing.decisions),
        "snapshot": routing.snapshot,
        "decisions": [asdict(record) for record in routing.decisions],
    }


def routing_capability(records: list[RouteRecord]) -> str | None:
    """Return the one routing fact a whole run shares, or None where it has none.

    Where the frozen context leaves no complete adapter that can express a safe
    point, every building role decided under it inherits the main seat, and
    every later one will too — the context is frozen for the night. That is one
    fact about the Harness rather than one fact per ticket, so it is stated
    once, before the run, instead of being decoded from a dozen identical
    inheritance reasons in the account after it (ADR-0110).
    """

    if not records:
        return None

    for record in records:
        decision = record.decision
        if str(decision.get("status")) != ROUTE_INHERIT:
            return None
        inherited = cast(dict[str, Any], decision.get("inheritance") or {})
        if str(inherited.get("reason")) != INHERITED_FOR_NO_ADAPTER:
            return None

    return (
        "no complete adapter on this Harness can express a safe point, so every "
        "building role this run launches inherits the main seat"
    )


def frozen_routing(
    state_path: Path | None,
) -> tuple[Routing | None, str | None, str | None]:
    """Return this run's frozen routing, why there is none, and any damage.

    Three answers rather than two, because absence and damage are not the same
    fact. A run that has not reached its preflight yet has frozen nothing; a
    run whose frozen context is unreadable has lost something no tracker and no
    branch can give back, and the difference decides whether the next claim may
    be made at all (ADR-0085).
    """

    try:
        routing = read_routing(state_path)
    except RunError as exc:
        return None, str(exc), str(exc)

    if routing is None:
        return None, "this run has frozen no routing yet", None

    return routing, None, None


def dispatch_refusal(
    routing: Routing | None, request_id: str, described: str
) -> str | None:
    """Return why *described* may not launch from the frozen routing, or None.

    Route before dispatch is an invariant of the run rather than a paragraph on
    its opening path, so every verb that puts an execution role to work asks
    the same question of the same account: was this exact thing decided, and
    did the decision allow it (ADR-0085).
    """

    if routing is None:
        return (
            f"{described} before this run has any frozen routing: the preflight "
            "batches the frontier through model-selector's public route "
            "Interface before anything is claimed"
        )

    decided = routing.decided(request_id)
    if decided is None:
        return (
            f"{described}, and this run's frozen routing holds no {request_id} "
            "decision: route it from the frozen snapshot first"
        )

    if not decided.acceptable:
        reason = cast(dict[str, Any], decided.decision["reason"])
        return f"route refused {request_id}: {reason['code']}: {reason['detail']}"

    return None


def routing_refusal(
    routing: Routing | None,
    damaged: str | None,
    resuming: list[int],
    model: str | None,
    deliberation: str | None,
    fast: bool,
) -> str | None:
    """Return why a plan may not start on this run's routing, or None where it may.

    A run that has not routed yet is where every run begins, and the plan is
    what invites the preflight, so nothing is refused there. What is refused is
    a run carrying on past one: work already claimed under a frozen context
    that is now gone, a context damaged where it was written, and an invocation
    asking for locks the first frontier was not routed under.
    """

    if damaged is not None:
        return (
            f"{damaged}, and a frozen context is never rebuilt from current "
            "profiles, aliases, prices, evidence, or Harness defaults"
        )

    if routing is None:
        if not resuming:
            return None
        return (
            f"{as_references(resuming)} stand claimed by this run and its frozen "
            "routing is gone: restore the state directory it was written in, or "
            "record or release those claims before a fresh run freezes its own"
        )

    return locks_refusal(routing, model, deliberation, fast, "this invocation")


def routing_file(path: Path | None) -> Path | None:
    """Return the durable copy of a run's frozen routing account."""

    return None if path is None else path.parent / ROUTING_FILE


def attempts_file(path: Path | None) -> Path | None:
    """Return where the run writes the routed attempts a verdict has judged."""

    return None if path is None else path.parent / ATTEMPTS_FILE


def progress_file(path: Path | None) -> Path | None:
    """Return where a caller polls the run's non-authoritative dashboard."""

    return None if path is None else path.parent / PROGRESS_FILE


def write_progress(
    state_path: Path | None,
    phase: str,
    progress: ProgressState,
    outcome: dict[str, list[int]] | None,
) -> str | None:
    """Atomically replace the run dashboard, or do nothing without state."""

    # Resolve the dashboard beside this session's durable state.
    destination = progress_file(state_path)
    if destination is None:
        return None

    # Build the complete dashboard before exposing any bytes to pollers.
    dashboard = {
        "wave": progress.wave,
        "ticket": progress.ticket,
        "phase": phase,
        "amendments_spent": progress.amendments_spent,
        "tickets_completed": progress.tickets_completed,
        "tickets_remaining": progress.tickets_remaining,
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "outcome": outcome,
    }

    # Rename a flushed peer file so every concurrent read is complete JSON.
    write_atomically(destination, json.dumps(dashboard, indent=2) + "\n")

    return str(destination)


def advance_progress(
    cwd: Path,
    state_path: Path | None,
    phase: str,
    ticket: int,
    amendments_spent: int | None = None,
    is_ticket_completed: bool = False,
) -> None:
    """Advance an existing dashboard, recreating it from durable run state."""

    # Skip transitions for invocations without durable session state.
    destination = progress_file(state_path)
    if destination is None:
        return

    # Rebuild session-owned totals without consulting the disposable dashboard.
    remembered = remembered_state(state_path, cwd)
    current = remembered.progress if remembered is not None else None
    remaining = len(remembered.starting) if remembered is not None else 0

    # Read a resumed ticket's durable amendment bound when the session's last
    # transition concerned the whole wave or another ticket.
    amendment_count = (
        current.amendments_spent
        if current is not None and current.ticket == ticket
        else 0
    )
    if amendments_spent is None:
        try:
            ticket_state = recorded_amend_state(ticket_view(cwd, ticket, "comments"))
            amendment_count = ticket_state.attempt if ticket_state is not None else 0
        except RunError:
            pass

    # A terminal record settles exactly one current ticket; blocked records
    # leave it in the remaining scope.
    completed = current.tickets_completed if current is not None else 0
    remaining_count = current.tickets_remaining if current is not None else remaining
    if is_ticket_completed:
        completed += 1
        remaining_count = max(remaining_count - 1, 0)

    # Preserve the advanced baseline before projecting the latest dashboard.
    progress = ProgressState(
        wave=current.wave if current is not None else 1,
        ticket=ticket,
        amendments_spent=(
            amendment_count if amendments_spent is None else amendments_spent
        ),
        tickets_completed=completed,
        tickets_remaining=remaining_count,
    )
    remember_progress(state_path, cwd, progress)
    write_progress(state_path, phase, progress, None)


def observation_file(path: Path | None) -> Path | None:
    """Return the legacy path for the run's observation artifact.

    Runs created before automatic per-attempt import may still carry this path,
    so reports retain it as a backward-compatible historical detail. New runs
    import each attempt through the shared Library at its finish boundary.
    """

    return None if path is None else path.parent / OBSERVATION_FILE


def run_flakes_file(path: Path | None) -> Path | None:
    """Return this run's durable-flake selection, where state is available."""

    return None if path is None else path.parent / RUN_FLAKES_FILE


def decode_state(contents: str) -> RunState:
    """Decode one complete state document or raise on invalid content."""

    stored = json.loads(contents)
    progress = cast(dict[str, Any] | None, stored.get("progress"))
    return RunState(
        branch=str(stored["branch"]),
        label=str(stored["label"]),
        login=None if stored["login"] is None else str(stored["login"]),
        claimed=[int(number) for number in stored["claimed"]],
        base=str(stored["base"]),
        starting=[int(number) for number in stored["starting"]],
        contracts={
            int(number): contract
            for number, contract in cast(
                dict[str, list[dict[str, Any]]], stored.get("contracts", {})
            ).items()
        },
        contract_bases={
            int(number): str(commit)
            for number, commit in cast(
                dict[str, str], stored.get("contract_bases", {})
            ).items()
        },
        progress=(
            None
            if progress is None
            else ProgressState(
                wave=int(progress["wave"]),
                ticket=(
                    None if progress["ticket"] is None else int(progress["ticket"])
                ),
                amendments_spent=int(progress["amendments_spent"]),
                tickets_completed=int(progress["tickets_completed"]),
                tickets_remaining=int(progress["tickets_remaining"]),
            )
        ),
        approval_expected=(
            None
            if stored.get("approval_expected") is None
            else str(stored["approval_expected"])
        ),
        approval_identity=(
            None
            if stored.get("approval_identity") is None
            else str(stored["approval_identity"])
        ),
        approval_payload=cast(ApprovalPayload | None, stored.get("approval_payload")),
        approval_met=cast(bool | None, stored.get("approval_met")),
    )


def carry_state_forward(path: Path | None) -> None:
    """Move a state file left at the old place into the one it lives in now.

    The state used to sit at the root of the scratch directory the harness
    gives, where a subagent's own cleanup could reach it. It is read from there
    once, so a run interrupted before the move goes on where it left off rather
    than handing its own claims back as somebody else's, and it is never
    written back there. It is remembered rather than relied on either way: a
    move that fails costs the run only the tracker call the state would have
    saved.
    """

    if path is None or path.exists():
        return

    # Prove the former source is readable state before creating its new parent.
    legacy_state_path = path.parent.parent / STATE_FILE
    try:
        legacy_state = legacy_state_path.read_text(encoding="utf-8")
        decode_state(legacy_state)
    except (OSError, UnicodeError, TypeError, ValueError, KeyError):
        return

    # Move readable legacy state into the protected session subdirectory.
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(legacy_state, encoding="utf-8")
        legacy_state_path.unlink()
    except OSError:
        pass


def read_unscoped_state(path: Path | None) -> RunState | None:
    """Return one readable state document without applying run scope.

    The file is a boundary like any other: a session killed mid-write, a hand
    edit, or an absent scratch directory all produce something this cannot
    read, and each is answered the same way — as no state at all, which is a
    state the engine already knows how to work from.
    """

    # Return the established no-state result where no boundary exists.
    if path is None:
        return None

    # Collapse every unreadable or malformed boundary into that same result.
    try:
        return decode_state(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, TypeError, ValueError, KeyError):
        return None


def read_state(path: Path | None, branch: str) -> RunState | None:
    """Return what this branch's run remembered, or None where nothing does."""

    # Keep ordinary state scoped to the active branch and readiness label.
    stored = read_unscoped_state(path)
    if stored is None or stored.branch != branch or stored.label != READY_LABEL:
        return None
    return stored


def read_plan_state(path: Path | None, branch: str) -> RunState | None:
    """Return plan state, retaining an approval across a branch change."""

    # Read the session once and keep the readiness label as its scope boundary.
    stored = read_unscoped_state(path)
    if stored is None or stored.label != READY_LABEL:
        return None

    # A state directory identifies one invocation, whose approval must detect
    # rather than disappear on the branch change it was written to prevent;
    # unapproved state remains scoped to its original branch.
    if stored.branch != branch and stored.approval_met is None:
        return None
    return stored


def write_state(path: Path | None, state: RunState) -> str | None:
    """Store *state* and return where, or None where it was not stored.

    An ordinary run can continue from the tracker when its scratch directory
    cannot be written. A declared ticket cannot begin unless its contract and
    claim boundary can be stored there.
    """

    if path is None:
        return None

    # Preserve the established document byte shape when optional state is
    # unused.
    details = asdict(state)
    if state.progress is None:
        details.pop("progress")
    if state.approval_met is None:
        details = {
            key: value
            for key, value in details.items()
            if not key.startswith("approval_")
        }

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")
    except OSError:
        return None

    return str(path)


def read_routing(path: Path | None) -> Routing | None:
    """Return the run's frozen routing, or None where it never froze any.

    Absence and damage are different answers here, and that is the whole point
    of the file. An ordinary state file nothing can read is answered as no
    state; ordinary account fields are recovered, and checking verbs
    deliberately follow the undeclared path without its contract projection.
    A routing file nothing can read is answered as an error, because nothing
    else holds what it held and reconstructing it would mean routing this run's
    remaining work from a context it never ran under (ADR-0085, ADR-0138).
    """

    stored = routing_file(path)
    if stored is None or not stored.exists():
        return None

    try:
        held = json.loads(stored.read_text(encoding="utf-8"))
        snapshot = cast(dict[str, Any], held["snapshot"])
        snapshot["snapshot_identity"], snapshot["main_seat"]
        return Routing(
            snapshot=snapshot,
            model=None if held["model"] is None else str(held["model"]),
            deliberation=(
                None if held["deliberation"] is None else str(held["deliberation"])
            ),
            fast=bool(held.get("fast")),
            decisions=[
                RouteRecord(
                    request_id=str(record["request_id"]),
                    role=str(record["role"]),
                    ticket=(
                        None if record["ticket"] is None else int(record["ticket"])
                    ),
                    decision=cast(dict[str, Any], record["decision"]),
                    stage=str(record["stage"]),
                    workload_cohort=str(record["workload_cohort"]),
                    workload_tags=[str(tag) for tag in record["workload_tags"]],
                )
                for record in cast(list[dict[str, Any]], held["decisions"])
            ],
            attempts=cast(list[dict[str, Any]], held["attempts"]),
            run_identity=str(held.get("run_identity") or ""),
        )
    except (OSError, TypeError, ValueError, KeyError) as exc:
        raise RunError(
            f"this run's frozen routing at {stored} cannot be read ({exc})"
        ) from exc


def write_routing(path: Path | None, routing: Routing) -> str:
    """Store the frozen routing account, or say that it could not be stored.

    Unlike the ordinary state, this is not an optimisation a run can go on
    without: a frozen context nothing wrote down is one the next invocation
    cannot reuse, so a directory that will not take it stops the run here
    rather than at a claim it would then have to refuse.
    """

    stored = routing_file(path)
    if stored is None:
        raise RunError(
            "routing is frozen for the whole run, so it needs a state directory "
            "to be frozen in: pass --state-dir"
        )

    try:
        stored.parent.mkdir(parents=True, exist_ok=True)
        stored.write_text(
            json.dumps(
                {
                    "snapshot": routing.snapshot,
                    "model": routing.model,
                    "deliberation": routing.deliberation,
                    "fast": routing.fast,
                    "decisions": [asdict(record) for record in routing.decisions],
                    "attempts": routing.attempts,
                    "run_identity": routing.run_identity,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise RunError(
            f"this run's frozen routing could not be written: {exc}"
        ) from exc

    return str(stored)


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


def remember_progress(path: Path | None, cwd: Path, progress: ProgressState) -> None:
    """Keep session-owned dashboard values outside the disposable dashboard."""

    # Amend only an existing run account for the checked-out branch.
    state = remembered_state(path, cwd)
    if state is None:
        return

    # Preserve the next engine transition's reconstruction baseline.
    state.progress = progress
    write_state(path, state)


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

    `run_claimed` is the complete live claim account the plan derives for this
    run: `resuming` inside the current scope plus any live claims preserved
    outside an explicitly aimed scope. It is the claim state written for a real
    run and carried only in memory through a dry route.

    `solo` is the part of that shape a reader would otherwise have to infer:
    the tickets laid out in `waves` that declared they build alone, which is
    why each of them holds a wave nothing else is in. A ticket already recorded
    or stranded is in no wave and so in none of this either.

    `at_once` is the ceiling the developer set on how many tickets are built at
    the same time, and `starting` is what that makes of the frontier: the
    tickets this wave works, which is `workable` cut to the ceiling. `worktrees`
    is the isolation decision the ceiling carries with it — above one, each
    ticket is built in a working tree of its own, and at exactly one the work
    lands straight on the branch with nothing to integrate (ADR-0054).

    `model` and `deliberation` are the field-level locks this invocation puts
    on every building role, `fast` is the objective it puts on the whole run —
    the fastest configuration that holds quality rather than the cheapest —
    and `routing` is the frozen route account all three were frozen into: its
    identity, the main seat every verdict inherits, the snapshot a later
    request carries back unchanged, and every exact decision made under it. `routing_reason` is the other half of that answer: where
    there is no account to render, it says why, so a report never fills the gap
    in from what is current. `scope` is what the run was aimed at where it was
    aimed at anything — one entry per reference the developer named, and the
    tickets are the union of what they resolved to — and `state` is where the
    run left what it remembers of itself, all of it carried here because the
    plan is where the run says what it is about to do.
    """

    verb: str
    ready: bool
    reason: str | None
    dry_run: bool
    at_once: int
    worktrees: bool
    model: str | None
    deliberation: str | None
    fast: bool
    state: str | None
    routing: dict[str, Any] | None
    routing_reason: str | None
    branch: str
    default_branch: str | None
    label: str
    scope: list[dict[str, Any]] | None
    tickets: list[dict[str, Any]]
    workable: list[int]
    starting: list[int]
    claimed: list[int]
    resuming: list[int]
    run_claimed: list[int]
    recorded: list[int]
    stranded: list[int]
    blocked: list[int]
    waves: list[list[int]]
    solo: list[int]
    never_workable: list[int]
    approval_expected: str | None = None
    approval_identity: str | None = None
    approval_payload: ApprovalPayload | None = None


def plan_approval_payload(plan: Plan) -> ApprovalPayload:
    """Return exactly the plan fields a caller authorizes."""

    return {
        "branch": plan.branch,
        "default_branch": plan.default_branch,
        "scope": plan.scope,
        "at_once": plan.at_once,
        "worktrees": plan.worktrees,
        "model": plan.model,
        "deliberation": plan.deliberation,
        "waves": plan.waves,
        "solo": plan.solo,
    }


def plan_approval_identity(payload: ApprovalPayload) -> str:
    """Identify one authorized Orchestrate plan under its versioned domain."""

    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    prefix = f"kntnt-orchestrate-plan-v{APPROVAL_VERSION}\0".encode()
    return hashlib.sha256(prefix + canonical).hexdigest()


def approval_ceiling_refusal(plan: Plan, ceiling: ApprovalPayload) -> str | None:
    """Return why *plan* exceeds its first approved payload, if it does."""

    # Keep every execution dimension equal to its caller-authorized value.
    current = plan_approval_payload(plan)
    fixed_fields = (
        ("branch", ceiling["branch"], current["branch"]),
        ("default_branch", ceiling["default_branch"], current["default_branch"]),
        ("scope", ceiling["scope"], current["scope"]),
        ("at_once", ceiling["at_once"], current["at_once"]),
        ("worktrees", ceiling["worktrees"], current["worktrees"]),
        ("model", ceiling["model"], current["model"]),
        ("deliberation", ceiling["deliberation"], current["deliberation"]),
    )
    for field_name, authorized_value, current_value in fixed_fields:
        if current_value != authorized_value:
            return (
                f"the plan changes {field_name} from {authorized_value!r} "
                f"to {current_value!r} outside the approval ceiling"
            )

    # Reject work whose identity was absent from the authorized frontier.
    authorized = {int(number) for wave in ceiling["waves"] for number in wave}
    for wave in plan.waves:
        for number in wave:
            if number not in authorized:
                return f"the plan adds #{number} outside the approval ceiling"

    # Keep an authorized Solo Ticket isolated until it leaves the plan.
    current_tickets = {number for wave in plan.waves for number in wave}
    current_solo = set(plan.solo)
    for number in ceiling["solo"]:
        if number in current_tickets and number not in current_solo:
            return (
                f"the plan removes Solo protection from #{number} "
                "outside the approval ceiling"
            )

    return None


def plan_details(plan: Plan) -> dict[str, Any]:
    """Return the public plan, adding audit fields only when supplied."""

    details = asdict(plan)
    if plan.approval_expected is None:
        details.pop("approval_expected")
        details.pop("approval_payload")
    return details


def is_open_state(state: str) -> bool:
    """Say whether *state* requires no Ticket Resolution projection yet."""

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


def body_solo(body: str) -> bool:
    """Say whether a `Builds alone` line in *body* makes it a Solo Ticket."""

    return any(SOLO_LINE.match(line) for line in body.splitlines())


def body_commit_contract(body: str) -> list[dict[str, Any]] | None:
    """Return the ordered commit roles declared by *body*, if any.

    The declaration is `Commit roles: role: pattern, pattern; role: pattern`.
    A heading may instead put one `- role: patterns` entry on each following
    line. Patterns are Git pathspecs, interpreted by Git at the checking seam.
    """

    # Collect the sentence remainder and any list entries below a heading.
    written: list[str] = []
    declared = False
    lines = body.splitlines()
    for index, line in enumerate(lines):
        found = COMMIT_ROLES_LINE.match(line)
        if not found:
            continue
        declared = True
        if remainder := line[found.end() :].strip():
            written.extend(part.strip() for part in remainder.split(";"))
        for following in lines[index + 1 :]:
            if not following.strip():
                continue
            if not EDGE_LIST_ITEM.match(following):
                break
            written.append(EDGE_LIST_ITEM.sub("", following, count=1).strip())

    if not declared:
        return None
    if not written:
        raise RunError(
            "a `Commit roles` declaration must name at least one role and its "
            "Git pathspecs"
        )

    # Refuse declarations whose roles or allowed surfaces are incomplete.
    roles: list[dict[str, Any]] = []
    for entry in written:
        name, separator, surfaces = entry.partition(":")
        patterns = [
            pattern.strip() for pattern in surfaces.split(",") if pattern.strip()
        ]
        if not separator or not name.strip() or not patterns:
            raise RunError(
                "a `Commit roles` declaration must name each role and its "
                "Git pathspecs as `role: pattern, pattern`"
            )
        roles.append({"name": name.strip(), "patterns": patterns})

    if len({str(role["name"]) for role in roles}) != len(roles):
        raise RunError("a `Commit roles` declaration names the same role twice")

    return roles


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


def recorded_against(item: dict[str, Any]) -> tuple[str | None, str | None, list[int]]:
    """Return *item*'s historical Run Outcome, commit, and collision.

    The tracker is a boundary and a comment is prose anybody can write, so only
    an outcome this engine knows how to record is read back — a marker naming
    anything else is somebody else's writing and settles nothing. The last
    valid Run Outcome marker is retained as the unattended attempt's history;
    Reconciliation is read separately and never overwrites it.
    """

    # Read every valid marker and keep the latest historical Run Outcome.
    outcome: str | None = None
    commit: str | None = None
    against: list[int] = []
    for comment in item["comments"]:
        found = RECORDED_OUTCOME.search(str(comment["body"]))
        if found and found.group(1) in OUTCOMES:
            outcome, commit = found.group(1), found.group(2)
            against = numbers_in(found.group(3))

    return outcome, commit, against


def recorded_contract_base(item: dict[str, Any]) -> str | None:
    """Return the latest recorded completion's optional contract provenance."""

    base = None
    for comment in item["comments"]:
        if found := RECORDED_OUTCOME.search(str(comment["body"])):
            base = found.group(4)
    return base


def reconciled_at(item: dict[str, Any]) -> str | None:
    """Return the completion commit named by *item*'s Reconciliation."""

    # Keep the last readable event as the current Ticket Resolution provenance.
    completion_commit: str | None = None
    for comment in item["comments"]:
        found = RECORDED_RECONCILIATION.search(str(comment["body"]))
        if found:
            completion_commit = found.group(1)

    return completion_commit


def resolution_is_done(item: dict[str, Any], run_outcome: str | None) -> bool:
    """Say whether recorded history resolves *item* as completed work."""

    return run_outcome == DONE or reconciled_at(item) is not None


def as_references(numbers: list[int]) -> str:
    """Render ticket *numbers* the way a developer writes them."""

    return ", ".join(f"#{number}" for number in numbers)


def numbers_in(listed: str | None) -> list[int]:
    """Read back a marker's comma-separated ticket numbers, in the order given.

    Empty where the marker carried none, an outcome other than a collision
    having nothing on the other side of it to name.
    """

    return [int(number) for number in listed.split(",")] if listed else []


def engine_wrote(body: str) -> bool:
    """Say whether *body* is this engine talking to its next self.

    A recorded outcome, a rebuild note, an amend note, and a blocked note are
    written by a run, for a run: what they say is that this ticket has been
    here before, which is the one thing a builder briefed on the ticket has no
    use for. Read by exactly the patterns that write them, so nothing else a
    comment carries counts as the engine's — a marker naming an outcome this
    engine never records is prose somebody else wrote, and prose is relayed
    rather than interpreted.
    """

    outcome = RECORDED_OUTCOME.search(body)
    return (
        (outcome is not None and outcome.group(1) in OUTCOMES)
        or RECORDED_REBUILD.search(body) is not None
        or RECORDED_AMEND.search(body) is not None
        or RECORDED_BLOCKED.search(body) is not None
        or RECORDED_RECONCILIATION.search(body) is not None
    )


def thread_of(item: dict[str, Any]) -> list[Remark]:
    """Return what people have written on *item*, in the order they wrote it.

    The tracker's unit of record is the thread, so this is the rest of the
    ticket: everything said on it after it was filed, minus what a run wrote
    there itself. Nothing here reads what any of it says — the thread is
    relayed to a subagent whole, and the subagent is what reads it (ADR-0065).
    """

    return [
        Remark(
            author=str((comment.get("author") or {}).get("login", "")),
            created_at=str(comment.get("createdAt", "")),
            body=str(comment["body"]),
        )
        for comment in item["comments"]
        if not engine_wrote(str(comment["body"]))
    ]


def rebuilt_already(item: dict[str, Any]) -> bool:
    """Say whether a run has already spent *item*'s one rebuild on it."""

    return any(
        RECORDED_REBUILD.search(str(comment["body"])) for comment in item["comments"]
    )


def recorded_amend_state(item: dict[str, Any]) -> AmendState | None:
    """Return *item*'s latest append-only amend state, if it carries one.

    A numbered event carries the exact lifecycle phase and, where needed, the
    complete verdict after the fixed heading. The historical unnumbered event
    counts as attempt one but cannot reconstruct a phase it never recorded.
    """

    # Read every marker and retain the last event as the current phase.
    state: AmendState | None = None
    for comment in item["comments"]:
        body = str(comment["body"])
        found = RECORDED_AMEND.search(body)
        if found:
            attempt = int(found.group(1) or "1")
            phase = found.group(2) or AMEND_LEGACY
            _, heading, verdict = body.partition(AMEND_VERDICT_HEADING)
            state = AmendState(
                attempt=attempt,
                phase=phase,
                verdict=verdict if heading else None,
            )

    return state


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
    settles nothing. The tracker state is fetched once per number; the caller
    combines closure with Run Outcome and Reconciliation to decide whether the
    blocker's requested work is complete.
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


def blocker_still_blocks(cwd: Path, number: int, state: str) -> bool:
    """Say whether blocker *number* lacks a done Ticket Resolution."""

    # Open work has no completed resolution to project.
    if is_open_state(state):
        return True

    # Read the facts needed to distinguish completion from mere closure.
    try:
        ticket = ticket_view(cwd, number, "number,comments")
    except RunError as exc:
        raise RunError(
            f"#{number} is closed, but the tracker cannot say how its work resolved: {exc}"
        ) from exc

    # Project completion through the same rule Report uses.
    outcome, _, _ = recorded_against(ticket)
    return not resolution_is_done(ticket, outcome)


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
            {
                int(node["number"])
                for node in nodes
                if blocker_still_blocks(cwd, int(node["number"]), str(node["state"]))
            }
        )

    # A body edge is a bare number, so the state behind it is asked for.
    return sorted(
        number
        for number in set(body_edges(str(item["body"])))
        if blocker_still_blocks(cwd, number, ticket_state(cwd, number, states))
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


def named_parent(item: dict[str, Any]) -> int | None:
    """Return the spec *item* belongs to, saying which ticket carries a bad line.

    The reference alone would leave the whole label to be searched by hand for
    whichever ticket nobody can read.
    """

    try:
        return parent_of(item)
    except RunError as exc:
        raise RunError(f"#{int(item['number'])}: {exc}") from exc


@dataclass
class Aim:
    """One thing a run was aimed at, and which of two things it named.

    A run given no reference has no scope at all: every ticket the label holds
    is in, which is what a bare invocation has always meant. A run given
    several references is aimed at each of them, and its scope is the union of
    what they resolve to — every reference is read on its own exactly as a lone
    one is, so a ticket named twice, or named beside the spec that holds it,
    names the same set as either alone. A reference narrows the set the same
    questions are asked of and changes no rule about any ticket in it — an
    outcome already recorded still settles a ticket somebody names, and a
    blocking edge still holds one back (ADR-0053).

    `kind` is what the reference resolved to, `number` the ticket it named, and
    `reference` what the developer wrote, kept so the plan answers in the terms
    it was asked in.
    """

    reference: str
    kind: str
    number: int


def scope_numbers(reference: str) -> dict[int, str]:
    """Return the tickets *reference* names, each mapped to how it was written.

    A run may be aimed at one reference or at several, so the value is read as
    the set of them: the same ticket named twice is the same ticket, and the
    first way the developer wrote it is how the plan answers for it.

    One reference nobody can read refuses the whole invocation, because every
    way of going on is worse than stopping: dropping it works a scope the
    developer did not name, and picking one of two readings works tickets they
    never named at all.
    """

    # A reference in another tracker's terms is refused for the reason a body
    # edge written that way is: one repository's tracker is all a run reads.
    named = reference.strip()
    qualified = QUALIFIED_REFERENCE.search(named)
    if qualified:
        raise RunError(
            f"'{qualified.group()}' names another repository's tracker, and a "
            "run reads one: write it as #number"
        )

    # Every part of the value has to read as a number, and the parts that do
    # not are kept as they were written.
    numbered: dict[int, str] = {}
    unreadable: list[str] = []
    for part in re.split(r"[\s,]+", named):
        if not part:
            continue
        if (found := SCOPE_REFERENCE.match(part)) is None:
            unreadable.append(part)
        else:
            numbered.setdefault(int(found.group(1)), part)

    # The refusal names those parts rather than the whole value, or a developer
    # who wrote a list would be left to find which of it nobody could read. A
    # value naming nothing at all is quoted whole, having no part to name.
    if unreadable or not numbered:
        raise RunError(
            f"'{' '.join(unreadable) or named}' names no ticket or spec: "
            "write it as #number"
        )

    return numbered


def native_children(cwd: Path, number: int) -> list[int]:
    """Return the tickets the tracker itself files under *number*.

    This is the relation a `Parent` line in a body stands in for, and asking
    for it is also how a reference the tracker can answer for is told from one
    it cannot.
    """

    try:
        view = ticket_view(cwd, number, "number,subIssues")
        return [int(node["number"]) for node in view["subIssues"]["nodes"]]
    except (RunError, KeyError) as exc:
        raise RunError(
            f"#{number} is what this run was aimed at, and the tracker cannot "
            f"say what it is: {exc}"
        ) from exc


def resolve_scope(cwd: Path, reference: str, listed: list[dict[str, Any]]) -> list[Aim]:
    """Work out what *reference* aims the run at, reference by reference.

    A reference the tracker files children under is a spec, and the body is the
    same fallback here as it is for a blocking edge: where the relation carries
    nothing, a ticket naming this one as its parent settles it. Everything else
    the tracker can answer for is a ticket, and is worked alone. Children win
    that reading wherever both are available, because a spec is the shape of
    other work rather than work itself, and building one is what nobody meant.

    Several references are resolved independently and mean the union of what
    they come back with, so what a reference names is never a function of what
    was named beside it.
    """

    # Asking the tracker settles both halves of the question for each
    # reference: what it is, and whether it is anything at all. What it files
    # children under is a spec, and where it files none, a ticket naming this
    # one as its parent is the other way the breakdown writes the relation.
    aims = []
    for number, written in scope_numbers(reference).items():
        filed = bool(native_children(cwd, number)) or any(
            named_parent(item) == number for item in listed
        )
        aims.append(
            Aim(reference=written, kind=SPEC if filed else TICKET, number=number)
        )

    return aims


def in_scope(item: dict[str, Any], scope: list[Aim] | None) -> bool:
    """Whether *item* is one of the tickets the run was aimed at.

    The scope is the union of what the references resolved to, so a ticket any
    one of them reaches is in.
    """

    if scope is None:
        return True

    # A ticket named by number is in on its own account.
    number = int(item["number"])
    if any(aim.number == number for aim in scope if aim.kind == TICKET):
        return True

    # A spec in the aim is what makes a parent a question at all: where none
    # was named no body is read for one, so a ticket carrying a `Parent` line
    # nobody can read stops a run aimed at ticket numbers no more than it ever
    # did.
    specs = [aim.number for aim in scope if aim.kind == SPEC]
    return bool(specs) and named_parent(item) in specs


def waves_of(tickets: list[Ticket]) -> tuple[list[list[int]], list[int]]:
    """Lay *tickets* out in waves, and name the ones no wave can hold.

    A wave is the tickets whose blockers are all settled by the waves before
    it, so wave one is the frontier. Waves stop as soon as one comes back
    empty, which is what a cycle or a blocker outside the scope produces: the
    tickets left over are workable in no wave of this run, and the walk ends
    rather than turning over a frontier that never grows.

    A Solo Ticket is the one exception, and it is not an exception to the
    graph: it takes the first wave the blockers admit it in, exactly as it
    would have, and takes it alone. Its admissible siblings fall to the wave
    behind it — they are not blocked by it, and no edge could say they must
    wait, because what it excludes is every ticket that would write a new
    instance of the invariant it is rewriting (ADR-0099).
    """

    waiting = {ticket.number: set(ticket.blocked_by) for ticket in tickets}
    alone = {ticket.number for ticket in tickets if ticket.builds_alone}
    settled: set[int] = set()
    waves: list[list[int]] = []
    while waiting:
        wave = sorted(
            number for number, blockers in waiting.items() if blockers <= settled
        )
        if not wave:
            break

        # Where the frontier holds more than one ticket that rides alone, each
        # still rides alone: the first takes this wave and the rest come round
        # again, one wave at a time, in the order the plan already reads in.
        riding = next((number for number in wave if number in alone), None)
        if riding is not None:
            wave = [riding]

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
    recorded = {ticket.number for ticket in tickets if ticket.resolution.outcome}
    stranded: set[int] = set()
    spreading = [
        ticket.number
        for ticket in tickets
        if ticket.resolution.outcome not in (None, DONE)
    ]
    while spreading:
        for dependent in dependents.get(spreading.pop(), []):
            if dependent not in recorded and dependent not in stranded:
                stranded.add(dependent)
                spreading.append(dependent)

    return sorted(stranded)


def listed_tickets(
    cwd: Path, *query: str, label: str = READY_LABEL
) -> list[dict[str, Any]]:
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
        label,
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
    collided_with: list[int],
) -> Ticket:
    """Build one ticket out of what the tracker answered about it.

    Everything readable straight off that answer is read here. What costs the
    tracker a second question, or a judgement about the graph, is settled by
    the caller and passed in.
    """

    # Project current resolution and amend phase without rewriting history.
    run_outcome = outcome
    reconciliation_commit = reconciled_at(item)
    current_outcome = DONE if resolution_is_done(item, outcome) else outcome
    amend_state = recorded_amend_state(item)

    return Ticket(
        number=int(item["number"]),
        title=str(item["title"]),
        url=str(item["url"]),
        body=str(item["body"]),
        thread=thread_of(item),
        parent=parent_of(item),
        claimed_by=holders_of(item),
        blocked_by=blocked_by,
        resolution=TicketResolution(
            outcome=current_outcome,
            commit=reconciliation_commit or commit,
            run_outcome=run_outcome,
            is_reconciled=reconciliation_commit is not None,
        ),
        collided_with=collided_with,
        amends_spent=amend_state.attempt if amend_state else 0,
        amend_state=amend_state,
        builds_alone=body_solo(str(item["body"])),
        commit_contract=body_commit_contract(str(item["body"])),
        contract_base=recorded_contract_base(item),
    )


def open_listing(cwd: Path) -> list[dict[str, Any]]:
    """Return the open tickets the label holds, as the tracker answers for them.

    Asked for by label, a ticket without that label being unfinished thinking
    that is never worked. What a run was aimed at narrows this afterwards: the
    whole label is read either way, because an edge out of the aim points at a
    ticket in here and its state settles whether it still blocks.
    """

    return listed_tickets(
        cwd,
        "--state",
        "open",
        "--json",
        "number,title,url,body,parent,assignees,blockedBy,comments",
    )


def closed_since(cwd: Path) -> str | None:
    """Return the day this branch left the default one, or None where none can.

    The closed half of a scope is every ticket a run has ever finished, which
    grows for the life of the project and can only end in a refusal. The fork
    point bounds it honestly: it is an ancestor of everything this run built,
    so nothing this run recorded is earlier than it, and everything the
    project finished before this branch existed is.

    A day rather than an instant, because a whole day of slack in the safe
    direction costs a handful of tickets nobody reads and saves the question
    of whose clock settles a boundary. None where there is nothing to bound
    by — no default branch to fork from, the default branch itself in hand,
    or no common ancestor to find — and the full-page guard is what answers
    for the question then, as it always did.
    """

    # Nothing to fork from is nothing to bound by: no default to name it, or
    # the default itself in hand, and the question is left whole.
    branch = current_branch(cwd)
    default = default_branch(cwd)
    if default is None or default == branch:
        return None

    # The fork commit's own day, in the shape the tracker reads as a whole day.
    try:
        fork = git(cwd, "merge-base", "HEAD", default).strip()
        return git(cwd, "show", "--no-patch", "--format=%cs", fork).strip()
    except RunError:
        return None


def closed_listing(cwd: Path) -> list[dict[str, Any]]:
    """Return the finished tickets this machine's runs took on this branch.

    The ready label discovers unsuccessful work closed before Reconciliation;
    the neutral historical label discovers tickets whose active workflow state
    was cleaned on completion. The fork date bounds that growing history to
    what this branch could have recorded.
    """

    # A branch with nothing to fork from bounds nothing, and the question is
    # asked whole — where the guard against a full page is what answers.
    since = closed_since(cwd)
    bound = ["--search", f"closed:>={since}"] if since else []

    # An unsuccessful ticket closed outside Orchestrate still carries the
    # ready label until Reconciliation replaces its active lifecycle state.
    active = listed_tickets(
        cwd,
        "--state",
        "closed",
        *bound,
        "--json",
        "number,title,url,body,parent,assignees,comments",
        label=READY_LABEL,
    )
    historical = listed_tickets(
        cwd,
        "--state",
        "closed",
        *bound,
        "--json",
        "number,title,url,body,parent,assignees,comments",
        label=HISTORICAL_LABEL,
    )

    # Merge both discovery paths by identity so an interrupted transition that
    # temporarily carries both labels remains one ticket in the final account.
    found = {int(item["number"]): item for item in active}
    found.update({int(item["number"]): item for item in historical})
    return list(found.values())


def tickets_in_scope(
    cwd: Path, listed: list[dict[str, Any]], scope: list[Aim] | None
) -> list[Ticket]:
    """Return the open tickets the run was aimed at, oldest first.

    Ordered by number rather than by whatever order the tracker answers in, so
    that a plan is the same plan on two invocations with nothing changed.
    """

    # Every ticket the label holds is open, the query having asked for open
    # ones, so an edge pointing at one costs the tracker no second question —
    # including an edge pointing out of what the run was aimed at, which is
    # work this run will not do and still has to wait for.
    states = {int(item["number"]): "OPEN" for item in listed}

    # A body that cannot be read stops the plan, and says which ticket to go
    # and fix — the reference alone would leave the scope to be searched by
    # hand for whichever ticket carries it.
    tickets = []
    for item in listed:
        if not in_scope(item, scope):
            continue
        number = int(item["number"])
        try:
            outcome, commit, against = recorded_against(item)
            tickets.append(
                ticket_from(
                    item,
                    blocked_by=unmet_blockers(cwd, item, states),
                    outcome=outcome,
                    commit=commit,
                    collided_with=against,
                )
            )
        except RunError as exc:
            raise RunError(f"#{number}: {exc}") from exc

    return sorted(tickets, key=lambda ticket: ticket.number)


def tickets_recorded(
    listed: list[dict[str, Any]], scope: list[Aim] | None
) -> list[Ticket]:
    """Return closed tickets carrying an outcome or Reconciliation, oldest first.

    Closing is what takes a ticket out of the open scope, so the report would
    lose exactly the tickets it most needs to name if it read that scope alone
    — and done is not the only outcome a closed ticket carries. A ticket this
    run recorded failed is closed too once a person finishes it, or once the
    tracker reads a commit trailer off the default branch, and it was this
    run's all the same: the run claimed it, built it, and wrote an outcome on
    it. A parked ticket reconciled after manual completion instead carries the
    Reconciliation marker alone. Both engine facts are read back here, and a
    ticket closed carrying neither was never this run's to account for —
    accounting for it would be a report nobody can check.
    """

    # No edge is read off a finished ticket. There is nothing left for it to
    # wait for, and asking the tracker about a blocker named in its body is a
    # question whose answer could only ever fail the report.
    tickets = []
    for item in listed:
        if not in_scope(item, scope):
            continue
        number = int(item["number"])
        outcome, commit, against = recorded_against(item)
        if outcome is None and not resolution_is_done(item, outcome):
            continue
        try:
            tickets.append(
                ticket_from(
                    item,
                    blocked_by=[],
                    outcome=outcome,
                    commit=commit,
                    collided_with=against,
                )
            )
        except RunError as exc:
            raise RunError(f"#{number}: {exc}") from exc

    return sorted(tickets, key=lambda ticket: ticket.number)


def say_where_work_stands(cwd: Path, tickets: list[Ticket], run_branch: str) -> None:
    """Tell each of *tickets* which working tree still holds its work, if any.

    Asked of the repository once and answered for the whole set, rather than
    threaded through the reading of the tracker: where a ticket's work stands
    is the repository's answer and the tracker has no opinion about it.
    """

    open_now = open_worktrees(cwd, run_branch)
    for ticket in tickets:
        ticket.worktree = open_now.get(ticket.number)


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
    recorded = [
        ticket.resolution.commit
        for ticket in tickets
        if ticket.resolution.commit and not ticket.resolution.is_reconciled
    ]
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

    # A ceiling-one multi-commit ticket records the real pre-pass boundary,
    # which remains available after the scratch state has gone.
    oldest_ticket = next(
        (
            ticket
            for ticket in tickets
            if ticket.resolution.commit == oldest and ticket.contract_base
        ),
        None,
    )
    if oldest_ticket is not None:
        return cast(str, oldest_ticket.contract_base)

    # A run whose first recorded commit is the repository's root sits on that
    # commit itself: there is nothing before it to name.
    try:
        return git(cwd, "rev-parse", "--verify", f"{oldest}^").strip()
    except RunError:
        return oldest


def claimed_elsewhere(
    remembered: RunState | None,
    scope: list[Aim] | None,
    listed: list[dict[str, Any]],
    tickets: list[Ticket],
) -> set[int]:
    """Return the live claims of this run's that the plan was not aimed at.

    A run aimed at part of the graph revises only the claims it read about. A
    claim an earlier, wider plan of the same run took stands where it is, or
    the next invocation would find this run's own claim unaccounted for and
    read it as a stranger's — which is the one thing the state exists to
    prevent.

    Only a claim the label still holds open survives that. A ticket the tracker
    has finished with is one this run no longer holds, and preserving it would
    leave an aimed run's note growing with numbers a bare run prunes.
    """

    if scope is None or remembered is None:
        return set()

    open_now = {int(item["number"]) for item in listed}
    return open_now.intersection(remembered.claimed).difference(
        ticket.number for ticket in tickets
    )


def uncommitted_refusal(cwd: Path) -> str | None:
    """Return why a run may not work this repository, or None where it may.

    Asked wherever the run puts work on the branch the developer is standing
    on — when it plans, and again before a ticket is recorded done. A change
    nothing has committed is one the run cannot tell from a builder's: at a
    ceiling of one it lands inside the ticket's own commit, and above one it
    stops a merge that had nothing to collide with. What the repository
    ignores is not work and does not count.
    """

    if not git(cwd, "status", "--porcelain").strip():
        return None

    return (
        "the working tree holds work nothing has committed: a run would "
        "commit it under a ticket that did not make it"
    )


def no_ticket_reason(scope: list[Aim] | None) -> str:
    """Say why there is nothing to work, in the terms the run was asked in."""

    if scope is None:
        return f"no open ticket carries '{READY_LABEL}'"

    # One reference says which of the two things it named came back empty.
    if len(scope) == 1:
        aim = scope[0]
        if aim.kind == TICKET:
            return f"#{aim.number} is not an open ticket carrying '{READY_LABEL}'"
        return f"no child of #{aim.number} is an open ticket carrying '{READY_LABEL}'"

    # Several are named together: the scope is their union, so no one of them
    # is what came back empty.
    named = as_references([aim.number for aim in scope])
    return f"nothing {named} names is an open ticket carrying '{READY_LABEL}'"


def build_plan(
    cwd: Path,
    *,
    dry_run: bool,
    at_once: int,
    model: str | None,
    deliberation: str | None,
    fast: bool,
    state_path: Path | None,
    reference: str | None,
    approval: str | None,
) -> Plan:
    """Gather what a run in *cwd* would work, and whether it may start."""

    # What earlier waves of this run wrote down is where the plan starts, not
    # where it ends: a ticket already settled is never offered again, and what
    # waits on a settled failure is stranded rather than worked on top of code
    # that was never built.
    branch = current_branch(cwd)
    default = default_branch(cwd)
    remembered = read_plan_state(state_path, branch)
    routing, routing_reason, damaged = frozen_routing(state_path)
    listed = open_listing(cwd)
    scope = resolve_scope(cwd, reference, listed) if reference is not None else None
    tickets = tickets_in_scope(cwd, listed, scope)
    say_where_work_stands(cwd, tickets, branch)
    recorded = [ticket.number for ticket in tickets if ticket.resolution.outcome]
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
    held = [
        ticket
        for ticket in tickets
        if ticket.claimed_by and not ticket.resolution.outcome
    ]

    login = my_login(cwd, remembered) if held else None
    resuming = [
        ticket.number
        for ticket in held
        if ticket.claimed_by == [login]
        and (remembered is None or ticket.number in remembered.claimed)
    ]
    claimed = [ticket.number for ticket in held if ticket.number not in resuming]
    workable = sorted(frontier.difference(claimed))

    # Derive the exact claim account a real plan writes and a dry plan carries.
    run_claimed = sorted(
        set(resuming) | claimed_elsewhere(remembered, scope, listed, tickets)
    )

    plan = Plan(
        verb="plan",
        ready=True,
        reason=None,
        dry_run=dry_run,
        at_once=at_once,
        worktrees=at_once > ONE_AT_A_TIME,
        model=model,
        deliberation=deliberation,
        fast=fast,
        state=None,
        routing=routing_details(routing),
        routing_reason=routing_reason,
        branch=branch,
        default_branch=default,
        label=READY_LABEL,
        scope=None if scope is None else [asdict(aim) for aim in scope],
        tickets=[ticket_details(ticket) for ticket in tickets],
        workable=workable,
        starting=workable[:at_once],
        claimed=claimed,
        resuming=resuming,
        run_claimed=run_claimed,
        recorded=recorded,
        stranded=stranded,
        blocked=[ticket.number for ticket in tickets if ticket.number not in frontier],
        waves=waves,
        solo=[
            ticket.number
            for ticket in tickets
            if ticket.builds_alone and ticket.number not in settled
        ],
        never_workable=never_workable,
    )

    # Identify the complete caller-authorized frontier independently of ticket
    # prose, tracker comments, and the branch's moving base commit.
    plan.approval_expected = approval
    plan.approval_payload = plan_approval_payload(plan)
    plan.approval_identity = plan_approval_identity(plan.approval_payload)

    # Hold later unflagged work below the first caller-authorized frontier.
    ceiling_refusal: str | None = None
    drifted_state: RunState | None = None
    if (
        approval is None
        and remembered is not None
        and remembered.approval_met is True
        and remembered.approval_payload is not None
    ):
        ceiling_refusal = approval_ceiling_refusal(plan, remembered.approval_payload)

        # Preserve the ceiling audit while recording the refused identity.
        if ceiling_refusal is not None:
            plan.approval_expected = remembered.approval_expected
            plan.approval_payload = remembered.approval_payload
            drifted_state = replace(
                remembered,
                branch=branch,
                approval_identity=plan.approval_identity,
                approval_met=False,
            )

    # A run works the branch the developer left it on, whichever branch that
    # is (ADR-0064), so the tree it would commit in is the only thing left to
    # refuse about the state it starts in: a run cannot tell work the developer
    # left uncommitted from the work it is about to do.
    if dry_run:
        plan.ready = False
        plan.reason = "dry run: nothing is started"
    elif (standing := uncommitted_refusal(cwd)) is not None:
        plan.ready = False
        plan.reason = standing
    elif not tickets:
        plan.ready = False
        plan.reason = no_ticket_reason(scope)
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
    elif (
        adrift := routing_refusal(routing, damaged, resuming, model, deliberation, fast)
    ) is not None:
        plan.ready = False
        plan.reason = adrift
    if approval is not None and approval != plan.approval_identity:
        plan.ready = False
        plan.reason = (
            "the caller's approval does not match this plan: expected "
            f"{approval}, computed {plan.approval_identity}"
        )
    elif ceiling_refusal is not None:
        plan.ready = False
        plan.reason = ceiling_refusal

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
                claimed=plan.run_claimed,
                base=run_base(cwd, tickets),
                starting=plan.starting,
                contracts={
                    ticket.number: ticket.commit_contract
                    for ticket in tickets
                    if ticket.commit_contract is not None
                },
                contract_bases=remembered.contract_bases if remembered else {},
                progress=remembered.progress if remembered else None,
                approval_expected=(
                    approval
                    if approval is not None
                    else remembered.approval_expected
                    if remembered
                    else None
                ),
                approval_identity=(
                    plan.approval_identity
                    if approval is not None
                    else remembered.approval_identity
                    if remembered
                    else None
                ),
                approval_payload=(
                    plan.approval_payload
                    if approval is not None
                    else remembered.approval_payload
                    if remembered
                    else None
                ),
                approval_met=(
                    True
                    if approval is not None
                    else remembered.approval_met
                    if remembered
                    else None
                ),
            ),
        )
    elif not dry_run and drifted_state is not None:
        plan.state = write_state(state_path, drifted_state)
    elif not dry_run and approval is not None and approval != plan.approval_identity:
        plan.state = write_state(
            state_path,
            RunState(
                branch=branch,
                label=READY_LABEL,
                login=remembered.login if remembered else None,
                claimed=[],
                base=run_base(cwd, tickets),
                starting=[],
                contracts={},
                contract_bases={},
                progress=remembered.progress if remembered else None,
                approval_expected=approval,
                approval_identity=plan.approval_identity,
                approval_payload=plan.approval_payload,
                approval_met=False,
            ),
        )

    return plan


def cmd_plan(
    cwd: Path,
    *,
    dry_run: bool,
    at_once: int,
    model: str | None,
    deliberation: str | None,
    fast: bool,
    state_path: Path | None,
    reference: str | None,
    approval: str | None,
) -> int:
    """Print the plan, and answer whether work may start."""

    # A ceiling below one is a run that works no ticket at all, which is a run
    # nobody meant — and it is settled before the tracker is read, an argument
    # nothing can act on being no reason to go and ask about tickets.
    if at_once < ONE_AT_A_TIME:
        return fail(
            "--at-once caps how many tickets are worked at once, so it is at least 1"
        )

    try:
        plan = build_plan(
            cwd,
            dry_run=dry_run,
            at_once=at_once,
            model=model,
            deliberation=deliberation,
            fast=fast,
            state_path=state_path,
            reference=reference,
            approval=approval,
        )
    except RunError as exc:
        return fail(str(exc))

    emit(plan_details(plan))
    return 0 if plan.ready else 2


def workload_identity(role: str) -> dict[str, Any]:
    """Return the Cohort one building role's work belongs to.

    A Cohort is a role and a kind of work, and the request name this Skill
    writes is where the engine already reads both. The stage is that role; the
    Cohort is the workload stratum the role is charged to, under this Skill's
    own namespace; and the tags are empty, those two facts being the whole of
    what Orchestrate states about the work it routes. Deriving all three from
    the name alone is what lets the request the agent writes and the decision
    the engine froze name the same Cohort without either checking the other.
    """

    return {
        "stage": role,
        "workload_cohort": f"{OBSERVED_COHORT_PREFIX}{OBSERVED_STRATA[role]}",
        "workload_tags": [],
    }


def route_record(request_id: str, decision: dict[str, Any]) -> RouteRecord:
    """Read one decision's request name back into the role it was made for.

    The names are Orchestrate's own, so an unreadable one is this Skill's own
    mistake and is refused rather than kept: a decision nothing can attach to a
    role is a decision no gate can find when the work it covers is dispatched.
    """

    # A verdict is refused by name, before anything else is read of it. The
    # seat a verdict runs on is the orchestrator's own and is inherited whole,
    # so there is no decision about it for anybody to make (ADR-0085).
    if any(
        request_id == role or request_id.startswith(f"{role}-")
        for role in VERDICT_ROLES
    ):
        raise RunError(
            f"{request_id} routes a verdict, and a verdict is never routed: it "
            "inherits the orchestrating session's complete main seat exactly"
        )

    named = ROUTE_REQUEST.match(request_id)
    if named is None:
        raise RunError(
            f"{request_id} is not a request this run makes: an execution "
            "request is build-<ticket>, amend-<ticket>-<attempt>, "
            "repair-<ticket>, rebuild-<ticket>, or wave-fix-<wave>"
        )

    # One of the three alternatives matched, and each names its own role.
    ticket: int | None
    if named["role"]:
        role, ticket = str(named["role"]), int(named["ticket"])
    elif named["amended"]:
        role, ticket = "amend", int(named["amended"])
    else:
        role, ticket = "wave-fix", None
    return RouteRecord(request_id, role, ticket, decision, **workload_identity(role))


def read_response(response: Path) -> dict[str, Any]:
    """Return what model-selector answered at *response*, or say it did not."""

    try:
        return cast(dict[str, Any], json.loads(response.read_text(encoding="utf-8")))
    except (OSError, TypeError, ValueError) as exc:
        raise RunError(
            f"{response} is not a model-selector route response: {exc}"
        ) from exc


def routed_response(
    answered: dict[str, Any],
) -> tuple[dict[str, Any], list[RouteRecord]]:
    """Read one public route response into its snapshot and its decisions.

    Only the structure this engine acts on is checked here — the version of the
    Interface, the frozen context's identity and main seat, and each decision's
    request name and status. Everything inside a decision is model-selector's
    to say and is kept exactly as it said it (ADR-0083).
    """

    try:
        if answered["schema_version"] != ROUTE_SCHEMA_VERSION:
            raise RunError(
                f"this response answers version {answered['schema_version']} of "
                f"the model-selector route response, and this run reads version "
                f"{ROUTE_SCHEMA_VERSION}"
            )
        decisions = cast(list[dict[str, Any]], answered["decisions"])
        for decision in decisions:
            if decision["status"] not in (*ROUTE_ACCEPTABLE, ROUTE_REFUSED):
                raise RunError(
                    f"{decision['request_id']} came back {decision['status']}, "
                    "which is no decision this Interface makes"
                )
        snapshot = cast(dict[str, Any], answered["snapshot"])
        if snapshot["snapshot_identity"] is None or snapshot["main_seat"] is None:
            raise RunError("this response's snapshot names no identity or main seat")
    except RunError:
        raise
    except (OSError, TypeError, ValueError, KeyError) as exc:
        raise RunError(f"this is not a model-selector route response: {exc}") from exc

    return snapshot, [
        route_record(str(decision["request_id"]), decision) for decision in decisions
    ]


def emit_route(
    identity: str | None, records: list[RouteRecord], refusals: list[dict[str, Any]]
) -> None:
    """Print what one route call decided, and what it refused."""

    emit(
        {
            "verb": "route",
            "snapshot_identity": identity,
            "routing_capability": routing_capability(records),
            "decisions": [asdict(record) for record in records],
            "refused": refusals,
        }
    )


def frozen_refusal(routing: Routing, snapshot: dict[str, Any]) -> str | None:
    """Return why *snapshot* is not the one this run froze, or None where it is."""

    identity = str(snapshot["snapshot_identity"])
    if identity != routing.identity:
        return (
            f"this response carries snapshot {identity} where the run froze "
            f"{routing.identity}: every later wave and every resumed invocation "
            "reuses the snapshot the first frontier was routed from"
        )

    if snapshot != routing.snapshot:
        return (
            f"this response changes the frozen snapshot {identity} under its own "
            "identity, so the context it names is not the context it carries"
        )

    return None


def locks_refusal(
    routing: Routing,
    model: str | None,
    deliberation: str | None,
    fast: bool,
    invocation: str,
) -> str | None:
    """Return why these locks are not this run's own, or None where they are."""

    if (model, deliberation, fast) == (
        routing.model,
        routing.deliberation,
        routing.fast,
    ):
        return None

    return (
        f"{invocation} locks {described_locks(model, deliberation, fast)} where "
        "this run's routing was frozen for "
        f"{described_locks(routing.model, routing.deliberation, routing.fast)}: "
        "the fields the first frontier was routed under cannot change mid-run"
    )


def described_locks(model: str | None, deliberation: str | None, fast: bool) -> str:
    """Say in words which building fields and objective an invocation locked."""

    named = [
        f"--model={model}" if model else "no model",
        f"--deliberation={deliberation}" if deliberation else "no deliberation",
        "--fast" if fast else "no fast",
    ]
    return ", ".join(named[:-1]) + f", and {named[-1]}"


def claims_refusal(state: RunState) -> str | None:
    """Return why a run may not freeze a first snapshot now, or None where it may.

    A run holding claims has routed already, whatever is left of the file that
    said so. Freezing a context today's environment produced would decide the
    rest of the night from facts the claimed work was never done under, so this
    seam asks what the plan asks rather than trusting that the plan was reached
    (ADR-0085).
    """

    if not state.claimed:
        return None

    return (
        f"{as_references(state.claimed)} stand claimed by this run and its "
        "frozen routing is gone: a first snapshot frozen now would not be the "
        "one that work was claimed under"
    )


def batch_refusal(state: RunState, records: list[RouteRecord]) -> str | None:
    """Return why an opening batch is not the plan's frontier, or None where it is.

    Only the opening batch is held to this. A frontier routed a ticket at a
    time is a frontier whose tickets were each decided against a different set
    of peers, so the run's first request is the whole of what the plan said it
    starts, in that order. Every request after it is a smaller thing by nature
    — one replacement, one amend attempt, one repair, one reroute after a
    mechanical repair — and what keeps those honest is the claim and dispatch
    gates asking for the exact role rather than a shape asked of the batch.
    """

    batched = [record.ticket for record in records if record.role == "build"]
    if batched == state.starting:
        return None

    return (
        f"this batch routes {batched or 'no ticket'} where the plan's starting "
        f"frontier is {state.starting}: the preflight batches that frontier, in "
        "that order, before anything is claimed"
    )


def escalated_wave(request_id: str) -> str | None:
    """Return the wave whose fix round *request_id* escalates, or None."""

    named = ROUTE_REQUEST.match(request_id)
    if named is None or not named["escalated"]:
        return None
    return str(named["wave"])


def escalation_refusal(routing: Routing, records: list[RouteRecord]) -> str | None:
    """Return why an escalated wave fix may not be frozen, or None where it may.

    A changed-nothing fix round under a selected configuration buys exactly one
    further decision, because the inference the stop rests on — no fix the
    fixer could make means the finding was never mechanical — is restored the
    moment the fixer holds the main seat. Both halves of that bound are asked
    here rather than left to the step that describes them: an escalation
    follows a round this run actually routed, and it happens once (ADR-0110).
    """

    held = [record.request_id for record in routing.decisions]
    for record in records:
        wave = escalated_wave(record.request_id)
        if wave is None:
            continue

        if f"wave-fix-{wave}" not in held:
            return (
                f"{record.request_id} escalates a fix round this run never "
                f"routed: an escalation carries the wave-fix-{wave} round it "
                "follows as its verified failure"
            )
        if record.request_id in held:
            return (
                f"{record.request_id} stands in this run's frozen routing "
                "already: a changed-nothing fix round buys exactly one further "
                "decision, and a second changed-nothing round stops the run"
            )
        held.append(record.request_id)

    return None


def objective_refusal(snapshot: dict[str, Any], fast: bool) -> str | None:
    """Return why a snapshot's objective is not this invocation's, or None.

    `--fast` is a promise about how the night selects, and the selection is
    made inside the frozen snapshot rather than here. A context composed
    without the lock the invocation carries would leave the flag saying one
    thing and the routing doing another for the whole run, which is worse than
    refusing before the first claim.
    """

    wanted = "time_first" if fast else "cost_first"
    policy = snapshot.get("override_policy")
    frozen = policy.get("objective") if isinstance(policy, dict) else None
    if frozen == wanted:
        return None
    invoked = "--fast" if fast else "no --fast"
    return (
        f"this invocation was made with {invoked} and its frozen context "
        f"selects for {frozen!r}: compose the context request with objective "
        f"{wanted!r}, or invoke the run the other way"
    )


def cmd_route(
    cwd: Path,
    response: Path,
    state_path: Path | None,
    *,
    dry_run: bool,
    model: str | None,
    deliberation: str | None,
    fast: bool,
    starting: list[int] | None,
    run_claimed: list[int] | None,
) -> int:
    """Freeze one public model-selector route response for the rest of the run.

    Model-selector owns every selection rule behind the Interface and this verb
    reproduces none of them. What it owns is the run's side of the seam: that
    one context is frozen and reused, that the invocation's own locks travel
    with it, that a decision can be found again by the role it was made for,
    and that nothing a verdict runs on is ever decided here (ADR-0085).
    """

    try:
        answered = read_response(response)
    except RunError as exc:
        return fail(str(exc))

    # A whole-artifact refusal is not a decision about any one role, so it is
    # read before the decisions are and freezes nothing at all (ADR-0083).
    refusal = answered.get("artifact_refusal")
    if refusal is not None:
        emit_route(None, [], [{"request_id": None, **cast(dict[str, Any], refusal)}])
        return 2

    try:
        snapshot, records = routed_response(answered)
    except RunError as exc:
        return fail(str(exc))

    # Collect role refusals before both modes enter the shared route gates.
    refusals = [
        {"request_id": record.request_id, **record.decision["reason"]}
        for record in records
        if not record.acceptable
    ]

    # Rehydrate real state or bind a dry route to its in-memory plan frontier.
    state = remembered_state(state_path, cwd)
    if dry_run and starting is None:
        return fail(
            "dry routing validates the plan's starting frontier: pass "
            "--starting once for each ticket, in plan order"
        )
    if dry_run:
        state = RunState(
            branch=state.branch if state else current_branch(cwd),
            label=state.label if state else READY_LABEL,
            login=state.login if state else None,
            claimed=run_claimed or [],
            base=state.base if state else "",
            starting=starting or [],
            contracts=state.contracts if state else {},
            contract_bases=state.contract_bases if state else {},
        )
    elif starting is not None or run_claimed is not None:
        return fail(
            "--starting and --run-claimed carry a dry plan and are refused on "
            "a real route"
        )
    elif state is None:
        return fail(
            "routing is frozen against the run the plan wrote down, so there is "
            "nothing to freeze it against yet: plan before routing"
        )

    try:
        routing = read_routing(state_path)
    except RunError as exc:
        return fail(str(exc))

    # The first response of a run freezes its context and its locks; every one
    # after it is held to both, and to the frontier the plan named.
    if routing is None:
        if (standing := claims_refusal(state)) is not None:
            return fail(standing)
        if (opening := batch_refusal(state, records)) is not None:
            return fail(opening)
        if (mismatched := objective_refusal(snapshot, fast)) is not None:
            return fail(mismatched)
        routing = Routing(
            snapshot=snapshot,
            model=model,
            deliberation=deliberation,
            fast=fast,
            decisions=[],
            run_identity=secrets.token_hex(32),
        )
    elif (stale := frozen_refusal(routing, snapshot)) is not None:
        return fail(stale)
    elif (
        relocked := locks_refusal(routing, model, deliberation, fast, "this response")
    ) is not None:
        return fail(relocked)

    if (escalated := escalation_refusal(routing, records)) is not None:
        return fail(escalated)

    # Extend the candidate account in memory before the persistence seam.
    routing.decisions.extend(records)

    # Freeze only a real route; dry mode reports the same gated candidate.
    if not dry_run:
        try:
            write_routing(state_path, routing)
        except RunError as exc:
            return fail(str(exc))

    emit_route(routing.identity, records, refusals)
    return 2 if refusals else 0


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

    # Keep a failed caller expectation between the plan and the first tracker
    # mutation until a later flagged plan proves the authorized identity.
    if remembered and remembered.approval_met is False:
        return fail(
            "this run's caller-supplied approval has not matched a plan; run "
            "a flagged plan with the computed approval identity before claiming"
        )

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

    # Nothing this run takes was not routed first — the opening frontier's
    # tickets, a replacement considered after a collision, and a wave the last
    # one unblocked alike. It is asked after the tracker's own answer so that a
    # ticket somebody else already holds stays the ordinary refusal the wave
    # drops and replaces, and before the claim is written so that a ticket
    # nothing decided is never taken (ADR-0085).
    try:
        routing = read_routing(state_path)
    except RunError as exc:
        return fail(str(exc))
    unrouted = dispatch_refusal(routing, f"build-{number}", f"#{number} is claimed")
    if unrouted is not None:
        return fail(unrouted)

    # A declared ceiling-one walk needs the boundary from before its builder
    # starts. An existing claim without that durable boundary cannot invent it
    # from a branch the builder may already have changed.
    contract = remembered.contracts.get(number) if remembered else None
    if (
        holders
        and contract is not None
        and remembered is not None
        and number not in remembered.contract_bases
    ):
        return fail(
            f"#{number} declares commit roles but its saved claim head is absent; "
            "the contract boundary cannot be moved to the current HEAD"
        )

    # A ticket this run already holds is already claimed, and asking the
    # tracker to assign it again would write nothing it does not already say.
    if not holders:
        try:
            gh(cwd, "issue", "edit", str(number), "--add-assignee", CLAIM_ASSIGNEE)
        except RunError as exc:
            return fail(f"#{number} could not be claimed: {exc}")

    # Persist both the claim and its immutable contract anchor before a builder
    # can be dispatched, releasing a newly added tracker claim if that fails.
    if remembered is not None:
        remembered.claimed = sorted(set(remembered.claimed) | {number})
        if contract is not None:
            remembered.contract_bases.setdefault(
                number, git(cwd, "rev-parse", "HEAD").strip()
            )
        if write_state(state_path, remembered) is None:
            if not holders:
                try:
                    gh(
                        cwd,
                        "issue",
                        "edit",
                        str(number),
                        "--remove-assignee",
                        CLAIM_ASSIGNEE,
                    )
                except RunError:
                    pass
            return fail(f"#{number}'s claim could not be persisted")

    if remembered is None:
        remember_claim(state_path, cwd, number)
    emit({"verb": "claim", "ticket": number, "claimed": True, "reason": None})
    return 0


def cmd_park(cwd: Path, number: int, state_path: Path | None) -> int:
    """Return one ticket to the human loop, and release this run's claim on it.

    A ticket whose text leaves a decision open — a deferred value, a choice
    named as the maintainer's — carries a label triage got wrong, and under
    `--yes` there is nobody left to ask (ADR-0070). Only the deterministic
    half lives here: the label swap and the claim's release. The question
    itself is prose and judgment, written on the ticket by the orchestrator
    with the tracker's ordinary comment command.
    """

    try:
        ticket = ticket_view(cwd, number, "number,labels,assignees,comments")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")

    # A settled ticket is nobody's to park: what a run recorded on it is the
    # account the report reads, and the swap would take the ticket out of it.
    outcome, _, _ = recorded_against(ticket)
    if outcome is not None:
        emit(
            {
                "verb": "park",
                "ticket": number,
                "parked": False,
                "reason": (
                    f"#{number} already carries a recorded outcome ({outcome}), "
                    "and a settled ticket is nobody's to park"
                ),
            }
        )
        return 2

    # Whose a claim is only matters where somebody holds one, and only a claim
    # this run took is its own to release — a person's, or another session's,
    # stays with the ticket. The reading is the claim verb's in reverse: where
    # the run remembers nothing, a claim in its own name is the interrupted
    # run's it usually is.
    holders = holders_of(ticket)
    remembered = remembered_state(state_path, cwd)
    try:
        mine = my_login(cwd, remembered) if holders else None
    except RunError as exc:
        return fail(str(exc))
    releasing = holders == [mine] and (
        remembered is None or number in remembered.claimed
    )

    # One write carries the whole swap, so an interruption cannot leave the
    # ready label gone and the claim standing in two separate halves.
    swap = ["--remove-label", READY_LABEL, "--add-label", INFO_LABEL]
    if releasing:
        swap += ["--remove-assignee", CLAIM_ASSIGNEE]
    try:
        gh(cwd, "issue", "edit", str(number), *swap)
    except RunError as exc:
        return fail(f"#{number} could not be parked: {exc}")

    forget_claim(state_path, cwd, number)
    emit({"verb": "park", "ticket": number, "parked": True, "reason": None})
    return 0


def cmd_isolate(cwd: Path, number: int) -> int:
    """Give ticket *number* a working tree of its own, and say where it is."""

    try:
        return isolate(cwd, number)
    except RunError as exc:
        return fail(str(exc))


def isolate(cwd: Path, number: int) -> int:
    """Open the working tree ticket *number* is built in, or find the one open.

    Tickets built at once cannot share one working tree, and the developer's is
    not a place to build in: it is where they left it and it stays there. So
    each ticket gets one, on a branch of its own cut from where the run branch
    now stands — which is the code the earlier waves were integrated into.

    A working tree isolates the files a ticket edits and nothing else, so the
    same call hands out the rest of what the wave would otherwise share: a
    scratch directory of the ticket's own, and one record number in each of the
    repository's numbered registries (ADR-0071).
    """

    home = worktree_home(cwd)

    # Reading what a run has open and adding to it are one read-modify-write on
    # state git keeps for the whole repository, so they happen under the same
    # lock the reservations do. Git's own machinery is what forces it: both
    # listing the trees and adding one read every entry under `.git/worktrees`,
    # so an entry a sibling add has made and not yet filled in is read as a
    # corrupt repository rather than as a tree being made, and the ticket is
    # refused a tree it could have had. A wave whose isolations are started
    # together — which is how an orchestrator starts independent calls — enters
    # that stretch twice at once; here it takes turns and overlaps everywhere
    # else.
    with allocation_lock(home):
        run_branch = current_branch(cwd)
        open_now = open_worktrees(cwd, run_branch)
        branch = worktree_branch(run_branch, number)
        path = home / str(number)

        # A ticket picked up again is made nothing at all, the emit below
        # answering with the tree it was left in.
        if number not in open_now:
            # A branch with nothing checked out on it is work an earlier run
            # left behind and this one would silently build over, so it is
            # named instead.
            if git_ok(cwd, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"):
                return fail(
                    f"#{number} already has the branch '{branch}' and no working "
                    "tree holding it: look at what is on it, then delete it"
                )

            # A working tree standing at this ticket's path that is not this
            # run's is another branch's run, interrupted or failed and left to
            # be looked at. Building over it would take that branch's work for
            # this ticket's.
            if path.exists():
                return fail(
                    f"#{number} already has a working tree at {path} that belongs "
                    "to another run: look at what is in it, then remove it with "
                    "`git worktree remove`"
                )

            try:
                git(cwd, "worktree", "add", str(path), "-b", branch)
            except RunError as exc:
                raise RunError(
                    f"#{number} could not be given a working tree: {exc}"
                ) from exc

    # The invocation is the resume here as everywhere else (ADR-0052): a ticket
    # picked up again goes on in the working tree it was left in.
    if number in open_now:
        standing = Path(open_now[number])

        # Preserved work is the mandatory base of a resume, but work not yet
        # committed belongs to the parked builder and cannot be merged safely.
        if git_result(standing, "status", "--porcelain").stdout:
            return fail(
                f"#{number} has uncommitted work in its preserved working tree: "
                f"look at {standing} before resuming it"
            )

        # Bring resolved blockers and every other integrated predecessor into
        # the preserved ticket branch before another builder sees the tree.
        run_head = git(cwd, "rev-parse", run_branch).strip()
        ticket_head = git(standing, "rev-parse", "HEAD").strip()
        brought_forward = not git_ok(
            standing, "merge-base", "--is-ancestor", run_head, ticket_head
        )
        if brought_forward:
            message = bring_forward_message(number)
            merged = git_result(standing, "merge", "--no-ff", "-m", message, run_branch)
            if merged.returncode != 0:
                collisions = git_result(
                    standing, "diff", "--name-only", "--diff-filter=U"
                ).stdout.split()
                settled = settle_by_regenerating(
                    standing, number, collisions, commit_message=message
                )
                if settled is None:
                    against = tickets_touching(cwd, collisions, ticket_head)
                    git_result(standing, "merge", "--abort")
                    emit(
                        {
                            "verb": "isolate",
                            "ticket": number,
                            "worktree": str(standing),
                            "branch": current_branch(standing),
                            "brought_forward": False,
                            "collisions": collisions,
                            "collided_with": against,
                            "reason": (
                                f"#{number} collided while bringing the run branch "
                                "into its preserved working tree"
                            ),
                            **allocate(cwd, number),
                        }
                    )
                    return 2

        emit(
            {
                "verb": "isolate",
                "ticket": number,
                "worktree": str(standing),
                "branch": current_branch(standing),
                "brought_forward": brought_forward,
                "collisions": [],
                "collided_with": [],
                **allocate(cwd, number),
            }
        )
        return 0

    emit(
        {
            "verb": "isolate",
            "ticket": number,
            "worktree": str(path),
            "branch": branch,
            "brought_forward": False,
            "collisions": [],
            "collided_with": [],
            **allocate(cwd, number),
        }
    )
    return 0


def cmd_integrate(cwd: Path, number: int, state_path: Path | None) -> int:
    """Merge ticket *number*'s work into the run branch and tidy up after it."""

    try:
        return integrate(cwd, number, state_path)
    except RunError as exc:
        return fail(str(exc))


def commit_contract_refusal(
    cwd: Path,
    base: str,
    head: str,
    contract: list[dict[str, Any]],
) -> str | None:
    """Return why commits from *base* to *head* violate *contract*, if they do."""

    # Walk authored history in its append order; run-owned marked merges and
    # commits confined to the run's private directory are outside role passes.
    commits = git(
        cwd, "rev-list", "--reverse", "--first-parent", f"{base}..{head}"
    ).split()
    role_index = 0
    for commit in commits:
        message = git(cwd, "show", "-s", "--format=%B", commit)
        if any(marker.search(message) for marker in RUN_OWNED):
            continue
        paths = git(cwd, "diff", "--name-only", f"{commit}^1", commit).split()
        checked = [path for path in paths if not path.startswith(".kntnt-orchestrate/")]
        if not checked:
            continue

        role = contract[role_index % len(contract)]
        allowed = set(
            git(
                cwd,
                "diff",
                "--name-only",
                f"{commit}^1",
                commit,
                "--",
                *cast(list[str], role["patterns"]),
            ).split()
        )
        offending = sorted(set(checked).difference(allowed))
        if offending:
            return (
                f"commit {commit} is the {role['name']} role and touches "
                f"paths outside its declared surfaces: {', '.join(offending)}"
            )
        role_index += 1

    if role_index % len(contract):
        expected = contract[role_index % len(contract)]["name"]
        return f"the commit sequence ends before its next {expected} role"

    return None


def integrate(cwd: Path, number: int, state_path: Path | None = None) -> int:
    """Bring ticket *number*'s work onto the branch the developer comes back to.

    Called per verified ticket as its wave completes rather than at the end of
    the run, because a ticket in a later wave is blocked by one in an earlier
    wave: it builds on that code, and a working tree cut before the merge would
    not have it.

    A collision is an answer and not a breakage — the run branch is left as it
    was and the losing ticket's working tree stands, so the collision can be
    repaired from it.
    """

    branch = current_branch(cwd)
    open_now = open_worktrees(cwd, branch)

    # Nothing to merge is not a merge that failed: at a ceiling of one the
    # work is on the branch already, and asking here is asking for a run that
    # was never started this way.
    if number not in open_now:
        return fail(
            f"#{number} has no working tree to integrate: a ceiling of one "
            "commits straight to the branch and leaves nothing to merge"
        )

    # Work only the working tree holds would be swept away with it, so a
    # builder that stopped mid-ticket is named rather than quietly discarded.
    # Untracked files count: a file written and never added is the half of that
    # work the merge cannot carry and the removal would destroy outright. What
    # the repository ignores is not work and does not count.
    path = Path(open_now[number])
    if git_result(path, "status", "--porcelain").stdout:
        return fail(
            f"#{number} has work its working tree never committed, and merging "
            f"the branch would leave it behind: look at {path}"
        )

    # Refuse certified history that does not form complete declared passes
    # before the run branch is changed in any way.
    state = remembered_state(state_path, cwd)
    contract = state.contracts.get(number) if state else None
    if contract is not None:
        base = git(cwd, "merge-base", "HEAD", current_branch(path)).strip()
        if refusal := commit_contract_refusal(path, base, "HEAD", contract):
            return fail(f"#{number} cannot be integrated: {refusal}")

    # The merge itself, kept as its own commit so what a ticket delivered
    # stays legible on the branch afterwards, and marked so the branch can say
    # afterwards which ticket brought which file.
    built_on = current_branch(path)
    merged = git_result(cwd, "merge", "--no-ff", "-m", merge_message(number), built_on)

    # A collision the repository's own generators answer is not a collision two
    # builders have to settle: where every file it touched is declared
    # generated, the generator is run on the merged tree and what it produced
    # is committed, and no repair is dispatched (ADR-0106). Anything else, the
    # mixed case included, is refused exactly as it always was. The collision
    # is read first because settling one resolves it: what the refusal names
    # has to be what the merge left, not what an attempt at it left behind.
    regenerated: list[str] = []
    if merged.returncode != 0:
        collisions = git_result(cwd, "diff", "--name-only", "--diff-filter=U")
        files = collisions.stdout.split()
        settled = settle_by_regenerating(cwd, number, files)
        if settled is None:
            return refuse_merge(cwd, number, path, built_on, merged, files)
        regenerated = settled

    # The machine ends tidy: what is merged is on the branch the developer
    # comes back to, so the working tree it was built in and the branch it was
    # built on are both spent. A tree that will not go is left standing and
    # said so rather than reported gone.
    commit = git(cwd, "rev-parse", "HEAD").strip()
    removed = git_result(cwd, "worktree", "remove", "--force", str(path))
    if removed.returncode == 0:
        git_result(cwd, "branch", "--delete", built_on)
        discard_allocation(cwd, number)

    emit(
        {
            "verb": "integrate",
            "ticket": number,
            "merged": True,
            "commit": commit,
            "worktree": None if removed.returncode == 0 else str(path),
            "collisions": [],
            "regenerated": regenerated,
            "reason": None,
        }
    )
    return 0


def refuse_merge(
    cwd: Path,
    number: int,
    path: Path,
    built_on: str,
    merged: subprocess.CompletedProcess[str],
    files: list[str],
) -> int:
    """Undo a merge that did not go through, and say what stopped it.

    A collision is answered with both halves of it: the files the two tickets
    both touched, and the ticket on the other side of them. That pair names a
    blocking edge the ticket breakdown was missing, which is how one run
    improves the next one — and the files alone would leave the developer to
    work out whose work they had run into.

    *files* is what the merge left half-merged, read by the caller while the
    repository could still say it: an attempt at settling the collision stages
    what it settled, and a reading taken after one would name fewer files than
    the merge actually collided in.
    """

    # Whose work the collision ran into, before the merge that carries the
    # answer is undone.
    against = tickets_touching(cwd, files, built_on)
    git_result(cwd, "merge", "--abort")

    # Whose work it ran into, where the branch can say, and what stopped the
    # merge where it cannot — a merge that failed for some other reason than a
    # conflict leaves no unmerged file to name and has to speak for itself.
    whose = as_references(against)
    reason = (
        f"#{number} collided with {whose or 'work already on the branch'} in "
        + ", ".join(files)
        if files
        else (merged.stderr or merged.stdout).strip()
    )

    emit(
        {
            "verb": "integrate",
            "ticket": number,
            "merged": False,
            "commit": None,
            "worktree": str(path),
            "collisions": files,
            "regenerated": [],
            "collided_with": against,
            "reason": reason,
        }
    )
    return 2


def merge_message(number: int, regenerated: list[str] | None = None) -> str:
    """Render the message of the merge that brings ticket *number* over.

    One line a developer reading the branch can read, and a marker the engine
    reads back: which ticket a commit carried is the branch's own answer, and a
    branch that cannot give it can name no ticket on the other side of a
    collision.

    A merge that collided only in generated files says so in both halves. The
    branch is where that fact outlives the session that made it, which is what
    lets the run's own account name a regeneration as what it was rather than
    as a merge that went through untroubled (ADR-0106).
    """

    settled = (
        "\n\nThe collision in "
        + ", ".join(regenerated)
        + " was confined to files this repository declares generated, and was"
        + " settled by regenerating them on the merged tree."
        if regenerated
        else ""
    )
    marked = f" regenerated={','.join(regenerated)}" if regenerated else ""

    return (
        f"Merge #{number} into the run branch{settled}"
        f"\n\n<!-- {MARKER} merged={number}{marked} -->"
    )


def bring_forward_message(number: int) -> str:
    """Render the message of the merge that brings ticket *number* forward.

    A resumed ticket is handed back a tree standing where the run branch now
    does, and the merge that puts it there is the engine's, not the builder's.
    One line a developer reading the branch can read, and the same marker the
    engine reads back, because the alternative is deciding what a commit is
    from its subject line — which is how the merge came to be counted as a
    commit the ticket declared (ADR-0148).
    """

    return (
        f"Merge the run branch into #{number}"
        f"\n\n<!-- {MARKER} brought-forward={number} -->"
    )


@dataclass(frozen=True)
class Generator:
    """One declared generated output, and the command that produces it."""

    files: tuple[str, ...]
    command: str


def declared_generators(cwd: Path) -> list[Generator]:
    """Return what this repository declares generated, and what regenerates it.

    A declaration nobody can read declares nothing: an absent, unreadable, or
    malformed file leaves the list empty, and an entry that does not name both
    its files and its command is left out of it. Every one of those failures
    can only narrow what counts as generated, so the worst a broken
    declaration costs is the repair path a collision would have taken anyway.
    """

    try:
        declaration = json.loads(
            (cwd / GENERATED_DECLARATION).read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return []

    # The shape is checked rather than trusted: this file is prose somebody
    # wrote, and what it licenses is a command the run executes.
    entries = declaration.get("generated") if isinstance(declaration, dict) else None
    if not isinstance(entries, list):
        return []

    declared = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        files = entry.get("files")
        command = entry.get("command")
        if not isinstance(command, str) or not isinstance(files, list):
            continue
        if not files or not all(isinstance(name, str) for name in files):
            continue
        declared.append(Generator(files=tuple(files), command=command))

    return declared


def settle_by_regenerating(
    cwd: Path,
    number: int,
    collisions: list[str],
    *,
    commit_message: str | None = None,
) -> list[str] | None:
    """Settle a collision confined to declared-generated files, or answer None.

    A generated file is the output of a deterministic command, so two builders
    who each ran it honestly cannot produce the same bytes and will collide in
    it forever. There is no disagreement in such a collision for anybody to
    settle: the merged tree already determines what the file says, and running
    the generator there is what says it (ADR-0106).

    None is every other case — a collision reaching past what the repository
    declares, a repository that declares nothing, a generator that failed, one
    whose output did not settle what the merge could not, and one that wrote
    outside what it declares. The merge itself is left standing in each of
    them, for the caller to refuse and undo as it always did.
    """

    # Confinement is the whole of the question: every file the merge could not
    # settle has to be one the repository declares generated.
    touched = set(collisions)
    generators = declared_generators(cwd)
    declared = {name for generator in generators for name in generator.files}
    if not touched or not touched <= declared:
        return None

    # Only the generators the collision actually reaches are run, and each is
    # run in the merged tree rather than in either side of it.
    running = [
        generator for generator in generators if touched.intersection(generator.files)
    ]
    for generator in running:
        if not run_generator(cwd, generator):
            return None

    # What a generator that ran declares it wrote is staged whole: an output
    # the collision did not touch is still this generator's own, and staging
    # only the conflicted half would leave the tree disagreeing with itself.
    produced = sorted({name for generator in running for name in generator.files})
    staged = git_result(cwd, "add", "--", *produced)
    if staged.returncode != 0:
        return None

    # A file the generators did not rewrite is one regeneration did not settle,
    # whatever the declaration said, so the collision stands as a collision.
    if git_result(cwd, "diff", "--name-only", "--diff-filter=U").stdout.split():
        return None

    # A generator that touched anything its declaration does not name has
    # widened that declaration without saying so, and what it wrote there is
    # nobody's decision to commit. The tree the run commits is the one the
    # declaration accounts for, or the collision stands.
    outside = git_result(cwd, "diff", "--name-only").stdout.split()
    outside += git_result(
        cwd, "ls-files", "--others", "--exclude-standard"
    ).stdout.split()
    if outside:
        return None

    committed = git_result(
        cwd, "commit", "-m", commit_message or merge_message(number, produced)
    )
    if committed.returncode != 0:
        return None

    return produced


def run_generator(cwd: Path, generator: Generator) -> bool:
    """Run one declared generator in *cwd*, and say whether it succeeded.

    The command is run through a shell because that is how the repository's own
    guide writes it — an environment assignment in front of it, a pipe or a
    redirection in it — and a declaration a contributor cannot copy from the
    guide it lives beside is one that will drift from it. A command named there
    is trusted exactly as far as the code the merge is already bringing onto
    this branch, the declaration being a file of the same repository.
    """

    ran = subprocess.run(
        generator.command,
        cwd=cwd,
        shell=True,
        text=True,
        capture_output=True,
        check=False,
    )

    return ran.returncode == 0


def regenerated_merges(cwd: Path, accounted: set[int]) -> list[dict[str, Any]]:
    """Return the merges this branch settled by regenerating, ticket by ticket.

    Read off the branch's own merge markers for the reason a collision's
    counterpart is (ADR-0055): what a run did is a fact about the branch it did
    it on, and a report that remembered it instead would have nothing to say
    about a run some other session finished. Only the tickets *accounted* names
    are here — a branch worked more than once carries the merges of every run
    it carried, and a regeneration outside this report's scope belongs to
    somebody else's account of it.
    """

    return [
        {"ticket": number, "files": regenerated.split(",")}
        for number, regenerated, _ in merges_on_branch(cwd)
        if regenerated and number in accounted
    ]


def merges_on_branch(cwd: Path) -> list[tuple[int, str, str]]:
    """Return what each of this branch's own merges carried, newest first.

    Each entry is the ticket the merge brought, the generated files a
    regeneration settled its collision in as the marker spells them, and the
    commit itself. Only the merges a run made are here — the marker is what
    says so — and only along the first parent, that being the run branch's own
    history rather than everything the tickets brought with them.
    """

    record = git(cwd, "log", "--first-parent", "--format=%H%x1f%B%x1e")
    found = []
    for entry in record.split("\x1e"):
        commit, _, message = entry.strip().partition("\x1f")
        carried = MERGED_TICKET.search(message)
        if carried:
            found.append((int(carried.group(1)), carried.group(2) or "", commit))

    return found


def tickets_touching(cwd: Path, files: list[str], built_on: str) -> list[int]:
    """Return the tickets whose merged work *built_on* collided with in *files*.

    A merge is asked what it brought rather than what the branch looked like
    around it: the diff against its first parent is the ticket's own
    contribution, and everything else on the branch is somebody else's. No
    file is no question, and asking it would walk the branch to answer nothing.

    A merge the losing branch already contains is not one it can have collided
    with — the branch was cut after it, so that work is on both sides and the
    merge has it as common ground. Naming it anyway would report a blocking
    edge that is not missing, which is the one thing this pair is read for.
    """

    if not files:
        return []

    touched = set(files)
    return sorted(
        number
        for number, _, commit in merges_on_branch(cwd)
        if not git_ok(cwd, "merge-base", "--is-ancestor", commit, built_on)
        and touched.intersection(
            git(cwd, "diff", "--name-only", f"{commit}^1", commit).split()
        )
    )


def discard_tree(cwd: Path, number: int, path: Path) -> None:
    """Discard ticket *number*'s working tree at *path*, its branch, and what
    isolate gave it, uncommitted work and all.

    The one gesture in the run that destroys work on purpose, and what it
    destroys is always a first try nothing will ever integrate: a resolution a
    verifier has just refused, or a build toward a requirement that, by the
    builder's own finding, could not yet be met (ADR-0073).
    """

    built_on = current_branch(path)
    git(cwd, "worktree", "remove", "--force", str(path))
    git(cwd, "branch", "--delete", "--force", built_on)
    discard_allocation(cwd, number)


def cmd_rebuild(cwd: Path, number: int) -> int:
    """Discard what ticket *number* was built in, so it can be built again."""

    try:
        return rebuild(cwd, number)
    except RunError as exc:
        return fail(str(exc))


def rebuild(cwd: Path, number: int) -> int:
    """Spend ticket *number*'s one rebuild, and leave nothing of the first try.

    A collision whose repair does not verify is not repaired, and a resolution
    nobody can verify is not a resolution — so the losing ticket is built again
    from nothing, on top of the very code it collided with, which is where it
    cannot collide again. What it was built in the first time goes with it: a
    working tree holding a resolution that failed is a place a second builder
    would read as work already done (ADR-0055).

    The run branch is not touched. Nothing of this ticket ever reached it — the
    repair is settled on the ticket's own branch, and a merge that collided was
    undone where it collided.
    """

    # Which trees are this run's is a question about the branch it is on, the
    # branch being what says which run made a tree.
    open_now = open_worktrees(cwd, current_branch(cwd))

    # A ceiling of one merges nothing, so nothing of this kind can have gone
    # wrong there and there is no second place to build.
    if number not in open_now:
        return fail(
            f"#{number} has no working tree to discard: a ceiling of one "
            "merges nothing and so collides with nothing"
        )

    # The tracker is asked before anything is destroyed, so a ticket that has
    # already spent its rebuild keeps the working tree it stands in.
    try:
        ticket = ticket_view(cwd, number, "number,comments")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")
    if rebuilt_already(ticket):
        emit(
            {
                "verb": "rebuild",
                "ticket": number,
                "rebuilt": False,
                "worktree": open_now[number],
                "reason": (
                    f"#{number} has already been rebuilt once in this run, and "
                    "a rebuild is the one rerun a collision buys"
                ),
            }
        )
        return 2

    # The note goes on the ticket before the working tree goes, because the
    # note is the bound: a run interrupted between the two would otherwise come
    # back with its one rebuild unspent and spend it again.
    try:
        gh(cwd, "issue", "comment", str(number), "--body", rebuild_note())
    except RunError as exc:
        return fail(f"#{number} could not be recorded as rebuilt: {exc}")

    # What the first try left is discarded outright, uncommitted work and all:
    # what it holds is a resolution a verifier has just refused.
    discard_tree(cwd, number, Path(open_now[number]))

    emit(
        {
            "verb": "rebuild",
            "ticket": number,
            "rebuilt": True,
            "worktree": None,
            "reason": None,
        }
    )
    return 0


def rebuild_note() -> str:
    """Render what is written on a ticket that is being built a second time."""

    return f"<!-- {MARKER} rebuild --> {REBUILD_NOTE}"


def cmd_amend(
    cwd: Path,
    number: int,
    attempt: int,
    phase: str,
    verdict_file: str | None,
    state_path: Path | None,
) -> int:
    """Record one append-only *phase* of amend *attempt* on ticket *number*.

    A failed verification buys a first amend, and its fresh verdict may buy one
    continuation amend because it carries new information. Naming the attempt
    and phase makes replay after an uncertain tracker write idempotent. Verdicts
    persisted at builder and failed-verifier boundaries make the tracker alone
    sufficient to resume. Nothing here touches the work.
    """

    # The tracker is where the bound lives, for the reason every outcome lives
    # there: a run interrupted mid-amend must find it where it left it.
    try:
        ticket = ticket_view(cwd, number, "number,comments")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")
    current = recorded_amend_state(ticket)
    spent = current.attempt if current else 0
    if attempt > AMEND_LIMIT:
        emit(
            {
                "verb": "amend",
                "ticket": number,
                "amended": False,
                "attempt": attempt,
                "phase": phase,
                "amends_spent": spent,
                "newly_recorded": False,
                "reason": (
                    f"#{number} has no amend {attempt}: the verification-repair "
                    f"path is bounded to {AMEND_LIMIT} verifier-informed amends"
                ),
            }
        )
        return 2

    # Amending is building, so the amender is routed like every other execution
    # role — and for its own attempt, the escalation the second one may carry
    # being no part of what the first was decided on.
    if phase == AMEND_BUILDING:
        try:
            routing = read_routing(state_path)
        except RunError as exc:
            return fail(str(exc))
        refused = dispatch_refusal(
            routing,
            f"amend-{number}-{attempt}",
            f"#{number} amend {attempt} is about to build",
        )
        if refused is not None:
            return fail(refused)

    # Read verdicts only for phases whose recovery depends on their exact text.
    needs_verdict = phase in (AMEND_BUILDING, AMEND_FAILED)
    if needs_verdict and verdict_file is None:
        return fail(f"amend {attempt} phase {phase} requires --verdict-file")
    if not needs_verdict and verdict_file is not None:
        return fail(f"amend {attempt} phase {phase} does not accept --verdict-file")
    verdict: str | None = None
    if verdict_file is not None:
        try:
            verdict = Path(verdict_file).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return fail(
                f"the verifier verdict cannot be read from {verdict_file}: {exc}"
            )
        if not verdict.strip():
            return fail(f"the verifier verdict in {verdict_file} is empty")

    # A repeated phase transition resumes the work its existing marker fronts.
    if current and (attempt, phase) == (current.attempt, current.phase):
        if verdict != current.verdict:
            return fail(
                f"amend {attempt} phase {phase} is already recorded with a "
                "different verifier verdict"
            )
        emit(
            {
                "verb": "amend",
                "ticket": number,
                "amended": True,
                "attempt": attempt,
                "phase": phase,
                "amends_spent": spent,
                "newly_recorded": False,
                "reason": None,
            }
        )
        return 0

    # Only the next state-machine edge may be appended to the tracker.
    current_key = None if current is None else (current.attempt, current.phase)
    if (attempt, phase) not in AMEND_TRANSITIONS.get(current_key, ()):
        described = (
            "no amend"
            if current is None
            else f"amend {current.attempt} phase {current.phase}"
        )
        return fail(
            f"#{number} is at {described}, so amend {attempt} phase {phase} "
            "is not its next phase"
        )

    # Attempt two must carry the immediately preceding failed verdict verbatim.
    if (
        attempt == 2
        and phase == AMEND_BUILDING
        and current is not None
        and current.phase == AMEND_FAILED
        and verdict != current.verdict
    ):
        return fail(
            "amend 2 must carry amend 1's immediately preceding verifier "
            "verdict verbatim"
        )

    # Append the transition before dispatch or terminal action consumes it.
    try:
        gh(
            cwd,
            "issue",
            "comment",
            str(number),
            "--body",
            amend_note(attempt, phase, verdict),
        )
    except RunError as exc:
        return fail(
            f"#{number} amend {attempt} phase {phase} could not be recorded: {exc}"
        )

    emit(
        {
            "verb": "amend",
            "ticket": number,
            "amended": True,
            "attempt": attempt,
            "phase": phase,
            "amends_spent": max(spent, attempt),
            "newly_recorded": True,
            "reason": None,
        }
    )
    return 0


def amend_note(attempt: int, phase: str, verdict: str | None) -> str:
    """Render one tracker event for amend *attempt* at *phase*."""

    # Render the human half from the same phase carried by the marker.
    notes = {
        AMEND_BUILDING: (
            "Recorded by an unattended run: verification did not pass, and "
            f"amend {attempt} of {AMEND_LIMIT} is being spent before its fresh "
            "builder starts."
        ),
        AMEND_VERIFYING: (
            f"Recorded by an unattended run: amend {attempt} of {AMEND_LIMIT} "
            "finished building, and its fresh independent verifier is starting."
        ),
        AMEND_PASSED: (
            f"Recorded by an unattended run: amend {attempt} of {AMEND_LIMIT} "
            "passed its fresh independent verification."
        ),
        AMEND_FAILED: (
            f"Recorded by an unattended run: amend {attempt} of {AMEND_LIMIT} "
            "failed its fresh independent verification."
        ),
    }
    note = notes[phase]
    retained = f"{AMEND_VERDICT_HEADING}{verdict}" if verdict is not None else ""
    return f"<!-- {MARKER} amend={attempt} phase={phase} --> {note}{retained}"


def outcome_note(
    outcome: str,
    commit: str | None,
    against: list[int],
    contract_base: str | None = None,
) -> str:
    """Render what is written on a ticket when its outcome is recorded.

    One line, carrying a marker a later run can read the outcome back out of
    and prose the developer reading the ticket can read instead. Both halves
    name the ticket a collision was with, that being the pair the developer
    fixes the ticket breakdown from.
    """

    named = f" commit={commit}" if commit else ""
    marked = (
        " collided-with=" + ",".join(str(ticket) for ticket in against)
        if against
        else ""
    )
    anchored = f" contract-base={contract_base}" if contract_base else ""
    said = f" It collided with {as_references(against)}." if against else ""

    return f"<!-- {MARKER} outcome={outcome}{named}{marked}{anchored} --> {NOTES[outcome]}{said}"


def blocked_note(waiting_on: list[int]) -> str:
    """Render what is written on a ticket recorded blocked on open work.

    The note is the engine talking to the developer and its next self, so its
    marker keeps it out of every brief's thread — and nothing reads it back,
    the corrected edge on the tracker being the whole of the memory the
    mechanism needs (ADR-0073).
    """

    marked = ",".join(str(ticket) for ticket in waiting_on)
    return (
        f"<!-- {MARKER} blocked-by={marked} --> {NOTES[BLOCKED]} "
        f"It waits on {as_references(waiting_on)}."
    )


def write_edges(cwd: Path, number: int, waiting_on: list[int]) -> None:
    """Write the blocking edges ticket *number* waits on to the tracker.

    Written the way the ticket breakdown would have written them: the
    tracker's native blocked-by relation wherever it takes the write — the
    same relation every plan reads edges back off — and the `Blocked by` body
    line where it does not, which is the same fallback the plan reads, in the
    same order (ADR-0073).
    """

    # The native relation is keyed by the blocker's database id rather than
    # its number, so each edge costs the tracker one question and one write.
    unwritten = []
    for blocker in waiting_on:
        try:
            identity = gh(
                cwd,
                "api",
                f"repos/{{owner}}/{{repo}}/issues/{blocker}",
                "--jq",
                ".id",
            ).strip()
            if not identity.isdigit():
                raise RunError(f"the tracker answered no id for #{blocker}")
            gh(
                cwd,
                "api",
                "--method",
                "POST",
                f"repos/{{owner}}/{{repo}}/issues/{number}/dependencies/blocked_by",
                "-F",
                f"issue_id={identity}",
            )
        except RunError:
            unwritten.append(blocker)

    # A tracker that would not take the relation still gets the edge, as the
    # body line the breakdown writes where the relation is missing — appended
    # under the body as filed, and read back by exactly the pattern the
    # breakdown's own line is read by.
    if unwritten:
        body = str(ticket_view(cwd, number, "number,body")["body"])
        line = f"Blocked by: {as_references(unwritten)}"
        amended = f"{body.rstrip()}\n\n{line}\n" if body.strip() else f"{line}\n"
        gh(cwd, "issue", "edit", str(number), "--body", amended)


def release_claim(
    cwd: Path, number: int, ticket: dict[str, Any], state_path: Path | None
) -> None:
    """Release this run's claim on ticket *number*, where the claim is its own.

    The reading is the park verb's in reverse: only a claim this run took is
    its own to release, and a person's, or another session's, stays with the
    ticket. An unclaimed ticket costs the tracker nothing.
    """

    holders = holders_of(ticket)
    if not holders:
        return

    remembered = remembered_state(state_path, cwd)
    mine = my_login(cwd, remembered)
    if holders == [mine] and (remembered is None or number in remembered.claimed):
        gh(cwd, "issue", "edit", str(number), "--remove-assignee", CLAIM_ASSIGNEE)


def complete_lifecycle(cwd: Path, number: int, ticket: dict[str, Any]) -> None:
    """Replace active workflow state with completed historical state.

    Completion has no active lifecycle owner, so every remaining assignee is
    a stale claim and is removed by its recorded login rather than by whoever
    happens to perform the cleanup.
    """

    # Ensure the discovery label exists before any ticket carries completed
    # state that Report would otherwise be unable to find.
    labels_output = gh(
        cwd,
        "label",
        "list",
        "--json",
        "name",
        "--limit",
        str(REPOSITORY_LABEL_PAGE),
    )
    try:
        repository_labels = {str(label["name"]) for label in json.loads(labels_output)}
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise RunError(f"the tracker returned no readable label list: {exc}") from exc
    if HISTORICAL_LABEL not in repository_labels:
        gh(
            cwd,
            "label",
            "create",
            HISTORICAL_LABEL,
            "--color",
            HISTORICAL_LABEL_COLOR,
            "--description",
            "Completed ticket retained for Orchestrate history",
        )

    # Replace readiness and ownership with the neutral discovery marker in one
    # ticket edit, before an append-only completion fact makes the state final.
    labels = [str(label["name"]) for label in ticket.get("labels", [])]
    changes: list[str] = []
    if READY_LABEL in labels:
        changes.extend(("--remove-label", READY_LABEL))
    if INFO_LABEL in labels:
        changes.extend(("--remove-label", INFO_LABEL))
    if HISTORICAL_LABEL not in labels:
        changes.extend(("--add-label", HISTORICAL_LABEL))
    for holder in holders_of(ticket):
        changes.extend(("--remove-assignee", holder))
    if changes:
        gh(cwd, "issue", "edit", str(number), *changes)


def has_completed_lifecycle(ticket: dict[str, Any]) -> bool:
    """Say whether *ticket* carries the completed lifecycle projection."""

    labels = {str(label["name"]) for label in ticket.get("labels", [])}
    return (
        HISTORICAL_LABEL in labels
        and READY_LABEL not in labels
        and INFO_LABEL not in labels
        and not holders_of(ticket)
    )


def completion_candidates(cwd: Path, number: int) -> list[str]:
    """Return default-branch commits carrying an exact closing reference."""

    # Decline discovery without identifiable authoritative history.
    default = default_branch_reference(cwd)
    if default is None:
        return []

    # Read commit messages once and retain every exact closing-reference match.
    history = git(cwd, "log", default, "--format=%H%x1f%B%x1e")
    candidates: list[str] = []
    for entry in history.strip("\x1e\n").split("\x1e"):
        commit, _, message = entry.lstrip("\n").partition("\x1f")
        if number in [int(found) for found in CLOSING_REFERENCE.findall(message)]:
            candidates.append(commit)

    return candidates


def landed_completion_commit(cwd: Path, reference: str) -> str:
    """Resolve *reference* to a commit reachable from the default branch."""

    # Reject a reference that cannot name completion work in this repository.
    try:
        commit = git(cwd, "rev-parse", "--verify", f"{reference}^{{commit}}").strip()
    except RunError as exc:
        raise RunError(f"this repository has no commit {reference}") from exc

    # Require the repository's authoritative history to carry the completion.
    default = default_branch_reference(cwd)
    if default is None or not git_ok(
        cwd, "merge-base", "--is-ancestor", commit, default
    ):
        raise RunError(
            f"commit {reference} is not reachable from the repository's default branch"
        )

    return commit


def cmd_record(
    cwd: Path,
    number: int,
    outcome: str,
    named: str | None,
    against: list[int] | None,
    waiting_on: list[int] | None,
    state_path: Path | None,
) -> int:
    """Store ticket *number*'s *outcome* and the commit that carries it.

    The tracker is the store, because it is the one place an outcome outlives
    the session that produced it and the one place the developer will look. A
    blocked outcome settles nothing there: it writes the blocking edge the
    graph was missing and steps back, the ticket staying open to be offered
    again when the work it waits on exists (ADR-0073).
    """

    # Both halves of a done outcome are settled before the tracker is touched:
    # a ticket closed on a commit nothing can resolve is a report nobody can
    # check, which is the one thing an unattended run may not produce.
    if outcome == DONE and not named:
        return fail(f"recording #{number} done needs the commit that carries it")

    # Only a collision has a ticket on the other side of it, so naming one
    # against any other outcome would write down something that did not happen.
    collided = against or []
    if collided and outcome != CONFLICTED:
        return fail(
            f"#{number} is being recorded {outcome}, and only a conflicted "
            "outcome names the ticket it collided with"
        )

    # A blocked outcome is an edge and nothing else: it names the open work it
    # waits on and never a commit, its half-built tree being discarded rather
    # than carried by one — and a ticket waiting on itself is a graph nobody
    # could ever work.
    waiting = sorted(set(waiting_on or []))
    if waiting and outcome != BLOCKED:
        return fail(
            f"#{number} is being recorded {outcome}, and only a blocked "
            "outcome names the ticket it waits on"
        )
    if outcome == BLOCKED and not waiting:
        return fail(f"recording #{number} blocked needs the ticket it waits on")
    if outcome == BLOCKED and named:
        return fail(
            f"#{number} is being recorded blocked, and a blocked ticket has "
            "no commit to name: its half-built work is discarded"
        )
    if number in waiting:
        return fail(f"#{number} cannot be blocked by itself")

    # A done outcome names the commit that carries the work, so a tree still
    # holding work nothing committed is a tree where that cannot be true.
    # Above a ceiling of one `integrate` asks this of the ticket's own working
    # tree; at exactly one there is no such tree and this is the only gate.
    try:
        standing = uncommitted_refusal(cwd) if outcome == DONE else None
    except RunError as exc:
        return fail(str(exc))
    if standing is not None:
        return fail(f"#{number} cannot be recorded done: {standing}")

    commit = None
    if named:
        try:
            commit = git(cwd, "rev-parse", "--verify", f"{named}^{{commit}}").strip()
        except RunError:
            return fail(f"this repository has no commit {named}")

    # At a ceiling of one this is the integration gate: measure only the
    # declared ticket's history from the head saved when it was first claimed.
    remembered = remembered_state(state_path, cwd)
    contract = remembered.contracts.get(number) if remembered else None
    contract_base = remembered.contract_bases.get(number) if remembered else None
    if outcome == DONE and contract is not None:
        if contract_base is None:
            return fail(f"#{number} declares commit roles but has no saved claim head")
        if refusal := commit_contract_refusal(
            cwd, contract_base, cast(str, commit), contract
        ):
            return fail(f"#{number} cannot be recorded done: {refusal}")

    # The tracker is asked for the ticket before anything is written to it, so
    # a number it cannot answer for is refused rather than half-recorded. The
    # assignees come along because a blocked outcome releases this run's claim.
    try:
        ticket = ticket_view(cwd, number, "number,state,labels,assignees")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")

    # A blocked outcome names work still to exist. Closure alone does not
    # establish that work: only a done Ticket Resolution makes the edge over.
    for blocker in waiting:
        # Read the blocker's tracker state before projecting its resolution.
        try:
            state = str(ticket_view(cwd, blocker, "number,state")["state"])
        except (RunError, KeyError) as exc:
            return fail(f"the tracker cannot answer for blocker #{blocker}: {exc}")

        # Combine tracker closure with its recorded completion facts.
        try:
            blocks = blocker_still_blocks(cwd, blocker, state)
        except RunError as exc:
            return fail(str(exc))

        # Reject an edge whose prerequisite work is already established.
        if not blocks:
            return fail(
                f"#{number} cannot be blocked by #{blocker}: its done Ticket "
                "Resolution establishes that the required work exists"
            )

    # A blocked outcome is the corrected edge before it is anything else: the
    # dependency goes on the tracker the way the breakdown would have written
    # it, and the claim is released, a ticket waiting on open work being
    # nobody's to hold (ADR-0073).
    if outcome == BLOCKED:
        try:
            write_edges(cwd, number, waiting)
            release_claim(cwd, number, ticket, state_path)
        except RunError as exc:
            return fail(f"#{number} could not be recorded blocked: {exc}")

    # Done is the only outcome that closes a ticket, and the Skill records it
    # only where a separate subagent has verified the work — so there is no
    # path from a builder's own report to a closed ticket.
    note = (
        blocked_note(waiting)
        if outcome == BLOCKED
        else outcome_note(
            outcome, commit, collided, contract_base if outcome == DONE else None
        )
    )
    try:
        if outcome == DONE:
            complete_lifecycle(cwd, number, ticket)
            gh(cwd, "issue", "close", str(number), "--comment", note)
        else:
            gh(cwd, "issue", "comment", str(number), "--body", note)
    except RunError as exc:
        return fail(f"#{number} could not be recorded: {exc}")

    # What a blocked build made goes with the outcome, discarded exactly as a
    # refused repair is and without spending the ticket's one rebuild: when
    # the blocker resolves done, the ticket is isolated afresh from the branch
    # that by then carries the blocker's work, and built whole on top of it.
    if outcome == BLOCKED:
        try:
            open_now = open_worktrees(cwd, current_branch(cwd))
            if number in open_now:
                discard_tree(cwd, number, Path(open_now[number]))
        except RunError as exc:
            return fail(f"#{number}'s working tree could not be discarded: {exc}")

    forget_claim(state_path, cwd, number)

    emit(
        {
            "verb": "record",
            "ticket": number,
            "outcome": outcome,
            "commit": commit,
            "collided_with": collided,
            "blocked_by": waiting,
            "closed": outcome == DONE,
        }
    )
    return 0


def emit_reconciliation_result(
    number: int,
    run_outcome: str | None,
    commit: str,
    *,
    is_agreed: bool,
    is_lifecycle_repaired: bool,
) -> None:
    """Emit the stable public result of a Reconciliation request."""

    emit(
        {
            "verb": "reconcile",
            "ticket": number,
            "run_outcome": run_outcome,
            "resolution": DONE,
            "commit": commit,
            "already_agreed": is_agreed,
            "lifecycle_repaired": is_lifecycle_repaired,
        }
    )


def cmd_reconcile(cwd: Path, number: int, reference: str | None) -> int:
    """Resolve closed unsuccessful or parked work completed outside Orchestrate."""

    # Read every eligibility and lifecycle fact before allowing a tracker write.
    try:
        ticket = ticket_view(cwd, number, "number,state,labels,assignees,comments")
    except RunError as exc:
        return fail(f"the tracker cannot answer for #{number}: {exc}")

    # Require closure and reject only outcomes outside the eligible histories.
    if str(ticket["state"]).upper() != CLOSED:
        return fail(f"#{number} is open; Reconciliation never closes a ticket")
    outcome, _, _ = recorded_against(ticket)
    if outcome not in (None, FAILED, CONFLICTED):
        return fail(
            f"#{number} has a {outcome} Run Outcome; Reconciliation requires a "
            "failed or conflicted Run Outcome, or no Run Outcome after parking"
        )

    # Validate an existing event before deciding between agreement and recovery.
    existing_commit = reconciled_at(ticket)
    if existing_commit:
        # Hold historical provenance to the new event's default-branch gate.
        try:
            existing_commit = landed_completion_commit(cwd, existing_commit)
        except RunError as exc:
            return fail(f"#{number}'s existing Reconciliation is invalid: {exc}")

        # Refuse a caller's contradictory completion provenance.
        if reference:
            try:
                requested = landed_completion_commit(cwd, reference)
            except RunError as exc:
                return fail(str(exc))
            if requested != existing_commit:
                return fail(
                    f"#{number} is already reconciled at {existing_commit}, not {requested}"
                )

        # Recover an interrupted projection without calling mutation agreement.
        lifecycle_repaired = not has_completed_lifecycle(ticket)
        if lifecycle_repaired:
            try:
                complete_lifecycle(cwd, number, ticket)
            except RunError as exc:
                return fail(
                    f"#{number}'s reconciled lifecycle could not be repaired: {exc}"
                )

        # Distinguish a complete no-op from lifecycle recovery in the result.
        emit_reconciliation_result(
            number,
            outcome,
            existing_commit,
            is_agreed=not lifecycle_repaired,
            is_lifecycle_repaired=lifecycle_repaired,
        )
        return 0

    # Discover provenance only from one safe closing commit.
    if not reference:
        candidates = completion_candidates(cwd, number)
        if len(candidates) != 1:
            quantity = "no" if not candidates else "more than one"
            return fail(
                f"#{number} has {quantity} completion commit on the default branch; "
                "pass --commit after the maintainer identifies the one that completed it"
            )
        reference = candidates[0]

    # Resolve explicit and discovered provenance through one reachability gate.
    try:
        commit = landed_completion_commit(cwd, reference)
    except RunError as exc:
        return fail(str(exc))

    # Project completed lifecycle before appending the immutable Reconciliation.
    note = (
        f"<!-- {MARKER} reconciliation=done commit={commit} --> "
        "Reconciled by a maintainer: the ticket's requested work was completed "
        "outside Orchestrate and is carried by this commit."
    )
    try:
        complete_lifecycle(cwd, number, ticket)
        gh(cwd, "issue", "comment", str(number), "--body", note)
    except RunError as exc:
        return fail(f"#{number} could not be reconciled: {exc}")

    # Report the newly recorded current resolution and its preserved provenance.
    emit_reconciliation_result(
        number,
        outcome,
        commit,
        is_agreed=False,
        is_lifecycle_repaired=False,
    )
    return 0


def observation_library_candidates(script: Path | None = None) -> tuple[Path, ...]:
    """Return every supported location of the shared observation Library."""

    here = (script or Path(__file__)).resolve().parent
    return (
        here.parent.parent.parent / "kntnt/library/scripts/routed_observations.py",
        here.parent.parent / "kntnt/library/scripts/routed_observations.py",
        here.parent / "library/scripts/routed_observations.py",
    )


def routed_observations() -> Any:
    """Load the shared observation Library without reaching into another Skill."""

    # Resolve repository, installed-sibling, and Skill-local layouts in order.
    for candidate in observation_library_candidates():
        if not candidate.exists():
            continue
        spec = importlib.util.spec_from_file_location(
            "kntnt_routed_observations", candidate
        )
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    raise RunError(
        "routed observation mechanics are missing; install or update the Manager"
    )


def observed_task(record: RouteRecord, request_id: str) -> str:
    """Return the opaque identity of the work one routed attempt was an attempt at.

    A number and a wave count, and nothing of what either is about: an
    observation is statistical metadata, so the title, the body, and the branch
    of a ticket have no reason to be in one.
    """

    if record.ticket is not None:
        return f"ticket-{record.ticket}"
    named = ROUTE_REQUEST.match(request_id)
    return f"wave-{cast(re.Match[str], named)['wave']}"


def observed_attempt(
    routing: Routing,
    record: RouteRecord,
    request_id: str,
    outcome: str,
    started_at: str | None,
    measurements: dict[str, Any],
    commit: str | None,
    resolved_model: str | None,
) -> dict[str, Any]:
    """Build the completed routed attempt one external verdict established.

    Everything here is either the frozen decision itself, an identity of the
    thing the attempt was at, or a fact the verdict and the environment gave.
    The exact point, the mappings, the evidence class, and the provenance ride
    along inside the decision, because model-selector owns what they mean.
    """

    # Name the workload, the attempt at it, and who established its outcome.
    task = observed_task(record, request_id)
    stratum = OBSERVED_STRATA[record.role]
    result, condition, authority = OBSERVED_OUTCOMES[outcome]
    kin = [
        held.request_id
        for held in routing.decisions
        if observed_task(held, held.request_id) == task
    ]
    position = kin.index(request_id)

    # Say which point actually served, where the environment named another.
    decision = record.decision
    launch = cast(dict[str, Any], decision.get("launch") or {})
    inherited = cast(dict[str, Any], decision.get("inheritance") or {})
    routed_model = launch.get("model") or cast(
        dict[str, Any], inherited.get("main_seat") or {}
    ).get("model")
    served = resolved_model or routed_model

    return {
        "attempt_id": request_id,
        "prior_attempt_id": kin[position - 1] if position else None,
        "session_identity": "session-"
        + hashlib.sha256(f"{routing.identity}|{ROUTING_FILE}".encode()).hexdigest()[
            :16
        ],
        "run_identity": routing.run_identity or None,
        "task_identity": task,
        "workload_stratum": stratum,
        "stage": record.stage,
        "workload_cohort": record.workload_cohort,
        "workload_tags": list(record.workload_tags),
        "attempt_index": position + 1,
        "harness": routing.snapshot["harness"],
        "benchmark": {
            "key": f"orchestrate-{stratum.replace('_', '-')}",
            "name": "orchestrate",
            "version": None,
            "cohort": None,
            "tags": [],
        },
        "decision": decision,
        "outcome": {
            "result": result,
            "authority": authority,
            "checker": (
                None
                if condition is not None
                else {"identity": OBSERVED_CHECKERS[record.role], "independent": True}
            ),
            "condition": condition,
            "scores": None,
        },
        "resolution": {
            "model": served,
            "fallback_from": routed_model if served != routed_model else None,
        },
        "started_at": started_at,
        "completed_at": datetime.now(UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "measurements": measurements,
        "artifact_hashes": [] if commit is None else [f"sha1:{commit}"],
    }


def read_measurements(path: str | None) -> dict[str, Any]:
    """Return the usage, cost, quota, and latency facts the environment exposed.

    What is not there stays absent rather than becoming a zero: an unmeasured
    attempt is a cheaper-looking one only if absence is read as nothing spent.
    """

    if path is None:
        return {}

    try:
        exposed = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RunError(f"{path} does not hold exposed measurements: {exc}") from exc
    if not isinstance(exposed, dict):
        raise RunError(f"{path} must hold one object of exposed measurements")
    return cast(dict[str, Any], exposed)


def _import_details() -> dict[str, list[Any]]:
    """Return the empty durable account for one attempt's import results."""

    return {
        "imported": [],
        "identically_skipped": [],
        "conflicting": [],
        "refused": [],
        "standing_policy": [],
    }


def _extend_unique(target: list[Any], values: list[Any]) -> None:
    """Append each new JSON value once while preserving arrival order."""

    for value in values:
        if value not in target:
            target.append(value)


def _retain_import_result(
    attempt: dict[str, Any], result: dict[str, list[Any]]
) -> dict[str, list[Any]]:
    """Merge one automatic import result into the attempt's durable account."""

    held = attempt.get("import")
    retained = cast(dict[str, list[Any]], held) if isinstance(held, dict) else None
    if retained is None or set(retained) != set(_import_details()):
        retained = _import_details()
    for key, values in result.items():
        _extend_unique(retained[key], values)
    attempt["import"] = retained
    return retained


def _import_refusal(attempt_id: str, code: str, detail: str) -> dict[str, list[Any]]:
    """Return one retained automatic-import refusal for an attempt."""

    result = _import_details()
    result["refused"].append({"attempt_id": attempt_id, "code": code, "detail": detail})
    return result


def _automatic_import(attempt: dict[str, Any]) -> dict[str, list[Any]]:
    """Import one eligible attempt without letting evidence stop the run."""

    # Convert every Library failure into the stable non-fatal import account.
    try:
        return _automatic_import_unchecked(attempt)
    except Exception as exc:  # noqa: BLE001 - ledger failure never stops the run
        return _import_refusal(
            str(attempt.get("attempt_id") or "unknown"),
            "automatic_import_failed",
            str(exc),
        )


def _automatic_import_unchecked(
    attempt: dict[str, Any],
) -> dict[str, list[Any]]:
    """Import one eligible attempt and reduce expected Library responses."""

    attempt_id = str(attempt["attempt_id"])
    try:
        library = routed_observations()
        emitted = library.observe(
            {"schema_version": OBSERVATION_SCHEMA_VERSION, "attempts": [attempt]}
        )
    except (
        AttributeError,
        ImportError,
        KeyError,
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
    ) as exc:
        return _import_refusal(attempt_id, "automatic_import_failed", str(exc))

    # Preserve process and per-attempt refusals without reaching the ledger.
    if artifact_refusal := emitted.get("artifact_refusal"):
        return _import_refusal(
            attempt_id,
            str(artifact_refusal.get("code") or "invalid_artifact"),
            str(artifact_refusal.get("detail") or "Observation emission failed."),
        )
    refusals = [
        {
            "attempt_id": str(refusal.get("attempt_id") or attempt_id),
            "code": str(refusal.get("code") or "observation_refused"),
            "detail": str(refusal.get("detail") or "Observation emission failed."),
        }
        for refusal in emitted.get("refusals", [])
    ]
    if refusals:
        result = _import_details()
        result["refused"] = refusals
        return result

    # Import only external machine judgements and non-model conditions.
    observations = [
        observation
        for observation in emitted.get("observations", [])
        if observation.get("outcome_authority") in AUTOMATIC_AUTHORITIES
        or observation.get("outcome") in {"abstain", "infra_error"}
    ]
    if not observations:
        return _import_details()

    try:
        recorded = library.record(
            {
                "schema_version": OBSERVATION_SCHEMA_VERSION,
                "observations": observations,
            },
            Path.home() / ".kntnt" / "model-selector",
        )
    except (
        AttributeError,
        KeyError,
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
    ) as exc:
        return _import_refusal(attempt_id, "automatic_import_failed", str(exc))

    # Keep successful, duplicate, conflicting, and other refused identities.
    result = _import_details()
    result["imported"] = [str(key) for key in recorded.get("accepted", [])]
    result["identically_skipped"] = [str(key) for key in recorded.get("skipped", [])]
    result["standing_policy"] = list(recorded.get("standing_policy", []))
    for rejection in recorded.get("rejected", []):
        run_key = rejection.get("run_key")
        code = str(rejection.get("code") or "record_refused")
        if run_key is not None and code == "conflicting_identity":
            result["conflicting"].append(str(run_key))
        else:
            result["refused"].append(
                {
                    "attempt_id": attempt_id,
                    "code": code,
                    "detail": str(rejection.get("detail") or "Import was refused."),
                }
            )
    return result


def _resolve_observed_commit(cwd: Path, commit: str | None) -> str | None:
    """Resolve an optional artifact reference to its full commit digest."""

    if commit is None:
        return None
    try:
        return git(cwd, "rev-parse", "--verify", f"{commit}^{{commit}}").strip()
    except RunError as exc:
        raise RunError(
            f"{commit} is not a commit this repository resolves: name one it "
            "does — a digest, an abbreviation of one, or a reference such as "
            "a branch, a tag, or HEAD"
        ) from exc


def _write_attempt_account(path: Path | None, routing: Routing) -> Path:
    """Persist routing and the completed-attempt envelope as one run account."""

    write_routing(path, routing)
    written = attempts_file(path)
    if written is None:
        raise RunError("observed attempts need the run's state directory")
    completed = [attempt for attempt in routing.attempts if "outcome" in attempt]
    try:
        written.write_text(
            json.dumps(
                {
                    "schema_version": OBSERVATION_SCHEMA_VERSION,
                    "attempts": completed,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise RunError(
            f"this run's observed attempts could not be written: {exc}"
        ) from exc
    return written


def cmd_observe(
    cwd: Path,
    request_id: str,
    outcome: str,
    started_at: str | None,
    metrics: str | None,
    commit: str | None,
    resolved_model: str | None,
    state_path: Path | None,
) -> int:
    """Record what an independent verdict established about one routed attempt.

    The attempt becomes an importable observation and nothing else: no ledger,
    no profile, no frontier, no tracker state, and no repository file is
    touched here, and the artifact model-selector makes of it is imported only
    where the developer asks for it explicitly. A decision nothing judged stays
    audit data, a verdict role is refused by name, and a second outcome for the
    same attempt overwrites neither itself nor the first (ADR-0089).
    """

    # Refuse a verdict by name before the account is read at all: the seat a
    # verdict runs on is inherited, so there is no attempt of one to observe.
    try:
        route_record(request_id, {})
        routing = read_routing(state_path)
    except RunError as exc:
        return fail(str(exc))

    unrouted = dispatch_refusal(routing, request_id, f"{request_id} has completed")
    if unrouted is not None:
        return fail(unrouted)
    held = cast(Routing, routing)
    decided = cast(RouteRecord, held.decided(request_id))

    # An artifact identity is the digest itself and never a path into anybody's
    # checkout, but the caller has whatever reference its own commit gave it —
    # an abbreviation, a branch, the head it is standing on. So the repository
    # resolves what was named and the full digest is what gets recorded, and a
    # reference nothing resolves is refused in terms of what would be taken.
    try:
        commit = _resolve_observed_commit(cwd, commit)
    except RunError as exc:
        return fail(str(exc))

    if not isinstance(held.snapshot.get("harness"), dict):
        return fail(
            "this run's frozen snapshot names no Harness, and an observation is "
            "of the exact Harness its attempt ran on"
        )

    try:
        attempt = observed_attempt(
            held,
            decided,
            request_id,
            outcome,
            started_at,
            read_measurements(metrics),
            commit,
            resolved_model,
        )
    except RunError as exc:
        return fail(str(exc))

    # An outcome established twice is one fact; a different one is a conflict.
    standing = next(
        (kept for kept in held.attempts if kept["attempt_id"] == request_id), None
    )
    recorded = standing is None
    if standing is not None and _differs(standing, attempt):
        return fail(
            f"{request_id} already carries an observed outcome, and a second "
            "one changes neither: settle which verdict stands before observing"
        )
    if recorded:
        held.attempts.append(attempt)

    try:
        written = _write_attempt_account(state_path, held)
    except RunError as exc:
        return fail(f"this run's observed attempts could not be written: {exc}")

    emit(
        {
            "verb": "observe",
            "request_id": request_id,
            "role": decided.role,
            "ticket": decided.ticket,
            "stratum": attempt["workload_stratum"],
            "attempt_index": attempt["attempt_index"],
            "outcome": attempt["outcome"]["result"],
            "condition": attempt["outcome"]["condition"],
            "recorded": recorded,
            "observed": len(held.attempts),
            "attempts": str(written),
            "artifact": str(cast(Path, observation_file(state_path))),
        }
    )
    return 0


def _routed_attempt(
    request_id: str, state_path: Path | None, boundary: str
) -> tuple[Routing, RouteRecord]:
    """Return the frozen decision one internal lifecycle boundary addresses."""

    route_record(request_id, {})
    routing = read_routing(state_path)
    refused = dispatch_refusal(routing, request_id, boundary)
    if refused is not None:
        raise RunError(refused)
    held = cast(Routing, routing)
    return held, cast(RouteRecord, held.decided(request_id))


def cmd_attempt_start(request_id: str, state_path: Path | None) -> int:
    """Persist the first launch instant of one routed execution request."""

    try:
        routing, record = _routed_attempt(
            request_id, state_path, f"{request_id} is about to launch"
        )
    except RunError as exc:
        return fail(str(exc))

    # Preserve an in-flight start and refuse a request already completed.
    standing = next(
        (
            attempt
            for attempt in routing.attempts
            if attempt["attempt_id"] == request_id
        ),
        None,
    )
    if standing is not None and "outcome" in standing:
        return fail(f"{request_id} has already completed and cannot start again")
    recorded = standing is None
    if standing is None:
        standing = {
            "attempt_id": request_id,
            "started_at": datetime.now(UTC)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"),
        }
        routing.attempts.append(standing)
        try:
            write_routing(state_path, routing)
        except RunError as exc:
            return fail(str(exc))

    emit(
        {
            "verb": "attempt-start",
            "request_id": request_id,
            "role": record.role,
            "ticket": record.ticket,
            "started_at": standing["started_at"],
            "recorded": recorded,
        }
    )
    return 0


def cmd_attempt_finish(
    cwd: Path,
    request_id: str,
    outcome: str,
    metrics: str | None,
    commit: str | None,
    resolved_model: str | None,
    state_path: Path | None,
) -> int:
    """Persist, observe, and import one routed request's completion boundary."""

    try:
        routing, record = _routed_attempt(
            request_id, state_path, f"{request_id} has completed"
        )
        commit = _resolve_observed_commit(cwd, commit)
        measurements = read_measurements(metrics)
    except RunError as exc:
        return fail(str(exc))

    # Require a launch record before constructing the completed attempt.
    index = next(
        (
            position
            for position, attempt in enumerate(routing.attempts)
            if attempt["attempt_id"] == request_id
        ),
        None,
    )
    if index is None:
        return fail(f"{request_id} has no attempt-start to finish")
    standing = routing.attempts[index]
    offered = observed_attempt(
        routing,
        record,
        request_id,
        outcome,
        cast(str | None, standing.get("started_at")),
        measurements,
        commit,
        resolved_model,
    )

    # Persist a new completion before attempting the external ledger mutation.
    completed = "outcome" in standing
    conflicting = completed and _differs(standing, offered)
    retained = standing if completed else offered
    if not completed:
        routing.attempts[index] = offered
        try:
            _write_attempt_account(state_path, routing)
        except RunError as exc:
            return fail(str(exc))

    # Replay only the retained verdict; a conflict never enters the ledger.
    imported = _automatic_import(retained)
    if conflicting:
        run_keys = [
            *imported["imported"],
            *imported["identically_skipped"],
            *imported["conflicting"],
        ]
        _extend_unique(imported["conflicting"], run_keys)
    details = _retain_import_result(retained, imported)
    try:
        written = _write_attempt_account(state_path, routing)
    except RunError as exc:
        return fail(str(exc))

    if conflicting:
        return fail(
            f"{request_id} already carries a different completed outcome; "
            "the conflict was retained without overwriting it"
        )

    emit(
        {
            "verb": "attempt-finish",
            "request_id": request_id,
            "role": record.role,
            "ticket": record.ticket,
            "recorded": not completed,
            "observed": sum(1 for attempt in routing.attempts if "outcome" in attempt),
            "attempts": str(written),
            "import": details,
        }
    )
    return 0


def _differs(standing: dict[str, Any], offered: dict[str, Any]) -> bool:
    """Say whether two observations of one attempt establish different facts.

    The instant the outcome was recorded at is not one of those facts: the same
    verdict entered twice is the same verdict, and only what it says about the
    attempt decides whether the second entry conflicts with the first.
    """

    ignored = {"completed_at", "import"}
    return {key: value for key, value in standing.items() if key not in ignored} != {
        key: value for key, value in offered.items() if key not in ignored
    }


def observed_details(
    routing: Routing | None, state_path: Path | None
) -> dict[str, Any]:
    """Return completed attempts and every retained automatic import result."""

    # Aggregate each per-attempt account without multiplying replayed facts.
    completed = (
        []
        if routing is None
        else [attempt for attempt in routing.attempts if "outcome" in attempt]
    )
    details = _import_details()
    for attempt in completed:
        imported = attempt.get("import")
        if not isinstance(imported, dict):
            continue
        for key in (
            "imported",
            "identically_skipped",
            "conflicting",
            "standing_policy",
        ):
            values = imported.get(key)
            if isinstance(values, list):
                _extend_unique(details[key], values)
        refusals = imported.get("refused")
        if isinstance(refusals, list):
            _extend_unique(
                details["refused"],
                [
                    {
                        "attempt_id": refusal.get("attempt_id"),
                        "code": refusal.get("code"),
                    }
                    for refusal in refusals
                    if isinstance(refusal, dict)
                ],
            )

    return {
        "attempts": str(attempts_file(state_path)) if completed else None,
        "observed": len(completed),
        **details,
        "standing_policy": _escalated_cohorts(details["standing_policy"]),
    }


def _escalated_cohorts(evaluated: list[Any]) -> list[dict[str, Any]]:
    """Return the Cohorts this run's own evidence ratcheted, and the way back.

    Only the movements: a Cohort the threshold left where it was is an outcome
    the ledger accounted for and not a fact the night has to report. Each one
    carries the count behind it and the single command that undoes it, so the
    developer reads the decision and its reversal in the same line.
    """

    moved: list[dict[str, Any]] = []
    for entry in evaluated:
        if not isinstance(entry, dict) or entry.get("outcome") != POLICY_MOVED:
            continue
        row = entry.get("row")
        row = row if isinstance(row, dict) else {}
        cohort = str(entry.get("workload_cohort"))
        moved.append(
            {
                "workload_cohort": cohort,
                "from": row.get("from"),
                "to": row.get("to"),
                "failures": entry.get("failures"),
                "window": entry.get("window"),
                "threshold": entry.get("threshold"),
                "run_keys": entry.get("run_keys"),
                "reset": f"{POLICY_RESET_COMMAND} {cohort}",
            }
        )
    return moved


def repository_identity(cwd: Path) -> str:
    """Return the stable public identity available for the current repository."""

    remote = git_result(cwd, "config", "--get", "remote.origin.url")
    return remote.stdout.strip() if remote.returncode == 0 else str(cwd.resolve())


def flake_record(cwd: Path, evidence_path: Path) -> dict[str, Any]:
    """Complete and validate one checker-produced load-flake record."""

    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RunError(f"{evidence_path} does not hold flake evidence: {exc}") from exc
    if not isinstance(evidence, dict):
        raise RunError(f"{evidence_path} must hold one flake evidence object")

    required = {
        "failing_tests",
        "isolation_results",
        "full_rerun_result",
        "narrowed_command",
        "load_context",
    }
    if set(evidence) != required:
        raise RunError(
            f"{evidence_path} must hold exactly these fields: {', '.join(sorted(required))}"
        )
    if (
        not isinstance(evidence["failing_tests"], list)
        or not evidence["failing_tests"]
        or not all(isinstance(test, str) and test for test in evidence["failing_tests"])
    ):
        raise RunError("flake evidence must name at least one failing test")
    if evidence["isolation_results"] != ["passed", "passed", "passed"]:
        raise RunError("a load flake requires three passing isolated reruns")
    if evidence["full_rerun_result"] != "passed":
        raise RunError("a load flake requires one passing full-gate rerun")
    if not all(
        isinstance(evidence[field], str) and evidence[field]
        for field in ("narrowed_command", "load_context")
    ):
        raise RunError("flake evidence must name its narrowed command and load context")

    return {
        "repository": repository_identity(cwd),
        "branch": current_branch(cwd),
        "head": git(cwd, "rev-parse", "HEAD").strip(),
        **evidence,
        "timestamp": datetime.now(UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
    }


def flake_identity(record: dict[str, Any]) -> str:
    """Identify one unchanged-head flake independently of its write time."""

    stable = {key: value for key, value in record.items() if key != "timestamp"}
    return hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()


def write_atomically(path: Path, contents: str) -> None:
    """Replace one complete text file without exposing a partial generation."""

    # Allocate the replacement beside its destination for a same-volume rename.
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, text=True
    )

    # Flush a complete replacement before exposing it under the durable name.
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary).replace(path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def read_flake_ledger(path: Path) -> list[dict[str, Any]]:
    """Read the append-only flake ledger, refusing malformed durable state."""

    if not path.exists():
        return []
    try:
        return [
            cast(dict[str, Any], json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
        ]
    except (OSError, ValueError) as exc:
        raise RunError(f"the flake ledger could not be read: {exc}") from exc


@contextmanager
def flake_ledger_lock(ledger: Path) -> Iterator[None]:
    """Serialize atomic ledger generations without leaving another state file."""

    ledger.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(ledger.parent, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def cmd_flake(cwd: Path, evidence_path: Path, state_path: Path | None) -> int:
    """Append one independently established load flake to Skill-owned state."""

    ledger = Path.home() / FLAKE_HOME / FLAKE_LEDGER
    try:
        offered = flake_record(cwd, evidence_path)
        identity = flake_identity(offered)
        with flake_ledger_lock(ledger):
            records = read_flake_ledger(ledger)
            standing = next(
                (
                    record
                    for record in records
                    if record.get("repository") == offered["repository"]
                    and record.get("branch") == offered["branch"]
                    and record.get("head") == offered["head"]
                    and record.get("failing_tests") == offered["failing_tests"]
                ),
                None,
            )
            if standing is not None and flake_identity(standing) != identity:
                return fail(
                    "this unchanged-head flake already carries different evidence; settle which record stands before recording it"
                )
            recorded = standing is None
            if recorded:
                records.append(offered)
                write_atomically(
                    ledger,
                    "".join(
                        f"{json.dumps(record, sort_keys=True)}\n" for record in records
                    ),
                )

        run_path = run_flakes_file(state_path)
        if run_path is not None:
            run_ids = (
                []
                if not run_path.exists()
                else cast(list[str], json.loads(run_path.read_text(encoding="utf-8")))
            )
            if identity not in run_ids:
                run_ids.append(identity)
                write_atomically(run_path, json.dumps(run_ids, indent=2) + "\n")
    except (OSError, RunError, ValueError) as exc:
        return fail(f"flake evidence could not be written: {exc}")

    emit(
        {
            "verb": "flake",
            "recorded": recorded,
            "ledger": str(ledger),
            "record": standing or offered,
        }
    )
    return 0


def reported_flakes(cwd: Path, state_path: Path | None) -> list[dict[str, Any]]:
    """Return this run's flakes with earlier recurrence counts per test."""

    run_path = run_flakes_file(state_path)
    if run_path is None or not run_path.exists():
        return []
    ledger = read_flake_ledger(Path.home() / FLAKE_HOME / FLAKE_LEDGER)
    identities = cast(list[str], json.loads(run_path.read_text(encoding="utf-8")))
    repository = repository_identity(cwd)
    reported: list[dict[str, Any]] = []
    for index, record in enumerate(ledger):
        if flake_identity(record) not in identities:
            continue
        earlier = ledger[:index]
        reported.append(
            {
                **record,
                "earlier_records": {
                    test: sum(
                        prior.get("repository") == repository
                        and test in prior.get("failing_tests", [])
                        for prior in earlier
                    )
                    for test in record["failing_tests"]
                },
            }
        )
    return reported


def _attempt_passed(attempt: dict[str, Any]) -> bool:
    """Say whether one completed attempt carries an external passing verdict."""

    outcome = attempt.get("outcome")
    return isinstance(outcome, dict) and outcome.get("result") == "pass"


def _instant(value: Any) -> datetime | None:
    """Parse one engine-written instant, or None where none was written."""

    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def verified_pass_timing(routing: Routing | None) -> dict[int, dict[str, Any]]:
    """Return each ticket's Time to Verified Pass and the status that reads it.

    The measure runs from a ticket's first routed launch to the instant its
    first passing verdict landed, retries included: a cheap configuration that
    needed two tries took as long as both of them, and a report that showed
    only the successful try would price the policy as though the failures had
    been free. Both boundaries are the engine's own instants rather than
    anything a session reports about itself (ADR-0137).

    The status is what tells an absent number from a zero. A ticket nothing
    launched, a ticket whose every launched attempt finished without a pass,
    and a ticket still in flight are three different silences, and each of
    them is decided by engine facts alone.
    """

    if routing is None:
        return {}

    # Group the run's attempts under the ticket whose decision launched them.
    numbered = {
        record.request_id: record.ticket
        for record in routing.decisions
        if record.ticket is not None
    }
    grouped: dict[int, list[dict[str, Any]]] = {}
    for attempt in routing.attempts:
        number = numbered.get(str(attempt.get("attempt_id")))
        if number is not None:
            grouped.setdefault(number, []).append(attempt)

    # Read each ticket's own boundaries, or say which silence it is in.
    timing: dict[int, dict[str, Any]] = {}
    for number, attempts in grouped.items():
        launched = [
            instant
            for instant in (_instant(attempt.get("started_at")) for attempt in attempts)
            if instant is not None
        ]
        passed = [
            instant
            for instant in (
                _instant(attempt.get("completed_at"))
                for attempt in attempts
                if _attempt_passed(attempt)
            )
            if instant is not None
        ]
        seconds: float | None = None
        if any(_attempt_passed(attempt) for attempt in attempts):
            status = VERIFIED_PASS
            if launched and passed:
                seconds = (min(passed) - min(launched)).total_seconds()
        elif any("outcome" not in attempt for attempt in attempts):
            status = INCOMPLETE
        else:
            status = NOT_PASSED
        timing[number] = {
            "time_to_verified_pass_seconds": seconds,
            "time_to_verified_pass_status": status,
        }
    return timing


def cmd_report(cwd: Path, reference: str | None, state_path: Path | None) -> int:
    """Print every ticket in scope grouped by current Ticket Resolution.

    One report rather than a running commentary, and every ticket in scope in
    it exactly once — a ticket the run drops in silence is one the developer
    will not know to pick up. The five groups partition the scope by
    construction: current resolutions, what an unsuccessful resolution
    stranded, then everything this run never had on its frontier — held by a
    cycle, by work outside the run, by another session's claim, or by the run
    stopping before its wave came round. Ticket detail retains Run Outcome and
    Reconciliation provenance independently of that grouping.
    """

    # The label is asked for twice, because a ticket the run recorded is closed
    # by the run itself where it passed, and can be closed by anybody after it
    # where it did not. What the run was aimed at is resolved against both
    # halves, so a spec whose children are all finished is still the spec it
    # was named as.
    try:
        branch = current_branch(cwd)
        listed = open_listing(cwd)
        finished = closed_listing(cwd)
        scope = (
            resolve_scope(cwd, reference, listed + finished)
            if reference is not None
            else None
        )
        open_scope = tickets_in_scope(cwd, listed, scope)
        tickets = sorted(
            open_scope + tickets_recorded(finished, scope),
            key=lambda ticket: ticket.number,
        )
        say_where_work_stands(cwd, tickets, branch)
        base = run_base(cwd, tickets)
        regenerated = regenerated_merges(cwd, {ticket.number for ticket in tickets})
        flakes = reported_flakes(cwd, state_path)
    except (OSError, RunError, ValueError) as exc:
        return fail(str(exc))

    # Stranding is read off the open scope alone: a ticket that is finished has
    # no unmet blocker left to strand anything behind.
    recorded = {
        outcome: [
            ticket.number for ticket in tickets if ticket.resolution.outcome == outcome
        ]
        for outcome in OUTCOMES
    }
    stranded = stranded_behind(open_scope)
    accounted = set(stranded).union(*recorded.values())
    never_on_frontier = [
        ticket.number for ticket in tickets if ticket.number not in accounted
    ]
    outcome = {
        DONE: recorded[DONE],
        FAILED: recorded[FAILED],
        CONFLICTED: recorded[CONFLICTED],
        "stranded": stranded,
        "never_on_frontier": never_on_frontier,
    }

    # The route account is rendered from what was frozen or not at all: the
    # decisions a night was worked under are auditable exactly, and where they
    # are gone the account says so rather than reading what is current back as
    # though it had been (ADR-0085).
    routing, routing_reason, _ = frozen_routing(state_path)

    # Assemble the complete durable account from the facts read above.
    report = {
        "verb": "report",
        "label": READY_LABEL,
        "scope": None if scope is None else [asdict(aim) for aim in scope],
        "branch": branch,
        "base": base,
        "routing": routing_details(routing),
        "routing_reason": routing_reason,
        "observations": observed_details(routing, state_path),
        "flakes": flakes,
        "regenerated": regenerated,
        "tickets": [
            ticket_details(ticket, verified_pass_timing(routing)) for ticket in tickets
        ],
        **outcome,
    }

    # Project the authoritative account into the terminal dashboard itself.
    if progress_file(state_path) is not None:
        remembered = remembered_state(state_path, cwd)
        current = remembered.progress if remembered is not None else None
        completed = sum(len(outcome[group]) for group in OUTCOMES)
        write_progress(
            state_path,
            "wave_verdict",
            ProgressState(
                wave=current.wave if current is not None else 1,
                ticket=None,
                amendments_spent=0,
                tickets_completed=completed,
                tickets_remaining=len(tickets) - completed,
            ),
            outcome,
        )

    emit(report)
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


def add_deliberation_flag(parser: argparse.ArgumentParser) -> None:
    """Let a verb take the portable deliberation lock, and only its exact values.

    The five public levels are the whole of the portable scale, and a value
    outside them is refused rather than normalised: a level the Interface
    cannot map is a level nothing can launch, and quietly reading it as a
    neighbour would be the fall-through overrides never make (ADR-0083).
    """

    parser.add_argument("--deliberation", choices=DELIBERATION_LEVELS)


def add_scope_flag(parser: argparse.ArgumentParser) -> None:
    """Let a verb that reads the whole label be aimed at part of it.

    Only the two verbs that read a set take it. A verb already given one ticket
    by number is aimed, and taking a second way of saying which ticket would
    state something untrue about what happened — which is where ADR-0029 draws
    the line between a flag that is merely meaningless and one that misleads.
    """

    parser.add_argument("--scope")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the run CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="verb", required=True)

    plan = sub.add_parser("plan", help="Print what a run would work.")
    plan.add_argument("--dry-run", action="store_true")
    plan.add_argument("--at-once", type=int, default=ONE_AT_A_TIME)
    plan.add_argument("--model")
    plan.add_argument("--approval")
    plan.add_argument("--fast", action="store_true")
    add_deliberation_flag(plan)
    add_scope_flag(plan)
    add_shared_flags(plan)

    route = sub.add_parser("route", help="Freeze one model-selector route response.")
    route.add_argument("--response", required=True, type=Path)
    route.add_argument("--dry-run", action="store_true")
    route.add_argument("--model")
    route.add_argument("--fast", action="store_true")
    route.add_argument("--starting", action="append", type=int)
    route.add_argument("--run-claimed", action="append", type=int)
    add_deliberation_flag(route)
    add_shared_flags(route)

    claim = sub.add_parser("claim", help="Take one ticket before working it.")
    claim.add_argument("--ticket", required=True, type=int)
    add_shared_flags(claim)

    park = sub.add_parser("park", help="Return one ticket to the human loop.")
    park.add_argument("--ticket", required=True, type=int)
    add_shared_flags(park)

    isolate = sub.add_parser("isolate", help="Give one ticket a working tree.")
    isolate.add_argument("--ticket", required=True, type=int)
    add_shared_flags(isolate)

    integrate = sub.add_parser("integrate", help="Merge one ticket into the branch.")
    integrate.add_argument("--ticket", required=True, type=int)
    add_shared_flags(integrate)

    rebuild = sub.add_parser("rebuild", help="Discard one ticket's first try.")
    rebuild.add_argument("--ticket", required=True, type=int)
    add_shared_flags(rebuild)

    amend = sub.add_parser("amend", help="Record one numbered bounded amend.")
    amend.add_argument("--ticket", required=True, type=int)
    amend.add_argument("--attempt", required=True, type=int)
    amend.add_argument("--phase", required=True, choices=AMEND_PHASES)
    amend.add_argument("--verdict-file")
    add_shared_flags(amend)

    record = sub.add_parser("record", help="Record one ticket's outcome.")
    record.add_argument("--ticket", required=True, type=int)
    record.add_argument("--outcome", required=True, choices=RECORDABLE)
    record.add_argument("--commit")
    record.add_argument("--collided-with", action="append", type=int)
    record.add_argument("--blocked-by", action="append", type=int)
    add_shared_flags(record)

    reconcile = sub.add_parser(
        "reconcile", help="Resolve work completed outside Orchestrate."
    )
    reconcile.add_argument("--ticket", required=True, type=int)
    reconcile.add_argument("--commit")
    add_shared_flags(reconcile)

    observe = sub.add_parser(
        "observe", help="Record one routed attempt's established outcome."
    )
    observe.add_argument("--request", required=True)
    observe.add_argument("--outcome", required=True, choices=tuple(OBSERVED_OUTCOMES))
    observe.add_argument("--started-at")
    observe.add_argument("--metrics")
    observe.add_argument("--commit")
    observe.add_argument("--resolved-model")
    add_shared_flags(observe)

    attempt_start = sub.add_parser(
        "attempt-start", help="Start one internal routed attempt."
    )
    attempt_start.add_argument("--request", required=True)
    add_shared_flags(attempt_start)

    attempt_finish = sub.add_parser(
        "attempt-finish", help="Finish one internal routed attempt."
    )
    attempt_finish.add_argument("--request", required=True)
    attempt_finish.add_argument(
        "--outcome", required=True, choices=tuple(OBSERVED_OUTCOMES)
    )
    attempt_finish.add_argument("--metrics")
    attempt_finish.add_argument("--commit")
    attempt_finish.add_argument("--resolved-model")
    add_shared_flags(attempt_finish)

    flake = sub.add_parser("flake", help="Record one load-induced test flake.")
    flake.add_argument("--evidence", required=True, type=Path)
    add_shared_flags(flake)

    progress = sub.add_parser("progress", help="Replace the run progress dashboard.")
    progress.add_argument("--phase", required=True, choices=PROGRESS_PHASES)
    progress.add_argument("--wave", required=True, type=int)
    progress.add_argument("--ticket", type=int)
    progress.add_argument("--amends-spent", type=int, default=0)
    progress.add_argument("--completed", required=True, type=int)
    progress.add_argument("--remaining", required=True, type=int)
    add_shared_flags(progress)

    report = sub.add_parser("report", help="Print the consolidated report.")
    add_scope_flag(report)
    add_shared_flags(report)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Dispatch one verb. Return an exit code."""

    # Resolve the invocation and its session-scoped state location.
    args = parse_args(argv if argv is not None else sys.argv[1:])
    cwd = Path.cwd()
    state_path = state_file(args.state_dir)
    is_dry_run = args.verb in {"plan", "route"} and args.dry_run

    # Migrate legacy state only for verbs whose contract permits writes.
    if not is_dry_run:
        carry_state_forward(state_path)

    # Dispatch the selected verb against the resolved repository and state.
    if args.verb == "plan":
        return cmd_plan(
            cwd,
            dry_run=args.dry_run,
            at_once=args.at_once,
            model=args.model,
            deliberation=args.deliberation,
            fast=args.fast,
            state_path=state_path,
            reference=args.scope,
            approval=args.approval,
        )
    if args.verb == "route":
        return cmd_route(
            cwd,
            args.response,
            state_path,
            dry_run=args.dry_run,
            model=args.model,
            deliberation=args.deliberation,
            fast=args.fast,
            starting=args.starting,
            run_claimed=args.run_claimed,
        )
    if args.verb == "claim":
        result = cmd_claim(cwd, args.ticket, state_path)
        if result == 0:
            advance_progress(cwd, state_path, "preflight", args.ticket)
        return result
    if args.verb == "park":
        return cmd_park(cwd, args.ticket, state_path)
    if args.verb == "isolate":
        advance_progress(cwd, state_path, "isolate", args.ticket)
        return cmd_isolate(cwd, args.ticket)
    if args.verb == "integrate":
        advance_progress(cwd, state_path, "integrate", args.ticket)
        return cmd_integrate(cwd, args.ticket, state_path)
    if args.verb == "rebuild":
        return cmd_rebuild(cwd, args.ticket)
    if args.verb == "amend":
        result = cmd_amend(
            cwd,
            args.ticket,
            args.attempt,
            args.phase,
            args.verdict_file,
            state_path,
        )
        if result == 0:
            advance_progress(cwd, state_path, "amend", args.ticket, args.attempt)
        return result
    if args.verb == "record":
        result = cmd_record(
            cwd,
            args.ticket,
            args.outcome,
            args.commit,
            args.collided_with,
            args.blocked_by,
            state_path,
        )
        if result == 0:
            advance_progress(
                cwd,
                state_path,
                "note",
                args.ticket,
                is_ticket_completed=args.outcome in OUTCOMES,
            )
        return result
    if args.verb == "observe":
        return cmd_observe(
            cwd,
            args.request,
            args.outcome,
            args.started_at,
            args.metrics,
            args.commit,
            args.resolved_model,
            state_path,
        )
    if args.verb == "attempt-start":
        return cmd_attempt_start(args.request, state_path)
    if args.verb == "attempt-finish":
        return cmd_attempt_finish(
            cwd,
            args.request,
            args.outcome,
            args.metrics,
            args.commit,
            args.resolved_model,
            state_path,
        )
    if args.verb == "flake":
        return cmd_flake(cwd, args.evidence, state_path)
    if args.verb == "progress":
        progress = ProgressState(
            wave=args.wave,
            ticket=args.ticket,
            amendments_spent=args.amends_spent,
            tickets_completed=args.completed,
            tickets_remaining=args.remaining,
        )
        remember_progress(state_path, cwd, progress)
        written = write_progress(state_path, args.phase, progress, None)
        emit({"verb": "progress", "progress": written})
        return 0
    if args.verb == "reconcile":
        return cmd_reconcile(cwd, args.ticket, args.commit)
    return cmd_report(cwd, args.scope, state_path)


if __name__ == "__main__":
    raise SystemExit(main())
