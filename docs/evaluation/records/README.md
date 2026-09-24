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

## Idiomatic quoted speech, and leaving a working quotation alone — #363

The Claude-family evaluation of the wording [#363](https://github.com/Kntnt/skills/issues/363) proposed for Write and Redline, read with [`../editorial-363/plan.md`](../editorial-363/plan.md), its frozen [`fixtures/README.md`](../editorial-363/fixtures/README.md), [`../editorial-363/results.md`](../editorial-363/results.md) and [`../editorial-363/reviews/load-chain-review.md`](../editorial-363/reviews/load-chain-review.md). Three arms over the same frozen inputs — the product unchanged, and two candidate wordings — with the conclusion that neither failure the ticket is about reproduces in this family and that nothing ships (ADR-0212).

- [`write-claude-2026-09-22-363.md`](write-claude-2026-09-22-363.md) — the fifteen `case-study` `Write` runs, in `sv`, `en_US` and `en_GB` in the first two arms and in `sv` and `en_US` in the third, in Claude Code 2.1.278 on `claude-opus-5` at high deliberation, two blind judges each: every run delivered, every English draft carried the source sentence verbatim, and the only Swedish draft whose checker raised a translation finding repaired it by writing a referent into the quotation that the material does not settle.
- [`redline-claude-2026-09-22-363.md`](redline-claude-2026-09-22-363.md) — fifty source-blind `Redline` runs — thirty-five over the two frozen Swedish inputs, the two frozen English inputs and the three new contrast fixtures in all three arms, and fifteen paired replays of the delivered drafts — same Harness, model and judge arrangement: every run returned its quoted sentence word for word, and both judges read the Swedish passages as taken on one pass, the mandatory Swedish control and the `ellipsis-sv` negative control included. In English the judging splits — five of the hundred judgements read *before the next building starts* as a place the reader stops, all five by one judge — which the record sets out row by row.

## A bridge that prepares a quotation rather than pre-saying it — #364

The Claude-family evaluation of the bridge rule [#364](https://github.com/Kntnt/skills/issues/364) proposed to sharpen, read with [`../editorial-364/plan.md`](../editorial-364/plan.md) and [`../editorial-364/results.md`](../editorial-364/results.md). One arm only: the product unchanged, over the source the fault was found in and two positive controls, with the conclusion that the fault does not reproduce in this family and that nothing ships (ADR-0214). The result is filed as [#395](https://github.com/Kntnt/skills/issues/395), and what the run found in its place as [#396](https://github.com/Kntnt/skills/issues/396).

- [`write-claude-2026-09-22-364.md`](write-claude-2026-09-22-364.md) — the seven `case-study` `Write` runs, three of `case-question-en_GB` and two each of `case-study-en_US` and `case-study-sv`, against the corpus at `218e3be1`, in Claude Code 2.1.278 on `claude-opus-5` at high deliberation, two blind judges each: all seven delivered, and no `case-question-en_GB` draft carries a class (a) bridge on either judge across all three runs — though in `r2` both judges chose (b) over a live (a) reading each of them set out, and one of the two paired Redline judges read that same bridge (a). The two control rows split on one bridge each, `case-study-en_US-r1` at its second quotation and `case-study-sv-r2` over where the bridge is at all, so both rows count as unmet on that point; the record sets out every bridge, its class and the words that put it there, row by row. Four rows were dispatched more than once after a server-side kill delivered nothing, and their six voided attempts are kept beside the runs.
- [`redline-claude-2026-09-22-364.md`](redline-claude-2026-09-22-364.md) — the seven paired source-blind `Redline` runs of those drafts, same Harness, model and judge arrangement: `R1` passes on both judges in four rows and splits in three, every failure being a claim the review shipped or a change it did not report, of the shapes #377, #383, #389 and #392 already own. In all seven rows the preserved mechanical-pass output is byte-identical to the delivered artefact, so the closing pass is the last thing that touched the text; two class (a) bridges in the inputs were repaired on both judges and a third on one judge, two came back in class (a) and unfound on one judge each, and no review moved a bridge into class (a).

## Differences that trace to no finding, and the account that omits them — #383

The Claude-family evaluation of the change [#383](https://github.com/Kntnt/skills/issues/383) made to the correction loop of both editorial correction Skills and to the anti-slop catalogue's guard, read with [`../editorial-383/plan.md`](../editorial-383/plan.md) and [`../editorial-383/results.md`](../editorial-383/results.md). Two arms over the four #362 drafts and the ten `Redline controls`, the pre-change arm replayed here because twenty-seven of the files Redline loads had changed since [#377](https://github.com/Kntnt/skills/issues/377) ran.

- [`redline-claude-2026-09-22-383.md`](redline-claude-2026-09-22-383.md) — twenty-three source-blind `Redline` runs in Claude Code 2.1.278 on `claude-opus-5` at high deliberation, two blind judges each: four pre-change replays of the #362 drafts, the same four reviewed twice against the change, the ten `Redline controls` of the corpus, and one pre-change replay of the one control that missed. Every difference a round returns now traces to a finding and every reply closes with an account of what else it changed, which covers all three control blemishes #377 recorded and three of the four texts #386 found; the four drafts still fail `R1` in both arms on the article anatomy's missing parts being repaired by authoring prose into a finished text, and the claim account's assurance is written about claims received and so reads false once a run adds one. Both are recorded as measured and filed as #397 and #398, with #399, #400, #401 and #402 beside them; the record maps every `fail` line in it to the residual that carries it.

## A subheading that pre-spends the quotation under it — #396

The Claude-family evaluation of the rule [#396](https://github.com/Kntnt/skills/issues/396) added to `headlines.md` for a subheading standing over a quotation, read with [`../editorial-396/plan.md`](../editorial-396/plan.md) and [`../editorial-396/results.md`](../editorial-396/results.md). Two arms of seven `case-study` runs each, made with the #388 staged runner, the pre-change arm replayed in-session because the model and the files Write loads had both moved since #364 ran.

- [`write-claude-2026-09-24-396.md`](write-claude-2026-09-24-396.md) — fourteen `Write` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation, three of `case-question-en_GB` and two each of `case-study-en_US` and `case-study-sv` per arm, two blind judges each. Before the change every one of the seven drafts carried a subheading counted as a pre-echo, fourteen in all and five in the row the fault was found in; after it none did, and no quotation bridge was classed as restating its quotation in either arm. The change ships; `article`, `column`, `opinion` and the Redline-side wording are unmeasured.

## A conforming subheading rewritten on one install and not the other — #399

The Claude-family measurement [#399](https://github.com/Kntnt/skills/issues/399) asked for after #383's `case-study-clean` control missed against its post-change install and passed on one pre-change replay, read with [`../editorial-399/plan.md`](../editorial-399/plan.md) and [`../editorial-399/results.md`](../editorial-399/results.md). Five runs of that control against each of #383's two installs, `3167fb68` and `5af1390d`, alternating, one at a time, with #383's turn files and control judge brief. No product change on any outcome.

- [`redline-claude-2026-09-24-399.md`](redline-claude-2026-09-24-399.md) — ten source-blind `Redline` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation, each a top-level session running the `kntnt-opus-high` agent, two blind judges each. Each install rewrote the conforming subheading `Två perioder med olika arbetsbelastning` in one run of five, both on the finding that it had no verb, and returned the no-change status in the other four: one miss per arm is the second of the outcomes fixed in advance, so the miss belongs to the headline contract's authority over a subheading that already conforms (#397, #400) and not to the six files #383 changed. #383's miss on `claude-opus-5` is not re-tested, and the eight passes rest on a no-change status, the file-target runs of the protocol's clean-control rule having landed after this matrix was fixed.

## A part a finished text lacks is reported, not written — #397

The Claude-family evaluation of Thomas's ruling on [#397](https://github.com/Kntnt/skills/issues/397) that a review reports a part the text does not have and repairs a part it has, read with [`../editorial-397/plan.md`](../editorial-397/plan.md), [`../editorial-397/plan-amendment.md`](../editorial-397/plan-amendment.md) and [`../editorial-397/results.md`](../editorial-397/results.md). #383's method, with a pre-change arm replayed in-session because the model and the files Redline loads had both moved since #383 ran, and every run a top-level session made with the #388 staged runner because the evaluating session could not nest one.

- [`redline-claude-2026-09-24-397.md`](redline-claude-2026-09-24-397.md) — thirty-two `Redline` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation: the four #362 drafts once before the change and twice after, and the ten *Redline controls* once in each arm, two blind judges each. Before the change every draft run wrote a standfirst, subheadings, a lead or a call to action into a text that had none and failed `R1`; after it no run did, and `R1` was met on six of eight. The two misses reword a working column headline under the headline contract (#429); `article-clean`, `case-study-clean` and `column-clean` came back with a rewritten heading after passing before (#430, #399); `opinion-clean` changed in both arms (#431) and `web-copy-clean` missed in both (#432). The change ships, as the ruling requires.

## The ending is a section of its own — #402

The Claude-family evaluation of Thomas's ruling on [#402](https://github.com/Kntnt/skills/issues/402) that an article's ending owes a section of its own. Read it with [`../editorial-402/plan.md`](../editorial-402/plan.md) and [`../editorial-402/results.md`](../editorial-402/results.md). It uses #383's method on the ten controls, as #397 last applied it. The pre-change arm is replayed in-session from the commit the build started from, and every run is a top-level session made with the #388 staged runner.

- [`redline-claude-2026-09-24-402.md`](redline-claude-2026-09-24-402.md) — twenty-one `Redline` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation: the ten *Redline controls* once in each arm and `opinion-flawed` once more against a revised wording, with two blind judges each. Before the change no finding said that `opinion-flawed`'s ending had no section of its own. After it, every run said so, and every reply on an anatomy genre said what it had examined before saying whether the text conforms. The ending repair was written and then lost each time, with a round rejected for a heading echo elsewhere (#433). No conforming control gained an ending or section-count finding. `opinion-clean` (#434), `column-clean` (#430) and `web-copy-clean` (#432) missed `C1` after passing before. The first wording ships, as the ruling requires.

## The claim account covers the claims a run wrote — #398

The Claude-family evaluation of Thomas's ruling on [#398](https://github.com/Kntnt/skills/issues/398) that a claim the run wrote joins the claim account as a third class, and that no assurance contradicts a finding in the same reply. Read it with [`../editorial-398/plan.md`](../editorial-398/plan.md) and [`../editorial-398/results.md`](../editorial-398/results.md). It uses #383's method on the four #362 drafts and the ten controls, as #397 last applied it. The pre-change arm is replayed in-session from the commit the build started from, and every run is a top-level session made with the #388 staged runner.

- [`redline-claude-2026-09-24-398.md`](redline-claude-2026-09-24-398.md) — thirty-four `Redline` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation: the four drafts once before the change and twice after, the ten *Redline controls* once in each arm, and `opinion-flawed` and `web-copy-clean` once more against a revised wording, with two blind judges each. Before the change `opinion-en_GB-r1`'s reply said no claim had changed over a subheading that narrowed one. After it, every draft reply and `web-copy-flawed` met `A2`, and `web-copy-flawed` listed its *booking* inference as an added claim. The first wording regressed two controls on what their accounts said. The revised wording met both, and ships. Descriptive inaccuracies outside the claim account are filed as #435.
