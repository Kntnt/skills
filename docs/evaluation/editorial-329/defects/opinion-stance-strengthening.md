## What to build

Part of #329, discovered by the real candidate evaluation for #338. Preserve the supplied author's degree of commitment when composing an opinion article. A persuasive voice may sharpen the argument supported by the material; it may not turn absence of opposition into positive endorsement. Assess and clarify the existing authorial-voice boundary rather than adding a catalogue of stylistic rules.

Observed with instructions `d60c4fc`, frozen corpus `6e531f5`, GPT `gpt-6-astra/high`, Codex CLI 0.155.1. Reproduce with `/write --genre=opinion --language=en_GB --output=response source.md`, staging `docs/evaluation/corpus/editorial-quality/sources/opinion.md` as the sole input. The supplied Sanna Ek position says “Hon motsätter sig inte digital bokning.” The draft says “I support digital booking.” The former denies opposition; the latter asserts endorsement. This is a changed attributed standpoint, not a preferred translation or a demand for literal wording. The Swedish candidate preserved “Jag motsätter mig inte digital bokning.”

Complete local evidence is under `docs/evaluation/editorial-329/runs/candidate/opinion-en_GB/`: exact prompt, source, complete response and artifact, loading trace, native identity and full filesystem inventories. The artifact is passed unchanged to Redline, which has no source material and is not responsible for external verification. This evidence was first noted in a comment on #342, but is a separate genre-specific defect and is tracked here independently.

## Acceptance criteria

- [ ] The existing opinion voice/attribution instructions preserve the author's supplied stance without requiring neutralisation of a supported sharp argument.
- [ ] Real affected reruns retain the difference between non-opposition and endorsement while still delivering a persuasive debate article.
- [ ] Original failed evidence and source-aware F1 judgement remain visible; the source and frozen criteria are unchanged.
- [ ] Changed shipped resources have an updated catalog and pass the four CONTRIBUTING checks.

---
Written against d60c4fc
