# Select and Update default to Global; `--project` targets the Project

The collection is personal tooling, so Select and Update default to Global. Pass `--project` or `--project=on` to target the current Project. Pass nothing, or `--project=off`, to target Global. Uninstall has no Project form at all, which is its own decision rather than an omission (ADR-0040).

Project extras live as skill files in that Project's harness directories. A teammate who checks those files in receives the extras, not the author's Global set. There is no subtractive overlay: unchecking a row in `select --project` removes a skill Enabled in the Project layer and does nothing to one Enabled only in Global, because this layer holds no copy of it to remove. What the row says instead, and why the rule is the one it is, belong to ADR-0013.
