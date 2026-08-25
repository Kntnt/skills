# model-selector config show

## NAME

model-selector config show - display the active model and access profile

## SYNOPSIS

**/model-selector** **config** **show** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config show` displays the active profile path and revision together with model selections, access channels, commercial units, modes, version-watch policy, and unresolved fields. Bare `/model-selector config` has the same effect.

The command reads local configuration and evidence only; it performs no network access, evaluation, or write.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent or invalid profile is reported. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config show --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config add --help**, **/model-selector config history --help**, **/model-selector status --help**
