# Candidate Redline genre controls — editorial #338

- **record** — `redline-gpt-2026-09-19-338-controls-genres`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, observed native turn contexts
- **harness** — native Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commits** — first eight controls: `f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9`; web-copy controls and explicitly labelled affected reruns: `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`

## Conditions

The frozen [matrix](../corpus/editorial-quality/README.md) precedes every run. Each control has a fresh native session, immutable private installation and only its supplied artifact as input.md. No rubric, original source, baseline result or other provider record reaches the model. The ten controls are sequential; correction agents use the inherited observed model/effort. The neutral Harness dispatch identifies local SKILL.md and does not replace its workflow. Complete before/after inventories include work, resource copies, scratch and private native state. Side-effect classifications distinguish Skill work from Harness bootstrap/log/database changes. Each control is judged on its own before comparisons.

The per-session `trace-audit.json` checks required resource paragraphs separately for each actual parent, correction and mechanical session, not only their union. Every editorial correction in the ten original controls sees its full base/genre/web-craft/review/anti-slop resources; the mechanical-only children see the complete mechanics contract. Their scope split is intentional.

**R2 trace limit:** native dispatch serializes subagent task messages as encrypted strings. Fresh child sessions, inherited identities, actual resource reads/tool results, correction outputs, re-review and installed closing passes are observable, but the evaluator cannot independently reproduce every byte of the raw spawn brief from this trace. Statements about supplied findings are supported by the child's resulting account and visible behaviour, not claimed decryption. No source package is staged in any Redline session, and its fresh parent never receives one. This observation limit is retained even where the exercised R2 behaviour passes.

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

## `column-clean`

- **fixture** — `column-clean`, sv
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Completed no-change status; [final text](../editorial-329/runs/controls-genres/column-clean/final.md) equals the supplied artifact.
- **side effects** — No surviving Skill effects; full input/work/resource/scratch inventories unchanged. 316 native private-home entries and project-trust config update are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Preserves Nora Vik's personal questioning and self-irony, not recasting reflection as a campaign or manufacturing an anecdote.
  - `G2` — `pass` — The early point, reflection on valuable non-decision conversations and doubtful closing “Kanske” retain their distinct jobs.
  - `P1` — `pass` — The move from the meeting form to shared understanding remains coherent; the speculative benefit stays qualified rather than becoming a guarantee.
  - `W1` — `pass` — The coherent paragraph over 80 words, purposeful repeated question and lack of H2s survive. No numerical preference forces fragmentation or a deviation explanation.
  - `L1` — `pass` — Native Swedish personal syntax and dry final joke remain intact.
  - `L2` — `pass` — Punctuation and inflection are consistent after the final mechanical pass.
  - `T1` — `pass` — Default none is honoured in configuration and actual file loads; reflection's turn does not trigger ABT.
  - `R1` — `pass` — Every claim, doubt and rough personal turn is preserved byte-for-byte; no taste-only correction is requested.
  - `R2` — `pass` — Full required resource paragraphs are visible in native outputs. No correction is needed. Installed Proofread runs exactly once with resolved sv mechanics; no substantive edit follows.
  - `O1` — `pass` — Whole-root before/after inventories prove source preservation and no Skill scratch.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Positive preservation coverage includes the deliberate long coherent paragraph and purposeful recurrence. It contains no accidental verbatim whole-sentence duplication, so #346's subsequent classification clarification does not target its actual text.

## `column-flawed`

- **fixture** — `column-flawed`, sv
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Corrected [final text](../editorial-329/runs/controls-genres/column-flawed/final.md), preserving and explicitly reporting the irreparable participation contradiction.
- **side effects** — No Skill files survive; full input/work/resource/scratch unchanged. 319 native-home creations and private trust-config change are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Keeps the personal reflection about understanding together and the author's actual doubt; no replacement memory or invented habit is supplied.
  - `G2` — `pass` — Replaces the unsupported sweeping headline and generic ending with the text's concrete question and existing reflective ending; no compulsory anecdote or campaign is added.
  - `P1` — `fail` — **Reported irreparable contradiction:** the opening still asserts both a first meeting and never attending such a meeting. The supplied text cannot decide which is true; its continuing reader conflict is not falsely scored as repaired.
  - `W1` — `pass` — Removes the generic opening/closing material and tautology while preserving compact coherent paragraphs without manufactured H2s.
  - `L1` — `pass` — The author's Swedish reflection and uncertain voice remain idiomatic; contradiction is a factual/coherence problem rather than language interference.
  - `L2` — `pass` — Swedish quotation and sentence mechanics remain correct after the closing pass.
  - `T1` — `pass` — Default none, with no technique resources loaded.
  - `R1` — `pass` — Names the contradictory claims precisely, leaves both rather than selecting or inventing a memory, and reports the unresolved issue. Removes only identified sweeping/generic claims with a complete removal account; preserves non-decision value and uncertainty about the extra box.
  - `R2` — `pass` — Actual full scoped reads, one fresh same-model/high correction, re-review and exactly one successful installed Proofread pass are observable. No substantive edit follows.
  - `O1` — `pass` — Full-root inventories establish unchanged input/resources and no persistent Skill scratch.
- **unresolved findings** — Mutually incompatible meeting participation claims, explicitly reported with the inability to decide from text alone.
- **defects filed** — none; this is the control's intended missing-source boundary, correctly respected.
- **notes** — P1 records the final artifact's real remaining problem; R1 records successful detection, preservation and reporting. These are deliberately different judgements. The earlier invented scene is neither silently endorsed as factual nor replaced with a more plausible invented experience.

## `opinion-clean`

- **fixture** — `opinion-clean`, sv
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Completed no-change status; [final text](../editorial-329/runs/controls-genres/opinion-clean/final.md) is byte-identical to input.
- **side effects** — No remaining Skill artifacts; full input/work/resource/scratch unchanged. 316 native private-home entries and project-trust config change are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Preserves the author's polemical argument for postponement and a measured dual-channel trial, rather than flattening it to neutral exposition.
  - `G2` — `pass` — Early thesis, pilot evidence, real administrative objection and explicit council/administration action remain intact.
  - `P1` — `pass` — Distinguishes booking counts from people and digital ability; acknowledges the unmeasured workload/cost before demanding measurement.
  - `W1` — `pass` — Informative sections and coherent argument paragraphs remain navigable without mechanical shortening.
  - `L1` — `pass` — Native Swedish polemical syntax and the final calendar/assumption sentence retain their force.
  - `L2` — `pass` — Date, number, attribution and punctuation forms remain correct after the mechanics pass.
  - `T1` — `pass` — Default none resolves; actual loads contain no inferred technique.
  - `R1` — `pass` — Preserves every claim, objection, cost uncertainty and the sharp final sentence byte-for-byte; adds no generic hedges or unsupported motives.
  - `R2` — `pass` — Complete required scoped resource paragraphs are visible. No correction is warranted; exactly one installed Proofread invocation completes, with no substantive edit afterward.
  - `O1` — `pass` — Full-root inventories show no surviving Skill files and unchanged supplied input/resources.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — This is a positive preservation test of opinion strength and legitimate polemic, separate from the source-aware Write modality issue #343.

## `opinion-flawed`

- **fixture** — `opinion-flawed`, sv
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Corrected [final text](../editorial-329/runs/controls-genres/opinion-flawed/final.md), with the four removed unsupported claims named separately.
- **side effects** — No surviving Skill effects; input/work/resources/scratch unchanged after correction and a separate mechanical agent. 324 native-home creations and trust-config update are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Keeps the proposal to retain telephone booking during the six-month trial rather than making the author neutral; removes invented hateful/exclusionary motives.
  - `G2` — `pass` — Early position, attributed counts, administrative objection and named council action all remain. The vague exhortation becomes an action already supported in the body.
  - `P1` — `pass` — Removes the population/digital-ability inference that booking counts cannot support and the false no-cost conclusion that absence of time measurement cannot support.
  - `W1` — `pass` — Replaces opaque background/discussion headings with information-bearing entries while retaining coherent argument paragraphs.
  - `L1` — `pass` — Idiomatic direct Swedish argument remains; the final address to Kommunstyrelsen is clear and warranted.
  - `L2` — `pass` — Correct date, counts, compounds and punctuation survive the installed mechanical pass.
  - `T1` — `pass` — Default none, and actual resource loads contain no technique inferred from argument form.
  - `R1` — `pass` — Corrects all six visible findings while preserving 96/24 bookings, no unique-person count, unexamined digital ability, 8 April attribution, double-administration objection, no time measurement, uncomputed cost and the proposed measurement/trial. The removal account names only the unsupported motives, millions claim, population inference and cost conclusion. No force-reducing generic hedge is added.
  - `R2` — `pass` — Full scoped resources are visible; one fresh correction is re-reviewed, then a separate same-model/high agent executes the installed closing Proofread pass once. No substantive edit follows. Raw spawn briefs retain the common encrypted-trace limitation.
  - `O1` — `pass` — Complete inventories prove source preservation and zero remaining Skill files across all staged writable roots.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — A rejected rm-trap command did not execute. A subsequent bare mktemp attempted an unwritable system-temp location and failed, while the invocation engine itself succeeded; the agent then used the declared explicit scratch path with failure checking for mechanics resolution. These actual transient failures remain in the trace/side-effect account rather than being hidden, but caused no persistent side effect or second mechanical pass.

## `web-copy-clean`

- **fixture** — `web-copy-clean`, sv
- **instruction commit** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`
- **invocation** — `/redline --genre=web-copy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Completed no-change status; [final text](../editorial-329/runs/controls-genres/web-copy-clean/final.md) equals the supplied information page.
- **side effects** — No remaining Skill files; complete input/work/resource/scratch unchanged. 316 native-home entries and the trust-config update are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Preserves a useful information page explaining the expression-of-interest process; no sales template or invented CTA is imposed.
  - `G2` — `pass` — Keeps the nonorder condition, requested fields, lack of payment requirement and email/meeting consequence without inventing a destination or page function.
  - `P1` — `pass` — Explains what the form does before details, then what happens after submission; no hidden booking consequence is added.
  - `W1` — `pass` — Short informative headings and variable section lengths remain intact without numerical findings or gratuitous expansion.
  - `L1` — `pass` — Clear native Swedish action/information wording is preserved.
  - `L2` — `pass` — Correct e-post compound, punctuation and temporal expression survive the mechanics pass.
  - `T1` — `pass` — Default none, with no technique file loaded or sales arc inferred.
  - `R1` — `pass` — Preserves every condition and consequence byte-for-byte; no taste-only rewrite, unsupported button or embedded form state is requested.
  - `R2` — `pass` — Full required resource paragraphs are visible; no correction is needed. Exactly one installed Proofread invocation completes with mechanics scope and no substantive edit afterward.
  - `O1` — `pass` — Full-root inventory proves input/resource preservation and no Skill scratch.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Positive information-page coverage complements the separate service-page pipeline and misleading-action flawed control. The absence of a CTA is purposeful and accepted.

## `web-copy-flawed`

- **fixture** — `web-copy-flawed`, en_US
- **instruction commit** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`
- **invocation** — `/redline --genre=web-copy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Corrected [final text](../editorial-329/runs/controls-genres/web-copy-flawed/final.md), with the removed defective claims listed separately.
- **side effects** — No surviving Skill files; input/work/resources/scratch unchanged after actual fresh correction and installed Proofread. 317 native-home creations and private trust-config update are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Names the actual shared-room booking review and useful reader action rather than an abstract audience facing complexity.
  - `G2` — `pass` — Preserves price/scope/deliverables and the accurate expression-of-interest consequence. The link opens the supplied form; no embedded form fields, button state, payment function or destination are invented.
  - `P1` — `pass` — The offer precedes price/inclusions and the next step; no false promise that submission places an order or books a meeting survives.
  - `W1` — `pass` — Replaces fragmented opaque one-word headings with useful sections and a concise deliverables list; related conditions now sit together.
  - `L1` — `pass` — Removes “Take the thumb out” and generic translated-sounding promotion; the resulting English reads naturally as concise service information.
  - `L2` — `pass` — US-English mechanics, number/currency and punctuation are consistent; SEK 4,800 including VAT is retained without currency conversion.
  - `T1` — `pass` — Default none, actual files contain no inferred narrative technique.
  - `R1` — `pass` — Corrects the calque, abstract opening, opaque headings and false Book and pay action. Preserves one shared room/one housing association, 45 minutes/two representatives, written booking steps/unclear points/two simplifications, all requested fields, no order/payment/meeting booking, email within three working days and the exact URL. Removed empty/full-potential/journey/complexity and false-action claims are explicitly accounted for.
  - `R2` — `pass` — Full scoped resource paragraphs are visible. One fresh same-model/high correction is re-reviewed; exactly one installed Proofread pass resolves en_US mechanics and no substantive edit follows.
  - `O1` — `pass` — Complete inventories demonstrate unchanged source/resources and no persistent Skill effects.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Actual positive coverage of #345: the linked form is treated as a destination, not proof of embedded interface controls. Source-blind correction uses only the supplied offer and conditions and requests no nonexistent brief.

## Affected rerun: `article-flawed` — #346

- **fixture** — Exact unchanged `article-flawed`, sv; original failure remains above
- **instruction commit** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`; no expected repair or previous result supplied
- **output target** — `response`
- **observed delivery** — Corrected [final artifact](../editorial-329/runs/controls-genres-rerun/article-flawed/final.md), with one ingress sentence and an explicit removed-claim account.
- **side effects** — No surviving Skill effects. Input/work/resource/scratch inventories unchanged; 318 native-home creations and trust-config change are Harness effects.
- **criteria** —
  - `G1` — `pass` — An explanatory article replaces catastrophe/health certainty without inventing replacement stakes.
  - `G2` — `pass` — Informative headline, nonduplicated ingress, complementary evidential lead, explained limits and a supported next-step ending perform distinct jobs; no byline is manufactured.
  - `P1` — `pass` — Operative temperature is defined before the limitation; placement, missing measurements and funding uncertainty constrain the conclusions.
  - `W1` — `pass` — The duplicate is removed within correction; mixed material is grouped into measurement limits and the next trial. The final two short paragraphs have different jobs and are not failed on a length quota.
  - `L1` — `pass` — Idiomatic Swedish explanation preserves useful technical substance.
  - `L2` — `pass` — Swedish mechanics and date/number forms are correct after the closing installed pass.
  - `T1` — `pass` — Default none, with no technique resource loaded.
  - `R1` — `pass` — Repairs whole-sentence duplication in the editorial correction, along with the named unsupported claims and structural defects. Retains six rooms, 14/120, four weeks, local nonlegal threshold, two/four placements, no experimental placement comparison, operative-temperature definition/absence, missing draught/experience/duration/health-effect evidence, Rask's recommendation and November's undecided funding. Each legitimate removed claim is named.
  - `R2` — `pass` — Parent and one fresh correction each actually see complete editorial resources. A separate fresh same-model/high mechanical agent runs installed Proofread once after re-review; its first shell trap command was rejected before execution, and Python cleanup successfully executes the pass. No substantive edit follows. Raw dispatch remains encrypted as documented.
  - `O1` — `pass` — Entire-root inventory verifies no remaining correction or mechanical scratch and no source/resource mutation.
- **unresolved findings** — none
- **defects filed** — Positive affected rerun for [#346](https://github.com/Kntnt/skills/issues/346); the previous failed-quality run is preserved.
- **notes** — The same frozen artifact and invocation were used without rubric, expected findings or previous output. Different valid headings/paragraph grouping from the first attempt are not themselves scored as improvements; the decisive change is removal of the observable duplicate while preserving facts and the stage boundary.

## Positive rerun: `article-clean` — #346

- **fixture** — Exact unchanged `article-clean`, sv
- **instruction commit** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`; no earlier result or expected preservation supplied
- **output target** — `response`
- **observed delivery** — Completed no-change status; [final text](../editorial-329/runs/controls-genres-rerun/article-clean/final.md) equals the exact frozen input.
- **side effects** — No Skill artifacts; input/work/resources/scratch unchanged. 316 native-home creations and trust-config change are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Calm bounded explanation is preserved.
  - `G2` — `pass` — Informative short H1, result-bearing ingress, complementary lead, explanatory body and supported ending remain, with no invented byline.
  - `P1` — `pass` — Placement precedes interpretation; the local threshold and missing duration/experience evidence retain their constraints.
  - `W1` — `pass` — No finding targets valid heading/paragraph lengths or useful ingress/body overlap; no literal accidental duplicate exists.
  - `L1` — `pass` — Native Swedish explanation remains unchanged.
  - `L2` — `pass` — Swedish mechanics remain correct after the installed final pass.
  - `T1` — `pass` — Default none and no technique resource load.
  - `R1` — `pass` — Byte-identical preservation of working voice, facts, quote and limits; the new sentence-duplication classification does not induce taste-only editing.
  - `R2` — `pass` — Full resources actually visible, no correction needed, exactly one installed Proofread invocation and no later substantive edit.
  - `O1` — `pass` — Whole-root inventories show no surviving Skill files and unchanged source/resources.
- **unresolved findings** — none
- **defects filed** — Positive regression counterpart for [#346](https://github.com/Kntnt/skills/issues/346).
- **notes** — Combined with the unchanged purposeful-recurrence column control and the successful article-flawed rerun, this supports the narrowly observed boundary correction; it does not establish that all future repetition will be judged correctly.

## Affected rerun: `case-study-clean` — #341

- **fixture** — Exact unchanged `case-study-clean`, sv; its contaminated clean-label limitation remains
- **instruction commit** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`; no expected diagnosis, original source or previous output supplied
- **output target** — `response`
- **observed delivery** — No-change/no-findings status; [final text](../editorial-329/runs/controls-genres-rerun/case-study-clean/final.md) equals the input, including the previously identified quotation ellipsis.
- **side effects** — No surviving Skill files; all input/work/resource/scratch inventories unchanged. Native-home bootstrap/session effects and trust-config update are classified separately.
- **criteria** —
  - `G1` — `pass` — Customer agency, cross-shift purpose and supplier's supporting role remain intact.
  - `G2` — `pass` — Customer situation/action/results/appraisal and the supplier publication disclosure remain present and distinct.
  - `P1` — `pass` — Preparation, assignment-time comparison and different-workload causal limitation retain their relation.
  - `W1` — `pass` — Useful paragraphs, section entries and qualified appraisal remain readable without extra sales blocks.
  - `L1` — `fail` — **Remaining qualitative concern, consistent with the original assessment:** “innan nästa hus börjar” still leaves the activity unstated, requiring the reader to reconstruct what starts. This is an idiom/clarity judgement, not a mechanical error or proof of an invented quotation. Distinctive spoken voice alone is not grounds for replacement; several possible intended activities mean the source-blind reviewer cannot silently supply one as the speaker's words.
  - `L2` — `pass` — Swedish date, number, quotation and inflection mechanics are correct after installed Proofread.
  - `T1` — `pass` — Default none and no technique resource load.
  - `R1` — `fail` — **Remaining qualitative diagnosis miss:** the clearer case-review distinction is actually loaded, but the run still reports no findings and does not identify the ellipsis as a clarification concern. Preservation succeeds; the intended source-blind reporting regression is not demonstrated.
  - `R2` — `pass` — The parent actually sees every updated case-review paragraph and other editorial resources. No correction is spawned on its no-findings judgement. A separate fresh same-model/high agent executes installed Proofread once with the complete mechanics scope; no substantive edit follows. This is not a resource-loading failure.
  - `O1` — `pass` — Full-root inventory proves unchanged input/resources and no remaining Skill scratch.
- **unresolved findings** — The run reports none; the evaluator retains the L1/R1 concern. The revised instruction cannot be claimed to have solved this observed case.
- **defects filed** — Additional retained evidence for [#341](https://github.com/Kntnt/skills/issues/341).
- **notes** — This is a qualitative judgement with an explicit clean-fixture limitation, not an unconditional contract rejection or a demand for one preferred wording. The original and rerun remain separate. No rubric, example answer or source was exposed to induce the expected diagnosis.

## Positive rerun: `column-clean` — #348

- **fixture** — Exact unchanged `column-clean`, sv
- **instruction commit** — `7022c804dfbda4332723bf96b6a9857c24e63b6e`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`; no prior result or expected casing supplied
- **output target** — `response`
- **observed delivery** — Completed no-change status; [final text](../editorial-329/runs/controls-348/column-clean/final.md) equals the frozen original.
- **side effects** — No surviving Skill files; input/work/resources/scratch unchanged. 316 native-home creations and trust-config update are classified Harness effects.
- **criteria** —
  - `G1` — `pass` — Preserves the personal reflective angle and self-irony.
  - `G2` — `pass` — Keeps early point, meaningful non-decision reflection and qualified ending; no anecdote or campaign is manufactured.
  - `P1` — `pass` — Shared understanding remains a possible benefit, not an invented measured improvement.
  - `W1` — `pass` — The coherent long paragraph, purposeful recurrence, short H1 and absence of H2s are preserved without quantitative/taste findings.
  - `L1` — `pass` — Native Swedish personal voice remains unchanged.
  - `L2` — `pass` — The updated sv mechanics rule is actually visible in the resolver output; correct punctuation/casing is preserved, including “lösningen: ännu en ruta”.
  - `T1` — `pass` — Default none; no technique resource load.
  - `R1` — `pass` — Byte-identical preservation of every claim, doubt, voice choice and purposeful repetition.
  - `R2` — `pass` — Complete editorial resource paragraphs are visible; no correction is warranted. Exactly one installed Proofread invocation resolves the updated sv mechanics scope and no substantive edit follows.
  - `O1` — `pass` — Complete root inventories establish no Skill scratch and unchanged source/resources.
- **unresolved findings** — none
- **defects filed** — Positive preservation regression for [#348](https://github.com/Kntnt/skills/issues/348).
- **notes** — This control verifies preservation on the updated mechanics resource. It does not itself contain the disputed unquoted full-question casing; the root evaluator's exact earlier column-artifact replay supplies that targeted negative/positive case. The evidence boundaries are not conflated.
