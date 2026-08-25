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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check. Network access is required to refresh external evidence. The command reports an unreachable source without inventing current data.

## SEE ALSO

**/model-selector status --help**, **/model-selector config --help**
