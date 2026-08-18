# Disk is the source of truth; apply is idempotent

Harnesses only load skills that exist in their skills directories, so Enabled in a layer means present on disk in that layer. State is a reconstructable cache of those choices, not an authority. If State is missing or corrupt, the manager rebuilds it from collection skills on disk other than the Manager, and does not delete anything.

Select and Update compute the desired set for the targeted layer and apply the delta. A second run with the same answers is a no-op. A missing Catalog is fetched from the collection origin, never invented. If the manager itself is gone, the user reinstalls it with the transport. Which directories a layer applies to is not remembered either; it is resolved by detection at each invocation (ADR-0035).
