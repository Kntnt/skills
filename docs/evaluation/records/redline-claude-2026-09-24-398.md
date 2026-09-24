# redline — claude — 2026-09-24 — #398

- **record** — `redline-claude-2026-09-24-398`
- **date** — `2026-09-24`
- **ticket** — `#398`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.281
- **corpus commit** — `81f50bfd`

## Run conditions

Two arms over the four #362 drafts and the ten *Redline controls* rows, and one revise round on `opinion-flawed` and `web-copy-clean`. The pre-change arm was staged from `81f50bfd`, the branch head when #398's build began. The post-change arm was staged from `3891c4c5`, which carries the first wording, and the revise round from `3f5f8c30`, which carries the revised wording. The method is [#383's](../editorial-383/plan.md) as [#397's](../editorial-397/plan-amendment.md) and [#402's](../editorial-402/plan.md) last applied it. It was frozen for this ticket in [`../editorial-398/plan.md`](../editorial-398/plan.md), the whole evaluation is written up in [`../editorial-398/results.md`](../editorial-398/results.md), and every run's packet is under [`../editorial-398/runs/`](../editorial-398/runs/).

Each run was a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), with the Formal Invocation as its whole prompt and the editorial Skills and the Manager staged by `git archive` into a private root of its own. Every artefact was judged by two fresh judges, blind to the arm, the model and the ticket, using #383's briefs unchanged. No Codex Harness and no GPT model was started, controlled or invoked.

Three criteria are this evaluation's own: **`A2`**, read as the plan reads it — a judge's miss counts only where it turns on the claim account's assurance or on a claim the run added that the reply does not report as one, and one judge is enough — **`O1`** and **`S1`**. `R1` on the drafts and `C1` on the controls are recorded as the judges give them and not scored. A clean control was run once per arm to a response target, as the ticket fixes; the protocol's file-target run was not made.

## `pre-column-sv-r1`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with `Mallen` → `Mötesmallen` in the headline and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a miss; both find *Inget påstående har tagits bort eller ändrats* true.
  - `R1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-column-sv-r2`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with its headline rewritten and the dash corrected; missing parts reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *inga påståenden har tagits bort eller ändrats* true; judge B notes the new headline states what the old one only alluded to, supported by the body.
  - `R1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — `R1` misses on a working headline reworded (#429).

## `pre-opinion-en_GB-r1`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the byline moved up, `Lervik's` added to the lead and two subheadings rewritten; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — both judges: *Claims: no claim was removed or changed* is inaccurate against the third subheading, which narrows the survey to why people ring — the assurance.
  - `R1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — The defect this ticket was filed for, reproduced.

## `pre-opinion-en_GB-r2`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with headline, byline, lead, a term and one claim changed; the narrowed claim reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; judge B finds the byline's stated reason wrong (#400).
  - `R1` — recorded, not scored — judges pass / fail; met, split by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Judge B fails `R1` on the narrowed `cost of the work`, which the reply reports as a changed claim.

## `pre-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged after its round was rejected, and the reply's account, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed article, byline and sections reported, standfirst and ending rewritten, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — judge B: the standfirst's *vad artikeln tar upp* is not flagged as newly authored content, and the new closing sentence is not said to be an inference — an added claim not reported as one.
  - `C1` — recorded, not scored — judges pass / fail; met, split by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with headline, standfirst, lead and last subheading rewritten, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — both judges: *lika stark som den* is inaccurate for a headline that drops Lind's *men* — the assurance.
  - `C1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — `C1` misses as #399 records.

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired case study, byline and call to action reported missing, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; judge A: `kundens` → `Elm Quays` unreported, no claim moved.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with its headline rewritten and a new ending subheading, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; both judges find the headline's stated reason inaccurate and the section deviation self-caused (#402).
  - `C1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with a new headline and the generic opening and ending removed, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with *som kan ske i september* added to the lead, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; *inget påstående fick ändrad räckvidd, säkerhet eller innebörd* judged accurate.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged after its round was rejected, every finding reported unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged, one unresolved finding, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, pre arm, staged from `81f50bfd`
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the regrouped page with a new headline, removals and a relabelled link, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — The headline carries the *booking* inference, reported only as a changed headline; neither judge counted it.

## `post-column-sv-r1-a`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline naming *Bibliotekets mötesmall* and *rutor*; missing parts reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Utöver den ändrade rubriken ovan har inget påstående tagits bort, ändrats eller lagts till* true; *den obestämda* is a wrong label (#435).
  - `R1` — recorded, not scored — judges pass / fail; met, split by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #435
- **notes** — none

## `post-column-sv-r1-b`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline naming the library's template and *rutor*, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; both judges: *en ruta* → *rutor* not reported, only the subject half of the headline change (#400).
  - `R1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-a`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with its headline rewritten, reported as a changed claim, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Inga andra påståenden har tagits bort, ändrats eller lagts till* true.
  - `R1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — `R1` misses on #429's headline.

## `post-column-sv-r2-b`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with its headline rewritten, reported as a changed claim, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Utöver den ändrade rubriken har inga påståenden tagits bort, ändrats eller lagts till* true.
  - `R1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — `R1` misses on #429's headline.

## `post-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the byline moved, `administration` → `officers` twice and two subheadings reworded, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Removed and added: nothing* accurate.
  - `R1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with `Lervik's` in the lead, *two separate workflows*, the byline moved and a subheading rewritten, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Removed: none*, *Added: none* accurate; judge B calls the subheading's note broadly fair.
  - `R1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — `R1` misses on taste rewrites of working text.

## `post-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with `By`, the two routes named in the lead and `The municipal executive board`, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *no claim was removed, weakened or added* true; the byline's reason overstates (#400).
  - `R1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, post arm, staged from `3891c4c5`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with headline, byline, a term and one claim changed, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Removed: nothing. Added: nothing.* accurate; judge A: *stays at 52 characters* for 56 (#435).
  - `R1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #435
- **notes** — none

## `post-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged after its round was rejected, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired article with four added claims listed under *Tillagda*, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges: every difference reported; one word names two blocks (#435).
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #435
- **notes** — none

## `post-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with headline, standfirst, lead and last subheading rewritten, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; both judges: the changed headline's lost reservation is not said (#400).
  - `C1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — `C1` misses as #399 records.

## `post-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired case study with added claims listed and a new ending subheading, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss counted; *flyttats* for a heading set over lines (#435).
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #435
- **notes** — none

## `post-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with a new headline and four removals, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Inga påståenden har lagts till* true.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with *Bytet kan ske i september.* added, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no miss.
  - `C1` — recorded, not scored — judges fail / pass; met, split by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Judge A fails `C1` on the added sentence, which the reply reports.

## `post-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired piece with an ending section and one added claim listed, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — judge B: *Utöver de påståenden som redovisas ovan är inga påståenden borttagna, ändrade eller tillagda* is *a little too absolute* over the gloss *för två bokningsvägar* — the assurance.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — A regression against the pre-change run, taken into the revise round.

## `post-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page with *inom tre arbetsdagar* copied from a heading into the body, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — both judges: *har bara flyttats ner i stycket* is false for a copy, and the reply's closing paragraph says *också* — the assurance.
  - `C1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — A regression against the pre-change run, taken into the revise round; `C1` misses as #432 records.

## `post-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, post arm, staged from `3891c4c5`
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the regrouped page with the *booking* inference listed under *Claims added*, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find the added claim reported accurately.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #435
- **notes** — *The six unhelpful headings are gone* for one replaced (#435).

## `revise-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, revise arm, staged from `3f5f8c30`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged after its round was rejected for a headline echo, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Den levererade texten är byte för byte identisk … Inget påstående har tagits bort, ändrats eller lagts till* true.
  - `C1` — recorded, not scored — judges pass / pass; met by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No changed text for the revised sentences to describe.

## `revise-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, revise arm, staged from `3f5f8c30`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page with *inom tre arbetsdagar* copied into the body, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — both judges find *Den står nu också i brödtexten, med samma omfattning och säkerhet* accurate; a quotation placed under the wrong heading (#435).
  - `C1` — recorded, not scored — judges fail / fail; missed by #397's split rule.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `R1` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #435
- **notes** — `C1` misses as #432 records.
