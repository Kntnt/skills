# Finalisation of the completed GPT retest — #362

This additive handoff records progress against the 2026-10-02 Agent Brief. The commissioned experiment was already complete. No product trial, judge, repair, criterion change or historical rewrite was performed here. The builder's base is `5b0260283b1d1597ca1ed2dddc602888dac7119d`; the measured product remains `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`, native Codex CLI 0.159.3, `gpt-6.1-sol/xhigh`. This packet certifies no later main revision.

## Evidence transfer

The read-only source is `/Users/thomas/Projects/skills-eval-362-gpt-20261001`, branch `eval/362-gpt-20261001`, observed head `27061b27037f3ea215ed2619a189c8aa4f1565a2`. Its head was insufficient: 11 selected files were committed, one evaluator file had uncommitted modifications, and 618 final deliverables were untracked. All 630 files (55,473,412 bytes) were copied byte for byte, including the full packet, evaluator captures/helpers and both records. Nothing was committed, cleaned, reset or written in the source worktree.

- [Pre-transfer inventory](source-inventory.json) records every selected file's size/hash and the source's full Git status before copying.
- [Attribution](attribution.json) separates committed files, the modified evaluator and untracked deliverables. Files outside the packet and two named records were excluded. The source's shared index change is supplied to the run through `.kntnt-orchestrate/362.md`, preserving sibling entries.
- [Credential scan](credential-scan.json) found no authentication filenames or literal token candidates in the selected files. No authentication content or authentication digest was copied. References to authentication paths in evaluator code and provenance remain references.
- [Preservation receipt](preservation.json) checks the unchanged source head, status and selected bytes after finalisation, the untouched protected source and the absence of historical/product changes in this branch.

The [historical packet](../gpt-retest-2026-10-01/README.md), [Write record](../../records/write-gpt-2026-10-01-362.md) and [component record](../../records/source-check-gpt-2026-10-01-362.md) remain exactly as supplied. Their older publication/closure recommendations describe the previous session. They are superseded for this task by the issue's 06:37 Agent Brief and 09:47 owner clarification, retained in the [tracker snapshot](ownership-snapshot.json): publish the result comment; keep new proposals local; let Orchestrate decide closure only after independent verification. The builder closes nothing.

## Audit and actual outcome

[audit.py](audit.py) is a read-only command: `python3 docs/evaluation/editorial-362/finalisation-2026-10-02/audit.py`. Its [receipt](native-audit.json) verifies 577 original scratch-transfer hashes, every counted captured-file hash, 30 counted native sessions, the inherited seat/CLI/revision, native completion, and the retained cleanup receipts. These comprise six Write parents, eleven comparison children, six standalone diagnostics and seven judges. Two capacity-interrupted diagnostics and one unlaunched judge staging error remain separate under `voided/`; the capability smoke is not counted. No attempt was selectively rerun here.

For each Write row the audit independently extracts the fenced artifact, finds matching captured draft bytes and finds the exact delivered prose in the final comparison child's actual returned tool output. It does not infer identity from a writer's claim or a matching earlier draft. Comparison counts in commissioned order US1, GB1, US2, GB2, US3, GB3 are 2, 2, 2, 1, 2, 2. Report revisions and appended dispositions are versions of those eleven comparisons, not additional comparisons.

The six raw semantic judgments remain literal in the audit receipt. The supplied records correctly separate article F1 from full-response F1, true defects from false allegations, disputed editorial cautions, and skipped evidence from product failures. Their outcomes are:

| Commissioned measurement | Preserved outcome |
| --- | --- |
| V1: measured digital-use variable, actually expressed | 5/6 raw passes; GB1 fails. US3 and GB3 accept the same familiarity expression in their respective contexts. No universal synonym ruling follows. |
| V2: draft delivered | 6/6 pass. |
| V3: last-compared prose and residual accounting | 6/6 pass. Accurate carry-forward does not make an allegation true. |
| V4: unknown versus absent | 6/6 pass. |
| F1 / G2 / L1 | Article F1 4/6, complete-response F1 2/6, G2 5/6, L1 6/6. |
| X: findings/dispositions | 17 supported, 4 false, 0 disputed formal finding events; two separate disputed cautions. Two false findings are rejected, two accepted and stated as known defects. Captured versions are retained without inflating distinct finding counts. |
| D: document scope | 4/6 detections; repetitions 1 and 6 discuss then clear the established shift. Neither is a detection. No false/disputed formal finding or other finding. |
| R2 / O1 limits | Two observed validation failures; four overall R2 skips because exact dispatched briefings are opaque. GB1 O1 is skipped for HOME provenance, without proving an incorrect Skill side effect. |

The [scope disposition](../gpt-retest-2026-10-01/criterion-scope.md) preserves the raw judges' mistaken application of Redline's final Proofread duty to Write. No absent Proofread pass is counted as a Write defect or converted into an observed pass. T2, R1, new Redline pairs, stop/dependency behaviour, Swedish opinion/column, chronology/person negatives and a fresh baseline arm were not commissioned. [Original checklist disposition](../gpt-retest-2026-10-01/acceptance-disposition.md) retains every omission and failure. Completion of this bounded retest is not full editorial acceptance.

[Contracts and reading checks](contracts-and-reads.json) verify that the plan and both judge briefs still match `ebd1121a` and reconstruct 12,314 unique core whitespace words from the measured revision. All ten named core files are byte-identical at the builder base; this is no evaluation of later main. The existing locale measurement adds 188 US or 258 GB composition words. Exact contiguous-output matching is deliberately conservative: segmented, scoped and truncated/recovered reads need their trace, and unmatched whole files are not reported as unread. The preserved blind judges assessed actual loading and retain the remaining opaque briefing gaps.

Write wall time is 895.52–1992.92 seconds, median 1474.81; scope reports take 579.60–817.28 seconds, median 721.98, and contain 3994–5981 whitespace words. Historical fractions and timings use different seats/revisions and supply no causal comparison. Equal one-third scope miss fractions do not establish an extra checker's benefit or cost.

## Residual delivery and verification

[Residual mapping](residuals.md) audits current contracts and open/closed ownership. The two self-contained [false-allegation](followups/false-known-defect.md) and [standfirst](followups/standfirst.md) briefs remain local proposals. The source's [document-scope proposal](../gpt-retest-2026-10-01/tracker-drafts/document-scope.md) remains parked for Thomas; no repair or extra comparison is commissioned. Duplicates, supported disclosed residuals, semantic sensitivity and unestablished method allegations remain separate.

[Result comment](result-comment.md) answers the narrowed commissioning criteria and the seven original checklist items. Its publication receipt is [published-comment.json](published-comment.json). Only that authorised result comment is published; no new issue, closure, label, push, release or global installation is performed by this builder.

[Verification](verification.md) records both observed red steps, the green preservation/native-audit tests, and all four unchanged CONTRIBUTING commands on the integrated evidence. **Finalisation is incomplete:** three existing scheduler tests fail when pytest's temporary roots are confined to the permitted scratch directory inside the real account's home. Their fixtures expect a temporary root outside that home, while both authorised write roots are inside it. No product/test fixture was changed and no outside-root temporary writes were authorised. Complete gate outputs/process receipts are retained beside it. [Cleanup](cleanup.json) records the builder's own processes and removed scratch/cache paths. The source worktree, source branch and all historical handoffs remain deliverables. The enclosing run must settle this verification-environment conflict before acceptance or closure.

| Latest Agent Brief criterion | Builder disposition |
| --- | --- |
| 1. Preserve source and integrate attributable additive deliverables | Prepared: all 630 files preserved; one local delivery commit; index append isolated in the run's note. |
| 2. Audit actual attempts, artifacts, dispositions, judgments, measurements and receipts | Fulfilled as an evidence audit; failures, disputed readings, voids and skips remain distinct. |
| 3. Publish narrowed result with original omissions/failures | Published as the linked result comment, including the current gate blocker rather than a completion claim. |
| 4. Durable residual mapping and reviewed local briefs; scope question parked | Prepared; no new defect published or parked study commissioned. |
| 5. No fresh trial/product/criterion/history/ADR change or prohibited publication | Observed; builder performs no closure or other prohibited external action. |
| 6. Four project checks and cleanup receipts | Not fulfilled: final Ruff, format and mypy pass; final suite has 2,729 passes and three environment-dependent scheduler failures. Cleanup completed. |
