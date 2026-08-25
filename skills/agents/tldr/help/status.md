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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/tldr --help**, **/tldr on --help**, **/tldr off --help**
