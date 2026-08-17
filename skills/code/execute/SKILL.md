---
name: execute
description: Build the plans under plans/ unattended, landing each approved one on the current branch.
disable-model-invocation: true
argument-hint: '[NNN...] [--yes]'
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - gh
      - uv
    skills:
      - commit
    externals:
      - improve
    capabilities:
      - subagents
---

# execute

Build the Plans under `plans/` one at a time and Land each approved one on the branch you started on, so the run ends with the work committed, the changelog true, and no branch or worktree left over. It writes no code and reads no diff itself: the External `improve` dispatches the builder and renders the verdict. It stops at the commit — push, tag, and release stay with `push` and `release`.

Ticket in, Plan out is the `plan` skill. Given a Ticket, name `plan` and do nothing else.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, change nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

- `NNN...` — build these Plans, in the order their dependencies require.
- no arguments — pick from a list of the Plans still TODO.
- `--yes` — build every TODO Plan without showing the list, skip the gate, close the Tickets of Landed Plans, and answer yes wherever the run would otherwise ask.

## Steps

1. Selection. With `NNN...`, those Plans. With neither, show a checklist of every Plan in `plans/README.md` still TODO; `--yes` takes them all. A named Plan whose `**Depends on**` is not DONE is refused by name, saying which dependency is missing, and the rest of the queue goes on without it. A named Plan already marked DONE is asked about — skip it? — and `--yes` says yes. Order the survivors by their dependencies. Done when the queue is ordered.
2. The working tree. Run `git status --porcelain`. Clean: go on. Dirty: offer to commit it first — the default, and what `--yes` takes — or to stash it (`git stash push -u`), and stop if the user wants neither. Offer only the commit when any selected Plan file is itself among the uncommitted changes, because stashing would take the Plans away with it. Done when `git status --porcelain` is empty.
3. The base. Record `git rev-parse HEAD`. This is the run's base and the only point where Drift can belong to anyone else. Done when the base is recorded.
4. Preflight. For each queued Plan run its own drift-check command with `HEAD` replaced by the base. A Plan that drifted is stale: set it aside, and set aside every Plan that depends on it. Done when every queued Plan has been checked.
5. The gate. Show the queue, its order, its dependencies, what was already set aside and why, and that each approved Plan will be committed to the current branch. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
6. Build, one Plan at a time, never two at once. For each:
   1. Run `git rev-parse HEAD`. It must equal the base, or the commit the previous Landing produced. Anything else means someone committed during the run: that is real Drift — stop the whole run and say so.
   2. Run `/improve execute <the Plan's path>`, telling it that the drift preflight was done at the base and that every commit after the base on this branch is this run's own Landing, not Drift.
   3. APPROVE: follow [`land.md`](land.md).
   4. Any other verdict: set the Plan aside with the reason it gave, and set aside every Plan that depends on it. The queue goes on.

   Done when every queued Plan is Landed or set aside, or the run stopped on real Drift.
7. The stash, if step 2 made one. Ask whether to restore it; `--yes` says yes. Run `git stash apply`. Clean: `git stash drop`. Conflicted: `git reset --hard HEAD` — safe here, because every Landing is already committed, so the only thing discarded is the half-applied stash — then report which files collided and that the changes are still in `stash@{0}`, to be recovered with `git stash pop` when there is time to resolve them. Done when the working tree is clean either way.
8. The Tickets. List the Tickets of Landed Plans only, and ask whether to close them; `--yes` says yes. Close each with `gh issue close <n> --comment "..."` naming the commit that Landed it. A Plan that was set aside leaves its Ticket open and is not asked about. Done when the answer is acted on.
9. Report, in the conversation and nowhere else — `plans/README.md` already holds the status. One line per Plan: Landed with its commit SHA, or blocked or set aside and why. Then what needs you. Done when that report is shown.
