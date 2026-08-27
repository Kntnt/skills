# Landed-change Interface

This Interface is the durable Git baton shared by `/dispatch`, `/compile`, and `/land`. `/dispatch` writes it; `/compile` and `/land` consume it. The commit travels with the implementation in repository history, so no consumer depends on tracker projection or clone-local run state to decide whether the change exists.

## Landing commit

One ticket lands as one dispatcher-authored landing commit whose parent is the integration tip against which the approved candidate was built. That commit contains the complete implementation patch, the exact compiler-owned tests from the accepted [compiled plan](compiled-plan.md), and every dispatcher-owned shared write for the ticket. Nothing belonging to that landing is split across another commit, and nothing belonging to another ticket is included.

The commit message carries exactly one of each of these Git trailers, with the ticket reference and bundle fingerprint copied from the accepted compiled plan:

```text
Kntnt-Ticket: #<ticket>
Kntnt-Plan: sha256:<bundle-fingerprint>
```

`#<ticket>` is the canonical issue reference in the current repository. `<bundle-fingerprint>` is the compiled-plan bundle's 64 lowercase hexadecimal SHA-256 value; `sha256:` is part of the trailer value. A commit with either trailer absent, repeated, malformed, or disagreeing with the accepted ticket and plan is not a landing commit for that ticket.

Executor scratch commits are temporary execution evidence. They do not land on the integration history and never become the durable baton; `/dispatch` applies the approved patch and owned writes to the current integration tip and authors the one landing commit itself.

## Selection from history

Every consumer evaluates one named integration tip. Its integration history is that commit and all of its ancestors; a commit on another branch, in another worktree, or merely present in the object database is outside the history being evaluated.

For a ticket, a matching landing commit is a commit in that history carrying exactly one `Kntnt-Ticket` trailer equal to the canonical ticket reference and exactly one valid `Kntnt-Plan` trailer. The ticket has a selected landed-change baton only when exactly one matching landing commit is reachable from the integration history being evaluated. No match means the ticket is not landed there. More than one match is ambiguous and must be refused rather than resolved by date, topology order, tracker state, or journal evidence.

The selected commit is the implementation vantage, and its `Kntnt-Plan` value is the plan fingerprint. `/land` obtains both from Git without consulting a dispatch journal. Selection is repeated against the tip whose state the consumer is deciding; a baton selected on one branch or earlier tip proves nothing about another.

## Pipeline meaning

A blocker is complete for execution only when its selected landing commit is reachable from the current integration tip. Issue closure alone never makes dependent code exist, and an open issue does not make a reachable selected commit disappear. `/dispatch` therefore schedules from declared blocker relations plus the selected Git baton, never from issue status as a substitute for reachability.

The child issue remains open after `/dispatch` advances the integration branch. This open-until-land lifecycle leaves `/land` responsible for verifying the selected implementation vantage, reconciling durable knowledge and tracker state, and performing knowledge and tracker closure before it closes the child. The custom trailers record “landed but not yet closed” without using an auto-closing commit message.

`/compile` applies the same selection as a defensive eligibility guard. A ticket with the selected reachable baton is not compiled again, even when executable-ready label drift makes the tracker projection look eligible. Tracker closure without a selected baton does not activate this guard, and zero or multiple reachable matches provide no baton the compiler may guess from.

## Journal boundary

The dispatch journal may record the landing commit for recovery and audit evidence, including the candidate identity, expected trailers, tree, and compiler-owned test blobs. That record is not a portable or durable substitute for the reachable baton: a journal is clone-local and may disappear independently, while the selected commit is present exactly where the landed code is present.

Recovery may use the journal to reconstruct or verify an interrupted landing, but the integration ref must advance to the candidate and the selection rule above must succeed before any consumer treats the ticket as landed. A journal event, tracker comment, label, assignment, or issue status cannot manufacture Git reachability.

## Worked histories

| History observed from the evaluated integration tip | Matching reachable commits | Result |
| --- | ---: | --- |
| No commit carries the ticket's valid trailer pair | 0 | No selected baton; the blocker is incomplete and the compilation guard is inactive |
| One commit carries the ticket's valid trailer pair | 1 | Select that commit and expose its commit identity and plan fingerprint |
| One valid matching commit exists only off the evaluated history | 0 | No selected baton for this tip |
| Two reachable commits carry valid matching trailer pairs for the ticket | 2 | Ambiguous history; refuse selection |
| The issue is closed or its labels drift in any of the histories above | Unchanged | Preserve the Git result; tracker state neither creates nor removes a baton |
