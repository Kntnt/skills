# model-selector status

## NAME

model-selector status - report profile and evidence readiness

## SYNOPSIS

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector status` reports the active profile, evidence vintage, due sources, coverage gaps, provisional facts, low-confidence capability priors, and configuration selections without network access or writes.

The report distinguishes evidence that is absent, stale by configured cadence, provisional, or inapplicable rather than collapsing those states into one readiness value.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent or invalid profile is reported. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector status --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector update --help**, **/model-selector config --help**, **/model-selector recommend --help**
