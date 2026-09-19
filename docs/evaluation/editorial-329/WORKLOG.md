# Implementation log — #329

Start: 2026-09-19, clean main at `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`, origin `Kntnt/skills`.
Working branch: `editorial-329`. Handoff read in full. Main survives; rework untouched.

## Mandate and sequence

Implement #330–338, independent source/technical/editorial reviews, real GPT-only evaluation, local integration and commits, then close fulfilled issues. No push, release or active global installation update. Main agent authors all resources; reviewers read only, evaluators own isolated artifacts.

Hierarchy checked: #329 has exactly #330–338, no grandchildren. Dependencies: 331→330; 332→331; 333–337→331,332; 338→333–337. Full issue bodies/comments preserved in `sources/`.

## Remaining

- Freeze source map, fixtures and matrix, independently verify (#330).
- Prepare isolated baseline/candidate installations.
- Implement shared foundation/loading, techniques, five genres (#331–337).
- Independent technical and editorial reviews; resolve findings.
- Real Write→Redline 15 combinations, techniques/controls and baseline six pairs; record complete traces and filesystem effects; blind judgement (#338).
- Final four CONTRIBUTING checks, catalog, commits/integration, issue comments/closure and cleanup.

## Decisions / observations

- Besteller's later comments govern: short editorial direction, independent judgement, advisory web dimensions, no new human gate.
- No automatic technique for the five genres, existing explicit selection precedence retained.
- Existing base/review overprescribe rhetorical devices and require unavailable source checks; rewrite together, keeping truthfulness and claim preservation.
- Native Codex CLI 0.155.1 is available; identity/access and safe isolation still to establish.
- Source auditor dispatched; source copies and audit are declared deliverables.

## Freeze checkpoint

Source auditor approved the complete map/matrix after two coverage repairs (positive instruction-selected ABT and an actual early-answer PAC report). Translated case control quotations use Swedish speech dashes. Five source packages, 11 control artifacts, 15 candidate pairs, six baseline pairs, three explicit technique pairs and seven metadata/report/excerpt controls are fixed.

First four checks: ruff/format/mypy passed; pytest 1871 passed, two documentation failures (missing corpus-index Files declaration; evaluator command's separated output flag). Both repaired and their exact tests passed. Logs retained in validation/. Native access/isolation and UV sandbox probes passed with observed gpt-6-astra/high, CLI 0.155.1. No editorial model run yet. Freeze commit follows; no shipped editorial instruction has changed.
