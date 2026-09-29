# redline — claude — 2026-09-29 — #432

- **record** — `redline-claude-2026-09-29-432`
- **date** — `2026-09-29` (UTC)
- **ticket** — `#432`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.285
- **corpus commit** — `e7773344`

## Run conditions

Two arms over the same three inputs: `web-copy-clean`, `web-copy-flawed`, and the `web-copy-sv` pipeline. The pre-change arm was staged from `e7773344`, the branch head when #432's build began. The candidate arm was staged from `a1453560`, which carries the candidate. The method is [#397's](../editorial-397/plan.md) as [its amendment](../editorial-397/plan-amendment.md) makes a run, frozen for this ticket in [`../editorial-432/plan.md`](../editorial-432/plan.md) (`8575d6d2`) before the first run. The whole evaluation is written up in [`../editorial-432/results.md`](../editorial-432/results.md), and every run's packet is under [`../editorial-432/runs/`](../editorial-432/runs/).

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), with the Formal Invocation as its whole prompt. The editorial Skills and the Manager are staged by `git archive` into a private root of the run's own. `web-copy-clean` is run as the protocol's clean control: three pairs per arm, each pair one response-target run and one file-target run, the file-target run kept with `--capture-output-name=output.md`. Every Redline run was judged by two fresh judges, blind to the arm, the model and the ticket. A file-target run was judged on [`../editorial-432/control-judge-brief-file-target.md`](../editorial-432/control-judge-brief-file-target.md), which sees `output.md`. Where two judges split, #397's rule decides; no run's judges split. No Codex Harness and no GPT model was started, controlled or invoked.

This evaluation's criteria are **`C1`** (`R1` against the row's frozen expectation) on the two controls, **`R1`** on the pipeline's Redline half, **`O1`** and **`S1`**. One run the evaluator's launcher started out of order was cut off after sixteen seconds. It is kept under [`../editorial-432/voided/`](../editorial-432/voided/) and has no entry here.

## `pre-web-copy-clean-response-1`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, pair 1's response-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page in the reply with one sentence extended, one resolved finding and one unresolved finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: *inom tre arbetsdagar* copied from the subheading `Svar inom tre arbetsdagar` into the sentence under it, a change of taste against *Short headings … work*, and the page's form reported as missing. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432 (the defect this evaluation reproduces)
- **notes** — Carries both target misses: the reply's *Olöst … Sidan innehåller dock inte formuläret, länkar inte till det och säger inte var det finns*, and the copied reply time.

## `pre-web-copy-clean-file-1`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, pair 1's file-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed page written to `output.md` with the body under the last subheading changed, and the account in the reply.
- **side effects** — `work/output.md` created, as the output target asks; the runner's inventories show `work/input.md` unchanged, nothing else created, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: *inom tre arbetsdagar* copied from the subheading `Svar inom tre arbetsdagar` into the sentence under it, a change of taste against *Short headings … work*, and the page's form reported as missing. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — `work/output.md`, the file the invocation asked for, is the one path created; nothing else outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432 (the defect this evaluation reproduces)
- **notes** — Carries both target misses: the reply's *Formuläret finns inte i texten, och texten säger inte var det finns eller hur läsaren når det*, and `output.md`'s copied reply time.

## `pre-web-copy-clean-response-2`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, pair 2's response-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page in the reply with one sentence extended, one resolved finding and one unresolved finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: *inom tre arbetsdagar* copied from the subheading `Svar inom tre arbetsdagar` into the sentence under it, a change of taste against *Short headings … work*, and the page's form reported as missing. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432 (the defect this evaluation reproduces)
- **notes** — Carries both target misses: the reply's *Kvarstår: formuläret har ingen angiven plats*, and the copied reply time.

## `pre-web-copy-clean-file-2`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, pair 2's file-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed page written to `output.md` with the body under the last subheading changed, and the account in the reply.
- **side effects** — `work/output.md` created, as the output target asks; the runner's inventories show `work/input.md` unchanged, nothing else created, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: *inom tre arbetsdagar* copied from the subheading `Svar inom tre arbetsdagar` into the sentence under it, a change of taste against *Short headings … work*, and the page's form reported as missing. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — `work/output.md`, the file the invocation asked for, is the one path created; nothing else outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432 (the defect this evaluation reproduces)
- **notes** — Carries both target misses: the reply's *texten säger inte var det finns*, and `output.md`'s copied reply time.

## `pre-web-copy-clean-response-3`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, pair 3's response-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page in the reply with one sentence extended, one resolved finding and one unresolved finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: *inom tre arbetsdagar* copied from the subheading `Svar inom tre arbetsdagar` into the sentence under it, a change of taste against *Short headings … work*, and the page's form reported as missing. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432 (the defect this evaluation reproduces)
- **notes** — Carries both target misses: the reply's *Olöst: formuläret anges inte*, and the copied reply time.

## `pre-web-copy-clean-file-3`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre-change arm, pair 3's file-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed page written to `output.md` with the body under both subheadings changed, and the account in the reply.
- **side effects** — `work/output.md` created, as the output target asks; the runner's inventories show `work/input.md` unchanged, nothing else created, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both judges: *inom tre arbetsdagar* copied from the subheading `Svar inom tre arbetsdagar` into the sentence under it, a change of taste against *Short headings … work*, and the page's form reported as missing. A substantive edit.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — `work/output.md`, the file the invocation asked for, is the one path created; nothing else outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the form's location
- **defects filed** — #432 (the defect this evaluation reproduces)
- **notes** — Carries both target misses: the reply's *Olöst: texten innehåller inte formuläret och säger inte heller var det finns*, and `output.md`'s *Svale svarar på intresseanmälan via e-post inom tre arbetsdagar*. It also wrote *formuläret för intresseanmälan* for *formuläret* twice, which both judges count as taste.

## `post-web-copy-clean-response-1`

- **fixture** — `web-copy-clean` from the *Redline controls* table, candidate arm, pair 1's response-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status alone; no text delivered and no finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target entry of the same pair answers the criterion. Both judges pass it, and the reply names no finding, so it carries no target miss.
  - `R1` — see `C1`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No target miss.

## `post-web-copy-clean-file-1`

- **fixture** — `web-copy-clean` from the *Redline controls* table, candidate arm, pair 1's file-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the page written to `output.md`, byte-identical to `input.md`, and a reply with no finding.
- **side effects** — `work/output.md` created, as the output target asks; the runner's inventories show `work/input.md` unchanged, nothing else created, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: `output.md` is identical to `input.md`, the short headings and the page's own form left as they are.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — `work/output.md`, the file the invocation asked for, is the one path created; nothing else outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No target miss.

## `post-web-copy-clean-response-2`

- **fixture** — `web-copy-clean` from the *Redline controls* table, candidate arm, pair 2's response-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status alone; no text delivered and no finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target entry of the same pair answers the criterion. Both judges pass it, and the reply names no finding, so it carries no target miss.
  - `R1` — see `C1`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No target miss.

## `post-web-copy-clean-file-2`

- **fixture** — `web-copy-clean` from the *Redline controls* table, candidate arm, pair 2's file-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the page written to `output.md`, byte-identical to `input.md`, and a reply with no finding.
- **side effects** — `work/output.md` created, as the output target asks; the runner's inventories show `work/input.md` unchanged, nothing else created, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: `output.md` is identical to `input.md`, the short headings and the page's own form left as they are.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — `work/output.md`, the file the invocation asked for, is the one path created; nothing else outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No target miss.

## `post-web-copy-clean-response-3`

- **fixture** — `web-copy-clean` from the *Redline controls* table, candidate arm, pair 3's response-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status alone; no text delivered and no finding.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target entry of the same pair answers the criterion. Both judges pass it, and the reply names no finding, so it carries no target miss.
  - `R1` — see `C1`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No target miss.

## `post-web-copy-clean-file-3`

- **fixture** — `web-copy-clean` from the *Redline controls* table, candidate arm, pair 3's file-target run
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the page written to `output.md`, byte-identical to `input.md`, and a reply with no finding.
- **side effects** — `work/output.md` created, as the output target asks; the runner's inventories show `work/input.md` unchanged, nothing else created, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: `output.md` is identical to `input.md`, the short headings and the page's own form left as they are.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — `work/output.md`, the file the invocation asked for, is the one path created; nothing else outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — No target miss.

## `pre-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, pre-change arm
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired page in the reply, regrouped into two sections, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met, and heading 3 records the reply's finding 5 on the misleading *Book and pay now* link.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — The run also turned *working days* into *business days* under a finding of its own, which both judges read as a locale form.

## `post-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, candidate arm
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the repaired page in the reply, regrouped into three sections, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; both judges: every clause met, and heading 3 records the reply's point 3 on the misleading *Book and pay now* link.
  - `R1` — see `C1`, which is `R1` against the row.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Meets its reading in both arms, so it does not regress.

## `pre-web-copy-sv-write`

- **fixture** — `web-copy-sv`, the pipeline's Write half, pre-change arm
- **invocation** — `/write --genre=webcopy --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish service page with its `kntnt` map in a fenced block in the reply, and the run's account; the draft is kept as `draft.md` in the packet.
- **side effects** — `none`: the runner's inventories of the private root show `work/source.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `source.md` was the only file in the working directory when the session started.
  - every other criterion — `skipped` — the Write half stages the Redline half's input and is not judged.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Not judged, by the plan.

## `pre-web-copy-sv-redline`

- **fixture** — `web-copy-sv`, the pipeline's Redline half on the draft that arm's Write run delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status alone.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: no visible defect in the draft that the reply leaves unreported. The pipeline's Redline half is not a clean control, so the no-change reply is read against `R1` as it stands.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Meets its reading in both arms, so it does not regress.

## `post-web-copy-sv-write`

- **fixture** — `web-copy-sv`, the pipeline's Write half, candidate arm
- **invocation** — `/write --genre=webcopy --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish service page with its `kntnt` map in a fenced block in the reply, and the run's account; the draft is kept as `draft.md` in the packet.
- **side effects** — `none`: the runner's inventories of the private root show `work/source.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `source.md` was the only file in the working directory when the session started.
  - every other criterion — `skipped` — the Write half stages the Redline half's input and is not judged.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Not judged, by the plan.

## `post-web-copy-sv-redline`

- **fixture** — `web-copy-sv`, the pipeline's Redline half on the draft that arm's Write run delivered, candidate arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status alone.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both judges: no visible defect in the draft that the reply leaves unreported. The pipeline's Redline half is not a clean control, so the no-change reply is read against `R1` as it stands.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Meets its reading in both arms, so it does not regress.
