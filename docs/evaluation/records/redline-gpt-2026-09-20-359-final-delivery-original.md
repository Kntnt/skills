# redline-gpt-2026-09-20-359-final-delivery-original

- **record** — `redline-gpt-2026-09-20-359-final-delivery-original`
- **date** — `2026-09-20`
- **ticket** — #329, #341, #344, #352, #358, #359
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — inherited `gpt-6-astra`, `high`, observed in all native sessions
- **harness** — Codex CLI 0.155.1
- **corpus commit** — selected complete old `cd375d4f` case artifacts plus exact `7b86144d` US r2 artifact; selection hashes frozen
- **instruction commit** — `5ecadb76`

Three once-only source-blind replays declared in [matrix-final-delivery](../editorial-329/followup/matrix-final-delivery.md). [Full selection](../editorial-329/followup/reviews/final-delivery-original-selection.json) lists both excluded quote-free opinions and the included cases; Swedish fallback is not needed. Each supplied input contains only the exact complete saved artifact and metadata, with no source or judgement. Two pass applicable Redline criteria; Swedish case fails L1/R1. English quotations survive both US attempts. Full mechanical boundary passes in all three; the old US artifact’s inherited source-aware F1 failure remains separate. [Observations](../editorial-329/followup/reviews/final-delivery-original-observations.md), [inventory](../editorial-329/followup/reviews/final-delivery-original-inventory.json).

## case-study-en_US-r1

- **fixture** — exact predeclared `case-study-en_US-r1` original artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — One clean corrected artifact; only the redundant appraisal bridge becomes “Lind said:”. Both propositions remain explicit in the following quotation, so no claim is lost. [Full response](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/final.md), [account](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline-account.md), [source identity](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/source-artifact.json).
- **side effects** — [Before](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/inventory-before.json), [after](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/inventory-after.json), [all changes](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/cleanup.json). Only native state differs.
- **criteria** —
  - G1 — pass — Customer remains the acting party and supplier publication remains disclosed.
  - G2 — pass — Actual qualified customer appraisal, reservations, quantitative scope, pending expansion and document destination remain.
  - P1 — pass — No interview question is invented; quotations contribute the customer’s own experience.
  - W1 — pass — Coherent paragraphs and useful orientation preserved.
  - L1 — pass — Functioning English quotations preserved in context.
  - L2 — pass — One actual installed Proofread finds no mechanical error and retains all valid mechanics.
  - T1 — pass — Metadata resolves case-study, no technique and original locale, with no unselected technique.
  - R1 — pass — No needless correction or visible outstanding editorial defect.
  - R2 — pass — Complete scoped review followed by exactly one installed Proofread through private input and distinct output; full input/result read and exact transfer observed.
  - O1 — pass — All-root evidence shows no surviving Skill effect or source/installation/authentication mutation; root removed.
- **unresolved findings** — No visible source-blind finding. Inherited source-aware F1 failure #344 remains.
- **defects filed** — Inherited #344; #358 not reproduced.
- **notes** — Source-aware F1 fails because September still modifies supplier selection. [Mechanical audit](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/mechanical-transport-audit.json), [exact native boundary evidence](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/mechanical-transport-evidence.json), [full trace](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/trace.jsonl), [resource/identity audit](../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/redline/trace-audit.json). Mechanical-result prose and metadata match the delivered response exactly; literal bytes differ only by two outer trailing LFs, explicitly retained in the audit.

## case-study-sv-r1

- **fixture** — exact predeclared `case-study-sv-r1` original artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; complete input artifact retained byte for byte. [Full response](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/final.md), [account](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline-account.md), [source identity](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/source-artifact.json).
- **side effects** — [Before](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/inventory-before.json), [after](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/inventory-after.json), [all changes](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/cleanup.json). Only native state differs.
- **criteria** —
  - G1 — pass — Customer remains the acting party and supplier publication remains disclosed.
  - G2 — pass — Actual qualified customer appraisal, reservations, quantitative scope, pending expansion and document destination remain.
  - P1 — pass — No interview question is invented; quotations contribute the customer’s own experience.
  - W1 — pass — Coherent paragraphs and useful orientation preserved.
  - L1 — fail — Swedish calque “innan nästa byggnad kommer i gång” remains uncorrected; #341.
  - L2 — pass — One actual installed Proofread finds no mechanical error and retains all valid mechanics.
  - T1 — pass — Metadata resolves case-study, no technique and original locale, with no unselected technique.
  - R1 — fail — Parent-only review misses the concrete supplied Swedish activity-reference defect and returns no change; #341.
  - R2 — pass — Complete scoped review followed by exactly one installed Proofread through private input and distinct output; full input/result read and exact transfer observed.
  - O1 — pass — All-root evidence shows no surviving Skill effect or source/installation/authentication mutation; root removed.
- **unresolved findings** — #341 remains despite parent reporting none.
- **defects filed** — #341
- **notes** — Source-aware F1 passes. [Mechanical audit](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/mechanical-transport-audit.json), [exact native boundary evidence](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/mechanical-transport-evidence.json), [full trace](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/trace.jsonl), [resource/identity audit](../editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/redline/trace-audit.json). No-change mechanical result is written in full to its distinct file, then fully read before cleanup; retained final artifact matches exactly.

## english-preservation-control

- **fixture** — exact predeclared `english-preservation-control` original artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; complete input artifact retained byte for byte. [Full response](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/response.txt), [final artifact](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/final.md), [account](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline-account.md), [source identity](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/source-artifact.json).
- **side effects** — [Before](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/inventory-before.json), [after](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/inventory-after.json), [all changes](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/cleanup.json). Only native state differs.
- **criteria** —
  - G1 — pass — Customer remains the acting party and supplier publication remains disclosed.
  - G2 — pass — Actual qualified customer appraisal, reservations, quantitative scope, pending expansion and document destination remain.
  - P1 — pass — No interview question is invented; quotations contribute the customer’s own experience.
  - W1 — pass — Coherent paragraphs and useful orientation preserved.
  - L1 — pass — Functioning English quotations preserved in context.
  - L2 — pass — One actual installed Proofread finds no mechanical error and retains all valid mechanics.
  - T1 — pass — Metadata resolves case-study, no technique and original locale, with no unselected technique.
  - R1 — pass — No needless correction or visible outstanding editorial defect.
  - R2 — pass — Complete scoped review followed by exactly one installed Proofread through private input and distinct output; full input/result read and exact transfer observed.
  - O1 — pass — All-root evidence shows no surviving Skill effect or source/installation/authentication mutation; root removed.
- **unresolved findings** — none.
- **defects filed** — #358 not reproduced in this exact positive control.
- **notes** — Source-aware F1 passes. [Mechanical audit](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/mechanical-transport-audit.json), [exact native boundary evidence](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/mechanical-transport-evidence.json), [full trace](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/trace.jsonl), [resource/identity audit](../editorial-329/followup/runs/final-delivery-original/english-preservation-control/redline/trace-audit.json). No-change mechanical result is written in full to its distinct file, then fully read before cleanup; retained final artifact matches exactly.
