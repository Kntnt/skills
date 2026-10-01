# redline — claude — 2026-10-01 — #480

- **record** — `redline-claude-2026-10-01-480`
- **date** — `2026-10-01`
- **ticket** — `#480`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent, reply checker and nested Proofread pass in it, every judge and every validator
- **harness** — Claude Code 2.1.286
- **corpus commit** — `fb169087`

## Run conditions

Three installs. The pre-change arm was staged from `fb169087`, the commit #480's build started from. The first candidate was staged from `f39a3721`, and the revise round from `e4fe5890`. The pre-change arm and the first candidate ran every row of the frozen run table. `article-clean` ran as three response-target and file-target pairs and `article-allusion` as two pairs. `article-unnamed` and `article-overclaim` ran twice each, to the response. The revise round ran `article-clean` alone, as the plan's subset that failed. `article-clean` and its frozen expectation come from the corpus at `fb169087`. The three contrast inputs are `article-clean` with the headline replaced. They and their frozen expectations were committed at `e5fcdf4f` and `e7dd6701`, and validated blind before the first run. The method is frozen in [`../editorial-480/plan.md`](../editorial-480/plan.md). The whole evaluation is written up in [`../editorial-480/results.md`](../editorial-480/results.md), and every run's packet is under [`../editorial-480/runs/`](../editorial-480/runs/).

Each run is a fresh top-level Claude Code session, started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt. The Skills were staged by `git archive` into a private root of the run's own. Every run was judged by two fresh judges, blind to the arm, the model and the ticket, with #468's control briefs. A usage limit cut off two judges of the first candidate's arm. Those judgements are void and were sent again to fresh judges; no run was cut off. No Codex Harness and no GPT model was started, controlled or invoked.

Four criteria are this evaluation's own: **`R1`**, **`C1`** (the run meets its input's frozen expectation), **`O1`** and **`S1`**. A response-target run that returned only the no-change status has its `R1` skipped, and the file-target run of its pair answers the criterion. The Target and Control readings are in `results.md`. The defect reproduced in one pre-change `article-clean` run of six. The first candidate missed the Target on a lead rewrite outside it. The revised candidate met the Target with no Control regressed, and it ships.

## `pre-article-allusion-file-1`

- **fixture** — `article-allusion`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-allusion-file-1/`

## `pre-article-allusion-file-2`

- **fixture** — `article-allusion`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-allusion-file-2/`

## `pre-article-allusion-resp-1`

- **fixture** — `article-allusion`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-allusion-resp-1/`

## `pre-article-allusion-resp-2`

- **fixture** — `article-allusion`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-allusion-resp-2/`

## `pre-article-clean-file-1`

- **fixture** — `article-clean`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-clean-file-1/`; no finding against the headline.

## `pre-article-clean-file-2`

- **fixture** — `article-clean`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `fail` — both judges read *Conforms to the anatomy* as partly met, on an unresolved finding against the lead's placement sentence (#487).
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-clean-file-2/`; no finding against the headline.

## `pre-article-clean-file-3`

- **fixture** — `article-clean`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-clean-file-3/`; no finding against the headline.

## `pre-article-clean-resp-1`

- **fixture** — `article-clean`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-clean-resp-1/`; no finding against the headline.

## `pre-article-clean-resp-2`

- **fixture** — `article-clean`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the headline was rewritten to *Mätförsöket i Björkskolan visar när det var kallt, inte varför*, a change of taste and meaning on a clean text.
  - `C1` — `fail` — the headline, which the expectation treats as conforming, was found against and rewritten.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-clean-resp-2/`; shows the Target's defect: a finding against the working headline, answered by a rewrite.

## `pre-article-clean-resp-3`

- **fixture** — `article-clean`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-clean-resp-3/`; no finding against the headline.

## `pre-article-overclaim-1`

- **fixture** — `article-overclaim`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-overclaim-1/`

## `pre-article-overclaim-2`

- **fixture** — `article-overclaim`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-overclaim-2/`

## `pre-article-unnamed-1`

- **fixture** — `article-unnamed`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-unnamed-1/`

## `pre-article-unnamed-2`

- **fixture** — `article-unnamed`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line saying no file was written; the transcript holds an earlier full delivery that the Harness did not return (#488).
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the reply the Harness returned is one cleanup line and delivers no text (#488).
  - `C1` — `fail` — the reply as returned reports no finding against the headline.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #488
- **notes** — staged from `fb169087`; packet `../editorial-480/runs/pre-article-unnamed-2/`

## `post-article-allusion-file-1`

- **fixture** — `article-allusion`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-allusion-file-1/`

## `post-article-allusion-file-2`

- **fixture** — `article-allusion`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-allusion-file-2/`

## `post-article-allusion-resp-1`

- **fixture** — `article-allusion`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-allusion-resp-1/`

## `post-article-allusion-resp-2`

- **fixture** — `article-allusion`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-allusion-resp-2/`

## `post-article-clean-file-1`

- **fixture** — `article-clean`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-clean-file-1/`; no finding against the headline.

## `post-article-clean-file-2`

- **fixture** — `article-clean`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; `output.md` rewrites the lead's *Det gör placeringen viktig när …* to *Det avgränsar vad fastighetskontoret kan läsa ut av …*, a change of meaning on a clean text (#487).
  - `C1` — `fail` — the calm explanation lost an inference of its lead (#487).
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-clean-file-2/`; no finding against the headline.

## `post-article-clean-file-3`

- **fixture** — `article-clean`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-clean-file-3/`; no finding against the headline.

## `post-article-clean-resp-1`

- **fixture** — `article-clean`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-clean-resp-1/`; no finding against the headline.

## `post-article-clean-resp-2`

- **fixture** — `article-clean`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-clean-resp-2/`; no finding against the headline.

## `post-article-clean-resp-3`

- **fixture** — `article-clean`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-clean-resp-3/`; no finding against the headline.

## `post-article-overclaim-1`

- **fixture** — `article-overclaim`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-overclaim-1/`

## `post-article-overclaim-2`

- **fixture** — `article-overclaim`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-overclaim-2/`

## `post-article-unnamed-1`

- **fixture** — `article-unnamed`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-unnamed-1/`

## `post-article-unnamed-2`

- **fixture** — `article-unnamed`, first candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `pass` — both judges record the headline defect detected and repaired at the text's strength, with every other clause met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `f39a3721`; packet `../editorial-480/runs/post-article-unnamed-2/`

## `rev-article-clean-file-1`

- **fixture** — `article-clean`, revise round
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e4fe5890`; packet `../editorial-480/runs/rev-article-clean-file-1/`; no finding against the headline.

## `rev-article-clean-file-2`

- **fixture** — `article-clean`, revise round
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e4fe5890`; packet `../editorial-480/runs/rev-article-clean-file-2/`; no finding against the headline.

## `rev-article-clean-file-3`

- **fixture** — `article-clean`, revise round
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` is byte-identical to the input.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration and `work/output.md` created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `e4fe5890`; packet `../editorial-480/runs/rev-article-clean-file-3/`; no finding against the headline.

## `rev-article-clean-resp-1`

- **fixture** — `article-clean`, revise round
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `e4fe5890`; packet `../editorial-480/runs/rev-article-clean-resp-1/`; no finding against the headline.

## `rev-article-clean-resp-2`

- **fixture** — `article-clean`, revise round
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, with no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered; the file-target entry of the pair answers it.
  - `C1` — `pass` — both judges find every clause of the frozen expectation met.
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `e4fe5890`; packet `../editorial-480/runs/rev-article-clean-resp-2/`; no finding against the headline.

## `rev-article-clean-resp-3`

- **fixture** — `article-clean`, revise round
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; every difference repairs a defect the expectation names, or there is none.
  - `C1` — `fail` — both judges read *Conforms to the anatomy* as partly met, on an unresolved finding against the lead's placement sentence (#487).
  - `O1` — `pass` — no path outside the Harness's configuration created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #487
- **notes** — staged from `e4fe5890`; packet `../editorial-480/runs/rev-article-clean-resp-3/`; no finding against the headline.
