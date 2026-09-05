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

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/push`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

`<message>` and `--yes` mean what they mean to commit, whose grammar this is; step 1 hands them on as they stand.

## Steps

1. Follow `$HERE/../commit/SKILL.md` with the same Formal Invocation. If the outer Contextual Instruction contains guidance relevant to commit, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. If commit stops because there is nothing to commit, continue. Done when the working tree is clean, or commit stopped as clean.
2. Run `uv run "$LIBRARY/scripts/ship.py" plan push`. Done when stdout is a JSON plan, or the command exits 2.
3. Exit 2: emit the plan's `reason` and stop.
4. If commit did not already wait, show the plan and wait unless `--yes`. If the user asks to see every commit, re-run `plan --full push` and show that plan. Done when the user confirms, `--yes` is set, or commit already confirmed.
5. Run `uv run "$LIBRARY/scripts/ship.py" apply push`. Done when stdout contains `pushed`.
