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

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

Every due source is reported as unchanged, changed, unreachable, or invalid. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector update --help`.

## EXAMPLES

**/model-selector update --force**

Check every relevant mutable source once while retaining immutable details and recorded observations.

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

`uv` runs the Skill's dependency check. Network access is required to refresh external evidence. The command reports an unreachable source without inventing current data.

## SEE ALSO

**/model-selector status --help**, **/model-selector config --help**
