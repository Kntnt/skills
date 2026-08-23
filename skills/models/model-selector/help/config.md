# model-selector config

## NAME

model-selector config - inspect or revise the model and access profile

## SYNOPSIS

**/model-selector** **config** [**show**|**add** (**model**|**channel**)|**edit** (**model**|**channel**) *ID*|**remove** (**model**|**channel**) *ID*|**history**|**reset**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config` manages the persisted profile without network access or evaluations. Bare `config` is equivalent to `config show`.

Configuration changes are validated, saved as revisions, and reported with any newly due evidence or invalidated frontiers. They never delete the evidence ledger.

## COMMANDS

**show**

Display the active profile. This is the default when no configuration subcommand is supplied.

**add** (**model**|**channel**)

Add one model selection or access channel through a guided interview.

**edit** (**model**|**channel**) *ID*

Edit one identified model selection or access channel.

**remove** (**model**|**channel**) *ID*

Remove one identified selection or channel after confirmation.

**history**

Display profile revision timestamps and summaries.

**reset**

Remove the active profile after confirmation while retaining history and evidence.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown or incomplete configuration subcommand is refused rather than ignored. The Skill prints the addressed page's SYNOPSIS, changes nothing, and points to the corresponding `--help` invocation.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config show --help**, **/model-selector config add --help**, **/model-selector config edit --help**, **/model-selector config remove --help**, **/model-selector config history --help**, **/model-selector config reset --help**
