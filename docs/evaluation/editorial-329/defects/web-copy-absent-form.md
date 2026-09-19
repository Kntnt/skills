## What to build

Part of #329, found in the candidate evaluation for #338. Resolve or explicitly account for a web-copy interface reference that points to an absent form. First test whether the existing source-blind Redline diagnostics repair the reference from the visible text. A successful prescribed pipeline repair needs recorded evidence, not another general writing rule. If it survives review, inspect the existing task/surface boundary before adding instruction.

At instruction revision `d60c4fc`, corpus `6e531f5`, GPT `gpt-6-astra/high`, Codex CLI 0.155.1, `/write --genre=web-copy --language=en_GB --output=response source.md` with `docs/evaluation/corpus/editorial-quality/sources/web-copy.md` produced “provide your name, association and email address using the form below.” The complete Markdown artifact contains a link labelled “Express interest in a booking routine review” to the supplied external form destination, but no form below the paragraph. A reader is told to use an interface that is not present on the delivered surface. The material does support an interest form at the destination, so a bounded correction can name the linked form without inventing functionality.

Complete evidence and the unchanged input to Redline are under `docs/evaluation/editorial-329/runs/candidate/web-copy-en_GB/`. This is a concrete navigation/reference defect, separate from the correctly preserved price, scope, exclusions, non-order consequence and three-working-day reply. The evaluator identified it before reviewing Redline's output.

## Acceptance criteria

- [ ] The original Write defect remains recorded with the complete artifact and reproducible invocation.
- [ ] The paired source-blind Redline outcome is checked for an accurate form/link reference while preserving all service claims, conditions and destination.
- [ ] If the existing pipeline repairs it, record that bounded coverage without inventing a new general rule; if not, assess and verify the smallest justified correction to the existing instructions.
- [ ] Any shipped changes receive an updated catalog and the four CONTRIBUTING checks; evidence-only resolution records why no shipped change is needed.

---
Written against d60c4fc
