# redline-gpt-2026-09-20-341-quotation-original

- **record** — `redline-gpt-2026-09-20-341-quotation-original`
- **date** — `2026-09-20`
- **ticket** — #329, #341; quotation-preservation regression
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — inherited `gpt-6-astra`, `high`, observed in all native sessions
- **harness** — Codex CLI 0.155.1
- **corpus commit** — original source `6e531f5`; third artifacts generated at `7b86144d`; selection matrix frozen at `ae24f9b3`
- **instruction commit** — `ae24f9b3`

The frozen [quotation matrix](../editorial-329/followup/matrix-quotation.md) selects every delivered third artifact containing quoted statements by people. This record covers the six original rows assigned to this evaluator: two included and four excluded. Complete artifacts and metadata are copied byte-for-byte; no source, finding or expected verdict is supplied. [Selection reasons](../editorial-329/followup/reviews/quotation-original-selection.md) and [independent judgement history](../editorial-329/followup/reviews/quotation-original-observations.md) remain visible. Other evaluators own the other third artifacts and fixed controls.

## case-study-en_US-r1

- **fixture** — complete original third-candidate `case-study-en_US-r1` Write artifact, selected for three attributed English quotations
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A short no-change status, preserving the complete input exactly; [full response](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/response.txt), [input](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/draft.md), [final](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/final.md), [account](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline-account.md).
- **side effects** — No surviving Skill files or input/installation mutation. [Before](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/inventory-before.json), [after](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/inventory-after.json), [all changed paths](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/filesystem-changes.json) and [cleanup](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/cleanup.json) cover the complete writable root. Only native `home/.codex/` state differs; authentication unchanged.
- **criteria** —
  - G1 — pass — Customer agency and supplier publication remain.
  - G2 — pass — Qualified appraisal, metric boundaries, chronology and checklist destination survive.
  - P1 — pass — No question framing, factual transition or unsupported narrative premise is introduced.
  - W1 — pass — Coherent readable structure remains.
  - L1 — pass — Final English prose is idiomatic; the original English shorthand also functioned in context.
  - L2 — pass — American English mechanics remain valid after the closing installed Proofread.
  - T1 — pass — Case-study/en_US/no-technique metadata governs the actual review and is preserved.
  - R1 — pass — The focused reader explicitly accepts the contextually intelligible English shorthand and parent preserves it; no unwarranted correction occurs.
  - R2 — pass — Full parent review scopes are visible. One fresh quotation reader reports no findings; no correction is spawned. Exactly one final installed Proofread follows, with no substantive change afterwards.
  - O1 — pass — Full-root capture shows no surviving Skill effect; all input bytes preserved and private root removed.
  - Q1 — skipped — Exact child language-guidance transport: Complete artifact and base/genre contracts are visibly read; inherited fresh identities and complete internal reports are captured. Resolved language guidance is supplied inside encrypted dispatch without a separate child language-file read, so its exact complete child access cannot be verified.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — Independent source-aware F1 passes. “Before the next building starts” is explicitly understood as trial rollout shorthand in its full context. [Reader reports](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/quotation-reports.json), [native audit](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/trace-audit.json), [full trace](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/trace.jsonl) and [identity](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r1/redline/run.json) retain every stage.

## case-study-en_US-r2

- **fixture** — complete original third-candidate `case-study-en_US-r2` Write artifact, selected for three attributed English quotations
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — A complete corrected artifact, changing only the quoted activity reference and an outer blank line; [full response](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/response.txt), [input](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/draft.md), [final](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/final.md), [account](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline-account.md).
- **side effects** — No surviving Skill files or input/installation mutation. [Before](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/inventory-before.json), [after](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/inventory-after.json), [all changed paths](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/filesystem-changes.json) and [cleanup](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/cleanup.json) cover the complete writable root. Only native `home/.codex/` state differs; authentication unchanged.
- **criteria** —
  - G1 — pass — Customer agency and supplier publication remain.
  - G2 — pass — Qualified appraisal, metric boundaries, chronology and checklist destination survive.
  - P1 — pass — No question framing, factual transition or unsupported narrative premise is introduced.
  - W1 — pass — Coherent readable structure remains.
  - L1 — pass — Final English prose is idiomatic; the original English shorthand also functioned in context.
  - L2 — pass — American English mechanics remain valid after the closing installed Proofread.
  - T1 — pass — Case-study/en_US/no-technique metadata governs the actual review and is preserved.
  - R1 — fail — The reader and parent unnecessarily replace functioning English quoted shorthand with explicit activity wording. This repair-created preservation violation remains unrecognized and unreported: an unresolved mandatory requirement to preserve authentic functioning speech. It is not classified as an invented source proposition.
  - R2 — pass — Full parent review scopes are visible. Two fresh quotation readers surround one fresh correction, with parent validation and re-review. Exactly one final installed Proofread follows, with no substantive change afterwards.
  - O1 — pass — Full-root capture shows no surviving Skill effect; all input bytes preserved and private root removed.
  - Q1 — skipped — Exact child language-guidance transport: Complete artifact and base/genre contracts are visibly read; inherited fresh identities and complete internal reports are captured. Resolved language guidance is supplied inside encrypted dispatch without a separate child language-file read, so its exact complete child access cannot be verified.
- **unresolved findings** — None reported; the unnecessary quote smoothing above is independently confirmed and remains in delivery.
- **defects filed** — Quotation-preservation regression reported to the implementation owner; no F1 invention is alleged.
- **notes** — Independent source-aware F1 passes. The only substantive change is “before the next building starts” → “before the trial starts in the next building”. The actual reader finding cites only the literal building-as-actor reading, not a concrete obstruction under ordinary contextual English. This language-specific judgement does not excuse the different Swedish calque. [Reader reports](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/quotation-reports.json), [native audit](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/trace-audit.json), [full trace](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/trace.jsonl) and [identity](../editorial-329/followup/runs/quotation-candidate/case-study-en_US-r2/redline/run.json) retain every stage.

## opinion-sv-r1 — excluded by frozen selection

- **fixture** — third original `opinion-sv-r1`
- **invocation** — not invoked; selection excludes this row
- **contextual instruction** — none
- **output target** — not reached
- **observed delivery** — none; Write withheld after a false-positive source-comparison finding; no delivered artifact.
- **side effects** — none; no fourth native invocation started for this row.
- **criteria** —
  - G1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - G2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - P1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - W1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - T1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - O1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - Q1 — skipped — Excluded by the predeclared all-artifact selection rule.
- **unresolved findings** — not applicable to an uninvoked replay.
- **defects filed** — none from this uninvoked replay.
- **notes** — Retained checked prose from a withheld Write is evidence, not a delivered artifact and not a substitute input.

## opinion-en_GB-r1 — excluded by frozen selection

- **fixture** — third original `opinion-en_GB-r1`
- **invocation** — not invoked; selection excludes this row
- **contextual instruction** — none
- **output target** — not reached
- **observed delivery** — none; The delivered artifact has no quoted statement by a person; Sanna’s position is unquoted first-person argument.
- **side effects** — none; no fourth native invocation started for this row.
- **criteria** —
  - G1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - G2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - P1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - W1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - T1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - O1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - Q1 — skipped — Excluded by the predeclared all-artifact selection rule.
- **unresolved findings** — not applicable to an uninvoked replay.
- **defects filed** — none from this uninvoked replay.
- **notes** — Retained checked prose from a withheld Write is evidence, not a delivered artifact and not a substitute input.

## opinion-en_US-r1 — excluded by frozen selection

- **fixture** — third original `opinion-en_US-r1`
- **invocation** — not invoked; selection excludes this row
- **contextual instruction** — none
- **output target** — not reached
- **observed delivery** — none; Write withheld for a valid measurement-domain finding; no delivered artifact.
- **side effects** — none; no fourth native invocation started for this row.
- **criteria** —
  - G1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - G2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - P1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - W1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - T1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - O1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - Q1 — skipped — Excluded by the predeclared all-artifact selection rule.
- **unresolved findings** — not applicable to an uninvoked replay.
- **defects filed** — none from this uninvoked replay.
- **notes** — Retained checked prose from a withheld Write is evidence, not a delivered artifact and not a substitute input.

## case-study-sv-r1 — excluded by frozen selection

- **fixture** — third original `case-study-sv-r1`
- **invocation** — not invoked; selection excludes this row
- **contextual instruction** — none
- **output target** — not reached
- **observed delivery** — none; Write withheld for a valid Swedish quotation-idiom finding; no delivered artifact.
- **side effects** — none; no fourth native invocation started for this row.
- **criteria** —
  - G1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - G2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - P1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - W1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - L2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - T1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - R2 — skipped — Excluded by the predeclared all-artifact selection rule.
  - O1 — skipped — Excluded by the predeclared all-artifact selection rule.
  - Q1 — skipped — Excluded by the predeclared all-artifact selection rule.
- **unresolved findings** — not applicable to an uninvoked replay.
- **defects filed** — none from this uninvoked replay.
- **notes** — Retained checked prose from a withheld Write is evidence, not a delivered artifact and not a substitute input.
