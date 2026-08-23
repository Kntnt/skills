# model-selector config add

## NAME

model-selector config add - add a model selection or access channel

## SYNOPSIS

**/model-selector** **config** **add** (**model**|**channel**) [**--data=**_PATH_]

## DESCRIPTION

`model-selector config add` conducts a guided interview for one model selection or access channel, validates the complete revised profile, shows it for confirmation, and saves one new revision.

Adding a model attaches it to an existing or newly collected channel. Adding a channel may leave it unused only after explicit confirmation. Configuration commands consult local evidence and never trigger research or evaluations.

## POSITIONAL ARGUMENTS

**model**

Add one exact model selection with version identity, channel, modes, Harness, fallback policy, and watch policy.

**channel**

Add one access channel with provider, surface, billing type, tier, costs, quota rules, and provenance.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

A missing kind, unsupported kind, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config add --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config edit --help**, **/model-selector config show --help**, **/model-selector update --help**
