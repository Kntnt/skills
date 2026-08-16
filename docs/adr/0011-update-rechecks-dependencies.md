# Update re-checks dependencies; it does not refresh externals

`/kntnt update` refreshes only this collection. An External is updated with the transport. After the collection files change, every Dependency is checked again, because a new Skill revision may add, drop, or replace a Dependency. If a Dependency is Unsatisfied, Update does not install it; it tells the user how to satisfy it (ADR-0009). Update reports each new Catalog entry and leaves it Disabled (ADR-0007). Without `--project` it applies the Global layer; with `--project` it applies the Project layer.
