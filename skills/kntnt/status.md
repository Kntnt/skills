# status

Report whether named skills are Enabled or Disabled in both Project and Global. With no skill names, report every Catalog skill. Status still runs when the Harness list is Unsatisfied.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" status` plus each named skill. Done when stdout is JSON.
2. Group `skills` by `category`. Say `harness_list` and `harnesses`. For each skill say Global and Project (`enabled`, `disabled`, or `partial`). Done when the user has the report.
