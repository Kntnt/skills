---
name: push
description: Follow commit, then push the current branch.
disable-model-invocation: true
argument-hint: '[--yes] [<message>] [-- <instruction>]'
compatibility: Requires git and uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git uv"
  kntnt.skills: "commit"
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# push

Follow the commit skill, then push the current branch.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

`/push [--yes] [<message>]`, and nothing else. The order is part of the form: an operand written before a flag is refused, not repaired. It is the commit skill's grammar, which is what lets step 1 hand the arguments straight on — they are checked here first, so nothing reaches that skill it would have to refuse.

Anything else is an invalid form. Refuse it as `$LIBRARY/references/invocation-envelope.md` says, then commit nothing, push nothing, and stop.

## Steps

1. Follow `$HERE/../commit/SKILL.md` with the same Formal Invocation. If the outer Contextual Instruction contains guidance relevant to commit, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. If commit stops because there is nothing to commit, continue. Done when the working tree is clean, or commit stopped as clean.
2. Run `uv run "$LIBRARY/scripts/ship.py" plan push`. Done when stdout is a JSON plan, or the command exits 2.
3. Exit 2: emit the plan's `reason` and stop.
4. If commit did not already wait, show the plan and wait unless `--yes`. Done when the user confirms, `--yes` is set, or commit already confirmed.
5. Run `uv run "$LIBRARY/scripts/ship.py" apply push`. Done when stdout contains `pushed`.
