# redline-gpt-2026-09-20-356-presupposition-original

- **record** — `redline-gpt-2026-09-20-356-presupposition-original`
- **date** — `2026-09-20`
- **ticket** — #329, #341, #344, #349, #352, #358
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — inherited `gpt-6-astra`, `high`; observed native identity, no override
- **harness** — Codex CLI 0.155.1
- **corpus commit** — complete preceding original Write artifacts at `cd375d4f`; original sources `6e531f5`
- **instruction commit** — `cd375d4f` (Redline bytes unchanged from `3f21d9b1`)

Four fresh source-blind pairs from [matrix-presupposition](../editorial-329/followup/matrix-presupposition.md). Every staged input exactly matches its complete Write artifact and metadata; no source or evaluator judgement is supplied. Three pass applicable Redline criteria; US case fails R1 for unnecessary English quotation smoothing (#358). The Swedish case’s actual idiom repair succeeds. Source-aware final F1 is independently 3/4 because the US case retains the inherited #344 date assertion. These are different judgements. [Complete observations](../editorial-329/followup/reviews/presupposition-original-observations.md) and [all-root/native inventory](../editorial-329/followup/reviews/presupposition-original-inventory.json) retain the history.

## opinion-sv-r1

- **fixture** — original `opinion`, fresh pair `opinion-sv-r1`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — [Full response](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/final.md), [account](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline-account.md). No-change status; complete original artifact retained byte for byte.
- **side effects** — Full [before](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/inventory-before.json)/[after](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/inventory-after.json) inventories, [changed paths](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/filesystem-changes.json) and [cleanup](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/cleanup.json) retained; only native home state differs.
- **criteria** —
  - G1 — pass — Genre purpose and acting party remain intact.
  - G2 — pass — Mandatory genre work, attribution, qualifications and destination survive.
  - P1 — pass — Passage relations and quotation framing are supported; no question is invented.
  - W1 — pass — Coherent paragraphs and useful orientation remain.
  - L1 — pass — Final sv prose is idiomatic; the English issue is unnecessary voice alteration rather than remaining nonidiomatic wording.
  - L2 — pass — Valid sv mechanics are preserved by the final installed Proofread.
  - T1 — pass — Same metadata-resolved genre, language and no technique; no unselected technique applied.
  - R1 — pass — No mandatory visible defect remains and no needless correction is introduced.
  - R2 — pass — Complete selected editorial/language scopes visibly loaded; exactly one installed Proofread closes the review; no substantive change afterwards.
  - O1 — pass — Complete root inventories show no surviving Skill effects, source/installation/authentication mutation; root removed.
- **unresolved findings** — none; no independently visible outstanding defect.
- **defects filed** — none.
- **notes** — Independent source-aware F1 passes. [Exact staged input](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/supplied-input.md), [native audit](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/trace-audit.json), [complete trace](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/trace.jsonl) and [identity](../editorial-329/followup/runs/presupposition-candidate/opinion-sv-r1/redline/run.json).

## opinion-en_US-r1

- **fixture** — original `opinion`, fresh pair `opinion-en_US-r1`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — [Full response](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/final.md), [account](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline-account.md). No-change status; complete original artifact retained byte for byte.
- **side effects** — Full [before](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/inventory-before.json)/[after](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/inventory-after.json) inventories, [changed paths](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/filesystem-changes.json) and [cleanup](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/cleanup.json) retained; only native home state differs.
- **criteria** —
  - G1 — pass — Genre purpose and acting party remain intact.
  - G2 — pass — Mandatory genre work, attribution, qualifications and destination survive.
  - P1 — pass — Passage relations and quotation framing are supported; no question is invented.
  - W1 — pass — Coherent paragraphs and useful orientation remain.
  - L1 — pass — Final en_US prose is idiomatic; the English issue is unnecessary voice alteration rather than remaining nonidiomatic wording.
  - L2 — pass — Valid en_US mechanics are preserved by the final installed Proofread.
  - T1 — pass — Same metadata-resolved genre, language and no technique; no unselected technique applied.
  - R1 — pass — No mandatory visible defect remains and no needless correction is introduced.
  - R2 — pass — Complete selected editorial/language scopes visibly loaded; exactly one installed Proofread closes the review; no substantive change afterwards.
  - O1 — pass — Complete root inventories show no surviving Skill effects, source/installation/authentication mutation; root removed.
- **unresolved findings** — none; no independently visible outstanding defect.
- **defects filed** — none.
- **notes** — Independent source-aware F1 passes. [Exact staged input](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/supplied-input.md), [native audit](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/trace-audit.json), [complete trace](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/trace.jsonl) and [identity](../editorial-329/followup/runs/presupposition-candidate/opinion-en_US-r1/redline/run.json).

## case-study-en_US-r1

- **fixture** — original `case-study`, fresh pair `case-study-en_US-r1`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — [Full response](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/final.md), [account](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline-account.md). The quotation reader alleges literal building-as-actor reference; correction expands functioning English “before the next building starts”. That expansion is unnecessary and fails preservation. A separate pre-echo bridge is legitimately replaced by “Lind said:”; its claims remain in the quotation. Correction child reports both edits; final parent account mentions only the bridge.
- **side effects** — Full [before](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/inventory-before.json)/[after](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/inventory-after.json) inventories, [changed paths](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/filesystem-changes.json) and [cleanup](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/cleanup.json) retained; only native home state differs.
- **criteria** —
  - G1 — pass — Genre purpose and acting party remain intact.
  - G2 — pass — Mandatory genre work, attribution, qualifications and destination survive.
  - P1 — pass — Passage relations and quotation framing are supported; no question is invented.
  - W1 — pass — Coherent paragraphs and useful orientation remain.
  - L1 — pass — Final en_US prose is idiomatic; the English issue is unnecessary voice alteration rather than remaining nonidiomatic wording.
  - L2 — pass — Valid en_US mechanics are preserved by the final installed Proofread.
  - T1 — pass — Same metadata-resolved genre, language and no technique; no unselected technique applied.
  - R1 — fail — Unnecessary expansion of functioning English quotation changes supplied voice without a concrete language obstruction; #358.
  - R2 — pass — Complete selected editorial/language scopes visibly loaded; exactly one installed Proofread closes the review; no substantive change afterwards.
  - O1 — pass — Complete root inventories show no surviving Skill effects, source/installation/authentication mutation; root removed.
- **unresolved findings** — Independent R1 preservation failure; parent reports none. Inherited source-aware F1 failure #344 remains separate.
- **defects filed** — #358; inherited #344 independently retained.
- **notes** — Independent source-aware F1 fails for inherited September scope. [Exact staged input](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/supplied-input.md), [native audit](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/trace-audit.json), [complete trace](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/trace.jsonl) and [identity](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/run.json). [Focused reader reports](../editorial-329/followup/runs/presupposition-candidate/case-study-en_US-r1/redline/quotation-reports.json).

## case-study-sv-r1

- **fixture** — original `case-study`, fresh pair `case-study-sv-r1`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — [Full response](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/final.md), [account](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline-account.md). Only the idiom defect changes to “innan vi kommer i gång i nästa byggnad”, with no claim or distinctive voice loss. A clean corrected artifact is delivered alone, as required.
- **side effects** — Full [before](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/inventory-before.json)/[after](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/inventory-after.json) inventories, [changed paths](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/filesystem-changes.json) and [cleanup](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/cleanup.json) retained; only native home state differs.
- **criteria** —
  - G1 — pass — Genre purpose and acting party remain intact.
  - G2 — pass — Mandatory genre work, attribution, qualifications and destination survive.
  - P1 — pass — Passage relations and quotation framing are supported; no question is invented.
  - W1 — pass — Coherent paragraphs and useful orientation remain.
  - L1 — pass — Final sv prose is idiomatic; the English issue is unnecessary voice alteration rather than remaining nonidiomatic wording.
  - L2 — pass — Valid sv mechanics are preserved by the final installed Proofread.
  - T1 — pass — Same metadata-resolved genre, language and no technique; no unselected technique applied.
  - R1 — pass — No mandatory visible defect remains and no needless correction is introduced.
  - R2 — pass — Complete selected editorial/language scopes visibly loaded; exactly one installed Proofread closes the review; no substantive change afterwards.
  - O1 — pass — Complete root inventories show no surviving Skill effects, source/installation/authentication mutation; root removed.
- **unresolved findings** — none; no independently visible outstanding defect.
- **defects filed** — #341 supplied idiom repaired.
- **notes** — Independent source-aware F1 passes. [Exact staged input](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/supplied-input.md), [native audit](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/trace-audit.json), [complete trace](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/trace.jsonl) and [identity](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/run.json). [Focused reader reports](../editorial-329/followup/runs/presupposition-candidate/case-study-sv-r1/redline/quotation-reports.json).
