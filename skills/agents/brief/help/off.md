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

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/brief off --help`. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

None.

## SEE ALSO

**/brief --help**, **/brief on --help**, **/brief status --help**
