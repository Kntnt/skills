# brief status

## NAME

brief status - report the mode's state in both scopes

## SYNOPSIS

**/brief status** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief status` reports the session state, the user state, the verdict those two produce, and any staleness. It writes nothing, in either scope, and reframes nothing.

A user-scope block is stale when its text differs from the perspective the Skill would write today. The report names that condition rather than silently treating the block as current, and names `/brief on --user` as the fix, `on` over an existing block being a rewrite from the current text.

The command takes no option. It targets no scope because it reports both, and it asks no question because it changes nothing.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief status --help`. Every flag the Skill declares belongs to a form that writes, so any flag on this path has no work to do here and is refused; so is any token after the command path.

## EXAMPLES

**/brief status**

Report both scopes, the resulting verdict, and whether the user-level block still matches the perspective the Skill would write today.

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

**/brief --help**, **/brief on --help**, **/brief off --help**
