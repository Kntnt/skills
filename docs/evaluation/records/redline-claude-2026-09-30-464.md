# redline — claude — 2026-09-30 — #464

- **record** — `redline-claude-2026-09-30-464`
- **date** — `2026-09-30`
- **ticket** — `#464`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.285
- **corpus commit** — `41fd4c55`

## Run conditions

Two installs over the same inputs. The pre-change arm was staged from `41fd4c55`, the branch head when #464's build began; the post-change arm from `131c5c39`, #464's candidate, which ships. Both arms ran every row of the frozen run table: `column-clean` as three response-target and file-target pairs, and `opinion-flawed` twice. No revise round was taken. The method is frozen in [`../editorial-464/plan.md`](../editorial-464/plan.md), second freeze `e028affe`, which copies #429's control briefs, split rule, runner and void-run handling; the whole evaluation is written up in [`../editorial-464/results.md`](../editorial-464/results.md), and every counted run's packet is under [`../editorial-464/runs/`](../editorial-464/runs/). A first attempt made under the plan's first freeze, and eleven runs cut off by a usage limit, are void and kept under [`../editorial-464/voided/`](../editorial-464/voided/); no entry below is one of them. All counted runs were made on 2026-09-30.

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt, the editorial Skills and the Manager staged by `git archive` into a private root of its own; each file-target run's delivered `output.md` is captured into its packet as `captured-output.md`. Every run was judged by two fresh judges blind to the arm, the model and the ticket, with #429's control briefs; where they split, #429's counting rule decides. No Codex Harness and no GPT model was started, controlled or invoked.

Four criteria are this evaluation's own: **`R1`** on `column-clean`, **`C1`** — `R1` against the row's frozen expectation — on every run, **`O1`** and **`S1`**. A `column-clean` entry also carries the plan's target reading, whether a heading line was added or the last section split, and an `opinion-flawed` entry the control reading, whether its closing content got a section of its own or the missing ending section was reported. A response-target run that returned only the no-change status has its `R1` skipped, the file-target run of its pair answering the criterion.

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
  - target — no heading added — no text delivered.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-column-clean-resp-1/`.

## `pre-column-clean-file-1`

- **fixture** — `column-clean`, the file-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, identical to the input, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added, last section intact.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-column-clean-file-1/`.

## `post-column-clean-resp-1`

- **fixture** — `column-clean`, the response-target run of pair 1, post-change arm (candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added — no text delivered.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-column-clean-resp-1/`.

## `post-column-clean-file-1`

- **fixture** — `column-clean`, the file-target run of pair 1, post-change arm (candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, identical to the input, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added, last section intact.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-column-clean-file-1/`.

## `pre-column-clean-resp-2`

- **fixture** — `column-clean`, the response-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added — no text delivered.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-column-clean-resp-2/`.

## `pre-column-clean-file-2`

- **fixture** — `column-clean`, the file-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md` with one subheading added, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the subheading `Låt nästa mötesbokning bli ett försök` added before the ending's last paragraph, on the anatomy's own-section ending, with a claim the column does not make. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - target — heading added and last section split — reproduces the defect.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none; the defect is #464's own, and the candidate repairs it
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-column-clean-file-2/`.

## `post-column-clean-resp-2`

- **fixture** — `column-clean`, the response-target run of pair 2, post-change arm (candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added — no text delivered.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-column-clean-resp-2/`.

## `post-column-clean-file-2`

- **fixture** — `column-clean`, the file-target run of pair 2, post-change arm (candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, identical to the input, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added, last section intact.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-column-clean-file-2/`.

## `pre-column-clean-resp-3`

- **fixture** — `column-clean`, the response-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with one subheading added, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; the subheading `Ett försök utan löfte om bättre möten` added before the ending's last paragraph, on the anatomy's own-section ending, with a claim the column does not make. A substantive edit.
  - `C1` — `fail` — judges fail / fail, read against the row's frozen expectation.
  - target — heading added and last section split — reproduces the defect.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none; the defect is #464's own, and the candidate repairs it
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-column-clean-resp-3/`.

## `pre-column-clean-file-3`

- **fixture** — `column-clean`, the file-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, identical to the input, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added, last section intact.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-column-clean-file-3/`.

## `post-column-clean-resp-3`

- **fixture** — `column-clean`, the response-target run of pair 3, post-change arm (candidate)
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status and the run's account in the reply; no text.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `skipped` — the run returned only the no-change status, so no text was delivered; the file-target run of the pair answers the criterion.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added — no text delivered.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-column-clean-resp-3/`.

## `post-column-clean-file-3`

- **fixture** — `column-clean`, the file-target run of pair 3, post-change arm (candidate)
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, identical to the input, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; `output.md` identical to the input.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - target — no heading added, last section intact.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-column-clean-file-3/`.

## `pre-opinion-flawed-1`

- **fixture** — `opinion-flawed`, run 1, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; every clause of the row named, the standfirst reported and left unwritten, `Bakgrund` and `Diskussion` repaired.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - control — passes — both judges record the closing exhortation given a section of its own, `Kravet riktas till kommunstyrelsen`, built from the text's own actor and proposal.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-opinion-flawed-1/`.

## `post-opinion-flawed-1`

- **fixture** — `opinion-flawed`, run 1, post-change arm (candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; every clause of the row named, the standfirst reported and left unwritten, `Bakgrund` and `Diskussion` repaired.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - control — passes — both judges record the closing exhortation given a section of its own, `Kommunstyrelsen bör besluta och förvaltningen mäta`, built from the text's own actor and proposal.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-opinion-flawed-1/`. A first making of this run was cut off by the usage limit and is kept under `../editorial-464/voided/usage-limit/`.

## `pre-opinion-flawed-2`

- **fixture** — `opinion-flawed`, run 2, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; every clause of the row named, the standfirst reported and left unwritten, `Bakgrund` and `Diskussion` repaired.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - control — passes — both judges record the closing exhortation given a section of its own, `Nästa steg är kommunstyrelsens`, built from the text's own actor and proposal.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `41fd4c55`; packet `../editorial-464/runs/pre-opinion-flawed-2/`.

## `post-opinion-flawed-2`

- **fixture** — `opinion-flawed`, run 2, post-change arm (candidate)
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `C1` — `pass` — judges pass / pass; every clause of the row named, the standfirst reported and left unwritten, `Bakgrund` and `Diskussion` repaired.
  - `R1` — `skipped` — a flawed control is scored by `C1`, `R1` read against its row.
  - control — passes — both judges record the closing exhortation given a section of its own, `Kommunstyrelsen kan pröva båda bokningsvägarna`, built from the text's own actor and proposal.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `131c5c39`; packet `../editorial-464/runs/post-opinion-flawed-2/`.
