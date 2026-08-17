# Kntnt Skills

[![License](https://img.shields.io/github/license/Kntnt/skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/skills)](https://github.com/Kntnt/skills/releases/latest)

AI Agent Skills Collection by Kntnt Sweden AB

## Description

This repository is a collection of [Agent Skills](https://agentskills.io) for coding harnesses: Claude Code, OpenCode, Codex, and others that load skills from a well-known directory. It ships the skills, the shared scripts they call, and a manager named `kntnt`. It does not ship harness `commands/` files. What you type is a skill name (`/commit`, `/push`); the same gesture works in every harness you have.

`npx skills add Kntnt/skills` puts only `kntnt` on disk. The other skills stay off disk until you Enable them. You are never asked which harnesses to target: every skill you Enable is applied to every harness present on the machine, worked out on each run, so the set does not drift between Claude and OpenCode — and a harness you install next month is picked up by the next `/kntnt update` with nothing to configure. Where a skill goes is not a choice; which skills you Enable is.

There are two layers. Global is the set on this machine. Project is extras for one working directory. A harness in that directory loads the union of both. A Project cannot hide a Global skill. Project extras live as skill files in that project's harness directories; a teammate who checks those files in receives the extras, not your Global set.

New catalog entries stay Disabled after an Update. Enable them when you want them.

A few skills need something of the harness itself rather than of your machine — `delegation` is pointless where subagents cannot be spawned. Those requirements are dependencies like any other, not an install-time filter: the skill is enabled on every harness you have, and in one that cannot meet the requirement it says so and does nothing. No script can test this, since the manager cannot know which harness invoked it; the agent answers, because the agent is the harness.

## Recommended skills and collections of skills

None of these is required. They are the skills and collections that sit well beside this one, listed as a courtesy rather than as a checklist. A skill here that genuinely needs something else declares that dependency itself, and tells you what to do about it when you run it — so this list never has to be the place you find out.

- [Skills for Real Engineers](https://github.com/mattpocock/skills) if you want a full engineering and productivity set alongside these
- [Improve](https://github.com/shadcn/improve) if you want a codebase surveyed before you change it
- [No AI Slop](https://github.com/petergyang/no-ai-slop) if you want your prose to stop reading as machine-written
- [agent-browser](https://github.com/vercel-labs/agent-browser) if a task needs a real browser
- [Cloudflare Skills](https://github.com/cloudflare/skills) if you work with Cloudflare
- [Impeccable](https://github.com/pbakaus/impeccable) if you work with web design

## Installation

The manager and the skills run their scripts with [uv](https://docs.astral.sh/uv/). If `uv` is missing, they stop and tell you to install it.

```
npx skills add Kntnt/skills
```

That command is the transport. It does not offer the rest of the collection in a picker; Enable is how those skills become Enabled.

There is nothing to configure after it. In a harness that can see `kntnt`:

```
/kntnt enable
```

Omit the names and you get a picker grouped by category. Add or drop skills the same way later, with `/kntnt enable` and `/kntnt disable`. Pass `--project` to change only the current working directory.

Each of those commands works out where to write on its own: every harness with a home in that layer — `~/.claude`, `~/.config/opencode`, and so on for Global; `.claude`, `.crush` and their like for a Project. If it finds none, it writes to the shared `.agents/skills` directory alone, and never creates a directory for a harness you have not installed.

## Usage

Bare `/kntnt` is Help. The manager subcommands are:

| Command | What it does |
|---|---|
| `/kntnt help [skill]` | Help for the manager, or one named skill |
| `/kntnt status [skill...]` | Report Enabled or Disabled in Global and Project |
| `/kntnt enable [--project] [skill...]` | Enable skills (picker if none named) |
| `/kntnt disable [--project] [skill...]` | Disable skills (picker if none named) |
| `/kntnt update [--project]` | Refresh this collection and re-check dependencies |

Status with no names lists every skill in the catalog, Disabled ones included — that is how you find what there is to enable. The catalog ships with the manager, so a skill added upstream since your last `/kntnt update` appears only after you run it.

Enable, Disable, and Update default to Global. `--project` or `--project=on` targets the Project; `--project=off` targets Global. Update refreshes this collection only. It reports each new catalog skill and leaves it Disabled. It deletes a skill that has been withdrawn from the collection upstream, and does not ask: such a skill can no longer be updated or supported, and no other command here could reach it. It does not refresh a skill that came from another collection. If a dependency is missing, it tells you how to satisfy it and does not install anything.

`--yes` works the same on every skill here: whatever could be answered yes or no is answered yes instead of asked.

Enabled skills are invoked by their own names, not as `/kntnt <name>`.

### agents-md

Create, shrink, or tend `AGENTS.md` and `agents.d/`. After a task it writes only facts the next session cannot discover from the repo. Default is to write nothing. Run it on demand with `/agents-md` or `--force`.

### delegation

Turn delegation mode on or off: while it is on, the agent orchestrates — thinks, plans, briefs, verifies — and subagents execute on the cheapest model able to do the job. `/delegation` toggles it for this session; add `project` or `user` with `on` or `off` to make it standing, and the skill writes the mode as a managed block into the context file your harness already loads, after showing you the file and the exact insertion. `/delegation status` reports all three scopes. It never changes your model or effort. It needs a harness that can spawn subagents, and refuses in one that cannot.

### commit

Reconcile `CHANGELOG.md` `[Unreleased]`, propose a `.gitignore` when the project has none, then stage the whole working tree (`git add -A`) and commit. The agent proposes a subject line from the changelog (or the diff) unless you pass `"message"`. It shows the plan and waits unless you pass `--yes`.

### push

Follow `commit`, then push the current branch. Same `"message"` and `--yes` as `commit`. If the tree is clean it only pushes.

### release

Ship a version from the default branch: reconcile `CHANGELOG.md`, bump, follow `push`, tag `HEAD`, and open a GitHub release. If the project has a conventional archive script, build it and attach the zip. Pass `minor`, `major`, or `X.Y.Z` to force the bump; otherwise the bump comes from `[Unreleased]`. `--no-build` skips the archive. `gh` is required only for the GitHub release step.

`commit`, `push`, `release`, and `agents-md` need `git`; `release` also needs `gh` for the GitHub release step; `delegation` needs a harness that can spawn subagents. If a dependency is unsatisfied, the skill does no work and prints how to fix it.

## License

Apache License 2.0. See [LICENSE](LICENSE). How to contribute is in [CONTRIBUTING.md](CONTRIBUTING.md).
