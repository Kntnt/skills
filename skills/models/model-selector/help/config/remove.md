# model-selector config remove

## NAME

model-selector config remove - remove one model selection or access channel

## SYNOPSIS

**/model-selector** **config** **remove** (**model**|**channel**) *ID* [**--data=**_PATH_]

## DESCRIPTION

`model-selector config remove` shows the exact target and consequences, then removes it from the active profile after confirmation and saves one new revision. Evidence and configuration history are retained.

A channel still referenced by a model selection must be reassigned or have its dependent selections removed in the same revision.

## POSITIONAL ARGUMENTS

**model**|**channel**

Select whether *ID* identifies a model selection or an access channel.

*ID*

The stable identifier of the record to remove.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown ID, referenced channel without a resolution, declined confirmation, or unsupported option writes nothing. Invalid syntax is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config remove --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config edit --help**, **/model-selector config history --help**, **/model-selector config reset --help**
