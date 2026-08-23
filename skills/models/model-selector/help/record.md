# model-selector record

## NAME

model-selector record - append validated local evaluation observations

## SYNOPSIS

**/model-selector** **record** *PATH* [**--data=**_PATH_]

## DESCRIPTION

`model-selector record` validates local evaluation observations at *PATH* and appends unseen records to the evidence ledger. Conflicting historical observations are preserved instead of overwritten.

The command records the exact model configuration, workload, metrics, units, provenance, and run identity needed for later comparisons.

## POSITIONAL ARGUMENTS

*PATH*

The local file containing evaluation observations to validate and append.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unreadable path, invalid observation, unsupported option, or conflicting run identity is refused rather than ignored. The Skill prints this SYNOPSIS, appends nothing, and points to `/model-selector record --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector status --help**
