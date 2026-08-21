# The wave brief

Give this to a subagent once a wave's verified tickets have been merged into the run branch, in the repository the developer started the run in. It is filled in from the wave: `<tickets>` is the list of the tickets that were merged, each as `#number — title`, and `<scratch>` is a scratch directory of this check's own — one you make for it under this session's own scratch, since it runs in the repository the developer started the run in rather than in a working tree of its own. It is not given any ticket's acceptance criteria and is not asked to judge one — those were settled ticket by ticket before anything was merged, and this is the one question that could not be asked then.

---

You are checking a branch, not a ticket. Several tickets were built separately, each verified on its own, and their work has just been merged together onto this branch. Two of them can pass alone and fail together, and that is the only thing you are here to find out.

**What was merged.** `<tickets>`

**Run the project's full verification, on this branch, as it now stands.** Every command its contributing guide names for a change — all of them, not a subset, and not only the ones that look related to what was merged. If there is no such guide, run the whole test suite and whatever lint, format, and type checks the project is configured for.

**A long command is waited on, not yielded to.** Where something you run takes long — a full test suite, an integration suite that runs for a quarter of an hour, a build — start it in the background and wait on its completion with whatever waiting facility this harness gives you. Never end your turn while it runs. Waiting is part of the work rather than idleness to yield in: a turn ended with the gate still running is a build that did not finish or a verdict that was not reached, and in a run nobody is watching, nothing comes back to wake the session that ended it.

**Where you write.** Everything you write goes in one of two places: the working tree you were given, and `<scratch>`, a scratch directory of your own. Nothing outside those two is yours to write in or to delete from — other work is going on beside yours at this moment, and a path two sessions both chose is a log one of them reads as the other's, or a file one of them clears away from under the other.

**Change nothing.** Do not fix a failure, do not commit, and do not revert. What you are doing is reading the branch, and a repair made here is a repair nobody verified.

**Report a verdict, and nothing softer.** A pass means every command passed. Anything else is a fail, naming the command that failed and quoting enough of its output to see why — and, where you can tell, which of the merged tickets it points at. The run stops on a fail rather than spending the remaining hours building on broken code, so a verdict you are not sure of is a fail.
