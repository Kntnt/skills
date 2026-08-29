# model-selector config remove

## NAME

model-selector config remove - remove one model selection or access channel

## SYNOPSIS

**/model-selector** **config** **remove** [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config remove` shows the exact target and consequences, then removes it from the active profile after confirmation and saves one new revision. Evidence and configuration history are retained.

A channel still referenced by a model selection must be reassigned or have its dependent selections removed in the same revision.

## POSITIONAL ARGUMENTS

**model**|**channel**

Select whether *ID* identifies a model selection or an access channel.

*ID*

The stable identifier of the record to remove.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An unknown ID, referenced channel without a resolution, declined confirmation, or unsupported option writes nothing. Invalid syntax is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config remove --help`. An operand written before an option is out of order and is refused the same way.

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

**/model-selector config edit --help**, **/model-selector config history --help**, **/model-selector config reset --help**
