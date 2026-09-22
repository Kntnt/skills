# redline — claude — 2026-09-22 — #383

- **record** — `redline-claude-2026-09-22-383`
- **date** — `2026-09-22`
- **ticket** — `#383`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for every run, every correction subagent and nested Proofread pass a run started, and every judge
- **harness** — Claude Code 2.1.278
- **corpus commit** — `3167fb68`

## Run conditions

Two arms. The pre-change arm ran against the working tree at `3167fb68`; the post-change arm, the ten controls and one pre-change control replay ran against the tree object `5af1390d`, which carries this ticket's change and whose content the closing commit holds. The corpus is identical in both. The method was frozen before the first run in [`../editorial-383/plan.md`](../editorial-383/plan.md), with the two turn files and the two judge briefs beside it, both briefs byte copies of #377's; the whole evaluation is written up in [`../editorial-383/results.md`](../editorial-383/results.md) and the artefacts for every run are under [`../editorial-383/runs/`](../editorial-383/runs/).

**The pre-change arm was replayed rather than taken from #377.** #383 permits re-use only if nothing Redline loads has changed since `0f490dd4`, the corpus commit [`redline-claude-2026-09-20-377.md`](redline-claude-2026-09-20-377.md) names. Twenty-seven files differ, five of them added since — `article-anatomy.md`, its review extension, `headlines.md`, its review extension and `scripts/article_anatomy.py`, all of which Redline now loads and measures with for the four article genres — so the four inputs were replayed once each before any wording was touched.

Each run is one fresh subagent reading the Skill from a staged byte copy of `skills/editorial/{redline,proofread}` and `skills/kntnt`, written with `git archive` from the commit or tree it names and never copied from a working tree, with the Formal Invocation carried verbatim and one evaluator instruction added: save the reply to `response.md`. Each run's working directory held `input.md` and nothing else before its turn was dispatched. Every artefact was judged by two fresh judges, blind to the arm, to the model and to this ticket; where they split, both verdicts are recorded and neither is the oracle. No Codex Harness and no GPT model was started, controlled or invoked from this session.

Nine criteria are this evaluation's own. Besides the corpus's **`R1`**: **`A1`**, no difference counts against the run by #383's rule — both judges classing it as taste outside any finding, or either doing so where the reply covers it in neither the claim account nor the closing summary; **`A2`**, a judge finds no statement false against the returned text and no kind of difference the account leaves uncovered; **`N1`** and **`N2`** as #377 defines them; **`C1`**, each control meets its frozen expectation; **`C2`**, the three control blemishes #377 recorded are absent or covered; **`O1`**, the Output Target contract, source preservation and cleanup; **`S1`**, no source material was supplied.

**Two declared narrowings of the protocol.** The repository-working-copy half of the inventory is `git status --porcelain --untracked-files=all` in each of the two checkouts rather than a hash of either tree, because both carry work in progress while the runs are made and a hash would report an editing session's changes as a run's. And re-using #377's judge briefs as #383 requires means no judge was handed a measured anatomy figure; several counted a control's limits themselves, and the one place a count decides a verdict is `case-study-clean`.

## `pre-column-sv-r1`

- **fixture** — the `column-sv-r1` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and the run's account of itself.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — seven and nine differences; three and six changes to a claim. Both judges: a clean column rewritten to an anatomy — a 92-word third-person ingress, three headings and an appended reader instruction. A substantive edit.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim.
  - `N2` — `pass` — every change to a received claim named in the reply, with one loose tally recorded in the judgements.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; it is the comparison arm.
- **notes** — changes to a claim, judge A / judge B: 3 / 6. Judgements: [`../editorial-383/runs/pre-column-sv-r1/judgement-a.md`](../editorial-383/runs/pre-column-sv-r1/judgement-a.md).

## `pre-column-sv-r2`

- **fixture** — the `column-sv-r2` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and the run's account of itself.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — seven and eight differences; one change to a claim each. Both judges: the headline replaced, a 48-word ingress and three headings imposed on a clean first-person column to reach `conforms: true`. A substantive edit.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim.
  - `N2` — `pass` — every change to a received claim named in the reply, with one loose tally recorded in the judgements.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; it is the comparison arm.
- **notes** — changes to a claim, judge A / judge B: 1 / 1. Judgements: [`../editorial-383/runs/pre-column-sv-r2/judgement-a.md`](../editorial-383/runs/pre-column-sv-r2/judgement-a.md).

## `pre-opinion-en_GB-r1`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and the run's account of itself.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — eleven and twelve differences; two and four changes to a claim. Both judges: the headline recast to a word-and-character norm, a lead manufactured for an absent anatomy slot, three subheadings turned from labels into arguments. A substantive edit.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim.
  - `N2` — `pass` — every change to a received claim named in the reply, with one loose tally recorded in the judgements.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; it is the comparison arm.
- **notes** — changes to a claim, judge A / judge B: 2 / 4. Judgements: [`../editorial-383/runs/pre-opinion-en_GB-r1/judgement-a.md`](../editorial-383/runs/pre-opinion-en_GB-r1/judgement-a.md).

## `pre-opinion-en_GB-r2`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and the run's account of itself.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — four and five differences; one and none. Both judges: a clean text with no visible defect rewritten to norms, decisively the ten-word headline cut to seven. A substantive edit.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim.
  - `N2` — `pass` — every change to a received claim named in the reply, with one loose tally recorded in the judgements.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; it is the comparison arm.
- **notes** — changes to a claim, judge A / judge B: 1 / 0. Judgements: [`../editorial-383/runs/pre-opinion-en_GB-r2/judgement-a.md`](../editorial-383/runs/pre-opinion-en_GB-r2/judgement-a.md).

## `post-column-sv-r1-a`

- **fixture** — the `column-sv-r1` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — nine and seven differences; both judges class the ingress, the three headings and the appended reader exhortation as taste answering no finding. A substantive edit.
  - `A1` — `fail` — not met — both judges class the ingress, three headings and the appended exhortation as taste outside any finding.
  - `A2` — `fail` — not met — judge B finds `inget står kvar med förändrad räckvidd, säkerhet, källa, kronologi, orsak eller mening` false against the heading `Ett möte utan beslut har också ett skäl`; the uncovered-kind half is met, judge A recording every difference as reported and none misreported.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply states the review left nothing outstanding.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 0 / 3. Judgements: [`../editorial-383/runs/post-column-sv-r1-a/judgement-a.md`](../editorial-383/runs/post-column-sv-r1-a/judgement-a.md).

## `post-column-sv-r1-b`

- **fixture** — the `column-sv-r1` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — six and eight differences; both judges class the ingress, three headings and the closing reader instruction as additions answering no defect. A substantive edit.
  - `A1` — `fail` — not met — the same five additions, classed as taste by both judges.
  - `A2` — `fail` — not met — judge A finds the qualifier `allt formulerat ur det texten redan säger` false for the ingress clause `lämnar läsaren något att se efter i sin egen mall`, which is true only of the run's own second addition. Every difference is reported.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply states `Inga fynd kvarstår`.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 0 / 0. Judgements: [`../editorial-383/runs/post-column-sv-r1-b/judgement-a.md`](../editorial-383/runs/post-column-sv-r1-b/judgement-a.md).

## `post-column-sv-r2-a`

- **fixture** — the `column-sv-r2` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — six and seven differences; both judges class the rewritten headline, the ingress and the two headings as taste, the reply grounding them in `artikelanatomin kräver`. A substantive edit.
  - `A1` — `fail` — not met — headline, ingress and both headings classed as taste outside any finding by both judges.
  - `A2` — `fail` — not met — judge A finds the closing assurance `inget står kvar med ändrad omfattning, säkerhet, tillskrivning …` not true of the text returned. Every difference is reported.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply states `Inga fynd återstår`.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 3 / 2. Judgements: [`../editorial-383/runs/post-column-sv-r2-a/judgement-a.md`](../editorial-383/runs/post-column-sv-r2-a/judgement-a.md).

## `post-column-sv-r2-b`

- **fixture** — the `column-sv-r2` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — six and nine differences; both judges class the replaced title, the three-sentence ingress and the three headings as taste, the reply grounding the ingress in `där anatomin kräver en`. A substantive edit.
  - `A1` — `fail` — not met — title, ingress and three headings classed as taste outside any finding by both judges.
  - `A2` — `fail` — not met — both judges find `inget påstående har tagits bort eller fått ändrad omfattning, säkerhet, attribution, kronologi, kausalitet eller innebörd` false for the title and two ingress sentences. Every difference is reported.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply reports the round as sufficient.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 2 / 3. Judgements: [`../editorial-383/runs/post-column-sv-r2-b/judgement-a.md`](../editorial-383/runs/post-column-sv-r2-b/judgement-a.md).

## `post-opinion-en_GB-r1-a`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — ten and twelve differences; both judges class the manufactured lead, the shortened headline and the two rewritten subheadings as taste, the reply grounding two of them in `Two parts the anatomy requires`. A substantive edit, and an unsupported fact in the lead on both judgements.
  - `A1` — `fail` — not met — the lead, the headline and two subheadings classed as taste outside any finding by both judges.
  - `A2` — `fail` — not met — both judges find `Nothing. No passage carrying a claim was removed, and no claim was left standing with its scope … moved` false against a headline that lost `Lervik's` and a lead that added two assertions. Every difference is reported at least generically.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `fail` — both judges record the headline's loss of `Lervik's` as a change of scope the reply reports only as `the headline shorter`. A substantive edit reported as something else.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — one, reported: the third subheading repeats its own first sentence, left standing because the one-round budget was spent.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 2 / 3. Judgements: [`../editorial-383/runs/post-opinion-en_GB-r1-a/judgement-a.md`](../editorial-383/runs/post-opinion-en_GB-r1-a/judgement-a.md).

## `post-opinion-en_GB-r1-b`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — eleven differences on both judgements; both judges class the 60-word standfirst, the shortened headline and three of four rewritten subheadings as taste, the reply grounding them in the anatomy and in length. A substantive edit.
  - `A1` — `fail` — not met — standfirst, headline and three subheadings classed as taste outside any finding by both judges.
  - `A2` — `fail` — not met — both judges find the reply's statement that the shortened headline `asks for less than it did` false, dropping the place name making it ask for more; judge B also finds the byline's stated position wrong. Judge A records `Not reported: nothing.`
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply reports all eight findings repaired.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 1 / 5. Judgements: [`../editorial-383/runs/post-opinion-en_GB-r1-b/judgement-a.md`](../editorial-383/runs/post-opinion-en_GB-r1-b/judgement-a.md).

## `post-opinion-en_GB-r2-a`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — nine differences on both judgements; both judges class the rewritten headline, the added standfirst and the closing subheading as taste, the reply naming the headline's word count as the ground. A substantive edit.
  - `A1` — `fail` — not met — headline, standfirst and closing subheading classed as taste outside any finding by both judges.
  - `A2` — `fail` — not met — judge A finds the altered claim filed under a heading opening `No claim was removed`, and `Every sentence that bounds what the article claims stands exactly as it arrived` true of the input's sentences but not of the two bounds the new standfirst restates loosely. Every difference is reported.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply reports no findings outstanding.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 2 / 1. Judgements: [`../editorial-383/runs/post-opinion-en_GB-r2-a/judgement-a.md`](../editorial-383/runs/post-opinion-en_GB-r2-a/judgement-a.md).

## `post-opinion-en_GB-r2-b`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, replayed neutrally
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, the claim account, the closing summary, and any finding carried forward.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — six differences on both judgements; both judges class the shortened headline, the added standfirst and the byline form as taste, the reply naming the headline word-count norm as the ground. A substantive edit.
  - `A1` — `fail` — not met — headline, standfirst and byline form classed as taste outside any finding by both judges.
  - `A2` — `fail` — not met — both judges find the claim account's `Nothing else shifted in scope, certainty, attribution, chronology or causality` contradicted by the reply's own finding 2 on the same page. Every difference but the byline's position is reported.
  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened on either judgement; all of them verbatim, both halves of every two-part disclaimer included.
  - `N2` — `pass` — every change to a received claim is named in the reply, with both wordings.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — three, reported: the standfirst repeats the lead, the standfirst loses the pilot counts' scope, and the shortened headline no longer names the condition the piece argues for. Two of the three are damage the round itself caused.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — changes to a claim, judge A / judge B: 2 / 2. Judgements: [`../editorial-383/runs/post-opinion-en_GB-r2-b/judgement-a.md`](../editorial-383/runs/post-opinion-en_GB-r2-b/judgement-a.md).

## `control-article-clean`

- **fixture** — `article-clean`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — returned unchanged with no findings; every preservation clause verbatim and every named rejection avoided, both judges having measured the limits themselves.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no difference of any class.
  - `A2` — `pass` — no account to be wrong about and nothing left uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — the run returned the short no-change status rather than reprinting the text; both judges note it and neither counts it under `R1`. Judgements: [`../editorial-383/runs/control-article-clean/judgement-a.md`](../editorial-383/runs/control-article-clean/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-article-flawed`

- **fixture** — `article-flawed`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — the catastrophe and health certainty, the late concept, the 187-word lead, the missing byline, the absent subheadings and the closing sales line all detected; the 39-character headline failed on truthfulness, not length; measured facts, exclusions and the funding caveat verbatim.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no judge classes a difference as taste outside a finding.
  - `A2` — `pass` — both judges find every difference reported and no statement false; the four claim changes are each disclosed, one with an offer to revert.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — one, reported: the byline is named as missing and left unfilled, no author being named anywhere.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — **`C2` met here**: the paragraph split #377 recorded as repaired-but-unnamed is now covered by the closing summary — *det 187 ord långa ledet är delat i ett led och fyra stycken fördelade på två sektioner*. The removed headline claim #386 found missing is now the first item of the account. New reservation: the standfirst/lead repetition is repaired but diagnosed as overclaiming rather than as the repetition. Judgements: [`../editorial-383/runs/control-article-flawed/judgement-a.md`](../editorial-383/runs/control-article-flawed/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-case-study-clean`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — one difference: the subheading `## Två perioder med olika arbetsbelastning` became `## Anteckningen redovisar en kortare mediantid men ingen orsak`. Both judges class it as a taste rewrite of a conforming text and both note the new heading falls outside the 36–39-character band the expectation names. A substantive edit.
  - `C1` — `fail` — the run misses the `conforms to the anatomy` clause of its frozen expectation.
  - `A1` — `fail` — both judges class the subheading rewrite as taste outside any finding.
  - `A2` — `fail` — judge B finds the length change omitted from the account; judge A finds the reply reporting the change while denying any scope shift.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply reports the one finding repaired.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — the miss is **not** pre-existing: `pre-control-case-study-clean` below passes on both judgements. What the replay does not establish is that this ticket's change caused it — none of the six changed files authorises a heading rewrite, and the two runs raised different findings on the same text. Filed. Judgements: [`../editorial-383/runs/control-case-study-clean/judgement-a.md`](../editorial-383/runs/control-case-study-clean/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-case-study-flawed`

- **fixture** — `case-study-flawed`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — the first-person supplier praise, the rescue line, the pre-echoed quote, the duplicate standfirst/lead and the causal contradiction all detected and quoted; the missing byline and the missing call to action reported and left unfilled with nothing invented; the customer's reservation, both quotations and every measure verbatim.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no judge classes a difference as taste outside a finding.
  - `A2` — `fail` — judge A finds a recast `under åtta veckor` and an added `ny programvara` unreported; both judges find the removed-claim tally short by one, `Resultatet bevisar allt` being absent from it.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — six, reported: three needing material the text does not give, and three the round's own repair created.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — **`C2` met here**: the pre-echoed quote and the duplicate lead, repaired but unnamed in #377, are both now detected and quoted. Reservation: the two non-descriptive subheadings were replaced without their defect being named. Judgements: [`../editorial-383/runs/control-case-study-flawed/judgement-a.md`](../editorial-383/runs/control-case-study-flawed/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-column-clean`

- **fixture** — `column-clean`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — returned unchanged with no findings; the 83-word paragraph unsplit, the reflection, the early point, the purposeful recurrence, the admitted doubt and the non-commercial ending intact, every named rejection avoided.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no difference of any class.
  - `A2` — `pass` — no account to be wrong about and nothing left uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — the run returned the short no-change status rather than reprinting the text; both judges note it and neither counts it under `R1`. Judgements: [`../editorial-383/runs/control-column-clean/judgement-a.md`](../editorial-383/runs/control-column-clean/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-column-flawed`

- **fixture** — `column-flawed`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — the incompatible participation claims, the empty opening, the tautology and the recycled ending all addressed; every surviving sentence character for character; the scene's contradiction reported rather than replaced with an invented memory.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no judge classes a difference as taste outside a finding.
  - `A2` — `fail` — both judges find the headline replaced with its defects never named and its replaced claim absent from the removed-claims list.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — six, reported: three the round's own repair created, the missing call to action, and the text's having too little material for the genre.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — both judges also record that the call to action was detected and then declared impossible though the reflection supports it. Judgements: [`../editorial-383/runs/control-column-flawed/judgement-a.md`](../editorial-383/runs/control-column-flawed/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-opinion-clean`

- **fixture** — `opinion-clean`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — returned unchanged with no findings; the polemical final sentence, the early thesis, the attribution, the administrative objection, the cost uncertainty and the council's named decision verbatim, and no hedge added.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no difference of any class.
  - `A2` — `pass` — no account to be wrong about and nothing left uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — #386 found an invented exclusion clause in this control's lead and the whole account reading `Inga anmärkningar kvarstår.` That does not recur: the text comes back unchanged. Judgements: [`../editorial-383/runs/control-opinion-clean/judgement-a.md`](../editorial-383/runs/control-opinion-clean/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-opinion-flawed`

- **fixture** — `opinion-flawed`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — the unsupported motives, the population inference against the booking denominator, the cost non sequitur and the vague final exhortation all detected, repaired from the text's own material and accounted for; the qualified facts and the proposal verbatim.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no judge classes a difference as taste outside a finding.
  - `A2` — `fail` — both judges find the reply stating that the anatomy conforms without deviation while the ending still sits inside the last section with no section of its own.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — one, reported: the new standfirst does not stand alone, a defect the round's own repair created.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — **`C2` met here**: the two label subheadings #377 recorded as rewritten and unreported are now a stated finding — *de två etikettunderrubrikerna* — and both judges confirm that clause of the expectation is met. Judgements: [`../editorial-383/runs/control-opinion-flawed/judgement-a.md`](../editorial-383/runs/control-opinion-flawed/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-web-copy-clean`

- **fixture** — `web-copy-clean`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — returned unchanged with no findings; the complete information page survives with no sales template and no CTA, the short headings and uneven section lengths untouched, and nothing invented about the form's destination or function.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no difference of any class.
  - `A2` — `pass` — no account to be wrong about and nothing left uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — the run returned the short no-change status rather than reprinting the text; both judges note it and neither counts it under `R1`. Judgements: [`../editorial-383/runs/control-web-copy-clean/judgement-a.md`](../editorial-383/runs/control-web-copy-clean/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply where the run changed anything, otherwise the short no-change status, with whatever account the run gave.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — the Swedish idiom calque, the abstract audience opening, the six opaque headings and the misleading `Book and pay` label all detected and named; price with VAT, scope, timing, deliverables, the three link conditions and the destination verbatim; the licensed regrouping used on-page content only.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no judge classes a difference as taste outside a finding.
  - `A2` — `fail` — both judges find the rewritten headline printing `SEK 4,800` without `including VAT` — which the run reports against itself as an open finding — and judge A finds the headline's `shared-room booking` inference unreported.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — two, reported: the headline's unqualified price, a defect the round's own repair created, and a `three working days` the resolved `en_US` would write as business days.
- **defects filed** — `none` from this run on its own; the residuals are filed once for the whole evaluation, as #397 to #401.
- **notes** — the run's closing summary is the most complete of the eighteen, naming each kind of difference down to the merged one-sentence sections and the relocated link paragraph. Judgements: [`../editorial-383/runs/control-web-copy-flawed/judgement-a.md`](../editorial-383/runs/control-web-copy-flawed/judgement-a.md); the frozen expectation is `expectation.md` beside it.

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean`, replayed against the pre-change install
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in the reply, with one difference and an account of it.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — one difference, `Försöket pågick i åtta veckor` to `Ett försök med loggen pågick i åtta veckor`, which both judges class as the repair of a visible defect: a definite noun phrase whose antecedent stood only in the standfirst.
  - `C1` — `pass` — the run meets every clause of its frozen expectation on both judgements.
  - `A1` — `pass` — no judge classes the one difference as taste.
  - `A2` — `pass` — both judges find the account complete in both directions — the one change reported and no change that did not happen.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply reports the one finding repaired.
- **defects filed** — `none` from this run on its own; it establishes that `control-case-study-clean`'s miss is not pre-existing.
- **notes** — this is the whole of the revise-and-remeasure round the plan allowed — one run and two judges, spent on establishing whether the one control miss predates the change rather than on a second post-change arm. `A1` and `A2` are recorded here for comparability; the criteria as #383 states them range over the eighteen post-change runs and this is not one of them.

## What was filed

Five residuals, [#397](https://github.com/Kntnt/skills/issues/397) to [#401](https://github.com/Kntnt/skills/issues/401), each `needs-triage` naming #383 and each stated in [`../editorial-383/results.md`](../editorial-383/results.md): #397, the article anatomy's missing parts being repaired by authoring prose into a finished text, which is what `A1` measures on the four drafts and what `R1` fails on in both arms; #398, the claim account's assurance being written about claims received and so false once a run adds one, which is the whole of `A2`'s failure there; #399, `case-study-clean`'s `C1` miss, present in the post-change arm and absent from the pre-change replay, which one run per arm cannot separate from variance; #400, three control accounts still leaving a repaired defect unnamed; and #401, a correction subagent's scratch path still being shared between concurrent runs, observed once and reported by the run that hit it.

## What this record does not say

It says nothing about whether Redline's scoped contract loading happened or whether its closing Proofread pass ran, `T1` and `R2` being answerable only from a trace this method does not keep. It says nothing about Unslop, which receives the same two procedural changes and which #385 measures. And it makes no comparison with any GPT-family record: the protocol forbids one from this session, and none was opened.
