# The commissioned GPT retest of #362

Thomas commissioned six English opinion Write runs and six repetitions of the frozen document-scope checker diagnostic, against main as it stood at staging. Product and fixtures are exactly `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`; every parent, child and judge uses observed `gpt-6.1-sol/xhigh` in native Codex CLI `0.159.3`. Historical `gpt-6-astra/high`, CLI `0.155.1` results are retained as history, not a baseline. Shared main later advanced to `fe2587b7` with #476; no trial was retargeted and no later revision is certified.

The [plan](plan.md) and judge briefs were committed in `ebd1121a` before the first counted invocation. There is no candidate change or pre-change arm. Nothing here changes shipped Skills, historical plans/records, the protected rework branch/worktree, installations, releases or remote tracker state.

## Write outcomes

`P` means pass, `F` fail, `S` skipped. Scores preserve each independent blind judge's contextual reading. F1 distinguishes the draft's fidelity from the truth of the complete delivery response.

| Sample | Article F1 | Complete response F1 | G2 | V1 digital-use variable | V2 delivered | V3 exact compared prose + residual account | V4 unknown/absent | Comparisons | Formal findings supported/false/disputed | Seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US first | F | F | P | P | P | P | P | 2 | 5/1/0 | 1821.36 |
| GB first | F | F | P | F | P | P | P | 2 | 4/1/0 | 1530.67 |
| US second | P | F | P | P | P | P | P | 2 | 1/1/0 | 1418.95 |
| GB second | P | P | P | P | P | P | P | 1 | 0/0/0 | 895.52 |
| US third | P | P | F | P | P | P | P | 2 | 5/0/0 | 1178.63 |
| GB third | P | F | P | P | P | P | P | 2 | 2/1/0 | 1992.92 |

All six also pass G1, P1, W1, L1, L2 and current-selection T1. R2 has two observed report-validation failures and four overall skips because exact checker briefings are opaque; observed loading/forks/budgets/completion/prose-freeze subchecks conform. Five O1 readings pass the evidenced Skill lifecycle; GB first skips whole-effects certification for its HOME provenance gap. T2 and R1 were not exercised. The [Write record](../../records/write-gpt-2026-10-01-362.md) gives every criterion and the [scope note](criterion-scope.md) retains the raw judges' mistaken Proofread applicability readings without rewriting them.

US first delivers four supported residual source defects. GB first's judge rejects its expressed familiarity variable; US/GB third's judges accept the same expression in their own complete texts, so that sensitivity remains explicit. US second and GB third deliver faithful articles but falsely declare accepted checker allegations to be known defects; this is a real validation/account failure. US third has a standfirst that needs the headline or lead to identify the proposed decision. No final prose is changed after comparison and every remaining allegation has its proposed repair outside the artifact.

There are eleven completed source comparisons, with seventeen supported formal findings and four false ones; two separate editorial cautions in US first are disputed. Counts describe activity. They do not make a clean report or a low finding count a quality pass. Each raw judgment inventories intermediate findings/repairs and writer dispositions.

## Document-scope diagnostic

The six complete standalone reports detect the established document/knowledge-scope error correctly **4/6** times. Repetitions 1 and 6 discuss the difference but clear it, so **2/6 miss**. The other four each raise one supported focus finding. There are no false/disputed formal findings and no other findings; a false clearance is still a D failure. Both capacity-cut-off partial detections are excluded and replaced unchanged on the same seat.

See the [component record](../../records/source-check-gpt-2026-10-01-362.md), [unchanged blind judgment](judges/p3-document-scope/captured-output.md), [neutral-label mapping](scope-label-map.json) and [scope native audit](validation/scope-native-audit.json). Report lengths are 3994–5981 whitespace words, median 5842. Checker wall time is 579.60–817.28 seconds, median 721.98. The combined native judge takes 207.90 seconds.

The one-third miss proportion matches the historical parked Claude proportion, read as a separate measurement on a different seat/revision. It does not establish that another checker would help or be worth its cost. The parked owner question therefore has a concrete current result; its local proposal measures a possible response before installing one.

## Evidence and limits

- [Write native audit](validation/write-native-audit.json) verifies all 23 parent/child/judge rollouts on the inherited seat, complete native turns and no counted Write/judge service interruption.
- The seven further counted diagnostic/judge native sessions likewise complete on that seat and frozen revision; two service voids and the capability smoke are kept separately.
- `runs/<sample>/` retains exact invocation, source, response, extracted draft, every captured Markdown/text version, actual loaded-resource/tool trace, native parent/child sessions, before/after inventories, full delta, byte comparisons and cleanup receipt.
- `judges/<sample>/` retains the identity-blind input, untouched native judgment and full judge trace/inventories. Evidence was copied into named packet directories only after blind judging.
- The [criterion disposition](acceptance-disposition.md) answers all seven original checklist items and names the uncommissioned coverage. No omitted control is implied to have passed.
- [Source provenance](source-provenance.json), [identity](identity.json), [later environment drift](validation/environment-drift.json), [validation](validation/checks.md) and reading-volume JSON retain technical facts.
- Two capacity-interrupted checker attempts are kept apart under `voided/`; their partial detections are excluded. The staging error there launched no native judge and is excluded too.
- The [transfer manifest](validation/transfer-manifest.json) verifies every scratch evidence file byte for byte in the retained packet before duplicate observation scratch is removed.

Unique core resource volume is 12,314 whitespace words, plus 188 US or 258 GB composition-guidance words. This counts each named current resource once and excludes the source; actual repeated and recovered truncated reads remain in traces. Write wall time is 14.9–33.2 minutes, median 24.6. These measurements compare no arms and establish no cause of latency.

Ruff check and format, the CONTRIBUTING mypy invocation and 2,725 pytest tests pass against the frozen product. Final documentation/tool verification and lifecycle completion are recorded with the final handoff. No authentication content or digest is published.

## Tracker handoff

Current-session [owner steering](owner-steering.md) defers all publication. Exact local comment and defect proposals live in `tracker-drafts/`. They are deliverables, not issued tickets. #362 remains open and `ready-for-human` for Thomas's decision. The completed retest does not supply whole-matrix or six-of-six quality acceptance; a supported residual allowed by #376 is separately recorded from a false assertion in the delivery account.
