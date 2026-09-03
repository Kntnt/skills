# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read one Harness's own record of a finished session, field by field.

Capture learns the Seat it measures from an argument supplied once at
opt-in, which is a guess that goes stale the moment the user changes model
or effort, and no lifecycle payload carries either (issue #225). Some
Harnesses keep their own record of a session as it runs, and that record —
read once, after the session's last lifecycle event, never during it — names
the exact model and deliberation control each turn actually ran under and
the token categories the Harness itself counted. This module is that read.

Harness-specific mechanics belong to the Collection Library rather than to
the Skill that consumes them (ADR-0090), the same reasoning `integrations.py`
beside this module already answers for installing and removing lifecycle
hooks. Reading a finished session's record is a second, unrelated kind of
mechanics for the same reason: a second consumer will want it, and neither
Skill should have to learn a Harness's on-disk layout to get it.

Claude Code writes one JSON-lines transcript per session, and — where the
session delegated work — a companion `subagents/` directory beside it, one
transcript per subagent. Both are read here, bounded to exactly the file the
caller hands over and that file's own companion directory: no encoding is
derived, no other session's files are opened, and nothing broader than that
is ever walked. Every field name below is re-derived rather than trusted,
because a Harness upgrade may move any of them (ADR-0157) — this module is
where that erosion is absorbed so its caller never has to know the shape
underneath.

A missing, truncated, or unparseable record is an absence, never a failure:
every function here returns an empty result rather than raising, so a caller
can leave every measurement an explicit null and still write the row it was
about to write (ADR-0156 decision 4, narrowed for this read by ADR-0158).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# The Harnesses whose own finished-session record this module knows how to
# read at all. Reading Codex's or OpenCode's own record follows once those
# integrations are verified (out of scope for #225); a Harness outside this
# set is an absence to report, never a guess to attempt.
SUPPORTED: tuple[str, ...] = ("claude-code",)

# The token categories a Seat's usage is read into, named for what each
# counts rather than for the Harness's own key — `input`, `output`,
# `cache_read`, `cache_creation`, and `thinking`, re-derived per turn from
# `message.usage.input_tokens`, `output_tokens`, `cache_read_input_tokens`,
# `cache_creation_input_tokens`, and `output_tokens_details.thinking_tokens`.
# `output_tokens_details` is absent more often than it is present — on this
# collection's own machine, on roughly six in ten subagent turns — so its
# absence is read as an unmeasured `thinking`, never as a zero.
TOKEN_CATEGORIES: tuple[str, ...] = (
    "input",
    "output",
    "cache_read",
    "cache_creation",
    "thinking",
)

# The subdirectory name, and the glob one subagent's own transcript answers
# to, that sit beside a Claude Code session's own transcript file. Neither is
# derived from anything but the transcript path the caller already handed
# over.
_SUBAGENTS_DIRNAME = "subagents"
_SUBAGENT_GLOB = "agent-*.jsonl"


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
        line = line.strip()
        if not line:
            continue
        try:
            loaded = json.loads(line)
        except ValueError:
            continue
        if isinstance(loaded, dict):
            parsed.append(loaded)
    return parsed


def _number(value: Any) -> float | None:
    """Return one usage count as a number, or None where it is not one."""

    return (
        value
        if isinstance(value, int | float) and not isinstance(value, bool)
        else None
    )


def _turn_usage(message: dict[str, Any]) -> dict[str, float | None]:
    """Return one assistant turn's token counts, read category by category.

    A missing category — the whole `usage` block, or one field inside it —
    stays an explicit None rather than a zero a caller could mistake for a
    turn that used nothing.
    """

    usage = message.get("usage")
    usage = usage if isinstance(usage, dict) else {}
    details = usage.get("output_tokens_details")
    details = details if isinstance(details, dict) else {}
    return {
        "input": _number(usage.get("input_tokens")),
        "output": _number(usage.get("output_tokens")),
        "cache_read": _number(usage.get("cache_read_input_tokens")),
        "cache_creation": _number(usage.get("cache_creation_input_tokens")),
        "thinking": _number(details.get("thinking_tokens")),
    }


def _turn(
    line: dict[str, Any],
) -> tuple[str | None, str | None, dict[str, float | None], str | None] | None:
    """Return one line's model, deliberation, usage, and instant, or None.

    Only an assistant line carries a model and a usage block at all; every
    other line in a transcript — a user turn, a tool result, a summary — is a
    different kind of record this module never reads.
    """

    if line.get("type") != "assistant":
        return None
    message = line.get("message")
    if not isinstance(message, dict):
        return None
    model = message.get("model")
    effort = line.get("effort")
    timestamp = line.get("timestamp")
    return (
        model if isinstance(model, str) and model else None,
        effort if isinstance(effort, str) and effort else None,
        _turn_usage(message),
        timestamp if isinstance(timestamp, str) and timestamp else None,
    )


def _fold(
    groups: dict[tuple[str, str | None, str | None], dict[str, Any]],
    role: str,
    lines: list[dict[str, Any]],
) -> None:
    """Fold every assistant turn in *lines* into its own (role, model, effort) Seat.

    Turns are attributed to the Seat that actually ran them: two turns on the
    same model and deliberation, in the same role, are one Seat's usage,
    summed; a turn on a different model or deliberation opens its own group,
    because that is a distinct configuration by definition (CONTEXT.md
    `Seat`). Each group is timed on its own first and last turn.
    """

    for line in lines:
        turn = _turn(line)
        if turn is None:
            continue
        model, deliberation, usage, instant = turn
        key = (role, model, deliberation)
        group = groups.setdefault(
            key,
            {
                "role": role,
                "model": model,
                "native_deliberation": deliberation,
                "tokens": dict.fromkeys(TOKEN_CATEGORIES),
                "started_at": None,
                "completed_at": None,
            },
        )
        for category in TOKEN_CATEGORIES:
            value = usage[category]
            if value is None:
                continue
            group["tokens"][category] = (group["tokens"][category] or 0) + value
        if instant is None:
            continue
        if group["started_at"] is None or instant < group["started_at"]:
            group["started_at"] = instant
        if group["completed_at"] is None or instant > group["completed_at"]:
            group["completed_at"] = instant


def usage(harness: str, transcript_path: str | None) -> list[dict[str, Any]]:
    """Return every Seat's usage this Harness's own finished record supports.

    Bounded to exactly the session named by *transcript_path*: that file, and
    its own companion subagent directory (a `subagents/` directory named for
    the transcript's own stem, beside it), and nothing else — no encoding is
    derived from a working directory or a session identity, and no other
    session's files are ever opened.

    Returns an empty list where the Harness is unsupported, no usable path
    was handed over, or nothing in it could be read or parsed at all. That is
    an absence for the caller to leave every measurement null over, never a
    raised error (ADR-0156 decision 4, applied to this read by ADR-0158).

    Each returned entry carries `role` (`"main"` for the session's own turns,
    `"delegated"` for a subagent's), `model`, `native_deliberation`, `tokens`
    (one number or None per `TOKEN_CATEGORIES`), and `started_at` /
    `completed_at`, the instants of that Seat's own first and last turn. No
    prompt, response, reasoning, tool argument, tool output, file content, or
    working directory ever reaches a returned entry: only the fields named
    above are ever read out of a line.
    """

    if (
        harness not in SUPPORTED
        or not isinstance(transcript_path, str)
        or not transcript_path
    ):
        return []

    path = Path(transcript_path)
    groups: dict[tuple[str, str | None, str | None], dict[str, Any]] = {}
    _fold(groups, "main", _lines(path))

    subagents = path.with_suffix("") / _SUBAGENTS_DIRNAME
    if subagents.is_dir():
        for agent_transcript in sorted(subagents.glob(_SUBAGENT_GLOB)):
            _fold(groups, "delegated", _lines(agent_transcript))

    return list(groups.values())
