# model-selector config edit

## NAME

model-selector config edit - revise one model selection or access channel

## SYNOPSIS

**/model-selector** **config** **edit** [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config edit` shows one identified record, collects changed fields, validates the complete profile, shows the result for confirmation, and saves one new revision.

A selection ID remains stable when editing its version, channel, modes, or policies. Replacing a model version never occurs implicitly during evidence refresh.

## POSITIONAL ARGUMENTS

**model**|**channel**

Select whether *ID* identifies a model selection or an access channel.

*ID*

The stable identifier of the record to edit.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown ID, missing argument, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config edit --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config add --help**, **/model-selector config remove --help**, **/model-selector config history --help**
