# Results for #402

Both arms and one revise round, run on 2026-09-24 by the method [`plan.md`](plan.md) froze before the first run. Artefacts are in `runs/`. The record is [`../records/redline-claude-2026-09-24-402.md`](../records/redline-claude-2026-09-24-402.md).

There were twenty-one Redline invocations: ten in the pre-change arm, ten in the post-change arm and one in the revise round. They produced forty-two judgements, two per run. Each judge was a fresh `kntnt-opus-high` subagent, blind to the arm, the model and this ticket, and worked in a directory made by `mktemp -d` that named none of them. Every run was a fresh top-level Claude Code 2.1.281 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). Every session and every nested agent in it ran on `claude-opus-5-5` at high deliberation. The packets' `trace-index.json` files record that seat for all forty agents they hold, and every trace is complete. No Codex Harness and no GPT model was started, controlled or invoked. No run was void.

**The headline result.** The defect reproduces. Before the change, no finding says that `opinion-flawed`'s ending has no section of its own, and both judges record the ending clause as only partly met. After the change, every run on `opinion-flawed` reports it, in the post-change arm and in the revise round: *Den står dessutom i avsnittet som bär argumentationen, så texten saknar ett eget avslutande avsnitt*. All four judges record that half of the clause as met. Each of those runs also writes the repair: it gives the ending its own section, built from the body's actor and act. In both runs, though, the re-review rejects the whole round for an echo in a headline or another subheading the same round rewrote. So the delivered text still ends `Nu är det dags att agera.`, and no judge records the clause's second sentence, *Existing action/actor in body can repair the ending*, as met.

Criterion 1 is missed. Criterion 2 is met: no conforming control acquires an ending or section-count finding. Every post-change reply on an anatomy genre now says whether the text conforms, and says what it examined beyond the counted measures. Thomas's ruling ships whatever the measurement shows, so the first candidate's wording ships, and each miss is filed.

## What was built

- **`4b817d77`, the candidate.** `## Ending` of `article-anatomy.md` now states the requirement *The ending is a section of its own, opened by its own subheading, after at least one other section.* It also gives the test: the last section is the ending when its subheading and paragraphs close the piece and open no new line of argument, and a section that carries the argument with a closing line appended is not an ending.
  - `article-anatomy.review.md` now treats closing content inside a last section that carries the argument, or inside a text's only section, as a present ending that fails its rule. That ending is repaired by giving it a section of its own from the text's own content. A text with no section keeps its ending content where it stands, and the absent ending section is reported with the absent sections.
  - `article_anatomy.py` now fails a text of exactly one level-2 section, with part `sections`, the requirement sentence as its `rule` and `1 section` as `measured`.
  - Redline's step 6, its step 11 and its correction brief now say that exit 0 settles the counted requirements only. A reply or a return reports conformance to the anatomy only where every requirement the script does not count was examined.
- **`df6bb4a1`, the revised candidate.** It adds one sentence to the review half: the subheading written for such an ending describes its section in words of its own and does not repeat the paragraph under it.
- **`0d015bdc`.** It reverts `df6bb4a1`'s product change, because the revise round did not beat the first candidate (see *The exit*). The product that ships is `4b817d77`'s.

The pre-change arm was staged from `1ef14cb5` in every run. Its ten runs were dispatched before `4b817d77` was committed, and the candidate's wording was written while they ran. The post-change arm was staged from `4b817d77`, the revise round from `df6bb4a1`.

## Reproduced

`pre-control-opinion-flawed` leaves the ending clause unmet, so the defect reproduces. Finding 9 of its reply names the missing act and actor and the proposal in the body that could supply them. No finding says that the text has no ending section, or that the exhortation stands inside `Diskussion`. Judge A: *Partly met … No finding says that the text has no ending section of its own.* Judge B: *Partly met. Finding 9 reports the "naming no act" part.* The run's one round was rejected for a new source attribution and a headline that echoed the lead, so the text came back unchanged.

## The target criterion: `opinion-flawed`

| Run | Ending, first half: *no ending section … naming no act* (A / B) | Ending, second half: *existing action/actor … can repair the ending* (A / B) | Ending clause | `C1` A / B |
| --- | --- | --- | --- | --- |
| `pre-control-opinion-flawed` | partly / partly | detected, not applied / met as a finding, not applied | unmet | pass / pass |
| `post-control-opinion-flawed` | met / met | identified, not applied / recognised, no repair delivered | unmet | pass / pass |
| `revise-control-opinion-flawed` | met / met | detected, not repaired / not applied | unmet | pass / pass |

Every other clause of the row is met by both judges in all three runs: the motives, the population inference, the cost contradiction, the vague exhortation, the missing standfirst, the label subheadings, and the kept facts and proposal.

**Why the repair never reached the text.** Each run's correction subagent wrote the ending section, as its transcript under `runs/<run>/transcripts/subagents/` shows. Each round was rejected at Redline's step 7 for a defect that round created somewhere else:

- **Post-change.** The round wrote `## Kommunstyrelsen bör behålla båda kanalerna under försöket` over `Nu bör kommunstyrelsen behålla telefonbokningen under ett halvårs försök i alla sju lokaler.` Re-review found that subheading repeating its sentence. It also found the new headline, `Telefonbokningen bör behållas på prov i sex månader`, repeating the lead.
- **Revise round.** The round wrote `## Beslutet ligger hos kommunstyrelsen`, which repeats nothing, as the revised sentence asks. Re-review rejected the round for the rewritten first subheading, `## Telefonen stod för var femte bokning`, which repeated the start of its section.

The revised wording fixed the one echo it could reach, and the round was still lost to an echo in a heading this ticket does not govern. That is the behaviour #429 and #430 were filed against: headings the text had, rewritten on findings under the headline contract. Filed as [#433](https://github.com/Kntnt/skills/issues/433).

## Controls

`C1` is `R1` read against each row's frozen expectation, by the plan's split rule. No run split.

| Control | Pre A / B | Pre `C1` | Post A / B | Post `C1` | What the judgements record |
| --- | --- | --- | --- | --- | --- |
| `article-clean` | fail / fail | missed | fail / fail | missed | Pre: the headline rewritten as a comprehension defect, and `kort` struck from the standfirst. Post: the headline becomes `Björkskolans temperaturer bör läsas mot när rummen används` and the first subheading is rewritten. #430's behaviour in both arms. |
| `article-flawed` | pass / pass | met | pass / pass | met | The byline, sections and ending section are reported and not written in both arms. In neither arm is the 187-word lead named as an over-long lead. The late concept is named only in the pre-change arm, and only by judge A. |
| `case-study-clean` | fail / fail | missed | pass / pass | met | Pre: the headline and two subheadings rewritten, and the opening's sources moved. That is #399's behaviour. Post: the round was rejected and the text came back unchanged, with five findings left. |
| `case-study-flawed` | pass / pass | met | pass / pass | met | Pre: the byline and call to action reported and not written. Post: the same, and the closing section is built from the text's own content. |
| `column-clean` | pass / pass | met | fail / fail | **missed** | Post: the headline and the first subheading rewritten, and a standfirst verb changed. #430's behaviour. |
| `column-flawed` | pass / pass | met | pass / pass | met | The missing standfirst, sections and call to action are reported in both arms. Post also names the missing ending section. In neither arm does a finding say the old headline names no subject of its own. |
| `opinion-clean` | pass / pass | met | fail / fail | **missed** | In both arms the lead gains the standfirst's September (#431) and the body gains a sentence stating the assumption. Post: that sentence, `Att de räcker som underlag för att avskaffa telefonbokningen är ett antagande.`, and `kanaler` → `bokningsvägar` are what fail it. |
| `opinion-flawed` | pass / pass | met | pass / pass | met | See above. The ending clause is unmet in both arms. |
| `web-copy-clean` | pass / pass | met | fail / fail | **missed** | Post: `inom tre arbetsdagar` copied from a heading into the body, and a missing form link reported. #432's behaviour. |
| `web-copy-flawed` | pass / pass | met | pass / pass | met | Every clause met in both arms. |

**`C1`: 8 of 10 met before the change, 7 of 10 after.** `case-study-clean` moves from missed to met. `column-clean`, `opinion-clean` and `web-copy-clean` move from met to missed.

**Criterion 2, conforming controls: met.** No post-change reply on `article-clean`, `case-study-clean`, `column-clean` or `opinion-clean` has an ending finding or a section-count finding. Each reply says outright that its last section closes the piece:

- `article-clean`: *att sista avsnittet fungerar som avslutning*
- `case-study-clean`: *Avslutningen med uppmaning till handling håller*
- `column-clean`: *Sista avsnittet är ett avslut, med en uppmaning som följer av resonemanget*
- `opinion-clean`: *sista avsnittet är ett avslut med en uppmaning som riktar sig till kommunstyrelsen*

No pre-change reply on those four has such a finding either. The four clean controls still exit 0 on the script, and `tests/test_article_anatomy.py` checks that.

**Other findings the post-change runs have and the pre-change runs lack.** These are recorded and not counted:

- `article-clean` has a finding against the first subheading.
- `case-study-clean` has five findings, left unresolved, on the standfirst's *gruppen* and the second subheading among them. The judges call two of them over-detection on a conforming text.
- `column-clean` has headline, subheading and standfirst-verb findings.
- `opinion-clean` has *Två ord för samma sak* and *Antagandet sades aldrig ut*.

None of them is about the ending or the number of sections.

**What the three regressions are.** Each fails on a passage #402's change does not reach.

- `column-clean` is #430's behaviour: a headline the text had, rewritten on a headline-contract finding.
- `web-copy-clean` loads no anatomy, and its miss is #432's exactly. Its pre-change run passed where #397's two runs failed, which shows how much one run per arm varies on this row.
- `opinion-clean` fails on the stated-assumption sentence. The pre-change run added a sentence of the same kind and both of its judges passed it. The candidate touches no sentence about that finding, and one run per arm cannot separate the change from variance. Filed as [#434](https://github.com/Kntnt/skills/issues/434).

## What each reply says about conformance

| Run | What the reply says | True against the returned text |
| --- | --- | --- |
| every pre-change run | says nothing about conformance to the anatomy | — |
| `post-control-article-clean` | *Texten följer artikelns anatomi utan avvikelser*, naming what it read beyond the script | yes: its last section is an ending of its own |
| `post-control-case-study-clean` | the counted limits hold, two uncounted requirements deviate, and the ending holds | yes, as a statement of what it examined |
| `post-control-column-clean` | *Texten följer anatomin*, listing the uncounted requirements it read | yes |
| `post-control-opinion-clean` | *Texten uppfyller artikelanatomin*, listing the uncounted requirements it read | yes |
| `post-control-article-flawed` | *texten följer den inte*, since the byline, sections and ending section are absent | yes |
| `post-control-case-study-flawed` | *följer alltså inte artikelanatomin fullt ut*, and *avslutningen är ett eget avsnitt* | yes: the run built that section |
| `post-control-column-flawed` | *Texten följer alltså inte artikelanatomin. Jag gick igenom alla anatomikrav, även de som mätskriptet inte räknar.* | yes |
| `post-control-opinion-flawed` | *Texten följer inte artikelanatomin … avslutningen är inte ett eget avsnitt … Alla anatomikrav har granskats, även de som skriptet inte räknar.* | yes |
| `revise-control-opinion-flawed` | *Texten följer inte artikelanatomin … Avslutningen står inte som ett eget avsnitt* | yes |

#383's reply said *texten uppfyller anatomins krav utan avvikelser* of a text whose ending stood inside the argument. No post-change reply says anything like that of such a text.

## Whose miss

- `article-clean` in both arms and `column-clean` after the change are [#430](https://github.com/Kntnt/skills/issues/430)'s behaviour: a working headline and subheading rewritten under the headline contract.
- `case-study-clean` before the change is [#399](https://github.com/Kntnt/skills/issues/399)'s.
- `web-copy-clean` after the change is [#432](https://github.com/Kntnt/skills/issues/432)'s.
- `opinion-clean`'s September clause, in both arms, is [#431](https://github.com/Kntnt/skills/issues/431)'s. The added assumption sentence that fails it after the change is filed as [#434](https://github.com/Kntnt/skills/issues/434).
- `opinion-flawed`'s ending clause left unmet after the change is counted against this ticket and filed as [#433](https://github.com/Kntnt/skills/issues/433). Its cause is the whole-round rejection, triggered by a heading echo that belongs to #429 and #430.

## The exit

The first candidate meets criterion 2 and misses criterion 1.

**One revise round was taken**, on the one control that missed: `opinion-flawed`. The revised sentence targeted the echo that got the post-change round rejected. Its round did write an ending subheading that repeats nothing, but it was rejected for an echo in the first subheading. Both judges again record the repair as not applied, so the revised candidate misses criterion 1 just as the first did. It does not beat the first candidate, so by the plan the first candidate's wording ships. `0d015bdc` reverts the revised sentence and its test.

**What ships.** Thomas's ruling ships whatever the measurement shows. The anatomy requires an ending section of its own and says what makes a last section an ending. The review half repairs a closing passage inside the argument by giving it that section. The script counts at least two sections. Redline reports conformance only where the uncounted requirements were examined.

**A decision record.** None is written, as the clarifications of 19:50 UTC say, and ADR-0209's boundary is unchanged. The reserved number `0222` is left unused.

## Side effects

**`S1`** is met on all twenty-one runs. **`O1`** is met on twenty and missed on one, `pre-control-article-clean`, in the pre-change arm. That run's correction subagent wrote `scratch/cand.md` in the run's private scratch and left it there. Redline's step 11 requires removing every scratch file a response-target run created. The runner removed the private root afterwards. The run is not in the post-change arm or the target, and nothing in this ticket touches that step. No other packet's `filesystem-changes.json` shows a created, removed or changed path outside the Harness's own configuration directory and the caches: every `work/input.md` is unchanged, nothing was created beside it, and the staged Skills are unchanged. Every private root was removed (`cleanup.json`).

Scopes 3 to 5 were read around each of the five waves into `runs/wave-<n>-*.txt`:

- **Scope 3, the scratch root.** It changed only by this build's own packets, logs, judge records and expectation files.
- **Scope 4, the main checkout.** Its `HEAD` moved from `1ef14cb5` to `a24e70a3` during wave 5, which is the run integrating other tickets and not a Redline run. This build's working tree changed only by its own commits and edits.
- **Scope 5, the session scratchpad.** It changed once, in wave 4: `agentdone.py` was rewritten and `briefs/verify-401-build.md` appeared. Both belong to the session orchestrating the sibling build, not to any run.

Every judge's directory held its two inputs and its judgement and nothing else when collected, and each was removed afterwards.

## What is not measured

- **Write.** Write loads `article-anatomy.md`, so the two-section minimum and the ending test now bind its drafts and what its step 7 repairs. No Write run was made. That change goes unmeasured here.
- **Unslop.** It loads no anatomy and is out of scope.
- **The four #362 drafts** were not run, as the clarifications cut the measurement to the ten controls.
- **A clean control** was run once per arm, to a response target. The protocol's file-target run was not made.
- **`T1` and `R2`** are `skipped`. Every packet keeps its trace.
- **`A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2`** are `skipped`.

## What was filed

- [#433](https://github.com/Kntnt/skills/issues/433): `opinion-flawed`'s ending section is written and then lost when a heading echo gets the whole round rejected. This is criterion 1, missed after the change and after the revise round.
- [#434](https://github.com/Kntnt/skills/issues/434): `opinion-clean` gains a sentence stating its unstated assumption, and misses `C1` after the change where it met it before.
