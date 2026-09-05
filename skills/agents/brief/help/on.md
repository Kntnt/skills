# brief on

## NAME

brief on - adopt the Brief perspective for this conversation

## SYNOPSIS

**/brief on** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief on` adopts the Brief perspective as a standing instruction for the rest of this conversation. It does not revisit, reframe, or summarise the preceding answer; `/tldr` is what re-explains an answer that did not land.

The mode takes effect on the turn that switches it on, so the report of the change already obeys it. An explicit request for more detail overrides the default level for that reply, and the perspective governs conversation replies rather than code, documentation, comments, commit messages, or other artifacts.

It reaches this conversation and nothing else. Another window on the same project, another project, and every later session are unaffected, and the state ends when this conversation does.

Nothing is written. There is no settings key, no style file, and no state on disk, in any Harness: the mode lives in this conversation and ends with it, leaving nothing behind.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief on --help`. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

## EXAMPLES

**/brief on**

Keep later replies in this conversation concise and decision-relevant, leaving the preceding answer untouched.

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

**/brief --help**, **/brief off --help**, **/brief status --help**
