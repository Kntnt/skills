# redline — claude — 2026-09-24 — #400

- **record** — `redline-claude-2026-09-24-400`
- **date** — `2026-09-24` for the first eight runs of each arm; `2026-09-28` for the rest, which are six pre-change runs, ten post-change runs and the twelve #392 row runs. The record keeps the name the frozen plan fixed.
- **ticket** — `#400`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.281
- **corpus commit** — `c211a1d5`

## Run conditions

Two arms over the four #362 drafts and the ten *Redline controls* rows, and up to three runs on each of the four #392 rows. The pre-change arm was staged from `c211a1d5`, the branch head when #400's build began. The post-change arm and the #392 rows were staged from `c4c7b5e5`, the candidate. The method is [#383's](../editorial-383/plan.md), frozen for this ticket in [`../editorial-400/plan.md`](../editorial-400/plan.md) and amended in [`../editorial-400/plan-amendment.md`](../editorial-400/plan-amendment.md). The whole evaluation is written up in [`../editorial-400/results.md`](../editorial-400/results.md), and every counted run's packet is under [`../editorial-400/runs/`](../editorial-400/runs/).

Each run was a fresh top-level Claude Code session started by [`../editorial-400/runs/turn_run_2.sh`](../editorial-400/runs/turn_run_2.sh), not by `staged_run.py`. Its prompt was the arm's turn file and a three-line message naming the working directory, the invocation the user typed and the run directory. The script gave each session a private root of its own, with the staged Proofread copied into its home so that Redline's dependency check is met, and removed that root on exit. Each run's `seats.tsv` names `claude-opus-5-5` alone. No Codex Harness and no GPT model was started, controlled or invoked.

Every main-matrix run was judged by two fresh `kntnt-opus-high` judges, blind to the arm, the model and the ticket, using #383's briefs unchanged. The #392 rows had the pair brief ready, #380's with the one sentence the readiness addendum appends to item 6. No pair judge was sent, because no row's change recurred in three runs.

The frozen plan was edited once, in `9ab8b40e` at 05:00:40 UTC on 2026-09-24, after six runs had started. The resumed build voided those six runs and ran them again on 2026-09-28; every counted run started after the edit. Runs and judges cut off by a usage limit were voided and made again too. *The frozen plan, and what the build voided* in results.md gives the timeline, and *Voided runs* below lists them.

This evaluation's criteria are `R1` on the drafts, `C1` on the controls, `A2`, `N2` on the drafts, `O1` and `S1`. `R1` and `C1` are the judges' verdicts, and where the two split, #383's rule decides. `A2` and `N2` read `pass` where results.md reads *met* and `fail` where it reads *missed*; one judge is enough for a miss. Each miss names its owner, and a miss owned by another ticket counts neither for nor against #400. The wave inventories show no run with a side effect outside its own run directory. In a #392 row's packet, `redline/delivered.md`, the two `anatomy-*.json` files and `write/work/source.md` are the evaluator's, added after the run returned. A clean control was run once per arm to a response target, as the ticket fixes; the protocol's file-target run was not made, a declared narrowing.

## `pre-column-sv-r1`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre arm, staged from `c211a1d5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Mallen har en ruta för allt utom poängen` rewritten as `Bibliotekets mötesmall har rutor för allt utom poängen` and one dash set as an en dash, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / fail; met by #383's split rule, because B's passage, the reworded headline, is in the claim account.
  - `A2` — `fail` — missed by A: the plural credited to the headline repair (#429); recorded under #429, not counted against #400.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — A first run under this name started before the plan edit and is voided.

## `pre-column-sv-r2`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre arm, staged from `c211a1d5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` rewritten as `Mötesmallen saknar en ruta för syftet` and one dash set as an en dash, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a working column headline rewritten on a defect the judges reject, #429's shape.
  - `A2` — `fail` — missed by B: the working headline presented as a defect, *syftet* presented as grounded (#429); not counted against #400.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — A first run under this name started before the plan edit and is voided.

## `pre-opinion-en_GB-r1`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre arm, staged from `c211a1d5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the byline moved under the headline, the administration's actions given to its officers, and the third subheading rewritten as `Measure the staff time, and ask why people ring`; the headline unchanged, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the opinion subheading rewritten on a defect both judges reject, #436's shape.
  - `A2` — `fail` — missed: *one verb* for two, by both (#435); the byline's reason, by A (#435); the anatomy statement, by A (#402); none counted against #400.
  - `N2` — `pass` — met; judge B's *accurate but incomplete* on the subheading recorded, not counted.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 1 of the plan: not exercised. The headline `Don't switch off Lervik's phone booking before we know what it costs` came back unchanged, so nothing here measures the `Lervik's` narrowing the ticket was filed for. A first run under this name started before the plan edit and is voided.

## `pre-opinion-en_GB-r2`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre arm, staged from `c211a1d5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline's `Keep the telephone` made `Keep telephone venue booking`, the byline given the `By` form, `telephone and web` added to the lead, `channels` made `routes` and `It can adopt` made `The board can adopt`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `A2` — `fail` — missed by both: *the English form* for the byline (#435); not counted against #400.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — A first run under this name started before the plan edit and is voided.

## `pre-control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned; a short reply saying no change was needed.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Passes the pre-change arm.

## `pre-control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline `Givarna räddar skolan från en katastrof` replaced by `Mätförsök i Björkskolan fann värden under 20 grader`, the standfirst's duplicate removed and its first sentence rewritten, a sentence added to it, the health claim and `medan` removed, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 4 of the plan: met, with `C1`, `A2`, `O1` and `S1` all passing. The reply names the removed headline claim and the lost `medan`: *Sambandet ”medan” … är borta*.

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the third subheading `Kunden vill ge förberedelserna mer tid` rewritten as `Maya Lind ser tillbaka på reparationsloggen`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both decide on the rewritten subheading, a working one changed on a defect the text does not have.
  - `A2` — `fail` — missed by both: the subheading's defect is not in the text (no owner; #436); it counts against the run.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — #436
- **notes** — Fails the pre-change arm, so the regression clause does not reach it.

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text returned byte for byte after the run rejected its only correction round, every finding reported unresolved, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 2 of the plan: not exercised. Both subheadings stand.

## `pre-control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-28
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned; a short reply saying no change was needed and `input.md` is untouched.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Passes the pre-change arm. A first run under this name started before the plan edit and is voided.

## `pre-control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-28
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Möten förändrar allt` replaced by `Mötesmallen saknar plats för det vi ska förstå tillsammans` and three empty formulas removed, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 3 of the plan: exercised and met. The reply names the defect, *Rubriken ”Möten förändrar allt” påstod något som texten aldrig hävdar*, and lists the headline under *Ändrade*. Both judges note that no finding names the headline's other defect, that it names no subject of its own, and score it as partial detection, not as an inaccurate account. A first run under this name started before the plan edit and is voided.

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with `, ett byte som kan ske i september` added to the lead and `webbokningar` corrected to `webbbokningar`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — The lead edit is the one #431 was filed for. This run's judges pass it; `control-opinion-clean`'s judges fail the same edit.

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline `Kommunledningen hatar människor` replaced by `Telefonbokningen bör finnas kvar i ett halvår`, `Bakgrund` and `Diskussion` rewritten, a closing subheading added and the closing line rewritten, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `fail` — missed by A: *togs bort* for a rewritten closing line, outside the claim account (#435); not counted against #400.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Passes the pre-change arm: the one miss is #435's.

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned; a one-sentence reply saying no change was needed.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Passes the pre-change arm.

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, pre arm, staged from `c211a1d5`, made 2026-09-24
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page with the headline `Unlock your association's full potential` replaced, the six empty subheadings replaced by two descriptive ones and the opening paragraph removed, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Passes the pre-change arm.

## `post-column-sv-r1-a`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline rewritten as `Vår mötesmall har rutor för allt utom poängen` and one dash set as an en dash, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `A2` — `fail` — missed by B: the plural credited to the headline repair (#429); not counted against #400.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `post-column-sv-r1-b`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline rewritten as `Mötesmallen har en ruta för allt utom poängen` and one dash set as an en dash, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-a`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` rewritten as `Mötesmallen frågar inte varför vi behöver varandras tid` and one dash set as an en dash, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a working column headline rewritten on a defect the judges reject, #429's shape.
  - `A2` — `fail` — missed by A: *Brödtexten bär påståendet* overstates the support (#429); not counted against #400.
  - `N2` — `fail` — missed by A: the headline's *varför* moved from the agenda to the template, unreported (#429); not counted against #400.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-b`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline rewritten as `Bibliotekets mötesmall frågar efter tid men inte syfte` and one dash set as an en dash, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a working column headline rewritten on a defect the judges reject, #429's shape.
  - `A2` — `pass` — met.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — The first two judges were cut off by the usage limit. The run was judged again by fresh judges, and the first judges' files are kept unread under `../editorial-400/voided/judges-cut-off/`.

## `post-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the byline moved under the headline, the administration's actions given to its officers, and the third subheading rewritten as `Running phone and web side by side would put numbers on the work`; the headline unchanged, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 1 of the plan: not exercised, because the headline came back unchanged. The subheading was rewritten on a defect the judges reject, without an `A2` miss; results.md counts it with #436's shape.

## `post-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the byline moved under the headline, two paragraphs split, and the third subheading rewritten as `Find out why people still phone before deciding for good`; the headline unchanged, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the opinion subheading rewritten on a defect both judges reject, #436's shape, and two paragraphs split against an 80-word guideline.
  - `A2` — `fail` — missed by both: the subheading's defect, *repeated the first sentence under it in the same words*, is not in the text (no owner; #436); *seven paragraphs*, by B (#435).
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — #436
- **notes** — Kept the same headline as `post-opinion-en_GB-r1-a`. The first attempt at this run stopped on the usage limit and is voided.

## `post-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline `Keep the telephone until Lervik knows why it is used` rewritten as `Keep venue phone booking until Lervik knows why it's used`, the byline given the `By` form and `can adopt` made `is free to adopt`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `A2` — `fail` — missed by both: the headline's contraction `it's` not reported (#400's shape; #437).
  - `N2` — `pass` — met; judge B's *can* → *is free to* recorded, not counted, because B marks it reported accurately.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — #437
- **notes** — The one miss of #400's own shape in the post-change arm. The reply reports the headline change with its defect and what the headline now asserts, but not the contraction brought in with it. The run is not a target line, so it does not bear on the exit. Its first judges were cut off by the usage limit, and it was judged again by fresh judges.

## `post-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline rewritten as `Keep telephone booking until Lervik knows why it is used`, the byline given the `By` form and `The report does not measure it.` made `The report measures neither.`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `pass` — met.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `C1` — `skipped` — read on the controls only.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — The first attempt at this run stopped on the usage limit and is voided.

## `control-article-clean`

- **fixture** — `article-clean` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline `Mätförsöket i Björkskolan visar när, inte varför` rewritten as `Mätförsöket i Björkskolan visar när det var kallt, inte varför`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both call the stated defect taste, the headline rewrite #430 was filed for.
  - `A2` — `fail` — missed by both: the headline's stated defect is taste (#430); not counted against #400.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Passes the post-change arm under the regression clause, because both misses are #430's. The first attempt at this run stopped on the usage limit and is voided.

## `control-article-flawed`

- **fixture** — `article-flawed` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text returned byte for byte after the run rejected its only correction round, thirteen findings reported unresolved, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 4 of the plan: met, with `C1`, `A2`, `O1` and `S1` all passing. The findings name the standfirst/lead repetition and the shared opening word that #383's run left unnamed. No paratext changed, so the run does not exercise the paratext account. The first attempt at this run stopped on the usage limit and is voided.

## `control-case-study-clean`

- **fixture** — `case-study-clean` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the closing subheading `Kunden vill ge förberedelserna mer tid` rewritten as `Arbetsledaren ser tillbaka på försöket`, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both decide on the rewritten closing subheading.
  - `A2` — `fail` — missed by A: the subheading's defect is not in the text (no owner; #436); it counts against the run.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — #436
- **notes** — Outside the regression clause: the control fails the pre-change arm on the same shape. The first attempt at this run stopped on the usage limit and is voided.

## `control-case-study-flawed`

- **fixture** — `case-study-flawed` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the headline, the standfirst and both subheadings replaced, a subheading `Kundens slutomdöme` added and the causal sentence with `därför` removed, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 2 of the plan: exercised and met. `Kunden fick en gemensam bild` became `Arbetsledaren om ärendearbetet`, and `Resultatet bevisar allt` became `Tilldelningen gick fortare, men arbetsbelastningen var olika`. The reply gives each changed part a *Defekt:* line, lists the subheading's claim that the result proves everything among the removed claims, and names what went with `därför`: *Läsaren har alltså inte längre textens egen slutsats från anteckningen till programvaran.* The first attempt at this run stopped on the usage limit and is voided.

## `control-column-clean`

- **fixture** — `column-clean` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned; a short reply saying no change was needed, with a note that one 83-word paragraph is kept.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Its first judges were cut off by the usage limit, and it was judged again by fresh judges.

## `control-column-flawed`

- **fixture** — `column-flawed` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Möten förändrar allt` replaced by `Mötesmallen saknar plats för gemensam förståelse` and three empty sentences struck, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Line 3 of the plan: exercised and met. The reply names the defect, *påstod en slutsats som texten varken drar eller stöder, och i en starkare ton än texten själv*, and reports the changed claim by what the headline now asserts. As in the pre-change arm, both judges note that the headline's other defect, that it names no subject of its own, is not named, and score it as partial detection. The first attempt at this run stopped on the usage limit and is voided.

## `control-opinion-clean`

- **fixture** — `opinion-clean` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-24
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with `, ett byte som kan ske i september` added to the lead, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `fail` — judges fail / fail; both decide on the lead edit, the one #431 was filed for.
  - `A2` — `fail` — missed by both: the premise of the lead edit does not hold (#431); B's doubt about *lagts till* is #398's or #431's, not #400's.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Passes the post-change arm under the regression clause, because both misses are #431's. The pre-change run made the same edit and its judges passed it. Its first judges were cut off by the usage limit, and it was judged again by fresh judges. Judgement B was copied into the run a few seconds before its judge returned; the file matches the judge's final reply.

## `control-opinion-flawed`

- **fixture** — `opinion-flawed` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline `Kommunledningen hatar människor` replaced by `Telefonen bör finnas kvar som bokningsväg på prov`, `Bakgrund` and `Diskussion` rewritten and a closing subheading added, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Every change is reported, and both subheadings are reported with their defect. The first attempt at this run stopped on the usage limit and is voided.

## `control-web-copy-clean`

- **fixture** — `web-copy-clean` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned; a short reply saying no change was needed and nothing was written.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — The first attempt at this run stopped on the usage limit and is voided.

## `control-web-copy-flawed`

- **fixture** — `web-copy-flawed` from the *Redline controls* table, post arm, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page with the headline replaced by `Svale reviews a shared room in your housing association`, `Start` removed, the other five empty subheadings replaced by two descriptive ones and the opening paragraph cut, and the run's account.
- **side effects** — `response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** —
  - `C1` — `pass` — judges pass / pass.
  - `A2` — `pass` — met; judge B's *British wording* recorded, not counted, because B marks the report accurate.
  - `N2` — `skipped` — read on the draft runs only.
  - `O1` — `pass` — the run's inventories show only `response.md` added beside `work/`, with the staged install unchanged.
  - `S1` — `pass` — the working directory held `input.md` alone when the session started.
  - `A1`, `C2` — `skipped` — #383's own criteria: its closing summary and its control replay.
  - `T1`, `R2` — `skipped` — answered from a Harness trace; each session's transcripts were kept in the build's scratch packet and are not committed, and this evaluation fixes no criterion on them.
  - `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
  - `R1` — `skipped` — on a control it is read as `C1`.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — Every heading change is reported with its defect. The first attempt at this run stopped on the usage limit and is voided.

## `pair-article-sv-1`

- **fixture** — `article-sv`, the #392 row `docs/evaluation/editorial-380/runs/article-sv/redline/work/input.md`, run 1 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text returned unchanged after the run rejected its one correction round, a headline rewrite; the headline's repetition of the standfirst reported unresolved, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 36, `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`. Reading: kept (text returned unchanged), so the causal link of `därför` is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The first attempt at this run stopped on the usage limit and is voided.

## `pair-article-sv-2`

- **fixture** — `article-sv`, the #392 row `docs/evaluation/editorial-380/runs/article-sv/redline/work/input.md`, run 2 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text returned unchanged after the run rejected its one correction round, another headline rewrite; the same finding reported unresolved, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 36, `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`. Reading: kept (text returned unchanged), so the causal link of `därför` is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — none

## `pair-article-sv-3`

- **fixture** — `article-sv`, the #392 row `docs/evaluation/editorial-380/runs/article-sv/redline/work/input.md`, run 3 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline `Mätningen i Björkskolan pekar ut lektioner, inte orsaker` rewritten as `Björkskolans givare visar lufttemperatur, inte upplevd kyla` and the standfirst's `ett kort mätförsök` made `mätförsöket`, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 36, `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`. Reading: kept (line 36 verbatim; headline and one standfirst phrase changed), so the causal link of `därför` is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The row is `not reproduced` after three runs.

## `pair-article-pac-1`

- **fixture** — `article-pac`, the #392 row `docs/evaluation/editorial-380/runs/article-pac/redline/work/input.md`, run 1 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline rewritten as `Classroom temperature readings show which lessons to examine`, one verb made plural, and `no capacity` and `with its exclusions` taken out of the sentence before the named one, which now stands as a paragraph of its own; and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 32, `the report therefore presents lesson periods instead of one figure per day`. Reading: kept (delivered line 34), so the causal link of `therefore` is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The first attempt at this run stopped on the usage limit and is voided. The run removed bounding words the plan does not name, and its account says what the reader lost: *Limit taken out (finding 2): the words "with its exclusions" are gone. This sentence no longer reminds the reader that the count has to be read alongside what it leaves out.* Recorded, not scored.

## `pair-article-pac-2`

- **fixture** — `article-pac`, the #392 row `docs/evaluation/editorial-380/runs/article-pac/redline/work/input.md`, run 2 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline rewritten as `Classroom air temperatures show which lessons to examine`, `counts` made `is a count of`, and the sentence before the named one cut to `no norm, no target — so the figure is not a verdict`, the named sentence standing as a paragraph of its own; and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 32, `the report therefore presents lesson periods instead of one figure per day`. Reading: kept (delivered line 34), so the causal link of `therefore` is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The run removed bounding words the plan does not name, and its account says what the reader lost: *A reader just no longer sees capacity named as one of them.* Recorded, not scored.

## `pair-article-pac-3`

- **fixture** — `article-pac`, the #392 row `docs/evaluation/editorial-380/runs/article-pac/redline/work/input.md`, run 3 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline rewritten as `Classroom air temperatures show when to look closer` and the sentence before the named one rewritten without `no capacity` or `with its exclusions`, the named sentence standing as a paragraph of its own; and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 32, `the report therefore presents lesson periods instead of one figure per day`. Reading: kept (delivered line 34), so the causal link of `therefore` is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The run removed bounding words the plan does not name, and its account says what the reader lost: *Without it, this sentence no longer tells the reader that the figure stands together with its exclusions.* Recorded, not scored. The row is `not reproduced` after three runs.

## `pair-article-abt-1`

- **fixture** — `article-abt`, the #392 row `docs/evaluation/editorial-380/runs/article-abt/redline/work/input.md`, run 1 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with only the dash before Elin Rask's quotation set as an en dash, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 36, the subheading `Effekten av eventuella justeringar är inte mätt`. Reading: kept (delivered line 36), so the subheading's limit is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The first attempt at this run stopped on the usage limit and is voided.

## `pair-article-abt-2`

- **fixture** — `article-abt`, the #392 row `docs/evaluation/editorial-380/runs/article-abt/redline/work/input.md`, run 2 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the same dash set as an en dash and two sentences added saying what the text does not show, one of them under the named subheading; and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 36, the subheading `Effekten av eventuella justeringar är inte mätt`. Reading: kept, and a sentence added under it, so the subheading's limit is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The reply the run saved to `response.md` and the reply the Harness returned differ in wording, but not in what they report. Both are kept, the second as `redline/response.txt`.

## `pair-article-abt-3`

- **fixture** — `article-abt`, the #392 row `docs/evaluation/editorial-380/runs/article-abt/redline/work/input.md`, run 3 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with only the dash before Elin Rask's quotation set as an en dash, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 36, the subheading `Effekten av eventuella justeringar är inte mätt`. Reading: kept (delivered line 36), so the subheading's limit is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The row is `not reproduced` after three runs.

## `pair-opinion-sv-r2-1`

- **fixture** — `opinion-sv-r2`, the #392 row `docs/evaluation/editorial-380/runs/opinion-sv-r2/redline/work/input.md`, run 1 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text returned unchanged after the run rejected its one correction round; all four findings reported unresolved, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 26, `, inte om att de som ringer skulle vara lata eller dyra`. Reading: kept (text returned unchanged), so the clause's bound on the objection is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The first attempt at this run stopped on the usage limit and is voided.

## `pair-opinion-sv-r2-2`

- **fixture** — `opinion-sv-r2`, the #392 row `docs/evaluation/editorial-380/runs/opinion-sv-r2/redline/work/input.md`, run 2 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline `Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` rewritten as `Låt telefonbokningen av föreningslokaler stå kvar ett halvår` and a sentence introducing the pilot report put at the head of the first section, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 26, `, inte om att de som ringer skulle vara lata eller dyra`. Reading: kept (delivered line 26), so the clause's bound on the objection is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — none

## `pair-opinion-sv-r2-3`

- **fixture** — `opinion-sv-r2`, the #392 row `docs/evaluation/editorial-380/runs/opinion-sv-r2/redline/work/input.md`, run 3 of up to three, staged from `c4c7b5e5`, made 2026-09-28
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with `Föreningen` put before `Öppna beslut` in the standfirst, the first section's opening sentence reworded to introduce the pilot report, and `kanal` made `bokningsväg`, and the run's account.
- **side effects** — `redline/response.md` alone, the evaluator's capture the turn asks for: the run's inventories show `redline/work/input.md` unchanged, nothing else created in the run directory and the staged install unchanged; the private root was removed on exit.
- **criteria** — not judged — the change did not recur. Passage compared: input line 26, `, inte om att de som ringer skulle vara lata eller dyra`. Reading: kept (delivered line 26), so the clause's bound on the objection is still there.
  - `O1` — `pass` — the run's inventories show only `redline/response.md` added, with the staged install unchanged.
  - `S1` — `pass` — `redline/work/` held `input.md` alone when the session started.
  - the #392 criterion and the limit criterion — `skipped` — not judged — the change did not recur.
  - `R1`, `A2`, `N2`, `C1` — `skipped` — not judged — the change did not recur.
  - `A1`, `C2`, `T1`, `R2`, `N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not judged — the change did not recur.
- **unresolved findings** — as the reply lists them; see the run's `redline/response.md`
- **defects filed** — none
- **notes** — The row is `not reproduced` after three runs.

## Voided runs

None of these is a finding. Each is kept whole under [`../editorial-400/voided/`](../editorial-400/voided/), and *The frozen plan, and what the build voided* in [`../editorial-400/results.md`](../editorial-400/results.md) gives the timeline.

- **Unmet Proofread dependency** — [`../editorial-400/voided/unsatisfied-dependency/`](../editorial-400/voided/unsatisfied-dependency/). The fourteen pre-change runs first made with `turn_run.sh` on 2026-09-24 stopped at Redline's shim, because the private home had no Proofread. None reviewed the text. The amendment's `turn_run_2.sh` fixed the home.
- **Plan edited after the run started** — [`../editorial-400/voided/plan-edited-after-start/`](../editorial-400/voided/plan-edited-after-start/). `pre-column-sv-r1`, `pre-column-sv-r2`, `pre-opinion-en_GB-r1`, `pre-opinion-en_GB-r2`, `pre-control-column-clean` and `pre-control-column-flawed` started before `9ab8b40e` edited the plan. They and their twelve judgements are kept unread, and all six were run again on 2026-09-28.
- **Usage limit** — [`../editorial-400/voided/api-error/`](../editorial-400/voided/api-error/). Fourteen runs ended with `api_error` and a `<synthetic>` seat: `post-opinion-en_GB-r1-b`, `post-opinion-en_GB-r2-b`, the controls `article-clean`, `article-flawed`, `case-study-clean`, `case-study-flawed`, `column-flawed`, `opinion-flawed`, `web-copy-clean` and `web-copy-flawed`, and `pair-<row>-1` for all four rows. All were run again on 2026-09-28.
- **Judges cut off** — [`../editorial-400/voided/judges-cut-off/`](../editorial-400/voided/judges-cut-off/). Eight judges of `post-column-sv-r2-b`, `post-opinion-en_GB-r2-a`, `control-column-clean` and `control-opinion-clean` ended on the usage limit. The two of `post-column-sv-r2-b` had written a judgement file, which is kept there unread with the directory mapping. The four runs were judged again by fresh judges.
