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

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

`/commit [--yes] [<message>]`, and nothing else. The order is part of the form: an operand written before a flag is refused, not repaired.

Anything else is an invalid form. Refuse it as `$LIBRARY/references/invocation-envelope.md` says, then commit nothing and stop.

## Steps

1. Run `uv run "$LIBRARY/scripts/ship.py" plan commit`. Done when stdout is a JSON plan, or the command exits 2.
2. Exit 2: say there is nothing to commit, and stop.
3. Follow `$LIBRARY/references/changelog.md`. Done when every real change is recorded in `CHANGELOG.md` — in `[Unreleased]` or already in a dated version section.
4. If the plan has `gitignore_proposal`, keep it for the gate. Done when the proposal is ready or none is needed.
5. Message: the `<message>` argument if given, otherwise one concrete subject line from the changelog entries just written, or from `git diff` when there is no user-facing entry. Done when the message is a single subject line.
6. Show the changelog diff, the message, and the proposed `.gitignore` if any. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
7. Write the proposed `.gitignore` if one was confirmed. Run `uv run "$LIBRARY/scripts/ship.py" apply commit --message="<message>"`. Done when stdout is a commit SHA.
