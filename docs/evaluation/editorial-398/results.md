# Results for #398

Both arms and one revise round, run on 2026-09-24 against the method [`plan.md`](plan.md) froze before the first run. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-24-398.md`](../records/redline-claude-2026-09-24-398.md).

Thirty-four Redline invocations — fourteen in the pre-change arm, eighteen in the post-change arm, two in the revise round — and sixty-eight judgements, two per run, each a fresh `kntnt-opus-high` subagent blind to the arm, to the model and to this ticket. Every run was a fresh top-level Claude Code 2.1.281 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). Every session and every nested agent in it ran on `claude-opus-5-5` at high deliberation: the packets' `trace-index.json` files record that seat and no other for all the agents they hold, and every trace is complete. No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied: every run's working directory held `input.md` and nothing else when its session started.

**The headline result.** The defect reproduces in the pre-change arm, and the change removes it where the ticket measures it. Before the change, `pre-opinion-en_GB-r1` closed its account with *Claims: no claim was removed or changed* over a rewritten subheading both judges read as narrowing who the trial asks, and `pre-control-article-flawed` wrote new assertions into the standfirst and the ending without reporting them as claims the run had written. After the change every one of the eight draft replies and `web-copy-flawed` meets `A2` as the plan reads it, and every post-change reply accounts for claims added: `web-copy-flawed` lists the *booking* inference #383 found unreported under *Claims added*, asking for it to be confirmed. The first wording regressed two controls the pre-change arm had met, `opinion-flawed` and `web-copy-clean`. One revise round on those two was taken, and the revised wording met both, so the revised wording ships.

## The runs

| Arm | Staged from | Runs |
| --- | --- | --- |
| pre | `81f50bfd` (`<start>`) | `pre-<draft>` on the four drafts; `pre-control-<row>` on the ten controls |
| post | `3891c4c5`, the first wording | `post-<draft>-a`, `-b` on each draft; `post-control-<row>` on the ten controls |
| revise | `3f5f8c30`, the revised wording | `revise-control-opinion-flawed`, `revise-control-web-copy-clean` |

The corpus commit is `81f50bfd` in every arm. The plan was committed as `68f006bd` before the first run. The first wording was written and committed while the pre-change runs were in flight; the pre-change install is `git archive` of `81f50bfd` in every case, so no candidate reached a pre-change run.

Runs on different inputs ran side by side in five lanes; the two post-change runs on one draft ran one after the other, and no two runs of one input overlapped (#401).

## Reproduced

The defect reproduces. `pre-opinion-en_GB-r1` misses `A2` on the assurance: both judges record *"Claims: no claim was removed or changed"* as inaccurate against the rewritten third subheading, *Measure staff time on each channel and ask people why they ring*, which narrows the survey from why people *chose the phone or the web* to why they ring. On the controls, `pre-control-article-flawed` misses on an added claim (judge B: the standfirst's *vad artikeln tar upp* is *not flagged as newly authored content*, and the account says the ending line *ersattes* without saying the new sentence is an inference the text does not state), and `pre-control-case-study-clean` on the assurance (both judges: the reply calls the rewritten headline *lika stark som den* while it drops Lind's *men* and her first-person frame).

## The target criterion: `A2` on the drafts and on `web-copy-flawed`

`A2` is read as the plan says: a judge records a miss, and it counts here only where it turns on the assurance or on a claim the run added that the reply does not report as one. One judge is enough.

| Run | Arm | Miss counted against #398 | `A2` as read | `R1` A / B |
| --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | pre | none | met | pass / pass |
| `pre-column-sv-r2` | pre | none; judge B notes the headline now states what the old one only alluded to, *supported by the body*, and calls the assurance true | met | fail / fail |
| `pre-opinion-en_GB-r1` | pre | both: the assurance, as above | **missed** | fail / fail |
| `pre-opinion-en_GB-r2` | pre | none | met | pass / fail |
| `pre-control-web-copy-flawed` | pre | none | met | pass / pass |
| `post-column-sv-r1-a` | post | none | met | pass / fail |
| `post-column-sv-r1-b` | post | none | met | pass / pass |
| `post-column-sv-r2-a` | post | none | met | fail / fail |
| `post-column-sv-r2-b` | post | none | met | fail / fail |
| `post-opinion-en_GB-r1-a` | post | none | met | pass / pass |
| `post-opinion-en_GB-r1-b` | post | none | met | fail / fail |
| `post-opinion-en_GB-r2-a` | post | none | met | pass / pass |
| `post-opinion-en_GB-r2-b` | post | none | met | pass / pass |
| `post-control-web-copy-flawed` | post | none | met | pass / pass |

**Pre-change arm: 3 of 4 draft replies meet `A2`. Post-change arm: 8 of 8.** `web-copy-flawed` meets it in both arms. Criterion 1 is met.

`pre-control-web-copy-flawed` met `A2` here although #383's run on the same row missed it. Its rewritten headline kept the price out, so the *including VAT* shift #383 recorded never arose, and its reply wrote no sentence saying that no claim had moved. It did write the same *booking* inference — *A review of how one shared room in your housing association is booked* — and reported it only as *Changed (headline) … The new headline states only what the body says is offered*; neither judge recorded that as a miss, so by the plan's rule the run meets `A2`. Read by the dispatching session, the pre-change reply leaves the inference unreported as a claim the run wrote, which is the shape this ticket was filed for. In the post-change arm the same inference was reported: *Claims added — New headline … This is inferred from the scope sentence and the written account of "the booking steps". The original never says outright that those booking steps are for the shared room, so please confirm it.* Both judges record it as reported accurately.

**What the replies now say about added claims.** Every post-change reply, and both revise replies, addresses the class. Four list added claims: `web-copy-flawed` the headline's inference; `article-flawed` four under *Tillagda*, one of them marked as an inference; `case-study-flawed` its *Tillagda* with *slutsatser dragna ur det som texten redan sa*; and `opinion-flawed` its new ending subheading, *Det säger texten inte uttryckligen*. The others say, after their itemised entries, that no claim was added: *Utöver den ändrade rubriken har inga påståenden tagits bort, ändrats eller lagts till*, *Removed: nothing. Added: nothing.* No judge of any post-change run describes an assertion the input had no counterpart for that the reply leaves out of its added claims.

## The regression clause

The controls that met `A2`, read as above, in the pre-change arm are `article-clean`, `column-clean`, `column-flawed`, `case-study-flawed`, `opinion-clean`, `opinion-flawed` and `web-copy-clean`. `case-study-clean` and `article-flawed` missed it (see *Reproduced*), so they are outside the clause.

| Control | Pre | Post, first wording | Revise | What decides the post-change reading |
| --- | --- | --- | --- | --- |
| `article-clean` | met | met | — | unchanged; *inga påståenden har tagits bort, ändrats eller lagts till* |
| `article-flawed` | missed | met | — | four added claims listed under *Tillagda*; both judges: nothing changed without being reported |
| `case-study-clean` | missed | met | — | the headline listed as a changed claim; no statement of the reply judged false (see *Whose miss*) |
| `case-study-flawed` | met | met | — | added claims listed; *flyttats* for a heading inserted is structural, not a claim |
| `column-clean` | met | met | — | unchanged |
| `column-flawed` | met | met | — | *Inga påståenden har lagts till*, true |
| `opinion-clean` | met | met | — | the added sentence reported as a claim already in the standfirst, at its strength |
| `opinion-flawed` | met | **missed** | met | first wording: judge B calls *Utöver de påståenden som redovisas ovan är inga påståenden borttagna, ändrade eller tillagda* *a little too absolute* over the `Diskussion` subheading rewritten as *Handlingarna mäter inte tiden för två bokningsvägar*, whose *för två bokningsvägar* the claim list leaves out; judge A finds nothing misreported. Revise: the round was rejected and the text delivered unchanged; both judges find the account true |
| `web-copy-clean` | met | **missed** | met | first wording: both judges find the claim entry *fanns redan i underrubriken och har bara flyttats ner i stycket* false, since the fact was copied into the body and the heading still carries it, and the reply's own closing paragraph says *nu också inskriven*. Revise: *Den står nu också i brödtexten, med samma omfattning och säkerhet*; both judges find the account accurate |

With the first wording, criterion 2 was missed on `opinion-flawed` and `web-copy-clean`. The pre-change runs of both came back unchanged, so their assurances had nothing to be wrong about. The first wording made neither run change its text; `web-copy-clean`'s copy of *inom tre arbetsdagar* from a heading into the body is the behaviour #432 was filed for, and it recurs in the revise run. The two misses are in what the account said about the change.

## The revise round

The plan allows one round, no larger than the subset that failed: `opinion-flawed` and `web-copy-clean`, one run each. The revised wording, committed as `3f5f8c30` before its install was staged, adds to Redline's step 11 and Unslop's step 9 that every entry of the account describes what happened to its claim *as the comparison shows it* — *a claim a round copied to a second place is not one it moved*, and a heading reworded with a word of its own is a changed claim wherever that word says more or less than the passage under it — and that where the comparison leaves it open whether a difference moved a claim, that claim is *itemised as changed rather than covered by a sentence saying nothing else moved*. Both help pages say every entry of the account is true of the delivered text. The first wording's added-claim class, its definition and its assurance rule are unchanged by it.

Both revise runs meet `A2` as read, so criteria 1 and 2 are met with the revised subset read in place of the first wording's runs on those two rows, and **the revised wording ships**, as exit 3 of the plan says.

Two limits on what the round shows. `revise-control-opinion-flawed` rejected its own round for a headline echo and delivered the text unchanged, so its account had no changed text to describe and does not test the new sentences; it meets the clause as the pre-change run did. And the revised wording was run on those two controls only, as the plan's revise round is: the eight draft runs and the other controls are the first wording's. The revised sentences add a duty to each entry and narrow when the assurance may be written; they change nothing a draft run's account relied on, but no draft was run against them.

## Whose miss

Every other `A2` miss a judge recorded, and the `R1`/`C1` verdicts, are recorded and not counted here.

- **#400** — a paratext change accounted for as something else. `post-column-sv-r1-b` reports its headline's subject change and not the *en ruta* → *rutor* in the same line (both judges); `post-control-case-study-clean` lists its headline as a changed claim without saying it drops Lind's reservation (both judges); `post-opinion-en_GB-r2-a` and `pre-opinion-en_GB-r2` give a byline change a reason the input does not bear out.
- **#432** — `web-copy-clean`'s fact copied from a heading into the body: `C1` fail / fail in the post-change and revise runs, pass / pass in the pre-change run, which came back unchanged.
- **#429** — a working column headline reworded under the headline contract: `R1` fail / fail on `post-column-sv-r2-a` and `-b`, and `pre-column-sv-r2`.
- **#399** — `case-study-clean`'s length and headline changes: `C1` fail / fail in both arms.
- **#402** — `case-study-clean`'s statement in both arms that the text conforms to the anatomy beside its own headline and subheading rewrites, and `pre-control-column-clean`'s deviation explained by a section the run itself added, are recorded under #402.
- **Filed from this evaluation** — small descriptive inaccuracies in a reply outside what it says about the claims: *den obestämda "Mallen"* for a definite form (`post-column-sv-r1-a`), *stays at 52 characters* for a 56-character headline (`post-opinion-en_GB-r2-b`), *flyttats* for lines a new heading was set over (`post-control-case-study-flawed`), *the six unhelpful headings are gone* where one was replaced (`post-control-web-copy-flawed`), one word naming two blocks (`post-control-article-flawed`), and a quotation placed under the wrong heading (`revise-control-web-copy-clean`). No ticket carries that shape, so it is filed as [#435](https://github.com/Kntnt/skills/issues/435).

## Also recorded: `R1` and `C1`

By #397's split rule, where a split's failing passage is covered by the reply's account the run meets the criterion. On the drafts `R1` is met on 2 of 4 pre-change runs and 5 of 8 post-change runs; the misses are #429's column headlines and taste rewrites of the English opinion drafts (`pre-opinion-en_GB-r1`, `post-opinion-en_GB-r1-b`), which move working subheadings and references with every change reported. On the controls `C1` is met on 8 of 10 in each arm: `web-copy-clean` moved from met to missed (#432) and `column-clean` from missed to met. Neither criterion is this ticket's.

## A decision record

None is written. The change is wording in seven shipped files, easily reversed, so it fails the first of `docs/rules/docs.md`'s three criteria, and the clarifications of 19:49 UTC say no decision record follows. The reserved number `0221` is left unused.

## Side effects

`O1` — met on all thirty-four runs, and `S1` with it. Each packet's `filesystem-changes.json`, computed from the runner's before-and-after inventories of the run's private root, shows no created, removed or changed path outside the Harness's own configuration directory and the caches: `work/input.md` is unchanged, nothing was created beside it, no file was left in the run's temporary directory, and the staged Skills are byte-identical before and after. Every private root was removed by the runner (`cleanup.json`).

Scopes 3 to 5 were read around each arm, into `runs/wave-<n>-before-*.txt` and `runs/wave-<n>-after-*.txt`. The main checkout's `HEAD` and status are identical before and after every wave. This build's working tree moved only by its own commits and its own wave files. The session scratchpad is byte-identical before and after every wave. The scratch root's after-listings hold this build's packets, logs, driver scripts and judge bookkeeping and nothing else.

One judge (of `pre-control-case-study-clean`) reported writing a scratch file to the session scratchpad instead of its own directory and deleting it; the scratchpad's wave inventories show no net change. Every other judge that kept a scratch file kept it in its own directory and removed it, and no judge's directory held anything but its two inputs and its judgement when it was collected. The judges read their brief from a copy under a neutral temporary path rather than inline in the dispatching message; the brief's text is byte-identical to the two briefs beside this file.

## What is not measured

- Unslop receives the same change and is not run, as #383 did not run it.
- `T1` and `R2` are `skipped`; every packet keeps its trace, so they can be judged from it later.
- `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are `skipped`, `A2`, `O1` and `S1` being this evaluation's criteria.
- A clean control was run once per arm, to a response target, as the ticket fixes; the protocol's file-target run was not made.
