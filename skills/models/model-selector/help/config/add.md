# model-selector config add

## NAME

model-selector config add - add a model selection or access channel

## SYNOPSIS

**/model-selector** **config** **add** (**model**|**channel**) [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config add` conducts a guided interview for one model selection or access channel, validates the complete revised profile, shows it for confirmation, and saves one new revision.

Adding a model attaches it to an existing or newly collected channel. Adding a channel may leave it unused only after explicit confirmation. Configuration commands consult local evidence and never trigger research or evaluations.

## POSITIONAL ARGUMENTS

**model**

Add one exact model selection with version identity, channel, modes, Harness, fallback policy, and watch policy.

**channel**

Add one access channel with provider, surface, billing type, tier, costs, quota rules, and provenance.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

A missing kind, unsupported kind, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config add --help`.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config edit --help**, **/model-selector config show --help**, **/model-selector update --help**
