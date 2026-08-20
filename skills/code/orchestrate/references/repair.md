# The repair brief

Give this to a subagent when `integrate` answers with a collision. It is filled in from the losing ticket's entry in the plan, from what `isolate` answered for it, and from what `integrate` answered: `<files>` is the collision's `collisions`, and `<others>` is one block per ticket in its `collided_with`, each carrying that ticket's number, title, url, and whole body from the plan's `tickets`. Where `collided_with` is empty, say instead that the work on the other side of the collision is the branch's own and no ticket in this run claims it. Everything in angle brackets is replaced; each `<body>` is pasted whole.

---

You are repairing a collision between two tickets that were built at the same time. Both were built alone, both passed verification alone, and they touched the same code — so the second one will not merge onto the branch the first is already on. Your job is to find out whether that is a cheap repair or not. Two added imports should not cost a full rebuild; a genuine disagreement about what the code should do is not yours to settle.

**Where you work.** In `<worktree>`, with the branch `<branch>` checked out in it. Everything you do happens there and nowhere else. The developer's branch `<run-branch>` already carries the other ticket's work, and you are bringing it here rather than putting anything there — nothing reaches that branch until a verifier that has not seen you says this repair holds.

**The ticket you are repairing.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**What it collided with.** `<others>`

**They collided in these files.** `<files>`

Do all of this, in this order:

1. **Bring the other work here.** `git merge <run-branch>` in your working tree. It will stop on the conflicts above; that is the point of running it.
2. **Settle each conflict so both tickets still hold.** Read what each side was doing and why, in the two bodies above, and produce the code somebody would have written had they built both. Not one side picked over the other, and not both pasted together — a resolution that keeps one ticket's criteria by dropping the other's is a repair that failed.
3. **Run the project's full verification yourself**, every command its contributing guide names for a change. A repair you did not run is a guess.
4. **Commit the merge.** Stage what you settled and commit it, leaving nothing uncommitted and nothing unmerged: work only a working tree holds is work the run cannot integrate.

**Do not go further than the repair.** Do not fix an unrelated failure, refactor around the conflict, or build anything either ticket left undone. Do not push, do not merge anything into `<run-branch>`, and touch no branch other than `<branch>`, the one you were given.

**Nobody is watching.** There is no human in this session to ask, and no answer is coming. Where the two tickets genuinely disagree — they made incompatible decisions the bodies do not settle, or holding both means designing something neither one specified — that is not a cheap repair and not yours to guess at. Stop, leave the merge unfinished, and report what the disagreement is. The run's answer to that is to build this ticket again from nothing on top of the other one's work, which costs one ticket's build and produces code somebody meant.

**Report.** Whether you settled it, what you decided at each conflict and why, and what you ran. Your report is not evidence: a separate session that has not seen this one verifies the repaired working tree against both tickets' acceptance criteria, and its verdict is what counts.
