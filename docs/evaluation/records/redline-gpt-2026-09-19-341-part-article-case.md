# Affected reruns — translated quotations and customer chronology

- **record** — `redline-gpt-2026-09-19-341-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #341 and #344, evaluation #338, part of #329
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`, verified against native turn contexts
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commits** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd` for article-en_GB; `7022c804dfbda4332723bf96b6a9857c24e63b6e` for article-en_US; `93758f485614c3b0e79b1bcce9fb8080de755d08` for the two case-study reruns. Changes across these revisions are Swedish colon variants and the base clarification that unknown/unclaimed does not mean known absent; each pair uses one immutable revision.
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

## article-en_US

- **fixture** — article-en_US, affected translation rerun
- **instruction commit** — 7022c804dfbda4332723bf96b6a9857c24e63b6e
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status, complete byte-identical input retained in `editorial-329/runs/rerun-341/article-en_US/redline/artifact.md`.
- **side effects** — No work/export/scratch changes; inventoried native home effects, authentication unchanged, root removed.
- **criteria** —
  - G1 — pass — Focused measurement explanation and reader's next investigation retained.
  - G2 — pass — Complete article opening, sectioned explanation and proportionate next step unchanged.
  - P1 — pass — Exact counts and distinct limits remain intelligible without internal contradiction.
  - W1 — pass — Clear headings and coherent paragraph sequence preserved, no scale quotas applied.
  - L1 — pass — Natural American explanation and idiomatic quotation retained.
  - L2 — pass — Shared/en_US mechanics actually read and valid forms left unchanged.
  - T1 — pass — Article/none/en_US from metadata; selected/shared pairs and three language scopes only, no technique.
  - R1 — pass — Byte-identical entire artifact; no taste repair, source request or unsupported caveat.
  - R2 — pass — Full editorial review, no correction needed; one fresh mechanical child reads installed Proofread, executes flags-only shim once and loads shared/en_US mechanics. No substantive change afterward.
  - O1 — pass — Complete inventories and transient cleanup show preserved input and no lasting Skill effect.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Both native identities confirmed in consolidated audit. Native spawn brief is encrypted; child executed instructions and no-change return are visible, rather than claimed plaintext handoff verification.

