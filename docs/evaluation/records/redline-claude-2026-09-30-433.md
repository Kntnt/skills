# redline — claude — 2026-09-30 — #433

- **record** — `redline-claude-2026-09-30-433`
- **date** — `2026-09-30`
- **ticket** — `#433`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session and every correction subagent in it, and every judge
- **harness** — Claude Code 2.1.285
- **corpus commit** — `2afeb95e`

## Run conditions

One install, the pre-change arm, staged from `2afeb95e`, the branch head when #433's build began and the tree #429 leaves. It ran `opinion-flawed` three times and `article-flawed`, `case-study-flawed` and `column-flawed` once each, in three waves. The method is #402's in the parts the ticket's second readiness addendum lists, frozen for this ticket in [`../editorial-433/plan.md`](../editorial-433/plan.md) at `fc45e604`; the whole evaluation is written up in [`../editorial-433/results.md`](../editorial-433/results.md), and every run's packet is under `../editorial-433/runs/<run>/`.

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt, the editorial Skills and the Manager staged by `git archive` into a private root of its own. Every run was judged by two fresh judges blind to the arm, the model and the ticket, on [`../editorial-433/control-judge-brief.md`](../editorial-433/control-judge-brief.md), a byte copy of #402's, with the row's frozen cell at `2afeb95e` as the **Frozen expectation**. Whether an `opinion-flawed` run delivers the ending was read by the evaluating session from the returned text, by the check the plan states. No Codex Harness and no GPT model was started, controlled or invoked.

**The outcome is not reproduced.** Two of the three `opinion-flawed` runs deliver the ending in a section of its own, built from the body's actor and act, so the plan's gate holds: no candidate was committed, the candidate arm was not run, no product file changed, nothing was filed, and ADR-0225 records why.

Four criteria are this evaluation's own: **`R1`**, **`C1`** — `R1` against the row's frozen expectation — **`O1`** and **`S1`**. An `opinion-flawed` entry also carries the plan's ending check.

## `pre-control-opinion-flawed-1`

- **fixture** — `opinion-flawed`, run 1 of 3, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text returned as received in the reply, its one correction round rejected whole, with ten findings reported unresolved and the rejected round described.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - ending check — does not deliver — the round was rejected, and the text still ends `Nu är det dags att agera.` inside `## Diskussion`; both judges record the ending clause not applied.
  - `R1` — `pass` — judges pass / pass; every defect the row names is reported, and nothing was changed.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — ten, as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — the reply says the round was rejected because its new headline and its new ending put *Föreningen*'s demand to measure time use in the writer's voice, not for a heading repeating what it stands over. No open ticket owns that rejection. Packet `../editorial-433/runs/pre-control-opinion-flawed-1/`.

## `pre-control-opinion-flawed-2`

- **fixture** — `opinion-flawed`, run 2 of 3, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text in the reply, with a new headline, both subheadings rewritten and a new ending section `## Nästa steg är ett halvårs försök`, three findings reported unresolved, and the claim account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - ending check — delivers — the last section is new, holds the closing call, and names kommunstyrelsen and keeping telephone booking; both judges record the ending clause met.
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst, the opening that does not say what is booked, and the unintroduced *Föreningen*
- **defects filed** — none
- **notes** — packet `../editorial-433/runs/pre-control-opinion-flawed-2/`.

## `pre-control-opinion-flawed-3`

- **fixture** — `opinion-flawed`, run 3 of 3, pre-change arm
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text in the reply, with a new headline, both subheadings rewritten and a new ending section `## Både kommunstyrelsen och förvaltningen behöver agera`, two findings reported unresolved, and the claim account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - ending check — delivers — the last section is new, holds the closing call, and names kommunstyrelsen and keeping telephone booking; both judges record the ending clause met.
  - `R1` — `pass` — judges pass / pass; the ending's second sentence puts *Föreningen*'s demand in the writer's voice, and the reply reports it as an added claim.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — the missing standfirst and the unintroduced *Föreningen*
- **defects filed** — none
- **notes** — this run's re-review passed the attribution shift that got run 1's round rejected. Packet `../editorial-433/runs/pre-control-opinion-flawed-3/`.

## `pre-control-article-flawed`

- **fixture** — `article-flawed`, pre-change arm
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text in the reply, headed `Mätförsök i Björkskolan visar temperaturer under 20 grader`, with the missing byline and sections reported and not written, and the claim account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both note the closing `Kontakta oss.` is reported as vague rather than as a sales line unrelated to the explanation.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — packet `../editorial-433/runs/pre-control-article-flawed/`.

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed`, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text in the reply, headed `I Elm Quays försök tilldelades ärenden på två arbetsdagar`, with both subheadings rewritten, the missing byline and call to action reported and not written, and the claim account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `R1` — `pass` — judges pass / pass.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — packet `../editorial-433/runs/pre-control-case-study-flawed/`.

## `pre-control-column-flawed`

- **fixture** — `column-flawed`, pre-change arm
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text in the reply, headed `Vår mötesmall saknar vad vi ska förstå tillsammans`, with the missing standfirst, sections and call to action reported and not written, the contradiction reported and left, and the claim account.
- **side effects** — an empty directory `scratch/tmp/tmp.EjAfUo14lq` left in the private root, which the Harness refused to remove because it had become the session's working directory, as the reply says; `work/input.md` unchanged; the runner removed the root afterwards.
- **criteria** —
  - `R1` — `pass` — judges pass / pass; both headline defects the row names are reported.
  - `C1` — `pass` — judges pass / pass, read against the row's frozen expectation.
  - `O1` — `fail` — an incorrect side effect: the run left the empty temporary directory it made.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — #429's `pre-case-question-en_GB-r3` failed `O1` the same way. Packet `../editorial-433/runs/pre-control-column-flawed/`.
