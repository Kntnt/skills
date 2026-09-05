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

    return CLAUDE_EVENTS if harness == "claude-code" else CODEX_EVENTS


def _unsatisfied(harness: str) -> dict[str, Any]:
    """Return the answer for a Harness no adapter can serve."""

    return {
        "harness": harness,
        "status": "unsatisfied",
        "entries": 0,
        "capability": UNSATISFIED,
        "detail": None,
    }


def install(owner: str, harness: str, root: Path, command: list[str]) -> dict[str, Any]:
    """Install *owner*'s integration into *harness* under *root*, idempotently.

    The result is read back from disk rather than assumed from the write, so a
    partially applied change is reported as the failure it is instead of as the
    installation it was meant to be.
    """

    if harness not in SUPPORTED:
        return _unsatisfied(harness)

    try:
        if harness == "opencode":
            path = _plugin_path(root, owner)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                _plugin_source(owner, harness, command, OPENCODE_EVENTS),
                encoding="utf-8",
            )
            installed = path.exists()
            entries = len(OPENCODE_EVENTS) if installed else 0
        else:
            path = _harness_file(harness, root)
            events = _events(harness)
            _write_json(
                path,
                _converge_hooks(_read_json(path), owner, harness, command, events),
            )
            entries = _count_hooks(_read_json(path), owner)
            installed = entries == len(events)
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


def health(owner: str, harness: str, root: Path) -> dict[str, Any]:
    """Report what *harness* actually holds of *owner*'s integration right now."""

    if harness not in SUPPORTED:
        return _unsatisfied(harness)

    try:
        if harness == "opencode":
            entries = len(OPENCODE_EVENTS) if _plugin_path(root, owner).exists() else 0
            expected = len(OPENCODE_EVENTS)
        else:
            entries = _count_hooks(_read_json(_harness_file(harness, root)), owner)
            expected = len(_events(harness))
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
