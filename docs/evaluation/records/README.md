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

## The final comparison and the delivery — #376

The Claude-family evaluation of what Write does when the last source comparison leaves a supported finding, read with [`../editorial-376/README.md`](../editorial-376/README.md).

- [`write-claude-2026-09-20-376.md`](write-claude-2026-09-20-376.md) — three `/write` runs of the corpus `opinion` source in `en_US` against the working tree at `4a932dd` with `skills/editorial/write/` changed, in Claude Code 2.1.278 on `claude-opus-5`: all three delivered the prose their last comparison read, with every remaining finding named beside the draft and no prose changed afterwards.

## Limiting sentences and the claim account — #377

The Claude-family evaluation of the change [#377](https://github.com/Kntnt/skills/issues/377) made to Redline's whole-passage removal permission and to the account both editorial correction Skills owe, read with [`../editorial-377/plan.md`](../editorial-377/plan.md), [`../editorial-377/diagnosis.md`](../editorial-377/diagnosis.md) and [`../editorial-377/results.md`](../editorial-377/results.md).

- [`redline-claude-2026-09-20-377.md`](redline-claude-2026-09-20-377.md) — twenty-two source-blind `/redline` runs in Claude Code 2.1.278 on `claude-opus-5`, two blind judges each: four pre-change replays of the #362 drafts, the same four reviewed twice against the change, and the ten `Redline controls` of the corpus. No limiting sentence is deleted or hardened after the change except under a verified class (a) finding, every changed claim is named in the account, and all ten controls meet their frozen expectation.

## The article anatomy on the revised controls and two pipeline rows — #386

The Claude-family evaluation of Write and Redline against the part of the editorial-quality corpus that was revised for the article anatomy and the headline reference and had never been run since, read with [`../editorial-386/runs/plan.md`](../editorial-386/runs/plan.md) and [`../editorial-386/runs/results.md`](../editorial-386/runs/results.md).

- [`write-claude-2026-09-21-386.md`](write-claude-2026-09-21-386.md) — the two `Write` pipeline rows `column-sv` and `case-study-sv` against the corpus at `9a29bad3`, in Claude Code 2.1.278 on `claude-opus-5` at high deliberation, two blind judges each: both delivered, both drafts measured conforming by `article_anatomy.py`, and one `G2` failure — a `column-sv` subheading repeating the sentence under it, which neither source checker nor the delivery account caught.
- [`redline-claude-2026-09-21-386.md`](redline-claude-2026-09-21-386.md) — the eight `Redline controls` of the four article genres and the two `Redline` pipeline rows of the same drafts, same Harness, model and judge arrangement: three of the four clean controls returned byte-identical, `opinion-clean` came back with an unreported clause added to its lead, and both rows that shipped a defect shipped one their own correction round had made and reported.

## The corpus coverage #362 left out — #380

The Claude-family evaluation of the `article`, `web-copy` and repeated `opinion` pipeline rows and all three explicit technique rows, which neither [#362](https://github.com/Kntnt/skills/issues/362) nor [#386](https://github.com/Kntnt/skills/issues/386) had run, read with [`../editorial-380/runs/plan.md`](../editorial-380/runs/plan.md) and [`../editorial-380/runs/results.md`](../editorial-380/runs/results.md).

- [`write-claude-2026-09-21-380.md`](write-claude-2026-09-21-380.md) — the eight `Write` pipeline rows `article-sv`, `article-en_GB`, `web-copy-sv`, `opinion-sv` twice, `article-abt`, `article-pac` and `web-copy-abt` against the corpus at `8a37e57e`, in Claude Code 2.1.278 on `claude-opus-5` at high deliberation, two blind judges each: all eight delivered, all eight delivered the prose their final comparison read, byte for byte on the prose itself — five of the eight files are identical to the compared draft and the other three differ only by the `kntnt` frontmatter block — and every `F1` failure is a residual the delivery account reported, which is the outcome #376 decided.
- [`redline-claude-2026-09-21-380.md`](redline-claude-2026-09-21-380.md) — the eight source-blind `Redline` runs of those drafts, same Harness, model and judge arrangement: seven pass every criterion, `opinion-sv-r2` fails `R1` for changing a conforming text to taste under an account that does not hold (#383), `article-en_GB` repaired one of Write's own reported residuals from the text alone, and half the rows dropped something the material required without being able to know it (#392).
