# model-selector update

## NAME

model-selector update - refresh catalogue facts without repeating setup

## SYNOPSIS

**/model-selector** **update** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Run the manual catalogue pass now using the existing profile's chosen Makers. It runs even when today's scheduled pass already ran, asks no questions and requires no renewed profile approval. Use `setup` to change your choices and `status` for diagnostics.

The brief answer says whether the pass ran, whether each consulted source was read completely, only in part, or not at all, its reason and change count, and which models were added or removed when those changes occurred. A complete source with zero changes means “no changes”. A source failure is reported alongside the other sources' actual results. Generated subagent definitions written or removed, and any write errors or deadline outcome, are reported where they occur.

The pass uses the existing lock, deadlines, validation, journal, missing-release rules and generated definition sync. It starts no model jobs and changes no daily schedule. The profile, including its answer date, Harnesses, Makers, payment channels and series choices, and the standing objective remain byte-identical. A new series gains only the permissions the profile already gives it: all-series includes future series; an explicit series selection does not.

When a model has been absent from its Maker's complete list on three consecutive days, the existing lifecycle rule removes it. Its measurements and pending units are deleted where no newer release of its family remains to inherit them.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

If another pass holds the lock, report that another pass is running and this caller did nothing. With no valid profile choosing a Maker, report “no makers chosen”, that no sources were read, and point briefly to `/model-selector setup`. Neither outcome starts an interview or writes a profile.

An operand or an option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector update --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator between the Formal Invocation and an optional Contextual Instruction. Its contract is in `library/references/invocation-envelope.md` in the Collection Library.

## DEPENDENCIES

`uv` runs the catalogue pass. The pass reads the chosen Makers' structured Claude Code or Codex model lists and OpenRouter's public model list; it starts no model to discover catalogue facts.

## SEE ALSO

**/model-selector setup --help**, **/model-selector status --help**, **/model-selector list --help**, **/model-selector --help**
