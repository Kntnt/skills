# model-selector config edit

## NAME

model-selector config edit - revise one model selection or access channel

## SYNOPSIS

**/model-selector** **config** **edit** (**model**|**channel**) *ID* [**--data=**_PATH_]

## DESCRIPTION

`model-selector config edit` shows one identified record, collects changed fields, validates the complete profile, shows the result for confirmation, and saves one new revision.

A selection ID remains stable when editing its version, channel, modes, or policies. Replacing a model version never occurs implicitly during evidence refresh.

## POSITIONAL ARGUMENTS

**model**|**channel**

Select whether *ID* identifies a model selection or an access channel.

*ID*

The stable identifier of the record to edit.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown ID, missing argument, invalid revision, or unsupported option is refused rather than ignored. The Skill prints this SYNOPSIS, writes nothing, and points to `/model-selector config edit --help`.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config add --help**, **/model-selector config remove --help**, **/model-selector config history --help**
