# redline — claude — 2026-09-20 — #377

- **record** — `redline-claude-2026-09-20-377`
- **date** — `2026-09-20`
- **ticket** — `#377`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for every run, every correction subagent and nested Proofread pass a run started, and every judge
- **harness** — Claude Code 2.1.278
- **corpus commit** — `0f490dd4`

## Run conditions

Two arms. The pre-change arm ran against the working tree at `4a932dd6`; the post-change arm and the ten controls ran against `0f490dd4`, which carries this ticket's change. The corpus itself is identical in both. The method was frozen before the first run in [`../editorial-377/plan.md`](../editorial-377/plan.md), with the turns and the two judge briefs beside it; the pre-change arm is written up in [`../editorial-377/diagnosis.md`](../editorial-377/diagnosis.md) and the rest in [`../editorial-377/results.md`](../editorial-377/results.md). Artefacts for every run are under [`../editorial-377/runs/`](../editorial-377/runs/).

Each run is one fresh subagent reading the Skill from a staged byte copy of `skills/editorial/{redline,proofread}` and `skills/kntnt` in the session scratchpad, with the Formal Invocation carried verbatim and one evaluator instruction added: save the reply to `response.md`. Each run's working directory held `input.md` and nothing else — no source material was supplied to Redline in any run. Every artefact was judged by two fresh judges, blind to the arm, to the model and to this ticket; where they split, both verdicts are recorded and neither is the oracle. No Codex Harness and no GPT model was started, controlled or invoked from this session.

Three criteria are this ticket's own, beside the corpus's `R1`: **N1**, no limiting sentence deleted or hardened unless the account reports a finding of class (a) or (b) a judge verifies from the input alone; **N2**, the account names every change to a claim's scope, certainty, attribution, chronology, causality or meaning; **C1**, each control meets its frozen expectation in the corpus's *Redline controls* table.

## `pre-column-sv-r1`

- **fixture** — the `column-sv-r1` draft #362 delivered, replayed neutrally against the pre-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and whatever account the run gave of itself.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `fail` — three differences: a limiting sentence deleted under class (a) and reported, a sentence added in the writer's first person asserting what the input nowhere asserts, and a locale dash correction. Both judges fail on the addition (a substantive edit).
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; the diagnosis it feeds is this ticket's.
- **notes** — judgements: [`../editorial-377/runs/pre-column-sv-r1/`](../editorial-377/runs/pre-column-sv-r1/judgement-a.md).

## `pre-column-sv-r2`

- **fixture** — the `column-sv-r2` draft #362 delivered, replayed neutrally against the pre-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and whatever account the run gave of itself.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `fail` — two limiting sentences deleted on the ground that the finding named the whole sentence, neither class (a) nor class (b) on both judgements, with the survival claims offered for them false against the returned text; an agentless claim given an actor (a substantive edit).
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; the diagnosis it feeds is this ticket's.
- **notes** — judgements: [`../editorial-377/runs/pre-column-sv-r2/`](../editorial-377/runs/pre-column-sv-r2/judgement-a.md).

## `pre-opinion-en_GB-r1`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, replayed neutrally against the pre-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and whatever account the run gave of itself.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `fail` — `I am not against digital booking.` became `I support digital booking` — hardening form 1 — outside any finding and unreported, beside an unreported serial-comma change (a substantive edit).
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; the diagnosis it feeds is this ticket's.
- **notes** — judgements: [`../editorial-377/runs/pre-opinion-en_GB-r1/`](../editorial-377/runs/pre-opinion-en_GB-r1/judgement-a.md).

## `pre-opinion-en_GB-r2`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, replayed neutrally against the pre-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, and whatever account the run gave of itself.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `split` — judge A fails, judge B passes. The limiting clause `and I do not accuse it of holding one` was deleted and reported; judge A finds neither class, judge B finds class (a). Four further differences, none reported.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none` from this run on its own; the diagnosis it feeds is this ticket's.
- **notes** — judgements: [`../editorial-377/runs/pre-opinion-en_GB-r2/`](../editorial-377/runs/pre-opinion-en_GB-r2/judgement-a.md).

## `post-column-sv-r1-a`

- **fixture** — the `column-sv-r1` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — one limiting sentence deleted, `Det är min reflektion, med den räckvidd en reflektion har.`; the reply reports the finding that the sentence before it already states the whole of that limit, and both judges verified class (a) from the input alone. No hardening.
  - `N2` — `pass` — one change to what a claim says, the opening's scope and meaning, named in the reply's *Ändrat* section with both wordings quoted and the question it leaves the author.
  - `R1` — `fail` — four differences; the opening claim widened from the missing decision box to the meeting's purpose, outside any visible defect (a substantive edit). Both judges.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — #383
- **notes** — judgements: [`../editorial-377/runs/post-column-sv-r1-a/`](../editorial-377/runs/post-column-sv-r1-a/judgement-a.md).

## `post-column-sv-r1-b`

- **fixture** — the `column-sv-r1` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted; all of them byte-identical on both judgements.
  - `N2` — `pass` — no change to what a claim says on either judgement; the one difference is the mechanical pass's.
  - `R1` — `pass` — one difference, a Swedish spaced en dash from the mechanical pass; the text otherwise byte-identical. Both judges.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/post-column-sv-r1-b/`](../editorial-377/runs/post-column-sv-r1-b/judgement-a.md).

## `post-column-sv-r2-a`

- **fixture** — the `column-sv-r2` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted; the two the pre-change replay deleted come back byte for byte on both judgements.
  - `N2` — `pass` — no change to what a claim says on either judgement.
  - `R1` — `pass` — one difference, the same locale dash; both limiting sentences the pre-change run deleted come back byte for byte. Both judges.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/post-column-sv-r2-a/`](../editorial-377/runs/post-column-sv-r2-a/judgement-a.md).

## `post-column-sv-r2-b`

- **fixture** — the `column-sv-r2` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted; the two the pre-change replay deleted come back byte for byte on both judgements.
  - `N2` — `pass` — no change to what a claim says on either judgement.
  - `R1` — `pass` — as `post-column-sv-r2-a`. Both judges.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/post-column-sv-r2-b/`](../editorial-377/runs/post-column-sv-r2-b/judgement-a.md).

## `post-opinion-en_GB-r1-a`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted on either judgement; `We make no claim to have funded or costed that trial` keeps its refusal and both disclaimed items, its subject alone moving.
  - `N2` — `pass` — four changes to what a claim says, and the reply names each under *What the corrections did to the claims* with both wordings and the finding it answered; only three consequent agreement fixes go unnamed.
  - `R1` — `split` — judge A passes on eight differences whose four claim changes are each reported; judge B fails on the officers' one stated reason rewritten on a vocabulary objection (a substantive edit).
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — #383
- **notes** — judgements: [`../editorial-377/runs/post-opinion-en_GB-r1-a/`](../editorial-377/runs/post-opinion-en_GB-r1-a/judgement-a.md).

## `post-opinion-en_GB-r1-b`

- **fixture** — the `opinion-en_GB-r1` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted on either judgement; the two-limb refusal survives word for word.
  - `N2` — `pass` — judge A finds one change to what a claim says and judge B two; the reply names both, and judge B holds that the second's class is asserted away. Split recorded, the stricter reading governing: named, and one classification disputed.
  - `R1` — `fail` — eight differences; `set … against` became `weigh … against` and two `channel` became `route`, unreported, on clean prose (a substantive edit). Both judges.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — #383
- **notes** — judgements: [`../editorial-377/runs/post-opinion-en_GB-r1-b/`](../editorial-377/runs/post-opinion-en_GB-r1-b/judgement-a.md).

## `post-opinion-en_GB-r2-a`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted on either judgement; all eleven, the two-limb refusal included, come back intact.
  - `N2` — `pass` — no change to what a claim says on either judgement.
  - `R1` — `pass` — four differences, all single-word substitutions moving no claim element; every limiting sentence intact. Both judges.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/post-opinion-en_GB-r2-a/`](../editorial-377/runs/post-opinion-en_GB-r2-a/judgement-a.md).

## `post-opinion-en_GB-r2-b`

- **fixture** — the `opinion-en_GB-r2` draft #362 delivered, reviewed against the post-change product
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply with its `kntnt` map, with the run's account of what it found and what it changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `N1` — `pass` — no limiting sentence weakened or deleted on either judgement.
  - `N2` — `pass` — no change to what a claim says on either judgement.
  - `R1` — `split` — judge A fails on three unreported `channel` to `route` substitutions in clean prose; judge B classes the same three as repairing a visible terminological split and passes.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — #383
- **notes** — judgements: [`../editorial-377/runs/post-opinion-en_GB-r2-b/`](../editorial-377/runs/post-opinion-en_GB-r2-b/judgement-a.md).

## `article-clean`

- **fixture** — `article-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — returned unchanged; heading, independent ingress and absent byline preserved, no technique selected, no numerical or missing-name finding. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-article-clean/`](../editorial-377/runs/control-article-clean/judgement-a.md).

## `article-flawed`

- **fixture** — `article-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — catastrophe and health certainty, the thrice-repeated lead and the late concept all detected and named; measured facts, exclusions and the funding uncertainty preserved. Both judges; both record the paragraph split as repaired but unnamed.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-article-flawed/`](../editorial-377/runs/control-article-flawed/judgement-a.md).

## `case-study-clean`

- **fixture** — `case-study-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — returned unchanged; customer agency, qualified appraisal, numbers and publisher disclosure preserved. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-case-study-clean/`](../editorial-377/runs/control-case-study-clean/judgement-a.md).

## `case-study-flawed`

- **fixture** — `case-study-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — supplier praise, the rescue claim and the causal contradiction detected and reported with the claim each removal took; the reservation and every measure preserved; unavailable support reported. Both judges; both record the pre-echoed quote and duplicate lead as repaired but unnamed.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-case-study-flawed/`](../editorial-377/runs/control-case-study-flawed/judgement-a.md).

## `column-clean`

- **fixture** — `column-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — returned unchanged; reflection, early point, recurrence, the single H1 and the 103-word paragraph preserved. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-column-clean/`](../editorial-377/runs/control-column-clean/judgement-a.md).

## `column-flawed`

- **fixture** — `column-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — the incompatible participation claims reported as unrepairable with the scene returned verbatim; generic opening and ending removed and reported; reflection and doubt preserved. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-column-flawed/`](../editorial-377/runs/control-column-flawed/judgement-a.md).

## `opinion-clean`

- **fixture** — `opinion-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — returned unchanged; polemical close, early thesis, attribution, administrative objection and cost uncertainty preserved, no hedge added. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-opinion-clean/`](../editorial-377/runs/control-opinion-clean/judgement-a.md).

## `opinion-flawed`

- **fixture** — `opinion-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — unsupported motives, the population inference against the booking denominator, the cost contradiction and the vague exhortation detected and named; qualified facts and the proposal preserved; the ending rebuilt from the actor already in the thesis. Both judges; both record two rewritten section headings as unreported.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-opinion-flawed/`](../editorial-377/runs/control-opinion-flawed/judgement-a.md).

## `web-copy-clean`

- **fixture** — `web-copy-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — returned unchanged; the information page survives with no sales template and no CTA, nothing invented. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-web-copy-clean/`](../editorial-377/runs/control-web-copy-clean/judgement-a.md).

## `web-copy-flawed`

- **fixture** — `web-copy-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reviewed text in the reply, with the run's findings and its account of what it removed or changed.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories differ nowhere in the working copy or the staged install, `work/input.md` is unchanged, and no scratch survived. `response.md` was created at the evaluator's request.
- **criteria** —
  - `C1` — `pass` — the calque, the abstract opener, the opaque headings and the misleading action label all detected and named; price, scope, timing, deliverables, conditions and destination preserved; the repair needing an absent fact reported unresolved. Both judges.
  - `R1` — `pass` — the same judgement as `C1` above, `R1` being what that row's frozen expectation is judged on.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`, and, for `case-study-flawed`, one judge's own scratch file written after the after-inventory.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this ticket's criteria; `R1`, `N1`, `N2` and `C1` are.
- **unresolved findings** — as the reply recorded them; see the artefacts.
- **defects filed** — `none`
- **notes** — judgements: [`../editorial-377/runs/control-web-copy-flawed/`](../editorial-377/runs/control-web-copy-flawed/judgement-a.md).

## What this evaluation exposed and did not settle

Redline still rewrites clean passages to taste, outside any finding and mostly without reporting it. Six of the sixteen post-change judgements fail `R1` on exactly that, and four of the twenty control judgements name it as their one blemish. It is the second half of what #362 found about this Skill, this ticket repaired the first half, and the readiness addendum scopes the body's *clean texts are returned unchanged* to the five clean controls alone. Filed for triage as [#383](https://github.com/Kntnt/skills/issues/383) rather than absorbed here. Two further issues the work owed are [#384](https://github.com/Kntnt/skills/issues/384), the frontmatter damage #362 recorded on `column-sv-r2`, and [#385](https://github.com/Kntnt/skills/issues/385), whether Unslop's whole-passage permission needs the same narrowing.
