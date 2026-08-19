# The tracker remembers what a run recorded

A run has to close the loop on itself: what it wrote down about one ticket must change what it is offered next. A ticket that failed verification is never retried, and everything waiting on that ticket can never be built either — so both facts have to survive the moment they were established, and be readable by the next `plan`.

There are two places they could live. One is the run's own memory: a state file, or the agent's context. The other is the tracker, where `record` already writes the outcome for a human to read. **The tracker is the store, and every verb reads its outcomes back off it.**

**An outcome the developer cannot see is not a record.** The developer will look at the ticket, not at a scratch file. An outcome written in two places is an outcome that can disagree with itself, and the half they look at would be the half nothing keeps true.

**It makes `plan` a function of the tracker alone.** Two invocations with nothing changed produce the same plan, in a fresh session, on a cleared scratch directory, after a machine restart — because there is nothing else for it to be a function of. Whatever a run later keeps of its own is therefore free to be an optimisation rather than a source of truth, and can be absent without changing an answer.

**It survives the session that produced it.** A run that is interrupted, or one the developer starts a second time in parallel, reads what the first one recorded, exactly as it reads a claim. The claim and the outcome are the same mechanism at two ends of a ticket's life, and neither needs anything shared between sessions.

So `record` writes one line on the ticket carrying a marked comment — machine-readable for the next run, prose for the developer — and `plan` and `report` read it back. A ticket with an outcome is settled and never offered again; what waits on a settled failure comes back stranded, which is the outcome a loop that only tracks what it can start drops without saying so.

**What this costs.** A tracker call, and a scope query that has to ask for the tickets a run closed as well as the ones still open — a done ticket having left the open scope by being closed. Both are paid once per verb, and buy an account that stays true when the session that produced it is gone.
