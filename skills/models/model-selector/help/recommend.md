# model-selector recommend

## NAME

model-selector recommend - select an exact configured model system for a workload

## SYNOPSIS

**/model-selector** **recommend** [**--decision=route**|**--decision=renew**] [**--budget=**_AMOUNT_|**--quality=**_SCORE_] [**--data=**_PATH_] [*WORKLOAD*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector recommend` builds comparable Pareto frontiers and selects one exact configured model system for a workload. It accounts for hard requirements, evidence quality, uncertainty, separate costs, decision mode, thresholds, and escalation.

When *WORKLOAD* is omitted, the current task is used only when unambiguous.

When representative matched measurements do not determine the exact point, cold start first chooses the weakest plausibly capable enabled model and then its lowest plausibly sufficient supported reasoning control. Reversible, objectively checked work begins there and escalates one adjacent Rung only after verified failure — the next reasoning control on the same model, or the next model up by capability where that scale is exhausted or the Harness carries the control. High-consequence or irreversible work without a trustworthy checker uses the strongest plausible enabled configuration and refuses unsafe exploration.

The result starts with one text-bearing evidence banner: `🔵 HEURISTISK STARTPUNKT`, `🟠 BLANDAD EVIDENS`, or `🟢 MÄTDATABASERAD REKOMMENDATION`.

The banner states its classification reason, confidence, missing evidence, and whether the point is an exploration start or production recommendation.

The result names the decision rule, nearest cheaper and stronger comparable neighbours, exclusions, uncertainty, and evidence staleness. If the evidence cannot support a choice, the command identifies the gap and proposes the smallest discriminating evaluation instead of inventing a rank.

After a blue or orange banner, a section titled `Snabbaste vägen till mätdata` supplies frozen inputs, the exact configurations to measure — the launch point and the one adjacent Rung the request can reach, or the measured frontier and the launchable points beside it where no exact point was selected, or that point alone where it reaches no second one, in which case both plans say there is nothing to compare — the checker and measurements, a bounded confidence-based stop, and both a quota-efficient sequential mode and a time-efficient parallel mode. The resulting observation artifact is accepted by `model-selector record`. `recommend` plans the experiment but performs no network request, evaluation, or write; normal work executes the brief, and there is no experiment command.

A section titled `Observerad förbrukning` follows, beside the recommendation and never inside it. For the selected point and its frontier neighbors, it reports what this machine's own Usage Record store holds for that Seat: the mean of each token category the Harness counted, the mean elapsed seconds, and the record count and vintage behind them. A figure no record supports is stated as absent, never as zero, and none of it enters the frontier, clears the quality floor, or chooses anything — the same profile and ledger, with and without Usage Records, select the same point.

## POSITIONAL ARGUMENTS

*WORKLOAD*

The task or workload to evaluate. Free-form text may contain several words.

## OPTIONS

**--decision=route**, **--decision=renew**

Compare marginal routing economics now or whether a fixed subscription fee earns renewal. `route` is the default.

**--budget=**_AMOUNT_

Select the highest conservative quality within a budget when every eligible point uses a comparable cost unit. Mutually exclusive with `--quality`.

**--quality=**_SCORE_

Select the lowest conservative comparable cost that clears the quality floor. Mutually exclusive with `--budget`.

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An absent profile starts guided setup. An unsupported option, incompatible threshold pair, or insufficiently identified workload is refused rather than ignored; the Skill prints this SYNOPSIS, changes nothing, and points to `/model-selector recommend --help`. An operand written before an option is out of order and is refused the same way.

## EXAMPLES

**/model-selector recommend --decision=route repository refactor**

Select a configured system for repository refactoring using marginal routing economics.

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

`uv` runs the shared offline selection module. The command reads bundled or locally stored evidence and reports when it is insufficient.

## SEE ALSO

**/model-selector chart --help**, **/model-selector config --help**, **/model-selector status --help**
