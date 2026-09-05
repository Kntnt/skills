# model-selector config policy reset

## NAME

model-selector config policy reset - restore the shipped Standing Policy for a Cohort

## SYNOPSIS

**/model-selector** **config** **policy** **reset** [**--data=**_PATH_] [*COHORT*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config policy reset` removes a Cohort's stored override and appends one history row saying the user restored it. With *COHORT* it restores that Cohort. With no operand it restores every overridden Cohort, appending one row per Cohort removed. Resetting a Cohort nothing ever moved changes nothing and records nothing.

This is the narrower of the Standing Policy's two downward moves. A Cohort ratchets up only from its failure threshold, and only a deliberate act of the user's brings it back down: this command, which restores the shipped default for one Cohort and keeps the history, or `config reset --evidence`, which discards the measurement the movement rests on and the history with it. The Skill shows the exact store path and the Cohorts about to be restored, and asks for confirmation before writing.

Evidence, derived frontiers, and the model and access profile are untouched. The restored default reaches the next frozen routing context, never a run already under way.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

A declined confirmation changes nothing. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config policy reset --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config policy show --help**, **/model-selector config reset --help**, **/model-selector route --help**
