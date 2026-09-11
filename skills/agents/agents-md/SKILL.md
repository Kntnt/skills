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

Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/agents-md`, verbatim and however many lines, on stdin. Exit 0: do what it prints. Any other exit: show what it printed to the user verbatim, and stop.

## Arguments

`path`, when present, must resolve inside the current repository root. The Skill never creates or changes user-level, home-directory, Harness-global, or system-level agent instructions.

## Steps

1. Run only after the current task is complete, or when the user passed `/agents-md` or `--force`. Mid-task with no user invoke: stop. Done when this run is after the task or the user invoked it.
2. Resolve the current repository root. Refuse a `path` outside it; otherwise target `path` or that root. Never target agent instructions above or outside the repository. Inventory `CLAUDE.md`, `AGENTS.md`, `agents.d/`, `docs/`, `README*`, and every tracked Project `SKILL.md` (`git ls-files` under `.claude/skills/`, `.agents/skills/`, and `skills/`). Done when the target is project-local and that inventory exists.
3. Collect candidate facts from those files and from this session. Read [`gates.md`](references/gates.md) and apply every gate to every candidate. Read [`placement.md`](references/placement.md) and give each survivor a home. Done when every candidate is `KEEP`, `CUT`, `ASK`, or placed.
4. Read [`writes.md`](references/writes.md). Split the plan into writes and questions. Done when every change is one or the other.
5. No `KEEP` and no `--force`: write no file. Report why. Stop. Done when the working tree is unchanged.
6. Ask every question after the work, as a concrete fact, not “run `/agents-md`”. With `--yes`, ask nothing: make each change the question would have proposed, and list it in the report instead. Write the safe set. `--force` with no facts: `CLAUDE.md` is exactly `@AGENTS.md`; `AGENTS.md` is the title plus Ground rules only if `README*` or other narrative exists; `agents.d/.gitkeep` if the directory is empty. Every References line is `read when <situation>` and passes the completeness test in [`placement.md`](references/placement.md). Done when writes match the plan, `docs/` is untouched, every `agents.d/` file has a References line, and every References line passes the test.
7. Report `wc -c` before and after for the always-loaded pair and for the total including `agents.d/`. List each cut, keep, split, and pointer with its reason. Cite the source for every `CUT`. Done when that report is shown.
