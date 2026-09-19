# Candidate Redline genre controls — editorial #338

- **record** — `redline-gpt-2026-09-19-338-controls-genres`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, observed native turn contexts
- **harness** — native Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9`

## Conditions

The frozen [matrix](../corpus/editorial-quality/README.md) precedes every run. Each control has a fresh native session, immutable private installation and only its supplied artifact as input.md. No rubric, original source, baseline result or other provider record reaches the model. The ten controls are sequential; correction agents use the inherited observed model/effort. The neutral Harness dispatch identifies local SKILL.md and does not replace its workflow. Complete before/after inventories include work, resource copies, scratch and private native state. Side-effect classifications distinguish Skill work from Harness bootstrap/log/database changes. Each control is judged on its own before comparisons.

## `article-clean`

- **fixture** — `article-clean`, sv
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Successful no-change status; [final text](../editorial-329/runs/controls-genres/article-clean/final.md) is byte-identical to the input.
- **side effects** — No surviving Skill effects; all work/resources/input/scratch unchanged. 318 native private-home entries and the project-trust config update are classified Harness effects. Full inventories and cleanup evidence are preserved in the run.
- **criteria** —
  - `G1` — `pass` — Preserves calm explanation of what the readings establish and cannot establish, rather than replacing it with promotion or crisis.
  - `G2` — `pass` — Short informative H1, independent result-bearing ingress, explanatory lead, supported ending and absence of an unavailable byline all survive without manufactured findings.
  - `P1` — `pass` — Sensor placement precedes interpretation; the local threshold, missing duration and missing experience measures constrain the conclusion.
  - `W1` — `pass` — The short heading and useful section entries remain; no numerical length rule provokes a rewrite.
  - `L1` — `pass` — Native Swedish explanatory wording is preserved, including “pekar ut tillfällen att undersöka”.
  - `L2` — `pass` — Swedish quotation marks, date and number forms remain correct after the mechanics pass.
  - `T1` — `pass` — Default none is resolved, and no technique resource is loaded despite the text's question/answer shape.
  - `R1` — `pass` — No change to working facts, voice, quotations, limits or ending; no taste-only correction.
  - `R2` — `pass` — Actual local Skill, base/genre review, web-craft halves, anti-slop and sv composition/review scopes are read. No correction is needed. Installed Proofread is invoked once with separate formal flags and the in-memory artifact; mechanics and sv mechanics resolve successfully. No substantive edit follows.
  - `O1` — `pass` — Full-root inventories establish source preservation and no remaining Skill-created artifacts.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — The initial shell trap command was automatically rejected before execution. The agent adapted to Python try/finally cleanup and completed the invocation; this did not alter the editorial instructions or input.

## `article-flawed`

- **fixture** — `article-flawed`, sv
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — A corrected [final artifact](../editorial-329/runs/controls-genres/article-flawed/final.md), with an explicitly reported remaining duplicated ingress sentence and full removed-claim account.
- **side effects** — No surviving Skill files after a real fresh correction and a separate closing Proofread agent; complete input/work/resource/scratch inventories unchanged. Native private-home changes are classified separately.
- **criteria** —
  - `G1` — `pass` — Removes the manufactured catastrophe and health certainty, returning the article to a bounded explanation of what the temperature readings show.
  - `G2` — `fail` — **Qualitative remaining finding:** H1, lead, explanation and earned ending work, but the ingress still repeats the exact same sentence twice. The run reports this openly rather than falsely claiming complete repair.
  - `P1` — `pass` — Defines operative temperature before explaining its absence, separates placement from interpretation and keeps the recommendation within the available evidence.
  - `W1` — `fail` — The mixed long paragraph is usefully regrouped into findings, limits and next step; however, the literal double ingress makes the reader read the same assertion twice without function.
  - `L1` — `pass` — Swedish explanatory syntax is idiomatic; the remaining whole-sentence duplicate is scored under G2/W1/R1 rather than being mistaken for a locale error.
  - `L2` — `pass` — Swedish date, number and inflection forms remain correct after the installed mechanical pass.
  - `T1` — `pass` — Default none resolves and no technique file is loaded; the correction is not forced into ABT.
  - `R1` — `fail` — **Qualitative repair failure:** seven visible findings are addressed, but the parent expressly excludes the duplicated ingress sentence from correction as supposedly mechanical. It survives Proofread. Every measured fact, exclusion, uncertainty and quotation-free attribution remains; the reported removal account correctly names only the rejected catastrophe, health, empty importance and rescue claims.
  - `R2` — `pass` — Full scoped resources are actually visible. A fresh same-model/high correction runs once, is re-reviewed, and a separate fresh agent executes exactly one successful installed Proofread invocation. An initial shell cleanup command is rejected before execution and retried through Python, not counted as a second pass. No substantive change follows Proofread. Misclassification of the duplicate is the observed R1 quality failure, and is disclosed in the final account.
  - `O1` — `pass` — Full-root inventories, including correction and mechanical subagents' scratch, show no remaining Skill-generated files. This is a real positive test of #340, not merely a no-change path.
- **unresolved findings** — Exact duplicated ingress sentence, explicitly named in the final delivery.
- **defects filed** — [#346](https://github.com/Kntnt/skills/issues/346).
- **notes** — Retains six rooms, four weeks, 14/120 passes, the local nonlegal 20-degree threshold, two outer/four inner placements, no experimental placement comparison, operative-temperature definition and absence, missing draught/experience/duration measures, no health study, Elin Rask's recommendation and November's undecided funding. The completed artifact remains a quality failure pending an affected rerun; honest reporting does not make its prose fully correct.

## `case-study-clean`

- **fixture** — `case-study-clean`, sv; frozen name retained, with a discovered limitation as a pure preservation control
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Successful no-change status; [final text](../editorial-329/runs/controls-genres/case-study-clean/final.md) equals the supplied text.
- **side effects** — No surviving Skill files; input/work/resources/scratch unchanged. 318 created native private-home entries and its project-trust config update are classified Harness effects, with full inventories and cleanup captured.
- **criteria** —
  - `G1` — `pass` — Preserves the customer's agency, cross-shift purpose and supplier's supporting role.
  - `G2` — `pass` — Situation, category work, results and the customer's qualified appraisal remain distinct; Svale's publisher disclosure and checklist destination stay truthful.
  - `P1` — `pass` — Preparation precedes the results, and the explicit workload difference prevents a causal inference from two rather than three assignment days.
  - `W1` — `pass` — The coherent paragraphs and informative result/preparation sections remain readable without an added sales block or quote-count requirement.
  - `L1` — `fail` — **Qualitative text-internal clarity concern:** the quotation “Den tiden skulle jag avsätta innan nästa hus börjar” leaves the activity unexpressed; a house does not begin in the sense the maintenance trial needs. This is the same reader reconstruction burden as baseline “innan nästa byggnad börjar”, scored consistently. No unseen English original is needed to recognise the ellipsis, though Redline cannot establish the speaker's intended replacement from a source it lacks.
  - `L2` — `pass` — Correct Swedish quotation dashes, date, inflection and number forms are preserved; L1's issue is not relabelled a mechanical error.
  - `T1` — `pass` — Default none resolves, and only base/genre/web-craft/review/anti-slop and the selected sv scopes load; no ABT is inferred.
  - `R1` — `fail` — **Qualitative diagnosis/reporting miss:** preservation of the customer's claims, reservation, figures and publisher stance succeeds, but the text-internal quotation ellipsis is neither diagnosed nor reported as requiring clarification. A silent invented replacement quotation would not be an acceptable repair.
  - `R2` — `pass` — Actual outputs contain all required resource paragraphs; no correction is spawned on the reported no-findings path. Installed Proofread completes once with the separate formal invocation and mechanics scope, followed by no substantive edit.
  - `O1` — `pass` — Whole-root inventories show no surviving Skill artifacts or changes to the supplied input/resources.
- **unresolved findings** — Redline reports none; the evaluator identifies the unreported quotation ellipsis under L1/R1.
- **defects filed** — Additional source-blind Redline evidence for [#341](https://github.com/Kntnt/skills/issues/341); the original source-aware Write defect remains independently recorded.
- **notes** — **Method limit:** despite its frozen clean label, this fixture is contaminated as a pure “nothing should change” test by an existing idiom defect. The label does not override the actual text or predeclared L1 criterion. Its other preservation expectations remain meaningful. Neither the fixture nor the expected matrix was rewritten after this observation. A reported irreparable wording concern would satisfy reporting while still leaving a quality limitation in the quotation; authentic distinctive voice must not be normalised merely for taste.

## `case-study-flawed`

- **fixture** — `case-study-flawed`, sv
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Corrected [final text](../editorial-329/runs/controls-genres/case-study-flawed/final.md) and a clear unresolved-finding/removal account.
- **side effects** — No Skill files survive; input/work/resources/scratch unchanged after fresh correction and closing Proofread. 321 native-home entries and the trust-config change are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — The customer and its qualified appraisal replace first-person supplier self-praise and rescue framing; the title's shared view is supported by Lind's retained quotation.
  - `G2` — `fail` — **Reported irreparable quality limitation:** results and appraisal are present, but customer background, purpose, choices and implementation cannot be supplied from the given artifact. The delivery explicitly names these missing case functions instead of inventing them.
  - `P1` — `pass` — The revised result retains the differing workload and no-causation statement, removing the adjacent contradictory software-caused conclusion.
  - `W1` — `pass` — Removes the literal double ingress and repeated lead, deletes the quotation's pre-echo and uses informative result/appraisal sections. Restating the result in its detailed evidential paragraph has a useful job and is not treated as forbidden recurrence.
  - `L1` — `pass` — Clear idiomatic Swedish preserves Lind's reservation and direct speech.
  - `L2` — `pass` — Swedish compounds, speech dashes and forms remain correct after the mechanics pass.
  - `T1` — `pass` — Default none; actual resource reads contain no technique.
  - `R1` — `pass` — Corrects visible self-praise, unsupported rescue, redundancy and causal contradiction; preserves 31 cases/eight weeks/emergency exclusions, two-versus-three assignment days, workload reservation, both substantive appraisals and supplier publication. Each removed claim is explicitly listed. Missing customer background/action is reported as irreparable without absent facts.
  - `R2` — `pass` — Required resource paragraphs are visible; one fresh same-model/high correction is re-reviewed, then exactly one installed Proofread pass resolves mechanics and returns before delivery. No substantive edit follows.
  - `O1` — `pass` — Whole-root inventories establish no surviving Skill-generated artifacts, including after correction.
- **unresolved findings** — Customer background, purpose, choices and implementation absent from the input, explicitly reported.
- **defects filed** — none; the remaining quality gap is the control's intentionally unavailable information, correctly handled.
- **notes** — The frozen expectation separates detection/preservation from final completeness. G2 therefore remains fail while R1/R2 pass; the honest missing-facts account is not falsely scored as a complete customer case. This run already repairs the whole-sentence duplication correctly on f8cac6d, independently of #346's later boundary clarification.
