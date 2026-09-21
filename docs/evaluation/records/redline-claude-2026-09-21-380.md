# redline — claude — 2026-09-21 — #380

- **record** — `redline-claude-2026-09-21-380`
- **date** — `2026-09-21`
- **ticket** — `#380`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for all eight runs, for every subagent a run started, and for all sixteen judges
- **harness** — Claude Code 2.1.278
- **corpus commit** — `8a37e57e`, whose `docs/evaluation/corpus/` is byte-identical to `9a29bad3`, the corpus commit [`redline-claude-2026-09-21-386.md`](redline-claude-2026-09-21-386.md) names, so the two records are comparable

## Run conditions

The eight source-blind `Redline` runs of the drafts the `Write` rows in [`write-claude-2026-09-21-380.md`](write-claude-2026-09-21-380.md) delivered: `article` in `sv` and `en_GB`, `web-copy` in `sv`, `opinion` in `sv` twice, and the three explicit technique rows. Each run's `input.md` is the draft its row delivered, its `kntnt` metadata included and nothing else; the run never saw the source package, and the invocation carries no `--genre` and no `--language`, so the draft's own metadata resolves both. That is what the pipeline tests. The method was frozen before the first run in [`../editorial-380/runs/plan.md`](../editorial-380/runs/plan.md), the results are in [`../editorial-380/runs/results.md`](../editorial-380/runs/results.md), and every artefact is under [`../editorial-380/runs/`](../editorial-380/runs/).

Each run is one fresh subagent with no history, told that a staged `SKILL.md` is its instructions and `$HERE` its directory, carrying the Formal Invocation verbatim. The staged install is the byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` taken from `8a37e57e` with `git archive` that served the whole wave, byte-identical to the repository at that commit after it as before. Each run's working directory held `input.md` and an empty `scratch/` and nothing else. No Codex Harness and no GPT model was started, controlled or invoked from this session.

Two statements beyond the invocation went into each turn, and they are the evaluator's rather than the Skill's: save the complete user-facing reply verbatim to `response.md`, and, where the Skill tells the run to ask the user something, state the question in the final reply and stop, because nobody is available to answer. No run's `response.md` write was refused.

Counted requirements are counted by script. `skills/kntnt/library/scripts/article_anatomy.py` as `8a37e57e` holds it was run by the evaluator from its own copy, never from the staged install, on each run's `work/input.md` and on the text it returned; the two JSON files sit beside the run, and their figures are the evidence for every counted line below. A judge was handed those figures and counted nothing itself. **On the three `web-copy` rows the anatomy does not apply**: the corpus binds that skeleton to the four article genres and leaves the scale advisory for `web-copy`, so the script's `conforms: false` there is description and fails nothing, and a finding against one of those counts would have been a wrong finding.

Every reply was judged by two fresh subagents, blind to each other, to this ticket, to the model identity and to any wording of the expected outcome beyond the criterion text. Each was also asked one question outside every criterion, because the Skill could not answer it: whether a change removed or altered something the source material required. Four of the eight rows answered yes, and that is [#392](https://github.com/Kntnt/skills/issues/392); it counts against no criterion here, because the Skill has no access to the material by contract.

The inventory scope is the protocol's wider one, as described in the Write record of the same wave, and the developer's working copy is covered by its git state rather than by a hash, a declared narrowing; both readings are identical before and after.

## `article-sv`

- **fixture** — `article-sv`, the pipeline `Redline` of the draft that row's `Write` run delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved genre, technique and language, all three from the text's own `kntnt` map, then carries the returned article in a fenced block and accounts for the claims that changed; wall time 863 seconds.
- **side effects** — `none` from the Skill. The before-and-after `sha256` inventories over the run directory and the staged install differ only by `response.md`, written on the evaluator's instruction, plus the evaluator's `delivered.md`, `anatomy-input.json`, `anatomy-delivered.json`, `start-epoch.txt`, `end-epoch.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty. The staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the returned article still does its job for a property manager and keeps its angle; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` for input and for output; every part present in order and doing its own job, the repaired headline no longer echoing the standfirst; both judges.
  - `P1` — `pass` — the reasoning survives the three changes intact; both judges.
  - `W1` — `pass` — the script reports `norms: []` for both texts; both judges.
  - `L1` — `pass` — native Swedish; both judges.
  - `L2` — `pass` — Swedish mechanics govern and nothing was introduced that breaks them; both judges.
  - `R1` — `pass` — three changes, each reported: the headline rewritten because it shared `pekar ut` and its opposition with the standfirst, which is a stated requirement of the headline reference and a legitimate finding; `därför` removed as a reason the text does not visibly support, reported as the one proposition withdrawn; and two sentences merged under the anatomy's plain statement that `Sentence length varies within the paragraph`, which the input's 8-, 8- and 7-word run departs from. Judge A fails `R1`, holding the merge a change of taste to a clean text and the `därför` diagnosis wrong because the preceding sentence supplies the ground; judge B passes, calling the merge a reported change of taste and the `därför` removal defensible and minimal. Neither reading names one of the protocol's five rejections, so the evaluator's verdict stands: the merge answers a plain statement of the anatomy rather than a *most* count or a *should*, and every change is reported.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — its evidence is *resolved configuration and actual loaded files*, and a Claude Code subagent's transcript cannot be read from the session that started it; answerable only from a Harness trace, which [#388](https://github.com/Kntnt/skills/issues/388) asks for.
  - `R2` — `skipped` — same reason: it asks what the trace establishes, Redline's one closing installed Proofread pass among it. The reply states that a closing mechanical pass ran and found nothing, and no criterion is recorded `pass` on a run's own account of itself.
  - `T2` — `skipped` — the text's metadata reads `technique: none`; the *Applies* column's baseline arm is not run here.
- **unresolved findings** — none reported as unresolved. The account names all three changes and states plainly that the headline rewrite dropped the headline's own `inte orsaker`, which survives in the standfirst, the third section and the quotation.
- **defects filed** — [#392](https://github.com/Kntnt/skills/issues/392), for the source loss below.
- **notes** — Judgements: [`../editorial-380/runs/article-sv/redline/judgement-a.md`](../editorial-380/runs/article-sv/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/article-sv/redline/judgement-b.md). **Split on `R1`**, both readings above. Judge B also records one nuance the account does not name: `Mätningen i Björkskolan` became `Björkskolans mätning`, which reseats the trial with the school — that omission is [#383](https://github.com/Kntnt/skills/issues/383), already open. **Source loss**, outside every criterion and not the Skill's to know: the source itself reads `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`, so the removed causal relation was the report's own, and the headline's `inte orsaker` carried the brief's `Forbidden inferences` in the headline. Both judges name both.

## `article-en_GB`

- **fixture** — `article-en_GB`, the pipeline `Redline` of the draft that row's `Write` run delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved configuration from the text's own map, carries the returned article in a fenced block, reports one unresolved finding and accounts for the one claim that changed; wall time 540 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the article does its job and keeps its angle; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` for both texts; both judges.
  - `P1` — `pass` — the argument is intact; both judges.
  - `W1` — `pass` — the script reports `norms: []` for both texts; both judges.
  - `L1` — `pass` — idiomatic British English; both judges.
  - `L2` — `pass` — `en_GB` mechanics govern; both judges.
  - `R1` — `pass` — one change, and it repairs a visible defect from the text alone: `why Björkskolan's classrooms turned cold` became `why the temperature in Björkskolan's classrooms fell below the limit`, because the article refuses that characterisation twice in its own voice. The account quotes the input clause, names the change and its ground, and states that nothing else moved; nothing was removed, and one finding the text cannot close — the lead promising what the office did next against a presupposition the body never states — is reported rather than invented away; both judges.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — the text's metadata reads `technique: none`.
- **unresolved findings** — one, reported with its passage and the reason it cannot be closed from the text: whether any adjustment was actually made after the walkthrough is a fact the artifact does not carry, so supplying it would be invention and cutting the sentence would cost the reader the limit.
- **defects filed** — none
- **notes** — Judgements: [`../editorial-380/runs/article-en_GB/redline/judgement-a.md`](../editorial-380/runs/article-en_GB/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/article-en_GB/redline/judgement-b.md). No split on any criterion. This is the one row where the source-blind review repaired a residual the `Write` run had reported and could not repair itself, and it found it from the text alone. **Source loss**: none; both judges checked every caveat the source requires and the change moves toward the source's own caution rather than away from it.

## `web-copy-sv`

- **fixture** — `web-copy-sv`, the pipeline `Redline` of the draft that row's `Write` run delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no change: the reply is the short no-change status the delivery contract prescribes — the resolved configuration from the text's own map, no findings, the correction budget unused and the text not repeated — and carries no fenced text, because there is no changed artifact to carry; wall time 324 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the page is returned doing its job unchanged; both judges.
  - `G2` — `pass` — judged on the `Web-copy` clause, the anatomy being advisory here: the script reports the same `conforms: false` for an absent byline and lead before and after, which are parts this genre need not have, so leaving them was right rather than an omission; both judges.
  - `P1` — `pass` — unchanged and followable; both judges.
  - `W1` — `pass` — advisory scale; the 61-character headline the script reports as a norm line is description on this genre; both judges.
  - `L1` — `pass` — native Swedish, unchanged; both judges.
  - `L2` — `pass` — Swedish mechanics, unchanged; both judges.
  - `R1` — `pass` — the restraint is the pass: the text came back byte-identical, the account says exactly that, and no finding was raised against a count the genre does not bind. Several passages invited taste-driven rewriting and were left alone; both judges.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason. The reply states that a closing Swedish proofreading pass found no mechanical error; no criterion rests on that statement.
  - `T2` — `skipped` — the text's metadata reads `technique: none`.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Judgements: [`../editorial-380/runs/web-copy-sv/redline/judgement-a.md`](../editorial-380/runs/web-copy-sv/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/web-copy-sv/redline/judgement-b.md). No split on any criterion. `delivered.md` is a byte copy of `work/input.md`, as the plan prescribes for a no-change reply; the short status carries no fence, which the delivery contract asks for. **Source loss**: none — nothing changed. The two findings the `Write` run had reported as remaining both survive here untouched, which is what a source-blind pass can be expected to do with them.

## `opinion-sv-r1`

- **fixture** — `opinion-sv`, the pipeline `Redline` of the draft the first of the two `opinion` runs delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved configuration from the text's own map, says the review gave three findings and that one correction round repaired all three, then carries the returned piece in a fenced block; wall time 587 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the piece does its job and keeps its position; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` for both texts, and the repaired subheading `Dubbelarbetet är verkligt` now stands on its own where the input's `Invändningen är verklig` depended on the sentence before it; both judges.
  - `P1` — `pass` — the rewritten section opening supplies the transition the input lacked; both judges.
  - `W1` — `pass` — the script reports `norms: []` for both texts; both judges.
  - `L1` — `pass` — native Swedish; both judges.
  - `L2` — `pass` — Swedish mechanics govern; both judges.
  - `R1` — `pass` — three changes, all repairs of visible defects and none against a requirement the text met: `Öppna beslut` → `Föreningen Öppna beslut` in a standfirst that has to stand alone, a section opening given its link to the proposal, and the anaphoric subheading made self-contained. Nothing was removed and no claim changed strength, subject, scope or modality; both judges.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — the text's metadata reads `technique: none`.
- **unresolved findings** — none. The account states that the re-review left no finding.
- **defects filed** — none of this row's own; [#383](https://github.com/Kntnt/skills/issues/383) is cited for the account below.
- **notes** — Judgements: [`../editorial-380/runs/opinion-sv-r1/redline/judgement-a.md`](../editorial-380/runs/opinion-sv-r1/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/opinion-sv-r1/redline/judgement-b.md). No split on any criterion. Both judges name the same weakness inside a passing `R1`: the account is a bare count — *three findings, one round, all repaired* — and names none of the three, so a reader of the reply cannot tell what moved. Both class it a qualitative concern rather than a rejection, since nothing was removed and no claim changed; it is the shape [#383](https://github.com/Kntnt/skills/issues/383) is open for. **Source loss**: none, and two of the three changes move toward the source's own wording.

## `opinion-sv-r2`

- **fixture** — `opinion-sv`, the pipeline `Redline` of the draft the second of the two `opinion` runs delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved configuration from the text's own map, says three findings were repaired and none is unresolved, carries the returned piece in a fenced block and accounts for one claim removed and one moved; wall time 795 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the piece still does its job and keeps its position; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` for both texts; both judges.
  - `P1` — `pass` — the reasoning is followable; both judges.
  - `W1` — `pass` — the script reports `norms: []` for both texts, and the repaired lead no longer restates the standfirst almost verbatim; both judges.
  - `L1` — `pass` — native Swedish; both judges.
  - `L2` — `pass` — Swedish mechanics govern; both judges.
  - `R1` — `fail` — a clean text changed to taste, and an account that does not hold. The script measured the input `conforms: true`, `failures: []`, `norms: []`, and the run deleted `, inte om att de som ringer skulle vara lata eller dyra` from it, then wrote `Texten avgränsar därmed sina anspråk precis lika långt som förut`, which is not accurate: the deleted clause is what bounded the objection. Two further edits — the first subheading and the section-1 opening — are not reported at all, though the account presents itself as covering what moved. Judge A passes `R1`, counting the removal reported and its risk volunteered and calling the other two undisclosed taste edits a qualitative concern; judge B fails on the same facts. Neither names one of the five rejections; the evaluator's verdict is `fail`, because `R1` states in terms that a clean text is not rewritten to satisfy taste, and two of the four edits here were both. The one genuine repair, the lead's echo of the standfirst, is reported well, and the trade-off in `föreslår` → `vill ha` is handed back to the user.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — the text's metadata reads `technique: none`.
- **unresolved findings** — none reported. Two of the four changes are not in the account at all, which is the failure above rather than an unresolved finding.
- **defects filed** — [#383](https://github.com/Kntnt/skills/issues/383) for the `R1` failure, already open and cited rather than filed again; [#392](https://github.com/Kntnt/skills/issues/392) for the source loss below.
- **notes** — Judgements: [`../editorial-380/runs/opinion-sv-r2/redline/judgement-a.md`](../editorial-380/runs/opinion-sv-r2/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/opinion-sv-r2/redline/judgement-b.md). **Split on `R1`**, both readings above. **Source loss**, outside every criterion and not the Skill's to know: the source requires the distinction the deleted clause carried — `Förvaltningens verkliga invändning … är dubbel administration, inte att telefonanvändare är lata eller dyra` — and judge B adds that `Tjänsteutlåtandet … föreslår` weakened to `vill ha` moves an attributed act.

## `article-abt`

- **fixture** — `article-abt`, the pipeline `Redline` of the draft that row's `Write` run delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved genre, technique and language, all three from the text's own `kntnt` map, says no findings remain, carries the returned article in a fenced block and accounts for the one claim that went out with the rewritten subheading and for the one mechanical correction; wall time 576 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the article does its job and keeps its angle; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` for both texts, and the replaced subheading now describes the section under it; both judges.
  - `P1` — `pass` — the reasoning is intact; both judges.
  - `W1` — `pass` — the script reports `norms: []` for both texts; both judges.
  - `L1` — `pass` — native Swedish; both judges.
  - `L2` — `pass` — Swedish mechanics govern, and the one mechanical correction is a locale repair: an English em dash before the quotation replaced by the Swedish tankstreck; both judges.
  - `R1` — `pass` — exactly two changes, both reported accurately: a subheading that claimed what its own section does not carry, replaced by one the section supports, and the dash. Nothing else moved, no clean passage was touched on taste, and the account states plainly which proposition left with the old subheading; both judges.
  - `T2` — `pass` — ABT is named in the text's metadata and in the reply, and the returned text keeps the arc it came with: a situation, a genuine complication and a supported response, with no crisis or triumph introduced by the review; both judges.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
- **unresolved findings** — none
- **defects filed** — [#392](https://github.com/Kntnt/skills/issues/392), for the source loss below.
- **notes** — Judgements: [`../editorial-380/runs/article-abt/redline/judgement-a.md`](../editorial-380/runs/article-abt/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/article-abt/redline/judgement-b.md). No split on any criterion. **Source loss**, outside every criterion and not the Skill's to know: the replaced subheading `Effekten av eventuella justeringar är inte mätt` was the text's only carrier of the source's `Inga justeringars effekt har ännu mätts`, and after the repair that limit is stated nowhere in the article. Both judges name it, both note that the repair creates no false claim and that no text-only repair preserved the limit.

## `article-pac`

- **fixture** — `article-pac`, the pipeline `Redline` of the draft that row's `Write` run delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved genre, technique and language, all three from the text's own `kntnt` map, says one correction round was delegated and verified by re-review with nothing left unresolved, carries the returned article in a fenced block and accounts for the two claims that moved; wall time 727 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the article does its job for a property manager; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` for both texts, and the rewritten headline — 57 characters against the input's 43, both inside the requirement — now names what was measured; both judges.
  - `P1` — `pass` — the reasoning is intact; both judges.
  - `W1` — `pass` — the script reports `norms: []` for both texts; both judges.
  - `L1` — `pass` — idiomatic British English; both judges.
  - `L2` — `pass` — `en_GB` mechanics govern; both judges.
  - `R1` — `pass` — three changes, each inside a named finding and each reported accurately: the headline rewritten because it named neither what was measured nor what to look at, `for the whole period` disambiguated to `for the whole four weeks` where *period* means a lesson period throughout, and a causal `therefore` removed as a reason the text sources nowhere. No claim was removed, and every sentence that bounds what the text asserts came back as it went in; both judges.
  - `T2` — `pass` — PAC is named in the text's metadata, and the returned text keeps the factual starting point leading through analysis to a warranted conclusion; both judges.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
- **unresolved findings** — none
- **defects filed** — [#392](https://github.com/Kntnt/skills/issues/392), for the source loss below.
- **notes** — Judgements: [`../editorial-380/runs/article-pac/redline/judgement-a.md`](../editorial-380/runs/article-pac/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/article-pac/redline/judgement-b.md). No split on any criterion. **Source loss**, outside every criterion and not the Skill's to know: the source reads `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`, so the removed `therefore` withdrew a reason the material gives the report. This is the same sentence, in English, that `article-sv` lost in Swedish — the two independent occurrences are why [#392](https://github.com/Kntnt/skills/issues/392) was filed. Both judges call the diagnosis sound source-blind and the error the cautious one.

## `web-copy-abt`

- **fixture** — `web-copy-abt`, the pipeline `Redline` of the draft that row's `Write` run delivered
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — changed: the reply states the resolved genre, technique and language, all three from the text's own `kntnt` map, carries the returned page in a fenced block, reports one finding it could not repair and accounts for three claims that moved; wall time 506 seconds.
- **side effects** — `none` from the Skill. The inventories differ only by `response.md` plus the evaluator's own files. `work/input.md` is unchanged, `work/scratch/` is empty, and the staged install appears in no diff.
- **criteria** —
  - `G1` — `pass` — the page does a service page's job; both judges.
  - `G2` — `pass` — judged on the `Web-copy` clause, the anatomy being advisory here; the script reports the same `conforms: false` for an absent byline and lead before and after, which this genre need not have; both judges.
  - `P1` — `pass` — the page can be followed in one pass, and the repaired naming makes the exclusions' reach plain; both judges.
  - `W1` — `pass` — advisory scale; no reader loss; both judges.
  - `L1` — `pass` — native Swedish; both judges.
  - `L2` — `pass` — Swedish mechanics govern, an em dash replaced by the Swedish en dash; both judges.
  - `R1` — `pass` — four changes, no removals, and three of the four reported: one offering called by two names in the sentence that fixes the exclusions' reach, an ambiguous `visa … instruktionen` resolved, a standfirst addition, and the dash. The unresolved finding — the page never says when the written summary arrives — is detected, stated as the reader's problem and reported rather than invented away, which the source expressly forbids inventing. Both judges name `Styrelsen` → `Ni` as the one change left out of a list the account introduces as complete, and both class it a qualitative concern rather than a rejection; both judges pass.
  - `T2` — `pass` — ABT is named in the text's metadata and in the reply, and the returned page keeps the section-level arc without a manufactured crisis; both judges.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
- **unresolved findings** — one, reported as unresolved with the reason: the page says when Svale answers an enquiry but never when the written summary — the engagement's main deliverable — arrives after the meeting, and the fact is not in the text and cannot be written out of it. The correction budget was spent, and the finding is handed on.
- **defects filed** — none of this row's own; [#383](https://github.com/Kntnt/skills/issues/383) is cited for the unreported change.
- **notes** — Judgements: [`../editorial-380/runs/web-copy-abt/redline/judgement-a.md`](../editorial-380/runs/web-copy-abt/redline/judgement-a.md) and [`judgement-b.md`](../editorial-380/runs/web-copy-abt/redline/judgement-b.md). No split on any criterion. Both judges also note that the account says a clause was `flyttad` where it was copied, and that the headline still says `Genomgång` while the body now says `Uppdraget` throughout. **Source loss**: none; the no-guarantee caveat, the non-order caveat and the link destination all survive, the source's prohibition on inventing a delivery time was honoured source-blind, and `Genomgången` → `Uppdraget` in fact restores the source's own scope. The `Write` residual `Uppdraget består av två delar:` survives review untouched.

## What this evaluation exposed and did not settle

Seven of the eight reviews pass every criterion the matrix applies to them, and sixty-six of the sixty-seven judged lines pass. The one failure is `opinion-sv-r2`, which deleted a clause from a conforming text, described the deletion under a claim of equivalence that does not hold, and left two further edits out of its account — the shape [#383](https://github.com/Kntnt/skills/issues/383) is already open for, and the shape three other rows show in smaller ways inside a passing `R1`.

`article-en_GB` is the counter-case worth keeping: from the text alone it found and repaired one of the two residuals its own `Write` run had reported and could not touch, and it reported the change exactly.

The question no criterion could reach is what the four rows lost. In half the wave a source-blind change removed or weakened a formulation the material required — twice the same causal connective in two languages, twice a clause bounding what the text claims. No judge counted it against `R1`, because the Skill cannot see the material by contract. It is [#392](https://github.com/Kntnt/skills/issues/392), and it is a question about how the two Skills meet rather than a bug in either.

Nothing here establishes whether the scoped contract loading happened, and **nothing here establishes whether Redline's closing Proofread pass ran**. `T1` and `R2` are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started; four of the eight replies assert that a closing mechanical pass ran, and no criterion is recorded `pass` on a run's own account of itself. The trace-bearing Claude-family harness is [#388](https://github.com/Kntnt/skills/issues/388).
