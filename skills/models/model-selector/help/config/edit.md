# model-selector config edit

## NAME

model-selector config edit - revise one model selection or access channel

## SYNOPSIS

**/model-selector** **config** **edit** [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config edit` shows one identified record, collects changed fields, validates the complete profile, shows the result for confirmation, and saves one new revision.

A selection ID remains stable when editing its version, channel, modes, or policies. Replacing a model version never occurs implicitly during evidence refresh.

## POSITIONAL ARGUMENTS

**model**|**channel**

Select whether *ID* identifies a model selection or an access channel.

*ID*

The stable identifier of the record to edit.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown ID, missing argument, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config edit --help`. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config add --help**, **/model-selector config remove --help**, **/model-selector config history --help**
