# Corrected candidate Redline — web-copy

- **record** — `redline-gpt-2026-09-19-345-web-copy`
- **date** — `2026-09-19`
- **ticket** — `#345`, evaluation `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against each native rollout
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) and [protocol](../protocol.md) remain unchanged. Each invocation is a fresh native session with the same exact user prompt/material and immutable local Skills; no model/effort override is introduced. Write receives source.md alone; Redline receives the complete extracted artifact including YAML, without source material or Write commentary. Exact context, prompts, responses, traces including child sessions and full inventories are retained under runs/rerun-345; artifacts are evaluator captures. Original failures under runs/candidate and their initial records remain unchanged. Each result is judged independently before comparison, with no other provider's records read.

This record is in progress. Missing planned entries are pending, never passed. Web-copy covers three locales, explicit ABT and the extra Redline-only regression using the original missed British draft; opinion covers three locales. Side effects are established from inventories and executed commands, not the agent's own account.

## `web-copy-en_GB-regression`

- **fixture** — `web-copy-en_GB-regression`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full corrected artifact in `../editorial-329/runs/rerun-345/web-copy-en_GB-regression/final.md`; exact original faulty d60 Write artifact was the sole input.
- **side effects** — 321 created home runtime entries; one home config trust change; no work/scratch changes; isolated root removed after audit.
- **criteria** —
  - `G1` — `pass` — Service, price, scope and next action remain clear.
  - `G2` — `pass` — Detects absent inline form and changes 'form below' to 'form linked below'.
  - `P1` — `pass` — No argument or unsupported bridge added.
  - `W1` — `pass` — Link now accurately describes the actual interface.
  - `L1` — `pass` — Idiomatic en_GB retained.
  - `L2` — `pass` — en_GB mechanics loaded and preserved.
  - `T1` — `pass` — YAML none; selected genre/web craft and relevant base/language resources loaded, no technique.
  - `R1` — `pass` — One concrete mandatory UX repair; full text otherwise unchanged apart from terminal blank line.
  - `R2` — `pass` — One fresh correction fork_turns=none, child loaded all relevant base/genre/web/anti-slop/language resources, parent re-reviewed and ran exactly one final Proofread. Incoming brief text is encrypted in native evidence: complete handoff content is inferred from full corrected return and absence of child input reads, not byte-verifiable.
  - `O1` — `pass` — Full isolated-root inventory and native home effects inspected; no lasting author workspace writes.
- **unresolved findings** — `none`
- **defects filed** — #345 — reproduced miss on d60; regression now detects and fixes it.
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently. Original failure retained. Corrected response differs by 'linked' and one terminal blank line. Encrypted native correction brief limits direct handoff-content inspection; flags, reads and full result remain observable.

## Revision boundary

The #345 Redline-only regression and the already-started complete web-copy-sv pair use `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`. All remaining pairs (web-copy-en_GB, web-copy-en_US, web-copy-abt, opinion-sv, opinion-en_GB, opinion-en_US) use `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`. This changes only base review duplicate-sentence guidance and case-study review idiom guidance; Write-loaded bytes remain unchanged. Each native run retains its exact commit in run metadata.

## `web-copy-sv`

- **fixture** — `web-copy-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No changes after editorial review and Proofread. Complete unchanged artifact retained at `../editorial-329/runs/rerun-345/web-copy-sv/final.md`.
- **side effects** — 314 created native home entries and config trust entry only; root removed.
- **criteria** —
  - `G1` — `pass` — Clear board-facing service copy preserved.
  - `G2` — `pass` — Price, preparation, scope and nonbinding interest action retained.
  - `P1` — `pass` — Bounded benefits need no invented causal support.
  - `W1` — `pass` — Descriptive link and surrounding action consequences fit actual artifact.
  - `L1` — `pass` — Idiomatic Swedish retained; optional tightening not treated as mandatory finding.
  - `L2` — `pass` — Swedish mechanics checked once; no mechanical fault.
  - `T1` — `pass` — web-copy/none/sv from metadata; actual complete genre/base/web/review/anti-slop and scoped language reads.
  - `R1` — `pass` — No taste-based change; every claim, boundary and formatting preserved.
  - `R2` — `pass` — Review items5–7, no correction needed; exactly one final installed Proofread invocation item10 with flags only, shared/sv mechanics items11–12.
  - `O1` — `pass` — Response-only with complete native-root audit and cleanup.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Complete pair uses 2bd2afe; remaining pairs move to 1a4f65b. Independently judged before baseline comparison.

## `web-copy-en_GB`

- **fixture** — `web-copy-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete input copied to `../editorial-329/runs/rerun-345/web-copy-en_GB/final.md`.
- **side effects** — 316 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Board service information remains actionable.
  - `G2` — `pass` — Distinct offer, preparation, boundaries and nonbinding next step.
  - `P1` — `pass` — No unsupported internal implication.
  - `W1` — `pass` — Explicit linked form fits actual interface.
  - `L1` — `pass` — Idiomatic en_GB preserved.
  - `L2` — `pass` — Locale mechanics checked and preserved.
  - `T1` — `pass` — Metadata none; only selected genre and bounded base/web/language/review/anti-slop loaded.
  - `R1` — `pass` — Clean input kept byte for byte; no optional rewriting.
  - `R2` — `pass` — Full actual review loads items5–7; no correction; exactly one installed final Proofread item10 and shared/locale mechanics items11–12.
  - `O1` — `pass` — Complete root evidence confirms response-only effects and cleanup.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. Independent assessment before baseline comparison.

## `web-copy-en_US`

- **fixture** — `web-copy-en_US`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; exact complete artifact retained at `../editorial-329/runs/rerun-345/web-copy-en_US/final.md`.
- **side effects** — 320 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Useful service page preserved.
  - `G2` — `pass` — Offer, bounds and action consequences remain distinct.
  - `P1` — `pass` — Supported shared understanding without invented effects.
  - `W1` — `pass` — Actual linked interface and descriptive label remain correct.
  - `L1` — `pass` — Natural US English retained.
  - `L2` — `pass` — US mechanics checked with no changes.
  - `T1` — `pass` — web-copy/none/en_US; actual selected/base/review/web/anti-slop language scopes.
  - `R1` — `pass` — No mandatory finding; complete input remains unchanged.
  - `R2` — `pass` — Full review items5–6, no correction; exactly one installed Proofread item9, shared and en_US mechanics item10.
  - `O1` — `pass` — Response-only; complete inventories verify source preservation and cleanup.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. Independently assessed.

## `web-copy-abt`

- **fixture** — `web-copy-abt`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete unchanged artifact in `../editorial-329/runs/rerun-345/web-copy-abt/final.md`.
- **side effects** — 316 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Board-facing service copy preserved.
  - `G2` — `pass` — Complete price/scope/fit/action information without invented form location.
  - `P1` — `pass` — Section questions lead to bounded offered answers.
  - `W1` — `pass` — Functional headings and independent sections preserved.
  - `L1` — `pass` — Natural Swedish retained.
  - `L2` — `pass` — Swedish mechanics checked once, no changes.
  - `T1` — `pass` — Metadata web-copy/abt/sv honoured; only selected ABT contract loaded.
  - `T2` — `pass` — Actual review accepts independent reader-question arcs, without forcing global crisis or hiding early offer.
  - `R1` — `pass` — Complete input kept, no claims or voice lost.
  - `R2` — `fail` — Limited scope overread: item6 reads all genre opening definitions despite valid explicit genre metadata, where Resolution permits this discovery for inference. No unselected full genre contract or technique is loaded. Otherwise full scoped selected resources at item7 and exactly one final installed Proofread item10/shared-sv mechanics item11; no correction required.
  - `O1` — `pass` — Complete root inventory and cleanup; response-only.
- **unresolved findings** — No textual findings. Evaluator records unnecessary genre-opening discovery as a bounded-reading-path deviation; original metadata selection and final artifact remain correct.
- **defects filed** — Scope-overread observation reported to parent; tracking disposition pending.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. This observed trace deviation is separate from successful text and technique criteria, and is not the protocol's unsupported-fact/locale/mechanics/side-effect rejection.

## Tracking clarification

The web-copy-abt R2 opening-discovery deviation is [#350](https://github.com/Kntnt/skills/issues/350). The integrating parent and reviewer agree the selector instruction is already unambiguous: retain the observed failure without adding an instruction solely to fit this sample. Any replay is additional evidence, not erasure. All four pipeline cases and the exact #345 Redline regression are complete; all nine isolated roots are absent after explicit audited cleanup.
