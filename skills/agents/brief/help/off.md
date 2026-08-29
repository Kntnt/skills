# brief off

## NAME

brief off - disable Brief mode for the selected scope

## SYNOPSIS

**/brief off** [**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`brief off` treats the standing Brief instruction as inert history for subsequent replies. It changes nothing about the preceding answer and reframes nothing.

It takes effect on the turn that switches it off, so the report of the removal is already written without the perspective. Without `--user` it suspends the mode for this session alone. With `--user` it removes the managed block from this Harness's global context file, both markers included and nothing else, after showing the exact target and the exact removal.

`off` is an exact undo of `on`, which is why no backup file is written, in git or out. Where there is no block to remove, the Skill says so and stops: nothing to remove is not an error.

## OPTIONS

**--user**

Target this Harness's user context instead of the current session. There is no Project scope: conversational perspective and density are reader preferences rather than a shared Project convention.

**--yes**

Remove the user block without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by the user scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief off --help`. A flag is refused rather than ignored where it has no work to do here, and any token after the command path that is neither `--user` nor `--yes` is refused the same way.

Two managed blocks in one file, or a marker without its pair, stop the removal: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/brief off**

Stop applying the Brief perspective to later replies in this conversation, leaving any user-level block alone.

**/brief off --user**

Show the managed block in this Harness's global context file and, once confirmed, remove it together with both markers.

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
