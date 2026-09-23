# redline — claude — 2026-09-21 — #386

- **record** — `redline-claude-2026-09-21-386`
- **date** — `2026-09-21`
- **ticket** — `#386`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for every run, every correction subagent and nested Proofread pass a run started, and all twenty judges
- **harness** — Claude Code 2.1.278
- **corpus commit** — `9a29bad3`

## Run conditions

Ten runs: the eight `Redline controls` of the four article genres, all in `sv`, and the two pipeline `Redline` rows `column-sv` and `case-study-sv`, each on the draft its `Write` row delivered. The method was frozen before the first run in [`../editorial-386/runs/plan.md`](../editorial-386/runs/plan.md), with the turns and the three judge briefs beside it; the results are in [`../editorial-386/runs/results.md`](../editorial-386/runs/results.md) and every artefact under [`../editorial-386/runs/`](../editorial-386/runs/). The two `Write` rows of the same wave are in [`write-claude-2026-09-21-386.md`](write-claude-2026-09-21-386.md).

Each run is one fresh subagent with no history, told that a staged `SKILL.md` is its instructions and `$HERE` its directory, carrying the Formal Invocation verbatim. The staged install is a byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` taken from `9a29bad3` with `git archive`, in the session scratchpad; one install served the whole wave. Each run's working directory held `input.md` and an empty `scratch/` and nothing else, and no source material was supplied to any Redline run. The two pipeline rows carry no `--genre` and no `--language`: the draft's own `kntnt` map resolves both, which is what the pipeline tests. The dispatching session's own seat is `claude-fable-5-1`, and it ran and judged nothing itself. No Codex Harness and no GPT model was started, controlled or invoked from this session.

Two statements beyond the invocation went into each turn, and they are the evaluator's rather than the Skill's: save the complete user-facing reply verbatim to `response.md`, and, where the Skill tells the run to ask the user something, state the question in the final reply and stop. No run's `response.md` write was refused, so all ten are the runs' own and are declared evaluator additions rather than Skill side effects.

Counted requirements are counted by script. `skills/kntnt/library/scripts/article_anatomy.py` as `9a29bad3` holds it was run by the evaluator, from its own copy and never from the staged install, on each `work/input.md` and each `delivered.md`; the JSON sits beside the run as `anatomy-input.json` and `anatomy-delivered.json`, and its figures are the evidence for every counted line below. A judge was handed those figures and counted nothing itself.

Every reply was judged by two fresh subagents, blind to each other, to this ticket, to the model identity and to any wording of the expected outcome beyond the criterion text and — for a control — the row's frozen expectation, copied verbatim from the corpus README to `expectation.md` in the run directory. Where they split, both readings are recorded and neither is the oracle: no dissenting judge in this wave named one of the protocol's five unconditional rejections, so each split line reads the evaluator's verdict, with both readings in the evidence sentence and the dissent in `notes`.

## `article-clean`

- **fixture** — `article-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `no change`: a three-line reply stating the resolved genre and language, that no technique applied, that the review and the proofread pass found nothing, and `Texten är oförändrad, och inget har skrivits.`; `delivered.md` is a byte copy of `work/input.md`. Wall time 280 seconds.
- **side effects** — `none` from the Skill: the before-and-after `sha256` inventories over the run directory and the staged install differ only by the evaluator's own files — `response.md`, written by the run on the evaluator's instruction, and `delivered.md`, `anatomy-input.json`, `anatomy-delivered.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — one angle held from `Mätförsöket i Björkskolan visar när, inte varför` to the close, every figure attributed to a dated report and the causes explicitly left open; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []` and every part in order: a 48-character headline, a 46-word standfirst in one paragraph, the byline `Text: Hedda Lund`, a 33-word lead in one paragraph before the first H2, two sections with 32- and 34-character subheadings, and an ending whose next step is non-commercial; both judges.
  - `P1` — `pass` — the sensor's measurement is defined before placement is made to matter, `alltså` and `därför` carry real inferences, and the conclusions stop where the report stops; both judges.
  - `W1` — `pass` — the script reports `norms: []`: headline 48 characters and 7 words, standfirst 46 words, subheadings 32 and 34 characters, longest paragraph 45 words, and across the whole text `paragraphs_of_two_or_three_sentences: 5` of `paragraphs: 7` with `sections_of_two_or_three_paragraphs: 2` of `sections: 2`; standfirst and lead open on `Under` and `En`; both judges.
  - `L1` — `pass` — native Swedish syntax and compounding throughout, including the fronted `Hur länge temperaturen låg under den anger rapporten inte`; both judges.
  - `L2` — `pass` — Swedish quotation marks, `daterad 12 mars 2026` with a lower-case month, `20 grader Celsius` rather than an imported unit form, and nothing invented because nothing was changed; both judges.
  - `R1` — `pass` — `delivered.md` is byte-identical to `work/input.md` and the account says exactly that, and no finding was made against the 48-character headline, the 46-word standfirst, the 32- and 34-character subheadings, the one-sentence or four-sentence paragraph, one section's paragraph count or the Swedish `Text:` byline form; both judges. None of the five rejections.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — its evidence is *resolved configuration and actual loaded files*, and a Claude Code subagent's transcript cannot be read from the session that started it; answerable only from a Harness trace, which [#388](https://github.com/Kntnt/skills/issues/388) asks for.
  - `R2` — `skipped` — same reason: it asks what the trace establishes, Redline's one closing installed Proofread pass included.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be; the reply states that the `article` genre names none.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Judgements: [`../editorial-386/runs/article-clean/judgement-a.md`](../editorial-386/runs/article-clean/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/article-clean/judgement-b.md). No split on any criterion. The frozen expectation is at [`expectation.md`](../editorial-386/runs/article-clean/expectation.md) in the run directory. The wave's shared method notes — the single rolling wave, the judges writing while later runs were in flight, the brief copies handed to judges by path, the corrected helper run, the other session's use of the repository working copy, the three finished agents stopped after their replies were saved — are in [`../editorial-386/runs/results.md`](../editorial-386/runs/results.md) and apply to every entry here.

## `article-flawed`

- **fixture** — `article-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reviewed text in the reply, preceded by the resolved configuration and the spent one-round budget, and followed by four remaining findings and a section headed `Vad som hände med påståendena`. Wall time 645 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, written by the run on the evaluator's instruction, and `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty. The reply itself states that no `kntnt` frontmatter existed or was added and that nothing was written to disk, which the inventory bears out.
- **criteria** —
  - `G1` — `pass` — the reader learns what the report measured, what the figure does and does not mean (`vilket inte är en lagregel`), what the trial could not answer and what happens next under what uncertainty; both judges.
  - `G2` — `fail` — the returned text still calls the reader to nothing, its last paragraph being the property office's next step, and it carries the subheading `Elin Rask vill se användningstiderna först` over a sentence repeating both the name and *användningstider*; the script's only remaining failure is `byline` `absent`, correctly reported and left unfilled, and the subheadings measure 43, 27 and 42 characters, all inside 70. Judge B fails, judge A passes on the ground that neither shortfall stops a part from working; the evaluator's verdict is `fail`, because the round itself created the echo and the corpus README holds that a reported irreparable finding still leaves the text labelled as having a remaining quality problem. None of the five rejections: both are reported.
  - `P1` — `pass` — `operativ temperatur` is defined where the body first uses it, the transitions are real, and with the health certainty gone nothing claims more than the trial measured; both judges.
  - `W1` — `pass` — the script reports `norms: []` for the delivered text against two for the input (`lead` `187 words`, and standfirst and lead `both open on “givarna”`); headline 52 characters and 6 words, standfirst 35 words in one paragraph, lead 53 words in one paragraph, subheadings 43, 27 and 42 characters, each section with at least one paragraph; both judges, each recording `sections_of_two_or_three_paragraphs: 1` of `sections: 3` as a *most* statement read across the text rather than a failure.
  - `L1` — `pass` — the new headline, standfirst and attributions are idiomatic Swedish, and the one clumsy stretch is carried over verbatim from the input rather than introduced; both judges.
  - `L2` — `pass` — `den 12 mars 2026`, `under 20 grader`, `14 av 120 lektionspass` and sentence-case headings all keep Swedish form, and no new date or figure appears; both judges.
  - `R1` — `fail` — the account opens its ledger `Fyra påståenden togs bort, och alla fyra togs bort därför att fyndet pekade ut just dem som defekten`, which is stated as complete and is not: the headline `Givarna räddar skolan från en katastrof` was replaced and the standfirst rewritten wholesale, and neither appears anywhere in it. Judge A fails on that, judge B passes while recording the same headline omission as *the run's one accounting gap*; the evaluator's verdict is `fail`. None of the five rejections — nothing false entered the text and every remaining finding is reported — this is the account failing its own completeness claim, which is [#383](https://github.com/Kntnt/skills/issues/383).
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace, which a session cannot read for a subagent it started ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — four, all reported with the text. The missing byline, reported as absent and left unfilled. The subheading `Elin Rask vill se användningstiderna först` repeating its first sentence, which the reply states the correction round itself created. The sentence `Givarna registrerade temperaturer under 20 grader.` restating the sentence before it, likewise created by the round when it split the original opening. And the absent call to action, which the reply says cannot be filled without inventing a task the material does not carry.
- **defects filed** — [#389](https://github.com/Kntnt/skills/issues/389), [#383](https://github.com/Kntnt/skills/issues/383)
- **notes** — Judgements: [`../editorial-386/runs/article-flawed/judgement-a.md`](../editorial-386/runs/article-flawed/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/article-flawed/judgement-b.md). Two splits, recorded above and neither resolved by a rejection: on `G2` judge A passes and judge B fails; on `R1` judge A fails and judge B passes. Judge B additionally marks the subheading `Placeringen redovisas, men inte dess effekt` as an echo of its one sentence, where judge A does not. Both judges record that the 39-character input headline drew no length finding, which the frozen expectation requires. The repair-created subheading echo is the second instance of the pattern [#389](https://github.com/Kntnt/skills/issues/389) is filed for; the first is `case-study-sv` Redline below.

## `case-study-clean`

- **fixture** — `case-study-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `no change`: a two-line reply stating the resolved genre and language, that no technique applied, and `Texten är oförändrad, korrigeringsbudgeten är outnyttjad och inget har skrivits till disk.`; `delivered.md` is a byte copy of `work/input.md`. Wall time 235 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — situation, action, sourced results and the customer's own appraisal, with the angle that agreeing the categories cost more than logging the cases held from headline to ending; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []`: a 36-character headline, a 40-word standfirst in one paragraph, the byline `Text: Iris Falk`, a 43-word lead in one paragraph before the first H2, three sections with 36-, 39- and 38-character subheadings, the publisher stance stated outright and a call to action built from the supplied checklist link; both judges.
  - `P1` — `pass` — the exclusions are stated before the comparison is drawn on, and the one inference the figures invite is refused by the text itself; both judges.
  - `W1` — `pass` — the script reports `norms: []`: headline 36 characters and 4 words, standfirst 40 words, subheadings 36, 39 and 38 characters, longest paragraph 40 words, and across the whole text `paragraphs_of_two_or_three_sentences: 6` of `paragraphs: 8` with `sections_of_two_or_three_paragraphs: 3` of `sections: 3`; standfirst and lead open on `Elm` and `Att`; both judges.
  - `L1` — `pass` — native idiom throughout, including the double-object `anteckningen tillskriver därför inte skillnaden programvaran` and the Swedish speech dash with a trailing attribution; both judges.
  - `L2` — `pass` — `den 4 december 2025` in Swedish form, small numbers spelled out against `31 ärenden`, speech dashes rather than quotation marks, and nothing invented because nothing was changed; both judges.
  - `R1` — `pass` — `delivered.md` is byte-identical to `work/input.md`, the account says so accurately, and no finding was made against the 36-character headline, the 40-word standfirst, the 36–39-character subheadings, the one-sentence or four-sentence paragraph, one section's paragraph count or the `Text:` byline form; both judges. None of the five rejections.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Judgements: [`../editorial-386/runs/case-study-clean/judgement-a.md`](../editorial-386/runs/case-study-clean/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/case-study-clean/judgement-b.md). No split on any criterion. Judge A records that the account is thin — it names no part it checked — and holds that a reporting economy on a text with no finding is not an unresolved finding.

## `case-study-flawed`

- **fixture** — `case-study-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reviewed text in the reply under `## Texten`, followed by five remaining findings and a `Borttagna och ändrade påståenden` section; the reply states the budget was one round and was spent with findings left. Wall time 838 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — the returned text argues from what the trial measured and what it cannot settle, with the publisher's interest declared and the customer's reservation left standing; both judges.
  - `G2` — `fail` — three of the genre's parts are absent from the returned text: the byline, which the script reports as the delivered text's one failure (`byline` `absent`); the ending's call to action, the text supplying no offer, link or contact route; and the customer's background and course of action. None can be supplied from the text, and the run reports all three as needing material it does not have, which is credited under `R1`. Judge A fails, judge B passes on the ground that the reporting is what the criterion asks of a source-blind run; the evaluator's verdict is `fail`, because the parts are missing from the delivered text. None of the five rejections: every one is reported.
  - `P1` — `pass` — the figures are stated, then bounded, and no inference is drawn past the bound; the subheading `Siffrorna säger inte varför tilldelningen gick fortare` tells the reader in advance that no attribution is coming; both judges.
  - `W1` — `fail` — the counted scale is met throughout on the script's figures (headline 52 characters and 8 words, standfirst 38 words in one paragraph, lead one paragraph, subheadings 42 and 54 characters, longest paragraph 37 words, `norms: []` against the input's `both open on “elm”`), but the lead's whole first sentence restates the standfirst and adds only a pointer to the article itself, so a reader who has read the standfirst is restarted before the text moves. Judge A fails on that reader loss, judge B passes it as typicality; the evaluator's verdict is `fail`, because the run concedes the overlap in its own finding 4 with the budget spent and both sentences are its own, so following the norm was possible. None of the five rejections: it is reported.
  - `L1` — `pass` — `som är noga med vad de inte kan avgöra`, `Arbetsledaren efterlyser en längre upptakt` and the correct genitive `Elm Quays försöksanteckning` are native Swedish, with one sober voice across the new material; both judges.
  - `L2` — `pass` — the Swedish speech dash with the attribution inside the line, `31` as a figure against `åtta veckor` and `två arbetsdagar` spelled out, and no date, currency or conversion anywhere; both judges.
  - `R1` — `fail` — the account states `Korrigeringsrundan tog bort fyra påståenden och flyttade tre` and then lists exactly that, while the headline `Vår fantastiska lösning räddade Elm Quay` and both subheadings — `Kunden fick en gemensam bild` and `Resultatet bevisar allt` — were replaced and appear nowhere in it; both judges, who also record the dangling cross-reference to a `fynd 6` the reply does not contain. None of the five rejections: the repairs are right and the direction of every unreported change lowers a claim; the completeness claim is what fails, which is [#383](https://github.com/Kntnt/skills/issues/383).
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — five, all reported with the text and the first three marked as unrepairable without material the text lacks: the missing byline, left unfilled; the missing call to action, the text supplying no offer, link or contact route; the missing customer background, prompting situation and roll-out; the standfirst and lead still overlapping; and the first section standing as a subheading and a bare quotation after the pre-echo was removed.
- **defects filed** — [#383](https://github.com/Kntnt/skills/issues/383)
- **notes** — Judgements: [`../editorial-386/runs/case-study-flawed/judgement-a.md`](../editorial-386/runs/case-study-flawed/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/case-study-flawed/judgement-b.md). Two splits, recorded above and neither resolved by a rejection: on `G2` and on `W1`, judge A fails and judge B passes. `R1` is unanimous. Both judges record that every defect the frozen expectation names as visible was found and handled, that nothing was invented, and that the customer's reservation and every factual measure survive verbatim.

## `column-clean`

- **fixture** — `column-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `no change`: the reply opens `Ingen ändring.` and states that neither the review nor the proofread pass found anything and that the one-correction budget is unused; `delivered.md` is a byte copy of `work/input.md`. Wall time 208 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — a personal reflection on one concrete artefact with the angle held to the last line, offering the reader something to consider rather than a procedure; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []`: a 44-character headline, a 41-word standfirst in one paragraph, the byline `Text: Nora Vik`, a 39-word lead in one paragraph before the first H2, two sections with 37-character subheadings, and an ending that invites the reader to try the question and stands beside admitted doubt; both judges.
  - `P1` — `pass` — nothing is used before the lead introduces it, the transitions turn the argument rather than decorate it, and the text claims less than its own case would license; both judges.
  - `W1` — `pass` — headline 44 characters and 8 words, standfirst 41 words, subheadings 37 characters each, and across the whole text `paragraphs_of_two_or_three_sentences: 4` of `paragraphs: 6` with `sections_of_two_or_three_paragraphs: 2` of `sections: 2`; the script's one `norms` entry is section 1's paragraph at `83 words` against the 80-word *should*, a departure both judges hold the text better for, the paragraph being one unbroken thought; standfirst and lead open on `Det` and `Vår`.
  - `L1` — `pass` — `klä ut sig till ett beslut`, `mynna ut i ett svar` and V2 inversion after fronted adverbials throughout, with no translated cadence; both judges.
  - `L2` — `pass` — Swedish spelling, sentence-case headings, the `Text:` byline form and a lower-case continuation after the colon; no number, date or currency to invent; both judges.
  - `R1` — `pass` — `delivered.md` is byte-identical to `work/input.md`, the account says so accurately, the 83-word paragraph was not split, and no finding was made against the 44-character headline, the 41-word standfirst, the 37-character subheadings, the one-sentence or four-sentence paragraph, one section's paragraph count or the `Text:` byline form; both judges. None of the five rejections.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Judgements: [`../editorial-386/runs/column-clean/judgement-a.md`](../editorial-386/runs/column-clean/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/column-clean/judgement-b.md). No split on any criterion. Both judges treat the 83-word paragraph as a *should* the text had good reason to leave, which the frozen expectation names, and record that leaving it unreported is not a gap because it is neither a mandatory nor an irreparable finding.

## `column-flawed`

- **fixture** — `column-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reviewed text in the reply under `## Texten`, followed by one remaining finding, a list of the findings it calls addressed with the script's figures quoted back, and a `Borttagna påståenden` section naming four removals. Wall time 561 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — one small institutional object turned into a reflection, the angle held from the headline, and the reader left with something to do and a stated reason to doubt it; both judges.
  - `G2` — `pass` — the script turns the input's three failures (`standfirst` `absent`, `lead` `4 paragraphs`, `sections` `absent`) into `conforms: true` with `failures: []`: a 40-character headline, a 51-word standfirst in one paragraph, the bare-name byline `Nora Vik` left as the conventional Swedish form, a 28-word lead in one paragraph before the first H2, two sections with 29- and 31-character subheadings, and a call to action that grows out of the reflection; both judges.
  - `P1` — `pass` — the standfirst frames, the first section states the concrete gap, the second draws the reflection, and the conclusion stays at the strength the column earns. Judge A only: judge B's file gives no `P1` verdict.
  - `W1` — `pass` — the script reports `failures: []` and `norms: []`: headline 40 characters and 5 words, standfirst 51 words in one paragraph, subheadings 29 and 31 characters, no paragraph over 80 words, no heading below level two, and standfirst and lead opening on `Ett` and `Förra`; judge A passes, judge B fails on `sections_of_two_or_three_paragraphs: 0` of `sections: 2` read across the text; the evaluator's verdict is `pass`, because the anatomy requires a section and an ending and the fixture's body is some sixty words, so two one-paragraph sections are what conformity costs here rather than a loss the review could have avoided. None of the five rejections.
  - `L1` — `pass` — the new standfirst, subheadings and closing sentence are plain native Swedish, and the one mechanical repair moves the text toward idiom (`prova frågan om vad`); both judges.
  - `L2` — `pass` — the quotation keeps Swedish quotation marks with the stop inside, the new standfirst uses a spaced en dash as the Swedish tankstreck, headings are sentence case, and no date, number or currency was introduced; both judges.
  - `R1` — `pass` — all four removals are listed under `Borttagna påståenden` with the finding each answered, the old headline's claim is reported as its own finding, the new standfirst and ending are flagged as newly written text worth the author's reading, and the account's counted claims (`ledet mättes som fyra stycken`; `rubrik 40 tecken och 5 ord, ingress 51 ord, led ett stycke, två sektioner`) each match the script exactly; both judges. None of the five rejections.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — one, reported with the text: the lead's library scene no longer connects to the meeting template, because resolving the participation contradiction removed the sentence that bound them. The reply states that only the author knows whether the scene was a meeting about the template, and offers two routes rather than inventing a replacement memory.
- **defects filed** — `none`
- **notes** — Judgements: [`../editorial-386/runs/column-flawed/judgement-a.md`](../editorial-386/runs/column-flawed/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/column-flawed/judgement-b.md). One split, on `W1`: judge B reads the two one-paragraph sections as avoidable fragmentation — a subheading, one sentence of 16 words, then another subheading — and holds that one section carrying both paragraphs would have satisfied the anatomy and kept the reflection running. The evaluator's ruling is recorded above. Judge B also records the unreported mechanical insertion of `om` in `frågan om vad` as a silent change that moves no claim. **Judge B's file gives no verdict for `P1`**; the criterion is recorded on judge A's reading alone. Both judges record that the 20-character input headline drew no length finding and that the bare-name byline was left alone, which the frozen expectation requires.

## `opinion-clean`

- **fixture** — `opinion-clean` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reply states the resolved genre and language, that no technique applied and `Inga anmärkningar kvarstår.`, and then carries the text with one clause added to the lead's thesis sentence. There is no changelog, no finding and no statement that the text is unchanged. Wall time 393 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — the reader learns what is on the table, what the evidence is and why it does not reach the conclusion drawn from it, closing on the polemical `Ett antagande blir inte ett beslutsunderlag för att kalendern säger september.`; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []`: a 47-character headline, a 39-word standfirst in one paragraph, the byline `Text: Sanna Ek, Öppna beslut`, a lead in one paragraph before the first H2 (42 words in the input, 48 after the added clause), three sections with 40-, 33- and 39-character subheadings, an early position, a real administrative objection granted on its merits and the stance as the call to action with an identifiable actor; both judges.
  - `P1` — `pass` — `En bokning är en händelse, inte en invånare.` is stated before the distinction is leaned on, the transitions are real, and the text asks for a trial and a measurement rather than the abandonment its figures would not support; both judges.
  - `W1` — `pass` — the script reports `norms: []`: headline 47 characters and 6 words, standfirst 39 words, subheadings 40, 33 and 39 characters, longest paragraph 50 words, and across the whole text `paragraphs_of_two_or_three_sentences: 5` of `paragraphs: 7` with `sections_of_two_or_three_paragraphs: 2` of `sections: 3`; standfirst and lead open on `I` and `Kommunstyrelsen`; both judges, each recording the added clause's repetition of the standfirst's September as a qualitative loss rather than a counted failure.
  - `L1` — `pass` — `slippa dubbel administration`, `det som nu ligger på bordet` and `varken … eller` are native Swedish; both judges record the inserted relative `som` reading onto `föreningslokaler` rather than `bytet` as a blemish in one clause rather than a failure of the prose.
  - `L2` — `pass` — `den 8 april 2026` with a lower-case month, lower-case `september` throughout, digits for 96 and 24 against spelled-out small numbers, and no currency or converted figure; both judges.
  - `R1` — `fail` — the run made exactly one change, inserting `, som annars kan ske i september` into the lead's thesis sentence, and reported it neither as a finding nor as a repair: the whole account is `Inga anmärkningar kvarstår.` The script reports the input `conforms: true` with `failures: []` and `norms: []`, so there was nothing to repair, and the September the clause supplies is already in the standfirst one line above; both judges. None of the five rejections as the protocol words them — judge A says outright that the clause is no unsupported fact, the standfirst carrying it — this is `R1`'s own failure, a change outside any finding that the account does not report; this is [#383](https://github.com/Kntnt/skills/issues/383).
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — none reported. The reply states `Inga anmärkningar kvarstår.`, which is where the silent edit is hidden rather than declared.
- **defects filed** — [#383](https://github.com/Kntnt/skills/issues/383)
- **notes** — Judgements: [`../editorial-386/runs/opinion-clean/judgement-a.md`](../editorial-386/runs/opinion-clean/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/opinion-clean/judgement-b.md). No split on any criterion. Both judges record that every finding the frozen expectation rejects was avoided — nothing against the 47-character headline, the 39-word standfirst, the 33–40-character subheadings, the single-paragraph section, the one-sentence closing paragraph, the four-sentence paragraph or the `Text:` byline — and that the expectation did not foresee an edit made with no finding behind it at all. This is the only clean control of the four that did not come back byte-identical.

## `opinion-flawed`

- **fixture** — `opinion-flawed` from the corpus's *Redline controls* table
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reply states the resolved configuration, the spent one-round budget, that the re-review leaves no remaining findings and that the anatomy is machine-measured and meets every counted requirement, then carries the text and a `Borttagna påståenden` and `Ändrade påståenden` account. Wall time 631 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty.
- **criteria** —
  - `G1` — `pass` — the position stands in the lead, the support is the pilot's own figures and the report's own admissions, the objection is named rather than dismissed, and the actor is identifiable; both judges.
  - `G2` — `pass` — the script turns the input's one failure (`standfirst` `absent`) into `conforms: true` with `failures: []`: a 48-character headline, a 45-word standfirst in one paragraph built only from material already in the text, the byline `Sanna Ek, Öppna beslut` carried unchanged, a 12-word lead in one paragraph before the first H2, and two sections whose 54- and 46-character subheadings replace the bare labels `Bakgrund` and `Diskussion`; both judges, each recording that the closing sentence remains the last section's second paragraph rather than an ending of its own, which the script counts as no failure and the frozen expectation's own remedy — existing action and actor repairing the ending — is what the run did.
  - `P1` — `pass` — the chain from 24 of 120 bookings to the report's own limits to the demand for measurement is visible at every step, and the two leaps the input made are gone; both judges.
  - `W1` — `pass` — the script reports `norms: []`: headline 48 characters and 7 words, standfirst 45 words in one paragraph, lead one paragraph, subheadings 54 and 46 characters, longest paragraph 38 words, no section over three paragraphs; standfirst and lead open on `Ett` and `Kommunstyrelsen`; both judges read `paragraphs_of_two_or_three_sentences: 2` of `paragraphs: 5` across the whole text and record no reader loss, the paragraphs outside the band being the one-sentence lead, the one-sentence close and a 32-word four-sentence paragraph.
  - `L1` — `pass` — `Var femte bokning gjordes alltså per telefon.` is the Swedish fraction idiom and `Det är kommunstyrelsen som kan säga ja …` a natural cleft, with the new sentences in the same register as the preserved administrative vocabulary; both judges.
  - `L2` — `pass` — `den 8 april 2026` carried unchanged, `96`, `24` and `120` as unformatted integers, sentence-case headings, and the one new number, 120, the sum of the text's own 96 and 24, which the account states; both judges.
  - `R1` — `pass` — three removals and three changed claims, every one reported with the sentence it sat in and the reason, including the denominator correction from `20 procent av kommunens invånare` to `Var femte bokning`, the ending rebuilt from the act and actor already in the text, and the added standfirst with the derivation of 120 stated outright; the preserved sentences the account lists as standing verbatim do stand verbatim; both judges. None of the five rejections.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row and none was expected to be.
- **unresolved findings** — `none`; the reply states that the re-review after the correction round leaves none.
- **defects filed** — `none`
- **notes** — Judgements: [`../editorial-386/runs/opinion-flawed/judgement-a.md`](../editorial-386/runs/opinion-flawed/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/opinion-flawed/judgement-b.md). No split on any criterion. This is the one changed row in the wave whose account names the old headline's claim among its removals — `Att kommunledningen hatar människor. Låg i den gamla rubriken` — which is what makes the omissions in `article-flawed`, `case-study-flawed` and `case-study-sv` Redline inconsistent rather than systematic, and is cited to [#383](https://github.com/Kntnt/skills/issues/383) as such. Both judges record that no finding was made against a counted requirement the input met: the input headline measured 31 characters and the subheadings 8 and 10, and the objections raised to all three were to claim and angle, not to length.

## `column-sv`

- **fixture** — `column-sv`, the pipeline row: the draft the `column-sv` Write run delivered, with its `kntnt` metadata and nothing else, given to a fresh session that never saw the source
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reply states that genre, language and `technique: none` all came from the document's own `kntnt` block, names the one finding and its repair, states that nothing else in substance changed, and carries the text with its frontmatter in a fenced block; it closes `Inga fynd återstår.` Wall time 580 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty. `anatomy-input.json` here is byte-identical to the `column-sv` Write row's `anatomy-delivered.json`, which is what makes the pipeline's hand-off checkable.
- **criteria** —
  - `G1` — `pass` — the angle is single and held, the reflection is marked as reflection in the text itself, and the close invites the reader without a campaign or a commercial turn; both judges.
  - `G2` — `pass` — the script reports `conforms: true` with `failures: []`: a 41-character headline, a 47-word standfirst in one paragraph, the byline `Av Nora Vik`, a 42-word lead in one paragraph before the first H2, and three sections with 41-, 45- and 53-character subheadings, the third now stating the section's angle instead of repeating the sentence under it; both judges.
  - `P1` — `pass` — the argument moves in one pass with real transitions, and the conclusions stay inside the visible support, twice said so by the text itself; both judges.
  - `W1` — `pass` — the script reports `norms: []`: longest paragraph 56 words, no section over three paragraphs, no heading below level two, headline 41 characters and 6 words, and across the whole text `paragraphs_of_two_or_three_sentences: 5` of `paragraphs: 7` with `sections_of_two_or_three_paragraphs: 2` of `sections: 3`; standfirst and lead open on `Vad` and `Jag`; both judges record the repaired subheading as the reader gain, a skimmer now leaving with the proposal rather than the same hesitation twice.
  - `L1` — `pass` — native Swedish throughout, and the introduced subheading is an idiomatic Swedish imperative in the surrounding register; both judges.
  - `L2` — `pass` — the one mechanical change improved the locale: the standfirst's parenthetical dash is now the spaced en dash Swedish sets as the tankstreck, where the input had an em dash; `kolleger` was preserved rather than normalised, and no figure, date or currency appears; both judges.
  - `R1` — `pass` — two differences and no removal: the dash, and the third subheading, replaced because it repeated its first sentence almost word for word. The account names the finding, the defect, the reader effect and the fact that the replacement is drawn from the section itself, and its claim that no claim's scope, certainty, source, chronology, causality or meaning moved holds against the diff; both judges. None of the five rejections. Both record one thinness: the dash change is covered only by the class statement `Därefter gjordes en avslutande mekanisk korrekturomgång` and is not itemised.
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row; the reply states that `technique: none` came from the document's own map.
- **unresolved findings** — `none`; the reply states `Inga fynd återstår.`, which the returned text bears out.
- **defects filed** — `none`
- **notes** — Judgements: [`../editorial-386/runs/column-sv/redline/judgement-a.md`](../editorial-386/runs/column-sv/redline/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/column-sv/redline/judgement-b.md). No split on any criterion. The finding this run repaired is the one the `column-sv` Write row shipped and both Write judges failed `G2` on, which is [#390](https://github.com/Kntnt/skills/issues/390): the review caught on its first pass what the writing pass and both source checkers missed. Both judges answer the briefs' separate source question and find no source loss — the pipeline's source requires an ending that keeps the uncertainty, and the new subheading carries the hope and the doubt where the old one carried only the doubt.

## `case-study-sv`

- **fixture** — `case-study-sv`, the pipeline row: the draft the `case-study-sv` Write run delivered, with its `kntnt` metadata and nothing else, given to a fresh session that never saw the source
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — `changed`: the reply states the resolved configuration from the document's own `kntnt` block and the spent one-round budget, carries the text in a fenced block, and follows it with `Fynd som återstår`, holding one finding marked `Olöst`, and a `Påståenden` section. Wall time 814 seconds.
- **side effects** — `none` from the Skill: the inventories differ only by the evaluator's own files — `response.md`, `delivered.md`, the two `anatomy-*.json`, `run-facts.txt` and `inventory-after.txt`. `work/input.md` is unchanged and `work/scratch/` is empty. `anatomy-input.json` here is byte-identical to the `case-study-sv` Write row's `anatomy-delivered.json`.
- **criteria** —
  - `G1` — `pass` — the situation, the action, the results with their limits, the customer's own appraisal and the publisher stance all survive intact, and the reader still learns what the trial cost in preparation and what the numbers do not establish; both judges.
  - `G2` — `fail` — the anatomy requires a headline understood on its own without claiming more than the text claims, and the returned headline `Gemensam logg hjälpte Elm Quay men kostade förberedelsetid`, 58 characters and 8 words, asserts in the text's own voice an effect the body withholds two sections later in `anteckningen tillskriver uttryckligen inte skillnaden programvaran`; the only support is Maya Lind's quoted `Att ha en samlad bild av anmälningarna hjälper oss`; both judges. Of the five rejections this is an unsupported fact: a claim the supplied text does not carry, made by the round itself and shipped.
  - `P1` — `pass` — the body's reasoning is intact, the one figure that could carry an inference is fenced on both sides, and the disproportionate conclusion is the headline, scored at `G2`; both judges.
  - `W1` — `pass` — the script reports `conforms: true`, `failures: []` and `norms: []`: headline 58 characters and 8 words, standfirst 51 words in one paragraph, lead one paragraph, subheadings 52, 32 and 29 characters, longest paragraph 42 words, every section with three paragraphs, and across the whole text `paragraphs_of_two_or_three_sentences: 10` of `paragraphs: 11` with `sections_of_two_or_three_paragraphs: 3` of `sections: 3`; standfirst and lead open on `Hösten` and `Telefonanmälningar`; both judges.
  - `L1` — `pass` — the Swedish reads as written Swedish; both judges record `Lind gav ingen generell rekommendation av Svale` as a qualitative concern, the repair of one ambiguity opening a smaller one, since `rekommendation av Svale` can be read as a recommendation made by Svale.
  - `L2` — `pass` — lower-case months in `4 december 2025`, `Hösten 2025` and `I september 2025`, spaced speech dashes for the quotations and an en dash in the standfirst, and no date invented or currency converted; both judges.
  - `R1` — `fail` — five differences, two of them reported well and three not at all: the headline rewrite is reported at length with the round named as its author, and the `Lind` sentence's moved scope is reported with the residual reading flagged, but the standfirst's added exclusion clause, the first subheading's replacement and `testade` → `undersökte` appear nowhere in the account, whose `Påståenden` section states that exactly one claim moved in scope; both judges, who also hold that reverting the headline needed no material the run lacked, so a self-inflicted overclaim was shipped on a spent budget. Of the five rejections the nearest is the unsupported fact: judge B writes that the run `delivers a text carrying an unsupported claim that it could have withdrawn`, and judge A that the headline states in the publication's voice what the text carries only as Lind's attributed judgement; the unreported changes are [#383](https://github.com/Kntnt/skills/issues/383).
  - `O1` — `pass` — read from the inventories: the diff adds only the evaluator's own files, `work/input.md` is unchanged, and `work/scratch/` is empty.
  - `T1` — `skipped` — answerable only from a Harness trace ([#388](https://github.com/Kntnt/skills/issues/388)).
  - `R2` — `skipped` — same reason.
  - `T2` — `skipped` — no technique was selected on this row; the reply states that `technique: none` came from the document's own map.
- **unresolved findings** — one, reported with the text and marked `Olöst`: the rewritten headline claims more than the text claims. The reply states that the finding did not exist in the input, that the round's own repair created it, what the only support is, and that the loop stopped because `budgeten var förbrukad` and a further round would only have repaired the previous round's work; it hands the user two routes.
- **defects filed** — [#389](https://github.com/Kntnt/skills/issues/389), [#383](https://github.com/Kntnt/skills/issues/383)
- **notes** — Judgements: [`../editorial-386/runs/case-study-sv/redline/judgement-a.md`](../editorial-386/runs/case-study-sv/redline/judgement-a.md) and [`judgement-b.md`](../editorial-386/runs/case-study-sv/redline/judgement-b.md). No split on any criterion. Both judges call the detection and reporting of the headline exemplary and both fail `R1` anyway: honest reporting does not make the delivered text sound, and the account of what was resolved is incomplete in three places. Both answer the briefs' separate source question and find the same loss, which the Skill could not have known: the pipeline's source forbids any claim that the software caused the shorter assignment time, and the new headline asserts that benefit in the publisher's own voice. Both also record a milder drift, the source asking that the customer remain the acting party where the new first subheading gives the supplier the first subject position.

## What this evaluation exposed and did not settle

Three of the four clean controls came back byte-identical with an account that says so, and no finding was raised against a limit any of them meets. The fourth, `opinion-clean`, came back with a clause added to its thesis sentence under an account reading `Inga anmärkningar kvarstår.` — a clean passage changed outside any finding and omitted from the account, which is [#383](https://github.com/Kntnt/skills/issues/383) reaching a control for the first time. The same issue takes the unreported headline, standfirst and subheading rewrites in `article-flawed`, `case-study-flawed` and `case-study-sv`; `opinion-flawed` in the same wave did list its old headline's claim, so the omission is inconsistent rather than systematic.

The new thing this wave found is what a correction round does to its own work. `case-study-sv` replaced a conforming headline with one claiming an effect its body refuses, re-reviewed it, reported the finding in full and shipped it on a spent budget; `article-flawed` created a subheading that repeats the sentence under it and did the same. Both are filed as [#389](https://github.com/Kntnt/skills/issues/389). Neither run lacked the material to undo its own repair.

Nothing here establishes whether the scoped contract loading happened or whether Redline's one closing installed Proofread pass ran. `T1` and `R2` are `skipped` on all ten entries: both are answerable only from a Harness trace, and a Claude Code session cannot read the transcript of a subagent it started. The trace-bearing Claude-family harness is [#388](https://github.com/Kntnt/skills/issues/388).
