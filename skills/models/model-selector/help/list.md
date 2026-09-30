# model-selector list

## NAME

model-selector list - list selected Harnesses and current models

## SYNOPSIS

**/model-selector** **list** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Print two short inventories: the Harnesses selected in your validated profile, and the latest local catalogue release of each selected model series, grouped under its Maker's display name. Each series has one row with its concrete model id, so GPT-6.1 Sol and GPT-6 Sol can be distinguished. Harnesses, Makers and series are sorted stably.

Here “enabled” means selected in Model Selector's profile. A profile without `families` selects all series of its chosen Makers; an explicit selection follows new releases of those series automatically. The list reports profile choices regardless of which models a particular run can call.

The command reads the profile and local catalogue only. It asks no questions, reads no usage, selects no model, starts no Harness, probes no Bridge, reaches no network, generates no agent definitions and writes no persistent file. It performs no automatic refresh. Use `status` for the diagnostic report.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

With no valid profile, report that no configured models can be listed and point to `/model-selector setup`. Filesystem-detected Harnesses are never presented as profile choices. A selected series temporarily absent from the catalogue keeps its row, marked as having no catalogue release, without selecting another series.

An operand or an option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector list --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator between the Formal Invocation and an optional Contextual Instruction. Its contract is in `library/references/invocation-envelope.md` in the Collection Library.

## DEPENDENCIES

`uv` runs the local inventory reader. It reads the validated profile and local catalogue without reaching the network or writing anything.

## SEE ALSO

**/model-selector setup --help**, **/model-selector status --help**, **/model-selector --help**
