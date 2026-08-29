# model-selector config add

## NAME

model-selector config add - add a model selection or access channel

## SYNOPSIS

**/model-selector** **config** **add** [**--data=**_PATH_] (**model**|**channel**) [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config add` conducts a guided interview for one model selection or access channel, validates the complete revised profile, shows it for confirmation, and saves one new revision.

Adding a model attaches it to an existing or newly collected channel. Adding a channel may leave it unused only after explicit confirmation. Configuration commands consult local evidence and never trigger research or evaluations.

## POSITIONAL ARGUMENTS

**model**

Add one exact model selection with version identity, channel, modes, Harness, fallback policy, and watch policy.

**channel**

Add one access channel with provider, surface, billing type, tier, costs, quota rules, and provenance.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

A missing kind, unsupported kind, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config add --help`. An operand written before an option is out of order and is refused the same way.

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

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config edit --help**, **/model-selector config show --help**, **/model-selector update --help**
