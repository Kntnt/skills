# model-selector recommend

## NAME

model-selector recommend - select an exact configured model system for a workload

## SYNOPSIS

**/model-selector** **recommend** [*WORKLOAD*] [**--decision=route**|**--decision=renew**] [**--budget=**_AMOUNT_|**--quality=**_SCORE_] [**--data=**_PATH_]

## DESCRIPTION

`model-selector recommend` builds comparable Pareto frontiers from configured model systems and stored evidence, then selects one exact model, effort or thinking setting, Harness, tool policy, access channel, and commercial schedule. When *WORKLOAD* is omitted, the current task is used only when it is unambiguous.

The result names the decision rule, nearest cheaper and stronger comparable neighbours, exclusions, uncertainty, and evidence staleness. If the evidence cannot support a choice, the command identifies the gap and proposes the smallest discriminating evaluation instead of inventing a rank.

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

An absent profile starts guided setup. An unsupported option, incompatible threshold pair, or insufficiently identified workload is refused rather than ignored; the Skill prints this SYNOPSIS, changes nothing, and points to `/model-selector recommend --help`.

## EXAMPLES

**/model-selector recommend repository refactor --decision=route**

Select a configured system for repository refactoring using marginal routing economics.

## DEPENDENCIES

None. The command reads bundled or locally stored evidence and reports when it is insufficient.

## SEE ALSO

**/model-selector chart --help**, **/model-selector config --help**, **/model-selector status --help**
