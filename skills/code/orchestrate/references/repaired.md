# The repaired-collision brief

Give this to a second subagent once a repair subagent says it settled a collision, in the same working tree and filled in the same way as `repair.md`: `<worktree>` is where the repair was made, `<scratch>` is the same scratch directory that repair was given, and the ticket blocks are the losing ticket and every ticket in the collision's `collided_with`, each with its number, title, url, and whole body. It has not seen the repair session and is never told what it reported. Its verdict is what decides whether the repair stands or the ticket is built again from nothing.

---

You are verifying a repair that somebody else made. Two tickets were built separately, they touched the same code, and one session has just merged them together and settled the conflicts. You did not make that resolution, you have not seen the session that did, and nothing it claims reaches you.

A resolution is not judged on whether it looks reasonable. It is judged on whether both tickets are still satisfied by the code in front of you — a resolution that keeps one ticket's acceptance criteria by quietly dropping the other's is exactly the failure you are here to catch, and it is the one that reads best in a diff.

**Where you look.** In `<worktree>`, which now holds both tickets' work merged together. Run everything there. The branch the developer started the run on does not carry this repair, and it is this verdict that decides whether it ever does.

**Where you write.** Everything you write goes in one of two places: the working tree you were given, and `<scratch>`, a scratch directory of your own. Nothing outside those two is yours to write in or to delete from — other work is going on beside yours at this moment, and a path two sessions both chose is a log one of them reads as the other's, or a file one of them clears away from under the other.

**The ticket that was repaired.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**The ticket it collided with.** `<others>`

Do all of this, in this order:

1. **Run the project's full verification yourself.** Every command its contributing guide names for a change — all of them, not a subset, and not only the ones that look related to the conflict. If there is no such guide, run the whole test suite and whatever lint, format, and type checks the project is configured for.
2. **Check every acceptance criterion of both tickets, one at a time**, against the repository as it is now. Say for each one whether it is met and what you looked at to decide. A criterion about behaviour is checked by exercising the behaviour, not by reading the diff and finding code that looks like it would do that.
3. **Check what the repair did beyond repairing.** Work neither ticket asked for, a test weakened or deleted to make the merge pass, one side of a conflict dropped rather than settled.

**A long command is waited on, not yielded to.** Where something you run takes long — a full test suite, an integration suite that runs for a quarter of an hour, a build — start it in the background and wait on its completion with whatever waiting facility this harness gives you. Never end your turn while it runs. Waiting is part of the work rather than idleness to yield in: a turn ended with the gate still running is a build that did not finish or a verdict that was not reached, and in a run nobody is watching, nothing comes back to wake the session that ended it.

**Report a verdict, and nothing softer.** A pass means every command passed and every acceptance criterion of both tickets is met. Anything else is a fail, naming the command that failed or the criterion that is not met. There is no partial pass and no pass with reservations. A fail is not expensive here: the run answers it by building the repaired ticket again from nothing on top of the other one's work, which is code somebody meant rather than a stitched-together guess. So a verdict you are not sure of is a fail.
