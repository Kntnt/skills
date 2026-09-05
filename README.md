# Kntnt Skills

[![License](https://img.shields.io/github/license/Kntnt/skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/skills)](https://github.com/Kntnt/skills/releases/latest)

You are in the right place if you want practical [agent skills](https://agentskills.io) for maintaining agent instructions, delegating work, shipping code, preparing tickets, editing prose, choosing AI models, and organizing accounting PDFs.

The collection works across Claude Code, Codex, OpenCode, and other harnesses. Its `kntnt` manager installs the skills you choose into every detected harness, while keeping machine-wide skills separate from project-specific ones.

## Quick start

Make sure you have the prerequisites in place: [uv](https://docs.astral.sh/uv/), [npx](https://docs.npmjs.com/cli/v8/commands/npx), and network access.

```sh
TODO
```

Install Kntnt Skills:

```sh
npx skills add Kntnt/skills
```

Open the catalog of available skills:

```text
/kntnt select
```

Choose the skills you want in plain text. You can ask to read any skill's help before confirming the list.

## Choose where skills apply

| Layer | Purpose | Command |
|---|---|---|
| Global | Make skills available on this machine | `/kntnt select` |
| Project | Add skills for the current working directory | `/kntnt select --project` |

A project can add to the global set but cannot hide a global skill. The manager detects harnesses on every run; if none is detected, it uses `.agents/skills`.

## Manage the collection

| Command | Result |
|---|---|
| `/kntnt` | Show manager help |
| `/kntnt select [--project]` | View the catalog and change enabled skills |
| `/kntnt select --on=<skill> --yes` | Enable a named skill without opening the list |
| `/kntnt update [--project]` | Refresh changed skills and handle catalog changes |
| `/kntnt uninstall` | Remove global skills and the manager |

Use `/kntnt help <command>` for manager details. Use `/<skill> --help` for an enabled skill.

`--dry-run` is available for select, update, and uninstall. `--yes` answers every yes-or-no question with yes; on update, that includes enabling new skills.

## Usage

These summaries help you choose a skill. Each skill's `--help` page contains its complete syntax, options, defaults, and failure behavior.

### agents-md

Keep a project's `AGENTS.md`, `CLAUDE.md`, and `agents.d/` concise and current. It records only useful facts that later sessions cannot discover elsewhere.

Run `/agents-md [--force] [--yes] [path]`.

### brief

Reframe the previous answer at a more useful level, or keep later replies concise and decision-focused. The standing mode can apply to the session or the current harness's user context.

Run `/brief`, `/brief on|off [--user] [--yes]`, or `/brief status`.

### delegation

Let the main agent decide, plan, and verify while subagents perform selected work routed by `model-selector` unless run on the frozen main seat with no override. The mode can apply to the session, project, or current harness user.

Run `/delegation`, `/delegation on|off [--project|--user] [--yes]`, or `/delegation status [--project|--user]`.

### tldr

Explain the answer just given to somebody who delegated the work and therefore did not follow it. The reply is treated as correct but pitched at the wrong reader, so the re-explanation adds the background the original assumed and unpacks the terms belonging to this work alone, while the ordinary technical vocabulary you already use stays as it is. It always closes by naming what you have to do — or saying plainly that nothing is asked of you.

Run `/tldr`, optionally followed by an instruction such as `/tldr bara säkerhetsdelen`.

### commit

Reconcile the changelog, review the complete working tree, and create one commit without pushing. A message is derived when none is supplied.

Run `/commit [--yes] [message]`.

### push

Run the commit workflow, then push the current branch to its upstream. Existing unpushed commits can be pushed even when the working tree is clean.

Run `/push [--yes] [message]`.

### release

Publish a version from the default branch. The skill updates the changelog and version files, pushes, tags, and creates a GitHub release when `gh` and a GitHub remote are available.

Run `/release [--no-build] [--yes] [minor|major|X.Y.Z]`.

### ready-for-agent-check

Check whether GitHub tickets contain enough settled, current information for unattended implementation. It reports blockers and costs without changing the tracker.

Run `/ready-for-agent-check [#ticket ...]`.

### orchestrate

Build `ready-for-agent` tickets in dependency waves. Fresh subagents implement and independently verify each ticket; successful work is integrated and recorded, but never pushed or released.

Run `/orchestrate [--dry-run] [--at-once=N] [--model=NAME] [--deliberation=LEVEL] [--fast] [--approval=IDENTITY] [--yes] [#ticket-or-spec ...]`.

Use `/orchestrate reconcile [--commit=COMMIT] [--yes] #ticket` when a failed or conflicted attempt was completed outside orchestrate.

### proofread

Correct mechanical language errors in one text while preserving wording, meaning, tone, structure, formatting, code, and metadata. The result goes to the response unless another output or explicit in-place editing is selected.

Run `/proofread [--language=LANGUAGE] [--output=TARGET] [text|path|url]` or `/proofread [--language=LANGUAGE] --in-place path`.

### redline

Review one text against the editorial contract, correct findings within a bounded correction budget, and finish with one proofreading pass. Remaining findings are reported with the delivered text.

Run `/redline [--genre=GENRE] [--technique=TECHNIQUE] [--language=LANGUAGE] [--max=N] [--output=TARGET] [text|path|url]` or use `--in-place path`.

### unslop

Remove seven defined patterns of machine-sounding prose from one otherwise finished text. It does not apply the wider editorial contract or correct spelling, grammar, and punctuation.

Run `/unslop [--language=LANGUAGE] [--max=N] [--output=TARGET] [text|path|url]` or use `--in-place path`.

### write

Turn a brief and one or more sources into a first draft. It preserves source fidelity, resolves genre, technique, and language, and can attach handoff metadata for later review.

Run `/write [--genre=GENRE] [--technique=TECHNIQUE] [--language=LANGUAGE] [--frontmatter=BOOLEAN] [--output=TARGET] [brief]`.

### model-selector

Compare complete AI model configurations using local profiles, costs, quotas, latency, and measured quality. It can recommend a configuration, derive reproducible routing context, route delegated workloads, maintain evidence, and — once Enabled — measure ordinary local session usage automatically.

Start with `/model-selector setup`, then use `/model-selector recommend <workload>`, `/model-selector context <path>`, `/model-selector route <path>`, or `/model-selector --help`.

### rename-invoices

Plan and apply deterministic filenames for accounting PDFs using extracted document evidence, an explicit document type, and configured locales. By default, it applies after confirmation; `--yes` skips the question and `--dry-run` only reports the plan.

Run `/rename-invoices [--folder=<path>] --type=<name> [--locale=<name> ...] [--yes|--dry-run]`.

## Dependencies

Most skills require `uv` and the manager. `brief` and `tldr` require neither.

Git workflows also require `git`; ticket workflows require `gh`; `rename-invoices` requires Poppler's `pdftotext`. `release` can finish without `gh`, but then skips the GitHub release.

`push` requires `commit`; `release` requires `push`; `delegation` and `orchestrate` require `model-selector`; `redline` requires `proofread`.

Delegation, orchestrate, ready for agent check, redline, and unslop require a harness that can spawn subagents. Select shows skill and harness requirements before enablement.

## Contributing and license

Bug fixes, corrections, and clarifications are welcome. Discuss features and behavior changes before opening a pull request; see [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and verification commands.

Kntnt Skills is licensed under the [Apache License 2.0](LICENSE).
