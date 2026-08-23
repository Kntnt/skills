# model-selector status

## NAME

model-selector status - report profile and evidence readiness

## SYNOPSIS

**/model-selector** **status** [**--data=**_PATH_]

## DESCRIPTION

`model-selector status` reports the active profile, evidence vintage, due sources, coverage gaps, provisional facts, low-confidence capability priors, and configuration selections without network access or writes.

The report distinguishes evidence that is absent, stale by configured cadence, provisional, or inapplicable rather than collapsing those states into one readiness value.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent or invalid profile is reported. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector status --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector update --help**, **/model-selector config --help**, **/model-selector recommend --help**
