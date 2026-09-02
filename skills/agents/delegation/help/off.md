# delegation off

## NAME

delegation off - disable delegation mode in the selected scope

## SYNOPSIS

**/delegation off** [**--project**|**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation off` treats the standing mode instruction as inert history: the agent executes tasks itself again and spawns subagents only when the user asks. Delegating in general stays open — what stops is this Skill's own instruction.

Without a scope flag it suspends the mode for this session alone, including where a Project or user trio is standing. Context already loaded for this session and its tokens are still paid; a compaction can drop the session instruction while the persistent trio survives, so run `/delegation off` again if delegating resumes.

With `--project` or `--user` it removes the managed pointer block from that scope's context file and deletes both companion files after showing all three exact removals. `off` is the exact undo of `on`, which is why no backup file is written, in git or out. Where none of the three managed files exists, the Skill says so and stops: nothing to remove is not an error.

## OPTIONS

**--project**

Target the context file this Project already loads instead of the current session.

**--user**

Target this Harness's global context file instead of the current session. Run the Skill again in another Harness to remove that one's block.

**--yes**

Remove the persistent files without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by a persistent scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation off --help`. A flag is refused rather than ignored where it has no work to do here, so both scope flags at once are invalid, and any token after the command path that is neither a scope flag nor `--yes` is refused the same way.

Two managed pointer blocks, a marker without its pair, a pointer with either companion missing, or either companion without its pointer stop the removal: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/delegation off**

Stop obeying the mode for the rest of this conversation, leaving any persistent trio in place.

**/delegation off --user**

Show the managed pointer and both companions in this Harness's global context and, once confirmed, remove all three.

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

**/delegation --help**, **/delegation on --help**, **/delegation status --help**
