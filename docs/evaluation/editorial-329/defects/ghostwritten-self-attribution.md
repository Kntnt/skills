## What to build

Part of #329, found during the candidate evaluation for #338. Preserve the supplied author's standpoint when ghostwriting a column: an author's reflection about a practice is not evidence that the author personally follows that practice. Diagnose the existing wording first and, where needed, clarify the existing ghostwriting boundary without adding a catalogue of stylistic rules.

Observed with instruction revision `d60c4fc`, frozen corpus `6e531f5`, GPT `gpt-6-astra/high`, Codex CLI 0.155.1. The synthetic source `docs/evaluation/corpus/editorial-quality/sources/column.md` says Nora is irritated that calendar time easily gets treated as a result, explicitly framing this as her reflection rather than something measured in others. It does not say she herself treats calendar entries as results.

The invocation `/write --genre=column --language=en_GB --output=response source.md` produced: “What irritates me is how easily I find myself regarding time in the calendar as a result in itself.” That introduces an unsupported personal admission. The Swedish invocation produced the related narrowing “åtminstone i mitt sätt att tänka kring mötesplanering”, likewise relocating the criticised tendency into Nora's own thinking. The reflection may be developed, but an unprovided personal habit cannot be used to make it sound more intimate. This is Source Fidelity, not a preference for impersonal writing.

Reproduction and complete evidence are local evaluation deliverables under `docs/evaluation/editorial-329/runs/candidate/column-en_GB/` and `column-sv/`, including source, exact prompt, full output, scoped loading trace and filesystem inventories. No source-aware correction is expected from Redline, which receives only the draft.

## Acceptance criteria

- [ ] Existing column/Source Fidelity instructions are assessed for ambiguity, and any necessary clarification preserves short professional guidance and legitimate personal reflection.
- [ ] A real affected rerun preserves the author's reflection without introducing a personal practice, memory, feeling or admission not supplied in the material.
- [ ] Failed candidate evidence and the source-aware finding remain recorded; no frozen criterion or source fixture is weakened.
- [ ] Any changed shipped resources have an updated catalog and pass the four CONTRIBUTING checks.

---
Written against d60c4fc
