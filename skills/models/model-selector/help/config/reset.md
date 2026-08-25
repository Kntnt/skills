# model-selector config reset

## NAME

model-selector config reset - remove the active profile while retaining evidence

## SYNOPSIS

**/model-selector** **config** **reset** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config reset` shows the exact active configuration path, requests confirmation, appends a tombstone to configuration history, and removes only the active `config.json`. Evidence and revision history are retained.

The next command that requires model selections starts guided setup.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

A declined confirmation, absent profile, or unsupported option changes nothing. Invalid syntax is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config reset --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector setup --help**, **/model-selector config history --help**, **/model-selector config remove --help**
