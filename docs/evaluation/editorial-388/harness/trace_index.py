# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Reconstruct who ran what, from the transcripts one evidence packet preserved.

An evaluator judging `T1` and `R2` has to answer two questions the delivered
text cannot answer: which files a run actually loaded, and in what order it
corrected, re-reviewed and closed with the installed Proofread pass. Claude
Code records both — every tool call with its arguments in the session's own
transcript, and every subagent in a transcript of its own beside a `.meta.json`
naming the call that started it — and this module turns that record into one
index an evaluator reads instead of walking JSON lines by hand.

Two things it deliberately does not do. It judges no criterion: it says what
was recorded and leaves `pass` or `fail` to whoever reads it. And it takes no
statement from the run's own reply — a run that says it started a correction
agent and closed with Proofread has claimed it, and the claim is not evidence.
The completeness status below is computed from the transcripts and the runner's
own outcome alone, so a packet whose reply reads like a success and whose trace
is missing a child is `incomplete`.

Read as evidence, an entry says how it was established. A path in a `Read`
argument is the Harness's own record that the file was opened. A path inside a
shell command is the command the run submitted, which is weaker: it establishes
what was asked for rather than what arrived, and a command carrying a glob or a
recursive search names a set rather than a file, which is what `exact` says.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

# Where a packet keeps what this module reads. The runner writes them and an
# evaluator may re-run this module over a saved packet years later, so the
# layout is stated here rather than passed in.
PARENT_TRANSCRIPT = Path("transcripts") / "parent.jsonl"
SUBAGENTS = Path("transcripts") / "subagents"
RESULT_FILE = "result.json"
INDEX_FILE = "trace-index.json"
STATUS_FILE = "trace-status.json"

# The tools that name one file in one argument, and the argument each names it
# in. A call to one of these is the Harness's own record that the path was
# opened, which is the strongest evidence of loading a trace carries.
FILE_ARGUMENTS: dict[str, tuple[str, str]] = {
    "Read": ("file_path", "read"),
    "Edit": ("file_path", "write"),
    "Write": ("file_path", "write"),
    "NotebookEdit": ("notebook_path", "write"),
}

# The tools that name a set of files rather than one. What they establish is
# that the run looked in a directory, never that it read any file under it.
SEARCH_ARGUMENTS: dict[str, str] = {"Glob": "path", "Grep": "path"}

# What a shell command runs through, and what starts a subagent. Claude Code
# 2.1.278 names the delegation tool `Agent`; `Task` is the same tool under the
# name older records carry, and both are read so that a packet kept from an
# earlier version still indexes.
SHELL_TOOLS = frozenset({"Bash"})
DELEGATION_TOOLS = frozenset({"Agent", "Task"})

# What makes a whole shell command name a set rather than the files it lists: a
# command whose job is to walk a tree, or a flag that makes one do so. The trace
# then records the request and not the files it reached.
WALKING_COMMANDS = frozenset({"find", "grep", "rg", "ag", "fd", "tree", "ls"})
RECURSIVE_FLAGS = frozenset({"-r", "-R", "-rn", "-rl", "--recursive"})

# What makes one token stand for something other than the path it spells: a
# glob the shell expands at run time, or a variable only the run knew the value
# of. The path is recorded as written, and `exact` says it was not resolved.
UNRESOLVED_CHARACTERS = ("*", "?", "[", "$")

# A token is a path where it carries a separator or reads as a filename with an
# extension. Everything else on a command line — a flag, a `1,40p`, a pattern —
# is left out, because a mention that is not a path is not evidence of a read.
# A leading `NAME=` is an assignment rather than part of the path it assigns.
FILENAME = re.compile(r"^[\w.@+-]+\.[A-Za-z0-9]{1,6}$")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
REDIRECTION = re.compile(r"^\d*[<>]")
PUNCTUATION = "'\"();,&|"

# A shell variable, and how deep a chain of them is followed. A run writes the
# staged installation's path into one and then reads every reference through
# it, so a token left unexpanded would report a whole contract's loading as
# unresolved. Only assignments the same command makes are followed, which is a
# substitution of what the shell itself would have substituted; the command
# stays verbatim beside the entry either way.
VARIABLE = re.compile(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?")
EXPANSION_ROUNDS = 3

# What a variable's value may not carry for the substitution to be made: output
# only the run itself had. Expanding one of these would print a path that never
# existed, where leaving the variable written says exactly what is unknown.
SUBSTITUTIONS = ("$(", "`")

# What separates one command from the next inside one submitted string. A
# trailing `;` attaches to the word before it and is handled beside these.
SEPARATORS = frozenset({"&&", "||", "|", "&", ";"})

# A `mktemp` template: the run named a shape and the system named the file, so
# the token stands for a path nobody wrote, exactly as an unresolved variable
# does.
TEMPLATE = "XXX"

# Markdown inside a command — a link, a reference — carries a separator and is
# not a path. It arrives where a run greps a text for one of its own sentences.
MARKDOWN = "]("

# Where a command stops naming files and starts carrying a document. A run
# writes a draft, a report or an artifact through a heredoc, and every sentence
# of it would otherwise be lexed for paths; the line opening the heredoc names
# the file being written and is kept, and the body up to the marker is dropped.
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(?P<marker>[A-Za-z_]\w*)\1")

# Where Claude Code puts a Skill's own body when a Formal Invocation loads it.
# The line is the Harness's record of which installation answered the
# invocation, which is what `T1` asks about the Skill's own files.
SKILL_BODY_PREFIX = "Base directory for this skill:"

# How much of a tool result the index repeats. The whole of it is in the
# preserved transcript beside the index; this is the excerpt that makes the
# index readable on its own, and `result_chars` says what was left out.
RESULT_EXCERPT_CHARS = 400


@dataclass(frozen=True)
class Touch:
    """One file the trace records a run touching, and how that was established.

    `established_from` says which kind of record it is — a tool's own argument
    or a command the run submitted — and `exact` whether it stands for that one
    file or for whatever a glob, a variable, a template or a walk settles.
    """

    ordinal: int
    at: str | None
    tool: str
    path: str
    access: str
    established_from: str
    exact: bool
    command: str | None


def _loaded(path: Path) -> dict[str, Any]:
    """Return one JSON object a packet holds, and an empty mapping where it has none.

    A packet is read after the fact, so a file of it can be absent, truncated by
    the run that was writing it, or something other than an object. Each is a
    thing this module reports around rather than raises on.
    """

    try:
        found = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def _lines(path: Path) -> tuple[list[dict[str, Any]], int]:
    """Return every JSON object one transcript holds, and how many lines failed.

    A run killed mid-write leaves a partial last line. It is counted rather
    than raised, because an incomplete trace is a thing this module reports and
    never a thing it refuses to read.
    """

    if not path.is_file():
        return [], 0

    parsed: list[dict[str, Any]] = []
    unparsable = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            loaded = json.loads(stripped)
        except ValueError:
            unparsable += 1
            continue
        if isinstance(loaded, dict):
            parsed.append(loaded)
            continue
        unparsable += 1
    return parsed, unparsable


def _text_of(content: Any) -> str:
    """Return the plain text of one message body, blocks folded in order."""

    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "".join(
        block.get("text", "")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    )


def _blocks(line: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    """Return one line's content blocks of *kind*, in the order it carries them."""

    content = (line.get("message") or {}).get("content")
    if not isinstance(content, list):
        return []
    return [
        block
        for block in content
        if isinstance(block, dict) and block.get("type") == kind
    ]


def _arguments(call: dict[str, Any]) -> dict[str, Any]:
    """Return one tool call's arguments, and an empty mapping where it has none."""

    supplied = call.get("input")
    return supplied if isinstance(supplied, dict) else {}


def _without_heredocs(command: str) -> str:
    """Return one command with every heredoc body removed, the openings kept."""

    kept: list[str] = []
    marker: str | None = None
    for line in command.split("\n"):
        if marker is not None:
            marker = None if line.strip() == marker else marker
            continue
        kept.append(line)
        opening = HEREDOC.search(line)
        if opening:
            marker = opening.group("marker")
    return "\n".join(kept)


def _tokens(command: str) -> list[str]:
    """Return one shell command's words, falling back on whitespace.

    A command this module cannot lex — an unbalanced quote, a heredoc — still
    carries paths worth naming, so the crude split answers rather than nothing.
    """

    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def _segments(command: str) -> list[list[str]]:
    """Return one command's words, split at each point where a new command starts.

    A command is rarely one command: `cat one.md && find . -name '*.md'` reads a
    file and walks a tree, and judging the whole of it either way would credit
    the walk to the file or the file to the walk. Lexing first and splitting on
    the operator *tokens* keeps a separator inside a quoted argument out of it.
    """

    found: list[list[str]] = []
    for line in command.split("\n"):
        current: list[str] = []
        for word in _tokens(line):
            if word in SEPARATORS:
                found.append(current)
                current = []
                continue
            trailing = word.endswith(";")
            current.append(word.rstrip(";") if trailing else word)
            if trailing:
                found.append(current)
                current = []
        found.append(current)
    return [segment for segment in found if segment]


def _names_a_set(words: list[str]) -> bool:
    """Whether one command names a set of files rather than the files it lists."""

    if not words:
        return False
    if Path(words[0]).name in WALKING_COMMANDS:
        return True
    return any(word in RECURSIVE_FLAGS for word in words)


def _expanded(text: str, values: dict[str, str]) -> str:
    """Substitute the variables *values* settles, leaving the others written."""

    return VARIABLE.sub(lambda found: values.get(found.group(1), found.group(0)), text)


def _assignments(words: list[str]) -> dict[str, str]:
    """Return what one command's own assignments settle, chains followed."""

    values: dict[str, str] = {}
    for word in words:
        assigned = ASSIGNMENT.match(word.strip(PUNCTUATION))
        if assigned:
            values[assigned.group(0)[:-1]] = word.strip(PUNCTUATION)[assigned.end() :]

    for _ in range(EXPANSION_ROUNDS):
        values = {name: _expanded(value, values) for name, value in values.items()}
    return {
        name: value
        for name, value in values.items()
        if not any(opening in value for opening in SUBSTITUTIONS)
    }


def _paths_in(command: str) -> list[tuple[str, bool]]:
    """Return each path a shell command names, with whether that segment walks.

    The assignments of every segment carry forward — a run settles `$LIB` on one
    line and reads through it on the next — while whether a set was named is
    asked of the segment the path stands in and of no other.
    """

    values: dict[str, str] = {}
    found: list[tuple[str, bool]] = []
    for words in _segments(_without_heredocs(command)):
        values.update(_assignments(words))
        walks = _names_a_set(words)
        for word in words:
            stripped = word.strip(PUNCTUATION)
            candidate = _expanded(ASSIGNMENT.sub("", stripped), values)
            if candidate.startswith("-") or REDIRECTION.match(candidate):
                continue
            if MARKDOWN in candidate:
                continue
            if "/" in candidate or FILENAME.match(candidate):
                found.append((candidate, walks))
    return found


def _activity(
    ordinal: int, at: str | None, call: dict[str, Any]
) -> list[dict[str, Any]]:
    """Return what one tool call establishes about the files a run touched."""

    tool = call.get("name")
    arguments = _arguments(call)

    # A tool that names one file in one argument establishes that file exactly.
    if tool in FILE_ARGUMENTS:
        argument, access = FILE_ARGUMENTS[tool]
        path = arguments.get(argument)
        if not isinstance(path, str) or not path:
            return []
        return [_touch(ordinal, at, tool, path, access, "tool-argument", True)]

    # A search names where it looked, which is a set whatever it found.
    if tool in SEARCH_ARGUMENTS:
        path = arguments.get(SEARCH_ARGUMENTS[tool]) or "."
        return [_touch(ordinal, at, tool, path, "search", "tool-argument", False)]

    # A shell command establishes what was submitted; `exact` says how far. One
    # command naming the same path several times touched it once.
    if tool in SHELL_TOOLS:
        command = arguments.get("command")
        if not isinstance(command, str) or not command:
            return []
        seen: dict[str, bool] = {}
        for path, walks in _paths_in(command):
            seen.setdefault(path, not walks and _resolved(path))
        return [
            _touch(ordinal, at, tool, path, "shell", "shell-command", exact, command)
            for path, exact in seen.items()
        ]

    return []


def _touch(
    ordinal: int,
    at: str | None,
    tool: str,
    path: str,
    access: str,
    established_from: str,
    exact: bool,
    command: str | None = None,
) -> dict[str, Any]:
    """One `Touch`, as the mapping the index is written out of."""

    return asdict(
        Touch(ordinal, at, tool, path, access, established_from, exact, command)
    )


def _resolved(path: str) -> bool:
    """Whether a path stands for itself rather than for whatever settles it."""

    if any(character in path for character in UNRESOLVED_CHARACTERS):
        return False
    return TEMPLATE not in path


def _walk(lines: list[dict[str, Any]]) -> dict[str, Any]:
    """Fold one agent's transcript into its instruction, seats, calls and effects.

    The first user line is the instruction the agent was given, which for the
    session is the Formal Invocation as it was typed and for a subagent is the
    prompt the call that started it carried. A Skill body arrives as a later
    user line the Harness marks `isMeta`, and is recorded as a loaded
    installation rather than as another instruction.
    """

    walked: dict[str, Any] = {
        "instruction": "",
        "started_at": None,
        "ended_at": None,
        "seats": [],
        "skill_bodies": [],
        "calls": [],
        "file_activity": [],
        "delegations": [],
        "interrupted": False,
    }
    seats: dict[tuple[str | None, str | None], int] = {}
    pending: dict[str, dict[str, Any]] = {}
    ordinal = 0

    for line in lines:
        instant = line.get("timestamp")
        if isinstance(instant, str) and instant:
            walked["started_at"] = walked["started_at"] or instant
            walked["ended_at"] = instant

        # A user line is the instruction, a Skill body, or a tool result.
        if line.get("type") == "user":
            text = _text_of((line.get("message") or {}).get("content"))
            if text.startswith(SKILL_BODY_PREFIX):
                walked["skill_bodies"].append(_skill_body(text))
            elif not walked["instruction"] and text.strip():
                walked["instruction"] = text
            for result in _blocks(line, "tool_result"):
                _close(pending, result)
            continue

        if line.get("type") != "assistant":
            continue

        # The Seat is counted per turn, so a run that changed model mid-way
        # shows both rather than whichever one happened to be first or last.
        message = line.get("message") or {}
        seat = (message.get("model"), line.get("effort"))
        if seat != (None, None):
            seats[seat] = seats.get(seat, 0) + 1

        for call in _blocks(line, "tool_use"):
            ordinal += 1
            recorded = _recorded(ordinal, instant, call)
            walked["calls"].append(recorded)
            pending[str(call.get("id"))] = recorded
            walked["file_activity"].extend(_activity(ordinal, instant, call))
            if call.get("name") in DELEGATION_TOOLS:
                walked["delegations"].append(_delegation(ordinal, instant, call))

    walked["seats"] = [
        {"model": model, "deliberation": effort, "turns": turns}
        for (model, effort), turns in seats.items()
    ]
    return walked


def _skill_body(text: str) -> dict[str, Any]:
    """One Skill body the Harness loaded, and the installation it came from."""

    first, _, _ = text.partition("\n")
    return {
        "base_directory": first[len(SKILL_BODY_PREFIX) :].strip(),
        "chars": len(text),
    }


def _recorded(ordinal: int, at: str | None, call: dict[str, Any]) -> dict[str, Any]:
    """One tool call, with its arguments exactly as the transcript holds them."""

    return {
        "ordinal": ordinal,
        "at": at,
        "tool": call.get("name"),
        "tool_use_id": call.get("id"),
        "arguments": call.get("input"),
        "is_error": None,
        "result_chars": None,
        "result_excerpt": None,
    }


def _close(pending: dict[str, dict[str, Any]], result: dict[str, Any]) -> None:
    """Attach one tool result to the call it answers."""

    call = pending.pop(str(result.get("tool_use_id")), None)
    if call is None:
        return
    text = _text_of(result.get("content")) or str(result.get("content") or "")
    call["is_error"] = bool(result.get("is_error"))
    call["result_chars"] = len(text)
    call["result_excerpt"] = text[:RESULT_EXCERPT_CHARS]


def _delegation(ordinal: int, at: str | None, call: dict[str, Any]) -> dict[str, Any]:
    """One subagent this agent started, as the call that started it records it."""

    arguments = _arguments(call)
    return {
        "ordinal": ordinal,
        "at": at,
        "tool_use_id": call.get("id"),
        "description": arguments.get("description"),
        "subagent_type": arguments.get("subagent_type"),
        "prompt": arguments.get("prompt"),
        "child_agent_id": None,
    }


def _children(packet: Path) -> list[dict[str, Any]]:
    """Return every subagent transcript the packet preserved, oldest name first."""

    directory = packet / SUBAGENTS
    if not directory.is_dir():
        return []

    found: list[dict[str, Any]] = []
    for transcript in sorted(directory.glob("agent-*.jsonl")):
        identity = transcript.stem.removeprefix("agent-")
        meta_file = transcript.with_suffix("").with_suffix(".meta.json")
        found.append(
            {
                "agent_id": identity,
                "meta": _loaded(meta_file),
                "transcript": transcript,
            }
        )
    return found


def read_packet(packet: Path | str) -> dict[str, Any]:
    """Return the trace one evidence packet holds, with its completeness status.

    The parent session comes first and every subagent follows it, each carrying
    the call that started it and the agent that made that call, so the run can
    be reconstructed without opening a transcript. Nothing here reads the run's
    reply: the status is the transcripts' and the runner's outcome alone.
    """

    packet = Path(packet)
    unparsable: dict[str, int] = {}

    # The session's own transcript, which may be absent from a run that was
    # killed before the Harness wrote one.
    parent_path = packet / PARENT_TRANSCRIPT
    parent_lines, parent_failed = _lines(parent_path)
    if parent_failed:
        unparsable[PARENT_TRANSCRIPT.as_posix()] = parent_failed
    parent_present = parent_path.is_file()

    agents: list[dict[str, Any]] = []
    session_id = _session_of(parent_lines)
    if parent_present:
        agents.append(
            {
                "agent_id": session_id,
                "role": "session",
                "parent_agent_id": None,
                "tool_use_id": None,
                "agent_type": None,
                "description": None,
                "spawn_depth": 0,
                "transcript": PARENT_TRANSCRIPT.as_posix(),
                **_walk(parent_lines),
            }
        )

    # Every subagent, read the same way and linked to the call that started it.
    for child in _children(packet):
        lines, failed = _lines(child["transcript"])
        relative = child["transcript"].relative_to(packet).as_posix()
        if failed:
            unparsable[relative] = failed
        meta = child["meta"]
        agents.append(
            {
                "agent_id": child["agent_id"],
                "role": "subagent",
                "parent_agent_id": meta.get("parentAgentId") or session_id,
                "tool_use_id": meta.get("toolUseId"),
                "agent_type": meta.get("agentType"),
                "description": meta.get("description"),
                "spawn_depth": meta.get("spawnDepth"),
                "transcript": relative,
                **_walk(lines),
            }
        )

    _link(agents)
    return {
        "schema_version": SCHEMA_VERSION,
        "packet": packet.name,
        "agents": agents,
        "status": _status(packet, agents, parent_present, unparsable),
    }


def _session_of(lines: list[dict[str, Any]]) -> str | None:
    """Return the session identity the parent transcript stamps on its lines."""

    for line in lines:
        identity = line.get("sessionId")
        if isinstance(identity, str) and identity:
            return identity
    return None


def _link(agents: list[dict[str, Any]]) -> None:
    """Point every delegation at the child transcript that answered it."""

    by_call = {
        agent["tool_use_id"]: agent["agent_id"]
        for agent in agents
        if agent["role"] == "subagent" and agent["tool_use_id"]
    }
    for agent in agents:
        for delegation in agent["delegations"]:
            delegation["child_agent_id"] = by_call.get(delegation["tool_use_id"])


def _status(
    packet: Path,
    agents: list[dict[str, Any]],
    parent_present: bool,
    unparsable: dict[str, int],
) -> dict[str, Any]:
    """Say whether this trace is whole, and name every way it is not.

    A reason here is a fact about the recorded material or about how the runner
    exited. None of them is a judgement on the Skill, and a packet reported
    `incomplete` still holds every transcript it managed to keep.
    """

    started = {
        delegation["tool_use_id"]: delegation["child_agent_id"]
        for agent in agents
        for delegation in agent["delegations"]
    }
    without_child = sorted(call for call, child in started.items() if child is None)
    without_delegation = sorted(
        agent["agent_id"]
        for agent in agents
        if agent["role"] == "subagent" and agent["tool_use_id"] not in started
    )

    # How the runner itself ended, which a trace alone cannot say.
    outcome = _loaded(packet / RESULT_FILE)
    finished = (
        outcome.get("returncode") == 0
        and not outcome.get("timed_out")
        and not outcome.get("interrupted")
    )

    reasons: list[str] = []
    if not parent_present:
        reasons.append("parent-transcript-missing")
    if unparsable:
        reasons.append("unparsable-line")
    if without_child:
        reasons.append("delegation-without-child")
    if without_delegation:
        reasons.append("child-without-delegation")
    if not finished:
        reasons.append("run-did-not-finish")

    return {
        "status": "incomplete" if reasons else "complete",
        "reasons": reasons,
        "parent_transcript": "present" if parent_present else "missing",
        "unparsable_lines": unparsable,
        "delegations_without_child": without_child,
        "children_without_delegation": without_delegation,
        "run_outcome": {
            "returncode": outcome.get("returncode"),
            "timed_out": outcome.get("timed_out"),
            "interrupted": outcome.get("interrupted"),
        },
        "agents": len(agents),
        "calls": sum(len(agent["calls"]) for agent in agents),
        "read_from": "transcripts and runner outcome only; never the run's reply",
    }


def main(argv: list[str] | None = None) -> int:
    """Write the index and its status into the packet the argument names."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    arguments = parser.parse_args(argv)

    trace = read_packet(arguments.packet)
    (arguments.packet / INDEX_FILE).write_text(
        json.dumps(trace, ensure_ascii=False, indent=2) + "\n"
    )
    (arguments.packet / STATUS_FILE).write_text(
        json.dumps(trace["status"], ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(trace["status"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
