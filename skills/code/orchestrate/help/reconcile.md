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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current repository.

## SEE ALSO

**/orchestrate --help**
