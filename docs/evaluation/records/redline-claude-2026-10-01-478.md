# redline — claude — 2026-10-01 — #478

- **record** — `redline-claude-2026-10-01-478`
- **date** — `2026-10-01`
- **ticket** — `#478`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent, checker and nested Proofread pass in it, every replay, and every judge and classifier
- **harness** — Claude Code 2.1.286
- **corpus commit** — `fb169087`

## Run conditions

The evaluation has two arms, each with the same eight runs:

- `case-study-clean` as three pairs, one run to the response and one to a new file `output.md`, as the protocol's *A clean control* requires;
- `case-study-flawed` twice, to the response.

The pre-change arm was staged from `fb169087`, the commit #478's build started from. The candidate arm was staged from `cbda0352`, which widens the second list of Redline's reply checker (`skills/editorial/redline/references/reply-check.md`). The method is in [`../editorial-478/plan.md`](../editorial-478/plan.md), frozen at `ca225468` before the first run, and the outcome in [`../editorial-478/results.md`](../editorial-478/results.md).

**How each run was made.** Each run was a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). The Formal Invocation was its whole prompt, with no contextual instruction. The editorial Skills and the Manager were staged by `git archive` into a private root of its own. The runs were made on 1 October in two waves:

- wave 1 from 11:56 to 13:05 UTC;
- wave 2 from 15:32 to 15:53 UTC.

Three runs of wave 1 were cut off by the account's usage limit and are void. They are kept in [`../editorial-478/voided/`](../editorial-478/voided/), and wave 2 made them again from the same commits.

**How each run was judged.** Every run had two fresh judges, blind to the arm, the model and the ticket:

- a response-target run with #475's `control-judge-brief.md`;
- a file-target run with #475's `control-judge-brief-file.md`.

Each brief was used byte for byte. Fresh classifiers put every `A2` miss in the plan's classes. No Codex Harness and no GPT model was started, controlled or invoked.

**Replays.** Eighteen further sessions replayed the checker's brief, filled with three frozen contrasts, three times per arm. They are diagnosis, not Redline runs, so they have no entries below. Their packets are under `../editorial-478/runs/*-replay-*`, and their reading is in `results.md`.

**This evaluation's own criteria.**

- **`A2`**, read as the plan reads it. Every miss a judge records is put in one of four classes:
  1. the claim account;
  2. a statement about a text that the text contradicts;
  3. a statement true of its text that the judge faults for what it suggests;
  4. an omission of a difference that moves no claim.

  A run fails `A2` here where it carries a class 1 or class 2 miss. One judge is enough. A *target miss* is a class 1 miss about an attribution the run moved.
- **`C1`**, each judge's heading-4 verdict. It passes where both judges pass.
- **`O1`**.
- **`S1`**.

Whether the run started the checker, and whether the delivered text equals the final Text Artifact the checker was shown, is recorded on every run.

**Outcome.** No run in either arm carries a class 1 or class 2 miss, so the fault is not reproduced. The candidate is reverted, nothing ships, nothing is filed, and ADR-0233 records why.

## `pre-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed from the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.

## `post-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.

## `pre-case-study-clean-file-1`

- **fixture** — `case-study-clean`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the text written to `output.md`, changed from the input, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, the effect asked for; nothing else outside the Harness's configuration and caches; `work/input.md` unchanged; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges pass / fail; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed, save `output.md`, the effect asked for.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge B.

## `post-case-study-clean-file-1`

- **fixture** — `case-study-clean`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the text written to `output.md`, changed from the input, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, the effect asked for; nothing else outside the Harness's configuration and caches; `work/input.md` unchanged; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed, save `output.md`, the effect asked for.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge A; class 3, judge B; class 3, judge B.

## `pre-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.

## `post-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge A; class 3, judge B.

## `pre-case-study-clean-file-2`

- **fixture** — `case-study-clean`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the text written to `output.md`, changed from the input, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, the effect asked for; nothing else outside the Harness's configuration and caches; `work/input.md` unchanged; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed, save `output.md`, the effect asked for.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge A; class 3, judge B.

## `post-case-study-clean-file-2`

- **fixture** — `case-study-clean`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the text written to `output.md`, changed from the input, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, the effect asked for; nothing else outside the Harness's configuration and caches; `work/input.md` unchanged; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / pass; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed, save `output.md`, the effect asked for.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge A.

## `pre-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed from the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`. The run also left the empty working directory `scratch/tmp/tmp.1reKUB81FT` in its private scratch, which its reply names; the runner removed it with the root. Recorded under #476.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / pass; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge A; class 3, judge A; class 3, judge A; class 3, judge B.

## `post-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.

## `pre-case-study-clean-file-3`

- **fixture** — `case-study-clean`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the text written to `output.md`, changed from the input, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, the effect asked for; nothing else outside the Harness's configuration and caches; `work/input.md` unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / pass; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed, save `output.md`, the effect asked for.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge B.

## `post-case-study-clean-file-3`

- **fixture** — `case-study-clean`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the text written to `output.md`, changed from the input, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, the effect asked for; nothing else outside the Harness's configuration and caches; `work/input.md` unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail; recorded with its cause in `results.md`, not a Control miss.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed, save `output.md`, the effect asked for.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 4, judge A; class 4, judge B.

## `pre-case-study-flawed-1`

- **fixture** — `case-study-flawed`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed from the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.

## `post-case-study-flawed-1`

- **fixture** — `case-study-flawed`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed from the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.

## `pre-case-study-flawed-2`

- **fixture** — `case-study-flawed`, pre-change arm, staged from `fb169087`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Misses recorded: class 3, judge A.

## `post-case-study-flawed-2`

- **fixture** — `case-study-flawed`, candidate arm, staged from `cbda0352`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none` outside the Harness's configuration and caches: `work/input.md` unchanged, nothing created beside it; the root was removed. Wave 1's inventories also show `returned.md` appearing in the session scratchpad, which no run of this build wrote to and which is named by no one; see `results.md`.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration, caches and private scratch created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - The checker — started once; the delivered text equals the final Text Artifact it was shown.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — No `A2` miss recorded.
