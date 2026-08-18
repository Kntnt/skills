---
name: push
description: Follow commit, then push the current branch.
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

Follow the commit skill, then push the current branch.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` as it stands and stop. It is this skill's manpage: print it, do not summarise or extend it.

## Arguments

- `"message"` — use this commit message.
- `--yes` — skip the confirmation.

## Steps

1. Follow `$HERE/../commit/SKILL.md` with the same arguments. If it stops because there is nothing to commit, continue. Done when the working tree is clean, or commit stopped as clean.
2. Run `uv run "$HERE/../commit/scripts/ship.py" plan push`. Done when stdout is a JSON plan, or the command exits 2.
3. Exit 2: emit the plan's `reason` and stop.
4. If commit did not already wait, show the plan and wait unless `--yes`. Done when the user confirms, `--yes` is set, or commit already confirmed.
5. Run `uv run "$HERE/../commit/scripts/ship.py" apply push`. Done when stdout contains `pushed`.
