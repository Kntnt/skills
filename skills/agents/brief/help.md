# brief

## NAME

brief - keep this conversation's replies concise and decision-relevant

## SYNOPSIS

**/brief** (**on**|**off**) [**--** *INSTRUCTION*]

**/brief** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`on` adopts the Brief perspective for later replies: it leads with the conclusion, keeps practical implications, decisions, and required user actions, and drops the narration around them. `off` drops the perspective again. Neither revisits the preceding answer, and an explicit request for detail overrides the mode for that reply.

The state belongs to the conversation it is typed in and to nothing else. It holds until `off` or until that conversation ends, and it is never observable in another window, another project, or a later session — two conversations open on the same project hold independent states, and `status` is how you ask which one you are sitting in.

Nothing is written anywhere. There is no settings key, no style file, and no state on disk, in any Harness: the mode lives in this conversation and ends with it, leaving nothing behind. A standing default across sessions is the user's own configuration rather than this Skill's business.

The mode takes effect on the turn it is typed, so the report of the change already obeys it.

The Skill takes no free-text operand and declares no flag. Put any guidance about the run after `--`, as `/brief on -- svara på svenska`.

Brief mode affects conversation replies, not code, documentation, commit messages, or other artifacts.

## COMMANDS

**on**

Adopt the Brief perspective for the rest of this conversation.

**off**

Drop the Brief perspective for the rest of this conversation.

**status**

Report whether the perspective is on or off in this conversation, without changing anything.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the most specific SYNOPSIS, changes nothing, and points to that page. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

A command path is required. A bare **/brief**, a second command path, and unseparated text are each an invalid form.

## EXAMPLES

**/brief on**

Keep later replies in this conversation concise and decision-relevant, leaving the preceding answer untouched.

**/brief status**

Report whether this conversation is currently in Brief mode.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/brief on --help**, **/brief off --help**, **/brief status --help**, **/tldr --help**, **/delegation --help**, **/kntnt select**
