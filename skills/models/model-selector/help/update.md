# model-selector update

## NAME

model-selector update - refresh due public model evidence

## SYNOPSIS

**/model-selector** **update** [**--force**] [**--data=**_PATH_]

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

## DEPENDENCIES

Network access is required to refresh external evidence. The command reports an unreachable source without inventing current data.

## SEE ALSO

**/model-selector status --help**, **/model-selector config --help**
