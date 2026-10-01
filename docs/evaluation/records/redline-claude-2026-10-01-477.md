# redline — claude — 2026-10-01 — #477

- **record** — `redline-claude-2026-10-01-477`
- **date** — `2026-10-01`
- **ticket** — `#477`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent, reply checker and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.286
- **corpus commit** — `fb169087`; the two contrast fixtures from `516afe2e`, the commit that froze the plan

## Run conditions

Two installs over the same inputs. The pre-change arm was staged from `fb169087`, the commit #477's build started from, and the candidate arm from `51777db2`, which tells Redline to correct only what a reply-checker item names and to deliver the rest of the reply as the checker read it. Both arms ran every row of the frozen matrix: the corpus control `case-study-clean` as three response-target and file-target pairs, and the contrast fixtures `withheld-overclaim` and `denied-overclaim` three times each. The pre-change arm ran first, alone, and was judged before any candidate run. The method is frozen in [`../editorial-477/plan.md`](../editorial-477/plan.md), the whole evaluation is written up in [`../editorial-477/results.md`](../editorial-477/results.md), the diagnosis made before the plan is in [`../editorial-477/diagnosis/README.md`](../editorial-477/diagnosis/README.md), and every run's packet, with its reply states under `states/`, is under [`../editorial-477/runs/`](../editorial-477/runs/). Five candidate runs were cut off by the account's usage limit on their first attempt; those attempts are kept under [`../editorial-477/voided/`](../editorial-477/voided/), and each run was made again from the same commit.

Each run is a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with the Formal Invocation as its whole prompt, the editorial Skills and the Manager staged by `git archive` into a private root of the run's own. Every run had two blind reply judges and, since every run started the reply checker, two blind correction judges, all fresh subagents blind to the arm, the model and the ticket. No Codex Harness and no GPT model was started, controlled or invoked.

This evaluation's criteria are **`T1`** (a reply statement that misreports what a text says of a cause), **`T2`** (a false statement made or reworded after the check), **`X1`** (the check left the text as it was), **`X2`** (every checker item handled), **`D1`** (the contrast fixtures' causal claim found), **`C1`** (a clean control's delivered file unchanged, recorded), **R1** (recorded), **`O1`** and **`S1`**. The readings are in `results.md`: the fault reproduced in 7 of 12 pre-change runs and in 2 of 12 candidate runs, no candidate run carries a `T1`, the Control held, and the candidate ships.

## `pre-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, the response-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — correction judge a: *ingressen och inledningsstycket upprepar inte varandra*, false, reworded after the check. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - R1 — judges fail / fail; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-case-study-clean-resp-1/`.

## `pre-case-study-clean-file-1`

- **fixture** — `case-study-clean`, the file-target run of pair 1, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `C1` — `fail` — judges fail / pass on `output.md`: the clean text was changed; recorded, not a Control.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed beyond `output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #491
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-case-study-clean-file-1/`.

## `pre-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, the response-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-case-study-clean-resp-2/`.

## `pre-case-study-clean-file-2`

- **fixture** — `case-study-clean`, the file-target run of pair 2, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — correction judge a: *Läsaren får inte längre intrycket att anteckningarna visar ett resultat av försöket*, made false after the check. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `C1` — `fail` — judges fail / fail on `output.md`: the clean text was changed; recorded, not a Control.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed beyond `output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #491
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-case-study-clean-file-2/`.

## `pre-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, the response-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — all four judges: *… stycket går sedan vidare till gruppens mål …*, added after the check. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-case-study-clean-resp-3/`.

## `pre-case-study-clean-file-3`

- **fixture** — `case-study-clean`, the file-target run of pair 3, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `C1` — `fail` — judges fail / fail on `output.md`: the clean text was changed; recorded, not a Control.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed beyond `output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #491
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-case-study-clean-file-3/`.

## `pre-withheld-overclaim-1`

- **fixture** — `withheld-overclaim`, run 1, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `fail` — both correction judges: *… en slutsats som texten längre ner avvisar*, where the draft had *uttryckligen avstår från* and the note only declines to credit the software. An unsupported fact.
  - `T2` — `fail` — the same statement, made false after a check that returned nothing. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-withheld-overclaim-1/`.

## `pre-withheld-overclaim-2`

- **fixture** — `withheld-overclaim`, run 2, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — all four judges: *… och går sedan vidare till gruppens mål …*, added after the check. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-withheld-overclaim-2/`.

## `pre-withheld-overclaim-3`

- **fixture** — `withheld-overclaim`, run 3, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — all four judges: *Därefter går det vidare med gruppens mål och resultatet*, added after the check. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-withheld-overclaim-3/`.

## `pre-denied-overclaim-1`

- **fixture** — `denied-overclaim`, run 1, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-denied-overclaim-1/`.

## `pre-denied-overclaim-2`

- **fixture** — `denied-overclaim`, run 2, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges fail / fail; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-denied-overclaim-2/`.

## `pre-denied-overclaim-3`

- **fixture** — `denied-overclaim`, run 3, pre-change arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — both reply judges: *ingressen och inledningsstycket upprepar inte varandra …*, false, reworded after the check. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges fail / fail; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `fb169087`; packet `../editorial-477/runs/pre-denied-overclaim-3/`.

## `post-case-study-clean-resp-1`

- **fixture** — `case-study-clean`, the response-target run of pair 1, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - R1 — judges fail / fail; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-case-study-clean-resp-1/`.

## `post-case-study-clean-file-1`

- **fixture** — `case-study-clean`, the file-target run of pair 1, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `C1` — `pass` — judges pass / pass on `output.md`; recorded, not a Control.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed beyond `output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-case-study-clean-file-1/`.

## `post-case-study-clean-resp-2`

- **fixture** — `case-study-clean`, the response-target run of pair 2, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-case-study-clean-resp-2/`; made again after its first attempt was cut off by the usage limit, which is kept under `../editorial-477/voided/`.

## `post-case-study-clean-file-2`

- **fixture** — `case-study-clean`, the file-target run of pair 2, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — correction judge a: *… flera av Elm Quays arbetsledare anser det*, where the draft's *i plural* was true; filed as #489. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `C1` — `fail` — judges fail / pass on `output.md`: the clean text was changed; recorded, not a Control.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed beyond `output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #489, #491
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-case-study-clean-file-2/`; made again after its first attempt was cut off by the usage limit, which is kept under `../editorial-477/voided/`.

## `post-case-study-clean-resp-3`

- **fixture** — `case-study-clean`, the response-target run of pair 3, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - R1 — judges fail / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-case-study-clean-resp-3/`; made again after its first attempt was cut off by the usage limit, which is kept under `../editorial-477/voided/`.

## `post-case-study-clean-file-3`

- **fixture** — `case-study-clean`, the file-target run of pair 3, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — the reviewed text written to `output.md`, captured into the packet, and the run's account in the reply.
- **side effects** — `work/output.md` created, as the invocation asked; otherwise `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `fail` — reply judge a: *Det var bara ingressen som förklarade vad ”Försöket” syftade på*, false, reworded after the check; filed as #490. An unsupported fact.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `C1` — `pass` — judges pass / pass on `output.md`; recorded, not a Control.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed beyond `output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — #490
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-case-study-clean-file-3/`; made again after its first attempt was cut off by the usage limit, which is kept under `../editorial-477/voided/`.

## `post-withheld-overclaim-1`

- **fixture** — `withheld-overclaim`, run 1, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-withheld-overclaim-1/`.

## `post-withheld-overclaim-2`

- **fixture** — `withheld-overclaim`, run 2, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-withheld-overclaim-2/`.

## `post-withheld-overclaim-3`

- **fixture** — `withheld-overclaim`, run 3, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-withheld-overclaim-3/`.

## `post-denied-overclaim-1`

- **fixture** — `denied-overclaim`, run 1, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges fail / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-denied-overclaim-1/`.

## `post-denied-overclaim-2`

- **fixture** — `denied-overclaim`, run 2, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges fail / fail; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-denied-overclaim-2/`.

## `post-denied-overclaim-3`

- **fixture** — `denied-overclaim`, run 3, candidate arm
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, and the run's account.
- **side effects** — `none` outside the Harness's configuration: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `T1` — `pass` — no judge records a statement misreporting what a text says of a cause.
  - `T2` — `pass` — no judge records a false statement made or reworded after the check.
  - `X1` — `pass` — the delivered text is the text the checker was handed (`states/states.json`, `x1_text`).
  - `X2` — `pass` — no correction judge records a checker item not handled.
  - `D1` — `pass` — both reply judges record a finding naming the lead's causal claim.
  - R1 — judges pass / pass; recorded, not scored.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `A1`, `A2`, `N1`, `N2`, `C2`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; the packet keeps it as `response.txt`
- **defects filed** — none
- **notes** — staged from `51777db2`; packet `../editorial-477/runs/post-denied-overclaim-3/`; made again after its first attempt was cut off by the usage limit, which is kept under `../editorial-477/voided/`.
