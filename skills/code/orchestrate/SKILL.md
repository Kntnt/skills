---
name: orchestrate
description: Work the tracker's ready-for-agent tickets unattended — claim, build, and independently verify one ticket at a time on the current branch.
disable-model-invocation: true
argument-hint: '[--dry-run] [--model <name>] [--yes]'
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

Read the tracker, and work the `ready-for-agent` tickets it holds on the branch the developer is already on: one at a time, each built by its own subagent and verified by a second one that did not build it.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, do no work, install nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Steps

1. Run `uv run "$HERE/scripts/run.py" plan`, passing the user's `--dry-run`, `--model`, and `--yes` through. Done when stdout is the JSON plan; anything else on stdout means the engine refused the arguments, so show stderr and stop.
2. Where `ready` is false: go to step 8, having started nothing. `reason` is why no run may start, and a dry run is one of those reasons. Done when you have stopped or `ready` is true.
3. Take the first ticket in `workable` and claim it: `uv run "$HERE/scripts/run.py" claim --ticket <number>`. Exit 2 means another session or a person already has it — leave it untouched, record nothing, and claim the next ticket in `workable` instead. Done when a claim is taken, or `workable` is exhausted and you go to step 8.
4. Build it in a subagent with its own context window, on the model `model` names where it names one. Read `$HERE/brief.md`, fill it in from that ticket's entry in `tickets`, and give the subagent the filled-in brief and nothing else. Never build a ticket in this context: a ticket built here is a ticket whose builder and verifier are the same session, and the run would be reporting on itself. Done when the subagent has finished or stopped and reported.
5. Verify it in a second subagent that has not seen the building session, and that is told nothing the builder said. Read `$HERE/verify.md`, fill it in from the same entry, and give it that. Its verdict decides; the builder's report is evidence of nothing. No argument, flag, or circumstance skips this step. Done when that subagent has given a verdict.
6. Record the outcome. A pass: `uv run "$HERE/scripts/run.py" record --ticket <number> --outcome done --commit "$(git rev-parse HEAD)"`, which closes the ticket. Anything else, including a builder that stopped and reported: the same command with `--outcome failed` and no `--commit`, which leaves the ticket open and claimed so nothing retries it. Done when the engine has stored the outcome.
7. On a pass, run step 1's `plan` command again and go to step 3 with what it now returns — the outcome you just recorded is what changes it: a closed ticket unblocks whatever waited on it, and a recorded failure strands whatever waited on that. Never carry a ticket forward from an earlier plan; the plan you act on is always the one you just read. On a failure, go to step 8: the ticket's work is on the branch unverified, and the next ticket would be built on top of it. Done when a ticket has failed or no ticket is workable.
8. Report the run in one go, rather than as a running commentary, and render it from what the engine returned rather than from your own account of the session. Where nothing started, that account is the last plan's `reason` together with its `waves`, `workable`, `claimed`, `recorded`, `stranded`, and `never_workable` — which is what a dry run is read for — and you are done. Otherwise run `uv run "$HERE/scripts/run.py" report` and give the developer what it emits: its `branch`, then every ticket in scope under the outcome it fell to — `done`, `failed`, `conflicted`, `stranded` behind a failure, and `never_on_frontier`, which is every ticket this run never had on its frontier, whether held by a cycle, by work outside the run, by another session's claim, or by the run stopping before its wave came round. Name each ticket by number and title from `tickets`, and give its `commit` where the outcome carries one. Those five lists are the whole account and each ticket is in exactly one of them, so render them as they came and never compose a sixth grouping, drop a list because it is empty, or add a ticket from your own memory of the session. Say plainly that a failed ticket's work is still on the branch and was not reverted. Done when the user has that report.
