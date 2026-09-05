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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation --help**, **/delegation on --help**, **/delegation status --help**
