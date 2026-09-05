# brief off

## NAME

brief off - drop the Brief perspective for this conversation

## SYNOPSIS

**/brief off** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief off` treats the standing Brief instruction as inert history for the rest of this conversation. It changes nothing about the preceding answer and reframes nothing.

It takes effect on the turn that switches it off, so the report of the change is already written without the perspective. It reaches this conversation and nothing else, exactly as `on` does.

Nothing is removed, because nothing was written. `off` where the mode was never on is not an error: the Skill says so and stops.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief off --help`. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

## EXAMPLES

**/brief off**

Stop applying the Brief perspective to later replies in this conversation.

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

None.

## SEE ALSO

**/brief --help**, **/brief on --help**, **/brief status --help**
