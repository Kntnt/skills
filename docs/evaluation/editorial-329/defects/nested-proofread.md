## What to build

Part of #329; discovered by the real baseline evaluation in #338. Redline's closing Proofread handoff must carry the complete current artifact without letting YAML frontmatter or text tokens become invocation flags. Use the existing omitted-operand contract with the complete text explicitly supplied to the nested turn, or another demonstrably lossless existing invocation form. Do not add grammar, bypass the installed Proofread Skill or weaken the single final pass.

Observed on baseline `8ae4c21`, corpus `6e531f5`, GPT `gpt-6-astra/high`, Codex CLI 0.155.1. Reproduction: Write article/sv from `docs/evaluation/corpus/editorial-quality/sources/article.md`, then `/redline --output=response input.md` on the resulting YAML-bearing draft. Redline sent `--language=sv --output=response` followed by an unquoted `---` block to the Proofread shim. The engine refused `'---' is not a flag of this collection's grammar`; Redline delivered no final artifact. Evidence: `docs/evaluation/editorial-329/runs/baseline/article-sv/redline/` (local evaluation deliverable; not yet pushed).

## Acceptance criteria

- [ ] The shipped Redline instruction explicitly separates the nested Formal Invocation from the complete current Text Artifact, preserving frontmatter and text verbatim.
- [ ] A real candidate pipeline with YAML metadata reaches exactly one successful final Proofread pass and delivers the complete artifact or correct no-change status.
- [ ] Previous failed baseline evidence remains, with no retroactive claim that it passed.
- [ ] The four CONTRIBUTING checks pass for the integrated change.

---
Written against 6e531f5
