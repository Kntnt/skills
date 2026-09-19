# Opinion state-of-knowledge verification — redline

- **date** — 2026-09-19
- **ticket** — #349, #343, #338, #329
- **skill** — redline
- **provider family** — gpt
- **model** — gpt-6-astra/high, verified per native turn context; no override
- **harness** — Codex CLI 0.155.1, unchanged native runner
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — 93758f485614c3b0e79b1bcce9fb8080de755d08

All three opinion locales use the exact frozen source and unchanged candidate prompts. Write and Redline are independent fresh sessions; Redline receives only the complete extracted YAML-bearing artifact, no source or delivery account. Prior 343 rerun failures under #349 remain visible in their separate records. Each criterion is assessed before baseline comparison; one sample is observed coverage, not a reliability guarantee. Full writable-root inventories, native child sessions and final installed Proofread are examined per run.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete unchanged input retained in `../editorial-329/runs/rerun-349/opinion-sv/final.md`.
- **side effects** — 316 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Accountable opinion voice maintained.
  - `G2` — `pass` — Complete thesis, evidence, real objection and named decision.
  - `P1` — `pass` — Argument internally coherent; source-only funding distinction is unknowable here.
  - `W1` — `pass` — Heading sequence and readable paragraphs retained.
  - `L1` — `pass` — Natural Swedish.
  - `L2` — `pass` — Correct Swedish mechanics retained, including revised sv scope actually loaded.
  - `T1` — `pass` — opinion/none/sv; actual correct bounded genre/base/web/language/review scopes.
  - `R1` — `pass` — No visible mandatory defect; no source-verification caveat or taste change.
  - `R2` — `pass` — Full review items5–7; no correction; exactly one installed Proofread item10 and shared/sv mechanics items11–12.
  - `O1` — `pass` — Complete inventories and literal root cleanup prove response-only effects.
- **unresolved findings** — Pipeline retains source-aware Write F1 defect #349; Redline is correctly assessed without source.
- **defects filed** — No new Redline defect; #349 remains upstream.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 93758f4. Whole artifact preserved byte for byte.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; full input retained at `../editorial-329/runs/rerun-349/opinion-en_GB/final.md`.
- **side effects** — 316 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Clear opinion voice preserved.
  - `G2` — `pass` — Thesis, attribution, genuine objection and specific board decision remain.
  - `P1` — `pass` — Internal argument coherent; hidden source distinction not testable here.
  - `W1` — `pass` — Useful headings and paragraph rhythm.
  - `L1` — `pass` — Idiomatic British English retained.
  - `L2` — `pass` — Final British mechanics no-change.
  - `T1` — `pass` — Metadata opinion/none/en_GB; actual selected/base/web/review/language scopes only.
  - `R1` — `pass` — Full artifact unchanged, no source-verification overreach or removed claim.
  - `R2` — `pass` — Review items5–7, no correction; one installed Proofread item10, shared/locale mechanics items11–12, no later edits.
  - `O1` — `pass` — Complete inventory and cleanup establish response-only effects.
- **unresolved findings** — Upstream #349 costing-absence claim remains in pipeline; Redline cannot know source mismatch.
- **defects filed** — No new Redline defect.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 93758f4. Source-aware and source-blind outcomes kept separate.

## `opinion-en_US`

- **fixture** — `opinion-en_US`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete input retained at `../editorial-329/runs/rerun-349/opinion-en_US/final.md`.
- **side effects** — 320 native home entries plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Persuasive accountable opinion remains.
  - `G2` — `pass` — Complete thesis, evidence, real objection and named board action.
  - `P1` — `pass` — Visible argument coherent; source-only absence defect unknowable here.
  - `W1` — `pass` — Functional headings and paragraphs preserved.
  - `L1` — `pass` — Idiomatic US English retained.
  - `L2` — `pass` — Final US mechanics no-change.
  - `T1` — `pass` — Metadata opinion/none/en_US matches actual selected/shared scopes; no extra genre or technique.
  - `R1` — `pass` — No visible mandatory defect or taste edit; no removed claims.
  - `R2` — `pass` — Review items5–7; no correction; installed Proofread exactly once item10 plus shared/locale mechanics items11–12.
  - `O1` — `pass` — Complete inventory and root cleanup; response-only.
- **unresolved findings** — Source-aware Write failure #349 remains in pipeline; Redline did not receive its source.
- **defects filed** — No new Redline defect.
- **notes** — Native rollout confirms gpt-6-astra/high. Entire pair uses93758f4; d0 source-check verification is separate.

## Completed 93758f4 series

All three pairs are complete, all native roots inventoried and removed. Write F1fails#349 in every locale; Redline correctly retains each internally coherent text without unseen-source verification. The knowledge-state wording clarification alone is not verified to repair this behaviour. New d0b2c99 source-support completion verification has separate 349-source-check-opinion records and rerun-349-source-check paths. No original outcome is overwritten.
