---
name: push
description: Commit tracked work and push the current branch.
disable-model-invocation: true
argument-hint: '["message"] [--yes]'
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - uv
    skills:
      - commit
---

# push

Commit tracked changes on the current branch, then push.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

- `"message"` — use this commit message.
- `--yes` — skip the confirmation.

## Steps

1. Run `uv run "$HERE/../commit/scripts/ship.py" plan push`. Done when stdout is a JSON plan, or the command exits 2.
2. Exit 2: say everything is up to date, and stop.
3. Message: the `"message"` argument if given, otherwise one concrete subject line from the plan — or `(none)` when `dirty` is false. Done when the message is decided.
4. Show the plan and the message. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
5. Run `uv run "$HERE/../commit/scripts/ship.py" apply push --message "<message>"`. Add `--include <path>` for each untracked file that belongs in the commit. When `dirty` is false, any non-empty `--message` is fine. Done when stdout contains `pushed`.
