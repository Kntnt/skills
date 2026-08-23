# model-selector update

## NAME

model-selector update - refresh due public model evidence

## SYNOPSIS

**/model-selector** **update** [**--force**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector update` performs one bounded refresh of mutable model indexes, first-party qualitative capability sources, commercial terms, and benchmark release indexes required by enabled selections and watched families. It initializes or appends applicable evidence and then rebuilds affected configured frontiers.

Capability sources follow the existing model/release cadence. A changed claim or normalized tag set appends an explicitly low-confidence categorical prior without rewriting history; provider prose never becomes a numeric score, clears a quality floor, or enters a Pareto frontier.

Known immutable model detail pages and recorded local run keys are not fetched or executed again. A discovered newer model version is reported but never enabled or substituted automatically.

## OPTIONS

**--force**

Check every relevant mutable index once regardless of cadence. Immutable details and existing observations remain untouched.

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

Every due source is reported as unchanged, changed, unreachable, or invalid. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector update --help`.

## EXAMPLES

**/model-selector update --force**

Check every relevant mutable source once while retaining immutable details and recorded observations.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. If unusable guidance can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

Network access is required to refresh external evidence. The command reports an unreachable source without inventing current data.

## SEE ALSO

**/model-selector status --help**, **/model-selector config --help**
