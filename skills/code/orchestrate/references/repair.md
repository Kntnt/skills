# The repair brief

Give this to a subagent when `integrate` answers with a collision. It is filled in from the losing ticket's entry in the plan, from what `isolate` answered for it, and from what `integrate` answered: `<files>` is the collision's `collisions`, and `<others>` is one block per ticket in its `collided_with`, each carrying that ticket's number, title, url, and whole body from the plan's `tickets`. `<scratch>` is the scratch directory `isolate` answered with for that ticket. `<gate>` is the gate you resolved at run start, pasted as the list of commands it was written down as — never re-derived here, and never widened. Where `collided_with` is empty, say instead that the work on the other side of the collision is the branch's own and no ticket in this run claims it. Everything in angle brackets is replaced; each `<body>` is pasted whole.

---

You are repairing a collision between two tickets that were built at the same time. Both were built alone, both passed verification alone, and they touched the same code — so the second one will not merge onto the branch the first is already on. Your job is to find out whether that is a cheap repair or not. Two added imports should not cost a full rebuild; a genuine disagreement about what the code should do is not yours to settle.

**Where you work.** In `<worktree>`, with the branch `<branch>` checked out in it. Everything you do happens there and nowhere else. The developer's branch `<run-branch>` already carries the other ticket's work, and you are bringing it here rather than putting anything there — nothing reaches that branch until a verifier that has not seen you says this repair holds.

**Where you write.** Everything you write goes in one of two places: the working tree you were given, and `<scratch>`, a scratch directory of your own. Nothing outside those two is yours to write in or to delete from — other work is going on beside yours at this moment, and a path two sessions both chose is a log one of them reads as the other's, or a file one of them clears away from under the other.

**What you leave running.** The rule above is about paths, and a process is not a path: whatever you start, you stop before you report. End every process you set going — a command you put in the background, and whatever you waited on it with — so that nothing you started outlives the turn that started it. Where you deliberately leave something standing, name it in your report, saying what it is and why, so the run can account for it rather than discover it. A process nobody owns is not litter: it holds the machine other work is being done on, and it goes on speaking for a session that has finished.

**The ticket you are repairing.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**What it collided with.** `<others>`

**They collided in these files.** `<files>`

Do all of this, in this order:

1. **Bring the other work here.** `git merge <run-branch>` in your working tree. It will stop on the conflicts above; that is the point of running it.
2. **Settle each conflict so both tickets still hold.** Read what each side was doing and why, in the two bodies above, and produce the code somebody would have written had they built both. Not one side picked over the other, and not both pasted together — a resolution that keeps one ticket's criteria by dropping the other's is a repair that failed.
3. **Run the project's verification gate yourself.** These commands, resolved once at run start from the project's contributing guide, are the gate: `<gate>`. Run all of them, not a subset — a check this list does not name is not run in its place, and a repair you did not run is a guess.
4. **Commit the merge.** Stage what you settled and commit it with `<!-- kntnt-orchestrate repair=<number> -->` in its message, leaving nothing uncommitted and nothing unmerged: work only a working tree holds is work the run cannot integrate.

**A long command is waited on, not yielded to.** Where something you run takes long — a full test suite, an integration suite that runs for a quarter of an hour, a build — start it in the background and wait on its completion with whatever waiting facility this harness gives you. Never end your turn while it runs. Waiting is part of the work rather than idleness to yield in: a turn ended with the gate still running is a build that did not finish or a verdict that was not reached, and in a run nobody is watching, nothing comes back to wake the session that ended it.

The wait ends with the command it waits on, and no wait survives the turn that created it. Wait with something that ends when the command ends; where the only waiting you can arrange cannot tell that it has, bound it and end it yourself before you report. A wait outliving what it waited on is no longer a wait but a leftover that goes on announcing a finished command, and in a run nobody is watching, each announcement is answered by a session that starts another.

**Do not go further than the repair.** Do not fix an unrelated failure, refactor around the conflict, or build anything either ticket left undone. Do not push, do not merge anything into `<run-branch>`, and touch no branch other than `<branch>`, the one you were given.

**Nobody is watching.** There is no human in this session to ask, and no answer is coming. Where the two tickets genuinely disagree — they made incompatible decisions the bodies do not settle, or holding both means designing something neither one specified — that is not a cheap repair and not yours to guess at. Stop, leave the merge unfinished, and report what the disagreement is. The run's answer to that is to build this ticket again from nothing on top of the other one's work, which costs one ticket's build and produces code somebody meant.

**Report.** Whether you settled it, what you decided at each conflict and why, and what you ran. Your report is not evidence: a separate session that has not seen this one verifies the repaired working tree against both tickets' acceptance criteria, and its verdict is what counts.
