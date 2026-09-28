# redline — claude — 2026-09-28 — #415

- **record** — `redline-claude-2026-09-28-415`
- **date** — `2026-09-28`
- **ticket** — `#415`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session and every correction subagent in it, and every judge
- **harness** — Claude Code 2.1.283
- **corpus commit** — `708bff52`

## Run conditions

The plan is [`../editorial-415/plan.md`](../editorial-415/plan.md), frozen at `22ef6183` before the first run and not edited since, and the outcome is [`../editorial-415/results.md`](../editorial-415/results.md). The method is [#383's](../editorial-383/plan.md), with the staging [#400](../editorial-400/plan.md) used.

The pre-change arm was staged from `708bff52`, the commit #415's build began from, by `git archive` into an install holding `write/`, `redline/`, `proofread/`, `unslop/` and `kntnt/` side by side. The shim printed a `$LIBRARY` under the install, and the install was byte-identical to the archive after the last run. Each run was a fresh top-level session started by [`../editorial-415/runs/turn_run.sh`](../editorial-415/runs/turn_run.sh) with `--model=claude-opus-5-5 --effort=high`, in a private root removed on exit, with the staged Proofread copied into that root's home so that Redline's dependency check is met. Its prompt was [`../editorial-415/redline-turn-pre.md`](../editorial-415/redline-turn-pre.md) and a three-line message naming the working directory, the invocation and the run directory, and its working directory held only `input.md`. Each run's `seats.tsv` names `claude-opus-5-5` alone. No Codex Harness and no GPT model was started, controlled or invoked.

Each run was judged by two fresh `kntnt-opus-high` judges, blind to the arm, the model and the ticket, on [`../editorial-415/paratext-judge-brief.md`](../editorial-415/paratext-judge-brief.md), each in a neutral `mktemp -d` directory. The brief asks one question: does the returned text contain a headline, subheading or standfirst the run wrote or changed that asserts past a limiting sentence the returned text keeps? A run counts when both judges answer yes. No run counts, so the defect is recorded as not reproduced (ADR-0223). As the plan settles, the frozen briefs were not run, the post-change arm was not run, and no product file changed.

Every entry below records:

- the paratext count as `pass` where the run does not count;
- `R1`, `N1` and `C1` as `skipped`, because the plan runs the frozen briefs only where the pre-change arm shows the form;
- `A1`, `A2`, `N2`, `O1` and `S1` as `skipped`, because the readiness addendum says this is not their evaluation, and no inventory was taken;
- `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` as `skipped`, because they are not this evaluation's criteria.

A clean control was run once, to a response target, as the ticket fixes #383's matrix; the protocol's file-target run was not made, a declared narrowing.

## `pre-column-sv-r1-a`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Mallen har en ruta för allt utom poängen` rewritten as `Bibliotekets mötesmall har rutor för allt utom poängen`, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-column-sv-r1-b`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with one dash in the body changed and nothing else, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-column-sv-r2-a`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` rewritten as `Mötesmallen kan behöva ett varför bredvid klockslagen`, the missing standfirst and sections reported and not written, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-column-sv-r2-b`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` rewritten as `Mötesmallen frågar efter tid och deltagare, inte syfte`, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with a byline added under the headline and the third subheading rewritten as `Find out why people still ring before settling how booking works`, the headline unchanged, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with a byline added under the headline and the third subheading rewritten as `Measure staff time and ask why people still phone before deciding`, the headline unchanged, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with the headline `Keep the telephone until Lervik knows why it is used` rewritten as `Keep telephone booking until Lervik knows why it is used` and the byline given `By`, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the same headline and byline changes as `pre-opinion-en_GB-r2-a`, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-article-clean`

- **fixture** — `article-clean`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Swedish no-change status and no text.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-article-flawed`

- **fixture** — `article-flawed`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/article-flawed.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline rewritten as `Mätförsök i Björkskolan fann värden under 20 grader` and the standfirst and lead rewritten, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged, its one correction round rejected, and the run's findings.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/case-study-flawed.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the headline rewritten as `Elm Quays ärenden tilldelades snabbare under försöket`, the standfirst rewritten, both subheadings replaced and two added, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-column-clean`

- **fixture** — `column-clean`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Swedish no-change status and no text.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-column-flawed`

- **fixture** — `column-flawed`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/column-flawed.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Möten förändrar allt` rewritten as `Mötesmallen rymmer inte det vi ska förstå tillsammans`, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the piece with one sentence of the lead changed, headline, standfirst and subheadings unchanged, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/opinion-flawed.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text unchanged, its one correction round rejected, and the run's findings.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Swedish no-change status and no text.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, the corpus control `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, pre arm, staged from `708bff52`
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the page with the headline rewritten as `A review of how a shared room in your housing association is booked`, the six fragment headings replaced by one subheading and the opening paragraph rewritten, and the run's account.
- **side effects** — not inventoried, as the plan settles. The run directory held `work/input.md`, byte-identical to the fixture, an empty `scratch/` and the evaluator's `response.md` afterwards, and the private root was removed on exit.
- **criteria** —
  - paratext count — `pass` — both judges answer `no`; the run does not count.
  - `R1`, `N1`, `C1` — `skipped` — the frozen briefs are run only where the pre-change arm shows the form, and it does not.
  - `A1`, `A2`, `N2`, `O1`, `S1` — `skipped` — not this evaluation's, as the readiness addendum settles.
  - `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the run's `response.md`
- **defects filed** — none
- **notes** — none
