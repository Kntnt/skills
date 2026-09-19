# Baseline Write — editorial #338

- **record** — `write-gpt-2026-09-19-338-baseline`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, observed in native turn contexts
- **harness** — native Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) supplied the criteria before any editorial run. Each invocation used a fresh native session, immutable local skill copies, one staged input and no previous conversation. The complete source package was given only to Write; Redline received only the complete extracted draft, including metadata. The baseline's ordinary ABT is retained rather than overridden. Exact neutral dispatch and scratch context are captured in each run's `harness-context.md`; they add no editorial instruction. No other provider's evaluation record was consulted. Judgements below precede any candidate comparison.

Raw responses, invocation/context, inventories, exact filesystem changes, native parent/correction rollouts and cleanup evidence are under [baseline runs](../editorial-329/runs/baseline/). Harness-created caches, native sessions and trusted-project config updates are explicitly distinguished from Skill effects in each `side-effects.md`. The evaluator's artifact extraction removes only the separately identified delivery account; it does not rewrite the text. Failed runs remain.

## `article-sv`

- **fixture** — `article-sv`
- **invocation** — `/write --genre=article --language=sv --output=response source.md`
- **contextual instruction** — `none`; neutral Harness dispatch is preserved separately.
- **output target** — `response`
- **observed delivery** — Complete Swedish article, leading Kntnt metadata and a separate delivery account; [draft](../editorial-329/runs/baseline/article-sv/draft.md), [full response](../editorial-329/runs/baseline/article-sv/write/response.txt).
- **side effects** — No remaining Skill-created files; source, complete working copy, installed resources and scratch are unchanged. Two private UV directories were created and cleaned; an earlier rm command was rejected before execution. Native Codex created 316 private-home entries and changed only its private config to add project trust; [full classification](../editorial-329/runs/baseline/article-sv/write/side-effects.md).
- **criteria** —
  - `F1` — `pass` — “14 minst en mätning under 20 grader”, unknown duration/experience, six-room/four-week scope, non-legal threshold, unmeasured adjustment effect and undecided funding all remain; no saving, health effect or causal explanation is invented.
  - `G1` — `pass` — The angle is what the manager can do with the measurements: “pekar ut tider att undersöka vidare”; the ending turns that into comparing the readings with room-use times.
  - `G2` — `pass` — The H1 supplies the bounded result, the standfirst frames the management question, and the body lead introduces who measured where/when before the first H2; no byline is invented. The standfirst is less specific than the body but still informative.
  - `P1` — `pass` — “ett mått som tar hänsyn till ... kallas operativ temperatur” explains the concept before using its name; the article distinguishes a below-threshold reading from a whole cold lesson and defines temperature series at its practical recommendation.
  - `W1` — `pass` — Three informative H2s provide useful entry points; the lead introduces the actual trial rather than repeating the standfirst's question. Short coherent paragraphs preserve the technical explanation.
  - `L1` — `pass` — Swedish clause order and idiom are natural, including “Den var inte ett påstående om ett rättsligt krav”; the explicit “materialet innehåller ingen normjämförelse” is slightly report-like but an intelligible qualification, not language interference.
  - `L2` — `pass` — Swedish dates, compounds and interview speech dash are consistently used; no locale conversion or new date is introduced.
  - `T1` — `pass` — Metadata and delivery report `abt` from `article`; trace item_4 loads the installed article/base and item_6 loads only `techniques/abt.md`. Item_5 returns the actual Swedish composition scope.
  - `T2` — `pass` — The question concerns what the readings establish; the response is further targeted investigation. Neither crisis nor successful remedy is manufactured.
  - `R2` — `pass` — Trace loads common base, genre, selected ABT and resolved composition content; no review half, review scope or peer editorial Skill is run.
  - `O1` — `pass` — Whole-root before/after inventories and executed cleanup commands establish preserved source/resources and no surviving Skill scratch; Harness changes are enumerated separately.
- **unresolved findings** — The account names unknown duration, cause, pupil experience and adjustment effects as source limits; these are preserved qualifications, not invented answers.
- **defects filed** — `none` for this Write run.
- **notes** — The roughly 450-word orientation was supported without filler. Several valid dispositions could pass; the number of headings is not a gate. The paired Redline run subsequently failed at its nested Proofread invocation, recorded separately.

## `article-en_GB`

- **fixture** — `article-en_GB`, Swedish source to British English
- **invocation** — `/write --genre=article --language=en_GB --output=response source.md`
- **contextual instruction** — `none`; neutral Harness context is captured separately.
- **output target** — `response`
- **observed delivery** — Complete British English article, metadata and delivery account; [draft](../editorial-329/runs/baseline/article-en_GB/draft.md), [full response](../editorial-329/runs/baseline/article-en_GB/write/response.txt).
- **side effects** — No remaining Skill-created files; all work/source/resource/scratch paths unchanged. The two UV directories were cleaned and checked. The 316 new Codex-home paths and its trusted-project config update are Harness effects, fully enumerated in the inventories and [classification](../editorial-329/runs/baseline/article-en_GB/write/side-effects.md).
- **criteria** —
  - `F1` — `pass` — “at least one reading below 20°C” is not inflated into a whole cold lesson; “Funding has not been decided”, unmeasured adjustments, pupil experience and the non-legal working threshold preserve the source's qualifications. The translated Rask quote retains both knowledge and uncertainty.
  - `G1` — `pass` — “shows when to look closer” gives property managers a bounded reporting angle, carried through to matching readings with occupancy before changing controls.
  - `G2` — `pass` — H1 states the result, the separate standfirst identifies audience and evidential limits, and the lead introduces the actual January trial; the three analytical sections lead to an earned practical ending and no invented byline.
  - `P1` — `pass` — “A measure that accounts for both air temperature and heat radiating ... is called operative temperature” introduces the unfamiliar measure intelligibly. The lesson count, placements and causal limits form a connected explanation.
  - `W1` — `pass` — “What the lesson count tells you” and “What a sensor measures” give useful independent entry points; coherent paragraphs and three sections retain the technical detail without fragmentation.
  - `L1` — `pass` — “where the evidence stops”, “room-use times” and “the school caretaker” are idiomatic English choices rather than Swedish word order or literal nominal constructions.
  - `L2` — `pass` — “draughts”, “pupils”, 12 March 2026 and single quotation marks follow British conventions without changing dates or quantities.
  - `T1` — `pass` — Metadata selects article/abt/en_GB; trace item_4 reads local genre/base, item_5 returns actual en_GB composition content, and item_7 reads only the selected ABT resource.
  - `T2` — `pass` — Ordinary evidence limits supply the complication; the answer is a proportionate next investigation, not an invented cause or triumph.
  - `R2` — `pass` — The trace loads composition-only language, common base, genre and ABT and contains no review-half or peer editorial pass.
  - `O1` — `pass` — Complete inventories and explicit temporary-directory cleanup establish response delivery without surviving Skill files or mutated source/resources.
- **unresolved findings** — The delivery account preserves the unknown cause, pupil experience and adjustment effects.
- **defects filed** — `none` for this Write run.
- **notes** — The standfirst explicitly calls the case fictional, compatible with the synthetic material. No reference wording was required and no candidate output had been read when judging this run.

## `case-study-sv`

- **fixture** — `case-study-sv`, English source to Swedish; complete source package
- **invocation** — `/write --genre=case-study --language=sv --output=response source.md`
- **contextual instruction** — `none`; neutral Harness context is captured separately.
- **output target** — `response`
- **observed delivery** — Complete customer case with metadata and separate delivery account, with the observed translation flaw retained; [draft](../editorial-329/runs/baseline/case-study-sv/draft.md), [final](../editorial-329/runs/baseline/case-study-sv/final.md), [response](../editorial-329/runs/baseline/case-study-sv/write/response.txt).
- **side effects** — No remaining Skill files; full work/input/resource/export/scratch inventories unchanged. Private UV directories were cleaned. Native Codex created 316 private-home entries and added project trust to its config; [classification](../editorial-329/runs/baseline/case-study-sv/write/side-effects.md) lists the evidence boundaries.
- **criteria** —
  - `F1` — `pass` — The customer selects/designs the trial, telephone reporting remains, 31 excludes emergencies/prior work, two versus three days measures assignment rather than completion, and “Anteckningen tillskriver uttryckligen inte programvaran skillnaden” preserves non-causality. The qualified appraisal and lack of expansion survive.
  - `G1` — `pass` — The customer's own maintenance problem, category work and qualified appraisal organise the case; the supplier is a supporting third-person actor rather than a rescuer or first-person advertiser.
  - `G2` — `pass` — Situation, action, bounded results and actual quoted appraisal are all present; the checklist link describes a document, not a booking. The publisher is identified only in Write's delivery account, a reuse-context limitation, but the text does not claim independent publication.
  - `P1` — `pass` — The shift-work purpose precedes configuration, and the measured assignment time is explicitly distinguished from repair completion; workload differences explain why causation cannot be assigned.
  - `W1` — `pass` — The short coherent paragraphs move through decision, preparation, measured results and appraisal; no H2s are used, but this moderately sized case remains navigable through clear paragraph openings. No heading quota is imposed.
  - `L1` — `fail` — **Qualitative language interference:** “innan nästa byggnad börjar” carries over the source's “before the next building starts”; the Swedish reader has to reconstruct that the trial/implementation begins in that building. This is neither a fabricated fact nor a mechanical spelling error.
  - `L2` — `pass` — Swedish speech dashes, compounds, date and number forms are consistent; the awkward translated predicate is scored under L1 rather than misclassified as wrong locale mechanics.
  - `T1` — `pass` — The metadata carries case-study/abt/sv and the actual trace loads the selected case and only ABT, with Swedish scopes resolved explicitly; the default originates with the baseline genre for Write and the input metadata for Redline.
  - `T2` — `pass` — The need for shared information, category-preparation burden and qualified decision form a restrained arc; no miraculous rescue, satisfaction increase or software-caused improvement is invented.
  - `R2` — `pass` — Trace items_4–6 load common base, case-study, quotation guidance, Swedish composition and ABT; no review half or peer editorial pass runs.
  - `O1` — `pass` — Entire-root inventories and executed temporary-directory cleanup establish preserved source/resources and no surviving Skill scratch.
- **unresolved findings** — The delivery account names absent supplier comparison and absent cost, satisfaction and completion-time measures. The evaluator identifies the translation flaw.
- **defects filed** — [#341](https://github.com/Kntnt/skills/issues/341).
- **notes** — Several idiomatic translations could satisfy L1, and the quotation need not be retained in every valid draft. This observation does not itself justify an additional blanket instruction. Candidate wording was not consulted for this judgement.

