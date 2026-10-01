# Results for #479

Measured on 2026-10-01 under [the frozen plan](plan.md), committed as `43aa13fe` before the first run. Every run, correction subagent, nested Proofread pass and judge ran on `claude-opus-5-5` at high deliberation; every run's `trace-index.json` records that model and deliberation for the session and for every nested agent, 81 agents in all, and every trace is `complete`. The pre-change arm was staged from `fb169087`, the commit this build started from. The candidate was written after that arm had been read, committed as `f3851e9f`, and the post-change arm was staged from it. Harness: Claude Code 2.1.286.

**The headline result.** The defect reproduces and the candidate ships.

- **Reproduced.** Three of six pre-change runs of `opinion-clean` recorded a closure-as-given finding against the standfirst's *innan den ena stängs*, and all three delivered the change: the clause deleted once, and twice reworded to *innan det avgörs om den ena ska stängas*.
- **Target met.** No candidate run of `opinion-clean` recorded any finding at all. All six delivered the text unchanged or returned the no-change status, and both judges pass `R1` on every one.
- **The negative case holds.** `opinion-closure-certain`, which states the closure as settled, was detected in three of three runs in each arm, and every run meets `R1`.
- **The controls hold.** `article-clean`'s standfirst changed in no run of either arm, and each arm has two `R1` misses. Every `opinion-flawed` defect was detected in both runs of both arms.

No revise round was taken. No run was void: every run exited 0 with `terminal_reason: completed`, and no reply carries a limit, overload or API error.

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

- **Reproduced:** three pre-change runs of six show the defect, each at the depth *delivered*. No pre-change run reached the depths *reported* or *restored*: in each of the three, the session accepted the round and the proofreading pass changed nothing further.
- **Target met:** no candidate run shows the defect, and no candidate run misses `R1`.
- **Every other finding** against `opinion-clean` was the lead's unnamed telephone route, in `pre-opinion-clean-resp-1` and `pre-opinion-clean-resp-3`. It is a clarification of the kind ADR-0230 records, and both judges pass `R1` on both runs. No candidate run raised it.

All three findings cite the claim rule of `base.md`. One adds the headline rule that a standfirst claims only what the text claims, and two add the opinion genre's rule that the author's position is neither strengthened nor weakened. Each says the reader of the standfirst would take the author as conceding that a route closes. None cites the reader-loss rule #468 shipped into `base.review.md`, which was in force in this arm. The reading arises where the opinion review checks *factual premises and predictions*: the clause was read as the author's forecast of the decision's outcome, although the headline and the lead make that outcome the pending decision the author asks to postpone.

## The trace

For the twelve `opinion-clean` runs and the six `opinion-closure-certain` runs, each packet's `rounds.md` keeps the four stages apart:

1. **The first review's findings**, quoted whole from the first correction brief, or a line saying no correction subagent was started.
2. **The correction proposal**, as every difference between the text the round was handed and the text it returned, with the subagent's note.
3. **The re-review's decision**, as the session's own words after the round.
4. **The delivered text**, as every difference between the input and `output.md` or the text in the reply.

In the three pre-change runs that show the defect, the proposal at stage 2 is the change delivered at stage 4, the session accepted it at stage 3 (*I've accepted the correction and am now starting the one mechanical proofreading pass* in `pre-opinion-clean-file-1`), and every reply reports the change accurately as a changed or removed claim. An accurate account does not make the change permissible: the run still shows the defect. No run in either arm restored a closure change, so no restored deletion is counted as a delivered one. No candidate run of `opinion-clean` reached stage 2.

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

Detected in three of three runs in each arm, with no `R1` miss in either, so **the negative case holds**. The candidate's rule kept the finding for a closure stated as settled, with the word *innan* and the standfirst position both kept from the target. In `pre-opinion-closure-certain-3` the closing Proofread pass also changed *webbokningar* to *webbbokningar*; both judges class it as mechanical, and one notes that the original form was not wrong.

## The controls

### `article-clean`

The standfirst changed in no run of either arm. The candidate changes only `genres/opinion.review.md`, and every `article-clean` trace in both arms shows the session loading `genres/article.md` and `genres/article.review.md` and no other genre file, so the two arms ran byte-identical instructions on this fixture.

| Run | Delivered | Difference | `R1` (a / b) | Whose |
| --- | --- | --- | --- | --- |
| `pre-article-clean-resp-1` | no-change status | none | pass / pass | – |
| `pre-article-clean-file-1` | `output.md`, identical | none | pass / pass | – |
| `pre-article-clean-resp-2` | no-change status, the placement finding unresolved | none | pass / pass | – |
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

## Judging

Sixty-eight judgements, two per run, each by a fresh `kntnt-opus-high` subagent sent its brief verbatim and a directory under `j/` named by twelve random hexadecimal digits; `runs/judges.tsv` maps each directory to its run. Two messages named a directory one character off the one prepared, through this session's typing. The judge of `pre-opinion-clean-file-3` letter b found no such directory and wrote nothing; it was sent the correct path and judged that directory. The judge of `post-opinion-closure-certain-2` letter a found the one directory sharing the prefix, judged it, and says so in its judgement. The second judge listed the names under `j/` to find it; neither judge read any other run's files.

## Ship

**The candidate ships.** It reproduced, its Target is met, the negative case holds and every control holds, so no revise round was taken. `genres/opinion.review.md` gains one paragraph: an opinion often argues over a decision still to be taken, and a passage setting out what should happen before it names that decision as the text presents it, pending, proposed or possible. Read with the headline, the standfirst and the lead, such a passage neither forecasts nor concedes the outcome, in the standfirst as in the body, and is no finding. It is one where the text states the outcome as settled while another passage leaves it open, or predicts what nothing in the text carries. `test_an_opinions_step_before_a_pending_decision_is_not_a_forecast` in `tests/test_kntnt.py` pins it, and `skills/kntnt/catalog.json` is regenerated. Redline's `SKILL.md`, `help.md` and correction brief, `base.review.md`, `headlines.review.md`, Write's halves, the corpus, the correction budget, the closing Proofread pass, metadata and the input and output contracts are unchanged; Redline's help does not describe the genre review halves at this level, so nothing in it disagrees.

The candidate touches neither `base.review.md` nor `headlines.review.md`, so it does not meet #480's change in a shared file. #480's target is `article-clean`'s headline, which this candidate cannot reach, since an `article` run does not load the opinion review.

No decision record is written. The change is prose in a genre's review half that one commit reverses, so it fails the first of `docs/rules/docs.md`'s three criteria, as #468's shipped half did. The number reserved for one, `0234`, is left unused.

## Filed

- #486: `article-clean`'s lead loses its placement sentence in `post-article-clean-resp-3`, on instructions identical to the pre-change arm's.

## Inventories

Wave 1 held the seventeen pre-change runs and wave 2 the seventeen candidate runs. [`runs/waves/`](runs/waves/) holds each wave's before and after inventories of scopes 3 to 5. In scope 3, the build's scratch root changed only under paths this build wrote: `packets/`, `inputs/`, `logs/`, `j/`, `msgs/`, `tools/`, `judges.tsv` and `waves/`. In scope 4, this build's working tree gained only `runs/rounds.py`, written by this session during wave 1, and the main checkout's `HEAD` moved from `fb169087` to `fe2587b7` during wave 2, which is other sessions integrating their work. In scope 5, the session scratchpad gained `out.md` and `ret.md` during wave 1, and `own/gate-476.json` and `own/verify-476.md` with a changed `own/builders.txt` during wave 2, all written by the run's orchestrating session for other tickets. No change under scopes 3 to 5 is attributed to a run. Every run's private root was removed by the runner, and every run's `filesystem-changes.json` shows only files under the Harness's own configuration directory (`home/.claude/`) and, for each of the eighteen file-target runs, `work/output.md`. Every run's before-inventory shows `work/input.md` as the only file in its working directory.
