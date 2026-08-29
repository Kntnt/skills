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

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An absent workload or unsupported option is refused rather than ignored. An incomparable cohort is reported rather than silently combined. Invalid syntax prints this SYNOPSIS and points to `/model-selector chart --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## DEPENDENCIES

`uv` runs the Skill's dependency check. The command reads bundled or locally stored evidence.

## SEE ALSO

**/model-selector compare --help**, **/model-selector recommend --help**
