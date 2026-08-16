# Each skill declares its dependencies; the catalog is generated; checks are shared

The Skill's `SKILL.md` is the source of its Dependency list, because the Skill must be able to refuse when the Catalog is not there. The Catalog is generated from those files so Status and Update can see the graph. The Catalog ships with the Manager; if it is missing it is fetched from the collection origin (ADR-0003). Every Skill calls the same checker in the Manager, so the Unsatisfied message stays one instruction, not a different paragraph in each Skill.
