# model-selector record

## NAME

model-selector record - append validated local evaluation observations

## SYNOPSIS

**/model-selector** **record** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector record` validates local evaluation observations at *PATH* and appends unseen records to the evidence ledger. Conflicting historical observations are preserved instead of overwritten. Only the derived frontiers whose eligible run set changed are rebuilt, each named by its benchmark key, stage, workload cohort and workload tags; an observation naming no cohort is kept in the ledger and belongs to no frontier.

The command records the exact model configuration, workload, metrics, units, provenance, and run identity needed for later comparisons. An artifact reported by `/model-selector observe` is accepted here unchanged. This public command remains a user invocation; Orchestrate's verdict path imports eligible machine-judged attempts automatically, while delegation remains emission-only.

## POSITIONAL ARGUMENTS

*PATH*

The local file containing evaluation observations to validate and append.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An unreadable path, invalid observation, unsupported option, or conflicting run identity is refused rather than ignored. The Skill prints this SYNOPSIS, appends nothing, and points to `/model-selector record --help`. An operand written before an option is out of order and is refused the same way.

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

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector observe --help**, **/model-selector recommend --help**, **/model-selector status --help**
