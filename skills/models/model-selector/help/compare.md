# model-selector compare

## NAME

model-selector compare - report comparable model-system frontiers

## SYNOPSIS

**/model-selector** **compare** *WORKLOAD* [**--decision=route**|**--decision=renew**] [**--data=**_PATH_]

## DESCRIPTION

`model-selector compare` is an alias of `model-selector chart`. It builds comparable Pareto frontiers without selecting one winner, then emits compact tables and plotting-ready CSV.

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

An absent workload or unsupported option is refused rather than ignored. An incomparable cohort is reported rather than silently combined. Invalid syntax prints this SYNOPSIS and points to `/model-selector compare --help`.

## DEPENDENCIES

None. The command reads bundled or locally stored evidence.

## SEE ALSO

**/model-selector chart --help**, **/model-selector recommend --help**
