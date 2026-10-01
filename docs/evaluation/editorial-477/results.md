# Results for #477

Both arms were run on 2026-10-01 under the method [`plan.md`](plan.md) froze in `516afe2e`, before the first run. The pre-change arm ran from 12:01 to 12:44 UTC and was judged and read before any candidate run. The candidate arm ran from 12:46 UTC; five of its runs were cut off at 13:05 UTC by the account's usage limit, kept apart as void, and made again from the same commit between 15:32 and 16:02 UTC, after the limit reset. Artefacts: `runs/`, and `voided/` for the cut-off runs. The record is [`../records/redline-claude-2026-10-01-477.md`](../records/redline-claude-2026-10-01-477.md).

Twenty-four Redline runs count, twelve in each arm. Every one is a fresh top-level Claude Code 2.1.286 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py); every trace is complete (`trace-status.json`), and the packets' `trace-index.json` files record `claude-opus-5-5` for every agent they hold — the sessions, their correction subagents and their reply checkers. Every run has two blind reply judges, and every run had a checker, so every run also has two blind correction judges: ninety-six judgements, each a fresh `kntnt-opus-high` subagent. No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied: every run's working directory held `input.md` and nothing else when its session started (`S1`, all 24).

**The headline result.** The fault reproduces: 7 of the pre-change arm's 12 runs carry a `T1` or `T2` miss, one of them a `T1` — a withheld attribution delivered as a rejection, made after the check from a draft that had it right, which is the historical fault. The candidate carries one in 2 of its 12, neither a `T1`. That is at most half the pre-change share (58.3% against 16.7%), and no candidate run carries a `T1` miss. **The Target is met.** `X1` holds in every candidate run, and each of `D1` on both contrast fixtures and `X2` passes in both arms. **The Control is met.** No revise round is taken. **The candidate `51777db2` ships.** Its two remaining misses are filed as #489 and #490, and the clean-text rewrites of `case-study-clean`, which no open ticket carries, as #491.

## The runs

| Arm | Staged from | Runs |
| --- | --- | --- |
| pre-change | `fb169087` | 12: `case-study-clean` as three response-target and file-target pairs, `withheld-overclaim` and `denied-overclaim` three times each |
| candidate | `51777db2` | 12, the same rows |
| void | `51777db2` | 5, kept under `voided/`: `post-case-study-clean-resp-2`, `-file-2`, `-resp-3`, `-file-3` and `post-denied-overclaim-3`, each ending *You've hit your session limit* with `terminal_reason: api_error`; each was made again |

Three judges were cut off by the same limit before writing anything — reply judge `b` and both correction judges of `post-withheld-overclaim-3`. They were dispatched again, as fresh subagents, on the same blind directories; `runs/judges.tsv` keeps one line per judgement counted.

## The states of each reply

`runs/states.py` wrote every run's states into `runs/<run>/states/`. Two things it does not do were found while the runs were judged, and are recorded rather than mended, since the script was frozen with the plan:

- **Three-backtick fences.** It reads the delivered text out of a reply, and the texts and the draft out of the checker's brief, only inside a fence of four or more backticks. Where a reply fenced its text with three, [`runs/delivered.py`](runs/delivered.py), written after the first run and named in each such `states.json` as `delivered_by`, wrote `delivered.md` and `final-reply.md` without the text. Where the checker's brief fenced with three, `checked-delivered.md` and `draft-reply.md` keep the fence and the brief's lead-in line (*This is everything the run is about to say about the two texts:*); the correction judges read past it, and several say so.
- **`X1` across fences.** For the same reason `states.json`'s `x1` compares the fence too, and is `false` for `post-case-study-clean-resp-2` alone. [`runs/x1.py`](runs/x1.py) compares the fenced text itself and writes it beside it as `x1_text`, which is `true` in all 24 runs. The plan's `X1` is read from `x1_text`.

The judge directories were staged by [`runs/judge_dirs.py`](runs/judge_dirs.py) and the judgements copied back by [`runs/collect.py`](runs/collect.py), both written for this run as the plan's *Judging* describes.

## The Target

A run's `T1` and `T2` misses, read from both kinds of judge and, for a reply judge's false statement, from whether it stands in `states/draft-reply.md` in the same words.

| Run | Miss | The delivered statement, and where it came from |
| --- | --- | --- |
| `pre-withheld-overclaim-1` | **`T1`, `T2`** | *Den som läste inledningsstycket fick alltså med sig en slutsats som texten längre ner avvisar.* The draft the checker read said *… som texten längre ner uttryckligen avstår från*. The checker returned nothing. Both correction judges: made false after the check — the note declines to credit the software and does not reject the conclusion. Both reply judges called *avvisar* borderline and passed it. |
| `pre-withheld-overclaim-2` | `T2` | *… och går sedan vidare till gruppens mål …* added while correcting the one item the checker returned; the goal is the paragraph's first sentence. Both reply and both correction judges. |
| `pre-withheld-overclaim-3` | `T2` | *Därefter går det vidare med gruppens mål och resultatet.* added the same way. All four judges. |
| `pre-case-study-clean-resp-3` | `T2` | *… stycket går sedan vidare till gruppens mål …* added the same way. All four judges. |
| `pre-case-study-clean-file-2` | `T2` | *Läsaren får inte längre intrycket att anteckningarna visar ett resultat av försöket.* The draft limited it to the reader of the lead; the reword dropped the limit, and the delivered text still reports the note's results. Correction judge `a`; judge `b` read it as limited and passed it. |
| `pre-case-study-clean-resp-1` | `T2` | *ingressen och inledningsstycket upprepar inte varandra*, false — both give eight weeks and two houses — and reworded after the check from a draft that made the same claim in other words. Correction judge `a`. |
| `pre-denied-overclaim-3` | `T2` | *ingressen och inledningsstycket upprepar inte varandra och börjar med olika ord*, the same claim, reworded after the check. Both reply judges. |
| `post-case-study-clean-file-2` | `T2` | *Den som bara ser rubriken kan därför läsa det som att flera av Elm Quays arbetsledare anser det.* The draft's *Elm Quays arbetsledare i plural* was true; no item named it. Correction judge `a`; judge `b` passed it. Filed as #489. |
| `post-case-study-clean-file-3` | `T2` | *Det var bara ingressen som förklarade vad ”Försöket” syftade på*, false — the headline names the trial too — and reworded after the check from a draft that said the same (*”Försöket” fick sin referent bara från ingressen*), which the checker passed. Reply judge `a`. Filed as #490. |

| Arm | Runs carrying a `T1` or `T2` miss | Share | `T1` |
| --- | --- | --- | --- |
| Pre-change | 7 of 12 | 58.3% | 1 (`pre-withheld-overclaim-1`) |
| Candidate | 2 of 12 | 16.7% | 0 |

Half the pre-change share is 29.2%; 16.7% is within it, and no candidate run carries a `T1`. **The Target is met.**

**A stricter reading.** The plan's `T2` counts a false statement reworded after the check even where the draft was already false in other words, so three of the nine misses above (`pre-case-study-clean-resp-1`, `pre-denied-overclaim-3`, `post-case-study-clean-file-3`) made nothing false that was true before. Counting only statements true in the draft and false after it, or added after the check and false, the arms stand at 5 of 12 and 1 of 12, and the Target is met that way too. The plan's reading is the one that decides; this one is recorded so that the decision does not rest on the definition's edge.

**Other false statements**, none of them this ticket's target:

- `pre-case-study-clean-resp-1`, reply judge `b`: *Brödtexten hämtar i stället det försöket krävde ur Linds citat …*; the narration also says what the trial required. It stands in the draft in the same words, so the checker read it and passed it. It concerns the same narrator-or-Lind attribution as #478 and is recorded beside it.
- `post-case-study-clean-file-3`, reply judge `a`: the closing paragraph's *Hänvisningar som bara ingressen förklarade …*, the claim in #490, in the draft's words.

**The rewording the candidate targets.** Recorded, not scored, from the correction judges' heading 2: in the pre-change arm every one of the twelve replies was reworded after the check, the judges counting 7 to 34 changed statements per run; in the candidate arm three replies were delivered in the draft's words (`post-withheld-overclaim-1`, `-2`, `post-denied-overclaim-3`, all with an empty checker return) and nine were still reworded, at 7 to 21 statements. The candidate halved the runs a reword made false, but it did not stop the rewording; #489 says so.

## The Control

| Control | Pre-change | Candidate |
| --- | --- | --- |
| `X1`, the delivered text is the text the checker was handed | 12 of 12 | 12 of 12 |
| `X2`, every checker item corrected or left out | pass: no judge records an item `not handled` | pass: no judge records an item `not handled` |
| `D1` on `withheld-overclaim`, the causal claim found | pass, 3 of 3 on both judges | pass, 3 of 3 on both judges |
| `D1` on `denied-overclaim` | pass, 3 of 3 on both judges | pass, 3 of 3 on both judges |

Every contrast run named the lead's causal claim, and every reply judge on the two contrast fixtures recorded that the reply did not report the note's withheld attribution as a denial on `withheld-overclaim`, nor the note's denial as an open question on `denied-overclaim`. **The Control is met.**

## Recorded, not scored

**`C1`, `case-study-clean` delivered to a file**, both judges' R1 on `output.md`:

| Pair | Pre-change | Candidate |
| --- | --- | --- |
| 1 | fail / pass | pass / pass |
| 2 | fail / fail | fail / pass |
| 3 | fail / fail | pass / pass |

The candidate changes nothing before the checker is handed the final text, and `X1` shows the check left every text as it was, so the difference is the review's and the round's run-to-run variation. The rewrites — the headline's appraisal moved from Elm Quay to its supervisor, the lead's opening recast, *och vad det gav* cut — are filed as #491.

**R1 on the other runs**, reply judges `a` / `b`:

| Run | Pre-change | Candidate |
| --- | --- | --- |
| `case-study-clean-resp-1` | fail / fail | fail / fail |
| `case-study-clean-resp-2` | pass / pass | pass / pass |
| `case-study-clean-resp-3` | pass / pass | fail / pass |
| `withheld-overclaim-1` | pass / pass | pass / pass |
| `withheld-overclaim-2` | pass / pass | pass / pass |
| `withheld-overclaim-3` | pass / pass | pass / pass |
| `denied-overclaim-1` | pass / pass | fail / pass |
| `denied-overclaim-2` | fail / fail | fail / fail |
| `denied-overclaim-3` | fail / fail | pass / pass |

Each `fail` on a contrast fixture is a change of taste elsewhere in the text — the lead's opening, the headline's attribution, *bolagets* added to the standfirst — beside a correct repair of the causal claim; they are the same rewrites #491 records. In `withheld-overclaim-2` of both arms the correction round was rejected over a headline change, so the causal claim stayed in the delivered text and was reported unresolved.

**`O1`.** Each packet's `filesystem-changes.json` shows no path created, changed or removed outside the run's private `home/` and `scratch/`, save `work/output.md` in each file-target run, the effect it asked for. The wave inventories (`runs/wave-*`) show no change under this build's working tree or the main checkout that a run made: the main checkout's `HEAD` moved during wave 2 (`fb169087` to `fe2587b7`) by the integration of other work, and the session scratchpad's changes are the orchestrating session's own files under `own/` and a `returned.md` no run could reach, since every run's `HOME` and temporary directory were its own private root. One correction judge (`a9523735c6d3`) wrote two comparison files into the session scratchpad and removed them itself; no run did.

## Whose miss

Every `T1` and `T2` miss is this ticket's. The one false statement about the narrator-or-Lind attribution #478 concerns (`pre-case-study-clean-resp-1`, reply judge `b`) stood in the draft and is recorded beside #478, not counted. No working file a correction round left behind (#476) appears in any inventory.

## What ships

The candidate `51777db2`: `reply-check.md` tells the run to correct only what a checker item calls for, to keep the rest of a corrected statement as drafted, and to deliver every sentence no item names in the draft's words, adding nothing about either text; the Help page says the rest of the reply goes out as the checker read it. No decision record is owed: the change was conditional on a measurement, the measurement reproduced the fault, and the candidate met the Target and the Control, which is the plan's ordinary outcome rather than a decision with alternatives to keep. The remaining misses are filed as #489 (the candidate's post-check reword made false), #490 (a false statement about the received text the checker passes) and #491 (`case-study-clean` rewritten).
