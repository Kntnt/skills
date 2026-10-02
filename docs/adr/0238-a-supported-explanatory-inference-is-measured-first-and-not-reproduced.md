# A supported explanatory inference — measured first, and not reproduced

This record decides **not** to add product wording for #486's false placement finding. The ticket makes a correction conditional on a fresh native baseline reproducing it. The six baseline `article-clean` replies show no such finding, and their artifacts preserve the supported lead inference. No candidate was written and no shipped file changed. Recorded on 2026-10-02.

## The observation that remains valid

#479's `post-article-clean-resp-3` replaced the lead's “Det gör placeringen viktig när …” with “Det är utgångspunkten när …”. #480's `post-article-clean-file-2` replaced it with “Det avgränsar vad …”. Both judges failed R1 on each. The replies treated a supported explanation as a promise to give actual sensor locations: the preceding sentence already explains that a sensor measures the air where it sits, and the ending takes placement up with “likadant placerade givare”. Missing location data therefore does not leave this explanation unfulfilled. #487's duplicate evidence was merged into #486 and is not reopened.

The supplied thread places the over-reading in the article follow-through and lead/ending relationship, against the existing generic reader-loss and smallest-correction guidance. The old observations justify measuring the problem; they are not a fresh comparison arm and do not justify choosing another rule without a reproduced miss.

## Why no wording ships

[The frozen plan](../evaluation/editorial-486/plan.md) was committed at `d8c36e42` before any native validation or review. Product and corpus instructions were staged from the build's starting commit, `5457c894`. Every native run, correction delegate, reply checker, validator and judge ran on `gpt-6.1-sol` at `xhigh` in Codex CLI 0.160.0, verified from native turn and session metadata. A Codex session cannot invoke Claude under the evaluation protocol, so the older Opus measurements remain historical evidence rather than this baseline.

Three independent response/file pairs of the unchanged corpus control produced **zero placement misses in six replies**. None reports the placement inference as an unfulfilled promise, leaves such a finding unresolved, reports a rejected placement repair, or offers an alternative for that sentence. Every delivered artifact keeps the entire original lead and body. Two file artifacts are byte-identical to the input; the third changes only the headline. Both independent judges of every run confirm preservation of the placement explanation. Headline findings in four clean runs belong to #480 and are recorded separately rather than repaired here.

The additional denominator inference is retained in both of its runs without a demand for absent hourly observations. The explicit sensor-position/window-distance disclosure promise is detected in both of its runs and removed without invented details. The contrast validation confirmed this distinction, but did not establish whole-anatomy conformance after replacing the leads. The frozen clean expectations and body-independent referent repairs consequently conflict in the R1 judgements; that gap is preserved and filed as #493. It does not change the untouched corpus control's placement result, and these contrasts are not claimed as wholly successful clean controls.

The [results](../evaluation/editorial-486/results.md) and [protocol record](../evaluation/records/redline-gpt-2026-10-02-486.md) keep every counted run, both judgements, inventories, differences and observable review/correction/re-review/delivery/report stages. No plan, input, brief or frozen harness was rewritten to improve the result. The conditional candidate and revise arms are recorded as not run.

## What would reopen the measurement

A fresh run of the current product that reports the supported lead inference as a demand for missing location details, whether repaired, unresolved or attached to a rejected correction, supplies the missing red step. An unchanged file or an R1 pass cannot clear that false report. The valid-inference/unfulfilled-promise distinction and the source-protection contract still hold; this record adds no exemption to either. It records non-reproduction on this seat, not a finding that the older Claude observations never happened or that the behaviour cannot recur.
