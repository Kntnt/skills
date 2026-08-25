---
name: agents-md
description: "AGENTS.md: create, shrink, or tend the current project's always-loaded file and agents.d/ after a task when a non-discoverable fact is new, a line is stale or sprawling, or a pointer is missing; also `/agents-md` and `--force`."
disable-model-invocation: false
argument-hint: "[--force] [--yes] [path] [-- <instruction>]"
compatibility: Requires git and uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# agents-md

Write the fewest always-loaded tokens that still keep the next session safe. Default is nothing.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

`/agents-md [--force] [--yes] [path]`, and nothing else. The order is part of the form: an operand written before a flag is refused, not repaired.

`path`, when present, must resolve inside the current repository root. The Skill never creates or changes user-level, home-directory, Harness-global, or system-level agent instructions.

Anything else is an invalid form. A `path` outside the current repository is invalid too. Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/agents-md --help` for the page in full. Then write no file and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Run only after the current task is complete, or when the user passed `/agents-md` or `--force`. Mid-task with no user invoke: stop. Done when this run is after the task or the user invoked it.
2. Run the dependency checker. Done when it exits 0, or you told the user to install the Manager.
3. Resolve the current repository root. Refuse a `path` outside it; otherwise target `path` or that root. Never target agent instructions above or outside the repository. Inventory `CLAUDE.md`, `AGENTS.md`, `agents.d/`, `docs/`, `README*`, and every tracked Project `SKILL.md` (`git ls-files` under `.claude/skills/`, `.agents/skills/`, and `skills/`). Done when the target is project-local and that inventory exists.
4. Collect candidate facts from those files and from this session. Read [`gates.md`](references/gates.md) and apply every gate to every candidate. Read [`placement.md`](references/placement.md) and give each survivor a home. Done when every candidate is `KEEP`, `CUT`, `ASK`, or placed.
5. Read [`writes.md`](references/writes.md). Split the plan into writes and questions. Done when every change is one or the other.
6. No `KEEP` and no `--force`: write no file. Report why. Stop. Done when the working tree is unchanged.
7. Ask every question after the work, as a concrete fact, not “run `/agents-md`”. With `--yes`, ask nothing: make each change the question would have proposed, and list it in the report instead. Write the safe set. `--force` with no facts: `CLAUDE.md` is exactly `@AGENTS.md`; `AGENTS.md` is the title plus Ground rules only if `README*` or other narrative exists; `agents.d/.gitkeep` if the directory is empty. Every References line is `read when <situation>` and passes the completeness test in [`placement.md`](references/placement.md). Done when writes match the plan, `docs/` is untouched, every `agents.d/` file has a References line, and every References line passes the test.
8. Report `wc -c` before and after for the always-loaded pair and for the total including `agents.d/`. List each cut, keep, split, and pointer with its reason. Cite the source for every `CUT`. Done when that report is shown.
