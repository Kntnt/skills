# Results for #386

Twelve runs made on 2026-09-21 against the method [`plan.md`](plan.md) froze before the first one. Artefacts are beside this file, one directory per row. The records are [`../../records/write-claude-2026-09-21-386.md`](../../records/write-claude-2026-09-21-386.md) and [`../../records/redline-claude-2026-09-21-386.md`](../../records/redline-claude-2026-09-21-386.md).

## What the evaluation found

- Twelve invocations and twenty-four judgements, every run and every judge a fresh `claude-opus-5` subagent at high deliberation. Nine rows carry every criterion; three do not.
- Three of the four clean controls are the cleanest result here: `article-clean`, `case-study-clean` and `column-clean` came back byte-identical with an account that says so, and no finding was raised against a limit the text met.
- The fourth clean control is the worst. `opinion-clean` came back with a clause added to its thesis sentence, under an account that reads in full `Inga anmärkningar kvarstår.` Both judges fail `R1`. That is [#383](https://github.com/Kntnt/skills/issues/383), now on a control.
- Redline's own repairs make the defects that ship. `article-flawed` delivers a subheading that repeats the sentence under it, and `case-study-sv` Redline delivers a headline claiming an effect its own body refuses; the round created both, reported both, and withdrew neither. Filed as [#389](https://github.com/Kntnt/skills/issues/389).
- Redline's accounts under-report what they changed. Three flawed controls and one pipeline row rewrote a headline, a standfirst or a subheading without naming it, and two of the four state their list of removals as complete. That is #383 again.
- Write is the quieter side: both rows delivered, both drafts measured conforming, one criterion failed — a `column-sv` subheading repeating its own first sentence, which neither checker nor account caught ([#390](https://github.com/Kntnt/skills/issues/390)).
- Both Write rows started unbounded background waits for a checker report file the harness would not let the checker write ([#391](https://github.com/Kntnt/skills/issues/391)). None was left once the last run had ended, but a file inventory cannot see such a process either way.
- Nothing was written outside each run's own directory. The staged install is byte-identical before and after the wave, every `work/input.md` is unchanged, and every `work/scratch/` is empty.
- **Contract loading and Redline's closing Proofread pass stayed unobserved in this family.** `T1` and `R2` are `skipped` on every entry: both are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started. Nothing here says the scoped loading happened, and nothing here says the one closing Proofread pass ran. The trace-bearing harness is [#388](https://github.com/Kntnt/skills/issues/388).
- The measuring script was visibly in use. Every run that repaired an anatomy failure quotes its figures back — `column-flawed` reports `rubrik 40 tecken och 5 ord, ingress 51 ord, led ett stycke, två sektioner`, `case-study-flawed` quotes `byline: absent` — and the evaluator re-measured every input and every delivered text from its own copy of the script at `9a29bad3`.
- Ten inputs were measured: six at exit 0, four at exit 1. Twelve delivered texts were measured: ten at exit 0, two at exit 1.
- The two that stay at exit 1 are `article-flawed` and `case-study-flawed`, both on one failure and the same one: `byline` `absent`, because nobody names an author. Both runs report it missing and leave it unfilled rather than invent a name, which is what the criterion asks.

## The twelve runs

`A / B` marks a split; the verdict recorded is the one before the bracket, and the dissent is in the entry's `notes`. `—` marks a criterion that does not apply to that side. `T1`, `R2` and `T2` are `skipped` on all twelve and are not repeated here.

| Run | Side | Outcome | Script, input | Script, delivered | F1 | G1 | G2 | P1 | W1 | L1 | L2 | R1 | O1 | Wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `article-clean` | Redline control | no change | exit 0 | exit 0 | — | pass | pass | pass | pass | pass | pass | pass | pass | 280 s |
| `article-flawed` | Redline control | changed | exit 1 | exit 1 | — | pass | **fail** (A pass / B fail) | pass | pass | pass | pass | **fail** (A fail / B pass) | pass | 645 s |
| `case-study-clean` | Redline control | no change | exit 0 | exit 0 | — | pass | pass | pass | pass | pass | pass | pass | pass | 235 s |
| `case-study-flawed` | Redline control | changed | exit 1 | exit 1 | — | pass | **fail** (A fail / B pass) | pass | **fail** (A fail / B pass) | pass | pass | **fail** | pass | 838 s |
| `column-clean` | Redline control | no change | exit 0 | exit 0 | — | pass | pass | pass | pass | pass | pass | pass | pass | 208 s |
| `column-flawed` | Redline control | changed | exit 1 | exit 0 | — | pass | pass | pass (A only) | pass (A pass / B fail) | pass | pass | pass | pass | 561 s |
| `opinion-clean` | Redline control | changed | exit 0 | exit 0 | — | pass | pass | pass | pass | pass | pass | **fail** | pass | 393 s |
| `opinion-flawed` | Redline control | changed | exit 1 | exit 0 | — | pass | pass | pass | pass | pass | pass | pass | pass | 631 s |
| `column-sv` | Write | delivered | — | exit 0 | pass | pass | **fail** | pass | pass | pass | pass | — | pass | 1777 s |
| `column-sv` | Redline | changed | exit 0 | exit 0 | — | pass | pass | pass | pass | pass | pass | pass | pass | 580 s |
| `case-study-sv` | Write | delivered | — | exit 0 | pass | pass | pass | pass | pass | pass | pass | — | pass | 1355 s |
| `case-study-sv` | Redline | changed | exit 0 | exit 0 | — | pass | **fail** | pass | pass | pass | pass | **fail** | pass | 814 s |

Eighty criterion lines are judged on the Redline side, seventy-two `pass` and eight `fail`; sixteen on the Write side, fifteen `pass` and one `fail`. Thirty-six lines are `skipped` — `T1`, `R2` and `T2` on all twelve entries of the two records taken together.

The wave ran from `2026-09-21T14:48:30Z` to `2026-09-21T15:28:39Z`, 2409 seconds of wall time for 8317 seconds of run time.

## Every headline and subheading the twelve runs delivered

The marks are the judges' own, on the returned text. Counts are the script's, from each row's `anatomy-delivered.json`. **No heading in any of the twelve uses a colon for a verb and none is a question**, so those two marks appear nowhere below.

| Run | Heading | Chars | Words | Marks |
| --- | --- | --- | --- | --- |
| `article-clean` | `# Mätförsöket i Björkskolan visar när, inte varför` | 48 | 7 | statement |
| `article-clean` | `## En gräns för det lokala försöket` | 32 | 6 | label |
| `article-clean` | `## Nästa försök behöver mer än givare` | 34 | 6 | statement |
| `article-flawed` | `# Mätförsöket i Björkskolan saknar operativ temperatur` | 52 | 6 | statement |
| `article-flawed` | `## Placeringen redovisas, men inte dess effekt` | 43 | 6 | statement; **echo** on judge B only (its second half restates the one sentence under it) |
| `article-flawed` | `## Underlaget har flera luckor` | 27 | 4 | statement |
| `article-flawed` | `## Elin Rask vill se användningstiderna först` | 42 | 6 | statement, **echo** (both judges; the name and *användningstider* stand in the sentence directly under it) |
| `case-study-clean` | `# Elm Quay samlade reparationsärendena` | 36 | 4 | statement |
| `case-study-clean` | `## Gruppen enades om kategorierna först` | 36 | 5 | statement |
| `case-study-clean` | `## Två perioder med olika arbetsbelastning` | 39 | 5 | label |
| `case-study-clean` | `## Kunden vill ge förberedelserna mer tid` | 38 | 6 | statement |
| `case-study-flawed` | `# I Elm Quays försök tog tilldelningen två arbetsdagar` | 52 | 8 | statement |
| `case-study-flawed` | `## Arbetsledaren efterlyser en längre upptakt` | 42 | 5 | statement |
| `case-study-flawed` | `## Siffrorna säger inte varför tilldelningen gick fortare` | 54 | 7 | statement |
| `column-clean` | `# Mötesmallen har en ruta för allt utom varför` | 44 | 8 | statement |
| `column-clean` | `## Det är inte bara besluten jag vill åt` | 37 | 8 | statement |
| `column-clean` | `## Ännu en ruta, och ändå vill jag prova` | 37 | 8 | statement |
| `column-flawed` | `# Mötesmallen saknar plats för förståelsen` | 40 | 5 | statement |
| `column-flawed` | `## Mallen frågar efter klockslag` | 29 | 4 | statement |
| `column-flawed` | `## Prova frågan innan mallen växer` | 31 | 5 | statement |
| `opinion-clean` | `# Avskaffa inte telefonbokningen på ett antagande` | 47 | 6 | statement |
| `opinion-clean` | `## Bokningar är inte samma sak som personer` | 40 | 7 | statement |
| `opinion-clean` | `## Mät också arbetet med två kanaler` | 33 | 6 | statement |
| `opinion-clean` | `## Besluta om försöket, inte om antagandet` | 39 | 6 | statement |
| `opinion-flawed` | `# Telefonbokningen bör finnas kvar ett halvår till` | 48 | 7 | statement |
| `opinion-flawed` | `## Siffrorna säger inte hur många personer som står bakom` | 54 | 9 | statement |
| `opinion-flawed` | `## Kostnaden för två bokningsvägar är inte räknad` | 46 | 7 | statement |
| `column-sv` Write | `# Mötesmallen saknar en ruta för förståelse` | 41 | 6 | statement, **echo** (both judges; the standfirst's second clause restates the proposition, and both judges hold the overlap forced by the standfirst's duty to stand alone) |
| `column-sv` Write | `## Jag värderar det mallen inte frågar efter` | 41 | 7 | statement |
| `column-sv` Write | `## Ett samtal utan beslut kan också ha ett syfte` | 45 | 9 | statement |
| `column-sv` Write | `## Jag vet inte om rutan skulle hjälpa` | 35 | 7 | statement, **echo** (both judges; the sentence under it is `Jag vet inte om ytterligare en ruta gör möten bättre.`) — the `G2` failure, #390 |
| `column-sv` Redline | `# Mötesmallen saknar en ruta för förståelse` | 41 | 6 | statement; neither judge marked echo here, both reading the shared nouns as the subject rather than the phrasing |
| `column-sv` Redline | `## Jag värderar det mallen inte frågar efter` | 41 | 7 | statement |
| `column-sv` Redline | `## Ett samtal utan beslut kan också ha ett syfte` | 45 | 9 | statement |
| `column-sv` Redline | `## Testa en fråga bredvid tiden, utan att släppa tvivlet` | 53 | 9 | statement — the repaired heading, no echo on either judgement |
| `case-study-sv` Write | `# Elm Quay testade gemensam logg i två hus` | 40 | 8 | statement, **echo** (both judges; judge B marks it partial, the standfirst adding the season and the duration) |
| `case-study-sv` Write | `## Så kom systemet på plats i de två husen` | 39 | 9 | statement on judge A, **label** on judge B |
| `case-study-sv` Write | `## Siffrorna säger inget om orsaken` | 32 | 5 | statement |
| `case-study-sv` Write | `## Beslutet om fler hus återstår` | 29 | 5 | statement |
| `case-study-sv` Redline | `# Gemensam logg hjälpte Elm Quay men kostade förberedelsetid` | 58 | 8 | statement, **claims beyond the text** (both judges; the body says `anteckningen tillskriver uttryckligen inte skillnaden programvaran`, and the only support is Maya Lind's quoted `Att ha en samlad bild av anmälningarna hjälper oss`) — the `G2` failure, #389 |
| `case-study-sv` Redline | `## Svale satte upp loggen – laget stod för kategorierna` | 52 | 8 | statement |
| `case-study-sv` Redline | `## Siffrorna säger inget om orsaken` | 32 | 5 | statement |
| `case-study-sv` Redline | `## Beslutet om fler hus återstår` | 29 | 5 | statement |

Forty-three headings in all. Every one of the twelve delivered texts sits inside the 20–70-character headline requirement and the 70-character subheading requirement on the script's figures; every headline is inside the eight-word and 60-character norms as well. The anatomy's counted requirements are therefore not where these texts fail. What the marks show instead is that four of the twelve carry an echo, and three of those four echoes were written by the run itself: the `article-flawed` and `case-study-sv` Redline headings, and the `column-sv` Write subheading.

## Method

Nine things about how this wave was made, declared here rather than inferred from the artefacts.

1. **One rolling wave, not the two the plan pictured.** The two Write rows and five controls were dispatched first, the other three controls as slots freed, and each pipeline Redline as soon as its Write row delivered. The scope-3 and scope-4 inventories were therefore taken once, before the first run and after the last, and are `wave-1-before.txt`, `wave-1-after.txt`, `wave-1-before-repo.txt` and `wave-1-after-repo.txt` beside this file. A change under scope 2 or 3 during the wave could not have been attributed to a single run; none occurred.
2. **Judges of finished rows wrote while later runs were still in flight.** Each `judgement-a.md` and `judgement-b.md` therefore appears in the wave-level diff, and each is attributable by its name and its directory rather than by its timing.
3. **Each judge was pointed at a byte copy of its frozen brief by path**, in the evaluator's own directory in the staging area, rather than having the text pasted into its turn. It then received the two lines the plan describes, plus one evaluator sentence: if the judgement file write is refused, reply with the whole judgement. No judge's write was refused.
4. **No run's `response.md` write was refused**, so every `response.md` in this tree is the run's own, written on the evaluator's instruction. It is a declared evaluator addition and not a Skill side effect, as is `evidence/` on the two Write rows.
5. **`delivered.md` was extracted from `response.md` mechanically by the evaluator**, between the markers each reply used. For the three unchanged clean controls it is a byte copy of `work/input.md`.
6. **One corrected helper run.** The evaluator's first helper recorded a wrong exit code for the measuring script in `run-facts.txt`. It was corrected and rerun before any judge was dispatched, and the JSON files were never affected.
7. **The repository working copy was in use by another session throughout.** Its `HEAD` moved from `76ddacc1` to `1a81bc56` by that session's own commits, and `git status --porcelain --untracked-files=all` was clean at both ends. Nothing staged for a run lives there: the Skills, the measuring script and the fixtures were all taken from `9a29bad3` with `git archive` and `git show`.
8. **Three finished run agents were stopped by the evaluator** after their replies had arrived and been saved, because stale wait timers kept re-waking them. Nothing was written after the saved reply; the before-and-after checksums agree.
9. **What the wave-level diff shows outside the run tree** is only the evaluator's own helper files — the brief copies, `extract.py`, `extract2.py` and `post.sh` — in the evaluator's directory in the staging area. The staged install appears nowhere in that diff, so it is byte-identical before and after, and the only line the diff removes is the `wave-1-before.txt` listing's own hash.

`O1` and the `side effects` field in both records were read by the evaluator from each run's `inventory-before.txt` and `inventory-after.txt`, never from a run's report of itself. In all twelve the diff adds only the evaluator's own files — `response.md`, `delivered.md`, `anatomy-*.json`, `run-facts.txt`, `inventory-after.txt`, and on the Write rows `evidence/` — `work/input.md` or `work/source.md` is unchanged, and `work/scratch/` is empty after every run.

## Defects

- **[#389](https://github.com/Kntnt/skills/issues/389) — Redline keeps a repair its own re-review found to add an unsupported claim.** `case-study-sv` Redline replaced a conforming headline with `Gemensam logg hjälpte Elm Quay men kostade förberedelsetid`, re-reviewed it, reported it `Olöst` with the reason that the body declines exactly that conclusion, and shipped it on the ground that `budgeten var förbrukad`. Reverting needed no material the run lacked. The same shape appears in `article-flawed`, where the round created the subheading `Elin Rask vill se användningstiderna först`, reported it as repeating its first sentence, and left it standing.
- **[#390](https://github.com/Kntnt/skills/issues/390) — Write: a subheading repeats the sentence under it.** `column-sv` Write delivered `## Jag vet inte om rutan skulle hjälpa` over `Jag vet inte om ytterligare en ruta gör möten bättre.` Both judges fail `G2` on it as a stated requirement, not a preference. Neither source checker raised it and the delivery account does not mention it. The `column-sv` Redline row found it on the first pass and repaired it, which is where the defect's visibility comes from.
- **[#391](https://github.com/Kntnt/skills/issues/391) — Write: an unbounded wait for the checker's report file outlives the run.** The harness blocks a subagent from writing a report file; both Write rows record it — `case-study-sv` in its own account (`Den första kontrollantens rapport kunde inte skrivas till fil, eftersom harnesset stoppar rapportfiler från underagenter`), `column-sv` in a NOTE carried by both checker reports. The wait that follows is a process, not a file, so no inventory sees it. The evaluator saw it in the process table while the runs were in flight — three `until [ -f …/report-1.md ]; do sleep 5; done` shells for each Write row — and found none left once the last run had ended; the one loop known to have outlived its run, by five hours and fifty-five minutes, came from a staged run made earlier the same day outside this evaluation.
- **[#383](https://github.com/Kntnt/skills/issues/383) — Redline changes a clean passage outside any finding and omits changes from its account.** Already open; cited rather than filed again. Four rows here: the silent clause in `opinion-clean`, and the unreported headline, standfirst and subheading rewrites in `article-flawed`, `case-study-flawed` and `case-study-sv` Redline.
- **[#388](https://github.com/Kntnt/skills/issues/388) — a trace-bearing Claude-family evaluation harness.** Already open; both records name it against every `T1` and `R2` line.

## One gap in the evidence

`column-flawed`'s judge B gives no verdict for `P1`. Its file runs `G1`, `G2`, `W1`, `L1`, `L2`, `R1` and stops. Its reply to the evaluator did read `P1 pass`, but the file is the judgement, so the criterion is recorded `pass` on judge A's reading alone, and the entry's `notes` say so. Nothing else in the twenty-four judgements is missing a criterion its brief asked for.
