# Update re-adds; the transport's `update` is not a refresh

`npx skills update` compares `SKILL.md` and skips a skill whose `SKILL.md` is unchanged. It exits 0 and reports everything up to date, while every sidecar in that directory — `catalog.json`, helper documents, scripts — stays at the revision that last happened to touch `SKILL.md`. A collection whose skills are mostly sidecar therefore could not be updated at all: `delegation` was added to the Catalog in 0.3.0, and no `/kntnt update` could deliver it, because `skills/kntnt/SKILL.md` had not changed since 0.1.0.

Update calls the transport's `add` instead, which re-copies the whole directory and is idempotent (ADR-0003). Update also writes the Catalog to the running Manager's own directory. `add` reaches the recorded Harnesses, and those need not include the copy of the Manager being run right now — a Harness list of `opencode` never refreshes a Manager invoked from `~/.claude/skills` — so the layer that Status reads has to be refreshed directly or it stays frozen.

The test double models the real `update`, skipping a skill whose `SKILL.md` matches. It previously copied unconditionally, which is why the suite was green while the collection could not be updated: a double more capable than the thing it stands in for tests nothing.
