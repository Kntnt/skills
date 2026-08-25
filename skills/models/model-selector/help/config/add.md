# model-selector config add

## NAME

model-selector config add - add a model selection or access channel

## SYNOPSIS

**/model-selector** **config** **add** [**--data=**_PATH_] (**model**|**channel**) [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config add` conducts a guided interview for one model selection or access channel, validates the complete revised profile, shows it for confirmation, and saves one new revision.

Adding a model attaches it to an existing or newly collected channel. Adding a channel may leave it unused only after explicit confirmation. Configuration commands consult local evidence and never trigger research or evaluations.

## POSITIONAL ARGUMENTS

**model**

Add one exact model selection with version identity, channel, modes, Harness, fallback policy, and watch policy.

**channel**

Add one access channel with provider, surface, billing type, tier, costs, quota rules, and provenance.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

A missing kind, unsupported kind, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config add --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config edit --help**, **/model-selector config show --help**, **/model-selector update --help**
