# delegation on

## NAME

delegation on - enable delegation mode in the selected scope

## SYNOPSIS

**/delegation on** [**--project**|**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation on` adopts the mode as a standing instruction: the main agent decides whether delegation is worthwhile and which path execution takes — a process detached from the conversation, a subagent, or its own seat narrowed at the source — then plans, briefs, orchestrates, and verifies, while subagents execute what it chose to delegate. Once it has chosen, execution it runs on the frozen main seat with no model, deliberation, or surface override is not routed; all other execution goes through model-selector's public `route` Interface, and routing never changes the main agent's own model or deliberation configuration.

The mode takes effect on the turn that switches it on, whichever scope was selected, so the mode does not wait for a restart. Without a scope flag the scope is this session alone, and context compaction may drop it — the Skill records the session state in the Harness's per-session scratch directory when one exists, so that it does not.

With `--project` or `--user`, the Skill shows the context file's managed `@agents.d/kntnt-delegation.md` pointer, the companion mode file, and any bridge before writing. A committed Project pair applies to everyone using the repository.

Repeating `on` refreshes an existing or stale pointer and companion.

## OPTIONS

**--project**

Target the context file this Project already loads instead of the current session.

**--user**

Target this Harness's global context file instead of the current session. There is no cross-agent convention for a global context file, so this scope covers the Harness it runs in; run the Skill again in another Harness to give that one the mode too.

**--yes**

Write the persistent files without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by a persistent scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation on --help`. A flag is refused rather than ignored where it has no work to do here, so both scope flags at once are invalid, and any token after the command path that is neither a scope flag nor `--yes` is refused the same way.

Two managed pointer blocks, a marker without its pair, or a companion without its pointer stop the write: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/delegation on**

Adopt the mode for the rest of this conversation, leaving any persistent pair alone.

**/delegation on --project --yes**

Write the managed pointer and companion into the Project without asking for confirmation first.

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

**/delegation --help**, **/delegation off --help**, **/delegation status --help**
