# model-selector config reset

## NAME

model-selector config reset - remove the active profile while retaining evidence

## SYNOPSIS

**/model-selector** **config** **reset** [**--data=**_PATH_]

## DESCRIPTION

`model-selector config reset` shows the exact active configuration path, requests confirmation, appends a tombstone to configuration history, and removes only the active `config.json`. Evidence and revision history are retained.

The next command that requires model selections starts guided setup.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

A declined confirmation, absent profile, or unsupported option changes nothing. Invalid syntax is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config reset --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector setup --help**, **/model-selector config history --help**, **/model-selector config remove --help**
