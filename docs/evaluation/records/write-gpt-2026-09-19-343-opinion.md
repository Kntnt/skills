# Corrected candidate Write — opinion

- **record** — `write-gpt-2026-09-19-343-opinion`
- **date** — `2026-09-19`
- **ticket** — `#343`, evaluation `#338`, parent `#329`
- **skill** — `write`
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
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full YAML-bearing artifact and separated delivery account in `../editorial-329/runs/rerun-343/opinion-sv/write/response.txt`.
- **side effects** — Complete inventory: 318 native home entries created, one config trust change, no work/scratch change; auth unchanged. Root already absent at evaluator's explicit cleanup attempt; removal attribution pending, all evidence preserved.
- **criteria** —
  - `F1` — `fail` — Source “gör inget anspråk på att ha finansierat eller kostnadsberäknat” becomes categorical “Vi har varken kostnadsberäknat eller finansierat försöket.” Withholding a claim does not establish absence of work. Other figures, limits and the #343 non-opposition stance survive.
  - `G1` — `pass` — Clear accountable debate article for Lervik residents; sharp supported argument.
  - `G2` — `pass` — Early thesis, report attribution, real double-administration objection and named board action; cost decision remains.
  - `P1` — `pass` — Booking/people distinction and missing savings evidence lead to the bounded trial; unsupported external absence scored F1.
  - `W1` — `pass` — Functional evidence/objection/proposal headings and coherent paragraphs.
  - `L1` — `pass` — Idiomatic Swedish, preserving sharpness without motives.
  - `L2` — `pass` — Swedish date, compounds, punctuation and numerals.
  - `T1` — `pass` — Explicit opinion, metadata none/sv; selected genre/base/web/composition loads only. Quotation guidance read while considering the supplied speech.
  - `R2` — `pass` — Actual installed Write; composition resources only, one first draft, no review pass.
  - `O1` — `pass` — Native complete root inventories prove response-only output and source/resource preservation; root absent after audit, with removal actor pending.
- **unresolved findings** — Source-aware F1 failure remains; Redline receives no source and cannot fairly detect this distinction.
- **defects filed** — [#349](https://github.com/Kntnt/skills/issues/349); complete body in `../editorial-329/defects/opinion-unsupported-absence.md`.
- **notes** — Instruction commit `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`; native gpt-6-astra/high. Independently assessed before Redline output. #343 stance is fixed in this sample; new absence claim remains separately visible.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/write --genre=opinion --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full YAML-bearing artifact and separated account in `../editorial-329/runs/rerun-343/opinion-en_GB/write/response.txt`.
- **side effects** — 314 home entries plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — 'Öppna beslut has neither funded nor costed this proposal' repeats #349: absence of a source claim becomes asserted absence of work. 'I do not oppose digital booking' correctly preserves #343 stance. All counts/denominator/limits retained.
  - `G1` — `pass` — Sharp accountable opinion for residents; 'So must a proposal to abolish it' preserves force without motives.
  - `G2` — `pass` — Early thesis, named author, attributed evidence, genuine administration objection and specific committee action/cost decision.
  - `P1` — `pass` — Evidence limits lead to measured trial and later choice; source-only unsupported absence scored F1.
  - `W1` — `pass` — Informative headings and coherent argument paragraphs.
  - `L1` — `pass` — Idiomatic British English; 'costed', 'centre' and natural argumentative syntax.
  - `L2` — `pass` — British date/orthography and unchanged figures.
  - `T1` — `pass` — opinion/none/en_GB metadata matches actual selected genre/base/web/composition loads.
  - `R2` — `pass` — Installed Write, one draft, no review halves; quotation guidance consulted for supplied speech.
  - `O1` — `pass` — Complete root inventory and cleanup; response-only output.
- **unresolved findings** — Source-fidelity failure #349 remains in artifact; no source supplied to paired Redline.
- **defects filed** — #349 repeats in en_GB. #343 original stance issue fixed in this sample.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit 1a4f65b. Assessed independently before paired output.

## Cleanup attribution clarification

For opinion-sv, the registered native root was already absent at the evaluator's explicit literal-path removal attempt. Parent likewise observed a completed root disappear, but neither agent performed a global cleanup. An automatic completed-session cleanup hook is plausible, not proven. Complete inventories/native captures preceded disappearance; no evidence was lost. This is not falsely credited as evaluator manual removal.

## Stage completion and next revision

The sv and en_GB pairs on 1a4f65b are complete and preserved, with Write F1 failures #349 and appropriate source-blind no-change Redline outcomes. opinion-en_US was not started on this revision. Parent requested a clarification of the existing base Claims state-of-knowledge boundary and new unchanged-source/prompt pairs in all three locales; these will have separate 349 records. Original #343 stance is fixed in both completed samples. All completed roots are absent, with the sv Write removal actor unproven as recorded above.

## Cleanup attribution resolved

The prior uncertain attribution for opinion-sv is now resolved by `../editorial-329/reviews/automatic-cleanup-events.json`: the global session-cleanup start hook deleted the registered oc0bvl8y root at2026-09-19T19:11:05+00:00. This supersedes the earlier unproven-actor note. Complete inventories and native captures predated deletion; no evidence was lost and no evaluator manual deletion is claimed.
