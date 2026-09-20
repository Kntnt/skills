# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""How a chosen point is actually started.

Choosing a model is arithmetic; reaching it is plumbing, and the two are kept
apart so that neither has to know much about the other. A harness can start a
model three ways. Claude Code starts an Anthropic model as a subagent, which
is why this module also generates the agent definitions that make those
subagents exist. Anything the Codex or opencode CLI can reach is started as a
command. Everything else is not reachable at all, and the honest answer there
is `inherit`: let the caller do the work in the seat it already occupies,
rather than hand it a command that will fail in somebody else's terminal.

A Codex or headless-Claude bridge command also carries the caller's own
permission level across to the other tool, because a delegated run inherits
what the caller was running at unless the caller says otherwise — the same
inheritance model and deliberation already have, where an explicit choice wins
and silence means inheritance. The vocabulary is this module's: a closed set of
harness-neutral names, each translated into the spelling of the CLI being
started. Silence names no flag at all, which leaves the started CLI at the
user's own configuration for that tool.

`plan` never raises and never returns None, because it is called from inside a
decision that has already been made. An unreachable point degrades the launch,
never the answer.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path

from catalogue import Catalogue, Model
from profiles import Profile, channel_for

# The prefix every generated agent definition carries, in both its file name
# and its `name`. It is what tells `sync_definitions` which files in somebody
# else's agents directory are this Skill's to rewrite and delete.
PREFIX = "kntnt"

# The providers each bridge can reach. Codex speaks to OpenAI alone; opencode
# is a front end for whatever the user has configured behind it, so it is
# limited here only by the makers the profile chooses.
CODEX_PROVIDERS = frozenset({"openai"})

# The providers the Claude CLI can reach in its headless form. This is the path
# a process takes to an Anthropic model — from another Harness, or from a script
# of this Skill's own, neither of which can spawn a subagent. On Claude Code
# itself the native subagent path is tried first and wins.
CLAUDE_PROVIDERS = frozenset({"anthropic"})

# Where a bridge command runs when the caller named no repository. The Codex
# CLI insists on a directory, and the caller's own is the only one this module
# can name without inventing a path that may not exist.
HERE = "."


@dataclass(frozen=True)
class Launch:
    """How to start one chosen point, in the terms the caller acts on."""

    how: str
    subagent_type: str | None
    command: tuple[str, ...] | None
    note: str | None


@dataclass(frozen=True)
class SyncReport:
    """What `sync_definitions` did to the agents directory."""

    written: list[str]
    unchanged: list[str]
    removed: list[str]
    created_directory: bool


@dataclass(frozen=True)
class Permission:
    """One permission level, spelled as the Claude and Codex CLIs spell it."""

    claude: tuple[str, ...]
    codex: tuple[str, ...]


# The permission levels a caller may say it is running at, and what each one
# becomes on either bridge. The names are this module's own and belong to no
# tool: a caller states the level it reads off itself, and the translation into
# a CLI's spelling happens here and nowhere else. The set is closed and is
# exhaustive as this is written; a level a CLI grows later is added here with
# the nearest equivalent on the other side, and the bridge's docstring says why
# that one is the nearest.
#
# Two pairs coincide on the Codex side, where the sandbox is what decides an
# unattended `exec`: `edits` and `never-ask` both reach it as the writable
# workspace, and `manual` and `plan` both as the sandbox that cannot write.
# Neither level sets an approval policy — `_codex` says why.
#
# Read from `claude --help` (Claude Code 2.1.278) and `codex exec --help`
# (codex-cli 0.155.1) on 2026-09-20. Re-read both when either is upgraded: a
# flag a CLI does not have is refused before the model is reached.
PERMISSIONS: Mapping[str, Permission] = {
    "bypass": Permission(
        claude=("--permission-mode", "bypassPermissions"),
        codex=("--dangerously-bypass-approvals-and-sandbox",),
    ),
    "auto": Permission(
        claude=("--permission-mode", "auto"),
        codex=("--approve-for-me",),
    ),
    "edits": Permission(
        claude=("--permission-mode", "acceptEdits"),
        codex=("-s", "workspace-write"),
    ),
    "never-ask": Permission(
        claude=("--permission-mode", "dontAsk"),
        codex=("-s", "workspace-write"),
    ),
    "manual": Permission(
        claude=("--permission-mode", "manual"),
        codex=("-s", "read-only"),
    ),
    "plan": Permission(
        claude=("--permission-mode", "plan"),
        codex=("-s", "read-only"),
    ),
}


def plan(
    model: Model,
    deliberation: str | None,
    harness: str,
    profile: Profile,
    cat: Catalogue,
    *,
    repo: str | None,
    read_only: bool = False,
    permissions: str | None = None,
) -> Launch:
    """Return how to start *model* at *deliberation* from *harness*.

    `permissions` is the level the caller says it is itself running at, named
    in this module's own vocabulary, and a Codex or headless-Claude bridge
    command carries it across to the other tool in that tool's spelling; the
    opencode bridge carries none. Naming none is inheritance from the user's
    own configuration for the CLI being started, which is what a command with
    no permission flag leaves it at. A level this module does not know is
    answered as silence with a note naming it, never as a refusal: a caller
    that cannot read its own level off itself is exactly the caller that most
    needs an answer, and nothing here is a status meaning *start nothing*
    (ADR-0182).

    `read_only` outranks the level entirely. A read-only call is the grader's
    own posture — it reads two excerpts and answers — so it keeps the sandbox
    and the tool list that grant no way to write whatever level came with it,
    and its command is byte for byte what it was before any level existed.

    The order is deliberate: the native path first, then the bridges, then the
    admission that there is no path. A point the caller cannot start is worth
    saying out loud, because the alternative is a command that fails later and
    further away from the decision that produced it.

    `cat` is part of the signature because every planner in this Skill is
    handed the world it plans against; reaching one already chosen model needs
    nothing else looked up in it.
    """

    if permissions is None or permissions in PERMISSIONS:
        return _reached(
            model,
            deliberation,
            harness,
            profile,
            cat,
            repo=repo,
            read_only=read_only,
            permissions=permissions,
        )

    unknown = (
        f"{permissions!r} is no permission level this module knows, so the launch "
        "names none and the started CLI follows the user's own configuration"
    )
    started = _reached(
        model,
        deliberation,
        harness,
        profile,
        cat,
        repo=repo,
        read_only=read_only,
        permissions=None,
    )
    return replace(
        started,
        note=unknown if started.note is None else f"{started.note}; {unknown}",
    )


def _reached(
    model: Model,
    deliberation: str | None,
    harness: str,
    profile: Profile,
    cat: Catalogue,
    *,
    repo: str | None,
    read_only: bool,
    permissions: str | None,
) -> Launch:
    """Return the launch itself, for a level already known to be one of ours."""

    # The native path. A subagent exists only where `definitions` generated
    # one, which is per family and per supported level, so a level this model
    # does not support has no agent to name and is not claimed as reachable.
    if harness == "claude-code" and model.provider == "anthropic":
        subagent = agent_name(model, deliberation)
        if subagent is not None:
            return Launch("claude-code-agent", subagent, None, None)
        return Launch(
            "inherit",
            None,
            None,
            f"{model.id} has no generated agent for deliberation {deliberation!r}",
        )

    if model.provider in CODEX_PROVIDERS and "codex" in profile.harnesses:
        return Launch(
            "bridge-command",
            None,
            _codex(model, deliberation, repo, read_only, permissions),
            None,
        )

    if model.provider in CLAUDE_PROVIDERS and "claude-code" in profile.harnesses:
        return Launch(
            "bridge-command",
            None,
            _claude(model, deliberation, repo, read_only, permissions),
            None,
        )

    if "opencode" in profile.harnesses and model.provider in profile.makers:
        return _through_opencode(model, deliberation, profile, repo)

    return Launch("inherit", None, None, _unreachable(model, harness, profile))


def agent_name(model: Model, deliberation: str | None) -> str | None:
    """Return the subagent this point is launched as, or None where none exists.

    A model with no effort control at all — Anthropic publishes one — has
    exactly one point rather than five, and its definition carries no level in
    its name because there is no level to name.
    """

    if not model.deliberation:
        return f"{PREFIX}-{model.family}" if deliberation is None else None
    if deliberation in model.deliberation:
        return f"{PREFIX}-{model.family}-{deliberation}"
    return None


def definitions(profile: Profile, cat: Catalogue) -> dict[str, str]:
    """Return the agent-definition matrix, keyed by file name.

    One definition per Anthropic model and supported level wherever the
    profile chooses Anthropic as a maker, because Claude Code selects a model
    by naming a subagent and nothing else. Every model the maker offers gets
    its files, since no single model is chosen within a maker (ADR-0190), and
    none needs a channel: Anthropic is the provider a Claude Code seat already
    pays for. A profile that does not choose Anthropic defines none. Two
    Anthropic models in one family would want the same file name; the newer
    one takes it, which is the same rule `resolve` applies to an ambiguous
    alias.
    """

    ordered = sorted(
        (model for model in cat.models if _generates_an_agent(model, profile)),
        key=lambda model: (model.released or "", model.id),
        reverse=True,
    )

    matrix: dict[str, str] = {}
    for model in ordered:
        for level in model.deliberation or (None,):
            name = agent_name(model, level)
            if name is not None:
                matrix.setdefault(f"{name}.md", _definition(model, level))
    return matrix


def sync_definitions(dest: Path, wanted: Mapping[str, str]) -> SyncReport:
    """Make *dest* hold exactly the wanted definitions, and nothing else of ours.

    Only files matching the Skill's own prefix are ever removed. The directory
    belongs to the user and to every other tool that writes agents into it, so
    a file this Skill did not generate is not this Skill's to delete.
    """

    created = not dest.is_dir()
    dest.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    unchanged: list[str] = []
    for name in sorted(wanted):
        path = dest / name
        if path.is_file() and path.read_text(encoding="utf-8") == wanted[name]:
            unchanged.append(name)
            continue
        path.write_text(wanted[name], encoding="utf-8")
        written.append(name)

    removed: list[str] = []
    for path in sorted(dest.glob(f"{PREFIX}-*.md")):
        if path.name not in wanted:
            path.unlink()
            removed.append(path.name)

    return SyncReport(written, unchanged, removed, created)


def _generates_an_agent(model: Model, profile: Profile) -> bool:
    """Return whether this model is one Claude Code can be taught to start."""

    return model.provider == "anthropic" and model.provider in profile.makers


def _definition(model: Model, level: str | None) -> str:
    """Return the complete agent-definition file for one point.

    A model with no effort control gets no `effort:` line, because a line
    naming a level the model does not have is a line the harness either
    rejects or silently ignores, and neither is worth generating.

    Claude Code honours both lines, verified against Claude Code 2.1.263: from
    a session running at `xhigh`, subagents spawned from these definitions ran
    at the model and the level their own file named — `claude-opus-5` at `low`
    and `claude-sonnet-5` at `high` on every assistant line of their
    transcripts — rather than at the parent session's. That is what lets
    evidence accrue to the level the answer chose (issue #297), which the
    deliberation ladder rests on entirely: a level nothing ever ran at is
    worth nothing. Re-verify it against a later version before trusting it
    there.
    """

    at = f" at {level} deliberation" if level else ""
    effort = f"effort: {level}\n" if level else ""
    return (
        "---\n"
        f"name: {agent_name(model, level)}\n"
        f"description: Delegated work on {model.id}{at}.\n"
        f"model: {model.id}\n"
        f"{effort}"
        "---\n"
        "\n"
        f"This file is generated by the Model Selector Skill. It launches {model.id}"
        f"{at} and exists so that Claude Code has a subagent to name for that "
        "point. Editing it is pointless: the daily catalogue pass and "
        "`/model-selector setup` rewrite this directory from the catalogue and the "
        "profile, and every change made here is lost the next time either runs.\n"
    )


# The Codex CLI's own `model_reasoning_effort` stops at `xhigh`, though the API
# behind it accepts `max`. That is a property of the bridge rather than of the
# model, so the highest level a caller can ask for arrives here and has to be
# spent on the highest the command line can actually carry.
CODEX_TOP = "xhigh"


def _codex(
    model: Model,
    deliberation: str | None,
    repo: str | None,
    read_only: bool = False,
    permissions: str | None = None,
) -> tuple[str, ...]:
    """Return the Codex CLI command that starts one point.

    A `max` point launches at `xhigh` because the CLI accepts nothing higher.
    The answer still names `max`, which is what the point was chosen as and
    what evidence should accrue to; a caller who needs the difference reaches
    the API rather than this command.

    The git check is skipped because the directory belongs to the caller. Codex
    refuses outright — in milliseconds, before the model is reached — where it
    is neither a git repository nor one somebody has told the CLI to trust, and
    a Skill that plans a launch has no way to know which the caller's is. The
    grader is the case that proves it: it runs from a home directory on purpose,
    so that no process it starts holds a working directory this collection may
    replace under it, and every judge call it made was refused for that reason
    alone.

    A read-only call is given a sandbox that cannot write, whatever level came
    with it. Otherwise the caller's own level decides, and naming none names no
    flag: `codex exec` then follows the user's own `~/.codex/config.toml`,
    which on a machine setting `sandbox_mode` there is what the user chose and
    on one setting nothing is the CLI's own default. Silence is inheritance
    from that configuration and never a promise of write access; a role that
    has to write is given a level by its caller.

    Every claim below was read or tried against codex-cli 0.155.1 on
    2026-09-20. `codex exec` does have an approval flag, `--approve-for-me`,
    and `auto` is exactly it: it routes approval requests through an automatic
    review rather than to a person, so it cannot leave an unattended start
    waiting on somebody who is not there. The CLI refuses it beside a sandbox —
    `--approve-for-me -s read-only` exits 2 with *the argument
    '--approve-for-me' cannot be used with '--sandbox <SANDBOX_MODE>'* before
    anything runs — so that is the one row carrying no `-s`.

    No level reaches the approval policy through `-c approval_policy=`, and no
    command built here contains it. `untrusted` is refused by this version
    outright (*approval_policy = "untrusted" is no longer supported; remove
    this setting*), and `on-request` or `on-failure` set that way have no
    automatic reviewer behind them, so either can leave an unattended start
    waiting on an approval nobody can answer. That is why `manual` is `-s
    read-only` and not an approval policy: nothing in this CLI means *ask a
    person first*, and the faithful outcome of a level that would have asked,
    in a start with nobody to ask, is a start that cannot write — the same
    command `plan` gets, and the closest equivalent there is. `edits` and
    `never-ask` coincide for the same reason from the other side: with no
    policy set, the sandbox is the whole of what decides an unattended `exec`,
    so both are the writable workspace.
    """

    effort = CODEX_TOP if deliberation == "max" else deliberation or "medium"
    spelled = () if permissions is None else PERMISSIONS[permissions].codex
    return (
        "codex",
        "exec",
        "-C",
        repo or HERE,
        "--skip-git-repo-check",
        "-m",
        model.id,
        "-c",
        f"model_reasoning_effort={effort}",
        *(("-s", "read-only") if read_only else spelled),
        "--json",
    )


def _claude(
    model: Model,
    deliberation: str | None,
    repo: str | None,
    read_only: bool = False,
    permissions: str | None = None,
) -> tuple[str, ...]:
    """Return the headless Claude CLI command that starts one point.

    A model with no effort control takes no effort flag, which is the same
    absence a generated agent definition expresses by leaving the line out. A
    read-only call is given an empty tool list, which is what this CLI offers
    for a call that is to answer and touch nothing, and that is the only thing
    `--tools` is ever used for here.

    The caller's own level travels as `--permission-mode`, whose six values in
    Claude Code 2.1.278 are exactly this module's six levels, so the mapping is
    one to one in both directions. `plan` is that mode rather than a
    description of one: a session in it cannot edit, which is the whole of what
    the level promises. A read-only call takes no level at all, its own form
    already granting no way to write.

    Naming no level names no flag, and the start then follows whatever the user
    set: `permissions.defaultMode` in their own settings where they set one,
    and otherwise this CLI's own headless default, which the tool's
    documentation gives as manual on every plan for `-p` (Claude Code 2.1.278,
    read 2026-09-20). Silence is inheritance from configuration and never a
    promise of write access.

    The order is load-bearing. The caller appends its prompt to this command,
    and `--add-dir` and `--tools` each take a variable number of values, so a
    command ending in one of them would swallow the prompt as another value.
    Every point therefore ends on a flag that takes exactly one: the effort
    level where the model has one, and the model identity where it has not.
    `--permission-mode` takes exactly one value and is placed before both, so
    the tail the rule is about is the same tail it always was.
    """

    command = ["claude", "-p", "--add-dir", repo or HERE]
    if read_only:
        command += ["--tools", ""]
    elif permissions is not None:
        command += list(PERMISSIONS[permissions].claude)
    command += ["--model", model.id]
    if deliberation is not None:
        command += ["--effort", deliberation]
    return tuple(command)


def _through_opencode(
    model: Model, deliberation: str | None, profile: Profile, repo: str | None
) -> Launch:
    """Return how opencode starts one point, as the channel paying for it routes it.

    The paying channel is the profile's opencode channel for this model's
    provider, matched exactly rather than through `channel_for`'s fallback: a
    gateway on some other harness's channel says nothing about what opencode
    is configured to reach. Where that channel names a gateway, the model is
    named the way the gateway routes it, by the slug the catalogue records for
    that gateway; with no slug recorded there is no route to name, and a guess
    would be a command that fails later and further away, so the point is
    inherited. A channel with no gateway, or no opencode channel at all, keeps
    the provider's own name.
    """

    gateway = next(
        (
            channel.gateway
            for channel in profile.channels
            if channel.harness == "opencode" and channel.provider == model.provider
        ),
        None,
    )
    if gateway is None:
        route = f"{model.provider}/{model.id}"
    elif (slug := dict(model.gateways).get(gateway)) is not None:
        route = f"{gateway}/{slug}"
    else:
        return Launch(
            "inherit",
            None,
            None,
            f"{model.id} has no slug recorded for the {gateway} gateway its opencode "
            "channel pays through, so opencode has no route to start it by",
        )

    return Launch("bridge-command", None, _opencode(route, deliberation, repo), None)


def _opencode(
    route: str, deliberation: str | None, repo: str | None
) -> tuple[str, ...]:
    """Return the opencode command that starts one point by its *route*.

    The flags are the ones `opencode run --help` lists, verified against
    opencode 1.18.30 (issue #308): the working directory is `--dir`, since the
    command refuses anything else before a model is reached, and the model is
    `<provider>/<model>` in opencode's own sense of provider, which for a
    gateway is the gateway and its slug. The level travels as `--variant`, so
    that a row recorded at a level ran at it; a point with no level passes
    none. The prompt is the trailing argument the caller appends: this module
    plans a launch rather than composing somebody else's brief.
    """

    command = ["opencode", "run", "--dir", repo or HERE, "--model", route]
    if deliberation is not None:
        command += ["--variant", deliberation]
    return tuple(command)


def _unreachable(model: Model, harness: str, profile: Profile) -> str:
    """Say why this point cannot be started, in terms the caller can act on."""

    if not profile.harnesses:
        return f"no harness detected on this machine, so {model.id} cannot be started"
    if channel_for(profile, model, harness) is None:
        return f"{harness} has no channel for {model.provider}, so {model.id} cannot be started"
    return f"{harness} has no way to start a {model.provider} model on this machine"
