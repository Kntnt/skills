# Disk is the source of truth; apply is idempotent

Harnesses only load skills that exist in their skills directories, so Enabled in a layer means present on disk in that layer. State is a reconstructable cache of those choices, not an authority. If State is missing or corrupt, the manager rebuilds it from collection skills on disk other than the Manager, and does not delete anything.

Enable, Disable, and Update compute the desired set for the targeted layer and apply the delta. Setup applies every skill Enabled in Global when it adds a Harness. A second run with the same answers is a no-op. A missing Catalog is fetched from the collection origin, never invented. If the manager itself is gone, the user reinstalls it with the transport. How a missing Harness list is rebuilt is ADR-0014.
