# model-selector status

## NAME

model-selector status - report profile and evidence readiness

## SYNOPSIS

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector status` reports the active profile, evidence vintage, due sources, coverage gaps, provisional facts, low-confidence capability priors, configuration selections, and capture's own health without network access or writes.

The report distinguishes evidence that is absent, stale by the shipped cadence, provisional, or inapplicable rather than collapsing those states into one readiness value. Cadences are shipped with the Skill and the profile cannot override them.

`status` is also where unattended refresh is reported. Enabling this Skill installs a session-end pass that conditionally re-retrieves the non-commercial sources that are due; this section names every due source that pass may never retrieve — commercial terms, gateway rate cards, and any source kind or address it does not recognise — with `/model-selector update` as the command that resolves each. Where no source state exists yet, it reports that unattended refresh has nothing to check and that a typed `update` establishes the sources.

The same section names every enabled model selection that no benchmark has ranked, and every newer family version a previous `update` discovered and left excluded — the first resolved by `update`, the second by `config add model` or `config edit model`, adoption being your own act. Everything here is a report: `status` asks nothing, refuses nothing, and stops nothing.

Capture's own health is adapter presence per Harness this collection has an adapter for (`healthy`, `gated`, `degraded`, `absent`, or `unsatisfied`), whether that Harness's own finished session record can supply measurements at all, and how many bytes the capture store holds. This section performs no network request and writes nothing.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An absent or invalid profile is reported. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector status --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector update --help**, **/model-selector config --help**, **/model-selector recommend --help**
