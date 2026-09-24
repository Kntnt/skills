# redline — claude — 2026-09-24 — #402

- **record** — `redline-claude-2026-09-24-402`
- **date** — `2026-09-24`
- **ticket** — `#402`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.281
- **corpus commit** — `1ef14cb5`

## Run conditions

Two arms over the ten *Redline controls* rows, and one revise round on `opinion-flawed`. The pre-change arm was staged from `1ef14cb5`, the branch head when #402's build began, with #397's change in it. The post-change arm was staged from `4b817d77`, which carries the candidate, and the revise round from `df6bb4a1`, which carries the revised wording. The method is [#383's](../editorial-383/plan.md) as [#397's](../editorial-397/plan-amendment.md) last applied it. It was frozen for this ticket in [`../editorial-402/plan.md`](../editorial-402/plan.md), the whole evaluation is written up in [`../editorial-402/results.md`](../editorial-402/results.md), and every run's packet is under [`../editorial-402/runs/`](../editorial-402/runs/).

Each run was a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), with the Formal Invocation as its whole prompt and the editorial Skills and the Manager staged by `git archive` into a private root of its own. Every artefact was judged by two fresh judges, blind to the arm, the model and the ticket, using #383's control brief unchanged; no run split. No Codex Harness and no GPT model was started, controlled or invoked.

Four criteria are this evaluation's own: **`C1`**, which is `R1` against the row's frozen expectation, **`O1`** and **`S1`**. A clean control was run once per arm to a response target, as the ticket fixes; the protocol's file-target run was not made.

## `pre-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with its headline rewritten and `kort` struck from the standfirst, and the run's account.
- **side effects** — the correction subagent's `scratch/cand.md` was left in the run's private scratch; `work/input.md` unchanged, the staged Skills unchanged; the root was removed by the runner.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: a conforming text given findings and rewritten; the headline change and the struck `kort` are taste on a clean control.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `fail` — the correction subagent's `scratch/cand.md` survived in the run's private scratch after the reply; the runner removed the root afterwards.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #430 (the behaviour it shows)
- **notes** — `O1` misses on a scratch file the correction subagent left.

## `pre-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed article in the reply, the byline, sections and ending section reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the unsupported certainty removed and every measured fact, exclusion and funding uncertainty kept; the missing navigation reported, not written. The 187-word lead is not named as over-long.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing byline, sections and ending section
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with its headline and two subheadings rewritten, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: a conforming text rewritten on taste; the new headline states Lind's qualified view as fact.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #399 (the behaviour it shows)
- **notes** — none

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed case study, the byline and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause reported, and the reservation and measures kept word for word.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing byline and call to action
- **defects filed** — none
- **notes** — none

## `pre-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the text unchanged and every clause met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `pre-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed column with its headline rewritten and three filler sentences removed, the missing parts reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the contradiction reported without an invented memory, and the reflection and doubt kept. The missing ending is not named as such.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst, sections and call to action
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the September clause in the lead and a sentence naming the assumption, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every preservation clause met; the September clause is borderline taste and covered by the account.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #431 (the September clause)
- **notes** — none

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input unchanged, the one round rejected, and nine unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause met except the ending's, which both record as partly met: no finding says the ending has no section of its own.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — nine, the vague exhortation among them
- **defects filed** — #402 (the defect this evaluation reproduces)
- **notes** — Reproduces the defect.

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the page unchanged and every clause met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, pre-change arm, staged from `1ef14cb5`
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed page with the calque, the audience description, the headings and the action repaired, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met; one inferred claim reported for the author to confirm.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with its headline and first subheading rewritten, and a reply saying the text meets the anatomy without deviation after reading the uncounted requirements.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: a conforming text rewritten on taste; the new headline moves Rask's recommendation into the headline.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #430 (the behaviour it shows)
- **notes** — No ending or section-count finding.

## `post-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed article, the byline, sections and ending section reported and not written, and a reply saying the text does not follow the anatomy.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the certainty removed, the paragraph split, the missing parts reported and not written. The late concept is not named, and the 187-word lead is named only as a paragraph to split.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing byline, sections and ending section
- **defects filed** — none
- **notes** — none

## `post-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input unchanged, the one round rejected, and five unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the text unchanged; two judges call the five findings over-detection on a conforming text.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — five, on the standfirst and the second subheading among them
- **defects filed** — none
- **notes** — No ending or section-count finding; the reply says the ending holds.

## `post-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed case study with a closing section built from its own content, the byline and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met; the reservation and measures kept word for word.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing byline and call to action
- **defects filed** — none
- **notes** — none

## `post-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with its headline, first subheading and a standfirst verb changed, and a reply saying the text follows the anatomy.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: the headline and subheading rewritten on taste, and the subheading's meaning moved.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #430 (the behaviour it shows)
- **notes** — A regression from the pre-change arm. No ending or section-count finding.

## `post-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed column with its headline rewritten and filler removed, the missing standfirst, sections, ending section and call to action reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met but the headline's missing subject, which no finding names.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst, sections, ending section and call to action
- **defects filed** — none
- **notes** — none

## `post-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the September clause, a sentence stating the assumption and `kanaler` changed to `bokningsvägar`, and a reply saying the text meets the anatomy.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: the added assumption sentence is a new claim in the author's name repairing no visible defect.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #434, #431 (the September clause)
- **notes** — A regression from the pre-change arm. No ending or section-count finding.

## `post-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input unchanged, the one round rejected, and ten unresolved findings, the missing ending section among them.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met, the missing ending section now among them; the repair from the body's actor and act identified but not applied, so the ending clause is unmet.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — ten, the ending among them
- **defects filed** — #433
- **notes** — The rejected round had written the ending section.

## `post-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page with a heading's fact copied into the body and `formuläret` expanded, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: taste edits on a clean page, and a missing form link reported as a defect.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing form location
- **defects filed** — #432 (the behaviour it shows)
- **notes** — A regression from the pre-change arm; web-copy loads no anatomy.

## `post-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, post-change arm, staged from `4b817d77`
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed page with the calque, the audience description, the headings and the action repaired, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `revise-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, revise round, staged from `df6bb4a1`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input unchanged, the one round rejected, and ten unresolved findings, the missing ending section among them.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met, the missing ending section among them; the repair identified but not applied, so the ending clause is unmet.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — ten, the ending among them
- **defects filed** — #433
- **notes** — The rejected round wrote an ending subheading that repeated nothing, and was rejected for the first subheading's echo.
