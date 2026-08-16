# Enable and Disable default to Global; `--project` targets the Project

The collection is personal tooling, so Enable, Disable, and Update default to Global. Pass `--project` or `--project=on` to target the current Project. Pass nothing, or `--project=off`, to target Global. Status always reports both layers.

Project extras live as skill files in that Project's harness directories. A teammate who checks those files in receives the extras, not the author's Global set. There is no subtractive overlay: `disable --project` does nothing to a skill that is Enabled only in Global (ADR-0013).
