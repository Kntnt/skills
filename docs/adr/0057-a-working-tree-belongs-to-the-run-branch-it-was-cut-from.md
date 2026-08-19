# A working tree belongs to the run branch it was cut from

A ticket's working tree lives at `.git/kntnt-orchestrate/<number>` and is checked out on `kntnt-orchestrate/<run branch>/<number>`. The branch says which run made it. The path says only which ticket it holds.

That difference had a consequence. A run reads git's account of its working trees to find the one an interrupted run left and the one a failed ticket kept — the same question asked the same way (ADR-0054) — and it matched on the path alone. So a tree left by a run on one branch was picked up, built in, and merged by a run on another: work cut from one branch arrived on a branch that never asked for it, under a ticket number the two runs happened to share. Nothing had to go wrong for it to happen — a claim an interrupted run left standing is offered again by the next run, and the next run is often on a fresh branch.

**So a working tree is this run's only where the branch checked out in it is the branch this run would have cut for that ticket.** Anything else standing at that path belongs to another run and is named rather than adopted or built over, in the same terms as the abandoned branch this verb already refuses over: look at what is in it, then remove it.

**The path stays where ADR-0054 put it.** Naming the run branch in the path would make a tree's identity readable without asking, but it would also make the path a function of a branch name, which is a thing developers rename — and the reason that ADR gives for the location, the developer's own working tree exactly as they left it, is served either way. The branch was already the identity. This is the code catching up with it.

**What this costs.** A tree an earlier run left on another branch has to be removed by hand before that ticket can be worked again. That is one gesture, over work somebody may still want to look at, and the alternative was building on top of it without saying so.
