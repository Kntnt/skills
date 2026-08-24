---
name: release
description: Ship a version — changelog, bump, push, tag, and GitHub release.
disable-model-invocation: true
argument-hint: "[minor|major|X.Y.Z] [--no-build] [--yes] [-- <instruction>]"
compatibility: Requires git and uv; gh only for the GitHub release step
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git uv"
  kntnt.skills: "push"
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# release

Ship a version from the default branch: changelog, bump, push, tag, GitHub release, optional archive.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`). `gh` is required only for the GitHub release step.

`$HERE` is the directory that contains this SKILL.md.

`$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

`/release [minor|major|X.Y.Z] [--no-build] [--yes]`, and nothing else.

Anything else is an invalid form. Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/release --help` for the page in full. Then ship nothing and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Run `uv run "$LIBRARY/scripts/ship.py" plan release`. Done when stdout is a JSON plan.
2. If the plan's `branch` is not `default_branch`, stop and say to integrate onto the default branch first.
3. Follow `$LIBRARY/references/changelog.md`. Empty `[Unreleased]` → stop; there is nothing to ship.
4. Version: the `X.Y.Z` argument if given; else bump `current_version` by `major`/`minor` if given; else `Removed` or breaking → major (below 1.0.0 → minor), else `Added` → minor, else patch. Done when the version string is known.
5. Show the plan, the changelog diff, the version, and the build command if any. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
6. Run `uv run "$LIBRARY/scripts/ship.py" apply bump --version=X.Y.Z`. Done when stdout is the version.
7. Follow `$HERE/../push/SKILL.md` with the Formal Invocation `"Release X.Y.Z: <summary>" --yes`. Summary is a short comma-separated reading of the changelog highlights. If the outer Contextual Instruction contains guidance relevant to push, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. Done when stdout contains `pushed`.
8. Run `uv run "$LIBRARY/scripts/ship.py" apply tag --version=X.Y.Z`. Done when stdout contains the tag.
9. Run `uv run "$LIBRARY/scripts/ship.py" apply publish --version=X.Y.Z`. If it fails because `gh` is missing or origin is not GitHub, say the tag is pushed and stop after reporting that. Done when stdout contains `released`, or that report is given.
10. If the plan has `build` and `--no-build` was not given: run the build command, then `uv run "$LIBRARY/scripts/ship.py" apply publish --version=X.Y.Z --asset=<zip>`. Done when stdout contains `uploaded` or `released`, or there was no archive to attach.
