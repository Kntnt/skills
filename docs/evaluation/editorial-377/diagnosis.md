# Diagnosis: what makes Redline take a limiting sentence, and what leaves the rest unreported

The pre-change arm of [the plan](plan.md), run on 2026-09-20 before any shipped file was touched. Four neutral replays of the four inputs #362 recorded, against the product at `4a932dd6` staged as `install-pre`; the turn is [`redline-turn-pre.md`](redline-turn-pre.md) and carries no hint of what is under investigation. Each replay was judged by two fresh `kntnt-opus-high` judges, blind to the arm, to the model and to this ticket, under [`redline-judge-brief.md`](redline-judge-brief.md). Artefacts: `runs/pre-*/`.

The vocabulary is the plan's: a difference is **a change to what a claim says** when it alters a claim's **scope, certainty, attribution, chronology, causality** or **meaning**, which is the list both correction briefs already hand the agent that makes the repair.

## What was replayed, and what came back

| Run | Differences | Limiting sentences deleted or weakened | Judge A | Judge B |
| --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | 3 | 1 deleted, class **(a)** on both judgements | R1 fail | R1 fail |
| `pre-column-sv-r2` | 4 | 2 deleted, **neither (a) nor (b)** on both judgements | R1 fail | R1 fail |
| `pre-opinion-en_GB-r1` | 4 | 1 weakened, **neither**, hardening form 1 on both judgements | R1 fail | R1 fail |
| `pre-opinion-en_GB-r2` | 5 | 1 deleted; judge A **neither**, judge B **(a)** | R1 fail | R1 pass |

Seven of the eight judgements fail `R1`. The one split is recorded as a split: on `pre-opinion-en_GB-r2` the two judges agree on what changed and disagree on whether the deleted clause's limit survives in the clause beside it. Neither is treated as the oracle; the stricter reading governs the diagnosis below.

The behaviour #362 reported is reproduced. `pre-column-sv-r2` deleted the same two sentences on the same stated ground, in a fresh session that had never seen that run.

## Every difference, classed

### `pre-column-sv-r1`

| # | Before | After | Class |
| --- | --- | --- | --- |
| 1 | `Jag har inte mätt det här hos andra, och jag påstår inget om möten i allmänhet. Det är min reflektion, med den räckvidd en reflektion har.` | the second sentence deleted | A **limiting sentence deleted**. Judge A classes the difference as the repair of a visible defect carried out as a deletion; judge B as a change to what a claim says (certainty, attribution). Both find class **(a)**: the retained sentence states the limit in full, so nothing hardens. |
| 2 | `Så jag vill prova en enkel fråga bredvid tiden: vad behöver vi förstå tillsammans?` | the same, plus `Den rymmer bara det ena av mina skäl: ett möte som finns till för att bygga förtroende har inget svar att ge på vad vi behöver förstå tillsammans.` | **A change to what a claim says — scope and meaning.** A sentence is added, in the writer's first person, asserting something the input nowhere asserts. Both judges. |
| 3 | `formuläret — bibliotekarien` | `formuläret – bibliotekarien` | **Mechanical correction**, Swedish spaced en dash. Both judges. |

All three are reported by the run, and reported accurately. This is the run the ticket body records as a pass, and it is still the behaviour the ticket wants of a limiting sentence. It fails `R1` for an unrelated reason both judges reach independently: difference 2 inserts an authorial claim and breaks the hinge `Där börjar tvivlet.` that no finding had named.

### `pre-column-sv-r2`

| # | Before | After | Class |
| --- | --- | --- | --- |
| 1 | `Det här är en iakttagelse av ett dokument, inte en scen från ett visst möte.` | deleted | A **limiting sentence deleted**, classed a change to what a claim says — scope and certainty (judge A), scope, certainty and meaning (judge B). Hardening form 3. **Neither (a) nor (b)** on both judgements. |
| 2 | `är något annat — att` | `är något annat – att` | **Mechanical correction**, Swedish spaced en dash. **Not reported.** |
| 3 | `att tid i kalendern så lätt behandlas som ett resultat i sig` | `att vi så lätt behandlar tid i kalendern som ett resultat i sig` | **A change to what a claim says — attribution and scope.** An agentless claim acquires an actor. Both judges. |
| 4 | `Det är min reflektion, inte något jag har mätt hos andra.` | deleted | A **limiting sentence deleted**, classed a change to what a claim says — certainty and scope. Hardening form 3. **Neither (a) nor (b)** on both judgements. |

The run reports 1, 3 and 4 and states of the two deletions: *"Två meningar ströks i sin helhet, båda för att anmärkningen pekade ut hela meningen som bristen."* Both judges accept that the removals are disclosed and both find the survival claims offered for them false against the returned text: `Jag granskar bibliotekets mötesmall` does not say that the piece is not a scene from an occasion, and `Det som retar mig` does not say that the behaviour described is unmeasured. Differences 3 and 4 compound: the claim that gains an actor is the claim that loses its *not measured* bound.

### `pre-opinion-en_GB-r1`

| # | Before | After | Class |
| --- | --- | --- | --- |
| 1 | `That is thin ground for making the change permanent.` | deleted | **A change to what a claim says — meaning and scope**, and the repair of a visible defect on both judgements: it echoes the lede. Not a limiting sentence: its work is to assess a case, not to bound what the text asserts. **Reported, accurately.** |
| 2 | `## Six months, both routes, and something to measure` | serial comma dropped | **A change of taste.** Both judges: the input form is standard en_GB, so nothing was corrected. **Not reported.** |
| 3 | `I am not against digital booking.` | `I support digital booking;` | A **limiting sentence weakened**: **a change to what a claim says — certainty and meaning**, and **hardening form 1**, a refusal to assert becoming an assertion. **Neither (a) nor (b)** on both judgements. **Not reported.** |
| 4 | `I am against settling its shape before the council can…` | `my objection is to settling its shape before the council can…` | **A change of taste**, consequent on 3. **Not reported.** |

The reply names one repair and closes *"No findings remain."* Three of the four differences stand outside it.

### `pre-opinion-en_GB-r2`

| # | Before | After | Class |
| --- | --- | --- | --- |
| 1 | `keeping both channels` | `keeping both routes` | **A change of taste.** **Not reported.** |
| 2 | `and I do not accuse it of holding one` | deleted | A **limiting clause deleted**. Judge A: a change to what a claim says — scope, secondarily certainty; hardening form 3 and, on its reading, form 2. Judge B: attribution, secondarily certainty; hardening form 3. **Split on the class: judge A finds neither (a) nor (b); judge B finds (a).** **Reported**, with a survival claim judge A rejects and judge B accepts. |
| 3 | `It can adopt the September removal` | `The board can adopt the September removal` | Judge A: a change of taste. Judge B: the repair of a visible defect, the pronoun's only antecedent being in the heading. **Split.** **Not reported.** |
| 4 | `keep a channel` | `keep a route` | **A change of taste**, consequent on 1. **Not reported.** |
| 5 | `before the channel goes` | `before the route goes` | **A change of taste**, consequent on 1. **Not reported.** |

## What authorised it

For each difference above that deletes or weakens a limiting sentence, or that the account does not report, the sentence of a loaded resource that authorised it, or the statement that none does.

The resources a run loads are fixed by `SKILL.md` step 5, and were read in full for this section: `base.md`, `base.review.md`, the resolved genre (`genres/column.md` and `genres/column.review.md`; `genres/opinion.md` and `genres/opinion.review.md`), `anti-slop.md`, `web-craft.md` and `web-craft.review.md`, and the `composition`, `review` and `anti-slop` scopes of `languages/sv.md` and `languages/en_GB.md`. No technique was resolved in any run. The correction agent additionally receives `references/correction.md`, and the run itself is following `SKILL.md`.

### The removals: three sentences of the shipped contract, each quoted

Every deletion of a limiting sentence in all four runs stands on the same permission, stated three times in the files the run and its correction agent read:

- `skills/editorial/redline/SKILL.md`, step 7: *"Where the finding named the whole claim as the defect, its removal may stand, but the delivery still names the claim that went."*
- `skills/editorial/redline/references/correction.md`, **What a repair may take with it, and what it may not**: *"Where the defect a finding names is the whole of the passage — an opening that would sit in front of any text, a closing that restates what the reader has just read, a claim credited to nobody that the text cannot source — removing it may be the repair, and any claim removed with it must be named in your return."*
- the same file, the before-and-after paragraph: *"Every claim you received must still appear with its scope, certainty, attribution, chronology, causality and meaning intact unless the finding named the whole claim as the defect."*

`pre-column-sv-r2` invoked the first of these in as many words — *"båda för att anmärkningen pekade ut hela meningen som bristen"* — and `pre-opinion-en_GB-r2` invoked it as *"The finding named that clause itself as the defect"*. A criterion that left these three sentences standing would be met by a run that reproduced the defect exactly.

`base.review.md` supplies the account half rather than the permission: *"A claim removed because the finding named that claim itself remains part of the removal account."*

### What made the sentences findings in the first place

Three loaded sentences turn a limiting sentence into a finding, and none of them excludes one:

- `anti-slop.md`, **False contrasts**: *"A negation used as a run-up to the actual claim: This isn't a tool. It's a way of working. … The rejected half was never in play, so the sentence spends the reader's attention establishing a position nobody held. State the second half on its own."* This is what authorises `pre-opinion-en_GB-r1`'s difference 3. *I am not against digital booking. I am against settling its shape…* has the catalogue's exact shape, and the catalogue's remedy — state the second half on its own — is the change that was made. The premise the pattern rests on is false here: the rejected half **was** in play, which is why the sentence is in an opinion piece by a named spokesperson, and stating the second half alone is what turns a refusal to oppose into a declaration of support.
- `base.md`, Expression: *"Each passage earns its place. Repetition may establish an independent entry point, explain a hard idea or give a deliberate rhetorical return; merely saying the same thing again does none of these."* This is what authorises the deletions in `pre-column-sv-r1`, `pre-column-sv-r2` and `pre-opinion-en_GB-r2`: each run judged a caveat to be saying again what a nearby caveat already said. Nothing in the loaded path tells a review that the thing being said again is a limit, or that two caveats bounding different things are not one caveat twice.
- `languages/en_GB.md`, `## Review`: *"Watch for hedges in chains — somewhat rather more likely, it may perhaps be the case that — where British understatement has stopped being restraint and become evasion. One hedge does work; three cancel each other."* Loaded on both English runs, and readable as licence against a sentence carrying two refusals.

The one guard in the loaded path is `anti-slop.md`'s opening: *"where a phrase is doing real work — a hedge that marks genuine doubt, a repetition that lands — the pattern is not present and nothing is changed."* It is stated as an exception to a pattern rather than as a test a reviewer applies to a sentence, it says nothing about how a limit is recognised in the text alone, and it did not hold in any of the four runs. The two genre review halves say *"Preserve purposeful fragments, rhetorical recurrence, pointed imagery and admitted doubt"* (`column.review.md`) and *"Preserve a successful polemic, its authorial responsibility and its qualifications"* (`opinion.review.md`) — each a requirement, neither a diagnostic for telling a qualification from a redundancy.

### The changes of taste: no loaded resource authorises them

`pre-column-sv-r2` difference 3, `pre-opinion-en_GB-r1` differences 2 and 4, and `pre-opinion-en_GB-r2` differences 3 and 5 have **no authorising sentence in any loaded resource**. Every resource read above runs the other way:

- `references/correction.md`: *"Repair what the findings name and nothing else. Preserve everything the findings do not concern: every sentence, every fact, every quotation, every code sample, every heading, every piece of formatting and every line of frontmatter among them comes back exactly as you received it — a repair that improves a paragraph nobody complained about is a change nobody asked for and nobody will review."*
- `base.review.md`: *"Preserve functioning wording, voice and formatting outside the finding; concision is not permission to summarise the text away."*
- `web-craft.review.md`: *"Preserve successful genre-specific voice and structure instead of standardising them."*

One exception: `pre-opinion-en_GB-r2`'s `channel` → `route` substitutions (differences 1, 4 and 5) are authorised, by `anti-slop.md`, **Synonym cycling**: *"One thing given a new name every time it is mentioned… Pick the clear name and repeat it."* The pattern is real and the input does alternate; what the catalogue cannot see is that the input's two words name two things.

### Why none of it was reported

Every unreported difference above is a change the run made to a text and did not name. No loaded resource required it to. The account duty, stated in each of the four places the run or its agent reads it, covers removals and nothing else:

- `SKILL.md` step 11: *"Where any round removed a passage carrying a claim … report every removed claim separately and say which repair removed or attempted to remove it."*
- `SKILL.md` step 7: *"record every removed claim, whether the finding named that whole claim as the defect or the claim sat beside the defect."*
- `references/correction.md`, **What you return**: *"Where any repair removed a passage carrying a claim, name every removed claim and say which finding made the claim itself the defect."*
- `base.review.md`: *"A claim removed because the finding named that claim itself remains part of the removal account."*

`pre-opinion-en_GB-r1` is the clearest case. Its reply says *"no claim was removed"* and *"No findings remain"*, and both statements are true of the duty as written: no claim was removed. A claim's certainty was raised, a heading was restyled and a sentence pair was recast, and the contract has no sentence under which any of the three is owed to the reader. `pre-column-sv-r2` is the same failure on a mechanical correction: the one legitimate repair in the run is the one thing the account does not mention.

## The cause, in three sentences

A limiting sentence is visible in the text alone, and nothing Redline loads says how to recognise one or what a review owes it; three loaded sentences — the false-contrast pattern, the repetition rule, and the English hedge-chain line — make one a finding, and the sole guard against them is an aside inside a pattern.

Once it is a finding, the whole-passage permission, stated three times in Redline's own files, lets a correction agent delete the sentence entire, because a finding that names the sentence and nothing inside it satisfies *the finding named the whole claim as the defect* exactly.

And a run that changes what a claim says without removing it owes the reader nothing, because the account duty is written about removals, which is why eight of the sixteen differences in these four runs were delivered without a word.
