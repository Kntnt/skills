# model-selector config history

## NAME

model-selector config history - display profile revision history

## SYNOPSIS

**/model-selector** **config** **history** [**--data=**_PATH_]

## DESCRIPTION

`model-selector config history` displays stored profile revision timestamps and summaries from local history. It performs no network access or writes.

Evidence history is separate and remains append-only across configuration revisions.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unreadable history is reported. An unsupported option is refused rather than ignored; invalid syntax prints this SYNOPSIS and points to `/model-selector config history --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config show --help**, **/model-selector config reset --help**, **/model-selector status --help**
