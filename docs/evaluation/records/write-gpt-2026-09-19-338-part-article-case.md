# Candidate evaluation: write, article and customer case

- **record** — `write-gpt-2026-09-19-338-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #338, part of #329
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`; each native turn context is checked below
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd`
- **method** — Frozen editorial-quality matrix; no other provider's results consulted. Every input/output is synthetic. This record is the article/case-study part of the candidate matrix, including article ABT and PAC.

## article-sv

- **fixture** — article-sv
- **invocation** — `/write --genre=article --language=sv --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete Swedish article, metadata `article/none/sv`, followed by a separate delivery account; preserved in `editorial-329/runs/candidate/article-sv/write/`.
- **side effects** — No work/export/scratch changes survived. Temporary UV directories were scoped and removed in the executed commands. Private home additions were native bootstrap/plugin caches, sessions and databases; config changed through Harness bootstrap. Authentication unchanged. Full inventories retained; evaluator removed the private root after capture (`cleanup.json`).
- **criteria** —
  - F1 — pass — The article retains 14/120 sessions, local 20-degree threshold, placement limits, unmeasured causes/comfort, and undecided funding; no count-size or causal inference added.
  - G1 — pass — The angle “vad … lektionspass berättar” serves property managers deciding what a short measurement can establish.
  - G2 — pass — Informative H1, distinct ingress, January deployment lead before H2, no invented byline, explanatory sections and a qualified next investigation.
  - P1 — pass — Sensor locality and operative temperature are explained before the limits are drawn; time-series meaning is supplied inline.
  - W1 — pass — Three informative sections separate counts, measurement scope and next steps; ingress gives the limits while the lead begins the actual deployment.
  - L1 — pass — Natural Swedish such as “ringat in tillfällen att följa upp” supports a measured professional explanation.
  - L2 — pass — Swedish date, speech dash and number/unit forms; no imported locale convention observed.
  - T1 — pass — Metadata says none; trace loads article, base, web-craft and only Swedish composition, no technique.
  - R2 — pass — Native trace reads Write SKILL, invocation shim, delivery, quotations and bounded writing resources; no review or proofreading pass.
  - O1 — pass — Supplied source unchanged; no surviving Skill artifacts in any writable root. Inventory and trace support the account.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Exact native turn context confirms `gpt-6-astra/high`. This draft was judged against its source and the frozen criteria before examining its Redline result.

## article-en_GB

- **fixture** — article-en_GB
- **invocation** — `/write --genre=article --language=en_GB --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full British English article and separate delivery account, preserved in `editorial-329/runs/candidate/article-en_GB/write/`.
- **side effects** — No work/export/scratch changes survived; scoped UV temporary directories removed. Private-home native bootstrap/cache/database/session effects retained in inventories; authentication unchanged. Evaluator cleaned the root after capture.
- **criteria** —
  - F1 — pass — Retains 14/120, the non-legal threshold, no duration/comfort findings, non-experimental placement and undecided funding; the quote translation preserves uncertainty.
  - G1 — pass — “A reading below 20°C is only part of the picture” carries a practical measurement-limits angle for property managers.
  - G2 — pass — Standalone ingress, January deployment lead, informative H2 sections and Rask’s qualified next step perform distinct jobs; no invented byline.
  - P1 — pass — The text explains the combined air/radiant measure before naming operative temperature and keeps placement distinct from perceived comfort.
  - W1 — pass — Three coherent sections support entry at counts, measurement limits or actions without duplicating the whole opening.
  - L1 — pass — “keep attention on the time that matters to the enquiry” and “take a closer look” are idiomatic British explanation, without Swedish syntax.
  - L2 — pass — British enquiry, draughts, caretaker, 12 March date and single-quote convention used consistently.
  - T1 — pass — Metadata article/none/en_GB; trace loads only article/base/web-craft and British composition, no technique.
  - R2 — pass — Actual reads include Write SKILL, shim, delivery and quotations; no review resources or peer pass.
  - O1 — pass — Input preserved, no surviving Skill files; full root inventories and executed cleanup support this.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Source-to-English transformation judged independently before its Redline result; native identity is checked with the consolidated trace audit.

