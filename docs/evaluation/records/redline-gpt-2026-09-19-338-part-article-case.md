# Candidate evaluation: redline, article and customer case

- **record** — `redline-gpt-2026-09-19-338-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #338, part of #329
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`; each native turn context is checked below
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commits** — `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd` for the first five cases; `f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9` for case-study-en_US; `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd` for article-abt/article-pac. F8 clarifies translated quotations; 1a4 also clarifies review responsibility for whole-sentence repetition and visible quoted idiom. Per-case traces preserve exact bytes.
- **method** — Frozen editorial-quality matrix; no other provider's results consulted. Every input/output is synthetic. This record is the article/case-study part of the candidate matrix, including article ABT and PAC.

## article-sv

- **fixture** — article-sv
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; final artifact is the complete supplied draft, preserved under `editorial-329/runs/candidate/article-sv/redline/`.
- **side effects** — No work/export/scratch changes; transient UV directories removed in scoped commands. Native home bootstrap/cache/session/database effects inventoried, authentication unchanged. Evaluator root cleanup recorded.
- **criteria** —
  - G1 — pass — The focused account of what four weeks of measurement establishes is retained.
  - G2 — pass — Distinct ingress and deployment lead, informative sections, conditional follow-up and no invented byline remain.
  - P1 — pass — Definition and placement explanation still precede the methodological conclusions.
  - W1 — pass — Intelligible section entries and cohesive varied paragraphs survive unchanged.
  - L1 — pass — Natural Swedish professional register is retained.
  - L2 — pass — Final Swedish mechanical pass found no errors; artifact inspection agrees.
  - T1 — pass — Article/none/sv metadata respected; actual base, genre, web-craft and three language scopes loaded, no technique resource.
  - R1 — pass — Every claim and quotation is byte-identical to the input; no taste-driven finding or unavailable-source check.
  - R2 — pass — Trace establishes full scoped review, zero unnecessary corrections and one installed Proofread invocation with mechanics scope; no edit afterwards.
  - O1 — pass — Source unchanged and no surviving Skill output in inventoried writable roots.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Native identity `gpt-6-astra/high`; no correction child was needed. Full response, trace, input/final artifact, disk evidence and cleanup remain with the case.

## article-en_GB

- **fixture** — article-en_GB
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; complete supplied draft remains final in `editorial-329/runs/candidate/article-en_GB/redline/`.
- **side effects** — No work/export/scratch changes. Temporary directories cleaned in executed commands; native home bootstrap/cache/database/session effects inventoried. Authentication unchanged; evaluator root removed after capture.
- **criteria** —
  - G1 — pass — Focused measurement explanation remains useful to municipal property managers.
  - G2 — pass — Complementary ingress/lead and useful final recommendation retained; no invented byline.
  - P1 — pass — Operative temperature explained before naming; count and scope limitations remain explicit.
  - W1 — pass — Clear counts/measurement/action sections and cohesive paragraphing preserved.
  - L1 — pass — Idiomatic British explanation and natural translated quotation retained.
  - L2 — pass — Inspection agrees with the final British mechanics pass: consistent locale conventions.
  - T1 — pass — Metadata article/none/en_GB respected; no technique read, only selected genre plus bounded web support.
  - R1 — pass — Byte-identical final artifact preserves every claim, qualification and quotation; no editorial finding was fabricated.
  - R2 — pass — Full review resources and three language scopes loaded; zero corrections, exactly one installed Proofread invocation and mechanics load, no later substantive edit.
  - O1 — pass — Input unchanged and no surviving Skill file anywhere in the inventory.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Native identity checked in the consolidated audit; no correction child needed.

## article-en_US

- **fixture** — article-en_US
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; supplied article preserved as final in `editorial-329/runs/candidate/article-en_US/redline/`.
- **side effects** — No work/export/scratch changes; scoped transient directories removed. Only native home bootstrap/cache/session/database changes inventoried. Authentication unchanged; evaluator removed root.
- **criteria** —
  - G1 — pass — Useful distinction between measurement and explanation remains central.
  - G2 — pass — Complete article form and differentiated ingress/lead retained.
  - P1 — pass — Air versus operative temperature and limits on the count remain intelligible and proportionate.
  - W1 — pass — Informative headings and coherent sections preserve scanning and continuous reading.
  - L1 — pass — Natural American explanation and quotation retained without gratuitous editing.
  - L2 — pass — American dates, spelling and quotation punctuation remain consistent after the installed mechanical pass.
  - T1 — pass — None metadata honoured in actual loading; only article and bounded support loaded.
  - R1 — pass — Final artifact equals input byte for byte; claims, quotation, qualifiers and formatting unchanged.
  - R2 — pass — Full review contract and language scopes loaded; no needless correction; one Proofread shim with omitted operand, shared/local mechanics, no edit afterwards.
  - O1 — pass — Source unchanged and no enduring Skill file across inventoried roots.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Native identity covered in consolidated audit; no correction child needed.

## case-study-sv

- **fixture** — case-study-sv
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; final artifact remains supplied customer case under `editorial-329/runs/candidate/case-study-sv/redline/`.
- **side effects** — No work/export/scratch changes; transient UV directories removed. Native home bootstrap/cache/database/session effects inventoried, authentication unchanged. Evaluator root cleaned.
- **criteria** —
  - G1 — pass — Customer agency and qualified appraisal remain, with supplier publication disclosed.
  - G2 — pass — Complete case structure and accurate optional checklist action retained.
  - P1 — pass — Assignment median retains its workload/causal caveat and remains distinct from completion.
  - W1 — pass — Scannable sections and distinct ingress/body preserve the customer account.
  - L1 — fail (qualitative concern) — “innan nästa byggnad börjar” remains an unidiomatic literal transfer; the reader must supply the missing rollout activity.
  - L2 — pass — Swedish locale mechanics remain correct; Proofread appropriately makes no stylistic repair.
  - T1 — pass — Case-study/none/sv metadata respected; selected resources and three language scopes loaded, no technique.
  - R1 — fail — Visible L1 obstruction was neither repaired nor reported; this is an unresolved required editorial defect, not absent-source verification. Every claim and quotation otherwise remains byte-identical.
  - R2 — pass — Full review contract loaded; no correction round. One fresh mechanical_pass child reads installed Proofread SKILL, invokes its shim once with omitted operand, loads shared/Swedish mechanics and returns no-change; parent edits nothing afterwards.
  - O1 — pass — No source change or surviving Skill artifact across all inventories.
- **unresolved findings** — Skill reported none; evaluator’s L1 finding remains unreported.
- **defects filed** — #341, candidate repetition and missed editorial diagnosis.
- **notes** — Both parent and mechanical child native contexts are `gpt-6-astra/high`. No source package or expected finding was supplied to Redline. This observation remains even if a later rerun passes.

## case-study-en_GB

- **fixture** — case-study-en_GB
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete corrected case with a separate removal account, retained under `editorial-329/runs/candidate/case-study-en_GB/redline/`.
- **side effects** — No work/export/scratch changes survive; scoped transient UV directories removed. Two shell cleanup forms were denied before successful Python temporary-directory forms. Native home effects inventoried, authentication unchanged; evaluator root removed.
- **criteria** —
  - G1 — pass — Customer agency and qualified voice retained.
  - G2 — pass — Case’s functional parts and precise checklist destination remain.
  - P1 — pass — Visible result limitations remain; the source-only chronology mismatch is not diagnosable from this artifact.
  - W1 — pass — The quotation now contributes its own advice without a pre-echo in the narrative; cohesive paragraphing remains.
  - L1 — pass — Native British narrative and original English customer voice retained.
  - L2 — pass — British conventions preserved; final mechanical pass changed nothing.
  - T1 — pass — Case-study/none/en_GB metadata and actual selected-resource loads agree; no technique resource.
  - R1 — pass — Only “For Lind, the preparation involved work that another building would also need time to do” became “Lind said:”. The same advice remains in the quotation. Every other claim and quotation is unchanged; the removal is explicitly reported.
  - R2 — pass — Full parent and fresh correction-child base/genre/web/anti-slop/language loads established in native traces; one correction and re-review, then one installed Proofread shim with shared/local mechanics, no later substantive edit.
  - O1 — pass — Input unchanged, no enduring Skill file in any inventoried writable root.
- **unresolved findings** — Skill reports none. Source-aware evaluator notes Write’s September commencement error remains; Redline was not given the evidence needed to detect it.
- **defects filed** — #344 belongs to Write’s source-fidelity result, not a Redline failure.
- **notes** — Parent and fresh correction child expose gpt-6-astra/high. Complete input/output diff and removal account support the preservation judgment.

## case-study-en_US

- **fixture** — case-study-en_US
- **instruction commit** — f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete corrected case and explicit two-claim removal account in `editorial-329/runs/candidate/case-study-en_US/redline/`.
- **side effects** — No work/export/scratch changes survive. Initial shell cleanup commands were denied and safely retried with scoped Python temporary directories. Native private-home effects inventoried; authentication unchanged. Evaluator root removed.
- **criteria** —
  - G1 — pass — Customer agency and qualified perspective remain the focus.
  - G2 — pass — Functional case parts, supplier disclosure and correct checklist action retained.
  - P1 — pass — Median limitations, report exclusions and conditional expansion preserved.
  - W1 — pass — Removing pre-echoed appraisal and a repeated next-decision sentence improves economy without imposing headings or a template.
  - L1 — pass — Native American prose and complete original quotations remain intact.
  - L2 — pass — American conventions preserved; actual final Proofread returned no-change.
  - T1 — pass — Case-study/none/en_US metadata honoured in parent and correction resource loading.
  - R1 — pass — Only the appraisal pre-summary became “Lind said:” and the redundant “That leaves Elm Quay with a specific question...” sentence was deleted. Both meanings remain in adjacent quotation/specific next step; every other claim/quote is unchanged. Both removals reported.
  - R2 — pass — Parent and fresh correction child loaded full bounded contracts. One correction, re-review, then one fresh mechanical child loaded/invoked installed Proofread with shared/local mechanics. No substantive edit followed.
  - O1 — pass — Input unchanged and no enduring Skill file in all inventories.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — All three native sessions expose gpt-6-astra/high; comparison of complete input/output supports the narrowly reported removals.

## article-abt

- **fixture** — article-abt
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete corrected article, preserved in `editorial-329/runs/candidate/article-abt/redline/`; one word changed in the faulty heading.
- **side effects** — No work/export/scratch changes. Denied shell cleanup form replaced with scoped Python temporary directory; native home changes inventoried, authentication unchanged, evaluator root removed.
- **criteria** —
  - G1 — pass — Clear measurement-limits angle and professional explanation retained.
  - G2 — pass — Article’s distinct parts and noncommercial useful conclusion retained.
  - P1 — pass — “hur eleverna frös” becomes “om eleverna frös”, restoring agreement with the body’s explicit uncertainty.
  - W1 — pass — Useful headings and cohesive explanatory paragraphs unchanged except the semantic repair.
  - L1 — pass — Natural Swedish professional register retained.
  - L2 — pass — Installed final Swedish mechanics pass makes no changes; inspection agrees.
  - T1 — pass — Metadata ABT honoured, only selected technique and its review loaded in parent/child.
  - T2 — pass — Situation, genuine question and supported next investigation still form a calm arc; early ingress result left in place.
  - R1 — pass — Exactly the named heading defect repaired (hur→om); all other wording, claims, quotation and metadata remain identical. No passage was deleted or unrelated claim lost.
  - R2 — pass — Full scoped parent/fresh correction-child contracts loaded, one correction and re-review, then exactly one installed Proofread invocation with shared/local mechanics; no substantive change after it.
  - O1 — pass — Input unchanged and no surviving Skill file anywhere in inventoried roots.
- **unresolved findings** — none
- **defects filed** — #347 remains the observed Write failure; this Redline outcome repairs its visible contradiction.
- **notes** — Parent and correction child are gpt-6-astra/high. Source was never supplied to Redline. This successful correction does not erase the first-draft failure or guarantee future detection.

## article-pac

- **fixture** — article-pac
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change response; input retained as final artifact in `editorial-329/runs/candidate/article-pac/redline/`.
- **side effects** — No work/export/scratch changes; scoped UV temporary directories removed, native home effects inventoried, authentication unchanged, evaluator root removed.
- **criteria** —
  - G1 — pass — Focused professional account of measurement value and limits preserved.
  - G2 — pass — Complete article form and distinct explanatory opening retained.
  - P1 — pass — Facts lead through duration/location limits to a proportionate recommendation.
  - W1 — pass — Clear section entries and coherent paragraphs retained without template-driven changes.
  - L1 — pass — Natural British narrative and translated quotation retained.
  - L2 — pass — Final installed British mechanics pass correctly retains valid dash/quotation choices.
  - T1 — pass — Metadata PAC governs actual PAC base/review loading; ABT absent.
  - T2 — pass — Descriptive facts are accepted as a premise, analysis earns the conclusion; no invented thesis or counterargument demanded.
  - R1 — pass — Every word, claim, qualification, quote and metadata byte preserved; no taste-driven finding.
  - R2 — pass — Full review resources and three language scopes loaded; no unnecessary correction; exactly one installed Proofread shim and shared/local mechanics pass, no later edit.
  - O1 — pass — Input unchanged and no enduring Skill file in all inventories.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Native identity covered in consolidated audit; no correction child required.

