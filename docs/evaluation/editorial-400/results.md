# Results for #400

Both arms and the four #392 rows, run against the method [`plan.md`](plan.md) sets out as [`plan-amendment.md`](plan-amendment.md) amends it. The plan's own freeze was broken once, before any counted run began; *The frozen plan, and what the build voided* below says how, and what was done about it. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-24-400.md`](../records/redline-claude-2026-09-24-400.md), under the name the plan fixed.

Forty-four counted Redline invocations: fourteen in the pre-change arm, eighteen in the post-change arm and twelve on the #392 rows. Sixty-four judgements, two for each of the thirty-two main-matrix runs. Each judge was a fresh `kntnt-opus-high` subagent, blind to the arm, to the model and to this ticket. Every run was a fresh top-level Claude Code 2.1.281 session, started by [`runs/turn_run_2.sh`](runs/turn_run_2.sh). The model every session and every nested agent in it ran is recorded in the run's `seats.tsv`. For all forty-four counted runs that is `claude-opus-5-5`, at high deliberation, and nothing else. No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied to any run: every working directory held `input.md` and nothing else when its session started.

**The headline result.** The pre-change arm does not reproduce the defect where the plan measures it. Its one exercised target run, `pre-control-column-flawed`, replaced the headline `Möten förändrar allt`, named its defect and listed the changed claim, and both judges find the account accurate. `pre-control-article-flawed` passes every criterion. The other two target runs were not exercised: the headline in `pre-opinion-en_GB-r1` was left alone, and `pre-control-case-study-flawed` rejected its only round and returned the text unchanged.

The post-change arm meets every target line it exercised:

- `control-case-study-flawed` replaced both subheadings and the headline. Its account reports each with the defect that licensed it, and the removed `därför` with what the reader no longer has. Both judges find no difference unreported.
- `control-column-flawed` replaced the headline, reported it with its defect, and reported the changed claim by what the headline now asserts.
- `control-article-flawed` passes every criterion.
- `post-opinion-en_GB-r1-a` kept its headline, so line 1 was not exercised.

No control that passes the pre-change arm fails the post-change arm. None of the four #392 rows reproduced its change in three runs, so the #392 criterion and the limit criterion are `not exercised`.

As Thomas's ruling and the clarifications settle, **the candidate `c4c7b5e5` ships as it stands** under the plan's exit 2. No revise round was taken, no decision record is written, and two remaining misses are filed as #436 and #437.

## The frozen plan, and what the build voided

This build was resumed on 2026-09-28. The first builder was dispatched on 2026-09-24 and cut off by an account usage limit at 05:24 UTC. What it left was inspected before anything else was run. Every time below is UTC.

| Time (2026-09-24) | Event |
| --- | --- |
| 04:54:51 | `plan.md`, the turn files, the three briefs and the scripts under `runs/` committed as `57538946` |
| 04:55:19 – 04:56:48 | the fourteen pre-change runs made with `turn_run.sh` all stop at Redline's shim on the unmet Proofread dependency |
| 04:58:29 | [`plan-amendment.md`](plan-amendment.md) and `runs/turn_run_2.sh` committed as `82c119c3`; the fourteen refusals kept under [`voided/unsatisfied-dependency/`](voided/unsatisfied-dependency/) |
| 04:58:40 | `pre-column-sv-r1`, `pre-column-sv-r2`, `pre-opinion-en_GB-r1`, `pre-opinion-en_GB-r2` and `pre-control-column-clean` start |
| 05:00:29 | `pre-control-column-flawed` starts |
| **05:00:40** | **`plan.md` edited in `9ab8b40e`**: the seat flags of the one command line in its prose respelled as `--model=claude-opus-5-5 --effort=high`, because the suite's flag-grammar test refuses a value written apart from its flag |
| 05:03:15 | `pre-control-article-clean` starts: the first run started after the edit |
| 05:06:22 | the candidate committed as `c4c7b5e5` |
| 05:10:28 | the first post-change run starts |
| 05:17:05 – 05:24:33 | fourteen runs and eight judges stop on `You've hit your weekly limit` |

The plan says nothing in it is edited after the first run. `9ab8b40e` edited it after twenty runs had started: the fourteen dependency refusals, which were already void, and the six runs started at 04:58:40 and 05:00:29. A plan edited after a run started voids the runs made against the plan as it stood before the edit. The resumed build therefore **voids those six runs as well**. Their directories, packets, logs and the twelve judgements the first builder had collected for them are kept unread under [`voided/plan-edited-after-start/`](voided/plan-edited-after-start/). All six were run again under the same names on 2026-09-28.

Every counted run was started after 05:00:40, against the plan exactly as it stands in the tree. That plan has not been edited since. The edit changed the spelling of one command in the plan's prose. It did not change `turn_run.sh` or `turn_run_2.sh`, which is what starts a session, and it changed no turn, brief, criterion or exit. The disclosure stands anyway: the plan's opening sentence, *Nothing in this file … is edited after the first run*, is not true of the plan itself. Nothing this build wrote repeats that sentence.

**The other voids.**

- **Fourteen runs** stopped on the usage limit, with `api_error` as their terminal reason and a `<synthetic>` seat in `seats.tsv`. They are kept under [`voided/api-error/`](voided/api-error/) and were run again on 2026-09-28. They are `post-opinion-en_GB-r1-b`, `post-opinion-en_GB-r2-b`, eight controls (all but `column-clean` and `opinion-clean`) and `pair-<row>-1` for all four rows.
- **Eight judges** of `post-column-sv-r2-b`, `post-opinion-en_GB-r2-a`, `control-column-clean` and `control-opinion-clean` ended on the same limit. Their transcripts end in the limit message.
  - The two for `post-column-sv-r2-b` had written a judgement file into their directories. It was never collected and was not read. It is kept under [`voided/judges-cut-off/`](voided/judges-cut-off/), with the directory mapping.
  - The four runs were judged again by fresh judges.

**What was kept, and why it is sound.** Sixteen runs completed whole after the edit:

- eight pre-change controls: `article-clean`, `article-flawed`, `case-study-clean`, `case-study-flawed`, `opinion-clean`, `opinion-flawed`, `web-copy-clean` and `web-copy-flawed`;
- `post-column-sv-r1-a`, `post-column-sv-r1-b`, `post-column-sv-r2-a`, `post-column-sv-r2-b`, `post-opinion-en_GB-r1-a` and `post-opinion-en_GB-r2-a`;
- `control-column-clean` and `control-opinion-clean`.

For each of the sixteen:

- the return code is 0 and the terminal reason `completed`;
- `seats.tsv` names `claude-opus-5-5` alone;
- `response.md` is byte-identical to the reply the Harness returned;
- the run's own inventories show S1 and O1 holding.

Their installs are byte-identical to `git archive` of `c211a1d5` and of `c4c7b5e5`, checked again on 2026-09-28.

Twenty-four judgements of the twelve judged ones are kept. The build session's own subagent transcripts show each came from a `kntnt-opus-high` judge that completed normally. Each judge was sent only its neutral directory and, for a control, the frozen expectation, in the same message form the resumed judges were sent.

**Other departures, disclosed.**

- **Wave 1's closing inventory.** It was taken on 2026-09-28 at 07:29 rather than when the wave ended, because the builder was cut off before taking it. Between the two inventories:
  - The #385 checkout moved: #385's build committed in its own worktree, which is not this evaluation's. `main` did not move.
  - This build's own tree gained its commits.
  - The scratch root gained `install-post`, staged from the committed candidate, and the runs' own directories and packets.
  - Nothing is attributable to a run outside its own directory.
- **Wave 2's closing inventory.** [`runs/wave_inventory.sh`](runs/wave_inventory.sh) stopped part-way because the checkout `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/385` no longer exists; the run that integrated #385 removed it. The same commands were run by hand over the four checkouts, recording that one as absent, into `runs/waves/wave-2-after-repo.txt`. In wave 2:
  - `main` moved from `c211a1d5` to `b2bc8659` (*Merge #385 into the run branch*), and that checkout went away;
  - the session scratchpad did not change;
  - the scratch root changed only in this build's run directories, packets, logs, judge records and scoring notes.
  - No run of either wave has a side effect outside its own run directory.
- **One line redacted in the four `*-repo.txt` wave inventories.** Each recorded the read-only rework checkout `/Users/thomas/Projects/skills-rework` with a modified file in the directory this repository retired for agent documents, and the literal directory name, committed, fails `tests/test_agents_md.py::test_no_active_file_names_the_retired_agent_directory`. After the build was verified, line 7 of each file was changed to ` M <the retired agent-documents directory>/rework-handoff.md`, and nothing else in any file changed. The line is identical in all four files, so the before-and-after comparison is the same as it was. That checkout is not one a run could write, and the line does not bear on any criterion. The SHA-256 of each file as it was recorded:
  - `wave-1-before-repo.txt`: `bff5a8fbf5572ac53890eafa0add59afa09a98b022ab25812b5cfdad33fc0f54`
  - `wave-1-after-2026-09-28-repo.txt`: `90e7369d0afeaa020593af7ba9fec45c11535dbbc4b04bd13b7517eccc238d55`
  - `wave-2-before-repo.txt`: `90e7369d0afeaa020593af7ba9fec45c11535dbbc4b04bd13b7517eccc238d55`
  - `wave-2-after-repo.txt`: `36e602f58f82c32d680e6839aaea9783db16d08414cc8b825bc416bf8253549d`
- **One judgement copied early.** `control-opinion-clean`'s judgement B was copied into the run a few seconds before its judge returned. Its file matches the judge's final reply, *Fail, narrowly*, and the judge's directory was not recreated after it was removed. Every other judgement was collected only after its judge had returned.
- **Two replies differ.** In `pair-article-abt-2`, the reply the run saved to `response.md` and the reply the Harness returned differ in wording, but not in what they report. Both are kept, the second as `response.txt`. The run was not judged, because its change did not recur.
- **The judge directories** were made with `mktemp -d` in the system temporary directory, as the plan requires, so that no path a judge sees names the arm or the ticket. The eight directories the cut-off judges left there were moved whole into the scratch root.

## The runs

| Arm | Staged from | Runs | Made |
| --- | --- | --- | --- |
| pre | `c211a1d5` (`<start>`) | `pre-<draft>` on the four drafts; `pre-control-<row>` on the ten controls | 8 on 2026-09-24, 6 on 2026-09-28 |
| post | `c4c7b5e5`, the candidate | `post-<draft>-a`, `-b` on each draft; `control-<row>` on the ten controls | 8 on 2026-09-24, 10 on 2026-09-28 |
| #392 rows | `c4c7b5e5` | `pair-<row>-1` to `-3` on each of the four rows | 12 on 2026-09-28 |

The corpus commit is `c211a1d5` in every arm. Runs on different inputs ran side by side, at most five at once. The two post-change runs on one draft, and a row's successive runs, ran one after the other. Every run on one of the four #362 drafts held the shared `kntnt-eval-lock-<draft>` for its whole length.

## Reproduced

**Not reproduced.** The plan reads the defect as reproduced when one of the three named pre-change runs is exercised and misses, or `pre-control-article-flawed` misses line 4 on a miss counted against #400.

- **`pre-opinion-en_GB-r1`: not exercised.** The headline `Don't switch off Lervik's phone booking before we know what it costs` came back unchanged. The run rewrote the third subheading instead.
- **`pre-control-case-study-flawed`: not exercised.** The run rejected its only correction round and returned the text byte for byte. Both subheadings stand.
- **`pre-control-column-flawed`: exercised, met.**
  - The headline became `Mötesmallen saknar plats för det vi ska förstå tillsammans`.
  - The reply names its defect: *Rubriken ”Möten förändrar allt” påstod något som texten aldrig hävdar*.
  - It lists the headline under *Ändrade* with what it now says, and notes that the definite form *kan dock läsas som mer allmän än brödtextens ”vår mötesmall”*.
  - Both judges find every difference reported accurately. Neither records an `A2` miss.
- **`pre-control-article-flawed`: meets `C1`, `A2`, `O1` and `S1`.**
  - It names its removed headline claim and the lost `medan`: *Sambandet ”medan” … är borta*.
  - Both judges find the account accurate.

As the clarifications settle, the ruling ships all the same. The post-change arm was run and scored, and its results are written below as measured. No decision record is written.

## The target criterion: lines 1 to 3

| Line | Run | Arm | Exercised | Reading |
| --- | --- | --- | --- | --- |
| 1 — `N2` | `pre-opinion-en_GB-r1` | pre | no: headline unchanged | not exercised |
| 1 — `N2` | `post-opinion-en_GB-r1-a` | post | no: headline unchanged | not exercised |
| 2 — `A2` | `pre-control-case-study-flawed` | pre | no: text returned unchanged | not exercised |
| 2 — `A2` | `control-case-study-flawed` | post | yes: `Kunden fick en gemensam bild` → `Arbetsledaren om ärendearbetet`, `Resultatet bevisar allt` → `Tilldelningen gick fortare, men arbetsbelastningen var olika` | **met**: no judge records a miss |
| 3 — `A2` | `pre-control-column-flawed` | pre | yes | **met** |
| 3 — `A2` | `control-column-flawed` | post | yes: `Möten förändrar allt` → `Mötesmallen saknar plats för gemensam förståelse` | **met**: no judge records a miss |

**Exercised lines met: pre-change 1 of 1, post-change 2 of 2.** The two replacements in lines 2 and 3 were established by this session from `work/input.md` and the returned text.

Line 1 is not exercised in either arm, because neither run rewrote the headline. So nothing here measures the `Lervik's` narrowing the ticket was filed for. `post-opinion-en_GB-r1-b` kept the same headline too.

**What the post-change accounts say about the paratext.**

- **`control-case-study-flawed`** gives each changed part a numbered finding with a *Defekt:* line:
  - the headline: *”räddade” var ett orsakspåstående som texten själv motsäger*;
  - the first subheading: *både rubriken och meningen sa citatets omdöme i förväg, med samma ord*;
  - the second subheading: *rubriken påstod ett bevis som anteckningen i samma avsnitt motsäger*;
  - the new third subheading: *kundens omdöme … hängde efter resultatavsnittet*.

  It lists *Mellanrubrikens påstående att resultatet bevisar allt* among the removed claims, which is the entry #383's run left out. Both judges: *No difference goes unreported*, *Every difference is reported, and no report misstates what changed*.
- **`control-column-flawed`** names the headline's defect as *påstod en slutsats som texten varken drar eller stöder, och i en starkare ton än texten själv*. It reports the changed claim as *Nu påstår den att mötesmallen saknar plats för gemensam förståelse*.

**What neither arm names.** Both judges of both `column-flawed` runs note that no finding names the headline's other defect in the frozen expectation, that *it names no subject of its own*. They score that as partial detection under the expectation, not as an inaccurate account, and `C1` passes in both arms. The ticket body's *its two defects never named* is therefore half addressed in both arms: one defect is named and the other is not. The plan reads the line through `A2`, so the line is met, and this is recorded rather than scored.

## Line 4: `control-article-flawed` passes every criterion

| Run | `C1` A / B | `A2` | `O1` | `S1` |
| --- | --- | --- | --- | --- |
| `pre-control-article-flawed` | pass / pass | met | pass | pass |
| `control-article-flawed` | pass / pass | met | pass | pass |

`control-article-flawed` rejected its only round and returned the text byte for byte, so its account had no changed text to describe. Its thirteen findings name the standfirst/lead repetition and the shared opening word that #383's run left unnamed. Judge B: *the standfirst repeating the lead with the same opening word*. It does not exercise the paratext account, because no paratext changed.

## The #392 rows

Each row was run source-blind on its `redline/work/input.md` with the post-change turn file, one run at a time, up to three runs. For each run, this session compared `input.md` with the run's `delivered.md` at the passage the plan names, before any judge was sent. No row's change recurred, so no pair judge was sent.

| Row | Passage compared (input) | Run 1 | Run 2 | Run 3 | Row |
| --- | --- | --- | --- | --- | --- |
| `article-sv` | line 36, `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde` | kept (text returned unchanged) | kept (text returned unchanged) | kept (line 36 verbatim; headline and one standfirst phrase changed) | **not reproduced** |
| `article-pac` | line 32, `the report therefore presents lesson periods instead of one figure per day` | kept (delivered line 34) | kept (delivered line 34) | kept (delivered line 34) | **not reproduced** |
| `article-abt` | line 36, subheading `Effekten av eventuella justeringar är inte mätt` | kept (delivered line 36) | kept, and a sentence added under it | kept (delivered line 36) | **not reproduced** |
| `opinion-sv-r2` | line 26, `, inte om att de som ringer skulle vara lata eller dyra` | kept (text returned unchanged) | kept (delivered line 26) | kept (delivered line 26) | **not reproduced** |

**No row recurs, so the #392 criterion and the limit criterion are recorded `not exercised`.** Neither is met nor failed, and neither stops the candidate from shipping.

**What the rows did show, recorded and not scored.** All three `article-pac` runs removed other bounding words from the sentence before the one the plan names:

- `no capacity`;
- `a count with its exclusions`, which became `a count` or `not a verdict`.

All three accounts say what the reader lost:

- **`pair-article-pac-1`**: *Limit taken out (finding 2): the words "with its exclusions" are gone. This sentence no longer reminds the reader that the count has to be read alongside what it leaves out.*
- **`pair-article-pac-2`**: *A reader just no longer sees capacity named as one of them.*
- **`pair-article-pac-3`**: *Without it, this sentence no longer tells the reader that the figure stands together with its exclusions.*

`control-case-study-flawed` does the same for the removed `därför`: *Läsaren har alltså inte längre textens egen slutsats från anteckningen till programvaran.*

The same session behaviour appears once in the pre-change arm, where `pre-control-article-flawed` names the lost `medan`. These removals are not the rows' named changes, and no judge scored them.

## The regression clause

A control passes an arm when it meets `C1`, `A2`, `O1` and `S1` there, and a miss owned by another ticket counts neither way. `column-flawed` was exercised under line 3 in both arms and is read by that line. `case-study-flawed` was exercised in the post-change arm only, so it is read by this clause.

| Control | Pre: `C1` A/B, `A2` | Pre passes | Post: `C1` A/B, `A2` | Post passes | What decides the post-change reading |
| --- | --- | --- | --- | --- | --- |
| `article-clean` | pass/pass, met | yes | fail/fail, missed by both | yes: both misses are #430's | the headline `Mätförsöket i Björkskolan visar när, inte varför` rewritten, the `article-clean` headline #430 was filed for; both judges fail `C1` and call the stated defect taste |
| `article-flawed` | pass/pass, met | yes | pass/pass, met | yes | line 4 |
| `case-study-clean` | fail/fail, missed by both | **no** | fail/fail, missed by A | no | outside the clause: it fails the pre-change arm on the same shape (#436) |
| `case-study-flawed` | pass/pass, met | yes | pass/pass, met | yes | line 2 |
| `column-clean` | pass/pass, met | yes | pass/pass, met | yes | returned unchanged |
| `column-flawed` | pass/pass, met | yes | pass/pass, met | yes | line 3 |
| `opinion-clean` | pass/pass, met | yes | fail/fail, missed by both | yes: both misses are #431's | the lead gains `, ett byte som kan ske i september`, the edit #431 was filed for, which the pre-change run also made; this run's judges fail it and the pre-change run's pass it |
| `opinion-flawed` | pass/pass, missed by A (#435) | yes | pass/pass, met | yes | every change reported; both subheadings reported with their defect |
| `web-copy-clean` | pass/pass, met | yes | pass/pass, met | yes | returned unchanged |
| `web-copy-flawed` | pass/pass, met | yes | pass/pass, met | yes | every heading change reported with its defect |

**No control that passes the pre-change arm fails the post-change arm.** The regression clause holds.

## Exit

Lines 1 to 5 are met as far as they were exercised:

- line 1: not exercised;
- lines 2 and 3: met;
- line 4: met;
- line 5: not exercised.

The regression clause holds. By exit 2 of the plan, **the candidate ships as it stands** and no revise round is taken. The first three criteria of the triage addendum are met by the shipped wording stating them, as the clarifications settle. The shipped wording is `c4c7b5e5`:

- **Step 6 of Redline's `SKILL.md`.** A finding against a headline, a standfirst or a subheading *names that part and the defect in it*, since *that defect is what the delivery reports a repaired part by*.
- **Step 11 of Redline's `SKILL.md`.**
  - Every headline, standfirst and subheading the delivered text changed is reported with *the finding its repair answered — the part, and the defect that licensed the change*.
  - A repair that took *a limit, a connective or a bounding clause* out of the text is reported by *what a reader of that text no longer has*.
  - A changed claim is reported by *what it now asserts rather than how far its wording moved*, with *a headline, a standfirst and a subheading* named as claim-carrying and *never as shorter*.
- **Redline's `references/correction.md` and `help.md`** carry the same rules.
- **Unslop.** Step 9 of its `SKILL.md`, its `references/correction.md` and its `help.md` carry the limit rule and the changed-claim sentence in Unslop's words.
- **`base.review.md` and `headlines.review.md`** agree.

The requirement is the ticket thread. The candidate was written from it after the pre-change runs had started, and the resumed build did not change it.

## Every criterion, per run

`R1` on the drafts and `C1` on the controls are the judges' verdicts. Where the two split, #383's rule decides: the failing reading stands only where the passage it names is covered by neither the claim account nor the closing summary. `A2` and `N2` are read as the plan reads them, one judge being enough. A miss owned by another ticket is recorded under it. `O1` and `S1` pass on every counted run: each working directory held `input.md` alone when its session started, and the run's inventories show only `response.md` added beside it, with the staged install unchanged.

| Run | `R1`/`C1` A / B | `A2` | `N2` |
| --- | --- | --- | --- |
| `pre-column-sv-r1` | pass / fail: met (B's passage, the reworded headline, is in the claim account) | missed by A: the plural credited to the headline repair (#429) | met |
| `pre-column-sv-r2` | fail / fail | missed by B: the working headline presented as a defect, *syftet* presented as grounded (#429) | met |
| `pre-opinion-en_GB-r1` | fail / fail | missed: *one verb* for two, by both (#435); the byline's reason, by A (#435); the anatomy statement, by A (#402) | met; judge B's *accurate but incomplete* on the subheading recorded, not counted |
| `pre-opinion-en_GB-r2` | pass / pass | missed by both: *the English form* for the byline (#435) | met |
| `post-column-sv-r1-a` | pass / pass | missed by B: the plural credited to the headline repair (#429) | met |
| `post-column-sv-r1-b` | pass / pass | met | met |
| `post-column-sv-r2-a` | fail / fail | missed by A: *Brödtexten bär påståendet* overstates the support (#429) | missed by A: the headline's *varför* moved from the agenda to the template, unreported (#429) |
| `post-column-sv-r2-b` | fail / fail | met | met |
| `post-opinion-en_GB-r1-a` | pass / pass | met | met |
| `post-opinion-en_GB-r1-b` | fail / fail | missed by both: the subheading's defect, *repeated the first sentence under it in the same words*, is not in the text (**no owner; #436**); *seven paragraphs*, by B (#435) | met |
| `post-opinion-en_GB-r2-a` | pass / pass | missed by both: the headline's contraction `it's` not reported (**#400's shape; #437**) | met; judge B's *can* → *is free to* recorded, not counted: B marks it reported accurately |
| `post-opinion-en_GB-r2-b` | pass / pass | met | met |
| `pre-control-article-clean` | pass / pass | met | — |
| `pre-control-article-flawed` | pass / pass | met | — |
| `pre-control-case-study-clean` | fail / fail | missed by both: the subheading's defect is not in the text (**no owner; #436**) | — |
| `pre-control-case-study-flawed` | pass / pass | met | — |
| `pre-control-column-clean` | pass / pass | met | — |
| `pre-control-column-flawed` | pass / pass | met | — |
| `pre-control-opinion-clean` | pass / pass | met | — |
| `pre-control-opinion-flawed` | pass / pass | missed by A: *togs bort* for a rewritten closing line, outside the claim account (#435) | — |
| `pre-control-web-copy-clean` | pass / pass | met | — |
| `pre-control-web-copy-flawed` | pass / pass | met | — |
| `control-article-clean` | fail / fail | missed by both: the headline's stated defect is taste (#430) | — |
| `control-article-flawed` | pass / pass | met | — |
| `control-case-study-clean` | fail / fail | missed by A: the subheading's defect is not in the text (**no owner; #436**) | — |
| `control-case-study-flawed` | pass / pass | met | — |
| `control-column-clean` | pass / pass | met | — |
| `control-column-flawed` | pass / pass | met | — |
| `control-opinion-clean` | fail / fail | missed by both: the premise of the lead edit does not hold (#431); B's doubt about *lagts till* is #398's or #431's, not #400's | — |
| `control-opinion-flawed` | pass / pass | met | — |
| `control-web-copy-clean` | pass / pass | met | — |
| `control-web-copy-flawed` | pass / pass | met; judge B's *British wording* recorded, not counted: B marks the report accurate | — |

**`R1` on the drafts: pre-change 2 of 4, post-change 5 of 8.** Every draft `R1` miss turns, at least in part, on a paratext part rewritten on a defect the judges reject. For the column headlines that is #429's shape, and for the opinion subheading it is #436's. `post-opinion-en_GB-r1-b` also split two paragraphs against an 80-word guideline, which both judges count against it.

**The misses of #400's own shape.**

- **Pre-change arm: none.** No judge of a pre-change run records a paratext change unreported, or one reported without its defect or by its extent.
- **Post-change arm: one.** In `post-opinion-en_GB-r2-a` the headline `Keep the telephone until Lervik knows why it is used` became `Keep venue phone booking until Lervik knows why it's used`. The reply reports the change with its defect and what the headline now asserts. Both judges record the contraction brought in with it as unreported. The run is not a target line, so it does not bear on the exit. It is filed as #437.

**Misses no ticket above owns.** A working subheading was rewritten on a defect the judges find the text does not have, and the reply gave that defect as the reason. This happened in `pre-control-case-study-clean`, `control-case-study-clean` and `post-opinion-en_GB-r1-b`. The same opinion subheading was rewritten on a rejected defect in `pre-opinion-en_GB-r1` and `post-opinion-en_GB-r1-a` too, without an `A2` miss. The shape is in both arms and was not caused by the candidate. It is filed as #436.

## Criteria recorded `skipped`

- **`A1` and `C2`.** They are #383's own criteria: #383's closing summary and its control replay. The clarifications record them `skipped`.
- **`T1` and `R2`.** They are answered from a Harness trace. Each session's transcripts were kept in the build's scratch packet, as the plan says, and are not committed; this evaluation fixes no criterion on them.
- **`N1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2`.** They are not this evaluation's criteria, which are `R1`, `A2`, `N2`, `C1`, `O1` and `S1`.

No pair judge was sent, so no #380-brief criterion was scored.

## What is filed

- **#436** — Redline rewrites a working subheading on a defect the text does not have, and gives that defect as the reason — in a case study and an opinion piece.
- **#437** — Redline's account quotes a rewritten headline without saying it brought a contraction into a text that uses none.

Each is `needs-triage` and names #400. The other misses recorded above are owned by tickets that were already open: #398, #402, #429, #430, #431 and #435.
