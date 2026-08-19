# orchestrate

Plan an unattended run over the tracker's ready-for-agent tickets.

## Synopsis

`/orchestrate [--dry-run] [--yes]`

## Description

Reads the issue tracker for this repository and reports the tickets an unattended run would work: every open ticket carrying `ready-for-agent`, and which of them are workable now. A ticket without that label never appears, because a ticket without it is unfinished thinking and is never built.

The report is what you check before committing a night to a run. It names the branch the run would use, the tickets in scope, and the reason where no run may start at all.

It plans; it does not build. Working a ticket means briefing a session for it and verifying the result independently, and this skill grows into that. What it gives you today is the scope.

## Options

- `--dry-run` — plan the run, print what would be worked, and start nothing.
- `--yes` — assume yes: answer any question the run would otherwise ask.

## Notes

A run works the branch you are on, so it refuses on the repository's default branch and says so — an unattended night must never land there. The plan is still printed, so you can read the scope from the branch you happen to be on.

Where nothing can say which branch is the default — no remote to ask, and neither `main` nor `master` in the repository — it refuses rather than guess, and tells you to name it. A guess would either work the branch it must not touch, or refuse the branch you are on under a reason that is not true.

Nothing is pushed, tagged, or released, and no ticket is created or triaged. `/release` ships a version; this skill consumes tickets somebody else has decided are ready.

A repository whose tracker holds no ready-for-agent ticket is said so, and nothing starts.

## Dependencies

`git`, `gh`, and `uv` on PATH, the manager installed, and a harness that can spawn subagents. The last one is a Capability no script can test: the skill asks you to confirm it, and does no work where it is not true.

## See also

`/commit` records what a run leaves on the branch. `/kntnt select` to Enable this skill elsewhere.
