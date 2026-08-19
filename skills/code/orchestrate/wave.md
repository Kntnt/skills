# The wave brief

Give this to a subagent once a wave's verified tickets have been merged into the run branch, in the repository the developer started the run in. It is filled in from the wave: `<tickets>` is the list of the tickets that were merged, each as `#number — title`. It is not given any ticket's acceptance criteria and is not asked to judge one — those were settled ticket by ticket before anything was merged, and this is the one question that could not be asked then.

---

You are checking a branch, not a ticket. Several tickets were built separately, each verified on its own, and their work has just been merged together onto this branch. Two of them can pass alone and fail together, and that is the only thing you are here to find out.

**What was merged.** `<tickets>`

**Run the project's full verification, on this branch, as it now stands.** Every command its contributing guide names for a change — all of them, not a subset, and not only the ones that look related to what was merged. If there is no such guide, run the whole test suite and whatever lint, format, and type checks the project is configured for.

**Change nothing.** Do not fix a failure, do not commit, and do not revert. What you are doing is reading the branch, and a repair made here is a repair nobody verified.

**Report a verdict, and nothing softer.** A pass means every command passed. Anything else is a fail, naming the command that failed and quoting enough of its output to see why — and, where you can tell, which of the merged tickets it points at. The run stops on a fail rather than spending the remaining hours building on broken code, so a verdict you are not sure of is a fail.
