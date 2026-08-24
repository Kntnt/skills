# model-selector record

## NAME

model-selector record - append validated local evaluation observations

## SYNOPSIS

**/model-selector** **record** *PATH* [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector record` validates local evaluation observations at *PATH* and appends unseen records to the evidence ledger. Conflicting historical observations are preserved instead of overwritten. Only the derived frontiers whose eligible run set changed are rebuilt.

The command records the exact model configuration, workload, metrics, units, provenance, and run identity needed for later comparisons. An artifact reported by `/model-selector observe` is accepted here unchanged, and this explicit invocation is the only thing that imports one: routed work never imports its own evidence.

## POSITIONAL ARGUMENTS

*PATH*

The local file containing evaluation observations to validate and append.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unreadable path, invalid observation, unsupported option, or conflicting run identity is refused rather than ignored. The Skill prints this SYNOPSIS, appends nothing, and points to `/model-selector record --help`.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector observe --help**, **/model-selector recommend --help**, **/model-selector status --help**
