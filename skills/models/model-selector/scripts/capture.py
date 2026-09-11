# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Turn ordinary Harness work into Units of Work, without anybody asking.

A user works in their Harness all day, and what that work cost — the model it
ran on, how long it took, how much of it changed anything — is never written
down, because writing it down is a thing they have to remember to do. This is
that capture, and it measures ordinary work; it never judges it (ADR-0179).
Grading is `grade.py`'s, bought deliberately and under a budget, and this
module only hands it something to grade.

What it hands over is a **Unit of Work**: one instruction and the work done in
answer to it, from the moment an agent is told to do something — by a person
or by another agent — to the moment it hands control back. Only a Unit that is
a job is ever written: a delegated one — a subagent's own record, or a span
whose instruction names a routed attempt — once it is substantial, and one of
the session's own once it is substantial and ran for ten minutes besides. A
session of quick questions and answers, and a person's short exchanges with
their own Main Seat, leave no trace at all. On Claude Code a finished record
splits cleanly into Units, and there are two of them: a subagent's own record
is one whole Unit, carrying the model and effort that subagent actually ran
on, and the session's own record is one Unit per user instruction.

Each record is read the moment it is finished and never before. A subagent's
is read at that subagent's own stop, which is the moment its record is whole
and the moment the Harness names the file; the session's is read at the
session's own end. Nothing runs per turn: a start and a stop are moments this
feature no longer asks any Harness for, because the answer to either was a
file written for nobody and a session that never reached its end was never
measured at all (#294).

Capture follows this Skill's own Enabled state and asks for nothing beyond it
(#223). The Manager installs this feature's owned lifecycle integration into
every supported Detected Harness of the Global layer the moment the Skill is
Enabled, placed, or refreshed, and removes every entry the moment it is
Disabled there — the same two seams that already place and remove the Skill's
own files. There is no second opt-in, no consent prompt, and no configuration
state of this feature's own to go stale: disk is the one truth (ADR-0179), so
a hook either runs because a Harness's own configuration names it or it does
not run at all.

What it writes is the minimum a Unit needs: identities are opaque,
measurements the environment did not expose stay `null`, and no prompt,
response, reasoning, diff, terminal output, or transcript is ever copied. The
two excerpts a Unit carries exist for the grader alone, are capped at
`INSTRUCTION_CHARS` and `RESULT_CHARS`, and are removed from the pending store
the moment that Unit becomes a measurement.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from contextlib import suppress
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

SCHEMA_VERSION = 2

# Every lifecycle signal this feature understands, per Harness family. A stop
# is one turn of an ongoing session and never a session's own end. Codex CLI
# 0.153.0's own `hooks.json` names its moments in the same PascalCase Claude
# Code's `settings.json` does, which is what this feature's own hook table is
# registered under; the camelCase spellings (`sessionStart`, `stop`,
# `sessionEnd`) are the app-server protocol's own `HookEventName`, the
# normalized runtime view `hooks/list` reports back, and are accepted here as
# the same convention rather than as a confirmed reading of any payload
# (ADR-0179).
START_EVENTS = frozenset({"SessionStart", "sessionStart", "session.created"})
TURN_EVENTS = frozenset({"Stop", "stop", "session.idle"})
SUBAGENT_EVENTS = frozenset({"SubagentStop"})
ERROR_EVENTS = frozenset({"session.error"})
END_EVENTS = frozenset({"SessionEnd", "sessionEnd", "session.deleted"})

# The moments this feature actually asks each Harness for, which are the
# moments at which a record it can read has just been finished. Everything
# else a Harness offers is left uninstalled: an entry at a moment this module
# answers with no work is an interpreter started once a turn, every turn, in
# every session on the machine (#294). The two sets above are still named
# because a stale entry on a machine the Manager has not reconverged goes on
# arriving, and is answered with no work rather than with a traceback.
#
# Codex and OpenCode keep their finishing moments alone, no record this module
# knows how to split existing at either. OpenCode has two of them — a session
# deleted and a session errored — because either is that session finishing.
WANTED_EVENTS: dict[str, tuple[str, ...]] = {
    "claude-code": ("SubagentStop", "SessionEnd"),
    "codex": ("SessionEnd",),
    "opencode": ("session.deleted", "session.error"),
}

# Where a Harness names the lifecycle moment inside the payload rather than on
# the command line. Claude Code and Codex both do, so a hook installed without a
# per-event command still knows which moment it is answering. `eventName` is
# Codex's own field for this everywhere else its JSON API names a moment
# (`hooks/list`'s `HookMetadata`, its `HookRunSummary` notifications); its
# hook-invocation payload was not directly observable — every attempt to
# drive a hook to fire, trust-bypassed or not, ran into Codex's own
# session/auth lifecycle rather than a shape problem — so this is carried as
# the same convention rather than as a confirmed reading of that payload.
EVENT_FIELDS: tuple[str, ...] = ("hook_event_name", "eventName", "event", "type")

# The only fields a lifecycle payload may contribute. Everything else a
# Harness sends — and Harnesses send whole transcripts — is dropped before
# anything is written, so nothing forbidden can arrive by sitting beside what
# is wanted.
#
# Both paths are locate-only (#225): each is read to open one finished record
# and is discarded inside the same invocation. Neither reaches a Unit, and
# nothing this module writes to disk carries either — `_hook` reads them
# locally out of the cleaned payload and passes one of them straight to the
# read that moment makes.
PAYLOAD_ALLOWED = frozenset(
    {
        "session_id",
        "harness",
        "transcript_path",
        "agent_transcript_path",
    }
)

# Where Claude Code names the stopped subagent's own record. Established from
# the Harness as installed rather than assumed (ADR-0179): Claude Code 2.1.263
# states of `SubagentStop` that its "Input to command is JSON with agent_id,
# agent_type, and agent_transcript_path". That is a different file from the
# `transcript_path` every hook carries, which at this moment names the parent
# session's own record and must not be read here — the session's turn to be
# read is its own end.
SUBAGENT_TRANSCRIPT_FIELD = "agent_transcript_path"

# Where the pending Units wait for the grader, beside the measurement ledger
# under the selected data directory, and where the grader records that it ran.
# Named once here rather than left for a consumer to infer.
PENDING_FILE = "pending.jsonl"

# What earlier designs of this Skill left behind in a data directory. Nothing
# reads any of them and nothing writes them any more: they are the stored
# configuration, the standing policy, the frozen snapshots and the two ledgers
# of a router that no longer exists, and the check state of an unattended
# source refresh that no longer runs. Named here because a verb that does not
# know a file exists cannot remove it, and a file no verb knows about sits in
# somebody's home directory for as long as the Skill stays installed.
RETIRED_FILES = (
    "access-channel-snapshots.jsonl",
    "alias-bindings.jsonl",
    "benchmark-definitions.jsonl",
    "capability-priors.jsonl",
    "config-history.jsonl",
    "config.bak.json",
    "config.json",
    "derived-frontiers.json",
    "evaluation-configurations.jsonl",
    "model-versions.jsonl",
    "price-schedules.jsonl",
    "run-observations.jsonl",
    "source-states.jsonl",
    "standing-policy-history.jsonl",
    "standing-policy.json",
    "subscription-schedules.jsonl",
    "usage-records.jsonl",
)

# The invalid configurations the retired design saved beside its own, each
# stamped with the instant it was rejected. Matched by shape rather than named,
# because there is one per rejection and no list can hold them all.
RETIRED_PATTERN = "config.invalid.*.json"
GRADER_STATE_FILE = "grader.json"

# The Harnesses whose own finished record this module knows how to split into
# Units. It is capture's own list rather than the Collection Library's,
# because the split is by instruction and the Library's reader folds by Seat:
# a Harness the Library learns to read is not thereby a Harness whose
# instruction boundaries this module knows.
READABLE_HARNESSES: tuple[str, ...] = ("claude-code",)

# The line a routed builder brief opens with, naming the attempt whoever
# dispatched it already decided. Where an instruction opens with it — a
# subagent's first user message, or an instruction in the session's own
# record — that attempt is this Unit's identity rather than the hash below,
# and the Unit is delegated: the caller that dispatched the work files its own
# verdict under the same name, and one build filed from two sides is one row
# rather than two (issue #291, #303). Matched on the instruction's first line
# only. A person at a keyboard does not type it, so an instruction carrying it
# is a routed brief wherever it arrived. The same form is stated for the tests
# in `tests/support/model_routing.py`, a shipped script having no business
# importing a test file. The backticks are optional because a brief is
# Markdown and a filler may leave the placeholder's own.
ATTEMPT_LINE = re.compile(r"^attempt_id:[ \t]*`?([^\s`]+)`?[ \t]*$")

# How the token categories a Claude Code turn reports map onto the five a
# measurement is priced in. Re-derived per turn from `message.usage`:
# `output_tokens_details` is absent more often than it is present — on this
# collection's own machine, on roughly six in ten subagent turns — so its
# absence is read as an unmeasured `reasoning`, never as a zero.
TOKEN_FIELDS: tuple[tuple[str, str], ...] = (
    ("input", "input_tokens"),
    ("cache_read", "cache_read_input_tokens"),
    ("cache_write", "cache_creation_input_tokens"),
    ("output", "output_tokens"),
)
REASONING_FIELD = "thinking_tokens"
TOKEN_CATEGORIES: tuple[str, ...] = (
    "input",
    "cache_read",
    "cache_write",
    "output",
    "reasoning",
)

# What makes a Unit substantial enough to be worth measuring at all. Any one
# of the three is enough, because they are three ways of being real work: a
# job that changed things, a job that took time, and a job that wrote a lot.
# Everything below all three is discarded with no trace, which is what keeps a
# session of quick questions and answers out of the measurement entirely. A
# delegated Unit needs nothing more; a Unit of the session's own also has to
# have run for `OWN_UNIT_SECONDS`, below.
SUBSTANTIAL_CHANGING_CALLS = 3
SUBSTANTIAL_SECONDS = 60.0
SUBSTANTIAL_OUTPUT_TOKENS = 4000.0

# How long a Unit of the session's own has to run before it is evidence at
# all. Model Selector is only ever asked what to delegate, and a person's
# exchange with their own Main Seat is mostly a different size of job; fitted
# beside delegated work, that difference in size is read as a difference in
# models. What makes a Unit a job is an agent working on its own long enough,
# so a Unit that was delegated — read from a subagent's own record, or opened
# by an instruction naming a routed attempt — is held to the substantial test
# alone, and any other Unit is written only once it ran this long from its
# instruction to handing control back (#303).
OWN_UNIT_SECONDS = 600.0

# How much of an instruction and of a result the grader is given. They are the
# only free text a Unit carries, they exist to be read by one judge once, and
# they are gone from the store the moment that Unit is graded. Two limits
# rather than one, because the two texts are not the same length of thing: an
# instruction is a brief and a result is the answer to it, and a judge shown
# the opening of each is grading a summary it invented rather than the work.
INSTRUCTION_CHARS = 4000
RESULT_CHARS = 12000

# The tools that change something by definition, whatever their arguments.
CHANGING_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})

# The tools that run a shell command, whose arguments decide whether the call
# changed anything. The command string is classified here and discarded here:
# no part of it reaches a Unit or a measurement.
SHELL_TOOLS = frozenset({"Bash"})

# Shell commands that only read. A call every one of whose segments starts
# with one of these is a look at the machine rather than a change to it;
# anything else is counted as changing, because the cost of over-counting is
# one more Unit measured and the cost of under-counting is real work lost.
READING_HEADS = frozenset(
    {
        "awk",
        "basename",
        "cat",
        "cd",
        "cut",
        "date",
        "df",
        "diff",
        "dirname",
        "du",
        "echo",
        "env",
        "file",
        "find",
        "grep",
        "head",
        "jq",
        "ls",
        "printenv",
        "ps",
        "pgrep",
        "pwd",
        "readlink",
        "realpath",
        "rg",
        "sed",
        "sort",
        "stat",
        "tail",
        "tr",
        "tree",
        "type",
        "uniq",
        "wc",
        "which",
    }
)

# `git` is the one head common enough that treating the whole of it as a
# change would call nearly every session substantial. Its reading verbs are
# named instead, and every other one counts as a change.
READING_GIT_VERBS = frozenset(
    {
        "blame",
        "branch",
        "describe",
        "diff",
        "log",
        "ls-files",
        "remote",
        "rev-parse",
        "show",
        "status",
        "worktree",
    }
)

# What a shell command has to mention before a Unit is credited with having
# run tests. It is a free signal rather than a reading of anybody's output:
# whether they passed is the tool result's own error flag and nothing else.
TEST_RUNNERS = (
    "pytest",
    "vitest",
    "jest",
    "phpunit",
    "go test",
    "cargo test",
    "npm test",
)

# What Claude Code writes into the transcript when a person stops a turn.
INTERRUPTION_MARKER = "[Request interrupted"

# Who a user line has to have come from for it to begin a Unit. Claude Code
# stamps every user line with an `origin.kind`, and only two of those kinds
# are an instruction somebody gave: `human` is a person typing, `peer` is
# another session messaging this one. `task-notification` is a background task
# reporting back and `auto-continuation` is the session continuing itself —
# neither is anybody's instruction, and splitting at a notification files a
# Unit whose instruction is a report and whose result is whatever the session
# did next.
INSTRUCTION_ORIGINS = frozenset({"human", "peer"})


@dataclass(frozen=True)
class Unit:
    """One instruction and the work done in answer to it."""

    unit_id: str
    session: str
    harness: str
    started_at: str
    ended_at: str
    seconds: float
    model: str | None
    deliberation: str | None
    tokens: dict[str, float | None]
    tool_calls: int
    changing_tool_calls: int
    delegated: bool
    signals: dict[str, Any]
    instruction_excerpt: str
    result_excerpt: str


@dataclass
class _Span:
    """One Unit under construction, as the transcript is walked in order.

    Mutable on purpose: a span is filled turn by turn and frozen into a `Unit`
    once the instruction after it arrives, which is the only moment its end is
    known.
    """

    instruction: str
    started_at: str
    ended_at: str
    result: str = ""
    seats: dict[tuple[str | None, str | None], int] = field(default_factory=dict)
    tokens: dict[str, float | None] = field(
        default_factory=lambda: dict.fromkeys(TOKEN_CATEGORIES)
    )
    tool_calls: int = 0
    changing_tool_calls: int = 0
    tests_ran: bool = False
    tests_failed: bool = False
    interrupted: bool = False
    errored: bool = False


def _parsed(instant: Any) -> datetime | None:
    """Return one recorded instant as a datetime, or None where it is unusable."""

    if not isinstance(instant, str):
        return None
    try:
        return datetime.fromisoformat(instant)
    except ValueError:
        return None


def _opaque(value: Any) -> str:
    """Return one stable opaque identity for a Harness-supplied identifier.

    A session id is a path, a ticket number, or a workspace name often enough
    that keeping it raw would leak exactly what the data boundary excludes. The
    digest is stable, so the same session is the same identity across events.
    """

    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return digest[:32]


def home(data: Path) -> Path:
    """Return the capture home inside one data directory.

    Nothing writes it any more. It is still named because an earlier design
    filled it with per-session drafts, and a directory no verb knows about
    sits in somebody's home directory for as long as the Skill stays installed
    (#294).
    """

    return data / "capture"


def _by_path(name: str, *candidates: Path) -> Any:
    """Load one module by path under *name*, from the first candidate that exists.

    Every module this one reaches is loaded this way rather than imported: a
    Skill's scripts are placed, not installed, so there is no package for an
    ordinary import to resolve against. The loaded module is registered under
    *name* before it executes, which is what lets its own dataclasses resolve
    the annotations they declare.
    """

    # A module already registered under this name is handed back as it stands,
    # so that one invocation loading the same sibling twice executes it once.
    held = sys.modules.get(name)
    if held is not None:
        return held

    for candidate in candidates:
        if not candidate.exists():
            continue
        spec = importlib.util.spec_from_file_location(name, candidate)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    raise RuntimeError(f"{name} is missing")


def _library(*relative: str) -> tuple[Path, Path]:
    """Return the two places a Collection Library module may sit, in order.

    Two layouts, tried in turn: this repository's own
    `skills/models/model-selector/scripts/` sits three directories above
    `skills/kntnt/library/`, while an Enabled Skill's installed copy — the
    only copy the Manager's own install and remove seams ever run (#223) —
    sits at `<layer>/model-selector/scripts/`, two directories above the
    sibling `<layer>/kntnt/library/`.
    """

    here = Path(__file__).resolve().parent
    tail = Path("kntnt", "library", "scripts", *relative)
    return here.parent.parent.parent / tail, here.parent.parent / tail


def _integrations() -> Any:
    """Load the Collection Library's owned-integration mechanics.

    Harness-specific installation is not this feature's knowledge to hold: it is
    the Library's, so that a second Skill needing the same thing finds it there
    rather than reaching into this one (ADR-0177).
    """

    return _by_path("kntnt_integrations", *_library("integrations.py"))


def _sibling(name: str) -> Any:
    """Load one of this Skill's own scripts, from beside this module.

    Its own knowledge rather than the Library's, so it sits in `scripts/` next
    to this file and needs neither of the two layouts a Library module is
    resolved through.
    """

    return _by_path(
        f"model_selector_{name}", Path(__file__).resolve().parent / f"{name}.py"
    )


def owner() -> str:
    """Return the stable ownership identity every installed integration carries."""

    return "kntnt.model-selector.capture"


def install(
    data: Path, root: Path, harnesses: list[str], command: list[str]
) -> dict[str, Any]:
    """Install this feature's owned integration, idempotently.

    This is the word the Manager says at every seam that places or refreshes
    an Enabled Skill's files (#223): install, repair, and refresh are the
    same convergence over whatever is on disk (ADR-0179), so being asked
    twice changes nothing. Naming no Harness means every Harness the
    Collection Library has an adapter for.

    Only a named Harness the Library's `integrations.SUPPORTED` actually
    holds an adapter for is attempted; the rest is reported as a single
    count naming the supported set rather than one row each, because a
    caller naming Detected Harnesses in bulk — this collection ships an
    adapter for three of the seventy-odd this machine may have — would
    otherwise bury the outcome that matters under rows for Harnesses no
    adapter exists for (#223 decision 3).
    """

    integrations = _integrations()
    supported = set(integrations.SUPPORTED)
    named = list(harnesses) or list(integrations.SUPPORTED)
    attempted = [harness for harness in named if harness in supported]
    unsupported = [harness for harness in named if harness not in supported]
    runs = _hook_command(command, data)
    installed = [
        integrations.install(
            owner(), harness, root, runs, events=WANTED_EVENTS.get(harness)
        )
        for harness in attempted
    ]
    return {
        "installed": installed,
        "unsupported": {"count": len(unsupported), "supported": sorted(supported)},
    }


def disable(
    data: Path, root: Path, harnesses: list[str] | None = None
) -> dict[str, Any]:
    """Remove every integration this feature owns, wherever it installed one.

    What was measured is untouched. Naming no Harness means every Harness the
    Collection Library has an adapter for, whether or not this machine ever
    held our entry there: removal reads the Harness's own file and converges
    it (ADR-0179), so trying one that never carried our entry is a converged
    state rather than an error, and there is no separate on/off flag of this
    feature's own left to update — the Harness's own configuration is the one
    truth capture ever reads.

    Naming Harnesses narrows it to exactly those, the way naming them narrows
    an install. The word accepts `--harness` on either side of the seam, and a
    caller reading the two as symmetric would otherwise lose an integration it
    never named.
    """

    integrations = _integrations()
    supported = set(integrations.SUPPORTED)
    named = list(harnesses or []) or list(integrations.SUPPORTED)
    attempted = [harness for harness in named if harness in supported]
    removed = [integrations.remove(owner(), harness, root) for harness in attempted]
    return {
        "harnesses": removed,
        "unsupported": {
            "count": len(named) - len(attempted),
            "supported": sorted(supported),
        },
    }


def _opencode_session_id(payload: dict[str, Any]) -> str | None:
    """Return the session identity OpenCode's own event envelope carries.

    OpenCode's plugin hands its event object on unmodified (ADR-0179: it
    interprets nothing), and that object never carries the identity where
    Claude Code and Codex do — it nests it inside `properties`, and at a
    different path per event: `session.idle` names it directly as
    `sessionID`, while `session.created` and `session.deleted` embed it in
    the session record at `info.id`.
    """

    properties = payload.get("properties")
    if not isinstance(properties, dict):
        return None
    session_id = properties.get("sessionID")
    if isinstance(session_id, str) and session_id:
        return session_id
    info = properties.get("info")
    if isinstance(info, dict):
        info_id = info.get("id")
        if isinstance(info_id, str) and info_id:
            return info_id
    return None


def _normalized(payload: Any) -> dict[str, Any]:
    """Return one lifecycle payload with a Harness's own envelope unwrapped.

    Claude Code and Codex already hand over a flat payload naming what this
    feature needs directly, under the keys `_clean` allow-lists. OpenCode's
    forwarded event does not, so its session identity is found here once
    rather than by every caller of `_clean` re-deriving OpenCode's own shape.
    """

    if not isinstance(payload, dict):
        return {}
    if isinstance(payload.get("session_id"), str) and payload["session_id"]:
        return payload
    session_id = _opencode_session_id(payload)
    if session_id is None:
        return payload
    return {**payload, "session_id": session_id}


def _clean(payload: Any) -> dict[str, Any]:
    """Return only the allow-listed fields of one lifecycle payload."""

    if not isinstance(payload, dict):
        return {}
    return {key: value for key, value in payload.items() if key in PAYLOAD_ALLOWED}


def _elapsed_seconds(started: Any, completed: Any) -> float:
    """Return the seconds between two instants, or zero where either is unusable."""

    first, last = _parsed(started), _parsed(completed)
    return 0.0 if first is None or last is None else (last - first).total_seconds()


def _lines(path: Path) -> list[dict[str, Any]]:
    """Return every JSON object one JSON-lines file holds, skipping what is not one.

    A session can end mid-write, and a concurrent writer can leave a blank or
    partial line; both are skipped rather than raised, because a finished
    record is read after the fact and never gets a second chance to be whole.
    """

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    parsed: list[dict[str, Any]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            loaded = json.loads(stripped)
        except ValueError:
            continue
        if isinstance(loaded, dict):
            parsed.append(loaded)
    return parsed


def _number(value: Any) -> float | None:
    """Return one usage count as a number, or None where it is not one."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _text_of(content: Any) -> str:
    """Return the plain text of one message body, and nothing structural.

    A body is either a bare string or a list of blocks, and only a `text`
    block carries anything a person wrote. A `tool_result` block is somebody
    else's output and is never read here.
    """

    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    said = [
        block.get("text")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    return "\n".join(part for part in said if isinstance(part, str))


def _excerpt(text: str, limit: int) -> str:
    """Return at most *limit* characters of *text*, with its edges trimmed."""

    return text.strip()[:limit]


def _is_instruction(line: dict[str, Any]) -> bool:
    """Return whether this line is an instruction that begins a Unit.

    A user line begins a Unit exactly where its `origin.kind` is one of
    `INSTRUCTION_ORIGINS` — a person typing, or a peer session messaging this
    one. `isMeta` is not consulted for those two, because a peer's message
    carries it. Every other user line — a background task's report, the
    session continuing itself, a tool result, a command echo, an injected
    reminder, anything carrying no `origin` at all — is absorbed into the
    running Unit, because none of it is an instruction anybody gave.
    """

    if line.get("type") != "user":
        return False
    origin = line.get("origin")
    return isinstance(origin, dict) and origin.get("kind") in INSTRUCTION_ORIGINS


def _reads_only(command: str) -> bool:
    """Return whether one shell command only looked at the machine.

    Segment by segment, because a command is usually a pipeline or a chain and
    the interesting verb is rarely the first word of the whole thing. A
    segment that is a variable assignment carries no verb of its own and is
    passed over; a segment whose head is not a known reader makes the whole
    command a change.
    """

    segments = command.replace("||", "&&").replace(";", "&&").replace("|", "&&")
    heads: list[list[str]] = []
    for segment in segments.split("&&"):
        words = [word for word in segment.split() if "=" not in word.split("/")[0]]
        if words:
            heads.append(words)

    # A call that named no command at all is not a change: an absence is not
    # a reading, and counting it as one would call every unclassifiable tool
    # call substantial work.
    if not heads:
        return True

    return all(
        _head_reads_only(words[0].rsplit("/", 1)[-1], words[1:]) for words in heads
    )


def _head_reads_only(head: str, rest: list[str]) -> bool:
    """Return whether one command's own verb only reads."""

    if head == "git":
        verbs = [word for word in rest if not word.startswith("-")]
        return bool(verbs) and verbs[0] in READING_GIT_VERBS
    return head in READING_HEADS


def _tool_uses(message: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every tool call one assistant message made."""

    content = message.get("content")
    if not isinstance(content, list):
        return []
    return [
        block
        for block in content
        if isinstance(block, dict) and block.get("type") == "tool_use"
    ]


def _command_of(call: dict[str, Any]) -> str:
    """Return the shell command one tool call ran, or an empty string."""

    arguments = call.get("input")
    command = arguments.get("command") if isinstance(arguments, dict) else None
    return command if isinstance(command, str) else ""


def _absorb_assistant(span: _Span, line: dict[str, Any]) -> None:
    """Fold one assistant turn into the span it belongs to.

    The Seat is counted per turn rather than taken from the first or the last
    one, so a Unit that ran mostly on one model and briefly on another is
    attributed to the one that did the work.
    """

    message = line.get("message")
    if not isinstance(message, dict):
        return

    if line.get("isApiErrorMessage") is True:
        span.errored = True

    # The Seat this turn ran on, counted; the model is the message's own and
    # the deliberation control is the line's, which is where Claude Code
    # records the effort a turn was asked for.
    model = message.get("model")
    effort = line.get("effort")
    seat = (
        model if isinstance(model, str) and model else None,
        effort if isinstance(effort, str) and effort else None,
    )
    if seat != (None, None):
        span.seats[seat] = span.seats.get(seat, 0) + 1

    # The token categories the Harness itself counted, summed. A category no
    # turn reported stays None rather than becoming a zero: a zero is a
    # reading and an absence is not.
    usage = message.get("usage")
    usage = usage if isinstance(usage, dict) else {}
    details = usage.get("output_tokens_details")
    details = details if isinstance(details, dict) else {}
    counted = {category: _number(usage.get(key)) for category, key in TOKEN_FIELDS}
    counted["reasoning"] = _number(details.get(REASONING_FIELD))
    for category, value in counted.items():
        if value is not None:
            span.tokens[category] = (span.tokens[category] or 0.0) + value

    # What the turn did, classified and then forgotten: the command string is
    # read here to decide whether the call changed anything and whether it ran
    # tests, and no part of it is kept.
    for call in _tool_uses(message):
        span.tool_calls += 1
        name = call.get("name")
        if name in CHANGING_TOOLS:
            span.changing_tool_calls += 1
            continue
        if name not in SHELL_TOOLS:
            continue
        command = _command_of(call)
        if not _reads_only(command):
            span.changing_tool_calls += 1
        if any(runner in command for runner in TEST_RUNNERS):
            span.tests_ran = True

    said = _text_of(message.get("content"))
    if said.strip():
        span.result = said


def _absorb_user(span: _Span, line: dict[str, Any]) -> None:
    """Fold one tool result or interruption into the span it belongs to.

    A tool result's own error flag is the whole of what is read from it: what
    the tool printed is terminal output and never reaches this module.
    """

    content = (line.get("message") or {}).get("content")
    if INTERRUPTION_MARKER in _text_of(content):
        span.interrupted = True

    result = line.get("toolUseResult")
    if isinstance(result, dict) and result.get("interrupted") is True:
        span.interrupted = True

    if not isinstance(content, list):
        return
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_result":
            continue
        if block.get("is_error") is True and span.tests_ran:
            span.tests_failed = True


def _stamped(line: dict[str, Any]) -> str | None:
    """Return one line's instant, or None where it carries none."""

    instant = line.get("timestamp")
    return instant if isinstance(instant, str) and instant else None


def _spans(lines: list[dict[str, Any]], whole: bool) -> list[_Span]:
    """Split one transcript into spans, one per instruction.

    A subagent's transcript is one span *whole*: it was opened by one
    instruction and everything in it answers that instruction. The main
    transcript is split, each span running from a user instruction to the turn
    before the next one. Which spans become Units is decided after the split —
    the substantial test in `_unit`, and the ten-minute threshold on a Unit of
    the session's own in `units` — so a session that alternates between quick
    questions and long jobs contributes the long jobs alone.
    """

    spans: list[_Span] = []
    current: _Span | None = None
    for line in lines:
        if _is_instruction(line) or (
            whole and current is None and line.get("type") == "user"
        ):
            instruction = _text_of((line.get("message") or {}).get("content"))
            started = _stamped(line) or ""
            current = _Span(
                instruction=_excerpt(instruction, INSTRUCTION_CHARS),
                started_at=started,
                ended_at=started,
            )
            spans.append(current)
            continue
        if current is None:
            continue

        instant = _stamped(line)
        if instant:
            current.ended_at = instant
        if line.get("type") == "assistant":
            _absorb_assistant(current, line)
        elif line.get("type") == "user":
            _absorb_user(current, line)
    return spans


def _seat_of(span: _Span) -> tuple[str | None, str | None]:
    """Return the model and deliberation this span mostly ran on."""

    if not span.seats:
        return None, None
    return max(span.seats.items(), key=lambda entry: entry[1])[0]


def _substantial(span: _Span, seconds: float) -> bool:
    """Return whether this span is work worth measuring at all."""

    output = span.tokens.get("output") or 0.0
    return (
        span.changing_tool_calls >= SUBSTANTIAL_CHANGING_CALLS
        or seconds >= SUBSTANTIAL_SECONDS
        or output >= SUBSTANTIAL_OUTPUT_TOKENS
    )


def _named_attempt(instruction: str) -> str | None:
    """Return the attempt a routed brief named, or None where none did.

    Whoever dispatched a routed builder holds an identity for that attempt
    before the work starts, and files its own verdict under it. A brief that
    opens with that identity lets this read of the same builder's transcript
    file what the attempt spent under the same name, so the store ends with
    one row rather than one graded attempt without a cost beside one costed
    attempt with a weaker grade (issue #291).
    """

    matched = ATTEMPT_LINE.match(instruction.split("\n", 1)[0])
    return matched.group(1) if matched else None


def _unit(span: _Span, session: str, harness: str, delegated: bool) -> Unit | None:
    """Return one span as a Unit, or None where it is not substantial.

    The identity is the attempt the brief named, where a routed builder's
    brief named one, and a span whose instruction names an attempt is
    delegated wherever it was read. Otherwise the identity is the session, the
    Seat and the instant the Unit began, so the same finished session read
    twice yields the same Unit and the measurement store folds the second copy
    into the first rather than counting it twice.

    Only the substantial test is applied here. Whether a Unit of the session's
    own ran long enough to be written is `units`' to decide, once it has
    marked the retries among every substantial Unit (#303).
    """

    seconds = _elapsed_seconds(span.started_at, span.ended_at)
    if not _substantial(span, seconds):
        return None

    model, deliberation = _seat_of(span)
    identity = json.dumps(
        {
            "session": session,
            "model": model,
            "deliberation": deliberation,
            "started_at": span.started_at,
        },
        sort_keys=True,
    )
    named = _named_attempt(span.instruction)
    return Unit(
        unit_id=named or f"unit-{_opaque(identity)}",
        session=session,
        harness=harness,
        started_at=span.started_at,
        ended_at=span.ended_at,
        seconds=seconds,
        model=model,
        deliberation=deliberation,
        tokens=dict(span.tokens),
        tool_calls=span.tool_calls,
        changing_tool_calls=span.changing_tool_calls,
        delegated=delegated or named is not None,
        signals={
            "retried": False,
            "tests_ran": span.tests_ran,
            "tests_passed": span.tests_ran and not span.tests_failed,
            "interrupted": span.interrupted,
            "errored": span.errored,
        },
        instruction_excerpt=span.instruction,
        result_excerpt=_excerpt(span.result, RESULT_CHARS),
    )


def _retried(units: list[Unit]) -> list[Unit]:
    """Mark every Unit a later one in the same session repeated.

    An instruction given twice is the cheapest evidence there is that the
    first answer was not good enough, and it costs nothing to establish.
    """

    seen: dict[str, int] = {}
    for index, unit in enumerate(units):
        key = " ".join(unit.instruction_excerpt.split())
        if not key:
            continue
        earlier = seen.get(key)
        if earlier is not None:
            marked = dict(units[earlier].signals)
            marked["retried"] = True
            units[earlier] = Unit(**{**asdict(units[earlier]), "signals": marked})
        seen[key] = index
    return units


def _readable(harness: Any, transcript_path: Any) -> tuple[Path, str] | None:
    """Return the one record to read and the Harness it came from, or None.

    None where there is nothing to read at all, which is an absence for the
    caller to write no Unit over rather than a raised error (ADR-0179,
    decision 4 as applied to this read): a Harness whose record this module
    cannot split and a payload that named no path are the same answer.
    """

    if not isinstance(harness, str) or harness not in READABLE_HARNESSES:
        return None
    if not isinstance(transcript_path, str) or not transcript_path:
        return None
    return Path(transcript_path), harness


def units(session: str, harness: str | None, transcript_path: Any) -> list[Unit]:
    """Return every Unit one finished session produced that is evidence.

    A Unit is evidence where it is substantial and, unless an instruction
    naming a routed attempt made it delegated, ran for `OWN_UNIT_SECONDS` or
    longer. The retries are marked first, across every substantial Unit, so
    a long job redone as a short one keeps the signal the redo gave it (#303).

    Bounded to exactly the file named by *transcript_path* and nothing else —
    no encoding is derived from a working directory or a session identity, no
    companion directory is walked, and no other session's files are ever
    opened. A subagent of this session is read at its own stop, by
    `subagent_units`, and never here (#294).
    """

    readable = _readable(harness, transcript_path)
    if readable is None:
        return []
    path, known = readable
    marked = _retried(
        [
            unit
            for span in _spans(_lines(path), whole=False)
            if (unit := _unit(span, session, known, delegated=False)) is not None
        ]
    )
    return [
        unit for unit in marked if unit.delegated or unit.seconds >= OWN_UNIT_SECONDS
    ]


def subagent_units(
    session: str, harness: str | None, transcript_path: Any
) -> list[Unit]:
    """Return the Unit one finished subagent produced, under its session's identity.

    The record is one whole Unit: it was opened by one instruction and
    everything in it answers that instruction. What it carries that the
    session's own record cannot is the model and the effort that subagent
    actually ran on — the cleanest available signal that a delegated point did
    or did not do the work it was given.

    The identity is the parent session's, because that is whose work this was;
    the subagent's own name is not an identity and never reaches a Unit.
    Bounded to the one file *transcript_path* names, on the same terms `units`
    is bounded to the one file its own caller named.
    """

    readable = _readable(harness, transcript_path)
    if readable is None:
        return []
    path, known = readable
    return [
        unit
        for span in _spans(_lines(path), whole=True)
        if (unit := _unit(span, session, known, delegated=True)) is not None
    ]


def pending(data: Path) -> list[dict[str, Any]]:
    """Return every Unit still waiting to be graded."""

    path = data / PENDING_FILE
    return _lines(path) if path.exists() else []


def _remember(data: Path, found: list[Unit]) -> dict[str, Any]:
    """Append every Unit the pending store does not already hold.

    A lifecycle signal redelivered after the store was already written adds
    nothing the second time, which is what the Unit's own identity is for.
    """

    held = {str(row.get("unit_id")) for row in pending(data)}
    fresh = [unit for unit in found if unit.unit_id not in held]
    if fresh:
        data.mkdir(parents=True, exist_ok=True)
        with (data / PENDING_FILE).open("a", encoding="utf-8") as store:
            for unit in fresh:
                store.write(json.dumps(asdict(unit), sort_keys=True) + "\n")
    return {
        "recorded": [unit.unit_id for unit in fresh],
        "skipped": [unit.unit_id for unit in found if unit.unit_id in held],
    }


def _finish(
    data: Path, session: str, harness: str | None, transcript_path: Any
) -> dict[str, Any]:
    """Answer one session-ending signal: derive that session's own Units.

    A session that ended abruptly contributes whatever its own record
    establishes and nothing more; nothing here waits for a human. The one
    sibling action this moment carries — grading what is pending — writes
    nothing capture owns, and its every failure is swallowed here exactly as
    this path's own are.
    """

    written = _remember(data, units(session, harness, transcript_path))

    with suppress(Exception):
        _sibling("grade").hook_pass(data)

    return {"ok": True, "fail_open": False, **written}


def _stopped(
    data: Path, session: str, harness: str | None, transcript_path: Any
) -> dict[str, Any]:
    """Answer one subagent's own stop: derive that subagent's Unit.

    One bounded read of one finished record, made at the moment that record is
    finished rather than hours later at a session end the session may never
    reach. It carries no grading pass: buying a judgement is the session's own
    last invocation's to carry, and a session that delegates twenty times must
    not pay for twenty of them.
    """

    return {
        "ok": True,
        "fail_open": False,
        **_remember(data, subagent_units(session, harness, transcript_path)),
    }


def hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal, and never let answering it cost the session.

    This is the synchronous path a Harness runs, so it does bounded local
    metadata I/O and nothing else: no model call, no test run, no repository
    scan, and no long-lived work. Every failure in it is swallowed, because a
    capture that breaks a session is worse than no capture. The one thing a
    session's own last invocation additionally carries — one bounded grading
    pass — is bounded in its own module and reaches a model only from there
    (ADR-0179). Nothing on this path reaches the network at all: the world's
    own facts are read by the catalogue pass, which a person runs, and by the
    agent running `setup` or `update` (ADR-0185, ADR-0191).

    The object returned here is a diagnostic and never a Harness's protocol,
    so the command line writes it to standard error and leaves standard output
    empty: a Harness reads its own hook's standard output as its own protocol
    and refuses an object carrying fields from anywhere else (#259).
    """

    try:
        return _hook(data, event, payload)
    except Exception as exc:  # noqa: BLE001 - the hook path is fail-open by contract
        return {
            "ok": False,
            "fail_open": True,
            "detail": type(exc).__name__,
            "recorded": [],
            "skipped": [],
        }


def _moment(event: str, payload: Any) -> str:
    """Return the lifecycle moment this signal is, from wherever it was named.

    A Harness that interpolates the event into the command it runs says it
    there; Claude Code and Codex instead hand the whole event over on stdin, so
    an installed hook that took only the command line would answer every moment
    as if it were none of them.
    """

    if event:
        return event
    if not isinstance(payload, dict):
        return ""
    for name in EVENT_FIELDS:
        named = payload.get(name)
        if isinstance(named, str) and named:
            return named
    return ""


def _idle() -> dict[str, Any]:
    """Return the answer for a moment this feature does no work at.

    A moment it no longer asks any Harness for and a payload naming no session
    are answered the same way: nothing recorded, and nothing charged to the
    session that carried it (#294).
    """

    return {"ok": True, "fail_open": False, "recorded": [], "skipped": []}


def _hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal.

    There is no separate on/off state of this feature's own to check any
    more (#223): a hook only ever runs because a Harness's own configuration
    names it, which only happens once this Skill's integration has been
    installed, so answering the signal is the whole of the work.
    """

    event = _moment(event, payload)
    clean = _clean(_normalized(payload))
    session = clean.get("session_id")
    if not session:
        return _idle()

    identity = _opaque(session)
    harness = clean.get("harness")

    if event in END_EVENTS or event in ERROR_EVENTS:
        return _finish(data, identity, harness, clean.get("transcript_path"))
    if event in SUBAGENT_EVENTS:
        return _stopped(data, identity, harness, clean.get(SUBAGENT_TRANSCRIPT_FIELD))

    # Every other moment is one this feature no longer asks for. A stale entry
    # on a machine the Manager has not reconverged still fires, and is answered
    # with no work rather than with a traceback.
    return _idle()


def _storage(data: Path) -> int:
    """Return how many bytes the `capture/` directory still holds.

    Nothing writes it any more (#294), so this is the size of what an earlier
    design left rather than of a store anything is filling.
    """

    if not home(data).exists():
        return 0
    return sum(path.stat().st_size for path in home(data).rglob("*") if path.is_file())


def _grader_ran_at(data: Path) -> str | None:
    """Return when the grader last completed a pass, or None where it never has."""

    path = data / GRADER_STATE_FILE
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(state, dict):
        return None
    last = state.get("last_run_at")
    return last if isinstance(last, str) and last else None


def _stamp(instant: datetime) -> str:
    """Return one instant in the form every stored timestamp is written in."""

    return instant.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _oldest_waiting(data: Path) -> datetime | None:
    """Return when the Unit that has waited longest finished, or None.

    The smallest readable `ended_at` rather than the first row in the file,
    and a row with no readable finish is passed over rather than guessed at.
    """

    finished = [
        at if at.tzinfo else at.replace(tzinfo=UTC)
        for row in pending(data)
        if (at := _parsed(row.get("ended_at"))) is not None
    ]
    return min(finished, default=None)


def status(data: Path, root: Path, now: datetime | None = None) -> dict[str, Any]:
    """Report capture's own state, without a network request or an evaluation.

    Every Harness the Collection Library has an adapter for is reported,
    whether or not this machine happens to hold our entry there right now —
    there is no separate configuration of this feature's own left to consult
    (#223): the Harness's own file is read fresh, exactly as `install` and
    `remove` already read it (ADR-0179). Each one's health is reported beside
    whether its finished session record can be split into Units at all: a
    pending store that stays empty because a Harness keeps no readable record
    is something to say plainly here, never something left for the user to
    discover from the store itself.

    The pending count and the grader's last pass are reported here and nowhere
    else, because a measurement reminder placed where the model reads it
    changes the thing being measured. So is the judge's daily cap, worked out
    at *now* by the grader's own `judge_cap` rather than read off the last
    pass, whose `capped` a session end's free half always writes false: a
    queue at its cap every day falls further behind every day, and says so
    here with when the cap frees and when the oldest waiting Unit finished.
    `now` is reported beside them, the instant both were read at.
    """

    instant = now or datetime.now(UTC)
    cap = _sibling("grade").judge_cap(data, instant)
    oldest = _oldest_waiting(data)
    integrations = _integrations()
    return {
        "harnesses": [
            {
                **integrations.health(
                    owner(), harness, root, events=WANTED_EVENTS.get(harness)
                ),
                "measurements": harness in READABLE_HARNESSES,
            }
            for harness in integrations.SUPPORTED
        ],
        "storage_bytes": _storage(data),
        "pending": len(pending(data)),
        "pending_failures": _pending_failures(data),
        "grader_last_ran_at": _grader_ran_at(data),
        "now": _stamp(instant),
        "judge_capped": cap.capped,
        "judge_frees_at": _stamp(cap.frees_at) if cap.frees_at else None,
        "judged_in_window": cap.in_window,
        "oldest_waiting_at": _stamp(oldest) if oldest else None,
        "retired": len(retired(data)),
    }


def _pending_failures(data: Path) -> dict[str, int]:
    """Return how many pending Units last failed for each named reason.

    A queue reported as one number looks the same whether it is waiting for
    the next pass or whether nothing on this machine can reach a judge at all.
    A Unit no pass has tried yet carries no reason and is counted in neither.
    """

    counted: dict[str, int] = {}
    for row in pending(data):
        why = row.get("last_failure")
        if isinstance(why, str) and why:
            counted[why] = counted.get(why, 0) + 1
    return dict(sorted(counted.items()))


def retired(data: Path) -> list[Path]:
    """Return the files of the retired design this directory still holds.

    Reported by `status` as well as removed by a purge, because a tidying
    nobody is told about is a verb nobody runs.
    """

    named = [data / name for name in RETIRED_FILES]
    return sorted(
        path for path in named + list(data.glob(RETIRED_PATTERN)) if path.is_file()
    )


def _row_count(path: Path) -> int:
    """Return how many non-blank JSONL lines one file holds."""

    return sum(
        1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    )


def purge_paths(data: Path) -> list[dict[str, Any]]:
    """Return what this feature owns beyond the ledger, present or not.

    This is the preview a reset renders before it removes the whole `capture/`
    subdirectory and the pending Units beside it, keeping the Harness hooks
    installed (issue #227). `capture/` is a directory rather than a JSONL file,
    so it is sized in bytes; the pending store is JSONL, sized in rows.

    `capture/` is itself one of the things an earlier design left: it held a
    per-session draft written at every start and every turn, and nothing
    writes it any more (#294). It is named first because it is a directory
    removed whole, while `RETIRED_FILES` is a list of files; what a reset does
    with the two is the same.

    The retired design's leftovers come last and are sized in bytes, being
    files rather than stores anything counts rows in.
    """

    directory = home(data)
    waiting = data / PENDING_FILE
    entries: list[dict[str, Any]] = []
    if directory.exists():
        entries.append(
            {
                "path": str(directory),
                "present": True,
                "unit": "bytes",
                "count": _storage(data),
            }
        )
    else:
        entries.append({"path": str(directory), "present": False})
    if waiting.exists():
        entries.append(
            {
                "path": str(waiting),
                "present": True,
                "unit": "rows",
                "count": _row_count(waiting),
            }
        )
    else:
        entries.append({"path": str(waiting), "present": False})

    # The retired design's leftovers, each named whether or not it is here, so
    # that a preview says what a reset will actually take.
    left = {path.name for path in retired(data)}
    entries += [
        {"path": str(data / name), "present": True, "unit": "bytes", "count": size}
        if (size := _size(data / name)) is not None
        else {"path": str(data / name), "present": False}
        for name in sorted(set(RETIRED_FILES) | left)
    ]

    return entries


def _size(path: Path) -> int | None:
    """Return how many bytes one file holds, or None where it is not there."""

    try:
        return path.stat().st_size
    except OSError:
        return None


def purge(data: Path) -> list[dict[str, Any]]:
    """Remove everything this feature owns beyond the ledger, and report it.

    The Harness hooks stay installed, since this verb never touches them and
    there is no on/off flag of this feature's own for a purge to clear any
    more (#223): a session that starts after a purge is captured exactly as
    one before it was, into the pending store this verb has just emptied.

    `capture/` goes whole and stays gone, nothing writes it any more (#294),
    and the retired design's other leftovers go with it. Those are not this
    feature's own, but discarding the store is the one moment somebody has
    said they want the directory cleared of what nothing reads.
    """

    report = purge_paths(data)
    shutil.rmtree(home(data), ignore_errors=True)
    (data / PENDING_FILE).unlink(missing_ok=True)
    for path in retired(data):
        path.unlink(missing_ok=True)
    return report


def _hook_command(supplied: list[str], data: Path) -> list[str]:
    """Return the command a Harness runs for a lifecycle event.

    The data directory travels inside it. A hook installed for one directory
    and run against another writes its Units where nobody looks for them.
    """

    command = list(supplied) or ["uv", "run", str(Path(__file__).resolve()), "hook"]
    if data.resolve() != default_data().resolve() and "--data" not in command:
        command += ["--data", str(data)]
    return command


def default_data() -> Path:
    """Return the data directory this Skill keeps its evidence in by default."""

    return Path.home() / ".kntnt" / "model-selector"


def install_integrations(harnesses: list[str]) -> dict[str, Any]:
    """Install this feature's owned integration, resolving its own data and root.

    This is the mirror of `remove_integrations`, the other word the Manager
    says at the seams that place or refresh an Enabled Skill's files (#223):
    it resolves this Skill's own default data directory and Harness root
    itself, because the Manager asking for it must not have to know where
    this Skill keeps its evidence (ADR-0179), exactly as removal already
    does for the opposite word.
    """

    return install(default_data(), Path.home(), harnesses, [])


def remove_integrations(harnesses: list[str]) -> dict[str, Any]:
    """Remove every integration this feature owns, wherever it installed one.

    This is the word the Manager says when the Skill is being made Disabled in
    the Global layer, withdrawn from it, or uninstalled: the Project layer is
    never removing what it never installed, so the Manager's own gate is what
    keeps this from clearing a Global Enable's entries from inside a working
    directory. It runs while these files still exist, takes the hooks out of
    every Harness, and leaves what was measured alone. It is answerable at any
    time, because removing what is already gone is a state rather than an
    error.

    Naming Harnesses narrows it to those, exactly as it narrows the mirror
    word; the Manager names none, which is every Harness and is what it
    relies on. The list is carried down to `disable`, which is where the
    Harnesses are actually iterated.
    """

    data = default_data()
    result = disable(data, Path.home(), harnesses)
    return {
        "removed": result["harnesses"],
        "unsupported": result["unsupported"],
        "measurements_preserved": True,
    }


def _emit(payload: dict[str, Any], stream: TextIO | None = None) -> None:
    """Print one machine-readable answer, on *stream* or on standard output.

    A Harness that runs a hook it owns reads what that hook writes on standard
    output as its own protocol, so `hook` — the one action a Harness ever runs
    — hands standard error in here and leaves that channel empty (#259). Every
    other action answers where it always has, because the Manager's two
    integration words and this Skill's own two report verbs are read from
    standard output by whatever asked for them.

    The stream is resolved at call time rather than bound as a default, so a
    caller that replaced the process's own streams is answered on the ones it
    installed.
    """

    target = sys.stdout if stream is None else stream
    json.dump(payload, target, indent=2, sort_keys=True)
    target.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse one capture invocation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=(
            "install-integrations",
            "remove-integrations",
            "hook",
            "status",
            "purge",
        ),
    )

    # Every action but the Manager's own two — install and remove — is
    # invoked by this Skill, which resolves the data directory itself; the
    # Manager's two are invoked by something that must not have to know
    # where this Skill keeps its evidence.
    parser.add_argument("--data", default=str(default_data()))
    parser.add_argument("--root", default=str(Path.home()))
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--event", default="")
    parser.add_argument("--owner", default=owner())

    # `--yes` gates only `purge`'s write: a preview without it is a success,
    # never a refusal.
    parser.add_argument("--yes", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one capture action."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = Path(args.data)
    root = Path(args.root)

    # The hook is the only action a Harness runs, and it is fail-open whatever
    # reaches it — including a payload that is not JSON at all. Its answer goes
    # to standard error, because the channel it would otherwise print on is the
    # one the Harness reads back as its own protocol (#259).
    if args.action == "hook":
        try:
            payload = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            payload = {}
        named = args.harness[0] if args.harness else None
        if named and isinstance(payload, dict) and not payload.get("harness"):
            payload["harness"] = named
        _emit(hook(data, args.event, payload), sys.stderr)
        return 0

    if args.action == "remove-integrations":
        _emit(remove_integrations(args.harness))
    elif args.action == "install-integrations":
        _emit(install_integrations(args.harness))
    elif args.action == "purge":
        _emit(
            {
                "schema_version": SCHEMA_VERSION,
                "verb": "purge",
                "confirmed": args.yes,
                "data": str(data),
                "paths": purge(data) if args.yes else purge_paths(data),
            }
        )
    else:
        _emit(status(data, root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
