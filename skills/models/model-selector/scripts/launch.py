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

`plan` never raises and never returns None, because it is called from inside a
decision that has already been made. An unreachable point degrades the launch,
never the answer.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from catalogue import Catalogue, Model
from profiles import Profile, channel_for

# The prefix every generated agent definition carries, in both its file name
# and its `name`. It is what tells `sync_definitions` which files in somebody
# else's agents directory are this Skill's to rewrite and delete.
PREFIX = "kntnt"

# The providers each bridge can reach. Codex speaks to OpenAI alone; opencode
# is a front end for whatever the user has configured behind it, so it is
# limited here only by what the profile says the user has.
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


def plan(
    model: Model,
    deliberation: str | None,
    harness: str,
    profile: Profile,
    cat: Catalogue,
    *,
    repo: str | None,
) -> Launch:
    """Return how to start *model* at *deliberation* from *harness*.

    The order is deliberate: the native path first, then the bridges, then the
    admission that there is no path. A point the caller cannot start is worth
    saying out loud, because the alternative is a command that fails later and
    further away from the decision that produced it.

    `cat` is part of the signature because every planner in this Skill is
    handed the world it plans against; reaching one already chosen model needs
    nothing else looked up in it.
    """

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
        return Launch("bridge-command", None, _codex(model, deliberation, repo), None)

    if model.provider in CLAUDE_PROVIDERS and "claude-code" in profile.harnesses:
        return Launch("bridge-command", None, _claude(model, deliberation, repo), None)

    if "opencode" in profile.harnesses and model.provider in profile.providers:
        return Launch("bridge-command", None, _opencode(model, repo), None)

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

    One definition per enabled Anthropic model and supported level, because
    Claude Code selects a model by naming a subagent and nothing else. Two
    enabled models in one family would want the same file name; the newer one
    takes it, which is the same rule `resolve` applies to an ambiguous alias.
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

    return model.provider == "anthropic" and model.id in profile.models


def _definition(model: Model, level: str | None) -> str:
    """Return the complete agent-definition file for one point.

    A model with no effort control gets no `effort:` line, because a line
    naming a level the model does not have is a line the harness either
    rejects or silently ignores, and neither is worth generating.
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
        "point. Editing it is pointless: `/model-selector update` rewrites this "
        "directory from the catalogue and the profile, and every change made here "
        "is lost the next time it runs.\n"
    )


# The Codex CLI's own `model_reasoning_effort` stops at `xhigh`, though the API
# behind it accepts `max`. That is a property of the bridge rather than of the
# model, so the highest level a caller can ask for arrives here and has to be
# spent on the highest the command line can actually carry.
CODEX_TOP = "xhigh"


def _codex(model: Model, deliberation: str | None, repo: str | None) -> tuple[str, ...]:
    """Return the Codex CLI command that starts one point.

    A `max` point launches at `xhigh` because the CLI accepts nothing higher.
    The answer still names `max`, which is what the point was chosen as and
    what evidence should accrue to; a caller who needs the difference reaches
    the API rather than this command.
    """

    effort = CODEX_TOP if deliberation == "max" else deliberation or "medium"
    return (
        "codex",
        "exec",
        "-C",
        repo or HERE,
        "-m",
        model.id,
        "-c",
        f"model_reasoning_effort={effort}",
        "-s",
        "workspace-write",
        "--json",
    )


def _claude(
    model: Model, deliberation: str | None, repo: str | None
) -> tuple[str, ...]:
    """Return the headless Claude CLI command that starts one point.

    A model with no effort control takes no effort flag, which is the same
    absence a generated agent definition expresses by leaving the line out.
    """

    command = ["claude", "-p", "--model", model.id, "--add-dir", repo or HERE]
    if deliberation is not None:
        command += ["--effort", deliberation]
    return tuple(command)


def _opencode(model: Model, repo: str | None) -> tuple[str, ...]:
    """Return the opencode command that starts one point.

    opencode names a model as `provider/model` and takes the prompt as its
    trailing argument, which the caller appends: this module plans a launch
    rather than composing somebody else's brief.
    """

    return (
        "opencode",
        "run",
        "--cwd",
        repo or HERE,
        "--model",
        f"{model.provider}/{model.id}",
    )


def _unreachable(model: Model, harness: str, profile: Profile) -> str:
    """Say why this point cannot be started, in terms the caller can act on."""

    if not profile.harnesses:
        return f"no harness detected on this machine, so {model.id} cannot be started"
    if channel_for(profile, model, harness) is None:
        return f"{harness} has no channel for {model.provider}, so {model.id} cannot be started"
    return f"{harness} has no way to start a {model.provider} model on this machine"
