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

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent profile starts guided setup. An unsupported option, incompatible threshold pair, or insufficiently identified workload is refused rather than ignored; the Skill prints this SYNOPSIS, changes nothing, and points to `/model-selector recommend --help`. An operand written before an option is out of order and is refused the same way.

## EXAMPLES

**/model-selector recommend --decision=route repository refactor**

Select a configured system for repository refactoring using marginal routing economics.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the shared offline selection module. The command reads bundled or locally stored evidence and reports when it is insufficient.

## SEE ALSO

**/model-selector chart --help**, **/model-selector config --help**, **/model-selector status --help**
