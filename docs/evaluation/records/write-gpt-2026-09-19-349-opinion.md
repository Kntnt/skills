# Opinion state-of-knowledge verification — write

- **date** — 2026-09-19
- **ticket** — #349, #343, #338, #329
- **skill** — write
- **provider family** — gpt
- **model** — gpt-6-astra/high, verified per native turn context; no override
- **harness** — Codex CLI 0.155.1, unchanged native runner
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — 93758f485614c3b0e79b1bcce9fb8080de755d08

All three opinion locales use the exact frozen source and unchanged candidate prompts. Write and Redline are independent fresh sessions; Redline receives only the complete extracted YAML-bearing artifact, no source or delivery account. Prior 343 rerun failures under #349 remain visible in their separate records. Each criterion is assessed before baseline comparison; one sample is observed coverage, not a reliability guarantee. Full writable-root inventories, native child sessions and final installed Proofread are examined per run.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full YAML-bearing draft and distinct delivery account in `../editorial-329/runs/rerun-349/opinion-sv/write/response.txt`.
- **side effects** — 316 native home additions plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — Repeats 'Vi har varken kostnadsberäknat eller finansierat försöket' although source only disclaims an assertion of funding/costing. #349 persists after new state-of-knowledge sentence was actually loaded. Other figures, denominator and non-opposition stance preserved.
  - `G1` — `pass` — Accountable, pointed local debate article.
  - `G2` — `pass` — Early thesis and author, attributed pilot, real administration objection, six-month proposal and board cost decision.
  - `P1` — `pass` — Evidence limits and administration cost lead to bounded trial; source-only absence defect scored F1.
  - `W1` — `pass` — Headings and paragraphs orient; modest recurrence of booking/ability distinction supports emphasis.
  - `L1` — `pass` — Natural Swedish argumentative syntax.
  - `L2` — `pass` — Swedish date and punctuation conventions.
  - `T1` — `pass` — opinion/none/sv correctly resolved and recorded; actual selected/base/web/composition loads.
  - `R2` — `pass` — Updated base Claims actually read item5, installed Write one draft; quotation guidance consulted; no review half.
  - `O1` — `pass` — Complete root inventory proves response-only effects and source preservation; cleanup complete.
- **unresolved findings** — #349 source fidelity remains a mandatory Write failure on revised instructions.
- **defects filed** — #349 — repeated after clarification, not verified repaired.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 93758f485614c3b0e79b1bcce9fb8080de755d08. Independent assessment; no source to Redline, no change to fixture or prompt.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/write --genre=opinion --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete YAML-bearing artifact and separate account in `../editorial-329/runs/rerun-349/opinion-en_GB/write/response.txt`.
- **side effects** — 318 native home additions plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — 'Öppna beslut has neither costed the trial nor claimed to have funded it' preserves unclaimed funding but still asserts unperformed costing. Both source statuses were merely unclaimed. #349 partially persists; #343 non-opposition and all report figures/limits remain correct.
  - `G1` — `pass` — Clear accountable debate voice; criticism of evidence remains sharp.
  - `G2` — `pass` — Early proposal/byline, attributed counts, real administrative objection and board action/cost decision.
  - `P1` — `pass` — Questions about staff time and user reasons justify measured trial; hidden-source absence scored F1.
  - `W1` — `pass` — Orienting section headings and coherent argument.
  - `L1` — `pass` — Natural British English, e.g. 'identifies a burden without establishing its size'.
  - `L2` — `pass` — British spelling/date and punctuation.
  - `T1` — `pass` — opinion/none/en_GB and actual correct selected/shared composition resources.
  - `R2` — `pass` — Revised base Claims actually read; installed Write one draft, no review half.
  - `O1` — `pass` — Complete root inventory and cleanup; response-only.
- **unresolved findings** — #349 unsupported absence of costing remains. Funding's no-claim status now retained.
- **defects filed** — #349 remains after clarification.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 93758f4. The faulty sentence is third person, limiting any explanation attributing the failure solely to first-person grammar. Assessed independently before Redline.

## `opinion-en_US`

- **fixture** — `opinion-en_US`
- **invocation** — `/write --genre=opinion --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete YAML-bearing draft with separate account in `../editorial-329/runs/rerun-349/opinion-en_US/write/response.txt`.
- **side effects** — 316 native home entries plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — 'Our association has neither costed nor funded this proposal' converts unclaimed work into asserted absence, repeating #349 in en_US. Figures, pilot limits, cost responsibility and non-opposition otherwise retained.
  - `G1` — `pass` — Sharp accountable debate article for local residents.
  - `G2` — `pass` — Early thesis/byline, report attribution, genuine objection and board action preserve complete form.
  - `P1` — `pass` — Booking denominator and missing administrative evidence support proposed trial; external no-claim mismatch scored F1.
  - `W1` — `pass` — Useful headings and coherent argument paragraphs.
  - `L1` — `pass` — Idiomatic US English; 'costed' is less usual in US usage but intelligible professional language, not a hard dialect defect.
  - `L2` — `pass` — American dates, authorize, tradeoff, serial commas.
  - `T1` — `pass` — opinion/none/en_US and scoped actual genre/base/web/composition reads.
  - `R2` — `pass` — Installed Write one draft, new base Claims actually read; no review half or second pass.
  - `O1` — `pass` — Complete root evidence and cleanup; response-only.
- **unresolved findings** — #349 remains in all three locale samples on 93758f4.
- **defects filed** — #349 — en_US recurrence.
- **notes** — Native rollout confirms gpt-6-astra/high. This pair began before d0b2c99 was supplied and stays wholly on93758f4. New source-check stage verification will use separate paths/records.
