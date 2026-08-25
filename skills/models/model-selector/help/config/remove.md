# model-selector config remove

## NAME

model-selector config remove - remove one model selection or access channel

## SYNOPSIS

**/model-selector** **config** **remove** [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config remove` shows the exact target and consequences, then removes it from the active profile after confirmation and saves one new revision. Evidence and configuration history are retained.

A channel still referenced by a model selection must be reassigned or have its dependent selections removed in the same revision.

## POSITIONAL ARGUMENTS

**model**|**channel**

Select whether *ID* identifies a model selection or an access channel.

*ID*

The stable identifier of the record to remove.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown ID, referenced channel without a resolution, declined confirmation, or unsupported option writes nothing. Invalid syntax is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config remove --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config edit --help**, **/model-selector config history --help**, **/model-selector config reset --help**
