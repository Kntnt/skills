---
name: release
description: Ship a version — changelog, bump, push, tag, and GitHub release.
disable-model-invocation: true
argument-hint: "[minor|major|X.Y.Z] [--no-build] [--yes]"
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - uv
    skills:
      - push
---

# release

Ship a version from the default branch: changelog, bump, push, tag, GitHub release, optional archive.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`). `gh` is required only for the GitHub release step.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

- `minor` / `major` / `X.Y.Z` — force the bump; otherwise derive it from `[Unreleased]`.
- `--no-build` — skip the archive even when the plan has a `build` command.
- `--yes` — skip the confirmation.

## Steps

1. Run `uv run "$HERE/../commit/scripts/ship.py" plan release`. Done when stdout is a JSON plan.
2. If the plan's `branch` is not `default_branch`, stop and say to integrate onto the default branch first.
3. Follow `$HERE/../commit/changelog.md`. Empty `[Unreleased]` → stop; there is nothing to ship.
4. Version: the `X.Y.Z` argument if given; else bump `current_version` by `major`/`minor` if given; else `Removed` or breaking → major (below 1.0.0 → minor), else `Added` → minor, else patch. Done when the version string is known.
5. Show the plan, the changelog diff, the version, and the build command if any. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
6. Run `uv run "$HERE/../commit/scripts/ship.py" apply bump --version X.Y.Z`. Done when stdout is the version.
7. Follow `$HERE/../push/SKILL.md` with `--yes` and message `Release X.Y.Z: <summary>`. Summary is a short comma-separated reading of the changelog highlights. Done when stdout contains `pushed`.
8. Run `uv run "$HERE/../commit/scripts/ship.py" apply tag --version X.Y.Z`. Done when stdout contains the tag.
9. Run `uv run "$HERE/../commit/scripts/ship.py" apply publish --version X.Y.Z`. If it fails because `gh` is missing or origin is not GitHub, say the tag is pushed and stop after reporting that. Done when stdout contains `released`, or that report is given.
10. If the plan has `build` and `--no-build` was not given: run the build command, then `uv run "$HERE/../commit/scripts/ship.py" apply publish --version X.Y.Z --asset <zip>`. Done when stdout contains `uploaded` or `released`, or there was no archive to attach.
