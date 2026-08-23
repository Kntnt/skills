# kntnt update

## NAME

kntnt update - refresh the Collection and re-check Dependencies

## SYNOPSIS

**/kntnt** **update** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**]

## DESCRIPTION

`kntnt update` re-copies every Enabled Skill in the targeted layer whose files differ from the current Catalog Digest and leaves matching Skills unchanged. Global is the default layer. Re-copying overwrites local changes to a Skill.

The Manager is refreshed on every successful update because it is not a Catalog entry and has no Digest. A Withdrawn Skill is removed from the targeted layer without confirmation. A newly added Catalog Skill is reported and offered for Enablement; accepting the offer Enables only that Skill, and any Unsatisfied Dependency is reported afterwards.

After file changes, Update checks every Dependency and Capability again. It is the only command that replaces the stored Catalog, preserving the comparison needed to identify new and Withdrawn entries on a later run.

## OPTIONS

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option.

**--yes**

Assume yes for confirmations, including the offer to Enable every new Catalog entry reported by the run. The report names every newly Enabled Skill.

**--dry-run**

Execute against a temporary home seeded with this Collection's files, report the Sandbox outcome, and discard it. Nothing in the selected layer changes. The isolated transport cache makes this slower than an ordinary run.

## OFFLINE OPERATION

If the Collection cannot be reached, Update refreshes nothing, removes nothing, reports no new entry, and leaves the stored Catalog unchanged. Run it again when the Collection is reachable.

## DIAGNOSTICS

An invalid argument or option with no work to do is refused rather than ignored. The Manager names the error, prints the SYNOPSIS, changes nothing, and points to the full page.

A Harness added since the previous run is detected automatically and needs no configuration.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Skill files move through `npx skills`.

**Network**

Required to fetch the current Catalog and Skill files. An unreachable Collection produces the bounded no-op described above.

## SEE ALSO

**/kntnt select --help**, **/kntnt uninstall --help**
