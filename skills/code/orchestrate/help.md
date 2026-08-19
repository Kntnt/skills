# orchestrate

Plan an unattended run over the tracker's ready-for-agent tickets, as a wave plan.

## Synopsis

`/orchestrate [--dry-run] [--yes]`

## Description

Reads the issue tracker for this repository and reports the tickets an unattended run would work: every open ticket carrying `ready-for-agent`, and which of them are workable now. A ticket without that label never appears, because a ticket without it is unfinished thinking and is never built.

The blocking edges between those tickets make the report a wave plan rather than a list. Wave one is what may start now; each later wave is what the wave before it unblocks. An edge comes from the tracker's own blocked-by relation, and where a ticket carries none, from a `Blocked by` line in its body naming other tickets — which is how the ticket breakdown writes an edge the tracker has no relation for. The body is that fallback and not a second source: where the relation carries any edge at all, it is the whole of that ticket's edges. A body edge is a bare `#number`; one written as `owner/repo#number` is refused rather than read, because a run reads one repository's tracker and cannot tell such a reference in it from one somewhere else. A blocker that is already closed names work that exists and blocks nothing.

The report is what you check before committing a night to a run. It names the branch the run would use, the shape of the night in waves, and the reason where no run may start at all.

It plans; it does not build. Working a ticket means briefing a session for it and verifying the result independently, and this skill grows into that. What it gives you today is the scope.

## Options

- `--dry-run` — plan the run, print what would be worked, and start nothing.
- `--yes` — assume yes: answer any question the run would otherwise ask.

## Notes

A run works the branch you are on, so it refuses on the repository's default branch and says so — an unattended night must never land there. The plan is still printed, so you can read the scope from the branch you happen to be on.

Where nothing can say which branch is the default — no remote to ask, and neither `main` nor `master` in the repository — it refuses rather than guess, and tells you to name it. A guess would either work the branch it must not touch, or refuse the branch you are on under a reason that is not true.

Nothing is pushed, tagged, or released, and no ticket is created or triaged. `/release` ships a version; this skill consumes tickets somebody else has decided are ready.

A repository whose tracker holds no ready-for-agent ticket is said so, and nothing starts. So is a scope where no ticket is workable at all — tickets waiting on each other in a circle, or on open work the run will never build because it carries no label. Those are named as reached by no wave, and nothing starts rather than a frontier being turned over that never grows.

## Dependencies

`git`, `gh`, and `uv` on PATH, the manager installed, and a harness that can spawn subagents. The last one is a Capability no script can test: the skill asks you to confirm it, and does no work where it is not true.

## See also

`/commit` records what a run leaves on the branch. `/kntnt select` to Enable this skill elsewhere.
