# Results for #397

Both arms, run on 2026-09-24 against the method [`plan.md`](plan.md) froze before the first run, as [`plan-amendment.md`](plan-amendment.md) amends how a run is made. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-24-397.md`](../records/redline-claude-2026-09-24-397.md).

Thirty-two Redline invocations — fourteen in the pre-change arm, eighteen in the post-change arm — and sixty-four judgements, two per run, each a fresh `kntnt-opus-high` subagent blind to the arm, to the model and to this ticket. Every run was a fresh top-level Claude Code 2.1.281 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py); every session and every nested agent in it ran on `claude-opus-5-5` at high deliberation, which the packets' `trace-index.json` files record for all sixty-three agents they hold across the thirty-two runs, every trace complete. No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied: every run's working directory held `input.md` and nothing else when its session started.

**The headline result.** The defect reproduces in every pre-change run on the four #362 drafts, and the change removes it: in the post-change arm no run wrote a standfirst, a subheading, an ending or a call to action into a draft that lacked one, and every one of the eight replies reports the absent parts as findings left for a person to fill. `R1` is met on six of the eight post-change draft runs against none of the four pre-change ones. The two that miss are the second run on each column draft, and both miss on the same thing: a working headline reworded under the headline contract, which both judges class as taste. Three clean controls that came back unchanged or passed in the pre-change arm — `article-clean`, `case-study-clean` and `column-clean` — each had a headline or subheading rewritten in the post-change arm, one run per arm. Thomas's ruling ships whatever the measurement shows, so the candidate ships; every miss is recorded here as measured and filed.

## Before the first valid run

**The corpus rows.** `a321690f` revised the three clauses the readiness addenda name — `article-flawed`'s navigation, `column-flawed`'s standfirst and `column-flawed`'s call to action — and nothing else in the file. Both arms were judged against those rows.

**The eight voided runs.** The plan made each run a subagent of this build's session. That session is itself a subagent, and a subagent of a subagent has no tool for starting a third, so seven of the first eight Redline runs stopped at step 1 on the `subagents` Capability and the eighth, `pre-control-article-clean`, returned the no-change status in a Harness lacking it. None of the eight is a run of the method. They are kept under [`voided/subagent-runs/`](voided/subagent-runs/), and [`plan-amendment.md`](plan-amendment.md), committed before the first valid run, makes every run a fresh top-level session on the same seat through the protocol's Claude-family runner, as #396's build did in the same unattended run. The readiness addendum reserves that runner for criteria answered from a trace; it was used here because it is the one way from this seat to give Redline a session that can start its correction subagents. That is a departure from the addendum's letter, stated here so that it can be reviewed.

**The order of work.** The candidate's wording was written into the working tree while the pre-change runs were in flight and before any of them had been judged, and committed as `d1be1731` after all four draft runs and nine of the ten controls had been judged. The tenth, `pre-control-case-study-clean`, waited on the shared `case-study-clean` lock the sibling build held and ran last, at 03:10, after `post-control-case-study-clean` had released it. The pre-change install is `git archive` of `20133068` in every case, so the candidate's commit reached no pre-change run.

## Reproduced

The defect reproduces: every pre-change run on the four drafts wrote a part its input did not have, and both judges of every one fail `R1` on it.

| Run | What the run wrote into the draft | `R1` A / B |
| --- | --- | --- |
| `pre-column-sv-r1` | a third-person standfirst about the bylined author, three subheadings, and a closing call to action in her voice after her ending (`Pröva gärna själv nästa gång du fyller i en mötesmall …`) | fail / fail |
| `pre-column-sv-r2` | a standfirst, two subheadings, and a closing call to action inside her last paragraph (`Prova gärna att ställa den själv nästa gång du kallar till ett möte …`) | fail / fail |
| `pre-opinion-en_GB-r1` | a new lead paragraph after the byline it moved, the headline reworded to fit the band, two paragraphs split | fail / fail |
| `pre-opinion-en_GB-r2` | a standfirst above the byline, the headline reworded to fit the band, which moved its claim from *until Lervik knows why* to *through a six-month trial* | fail / fail |

Both judges of `pre-column-sv-r1` and of `pre-column-sv-r2` record the added call to action as a change to what a claim says by scope: the writer's own tentative trial becomes advice to the reader. Both judges of `pre-opinion-en_GB-r2` record the headline's move as a change of chronology.

## The target criterion: `R1` on the four drafts

| Run | Arm | What differs from the input | `R1` A / B | Met |
| --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | pre | as above | fail / fail | no |
| `pre-column-sv-r2` | pre | as above | fail / fail | no |
| `pre-opinion-en_GB-r1` | pre | as above | fail / fail | no |
| `pre-opinion-en_GB-r2` | pre | as above | fail / fail | no |
| `post-column-sv-r1-a` | post | the dash, set as a Swedish en dash by the mechanical pass; standfirst, sections and call to action reported absent and left unwritten | pass / pass | yes |
| `post-column-sv-r1-b` | post | the headline `Mallen har en ruta för allt utom poängen` → `Bibliotekets mötesmall har rutor för allt utom poängen`, on a finding that it is not understood on its own; the dash | fail / fail | no |
| `post-column-sv-r2-a` | post | the dash; a headline rewrite attempted and rejected by the run's own re-review; absent parts reported | pass / pass | yes |
| `post-column-sv-r2-b` | post | the headline `Rutan som inte finns` → `Bibliotekets mötesmall har ingen ruta för mötets syfte`; the dash | fail / fail | no |
| `post-opinion-en_GB-r1-a` | post | the closing sign-off moved into place as the byline; `Lervik` added to the lead; the third subheading reworded for repeating the sentence under it | pass / pass | yes |
| `post-opinion-en_GB-r1-b` | post | as `-a`, and two long paragraphs each split in two | pass / fail | yes, by the split rule |
| `post-opinion-en_GB-r2-a` | post | `By` added to the byline; *both routes, web and telephone* in the lead; *It* → *The executive board* | pass / pass | yes |
| `post-opinion-en_GB-r2-b` | post | `By` added; the headline's *the telephone* → *telephone booking*; *It* → *The board* | pass / pass | yes |

**Pre-change arm: 0 of 4 met. Post-change arm: 6 of 8 met.** The candidate beats the pre-change arm on the target criterion.

**The split.** In `post-opinion-en_GB-r1-b` judge B fails the run on the reworded subheading and on the two paragraph splits, which it reads as made for length alone. Both are covered in the reply's closing summary — *The long single paragraphs in "What the pilot actually counted" and "A motive on the table…" are each split in two where the evidence ends and the argument begins, with no wording changed. The subheading "Six months, both routes, and something to measure" repeated the sentence under it, and now reads …* — so by the plan's rule the run meets `R1`, and both readings are recorded. The reply grounds the splits in where the evidence ends and the argument begins rather than in the count; whether that is a second thought or a split to reach the band is exactly where the two judges part.

**What changed between the arms.** No post-change run wrote a standfirst, a subheading, an ending or a call to action into a draft that lacked one; the section count of every draft is the same after as before; and every post-change reply lists the absent standfirst, and for the columns the absent sections and call to action, as findings left for a person — *Vid en granskning skrivs sådana delar inte, så det är du som avgör vad de ska innehålla*, *You need to write it, so I left it out*. `post-column-sv-r1-a` reports the seven-paragraph lead as caused by the absent sections, which is point 5 of the rule, in its own words: *Den räknas därför som ett lead på sju stycken, men det felet beror bara på att avsnitten saknas.* The byline standing at the end of `opinion-en_GB-r1` was moved into place in both post-change runs, point 3. No headline was reworded to reach a band in any post-change run, and `post-opinion-en_GB-r2-a` says so of its own ten-word headline in the words of point 7: *The headline is ten words, above the usual three to eight, but it meets the headline requirements, so it stays as it is.*

**The two misses.** Both are the second run on a column draft, and both rewrite a headline the text had, on a finding under the headline contract: *Rubriken förstods inte fristående* for `Mallen har en ruta för allt utom poängen`, and *Rubriken var otydlig* for `Rutan som inte finns`. `headlines.review.md` lists vague wording that needs the text to be understood as a finding in its *Avoid* list. Both judges of each run class the rewrite as taste on a working headline, and both judges of `post-column-sv-r2-b` record the new headline's *syfte* as a change of meaning against the body's *beslut*. `post-column-sv-r1-b` also turned `en ruta` into `rutor` without reporting it, which breaks the column's recurring *en ruta*. This is not the band rewrite point 7 governs, and it is not a part the text lacked. `headlines.md` and `headlines.review.md` are outside this ticket by the readiness addendum, so no wording this ticket may change reaches it. Filed as [#429](https://github.com/Kntnt/skills/issues/429).

## Controls

`C1` is `R1` against each row's frozen expectation, read by the same split rule.

| Control | Pre A / B | Pre `C1` | Post A / B | Post `C1` | What the post-change judgements record |
| --- | --- | --- | --- | --- | --- |
| `article-clean` | pass / pass | met | fail / fail | **missed** | headline `… visar när, inte varför` → `Björkskolans givare visar ibland kall luft, inte orsaken`, the first subheading replaced, `kort` struck from the standfirst. The pre-change run attempted the same headline and subheading and its own re-review rejected the round. |
| `article-flawed` | pass / pass | met | pass / pass | met | byline reported and left unfilled; the missing subheadings and ending reported and not written; the duplicate standfirst repaired; the sales line replaced from the text's own content. The pre-change run's only round was rejected, so it delivered the input unchanged with fourteen findings. |
| `case-study-clean` | pass / pass | met | fail / fail | **missed** | headline, last subheading and standfirst rewritten on five findings. The pre-change run raised six and its re-review rejected the round. |
| `case-study-flawed` | pass / pass | met | pass / pass | met | missing byline and missing call to action reported, neither written; both subheadings replaced, their defect named only generally |
| `column-clean` | pass / pass | met | fail / fail | **missed** | the headline's hyperbole `en ruta för allt utom varför` read as an overclaim and replaced |
| `column-flawed` | fail / fail | missed | pass / pass | met | standfirst and call to action reported and not written; the pre-change run wrote a 46-word standfirst and did not report the missing call to action |
| `opinion-clean` | pass / fail | met, split | fail / pass | met, split | in both arms the lead gains the standfirst's *september* clause, covered in both replies' closing summary |
| `opinion-flawed` | pass / pass | met | pass / pass | met | ending repaired from the body's own actor and act; `Bakgrund` and `Diskussion` replaced; the missing ending section still unreported (#402) |
| `web-copy-clean` | fail / fail | missed | fail / fail | missed | in both arms *inom tre arbetsdagar* copied from a heading into the body, and a missing form link reported as a defect |
| `web-copy-flawed` | pass / pass | met | pass / pass | met | every clause met in both arms |

**`C1`: 8 of 10 met before the change, 6 of 10 after.** `column-flawed` moves from missed to met, on exactly the clause this ticket revised. `article-clean`, `case-study-clean` and `column-clean` move from met to missed.

**Clean controls come back unchanged.** Not met. `article-clean` and `column-clean` came back unchanged in the pre-change arm and changed in the post-change arm; `opinion-clean` changed in both, on the same clause. No difference in any of the three, in either arm, is a mechanical correction.

**Reported rather than invented.** Met. In the post-change arm `article-flawed`'s reply says *Byline saknas. Texten, anropet och eventuell metadata namnger ingen författare. En person behöver fylla i den.* and delivers no byline, and `case-study-flawed`'s says *Uppmaning till handling saknas. Avslutningen har ingen uppmaning, och texten innehåller inga erbjudanden, länkar eller kontaktvägar att bygga en på.* and delivers none. Both controls meet `C1`, on both judgements.

**What the three regressions are and are not.** Each is a headline or a subheading the text had, rewritten on a finding under the headline contract, and in each the judges read the finding as taste. None is a part the text lacked and none is a band. In `article-clean` and `case-study-clean` the pre-change run raised the same kind of findings and attempted the same kind of rewrite, and its own re-review rejected the round; in the post-change runs the re-review passed it. One run per arm cannot separate that from a caused regression, and the candidate changes no sentence about headline findings, about a round's re-review or about what a working headline is — the only step 7 sentence it touches now says *a part the round changed … that said something else before the round, or stood somewhere else*, which still names a reworded headline as where a repair-created defect is looked for. Recorded as measured, and filed.

## Whose miss

- `case-study-clean` missing `C1` in the post-change arm on rewritten headings is the behaviour [#399](https://github.com/Kntnt/skills/issues/399) was filed against — case-study-clean missing `C1` on a rewritten subheading in one arm and passing in the other — and is recorded under #399 rather than counted against this ticket. It is named here because #399 is not in the readiness addendum's list; the addendum's general rule, *a miss caused by a behaviour another ticket was filed against is recorded under that ticket's number*, is what places it.
- `opinion-flawed`'s missing ending section, left unreported in both arms while the reply says the counted requirements hold, is [#402](https://github.com/Kntnt/skills/issues/402)'s, as #383 found.
- `case-study-flawed`'s and `article-flawed`'s subheadings or standfirst replaced with the defect named only generally are [#400](https://github.com/Kntnt/skills/issues/400)'s shape; no criterion here turns on them.
- Every other miss above is recorded against this ticket's criteria and filed.

## The exit

The candidate meets the third criterion and misses the first two: `R1` is not met on every draft run, and two clean controls did not come back unchanged.

**No revise round was taken.** The plan allows at most one, no larger than the subset that failed. Every miss in that subset — the two column headlines and the three clean controls — is a headline or subheading the text had, rewritten on a finding under `headlines.md` and `headlines.review.md`, which the readiness addendum keeps out of this ticket. A revised wording within this ticket's files could only restate what `headlines.review.md` already says (*A working headline is left alone*) or add a threshold for headline findings nobody has specified. The first would re-measure the same wording; the second would be a requirement guessed in Thomas's absence. So the round was not spent, and that choice is recorded here for review.

**What ships.** Item 4 of the readiness addendum's common clause would keep the product as it was, since the candidate beats the pre-change arm on the target criterion but three controls that passed before fail after. Its section *Items 3 and 4 do not undo Thomas's ruling*, confirmed by the clarifications of 19:50 UTC, overrides that: the ruling ships whatever the measurement shows, and the measurement decides only which wording ships and what is written down. One wording was tried, so the candidate at `d1be1731` ships.

**A decision record.** None is written. The change is wording in four editorial files and is easily reversed, so it fails the first of `docs/rules/docs.md`'s three criteria, and the clarifications of 19:50 UTC say that no decision record follows. The reserved number `0221` is left unused.

## Side effects

`O1` — met on all thirty-two runs, and `S1` with it. Each packet's `filesystem-changes.json`, computed from the runner's before-and-after inventories of the run's private root, shows no created, removed or changed path outside the Harness's own configuration directory and the caches: `work/input.md` is unchanged, no file was created beside it, no file was left in the run's temporary directory, and the staged Skills are byte-identical before and after. Every private root was removed by the runner (`cleanup.json`).

Scopes 3 to 5 were read once around the whole of both arms, into `runs/wave-1-before-*.txt` and `runs/wave-1-after-*.txt`. The main checkout's `HEAD` and status are identical before and after. This build's working tree moved from `26a0e23d` to `d1be1731` by its own commits and shows nothing else. The session scratchpad is byte-identical before and after: neither this build's runs nor, as far as that directory shows, the sibling's wrote anything there, so there was no file of the sibling's to attribute. The scratch root's after-listing holds this build's packets, its judges' directories, its logs and its evaluator scripts; the pytest files a gate run left under its `tmp/` and uv's lock files were removed before the after-listing was taken, and are this build's own.

Two judges reported writing and then deleting a scratch file of their own inside their own directory, and no judge's directory held anything but its two inputs and its judgement when it was collected. None reported a file changed under it.

## What is not measured

- Unslop loads no anatomy and is out of scope; Write loads `article-anatomy.md`, whose one new sentence is worded not to bind it, and no Write run was made.
- `T1` and `R2` are `skipped`; every packet keeps its trace, so they can be judged from it later.
- `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are `skipped`, `R1`, `C1`, `O1` and `S1` being this evaluation's criteria.
- A clean control was run once per arm, to a response target, as the ticket fixes; the protocol's file-target run was not made.

## What was filed

Each remaining miss is filed as its own `needs-triage` issue naming #397; the record's *defects filed* fields map each run to the issue that carries it.

- [#429](https://github.com/Kntnt/skills/issues/429) — the second run on each column draft misses `R1` on a working headline reworded under the headline contract.
- [#430](https://github.com/Kntnt/skills/issues/430) — `article-clean` and `column-clean` pass `C1` and come back unchanged before the change, and miss both after, each on a rewritten headline, one run per arm. `case-study-clean`'s move the same way is recorded under [#399](https://github.com/Kntnt/skills/issues/399).
- [#431](https://github.com/Kntnt/skills/issues/431) — `opinion-clean` comes back changed in both arms: the lead gains the standfirst's *september* clause under the review extension's rule for a body that leans on its standfirst.
- [#432](https://github.com/Kntnt/skills/issues/432) — `web-copy-clean` misses `C1` in both arms, on a fact copied from a heading into the body and a missing form link reported as a defect.
