# Opinion source-support completion verification — redline

- **date** — 2026-09-19
- **ticket** — #349, #343, #338, #329
- **skill** — redline
- **provider family** — gpt
- **model** — gpt-6-astra/high, verified in native context; no override
- **harness** — Codex CLI 0.155.1, unchanged native runner
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — d0b2c99c12a8727503b1738f1cad92611d879e1e

The frozen source, invocations and candidate prompts are unchanged. Write step6 now makes source support checked as part of writing a condition of draft completion. This is a bounded operational hypothesis after semantic guidance alone failed in all three locales; it does not authorize a separate editorial review or Proofread pass. Prior failures remain in 338/343/349 records. New independent Write→Redline sessions retain complete YAML-bearing text; Redline gets no source or delivery account. Each criterion is assessed before comparison. One sample is observed coverage, not future reliability. All writable roots, actual contract loads, native children and final installed Proofread are inspected.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete input retained at `../editorial-329/runs/rerun-349-source-check/opinion-sv/final.md`.
- **side effects** — 314 home entries plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Accountable debate voice preserved.
  - `G2` — `pass` — Early thesis/byline, evidence, genuine objection and board decision.
  - `P1` — `pass` — Internally coherent argument; source-only absence defect unknown.
  - `W1` — `pass` — Useful headings and connected paragraphs.
  - `L1` — `pass` — Idiomatic Swedish.
  - `L2` — `pass` — New Swedish mechanics scope actually checked; unchanged correct locale.
  - `T1` — `pass` — opinion/none/sv honoured in metadata and bounded actual reads.
  - `R1` — `pass` — No visible defect requiring repair; no claim removed or source verification requested.
  - `R2` — `pass` — Full review items5–6, no correction; installed Proofread exactly once item9 and shared/sv mechanics item10.
  - `O1` — `pass` — Whole-root inventory establishes response-only effects and cleanup.
- **unresolved findings** — Upstream Write #349 still present; not discoverable from this source-blind input.
- **defects filed** — No new Redline defect.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit d0b2c99. Source-check completion change belongs to Write; no extra pass occurs here.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; complete input retained at `../editorial-329/runs/rerun-349-source-check/opinion-en_GB/final.md`.
- **side effects** — 318 native home additions plus config trust; root removed.
- **criteria** —
  - `G1` — `pass` — Clear accountable opinion retained.
  - `G2` — `pass` — Thesis, attribution, real objection and committee action preserved.
  - `P1` — `pass` — Internally coherent; source-only absence defect not detectable.
  - `W1` — `pass` — Useful headings and paragraph progression.
  - `L1` — `pass` — Idiomatic en_GB unchanged.
  - `L2` — `pass` — British mechanics no-change.
  - `T1` — `pass` — opinion/none/en_GB metadata and actual selected/shared scopes agree.
  - `R1` — `pass` — No visible defect or unnecessary rewrite; no removed claims.
  - `R2` — `pass` — Full review items6–8; no correction; installed Proofread exactly once item11, shared/locale mechanics items12–13.
  - `O1` — `pass` — Full inventory and cleanup, response-only.
- **unresolved findings** — Upstream #349 remains in final pipeline; source unavailable to Redline.
- **defects filed** — No new Redline defect.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit d0b2c99. Complete artifact preserved byte for byte.
