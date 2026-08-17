# Land one approved Plan

Bring one approved Plan's work onto the branch the run started on, as a single commit made by the `commit` skill, and leave nothing behind. `improve` reports the worktree's path and its branch with the verdict; both are needed here.

1. Stage the work. Run `git merge --squash <the worktree branch>` from the run's branch. It leaves the changes in the working tree without committing. It cannot conflict: the worktree was created from the commit this branch is on, because the previous Plan was Landed before this one was dispatched. Done when `git status --porcelain` shows the Plan's files.
2. Set this Plan's row in `plans/README.md` to DONE, so the status lands in the same commit as the work it describes. Done when the row reads DONE.
3. Commit. Follow `$HERE/../commit/SKILL.md` with `--yes` and the Plan's title as the message, dropping its `Plan NNN:` prefix so the subject line stands on its own. Done when it reports a commit SHA.
4. Remember that SHA. It is where `HEAD` must stand when the next Plan is dispatched. Done when it is recorded.
5. Clean up. Run `git worktree remove <the worktree path> --force`, then `git branch -D <the worktree branch>`. Done when `git worktree list` shows only the main tree and `git branch` no longer lists it.
