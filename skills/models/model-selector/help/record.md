# model-selector record

## NAME

model-selector record - append validated local evaluation observations

## SYNOPSIS

**/model-selector** **record** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector record` validates local evaluation observations at *PATH* and appends unseen records to the evidence ledger. Conflicting historical observations are preserved instead of overwritten. Only the derived frontiers whose eligible run set changed are rebuilt, each named by its benchmark key, stage, workload cohort and workload tags; an observation naming no cohort is kept in the ledger and belongs to no frontier.

The same call evaluates the Standing Policy failure threshold of every cohort the import touched. A cohort whose last judged attempts at its own starting Rung hold enough externally verified failures moves one Rung up and is reported with the count behind it and the `config policy reset` that undoes it. Nothing ever moves down on its own, evidence frozen under a superseded policy revision moves nothing at all, and a movement reaches routing only at the next frozen context.

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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector observe --help**, **/model-selector config policy show --help**, **/model-selector recommend --help**, **/model-selector status --help**
