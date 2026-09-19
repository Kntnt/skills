## What to build

Part of #329. Make the independent source comparison account for factual presuppositions as well as the main assertions it reconstructs. Third-candidate `7b86144d` customer drafts use “her email” for Lena Ortiz and “Asked whether she…” for Priya Vale, while their complete fictional source packages provide no gender or gendered pronouns. The original Lind source does provide “Her”; supported personal attribution must remain available.

In the Ortiz report, the checker retains “her” in both its reconstructed assertion and its precise negation, then tests only whether Ortiz explained the subject in the email. The unprovided personal attribution is therefore never itself checked. This is a general proposition-coverage problem, not a reason to introduce a name-specific or gender-specific writing prohibition. Source Fidelity's existing criterion already applies.

Keep the full failures at `docs/evaluation/editorial-329/followup/runs/third-candidate/case-unprompted-en_US-r1/` and `case-question-en_GB-r1/`. Earlier equivalent baseline and first-candidate passes receive visible superseding judgements; their original records and authentic-question positive-control results remain history. Diagnose the missed operation with a neutral full-source replay before changing product instructions.

## Acceptance criteria

- [ ] Preserve every observed failure and its full source, final artifact, native claim account and unchanged F1 judgement.
- [ ] The comparison checks factual presuppositions independently rather than carrying them untested into both assertion and negation; avoid fixture-specific wording rules.
- [ ] Repeated fresh runs of both supplementary customer sources avoid unsupported personal attribution while preserving supplied quotations and genuine question framing where present.
- [ ] A source that expressly supplies the personal attribution remains a preservation control; chronology and document-scope cases retain regression coverage.
- [ ] Record complete source-blind Redline pairs, applicable criteria, actual execution and cleanup, and run the four CONTRIBUTING checks for the integrated change.

---
Written against 7b86144d; fourth Redline-only candidate ae24f9b3 leaves this source-check resource unchanged.
