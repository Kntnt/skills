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

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation status --help`. A flag is refused rather than ignored where it has no work to do here: `status` writes nothing and so asks nothing, which is why `--yes` has no work to do on this path and is refused, and both scope flags at once are invalid. So is any token after the command path that is not a scope flag.

## EXAMPLES

**/delegation status**

Report all three scopes, the effective verdict, and whether a standing block still matches the mode text the Skill would write today.

**/delegation status --project**

Report the Project scope alone.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/delegation status --help`. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation --help**, **/delegation on --help**, **/delegation off --help**
