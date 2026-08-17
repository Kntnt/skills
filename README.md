# Kntnt Skills

[![License](https://img.shields.io/github/license/Kntnt/skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/skills)](https://github.com/Kntnt/skills/releases/latest)

AI Agent Skills Collection by Kntnt Sweden AB

## Description

This repository is a collection of [Agent Skills](https://agentskills.io) for coding harnesses: Claude Code, OpenCode, Codex, and others that load skills from a well-known directory. It ships the skills, the shared scripts they call, and a manager named `kntnt`. It does not ship harness `commands/` files. What you type is a skill name (`/commit`, `/push`); the same gesture works in every harness on your list.

`npx skills add Kntnt/skills` puts only `kntnt` on disk. The other skills stay off disk until you Enable them. You pick the harnesses once. Every skill Enabled in a layer is then applied to all of them, so the set does not drift between Claude and OpenCode.

There are two layers. Global is the set on this machine. Project is extras for one working directory. A harness in that directory loads the union of both. A Project cannot hide a Global skill. Project extras live as skill files in that project's harness directories; a teammate who checks those files in receives the extras, not your Global set.

New catalog entries stay Disabled after an Update. Enable them when you want them.

## Essential and recommended skills and skill sets

Essential skills on which Kntnt Skills depends:

- [Skills for Real Engineers](https://github.com/mattpocock/skills) (select engineering and productivity skills)
- [Improve](https://github.com/shadcn/improve)
- [No AI Slop](https://github.com/petergyang/no-ai-slop)
- [agent-browser](https://github.com/vercel-labs/agent-browser)

Other recommended skills or collections of skills:

- [Cloudflare Skills](https://github.com/cloudflare/skills) if you work with Cloudflare
- [Impeccable](https://github.com/pbakaus/impeccable) if you work with web design

## Installation

The manager and the skills run their scripts with [uv](https://docs.astral.sh/uv/). If `uv` is missing, they stop and tell you to install it.

```
npx skills add Kntnt/skills
```

That command is the transport. It does not offer the rest of the collection in a picker; Enable is how those skills become Enabled.

In a harness that can see `kntnt`:

```
/kntnt setup
```

Setup records the harness list. Detected harnesses are pre-checked; you can change the set. Adding a harness copies every skill already Enabled in Global onto it. Removing a harness asks before deleting this collection's files there. The first run then offers Enable so you can pick skills.

Later, add or drop skills with `/kntnt enable` and `/kntnt disable`. Omit the names and you get a picker grouped by category. Pass `--project` to change only the current working directory.

## Usage

Bare `/kntnt` is Status. The manager subcommands are:

| Command | What it does |
|---|---|
| `/kntnt status [skill...]` | Report Enabled or Disabled in Global and Project |
| `/kntnt setup` | Record the harness list |
| `/kntnt enable [--project] [skill...]` | Enable skills (picker if none named) |
| `/kntnt disable [--project] [skill...]` | Disable skills (picker if none named) |
| `/kntnt update [--project]` | Refresh this collection and re-check dependencies |
| `/kntnt help [skill]` | Help for the manager, or one named skill |

Enable, Disable, and Update default to Global. `--project` or `--project=on` targets the Project; `--project=off` targets Global. Update refreshes this collection only. It reports each new catalog skill and leaves it Disabled. It does not refresh a skill that came from another collection. If a dependency is missing, it tells you how to satisfy it and does not install anything.

Enabled skills are invoked by their own names, not as `/kntnt <name>`.

### agents-md

Create, shrink, or tend `AGENTS.md` and `agents.d/`. After a task it writes only facts the next session cannot discover from the repo. Default is to write nothing. Run it on demand with `/agents-md` or `--force`.

### delegation

Turn delegation mode on or off: while it is on, the agent orchestrates — thinks, plans, briefs, verifies — and subagents execute on the cheapest model able to do the job. `/delegation` toggles it for this session; add `project` or `user` with `on` or `off` to make it standing, and the skill writes the mode as a managed block into the context file your harness already loads, after showing you the file and the exact insertion. `/delegation status` reports all three scopes. It never changes your model or effort.

### commit

Reconcile `CHANGELOG.md` `[Unreleased]`, propose a `.gitignore` when the project has none, then stage the whole working tree (`git add -A`) and commit. The agent proposes a subject line from the changelog (or the diff) unless you pass `"message"`. It shows the plan and waits unless you pass `--yes`.

### push

Follow `commit`, then push the current branch. Same `"message"` and `--yes` as `commit`. If the tree is clean it only pushes.

### release

Ship a version from the default branch: reconcile `CHANGELOG.md`, bump, follow `push`, tag `HEAD`, and open a GitHub release. If the project has a conventional archive script, build it and attach the zip. Pass `minor`, `major`, or `X.Y.Z` to force the bump; otherwise the bump comes from `[Unreleased]`. `--no-build` skips the archive. `gh` is required only for the GitHub release step.

`commit`, `push`, `release`, and `agents-md` need `git`. If a dependency is unsatisfied, the skill does no work and prints how to fix it.

## License

Apache License 2.0. See [LICENSE](LICENSE). How to contribute is in [CONTRIBUTING.md](CONTRIBUTING.md).
