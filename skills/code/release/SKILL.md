---
name: release
description: Ship a version — changelog, bump, push, tag, and GitHub release.
disable-model-invocation: true
argument-hint: "[--no-build] [--yes] [minor|major|X.Y.Z] [-- <instruction>]"
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

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/release`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

The operand is the version to ship — `X.Y.Z` exactly, or `minor` or `major` as the bump to apply — and step 4 says what its absence means. `--no-build` skips the archive step 10 would build and attach; `--yes` answers the wait in step 5. `gh` is required only for the GitHub release step.

## Steps

1. Run `uv run "$LIBRARY/scripts/ship.py" plan release`. Done when stdout is a JSON plan.
2. If the plan's `branch` is not `default_branch`, stop and say to integrate onto the default branch first.
3. Follow `$LIBRARY/references/changelog.md`. Empty `[Unreleased]` → stop; there is nothing to ship.
4. Version: the `X.Y.Z` argument if given; else bump `current_version` by `major`/`minor` if given; else `Removed` or breaking → major (below 1.0.0 → minor), else `Added` → minor, else patch. Done when the version string is known.
5. Show the plan, the changelog diff, the version, and the build command if any. If the user asks to see every commit, re-run `plan --full release` and show that plan. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
6. Run `uv run "$LIBRARY/scripts/ship.py" apply bump --version=X.Y.Z`. Done when stdout is the version.
7. Follow `$HERE/../push/SKILL.md` with the Formal Invocation `--yes "Release X.Y.Z: <summary>"`. Summary is a short comma-separated reading of the changelog highlights. If the outer Contextual Instruction contains guidance relevant to push, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. Done when stdout contains `pushed`.
8. Run `uv run "$LIBRARY/scripts/ship.py" apply tag --version=X.Y.Z`. Done when stdout contains the tag.
9. Run `uv run "$LIBRARY/scripts/ship.py" apply publish --version=X.Y.Z`. If it fails because `gh` is missing or origin is not GitHub, say the tag is pushed and stop after reporting that. Done when stdout contains `released`, or that report is given.
10. If the plan has `build` and `--no-build` was not given: run the build command, then `uv run "$LIBRARY/scripts/ship.py" apply publish --version=X.Y.Z --asset=<zip>`. Done when stdout contains `uploaded` or `released`, or there was no archive to attach.
