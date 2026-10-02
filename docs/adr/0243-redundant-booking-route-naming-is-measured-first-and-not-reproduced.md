# Redundant booking-route naming — measured first and not reproduced

Issue #492 makes a wording change conditional on a fresh native reproduction. Its six fresh `opinion-clean` runs show none of the unnecessary route findings or additions it names, so no product wording is changed. This records the measured disposition, not a declaration that the historical fault was correct or has been repaired.

## The observed fault and the distinction it keeps

#479's `rev-opinion-clean-resp-2` added `och som tar bort telefonbokningen` to the lead. The first review licensed it by removing both headline and standfirst from the body's reading test, although the anatomy's independence requirement names the standfirst. The headline names telephone booking, the lead's digital-only proposal gives the contrast, and the subsequent account identifies both channels. Both historical judges failed R1 as unnecessary repetition while agreeing that the reply accurately reported the edit and that no claim changed. Other historical runs passed or split on comparable additions. Those readings remain preserved in their packets and in [this evaluation's results](../evaluation/editorial-492/results.md).

This is not the unstated-premise behaviour ADR-0230 measured. Naming telephone booking where another passage already names it repeats existing information; it does not assert a premise absent from the text. Neither a correct change account nor the split rule establishes that such an addition was needed. A false finding would still matter if its correction were restored and the finding left standing.

## Why no additional instruction ships

The [prospective plan](../evaluation/editorial-492/plan.md) was committed as `cb446552`. A [second execution freeze](../evaluation/editorial-492/plan-pass-2.md), `115e04bd`, preserved the original and restarted before counted runs with a formatted evaluator; only a noneditorial capability smoke preceded it. The product and corpus baseline is `4cf05813`. The fresh evaluation uses Codex CLI `0.160.0`, `gpt-6.1-sol/xhigh`, one seat for runs, correction agents, Proofread, reply checks, validators and judges.

All three response runs of `opinion-clean` return authorised no-change statuses, and all three file runs deliver byte-identical texts. The recorded initial reviews and final reports contain no route finding, and no correction round adds another naming. The target therefore appears in zero of six fresh baseline runs. The old Claude arm is history, not a free baseline for this GPT measurement.

The two independent validators agreed that a different library lead's alternatives were already identifiable with the standfirst covered, while `Den kartläggningen` in its contrast needed the standfirst's mapping of opening hours named in the body. Both missing-reference runs made that minimal repair from existing content. Both certain-closure runs detected #479's genuinely settled outcome and removed `ändå`, rather than changing the pending-decision guard. Both judges of each nevertheless failed R1: they still read permanent closure as settled and the native declaration of no remaining finding as premature. That reviewer/judge disagreement is retained and filed as #497; detection is not silently counted as adequate repair. The working library's file run rewrote its lead under a different finding about standfirst repetition; both judges failed R1, and that separate miss is recorded and filed as #496. Neither is used to manufacture reproduction of the booking-route target.

Without a fresh target fault, another sentence loaded into every review would have no measured defect to repair and no candidate comparison that could show it works. The alternative is to keep the product as it stood, retain all observations, and leave a later native reproduction able to motivate a correction. The ticket and protocol choose that alternative. No candidate or revise arm is staged; their rows are explicitly skipped in the record.

## What remains true

The body must remain intelligible without the standfirst, and a genuinely unresolved referent is still detected and minimally repaired. Ordinary contextual inference is not itself a missing step, and the historical finding's additional removal of the headline is not silently adopted here. No telephone-booking exemption, blanket clarification ban, premise prohibition or expansion of the opinion's pending-decision rule is written. Source-blind review, the correction budget, whole-round rejection, final Proofread and reply checking, source/destination authority and cleanup are unchanged.
