# model-selector recommend

## NAME

model-selector recommend - select an exact configured model system for a workload

## SYNOPSIS

**/model-selector** **recommend** [**--decision=route**|**--decision=renew**] [**--budget=**_AMOUNT_|**--quality=**_SCORE_] [**--data=**_PATH_] [*WORKLOAD*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector recommend` builds comparable Pareto frontiers from configured model systems and stored evidence, then selects one exact model, effort or thinking setting, Harness, tool policy, access channel, and commercial schedule. It resolves complete points, categorical workload requirements, hard filters, evidence classes, uncertainty, multidimensional costs, route/renew decisions, budgets, quality floors, and escalation through the same executable selection core as `route`, then adds the detailed human presentation. When *WORKLOAD* is omitted, the current task is used only when it is unambiguous.

When representative matched measurements do not determine the exact point, cold start first chooses the weakest plausibly capable enabled model and then its lowest plausibly sufficient supported reasoning control. Reversible, objectively checked work begins there and escalates one adjacent reasoning rung only after verified failure. High-consequence or irreversible work without a trustworthy checker uses the strongest plausible enabled configuration and refuses unsafe exploration.

The result starts with exactly one text-bearing evidence banner: `🔵 HEURISTISK STARTPUNKT` for an exploratory point chosen from heuristics and capability priors, `🟠 BLANDAD EVIDENS` when measurements exist but a decision-relevant heuristic assumption remains, or `🟢 MÄTDATABASERAD REKOMMENDATION` when representative matched measurements determine the exact point and its conservative quality clears the floor. Every banner states the classification reason, confidence, missing evidence, and whether the point is an exploration start or a production recommendation; the words communicate the status without relying on emoji color.

The result names the decision rule, nearest cheaper and stronger comparable neighbours, exclusions, uncertainty, and evidence staleness. If the evidence cannot support a choice, the command identifies the gap and proposes the smallest discriminating evaluation instead of inventing a rank.

After a blue or orange banner, a section titled `Snabbaste vägen till mätdata` supplies frozen inputs, exact adjacent configurations, the checker and measurements, a bounded confidence-based stop, and both a quota-efficient sequential mode and a time-efficient parallel mode. The resulting observation artifact is accepted by `model-selector record`. `recommend` plans the experiment but performs no network request, evaluation, or write; normal work executes the brief, and there is no experiment command.

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

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

`uv` runs the shared offline selection module. The command reads bundled or locally stored evidence and reports when it is insufficient.

## SEE ALSO

**/model-selector chart --help**, **/model-selector config --help**, **/model-selector status --help**
