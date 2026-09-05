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

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector update --help**, **/model-selector config --help**, **/model-selector recommend --help**
