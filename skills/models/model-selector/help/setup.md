# model-selector setup

## NAME

model-selector setup - create or fully review the model and access profile

## SYNOPSIS

**/model-selector** **setup** [**--data=**_PATH_]

## DESCRIPTION

`model-selector setup` conducts a guided review of the exact model versions and access channels available to the user. It collects model identity, effort or thinking policy, serving modes, Harness, channel, commercial terms, quota rules, and version-watch policy without storing credentials.

The complete profile is shown before it is written. Reopening setup for an existing profile creates a validated revision and retains evidence history.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An incomplete or invalid profile is not written. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector setup --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config --help**, **/model-selector update --help**
