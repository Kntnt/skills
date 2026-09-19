## What to build

Part of #329; observed during baseline evaluation #338. Preserve the meaning of translated customer quotations in idiomatic target-language prose. This ticket records a concrete baseline language-quality failure, not proof that the candidate has the same defect and not a request for a new general style rule.

With instructions `8ae4c21`, corpus `6e531f5`, `gpt-6-astra` / `high` and native Codex CLI 0.155.1, `/write --genre=case-study --language=sv --output=response source.md` on the frozen English case-study source produced:

> Jag skulle avsätta den tiden innan nästa byggnad börjar

The source quotation is “I would set that time aside before the next building starts.” In context, the start concerns the trial/implementation in the next building. The Swedish sentence instead leaves “byggnad” as what starts, carrying over an English metonymic construction in a way that makes the Swedish reader reconstruct the missing activity. An idiomatic Swedish translation can preserve the same advice and qualification without implying that a building itself begins. No exact replacement wording is required.

Evidence, as local evaluation deliverables not yet pushed:

- `docs/evaluation/editorial-329/runs/baseline/case-study-sv/draft.md` — the complete observed draft.
- `docs/evaluation/editorial-329/runs/baseline/case-study-sv/write/supplied-input.md` — the complete English quotation and context.
- `docs/evaluation/editorial-329/runs/baseline/case-study-sv/write/trace.jsonl` — actual local-resource invocation and Swedish composition loading.
- `docs/evaluation/records/write-gpt-2026-09-19-338-baseline.md` — the independent L1 judgement, separate from source fidelity and Swedish mechanics.

Evaluate the candidate's corresponding cross-language case independently against the frozen L1 question before comparing this observation. If the candidate's existing instruction repairs the outcome, document that evidence without adding another rule. Only a recurring defect attributable to an unclear role, contradiction or excessive steering justifies a further instruction change. Do not demand this quotation's inclusion or one canonical Swedish sentence.

## Acceptance criteria

- [ ] Baseline evidence and its L1 failure remain visible; the outcome is not recast as mechanical misspelling or an invented fact.
- [ ] A real candidate case-study/sv run on the same English material is judged independently for native Swedish syntax/idiom and faithful quotation meaning, then compared with this observation.
- [ ] Any instruction change addresses a demonstrated cause; no new blanket rule is added merely because this single baseline wording was poor.
- [ ] The four CONTRIBUTING checks pass for the integrated change.

---
Written against 6e531f5
