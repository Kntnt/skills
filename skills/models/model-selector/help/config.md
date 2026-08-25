# model-selector config

## NAME

model-selector config - inspect or revise the model and access profile

## SYNOPSIS

**/model-selector** **config** [**show**|**history**|**reset**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** **add** [**--data=**_PATH_] (**model**|**channel**) [**--** *INSTRUCTION*]

**/model-selector** **config** (**edit**|**remove**) [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

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

An unknown or incomplete configuration subcommand is refused rather than ignored. The Skill prints the addressed page's SYNOPSIS, changes nothing, and points to the corresponding `--help` invocation. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config show --help**, **/model-selector config add --help**, **/model-selector config edit --help**, **/model-selector config remove --help**, **/model-selector config history --help**, **/model-selector config reset --help**
