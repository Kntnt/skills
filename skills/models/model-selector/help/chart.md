# model-selector chart

## NAME

model-selector chart - report comparable model-system frontiers without choosing a winner

## SYNOPSIS

**/model-selector** **chart** *WORKLOAD* [**--decision=route**|**--decision=renew**] [**--data=**_PATH_]

## DESCRIPTION

`model-selector chart` follows recommendation analysis through frontier construction without selecting one winner. It emits a compact table and plotting-ready CSV for each comparable cohort.

Cash, quota, and renewal views remain separate unless the profile supplies an explicit shadow price that makes a shared numeric axis valid. Unavailable metrics are `null`, never zero.

## POSITIONAL ARGUMENTS

*WORKLOAD*

The task or workload whose configured systems are compared.

## OPTIONS

**--decision=route**, **--decision=renew**

Compare marginal routing economics now or fixed-fee renewal economics. `route` is the default.

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.model-selector/`.

## DIAGNOSTICS

An absent workload or unsupported option is refused rather than ignored. An incomparable cohort is reported rather than silently combined. Invalid syntax prints this SYNOPSIS and points to `/model-selector chart --help`.

## DEPENDENCIES

None. The command reads bundled or locally stored evidence.

## SEE ALSO

**/model-selector compare --help**, **/model-selector recommend --help**
