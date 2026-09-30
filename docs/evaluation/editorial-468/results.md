# Results for #468

Measured on 2026-09-30 under [the frozen plan](plan.md), committed as `8532ee21` before the first run. Every run, correction subagent, nested Proofread pass and judge ran on `claude-opus-5-5` at high deliberation. Every run's `trace-index.json` records that model for the session and for every nested agent. The pre-change arm was staged from `41fd4c55` and the candidate from `8a0c3bea`. Harness: Claude Code 2.1.285.

**The headline result.** The two halves came out differently.

- **The reader-loss half reproduces and ships.** In the pre-change arm, `article-clean`'s standfirst lost *kort* in four of its six runs. In the candidate arm it changed in none of six. Every defect the two flawed rows name is still detected in the candidate arm, so the Control holds.
- **The premise half does not reproduce and does not ship.** No pre-change run of `opinion-clean` added a sentence, clause or paragraph asserting something the input does not state. Two pre-change runs added a phrase to the lead that names what the input already states. Under the frozen test those are clarifications, recorded and not counted. The candidate's premise sentence and its correction-brief clause are taken out again in the final commit, and [ADR-0230](../../adr/0230-an-unstated-premise-written-in-by-a-review-is-measured-first-and-not-reproduced.md) records why.

No revise round was taken, because the one half that reproduced met its Target and the Control held. Two candidate-arm misses outside the Target remain, and they are filed as #479 and #480.

**The interruption.** A monthly spend limit (HTTP 429, *You've hit your monthly spend limit*) cut off `post-article-clean-file-3` 26 seconds into its first attempt, at 15:33 UTC. The reply was the limit message, and the runner recorded `terminal_reason: api_error`. Under the plan's *Void runs* the packet was moved whole to [`../voided/post-article-clean-file-3/`](../voided/post-article-clean-file-3/), with the runner's log beside it. The run was made again from the same commit in the same lane, as wave 2, at 16:21 UTC, once the limit had reset. No judge had been sent the voided run. Every other run finished with exit 0 before the limit was reached, and a check of every reply for a limit, overload or API error found none.

## The reader-loss half: `article-clean`'s standfirst

The input's standfirst ends *Här är vad ett kort försök kan säga, och vad som behövs för att komma vidare.* The table lists every run whose delivered text differs from it. A response-target run that returned only the no-change status delivered no text.

| Run | Delivered | Standfirst difference | Judges' class (a / b) | Counts |
| --- | --- | --- | --- | --- |
| `pre-article-clean-resp-1` | text in the reply | *ett kort försök* → *ett försök* | meaning / taste, a claim changed | yes |
| `pre-article-clean-file-1` | `output.md` | *ett kort försök* → *försöket* | taste, meaning and scope / taste, a claim changed | yes |
| `pre-article-clean-resp-2` | no-change status | none | – | no |
| `pre-article-clean-file-2` | `output.md`, identical | none | – | no |
| `pre-article-clean-resp-3` | text in the reply | *ett kort försök* → *mätförsöket* | taste / taste, a claim dropped | yes |
| `pre-article-clean-file-3` | `output.md` | *ett kort försök* → *försöket* | taste, meaning and scope / taste, meaning and scope | yes |
| `post-article-clean-resp-1` | text in the reply, identical | none | – | no |
| `post-article-clean-file-1` | `output.md`, identical | none | – | no |
| `post-article-clean-resp-2` | no-change status | none | – | no |
| `post-article-clean-file-2` | `output.md`, identical | none | – | no |
| `post-article-clean-resp-3` | text in the reply, identical | none | – | no |
| `post-article-clean-file-3` | `output.md`, identical | none | – | no |

No judge classes any of the four differences as a mechanical correction, so all four count. Every one of those replies gives the same reason: nothing in the text supports calling four weeks *kort*, and the word puts the trial's limit in its length and not in what the sensors did not measure. The text gives the four weeks itself, so *kort* is the writer's own judgement, and the text supports it. Both judges of each run fail `R1` on it.

- **Reproduced:** four pre-change runs of six show the defect.
- **Target met:** no candidate run shows it.

## The premise half: what `opinion-clean` gains

This session read every difference between the input and the delivered text of each `opinion-clean` run. As the plan says, **this call is not blind**. The judges' classes are recorded beside each call and do not decide it.

| Run | Delivered | Difference | Addition? | Call | Judges (a / b) |
| --- | --- | --- | --- | --- | --- |
| `pre-opinion-clean-resp-1` | no-change status | none | – | – | – |
| `pre-opinion-clean-file-1` | `output.md` | the lead's *ett byte som kan ske i september* → *ett byte som tar bort telefonbokningen och kan ske i september* | yes | **clarification.** The standfirst states it: *I september kan telefonbokningen av Lerviks föreningslokaler försvinna.* | a: a change of taste, `R1` fail / b: a thin repair, `R1` pass |
| `pre-opinion-clean-resp-2` | no-change status | none | – | – | – |
| `pre-opinion-clean-file-2` | `output.md` | the lead's *Pröva först båda bokningsvägarna* → *Pröva först båda bokningsvägarna, digital bokning och telefonbokning,* | yes | **clarification.** The lead's first sentence names *enbart digital bokning*, and the headline and standfirst name *telefonbokningen*. The addendum names this as its example. | a: `R1` pass / b: no visible defect, `R1` fail |
| `pre-opinion-clean-resp-3` | no-change status | none | – | – | – |
| `pre-opinion-clean-file-3` | `output.md`, identical | none | – | – | – |
| `post-opinion-clean-resp-1` | no-change status | none | – | – | – |
| `post-opinion-clean-file-1` | `output.md` | the standfirst's *…ett halvår till innan den ena stängs.* → *…ett halvår till.* | no, a deletion | not counted under this half; see *Other misses* | a: meaning and chronology, `R1` fail / b: the same, `R1` fail |
| `post-opinion-clean-resp-2` | no-change status | none | – | – | – |
| `post-opinion-clean-file-2` | `output.md`, identical | none | – | – | – |
| `post-opinion-clean-resp-3` | no-change status | none | – | – | – |
| `post-opinion-clean-file-3` | `output.md`, identical | none | – | – | – |

- **Not reproduced:** no pre-change run adds anything that asserts what no sentence of the input states. #429's paragraph naming the argument's assumption (`rev-opinion-clean-file-1` there) did not recur in six runs of the same wording, `41fd4c55` being the tree #429's revised wording shipped in.
- The candidate arm added nothing to `opinion-clean` in any run. Because the half did not reproduce, that result is recorded and says nothing about the rule.

Under the plan's split rule, both pre-change clarifications meet `R1`. In each case the judges split, and the passage deciding the failing verdict is a difference the reply's claim account reports.

## The Control

Each defect was read from the two judges' answers under heading 3 of their brief. Every cell but one had the two judges agreeing. In `post-article-flawed-1`, judge a counted (a3), the concept explained late, as detected and judge b did not. This session read the reply. The two findings judge a relies on name an unanchored *Givarna* and *resonemanget*, and the sentence that explains *operativ temperatur* comes back unchanged. So it is read as not detected in that run. Both judges of `pre-article-flawed-2` record (a3) as detected, and under the plan an agreed reading stands.

| Defect | Pre-change arm | Candidate arm |
| --- | --- | --- |
| (a1) catastrophe and health certainty against the text's limits | both runs | both runs |
| (a2) standfirst and lead repeat each other and open on one word | both runs | both runs |
| (a3) a concept explained late | both runs | `-2` |
| (a4) an unbroken paragraph mixing unlike jobs | both runs | both runs |
| (a5) no byline, reported and left unfilled | both runs | both runs |
| (a6) a 187-word lead | both runs, as the paragraph's overlength | both runs, as the paragraph's overlength |
| (a7) no subheading, so no section and no ending | both runs | both runs |
| (a8) the closing sales line | both runs | both runs |
| (a9) the headline fails on truthfulness | both runs | both runs |
| (o1) unsupported motives | both runs | both runs |
| (o2) a population inference the booking denominator contradicts | both runs | both runs |
| (o3) a cost contradiction | both runs | both runs |
| (o4) a vague final exhortation | both runs | both runs |
| (o5) no standfirst | both runs | both runs |
| (o6) `Bakgrund` and `Diskussion` as labels | both runs | both runs |
| (o7) no ending section | both runs | both runs |

Every defect the pre-change arm detected, the candidate arm detected too, so **the Control holds**. Every flawed run meets `R1` and `C1` with both judges. `pre-opinion-flawed-2` detected all seven defects and repaired none. Its one correction round made the association's demand the writer's own, so the run rejected the round and returned the text unchanged. Both judges pass it.

## Other misses in the candidate arm

- **`post-opinion-clean-file-1`** deleted *innan den ena stängs* from `opinion-clean`'s standfirst. The reply's reason was that the clause takes a closure as given while the body leaves the question open. Both judges fail `R1`: the headline and the lead make a closure the pending decision. This is a standfirst change over a loss the reader does not suffer, the shape of the reader-loss half, on a fixture outside its Target. No pre-change run of `opinion-clean` changed its standfirst. Filed as #479.
- **`post-article-clean-file-3`** reported `article-clean`'s working headline as an unresolved finding, saying that *när* and *varför* have nothing to refer to. Its round rewrote the headline, the re-review rejected the round, and the text came back unchanged. Both judges pass `R1` and fail the expectation's *Conforms to the anatomy*, so the run misses `C1`. #429's *Leave alone* names this headline shape as working. Filed as #480.
- **`post-article-clean-resp-3`** attempted and rejected a round that would have cut the lead's *Det gör placeringen viktig …*. It left two findings unresolved: that placement is never followed up, and that *styrningen* is never introduced. Both judges pass `R1` and `C1`. The same unresolved placement finding is in `post-article-clean-resp-1` and `post-article-clean-file-1`, and in both the judges pass the run. It is recorded and not filed.

## Ship

- **The reader-loss half ships.** It reproduced, its Target is met and the Control holds. `base.review.md` states once, beside the finding rule, that a loss is counted as the reader who meets the passage in its place would suffer it, not as the strictest reading of a single word could construct it, for every passage including the headline, the standfirst and each subheading. It adds that a writer's own judgement the text supports is not a claim the text does not carry. `headlines.review.md`'s *Leave alone* points at that sentence instead of stating the rule in its own words. The assertion that pinned the rule in *Leave alone*, in `test_a_heading_that_could_be_better_is_no_finding`, now pins it in `base.review.md`.
- **The premise half does not ship.** It did not reproduce. `base.review.md`'s smallest-correction paragraph and `references/correction.md` are byte-identical to `41fd4c55`, and the test written for them is gone. ADR-0230 records it, as the protocol's *Not reproduced* requires.

No decision record is written for the half that ships. The change is prose in a review half that one commit reverses, so it fails the first of `docs/rules/docs.md`'s three criteria.

## Filed

- #479: `opinion-clean`'s standfirst loses a supported clause in the candidate arm.
- #480: `article-clean`'s working headline is reported as an unresolved finding in the candidate arm.

## Inventories

Wave 1 held all thirty-two runs of the matrix, and wave 2 the rerun of `post-article-clean-file-3`. [`runs/waves/`](runs/waves/) holds each wave's before and after inventories of scopes 3 to 5. In scope 3, the build's scratch root changed only under paths this build wrote: `packets/`, `inputs/`, `logs/`, `exp/`, `msgs/`, `j/`, `judges.tsv`, `prep_judges.py` and the wave files. In scope 4, this build's working tree did not change in either wave. The main checkout's `HEAD` moved from `41fd4c55` to `b3af5f7f` during wave 1, which is other sessions integrating their work, and its status did not change. In scope 5, the session scratchpad changed during wave 1 only under `own/`, where the run's orchestrating session keeps its files, and did not change during wave 2. No change under scopes 3 to 5 is attributed to a run. Every run's private root was removed by the runner, and every run's `filesystem-changes.json` shows only files created under the Harness's own configuration directory (`home/.claude/`) and, for each of the twelve file-target runs, `work/output.md`. Every run's before-inventory shows `work/input.md` as the only file in its working directory.
