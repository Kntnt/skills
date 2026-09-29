# Results for #432

Both arms were run on 2026-09-29 (UTC), under the method [`plan.md`](plan.md) froze before the first run. The plan is commit `8575d6d2`. Artefacts are under `runs/`. The record is [`../records/redline-claude-2026-09-29-432.md`](../records/redline-claude-2026-09-29-432.md).

The eighteen staged runs are nine per arm: eight Redline runs and one Write run. There are thirty-two judgements, two for each Redline run. Each judge was a fresh `kntnt-opus-high` subagent, blind to the arm, to the model and to this ticket. Every run was a fresh top-level Claude Code 2.1.285 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). Every session and every nested agent in it ran on `claude-opus-5-5` at high deliberation. The packets' `trace-index.json` files record that for all thirty agents across the eighteen runs, and every trace is complete. No Codex Harness and no GPT model was started, controlled or invoked. Every run's working directory held its one input and nothing else when its session started.

- **The pre-change arm** was staged from `e7773344`, the branch head when the build began.
- **The candidate arm** was staged from `a1453560`, which carries the candidate.
- **The corpus commit** is `e7773344`.

**The headline result.** The fault reproduces in all six pre-change runs of `web-copy-clean`. In every one of them, the reply reports the page's form as missing and asks for a link or a location. The delivered text copies `inom tre arbetsdagar` from the subheading into the sentence under it. Both judges of every one of those runs fail `C1`. In the candidate arm no run does either. All six return the page unchanged, and both judges of every one pass `C1`. Two of the file-target replies say, in their own words, why the two things are not findings: *Rubriken Svar inom tre arbetsdagar anger en tid som brödtexten inte behöver upprepa* and *Formuläret nämns utan gränssnittsmarkering, och det räknas inte som ett fynd.* Both controls meet their readings in both arms, so nothing regressed. The candidate ships, and no revise round was taken.

## The candidate

`a1453560` changes two review halves and no base half:

- **`genres/webcopy.review.md`.** The sentence *a reference to a form here needs an included or explicitly specified form, not just its link* is replaced. A reference to a form, button or link is now a finding only where the copy places or describes it differently from what the artifact shows. Three cases stay findings: *the form below* where the artifact holds only a link, which is #345's case; a link labelled as something it does not do, as *Book now* over an expression-of-interest form that books nothing; and an action the copy promises and the page contradicts. Copy that names the page's own form, where the artifact carries no interface markup at all, is not a finding. *Enter each section cold* now reads *Enter each section cold, reading its heading with it*.
- **`base.review.md`.** Beside *Cover the paratext to find unresolved references in the body*, it says that a heading may carry a fact that the section under it does not repeat. It then names what is a finding instead: a body that needs the heading to be understood, through a pronoun, a definite form or an ellipsis that only the heading completes. Such a body is repaired by naming the referent where the body first needs it.

`genres/webcopy.md`, `base.md` and every other file Write loads are byte-identical to `e7773344`. `tests/test_webcopy_review_limits.py` holds both limits in place. The catalog was regenerated in the same commit.

## Before the first valid run

**One run cut off by the evaluator.** The first launch of the run streams hit a fault in the evaluator's own launcher script, which read an unset array under Bash 3.2. So the `web-copy-clean` stream skipped its first response-target run, and it started `pre-web-copy-clean-file-1` out of the plan's order. The run was stopped after sixteen seconds, with `SIGINT` to the runner, which ended its process group and removed its private root. The launch never started the other streams' runs. The cut-off packet is kept under [`voided/launcher-order/`](voided/launcher-order/) and is not counted. The launcher was fixed, and the wave-1 before-inventory was taken again. All three streams were then started from their first run. No valid run was made before the plan's commit.

## Reproduced

The fault reproduces. Every pre-change run of `web-copy-clean` carries both target misses.

| Run | The form reported as missing (the reply) | The heading's fact copied (the delivered text) | `C1` A / B |
| --- | --- | --- | --- |
| `pre-web-copy-clean-response-1` | *Olöst … Sidan innehåller dock inte formuläret, länkar inte till det och säger inte var det finns. … Någon som vet var det finns behöver lägga in formuläret eller en länk* | *Svale svarar via e-post inom tre arbetsdagar för att stämma av uppdraget* | fail / fail |
| `pre-web-copy-clean-file-1` | *Olöst. … Formuläret finns inte i texten, och texten säger inte var det finns eller hur läsaren når det. … Någon behöver ange var formuläret finns, till exempel med en länk* | `output.md`: *Svale svarar via e-post inom tre arbetsdagar för att stämma av uppdraget* | fail / fail |
| `pre-web-copy-clean-response-2` | *Kvarstår: formuläret har ingen angiven plats. … Sidan innehåller inte formuläret och säger inte heller var det finns eller hur läsaren når det.* | *Svale svarar via e-post inom tre arbetsdagar för att stämma av uppdraget* | fail / fail |
| `pre-web-copy-clean-file-2` | *Olöst. … texten säger inte var det finns. … För att åtgärda det behövs ett faktum som texten saknar, nämligen var formuläret finns* | `output.md`: *Svale svarar via e-post inom tre arbetsdagar för att stämma av uppdraget* | fail / fail |
| `pre-web-copy-clean-response-3` | *Olöst: formuläret anges inte. … Den som ansvarar för sidan behöver ange var formuläret finns eller länka till det.* | *Svale svarar via e-post inom tre arbetsdagar för att stämma av uppdraget* | fail / fail |
| `pre-web-copy-clean-file-3` | *Olöst: texten innehåller inte formuläret och säger inte heller var det finns … Någon som vet måste lägga till en länk* | `output.md`: *Svale svarar på intresseanmälan via e-post inom tre arbetsdagar* | fail / fail |

Every one of the six gives the same reason for the copy: the reply time stood only in the subheading, so a reader of the body alone did not learn it. `pre-web-copy-clean-file-3` also wrote *formuläret för intresseanmälan* in both places the page says *formuläret*. The run reported that as a partial repair of the form finding. Both of its judges count it with the copied reply time as a change of taste.

## The target

| Run | Arm | Target reading, with the passage that decides it | `C1` A / B | `C1` met |
| --- | --- | --- | --- | --- |
| `pre-web-copy-clean-response-1` | pre | miss: both, as above | fail / fail | no |
| `pre-web-copy-clean-file-1` | pre | miss: both, as above | fail / fail | no |
| `pre-web-copy-clean-response-2` | pre | miss: both, as above | fail / fail | no |
| `pre-web-copy-clean-file-2` | pre | miss: both, as above | fail / fail | no |
| `pre-web-copy-clean-response-3` | pre | miss: both, as above | fail / fail | no |
| `pre-web-copy-clean-file-3` | pre | miss: both, as above | fail / fail | no |
| `post-web-copy-clean-response-1` | post | none: *Ingen ändring behövdes. … Granskningen gav inga anmärkningar* — no text delivered, and no finding | pass / pass | `skipped` in the record: a no-change status |
| `post-web-copy-clean-file-1` | post | none: `output.md` is byte-identical to `input.md`; *Rubriken bär tidsgränsen, och det är tillåtet.* | pass / pass | yes |
| `post-web-copy-clean-response-2` | post | none: *Ingen ändring behövdes. Texten följer redaktionella regler för webbtext* — no text delivered, and no finding | pass / pass | `skipped` in the record: a no-change status |
| `post-web-copy-clean-file-2` | post | none: `output.md` is byte-identical to `input.md`; *Rubriken Svar inom tre arbetsdagar anger en tid som brödtexten inte behöver upprepa. Formuläret nämns utan gränssnittsmarkering, och det räknas inte som ett fynd.* | pass / pass | yes |
| `post-web-copy-clean-response-3` | post | none: *Ingen ändring behövdes. … Granskningen gav inga anmärkningar* — no text delivered, and no finding | pass / pass | `skipped` in the record: a no-change status |
| `post-web-copy-clean-file-3` | post | none: `output.md` is byte-identical to `input.md`; *Svarstiden på tre arbetsdagar står bara i underrubriken, och det räcker eftersom brödtexten går att förstå utan den. ”Formuläret” är inget fynd, eftersom sidan inte innehåller några gränssnittselement.* | pass / pass | yes |

**Target met.** No candidate run carries a target miss: 0 of 6, against 6 of 6 before the change. Each of the three file-target runs delivered `output.md` byte-identical to its input, and those are what answer the criterion that a clean text comes back unchanged. The three response-target runs returned the short no-change status and nothing else. As the protocol and the plan say, their `C1` is `skipped` in the record, because no text was delivered and the file-target entry answers the criterion. Both of their judges pass them.

## The controls

| Control | Arm | Reading | `C1` or `R1` A / B | Met |
| --- | --- | --- | --- | --- |
| `web-copy-flawed` | pre | `C1` met; both judges' heading 3 records the reply's finding 5, *Link text "Book and pay now": it contradicted what the link does* | pass / pass | yes |
| `web-copy-flawed` | post | `C1` met; both judges' heading 3 records the reply's point 3, *"Book and pay now" promised a booking and a payment. The page's last section says the link does neither* | pass / pass | yes |
| `web-copy-sv`, Redline half | pre | `R1` met; the draft came back with the no-change status, and both judges find no visible defect left unreported | pass / pass | yes |
| `web-copy-sv`, Redline half | post | `R1` met; as in the pre-change arm | pass / pass | yes |

**`web-copy-flawed`** meets its row in both arms. In both, the misleading link is relabelled *Open the expression-of-interest form*, as its last section says it is. The link label is the case of a link labelled as something it does not do, which stays a finding. The price, scope, timing, deliverables, conditions and destination are kept. The six opaque sections are regrouped from the page's own content, into two sections before the change and three after. Both replies report one added claim, that Svale provides the review, inferred from the page's last sentence. The pre-change run also turned *working days* into *business days* under its own finding 6, which both of its judges read as a locale form. The candidate run kept *working days*.

**`web-copy-sv`.** Each arm's Write run delivered a Swedish service page with its `kntnt` map. The two drafts differ, since Write is not deterministic. Each draft is kept as `draft.md` in its Write packet and is byte-identical to the `supplied-input.md` of the Redline run that followed. In both arms Redline returned the no-change status on the draft. The pipeline's Redline half is not a clean control, and nothing froze an expectation that its draft comes back unchanged. So its `R1` is read from both judges' verdicts, and each judge found no visible defect that the reply left unreported. Both drafts reach the form through a link whose label says where it goes: *Gå till intresseanmälan* before the change, and *Gå till formuläret för intresseanmälan* after it. So neither draft reaches either limit the candidate draws.

**Regressions.** None. Every control that met its reading before the change meets it after.

## What shipped, and why

The candidate at `a1453560` ships. It meets the target, since no candidate run carries a target miss, and no control regresses. That is the plan's first exit, so no revise round was taken. The triage comment carries Thomas's ruling, so the change would have shipped whatever the measurement showed. The measurement shows that it does what the ruling asks.

**A decision record.** None is written. The fault reproduced, so the protocol's *Not reproduced* case, the one that writes a record, does not arise. The change is wording in two review halves and is easily reversed, so it fails the first of `docs/rules/docs.md`'s three criteria. The reserved number `0226` is left unused.

## Side effects

`O1` is met on all eighteen runs, and `S1` with it. Each packet's `filesystem-changes.json` shows no created, removed or changed path outside the Harness's own configuration directory and the caches, with one exception. Each file-target run created `work/output.md` beside the input, which is the effect it was asked for. `work/input.md` and `work/source.md` are unchanged. No file was left in any run's temporary directory. The staged Skills are byte-identical before and after. Every private root was removed by the runner (`cleanup.json`).

Scopes 3 to 5 were read once around the whole of both arms, into `runs/wave-1-before-*.txt` and `runs/wave-1-after-*.txt`:

- **The main checkout and this build's working tree.** Their `HEAD` and status are identical before and after.
- **The session scratchpad.** It is identical before and after.
- **The scratch root.** Its after-listing holds this build's packets, its judges' directories, its logs, its evaluator scripts and the two extracted drafts. It also holds the logs of a gate run made while the runs were in flight. All of these are this build's own.

No judge's directory held anything but its inputs and its judgement when it was collected.

## What is not measured

- `T1` and `R2` are `skipped`. Every packet keeps its trace, so they can be judged from it later.
- `A1`, `A2`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are `skipped`, since `C1`, `R1`, `O1` and `S1` are this evaluation's criteria.
- The Write half of `web-copy-sv` is not judged. It stages the Redline half's input.
- No draft in this evaluation says *the form below* over a link, so #345's case, which the candidate keeps as a finding, was not exercised by a run.

## What was filed

Nothing. No candidate run carries a target miss, no control regresses, and no file-target run left its `output.md` undelivered. So there is no remaining miss to file.
