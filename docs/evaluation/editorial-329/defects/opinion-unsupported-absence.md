## What to build

Part of #329, observed in #338's opinion rerun for #343. Preserve the distinction between an absent claim about completed work and a factual assertion that the work has not been done. Assess the existing base claim-strength/absence boundary before adding any rule; this may be a stochastic execution failure under already-clear instructions.

At `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`, corpus `6e531f5`, native GPT `gpt-6-astra/high`, Codex CLI 0.155.1, `/write --genre=opinion --language=sv --output=response source.md` turned the source statement “Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket” into “Vi har varken kostnadsberäknat eller finansierat försöket.” The former withholds a claim; the latter asserts absence of the work. That absence is not established by the source, even though both forms leave a practical cost decision with the board. The separate delivery account recognises missing information, but the artifact asserts a stronger fact. The fixed non-opposition stance remains correct in this run.

Full source, artifact and native evidence are retained in `docs/evaluation/editorial-329/runs/rerun-343/opinion-sv/`. Source-blind Redline receives only the complete artifact and cannot be expected to reconstruct this source distinction. This is the frozen F1/base Claims test, not a preference for a particular sentence.

## Acceptance criteria

- [ ] Preserve the complete failed Write artifact and source-aware F1 assessment.
- [ ] Assess the paired source-blind Redline independently without expecting unseen-source verification.
- [ ] Any affected rerun leaves both the unknown funding/cost work and the board's cost decision within supplied limits, without requiring one canonical wording.
- [ ] Record whether resolution is an existing-contract execution limitation or a justified instruction repair; a later pass is not proof of guaranteed reliability.
- [ ] Run the four CONTRIBUTING checks for the integrated change.

---
Written against 1a4f65b
