# Records

One file per evaluation, named `<skill>-<provider-family>-<YYYY-MM-DD>.md`, written from [`../record-template.md`](../record-template.md) in the format [`../protocol.md`](../protocol.md) defines.

A record holds one provider family. Two families are compared by reading their two records side by side, which is the whole reason the format is fixed: the comparison costs a read rather than a re-run, and it can be made long after either session has ended.

A re-run is a new record rather than an edit to an old one. What a configuration did on a given day is history, and a later repair does not change it.

Where a re-run lands on the same date as the record it follows, the name takes the issue it was run for after the date, because the convention above has nowhere else to put two records of one Skill and one family on one day.

- [`proofread-claude-2026-08-25.md`](proofread-claude-2026-08-25.md) — the Proofread Skill against the corpus at `e2e162c`, in Claude Code on `claude-opus-5`, for issue #107.
- [`write-claude-2026-08-25.md`](write-claude-2026-08-25.md) — the Write Skill against the corpus at `059e8bc`, in Claude Code on `claude-opus-5`, for issue #108.
- [`redline-claude-2026-08-25.md`](redline-claude-2026-08-25.md) — the Redline Skill against the corpus at `6d476db`, in Claude Code on `claude-opus-5`, for issue #109.
- [`write-claude-2026-08-25-138.md`](write-claude-2026-08-25-138.md) — the two briefs that state a length their material cannot fill, re-run against the Write Skill as issue #138 changed it, at the corpus commit `c922071`, in Claude Code on `claude-opus-5`.
- [`unslop-claude-2026-08-25.md`](unslop-claude-2026-08-25.md) — the Unslop Skill against the corpus at `26155fd`, in Claude Code on `claude-opus-5`, for issue #111.
- [`proofread-gpt-2026-08-26.md`](proofread-gpt-2026-08-26.md) — the Proofread Skill against the corpus at `46ba9c1`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, for issue #155.
- [`write-gpt-2026-08-26.md`](write-gpt-2026-08-26.md) — the Write Skill against the corpus at `46ba9c1`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, for issue #157.
- [`proofread-claude-2026-08-26.md`](proofread-claude-2026-08-26.md) — the Proofread Skill against the corpus at `46ba9c1`, in Claude Code on `claude-opus-5`, for issue #156.
- [`write-claude-2026-08-26.md`](write-claude-2026-08-26.md) — the Write Skill against the corpus at `46ba9c1`, in Claude Code on `claude-opus-5`, for issue #158.
- [`redline-gpt-2026-08-26.md`](redline-gpt-2026-08-26.md) — the Redline Skill against the corpus at `46ba9c1`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, for issue #159.
- [`unslop-gpt-2026-08-26.md`](unslop-gpt-2026-08-26.md) — the Unslop Skill against the corpus at `46ba9c1`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, for issue #161.
- [`redline-claude-2026-08-26.md`](redline-claude-2026-08-26.md) — the Redline Skill against the corpus at `46ba9c1`, in Claude Code on `claude-opus-5`, for issue #160.
- [`unslop-claude-2026-08-26.md`](unslop-claude-2026-08-26.md) — the Unslop Skill against the corpus at `46ba9c1`, in Claude Code on `claude-opus-5`, for issue #162.
- [`proofread-gpt-2026-08-26-170.md`](proofread-gpt-2026-08-26-170.md) — Proofread's two model-invocation triggers re-run against `flawed-en-US` at `d0ec602`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, with the loaded resources judged from each Harness trace for issue #170.
- [`redline-gpt-2026-08-26-174.md`](redline-gpt-2026-08-26-174.md) — Redline's explicit Swedish zero-budget `slop-heavy-sv` branch re-run at corpus commit `46ba9c1`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, with the complete closing Proofread delegation and every planted mechanical correction passing for issue #174.
- [`unslop-gpt-2026-08-26-177.md`](unslop-gpt-2026-08-26-177.md) — Unslop's `locale-divergent` fixture re-run under both English locales at corpus commit `46ba9c1`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, with both lens-boundary criteria passing for issue #177.
- [`write-gpt-2026-08-26-180.md`](write-gpt-2026-08-26-180.md) — Write's response default re-run with the whole staged working copy and a separate Harness scratch area inventoried at corpus commit `d3a746e`, in Codex CLI `0.149.1` on `gpt-5.6-sol`, with the filesystem unchanged and the delivery account matching it for issue #180.

## Editorial rebuild — #329

The [reading packet](../editorial-329/README.md) links full sources, drafts, reviewed artifacts, frozen criteria, native traces, defects, independent reviews and final coverage. These records use GPT only, native Codex CLI 0.155.1 and observed gpt-6-astra/high; no other provider's records informed their judgments. Baseline and failed runs remain alongside later attempts.

- [redline-gpt-2026-09-19-338-baseline.md](redline-gpt-2026-09-19-338-baseline.md).
- [redline-gpt-2026-09-19-338-controls-genres.md](redline-gpt-2026-09-19-338-controls-genres.md).
- [redline-gpt-2026-09-19-338-part-article-case.md](redline-gpt-2026-09-19-338-part-article-case.md).
- [redline-gpt-2026-09-19-338-part-column-opinion-web.md](redline-gpt-2026-09-19-338-part-column-opinion-web.md).
- [redline-gpt-2026-09-19-338-selection.md](redline-gpt-2026-09-19-338-selection.md).
- [redline-gpt-2026-09-19-341-control-case-study.md](redline-gpt-2026-09-19-341-control-case-study.md).
- [redline-gpt-2026-09-19-341-part-article-case.md](redline-gpt-2026-09-19-341-part-article-case.md).
- [redline-gpt-2026-09-19-341-translation-part-article-case.md](redline-gpt-2026-09-19-341-translation-part-article-case.md).
- [redline-gpt-2026-09-19-342-column-final.md](redline-gpt-2026-09-19-342-column-final.md).
- [redline-gpt-2026-09-19-342-column.md](redline-gpt-2026-09-19-342-column.md).
- [redline-gpt-2026-09-19-343-opinion.md](redline-gpt-2026-09-19-343-opinion.md).
- [redline-gpt-2026-09-19-345-web-copy.md](redline-gpt-2026-09-19-345-web-copy.md).
- [redline-gpt-2026-09-19-346-controls-genres.md](redline-gpt-2026-09-19-346-controls-genres.md).
- [redline-gpt-2026-09-19-348-colon.md](redline-gpt-2026-09-19-348-colon.md).
- [redline-gpt-2026-09-19-348-control-column.md](redline-gpt-2026-09-19-348-control-column.md).
- [redline-gpt-2026-09-19-349-completion-check.md](redline-gpt-2026-09-19-349-completion-check.md).
- [redline-gpt-2026-09-19-349-opinion.md](redline-gpt-2026-09-19-349-opinion.md).
- [redline-gpt-2026-09-19-349-source-check-column.md](redline-gpt-2026-09-19-349-source-check-column.md).
- [redline-gpt-2026-09-19-349-source-check-opinion.md](redline-gpt-2026-09-19-349-source-check-opinion.md).
- [redline-gpt-2026-09-19-350-genre-selection.md](redline-gpt-2026-09-19-350-genre-selection.md).
- [write-gpt-2026-09-19-338-baseline.md](write-gpt-2026-09-19-338-baseline.md).
- [write-gpt-2026-09-19-338-part-article-case.md](write-gpt-2026-09-19-338-part-article-case.md).
- [write-gpt-2026-09-19-338-part-column-opinion-web.md](write-gpt-2026-09-19-338-part-column-opinion-web.md).
- [write-gpt-2026-09-19-341-part-article-case.md](write-gpt-2026-09-19-341-part-article-case.md).
- [write-gpt-2026-09-19-341-translation-part-article-case.md](write-gpt-2026-09-19-341-translation-part-article-case.md).
- [write-gpt-2026-09-19-342-column-final.md](write-gpt-2026-09-19-342-column-final.md).
- [write-gpt-2026-09-19-342-column.md](write-gpt-2026-09-19-342-column.md).
- [write-gpt-2026-09-19-343-opinion.md](write-gpt-2026-09-19-343-opinion.md).
- [write-gpt-2026-09-19-345-web-copy.md](write-gpt-2026-09-19-345-web-copy.md).
- [write-gpt-2026-09-19-349-completion-check.md](write-gpt-2026-09-19-349-completion-check.md).
- [write-gpt-2026-09-19-349-opinion.md](write-gpt-2026-09-19-349-opinion.md).
- [write-gpt-2026-09-19-349-source-check-column.md](write-gpt-2026-09-19-349-source-check-column.md).
- [write-gpt-2026-09-19-349-source-check-opinion.md](write-gpt-2026-09-19-349-source-check-opinion.md).

## Source-fidelity follow-up — #329

[The follow-up packet](../editorial-329/followup/README.md) preserves repeated baseline and candidate runs, independent source judgements and all failed attempts.

- [redline-gpt-2026-09-19-349-followup-new.md](redline-gpt-2026-09-19-349-followup-new.md).
- [redline-gpt-2026-09-19-349-followup-original.md](redline-gpt-2026-09-19-349-followup-original.md).
- [write-gpt-2026-09-19-349-followup-baseline.md](write-gpt-2026-09-19-349-followup-baseline.md).
- [write-gpt-2026-09-19-349-followup-new.md](write-gpt-2026-09-19-349-followup-new.md).
- [write-gpt-2026-09-19-349-followup-original.md](write-gpt-2026-09-19-349-followup-original.md).

- [redline-gpt-2026-09-19-354-second-controls.md](redline-gpt-2026-09-19-354-second-controls.md).

- [redline-gpt-2026-09-19-354-third-controls.md](redline-gpt-2026-09-19-354-third-controls.md).

- [redline-gpt-2026-09-19-355-second-new.md](redline-gpt-2026-09-19-355-second-new.md).

- [write-gpt-2026-09-19-355-second-new.md](write-gpt-2026-09-19-355-second-new.md).

- [redline-gpt-2026-09-19-341-quotation-new.md](redline-gpt-2026-09-19-341-quotation-new.md).

- [redline-gpt-2026-09-19-355-third-new.md](redline-gpt-2026-09-19-355-third-new.md).

- [redline-gpt-2026-09-20-341-quotation-controls.md](redline-gpt-2026-09-20-341-quotation-controls.md).

- [redline-gpt-2026-09-20-341-second-idiom.md](redline-gpt-2026-09-20-341-second-idiom.md).

- [redline-gpt-2026-09-20-349-second-original.md](redline-gpt-2026-09-20-349-second-original.md).

- [write-gpt-2026-09-19-355-third-new.md](write-gpt-2026-09-19-355-third-new.md).

- [write-gpt-2026-09-20-349-second-original.md](write-gpt-2026-09-20-349-second-original.md).

- [redline-gpt-2026-09-20-341-final-delivery-new.md](redline-gpt-2026-09-20-341-final-delivery-new.md).
- [redline-gpt-2026-09-20-341-final-parent-control.md](redline-gpt-2026-09-20-341-final-parent-control.md).
- [redline-gpt-2026-09-20-341-final-quotation-controls.md](redline-gpt-2026-09-20-341-final-quotation-controls.md).
- [redline-gpt-2026-09-20-341-final-quotation-original.md](redline-gpt-2026-09-20-341-final-quotation-original.md).
- [redline-gpt-2026-09-20-341-quotation-original.md](redline-gpt-2026-09-20-341-quotation-original.md).
- [redline-gpt-2026-09-20-349-third-original.md](redline-gpt-2026-09-20-349-third-original.md).
- [redline-gpt-2026-09-20-356-presupposition-new.md](redline-gpt-2026-09-20-356-presupposition-new.md).
- [redline-gpt-2026-09-20-356-presupposition-original.md](redline-gpt-2026-09-20-356-presupposition-original.md).
- [redline-gpt-2026-09-20-359-final-delivery-original.md](redline-gpt-2026-09-20-359-final-delivery-original.md).
- [redline-gpt-2026-09-20-359-final-mechanical-controls.md](redline-gpt-2026-09-20-359-final-mechanical-controls.md).
- [write-gpt-2026-09-20-349-third-original.md](write-gpt-2026-09-20-349-third-original.md).
- [write-gpt-2026-09-20-356-presupposition-new.md](write-gpt-2026-09-20-356-presupposition-new.md).
- [write-gpt-2026-09-20-356-presupposition-original.md](write-gpt-2026-09-20-356-presupposition-original.md).

- [redline-gpt-2026-09-20-344-account-new.md](redline-gpt-2026-09-20-344-account-new.md).
- [redline-gpt-2026-09-20-344-account-original.md](redline-gpt-2026-09-20-344-account-original.md).
- [write-gpt-2026-09-20-344-account-new.md](write-gpt-2026-09-20-344-account-new.md).
- [write-gpt-2026-09-20-344-account-original.md](write-gpt-2026-09-20-344-account-original.md).

## Source comparison — #362

The Claude-family evaluation of the change to Write's source comparison, read with [`../editorial-362/README.md`](../editorial-362/README.md).

- [`write-claude-2026-09-20-362.md`](write-claude-2026-09-20-362.md) — nine `/write` runs of the `opinion`, `column` and `case-study` sources against the working tree at `65834c3` with `source-check.md` changed, in Claude Code 2.1.278 on `claude-opus-5`: seven delivered, two valid stops, one delivery past the gate.
- [`redline-claude-2026-09-20-362.md`](redline-claude-2026-09-20-362.md) — the four source-blind `/redline` pairs on drafts that record delivered, same Harness and model: `R1` passes twice and fails twice.

