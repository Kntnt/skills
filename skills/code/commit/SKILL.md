---
name: commit
description: Commit the working tree on the current branch, without pushing.
disable-model-invocation: true
argument-hint: '["message"] [--yes]'
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - uv
---

# commit

Commit the working tree on the current branch and stop.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

- `"message"` — use this commit message.
- `--yes` — skip the confirmation.

## Steps

1. Run `uv run "$HERE/scripts/ship.py" plan commit`. Done when stdout is a JSON plan, or the command exits 2.
2. Exit 2: say there is nothing to commit, and stop.
3. Follow `$HERE/changelog.md`. Done when every real change is recorded in `CHANGELOG.md` — in `[Unreleased]` or already in a dated version section.
4. If the plan has `gitignore_proposal`, keep it for the gate. Done when the proposal is ready or none is needed.
5. Message: the `"message"` argument if given, otherwise one concrete subject line from the changelog entries just written, or from `git diff` when there is no user-facing entry. Done when the message is a single subject line.
6. Show the changelog diff, the message, and the proposed `.gitignore` if any. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
7. Write the proposed `.gitignore` if one was confirmed. Run `uv run "$HERE/scripts/ship.py" apply commit --message "<message>"`. Done when stdout is a commit SHA.
