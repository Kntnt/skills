Read when starting or resuming any session on branch `rework` until phase 3 cleanup is complete.

# Rework session handoff

This is the authoritative session checkpoint for the temporary rebuild track. It exists because both the executing session and the read-only review session closed after `/dispatch` was completed. Delete this file and its `AGENTS.md` pointer in the final cleanup ticket.

## Verified checkpoint

- Work only in `/Users/thomas/Projects/skills-rework` on branch `rework`. The product checkpoint is `8b2e2af41a50ad5d717d93203d50e84cae75009f` (`Fix Dispatch recovery review findings (#186)`), pushed to `origin/rework`; any later commit that only records this handoff does not change the reviewed product state.
- `/frame`, `/to-slices`, `/compile`, and `/dispatch` are complete. `/land` is not built. `docs/rework/01-plan.md` therefore has phase 2 IN PROGRESS and phase 3 TODO.
- #183 landed through `61dd132`; #184's final reviewed checkpoint is `831a1b47ee27f29861a49215887cdc1d4273c225`; #185 landed through `f99b5b5` plus `109bc523283b29e34be2c2e8ba9be88a8b0645f9`; #186 landed initially in `872b7322ecadbc2e3753c06de3dc17e39bd21933` and was corrected by `8b2e2af41a50ad5d717d93203d50e84cae75009f`.
- The final two-axis review from fixed point `872b7322ecadbc2e3753c06de3dc17e39bd21933` to `8b2e2af41a50ad5d717d93203d50e84cae75009f` passed with Standards 0 findings and Spec 0 findings. Do not repeat it unless Git or tracker state has changed.
- Verified gates at `8b2e2af`: `git diff --check`, Ruff lint, Ruff format for 244 files, strict mypy for 37 source files, and all 1,062 pytest tests passed. `skills-ref read-properties` passed; `validate` reported only the ADR-0112 baseline fields `argument-hint` and `disable-model-invocation`.
- #183–#186 are CLOSED, unassigned, on milestone `Skills 2.0`, with only label `rework`. #186's updated landing comment is <https://github.com/Kntnt/skills/issues/186#issuecomment-5444783178>. #183–#185 were untouched by the #186 correction.
- At review completion there was no active dispatch journal, dispatch branch, dispatch worktree, or stray pytest/Ruff/mypy/skills-ref/orchestrate process. `HEAD == origin/rework` and the worktree was clean before this handoff was authored.

## What `8b2e2af` settled

- Pre-execution stale-plan REBUILD works without an invented review, projects `await-recompile`, binds the replacement bundle to the recorded new `HEAD`, resumes safely, and shares the ticket's single REBUILD budget with the unchanged post-review path.
- Executor patch capture starts from the materialized attempt base, includes only executor-owned deltas, excludes compiler tests and dispatcher-owned writes, inventories and hashes canonical tests separately, and rejects the complete result on tampering; real-Git fixtures cover new and replaced tests.
- R3 records `fresh-context`, preserves the same role and Route evidence, costs no revision round, and must be named in the final report.
- Material execution guidance from Conversation Context is selectively included in the exact resume line before confirmation and stored as identical UTF-8 instruction bytes; irrelevant conversation context is omitted.
- `TrackerConvention` and `TrackerTransition` replace positional tracker tuples, the paragraph-comment structure is compliant, and the published wording is “otherwise greedily fill.”

## Exact next checkpoint

1. On every fresh session, run read-only state checks first: fetch `origin`, confirm the branch and sync, inspect the worktree and process state, and read `docs/rework/00-brief.md` plus `docs/rework/01-plan.md` in full. Read `docs/rework/07-dispatch.md` when preparing or exercising `/dispatch`.
2. The current action is to wait for Thomas's explicit authorization to enter phase 3 and run the first real `/dispatch` batch. Readiness is not authorization. A message explicitly approving phase 3 or the first batch supplies this gate; otherwise report the verified readiness and stop.
3. After that authorization, resume as the executing agent and follow the checkpoint protocol in `docs/rework/01-plan.md`. Prepare the remaining pipeline work, principally `/land` plus the polish and cleanup tickets, and compile it before dispatch. Gated pipeline skills are user-invocation-only: prepare the state, then hand Thomas the exact prefilled invocation line instead of invoking the skill yourself.
4. The first real dispatch batch is the acceptance run and must exercise `--at-once=2`, at least one merge conflict, and one pause-and-resume. Only successful acceptance permits deletion of old `/orchestrate`. Do not delete it earlier.
5. The takeover merge requires a second, separate explicit authorization from Thomas. Its approved shape is the `docs/rework/00-brief.md` endgame: absorb `main` history into `rework` with the `ours` strategy, then fast-forward `main` to `rework`.
6. The final cleanup removes old `/orchestrate`, the temporary `AGENTS.md` protection and this handoff pointer/file, `docs/rework/`, rework labels and milestone, and the protected worktree/branch as specified by the endgame. Until that ticket, preserve all of them.

## Track guardrails

- Never use `/orchestrate` on a rework ticket and never use `/improve` anywhere in the rebuild. Rework-ready tickets use exactly `rework` plus `rework-ready-for-agent`, never plain `ready-for-agent`; completed pre-`/land` tickets remain CLOSED with only `rework`.
- Treat gated skills as Thomas-invoked checkpoints. Give the exact invocation line, with contextual instruction prefilled, instead of paraphrasing or self-invoking it.
- Thomas prefers a fresh executing agent for each new ticket. For corrections, provide a self-contained paste block between `---` markers and tell him to copy only the text between them.
- Commits and pushes to `origin/rework` are authorized. Preserve unrelated user changes, leave the integration tree clean, and remove only processes and temporary resources started by the current session.
