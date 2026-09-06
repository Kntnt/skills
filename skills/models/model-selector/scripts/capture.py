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
or by another agent — to the moment it hands control back. Only a substantial
Unit is ever written, so a session of quick questions and answers leaves no
trace at all. On Claude Code the finished session's own record splits cleanly
into Units: the companion `subagents/` directory is one Unit per subagent,
each carrying the model and effort that subagent actually ran on, and the main
transcript is one Unit per user instruction.

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
`EXCERPT_CHARS`, and are removed from the pending store the moment that Unit
becomes a measurement.
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
TURN_EVENTS = frozenset({"Stop", "stop", "SubagentStop", "session.idle"})
ERROR_EVENTS = frozenset({"session.error"})
END_EVENTS = frozenset({"SessionEnd", "sessionEnd", "session.deleted"})

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
# `transcript_path` is locate-only (#225): it is read at a session's end to
# open that session's own finished record, and it never reaches a draft
# written to disk or a Unit — `_hook` reads it locally out of the cleaned
# payload and passes it straight to `_finish` without ever folding it into the
# draft this set's other fields build up.
PAYLOAD_ALLOWED = frozenset(
    {
        "session_id",
        "harness",
        "harness_inventory_revision",
        "transcript_path",
    }
)

# Where the pending Units wait for the grader, beside the measurement ledger
# under the selected data directory, and where the grader records that it ran.
# Named once here rather than left for a consumer to infer.
PENDING_FILE = "pending.jsonl"

# What the design this Skill replaced left behind in a data directory. Nothing
# reads any of them and nothing writes them any more: they are the stored
# configuration, the standing policy, the frozen snapshots and the two ledgers
# of a router that no longer exists. Named here because a verb that does not
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

# The subdirectory beside a Claude Code transcript that holds one transcript
# per subagent, and the name each of those answers to. Neither is derived from
# anything but the transcript path the payload already handed over.
SUBAGENTS_DIRNAME = "subagents"
SUBAGENT_GLOB = "agent-*.jsonl"

# The line a routed builder brief opens with, naming the attempt whoever
# dispatched it already decided. Where a subagent's first user message opens
# with it, that attempt is this Unit's identity rather than the hash below:
# the caller that dispatched the work files its own verdict under the same
# name, and one build filed from two sides is one row rather than two
# (issue #291). Matched on the first line only, and never on a main-session
# instruction — a person at a keyboard is nobody's routed attempt. The same
# form is stated for the tests in `tests/support/model_routing.py`, a shipped
# script having no business importing a test file. The backticks are optional
# because a brief is Markdown and a filler may leave the placeholder's own.
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
# session of quick questions and answers out of the measurement entirely.
SUBSTANTIAL_CHANGING_CALLS = 3
SUBSTANTIAL_SECONDS = 60.0
SUBSTANTIAL_OUTPUT_TOKENS = 4000.0

# How much of an instruction and of a result the grader is given. They are the
# only free text a Unit carries, they exist to be read by one cheap model
# once, and they are gone from the store the moment that Unit is graded.
EXCERPT_CHARS = 800

# The tools that change something by definition, whatever their arguments.
CHANGING_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})

# The tools that run a shell command, whose arguments decide whether the call
# changed anything. The command string is classified here and discarded here:
# no part of it reaches a draft, a Unit, or a measurement.
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


def _now() -> str:
    """Return this instant, as a Unit writes instants."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


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
    """Return the capture home inside one data directory."""

    return data / "capture"


def _drafts(data: Path) -> Path:
    """Return where per-session drafts are kept."""

    return home(data) / "drafts"


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
        integrations.install(owner(), harness, root, runs) for harness in attempted
    ]
    return {
        "installed": installed,
        "unsupported": {"count": len(unsupported), "supported": sorted(supported)},
    }


def disable(data: Path, root: Path) -> dict[str, Any]:
    """Remove every integration this feature owns, wherever it installed one.

    What was measured is untouched. Every Harness the Collection Library has
    an adapter for is attempted, whether or not this machine ever held our
    entry there: removal reads the Harness's own file and converges it
    (ADR-0179), so trying one that never carried our entry is a converged
    state rather than an error, and there is no separate on/off flag of this
    feature's own left to update — the Harness's own configuration is the one
    truth capture ever reads.
    """

    integrations = _integrations()
    removed = [
        integrations.remove(owner(), harness, root)
        for harness in integrations.SUPPORTED
    ]
    return {"harnesses": removed}


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


def _draft_path(data: Path, session: str) -> Path:
    """Return where one session's draft is kept."""

    return _drafts(data) / f"{_opaque(session)}.json"


def _draft(data: Path, session: str) -> dict[str, Any] | None:
    """Return one session's draft, or None where there is none to read."""

    path = _draft_path(data, session)
    if not path.exists():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def _store(path: Path, record: dict[str, Any]) -> None:
    """Write one capture record, creating the directories it needs."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


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


def _excerpt(text: str) -> str:
    """Return at most `EXCERPT_CHARS` of *text*, with its edges trimmed."""

    return text.strip()[:EXCERPT_CHARS]


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
    before the next one, so a session that alternates between quick questions
    and long jobs contributes the long jobs alone.
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
                instruction=_excerpt(instruction), started_at=started, ended_at=started
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
    brief named one. Otherwise it is the session, the Seat and the instant the
    Unit began, so the same finished session read twice yields the same Unit
    and the measurement store folds the second copy into the first rather than
    counting it twice.
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
    named = _named_attempt(span.instruction) if delegated else None
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
        delegated=delegated,
        signals={
            "retried": False,
            "tests_ran": span.tests_ran,
            "tests_passed": span.tests_ran and not span.tests_failed,
            "interrupted": span.interrupted,
            "errored": span.errored,
        },
        instruction_excerpt=span.instruction,
        result_excerpt=_excerpt(span.result),
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


def units(session: str, harness: str | None, transcript_path: Any) -> list[Unit]:
    """Return every substantial Unit one finished session produced.

    Bounded to exactly the session named by *transcript_path*: that file, and
    its own companion subagent directory beside it, and nothing else — no
    encoding is derived from a working directory or a session identity, and no
    other session's files are ever opened.

    Returns nothing where the Harness keeps no record this module can split,
    where no usable path was handed over, or where nothing in it could be read
    at all. That is an absence for the caller to write no Unit over, never a
    raised error (ADR-0179, decision 4 as applied to this read).
    """

    if harness not in READABLE_HARNESSES:
        return []
    if not isinstance(transcript_path, str) or not transcript_path:
        return []

    path = Path(transcript_path)
    found = [
        unit
        for span in _spans(_lines(path), whole=False)
        if (unit := _unit(span, session, harness, delegated=False)) is not None
    ]

    # Each subagent transcript is one Unit of its own, carrying the model and
    # the effort that subagent actually ran on — the cleanest available signal
    # that a delegated point did or did not do the work it was given.
    subagents = path.with_suffix("") / SUBAGENTS_DIRNAME
    if subagents.is_dir():
        for transcript in sorted(subagents.glob(SUBAGENT_GLOB)):
            found += [
                unit
                for span in _spans(_lines(transcript), whole=True)
                if (unit := _unit(span, session, harness, delegated=True)) is not None
            ]

    return _retried(found)


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
    data: Path, draft: dict[str, Any], harness: str | None, transcript_path: Any
) -> dict[str, Any]:
    """Answer one session-ending signal: derive its Units and forget the draft.

    A session that ended abruptly contributes whatever its own record
    establishes and nothing more; nothing here waits for a human. The two
    sibling actions this moment carries — grading what is pending, and
    refreshing this Skill's own public sources — write nothing capture owns,
    and their every failure is swallowed here exactly as this path's own are.
    """

    written = _remember(
        data, units(draft["session_identity"], harness, transcript_path)
    )
    _draft_path(data, draft["session_key"]).unlink(missing_ok=True)

    with suppress(Exception):
        _sibling("grade").hook_pass(data)
    with suppress(Exception):
        _sibling("refresh").refresh(data)

    return {"ok": True, "fail_open": False, **written}


def hook(data: Path, event: str, payload: Any) -> dict[str, Any]:
    """Answer one lifecycle signal, and never let answering it cost the session.

    This is the synchronous path a Harness runs, so it does bounded local
    metadata I/O and nothing else: no model call, no test run, no repository
    scan, and no long-lived work. Every failure in it is swallowed, because a
    capture that breaks a session is worse than no capture. The two things a
    session's own last invocation additionally carries — one bounded grading
    pass and this Skill's unattended source refresh — are bounded in their own
    modules and reach a model or the network only from there (ADR-0179).

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
    """Return the answer for a signal that neither opens nor closes a session."""

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

    held = _draft(data, session) or {
        "schema_version": SCHEMA_VERSION,
        "session_key": session,
        "session_identity": _opaque(session),
        "harness": clean.get("harness"),
        "harness_inventory_revision": clean.get("harness_inventory_revision"),
    }
    draft = {**held, "session_key": session, "updated_at": _now()}

    if event in END_EVENTS or event in ERROR_EVENTS:
        return _finish(
            data,
            draft,
            clean.get("harness") or draft.get("harness"),
            clean.get("transcript_path"),
        )

    # A start or a turn is a draft update and nothing more.
    _store(_draft_path(data, session), draft)
    return _idle()


def _storage(data: Path) -> int:
    """Return how many bytes the capture store is using right now."""

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


def status(data: Path, root: Path) -> dict[str, Any]:
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
    changes the thing being measured.
    """

    integrations = _integrations()
    return {
        "harnesses": [
            {
                **integrations.health(owner(), harness, root),
                "measurements": harness in READABLE_HARNESSES,
            }
            for harness in integrations.SUPPORTED
        ],
        "storage_bytes": _storage(data),
        "pending": len(pending(data)),
        "grader_last_ran_at": _grader_ran_at(data),
        "retired": len(retired(data)),
    }


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
    subdirectory — drafts and all — and the pending Units beside it, keeping
    the Harness hooks installed (issue #227). `capture/` is a directory rather
    than a JSONL file, so it is sized in bytes; the pending store is JSONL,
    sized in rows.

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
    one before it was, into a `capture/` this verb's own removal recreates.

    The retired design's leftovers go with it. They are not this feature's
    own, but discarding the store is the one moment somebody has said they
    want the directory cleared of what nothing reads.
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
    and run against another writes its drafts and Units where nobody looks
    for them.
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


def remove_integrations() -> dict[str, Any]:
    """Remove every integration this feature owns, wherever it installed one.

    This is the word the Manager says when the Skill is being made Disabled in
    the Global layer, withdrawn from it, or uninstalled: the Project layer is
    never removing what it never installed, so the Manager's own gate is what
    keeps this from clearing a Global Enable's entries from inside a working
    directory. It runs while these files still exist, takes the hooks out of
    every Harness, and leaves what was measured alone. It is answerable at any
    time, because removing what is already gone is a state rather than an
    error.
    """

    data = default_data()
    result = disable(data, Path.home())
    return {"removed": result["harnesses"], "measurements_preserved": True}


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
        _emit(remove_integrations())
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
