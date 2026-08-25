# brief on

## NAME

brief on - enable Brief mode for the selected scope

## SYNOPSIS

**/brief on** [**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`brief on` adopts the Brief perspective as a standing instruction for subsequent replies. It does not revisit, reframe, or summarise the preceding answer; that is what a bare `/brief` is for.

The mode takes effect on the turn that switches it on, so the report of the write already obeys it. An explicit request for more detail overrides the default level for that reply, and the perspective governs conversation replies rather than code, documentation, comments, commit messages, or other artifacts.

Without `--user` the scope is this session alone, and context compaction may drop it. With `--user` the same text is written as a managed block into this Harness's global context file, last in the file, and the Skill shows the exact target and the exact insertion before writing. Repeating `on` over an existing block rewrites it from the current perspective text, so it is idempotent and doubles as the refresh for a block `status` reports as stale.

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

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/brief on --help`. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

None.

## SEE ALSO

**/brief --help**, **/brief off --help**, **/brief status --help**
