# commit

Commit the working tree on the current branch, without pushing.

## Synopsis

`/commit ["message"] [--yes]`

## Description

Records everything the working tree holds as one commit on the branch you are on, and stops there. Nothing is pushed, tagged, or released.

Before the commit is made, `CHANGELOG.md` is brought in line with what actually changed: an `[Unreleased]` section is written or extended, and a change already recorded anywhere in the file is not written twice. Only that section is edited — no version is promoted, bumped, or dated.

The commit message is the `"message"` argument when you give one. Otherwise it is a single concrete subject line drawn from the changelog entries just written, or from the diff where a change has no user-facing entry.

Nothing is written before you have seen it. The changelog diff, the message, and any proposed `.gitignore` are shown and waited on.

## Arguments

- `"message"` — use this as the commit message instead of one derived from the changes.

## Options

- `--yes` — assume yes: commit without waiting for a confirmation.

## Notes

A flag with no work to do on the invocation you typed is refused rather than ignored, because a flag accepted and ignored teaches that flags sometimes do nothing. So `/commit --force` is an error, while `/commit "a subject line" --yes` is not. An invalid form is refused the same way, so this skill has one failure behaviour rather than one per kind of mistake: the synopsis above, a line saying what was wrong, and nothing done.

A working tree with nothing to commit is said so and nothing happens.

Where untracked files look like they belong in `.gitignore` rather than in the repository, that addition is proposed with the rest and stands or falls with the same confirmation.

## Dependencies

`git` and `uv` on PATH, and the manager installed — the skill checks for it and says how to install it if it is missing.

## See also

`/push` commits and then pushes the branch. `/release` ships a version.
