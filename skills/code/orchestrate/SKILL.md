---
name: orchestrate
description: Work the tracker's ready-for-agent tickets unattended — claim, build, and independently verify them a wave at a time, integrating each wave into the current branch.
disable-model-invocation: true
argument-hint: '[#<ticket-or-spec>] [--dry-run] [--at-once <n>] [--model <name>] [--yes]'
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - gh
      - uv
    capabilities:
      - subagents
---

# orchestrate

Read the tracker, and work the `ready-for-agent` tickets it holds on the branch the developer is already on: a wave at a time, each ticket built by its own subagent, verified by a second one that did not build it, and integrated into that branch as its wave completes.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, do no work, install nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Steps

Every command below takes `--state-dir <directory>`. Pass whatever per-session scratchpad or temporary directory your harness gives you, the same one on every call, so what this run has claimed survives a compaction. Where your harness gives you none, leave the flag off: its absence is not an error, and the engine rebuilds what it needs from the tracker and the branch. There is no resume flag and none is wanted — re-invoked with the same arguments, this Skill continues an interrupted run rather than restarting it.

1. Run `uv run "$HERE/scripts/run.py" plan`, passing the user's `--dry-run`, `--at-once`, `--model`, and `--yes` through. Where the user named a ticket or a spec, pass it too, verbatim and as one value: `--scope "<what they wrote>"`. Never resolve that reference yourself, and never widen or narrow it — the engine reads the tracker and decides which of the two it is. Done when stdout is the JSON plan; anything else on stdout means the engine refused the arguments, so show stderr and stop.
2. Where `ready` is false: go to step 9, having started nothing. `reason` is why no run may start, and a dry run is one of those reasons. Done when you have stopped or `ready` is true.
3. Claim every ticket in `starting`, which is the frontier cut to the ceiling the developer set: `uv run "$HERE/scripts/run.py" claim --ticket <number>` for each. Exit 2 means another session or a person already has it — leave it untouched, record nothing, drop it from this wave, and claim the next ticket in `workable` that the wave does not already hold, so the ceiling stays filled. A ticket `resuming` names is one an earlier invocation of this run claimed and was interrupted before recording: it is in `workable` like any other and claiming it succeeds, the claim being already this run's own. Done when the wave is the tickets you claimed, or nothing could be claimed and you go to step 9.
4. Where `worktrees` is true, give each ticket in the wave a working tree of its own: `uv run "$HERE/scripts/run.py" isolate --ticket <number>`. It answers with the `worktree` that ticket is built and verified in and the `branch` it is built on, and a ticket picked up again gets back the working tree it was left in rather than a second one. Where `worktrees` is false the wave is one ticket and there is nothing to isolate: it is built in the repository as it stands, on the branch already checked out. Done when every ticket in the wave has somewhere to be built.
5. Build the wave, one subagent per ticket, each with its own context window and on the model `model` names where it names one. Start them together rather than one after another — working the frontier concurrently is what the ceiling is for, and a ticket that waits on an unrelated ticket is a run slower than its graph requires. Read `$HERE/brief.md`, fill it in per ticket from that ticket's entry in `tickets` and from what step 4 answered for it, and give each subagent the filled-in brief and nothing else. Never build a ticket in this context: a ticket built here is a ticket whose builder and verifier are the same session, and the run would be reporting on itself. Done when every subagent has finished or stopped and reported.
6. Verify each ticket in a second subagent that has not seen the building session, and that is told nothing the builder said. Read `$HERE/verify.md`, fill it in from the same entry and the same working tree, and give it that. Its verdict decides; the builder's report is evidence of nothing. No argument, flag, or circumstance skips this step. Done when every ticket in the wave has a verdict.
7. Integrate the wave, ticket by ticket in the order `starting` names them, and record every outcome as you go.
   - A ticket that passed, where `worktrees` is true: `uv run "$HERE/scripts/run.py" integrate --ticket <number>`. Exit 0 merges it into the run branch and takes its working tree away — record it with `record --ticket <number> --outcome done --commit <the commit it answered with>`, which closes the ticket. Exit 2 is a collision with work already on the branch: the branch is left as it was and the working tree stands, so record `--outcome conflicted` and keep its `collisions` — the files the merge could not settle — for the report.
   - A ticket that passed, where `worktrees` is false: its work is already on the branch, so record it done with `--commit "$(git rev-parse HEAD)"`.
   - Anything else, including a builder that stopped and reported: `--outcome failed` and no `--commit`, which leaves the ticket open and claimed so nothing retries it. Nothing integrates it, so its working tree stays where it is for the developer to look at.

   Done when every ticket in the wave carries an outcome.
8. Where `worktrees` is true and anything was integrated, run the project's full verification once on the integrated branch, in a subagent, from `$HERE/wave.md`. Two tickets that pass alone and fail together are caught here and nowhere else. A pass: run step 1's `plan` command again and go to step 3 with what it now returns — the outcomes you just recorded are what change it, a closed ticket unblocking whatever waited on it and a recorded failure stranding whatever waited on that. Never carry a ticket forward from an earlier plan; the plan you act on is always the one you just read. A failure: stop and go to step 9, saying which wave it was and that the run stopped rather than spend the remaining hours building on broken code. Where `worktrees` is false, there is nothing integrated to check: on a pass go to step 3 with a fresh plan as above, and on a failure go to step 9, the ticket's unverified work being on the branch itself and the next ticket otherwise built on top of it. Done when a wave has failed, a ticket has failed on a branch of its own, or no ticket is workable.
9. Report the run in one go, rather than as a running commentary, and render it from what the engine returned rather than from your own account of the session. Where nothing started, that account is the last plan's `reason` together with its `waves`, `workable`, `starting`, `claimed`, `resuming`, `recorded`, `stranded`, and `never_workable` — which is what a dry run is read for — and you are done. Otherwise run `uv run "$HERE/scripts/run.py" report`, passing the same `--scope` you passed in step 1 so the account covers what the run was aimed at, and give the developer what it emits: its `branch` and the `base` its work sits on top of, then every ticket in scope under the outcome it fell to — `done`, `failed`, `conflicted`, `stranded` behind a failure, and `never_on_frontier`, which is every ticket this run never had on its frontier, whether held by a cycle, by work outside the run, by another session's claim, or by the run stopping before its wave came round. Name each ticket by number and title from `tickets`, and give its `commit` where the outcome carries one and its `worktree` where the machine kept one, that being where a failure stands and how it is looked at. Those five lists are the whole account and each ticket is in exactly one of them, so render them as they came and never compose a sixth grouping, drop a list because it is empty, or add a ticket from your own memory of the session. Where the run stopped on an integration failure, say so and say that the tickets under `never_on_frontier` are what it did not attempt because of it. Say plainly that a failed ticket's work was not reverted — on its own branch and working tree where it had one, and on the run branch where it did not. Done when the user has that report.
