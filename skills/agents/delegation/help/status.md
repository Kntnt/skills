# delegation status

## NAME

delegation status - report the mode's state in one scope or in all three

## SYNOPSIS

**/delegation status** [**--project**|**--user**] [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation status` reports the state of the selected scope, the effective verdict, and any staleness. With no scope flag it reports all three scopes, which is what makes a disagreement between standing persistent state and a session instruction visible in one line. It writes nothing, in any scope, and asks nothing, because it changes nothing.

Persistent state is stale when its pointer block or either companion file differs from what the Skill would write today. The report names that condition rather than silently treating the trio as current, and names `/delegation on --project` or `/delegation on --user` as the fix because `on` rewrites all three managed files.

## OPTIONS

**--project**

Report the Project scope alone instead of all three.

**--user**

Report the user scope alone instead of all three.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/delegation status --help`. A flag is refused rather than ignored where it has no work to do here.

`--yes`, both scope flags together, and any unrecognized token are invalid.

## EXAMPLES

**/delegation status**

Report all three scopes, the effective verdict, and whether each standing pointer and both companions still match what the Skill would write today.

**/delegation status --project**

Report the Project scope alone.

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

**/delegation --help**, **/delegation on --help**, **/delegation off --help**
