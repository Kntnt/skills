---
name: orchestrate
description: Plan an unattended run over the tracker's ready-for-agent tickets, and name what it would work.
disable-model-invocation: true
argument-hint: '[--dry-run] [--yes]'
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - gh
      - uv
    capabilities:
      - subagents
---

# orchestrate

Read the tracker, and report the `ready-for-agent` tickets an unattended run would work on this branch.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, do no work, install nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Steps

1. Run `uv run "$HERE/scripts/run.py" plan`, passing the user's `--dry-run` and `--yes` through. Done when stdout is the JSON plan; anything else on stdout means the engine refused the arguments, so show stderr and stop.
2. Report the plan: the branch a run would work on, every ticket in `tickets` by number and title, which of them are in `workable`, and — where `ready` is false — `reason`, as why no run may start. Done when the user has that report.
3. Stop, having started nothing. This Skill plans a run and reports it; it works no ticket. Done when you have stopped.
