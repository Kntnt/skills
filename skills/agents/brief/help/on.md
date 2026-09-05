# brief on

## NAME

brief on - adopt the Brief perspective for this conversation

## SYNOPSIS

**/brief on** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief on` adopts the Brief perspective as a standing instruction for the rest of this conversation. It does not revisit, reframe, or summarise the preceding answer; `/tldr` is what re-explains an answer that did not land.

The mode takes effect on the turn that switches it on, so the report of the change already obeys it. An explicit request for more detail overrides the default level for that reply, and the perspective governs conversation replies rather than code, documentation, comments, commit messages, or other artifacts.

It reaches this conversation and nothing else. Another window on the same project, another project, and every later session are unaffected, and the state ends when this conversation does.

Nothing is written. There is no settings key, no style file, and no state on disk, in any Harness: the mode lives in this conversation and ends with it, leaving nothing behind.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief on --help`. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

## EXAMPLES

**/brief on**

Keep later replies in this conversation concise and decision-relevant, leaving the preceding answer untouched.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/brief --help**, **/brief off --help**, **/brief status --help**
