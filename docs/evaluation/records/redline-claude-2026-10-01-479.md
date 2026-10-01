# redline — claude — 2026-10-01 — #479

- **record** — `redline-claude-2026-10-01-479`
- **date** — `2026-10-01`
- **ticket** — `#479`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.286
- **corpus commit** — `fb169087`

## Run conditions

Two installs over the same inputs, then a revise round from a third. The pre-change arm was staged from `fb169087`, the commit #479's build started from, and the candidate arm from `f3851e9f`, which adds one paragraph to `genres/opinion.review.md`, written after the pre-change arm had been read. Both arms ran every row of the frozen run table: `opinion-clean` and `article-clean` as three response-target and file-target pairs each, `opinion-closure-certain` (an input written for this evaluation, `opinion-clean` with the standfirst stating the closure as settled) as three file-target runs, and `opinion-flawed` as two response-target runs. The session that verified that build then made five more runs of `f3851e9f` with the same runner, seat and inputs: four file-target runs of `opinion-clean` and one of `opinion-closure-certain`. They are recorded here as the `spot-` entries, judged by the same rules after the fact. Two of them showed the Target's defect, so the plan's one revise round was taken. It ran `opinion-clean`'s three pairs from `3b1f791d`, which rewrites that paragraph, and those runs are the `rev-` entries. The method is frozen in [`../editorial-479/plan.md`](../editorial-479/plan.md), the revise round's runs are listed in [`../editorial-479/runs/matrix-revise.tsv`](../editorial-479/runs/matrix-revise.tsv), the whole evaluation is written up in [`../editorial-479/results.md`](../editorial-479/results.md), and every run's packet is under [`../editorial-479/runs/`](../editorial-479/runs/). No run was void.

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt. The editorial Skills and the Manager were staged by `git archive` into a private root of the run's own. Each file-target run's delivered `output.md` is captured into its packet as `captured-output.md`. Every run was judged by two fresh judges blind to the arm, the model and the ticket, with the control briefs copied from #468. Where the judges split, the split rule the plan states decides. No Codex Harness and no GPT model was started, controlled or invoked.

Five criteria are this evaluation's own: **`R1`**, **`C1`** (the run against its row's frozen expectation), **`O1`**, **`S1`** and, for the two opinion inputs, **`T1`** (the four review stages read from the trace into the packet's `rounds.md`). A response-target run that returned only the no-change status has its `R1` skipped, and the file-target run of its pair answers the criterion. The Target and control readings are in `results.md`. The defect reproduced in three of six pre-change runs of `opinion-clean`. It showed in none of the six post-change runs of the first candidate, but in two of its four spot runs. It showed in none of the six revise-round runs, one of which misses `R1` over a lead clarification filed as #492. The negative case and every control held, read from the first candidate's arm for every input the revise round did not run again. Under the plan's fallback rule, the revised candidate ships.

## `pre-article-clean-resp-1`

- **fixture** — `article-clean`, the response-target run, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-article-clean-resp-1/`.

## `pre-article-clean-file-1`

- **fixture** — `article-clean`, the file-target run, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-article-clean-file-1/`.

## `pre-article-clean-resp-2`

- **fixture** — `article-clean`, the response-target run, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, unchanged, in a fenced block, with the placement finding reported unresolved and the run's account; nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — the text in the reply is identical to the input; judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — one: the lead raises sensor placement and never returns to it
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-article-clean-resp-2/`.

## `pre-article-clean-file-2`

- **fixture** — `article-clean`, the file-target run, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-article-clean-file-2/`.

## `pre-article-clean-resp-3`

- **fixture** — `article-clean`, the response-target run, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, its headline rewritten, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an unsupported fact: a working claim of a clean text changed in meaning, scope or chronology with no visible defect to license it, as the notes say.
  - `C1` — `fail` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them
- **defects filed** — none; #480 carries it
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-article-clean-resp-3/`; the headline *Mätförsöket i Björkskolan visar när, inte varför* rewritten; recorded under #480.

## `pre-article-clean-file-3`

- **fixture** — `article-clean`, the file-target run, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, its headline rewritten, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an unsupported fact: a working claim of a clean text changed in meaning, scope or chronology with no visible defect to license it, as the notes say.
  - `C1` — `fail` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them
- **defects filed** — none; #480 carries it
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-article-clean-file-3/`; the headline rewritten to *… visar när luften var kall, inte varför*; recorded under #480.

## `pre-opinion-clean-resp-1`

- **fixture** — `opinion-clean`, the response-target run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, the standfirst and the lead changed, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-clean-resp-1/`; shows the Target's defect, delivered: *innan den ena stängs* became *innan det avgörs om den ena ska stängas*; the lead gained *telefonbokning och digital bokning*.

## `pre-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst changed, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / fail; met under the split rule, since the reply reports the deciding change as a changed claim.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-clean-file-1/`; shows the Target's defect, delivered: *innan det avgörs om den ena ska stängas*; judges pass / fail, met under the split rule because the reply reports the changed claim.

## `pre-opinion-clean-resp-2`

- **fixture** — `opinion-clean`, the response-target run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-clean-resp-2/`.

## `pre-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst's last clause deleted, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an unsupported fact: a working claim of a clean text changed in meaning, scope or chronology with no visible defect to license it, as the notes say.
  - `C1` — `fail` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none; this is #479
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-clean-file-2/`; shows the Target's defect, delivered: *innan den ena stängs* deleted, the miss #468 measured.

## `pre-opinion-clean-resp-3`

- **fixture** — `opinion-clean`, the response-target run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, the lead gaining *digital bokning och telefonbokning*, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-clean-resp-3/`; no closure-as-given finding; judges split on `C1`, met under the split rule.

## `pre-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-clean-file-3/`.

## `pre-opinion-closure-certain-1`

- **fixture** — `opinion-closure-certain`, a run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… innan telefonbokningens framtid avgörs.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-closure-certain-1/`; the planted settled closure detected and repaired.

## `pre-opinion-closure-certain-2`

- **fixture** — `opinion-closure-certain`, a run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… innan det avgörs om telefonbokningen ska stängas för gott.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-closure-certain-2/`; the planted settled closure detected and repaired.

## `pre-opinion-closure-certain-3`

- **fixture** — `opinion-closure-certain`, a run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… ett halvår till.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-closure-certain-3/`; the planted settled closure detected and repaired. The closing Proofread pass also changed *webbokningar* to *webbbokningar*.

## `pre-opinion-flawed-1`

- **fixture** — `opinion-flawed`, a run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, repaired, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst, reported and left unwritten, among those the reply lists
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-flawed-1/`; all seven defects (o1)–(o7) detected.

## `pre-opinion-flawed-2`

- **fixture** — `opinion-flawed`, a run, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, repaired, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst, reported and left unwritten, among those the reply lists
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-479/runs/pre-opinion-flawed-2/`; all seven defects (o1)–(o7) detected.

## `post-article-clean-resp-1`

- **fixture** — `article-clean`, the response-target run, candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-article-clean-resp-1/`.

## `post-article-clean-file-1`

- **fixture** — `article-clean`, the file-target run, candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply. A headline round was rejected.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `fail` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — two: the headline's *när* and *varför*, and sensor placement
- **defects filed** — none; #480 carries it
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-article-clean-file-1/`; `C1` misses *Conforms to the anatomy* over the headline finding, recorded under #480.

## `post-article-clean-resp-2`

- **fixture** — `article-clean`, the response-target run, candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-article-clean-resp-2/`.

## `post-article-clean-file-2`

- **fixture** — `article-clean`, the file-target run, candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, its headline rewritten, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an unsupported fact: a working claim of a clean text changed in meaning, scope or chronology with no visible defect to license it, as the notes say.
  - `C1` — `fail` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them
- **defects filed** — none; #480 carries it
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-article-clean-file-2/`; the headline rewritten to *Björkskolans givare visar när det blev kallt, inte varför*; recorded under #480.

## `post-article-clean-resp-3`

- **fixture** — `article-clean`, the response-target run, candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, one lead sentence changed, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an unsupported fact: a working claim of a clean text changed in meaning, scope or chronology with no visible defect to license it, as the notes say.
  - `C1` — `fail` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #486
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-article-clean-resp-3/`; the lead's *Det gör placeringen viktig när …* became *Det är utgångspunkten när …*; the run's instructions are byte-identical to the pre-change arm's, since an `article` run does not load the file the candidate changes.

## `post-article-clean-file-3`

- **fixture** — `article-clean`, the file-target run, candidate arm
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-article-clean-file-3/`.

## `post-opinion-clean-resp-1`

- **fixture** — `opinion-clean`, the response-target run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-clean-resp-1/`; no finding recorded.

## `post-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-clean-file-1/`; no finding recorded.

## `post-opinion-clean-resp-2`

- **fixture** — `opinion-clean`, the response-target run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-clean-resp-2/`; no finding recorded.

## `post-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-clean-file-2/`; no finding recorded.

## `post-opinion-clean-resp-3`

- **fixture** — `opinion-clean`, the response-target run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-clean-resp-3/`; no finding recorded.

## `post-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-clean-file-3/`; no finding recorded.

## `post-opinion-closure-certain-1`

- **fixture** — `opinion-closure-certain`, a run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… ett halvår till.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-closure-certain-1/`; the planted settled closure detected and repaired.

## `post-opinion-closure-certain-2`

- **fixture** — `opinion-closure-certain`, a run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… innan telefonbokningens framtid avgörs.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-closure-certain-2/`; the planted settled closure detected and repaired.

## `post-opinion-closure-certain-3`

- **fixture** — `opinion-closure-certain`, a run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… innan det avgörs om telefonbokningen ska stängas för gott.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-closure-certain-3/`; the planted settled closure detected and repaired.

## `post-opinion-flawed-1`

- **fixture** — `opinion-flawed`, a run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, repaired, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst, reported and left unwritten, among those the reply lists
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-flawed-1/`; all seven defects (o1)–(o7) detected.

## `post-opinion-flawed-2`

- **fixture** — `opinion-flawed`, a run, candidate arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status after a rejected round, with every finding reported unresolved.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T1`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — every finding, the round having been rejected
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/post-opinion-flawed-2/`; all seven defects (o1)–(o7) detected. The round was rejected because its rewritten headline repeated the opening sentence.

## `spot-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run, first-candidate spot run, made by the verifying session
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst changed, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met under the split rule because the reply reports the changed claim.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none; this is #479
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/spot-opinion-clean-file-1/`; shows the Target's defect, delivered: *innan den ena stängs* became *innan det avgörs om den ena ska stängas*; the finding cites the first candidate's paragraph. Made as `spot-opinion-clean-file` in the verifying session's scratch.

## `spot-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run, first-candidate spot run, made by the verifying session
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst changed, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail; an unsupported fact: a working claim of a clean text changed in certainty and chronology with no visible defect to license it, as the notes say.
  - `C1` — `fail` — both judges record the early thesis as no longer stated the same way in the standfirst.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none; this is #479
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/spot-opinion-clean-file-2/`; shows the Target's defect, delivered: *innan det avgörs om den ena ska stängas*; the finding cites the first candidate's paragraph as its requirement. Made as `spot-opinion-clean-file-2` in the verifying session's scratch.

## `spot-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run, first-candidate spot run, made by the verifying session
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the lead gaining *telefonbokning och digital bokning*, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/spot-opinion-clean-file-3/`; no closure-as-given finding; the lead clarification #492 records. Made as `spot-opinion-clean-file-3` in the verifying session's scratch.

## `spot-opinion-clean-file-4`

- **fixture** — `opinion-clean`, the file-target run, first-candidate spot run, made by the verifying session
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/spot-opinion-clean-file-4/`; no finding recorded. Made as `spot-opinion-clean-file-4` in the verifying session's scratch.

## `spot-opinion-closure-certain-1`

- **fixture** — `opinion-closure-certain`, a run, first-candidate spot run, made by the verifying session
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the standfirst ending *… innan det avgörs om telefonbokningen ska stängas för gott.*, and the run's account.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `f3851e9f`; packet `../editorial-479/runs/spot-opinion-closure-certain-1/`; the planted settled closure detected and repaired. The closing Proofread pass also changed *webbokningar* to *webbbokningar*. Made as `spot-closure-certain-file` in the verifying session's scratch.

## `rev-opinion-clean-resp-1`

- **fixture** — `opinion-clean`, the response-target run, revise round
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `3b1f791d`; packet `../editorial-479/runs/rev-opinion-clean-resp-1/`; no finding recorded.

## `rev-opinion-clean-file-1`

- **fixture** — `opinion-clean`, the file-target run, revise round
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `3b1f791d`; packet `../editorial-479/runs/rev-opinion-clean-file-1/`; no finding recorded.

## `rev-opinion-clean-resp-2`

- **fixture** — `opinion-clean`, the response-target run, revise round
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, the lead gaining *och som tar bort telefonbokningen*, and the run's account.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `fail` — judges fail / fail, under the criterion's own clause that a clean text is not rewritten for taste. The clause added to the lead names only what the headline and the standfirst already state, so it adds no fact, and none of the protocol's five rejections fits it more closely.
  - `C1` — `pass` — judges split over *Conforms to the anatomy*; met under the split rule because the reply reports the change.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — #492
- **notes** — staged from `3b1f791d`; packet `../editorial-479/runs/rev-opinion-clean-resp-2/`; no closure-as-given finding; the standfirst kept. The lead finding cites the article anatomy's referent rule, which neither candidate changes.

## `rev-opinion-clean-file-2`

- **fixture** — `opinion-clean`, the file-target run, revise round
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, the lead gaining *digital bokning och telefonbokning*, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges fail / pass; split, met under the split rule because the reply reports the change.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none; #492 records the behaviour
- **notes** — staged from `3b1f791d`; packet `../editorial-479/runs/rev-opinion-clean-file-2/`; no closure-as-given finding; the standfirst kept.

## `rev-opinion-clean-resp-3`

- **fixture** — `opinion-clean`, the response-target run, revise round
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the no-change status in the reply; no text delivered and nothing written.
- **side effects** — `none` outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `skipped` — no text was delivered, and the file-target run of the pair answers the criterion; judges pass / pass on the reply.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `3b1f791d`; packet `../editorial-479/runs/rev-opinion-clean-resp-3/`; no finding recorded.

## `rev-opinion-clean-file-3`

- **fixture** — `opinion-clean`, the file-target run, revise round
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the reply.
- **side effects** — `work/output.md` created beside the input, as the output target asks; nothing else outside the Harness's configuration directory, by the runner's inventories of the private root, which was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — read against the row's frozen expectation in `expectation.md`, by the same rule as `R1`.
  - `O1` — `pass` — nothing created, changed or removed that the output target does not allow.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1` — `pass` — `rounds.md` keeps the first review's findings, each round's proposal, the session's words after it and the delivered text, from a complete trace.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — staged from `3b1f791d`; packet `../editorial-479/runs/rev-opinion-clean-file-3/`; no finding recorded.
