# redline — claude — 2026-09-22 — #363

- **record** — `redline-claude-2026-09-22-363`
- **date** — `2026-09-22`
- **ticket** — `#363`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for every run, for every subagent a run started, and for every judge
- **harness** — Claude Code 2.1.278
- **corpus commit** — `8a37e57e`, the commit the three staged installs were taken from

## Run conditions

Source-blind `/redline` runs over seven frozen inputs, in **three arms of one product** — `b`, the collection unchanged at `8a37e57e`; `c`, that tree plus the first candidate wording of #363; `r`, that tree plus the revised wording — together with the paired replays the frozen matrix requires of every draft the `Write` rows delivered. The matrix was frozen before the first run in [`../editorial-363/plan.md`](../editorial-363/plan.md), the results are in [`../editorial-363/results.md`](../editorial-363/results.md), and every artefact is under [`../editorial-363/runs/`](../editorial-363/runs/). The companion record is [`write-claude-2026-09-22-363.md`](write-claude-2026-09-22-363.md), whose run conditions — the two harnesses, the evaluator's four instructions, the inventories, the voided subagent attempts, the blind judging arrangement, and the `T1`/`R2` skip — hold here unchanged and are not repeated.

**Which seat each `r`-arm row used.** Eleven of this record's eighteen `r`-arm rows ran as fresh top-level Claude Code sessions: `en-positive-r2`, `en-us-r1-r1`, `en-us-r1-r2`, `metonymy-sv-r1`, `metonymy-sv-r2`, `rhythm-en_GB-r1`, `rhythm-en_GB-r2` and the four paired replays. The other seven — `sv-control-r1` and `r2`, `sv-artefact-r1` and `r2`, `ellipsis-sv-r1` and `r2`, and `en-positive-r1` — were dispatched as subagents, as the `b` and `c` arms were: their `started.txt` markers run from `17:30:54Z` to `17:31:37Z`, four and a half hours before the session wave, in the seven-second steps the two earlier waves carry. For those seven, whether Redline's correction round got the fresh seat its step 7 requires is the open question [#394](https://github.com/Kntnt/skills/issues/394) records, exactly as it is for the attempts under [`../editorial-363/voided/`](../editorial-363/voided/). An earlier version of this record described the whole `r` arm as sessions, and that was not true of those seven.

**How the mechanical pass's two files are named.** The frozen turn template asks for them as `mechanical-pass-input.md` and `mechanical-pass-output.md` in `evidence/`. Twenty-nine of the fifty runs used those names; twelve used `proofread-input.md` and `proofread-output.md`, and nine used `proofread-private-input.md` and `proofread-private-output.md`. Both files are present and complete in every run, and in all fifty the delivered artefact is byte-identical to the result. The naming is a deviation from an evaluator instruction rather than from the Skill's contract, and the artefacts are left under the names the runs gave them.

**Entries are one per row, with every arm and every run inside**, because seven inputs replayed up to five times each plus the paired replays would otherwise be sixty near-identical sections. No run is left out.

**Every run's working directory held `input.md` and nothing else**, and the invocation carries no `--genre` and no `--language`: genre, technique and language are resolved from each text's own `kntnt` map, which is what the recorded replays of these inputs did and what the paired replays test. The mandatory Swedish control has no such map and resolves from the text.

**The mandatory Swedish control is no longer byte-identical to the corpus control.** The plan and the ticket's addendum both say it is; that was true at `6e531f5`, and `28f7e66b` has since revised `controls/case-study-clean.md` for the article anatomy. Both still carry the sentence at issue. Neither file was edited.

## `sv-control` — `editorial-329/followup/runs/final-idiom-control/redline/supplied-input.md`

- **fixture** — the mandatory unchanged Swedish control; `b` once, `c` twice, `r` twice
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — every run delivered a changed artefact in the reply with an account of what it changed and what it left. `r/sv-control-r1` has no `finished.txt`.
- **side effects** — `none` from the Skill. Each run directory gained `response.md`, `delivered.md`, `started.txt`, `evidence/` and — except in the one run named above — `finished.txt`, all on the evaluator's instruction. `work/input.md` carries the same `sha256` before and after, and it is the same hash in all five runs. The staged installs are unchanged.
- **criteria** —
  - `R1` — `fail` on four of five and `pass` on one, the judges splitting on two of the four. `r/sv-control-r2` is the row both judges pass; `b/sv-control-r1` and `r/sv-control-r1` fail on judge B alone, and both `c` runs fail on both judges. Every failure is about headings, bridges, a re-cast standfirst or an account that says nothing else moved when something did — none about quoted speech.
  - **quotation** (the row's purpose) — the sentence *Den tiden skulle jag avsätta innan nästa hus börjar* came back **word for word in all five runs, in all three arms**, and no run's reported findings name it. Both judges, in all five, record that a Swedish reader takes the passage on one pass. Judge A wrote, in all five, that *"innan nästa hus börjar" is the ordinary Swedish shorthand for "innan arbetet i nästa hus börjar" — a metonymy the language uses of itself*, and that nothing has to be supplied from outside.
  - `G2`, `L1` — `pass` on the delivered artefacts except where the `R1` failures above touch a heading.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — every run carried findings forward, most of them defects its own correction round created, which is what stopped the loop.
- **defects filed** — recorded against [#377](https://github.com/Kntnt/skills/issues/377), [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389) and [#390](https://github.com/Kntnt/skills/issues/390); two runs moved the trial note's refusal to attribute the difference from *programvaran* to *loggen*, which is #377's shape exactly.
- **notes** — This is the row the ticket was filed on, and it behaves identically in all three arms. The historical GPT-family `L1` finding against this fixture stands as history and is not retested; what is established here is that **this** family's blind judges do not find it.

## `sv-artefact` — `editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/draft.md`

- **fixture** — the earlier Swedish artefact; `b` once, `c` twice, `r` twice
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — every run delivered a changed artefact.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — `fail` on two of five, `pass` on three, with one split. The failures are unreported claim changes and a false completeness statement.
  - **quotation** — *Jag skulle avsätta den tiden innan nästa byggnad kommer i gång* came back word for word in all five runs, unnamed by any reported finding, and both judges in all five record all three quoted passages as taken on one pass.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — carried forward in every run.
- **defects filed** — against #377, #383, #389, #390.
- **notes** — `c/sv-artefact-r1` is a clear #383: a bridge claim removed with no finding naming it, under a reply stating that one claim was removed and nothing's certainty moved.

## `en-positive` — `editorial-329/followup/runs/third-candidate/case-study-en_US-r2/draft.md`

- **fixture** — the exact old English positive control; `b` once, `c` twice, `r` twice
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — every run delivered a changed artefact.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — mixed, and every failure is a heading or an unreported change.
  - **quotation** — `pass` in every run of every arm: *I would set that time aside before the next building starts* came back unchanged, and both judges record every quoted passage as taken on one pass in English. **No run in any arm expanded it.**
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — carried forward in every run.
- **defects filed** — against #383, #389, #390.
- **notes** — The English preservation failure this ticket inherits from the GPT family did not reproduce here, in the unchanged product or in either candidate.

## `en-us-r1` — `editorial-329/followup/runs/account-candidate/case-study-en_US-r1/redline/supplied-input.md`

- **fixture** — the newer US r1 text; `b` once, `c` twice, `r` twice
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — every run delivered a changed artefact.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — mixed; `c/en-us-r1-r1` and `c/en-us-r1-r2` fail on judge B for a standfirst that has Lind judging preparation time *was too short* and for unreported terminology changes.
  - **quotation** — `pass` in every run of every arm on what the criterion asks: the sentence came back unchanged in all five. The judging is split, and an earlier version of this record said it was not. Judge B takes the passage on one pass in all five; judge A does so in the three `b`- and `c`-arm runs and in both `r`-arm runs reads *the second, no — the reader stops at "before the next building starts"*. In `r/en-us-r1-r1` the run itself reports that obstacle among its unresolved findings and judge A records the report as exact; in `r/en-us-r1-r2` it does not, and judge A records that too.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — carried forward in every run.
- **defects filed** — against #377, #383, #389, #390.
- **notes** — Together with `en-positive`, this closes the English half: the duty this ticket says failed is discharged by the product as it stands.

## `metonymy-sv`, `rhythm-en_GB`, `ellipsis-sv` — the three new contrast fixtures

- **fixture** — [`../editorial-363/fixtures/`](../editorial-363/fixtures/), frozen with their own criteria before any product change; each run once in `b` and twice in `c` and in `r`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — every run delivered a changed artefact.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `C-metonymy` — `pass` in all three arms. *Vi ville ha rutinen på plats innan terminen drog i gång* and *expeditionen märkte skillnaden redan första veckan* come back unchanged in every run, and no run paraphrased either figure.
  - `C-rhythm` — `pass` in all three arms. *We wanted the rotas settled before the winter* and *the depot stopped ringing round at six in the morning* come back unchanged in every run; both judges take the ellipsis *They were, just about* on one pass.
  - `C-ellipsis` — `fail`, identically in all three arms. *Sedan gick lagret över* comes back untouched with no reported finding against it, which the fixture states is a miss. The row has five runs — one in `b`, two in `c`, two in `r`, and `r/ellipsis-sv-r1` has no `finished.txt` — and in all ten judgements of them both judges read the passage as one-pass Swedish. `b/ellipsis-sv-r1` does report an unresolved finding against a different part of that quotation, naming *pärmar*; the fixture asks for one against `gick lagret över`, so the row still fails. **The fixture and the judges disagree**; the fixture was frozen first and is not edited, and what the disagreement rules out is using this row to separate the arms.
  - `R1` — mixed, on headings and accounts as elsewhere.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — carried forward in every run.
- **defects filed** — against #383, #389, #390. `r/ellipsis-sv-r1` is the sharpest #383 in the wave: three edits, none reported, under an account asserting that no claim was removed, weakened or moved.
- **notes** — The two positives did what they were built to do: they confirm that neither wording taught the product to expand an ordinary figure. The negative did not, and that is the more useful result.

## The paired source-blind replays

- **fixture** — every draft a `Write` row delivered, replayed whole as `input.md` on its own arm's install, in a fresh seat that had seen nothing of the Write run. This is the body's *verkliga kandidat-Write→färsk-källblind-Redline-anrop*.
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — all fifteen are complete: four in the `b` arm, seven in `c` and four in `r`, each delivering a changed artefact, each timed. **This row was not run at all by the two earlier sessions**, and completing it is most of what this session added to the matrix.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - **quotation** — `pass` in all fifteen: the Swedish and English renderings each Write row produced came back unchanged. The baseline arm's replay of its own Swedish draft returns *innan nästa hus börjar* untouched, which is the pipeline reproducing the ticket's Swedish case end to end and leaving it alone. Both judges take the rendering on one pass in twelve of the fifteen; in `b/case-study-en_GB-r1-paired`, `b/case-study-en_US-r1-paired` and `c/case-study-en_US-r1-paired` judge A stops at the English *before the next building starts* while judge B does not, and in each of those three the run's own reply leaves that obstacle unreported, which judge A says in as many words.
  - `R1` — recorded per replay in the run tree.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — recorded per replay.
- **defects filed** — against #377, #383, #389, #390 where the judgements name them.
- **notes** — No replay is incomplete; an earlier version of this record was written while some were still running and warned about ones that might be. All fifteen delivered, and all thirty judgements are beside them in the run tree.

## Outcome

The wording this evaluation was built to measure **is not shipped**; every file it touched is byte-identical to `main` at `8a37e57e`. Across fifty source-blind runs in three arms — thirty-five over the seven frozen inputs and fifteen paired replays — not one expanded a working quotation and not one repaired a Swedish one. Of the hundred judgements those runs carry, ninety-five read every quoted passage as taken on one pass in its own language; the five that do not are all judge A on the English *before the next building starts*, and they are listed under `en-us-r1` and the paired replays above. [ADR-0212](../../adr/0212-a-quotation-is-read-in-the-language-it-is-written-in.md) records the decision; the residual is filed as its own ticket.
