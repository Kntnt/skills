---
name: agents-md
description: "AGENTS.md: create, shrink, or tend the always-loaded file and agents.d/ after a task when a non-discoverable fact is new, a line is stale or sprawling, or a pointer is missing; also `/agents-md` and `--force`."
argument-hint: "[path] [--force] [--yes]"
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - uv
---

# agents-md

Write the fewest always-loaded tokens that still keep the next session safe. Default is nothing.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` as it stands and stop. It is this skill's manpage: print it, do not summarise or extend it.

## Arguments

- `path` — directory to tend. Default: current repo root.
- `--force` — lay the skeleton when no fact earns a file.
- `--yes` — take yes for an answer on every question in [`writes.md`](writes.md) and make the change, rather than asking. `docs/` stays a proposal even so: a human writes that text.

## Steps

1. Run only after the current task is complete, or when the user passed `/agents-md` or `--force`. Mid-task with no user invoke: stop. Done when this run is after the task or the user invoked it.
2. Run the dependency checker. Done when it exits 0, or you told the user to install the Manager.
3. Target `path` or the repo root. Inventory `CLAUDE.md`, `AGENTS.md`, `agents.d/`, `docs/`, `README*`, and every tracked Project `SKILL.md` (`git ls-files` under `.claude/skills/`, `.agents/skills/`, and `skills/`). Done when that inventory exists.
4. Collect candidate facts from those files and from this session. Read [`gates.md`](gates.md) and apply every gate to every candidate. Read [`placement.md`](placement.md) and give each survivor a home. Done when every candidate is `KEEP`, `CUT`, `ASK`, or placed.
5. Read [`writes.md`](writes.md). Split the plan into writes and questions. Done when every change is one or the other.
6. No `KEEP` and no `--force`: write no file. Report why. Stop. Done when the working tree is unchanged.
7. Ask every question after the work, as a concrete fact, not “run `/agents-md`”. With `--yes`, ask nothing: make each change the question would have proposed, and list it in the report instead. Write the safe set. `--force` with no facts: `CLAUDE.md` is exactly `@AGENTS.md`; `AGENTS.md` is the title plus Ground rules only if `README*` or other narrative exists; `agents.d/.gitkeep` if the directory is empty. Every References line is `read when <situation>` and passes the completeness test in [`placement.md`](placement.md). Done when writes match the plan, `docs/` is untouched, every `agents.d/` file has a References line, and every References line passes the test.
8. Report `wc -c` before and after for the always-loaded pair and for the total including `agents.d/`. List each cut, keep, split, and pointer with its reason. Cite the source for every `CUT`. Done when that report is shown.
