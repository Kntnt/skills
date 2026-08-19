# The closed half of a scope is bounded by the branch the run is on

Done is the one outcome that takes a ticket out of the open scope, so the report asks the tracker twice: once for the open tickets the label holds, and once for the ones this machine's runs closed. The second question has no natural end. Every ticket a run has ever finished stays closed, stays labelled, and stays assigned, so the answer grows for the life of the project — and a query that comes back a full page is refused rather than trusted, because a scope silently missing tickets is a report nobody can check. Left alone, the report stops working one night, at the end of a run, on a repository that has done nothing wrong.

**So the closed question is bounded by the branch the run is on: only tickets closed since this branch left the default one.** The fork point is an ancestor of everything the run has built, so it is earlier than any outcome the run recorded; nothing this run did can fall outside it, and everything the project finished before the branch existed does.

**A day is the unit, not an instant.** The bound is the fork commit's date, and a whole day of slack in the safe direction costs a handful of tickets nobody was going to read while saving the question of whose clock and which timezone settles a boundary.

**Where there is nothing to bound by, the question is asked whole.** A repository that cannot say which branch is its default, one whose branch in hand is that default, and a branch with no common ancestor to find all leave the query as it was — and the guard that refuses a full page is still there, saying what it always said.

**What this costs.** A branch open since long before the tickets on it were finished narrows to nothing, and a run of more than two hundred tickets on one branch is refused rather than half-reported. Both are the guard doing its job, and both are visible rather than silent.
