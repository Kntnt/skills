# Results for #429

Both arms and the one revise round, run on 2026-09-29 and 2026-09-30 against the method [`plan.md`](plan.md) froze before the first run. Artefacts: `runs/`, `voided/`. The record is [`../records/redline-claude-2026-09-30-429.md`](../records/redline-claude-2026-09-30-429.md).

One hundred and one counted Redline invocations: thirty-six in the pre-change arm staged from `e7773344`, thirty-six in the post-change arm staged from the first candidate `c7f639c6`, and twenty-nine in the revise round staged from the second candidate `2c5b191f`. Every run was a fresh top-level Claude Code 2.1.285 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), and every session and every nested agent in it ran on `claude-opus-5-5` at high deliberation, which each packet's `trace-index.json` records; every trace is complete. Ninety-seven runs were judged, each by two fresh `kntnt-opus-high` subagents blind to the arm, the model and this ticket: 194 judgements. #396's four control runs were read by this session from the reply, as the plan provides. No Codex Harness and no GPT model was started, controlled or invoked.

**The headline result.** The defect reproduces: in the pre-change arm every clean control came back with a heading rewritten or added in at least one of its six runs, and `column-sv-r2` and `opinion-en_GB-r1` missed `R1` on a heading rewrite in both of their runs. The first candidate left the target missed on six of seven fixtures, and made `column-clean` worse. The revise round's candidate met the target on `article-clean`, `opinion-clean` and `opinion-en_GB-r1`, and cut the runs that miss on the re-run subset from fourteen to six. The target is not met: `case-study-clean` still has its headline rewritten, `column-clean` still gains a subheading over its ending on the article anatomy's rule that an ending is a section of its own, and one `column-sv-r2` run repaired `Rutan som inte finns` without the column's *ruta*. `column-flawed`'s headline lost the finding that it names no subject of its own under both candidates, a regression. Thomas's ruling ships whatever the measurement shows; the second candidate ships, as the one with fewer target misses; every remaining miss is recorded here as measured and filed.

## Before the counted runs

**The interruption.** The first attempt at this build ran both arms on 2026-09-29 until an expired login (`authentication_failed`, *OAuth access token has been revoked*) cut off nine runs at 22:58 UTC: `pre-article-clean-resp-3`, `pre-article-clean-file-3`, `post-article-clean-resp-3`, `post-article-clean-file-3`, `post-case-study-clean-file-2`, `pre-case-study-clean-resp-3`, `pre-case-study-clean-file-3`, `post-case-study-clean-resp-3` and `post-case-study-clean-file-3`. Each returned the API error as its whole reply. Under the protocol's *Interrupted runs are void* they are kept under [`voided/`](voided/) and were made again on 2026-09-30 from the same commits, in the same lanes; no judge had been sent any of them. The other sixty-three runs and their 118 judgements had finished before the interruption and are counted as they stand.

**The order of work.** The second candidate was committed as `2c5b191f` on 2026-09-30, after every judgement of the first two arms apart from the nine reruns was in, and before its own first run. The interrupted attempt had left a draft of it uncommitted in the working tree; that draft named the fixtures' own words (*the library's meeting template*, *a decision* against *a purpose*), and those were taken out before the commit, so the committed wording names no fixture; its twenty-nine runs are the post-change arm's run names for the fixtures whose reading missed or regressed, listed in [`runs/matrix-revise.tsv`](runs/matrix-revise.tsv) and run by the frozen [`runs/lane.sh`](runs/lane.sh) with that matrix as its second argument. `rev-column-flawed` was added to that matrix when the analysis of the first arms found its regression; `rev-article-clean-*` and `rev-case-study-clean-*` waited in their lanes until the reruns of the same inputs had finished, so no two runs of one input were ever in flight at once.

**The wave inventories.** `runs/waves/wave-1-before-*` was read before the first run on 2026-09-29. `runs/waves/wave-1-after-*` was read on 2026-09-30 before the reruns, after the interruption, so it spans the interruption as well as the first wave. `runs/waves/wave-2-before-*` and `runs/waves/wave-2-after-*` bracket the reruns and the revise round. Between them, scope 4 shows the main checkout's `HEAD` moving as the run integrated another ticket, and this working tree gaining the revise candidate; scope 5 shows the orchestrator's own files appearing under the session scratchpad's `own/`. None is attributable to a run, and every run's own inventories show nothing outside its private root.

## The target, per fixture and arm

A clean control meets the target in an arm when none of its six runs rewrote, removed or added a heading line. A draft meets it when no run misses `R1` on a heading difference. No heading difference in any run is classed a mechanical correction by both judges, so every one below counts.

| Fixture | Pre-change | First candidate | Second candidate |
| --- | --- | --- | --- |
| `article-clean` | missed: `file-2`, `file-3` | missed: `resp-3` | **met** |
| `case-study-clean` | missed: `resp-1`, `file-3` | missed: `file-1`, `file-2`, `resp-3` | missed: `file-1`, `file-3`, `resp-3` |
| `column-clean` | missed: `file-2` (added), `resp-2`, `resp-3` (added) | missed: `file-1` (added), `file-2` (added), `file-3`, `resp-1` (added), `resp-2` | missed: `file-3` (added), `resp-1` (added) |
| `opinion-clean` | missed: `resp-3` | missed: `file-1`, `resp-2` | **met** |
| `column-sv-r1` | met | met | not re-run |
| `column-sv-r2` | missed: `a`, `b` | missed: `a`, `b` | missed: `a` |
| `opinion-en_GB-r1` | missed: `a`, `b` | missed: `b` | **met** |

**Reproduced.** The pre-change arm misses on six of seven fixtures, so the defect reproduces on this seat.

**The first candidate** met the target on `column-sv-r1` alone, as the pre-change arm did, and missed on the other six. Over those six it has fourteen runs that miss against the pre-change arm's twelve: `article-clean` and `opinion-en_GB-r1` fell by one, `column-clean` rose from three to five and `case-study-clean` and `opinion-clean` rose by one each.

**The second candidate**, over the same six fixtures re-run, has six runs that miss. It meets the target on `article-clean`, `opinion-clean` and `opinion-en_GB-r1`, in every one of their fourteen runs. `column-sv-r1` met the target in both earlier arms and was not re-run, since the revise round takes only the subset that failed; the second candidate's reading of it is therefore the first candidate's.

### Clean controls, run by run

Every heading difference, with how both judges classed it. `resp` is the response-target run of a pair and `file` the file-target run; a response-target run that returned only the no-change status delivered no text and has no heading to compare.

| Run | Heading difference | Judges A / B on it | `R1` A / B |
| --- | --- | --- | --- |
| `pre-article-clean-file-2` | `Mätförsöket i Björkskolan visar när, inte varför` → `Björkskolans givare visar när luften var kall, inte orsaken` | taste, attribution and meaning / taste, attribution and meaning | fail / fail |
| `pre-article-clean-file-3` | the same headline → `Björkskolans mätvärden bör ställas mot rummens användning` | a result turned into a recommendation / the same | fail / fail |
| `post-article-clean-resp-3` | the same headline → `Givare visar när Björkskolans klassrumsluft var kall, inte varför`; `En gräns för det lokala försöket` → `Arbetsgränsen underskreds i 14 pass – drag och upplevelse mättes inte` | taste / taste, both past the limits the text met | fail / fail |
| `pre-case-study-clean-resp-1` | `Elm Quay samlade reparationsärendena` → `Elm Quays arbetsledare ser nytta i gemensam reparationslogg`; `Två perioder med olika arbetsbelastning` → `Väntan på tilldelning var i median en arbetsdag kortare än tidigare` | meaning and attribution; meaning / attribution and meaning; meaning and causality | fail / fail |
| `pre-case-study-clean-file-3` | the headline → `Gemensam ärendebild hjälper, säger Elm Quays arbetsledare`; the second subheading → `Mediantiden till tilldelning var kortare än under de åtta veckorna före` | taste, the appraisal's condition lost / the same | fail / fail |
| `post-case-study-clean-file-1` | the headline → `Gemensam ärendebild hjälper, säger Elm Quays arbetsledare`; the second subheading → `Tilldelningen tog i median två arbetsdagar under försöket` | meaning, certainty, scope, attribution; causality / attribution and scope; meaning | fail / fail |
| `post-case-study-clean-file-2` | the headline → `Elm Quays arbetsledare skulle pröva reparationsloggen igen` | taste, the appraisal's condition lost / the same | fail / fail |
| `post-case-study-clean-resp-3` | the headline → `Reparationslogg gav Elm Quay en gemensam bild av ärendena`; the second subheading → `Kortare mediantid till tilldelning, men annan arbetsbelastning` | the customer no longer the actor, the condition lost / causality hardened | fail / fail |
| `rev-case-study-clean-file-1` | the headline → `Elm Quays loggförsök gav gemensam bild av ärendena` | a causal claim the text does not make / the same, the customer no longer the actor | fail / fail |
| `rev-case-study-clean-resp-3` | the headline → `Elm Quay samlade reparationsärenden på försök` | a reported repair / scope narrowed | pass / fail, met by the split rule: the reply covers the body sentence that decides it |
| `rev-case-study-clean-file-3` | the headline → `Elm Quay samlade reparationsärenden under ett försök` | a repair close to taste / the repair of a reported defect | pass / pass |
| `pre-column-clean-file-2` | added over the ending: `Ett försök med ett enda löfte` | taste, scope and meaning / taste, meaning and certainty | fail / fail |
| `pre-column-clean-resp-2` | `Mötesmallen har en ruta för allt utom varför` → `Mötesmallen har rutor för tid, inte för varför`; `Det är inte bara besluten jag vill åt` → `Beslut är inte det enda skälet att träffas` | scope; meaning and attribution / scope; attribution and meaning | fail / fail |
| `pre-column-clean-resp-3` | added over the ending: `Ett försök får visa vad frågan är värd` | taste, meaning / taste, meaning | fail / fail |
| `post-column-clean-file-1` | added over the ending: `Frågan får visa vad den är värd` | taste, meaning / taste, meaning | fail / fail |
| `post-column-clean-file-2` | added over the ending: `Jag kan inte lova mer innan frågan är provad` | taste, attribution / taste, attribution | fail / fail |
| `post-column-clean-file-3` | the headline → `Mötesmallen frågar när men inte varför` | meaning and scope / scope and meaning | fail / fail |
| `post-column-clean-resp-1` | added over the ending: `Om frågan hjälper återstår att pröva` | taste / taste, meaning | fail / fail |
| `post-column-clean-resp-2` | `Det är inte bara besluten jag vill åt` → `Ett möte kan ge mer än ett beslut` | taste, attribution and meaning / attribution and meaning | fail / fail |
| `rev-column-clean-resp-1` | added over the ending: `Låt varför stå före klockslagen` | taste / taste | fail / fail |
| `rev-column-clean-file-3` | added over the ending: `Vad jag ber dig om, och vad jag kan lova` | taste / taste | fail / fail |
| `pre-opinion-clean-resp-3` | `Mät också arbetet med två kanaler` → `Mät också arbetet med två bokningsvägar` | taste / taste | pass / pass |
| `post-opinion-clean-file-1` | `Besluta om försöket, inte om antagandet` → `Besluta om försöket, inte om ett antagande` | taste, meaning / taste, meaning | fail / fail |
| `post-opinion-clean-resp-2` | the same subheading → `Besluta om försöket, inte om antagandet att telefonen inte behövs` | meaning / meaning | fail / fail |

`pre-opinion-clean-resp-3` passed `R1` with both judges, who call the change taste and neither mechanical, so by the counting rule it is a rewrite. Every other run of every clean control delivered its headings unchanged or delivered no text.

**What the rewrites rest on.** The first candidate's clean-control rewrites each rest on a loss the reply names by reading one word at its strictest: *reparationsärendena* read as all of Elm Quay's repair cases, *en ruta för allt utom varför* read as an inventory of the template's boxes, *antagandet* read as pointing at an assumption nobody named although the headline above it says *ett antagande*, *vill åt* read as *wants to attack*, and a subheading naming its section's limit read as hiding the section's result. That is what the second candidate's wording answers. The added subheadings are another thing: each rests on `article-anatomy.review.md`'s reading that `column-clean`'s ending is not a section of its own, which no wording in `headlines.review.md` reaches and which the readiness addendum keeps out of this ticket's files.

### Drafts, run by run

| Run | What differs from the input | `R1` A / B | Heading miss |
| --- | --- | --- | --- |
| `pre-column-sv-r1-a` | the headline `Mallen` → `Mötesmallen`; the dash | pass / pass | no |
| `pre-column-sv-r1-b` | the dash | pass / pass | no |
| `post-column-sv-r1-a` | the headline `Mallen` → `Mötesmallen`; the dash | fail / pass, met by the split rule: the reply's claim account covers the headline | no |
| `post-column-sv-r1-b` | the same | pass / pass | no |
| `pre-column-sv-r2-a` | `Rutan som inte finns` → `Formuläret för bibliotekets möten saknar ett varför`; the dash | fail / fail | yes |
| `pre-column-sv-r2-b` | → `Bibliotekets mötesmall frågar när och vem, inte varför`; the dash | fail / fail | yes |
| `post-column-sv-r2-a` | → `Mötesmallen saknar en ruta för syftet`; the dash | fail / fail | yes |
| `post-column-sv-r2-b` | → `Bibliotekets mötesmall saknar en ruta för mötets syfte`; the dash | fail / fail | yes |
| `rev-column-sv-r2-a` | → `Bibliotekets mötesmall frågar inte varför vi ses`; the dash | fail / fail | yes |
| `rev-column-sv-r2-b` | → `Mötesmallen har ingen ruta för varför vi ses`; the dash | pass / fail, met by the split rule: the reply's claim account covers the headline | no |
| `pre-opinion-en_GB-r1-a` | `Six months, both routes, and something to measure` → `Get the evidence before settling how people book`; the byline moved; *Lervik's* | fail / fail | yes |
| `pre-opinion-en_GB-r1-b` | → `Measure each channel's staff time and ask why people still phone`; the byline moved; *Lervik's* | fail / fail | yes |
| `post-opinion-en_GB-r1-a` | the byline moved | pass / pass | no |
| `post-opinion-en_GB-r1-b` | → `Find out why people still ring before digital booking is settled`; the byline moved; *Lervik's*; two paragraphs split | fail / fail | yes |
| `rev-opinion-en_GB-r1-a` | the byline moved | pass / pass | no |
| `rev-opinion-en_GB-r1-b` | the byline moved; *Lervik's* | pass / pass | no |

**The `Rutan som inte finns` exception kept no run off the count.** It applies where a rewrite keeps the column's *ruta* and neither judge classes the change as a change to what a claim says. Three rewrites kept *ruta*:

- `post-column-sv-r2-a`, `Mötesmallen saknar en ruta för syftet`: judge A, *a change of taste, which is also a change to what a claim says by meaning, and secondarily by scope*; judge B, *a change to what a claim says, by meaning, with a lesser rise in certainty*. Counted.
- `post-column-sv-r2-b`, `Bibliotekets mötesmall saknar en ruta för mötets syfte`: both judges, *a change to what a claim says, by meaning and scope*, the body's *beslut* become *syfte*. Counted.
- `rev-column-sv-r2-b`, `Mötesmallen har ingen ruta för varför vi ses`: judge A, *a changed claim, by meaning*, judged a fair repair; judge B, *a change of taste that also changes meaning*. The run meets `R1` by the split rule, so it is no miss and the exception is not needed.

`pre-column-sv-r2-a`, `pre-column-sv-r2-b` and `rev-column-sv-r2-a` dropped *ruta*, so the exception cannot apply to them.

## Controls

### Flawed controls

A flawed control passes when the judges' answers under heading 3 of their brief, read by the split rule, record a finding in the reply that names each of its heading clauses. `C1` is both judges' `R1` against the row, read by the same rule.

| Control | Heading clauses, pre-change | First candidate | Second candidate | `C1` pre / first / second |
| --- | --- | --- | --- | --- |
| `article-flawed` | named: the headline faulted on truthfulness | named | not re-run | pass / pass / – |
| `case-study-flawed` | named: both subheadings, the second's unsupported conclusion; the first is repaired as a pre-echo of its quotation, which judge A reads as partly met and judge B as met in substance, and the reply's heading account covers it | named | not re-run | pass / pass / – |
| `column-flawed` | named: *angav inte kolumnens vinkel* and the claimed change | **not named**: the claimed change is named, the missing subject of its own is repaired but never reported, *partly met* by both judges | **not named**: implied by *fel bild av vad krönikan handlar om*, *only partly met* and *covered only by implication* | pass / pass / pass |
| `opinion-flawed` | named: `Bakgrund` and `Diskussion` as labels | named, the round rejected whole | not re-run | pass / pass / – |

`column-flawed` passed in the pre-change arm and fails in both candidates: a regression, filed below. The other three pass in both measured arms.

### #396's control

It fires when the reply reports that the subheading says what the closing quotation under it says, or changes that subheading and names that defect as the reason.

| Run | Fires | The reply |
| --- | --- | --- |
| `pre-case-question-en_GB-r2` | yes | *The section 3 subheading gave away the quotation. "Vale would use the schedule again for new jobs" said Vale's verdict before her quotation did*; repaired |
| `post-case-question-en_GB-r2` | yes | *Last subheading gave away the quotation beneath it … the reader met her judgement before reaching her quote*; repaired |
| `pre-case-question-en_GB-r3` | yes | *Subheading 3 gives away the quotation under it. "Vale would allow an extra week for the status names" states Vale's concession before her own words do*; reported, the round rejected |
| `post-case-question-en_GB-r3` | yes | *"Vale would allow an extra week for the status names" gave away the admission in Vale's quote below it*; repaired |

It fires in both measured arms on both drafts: no regression under the first candidate. The revise round re-runs only the subset that failed, so #396's control was not run against the second candidate; the second candidate keeps the bound that a subheading stating a quotation's judgement, figure or concession stays a finding, word for word as the first stated it.

## The revise round

**Why it was taken.** The first candidate missed the target on six fixtures and regressed `column-flawed`. The protocol allows one round, no larger than the subset that failed.

**What changed.** `2c5b191f` changes `headlines.review.md` alone, and no *Avoid* item: the *Avoid* opening says that a loss is something the reader gets wrong or does not get, and that a heading that could only be clearer, more specific or closer to another angle loses its reader nothing; *Leave alone* reads a heading as its reader meets it, counting a loss that reader would suffer rather than one the strictest reading of one word could construct, and says a subheading meets its reader after the headline and standfirst; the allusion case may name the subject in general terms where the first lines give the particulars; the figure-of-speech case covers the writer's own voice in a signed text and reads an overstating *everything* or *never* as the figure it is; a subheading summing up its section may name its limit or its setting; a heading one would word differently takes no finding and no change; and a repair names the text's point in the text's own word. It uses no wording from the fixtures, since a round tuned to its inputs fits the inputs rather than the behaviour. `test_a_heading_that_could_be_better_is_no_finding` holds the three sentences in place; it was seen failing against `c7f639c6`'s wording before `2c5b191f` was committed.

**The comparison.** Over the re-run subset the first candidate has fourteen runs that miss the target and the second six, so the second ships. The flawed control that regressed regresses under both.

## Whose miss

- `column-clean`'s added subheadings, in all three arms, rest on the article anatomy's own-section ending as `article-anatomy.review.md` reads it, not on the headline contract. #402 made that rule and is closed; no open ticket owns this behaviour. It is counted here, as the readiness addendum counts a candidate-arm rewrite of `article-clean`'s subheading, and filed.
- `opinion-clean`'s lead and body additions that name the text's assumption or both booking routes (`pre-opinion-clean-resp-2`, `post-opinion-clean-file-3`, `rev-opinion-clean-file-1`, and the lead additions of `pre-opinion-clean-file-2`, `pre-opinion-clean-resp-1`, `post-opinion-clean-resp-1`, `rev-opinion-clean-resp-1`, `rev-opinion-clean-resp-3`) are #434's behaviour and are recorded under it. None is a heading difference. #434 is closed and the behaviour remains in the shipped wording, so it is filed again as #468.
- `article-clean`'s standfirst losing *kort* (`post-article-clean-file-2`, `post-article-clean-resp-1`, `rev-article-clean-resp-1`, `rev-article-clean-resp-2`, `rev-article-clean-file-2`) is no heading difference and no open ticket owns it. It is filed as #467.
- Replies that report a heading finding against a clean control and change nothing (`post-article-clean-resp-2`, `post-case-study-clean-resp-1`, `rev-case-study-clean-resp-1`) miss `R1` under the literal split rule, the failing verdict resting on no difference. They are recorded, and the case-study ones are named in #463.

## What shipped, and why

The second candidate `2c5b191f` ships: Thomas's ruling ships whatever the measurement shows, this is the protocol's maintainer's-ruling case, and of the two candidates the second has fewer target misses over the re-run subset. The target is recorded as missed. No decision record is written: the change is prose in a review half that one commit reverses, so it fails the first of `docs/rules/docs.md`'s three criteria.

## Filed

Each remaining miss in the shipped arm, one issue per fixture, each `needs-triage` and naming #429:

- [#463](https://github.com/Kntnt/skills/issues/463) — `case-study-clean`: its headline rewritten as an overclaim the standfirst under it already bounds, in `rev-case-study-clean-file-1`, `-resp-3` and `-file-3`.
- [#464](https://github.com/Kntnt/skills/issues/464) — `column-clean`: a subheading added over its ending on the anatomy's own-section ending, in `rev-column-clean-resp-1` and `-file-3`, and in every arm.
- [#465](https://github.com/Kntnt/skills/issues/465) — `column-sv-r2`: `Rutan som inte finns` repaired without the column's *ruta*, in `rev-column-sv-r2-a`.
- [#466](https://github.com/Kntnt/skills/issues/466) — `column-flawed`: the headline's missing subject of its own no longer reported, under both candidates; the regression.

And two misses that are no heading but remain in the shipped wording with no open ticket to carry them:

- [#467](https://github.com/Kntnt/skills/issues/467) — `article-clean`: *kort* deleted from the standfirst, in three runs of the shipped wording and two of the first candidate.
- [#468](https://github.com/Kntnt/skills/issues/468) — `opinion-clean`: words naming its assumption added, #434's behaviour after #434 closed.

#396's control fired in every run, so nothing is filed against #396.

## Side effects and seat

`S1` passes on every run: each working directory held `input.md` alone when its session started. `O1` passes on one hundred runs: the runner's before-and-after inventories of each private root show nothing created, changed or removed outside the Harness's configuration beyond `work/output.md` on a file-target run, and in `post-case-study-clean-file-1` and `post-opinion-en_GB-r1-a` the system Python's bytecode cache, which is a cache. It fails on `pre-case-question-en_GB-r3`, whose reply says the Harness kept it from removing an empty temporary directory it had made as its working directory; the runner removed the root afterwards. Every file-target run delivered `output.md`.
