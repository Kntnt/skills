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

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/agents-md`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

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
