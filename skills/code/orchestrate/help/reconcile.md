# orchestrate reconcile

## NAME

orchestrate reconcile - record work completed outside Orchestrate

## SYNOPSIS

**/orchestrate reconcile** [**--commit=**_COMMIT_] [**--yes**] *TICKET* [**--** *INSTRUCTION*]

## DESCRIPTION

`reconcile` gives a closed ticket a done Ticket Resolution when its failed or conflicted unattended attempt was subsequently completed outside Orchestrate. It appends a distinct Reconciliation comment naming the completion commit, preserves the earlier Run Outcome unchanged, and does not close or reopen the ticket.

The ticket must already be closed and carry a failed or conflicted Run Outcome. The completion commit must be reachable from the repository's default branch. When exactly one default-branch commit carries an exact closing reference for the ticket, Orchestrate uses it. Otherwise an interactive invocation asks the maintainer to identify the commit and an unattended invocation refuses rather than guessing.

An identical repeated Reconciliation whose lifecycle projection is complete changes nothing and reports that the tracker already agrees. If an earlier attempt appended the event but was interrupted before cleanup, repeating it performs lifecycle repair without appending another event and reports recovery rather than agreement. An existing Reconciliation naming another commit is contradictory and is refused.

A successful Reconciliation removes `ready-for-agent`, removes every remaining assignment by its recorded login because completed lifecycle state has no active owner, then adds the neutral `orchestrated` label used to discover completed tickets for later reports.

## POSITIONAL ARGUMENTS

*TICKET*

Exactly one bare ticket reference, such as `#14`. Reconciliation never accepts a spec or a cross-repository reference.

## OPTIONS

**--commit=**_COMMIT_

Name the commit that completed the ticket. The commit may be any revision Git resolves to a commit, but the resolved commit must be reachable from the default branch.

**--yes**

Ask no question. If commit discovery does not establish exactly one candidate, refuse and leave tracker state unchanged.

## DIAGNOSTICS

An open ticket, a ticket without an unsuccessful Run Outcome, a commit outside the default branch, ambiguous commit discovery, and a contradictory repeat are refused before tracker state changes. A flag is refused rather than ignored where it has no work to do here. An operand written before an option is out of order and is refused the same way.

## EXAMPLES

**/orchestrate reconcile #14**

Reconcile ticket 14 using its unique default-branch closing commit, or ask for the commit when the evidence is not unique.

**/orchestrate reconcile --commit=71ec0de #14**

Reconcile ticket 14 to an explicitly named completion commit after verifying it is on the default branch.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current repository.

## SEE ALSO

**/orchestrate --help**
