# Baseline Redline — editorial #338

- **record** — `redline-gpt-2026-09-19-338-baseline`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, observed in native turn contexts
- **harness** — native Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) supplied the criteria before any editorial run. Each invocation used a fresh native session, immutable local skill copies, one staged input and no previous conversation. The complete source package was given only to Write; Redline received only the complete extracted draft, including metadata. The baseline's ordinary ABT is retained rather than overridden. Exact neutral dispatch and scratch context are captured in each run's `harness-context.md`; they add no editorial instruction. No other provider's evaluation record was consulted. Judgements below precede any candidate comparison.

Raw responses, invocation/context, inventories, exact filesystem changes, native parent/correction rollouts and cleanup evidence are under [baseline runs](../editorial-329/runs/baseline/). Harness-created caches, native sessions and trusted-project config updates are explicitly distinguished from Skill effects in each `side-effects.md`. The evaluator's artifact extraction removes only the separately identified delivery account; it does not rewrite the text. Failed runs remain.

## `article-sv`

- **fixture** — `article-sv`, complete baseline draft only
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`; neutral Harness dispatch is preserved separately.
- **output target** — `response`
- **observed delivery** — The run reviewed the article and announced no editorial findings, then returned only the nested Proofread parser error, `'---' is not a flag of this collection's grammar`; no final Text Artifact or completed no-change status was delivered. [Input](../editorial-329/runs/baseline/article-sv/redline/supplied-input.md), [response](../editorial-329/runs/baseline/article-sv/redline/response.txt).
- **side effects** — No remaining Skill-created files; source artifact, installed resources and full work/scratch are unchanged. Private UV directories were cleaned. Codex created 318 private-home entries and recorded project trust; full hashes and paths are in the run inventories and filesystem change list.
- **criteria** —
  - `G1` — `skipped` — No final reviewed artifact was delivered after the technical failure; the input's genre quality is judged in the independent Write record.
  - `G2` — `skipped` — No final artifact was delivered; the unchanged source file is not silently treated as successful output.
  - `P1` — `skipped` — Final reasoning cannot be assessed without a completed delivered artifact.
  - `W1` — `skipped` — No final artifact was delivered for web-reading assessment.
  - `L1` — `skipped` — No final artifact was delivered for idiom assessment.
  - `L2` — `skipped` — The mandatory mechanical pass never reached its language/mechanics resolution.
  - `T1` — `pass` — The recognized input map resolves article/ABT/sv; trace loads common base, article plus review, ABT plus review, anti-slop and actual Swedish composition/review/anti-slop scopes, with no competing technique.
  - `T2` — `skipped` — No final artifact was delivered; the baseline input's low-key ABT is independently judged in Write.
  - `R1` — `skipped` — The review announced no substantive findings and spent no correction budget, but its completed preservation result was never delivered because Proofread failed.
  - `R2` — `fail` — Contract failure: item_12 serializes the full YAML-bearing artifact directly after `--language=sv --output=response\n`; the nested invocation engine treats the initial `---` as a flag and exits 2. One closing pass was attempted but none completed. This is a failed invocation/delivery, not an invented textual error or a hidden repair.
  - `O1` — `pass` — Complete inventories show no model artifact or scratch left behind and no source/resource mutation; Harness-only writes are preserved explicitly.
- **unresolved findings** — No editorial finding was reported; the unresolved technical error was returned verbatim. A completed mechanical review is unavailable.
- **defects filed** — Reported to the integrating agent for a concrete follow-up issue; issue link to be added when filed.
- **notes** — This is an actual run with a failed mandatory stage, not an unrun cell or a quality pass. No final.md is fabricated from the input. Baseline instructions and prompts remain unchanged for subsequent cells.

