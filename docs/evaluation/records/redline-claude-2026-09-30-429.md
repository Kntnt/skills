# redline — claude — 2026-09-30 — #429

- **record** — `redline-claude-2026-09-30-429`
- **date** — `2026-09-30`
- **ticket** — `#429`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.285
- **corpus commit** — `e7773344`

## Run conditions

Three installs over the same inputs. The pre-change arm was staged from `e7773344`, the branch head when #429's build began; the post-change arm from `c7f639c6`, #429's first candidate; the revise round from `2c5b191f`, the second candidate, which shipped. Both arms ran every row of the frozen run table: the four clean controls as three response-target and file-target pairs each, the three #362 drafts twice each, the four flawed controls once each, and #396's two `case-question` controls once each. The revise round ran every run, under the post-change arm's run names, of the six fixtures whose reading missed and the one control that regressed. The method is #397's as its amendment runs it, frozen for this ticket in [`../editorial-429/plan.md`](../editorial-429/plan.md); the whole evaluation is written up in [`../editorial-429/results.md`](../editorial-429/results.md), and every run's packet is under [`../editorial-429/runs/`](../editorial-429/runs/). Most runs of the first two arms were made on 2026-09-29; nine were cut off there by an expired login, are kept under [`../editorial-429/voided/`](../editorial-429/voided/), and were made again on 2026-09-30 with the revise round.

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt, the editorial Skills and the Manager staged by `git archive` into a private root of its own; each file-target run's delivered `output.md` is captured into its packet as `captured-output.md`. Every judged run was judged by two fresh judges blind to the arm, the model and the ticket, with #397's briefs, and a file-target clean-control run with the copy of #397's control brief the plan declares as its one change of method; where they split, #397's counting rule decides. #396's controls were read by the evaluating session from the reply. No Codex Harness and no GPT model was started, controlled or invoked.

Four criteria are this evaluation's own: **`R1`** on the drafts and the clean controls, **`C1`** — `R1` against the row's frozen expectation — on every judged control, **`O1`** and **`S1`**. A flawed control's entry also carries the plan's reading of its heading clauses, and a `case-question` entry whether #396's control fired. A response-target clean-control run that returned only the no-change status has its `R1` skipped, the file-target run of its pair answering the criterion.

## `pre-article-clean-resp-1`

- **fixture** — `article-clean`, the response-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; the reply's rejected round had reworded the headline.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-clean-resp-1/`.

## `pre-article-clean-file-1`

- **fixture** — `article-clean`, the file-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-clean-file-1/`.

## `post-article-clean-resp-1`

- **fixture** — `article-clean`, the response-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the standfirst's *ett kort försök* became *försöket*; both judges: a change of meaning. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #467
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-clean-resp-1/`.

## `post-article-clean-file-1`

- **fixture** — `article-clean`, the file-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-clean-file-1/`.

## `pre-article-clean-resp-2`

- **fixture** — `article-clean`, the response-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; its round was rejected.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-clean-resp-2/`.

## `pre-article-clean-file-2`

- **fixture** — `article-clean`, the file-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline `Mätförsöket i Björkskolan visar när, inte varför` became `Björkskolans givare visar när luften var kall, inte orsaken`; both judges: taste, and a change of attribution and meaning. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-clean-file-2/`.

## `post-article-clean-resp-2`

- **fixture** — `article-clean`, the response-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges pass / fail; split, missed: the failing verdict rests on no difference the reply covers; the text came back unchanged; judge B fails the reply's false finding against a subheading, which no difference carries. A substantive edit.
  - `C1` — `fail` — judges pass / fail; split, missed: the failing verdict rests on no difference the reply covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-clean-resp-2/`.

## `post-article-clean-file-2`

- **fixture** — `article-clean`, the file-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the standfirst's *ett kort försök* became *försöket*; both judges: a change of meaning. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #467
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-clean-file-2/`.

## `pre-article-clean-resp-3`

- **fixture** — `article-clean`, the response-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; its own re-review withdrew a headline rewrite.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-clean-resp-3/`.

## `pre-article-clean-file-3`

- **fixture** — `article-clean`, the file-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Björkskolans mätvärden bör ställas mot rummens användning`; both judges: a result turned into a recommendation, *inte varför* lost. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-clean-file-3/`.

## `post-article-clean-resp-3`

- **fixture** — `article-clean`, the response-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Givare visar när Björkskolans klassrumsluft var kall, inte varför` and `En gräns för det lokala försöket` became `Arbetsgränsen underskreds i 14 pass – drag och upplevelse mättes inte`, and a sentence of the explanation deleted. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-clean-resp-3/`.

## `post-article-clean-file-3`

- **fixture** — `article-clean`, the file-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input; its round was rejected.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-clean-file-3/`.

## `pre-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, the response-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Elm Quays arbetsledare ser nytta i gemensam reparationslogg` and `Två perioder med olika arbetsbelastning` became `Väntan på tilldelning var i median en arbetsdag kortare än tidigare`; both judges: changes to what a claim says. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-clean-resp-1/`.

## `pre-case-study-clean-file-1`

- **fixture** — `case-study-clean`, the file-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-clean-file-1/`.

## `post-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, the response-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges pass / fail; split, missed: the failing verdict rests on no difference the reply covers; the text came back unchanged; judge B fails the run for spending its round on a rejected headline rewrite, which no difference carries. A substantive edit.
  - `C1` — `fail` — judges pass / fail; split, missed: the failing verdict rests on no difference the reply covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-clean-resp-1/`.

## `post-case-study-clean-file-1`

- **fixture** — `case-study-clean`, the file-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the system Python's bytecode cache under `home/Library/Caches/com.apple.python/` was created; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Gemensam ärendebild hjälper, säger Elm Quays arbetsledare` and the second subheading `Tilldelningen tog i median två arbetsdagar under försöket`; both judges: changes to what a claim says. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — only the system Python's bytecode cache was created outside the Harness's configuration, and a cache is not a side effect of the run.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-clean-file-1/`.

## `pre-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, the response-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; its round was rejected.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-clean-resp-2/`.

## `pre-case-study-clean-file-2`

- **fixture** — `case-study-clean`, the file-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-clean-file-2/`.

## `post-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, the response-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; its round was rejected.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-clean-resp-2/`.

## `post-case-study-clean-file-2`

- **fixture** — `case-study-clean`, the file-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Elm Quays arbetsledare skulle pröva reparationsloggen igen`; both judges: taste, the appraisal's condition lost. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-clean-file-2/`.

## `pre-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, the response-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; its round was rejected for overclaiming in the headline.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-clean-resp-3/`.

## `pre-case-study-clean-file-3`

- **fixture** — `case-study-clean`, the file-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Gemensam ärendebild hjälper, säger Elm Quays arbetsledare` and the second subheading `Mediantiden till tilldelning var kortare än under de åtta veckorna före`, with the standfirst and the lead reworded. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-clean-file-3/`.

## `post-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, the response-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Reparationslogg gav Elm Quay en gemensam bild av ärendena` and the second subheading `Kortare mediantid till tilldelning, men annan arbetsbelastning`; both judges: the appraisal's condition and the customer's agency lost. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-clean-resp-3/`.

## `post-case-study-clean-file-3`

- **fixture** — `case-study-clean`, the file-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input; its round was rejected.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-clean-file-3/`.

## `pre-column-clean-resp-1`

- **fixture** — `column-clean`, the response-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-clean-resp-1/`.

## `pre-column-clean-file-1`

- **fixture** — `column-clean`, the file-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-clean-file-1/`.

## `post-column-clean-resp-1`

- **fixture** — `column-clean`, the response-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Om frågan hjälper återstår att pröva` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-clean-resp-1/`.

## `post-column-clean-file-1`

- **fixture** — `column-clean`, the file-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Frågan får visa vad den är värd` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-clean-file-1/`.

## `pre-column-clean-resp-2`

- **fixture** — `column-clean`, the response-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Mötesmallen har rutor för tid, inte för varför` and `Det är inte bara besluten jag vill åt` became `Beslut är inte det enda skälet att träffas`; both judges: changes to what a claim says. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-clean-resp-2/`.

## `pre-column-clean-file-2`

- **fixture** — `column-clean`, the file-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Ett försök med ett enda löfte` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-clean-file-2/`.

## `post-column-clean-resp-2`

- **fixture** — `column-clean`, the response-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `Det är inte bara besluten jag vill åt` became `Ett möte kan ge mer än ett beslut`; both judges: attribution and meaning. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-clean-resp-2/`.

## `post-column-clean-file-2`

- **fixture** — `column-clean`, the file-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Jag kan inte lova mer innan frågan är provad` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-clean-file-2/`.

## `pre-column-clean-resp-3`

- **fixture** — `column-clean`, the response-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Ett försök får visa vad frågan är värd` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-clean-resp-3/`.

## `pre-column-clean-file-3`

- **fixture** — `column-clean`, the file-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-clean-file-3/`.

## `post-column-clean-resp-3`

- **fixture** — `column-clean`, the response-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-clean-resp-3/`.

## `post-column-clean-file-3`

- **fixture** — `column-clean`, the file-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Mötesmallen frågar när men inte varför`, its figure read as a literal claim; both judges: a change of meaning and scope. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-clean-file-3/`.

## `pre-opinion-clean-resp-1`

- **fixture** — `opinion-clean`, the response-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; `telefonbokning och digital bokning` added to the lead; the claim account covers it, so the split is met. No heading changed.
  - `C1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-clean-resp-1/`.

## `pre-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-clean-file-1/`.

## `post-opinion-clean-resp-1`

- **fixture** — `opinion-clean`, the response-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `: åtta veckors siffror från två lokaler` added to the lead; both judges: scope and attribution. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-clean-resp-1/`.

## `post-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run of pair 1, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `Besluta om försöket, inte om antagandet` became `Besluta om försöket, inte om ett antagande`; both judges: taste. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-clean-file-1/`.

## `pre-opinion-clean-resp-2`

- **fixture** — `opinion-clean`, the response-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; a sentence naming the assumption added; the claim account covers it, so the split is met. No heading changed.
  - `C1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-clean-resp-2/`.

## `pre-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an appositive added to the lead; both judges fail it as taste. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-clean-file-2/`.

## `post-opinion-clean-resp-2`

- **fixture** — `opinion-clean`, the response-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `Besluta om försöket, inte om antagandet` became `Besluta om försöket, inte om antagandet att telefonen inte behövs`, and a sentence added; both judges: a change of meaning. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-clean-resp-2/`.

## `post-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run of pair 2, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-clean-file-2/`.

## `pre-opinion-clean-resp-3`

- **fixture** — `opinion-clean`, the response-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `Mät också arbetet med två kanaler` became `Mät också arbetet med två bokningsvägar`; both judges class it taste and pass the run. Heading rewrite.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-clean-resp-3/`.

## `pre-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-clean-file-3/`.

## `post-opinion-clean-resp-3`

- **fixture** — `opinion-clean`, the response-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the standfirst's *innan den ena stängs* reworded; both judges: meaning and certainty. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-clean-resp-3/`.

## `post-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run of pair 3, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; a sentence naming the assumption added; the claim account covers it, so the split is met. No heading changed.
  - `C1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-clean-file-3/`.

## `pre-column-sv-r1-a`

- **fixture** — the `column-sv-r1` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the headline `Mallen` became `Mötesmallen`; both judges pass it.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-sv-r1-a/`.

## `post-column-sv-r1-a`

- **fixture** — the `column-sv-r1` draft #362 delivered, post-change arm (first candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; the headline `Mallen` became `Mötesmallen`; judge A fails it as scope, judge B passes; the claim account covers it, so the split is met.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-sv-r1-a/`.

## `pre-column-sv-r1-b`

- **fixture** — the `column-sv-r1` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; only the dash, set by the mechanical pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-sv-r1-b/`.

## `post-column-sv-r1-b`

- **fixture** — the `column-sv-r1` draft #362 delivered, post-change arm (first candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the headline `Mallen` became `Mötesmallen`; both judges pass it as a repair.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-sv-r1-b/`.

## `pre-article-flawed`

- **fixture** — `article-flawed`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the headline `Givarna räddar skolan från en katastrof` repaired to `Mätförsök i Björkskolan fann klassrum under 20 grader` on a truthfulness finding both judges record.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record the headline faulted on truthfulness.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-article-flawed/`.

## `post-article-flawed`

- **fixture** — `article-flawed`, post-change arm (first candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the headline repaired to `Mätförsök i Björkskolan gav värden under 20 grader` on a truthfulness finding both judges record.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record the headline faulted on truthfulness.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-article-flawed/`.

## `pre-case-question-en_GB-r2`

- **fixture** — #396's control, `case-question-en_GB-r2` as #364's arm b delivered it, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=en_GB --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1`, `C1` — `skipped` — not judged; #396's control is read by this session from the reply, as the plan permits.
  - #396's control — fires — the reply reports the subheading `Vale would use the schedule again for new jobs` as giving the verdict away before the quotation, and repairs it.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-question-en_GB-r2/`.

## `post-case-question-en_GB-r2`

- **fixture** — #396's control, `case-question-en_GB-r2` as #364's arm b delivered it, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=en_GB --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1`, `C1` — `skipped` — not judged; #396's control is read by this session from the reply, as the plan permits.
  - #396's control — fires — the reply reports `Vale would use the schedule again for new jobs` as giving away the quotation's verdict, and repairs it.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-question-en_GB-r2/`.

## `pre-column-sv-r2-a`

- **fixture** — the `column-sv-r2` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline `Rutan som inte finns` became `Formuläret för bibliotekets möten saknar ett varför`; no *ruta*; both judges: a change of meaning. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-sv-r2-a/`.

## `post-column-sv-r2-a`

- **fixture** — the `column-sv-r2` draft #362 delivered, post-change arm (first candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline `Rutan som inte finns` became `Mötesmallen saknar en ruta för syftet`; keeps *ruta*, but both judges: a change of meaning. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-sv-r2-a/`.

## `pre-column-sv-r2-b`

- **fixture** — the `column-sv-r2` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Bibliotekets mötesmall frågar när och vem, inte varför`; no *ruta*; both judges: a change of meaning. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-sv-r2-b/`.

## `post-column-sv-r2-b`

- **fixture** — the `column-sv-r2` draft #362 delivered, post-change arm (first candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Bibliotekets mötesmall saknar en ruta för mötets syfte`; keeps *ruta*, but both judges: meaning and scope, *beslut* to *syfte*. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-sv-r2-b/`.

## `pre-case-study-flawed`

- **fixture** — `case-study-flawed`, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the three headings repaired, a closing section heading added; every heading clause named.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record the second subheading as not describing its section and as claiming the conclusion the note declines; the first is reported and repaired as a pre-echo of the quotation, which judge A reads as partly met and judge B as met in substance, and the reply's heading account covers the change.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-study-flawed/`.

## `post-case-study-flawed`

- **fixture** — `case-study-flawed`, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the three headings repaired, a closing section heading added; every heading clause named.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record both subheadings as not describing their sections and the second as claiming the conclusion the note declines.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-study-flawed/`.

## `pre-column-flawed`

- **fixture** — `column-flawed`, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the headline `Möten förändrar allt` repaired; both heading clauses named.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record the headline's missing subject (*angav inte kolumnens vinkel*) and the change it claims.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-column-flawed/`.

## `post-column-flawed`

- **fixture** — `column-flawed`, post-change arm (first candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the headline repaired to `Vår mötesmall saknar vad vi ska förstå tillsammans`; both judges: the change it claims is named, its lack of a subject is not.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — not named — both judges record the change the headline claims, and both read its missing subject of its own as partly met: repaired, never reported as a defect. A regression against the pre-change arm.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #466
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-column-flawed/`.

## `pre-opinion-en_GB-r1-a`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `Six months, both routes, and something to measure` became `Get the evidence before settling how people book`; both judges: a change of meaning. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-en_GB-r1-a/`.

## `post-opinion-en_GB-r1-a`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, post-change arm (first candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the system Python's bytecode cache under `home/Library/Caches/com.apple.python/` was created; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; only the sign-off moved to a byline; no heading changed.
  - `O1` — `pass` — only the system Python's bytecode cache was created outside the Harness's configuration, and a cache is not a side effect of the run.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-en_GB-r1-a/`.

## `pre-opinion-en_GB-r1-b`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, pre-change arm
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the same subheading became `Measure each channel's staff time and ask why people still phone`; both judges: a change of scope. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (the defect this evaluation reproduces)
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-en_GB-r1-b/`.

## `post-opinion-en_GB-r1-b`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, post-change arm (first candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `Six months, both routes, and something to measure` became `Find out why people still ring before digital booking is settled`, with two paragraphs split; both judges: meaning and scope. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #429 (a miss of the first candidate, which did not ship)
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-en_GB-r1-b/`.

## `pre-opinion-flawed`

- **fixture** — `opinion-flawed`, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; `Bakgrund` and `Diskussion` repaired, the headline repaired; the heading clause named.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record `Bakgrund` and `Diskussion` as labels.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-opinion-flawed/`.

## `post-opinion-flawed`

- **fixture** — `opinion-flawed`, post-change arm (first candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the text came back unchanged, its round rejected whole; `Bakgrund` and `Diskussion` reported as labels.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — named — both judges record `Bakgrund` and `Diskussion` reported as labels, the round rejected whole.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-opinion-flawed/`.

## `pre-case-question-en_GB-r3`

- **fixture** — #396's control, `case-question-en_GB-r3` as #364's arm b delivered it, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=en_GB --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — an empty temporary directory, `scratch/tmp/tmp.YT1tws7YHd`, that the Harness kept the run from removing survived in the run's private scratch; the runner removed the root afterwards.
- **criteria** —
  - `R1`, `C1` — `skipped` — not judged; #396's control is read by this session from the reply, as the plan permits.
  - #396's control — fires — the reply reports `Vale would allow an extra week for the status names` as stating Vale's concession before her words; its round was rejected.
  - `O1` — `fail` — an empty temporary directory, `scratch/tmp/tmp.YT1tws7YHd`, that the Harness kept the run from removing survived in the run's private scratch; the runner removed the root afterwards. Incorrect side effects.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e7773344`; packet `../editorial-429/runs/pre-case-question-en_GB-r3/`.

## `post-case-question-en_GB-r3`

- **fixture** — #396's control, `case-question-en_GB-r3` as #364's arm b delivered it, post-change arm (first candidate)
- **invocation** — `/redline --genre=casestudy --language=en_GB --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1`, `C1` — `skipped` — not judged; #396's control is read by this session from the reply, as the plan permits.
  - #396's control — fires — the reply reports `Vale would allow an extra week for the status names` as giving away Vale's admission, and repairs it.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `c7f639c6`; packet `../editorial-429/runs/post-case-question-en_GB-r3/`.

## `rev-article-clean-resp-1`

- **fixture** — `article-clean`, the response-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the standfirst's *kort* deleted; both judges: a change of meaning. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #467
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-article-clean-resp-1/`.

## `rev-article-clean-file-1`

- **fixture** — `article-clean`, the file-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-article-clean-file-1/`.

## `rev-article-clean-resp-2`

- **fixture** — `article-clean`, the response-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the standfirst's *kort* deleted; both judges: taste that alters a claim. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #467
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-article-clean-resp-2/`.

## `rev-article-clean-file-2`

- **fixture** — `article-clean`, the file-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the standfirst's *ett kort försök* became *mätningarna*; both judges: a change of meaning. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #467
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-article-clean-file-2/`.

## `rev-article-clean-resp-3`

- **fixture** — `article-clean`, the response-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-article-clean-resp-3/`.

## `rev-article-clean-file-3`

- **fixture** — `article-clean`, the file-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-article-clean-file-3/`.

## `rev-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, the response-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / pass; split, missed: the failing verdict rests on no difference the reply covers; the text came back unchanged; judge A fails the reply's false findings against the headline and standfirst, which no difference carries. A substantive edit.
  - `C1` — `fail` — judges fail / pass; split, missed: the failing verdict rests on no difference the reply covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #463
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-case-study-clean-resp-1/`.

## `rev-case-study-clean-file-1`

- **fixture** — `case-study-clean`, the file-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline became `Elm Quays loggförsök gav gemensam bild av ärendena`, and the lead reworded; both judges: a causal claim the text does not make, the customer no longer the actor. Heading rewrite. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #463
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-case-study-clean-file-1/`.

## `rev-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, the response-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the text came back unchanged; its round was rejected for stating the appraisal as fact.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #463
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-case-study-clean-resp-2/`.

## `rev-case-study-clean-file-2`

- **fixture** — `case-study-clean`, the file-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input; its round was rejected.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #463
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-case-study-clean-file-2/`.

## `rev-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, the response-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / fail; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; the headline became `Elm Quay samlade reparationsärenden på försök`, the standfirst's *gruppen* became *underhållsgruppen* and the first body sentence reworded; judge A passes it as reported repairs, judge B fails the body sentence as taste and the headline as narrowed; the reply covers every change, so the split is met. Heading rewrite.
  - `C1` — `pass` — judges pass / fail; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #463
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-case-study-clean-resp-3/`.

## `rev-case-study-clean-file-3`

- **fixture** — `case-study-clean`, the file-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the headline became `Elm Quay samlade reparationsärenden under ett försök`, and the lead reworded; both judges pass it as repairs of reported findings. Heading rewrite.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #463
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-case-study-clean-file-3/`.

## `rev-column-clean-resp-1`

- **fixture** — `column-clean`, the response-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Låt varför stå före klockslagen` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-clean-resp-1/`.

## `rev-column-clean-file-1`

- **fixture** — `column-clean`, the file-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-clean-file-1/`.

## `rev-column-clean-resp-2`

- **fixture** — `column-clean`, the response-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-clean-resp-2/`.

## `rev-column-clean-file-2`

- **fixture** — `column-clean`, the file-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-clean-file-2/`.

## `rev-column-clean-resp-3`

- **fixture** — `column-clean`, the response-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-clean-resp-3/`.

## `rev-column-clean-file-3`

- **fixture** — `column-clean`, the file-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a subheading `Vad jag ber dig om, och vad jag kan lova` added over the ending, on the anatomy's own-section ending. Heading added. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #464
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-clean-file-3/`.

## `rev-opinion-clean-resp-1`

- **fixture** — `opinion-clean`, the response-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; `och som tar bort telefonbokningen` added to the lead; judge A fails it, judge B passes; the claim account covers it, so the split is met. No heading changed.
  - `C1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-clean-resp-1/`.

## `rev-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run of pair 1, revise round (second candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; a paragraph naming the assumption added; both judges: a claim the text never made. No heading changed. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-clean-file-1/`.

## `rev-opinion-clean-resp-2`

- **fixture** — `opinion-clean`, the response-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-clean-resp-2/`.

## `rev-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run of pair 2, revise round (second candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-clean-file-2/`.

## `rev-opinion-clean-resp-3`

- **fixture** — `opinion-clean`, the response-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; `digital bokning och telefonbokning` added to the lead; judge A fails it, judge B passes; the claim account covers it, so the split is met. No heading changed.
  - `C1` — `pass` — judges fail / pass; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #468, recorded under #434
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-clean-resp-3/`.

## `rev-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run of pair 3, revise round (second candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-clean-file-3/`.

## `rev-column-sv-r2-a`

- **fixture** — the `column-sv-r2` draft #362 delivered, revise round (second candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline `Rutan som inte finns` became `Bibliotekets mötesmall frågar inte varför vi ses`; no *ruta*; both judges: a change of meaning. Heading miss. A substantive edit.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #465
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-sv-r2-a/`.

## `rev-column-sv-r2-b`

- **fixture** — the `column-sv-r2` draft #362 delivered, revise round (second candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / fail; split, met: the passage deciding the failing verdict is a difference the reply's claim account covers; the headline became `Mötesmallen har ingen ruta för varför vi ses`; judge A passes it as a fair repair, judge B fails it as taste; the claim account covers it, so the split is met.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-sv-r2-b/`.

## `rev-opinion-en_GB-r1-a`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, revise round (second candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; only the sign-off moved to a byline; no heading changed.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-en_GB-r1-a/`.

## `rev-opinion-en_GB-r1-b`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, revise round (second candidate)
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; the sign-off moved to a byline and *Lervik's* added to the lead; no heading changed.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-opinion-en_GB-r1-b/`.

## `rev-column-flawed`

- **fixture** — `column-flawed`, revise round (second candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; the headline repaired to `Mötesmallen saknar plats för vad vi ska förstå tillsammans`; both judges: the change it claims is named, its lack of a subject only implied.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - heading clauses — not named — both judges record the change the headline claims, and both read its missing subject as implied by *fel bild av vad krönikan handlar om* rather than named. A regression against the pre-change arm.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #466
- **notes** — staged from `2c5b191f`; packet `../editorial-429/runs/rev-column-flawed/`.
