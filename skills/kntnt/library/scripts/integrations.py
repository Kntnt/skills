# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Install, verify, and remove Harness integrations one feature owns.

A Skill that needs the Harness to call it — rather than the user to invoke it —
has to write into that Harness's own configuration, and then has to be able to
take exactly that back out again later. Doing it per Skill would mean each one
learning three Harnesses' file formats and each one inventing its own idea of
what it owns, so the mechanics live here once and the feature supplies only its
owner identity and the command to run.

Disk is the truth (ADR-0003). Nothing here remembers what it installed: an
install reads the Harness's file, converges it, and reads it back, and a removal
finds its own entries by the owner they carry. That makes both idempotent, and
it makes a hand-edited or externally repaired Harness the state everything works
from rather than a state nothing can account for.

A Harness whose supported lifecycle cannot carry the contract is reported as an
Unsatisfied capability (ADR-0030) rather than silently skipped, because a
feature that believes it is installed where it is not is worse than one that
knows it is not. Event names, entry shape, and file location are established
from each Harness as installed rather than assumed from a sibling's (ADR-0157)
— Codex's own config file happens to accept the same PascalCase names and the
same nested matcher group Claude Code's does, confirmed live rather than
assumed, and is never the flat, camelCase shape its unrelated app-server
protocol reports back. A Harness that gates a new integration behind a user's
trust, as Codex does, is reported gated rather than healthy: present, not yet
active, and never a trust decision this collection forges on the user's
behalf.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# The lifecycle moments a capture-shaped integration needs. They are
# observations rather than verdicts: a stop says a turn ended, never that the
# work in it succeeded.
CLAUDE_EVENTS: tuple[str, ...] = ("SessionStart", "Stop", "SessionEnd")

# Codex CLI 0.153.0's own configuration file — `~/.codex/hooks.json`,
# deserialized through its `HookEventsToml` — names lifecycle events in the
# same PascalCase Claude Code's `settings.json` uses, confirmed live against
# the installed binary (`codex app-server`, `initialize` + `hooks/list`): a
# camelCase key here (`sessionStart`, `stop`, `sessionEnd`) is silently
# ignored rather than read. That camelCase spelling names a different thing
# — the app-server protocol's own `HookEventName`, the normalized runtime
# view `hooks/list` itself reports back — and never the config file's own
# shape, which an earlier draft of this adapter wrongly conflated with it.
CODEX_EVENTS: tuple[str, ...] = ("SessionStart", "Stop", "SessionEnd")

# What an installed entry asks its Harness for, in seconds, at any moment the
# Harness states no lower ceiling of its own.
HOOK_TIMEOUT_SECONDS = 10

# The moments a Harness will not give that much, established from the Harness
# as installed rather than assumed (ADR-0157). Codex (codex-cli 0.153.4),
# driven through `codex app-server` — `initialize`, an `initialized`
# notification, then `hooks/list`, standard input held open, `CODEX_HOME`
# pointed at the hook table under test — reports each entry's honoured
# `timeoutSec` beside a `warnings` array. Asked for 999, 10, 5 and 4 in turn it
# answers the same way every time: `SessionStart` and `Stop` are honoured
# exactly as asked, `SessionEnd` is three seconds whatever was asked, and the
# clamp is named in `warnings` — which is what the user was being told on every
# session for as long as this asked for ten there. Asked for three, it honours
# three and `warnings` comes back empty.
#
# Three seconds is a ceiling on the work that moment does, so what that work
# costs is written down here for whoever next spends it. Session end is the one
# place in the hook path permitted to reach the network (ADR-0167): `_finish`
# dispatches the unattended source refresh there and nowhere else, and that
# refresh's network portion is itself hard-capped at `refresh.BUDGET_SECONDS`,
# two seconds, against a monotonic deadline. A whole session-end invocation,
# launcher included, with every source in a real store forced due and fetched
# over the real network, completed in 1.1 to 1.7 seconds across repeated runs —
# about a second of margin under this ceiling. Raising that budget spends that
# margin, and beyond it Codex truncates the pass rather than this entry being
# given the longer run it asked for.
#
# The other two Harnesses state no ceiling for this table to meet. Claude Code
# exposes nothing that answers what it would honour the way `hooks/list` does,
# so its ten seconds is what it is installed with rather than what it was told,
# and no clamp has been observed there. OpenCode loads a plugin module instead
# of reading a hook table, and the file installed there carries no timeout at
# all.
HARNESS_TIMEOUT_CEILINGS: dict[str, dict[str, int]] = {"codex": {"SessionEnd": 3}}

OPENCODE_EVENTS: tuple[str, ...] = (
    "session.created",
    "session.idle",
    "session.error",
    "session.deleted",
)

SUPPORTED: tuple[str, ...] = ("claude-code", "codex", "opencode")

# Why a Harness outside SUPPORTED gets no adapter, in the words `check` uses for
# any other Capability the agent has to answer for itself.
UNSATISFIED = (
    "this Harness exposes no supported session lifecycle an integration can "
    "own; run the feature in Claude Code, Codex, or OpenCode instead"
)

# Codex reviews a hook that is new or has changed before it will ever run it
# (its own `HookTrustStatus`: `managed`, `untrusted`, `trusted`, `modified`,
# and the CLI's own startup copy: "Hooks need review... Trust all and
# continue... Continue without trusting (hooks won't run)"). This collection
# does not forge that trust decision or write a trust record on the user's
# behalf (ADR-0157), so a fully written Codex integration is reported gated —
# present, not yet active — and named to the user, rather than healthy.
CODEX_TRUST_GATE = (
    "Codex reviews a new or changed hook before it will run it. Start Codex "
    'and accept the review ("Trust all and continue"), or pass '
    "--dangerously-bypass-hook-trust, to activate this integration; until "
    "then it is written to disk but will not run."
)


class IntegrationError(RuntimeError):
    """A Harness's own configuration could not be read or written."""


def _read_json(path: Path) -> dict[str, Any]:
    """Return one JSON object from *path*, or an empty one where it is absent."""

    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise IntegrationError(f"{path} could not be read as JSON: {exc}") from exc
    if not isinstance(loaded, dict):
        raise IntegrationError(f"{path} does not hold a JSON object.")
    return loaded


def _write_json(path: Path, document: dict[str, Any]) -> None:
    """Write *document* to *path*, creating the directories it needs."""

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        raise IntegrationError(f"{path} could not be written: {exc}") from exc


def _owned_argv(owner: str, harness: str, command: list[str]) -> list[str]:
    """Return the argument vector an entry of *owner* runs in *harness*.

    The owner travels inside the command rather than beside it, because the
    surrounding object belongs to the Harness's own schema and an unknown key
    there is a key some Harness version rejects. A command string is the one
    field every hook shape has, and matching on it needs nothing to be
    remembered elsewhere.

    The Harness travels with it because the installer is the last thing that
    knows which Harness this entry is being written into: a script cannot ask
    what invoked it, and a feature that guessed would be guessing about the
    identity its own evidence is recorded under.
    """

    return [*command, f"--owner={owner}", f"--harness={harness}"]


def _owned_command(owner: str, harness: str, command: list[str]) -> str:
    """Return that argument vector as the one string a hook table holds."""

    return " ".join(_owned_argv(owner, harness, command))


def _owns(entry: Any, owner: str) -> bool:
    """Return whether one hook entry was installed by *owner*.

    Both Harnesses this owns entries in write the same nested matcher group
    — a top-level `hooks` list holding the handler. A flat entry with
    `command` directly on it is also recognized, which costs nothing and
    keeps a hand-edited or externally repaired file from being misread as
    somebody else's, without either Harness's own config file ever being
    written in that shape.
    """

    if not isinstance(entry, dict):
        return False
    handlers = entry.get("hooks")
    if isinstance(handlers, list):
        return any(
            isinstance(handler, dict)
            and isinstance(handler.get("command"), str)
            and f"--owner={owner}" in handler["command"]
            for handler in handlers
        )
    command = entry.get("command")
    return isinstance(command, str) and f"--owner={owner}" in command


def _hook_timeout(harness: str, event: str) -> int:
    """Return the timeout *harness* honours for an entry at *event*.

    Asking for more than a Harness gives is not a longer run; it is a clamp the
    Harness reports back to the user at every session. So an entry asks for
    what its own Harness accepts at that one moment, and
    `HARNESS_TIMEOUT_CEILINGS` is where what each was observed to accept is
    written down.
    """

    ceiling = HARNESS_TIMEOUT_CEILINGS.get(harness, {}).get(event)
    return (
        HOOK_TIMEOUT_SECONDS if ceiling is None else min(HOOK_TIMEOUT_SECONDS, ceiling)
    )


def _hook_entry(
    owner: str, harness: str, command: list[str], event: str
) -> dict[str, Any]:
    """Return the one hook entry this owner installs at *event*.

    Codex's own config file (`HookEventsToml`) accepts the same nested
    `{"hooks": [...]}` matcher group Claude Code's `settings.json` does,
    confirmed live against the installed binary — a flat `handlerType`/
    `command` entry here registers nothing, because that shape belongs to
    the app-server protocol's own runtime view, not to what this file reads.
    """

    return {
        "hooks": [
            {
                "type": "command",
                "command": _owned_command(owner, harness, command),
                "timeout": _hook_timeout(harness, event),
            }
        ]
    }


def _converge_hooks(
    document: dict[str, Any],
    owner: str,
    harness: str,
    command: list[str],
    events: tuple[str, ...],
) -> dict[str, Any]:
    """Return *document* holding exactly one entry of *owner* per event.

    Convergence rather than appending is what makes a second install a no-op and
    a repair after external damage a no-op too: whatever is there of ours is
    replaced by the one entry that should be there, and everybody else's entries
    keep their order.
    """

    hooks = dict(document.get("hooks") or {})
    for event in events:
        existing = hooks.get(event)
        others = [
            entry
            for entry in (existing if isinstance(existing, list) else [])
            if not _owns(entry, owner)
        ]
        hooks[event] = [*others, _hook_entry(owner, harness, command, event)]
    return {**document, "hooks": hooks}


def _strip_hooks(document: dict[str, Any], owner: str) -> tuple[dict[str, Any], int]:
    """Return *document* without any entry of *owner*, and how many went."""

    hooks = dict(document.get("hooks") or {})
    taken = 0
    for event, entries in list(hooks.items()):
        if not isinstance(entries, list):
            continue
        kept = [entry for entry in entries if not _owns(entry, owner)]
        taken += len(entries) - len(kept)

        # An event we emptied is an event nobody else uses, so the key goes
        # too: a Harness file left full of empty arrays is our leavings.
        if kept:
            hooks[event] = kept
        else:
            del hooks[event]

    remaining = {**document}
    if hooks:
        remaining["hooks"] = hooks
    else:
        remaining.pop("hooks", None)
    return remaining, taken


def _count_hooks(document: dict[str, Any], owner: str) -> int:
    """Return how many entries of *owner* one Harness document holds."""

    hooks = document.get("hooks")
    if not isinstance(hooks, dict):
        return 0
    return sum(
        1
        for entries in hooks.values()
        if isinstance(entries, list)
        for entry in entries
        if _owns(entry, owner)
    )


def _plugin_path(root: Path, owner: str) -> Path:
    """Return the plugin file *owner* owns in an OpenCode installation."""

    return root / ".config" / "opencode" / "plugins" / f"{owner}.js"


def _plugin_source(
    owner: str, harness: str, command: list[str], events: tuple[str, ...]
) -> str:
    """Return the OpenCode plugin that forwards its session events to *command*.

    OpenCode loads plugins as modules rather than reading a hook table, so the
    unit of ownership is the file itself: one file named for the owner, removed
    whole. The plugin does nothing but hand the event on — every judgement about
    what an event means belongs to the feature the command runs, not here.
    """

    argv = json.dumps(_owned_argv(owner, harness, command))
    watched = json.dumps(list(events))
    return f"""// Installed and owned by {owner}. Removing this file removes the
// integration; nothing else here belongs to it.
const OWNER = {json.dumps(owner)};
const COMMAND = {argv};
const WATCHED = {watched};

export const KntntOwnedCapture = async ({{ $ }}) => ({{
  event: async ({{ event }}) => {{
    if (!WATCHED.includes(event.type)) return;

    // Fail open: a capture that cannot run must never hold up the session.
    // The event is redirected onto the command's own standard input rather
    // than left unspecified, which is what carries the session identity
    // nested inside it — OpenCode never puts one on the command line — and
    // is also what keeps Bun's shell from handing the child this process's
    // own standard input, which a hook that reads to end-of-file could
    // otherwise block on for as long as this session's own stdin stays open.
    try {{
      await $`${{COMMAND}} --event=${{event.type}} < ${{new Response(JSON.stringify(event))}}`
        .quiet()
        .nothrow();
    }} catch {{
      // An integration owned by {owner} never becomes the session's problem.
    }}
  }},
}});
"""


def _harness_file(harness: str, root: Path) -> Path:
    """Return the file one Harness keeps its owned hook table in."""

    if harness == "claude-code":
        return root / ".claude" / "settings.json"
    return root / ".codex" / "hooks.json"


def _events(harness: str) -> tuple[str, ...]:
    """Return the lifecycle moments one Harness is asked for."""

    if harness == "opencode":
        return OPENCODE_EVENTS
    return CLAUDE_EVENTS if harness == "claude-code" else CODEX_EVENTS


def _wanted_events(harness: str, events: tuple[str, ...] | None) -> tuple[str, ...]:
    """Return the moments an owner asks of *harness*, narrowed to real ones.

    An owner names moments in the Harness's own vocabulary, and a name that
    Harness does not have is dropped rather than written: an entry at a moment
    nothing fires is an entry every later health check counts and no Harness
    ever runs. An owner that narrows the set to nothing gets the Harness's own
    full set, because installing at no moment at all is not an integration.
    """

    available = _events(harness)
    if events is None:
        return available
    narrowed = tuple(event for event in available if event in events)
    return narrowed or available


def _unsatisfied(harness: str) -> dict[str, Any]:
    """Return the answer for a Harness no adapter can serve."""

    return {
        "harness": harness,
        "status": "unsatisfied",
        "entries": 0,
        "capability": UNSATISFIED,
        "detail": None,
    }


def install(
    owner: str,
    harness: str,
    root: Path,
    command: list[str],
    *,
    events: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Install *owner*'s integration into *harness* under *root*, idempotently.

    The result is read back from disk rather than assumed from the write, so a
    partially applied change is reported as the failure it is instead of as the
    installation it was meant to be.

    *events* names the lifecycle moments this owner wants of this one Harness,
    for an owner that wants fewer than the whole set: a feature that acts on a
    session's beginning and its end has no use for the turns in between, and an
    entry installed at a moment nothing reads is an entry a later health check
    has to account for. Omitted, the Harness's own full set is installed, which
    is what capture — the first owner here — asks for.
    """

    if harness not in SUPPORTED:
        return _unsatisfied(harness)

    wanted = _wanted_events(harness, events)
    try:
        if harness == "opencode":
            path = _plugin_path(root, owner)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                _plugin_source(owner, harness, command, wanted),
                encoding="utf-8",
            )
            installed = path.exists()
            entries = len(wanted) if installed else 0
        else:
            path = _harness_file(harness, root)
            _write_json(
                path,
                _converge_hooks(_read_json(path), owner, harness, command, wanted),
            )
            entries = _count_hooks(_read_json(path), owner)
            installed = entries == len(wanted)
    except IntegrationError as exc:
        return {
            "harness": harness,
            "status": "failed",
            "entries": 0,
            "capability": None,
            "detail": str(exc),
        }

    # A write that succeeded for Codex is still not an active integration: the
    # Harness itself gates a new hook behind a trust review this collection
    # never clears on the user's behalf (ADR-0157), so installation says so
    # here rather than waiting for a later health check to be asked.
    gated = installed and harness == "codex"
    return {
        "harness": harness,
        "status": "installed" if installed else "failed",
        "entries": entries,
        "capability": None,
        "detail": (
            CODEX_TRUST_GATE
            if gated
            else (None if installed else "the integration is not on disk after writing")
        ),
    }


def remove(owner: str, harness: str, root: Path) -> dict[str, Any]:
    """Remove every integration *owner* installed into *harness* under *root*.

    Surgical and idempotent: entries nobody else owns go, everything else in the
    Harness's own configuration is left exactly as it was, and removing what is
    already absent is a converged state rather than an error.
    """

    if harness not in SUPPORTED:
        return _unsatisfied(harness)

    try:
        if harness == "opencode":
            path = _plugin_path(root, owner)
            taken = 1 if path.exists() else 0
            path.unlink(missing_ok=True)
            cleared = not path.exists()
        else:
            path = _harness_file(harness, root)
            if not path.exists():
                taken, cleared = 0, True
            else:
                remaining, taken = _strip_hooks(_read_json(path), owner)
                _write_json(path, remaining)
                cleared = _count_hooks(_read_json(path), owner) == 0
    except (IntegrationError, OSError) as exc:
        return {
            "harness": harness,
            "status": "failed",
            "entries": 0,
            "capability": None,
            "detail": str(exc),
        }

    return {
        "harness": harness,
        "status": "removed" if cleared else "failed",
        "entries": taken if cleared else 0,
        "capability": None,
        "detail": None if cleared else "entries remain on disk after removal",
    }


def health(
    owner: str,
    harness: str,
    root: Path,
    *,
    events: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Report what *harness* actually holds of *owner*'s integration right now.

    *events* is what this owner installs into this Harness, because how many
    entries make a whole integration is the owner's own number: judging an
    owner that installs two against a Harness's full set would call every
    healthy installation degraded.
    """

    if harness not in SUPPORTED:
        return _unsatisfied(harness)

    wanted = _wanted_events(harness, events)
    try:
        if harness == "opencode":
            entries = len(wanted) if _plugin_path(root, owner).exists() else 0
            expected = len(wanted)
        else:
            entries = _count_hooks(_read_json(_harness_file(harness, root)), owner)
            expected = len(wanted)
    except IntegrationError as exc:
        return {
            "harness": harness,
            "status": "failed",
            "entries": 0,
            "capability": None,
            "detail": str(exc),
        }

    # Some but not all of what we install is a Harness that would fire for one
    # moment and not another, which is not health and is not absence either.
    # A fully written Codex integration is a third case again: present, but
    # never observably active, because only the Harness's own trust review —
    # never this collection — can cross it into "healthy" (ADR-0157).
    if entries == 0:
        status = "absent"
    elif entries == expected:
        status = "gated" if harness == "codex" else "healthy"
    else:
        status = "degraded"
    return {
        "harness": harness,
        "status": status,
        "entries": entries,
        "capability": None,
        "detail": CODEX_TRUST_GATE if status == "gated" else None,
    }


# Where each Harness keeps the instructions it reads into every session of its
# own, relative to the home the caller hands in. These are the Harnesses' own
# documented paths rather than a sibling's guessed at (ADR-0157): Claude Code's
# `~/.claude/CLAUDE.md`, Codex's `~/.codex/AGENTS.md`, and OpenCode's
# `~/.config/opencode/AGENTS.md`, the last of which OpenCode's own rules
# documentation names as the global file applied across all its sessions.
#
# That last path carries a consequence worth knowing before it is written to.
# OpenCode falls back to reading `~/.claude/CLAUDE.md` when it finds no global
# file of its own and Claude Code compatibility is on, so creating this file is
# what ends that fallback: a machine that was reading one file through two
# Harnesses reads two files afterwards. Writing an owned block is still the
# right thing — a block that lands where the Harness does not read it is an
# install that looks successful and does nothing — but the file it creates is
# the user's from then on.
INSTRUCTION_FILES: dict[str, str] = {
    "claude-code": ".claude/CLAUDE.md",
    "codex": ".codex/AGENTS.md",
    "opencode": ".config/opencode/AGENTS.md",
}

# Why a Harness outside INSTRUCTION_FILES gets no owned block, in the same
# words every other Capability the agent has to answer for itself is said in.
INSTRUCTIONS_UNSATISFIED = (
    "this Harness exposes no global instruction file an owned block can be "
    "written into; run the feature in Claude Code, Codex, or OpenCode instead"
)

# The one Harness with a status line this collection has an adapter for.
STATUSLINE_HARNESSES: tuple[str, ...] = ("claude-code",)

STATUSLINE_UNSATISFIED = (
    "this Harness exposes no status line an integration can own; run the "
    "feature in Claude Code instead"
)


def _instructions_path(harness: str, root: Path) -> Path | None:
    """Return the global instruction file *harness* reads, or None where it has none."""

    relative = INSTRUCTION_FILES.get(harness)
    return None if relative is None else root / relative


def _fence(owner: str) -> tuple[str, str]:
    """Return the pair of comments that delimit *owner*'s block.

    A hook table holds objects, so an owner travels there inside a command
    string; an instruction file holds prose, so it travels as a comment the
    Harness renders as nothing and a reader sees as a boundary. Both put the
    ownership identity inside what is written rather than in a register beside
    it (ADR-0090), which is what makes a hand edit a state to converge from
    rather than a ledger that has gone wrong.
    """

    return f"<!-- {owner} begin -->", f"<!-- {owner} end -->"


def _block_pattern(owner: str) -> re.Pattern[str]:
    """Return the expression matching one whole block of *owner*, fences included."""

    begin, end = _fence(owner)
    return re.compile(
        r"\n*" + re.escape(begin) + r".*?" + re.escape(end) + r"[ \t]*\n?",
        re.DOTALL,
    )


def _unbalanced(text: str, owner: str) -> bool:
    """True when *text* holds a fence of *owner* that its partner does not close.

    A file in that state is one a hand edit or a crashed write left half of a
    block in, and converging it would append a second block below the orphan
    rather than replace it. Neither fence is removed on a guess: everything
    between them is the user's file, and this collection deletes only what it
    can see both ends of.
    """

    begin, end = _fence(owner)
    return text.count(begin) != text.count(end)


def _strip_block(text: str, owner: str) -> tuple[str, int]:
    """Return *text* without any block of *owner*, and how many went."""

    stripped, taken = _block_pattern(owner).subn("", text)
    return stripped, taken


def _count_blocks(text: str, owner: str) -> int:
    """Return how many whole blocks of *owner* one instruction file holds."""

    return len(_block_pattern(owner).findall(text))


def _converge_block(text: str, owner: str, body: str) -> str:
    """Return *text* holding exactly one block of *owner*, carrying *body*.

    Convergence rather than appending, for the reason `_converge_hooks` states:
    a second install is a no-op and a repair after external damage is a no-op
    too. The block goes at the end of the file, because everything above it is
    the user's own and its order is theirs to keep.
    """

    begin, end = _fence(owner)
    block = f"{begin}\n{body.strip()}\n{end}\n"
    stripped, _ = _strip_block(text, owner)
    kept = stripped.rstrip()
    return block if not kept else f"{kept}\n\n{block}"


def _instructions_failure(harness: str, detail: str) -> dict[str, Any]:
    """Return the record of an instruction file this run would not write."""

    return {
        "harness": harness,
        "status": "failed",
        "entries": 0,
        "capability": None,
        "detail": detail,
    }


def _unsatisfied_as(harness: str, capability: str) -> dict[str, Any]:
    """Return the answer for a Harness no adapter of this kind can serve."""

    return {
        "harness": harness,
        "status": "unsatisfied",
        "entries": 0,
        "capability": capability,
        "detail": None,
    }


def install_block(owner: str, harness: str, root: Path, body: str) -> dict[str, Any]:
    """Write *owner*'s one block of *body* into *harness*'s instruction file.

    Read back from disk rather than assumed from the write, exactly as a hook
    table is. A file that already carries an unbalanced fence of this owner is
    refused rather than converged, and the refusal names the file: the user
    can see both what is wrong and where, and nothing of theirs is guessed at.
    """

    path = _instructions_path(harness, root)
    if path is None:
        return _unsatisfied_as(harness, INSTRUCTIONS_UNSATISFIED)

    try:
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if _unbalanced(text, owner):
            return _instructions_failure(
                harness,
                f"{path} holds an unclosed '{owner}' fence; close or delete it "
                "by hand and enable this Feature again",
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_converge_block(text, owner, body), encoding="utf-8")
        entries = _count_blocks(path.read_text(encoding="utf-8"), owner)
    except (OSError, UnicodeDecodeError) as exc:
        return _instructions_failure(harness, f"{path} could not be written: {exc}")

    return {
        "harness": harness,
        "status": "installed" if entries == 1 else "failed",
        "entries": entries,
        "capability": None,
        "detail": None if entries == 1 else "the block is not on disk after writing",
    }


def remove_block(owner: str, harness: str, root: Path) -> dict[str, Any]:
    """Take *owner*'s block out of *harness*'s instruction file, and nothing else.

    Surgical and idempotent, the same contract `remove` holds for a hook table:
    a file this owner never wrote in is already converged, and prose nobody
    fenced as ours is never touched.
    """

    path = _instructions_path(harness, root)
    if path is None:
        return _unsatisfied_as(harness, INSTRUCTIONS_UNSATISFIED)

    try:
        if not path.exists():
            return {
                "harness": harness,
                "status": "removed",
                "entries": 0,
                "capability": None,
                "detail": None,
            }
        text = path.read_text(encoding="utf-8")
        if _unbalanced(text, owner):
            return _instructions_failure(
                harness,
                f"{path} holds an unclosed '{owner}' fence; remove it by hand",
            )
        remaining, taken = _strip_block(text, owner)
        path.write_text(
            remaining.rstrip() + "\n" if remaining.strip() else "", encoding="utf-8"
        )
        cleared = _count_blocks(path.read_text(encoding="utf-8"), owner) == 0
    except (OSError, UnicodeDecodeError) as exc:
        return _instructions_failure(harness, f"{path} could not be written: {exc}")

    return {
        "harness": harness,
        "status": "removed" if cleared else "failed",
        "entries": taken if cleared else 0,
        "capability": None,
        "detail": None if cleared else "the block remains on disk after removal",
    }


def block_health(owner: str, harness: str, root: Path) -> dict[str, Any]:
    """Report what *harness*'s instruction file holds of *owner*'s block now."""

    path = _instructions_path(harness, root)
    if path is None:
        return _unsatisfied_as(harness, INSTRUCTIONS_UNSATISFIED)

    try:
        text = path.read_text(encoding="utf-8") if path.exists() else ""
    except (OSError, UnicodeDecodeError) as exc:
        return _instructions_failure(harness, f"{path} could not be read: {exc}")

    if _unbalanced(text, owner):
        return {
            "harness": harness,
            "status": "degraded",
            "entries": _count_blocks(text, owner),
            "capability": None,
            "detail": f"{path} holds an unclosed '{owner}' fence",
        }

    entries = _count_blocks(text, owner)
    return {
        "harness": harness,
        "status": "healthy"
        if entries == 1
        else ("absent" if entries == 0 else "degraded"),
        "entries": entries,
        "capability": None,
        "detail": None
        if entries <= 1
        else f"{path} holds {entries} blocks of '{owner}'",
    }


def _statusline_command(setting: Any) -> str | None:
    """Return the command a `statusLine` setting names, or None where it names none."""

    if not isinstance(setting, dict):
        return None
    command = setting.get("command")
    return command if isinstance(command, str) else None


def _occupied(setting: Any, owner: str) -> str | None:
    """Return the foreign command holding the status line slot, or None.

    None covers both an empty slot and one this owner already holds, because
    those are the two states an install writes into without being told twice.
    Anything else is somebody's status line, and what happens to it is the
    user's to decide rather than this collection's to assume (ADR-0174): an
    install that was not told to replace it reports what holds the slot and
    writes nothing, and one that was told replaces it and says what went.

    What is never done either way is remembering the displaced value so that a
    later removal can put it back. The setting is single-valued, so there is
    nowhere to keep the old one that would not be a private ledger, and a
    ledger is the one thing convergence over disk has no place for (ADR-0090):
    it goes stale the moment the user edits the setting by hand, and a removal
    restoring a value they have since replaced is worse than one that restores
    nothing.
    """

    if setting is None:
        return None
    command = _statusline_command(setting)
    if command is not None and f"--owner={owner}" in command:
        return None
    return command if command is not None else "a statusLine setting of another shape"


def install_statusline(
    owner: str,
    harness: str,
    root: Path,
    command: list[str],
    *,
    replace: bool = False,
) -> dict[str, Any]:
    """Point *harness*'s status line at *command*, replacing another only if told.

    A status line somebody else's command holds is a thing the user chose, and
    what becomes of it is theirs to answer rather than this call's to decide
    (ADR-0174). Untold, this reports what holds the slot and writes nothing, so
    that the answer can be asked for where questions are asked; told, it writes
    ours and names what it displaced, because that name is the whole of what is
    left of the old value afterwards.
    """

    if harness not in STATUSLINE_HARNESSES:
        return _unsatisfied_as(harness, STATUSLINE_UNSATISFIED)

    path = _harness_file(harness, root)
    try:
        document = _read_json(path)
        held = _occupied(document.get("statusLine"), owner)
        if held is not None and not replace:
            return {
                "harness": harness,
                "status": "held",
                "entries": 0,
                "capability": None,
                "held": held,
                "detail": (
                    f"the statusLine setting in {path} already runs {held}, and it "
                    "holds one command rather than a list. Nothing was written. "
                    "Replacing it is the user's answer to give, and this "
                    "collection keeps no copy of what it replaces, so a later "
                    "Disable will not put that command back."
                ),
            }
        _write_json(
            path,
            {
                **document,
                "statusLine": {
                    "type": "command",
                    "command": _owned_command(owner, harness, command),
                },
            },
        )
        installed = _occupied(_read_json(path).get("statusLine"), owner) is None and (
            _read_json(path).get("statusLine") is not None
        )
    except IntegrationError as exc:
        return _instructions_failure(harness, str(exc))

    return {
        "harness": harness,
        "status": "installed" if installed else "failed",
        "entries": 1 if installed else 0,
        "capability": None,
        "detail": (
            (
                f"the status line that ran {held} was replaced, and no copy of it "
                "is kept anywhere"
            )
            if installed and held is not None
            else (None if installed else "the status line is not set after writing")
        ),
    }


def remove_statusline(owner: str, harness: str, root: Path) -> dict[str, Any]:
    """Clear *harness*'s status line where this owner holds it, and never otherwise."""

    if harness not in STATUSLINE_HARNESSES:
        return _unsatisfied_as(harness, STATUSLINE_UNSATISFIED)

    path = _harness_file(harness, root)
    try:
        document = _read_json(path)
        setting = document.get("statusLine")
        if setting is None or _occupied(setting, owner) is not None:
            return {
                "harness": harness,
                "status": "removed",
                "entries": 0,
                "capability": None,
                "detail": None,
            }
        remaining = {
            key: value for key, value in document.items() if key != "statusLine"
        }
        _write_json(path, remaining)
        cleared = _read_json(path).get("statusLine") is None
    except IntegrationError as exc:
        return _instructions_failure(harness, str(exc))

    return {
        "harness": harness,
        "status": "removed" if cleared else "failed",
        "entries": 1 if cleared else 0,
        "capability": None,
        "detail": None if cleared else "the status line remains set after removal",
    }


def statusline_health(owner: str, harness: str, root: Path) -> dict[str, Any]:
    """Report who holds *harness*'s status line right now."""

    if harness not in STATUSLINE_HARNESSES:
        return _unsatisfied_as(harness, STATUSLINE_UNSATISFIED)

    path = _harness_file(harness, root)
    try:
        setting = _read_json(path).get("statusLine")
    except IntegrationError as exc:
        return _instructions_failure(harness, str(exc))

    if setting is not None and _occupied(setting, owner) is None:
        return {
            "harness": harness,
            "status": "healthy",
            "entries": 1,
            "capability": None,
            "detail": None,
        }

    # A slot somebody else holds is absent for this owner and is not the same
    # absence as an empty one: it names what the user would be answering about,
    # and `held` carries that name so a row can ask rather than only report.
    held = _occupied(setting, owner)
    return {
        "harness": harness,
        "status": "absent",
        "entries": 0,
        "capability": None,
        "held": held,
        "detail": None if held is None else f"the statusLine setting runs {held}",
    }


# How the states of several records fold into the one state their Harness is
# in, weakest first: a Harness holding half of what an owner installs is not
# healthy because the other half is. Each list is read from the front, and the
# first state present is the answer.
_FOLD_ORDER: tuple[str, ...] = (
    "failed",
    "held",
    "unsatisfied",
    "absent",
    "degraded",
    "gated",
    "removed",
    "installed",
    "healthy",
)


def fold(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return several records about one Harness as the one record it earns.

    A feature that owns more than one thing in a Harness — a block of prose and
    a hook table entry, say — has one integration in that Harness and not two.
    Reporting each part separately would put two records with the same
    `harness` in front of a reader whose instructions say that records for one
    owner disagreeing about one Harness is itself the finding, and read two
    different things as one contradiction. So the parts fold: the entries add
    up, the details join, and the state is the weakest of them, which is the
    state a user has to act on.
    """

    if not records:
        raise IntegrationError("nothing to fold into a Harness record")
    if len(records) == 1:
        return records[0]

    present = {str(record["status"]) for record in records}
    status = next((name for name in _FOLD_ORDER if name in present), "failed")

    # A mixed answer says the whole is not what any single part reports: a
    # feature half installed is not installed, and one half removed is not
    # removed either.
    if status in {"installed", "removed", "healthy"} and len(present) > 1:
        status = "degraded" if status == "healthy" else "failed"

    details = [str(record["detail"]) for record in records if record.get("detail")]
    capability = next(
        (str(record["capability"]) for record in records if record.get("capability")),
        None,
    )
    folded = {
        "harness": str(records[0]["harness"]),
        "status": status,
        "entries": sum(int(record.get("entries") or 0) for record in records),
        "capability": capability,
        "detail": " ".join(details) or None,
    }

    # What holds a slot this owner wants survives the fold, because it is what
    # the question put to the user is about.
    held = next((record["held"] for record in records if record.get("held")), None)
    if held is not None:
        folded["held"] = held
    return folded


def _act(
    action: str, owner: str, harnesses: list[str], root: Path, command: list[str]
) -> list[dict[str, Any]]:
    """Apply one action across every named Harness, reporting each separately."""

    results: list[dict[str, Any]] = []
    for harness in harnesses:
        if action == "install":
            results.append(install(owner, harness, root, command))
        elif action == "remove":
            results.append(remove(owner, harness, root))
        else:
            results.append(health(owner, harness, root))
    return results


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the command line of one integration action."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "remove", "health"))
    parser.add_argument("--owner", required=True)
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--root", default=str(Path.home()))
    parser.add_argument("--command", action="append", default=[])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one integration action and report every Harness it touched."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    harnesses = args.harness or list(SUPPORTED)
    results = _act(args.action, args.owner, harnesses, Path(args.root), args.command)
    json.dump({"action": args.action, "harnesses": results}, sys.stdout, indent=2)
    sys.stdout.write("\n")

    # A Harness that could not be brought to the requested state is the whole
    # reason a caller checks an exit code here.
    return 1 if any(result["status"] == "failed" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
