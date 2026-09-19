## What to build

Part of #329; observed during the explicit article/ABT evaluation #338. Preserve uncertainty in headings as well as body prose. This is an observed breach of the existing claim-scope contract; investigate the actual need before adding an instruction.

At `1a4f65b`, corpus `6e531f5`, GPT-6-astra/high, Codex CLI 0.155.1, `/write --genre=article --technique=abt --language=sv --output=response source.md` produced the heading:

> Lufttemperatur berättar inte hur eleverna frös

The source says the report does not establish **whether** pupils felt cold. The output body itself retains “Rapporten säger heller inte om eleverna frös.” The heading’s **hur** instead presupposes that pupils did feel cold, turning unknown occurrence into an asserted experience whose manner is unknown. This is both a source-fidelity failure and a contradiction visible to source-blind Redline.

The full source, artifact, response and traces are preserved at `docs/evaluation/editorial-329/runs/candidate/article-abt/write/`; the ensuing unprompted Redline output is preserved separately. The frozen F1/P1 questions supply the judgment, not an exact preferred heading. The ABT relation itself is calm and functional: measurement, explanatory limits, supported further investigation.

## Acceptance criteria

- [ ] The original heading and its F1/P1 failure remain recorded with the complete input/output.
- [ ] Redline’s actual handling of the text-internal contradiction is recorded independently; no source package or expected correction is added to its prompt.
- [ ] Any rerun preserves uncertainty about whether the experience occurred, without requiring a canonical replacement sentence.
- [ ] Existing base/source-fidelity requirements are assessed before adding rules; a later successful sample is not claimed as guaranteed repair of a stochastic failure.
- [ ] The four checks in CONTRIBUTING.md pass for the integrated change.

---
Written against 1a4f65b
