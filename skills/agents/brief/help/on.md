# brief on

## NAME

brief on - enable Brief mode for the selected scope

## SYNOPSIS

**/brief on** [**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`brief on` adopts the Brief perspective as a standing instruction for subsequent replies. It does not revisit, reframe, or summarise the preceding answer; that is what a bare `/brief` is for.

The mode takes effect on the turn that switches it on, so the report of the write already obeys it. An explicit request for more detail overrides the default level for that reply, and the perspective governs conversation replies rather than code, documentation, comments, commit messages, or other artifacts.

Without `--user` the scope is this session alone, and context compaction may drop it.

With `--user` the Skill shows the target and managed block before writing to this Harness's global context file. Repeating `on` refreshes an existing or stale block.

## OPTIONS

**--user**

Target this Harness's user context instead of the current session. There is no Project scope: conversational perspective and density are reader preferences rather than a shared Project convention.

**--yes**

Write the user block without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by the user scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief on --help`. A flag is refused rather than ignored where it has no work to do here, and any token after the command path that is neither `--user` nor `--yes` is refused the same way.

Two managed blocks in one file, or a marker without its pair, stop the write: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/brief on**

Keep later replies in this conversation concise and decision-relevant, leaving the preceding answer untouched.

**/brief on --user --yes**

Write the managed block into this Harness's global context file without asking for confirmation first.

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
