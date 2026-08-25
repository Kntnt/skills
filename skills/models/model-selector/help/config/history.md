# model-selector config history

## NAME

model-selector config history - display profile revision history

## SYNOPSIS

**/model-selector** **config** **history** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config history` displays stored profile revision timestamps and summaries from local history. It performs no network access or writes.

Evidence history is separate and remains append-only across configuration revisions.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unreadable history is reported. An unsupported option is refused rather than ignored; invalid syntax prints this SYNOPSIS and points to `/model-selector config history --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config show --help**, **/model-selector config reset --help**, **/model-selector status --help**
