# orchestrate

Work the tracker's ready-for-agent tickets unattended, on the branch you are already on.

## Synopsis

`/orchestrate [#<ticket-or-spec> ...] [--dry-run] [--at-once <n>] [--model <name>] [--yes]`

## Description

Reads the issue tracker for this repository, works out which tickets an unattended run can start, and then works them: every open ticket carrying `ready-for-agent`, a wave at a time, or the part of them you aimed the run at. A ticket without that label never appears, because a ticket without it is unfinished thinking and is never built.

The blocking edges between those tickets make the plan a wave plan rather than a list. Wave one is what may start now; each later wave is what the wave before it unblocks. An edge comes from the tracker's own blocked-by relation, and where a ticket carries none, from a `Blocked by` line in its body naming other tickets — which is how the ticket breakdown writes an edge the tracker has no relation for. The body is that fallback and not a second source: where the relation carries any edge at all, it is the whole of that ticket's edges. A body edge is a bare `#number`; one written as `owner/repo#number` is refused rather than read, because a run reads one repository's tracker and cannot tell such a reference in it from one somewhere else. A blocker that is already closed names work that exists and blocks nothing.

Each ticket goes the same way. It is **claimed** on the tracker before any work on it starts, by assigning it, so a second session you start in parallel sees it taken and skips it — and so a ticket a person has taken is left alone too. It is then **built** by a subagent with its own context window, so a long run does not degrade as one context fills. The brief that subagent gets carries the ticket as the tracker now holds it rather than a summary of it — the body it was filed with, followed by everything written on it since, oldest first and each comment attributed and dated. That matters because a ticket is a thread: triage answers the body's open questions in a comment, and a builder given only the body would be answering them again. Where a comment contradicts the body the later text stands, and an acceptance criterion stated in a comment is one of the ticket's criteria. What a run wrote on the ticket itself — the outcome it recorded, the note it leaves before a rebuild — is left out, that being the engine talking to its next self. The brief also carries the ticket's parent spec with the instruction to read its testing decisions before writing any test, the instruction to build test-first, and the fact that nobody is watching — which makes a genuine decision something to stop and report rather than guess at.

The tickets that are workable now are built at the same time rather than one after another, up to the ceiling `--at-once` sets, so no ticket waits on an unrelated one. Above a ceiling of one, each ticket is built in a working tree of its own, cut from where your branch stands and kept under the repository's own git directory — your working tree is where you left it, and `git status` says nothing about a run in progress. A ceiling of exactly one needs none of that: the ticket is built where you are, on the branch you are on, and there is nothing to integrate.

It is then **verified** by a second subagent that never saw the building session and is told nothing the builder claimed. It is given the same account of the ticket the builder was given, body and thread alike, so a criterion stated in a comment is a criterion the verdict is taken against. That subagent runs the project's full verification itself and checks each acceptance criterion against the repository as it now is. Its verdict is what decides. There is no flag, argument, or circumstance that skips it, because a run that can report success it cannot support is worse than no run at all.

Only then is the ticket **integrated** — merged into the branch you started the run on — and **closed**, together with the commit that carries the work. That happens as each wave completes rather than at the end of the run, because a ticket in a later wave is blocked by one in an earlier wave: it builds on that code and must have it. Once a wave is merged, the project's full verification runs once more on the branch as it now stands, which is what catches two tickets that pass alone and fail together; a failure there stops the run rather than spending the remaining hours building on broken code, and the tickets it never attempted are named in the report. The working tree of a merged ticket is taken away and its branch with it, so you come back to one branch and a tidy machine.

A collision at the merge is repaired rather than reported straight away, because two tickets that both added an import should not cost a full rebuild. The run branch is merged into the losing ticket's own branch and the conflict is settled there, by a subagent that is given both tickets as they were filed — nothing is settled on your branch, which never carries a resolution nobody has checked. A second subagent that did not make that resolution then verifies it against **both** tickets' acceptance criteria and runs the project's full verification itself, because the way a repair fails quietly is by keeping one ticket's criteria and dropping the other's. On a pass the ticket merges and closes as any other does. Where it does not verify — the resolver hit a genuine disagreement the two bodies do not settle, or the verdict is a fail — the repair is thrown away with the working tree that holds it and the ticket is built again from nothing on top of the work it collided with, where it cannot collide again. That rebuild happens at most once per ticket and is the only rerun the run performs; a ticket that collides a second time is recorded conflicted instead. You are never asked to resolve anything mid-run.

A ticket that fails verification is written down as failed and left open and claimed, and it is not retried: the conditions of a rerun would be identical and so would the outcome. Nothing merges it, so its working tree stays exactly where it stood, which is where you look at what it did. Above a ceiling of one the run carries on — the failure is contained in a working tree of its own, and what waited on that ticket comes back stranded rather than built on code that does not exist. At a ceiling of one the run stops there instead, the unverified work being on your branch already.

Every outcome is written on the ticket it belongs to, which is where the next run reads it back from. So what has been recorded changes what comes next: a ticket already recorded is never offered again, and a ticket whose blocker failed comes back **stranded** — not workable, because the work it builds on does not exist, and not missing from the account either, which is what a loop that only tracks what it can start drops without saying so.

## Aiming the run

Typed bare, the run works every open ticket carrying the label. Name tickets or specs and it works those instead:

- **A ticket** — `/orchestrate #14` — works that ticket and no other. This is how one ticket is picked up on its own, without replaying the rest of the graph.
- **A spec** — `/orchestrate #6` — works that spec's children, so tickets from an unrelated effort in the same tracker are left alone. The spec itself is never built, even where it carries the label: what has children is the shape of other work rather than work.
- **Several of either** — `/orchestrate #14 #6 #21` — works the union of what they resolve to, in one run and one report. Every reference is read on its own exactly as a lone one is, so a ticket named twice, or named beside the spec that holds it, aims the run at the same set as either alone; the set is the set, and naming a ticket again is not an error.

Which of the two a reference named is the tracker's answer and not a guess, and it is asked once per reference. A reference the tracker files children under is a spec; where it files none, a ticket in scope naming it as its parent says the same thing, that being the other way the ticket breakdown writes the relation. Anything else the tracker can answer for is a ticket. A reference nothing can resolve — a number the tracker does not know, something that is not a number, or one written as `owner/repo#number` — is named as such and nothing is started, and one such reference stops the whole invocation however many readable ones stand beside it: working the rest of them would work a scope you did not name.

Aiming a run narrows what it works and changes nothing else about it. A named ticket still waits for the work it is blocked by — including work another ticket you named delivers, which is why several tickets come back laid out in waves rather than started together — and is reported as waiting rather than built on top of code that does not exist. A ticket whose outcome a run has already recorded is still settled, and naming it does not offer it again — clear that outcome from the ticket if you mean to build it afresh.

## Continuing an interrupted run

A run that was interrupted — the machine slept, the session was killed, you closed the laptop — is continued by starting it again exactly as you started it the first time. There is no resume flag, and none to forget: a ticket already recorded is never offered again, so an interruption costs you the tickets that were left rather than the ones that were built, and the ticket the run was on when it stopped is picked up again rather than treated as taken.

What makes that work is the tracker: outcomes are written on the tickets themselves, so a fresh session reads them exactly as the session that wrote them did. Alongside that, the run keeps a note of what it has claimed in whatever per-session scratch directory your harness provides. That note is remembered, never relied on — where it is gone, and after a machine restart it will be, the run rebuilds what it needs from the tracker and the branch and reaches the same account. What it buys is the one thing the tracker cannot say: whether a ticket standing in your name is a run of yours that stopped or a second one you started in parallel and is working right now.

## The report

The run ends with one report rather than a running commentary, so you read the whole night in one sitting. Every ticket in scope is in it exactly once — the whole label where you named nothing, and what you aimed the run at where you did — under one of five outcomes:

- **done** — built, independently verified, and closed on the commit that carries the work.
- **failed** — verification did not pass. The work was not reverted: it stands in the ticket's own working tree, or on your branch where the run made none, so you can look at it either way.
- **conflicted** — this ticket's work collided with work already on the branch, and neither the repair nor the rebuild that followed it settled the collision. Its working tree stands, and the report names the files the two tickets both touched together with the ticket on the other side of them — that pair is a blocking edge your ticket breakdown was missing, and fixing it there is how this run improves the next one.
- **stranded** — waiting, directly or through others, on a ticket that did not pass.
- **never on the frontier** — everything this run never had a chance at: tickets waiting on each other in a circle, tickets waiting on open work outside the run, tickets another session has claimed, and tickets whose wave never came round because the run stopped first — which is where the tickets a failed integration cost you are named.

There is no sixth pile and no ticket in two of them. A ticket the run dropped in silence is one you would not know to pick up. The report also names the commit the run's work sits on top of, so a night reads as one diff from there to the head of your branch.

## Options

- `--dry-run` — plan the run, print what would be worked, and start nothing. It reads the run you aimed, so a scope is honoured here exactly as it is when work starts.
- `--at-once <n>` — how many tickets are built at the same time, so concurrent test suites do not overload the machine and fail for the wrong reason. One by default. Above one, each ticket gets a working tree of its own and the work is merged into your branch wave by wave; exactly one keeps everything on your branch with nothing to integrate. The ceiling carries that isolation decision with it, because isolation is not a separate choice to make.
- `--model <name>` — the model the building subagents run on, so mechanical work can run cheaper than judgement work. Verification is not affected.
- `--yes` — assume yes: answer any question the run would otherwise ask.

## Notes

A flag with no work to do on the invocation you typed is refused rather than ignored, because a flag accepted and ignored teaches that flags sometimes do nothing. So `/orchestrate --force` is an error, while `/orchestrate #21 --at-once 3 --yes` is not. An invalid form is refused the same way, so this skill has one failure behaviour rather than one per kind of mistake: the synopsis above, a line saying what was wrong, and nothing done.

At a ceiling of one, work is committed straight to the branch you were on, one commit per ticket, and nothing is merged because there is nothing to integrate. Above one, each ticket is committed on a branch of its own in a working tree under `.git/kntnt-orchestrate/<number>`, and merged into your branch as its wave completes; the working tree and branch of a merged ticket are removed, and those of a failed or conflicted one are kept where they are. The one exception is a ticket being rebuilt after a repair that did not verify: that working tree and branch are discarded, uncommitted work and all, because what they hold is a resolution a verifier has just refused. Either way the run ends with everything on the one branch you started it on.

A working tree is named for its ticket and its branch for the run that made it, and it is the branch that says whose it is. So a tree left standing by a run on another branch — interrupted, or kept because its ticket failed — is named rather than picked up: this run would otherwise build its ticket on top of that branch's work and merge the result onto yours. Look at what is in it, then remove it with `git worktree remove`, and the ticket can be worked again.

A run refuses a working tree that holds work nothing has committed. It commits where you left off, and it cannot tell a change you had not committed from the work it is about to do: at a ceiling of one that change lands inside a ticket's own commit, and above one it stops a merge that had nothing to collide with. Commit it or stash it, and start the run again. What the repository ignores is not work and never refuses anything. The same question is asked once more before a ticket is closed, because that is the last moment work that was never committed can be told from work that was.

Where a ticket in scope is claimed, the run asks the tracker who you are, so it can tell a claim of your own from somebody else's — and where the tracker will not say, it stops and tells you rather than guess. Either guess is one an unattended night should not make: reading your own interrupted claim as a stranger's leaves the work undone, and reading a stranger's as your own builds the same ticket twice. Nothing is asked and nothing refuses where no ticket in scope is claimed.

A failed ticket's work is never reverted, so you can look at it. At a ceiling of one that work is on your branch, which is also why the run stops at the first failure: the next ticket would otherwise be built on top of unverified code. Above one it is in the ticket's own working tree and reaches your branch only by being merged, so the run carries on and what waited on that ticket comes back stranded.

Nothing is pushed, tagged, or released, and no ticket is created or triaged. `/release` ships a version; this skill consumes tickets somebody else has decided are ready.

A repository whose tracker holds no ready-for-agent ticket is said so, and nothing starts. So is a scope where no ticket is workable at all — tickets waiting on each other in a circle, or on open work the run will never build because it carries no label — and one where every workable ticket is already claimed.

## Dependencies

`git`, `gh`, and `uv` on PATH, the manager installed, and a harness that can spawn subagents. The last one is a Capability no script can test: the skill asks you to confirm it, and does no work where it is not true.

The tracker has to answer for more than the binary being there. Every plan asks it for each ticket's blocked-by relation and its parent, and a run aimed at a reference asks what is filed under that reference — so the repository needs issue dependencies and sub-issues, and `gh` needs to be new enough to know those fields. Where either is missing the first plan stops with what `gh` said, which names the field it could not answer for; `gh` upgraded, or the tracker's relations turned on, is what fixes it. The `Blocked by` and `Parent` lines a ticket body can carry are a fallback for a ticket that has no relation, not for a tracker that has none. `gh` also has to be authenticated for this repository, since the run claims tickets, comments on them, and closes them.

## See also

`/commit` records what a run leaves on the branch. `/kntnt select` to Enable this skill elsewhere.
