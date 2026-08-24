---
name: push
description: Follow commit, then push the current branch.
disable-model-invocation: true
argument-hint: '[<message>] [--yes] [-- <instruction>]'
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

`$HERE` is the directory that contains this SKILL.md.

`$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

`/push [<message>] [--yes]`, and nothing else. It is the commit skill's grammar, which is what lets step 1 hand the arguments straight on — they are checked here first, so nothing reaches that skill it would have to refuse.

Anything else is an invalid form. Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/push --help` for the page in full. Then commit nothing, push nothing, and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Follow `$HERE/../commit/SKILL.md` with the same Formal Invocation. If the outer Contextual Instruction contains guidance relevant to commit, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. If commit stops because there is nothing to commit, continue. Done when the working tree is clean, or commit stopped as clean.
2. Run `uv run "$LIBRARY/scripts/ship.py" plan push`. Done when stdout is a JSON plan, or the command exits 2.
3. Exit 2: emit the plan's `reason` and stop.
4. If commit did not already wait, show the plan and wait unless `--yes`. Done when the user confirms, `--yes` is set, or commit already confirmed.
5. Run `uv run "$LIBRARY/scripts/ship.py" apply push`. Done when stdout contains `pushed`.
