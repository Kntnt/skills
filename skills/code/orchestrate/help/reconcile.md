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

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/orchestrate reconcile --help`. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current repository.

## SEE ALSO

**/orchestrate --help**
