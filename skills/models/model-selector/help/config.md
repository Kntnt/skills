# model-selector config

## NAME

model-selector config - inspect or revise the model and access profile

## SYNOPSIS

**/model-selector** **config** [**show**|**add** (**model**|**channel**)|**edit** (**model**|**channel**) *ID*|**remove** (**model**|**channel**) *ID*|**history**|**reset**] [**--data=**_PATH_]

## DESCRIPTION

`model-selector config` manages the persisted profile without network access or evaluations. Bare `config` is equivalent to `config show`.

Configuration changes are validated, saved as revisions, and reported with any newly due evidence or invalidated frontiers. They never delete the evidence ledger.

## COMMANDS

**show**

Display the active profile. This is the default when no configuration subcommand is supplied.

**add** (**model**|**channel**)

Add one model selection or access channel through a guided interview.

**edit** (**model**|**channel**) *ID*

Edit one identified model selection or access channel.

**remove** (**model**|**channel**) *ID*

Remove one identified selection or channel after confirmation.

**history**

Display profile revision timestamps and summaries.

**reset**

Remove the active profile after confirmation while retaining history and evidence.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An unknown or incomplete configuration subcommand is refused rather than ignored. The Skill prints the addressed page's SYNOPSIS, changes nothing, and points to the corresponding `--help` invocation.

## DEPENDENCIES

None.

## SEE ALSO

**/model-selector config show --help**, **/model-selector config add --help**, **/model-selector config edit --help**, **/model-selector config remove --help**, **/model-selector config history --help**, **/model-selector config reset --help**
