# model-selector config policy

## NAME

model-selector config policy - inspect or restore the Standing Policy routing starts from

## SYNOPSIS

**/model-selector** **config** **policy** [**show**|**reset**] [**--data=**_PATH_] [*COHORT*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config policy` reads and restores the Standing Policy, which is where one workload Cohort starts on the Rung ladder and how far up and down that ladder routing may go. It ships working: nothing has to be set for routing to have a policy, and there is no `set`. A Cohort's policy moves only when measured failures trip its threshold, and it moves only upward; what brings it back down is a deliberate act of the user's — this command's `reset`, which restores the shipped default and keeps the history, or `config reset --evidence`, which discards the measurement the movement rests on and the history with it.

The policy lives beside `config.json` in the selected data directory, as `standing-policy.json` with an append-only `standing-policy-history.jsonl` next to it. Only Cohorts something moved are stored there; every other Cohort has the shipped default. The store is script-owned and is never hand-edited, so the profile's own `config.lock` protocol does not apply to it.

A policy change is frozen into the next routing context and covered by its snapshot identity, so it reaches the next run rather than one already under way.

## COMMANDS

**show** [*COHORT*]

Display the effective policy, its bounds, and the movements behind it. This is the default when no policy subcommand is supplied.

**reset** [*COHORT*]

Restore the shipped default for one Cohort, or for every overridden Cohort, after confirmation.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An unknown policy subcommand, a second Cohort operand, or an operand written after an option is refused rather than ignored. The Skill prints the addressed page's SYNOPSIS, changes nothing, and points to the corresponding `--help` invocation.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config policy show --help**, **/model-selector config policy reset --help**, **/model-selector config show --help**
