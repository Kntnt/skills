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

Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/push`, verbatim and however many lines, on stdin. Exit 0: do what it prints. On any other exit, if you introduced a known construction error and can correct it while preserving the user's request and authority, account for effects already produced, submit the corrected invocation through the same shim, and continue from the failed boundary; a refusal before the operation starts consumes no operation. Otherwise show what it printed to the user verbatim and stop. Never repair input the user supplied, or automatically retry exact help, an unmet dependency, an unrelated failure, or a failure whose origin or valid correction is unknown.

## Arguments

`<message>` and `--yes` mean what they mean to commit, whose grammar this is; step 1 hands them on as they stand.

## Steps

1. Follow `$HERE/../commit/SKILL.md` with the same Formal Invocation. If the outer Contextual Instruction contains guidance relevant to commit, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. If commit stops because there is nothing to commit, continue. Done when the working tree is clean, or commit stopped as clean.
2. Run `uv run "$LIBRARY/scripts/ship.py" plan push`. Done when stdout is a JSON plan, or the command exits 2.
3. Exit 2: emit the plan's `reason` and stop.
4. If commit did not already wait, show the plan and wait unless `--yes`. If the user asks to see every commit, re-run `plan --full push` and show that plan. Done when the user confirms, `--yes` is set, or commit already confirmed.
5. Run `uv run "$LIBRARY/scripts/ship.py" apply push`. Done when stdout contains `pushed`.
