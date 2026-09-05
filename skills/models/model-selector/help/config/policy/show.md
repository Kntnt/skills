# model-selector config policy show

## NAME

model-selector config policy show - display the Standing Policy and what moved it

## SYNOPSIS

**/model-selector** **config** **policy** **show** [**--data=**_PATH_] [*COHORT*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config policy show` displays the effective Standing Policy: the Rung routing starts an unmeasured Cohort at, the inclusive floor and ceiling it stays between, the failure threshold that may move it, and the exploration budget. With no *COHORT* it shows the shipped default, every Cohort that has moved, and the whole movement history. With one it shows only that Cohort's effective policy and its own history. It also reports `store_damaged`: routing always has a complete policy because the shipped default is one, so a stored layer that will not parse never stops a run — but it does put every ratcheted Cohort back at its cold start, and this is what tells that apart from a Cohort that never moved.

Every movement in that history was appended by one of two things: the failure threshold, which the evidence import evaluates whenever it records judged attempts and which names the run keys that tripped it, or `config policy reset`, which names nobody. Nothing else writes the store, and nothing moves a Cohort down but a deliberate act of the user's: this command's `reset`, which restores the shipped default and keeps the history, or `config reset --evidence`, which discards the whole store and its history together rather than writing a row to either.

The shipped default prints its values symbolically — `cold_start`, `weakest_enabled`, `main_seat` — because each one resolves against the candidate ladder of the individual request, and each printed line says so. A moved Cohort prints the exact Rung stored for it.

The command reads local configuration only; it performs no network access, evaluation, or write. Bare `/model-selector config policy` has the same effect.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An absent store is reported as the shipped default rather than as an error. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config policy show --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config policy reset --help**, **/model-selector config show --help**, **/model-selector route --help**
