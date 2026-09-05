# brief off

## NAME

brief off - drop the Brief perspective for this conversation

## SYNOPSIS

**/brief off** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief off` treats the standing Brief instruction as inert history for the rest of this conversation. It changes nothing about the preceding answer and reframes nothing.

It takes effect on the turn that switches it off, so the report of the change is already written without the perspective. It reaches this conversation and nothing else, exactly as `on` does.

Nothing is removed, because nothing was written. `off` where the mode was never on is not an error: the Skill says so and stops.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief off --help`. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

## EXAMPLES

**/brief off**

Stop applying the Brief perspective to later replies in this conversation.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/brief --help**, **/brief on --help**, **/brief status --help**
