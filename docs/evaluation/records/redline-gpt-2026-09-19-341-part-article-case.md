# Affected reruns — translated quotations and customer chronology

- **record** — `redline-gpt-2026-09-19-341-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #341 and #344, evaluation #338, part of #329
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`, verified against native turn contexts
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commits** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd` for article-en_GB; `7022c804dfbda4332723bf96b6a9857c24e63b6e` for remaining pairs. Only Swedish mechanics colon variants changed between these revisions; each pair uses one immutable revision.
- **method** — Same frozen matrix and source packages, no added prompt hints. New runs preserve the earlier d60 failures. No other provider's records consulted. Chronology is already covered by Source Fidelity: an observed pass on this revision is not proof of a targeted fix or future reliability.

## article-en_GB

- **fixture** — article-en_GB, affected translation rerun
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; input retained as final in `editorial-329/runs/rerun-341/article-en_GB/redline/`.
- **side effects** — No work/export/scratch changes; scoped transient directories removed. Native home effects inventoried, authentication unchanged, evaluator root removed.
- **criteria** —
  - G1 — pass — Focused council-property explanation retained.
  - G2 — pass — Functional article parts, distinct opening and useful final next step preserved.
  - P1 — pass — Sensor/count limits remain proportionate and introduced before conclusions.
  - W1 — pass — Coherent paragraphs and informative entries retained without imposing fixed dimensions.
  - L1 — pass — Natural translated quotation and British professional voice preserved.
  - L2 — pass — Valid British spelling/typography preserved by the final mechanics pass.
  - T1 — pass — None metadata and actual no-technique loading agree.
  - R1 — pass — Byte-identical final text preserves every claim/quote and introduces no taste-based findings.
  - R2 — pass — Full scoped review followed by exactly one installed Proofread shim/shared-local mechanics load; zero unnecessary corrections and no later edit.
  - O1 — pass — Source untouched; no enduring Skill artifact across all inventories.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No translation-policy regression observed; native identity checked in consolidated audit.

