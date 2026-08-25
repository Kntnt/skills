# Evaluation

The editorial Skills — Write, Redline, and Proofread — are judged by what they actually do in a real Harness, not by what their instructions say. This directory holds the two things that judging needs, and nothing else.

- [`corpus/`](corpus/README.md) — one shared body of fixture material: briefs, an interview transcript, a long factual source, clean and mechanically flawed prose, concentrated AI slop, material for several genres and techniques, Text Artifacts with present, conflicting, unusable, unrelated, and absent frontmatter, inline and file and URL sources, and the situations the output contract distinguishes. Each fixture is documented well enough to use without reading the Skill that consumes it.
- [`protocol.md`](protocol.md) — how a run is judged, what it writes down, and the provider-isolation rule that binds whoever runs it. Read it before running anything.

The corpus was built from the specification rather than from any Skill's implementation, which is what let it exist before the Skills did and what keeps it a test of the contract rather than a description of whatever was built.

Nothing here is a pytest suite. The suite under `tests/` checks that this corpus stays complete and self-describing; it does not run a model, and no test in this repository asserts a sentence a model has to write.

The reasoning is recorded in [ADR-0110](../adr/0110-what-an-editorial-skill-is-held-to.md).
