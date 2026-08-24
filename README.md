# Kntnt Skills

[![License](https://img.shields.io/github/license/Kntnt/skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/skills)](https://github.com/Kntnt/skills/releases/latest)

[Agent Skills](https://agentskills.io) are portable. Their paths are not: Claude Code, Codex, OpenCode and other Harnesses look for Skills in different directories. Kntnt Skills resolves that mismatch with one Manager. Choose the Skills for a layer once, and the Manager writes them to every Detected Harness.

The initial installation puts only the `kntnt` Manager on disk. Its Catalog lets you read every other Skill before you Enable it, keeps Global choices separate from Project extras and detects Harness paths for you.

## Quick start

You need [uv](https://docs.astral.sh/uv/), `npx` and network access. Install the Manager:

```sh
npx skills add Kntnt/skills
```

Then open its Catalog from any Harness that can see `kntnt`:

```
/kntnt select
```

The Manager groups Skills by Category and marks those already Enabled. Each row explains the Skill and names any Harness Capability it needs; a locked row also names the Skill you need to check first. You can ask to read any Skill's full help before replying to the list in plain text, for example `check commit, push and tldr`. Nothing is written until you confirm.

## Choose where Skills apply

Kntnt Skills keeps two layers. A Project adds to Global; it cannot hide a Global Skill.

| Layer | What it is for | Select it with |
|---|---|---|
| Global | Skills available on this machine | `/kntnt select` |
| Project | Extra Skills for the current working directory, suitable for committing with the Project | `/kntnt select --project` |

The Manager detects Harnesses afresh on every run. When it changes a layer, it writes to every Harness present in that layer. If you install another supported Harness later, confirm the next Select list or run Update to copy your Enabled Skills into it. If no Harness is detected, the Manager uses only the shared `.agents/skills` directory.

## Manage the collection

| Command | Result |
|---|---|
| `/kntnt` | Show Manager help |
| `/kntnt select [--project]` | Inspect the Catalog and change what is Enabled |
| `/kntnt select --on <skill> --yes` | Enable a named Skill without opening the list |
| `/kntnt update [--project]` | Refresh the Manager and Enabled Skills whose files differ, remove Withdrawn Skills, report new Skills and re-check Dependencies |
| `/kntnt uninstall` | Remove Global Skills and then the Manager; leave Project copies alone |

See `/kntnt help <command>` for all options. Select, Update and Uninstall accept `--dry-run`, which runs the operation against a temporary home and discards that home afterwards.

> [!IMPORTANT]
> `--yes` answers every yes-or-no question with yes. On `/kntnt update --yes`, that includes Enabling every new Skill reported by the update.

Enabled Skills are invoked by their own names, not through the Manager. Run `/<skill> --help` for a Skill you have. To inspect one you have not Enabled, ask for its help while the Select list is open.

## Usage

### agents-md

Review `AGENTS.md` and `agents.d/` after a task and write only facts that the next session needs and cannot discover elsewhere. Use `--force` to create the initial structure. Run `/agents-md [path] [--force] [--yes]`.

### delegation

Leave the decision to delegate, planning, briefing, verification, and the final answer with the unchanged main agent while subagents execute the chosen work. Predictably noisy tool work can stay in a subagent's context and return as a distilled result. Delegated execution uses model-selector's public routing Interface for an exact supported launch point, explicit inheritance, or a refusal; it never changes the main agent's model or deliberation configuration. A judged execution may leave a sanitized observation artifact in scratch, imported only by an explicit `/model-selector record`. The mode can last for the current session or be saved in Project or user context. Run `/delegation` to toggle the session, `/delegation [project|user] on|off [--yes]` to set a standing mode or `/delegation status` to inspect every scope.

### tldr

Reframe the previous answer at the level and focus useful to the person who owns the outcome, or keep later replies concise and decision-relevant by default. A bare `/tldr` answers the substance again without handing over every implementation detail; `--on` applies the same perspective only to subsequent replies. Run `/tldr [instruction]`, `/tldr --on|--off [--user] [--yes]` or `/tldr --status`.

### commit

Commit the entire working tree without pushing. The Skill reconciles `CHANGELOG.md`, proposes `.gitignore` additions where needed, derives a subject unless you provide one and shows the proposed changes before confirmation. Run `/commit [<message>] [--yes]`.

### push

Run the `commit` workflow, then push the current branch to its upstream. A clean working tree still allows existing unpushed commits to be sent. Run `/push [<message>] [--yes]`.

### release

Create a version from the default branch: reconcile the changelog, derive or accept the version, update version files, push and tag. When `gh` and a GitHub remote are available, the Skill also publishes a GitHub release; it attaches an archive when the Project provides a conventional archive build. Run `/release [minor|major|X.Y.Z] [--no-build] [--yes]`.

### ready-for-agent-check

Check whether tickets can be built unattended before a run begins. Each ticket is read in an isolated subagent context and checked against the current Project; the Skill reports anything that would stop or slow the builder and never changes the tracker. Run `/ready-for-agent-check [#ticket ...]`.

### orchestrate

Work the tracker's `ready-for-agent` tickets in Dependency waves on the current branch. Orchestrate preflights each execution role through model-selector's frozen public route Interface, while independent verdicts inherit the complete main seat. Each ticket is claimed, built by a subagent and independently verified, and every outcome is recorded on its ticket. Attempts an independent verdict judged are reported as an importable model-selector artifact in the run's own scratch, which nothing imports on the developer's behalf. The run neither pushes nor releases. Run it for all ready tickets, named tickets or the children of a spec with `/orchestrate [#ticket-or-spec ...] [--dry-run] [--at-once N] [--model NAME] [--deliberation low|medium|high|xhigh|max] [--yes]`. Where a failed or conflicted ticket was finished by hand afterwards, `/orchestrate reconcile #<ticket> [--commit <commit>] [--yes]` records that without rewriting the attempt.

### model-selector

Compare complete model configurations rather than model names in isolation. The Skill records exact versions, effort settings, serving modes and access channels, then recommends from price-performance evidence without reducing cash, quota, latency and quality to one ratio. Its offline, read-only `route` form resolves a structured delegated workload or ordered batch into exact Harness-native selection, inheritance, or refusal decisions and returns the frozen routing snapshot. When measurements do not determine the exact point, it visibly labels the result heuristic or mixed, begins at the lowest plausibly sufficient configuration where exploration is safe, and emits a frozen sequential and parallel experiment brief; only representative matched measurements can produce a measurement-based recommendation. Routed work can hand back what an external checker judged: `/model-selector observe <path> --artifact=<path>` turns completed routed attempts into a sanitized artifact of statistical metadata in the caller's own scratch, and `/model-selector record <path>` is the explicit invocation that imports one into the evidence ledger. Start with `/model-selector setup`, then use `/model-selector recommend <workload>`, `/model-selector route <path>`, or `/model-selector --help`.

**Dependencies.** `tldr` has no Dependencies and works without `uv`; every other Skill needs `uv` and the Manager. `agents-md`, `commit`, `push`, `release` and `orchestrate` also need `git`. `orchestrate` and `ready-for-agent-check` need `gh`; `release` uses it only for the GitHub release step. `delegation` and `orchestrate` need `model-selector`, and `delegation`, `orchestrate` and `ready-for-agent-check` need a Harness that can spawn subagents. `push` needs `commit`, and `release` needs `push`. Select shows Dependencies on other Skills and Harness Capabilities and can offer required Skills from this Collection. Any Unsatisfied binary Dependency is reported when the Skill is invoked.

## Contributing and licence

Bug fixes, corrections and clarifications are welcome. Discuss new features or changes to existing behaviour in an issue before opening a pull request; the full workflow and verification commands are in [CONTRIBUTING.md](CONTRIBUTING.md).

Kntnt Skills is licensed under the [Apache License 2.0](LICENSE).
