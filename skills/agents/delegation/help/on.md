# delegation on

## NAME

delegation on - enable delegation mode in the selected scope

## SYNOPSIS

**/delegation on** [**--project**|**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation on` adopts the mode as a standing instruction: the main agent decides whether delegation is worthwhile and which path execution takes — a process detached from the conversation, a subagent, or its own seat narrowed at the source — then plans, briefs, orchestrates, and verifies, while subagents execute what it chose to delegate. Once it has chosen, execution it runs on the frozen main seat with no model or deliberation override is not routed; all other execution asks model-selector's public `select` Interface for a seat, and that answer never changes the main agent's own model or deliberation configuration.

The mode takes effect on the turn that switches it on, whichever scope was selected, so the mode does not wait for a restart. Without a scope flag the scope is this session alone, and context compaction may drop it — the Skill records the session state in the Harness's per-session scratch directory when one exists, so that it does not.

With `--project` or `--user`, the Skill shows the context file's managed `@agents.d/kntnt-delegation.md` pointer, the mode and fence companion files, and any bridge before writing. A committed Project trio applies to everyone using the repository.

Repeating `on` refreshes an existing or stale pointer and both companions.

## OPTIONS

**--project**

Target the context file this Project already loads instead of the current session.

**--user**

Target this Harness's global context file instead of the current session. There is no cross-agent convention for a global context file, so this scope covers the Harness it runs in; run the Skill again in another Harness to give that one the mode too.

**--yes**

Write the persistent files without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by a persistent scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation on --help`. A flag is refused rather than ignored where it has no work to do here, so both scope flags at once are invalid, and any token after the command path that is neither a scope flag nor `--yes` is refused the same way.

Two managed pointer blocks, a marker without its pair, a pointer with either companion missing, or either companion without its pointer stop the write: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/delegation on**

Adopt the mode for the rest of this conversation, leaving any persistent trio alone.

**/delegation on --project --yes**

Write the managed pointer and both companions into the Project without asking for confirmation first.

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

**/delegation --help**, **/delegation off --help**, **/delegation status --help**
