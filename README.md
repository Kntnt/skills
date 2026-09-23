# Kntnt Skills

[![License](https://img.shields.io/github/license/Kntnt/skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/skills)](https://github.com/Kntnt/skills/releases/latest)

You are in the right place if you want practical [agent skills](https://agentskills.io) for maintaining agent instructions, delegating work, shipping code, preparing tickets, editing prose, choosing AI models, organizing accounting PDFs, and saving web pages for offline reading.

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
| `/kntnt select --on=<entry> --yes` | Enable a named skill or feature without opening the list |
| `/kntnt update [--project]` | Refresh changed skills and handle catalog changes |
| `/kntnt uninstall` | Remove global skills and the manager |

Use `/kntnt help <command>` for manager details. Use `/<skill> --help` or `/kntnt help <skill>` for an enabled skill.

`--dry-run` is available for select, update, and uninstall. `--yes` answers every yes-or-no question with yes; on update, that includes enabling new skills.

## Usage

These summaries help you choose a skill. Each skill's `--help` page contains its complete syntax, options, defaults, and failure behavior.

### agents-md

Keep a project's `AGENTS.md`, `CLAUDE.md`, and `docs/agents/` concise and current. It records only useful facts that later sessions cannot discover elsewhere.

Run `/agents-md [--force] [--yes] [path]`.

### delegation

Let the main agent decide, plan, and verify while subagents perform selected work routed by `model-selector` unless run on the frozen main seat with no override. The mode can apply to the session, project, or current harness user.

Run `/delegation`, `/delegation on|off [--project|--user] [--yes]`, or `/delegation status [--project|--user]`.

### explain

Get a brief, clear explanation of the reply just given, or whatever you name in the instruction. Written for an intelligent, busy colleague, it answers what needs clarification with just enough context, explains unfamiliar project terms, and makes any decision or action expected of you clear. Focused questions normally get one to three short paragraphs.

Run `/explain`, optionally followed by an instruction such as `/explain bara säkerhetsdelen`.

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

Run `/orchestrate [--dry-run] [--at-once=N] [--model=NAME] [--deliberation=LEVEL] [--max-deliberation=LEVEL] [--fast] [--approval=IDENTITY] [--yes] [#ticket-or-spec ...]`.

Use `/orchestrate reconcile [--commit=COMMIT] [--yes] #ticket` when a failed or conflicted attempt was completed outside orchestrate.

### proofread

Correct mechanical language errors in one text while preserving wording, meaning, tone, structure, formatting, code, and metadata. The result goes to the response unless another output or explicit in-place editing is selected.

Run `/proofread [--language=LANGUAGE] [--output=TARGET] [text|path|url]` or use `--in-place path`.

### redline

Review one text against the editorial contract, correct findings within a bounded correction budget, and finish with one proofreading pass. Remaining findings are reported with the delivered text.

Run `/redline [--genre=GENRE] [--technique=TECHNIQUE] [--language=LANGUAGE] [--max=N] [--output=TARGET] [text|path|url]` or use `--in-place path`.

### unslop

Remove seven defined patterns of machine-sounding prose from one otherwise finished text. It does not apply the wider editorial contract or correct spelling, grammar, and punctuation.

Run `/unslop [--language=LANGUAGE] [--max=N] [--output=TARGET] [text|path|url]` or use `--in-place path`.

### write

Turn a brief and one or more sources into a first draft, with an independent comparison of source support and translated quotations and evidence-based validation of its findings before delivery. It resolves genre, technique, and language, and can attach handoff metadata for later editorial review.

Run `/write [--genre=GENRE] [--technique=TECHNIQUE] [--language=LANGUAGE] [--frontmatter=BOOLEAN] [--output=TARGET] [brief]`.

### model-selector

Describe a piece of work and get back the model and reasoning effort expected to finish it for the least money, or in the least time where `/model-selector objective time` has made that your standing choice — among the points it has actually measured doing that kind of work, the one whose price divided by its chance of success is lowest, and where none of those measurements reaches the bar the cheapest of the ones they cannot tell apart from the best of them, a cheap run that has to be redone being the expensive one, rather than the cheapest sticker, the strongest model, or an estimate nothing here has ever tested, or whichever measured point happens to be cheapest — with what that estimate rests on, and the alternatives it beat. It is advice and never a refusal: with no profile, or nothing reachable, the answer is the seat you already have and a note saying why. Once Enabled it also measures substantial units of work in the harnesses on this machine — delegated work, and a session's own work that ran ten minutes or more, never quick exchanges — grades what nothing else judged with one bought model call, and keeps counts, prices and dates, never your prompts, code, or paths.

Run `/model-selector <work>` for an answer and `/model-selector setup` to say whose models you want and how you pay for them; `status`, `evidence`, `objective`, and `reset` are the rest. Read `/model-selector --help` for what enabling it measures before you enable it.

### rename-invoices

Plan and apply deterministic filenames for accounting PDFs using extracted document evidence, an explicit document type, and configured locales. By default, it applies after confirmation; `--yes` skips the question and `--dry-run` only reports the plan.

Run `/rename-invoices [--folder=<path>] --type=<name> [--locale=<name> ...] [--yes|--dry-run]`.

### mirror

Save a web page, and every page and file under it that its links, sitemaps and feeds reach, to disk with everything they need to display — images, stylesheets, scripts, fonts and media, on whatever host they are — and rewrite their references so the copy opens in a browser with nothing fetched from the network. The crawl stays under the start page's directory, widened by `--include` and narrowed by `--exclude` regular expressions, obeys `robots.txt`, and stops at 5000 pages unless `--max-pages` says otherwise; `--no-links`, `--no-sitemap` and `--no-feeds` turn each way of finding pages off. A host that blocks it climbs from plain HTTP to a Chrome identity and then to a headless browser, whose rendered page is saved without its scripts; `--headed` opens a visible browser where you can pass a challenge or log in, and `--profile` lends it your Chrome profile. Each run leaves a manifest of every URL it took a position on and a log beside the copy; `--dry-run` shows what would be fetched without writing anything.

Run `/mirror [--output=<dir>] [--resources=all|in-scope|none] [--max-pages=<n>] [--delay=<seconds>] [--no-links] [--no-sitemap] [--no-feeds] [--ignore-robots] [--include=<regex> ...] [--exclude=<regex> ...] [--header=<name: value> ...] [--user-agent=<string>] [--browser=auto|always|never] [--headed] [--profile=<name>|<path>] [--dry-run] <url>`.

### hetzner

Provision Hetzner Cloud servers, install software, and deploy or maintain their websites and applications with the official hcloud CLI, cloud-init, and SSH. It follows the project's existing stack and deployment files, reconciles existing resources and interrupted writes, and verifies bootstrap, services, and the requested public endpoint. Application-specific release and recovery routines stay in the project.

Run `/hetzner -- <operation>` with the operation and its constraints, or let the agent use it for a matching Hetzner Cloud task. A project is set up once with `/hetzner setup <project>`, after you copy a Read & Write API token from the project's Security page in the Console: the token goes from the clipboard into hcloud's own configuration without entering the conversation, `setup --yes` rotates it, and `/hetzner status` lists every project and what it reaches. `setup` also gives the agents a key of their own, `~/.ssh/kntnt-agent`: a server the Skill creates gets it at creation, and on one that already exists you admit the agents once, as a user `kntnt-agent` with passwordless `sudo`, by the procedure `setup` prints. Preparation alone creates no remote resources; billed and destructive changes stay within the established authorization. Robot dedicated servers and Object Storage are outside its scope.

## Features

Besides skills, the collection ships **features**: catalog entries that install nothing a harness loads. `/kntnt select` lists them as a second group under the skills, and a feature's row says what it writes and where before you check it. They apply to the machine rather than to a project, so `--project` offers none.

### session-cleanup

Leaves the machine as the session found it. It installs two things that only work together: a block in each harness's global instruction file asking the agent to record what it starts, and a session-lifecycle hook that stops exactly what was recorded. It kills only what a manifest names, and only while the recorded start time still matches, so a reused process id names something else and is left alone; it deletes only paths under a temp directory. It sweeps at session start as well as at session end, which covers a crash or a hard kill. A start preserves its own launcher's recorded work and every manifest whose Harness process still matches its recorded start time, regardless of age. Unknown ownership waits for a day; OpenCode shell recordings remain owned by its shared server until that process exits. Every action goes to `~/.kntnt/session-cleanup/cleanup.log`, including a session that recorded nothing.

Serves Claude Code, Codex, and OpenCode.

### statusline

A two-line Claude Code status line: path, worktree marker, branch, working-tree flags and any git operation in progress on the first; model, reasoning effort, context usage and the subscription windows on the second. It reads what the harness gives it plus one `git status`, calls no network service and reads no credential. Out of that same payload it writes this machine's weekly subscription window to `~/.kntnt/model-selector/quota.json`, which is what arms `model-selector`'s quota guard for the Claude channel; disabling this Feature disarms it.

`statusLine` holds one command rather than a list, so where it already runs something that is not this collection's, the row names that command and asks whether to replace it before anything is written — the same confirmation `--yes` answers. Nothing is kept of what is replaced. Serves Claude Code.

## Dependencies

Every skill requires `uv` and the manager: the manager ships the engine that reads a skill's invocation, and `uv` runs it.

`hetzner` can prepare deployment files without remote tools; Cloud operations additionally need hcloud, network access, and a project token, `setup` needs `ssh-keygen` and a clipboard tool, and host operations need OpenSSH and server access.

Git workflows also require `git`; ticket workflows require `gh`; `rename-invoices` requires Poppler's `pdftotext`; `mirror` requires `agent-browser`, which fetches in a real browser what plain HTTP cannot, installed with `brew install agent-browser` and then `agent-browser install`. `release` can finish without `gh`, but then skips the GitHub release.

`push` requires `commit`; `release` requires `push`; `delegation` and `orchestrate` require `model-selector`; `redline` requires `proofread`.

Delegation, orchestrate, ready for agent check, write, redline, and unslop require a harness that can spawn subagents. Select shows skill and harness requirements before enablement.

## Contributing and license

Bug fixes, corrections, and clarifications are welcome. Discuss features and behavior changes before opening a pull request; see [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and verification commands.

Kntnt Skills is licensed under the [Apache License 2.0](LICENSE).
