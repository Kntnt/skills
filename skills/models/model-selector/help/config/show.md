# model-selector config show

## NAME

model-selector config show - display the active model and access profile

## SYNOPSIS

**/model-selector** **config** **show** [**--data=**_PATH_]

## DESCRIPTION

`model-selector config show` displays the active profile path and revision together with model selections, access channels, commercial units, modes, version-watch policy, and unresolved fields. Bare `/model-selector config` has the same effect.

The command reads local configuration and evidence only; it performs no network access, evaluation, or write.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent or invalid profile is reported. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config show --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config add --help**, **/model-selector config history --help**, **/model-selector status --help**
