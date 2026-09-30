# Records

One file per evaluation, named `<skill>-<provider-family>-<YYYY-MM-DD>-<issue>.md` after the issue the evaluation was run for, and written from [`../record-template.md`](../record-template.md) in the format [`../protocol.md`](../protocol.md) defines.

A record holds one provider family. Two families are compared by reading their two records side by side, which is the whole reason the format is fixed: the comparison costs a read rather than a re-run, and it can be made long after either session has ended.

A re-run is a new record rather than an edit to an old one. What a configuration did on a given day is history, and a later repair does not change it.

Every new record's name carries the issue number, because two tickets built side by side can each evaluate one Skill in one family on one day, and neither builder can see the other's record. Records written under the earlier rule, which added the issue only where a record of the same Skill, family and date already existed, keep the names they were written under.

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

## Unslop and the sentences that limit a claim — #385

The Claude-family evaluation of whether Unslop needs the limiting-sentence narrowing [#377](https://github.com/Kntnt/skills/issues/377) gave Redline, filed as [#385](https://github.com/Kntnt/skills/issues/385). Read it with [`../editorial-385/plan.md`](../editorial-385/plan.md) and [`../editorial-385/results.md`](../editorial-385/results.md). It adapts #377's shape to Unslop on the four #362 drafts and runs the pre-change arm first, with the conclusion that Unslop does not reach a limiting sentence on them, that the candidate narrowing is reverted and nothing ships, and that Redline's and Unslop's rules diverge on purpose (ADR-0221).

- [`unslop-claude-2026-09-28-385.md`](unslop-claude-2026-09-28-385.md) — four `Unslop` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation, the four drafts once each against the product as it stood, with two blind judges each, made after the plan was frozen again; a first wave, voided because the plan was edited after it, is kept apart and not counted. Three runs returned the no-change status, and the fourth replaced *channel(s)* with *route(s)* in three places on a synonym-cycling finding, keeping the limiting clauses in the two sentences it touched word for word. No limiting sentence was removed, weakened, hardened or recast on either judge's reading, and *I am not against digital booking.* came back unchanged from both English runs. The eight post-change runs and the seven controls are recorded as not run.

## A changed headline is reported by its defect, a removed limit by its loss — #400

The Claude-family evaluation of Thomas's ruling on [#400](https://github.com/Kntnt/skills/issues/400). The ruling is that Redline's account names every change to a headline, a subheading or a standfirst with the defect that licensed it, and that where a removal takes a limit, a connective or a bounding clause out of the text, the account names what the reader no longer has. Read it with [`../editorial-400/plan.md`](../editorial-400/plan.md), its [amendment](../editorial-400/plan-amendment.md) and [`../editorial-400/results.md`](../editorial-400/results.md). It uses #383's method on the four #362 drafts and the ten controls, with a pre-change arm replayed from the commit the build started from, and it re-runs the four #392 pair rows source-blind. Every run is a top-level session started with the evaluation's own runner. The build was cut off by a usage limit and resumed four days later. The runs that limit stopped, and the six made before a spelling edit to the frozen plan, are void and were run again; `results.md` gives the timeline.

- [`redline-claude-2026-09-24-400.md`](redline-claude-2026-09-24-400.md) — forty-four `Redline` runs in Claude Code 2.1.281 on `claude-opus-5-5` at high deliberation, on 2026-09-24 and 2026-09-28. The four drafts ran once before the change and twice after, and the ten *Redline controls* once in each arm; these thirty-two runs had two blind judges each. Each #392 row ran up to three times. The pre-change arm did not reproduce the defect where the plan measures it. After the change, `case-study-flawed` and `column-flawed` reported each replaced heading with its defect, `article-flawed` passed every criterion, and no control regressed. The `Lervik's` headline was not rewritten in either arm, and no #392 row recurred, so those criteria are recorded as not exercised. The wording ships. Two remaining misses are filed as #436 and #437.

## A headline, subheading or standfirst that asserts past a kept limit — #415

The Claude-family evaluation of the form four judges of #383 named independently: a headline, subheading or standfirst the run wrote or changed that asserts past a limiting sentence the text keeps word for word, filed as [#415](https://github.com/Kntnt/skills/issues/415). Read it with [`../editorial-415/plan.md`](../editorial-415/plan.md) and [`../editorial-415/results.md`](../editorial-415/results.md). It uses #383's method on the four #362 drafts and the ten controls, with #400's staging, and runs the pre-change arm first under a new paratext brief, with the conclusion that the form does not reproduce, that no wording is written and nothing ships, and that the brief and its counting rule stay as the criterion for measuring the form (ADR-0223).

- [`redline-claude-2026-09-28-415.md`](redline-claude-2026-09-28-415.md) — eighteen `Redline` runs in Claude Code 2.1.283 on `claude-opus-5-5` at high deliberation, the four drafts twice each and the ten *Redline controls* once each against the product as it stood, with two blind judges each on the paratext brief. No run counts: all thirty-six judgements answer no. Every instance #383's judges named was a part written into a text that had none, and no run here wrote one, since #397's change reports a missing standfirst or subheading instead. Eleven runs changed a headline, subheading or standfirst the text already had, and no judge found one asserting past a kept limit. The post-change arm and the frozen briefs were not run.

## Writing Brief — #444

- [brief-gpt-2026-09-28.md](brief-gpt-2026-09-28.md) — the three Brief modes in Swedish and English, the bare-mention control, and each mode's file handed to Write; native Codex traces, synthetic fixtures, filesystem inventories and gate evidence are in [the #444 packet](../brief-444/README.md).

## Redline against a Writing Brief — #445

- [redline-gpt-2026-09-28-445.md](redline-gpt-2026-09-28-445.md) — native Codex evaluations of brief selection, template mapping and markers, map precedence, source-bound correction, brief protection and no-brief controls; the [packet](../redline-445/README.md) preserves fixtures, traces, inventories and red/green evidence.

## A web page's own form and a heading's fact are not findings — #432

- [`redline-claude-2026-09-29-432.md`](redline-claude-2026-09-29-432.md) — eighteen staged runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, nine in each arm: `web-copy-clean` as three response-target and file-target pairs, `web-copy-flawed` once, and the `web-copy-sv` Write→Redline pipeline once, with two blind judges for each of the sixteen Redline runs. Before the change, every `web-copy-clean` run reported the page's form as missing and copied `inom tre arbetsdagar` from a subheading into the body, and failed `C1`. After it, no run did, every file-target run delivered the page byte for byte, and both controls met their readings in both arms. The change ships, and nothing was filed.

## Everything a reply says about a text is true of the text it names — #435

The Claude-family evaluation of the duty [#435](https://github.com/Kntnt/skills/issues/435) wrote into the shared delivery contract: everything a run's reply says about a text is true of the text it names, checked against the delivered text after the last change. Read it with [`../editorial-435/plan.md`](../editorial-435/plan.md) and [`../editorial-435/results.md`](../editorial-435/results.md). It uses #398's method and briefs on the four #362 drafts and the ten controls, and reads every `A2` miss into four classes rather than only those about the claims. Every run is a top-level session made with the #388 staged runner.

- [`redline-claude-2026-09-30-435.md`](redline-claude-2026-09-30-435.md) — forty-three counted `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, with two blind judges each. They are the four drafts once before the change and twice after, the ten *Redline controls* once in each arm, and a revise round of eleven runs on the seven inputs the ship rule sent back. Six void runs are recorded beside them. Before the change, 2 of 14 replies said something false about a text outside the claim account; none of #435's six statements recurred. The first wording raised that to 6 of 18. The revised wording stopped every false *unchanged* or *named nowhere else*, but two false counts about the delivered text remain, 3 of 18 in all. So the Target is missed. The Control is missed on `column-sv-r1`. The revised wording ships, as the ship rule says, and the remaining misses are filed as #451–#462.

## A heading that works is left alone — #429

The Claude-family evaluation of Thomas's ruling on [#429](https://github.com/Kntnt/skills/issues/429) that on a finished text Redline leaves a heading that works, and rewrites one only where a reader would be misled or lose something it can name. Read it with [`../editorial-429/plan.md`](../editorial-429/plan.md) and [`../editorial-429/results.md`](../editorial-429/results.md). It uses #397's method with the clean controls run as the protocol's response-target and file-target pairs, a file-target run judged from the file it delivered, and every run a top-level session made with the #388 staged runner.

- [`redline-claude-2026-09-30-429.md`](redline-claude-2026-09-30-429.md) — one hundred and one `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation: the four clean controls as three pairs each, the three #362 drafts twice, the four flawed controls and #396's two controls once, in a pre-change arm and against the first candidate, and the failing subset again against a revised wording, with two blind judges on every judged run. Before the change every clean control had a heading rewritten or added and two drafts missed `R1` on a heading; the revised wording met the target on `article-clean`, `opinion-clean` and `opinion-en_GB-r1` and cut the runs that miss from fourteen to six, but `case-study-clean`'s headline is still rewritten (#463), `column-clean` still gains a subheading over its ending (#464), one `column-sv-r2` repair drops *ruta* (#465), and `column-flawed`'s missing subject is no longer reported (#466). #396's control fired in every run. The revised wording ships, as the ruling requires.

## A correction round's heading that repeats what it stands over — #433

The Claude-family evaluation of [#433](https://github.com/Kntnt/skills/issues/433): whether Redline's correction agent still returns a headline or subheading that repeats what it stands over, so that the re-review rejects the whole round and `opinion-flawed`'s ending section is lost with it. Read it with [`../editorial-433/plan.md`](../editorial-433/plan.md) and [`../editorial-433/results.md`](../editorial-433/results.md). It uses #402's method, reads whether a run delivers the ending from the returned text rather than from the blind judges, and makes every run a top-level session with the #388 staged runner.

- [`redline-claude-2026-09-30-433.md`](redline-claude-2026-09-30-433.md) — six `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, all in the pre-change arm staged from `2afeb95e`, the tree #429 leaves: `opinion-flawed` three times and `article-flawed`, `case-study-flawed` and `column-flawed` once each, with two blind judges on every run. Two of the three `opinion-flawed` runs deliver the ending in a section of its own built from the body's actor and act, and the third lost it to a round rejected for an attribution shift, not for a repeating heading. The defect is recorded as not reproduced: no candidate was committed, nothing ships, nothing is filed, and ADR-0225 records why. Every control met `C1`.

## What a quotation bridge may carry, stated where Write reads it — #438

The Claude-family control for [#438](https://github.com/Kntnt/skills/issues/438), which replaced the case-study genre's one sentence on the quotation bridge with what it may carry and a reader test, read with [`../editorial-438/plan.md`](../editorial-438/plan.md) and [`../editorial-438/results.md`](../editorial-438/results.md). Two arms of seven `case-study` runs each, made with the #388 staged runner on #396's rows, judged on #396's brief.

- [`write-claude-2026-09-30-438.md`](write-claude-2026-09-30-438.md) — fourteen `Write` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, three of `case-question-en_GB` and two each of `case-study-en_US` and `case-study-sv` per arm, two blind judges each. No quotation bridge was classed as restating its quotation and no subheading over a quotation as a pre-echo, in either arm, so the candidate met the ship rule in its first arm and ships. Judges weighed and rejected a reading of a bridge as restating its quotation on 6 of 14 pre-change judgements and on none after the change; that is recorded as measured and is not a criterion. The GPT-family retest stays #395.

## The press release follows the maintainer's instruction — #473

The Claude-family evaluation of [#473](https://github.com/Kntnt/skills/issues/473), which gave the press release genre the maintainer's shape, two counted limits measured by the Library's script, and two quotations in fixed places. Read it with [`../editorial-473/plan.md`](../editorial-473/plan.md) and [`../editorial-473/results.md`](../editorial-473/results.md). There is no pre-change arm, as the instruction ships whatever the measurement shows. Every run was a top-level session made with the #388 staged runner, on synthetic material tied to no real organisation.

- [`write-claude-2026-09-30-473.md`](write-claude-2026-09-30-473.md) — three `Write` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, one each on material with two quotations, one and none, two blind judges each. Every draft kept the part order, stayed inside both limits as the script measured them, wrote only the material's quotations in their places and reported the missing ones as gaps. One draft was delivered with a disclosed source-comparison finding, which is recorded under #376.
- [`redline-claude-2026-09-30-473.md`](redline-claude-2026-09-30-473.md) — seven `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation: three old-shape releases, one per quotation case, the conforming release as a response-target and file-target pair, and a revise round of the two old-shape runs that missed. On the first candidate the notes block to the editor did not fire in two of three runs. After the revised wording, every planted defect fired on both judges, and the conforming release came back byte-identical. Nothing is filed.

## A loss counted as its reader suffers it, and no premise written in — #468

The Claude-family evaluation of [#468](https://github.com/Kntnt/skills/issues/468), whose two halves were each conditional on the measurement. One half counts a loss as the reader of a passage would suffer it in every passage, the standfirst included. The other says a review writes in no premise an argument leaves unstated. Read it with [`../editorial-468/plan.md`](../editorial-468/plan.md) and [`../editorial-468/results.md`](../editorial-468/results.md). The plan copies #429's control briefs, split rule, runner and void-run handling, and every run is a top-level session made with the #388 staged runner.

- [`redline-claude-2026-09-30-468.md`](redline-claude-2026-09-30-468.md) — thirty-two counted `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, with two blind judges on every run. `article-clean` and `opinion-clean` ran as three response-target and file-target pairs each, and `article-flawed` and `opinion-flawed` twice each, in a pre-change arm and against the candidate. One run cut off by a spend limit is kept apart as void and was made again. Before the change `article-clean`'s standfirst lost *kort* in four of six runs, and after it in none. Every defect the two flawed rows name was still detected, so the reader-loss half ships. No pre-change run wrote a premise into `opinion-clean`. Two runs added a phrase naming what the text already states, which the plan counts as a clarification. So the premise half is recorded as not reproduced, does not ship, and ADR-0230 records why. The candidate arm's two remaining misses are filed as #479 and #480.

## Redline's reply checked by a reader that did not write it — #475

The Claude-family evaluation of the reply checker [#475](https://github.com/Kntnt/skills/issues/475) added to Redline: a fresh subagent reads the drafted reply against the text as it arrived and the delivered text, and the run corrects the reply from what it returns. Read it with [`../editorial-475/plan.md`](../editorial-475/plan.md) and [`../editorial-475/results.md`](../editorial-475/results.md). It uses #435's method and briefs on the four #362 drafts and the ten controls. It counts both claim-account misses and false statements about a text. It runs each clean control to a file as well, so that `C1` can be scored. Every run is a top-level session made with the #388 staged runner.

- [`redline-claude-2026-09-30-475.md`](redline-claude-2026-09-30-475.md) — forty-six `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, twenty-three in each arm, with two blind judges each. They cover the four drafts twice and the ten *Redline controls* once to the response, and the five clean controls once more to a file. Before the change, 5 of 18 replies carried a claim-account miss or a statement the text contradicts. After it, 1 of 18 did, and no false count or length remained, so the Target is met. `case-study-clean` failed `C1` after the change on a clean-text rewrite #468 owns, so the Control is met. The checker ships. The two misses in the one remaining run are filed as #477 and #478.

## A closing proposal is an ending — #464

The Claude-family evaluation of [#464](https://github.com/Kntnt/skills/issues/464), which changed the article anatomy's test for when the last section is the ending, so that stating the proposal the text has built towards, the writer's reservation about it and the call to act on it count as closing content. Read it with [`../editorial-464/plan.md`](../editorial-464/plan.md) and [`../editorial-464/results.md`](../editorial-464/results.md). It copies #429's control briefs, split rule, runner and void-run handling, and makes every run a top-level session with the #388 staged runner.

- [`redline-claude-2026-09-30-464.md`](redline-claude-2026-09-30-464.md) — sixteen `Redline` runs in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, with two blind judges each: `column-clean` as three response-target and file-target pairs and `opinion-flawed` twice, in a pre-change arm staged from `41fd4c55` and against the candidate `131c5c39`. Two pre-change `column-clean` runs split the ending under a new subheading and failed `R1`; no candidate run added a heading line, so the target is met. `opinion-flawed`'s closing exhortation got a section of its own in all four runs, so the control holds. The candidate ships. A first attempt, voided when the plan was refrozen to drop a decision-record number no record carries, and eleven runs cut off by a usage limit are kept under `voided/`; one voided candidate run left its working files behind (#476).
