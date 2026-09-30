# On the default branch the report is bounded by the day the run started

This record settles how `/orchestrate report` bounds its question about closed tickets on the default branch. [ADR-0058](0058-the-closed-half-of-a-scope-is-bounded-by-the-branch.md) bounded that question by the day the branch left the default one, and asked it whole where there is nothing to fork from. That exception stopped working, and every run on `main` ended without its report (issue #447). What the Skill now says about its state is in `skills/code/orchestrate/SKILL.md` and `help.md`. This record gives the reasons.

## Why the exception no longer holds

**ADR-0058 accepted asking the whole question on the default branch because that was rare.** A run was then expected on a branch of its own. [ADR-0064](0064-a-run-works-the-branch-it-was-left-on.md) since let a run work the branch it was left on, whichever that is, and this collection's runs are made on `main`. So the exception became the ordinary case.

**The whole question is now bigger than one page.** The report asks the tracker for every closed ticket that carries `ready-for-agent`, and for every closed ticket that carries the historical label `orchestrated`. On 2026-09-29 the second label was on 204 closed tickets. The tracker returns at most 200 on one page, and the report refuses a full page rather than trust it. The run of #439 and #440 on `main` ended with that refusal, and so would every run on `main` after it.

## The new bound

**The run remembers the day it started, and on the default branch the report reads only tickets closed on or after that day.** Where the fork point gives a bound, it stays exactly as ADR-0058 set it, and the start day plays no part. Where it gives none, and the run's state records a start day, both closed questions carry `closed:>=<start day>`. Where neither exists, the question is asked whole, and a full page is refused with the same message as before.

**The day is the UTC date at the moment the plan writes the state.** The tracker reads a bare date in `closed:>=` as a UTC day: on GitHub, `closed:>=2026-09-24 closed:<=2026-09-24` leaves out #387, which was closed at 23:12Z on 2026-09-23. East of UTC, the local date can be a day later than the UTC date. A run planned just after local midnight would then bound away the tickets it closed itself. The fork-point day keeps its own clock, the committer's date of the fork commit, because nothing about it changed.

**The day is written once, and only where the run starts.** A plan records it only where the run's subdirectory of the state directory holds no run file. A run file is every file the engine keeps there except the dashboard and the dot files `write_atomically` leaves while it replaces a file. The dashboard does not count because it is written with no run behind it, and it is never an input to an engine decision. Every later write carries the stored day forward unchanged. A state the plan does not take up is replaced by one with no day. That covers a state file that cannot be read, a state that belongs to another run, and any other run file that survived without its state. A state written by an earlier release records no day and never gets one. In each of those cases a day written now could be later than tickets the run already closed, and the report would leave them out without a word. With no day, the report asks the whole question, and a full page is refused where anyone can see it.

**So nothing this run recorded falls outside the bound.** The day is written before the run can claim anything, so every ticket it closes is closed on that day or later. The one exception is under *What this costs*.

## The ordinary account was widened

**[ADR-0051](0051-the-tracker-remembers-what-a-run-recorded.md) and [ADR-0052](0052-the-invocation-is-the-resume.md) defined the run's ordinary account as something the tracker and the branch can say again.** The start day belongs to that account, but neither of them can say it: nothing on the tracker or in Git records when a run on the default branch began. The definition is therefore widened, not left false. The tracker and the branch say all of the account again except the day the run started. The account is still remembered rather than relied on. No build, claim or outcome depends on the day. Losing the state file costs the report its bound on the default branch, which ends in the full-page refusal once history outgrows a page, and costs nothing else. No fifth class of state was added. A class of its own would have claimed more for the day than it carries.

## What this costs

**A ticket finished before the run existed falls outside the bound.** That is the trade ADR-0058 made for the fork point, and it is made here for the same reason. A report accounts for this run, and a ticket another run finished is not this run's to account for.

**A lost or unwritten day leaves the question whole.** A harness with no state directory, a state file that is gone or damaged, and a state written by an earlier release all leave the default-branch question unbounded. Once the history outgrows a page, the report refuses. That is visible, and it is what the report did before this change.

**One loss is silent.** Suppose every run file is lost partway through a run, and the Skill continues the run on a later UTC day. The next plan finds a subdirectory with no run file, which no rule can tell apart from a new run's, and records that later day. The tickets the run closed before that day then fall outside the bound, and the report leaves them out with nothing refusing. A run that keeps only its dashboard is the same case. This is accepted as a stated cost rather than designed away, because telling that directory from a new run's would need a record the run no longer has.

## The alternatives

**Paging through the whole closed history.** It would read every ticket the project ever finished, on every report, and the cost grows for the life of the project. ADR-0058 rejected this for the same reason, and the reason still holds.

**Bounding by the oldest claim or outcome the run can find.** A run's claims and outcomes are on the tickets, but finding them means asking the unbounded question first. It is the question this record exists to avoid.

**Writing today's date wherever a day is missing.** That would give a bound to every state, including one written by an earlier release. It would also drop, with no error, the tickets that run had already closed on earlier days. A refusal that shows is better than a report that is short without saying so.
