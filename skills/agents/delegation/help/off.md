# delegation off

## NAME

delegation off - disable delegation mode in the selected scope

## SYNOPSIS

**/delegation off** [**--project**|**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation off` treats the standing mode instruction as inert history: the agent executes tasks itself again and spawns subagents only when the user asks. Delegating in general stays open — what stops is this Skill's own instruction.

Without a scope flag it suspends the mode for this session alone, and it suspends it even where a Project or user block is standing: that block's text stays in the context window and its tokens are still paid, and a compaction can drop the session instruction while the block survives, so run `/delegation off` again if delegating resumes.

With `--project` or `--user` it removes the managed block from that scope's context file, both markers included and nothing else, after showing the exact target and the exact removal. `off` is an exact undo of `on`, which is why no backup file is written, in git or out. Where there is no block to remove, the Skill says so and stops: nothing to remove is not an error.

## OPTIONS

**--project**

Target the context file this Project already loads instead of the current session.

**--user**

Target this Harness's global context file instead of the current session. Run the Skill again in another Harness to remove that one's block.

**--yes**

Remove the persistent block without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by a persistent scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation off --help`. A flag is refused rather than ignored where it has no work to do here, so both scope flags at once are invalid, and any token after the command path that is neither a scope flag nor `--yes` is refused the same way.

Two managed blocks in one file, or a marker without its pair, stop the removal: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/delegation off**

Stop obeying the mode for the rest of this conversation, leaving any persistent block in place.

**/delegation off --user**

Show the managed block in this Harness's global context file and, once confirmed, remove it together with both markers.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/delegation off --help`. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation --help**, **/delegation on --help**, **/delegation status --help**
