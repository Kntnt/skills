# brief status

## NAME

brief status - report whether this conversation is in Brief mode

## SYNOPSIS

**/brief status** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief status` reports one bit: whether the Brief perspective is on or off in this conversation. It writes nothing, changes nothing, and reframes nothing.

It exists because the state belongs to the conversation it was set in. Two windows open on the same project hold independent states, and this is the only way to ask which one you are sitting in.

There is nothing else to report: the state is held in this conversation and written nowhere, so there is no second state for this one to be weighed against.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/brief status --help`. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

## EXAMPLES

**/brief status**

Report whether this conversation is currently in Brief mode.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/brief --help**, **/brief on --help**, **/brief off --help**
