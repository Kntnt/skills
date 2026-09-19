## What to build

Part of #329, discovered in the real #338 candidate control. Clarify ownership of literal sentence/paragraph duplication at the Redline→Proofread boundary, preserving the existing narrow mechanical remit. A reviewer must not exclude an obvious editorial duplication from its one correction round on the assumption that a later mechanical pass will remove it. Preserve purposeful recurrence and do not create a blanket anti-repetition taste rule.

Observed with candidate f8cac6d, frozen corpus 6e531f5, native Codex CLI 0.155.1, gpt-6-astra/high. Invoke `/redline --genre=article --language=sv --output=response input.md` on the unchanged `controls/article-flawed.md`. The parent identifies seven editorial findings and directs its fresh correction to leave the verbatim duplicated ingress sentence for Proofread. Correction does so. A separate fresh agent then really invokes installed Proofread and returns no mechanical errors. The final text repeats “Givarna registrerade temperaturer under 20 grader i sex klassrum.” twice in the ingress; the final delivery openly acknowledges this as unresolved and its earlier classification as mistaken. Reporting is compliant, but the visible quality defect remains despite being repairable without missing facts.

Exact deliverables (local, not yet pushed):

- `docs/evaluation/editorial-329/runs/controls-genres/article-flawed/redline/response.txt` — final text and the explicit unresolved-finding account.
- `docs/evaluation/editorial-329/runs/controls-genres/article-flawed/redline/native-sessions/2026/09/19/rollout-2026-09-19T20-50-00-01a0bb01-035f-7480-ba8e-1fcaef629e27.jsonl` — fresh correction preserves the duplicate according to its supplied brief.
- The adjacent parent rollout `rollout-2026-09-19T20-47-38-01a0bafe-d7bb-7e02-b6f3-7e478d95ad17.jsonl` and closing mechanical rollout `rollout-2026-09-19T20-51-22-01a0bb02-43bb-7ae3-a4e7-59e2f30df364.jsonl` preserve the actual boundary and installed pass.
- `trace-audit.json`, complete inventories and filesystem-changes.json demonstrate same model/effort, actual resource loading and no surviving Skill files. This is independent of the resolved cache defect #340.

Investigate and change the smallest existing boundary statement needed; do not expand Proofread into substantive rewriting, silently add another correction round or modify the frozen fixture to hide the failure.

## Acceptance criteria

- [ ] An instruction change, if needed, assigns visible whole-sentence/paragraph duplication to the appropriate existing stage while retaining purposeful repetition and Proofread's mechanical limits.
- [ ] A real fresh rerun of the unchanged article-flawed control removes the duplicate, retains measured facts, exclusions, concept explanation and funding uncertainty, and reports legitimate claim removals.
- [ ] Clean article and purposeful-recurrence column controls remain valid without taste-only rewriting, with actual correction/closing-pass traces and whole-root inventories preserved.
- [ ] The original failed-quality run and honest unresolved report remain visible in the record.
- [ ] The four CONTRIBUTING checks pass for any integrated change.

---
Written against f8cac6d
