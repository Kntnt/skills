# model-selector setup

## NAME

model-selector setup - create or fully review the model and access profile

## SYNOPSIS

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector setup` conducts a guided review of the exact model versions and access channels available to the user. It collects model identity, effort or thinking policy, serving modes, Harness, channel, commercial terms, quota rules, and version-watch policy without storing credentials.

The complete profile is shown before it is written. Reopening setup for an existing profile creates a validated revision and retains evidence history.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An incomplete or invalid profile is not written. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector setup --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config --help**, **/model-selector update --help**
