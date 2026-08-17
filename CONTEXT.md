# Kntnt Skills

The domain of distributing, enabling, and updating a collection of Agent Skills across coding harnesses.

## Language

**Collection**:
The set of skills, shared scripts, and shared documents shipped from the `kntnt/skills` repository.
_Avoid_: package, plugin, marketplace, bundle

**Category**:
A folder under `skills/` in the collection repository that groups related skills. Status and interactive Enable list skills by Category. A Category is not part of the skill name and cannot be Enabled as a set.
_Avoid_: namespace, group, tag, section

**Skill**:
A standalone Agent Skill with its own name. Collection skills are not namespaced under `kntnt`. The collection ships skills only — never harness `commands/` files.
_Avoid_: module, plugin, recipe, command, slash command

**User-invoked skill**:
A skill the user starts by typing `/name`. Same gesture in every harness; the body is static instructions, not a preprocessed prompt template.
_Avoid_: command, slash command

**Model-invoked skill**:
A skill the model may load on its own when the task matches the skill's description.

**Manager**:
The always-enabled skill named `kntnt`. It is the collection's only namespaced entry point.
_Avoid_: installer, CLI, wrapper

**Setup**:
The manager subcommand that records the Harness list. Adding a Harness applies every skill Enabled in Global to it. Removing a Harness asks before deleting this collection's skills there. The first run may then hand off to Enable.
_Avoid_: init, configure, target

**Enable**:
The manager subcommand that makes one or more skills enabled. With no skill names it opens an interactive list. It targets Global unless `--project` or `--project=on` is given. It requires a Harness list.
_Avoid_: add, activate, install

**Disable**:
The manager subcommand that makes one or more skills disabled. With no skill names it opens an interactive list. It uses the same `--project` rule as Enable. It requires a Harness list.
_Avoid_: remove, uninstall

**Status**:
The manager subcommand that reports whether named skills are Enabled or Disabled in both Project and Global. With no skill names it reports every skill in the Catalog, Disabled ones included.
_Avoid_: list, info, doctor

**Update**:
The manager subcommand that refreshes this collection's skills and then checks every Dependency again. It reports each new Catalog entry; it does not Enable that skill and it does not ask. It does not refresh an External. Without `--project` it applies the Global layer; with `--project` it applies the Project layer.
_Avoid_: upgrade, sync, pull

**Help**:
The manager subcommand that prints help for the manager, or for one named collection skill. Bare `/kntnt` means Help.
_Avoid_: usage, man

**Assume yes**:
What `--yes` means on any collection skill: every question that can be answered yes or no is answered yes instead of asked. Every verb of a collection script accepts the flag, so a skill can pass the user's arguments through unread. Where a subcommand deletes files, the flag is also the gate — the script refuses without it, because a script cannot prompt.
_Avoid_: force, non-interactive, quiet, auto-approve

**Enabled**:
A skill present on disk in a layer, in each recorded harness's skills directory for that layer.
_Avoid_: active, installed, on, turned on (installed is what the transport does; enabled is the user's choice)

**Disabled**:
A skill that is not present on disk in that layer.
_Avoid_: inactive, off, uninstalled

**Catalog**:
The collection's declared list of its skills and their dependencies, authored in the repository and shipped with the Manager.
_Avoid_: manifest, registry, index, lockfile

**State**:
The user's remembered choices: which skills are Enabled in Global and in each Project. Reconstructable from disk; never the source of truth. The Harness list is not State.
_Avoid_: lockfile, config, preferences

**Harness list**:
The recorded Harnesses the collection targets. Setup writes it. If it is missing, the Manager rebuilds it from Harnesses that already have a Collection skill other than the Manager. A Harness that has only the Manager stays off the list until Setup. If the rebuild finds no such Harness, the Harness list is Unsatisfied — Enable, Disable, and Update stop. Status and Help still run.
_Avoid_: agent list, targets, setup file

**Global**:
The desired set and harness list that apply on this machine. Enable, Disable, and Update without `--project` change only this layer.
_Avoid_: user, machine, default (say global)

**Project**:
A working directory with its own extra desired set. Enable, Disable, and Update with `--project` change only this layer. They do not change Global. They cannot Disable a skill that is Enabled only in Global.
_Avoid_: repo, workspace, local

**Effective**:
The skills a Harness can load in the current directory: every skill Enabled in Global, plus every skill Enabled in this Project.
_Avoid_: available, active set, override

**Harness**:
A coding agent that loads Agent Skills from a well-known directory (Claude Code, OpenCode, Codex, and others).
_Avoid_: agent, IDE, tool, client

**Transport**:
The existing `npx skills` CLI, used to add, remove, and refresh skill files in harness directories.
_Avoid_: installer, package manager

**Dependency**:
A skill or runtime that another collection skill cannot work without.
_Avoid_: requirement, prerequisite

**External**:
A dependency whose source is another collection, not this one.
_Avoid_: third-party, upstream, peer

**Capability**:
A Dependency on what the running Harness can do rather than on what is on disk — spawning subagents, for one. No script can test one, because the Manager cannot know which Harness invoked it; the agent answers, being the Harness. The checker therefore reports the Capabilities a skill requires and the skill's own instructions make answering them part of the check. A skill declaring one is still Enabled everywhere; it refuses where the Capability is Unsatisfied.
_Avoid_: feature, harness flag, platform check, gate

**Satisfied**:
A dependency that is present and usable: the skill exists in the harness directory, the binary is on PATH, or the agent confirms the Capability of itself.
_Avoid_: installed, resolved, met

**Unsatisfied**:
A dependency that is missing. The dependent skill does no work; it only tells the user how to satisfy it.
_Avoid_: broken, missing (say unsatisfied)

**Ticket**:
A unit of work in the project's issue tracker. The Collection says Ticket and never the tracker's own word, so no skill is bound to one tracker.
_Avoid_: issue, story, task, PRD

**Plan**:
A file under `plans/` describing one unit of work, self-contained enough that an agent with no other context can carry it out. It states its own dependencies, scope boundaries, and done criteria.
_Avoid_: spec, brief, ticket, design doc

**Land**:
Bring one approved Plan's changes onto the branch the run started on, as one commit made by the `commit` skill, leaving no branch or worktree behind. A Plan is Landed or it is not; there is no halfway state.
_Avoid_: merge, integrate, ship, apply

**Drift**:
A Plan whose in-scope files changed after it was written, so its excerpts and steps may no longer describe the code. A run's own Landings are not Drift, because the run knows it made them.
_Avoid_: staleness, rot, conflict
