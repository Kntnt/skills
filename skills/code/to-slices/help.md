# to-slices

## NAME

to-slices - publish one approved tracer-bullet set from a Frame Record

## SYNOPSIS

**/to-slices** [**--yes**] [*FRAME_RECORD*] [**--** *INSTRUCTION*]

## DESCRIPTION

`to-slices` turns one complete Frame Record into the durable decision layer: one non-executable decision issue and a graph of executable child tickets. It validates the framing handoff, synthesises narrow tracer bullets and their verification seams, asks whether the proposed granularity and blocking edges are approved, and publishes the approved set to GitHub.

The Skill accepts a framing commit that still equals `HEAD`. It also accepts a later `HEAD` whose intervening paths are all committed knowledge named by the record, after verifying that containment and updating the vantage point. Any other drift returns the record to `/frame` for resumed framing. Knowledge the record names must resolve from committed history before publication; the Skill never stages or commits it.

Publication is recoverable. Provenance identifies a partially published parent, the approved snapshot identifies its children, and re-invocation creates only missing issues and relations. The record is deleted only after the parent, every child, every label and milestone, parentage, and every blocking edge have been read back and verified.

The decision issue remains open through delivery and carries no executable ready label. Child tickets receive the repository's configured ready state, scope labels, milestone, native parentage, and native dependency edges where GitHub exposes them.

## POSITIONAL ARGUMENTS

*FRAME_RECORD*

The path to one complete Frame Record. Omitted, the only record under `.kntnt/frames/` is used. No record produces the `/frame` handoff; several records require an explicit selection.

## OPTIONS

**--yes**

Approve the first complete slice graph without asking the yes-or-no checkpoint. It does not choose among records, repair an incomplete record, or answer a missing owner decision.

## OUTPUT

One verified decision issue and its verified executable child issues on GitHub, followed by a concise report naming the published set and current unblocked frontier. The consumed Frame Record is removed only after verification succeeds.

## FILES

`.kntnt/frames/<slug>.md`

The untracked Frame Record read as input and retained as the recovery baton until publication verifies completely.

## DIAGNOSTICS

An invalid option, option order, or operand count is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, publishes nothing, and points to `/to-slices --help`. A flag with no work to do is refused rather than ignored.

A malformed, incomplete, or meaningfully stale Frame Record is preserved and returned through the exact `/frame --resume=<path>` handoff. A local-only knowledge entry stops before publication with the exact file to commit. Partial publication reports every issue and relation found, missing, or conflicting and preserves the record for recovery.

## EXAMPLES

`/to-slices .kntnt/frames/pdf-export.md` — preview one complete graph, ask for approval, and publish it.

`/to-slices --yes .kntnt/frames/pdf-export.md` — publish the first complete graph without asking the approval question.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator between the Formal Invocation and an optional Contextual Instruction.

The complete contract is stated once in the Collection Library at `library/references/invocation-envelope.md`: separator recognition, the boundaries on Contextual Instruction and Conversation Context, syntax and context refusals, and nested invocation handling.

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current GitHub repository.

**Skills**

The Manager must be Enabled so the dependency check and Collection Library are available.

## SEE ALSO

**/frame --help**, **/compile --help**
