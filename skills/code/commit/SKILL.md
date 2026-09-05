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

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/commit`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

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
