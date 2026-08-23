# kntnt uninstall

## NAME

kntnt uninstall - remove the Collection from the machine

## SYNOPSIS

**/kntnt** **uninstall** [**--yes**] [**--dry-run**]

## DESCRIPTION

`kntnt uninstall` removes every Catalog Skill Enabled in Global from every Harness detected in the user's home directory, then removes the Manager through the transport. The Manager is removed only after every other confirmed removal succeeds, so a partial run retains the command needed to finish.

Project copies are never removed. They are part of their repositories and travel with those Projects.

## OPTIONS

**--yes**

Remove the Collection without waiting for confirmation. The script requires this option because Uninstall deletes files.

**--dry-run**

Execute against a temporary home seeded with this Collection's files, report the Sandbox outcome, and discard it. Nothing on the machine changes. The isolated transport cache makes this slower than an ordinary run.

## OFFLINE OPERATION

Uninstall fetches the current Catalog when possible and otherwise uses the stored Catalog. The report identifies which source determined the removal set.

## DIAGNOSTICS

`--project` and every other unsupported option are refused rather than ignored. The Manager names the error, prints the SYNOPSIS, removes nothing, and points to the full page.

If any Skill cannot be removed, the Manager remains Enabled and the report names what is left.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Files are removed through `npx skills`.

**Network**

Used to fetch the current Catalog. The stored Catalog is the fallback when the Collection is unreachable.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**
