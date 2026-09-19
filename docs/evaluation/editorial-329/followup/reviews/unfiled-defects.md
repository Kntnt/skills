# Definite defect inventory for tracker integration

These are separate observed defect classes under the unchanged rubric, not speculative causes. Root owns filing and native parent/blocker relations. Paths below are relative to `docs/evaluation/editorial-329/followup/` unless explicitly prefixed otherwise.

## Preserve functioning quoted wording during source-blind review

At `ae24f9b3`, Redline unnecessarily changes the original English quotation “I would set that time aside before the next building starts.” to “I would set that time aside before the trial starts in the next building.” The exact positive-control replay at `3f21d9b1` repeats the change. Complete local context already identifies the repair-log trial and possible expansion; this is functioning contextual English shorthand. The reader's literal building-as-actor interpretation identifies no concrete English obstruction. Meaning remains faithful (F1 is not the failure); R1 preservation fails. This is distinct from the Swedish translation defect in #341.

Evidence:

- `runs/third-candidate/case-study-en_US-r2/draft.md`: exact original artifact, frozen before either review.
- `runs/quotation-candidate/case-study-en_US-r2/redline/{supplied-input.md,response.txt,quotation-reports.json,native-sessions/}`: first unnecessary change.
- `runs/final-quotation-original/case-study-en_US-r2/redline/{supplied-input.md,response.txt,quotation-reports.json,quotation-transport-audit.json,native-sessions/}`: repeat at latest quotation revision.
- In the latest native directory `2026/09/20/`, initial reader `rollout-2026-09-20T00-42-34-01a0bbd5-ebea-7b03-a944-782d97f83160.jsonl` supplies the finding; correction `00-44-18-01a0bbd7-81f3-7cf0-a9b5-e98761fa0eb9` implements it; fresh reader `00-45-32-01a0bbd8-a3c9-7c52-b8e5-220fda950303` approves. Full artifact/guidance file reads are visible, so this is not an input-transport conjecture.
- Formal records: `docs/evaluation/records/redline-gpt-2026-09-20-341-quotation-original.md` and `redline-gpt-2026-09-20-341-final-quotation-original.md`.

Suggested acceptance: preserve both failures and R1 judgments; diagnose unnecessary finding versus useful target-language correction without prohibiting metonymy; run source-blind full-artifact preservation controls on unchanged inputs alongside genuine Swedish idiom defects; preserve wording, voice and meaning outside concrete findings; retain all process/side-effect evidence and integrated technical checks. A rollback is an admissible implementation choice but needs final-revision evidence, not historical results relabeled as current.

## Preserve final artifact bytes through the closing mechanical pass and delivery

At `3f21d9b1`, fixed control `frozen-clean-r1` correctly repairs the Swedish quotation, but the final response changes “arbetsbelastning” into “arbetsbelastningning” in an unrelated paragraph. This is a new L2 and R1 failure even though the targeted #341 repair succeeds. The accepted correction and fresh quotation re-reader's actual artifact both retain the correct spelling. The installed closing Proofread reports no change. Its exact dispatch is encrypted; the typo is first directly visible in the parent final response. Do not claim the typo was definitely introduced after Proofread, or blame a mechanical checker that may not have received those bytes.

Evidence in `runs/final-quotation-controls/frozen-clean-r1/redline/`:

- `supplied-input.md`, `response.txt`, `independent-audit.json` (complete two-change diff), `observed-quotation-report-1.md`, `observed-quotation-report-2.md`.
- `native-sessions/2026/09/20/rollout-2026-09-20T00-33-34-01a0bbcd-b01a-7f53-966b-d414ba83fb7f.jsonl`: corrector's complete returned artifact has the correct spelling.
- `native-sessions/2026/09/20/rollout-2026-09-20T00-34-38-01a0bbce-a84f-7ca2-8ce9-30922e3b75f7.jsonl`: fresh quotation reader visibly reads the correctly spelled artifact.
- `native-sessions/2026/09/20/rollout-2026-09-20T00-35-21-01a0bbcf-5150-74b0-9ea4-070748950eb8.jsonl`: installed Proofread invocation and no-change report; exact passed text is not visible.
- `native-sessions/2026/09/20/rollout-2026-09-20T00-30-48-01a0bbcb-2797-70a3-ac42-4fd7278daeb5.jsonl`: parent final response first visibly contains the typo.
- Formal record: `docs/evaluation/records/redline-gpt-2026-09-20-341-final-quotation-controls.md`, frozen-clean-r1.

Suggested acceptance: preserve the complete observed pipeline and uncertainty about the hidden stage; identify any actual transport/transcription seam before changing instructions; verify that the complete final artifact preserves the accepted prose except verified mechanical corrections, including a no-change mechanical result; use exact artifacts without a word-specific runtime rule; audit actual single Proofread invocation, full output and cleanup. Existing step 9's complete-result rule and step 10's “nothing has been touched since the pass” already prohibit the observed corruption; do not infer a missing norm from one execution failure.

## Preserve measurement-variable meanings across translation

A distinct child issue is warranted. Four original English opinion drafts at `8f92e12` broaden or substitute the variables the pilot did not measure. Complete source says “Den mäter inte ålder, funktionsförmåga eller digital vana.” All four drafts instead say disability was not measured; three also say digital skills. Functional ability is not the same variable as disability status, and digital familiarity/experience is not the same as skill/confidence/proficiency. A report can collect one without collecting the other. These are report-wide claims about measured variables, unlike a later correct sentence saying aggregate booking counts do not establish users' skills.

Exact first-wave draft passages:

- `runs/candidate/opinion-en_GB-r1/draft.md`: “Nor did the report measure age, disability or digital skills.”
- `runs/candidate/opinion-en_GB-r2/draft.md`: “The report measures neither age nor disability nor digital skills.”
- `runs/candidate/opinion-en_US-r1/draft.md`: “The report does not measure age, disability, or digital skills.”
- `runs/candidate/opinion-en_US-r2/draft.md`: “The report measured neither age nor disability nor familiarity with digital tools.” Only disability is faulty in this last sentence.

Each sibling `write/supplied-input.md` retains the complete source, and `write/native-sessions/` retains the approving comparison. Formal original-candidate records visibly supersede their initial F1 passes; #349-target repair remains a separate success. Second-candidate en_GB-r1 contains an observed checker repair to “functional ability” / “familiarity with digital tools”. Third-candidate original en_US is validly withheld for this class of source-support defect; `probes/third-comparison/opinion-en_US/check/input.md` repairs disability but retains “digital proficiency”, which the fresh diagnostic report mistakenly treats as equivalent. The continuation is diagnostic evidence, not a successful Write delivery.

Suggested acceptance: preserve all complete failures and superseded judgments; source comparisons distinguish measured constructs from associated traits and check exact meaning across languages; repeat unchanged original English sources with full source-blind pairs, preserving the Swedish control and warranted quantitative limitations; count valid refusal separately from delivered fidelity and track false positives; introduce no fixed synonym list or canonical article sentence. This is not #349's no-claim/absence defect and is not #341's idiomatic-expression defect.

No additional ticket is proposed for the disputed financing-stage reading, voluntary-response forecast, ordinary rhetorical concessions or initial column “på annat håll” interpretation. Their uncertainty remains in diagnostic evidence.


## Tracker attribution added after filing

The existing judgments are unchanged. The distinct observed defects now have native #329 child/blocker issues: [#358 — unnecessary changes to functioning quoted wording](https://github.com/Kntnt/skills/issues/358), [#359 — final artifact corruption across the mechanical/delivery boundary](https://github.com/Kntnt/skills/issues/359), and [#360 — translated measurement-construct substitution](https://github.com/Kntnt/skills/issues/360). The fixed-control typo belongs to #359; the unresolved Swedish idiom remains [#341](https://github.com/Kntnt/skills/issues/341). No disputed diagnostic finding is promoted to a definite defect by these links.
