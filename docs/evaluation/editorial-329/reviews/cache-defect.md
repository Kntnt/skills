## What to build

Part of #329; discovered during the real baseline evaluation for #338. Make Redline's fresh correction agent preserve the same response-targeted filesystem contract as its parent. Its language-resolution command must use an isolated temporary directory and no persistent UV project/cache, with cleanup on success and failure. The parent must verify the whole scratch area after correction. This is an observed incorrect side effect, not an editorial taste rule.

Observed with instructions `8ae4c21`, corpus `6e531f5`, `gpt-6-astra` / `high`, native Codex CLI 0.155.1. Reproduce by running the matrix's article/en_GB Write on the Swedish article source, then `/redline --output=response input.md` on that full draft. The review found two issues and launched a fresh correction. In its separate native rollout, the correction agent invoked `uv run <isolated-library>/scripts/languages.py resolve --scope=composition --scope=review --scope=anti-slop en_GB` without the parent's private TMPDIR/no-cache convention. UV left its environment, PyYAML files and a lock under the declared harness scratch area. The main review later failed separately at Proofread (#339); failure does not authorise leaving the correction's files behind.

Exact local evaluation deliverables (not yet pushed):

- `docs/evaluation/editorial-329/runs/baseline/article-en_GB/redline/native-sessions/2026/09/19/rollout-2026-09-19T20-22-07-01a0bae7-7c5e-7392-8770-338e04e3660b.jsonl` — the correction's actual resolver command and tool result.
- `docs/evaluation/editorial-329/runs/baseline/article-en_GB/redline/filesystem-changes.json` and `inventory-before.json` / `inventory-after.json` — complete per-path evidence, including `scratch/tmp/uv-81b8e87d6827e8eb.lock` and the new environment below `scratch/uv-cache/environments-v2/languages-81b8e87d6827e8eb/`.
- `docs/evaluation/editorial-329/runs/baseline/article-en_GB/redline/trace.jsonl` — the parent checks only scratch's immediate child names, which cannot establish that existing cache directories remain empty.

The necessary instruction belongs in the shipped correction brief, where a fresh agent actually receives it. Do not solve this by excluding caches from evaluator inventories or silently treating agent-triggered dependency files as Harness logging. The existing candidate work for #331 may already contain the required correction; verify the final integrated behaviour before closing this defect.

## Acceptance criteria

- [ ] The correction brief gives the fresh agent the response-targeted UV isolation/cleanup contract, including the command's failure path, without relying on unseen parent history.
- [ ] A real candidate Redline run that actually performs correction leaves no new Skill-generated files anywhere in the staged writable roots, including UV caches/locks; full before/after inventories and correction trace support this.
- [ ] The baseline failure remains recorded as an incorrect side effect, even though the evaluator subsequently removes its private environment.
- [ ] The four CONTRIBUTING checks pass for the integrated change.

---
Written against 6e531f5
