# delegation on

## NAME

delegation on - enable delegation mode in the selected scope

## SYNOPSIS

**/delegation on** [**--project**|**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation on` adopts the mode as a standing instruction: the main agent decides whether delegation is worthwhile, plans, briefs, orchestrates, and verifies, while subagents execute what it chose to delegate. Once it has chosen, only that execution goes through model-selector's public `route` Interface, and routing never changes the main agent's own model or deliberation configuration.

The mode takes effect on the turn that switches it on, whichever scope was selected, so the mode does not wait for a restart. Without a scope flag the scope is this session alone, and context compaction may drop it — the Skill records the session state in the Harness's per-session scratch directory when one exists, so that it does not.

With `--project` or `--user` the mode text is written as a managed block into the context file that scope loads, last in the file, and the Skill shows the exact target, the exact insertion, and any bridge file to be created before writing. A Project block is normally committed, so everyone who clones the repository gets the mode. Repeating `on` over an existing block rewrites it from the current mode text, so it is idempotent and doubles as the refresh for a block `status` reports as stale.

## OPTIONS

**--project**

Target the context file this Project already loads instead of the current session.

**--user**

Target this Harness's global context file instead of the current session. There is no cross-agent convention for a global context file, so this scope covers the Harness it runs in; run the Skill again in another Harness to give that one the mode too.

**--yes**

Write the persistent block without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by a persistent scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation on --help`. A flag is refused rather than ignored where it has no work to do here, so both scope flags at once are invalid, and any token after the command path that is neither a scope flag nor `--yes` is refused the same way.

Two managed blocks in one file, or a marker without its pair, stop the write: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/delegation on**

Adopt the mode for the rest of this conversation, leaving any persistent block alone.

**/delegation on --project --yes**

Write the managed block into the Project's context file without asking for confirmation first.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints this page's SYNOPSIS, changes nothing, and points to `/delegation on --help`. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation --help**, **/delegation off --help**, **/delegation status --help**
