# orchestrate

Work the tracker's ready-for-agent tickets unattended, on the branch you are already on.

## Synopsis

`/orchestrate [--dry-run] [--model <name>] [--yes]`

## Description

Reads the issue tracker for this repository, works out which tickets an unattended run can start, and then works them: every open ticket carrying `ready-for-agent`, one at a time. A ticket without that label never appears, because a ticket without it is unfinished thinking and is never built.

The blocking edges between those tickets make the plan a wave plan rather than a list. Wave one is what may start now; each later wave is what the wave before it unblocks. An edge comes from the tracker's own blocked-by relation, and where a ticket carries none, from a `Blocked by` line in its body naming other tickets — which is how the ticket breakdown writes an edge the tracker has no relation for. The body is that fallback and not a second source: where the relation carries any edge at all, it is the whole of that ticket's edges. A body edge is a bare `#number`; one written as `owner/repo#number` is refused rather than read, because a run reads one repository's tracker and cannot tell such a reference in it from one somewhere else. A blocker that is already closed names work that exists and blocks nothing.

Each ticket goes the same way. It is **claimed** on the tracker before any work on it starts, by assigning it, so a second session you start in parallel sees it taken and skips it — and so a ticket a person has taken is left alone too. It is then **built** by a subagent with its own context window, so a long run does not degrade as one context fills. The brief that subagent gets carries the ticket's body as it was filed rather than a summary of it, the ticket's parent spec with the instruction to read its testing decisions before writing any test, the instruction to build test-first, and the fact that nobody is watching — which makes a genuine decision something to stop and report rather than guess at.

It is then **verified** by a second subagent that never saw the building session and is told nothing the builder claimed. That subagent runs the project's full verification itself and checks each acceptance criterion against the repository as it now is. Its verdict is what decides. There is no flag, argument, or circumstance that skips it, because a run that can report success it cannot support is worse than no run at all.

Only then is the ticket **closed**, together with the commit that carries the work. A ticket that fails verification is written down as failed and left open and claimed, and the run stops there. It is not retried: the conditions of a rerun would be identical and so would the outcome.

Every outcome is written on the ticket it belongs to, which is where the next run reads it back from. So what has been recorded changes what comes next: a ticket already recorded is never offered again, and a ticket whose blocker failed comes back **stranded** — not workable, because the work it builds on does not exist, and not missing from the account either, which is what a loop that only tracks what it can start drops without saying so.

## The report

The run ends with one report rather than a running commentary, so you read the whole night in one sitting. Every ticket in scope is in it exactly once, under one of five outcomes:

- **done** — built, independently verified, and closed on the commit that carries the work.
- **failed** — verification did not pass. The work is still on the branch and was not reverted, so you can look at it.
- **conflicted** — this ticket's work collided with another's and the collision was not repaired. Nothing produces this outcome yet; collisions arrive with integration, and the account has a place for them from the start.
- **stranded** — waiting, directly or through others, on a ticket that did not pass.
- **never on the frontier** — everything this run never had a chance at: tickets waiting on each other in a circle, tickets waiting on open work outside the run, tickets another session has claimed, and tickets whose wave never came round because the run stopped first.

There is no sixth pile and no ticket in two of them. A ticket the run dropped in silence is one you would not know to pick up.

## Options

- `--dry-run` — plan the run, print what would be worked, and start nothing.
- `--model <name>` — the model the building subagents run on, so mechanical work can run cheaper than judgement work. Verification is not affected.
- `--yes` — assume yes: answer any question the run would otherwise ask.

## Notes

Work is committed straight to the branch you were on, one commit per ticket. Nothing is merged, because there is nothing to integrate: this run works one ticket at a time and no worktree is created.

A run refuses on the repository's default branch and says so — an unattended night must never land there. The plan is still printed, so you can read the scope from the branch you happen to be on. Where nothing can say which branch is the default — no remote to ask, and neither `main` nor `master` in the repository — it refuses rather than guess, and tells you to name it. A guess would either work the branch it must not touch, or refuse the branch you are on under a reason that is not true.

A failed ticket's work is left on the branch rather than reverted, so you can look at it. That is also why the run stops at the first failure: the next ticket would otherwise be built on top of unverified code.

Nothing is pushed, tagged, or released, and no ticket is created or triaged. `/release` ships a version; this skill consumes tickets somebody else has decided are ready.

A repository whose tracker holds no ready-for-agent ticket is said so, and nothing starts. So is a scope where no ticket is workable at all — tickets waiting on each other in a circle, or on open work the run will never build because it carries no label — and one where every workable ticket is already claimed.

## Dependencies

`git`, `gh`, and `uv` on PATH, the manager installed, and a harness that can spawn subagents. The last one is a Capability no script can test: the skill asks you to confirm it, and does no work where it is not true.

## See also

`/commit` records what a run leaves on the branch. `/kntnt select` to Enable this skill elsewhere.
