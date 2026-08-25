# model-selector record

## NAME

model-selector record - append validated local evaluation observations

## SYNOPSIS

**/model-selector** **record** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

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

An unreadable path, invalid observation, unsupported option, or conflicting run identity is refused rather than ignored. The Skill prints this SYNOPSIS, appends nothing, and points to `/model-selector record --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector observe --help**, **/model-selector recommend --help**, **/model-selector status --help**
