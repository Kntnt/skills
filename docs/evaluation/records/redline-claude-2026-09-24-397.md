# redline — claude — 2026-09-24 — #397

- **record** — `redline-claude-2026-09-24-397`
- **date** — `2026-09-24`
- **ticket** — `#397`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.281
- **corpus commit** — `a321690f`

## Run conditions

Two arms over the same fourteen inputs: the four #362 drafts and the ten *Redline controls* rows. The pre-change arm was staged from `20133068`, the branch head when #397's build began; the post-change arm from `d1be1731`, which carries the candidate. The method is [#383's](../editorial-383/plan.md), frozen for this ticket in [`../editorial-397/plan.md`](../editorial-397/plan.md) and amended before the first valid run by [`../editorial-397/plan-amendment.md`](../editorial-397/plan-amendment.md); the whole evaluation is written up in [`../editorial-397/results.md`](../editorial-397/results.md), and every run's packet is under [`../editorial-397/runs/`](../editorial-397/runs/).

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt, the editorial Skills and the Manager staged by `git archive` into a private root of its own. The runs were not subagents of the evaluating session, as #383's were, because that session is itself a subagent and cannot give a run the means to start a correction subagent; eight runs first made that way are voided and kept under [`../editorial-397/voided/`](../editorial-397/voided/). Every artefact was judged by two fresh judges blind to the arm, the model and the ticket, with #383's briefs unchanged; where they split, #383's counting rule decides. No Codex Harness and no GPT model was started, controlled or invoked.

Four criteria are this evaluation's own: **`R1`** on the drafts, **`C1`** — `R1` against the row's frozen expectation — on the controls, **`O1`** and **`S1`**. A clean control was run once per arm to a response target, as the ticket fixes; the protocol's file-target run was not made.

## `pre-column-sv-r1`

- **fixture** — the `column-sv-r1` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed column in the reply with its `kntnt` map, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; both judges: a third-person standfirst, three subheadings and a closing call to action in the author's voice written into a column that had none; the call to action moves the writer's own trial to advice to the reader, by scope. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #397 (the defect this evaluation reproduces)
- **notes** — One of the four runs that reproduce the defect.

## `pre-column-sv-r2`

- **fixture** — the `column-sv-r2` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed column in the reply with its `kntnt` map, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; both judges: a standfirst, two subheadings and a call to action inside the last paragraph written in, and the headline replaced. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #397
- **notes** — Reproduces the defect.

## `pre-opinion-en_GB-r1`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed opinion piece in the reply with its `kntnt` map, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; both judges: a new lead paragraph written after the moved byline, the headline reworded to fit the band, two paragraphs split. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #397
- **notes** — Reproduces the defect.

## `pre-opinion-en_GB-r2`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed opinion piece in the reply with its `kntnt` map, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; both judges: a standfirst written above the byline and the headline reworded to fit the band, moving its claim by chronology. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #397
- **notes** — Reproduces the defect.

## `pre-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input unchanged in the reply, the one round rejected by the run's re-review, and two unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: byte-identical to the input; every preservation clause met, no rejected finding made.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — two headline and subheading findings
- **defects filed** — none
- **notes** — none

## `pre-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input unchanged in the reply, the one round rejected, and fourteen unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause reported, byline reported and left unfilled, navigation reported and not written, nothing deleted.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — fourteen, the missing byline, subheadings and ending among them
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the input in the reply with one mechanical word-order correction, the one round rejected, and six unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the only difference is the mechanical pass's; every clause met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — six
- **defects filed** — none
- **notes** — Run last, after the shared lock was released.

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired case study in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause met; missing byline and call to action reported, neither written.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing byline, the missing call to action, and gaps the genre asks the text to fill
- **defects filed** — none
- **notes** — none

## `pre-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: nothing changed, no finding, every clause met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `pre-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired column in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: a 46-word standfirst written where the row requires it reported and not written, and the missing call to action never reported. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing subheadings, sections and ending, and the first paragraph contradicting itself
- **defects filed** — none (the behaviour #397 changes)
- **notes** — The row as `a321690f` revised it.

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece in the reply with one clause added to the lead, and one unresolved finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / fail; split: judge B fails the added *september* clause as taste; it is covered in the closing summary, so by the plan's split rule `C1` is met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — one: the closing sentence promises more than the proposed trial measures
- **defects filed** — #431
- **notes** — Not unchanged.

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired opinion piece in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause met, the ending repaired from the body's actor and act; the missing ending section unreported (#402).
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — two: the association's demand now the writer's own, and what a booking counts
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page in the reply with one sentence extended, and one unresolved finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: a heading's reply time copied into the body as a repair, and a missing form link reported as a defect, against *Short headings … work*. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432
- **notes** — none

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired page in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met; price, scope, timing, deliverables, conditions and destination preserved.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-column-sv-r1-a`

- **fixture** — the `column-sv-r1` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column in the reply, changed only by the mechanical pass's dash, with three unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: one mechanical difference; the absent standfirst, sections and call to action reported and left unwritten.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst, the absent sections (the seven-paragraph lead named as caused by them), the absent call to action
- **defects filed** — none
- **notes** — none

## `post-column-sv-r1-b`

- **fixture** — the `column-sv-r1` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column in the reply with a reworded headline, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; both judges: the working headline `Mallen …` reworded to `Bibliotekets mötesmall har rutor …` on a *not understood on its own* finding, `en ruta` → `rutor` unreported; taste on a clean text. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst, sections and call to action
- **defects filed** — #429
- **notes** — No absent part was written; the miss is the headline.

## `post-column-sv-r2-a`

- **fixture** — the `column-sv-r2` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column in the reply, changed only by the mechanical pass's dash, with unresolved findings.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: one mechanical difference; a headline rewrite the run attempted was rejected by its own re-review; absent parts reported.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the headline finding, the absent standfirst, sections and call to action
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-b`

- **fixture** — the `column-sv-r2` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column in the reply with a reworded headline, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; both judges: the working headline `Rutan som inte finns` reworded to `Bibliotekets mötesmall har ingen ruta för mötets syfte` on an *unclear* finding, changing meaning (*syfte* against *beslut*). A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst, sections and call to action
- **defects filed** — #429
- **notes** — No absent part was written; the miss is the headline.

## `post-opinion-en_GB-r1-a`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: the closing sign-off moved into place as the byline, `Lervik` added to the lead, one subheading reworded for repeating the sentence under it; every limit verbatim.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r1-b`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / fail; split: judge B fails the reworded subheading and two paragraph splits as taste and length; both are covered in the reply's closing summary, so by the plan's split rule the run meets `R1`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst
- **defects filed** — none
- **notes** — Both readings recorded; the splits are grounded in where evidence ends and argument begins.

## `post-opinion-en_GB-r2-a`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: `By` added to the byline, the lead's second route named, a pronoun given its antecedent; the ten-word headline kept, the reply saying it meets its requirements.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r2-b`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, post-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: `By` added, *the telephone* → *telephone booking* in the headline, a pronoun given its antecedent; the absent standfirst reported, not written.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the absent standfirst
- **defects filed** — none
- **notes** — none

## `post-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article in the reply with a rewritten headline and first subheading, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: the headline, the first subheading and a standfirst word rewritten on a clean text as taste. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #430
- **notes** — Passed before the change.

## `post-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired article in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: byline reported and left unfilled, missing subheadings and ending reported and not written, no measured fact, exclusion or funding uncertainty deleted.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing byline, sections and ending
- **defects filed** — none
- **notes** — none

## `post-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study in the reply with a rewritten headline, last subheading and standfirst, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: conforming headline, subheading and standfirst rewritten as taste on a clean text. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #399 (recorded under it)
- **notes** — Passed before the change.

## `post-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired case study in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause met; the missing byline and call to action reported, neither written; both subheadings replaced, their defect named only generally (#400).
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing background, byline and call to action
- **defects filed** — none
- **notes** — none

## `post-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column in the reply with a rewritten headline.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: the headline's hyperbole read as an overclaim and replaced on a clean text. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #430
- **notes** — Passed before the change.

## `post-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired column in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: the standfirst and call to action reported and not written, the contradiction reported without an invented memory, the reflection and doubt verbatim.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — five: the missing standfirst, sections and call to action, the self-contradicting personal account, and the opening scene not joining the reflection
- **defects filed** — none
- **notes** — Missed before the change.

## `post-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece in the reply with one clause added to the lead.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges fail / pass; split: judge A fails the added *september* clause as taste; it is covered in the closing summary, so by the plan's split rule `C1` is met.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #431
- **notes** — Not unchanged.

## `post-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired opinion piece in the reply, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every detection clause met, the standfirst reported and not written, the ending repaired from the body; the missing ending section unreported (#402).
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — four: the missing standfirst, unsourced figures, the matter never presented, and which association is meant
- **defects filed** — none
- **notes** — none

## `post-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page in the reply with one sentence extended, and one unresolved finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: as before the change. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432
- **notes** — none

## `post-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, post-change arm
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired page in the reply, and the run's account.
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
