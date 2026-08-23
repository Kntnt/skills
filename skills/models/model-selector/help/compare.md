# model-selector compare

## NAME

model-selector compare - report comparable model-system frontiers

## SYNOPSIS

**/model-selector** **compare** *WORKLOAD* [**--decision=route**|**--decision=renew**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector compare` is an alias of `model-selector chart`. It builds comparable Pareto frontiers without selecting one winner, then emits compact tables and plotting-ready CSV.

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

An absent workload or unsupported option is refused rather than ignored. An incomparable cohort is reported rather than silently combined. Invalid syntax prints this SYNOPSIS and points to `/model-selector compare --help`.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

None. The command reads bundled or locally stored evidence.

## SEE ALSO

**/model-selector chart --help**, **/model-selector recommend --help**
