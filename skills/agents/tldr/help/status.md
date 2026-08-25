# tldr status

## NAME

tldr status - report the mode's state in both scopes

## SYNOPSIS

**/tldr status** [**--** *INSTRUCTION*]

## DESCRIPTION

`tldr status` reports the session state, the user state, the verdict those two produce, and any staleness. It writes nothing, in either scope, and reframes nothing.

A user-scope block is stale when its text differs from the perspective the Skill would write today. The report names that condition rather than silently treating the block as current, and names `/tldr on --user` as the fix, `on` over an existing block being a rewrite from the current text.

The command takes no option. It targets no scope because it reports both, and it asks no question because it changes nothing.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/tldr status --help`. Every flag the Skill declares belongs to a form that writes, so any flag on this path has no work to do here and is refused; so is any token after the command path.

## EXAMPLES

**/tldr status**

Report both scopes, the resulting verdict, and whether the user-level block still matches the perspective the Skill would write today.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/tldr status --help`. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

None.

## SEE ALSO

**/tldr --help**, **/tldr on --help**, **/tldr off --help**
