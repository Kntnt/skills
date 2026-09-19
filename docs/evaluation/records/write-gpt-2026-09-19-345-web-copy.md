# Corrected candidate Write — web-copy

- **record** — `write-gpt-2026-09-19-345-web-copy`
- **date** — `2026-09-19`
- **ticket** — `#345`, evaluation `#338`, parent `#329`
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against each native rollout
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) and [protocol](../protocol.md) remain unchanged. Each invocation is a fresh native session with the same exact user prompt/material and immutable local Skills; no model/effort override is introduced. Write receives source.md alone; Redline receives the complete extracted artifact including YAML, without source material or Write commentary. Exact context, prompts, responses, traces including child sessions and full inventories are retained under runs/rerun-345; artifacts are evaluator captures. Original failures under runs/candidate and their initial records remain unchanged. Each result is judged independently before comparison, with no other provider's records read.

This record is in progress. Missing planned entries are pending, never passed. Web-copy covers three locales, explicit ABT and the extra Redline-only regression using the original missed British draft; opinion covers three locales. Side effects are established from inventories and executed commands, not the agent's own account.

## `web-copy-sv`

- **fixture** — `web-copy-sv`
- **invocation** — `/write --genre=web-copy --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete YAML-bearing artifact plus separated truthful delivery account in `../editorial-329/runs/rerun-345/web-copy-sv/write/response.txt`.
- **side effects** — 318 created home entries and one config trust entry; no work/scratch changes; root removed.
- **criteria** —
  - `F1` — `pass` — All service facts, scope, SEK 4800 VAT, exclusions, preparation and response timing preserved; no invented payment or delivery terms.
  - `G1` — `pass` — Clear service page for smaller housing-association boards; readable headings and decision-oriented explanation.
  - `G2` — `pass` — Offer, boundaries, price and contact action complete; interest not order and meeting not booked.
  - `P1` — `pass` — Benefits bounded to shared understanding and possible simplifications.
  - `W1` — `pass` — Independent entry and descriptive working destination label; no imaginary embedded form.
  - `L1` — `pass` — Natural Swedish; modest repetition of scope and simplifications supports decision but could be tightened editorially.
  - `L2` — `pass` — Swedish composition loaded; 4 800 kronor and local punctuation.
  - `T1` — `pass` — Explicit genre, default none verified in YAML and actual resource loads.
  - `R2` — `pass` — Write used composition/base/genre/web craft only; stopped at one first draft.
  - `O1` — `pass` — Response delivery; full filesystem inventory verifies no surviving work/scratch output.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## Revision boundary

The #345 Redline-only regression and the already-started complete web-copy-sv pair use `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`. All remaining pairs (web-copy-en_GB, web-copy-en_US, web-copy-abt, opinion-sv, opinion-en_GB, opinion-en_US) use `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`. This changes only base review duplicate-sentence guidance and case-study review idiom guidance; Write-loaded bytes remain unchanged. Each native run retains its exact commit in run metadata.

## `web-copy-en_GB`

- **fixture** — `web-copy-en_GB`
- **invocation** — `/write --genre=web-copy --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete YAML-bearing artifact and distinct account in `../editorial-329/runs/rerun-345/web-copy-en_GB/write/response.txt`.
- **side effects** — 316 created home entries and one config trust entry; root removed.
- **criteria** —
  - `F1` — `pass` — Scope, 45 minutes, two representatives, written output, SEK price/VAT, exclusions and three-day response preserved without guarantees or extra terms.
  - `G1` — `pass` — Board reader learns offer, preparation, limitations and action through distinct useful headings.
  - `G2` — `pass` — Complete service page with explicit non-order and non-booking consequences.
  - `P1` — `pass` — Shared picture and two possible simplifications proportionate to service.
  - `W1` — `pass` — 'Use the linked form' accurately matches actual link; headings support independent entry.
  - `L1` — `pass` — Natural British English, e.g. 'take stock of those arrangements'; no source-language syntax.
  - `L2` — `pass` — British locale composition and unconverted SEK 4,800.
  - `T1` — `pass` — Metadata web-copy/none/en_GB; actual selected genre/base/web craft and composition only.
  - `R2` — `pass` — Installed Write invocation, no review resources or extra passes.
  - `O1` — `pass` — Response output and full root inventory demonstrate no surviving Skill files.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd. Independently assessed; original #345 failure preserved.

## `web-copy-en_US`

- **fixture** — `web-copy-en_US`
- **invocation** — `/write --genre=web-copy --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full YAML-bearing artifact and distinct account in `../editorial-329/runs/rerun-345/web-copy-en_US/write/response.txt`.
- **side effects** — 320 created home entries plus config trust; root removed.
- **criteria** —
  - `F1` — `pass` — Service facts, fixed SEK/VAT, scope, preparation, exclusions and business-day response stay within source; no invented payment terms or guarantees.
  - `G1` — `pass` — Board reader sees fit, concrete deliverables, cost and next step.
  - `G2` — `pass` — Complete service page with explicit non-order/non-booking consequences.
  - `P1` — `pass` — Shared reference point is proportionate to written summary; no promised operational result.
  - `W1` — `pass` — Local headings orient; 'linked form' accurately represents destination.
  - `L1` — `pass` — Natural US English; light repetition of simplifications is functional but optional editing could reduce it.
  - `L2` — `pass` — Serial commas and business days; SEK 4,800 remains correct without conversion.
  - `T1` — `pass` — web-copy/none/en_US, selected genre/base/web craft and composition only.
  - `R2` — `pass` — One installed Write draft; no review or proofreading pass.
  - `O1` — `pass` — Response-only and exact root inventory; all isolated state removed.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. Independent assessment before baseline comparison.

## `web-copy-abt`

- **fixture** — `web-copy-abt`
- **invocation** — `/write --genre=web-copy --technique=abt --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full artifact within outer Markdown presentation fence and separate account; extracted exactly inside fence to `../editorial-329/runs/rerun-345/web-copy-abt/artifact.md`.
- **side effects** — 318 native home entries plus config trust; root removed.
- **criteria** —
  - `F1` — `pass` — Price, scope, meeting, written deliverable, exclusions, preparation and nonbinding interest kept. Unspecified payment/delivery timing stays unspecified rather than invented.
  - `G1` — `pass` — Service page answers board reader's fit, process, scope and next-step questions.
  - `G2` — `pass` — Complete useful service copy with clear limited outcome and action.
  - `P1` — `pass` — Existing rules lead to questions about steps/uncertainties and bounded review; excluded services correctly limit fit.
  - `W1` — `pass` — Useful section entries and descriptive interest link, with no claim of a form physically below.
  - `L1` — `pass` — Idiomatic Swedish; 'från befintliga regler till möjliga förenklingar' establishes a natural progression.
  - `L2` — `pass` — Swedish spacing/currency and punctuation; composition resolved as sv.
  - `T1` — `pass` — Explicit flag ABT matches YAML and actual abt.md load; no other technique or review half.
  - `T2` — `pass` — Section-level arcs: existing routines → questions/uncertainties → meeting/summary; fit uncertainty → interest → promised response. No global crisis or hidden answer.
  - `R2` — `pass` — Actual scoped Write loads and one draft; no reviewer pass.
  - `O1` — `pass` — Complete response artifact; presentation fence extraction documented; no enduring Skill files.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. The extra sentence stating absent payment/delivery terms is editorially optional and could live solely in the delivery account; it does not assert invented terms or guarantee a later outcome. Independently judged before paired output.
