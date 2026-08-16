---
name: release
description: Ship a version — changelog, bump, tag, push, and GitHub release.
disable-model-invocation: true
argument-hint: "[minor|major|X.Y.Z] [--yes]"
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - uv
    skills:
      - commit
---

# release

Ship a version from the default branch: changelog, bump, commit, tag, push, GitHub release.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`). `gh` is required only for the GitHub release step.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

- `minor` / `major` / `X.Y.Z` — force the bump; otherwise derive it from `[Unreleased]`.
- `--yes` — skip the confirmation.

## Steps

1. Run `uv run "$HERE/../commit/scripts/ship.py" plan release`. Done when stdout is a JSON plan.
2. If the plan's `branch` is not `default_branch`, stop and say to integrate onto the default branch first.
3. Reconcile `CHANGELOG.md` `## [Unreleased]` with `commits` in the plan. Keep a Changelog sections, one user-facing bullet per change, in the file's existing language and voice. Empty `[Unreleased]` → stop; there is nothing to ship.
4. Version: the `X.Y.Z` argument if given; else bump `current_version` by `major`/`minor` if given; else `Removed` or breaking → major (below 1.0.0 → minor), else `Added` → minor, else patch. Done when the version string is known.
5. Show the plan, the changelog diff, and the version. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
6. Run `uv run "$HERE/../commit/scripts/ship.py" apply release --version X.Y.Z --message "Release X.Y.Z: <summary>"`. Summary is a short comma-separated reading of the changelog highlights. Done when stdout contains the tag and `pushed`.
