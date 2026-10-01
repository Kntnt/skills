# Results for #479

Measured on 2026-10-01 under [the frozen plan](plan.md), committed as `43aa13fe` before the first run. Every run, correction subagent, nested Proofread pass and judge ran on `claude-opus-5-5` at high deliberation; every run's `trace-index.json` records that model and deliberation for the session and for every nested agent, 107 agents in all, and every trace is `complete`. The pre-change arm was staged from `fb169087`, the commit this build started from. The candidate was written after that arm had been read, committed as `f3851e9f`, and the post-change arm was staged from it. The session that verified that build ran the candidate four more times on `opinion-clean` and once on `opinion-closure-certain`, with the same runner, seat and inputs; those five runs are recorded below as the `spot-` runs. They showed the Target missed, so the plan's one revise round was taken: a revised candidate, committed as `3b1f791d`, was run over `opinion-clean`'s three pairs. Harness: Claude Code 2.1.286.

**The headline result.** The defect reproduces. The first candidate missed its Target once it was run again, and the revised candidate ships under the plan's fallback rule.

- **Reproduced.** Three of six pre-change runs of `opinion-clean` recorded a closure-as-given finding against the standfirst's *innan den ena stängs*, and all three delivered the change: the clause deleted once, and twice reworded to *innan det avgörs om den ena ska stängas*.
- **The first candidate missed the Target.** Its six post-change runs recorded no finding. Of the four further file-target runs the verifying session made of it, two recorded the closure-as-given finding and delivered the clause reworded to *innan det avgörs om den ena ska stängas*. Both cited the candidate's own paragraph as the requirement the clause failed. Two of the first candidate's ten `opinion-clean` runs show the defect.
- **The revise round.** No run of the revised candidate recorded a closure-as-given finding, and all six kept the standfirst as it was. One run, `rev-opinion-clean-resp-2`, misses `R1` with both judges over a different change: a lead clarification that names the telephone route. So the Target as the plan defines it is not met.
- **The negative case holds.** `opinion-closure-certain`, which states the closure as settled, was detected in three of three runs of each arm, and in the one spot run of the first candidate. Every one of those runs meets `R1`. The revise round did not run it again; see *The negative case* for what that leaves unmeasured.
- **The controls hold.** `article-clean`'s standfirst changed in no run of either arm, and each arm has two `R1` misses. Every `opinion-flawed` defect was detected in both runs of both arms.
- **Ships under the fallback.** Fewer revised runs show the defect than pre-change runs, none of six against three of six. The negative case and every control hold, read from the first candidate's arm. The revised candidate therefore ships. The `R1` miss is filed as #492.

One revise round was taken. No run was void: every run exited 0 with `terminal_reason: completed`, and no reply carries a limit, overload or API error.

## What the ticket measured before

In #468's evaluation one candidate-arm run of six, `post-opinion-clean-file-1` staged from `8a0c3bea`, deleted *innan den ena stängs* from `opinion-clean`'s standfirst, and both judges failed `R1` on it for meaning and chronology. None of that evaluation's six pre-change runs, staged from `41fd4c55`, changed the standfirst. Those counts were made on other product versions and are recorded here as the ticket's history only. They are not this evaluation's baseline, and nothing below compares a rate against them: the baseline is the pre-change arm staged from `fb169087` in this evaluation, on the same seat.

## The Target: `opinion-clean`

Every finding in the table is quoted from the first correction brief the session handed a subagent, which [`runs/rounds.py`](runs/rounds.py) writes to each packet's `rounds.md` with the round's proposal, what the session said next and the delivered text. A run that started no correction subagent reported its findings in its reply. As the plan says, **the closure-as-given call is this session's and not blind**; the judges' `R1` readings are beside it and do not decide it.

| Run | First review's findings | Closure-as-given | Depth | Delivered | Judges' `R1` (a / b) |
| --- | --- | --- | --- | --- | --- |
| `pre-opinion-clean-resp-1` | 1. the standfirst's last sentence: *Bisatsen "innan den ena stängs" utgår från att en av bokningsvägarna kommer att stängas efter halvåret. Brödtexten drar inte den slutsatsen.* 2. the lead's *båda bokningsvägarna* names the telephone route only in the headline and standfirst | **yes**, finding 1 | delivered | text in the reply: *… ett halvår till innan det avgörs om den ena ska stängas.*, and the lead gains *telefonbokning och digital bokning* | pass / pass |
| `pre-opinion-clean-file-1` | 1. *bisatsen "innan den ena stängs" förutsätter att en av bokningsvägarna kommer att stängas när försöket är över. Brödtexten lämnar utfallet öppet* | **yes** | delivered | `output.md`: *… innan det avgörs om den ena ska stängas.* | pass / fail; split, the deciding passage is reported as a changed claim, so it meets `R1` |
| `pre-opinion-clean-resp-2` | none | no | – | no-change status | pass / pass |
| `pre-opinion-clean-file-2` | 1. *Bisatsen "innan den ena stängs" förutsätter att en av bokningsvägarna stängs när halvåret är slut. Brödtexten tar inte den ståndpunkten* | **yes** | delivered | `output.md`: *… ett halvår till.* | fail / fail |
| `pre-opinion-clean-resp-3` | 1. the lead's *båda bokningsvägarna* names the telephone route only in the headline and standfirst | no | – | text in the reply, the lead gaining *digital bokning och telefonbokning* | pass / pass |
| `pre-opinion-clean-file-3` | none | no | – | `output.md`, identical | pass / pass |
| `post-opinion-clean-resp-1` | none | no | – | no-change status | pass / pass |
| `post-opinion-clean-file-1` | none | no | – | `output.md`, identical | pass / pass |
| `post-opinion-clean-resp-2` | none | no | – | no-change status | pass / pass |
| `post-opinion-clean-file-2` | none | no | – | `output.md`, identical | pass / pass |
| `post-opinion-clean-resp-3` | none | no | – | no-change status | pass / pass |
| `post-opinion-clean-file-3` | none | no | – | `output.md`, identical | pass / pass |
| `spot-opinion-clean-file-1` | 1. *Krav: opinion.review.md – ett avsnitt som anger vad som bör ske före ett beslut som ännu ska fattas varken förutspår eller medger beslutets utfall … ”innan den ena stängs” förutsätter att en av bokningsvägarna kommer att stängas* | **yes** | delivered | `output.md`: *… innan det avgörs om den ena ska stängas.* | fail / pass; split, the deciding passage is reported as a changed claim, so it meets `R1` |
| `spot-opinion-clean-file-2` | 1. *Krav: en debattartikel som argumenterar om ett beslut som ännu inte är fattat varken förutsäger eller medger beslutets utfall … ”innan den ena stängs” säger att en av bokningsvägarna kommer att stängas när halvåret är slut* | **yes** | delivered | `output.md`: *… innan det avgörs om den ena ska stängas.* | fail / fail |
| `spot-opinion-clean-file-3` | 1. the lead's *båda bokningsvägarna* names the telephone route only in the headline and standfirst | no | – | `output.md`, the lead gaining *telefonbokning och digital bokning* | pass / pass |
| `spot-opinion-clean-file-4` | none | no | – | `output.md`, identical | pass / pass |
| `rev-opinion-clean-resp-1` | none | no | – | no-change status | pass / pass |
| `rev-opinion-clean-file-1` | none | no | – | `output.md`, identical | pass / pass |
| `rev-opinion-clean-resp-2` | 1. the lead names the digital route only, and *båda bokningsvägarna* has its telephone referent only in the headline and standfirst | no | – | text in the reply, the lead gaining *och som tar bort telefonbokningen* | fail / fail |
| `rev-opinion-clean-file-2` | 1. the lead's *båda bokningsvägarna* names the telephone route only in the headline and standfirst | no | – | `output.md`, the lead gaining *digital bokning och telefonbokning* | fail / pass; split, the deciding passage is a difference the reply reports, so it meets `R1` |
| `rev-opinion-clean-resp-3` | none | no | – | no-change status | pass / pass |
| `rev-opinion-clean-file-3` | none | no | – | `output.md`, identical | pass / pass |

- **Reproduced:** three pre-change runs of six show the defect, each at the depth *delivered*. No pre-change run reached the depths *reported* or *restored*: in each of the three, the session accepted the round and the proofreading pass changed nothing further.
- **The first candidate:** none of its six post-change runs shows the defect, but two of its four spot runs do, both at the depth *delivered*. The Target is missed, which is why the revise round was taken.
- **The revised candidate:** none of its six runs shows the defect. One run misses `R1`, `rev-opinion-clean-resp-2`, over the lead clarification below. So the Target is not met as the plan defines it.
- **Every other finding** against `opinion-clean` was the lead's unnamed telephone route. It came up in `pre-opinion-clean-resp-1`, `pre-opinion-clean-resp-3`, `spot-opinion-clean-file-3`, `rev-opinion-clean-resp-2` and `rev-opinion-clean-file-2`. Each cites the article anatomy's review rule on a definite form whose referent only the standfirst supplies, and none touches the file either candidate changes. It is a clarification of the kind ADR-0230 records. The judges pass it in the first three runs and split on the fifth. In `rev-opinion-clean-resp-2` both judges fail it as taste on a clean text. No open ticket carries it, so it is filed as #492.

All three findings cite the claim rule of `base.md`. One adds the headline rule that a standfirst claims only what the text claims, and two add the opinion genre's rule that the author's position is neither strengthened nor weakened. Each says the reader of the standfirst would take the author as conceding that a route closes. None cites the reader-loss rule #468 shipped into `base.review.md`, which was in force in this arm. The reading arises where the opinion review checks *factual premises and predictions*: the clause was read as the author's forecast of the decision's outcome, although the headline and the lead make that outcome the pending decision the author asks to postpone.

The two spot runs that show the defect cite the first candidate's own paragraph, and each turns it into a requirement. The paragraph said such a passage *neither forecasts that outcome nor concedes it*, and kept a finding where *the text states the outcome as settled while another passage leaves it open*. Both runs read *innan den ena stängs* as stating the closure as settled, which made the clause fail the very rule meant to protect it. The paragraph's examples (*try both, measure first, decide afterwards*) also named the step, but not the clause's reference to the change the decision would make, so nothing in it covered the clause. The revised candidate rewrites the paragraph to remove both gaps:

- It names the reference to the proposed change, with examples (*before the branch closes*, *until the switch*, *ahead of the merger*).
- It says that such a reference takes for granted only that the change is on the table.
- It says outright that the reference *is not the text stating the outcome as settled*.
- It says the reference needs no rewording to say *whether* the change will come.
- It keeps the finding for a passage that says the change is already decided, or will come *whatever the step shows*, while another passage leaves it open.

No restraint in it is worded as a property the protected passage must have.

## The trace

For the twelve `opinion-clean` runs and the six `opinion-closure-certain` runs, each packet's `rounds.md` keeps the four stages apart:

1. **The first review's findings**, quoted whole from the first correction brief, or a line saying no correction subagent was started.
2. **The correction proposal**, as every difference between the text the round was handed and the text it returned, with the subagent's note.
3. **The re-review's decision**, as the session's own words after the round.
4. **The delivered text**, as every difference between the input and `output.md` or the text in the reply.

In the three pre-change runs that show the defect, the proposal at stage 2 is the change delivered at stage 4, the session accepted it at stage 3 (*I've accepted the correction and am now starting the one mechanical proofreading pass* in `pre-opinion-clean-file-1`), and every reply reports the change accurately as a changed or removed claim. An accurate account does not make the change permissible: the run still shows the defect. No run in either arm restored a closure change, so no restored deletion is counted as a delivered one. No post-change run of `opinion-clean` reached stage 2. The two spot runs that show the defect went the same way as the pre-change runs: the proposal at stage 2 is the delivered change, and the session accepted it at stage 3. In `spot-opinion-clean-file-1` the session said *Omgranskningen hittar inga nya fynd … så kandidaten godtas*. In the revise round, only `rev-opinion-clean-resp-2` and `rev-opinion-clean-file-2` reached stage 2, each with the lead clarification. Each session accepted its round, and no closure change was proposed, restored or delivered. The five spot packets were copied from the verifying session's scratch (`verdict-b/spot/packets/`) under the names used here, and `rounds.py` was run on them again. Only the title line of each `rounds.md` differs from that session's copies.

## The negative case: `opinion-closure-certain`

The input differs from `opinion-clean` only in the standfirst's last clause, *innan telefonbokningen ändå stängs för gott*. Both judges of every run record it as detected under heading 3, so no split needed this session's reading.

| Run | Finding (stage 1) | Delivered standfirst ending | `R1` (a / b) |
| --- | --- | --- | --- |
| `pre-…-1` | the clause makes the closure *ett givet utfall*; the lead and the ending leave it open | *… innan telefonbokningens framtid avgörs.* | pass / pass |
| `pre-…-2` | the standfirst draws a conclusion the text does not draw and contradicts it | *… innan det avgörs om telefonbokningen ska stängas för gott.* | pass / pass |
| `pre-…-3` | the clause takes permanent closure as given; the text never draws that conclusion | *… ett halvår till.* | pass / pass |
| `post-…-1` | cites the new rule: a text arguing over a decision not yet taken neither forecasts nor concedes its outcome, and one stating the outcome as settled while another passage leaves it open contradicts itself | *… ett halvår till.* | pass / pass |
| `post-…-2` | cites the new rule's contradiction clause | *… innan telefonbokningens framtid avgörs.* | pass / pass |
| `post-…-3` | cites the new rule's contradiction clause | *… innan det avgörs om telefonbokningen ska stängas för gott.* | pass / pass |
| `spot-opinion-closure-certain-1` | cites the first candidate's rule: *ändå stängs för gott* states the closure as settled while the headline and the body keep it open | *… innan det avgörs om telefonbokningen ska stängas för gott.* | pass / pass |

Detected in three of three runs in each arm, with no `R1` miss in either, so **the negative case holds**. The first candidate's rule kept the finding for a closure stated as settled, with the word *innan* and the standfirst position both kept from the target. The spot run of the first candidate also detected it. In `pre-opinion-closure-certain-3` and `spot-opinion-closure-certain-1` the closing Proofread pass also changed *webbokningar* to *webbbokningar*; the judges class it as mechanical, and one notes that the original form was not wrong.

**What the revise round leaves unmeasured.** The plan's revise round covers only the input whose reading missed, `opinion-clean`, and reads every other input from the first candidate's arm. So no run of the revised candidate was made on `opinion-closure-certain` or `opinion-flawed`, and their readings above are the first candidate's. The revised paragraph keeps the finding this case needs, in different words: a passage that says the change *will come whatever the step shows*, while another passage leaves it open, is a contradiction. *Ändå stängs för gott* is such a passage. Whether the revised wording still detects it in every run is a reading of the text and not a measurement. `article-clean` is not affected by this gap: an `article` run loads no opinion file, so both candidates give it byte-identical instructions.

## The controls

### `article-clean`

The standfirst changed in no run of either arm. The candidate changes only `genres/opinion.review.md`, and every `article-clean` trace in both arms shows the session loading `genres/article.md` and `genres/article.review.md` and no other genre file, so the two arms ran byte-identical instructions on this fixture.

| Run | Delivered | Difference | `R1` (a / b) | Whose |
| --- | --- | --- | --- | --- |
| `pre-article-clean-resp-1` | no-change status | none | pass / pass | – |
| `pre-article-clean-file-1` | `output.md`, identical | none | pass / pass | – |
| `pre-article-clean-resp-2` | text in the reply, unchanged, the placement finding unresolved | none | pass / pass | – |
| `pre-article-clean-file-2` | `output.md`, identical | none | pass / pass | – |
| `pre-article-clean-resp-3` | text in the reply | headline rewritten to *Mätningar visar när Björkskolans luft var kall, inte varför* | fail / fail | #480 |
| `pre-article-clean-file-3` | `output.md` | headline rewritten to *… visar när luften var kall, inte varför* | fail / fail | #480 |
| `post-article-clean-resp-1` | no-change status | none | pass / pass | – |
| `post-article-clean-file-1` | `output.md`, identical, after a headline round was rejected; the headline and placement findings unresolved | none | pass / pass | #480 for `C1` |
| `post-article-clean-resp-2` | no-change status | none | pass / pass | – |
| `post-article-clean-file-2` | `output.md` | headline rewritten to *Björkskolans givare visar när det blev kallt, inte varför* | fail / fail | #480 |
| `post-article-clean-resp-3` | text in the reply | the lead's *Det gör placeringen viktig när …* → *Det är utgångspunkten när …* | fail / fail | #486 |
| `post-article-clean-file-3` | `output.md`, identical | none | pass / pass | – |

- **Standfirst differences:** none in either arm, so #468's improvement is preserved.
- **`R1` misses:** two in each arm, so **the control holds** under the plan's rule. The plan's whose-miss section takes `post-article-clean-file-2`, a working headline rewritten, off this ticket's account as #480's. Taking #480's misses off the pre-change count as well would leave none there against one in the candidate arm, `post-article-clean-resp-3`. That run's instructions are the pre-change arm's byte for byte, as above, so its miss is the product as it stood at `fb169087` and not the candidate's. It is recorded here with both readings and filed as #486, since no open ticket carries it; #468 recorded the same placement finding left unresolved in three of its candidate-arm runs without filing it.

### `opinion-flawed`

Every defect was read from both judges' answers under heading 3 of their brief, and every cell had the two judges agreeing.

| Defect | Pre-change arm | Candidate arm |
| --- | --- | --- |
| (o1) unsupported motives | both runs | both runs |
| (o2) a population inference the booking denominator contradicts | both runs | both runs |
| (o3) a cost contradiction | both runs | both runs |
| (o4) a vague final exhortation | both runs | both runs |
| (o5) no standfirst, reported and left unwritten | both runs | both runs |
| (o6) `Bakgrund` and `Diskussion` as labels | both runs | both runs |
| (o7) no ending section | both runs | both runs |

**The control holds.** Every flawed run meets `R1` with both judges. `post-opinion-flawed-2` rejected its round because the rewritten headline repeated the opening sentence, so it delivered the text unchanged with every finding reported unresolved. Both of its judges pass it, and one notes the sound repairs discarded with the round.

## `C1`

`C1` is met by every `opinion-clean`, `opinion-closure-certain` and `opinion-flawed` run, except `pre-opinion-clean-file-2`, whose deleted clause both judges record as the clean text not preserved. That is the Target's defect, counted above. `pre-opinion-clean-file-1` and `pre-opinion-clean-resp-3` split, and in both the deciding passage is reported in the reply's claim account, so both meet `C1`. In `article-clean`, `pre-article-clean-resp-3`, `pre-article-clean-file-3`, `post-article-clean-file-1` and `post-article-clean-file-2` miss *Conforms to the anatomy* over the headline, #480's, and `post-article-clean-resp-3` misses *the calm explanation*, #486.

Of the spot runs, `spot-opinion-clean-file-2` misses `C1`: both judges record the early thesis as no longer stated the same way in the standfirst, which is the Target's defect. `spot-opinion-clean-file-1` splits, and its deciding passage is reported in the reply's claim account, so it meets `C1`. The other three spot runs meet it. Every revise-round run meets `C1`. `rev-opinion-clean-resp-2` splits, one judge recording *Conforms to the anatomy* as not met over the lead finding, and the reply reports that change, so it meets `C1` under the same rule.

## Judging

Ninety judgements, two per run, each by a fresh `kntnt-opus-high` subagent sent its brief verbatim and a directory under `j/` named by twelve random hexadecimal digits; `runs/judges.tsv` maps each directory to its run. Two messages named a directory one character off the one prepared, through this session's typing. The judge of `pre-opinion-clean-file-3` letter b found no such directory and wrote nothing; it was sent the correct path and judged that directory. The judge of `post-opinion-closure-certain-2` letter a found the one directory sharing the prefix, judged it, and says so in its judgement. The second judge listed the names under `j/` to find it; neither judge read any other run's files.

The twenty-two judgements of the spot runs and the revise round were made by the session that wrote the revised candidate, under the same rules, with directories and messages made by the same script. The spot runs were judged after the fact, because the verifying session had read their outputs but not had them judged. Every judge found its directory.

## Ship

**The revised candidate ships, under the plan's fallback rule.** The defect reproduced, and the first candidate met the Target in its committed arm but missed it in two of the four spot runs. So the one revise round was taken over `opinion-clean`, the input whose reading missed. The revised candidate shows the defect in none of its six runs, against three of six before the change. One of its runs misses `R1` over a lead clarification that neither candidate's change reaches, so the Target as the plan defines it is not met. Under the plan, the revised candidate then ships only where fewer of its `opinion-clean` runs show the defect than the pre-change arm's, and the negative case and every control hold, reading an input not re-run from the first candidate's arm. All of that holds, so it ships. The remaining miss is filed as #492.

What ships is one paragraph in `genres/opinion.review.md`, the revised one, which replaces the first candidate's:

- An opinion often argues over a decision still to be taken, asks for a step before it, and names the change that decision would make as the text has proposed it.
- Where the headline, the standfirst or the lead sets that change out as proposed or pending, such a reference takes for granted only that the change is on the table, which the text says.
- It is not the text stating the outcome as settled, and no forecast or concession that the change will follow the step, in the standfirst as in the body.
- It is read as written, needs no rewording to say whether the change will come, and is no finding.
- A finding needs a passage that asserts the outcome itself. That is one that says the change is already decided, or will come whatever the step shows, while another passage leaves it open, which is a contradiction. It is also one that predicts what the decision or the step will show with nothing in the text to carry it.

`test_an_opinions_step_before_a_pending_decision_is_not_a_forecast` and `test_an_opinions_reference_to_a_pending_change_is_kept_out_of_the_finding` in `tests/test_kntnt.py` pin it. The second test also holds that the paragraph says nothing a passage *neither* does, the wording the spot runs turned into a requirement. `skills/kntnt/catalog.json` is regenerated. Nothing else changes: Redline's `SKILL.md`, `help.md` and correction brief, `base.review.md`, `headlines.review.md`, Write's halves, the corpus, the correction budget, the closing Proofread pass, metadata, and the input and output contracts. Redline's help does not describe the genre review halves at this level, so nothing in it disagrees.

Neither candidate touches `base.review.md` or `headlines.review.md`, so neither meets #480's change in a shared file. #480's target is `article-clean`'s headline. Neither candidate can reach it, since an `article` run does not load the opinion review.

No decision record is written. The change is prose in a genre's review half that one commit reverses. It therefore fails the first of `docs/rules/docs.md`'s three criteria, as #468's shipped half did. The number reserved for a record, `0234`, is left unused.

## Filed

- #486: `article-clean`'s lead loses its placement sentence in `post-article-clean-resp-3`, on instructions identical to the pre-change arm's.
- #492: `opinion-clean`'s lead gains a clause naming the telephone route in `rev-opinion-clean-resp-2`, and both judges fail `R1` on it. It is an `R1` miss in the arm whose wording ships, outside the Target.

The first candidate's two spot-run misses are the Target's own defect. The revised wording replaces that candidate's, so they are not filed again.

## Inventories

Wave 1 held the seventeen pre-change runs and wave 2 the seventeen candidate runs. [`runs/waves/`](runs/waves/) holds each wave's before and after inventories of scopes 3 to 5. In scope 3, the build's scratch root changed only under paths this build wrote: `packets/`, `inputs/`, `logs/`, `j/`, `msgs/`, `tools/`, `judges.tsv` and `waves/`. In scope 4, this build's working tree gained only `runs/rounds.py`, written by this session during wave 1, and the main checkout's `HEAD` moved from `fb169087` to `fe2587b7` during wave 2, which is other sessions integrating their work. In scope 5, the session scratchpad gained `out.md` and `ret.md` during wave 1, and `own/gate-476.json` and `own/verify-476.md` with a changed `own/builders.txt` during wave 2, all written by the run's orchestrating session for other tickets. No change under scopes 3 to 5 is attributed to a run. Every run's private root was removed by the runner, and every run's `filesystem-changes.json` shows only files under the Harness's own configuration directory (`home/.claude/`) and, for each of the eighteen file-target runs, `work/output.md`. Every run's before-inventory shows `work/input.md` as the only file in its working directory.

Wave 3 held the six revise-round runs.

- **Scope 3.** The scratch root changed only under paths this build wrote:
  - the six `rev-` packets under `packets/`;
  - the five `spot-` packets, copied there from `verdict-b/spot/packets/` during the wave;
  - the judges' directories under `j/` and their messages under `msgs/`;
  - `logs/` and `judges.tsv`.

  The verifying session's own `verdict-b/` did not change.
- **Scope 4.** This build's working tree moved from `fd586418` to `8ec5b483`, a correction this session committed during the wave. The main checkout stayed at `fe2587b7`.
- **Scope 5.** The session scratchpad gained `own/gate-477.json`, `own/gate-478.json`, `own/gate-480.json`, `own/verify-477.md`, `own/verify-478.md` and `own/verify-480.md`, and `own/builders.txt` changed. The run's orchestrating session wrote all of these for other tickets.

No change is attributed to a run. The spot runs were made by the verifying session outside this build's waves, so they have no wave inventory. For them, the runner's own inventories stand alone:

- every private root was removed;
- each run's `filesystem-changes.json` shows `work/output.md` and files under `home/.claude/` only;
- each run's before-inventory shows `work/input.md` alone.

The same holds for the six revise-round runs, except that the three response-target runs created no `work/output.md`.
