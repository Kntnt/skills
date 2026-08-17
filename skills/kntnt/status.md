# status

Report whether named skills are Enabled or Disabled in both Project and Global. With no skill names, report every Catalog skill.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" status` plus each named skill. Done when stdout is JSON.
2. Group `skills` by `category`. Name the `directories` the report covers in each layer — that is where Enable, Disable, and Update would act. Done when the report is grouped.
3. Report **every** skill the payload carries, Disabled ones included — with no names the payload is the whole Catalog, and a report that shows only the Enabled ones hides exactly what the user asked Status for. For each skill say Global and Project (`enabled`, `disabled`, or `partial`), and name any `capabilities` it needs of the harness. Done when the user has the report.
4. If a skill the user expected is absent, its Catalog is older than the collection: say `/kntnt update` refreshes it. Done when that is said, or nothing was missing.
