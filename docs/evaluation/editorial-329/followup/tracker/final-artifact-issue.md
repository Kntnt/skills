## What to build

Part of #329. Diagnose and repair corruption of accepted prose across Redline’s closing mechanical pass and final delivery. At 3f21d9b1, fixed control frozen-clean-r1 repairs its Swedish quotation correctly but changes unrelated “arbetsbelastning” to “arbetsbelastningning” in the final response. This is a new L2/R1 failure, distinct from #341’s successful target repair in that run.

Full evidence: docs/evaluation/editorial-329/followup/runs/final-quotation-controls/frozen-clean-r1/redline/, including supplied-input.md, response.txt, independent-audit.json, both observed quotation reports and native sessions. The accepted correction and fresh quotation re-reader visibly contain the correct spelling. Installed Proofread reports no change, but its exact text dispatch is encrypted. The typo first becomes directly visible in the parent final response. This does not establish whether the mechanical input or later transcription introduced it.

Existing Redline steps require the complete mechanical result and no subsequent editing. Identify an actual transport/transcription seam before changing instructions; one execution failure does not establish a missing norm. Keep the hidden-stage uncertainty explicit and avoid a word-specific runtime rule.

## Acceptance criteria

- [ ] Preserve complete failed pipeline evidence and distinguish observed facts from the unobserved mechanical-input stage.
- [ ] Diagnose any reproducible transport or delivery defect before selecting a repair; an unchanged instruction alone is not proof of correction.
- [ ] Verify final complete prose against accepted pre-mechanical prose and actual mechanical changes, including a no-change mechanical result, in fresh native full-artifact runs.
- [ ] Retain single installed Proofread, exact output, full-root effects and cleanup evidence; record any remaining execution limitation honestly.
- [ ] Run the four CONTRIBUTING checks for the integrated change.

---
Written against cd375d4f
