# Candidate evaluation: write, article and customer case

- **record** — `write-gpt-2026-09-19-338-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #338, part of #329
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`; each native turn context is checked below
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commits** — `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd` for the first five cases; `f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9` for case-study-en_US; `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd` for article-abt/article-pac. F8 clarifies translated quotations; 1a4 also clarifies review responsibility for whole-sentence repetition and visible quoted idiom. Per-case traces preserve exact bytes.
- **method** — Frozen editorial-quality matrix; no other provider's results consulted. Every input/output is synthetic. This record is the article/case-study part of the candidate matrix, including article ABT and PAC.

## article-sv

- **fixture** — article-sv
- **invocation** — `/write --genre=article --language=sv --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete Swedish article, metadata `article/none/sv`, followed by a separate delivery account; preserved in `editorial-329/runs/candidate/article-sv/write/`.
- **side effects** — No work/export/scratch changes survived. Temporary UV directories were scoped and removed in the executed commands. Private home additions were native bootstrap/plugin caches, sessions and databases; config changed through Harness bootstrap. Authentication unchanged. Full inventories retained; evaluator removed the private root after capture (`cleanup.json`).
- **criteria** —
  - F1 — pass — The article retains 14/120 sessions, local 20-degree threshold, placement limits, unmeasured causes/comfort, and undecided funding; no count-size or causal inference added.
  - G1 — pass — The angle “vad … lektionspass berättar” serves property managers deciding what a short measurement can establish.
  - G2 — pass — Informative H1, distinct ingress, January deployment lead before H2, no invented byline, explanatory sections and a qualified next investigation.
  - P1 — pass — Sensor locality and operative temperature are explained before the limits are drawn; time-series meaning is supplied inline.
  - W1 — pass — Three informative sections separate counts, measurement scope and next steps; ingress gives the limits while the lead begins the actual deployment.
  - L1 — pass — Natural Swedish such as “ringat in tillfällen att följa upp” supports a measured professional explanation.
  - L2 — pass — Swedish date, speech dash and number/unit forms; no imported locale convention observed.
  - T1 — pass — Metadata says none; trace loads article, base, web-craft and only Swedish composition, no technique.
  - R2 — pass — Native trace reads Write SKILL, invocation shim, delivery, quotations and bounded writing resources; no review or proofreading pass.
  - O1 — pass — Supplied source unchanged; no surviving Skill artifacts in any writable root. Inventory and trace support the account.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Exact native turn context confirms `gpt-6-astra/high`. This draft was judged against its source and the frozen criteria before examining its Redline result.

## article-en_GB

- **fixture** — article-en_GB
- **invocation** — `/write --genre=article --language=en_GB --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full British English article and separate delivery account, preserved in `editorial-329/runs/candidate/article-en_GB/write/`.
- **side effects** — No work/export/scratch changes survived; scoped UV temporary directories removed. Private-home native bootstrap/cache/database/session effects retained in inventories; authentication unchanged. Evaluator cleaned the root after capture.
- **criteria** —
  - F1 — pass — Retains 14/120, the non-legal threshold, no duration/comfort findings, non-experimental placement and undecided funding; the quote translation preserves uncertainty.
  - G1 — pass — “A reading below 20°C is only part of the picture” carries a practical measurement-limits angle for property managers.
  - G2 — pass — Standalone ingress, January deployment lead, informative H2 sections and Rask’s qualified next step perform distinct jobs; no invented byline.
  - P1 — pass — The text explains the combined air/radiant measure before naming operative temperature and keeps placement distinct from perceived comfort.
  - W1 — pass — Three coherent sections support entry at counts, measurement limits or actions without duplicating the whole opening.
  - L1 — pass — “keep attention on the time that matters to the enquiry” and “take a closer look” are idiomatic British explanation, without Swedish syntax.
  - L2 — pass — British enquiry, draughts, caretaker, 12 March date and single-quote convention used consistently.
  - T1 — pass — Metadata article/none/en_GB; trace loads only article/base/web-craft and British composition, no technique.
  - R2 — pass — Actual reads include Write SKILL, shim, delivery and quotations; no review resources or peer pass.
  - O1 — pass — Input preserved, no surviving Skill files; full root inventories and executed cleanup support this.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Source-to-English transformation judged independently before its Redline result; native identity is checked with the consolidated trace audit.

## article-en_US

- **fixture** — article-en_US
- **invocation** — `/write --genre=article --language=en_US --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete American English article with metadata and a separate delivery account, retained under `editorial-329/runs/candidate/article-en_US/write/`.
- **side effects** — No work/export/scratch changes remain; transient UV directories removed. Native home/bootstrap/cache/session/database effects inventoried; authentication unchanged. Evaluator removed isolated root after capture.
- **criteria** —
  - F1 — pass — Preserves the lesson denominator, local threshold, air-only measurement, placement and funding limitations, and unmeasured effects; quote translation retains “don’t yet know”.
  - G1 — pass — Counts, measurement limits and a cautious next step make a useful focused property-management article.
  - G2 — pass — Informative H1, separate ingress, deployment lead and explanatory H2 sections; conclusion follows Rask’s supported recommendation.
  - P1 — pass — Operative temperature receives an immediate definition and is distinguished from what the sensors actually measured.
  - W1 — pass — Cohesive short paragraphs and useful headings allow scanning without breaking the methodological explanation.
  - L1 — pass — “periods that deserve closer attention” and “before deciding how to respond” form native professional English without imported Swedish phrasing.
  - L2 — pass — March 12, drafts, students/custodian and American double quotation marks are locally consistent.
  - T1 — pass — Article/none/en_US resolved and loaded; no technique read despite a natural question-to-answer progression.
  - R2 — pass — Write SKILL/shim, bounded base/genre/web-craft, composition, delivery and quotations read; no review half or peer pass.
  - O1 — pass — Supplied source unchanged; full-root inventory shows no enduring Skill files.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Independently judged against source before Redline; identity checked in consolidated native audit.

## case-study-sv

- **fixture** — case-study-sv
- **invocation** — `/write --genre=case-study --language=sv --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete Swedish customer case, metadata case-study/none/sv and separate account; preserved under `editorial-329/runs/candidate/case-study-sv/write/`.
- **side effects** — No work/export/scratch changes; scoped UV temporary directories removed. Native private-home bootstrap/cache/session/database effects inventoried; authentication unchanged. Evaluator removed root.
- **criteria** —
  - F1 — pass — The trial’s agency, eight weeks, 31 reports/exclusions, assignment-versus-completion distinction, workload/causal caveat and customer reservation remain; no satisfaction or benefit invented.
  - G1 — pass — Customer decisions and Maya Lind’s own qualified appraisal carry the account, while supplier publication is explicit.
  - G2 — pass — Result headline, standalone ingress, customer context, choices, implementation, measured result, appraisal and accurate checklist link all function without a sales template.
  - P1 — pass — Two-versus-three-day median is separated from causality and completion; the next expansion decision remains conditional.
  - W1 — pass — Clear opening and two later sections organise experience, measurement and next decision; quote bridges add context without repeating the full speech.
  - L1 — fail (qualitative concern) — “Jag skulle avsätta den tiden innan nästa byggnad börjar” transfers the English construction literally: the Swedish reader must reconstruct which activity in the building starts. This is an idiom defect, not a fabricated fact or mechanical misspelling.
  - L2 — pass — Swedish quotation dashes, date and compound forms; the L1 defect is not a locale-mechanics error.
  - T1 — pass — None metadata and actual no-technique loading; selected case/base/web-craft plus Swedish composition only.
  - R2 — pass — Write SKILL/shim, complete bounded writing contract, quotation policy and delivery read; no review or Proofread invoked.
  - O1 — pass — Input untouched, no surviving Skill artifacts in all inventoried writable roots.
- **unresolved findings** — L1 translated interview idiom remains in this first draft.
- **defects filed** — #341, repeated candidate evidence of the already filed class.
- **notes** — Independent source/rubric judgement was made and reported before #341 was opened for comparison. The candidate repeats the same faulty phrase as that issue’s baseline evidence; no baseline output was supplied to the model. All other customer voice and content were preserved. Native identity covered by consolidated audit.

## case-study-en_GB

- **fixture** — case-study-en_GB
- **invocation** — `/write --genre=case-study --language=en_GB --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete British customer case and separate account, preserved under `editorial-329/runs/candidate/case-study-en_GB/write/`.
- **side effects** — No work/export/scratch changes; scoped transient UV directories removed. Native home bootstrap/cache/session/database effects inventoried; authentication unchanged. Root removed by evaluator.
- **criteria** —
  - F1 — fail (unsupported fact: chronology) — “Before the trial began in September 2025” dates commencement to the month the source assigns only to the decision. Source gives eight-week duration but no start date. Other measures, exclusions and quotations retain their limits.
  - G1 — pass — Customer agency, preparation effort and qualified appraisal drive the story rather than supplier praise.
  - G2 — pass — Benefit headline, ingress, context, implementation, results, appraisal and accurate checklist next step all present. No independent-reporting claim is made; delivery identifies supplier publication.
  - P1 — pass — The account distinguishes assignment from completion and preserves the different-workload caveat; conclusions otherwise remain proportionate.
  - W1 — pass — Short cohesive paragraphs and discrete customer quotations orient a roughly 400-word account without mandatory H2 sections; chronological reading stays clear.
  - L1 — pass — The supplied English quotations retain their natural register and the narrative reads as native British prose.
  - L2 — pass — Trialled, flats, organising, 4 December date and consistent double quotes are established British choices.
  - T1 — pass — Case-study/none/en_GB and corresponding selected resources; no technique loaded.
  - R2 — pass — Full bounded Write contract and quotation policy loaded; no review or Proofread pass.
  - O1 — pass — Input unchanged, no surviving Skill artifacts in inventoried roots.
- **unresolved findings** — Unsupported trial commencement date in September 2025.
- **defects filed** — #344 (linked to #329).
- **notes** — This is source-aware F1 evidence; the draft contains no internal fact exposing the date shift to Redline. Existing Source Fidelity already names chronology, so no additional rule is justified by this sample alone. A later successful rerun cannot establish guaranteed repair.

## case-study-en_US

- **fixture** — case-study-en_US
- **instruction commit** — f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9
- **invocation** — `/write --genre=case-study --language=en_US --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full American customer case and separate account in `editorial-329/runs/candidate/case-study-en_US/write/`.
- **side effects** — No work/export/scratch changes; temporary UV directories removed. Native home effects inventoried, authentication unchanged. Evaluator root removed.
- **criteria** —
  - F1 — pass — September dates the decision to test; 640 apartments, eight weeks, 31 reports/exclusions, medians and workload/causal limits remain exact. Original quotations and qualified appraisal preserved.
  - G1 — pass — Team choices and preparation experience carry the story, with Svale third-person support.
  - G2 — pass — Benefit headline, distinct ingress, customer context, implementation, results, appraisal and actual checklist function all supplied; supplier publication explicitly disclosed.
  - P1 — pass — Assignment/completion distinction and undecided expansion remain clear; no causal inference added.
  - W1 — pass — Compact paragraphs and quotations support a continuous short account without compulsory section headings.
  - L1 — pass — Native American narrative (“follow reports across shifts”) and preserved natural English customer speech.
  - L2 — pass — Apartments, staff members, December 4 and American quotation punctuation consistent.
  - T1 — pass — Case-study/none/en_US and actual selected-resource loading agree; no technique.
  - R2 — pass — Full bounded Write contract including updated quotation policy loaded; no review or peer pass.
  - O1 — pass — Input preserved and no surviving Skill artifacts in all inventories.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — English source needs no quotation translation; no unsupported trial-start date appears. Native identity checked in consolidated audit.

## article-abt

- **fixture** — article-abt
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/write --genre=article --technique=abt --language=sv --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete Swedish ABT article and separate account, retained under `editorial-329/runs/candidate/article-abt/write/`.
- **side effects** — No work/export/scratch changes, scoped UV temporary directories removed; native home effects inventoried, authentication unchanged, evaluator root removed.
- **criteria** —
  - F1 — fail (unsupported fact: presupposed experience) — H2 “Lufttemperatur berättar inte hur eleverna frös” presupposes cold pupils; source establishes neither whether pupils felt cold nor how. The body correctly retains the uncertainty.
  - G1 — pass — Focused practical measurement explanation remains useful; no manufactured crisis.
  - G2 — pass — Informative H1, standalone ingress, lead, explanation and qualified ending are distinct.
  - P1 — fail — The heading’s “hur eleverna frös” contradicts the section’s “Rapporten säger heller inte om eleverna frös”; the reader receives incompatible degrees of knowledge.
  - W1 — pass — Coherent sections and complementary ingress/lead support scanning and sustained explanation; numerical proportions are not used as thresholds.
  - L1 — pass — The Swedish is idiomatic; the heading fault is semantic certainty, not translation syntax.
  - L2 — pass — Swedish date, speech dashes and number/unit expressions remain correct.
  - T1 — pass — Formal ABT flag, metadata abt and actual ABT base loading agree; no PAC/review loaded.
  - T2 — pass — Situation and measured periods lead through real limits to linking readings with room use; no crisis, triumph or mandatory scene imposed.
  - R2 — pass — Full bounded Write/genre/web/composition/quotation contract loaded; no peer review or proofreading pass.
  - O1 — pass — Source unchanged, no enduring Skill artifact in any inventoried writable root.
- **unresolved findings** — Unsupported presupposition in the quoted H2 remains in this first draft.
- **defects filed** — #347 (linked to #329).
- **notes** — Existing base/Source Fidelity already protects headline claims and certainty; this observed failure does not itself justify another blanket rule. Redline receives the unaltered draft without a hint.

## article-pac

- **fixture** — article-pac
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/write --genre=article --technique=pac --language=en_GB --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full British PAC article and separate account under `editorial-329/runs/candidate/article-pac/write/`.
- **side effects** — No work/export/scratch changes, scoped UV temporary directories removed; native home effects inventoried, authentication unchanged; evaluator root removed.
- **criteria** —
  - F1 — pass — Count/denominator, unknown duration/comfort, local threshold, placement limits and undecided funding retained. Translated Rask quotation preserves its uncertainty and meaning.
  - G1 — pass — Focused explanation of what measurement establishes serves council property managers without promotion.
  - G2 — pass — Informative H1, standalone ingress, concrete deployment lead, explanatory body and supported next step all work separately.
  - P1 — pass — “A lesson count does not show duration” follows the reported facts; sensor locality and operative temperature clarify what cannot be concluded.
  - W1 — pass — Three clear sections and cohesive paragraphs permit scanning without losing the analytical argument.
  - L1 — pass — “brief dip”, “closer attention” and “funding remains undecided” are natural British phrasing, not translated Swedish syntax.
  - L2 — pass — British date, draughts, pupils/caretaker and single quotation marks consistent; em-dash house style is an established British option.
  - T1 — pass — PAC selected by flag, recorded in metadata and loaded alone; ABT absent.
  - T2 — pass — Given facts lead through duration/location/thermal limits to connecting readings and occupancy. No manufactured thesis or counterargument; early summary remains compatible with analysis.
  - R2 — pass — Actual Write/shim, bounded contract including PAC and translated-quotation policy, composition/delivery loads; no review or peer pass.
  - O1 — pass — Input unchanged, no enduring Skill artifact across all inventories.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Judged independently before Redline. Native identity covered by consolidated audit.

