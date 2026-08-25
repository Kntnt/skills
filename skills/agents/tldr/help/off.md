# tldr off

## NAME

tldr off - disable TL;DR mode for the selected scope

## SYNOPSIS

**/tldr off** [**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`tldr off` treats the standing TL;DR instruction as inert history for subsequent replies. It changes nothing about the preceding answer and reframes nothing.

It takes effect on the turn that switches it off, so the report of the removal is already written without the perspective. Without `--user` it suspends the mode for this session alone. With `--user` it removes the managed block from this Harness's global context file, both markers included and nothing else, after showing the exact target and the exact removal.

`off` is an exact undo of `on`, which is why no backup file is written, in git or out. Where there is no block to remove, the Skill says so and stops: nothing to remove is not an error.

## OPTIONS

**--user**

Target this Harness's user context instead of the current session. There is no Project scope: conversational perspective and density are reader preferences rather than a shared Project convention.

**--yes**

Remove the user block without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by the user scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/tldr off --help`. A flag is refused rather than ignored where it has no work to do here, and any token after the command path that is neither `--user` nor `--yes` is refused the same way.

Two managed blocks in one file, or a marker without its pair, stop the removal: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/tldr off**

Stop applying the TL;DR perspective to later replies in this conversation, leaving any user-level block alone.

**/tldr off --user**

Show the managed block in this Harness's global context file and, once confirmed, remove it together with both markers.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/tldr --help**, **/tldr on --help**, **/tldr status --help**
