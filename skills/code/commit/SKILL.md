---
name: commit
description: Commit the working tree on the current branch, without pushing.
disable-model-invocation: true
argument-hint: '[--yes] [<message>] [-- <instruction>]'
compatibility: Requires git and uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# commit

Commit the working tree on the current branch and stop.

Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/commit`, verbatim and however many lines, on stdin. Exit 0: do what it prints. On any other exit, if you introduced a known construction error and can correct it while preserving the user's request and authority, account for effects already produced, submit the corrected invocation through the same shim, and continue from the failed boundary; a refusal before the operation starts consumes no operation. Otherwise show what it printed to the user verbatim and stop. Never repair input the user supplied, or automatically retry exact help, an unmet dependency, an unrelated failure, or a failure whose origin or valid correction is unknown.

## Arguments

`<message>` is the subject line step 5 uses as it stands, and `--yes` is the confirmation step 6 otherwise waits for.

## Steps

1. Run `uv run "$LIBRARY/scripts/ship.py" plan commit`. Done when stdout is a JSON plan, or the command exits 2.
2. Exit 2: say there is nothing to commit, and stop.
3. Follow `$LIBRARY/references/changelog.md`. Done when every real change is recorded in `CHANGELOG.md` — in `[Unreleased]` or already in a dated version section.
4. If the plan has `gitignore_proposal`, keep it for the gate. Done when the proposal is ready or none is needed.
5. Message: the one entry of `operands` if there is one, otherwise one concrete subject line from the changelog entries just written, or from `git diff` when there is no user-facing entry. Done when the message is a single subject line.
6. Show the changelog diff, the message, and the proposed `.gitignore` if any. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
7. Write the proposed `.gitignore` if one was confirmed. Run `uv run "$LIBRARY/scripts/ship.py" apply commit --message="<message>"`. Done when stdout is a commit SHA.
