# push

Follow commit, then push the current branch.

## Synopsis

`/push ["message"] [--yes]`

## Description

Runs the commit skill with the arguments you gave — changelog, message, confirmation, commit — and then pushes the branch you are on. A working tree with nothing to commit does not stop the push: commits already made and not yet sent still go, which is what makes this the one gesture for *get my work to the remote*.

The branch is pushed to its upstream, and one is set on `origin` where the branch has none.

Nothing is pushed before you have seen what will go. Where commit already waited for a confirmation, you are not asked a second time for the same run.

## Arguments

- `"message"` — use this as the commit message instead of one derived from the changes.

## Options

- `--yes` — assume yes: commit and push without waiting for a confirmation.

## Notes

A flag with no work to do on the invocation you typed is refused rather than ignored, because a flag accepted and ignored teaches that flags sometimes do nothing. So `/push --force` is an error, while `/push --yes` is not. An invalid form is refused the same way, so this skill has one failure behaviour rather than one per kind of mistake: the synopsis above, a line saying what was wrong, and nothing done.

Nothing to send at all — a clean tree and a branch already level with its upstream — is said plainly and the run stops there.

Where the push cannot be made — no `origin` remote, a rejected non-fast-forward, a branch the remote will not take — the reason is given and the commit that was just made stays where it is, ready for another attempt.

## Dependencies

`git` and `uv` on PATH, the commit skill Enabled, and the manager installed — the skill checks for both and says how to install them if they are missing.

## See also

`/commit` stops before pushing. `/release` ships a version.
