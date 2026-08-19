# Kntnt Skills

[![License](https://img.shields.io/github/license/Kntnt/skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/skills)](https://github.com/Kntnt/skills/releases/latest)

AI Agent Skills Collection by Kntnt Sweden AB

## Description

This repository is a collection of [Agent Skills](https://agentskills.io) for coding harnesses: Claude Code, OpenCode, Codex, and others that load skills from a well-known directory. It ships the skills, the shared scripts they call, and a manager named `kntnt`. It does not ship harness `commands/` files. What you type is a skill name (`/commit`, `/push`); the same gesture works in every harness you have.

`npx skills add Kntnt/skills` puts only `kntnt` on disk. The other skills stay off disk until you check them in `/kntnt select`. You are never asked which harnesses to target: every skill you Enable is applied to every harness present on the machine, worked out on each run, so the set does not drift between Claude and OpenCode — and a harness you install next month is picked up by the next `/kntnt update` with nothing to configure. Where a skill goes is not a choice; which skills you Enable is.

There are two layers. Global is the set on this machine. Project is extras for one working directory. A harness in that directory loads the union of both. A Project cannot hide a Global skill. Project extras live as skill files in that project's harness directories; a teammate who checks those files in receives the extras, not your Global set.

A new catalog entry is never enabled without your say-so. It is on the list `/kntnt select` prints as soon as the collection carries it, and `/kntnt update` reports it and asks whether to enable it — at the moment you are already thinking about the collection, rather than leaving you to reach for a second command. `--yes` answers that question yes, as it answers every question here, so an unattended `/kntnt update --yes` does enable what the collection has added since your last one; every name it enabled is in its report.

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

That command is the transport. It does not offer the rest of the collection in a picker; `/kntnt select` is how the rest of it reaches your disk.

There is nothing to configure after it. In a harness that can see `kntnt`:

```
/kntnt select
```

You get the catalog as a list grouped by category, one row per skill, each with a checkbox that is checked when you already have that skill. You answer it in one sentence of plain text — *check commit and push, uncheck delegation* — so changing several skills is one reply rather than a walk through a menu, and you are asked to confirm once before anything is written. It is the same command later: reading what you have and changing it are the same gesture, not two verbs with a transcription step between them. There is no picker and there will not be one — a skill's script has no terminal to draw in, and a widget belonging to one harness would make this collection behave differently depending on where you ran it. Pass `--project` to list and change the current working directory instead of the machine.

That command works out where to write on its own: every harness with a home in that layer — `~/.claude`, `~/.config/opencode`, and so on for Global; `.claude`, `.crush` and their like for a Project. If it finds none, it writes to the shared `.agents/skills` directory alone, and never creates a directory for a harness you have not installed.

## Usage

Bare `/kntnt` is Help. The manager subcommands are:

| Command | What it does |
|---|---|
| `/kntnt help [command]` | Help for the manager or one of its verbs |
| `/kntnt select [--on <skill>]… [--off <skill>]… [--project]` | List what the collection has and change it in the same answer |
| `/kntnt update [--project]` | Refresh this collection and re-check dependencies |
| `/kntnt uninstall` | Remove this collection from this machine, manager last |

Select shows one layer and changes that one: Global bare, this working directory with `--project`. Reading it is never a side-effecting act, so an answer that changes nothing writes nothing. A skill whose files reached only some of your harnesses is shown checked and marked incomplete, and confirming the list repairs it; one whose files differ from the ones the collection ships is marked deviating, never *out of date*. What it is compared against is a digest: every catalog entry carries a content digest of the skill's directory as the collection ships it, and the same computation over what is on your disk answers the one freshness question this manager can answer honestly — are these the same files. A digest sees two states and no history, so it cannot say which way a difference runs, and outside a project copy that has fallen behind the likelier cause is an edit of your own, so the offer to re-copy says in the same breath that it overwrites that edit. The list is read from the collection itself, so a skill published upstream this morning is on it — and checkable — this afternoon, with no `/kntnt update` in between. When the collection cannot be reached, the list comes from the copy stored beside the manager and says so.

Any row can be read in full before you answer it. Ask for a skill's help and you get the manpage that skill ships — read from your own copy where you have one, and fetched from the collection where you do not — so deciding whether to enable something never means installing it first. Where you have no copy and the collection cannot be reached, you are told that rather than shown an invented page. Asking is not answering: nothing is written, and the list is still open.

The list carries the structure between skills as well as the skills. One that needs another of this collection is shown locked while that other is unchecked, and the row names what to check instead, so you can see why you cannot have it yet. Check it anyway and what it needs comes with it: you are asked one yes/no question naming exactly what would be added, once for the whole chain — checking `release` where you have neither `push` nor `commit` is a single yes rather than one question per level — and nothing is written until you have answered it. Unchecking a skill that another checked skill depends on is reported, not blocked: you are told what it leaves unsatisfied, and your answer stands.

A machine can also be set up with nobody at the list. `--on <skill>` and `--off <skill>` name skills directly and open none, as often as you have names and in either combination in one invocation. They apply a change rather than a whole set: a skill you do not name keeps the state it had, files included, so nothing is re-copied over an edit of yours under a command that named something else. What a named skill needs comes with it, and you are asked once before it does. `--off` deletes files, so the script refuses it without `--yes`. `--yes` given with neither of them is an instruction of its own: open no list, enable nothing you had not already enabled, and put what you have into good order — refresh what deviates, repair what is incomplete. That is the deliberate opposite of `/kntnt update --yes`, which does enable the collection's new entries: there you pointed the verb at the collection, and here nobody was asked whether they wanted the skill.

Every command here reads `--project` the same way: `--project` or `--project=on` means the Project, and nothing or `--project=off` means Global. Select and Update change that layer, and Select is also what lists it; Uninstall takes no `--project` at all. Update refreshes this collection only, and only what has moved: it compares each enabled skill against the digest its catalog entry carries and leaves alone the ones that already hold the collection's own files, so the report says what changed rather than how much you had enabled — and a skill it does re-copy loses any local edit you made to it. The manager is refreshed every time, since no catalog entry describes it and it is the verb that repairs the rest. It reports each new catalog skill and asks whether to enable it; a no leaves it Disabled, and `--yes` is a yes. It deletes a skill that has been withdrawn from the collection upstream, and does not ask: such a skill can no longer be updated or supported, and no other command here could reach it. It does not refresh a skill that came from another collection, and never deletes one: it recognises its own by a marker each carries in its own frontmatter. If a dependency is missing, it tells you how to satisfy it and does not install anything.

`--yes` works the same on every skill here: whatever could be answered yes or no is answered yes instead of asked.

`--dry-run` lets you watch a change happen before you let it happen. Select, Update, and Uninstall each accept it, and the run is the real one: the same code, the same transport, the same reading of the disk afterwards — only against a temporary home seeded with this collection's files as they are now, which is thrown away when the run ends. What you get back is the outcome rather than a description of it, and nothing on your machine has moved. It has an npm cache of its own, so it downloads the transport afresh and takes noticeably longer than the run it is previewing; the report says so before the wait. The confirmation each of those commands asks for anyway is the cheap way to see what is about to happen, and it is not this.

`/kntnt uninstall` is the way out, and the mirror of the one command that installed this. It removes every enabled catalog skill from every harness on the machine and then the manager itself, so there is nothing left for your harness's own uninstall to do. The manager goes last and only if everything else went: a run that leaves a skill behind keeps `kntnt`, because it is the only thing that can be asked to finish. It takes no `--project`: skills in a working directory are checked into that repository and travel with it, so they are left alone and the report says so. It deletes files, so it asks first — `--yes` answers.

Enabled skills are invoked by their own names, not as `/kntnt <name>`. Each one answers `--help` — `-h` and `help` too — with the manpage it ships beside itself, so a skill in front of you can be asked what it does without knowing which collection it arrived from. That, and the `select` list, are the two ways to a skill's help: the manager documents its own verbs and no skill.

### agents-md

Create, shrink, or tend `AGENTS.md` and `agents.d/`. After a task it writes only facts the next session cannot discover from the repo. Default is to write nothing. Run it on demand with `/agents-md` or `--force`.

### delegation

Turn delegation mode on or off: while it is on, the agent orchestrates — thinks, plans, briefs, verifies — and subagents execute on the cheapest model able to do the job. `/delegation` toggles it for this session; add `project` or `user` with `on` or `off` to make it standing, and the skill writes the mode as a managed block into the context file your harness already loads, after showing you the file and the exact insertion. `/delegation status` reports all three scopes. It never changes your model or effort. It needs a harness that can spawn subagents, and refuses in one that cannot.

### tldr

Summarise what was just said, and keep replies short by default. Typed bare, `/tldr` gives you back everything the agent has written since you last spoke, in three parts — what happened, what it decided on your behalf, and what needs you — with the last part present even when the answer is *nothing needs you*. Anything you type after it is a free-form instruction in any language, so `all` widens the range, `engelska` picks a language, and `bara säkerhetsdelen` narrows the focus. `/tldr --on` switches on TL;DR mode, so replies are short from the outset and the closing verdict arrives without your asking; `--user` makes that standing, `--status` reports it, and `--off` takes it back. The mode is a managed block in the context file your harness already loads rather than a Claude Code output style, so it works everywhere and takes effect on the turn that switches it on. It has no project scope, and it governs what the agent says to you and never what it writes into files.

### commit

Reconcile `CHANGELOG.md` `[Unreleased]`, propose a `.gitignore` when the project has none, then stage the whole working tree (`git add -A`) and commit. The agent proposes a subject line from the changelog (or the diff) unless you pass `"message"`. It shows the plan and waits unless you pass `--yes`.

### push

Follow `commit`, then push the current branch. Same `"message"` and `--yes` as `commit`. If the tree is clean it only pushes.

### release

Ship a version from the default branch: reconcile `CHANGELOG.md`, bump, follow `push`, tag `HEAD`, and open a GitHub release. If the project has a conventional archive script, build it and attach the zip. Pass `minor`, `major`, or `X.Y.Z` to force the bump; otherwise the bump comes from `[Unreleased]`. `--no-build` skips the archive. `gh` is required only for the GitHub release step.

`tldr` needs nothing at all — no binary, no capability, no other skill — and is the only skill here that runs on a machine without `uv`. `commit`, `push`, `release`, and `agents-md` need `git`; `release` also needs `gh` for the GitHub release step; `delegation` needs a harness that can spawn subagents. `push` needs `commit` and `release` needs `push`, and a dependency on another skill of this collection is the one kind `/kntnt select` can supply — it names it on the row and offers to add it. A binary, another collection's skill, and a harness capability are yours to satisfy: the skill that wants one does no work without it and prints how to fix it.

## License

Apache License 2.0. See [LICENSE](LICENSE). How to contribute is in [CONTRIBUTING.md](CONTRIBUTING.md).
