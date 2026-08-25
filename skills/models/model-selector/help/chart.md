# model-selector chart

## NAME

model-selector chart - report comparable model-system frontiers without choosing a winner

## SYNOPSIS

**/model-selector** **chart** [**--decision=route**|**--decision=renew**] [**--data=**_PATH_] *WORKLOAD* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector chart` follows recommendation analysis through frontier construction without selecting one winner. It emits a compact table and plotting-ready CSV for each comparable cohort.

Cash, quota, and renewal views remain separate unless the profile supplies an explicit shadow price that makes a shared numeric axis valid. Unavailable metrics are `null`, never zero.

## POSITIONAL ARGUMENTS

*WORKLOAD*

The task or workload whose configured systems are compared.

## OPTIONS

**--decision=route**, **--decision=renew**

Compare marginal routing economics now or fixed-fee renewal economics. `route` is the default.

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent workload or unsupported option is refused rather than ignored. An incomparable cohort is reported rather than silently combined. Invalid syntax prints this SYNOPSIS and points to `/model-selector chart --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check. The command reads bundled or locally stored evidence.

## SEE ALSO

**/model-selector compare --help**, **/model-selector recommend --help**
