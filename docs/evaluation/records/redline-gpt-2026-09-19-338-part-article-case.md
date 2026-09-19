# Candidate evaluation: redline, article and customer case

- **record** — `redline-gpt-2026-09-19-338-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #338, part of #329
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`; each native turn context is checked below
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd`
- **method** — Frozen editorial-quality matrix; no other provider's results consulted. Every input/output is synthetic. This record is the article/case-study part of the candidate matrix, including article ABT and PAC.

## article-sv

- **fixture** — article-sv
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; final artifact is the complete supplied draft, preserved under `editorial-329/runs/candidate/article-sv/redline/`.
- **side effects** — No work/export/scratch changes; transient UV directories removed in scoped commands. Native home bootstrap/cache/session/database effects inventoried, authentication unchanged. Evaluator root cleanup recorded.
- **criteria** —
  - G1 — pass — The focused account of what four weeks of measurement establishes is retained.
  - G2 — pass — Distinct ingress and deployment lead, informative sections, conditional follow-up and no invented byline remain.
  - P1 — pass — Definition and placement explanation still precede the methodological conclusions.
  - W1 — pass — Intelligible section entries and cohesive varied paragraphs survive unchanged.
  - L1 — pass — Natural Swedish professional register is retained.
  - L2 — pass — Final Swedish mechanical pass found no errors; artifact inspection agrees.
  - T1 — pass — Article/none/sv metadata respected; actual base, genre, web-craft and three language scopes loaded, no technique resource.
  - R1 — pass — Every claim and quotation is byte-identical to the input; no taste-driven finding or unavailable-source check.
  - R2 — pass — Trace establishes full scoped review, zero unnecessary corrections and one installed Proofread invocation with mechanics scope; no edit afterwards.
  - O1 — pass — Source unchanged and no surviving Skill output in inventoried writable roots.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Native identity `gpt-6-astra/high`; no correction child was needed. Full response, trace, input/final artifact, disk evidence and cleanup remain with the case.

