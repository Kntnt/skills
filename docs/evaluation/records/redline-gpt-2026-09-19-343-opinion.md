# Corrected candidate Redline — opinion

- **record** — `redline-gpt-2026-09-19-343-opinion`
- **date** — `2026-09-19`
- **ticket** — `#343`, evaluation `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against each native rollout
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) and [protocol](../protocol.md) remain unchanged. Each invocation is a fresh native session with the same exact user prompt/material and immutable local Skills; no model/effort override is introduced. Write receives source.md alone; Redline receives the complete extracted artifact including YAML, without source material or Write commentary. Exact context, prompts, responses, traces including child sessions and full inventories are retained under runs/rerun-343; artifacts are evaluator captures. Original failures under runs/candidate and their initial records remain unchanged. Each result is judged independently before comparison, with no other provider's records read.

This record is in progress. Missing planned entries are pending, never passed. Web-copy covers three locales, explicit ABT and the extra Redline-only regression using the original missed British draft; opinion covers three locales. Side effects are established from inventories and executed commands, not the agent's own account.

## Revision boundary

The #345 Redline-only regression and the already-started complete web-copy-sv pair use `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`. All remaining pairs (web-copy-en_GB, web-copy-en_US, web-copy-abt, opinion-sv, opinion-en_GB, opinion-en_US) use `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`. This changes only base review duplicate-sentence guidance and case-study review idiom guidance; Write-loaded bytes remain unchanged. Each native run retains its exact commit in run metadata.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete unchanged artifact retained at `../editorial-329/runs/rerun-343/opinion-sv/final.md`.
- **side effects** — 320 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Clear accountable debate voice retained.
  - `G2` — `pass` — Early position, evidence, administrative objection and specific board action.
  - `P1` — `pass` — Visible source-blind reasoning remains coherent; unavailable-source absence issue is not internally disproved.
  - `W1` — `pass` — Heading sequence and coherent paragraphs preserve reading.
  - `L1` — `pass` — Idiomatic Swedish.
  - `L2` — `pass` — Final Swedish mechanics checked, no changes.
  - `T1` — `pass` — Metadata opinion/none/sv honoured; only selected full genre/base/web/review/anti-slop and language scopes.
  - `R1` — `pass` — No visible mandatory defect; no source-verification request, rewriting or removed claims.
  - `R2` — `pass` — Full review resources items6–7; no correction; installed Proofread exactly once item10 and shared/sv mechanics item11.
  - `O1` — `pass` — Full root inventory and response-only cleanup.
- **unresolved findings** — Write's source-aware F1 failure #349 remains in the pipeline artifact; it is not detectable fairly from this source-blind input.
- **defects filed** — No new Redline defect. Upstream Write defect #349 retained.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. Source-aware and source-blind judgements kept separate.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete artifact retained at `../editorial-329/runs/rerun-343/opinion-en_GB/final.md`.
- **side effects** — 318 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Accountable persuasive voice retained.
  - `G2` — `pass` — Complete early thesis/evidence/real objection/action form.
  - `P1` — `pass` — Visible argument is coherent; source-only unsupported absence cannot be inferred as false here.
  - `W1` — `pass` — Useful headings and connected paragraphs preserved.
  - `L1` — `pass` — Idiomatic en_GB.
  - `L2` — `pass` — British mechanics checked; no changes.
  - `T1` — `pass` — opinion/none/en_GB metadata matches actual bounded selected and shared resource reads.
  - `R1` — `pass` — No invented source-verification issue or taste-based change; no removed claims.
  - `R2` — `pass` — Review items5–6; no correction needed; installed Proofread exactly once item9 and shared/en_GB mechanics item10.
  - `O1` — `pass` — Whole-root inventory and cleanup establish response-only effects.
- **unresolved findings** — Upstream source-aware Write failure #349 remains; Redline has no source to detect it.
- **defects filed** — No new Redline defect; #349 remains upstream.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. Independently assessed; no source or delivery account given to Redline.

## Stage completion and next revision

The sv and en_GB pairs on 1a4f65b are complete and preserved, with Write F1 failures #349 and appropriate source-blind no-change Redline outcomes. opinion-en_US was not started on this revision. Parent requested a clarification of the existing base Claims state-of-knowledge boundary and new unchanged-source/prompt pairs in all three locales; these will have separate 349 records. Original #343 stance is fixed in both completed samples. All completed roots are absent, with the sv Write removal actor unproven as recorded above.
