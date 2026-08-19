# release

Ship a version — changelog, bump, push, tag, and GitHub release.

## Synopsis

`/release [minor|major|X.Y.Z] [--no-build] [--yes]`

## Description

Takes what is in `[Unreleased]` and turns it into a released version, from the default branch and nowhere else. In order: the changelog is reconciled and its `[Unreleased]` section promoted to the new version under today's date, the version is written into the files that carry it, the branch is committed and pushed, an annotated tag is created and pushed, and a GitHub release is published from the changelog section. Where the project has a build that produces an archive, that archive is attached to the release.

The version is derived from the changelog unless you name one: a `Removed` section or a breaking change makes it a major bump — a minor one below 1.0.0 — an `Added` section makes it minor, and anything else a patch.

Nothing is written before you have seen it. The plan, the changelog diff, the version, and the build command are shown and waited on.

## Arguments

- `minor`, `major`, or `X.Y.Z` — force the bump rather than deriving it from `[Unreleased]`.

## Options

- `--no-build` — skip the archive even where the project has a build command.
- `--yes` — assume yes: release without waiting for a confirmation.

## Notes

A flag with no work to do on the invocation you typed is refused rather than ignored, because a flag accepted and ignored teaches that flags sometimes do nothing. So `/release --dry-run` is an error, while `/release minor --no-build --yes` is not. An invalid form is refused the same way, so this skill has one failure behaviour rather than one per kind of mistake: the synopsis above, a line saying what was wrong, and nothing done.

A branch that is not the default branch stops the run: integrate first. An empty `[Unreleased]` stops it too — there is nothing to ship.

A version that cannot be rewritten unambiguously aborts the whole bump rather than leaving some files written and others not.

Where `gh` is missing or the remote is not GitHub, the tag is pushed and that is reported as the end of it: the release is the only step that needs GitHub.

## Dependencies

`git` and `uv` on PATH, the push skill Enabled, and the manager installed — the skill checks for both and says how to install them if they are missing. `gh` is required only for the GitHub release step.

## See also

`/commit` records the working tree. `/push` commits and pushes.
