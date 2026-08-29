# delegation status

## NAME

delegation status - report the mode's state in one scope or in all three

## SYNOPSIS

**/delegation status** [**--project**|**--user**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation status` reports the state of the selected scope, the effective verdict, and any staleness. With no scope flag it reports all three scopes, which is what makes a disagreement between a standing block and a session instruction visible in one line. It writes nothing, in any scope, and asks nothing, because it changes nothing.

A persistent block is stale when its text differs from the mode text the Skill would write today. The report names that condition rather than silently treating the block as current, and names `/delegation on --project` or `/delegation on --user` as the fix, `on` over an existing block being a rewrite from the current text.

## OPTIONS

**--project**

Report the Project scope alone instead of all three.

**--user**

Report the user scope alone instead of all three.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation status --help`. A flag is refused rather than ignored where it has no work to do here.

`--yes`, both scope flags together, and any unrecognized token are invalid.

## EXAMPLES

**/delegation status**

Report all three scopes, the effective verdict, and whether a standing block still matches the mode text the Skill would write today.

**/delegation status --project**

Report the Project scope alone.

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

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation --help**, **/delegation on --help**, **/delegation off --help**
