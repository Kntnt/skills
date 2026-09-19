## What to build

Part of #329, observed during #338 final column verification. Preserve acceptable Swedish lowercase after a colon when the following complete clause is an integrated specification, rather than automatically capitalising every complete question. Clarify this locale distinction in the existing Swedish Mechanics scope; Proofread already owns preservation of established variation, so do not add a second general preservation rule or a style checklist.

At instruction revision `f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9`, corpus `6e531f5`, native GPT `gpt-6-astra/high`, Codex CLI 0.155.1, the source-blind `/redline --output=response input.md` pipeline in `docs/evaluation/editorial-329/runs/rerun-column-final/column-sv/redline/` delegated its final installed Proofread. It changed only “en fråga bredvid tiden: vad behöver vi förstå tillsammans?” to “en fråga bredvid tiden: Vad behöver vi förstå tillsammans?”. The whole artifact and native parent/child traces are preserved. The author text's lowercase question is a plausible integrated specification, not a changed claim or broken syntax.

Språkrådet's primary [Frågelådan guidance](https://frageladan.isof.se/faqs/25422) describes capitals as usual for utterance-like questions, while permitting lowercase in closely connected complete explanations. Thus the changed form is valid but the original is not demonstrably an error. The loaded Swedish Mechanics scope lacks this distinction; Proofread step 8 says to preserve what the loaded rules do not identify as erroneous. This is a limited variant-preservation defect, not substantive editorial rewriting or factual loss. Earlier L2 pass assessment is retained and explicitly superseded rather than erased.

## Acceptance criteria

- [ ] Preserve the exact original input, output, trace and superseded assessment with this finding.
- [ ] The existing Swedish Mechanics scope distinguishes independent quoted/utterance-like questions from acceptable integrated lowercase specification without forcing either form universally.
- [ ] Re-run the exact column-sv Redline input and the frozen column-clean control on the corrected resource revision; verify unchanged claims, purposeful recurrence, valid wording and exactly one final installed Proofread pass.
- [ ] Record the affected outcomes and observed limits without claiming broader reliability.
- [ ] Regenerate the shipped catalog and run the four CONTRIBUTING checks for any shipped resource change.

---
Written against 1a4f65b
