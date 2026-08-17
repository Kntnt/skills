# One desired set per layer; harnesses are not a matrix

Letting each harness enable a different subset doubles the work and guarantees drift (Claude has A, OpenCode does not). Every skill Enabled in a layer is applied to every Harness that layer targets, and Project extras are not copied into Global; the user applies the Project layer with Enable `--project` or Update `--project`.

Since targets are resolved by detection rather than chosen (ADR-0035), the rule is now trivially true: there is no per-harness dimension left for a set to differ along, and no list to offer with anything pre-checked. What remains of this record is the reason the collection never grew one.
