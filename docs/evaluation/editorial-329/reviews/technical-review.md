# Technical Standards/Spec review — #329

Reviewed on 2026-09-19 against start revision `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`, including the working changes on `editorial-329` above `6e531f5fe0b610e046ae58787f246cc6239acbcc`. The latter is the frozen corpus revision, not an immutable revision of the candidate instructions. This is an independent read-only review of the implementation; the reviewer changed only this report.

Sources: the complete captured #329–338 issue threads under [sources](../sources/), the execution handoff at `/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-329-astra-hi-handoff-8whdfn23.md`, `AGENTS.md`, the relevant general/Python/Skill/document rules, editorial and language format contracts, `CONTRIBUTING.md`, and the evaluation protocol. The later requester clarifications govern over the earlier detailed checklists. The review used the Standards/Spec distinction and writing-for-agents guidance; it did not treat personal stylistic preferences as requirements.

## Standards

**Hard findings: none identified in the reviewed implementation.**

The support pair lives outside the two selectable directories. Genre openings still identify the genre before the support pointer, and neither help expansion nor genre inference needs to open the support to identify a choice. Write, Redline and the correction brief enumerate the same exact five genres and the same bounded support files. Write excludes review halves; Redline and correction include both. The new format rule is represented in `docs/rules/skills.md` and the editorial README rather than left solely in a Skill body.

The base/review split remains usable: outcomes reside in base resources and diagnostics concern visible text. The review files do not introduce a new source-verification responsibility. The ordinary technique sections retain their machine-readable form; defaults outside the five remain intact. Report's PAC explanation and the active corpus description were updated to the broader factual-premise meaning. Teaser changes establish the ingress boundary without importing its full contract into article or case-study.

The evaluator harness exports immutable instruction bytes into private installations, retains failed evidence, registers its process group and scratch root, and inventories the full staged roots. Its final run records and cleanup still need inspection after execution; this review does not establish those outcomes. No provider evaluation or repository test was run by this reviewer.

## Spec

**Hard findings: none identified in the reviewed implementation. Pending verification is not counted as acceptance.**

The shared craft brief establishes the requested professional traditions and assigns idiom/syntax/typography to the target language. Only `en_US` composition changes, removing the conflicting structural/register prescription. Genre briefs retain the required differences: article's ingress/lead and conditional byline; customer agency, appraisal and quotation boundaries; column's personal reflection; opinion's early position and accountable action; web-copy's task, conditions and real action consequences. Advisory web dimensions explicitly allow successful departures without permission or explanation.

The five default to none without new flag grammar. The existing flag → recognized metadata → instruction/context precedence is preserved, including legacy ABT metadata. ABT and PAC now describe their relationships without forced crisis, falsifiable premise, section quota or hidden opening answer. Explicit selection still imposes real relationships at the level the genre permits.

For #339, Redline step 9 now gives Proofread only `--language=<resolved> --output=response` as the Formal Invocation and supplies the entire artifact separately under Proofread's existing omitted-operand contract. This directly removes YAML and flag-like artifact text from the parser payload without changing the parser, bypassing the installed Skill, introducing a file, or authorizing a second pass. Proofread already accepts an omitted operand and preserves frontmatter byte for byte. **A successful real metadata-bearing candidate pipeline and trace remain necessary evidence before #339 is complete.**

## Judgement, separate from defects

The combined editorial resources are substantially shorter, with useful role/form direction rather than an exhaustive checklist. [Reading-load accounting](../reading-load.md) includes language scopes, anti-slop, operational instructions and the correction boundary, and distinguishes conditional quotation and selected-technique costs. The remaining operational and language loads are significant; that fact alone is not a violated word limit or a reason to add another rule.

One wording tension merits observation rather than a mandatory edit: `editorial/anti-slop.md` ends its generic-conclusion diagnostic with an absolute instruction to remove a weak closing metaphor instead of improving it. A column whose closing image contains its reflective point could tempt an overbroad deletion. However, that catalogue's opening, the new base review and correction preservation contract explicitly protect useful voice and claims. There is insufficient evidence here to classify this as a hard contradiction; use the frozen preservation controls to assess actual behaviour, without turning this concern into another blanket instruction.

## Completion boundary

The implementation is suitable to proceed to the already-required evaluation. This review does **not** certify #338, the final catalog digest, the four CONTRIBUTING checks, cleanup, or the final integrated revision. Final acceptance needs the complete declared matrix, separate Write/Redline records, observed loading and correction/Proofread traces, claim-preservation comparisons, preserved failures and affected reruns, followed by review of any material late changes. No conclusion about the other provider family is made.

## Late-change inspection checkpoint

Independently read the full changed resources through `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`, including column/opinion author-perspective boundaries, translated quotation guidance, web-copy physical-interface descriptions, whole-sentence duplication ownership and case-study quoted idiom. No new hard implementation contradiction identified. The revised paragraphs refine existing responsibilities without adding a separate checklist or a source-verification obligation. Final behavioural coverage and reading-load regeneration remain pending at this checkpoint.

The final column-sv and column-en_GB Write artifacts retain the supplied observation and irritation without claiming the author has that thought habit herself. The distinction is semantic: “That is my own irritation” attributes the supplied response, whereas the failed “I find myself regarding” attributed the practice to the author.

### Swedish colon capitalisation: observed boundary concern

The column-sv final pipeline changed only `en fråga bredvid tiden: vad behöver vi förstå tillsammans?` to `...: Vad behöver ...?` via installed Proofread. This changes no claim and is not substantive editorial rewriting. Nevertheless, the reviewer cannot establish that the original was an objective error under the loaded contract. Swedish Mechanics has no specific colon-capitalisation rule; shared Mechanics requires sentence-opening case for a quotation introduced as an utterance, while this unmarked question can also be read as a specification integrated with its host. [Språkrådet’s Frågelådan](https://frageladan.isof.se/faqs/25422) calls capitals usual for speech-like questions and permits lowercase for a closely connected complete explanatory sentence. Capitalisation is a defensible choice, but necessity is not demonstrated. Proofread step 8 requires preservation where the loaded rules do not identify an error. Record this as a limited mechanical-preservation concern, not a claim loss or an unconditional substantive-mechanics rejection, and do not silently turn a preference into a new normative checklist.

The colon-variation concern is tracked as [#348](https://github.com/Kntnt/skills/issues/348); parent requested a bounded Swedish Mechanics clarification and exact-input regression. It is an observed preservation defect, while its lack of claim loss keeps it distinct from the protocol's unconditional substantive-mechanics rejection. Final regression pending.

### Explicit web-copy ABT trace: unnecessary discovery

On `1a4f65b`, `runs/rerun-345/web-copy-abt/redline/trace.jsonl` item 6 reads the heading and definition of every installed genre despite complete usable `genre: web-copy` metadata. Redline Resolution suppresses lower levels when metadata settles a value and scopes this discovery to genre inference; it distinguishes those openings from loading a full genre contract. Selection itself remains correct and only web-copy/ABT full contracts load afterward. The text passes all applicable content/technique criteria and remains byte-identical. The record therefore marks a limited R2 overread separately from text correctness and unconditional contract-rejection categories. No new general rule is inferred from this one unnecessary discovery operation; disposition remains with the integrating parent.

## Final-resource contract reread — 93758f4

Reread the complete shared craft pair, base pair, all five genre pairs, selected-technique pairs, changed quotation and language paragraphs, and the effective Write/Redline/correction/Proofread loading and selection boundaries. Rechecked active help, genre openings/default declarations and repository format rules against the start diff. The final changes remain scoped to the approved normative surfaces and evaluation-discovered boundary repairs. No implementation-level Standards/Spec contradiction was found. The colon clarification occupies Swedish Mechanics, where the more specific locale rule belongs; it does not duplicate Proofread's preservation policy. The knowledge-state sentence refines existing claim strength for all genres instead of prescribing the fixture's funding phrase.

The seven independent selection controls have been reviewed against complete responses and actual loads. Flag→metadata→instruction precedence, explicit none, legacy ABT, factual PAC, report's early answer and the article excerpt all behave as specified. Their native sessions each use gpt-6-astra/high; successful installed Proofread invocation count is one per parent; no full-root changes occur outside native home state. Report's one fresh correction adds only existing year/library references and a section cross-reference warranted by its unchanged report contract. Its encrypted dispatch message is explicitly a method limit, not evidence of an inspectable exact brief.

Final root-owned column artifacts in all three locales preserve the supplied viewpoint and ghostwriting boundary; en_US's hypothetical form complaint develops the supplied opposition to compulsory decisions, rather than inventing a past scene or a personal calendar-as-result habit. The Swedish final-pass variation defect #348 remains separately tracked pending its exact replay. The original failed column and opinion samples are not reclassified as passing merely because later samples improve.

Runtime failures are distinct from static implementation findings: #349 repeats an unsupported absence despite the earlier general claim rule, and #350 unnecessarily reads genre opening definitions despite a metadata-resolved genre. Both remain explicit failures in append-only records. Three fresh opinion pairs and the exact #350 replay are now authorised on 93758f4; until assessed, this review does not mark their coverage complete.

### Source-support completion condition — d0b2c99

The state-of-knowledge sentence was actually loaded but did not prevent #349 in any of the three 93758f4 Write samples: sv and en_US assert absent costing/funding; en_GB preserves unclaimed funding but asserts absent costing. The en_GB sentence is third person. This evidence does not establish first-person pronouns as the cause, and it does not justify treating further genre-voice wording as a proven remedy. Historical reassessment also finds the same defect in baseline opinion-sv and the first candidate samples, so it is not established as a #329 regression.

The d0b2c99 change instead strengthens Write step6's existing completion condition: source support is checked as part of writing the first draft. That phrase keeps the operation within source-aware composition; it neither loads review resources nor invokes Redline/Proofread, so it is compatible with the opening and step8 prohibition on a separate review/proofreading pass. It adds no new editorial quality catalogue, canonical fixture phrase or resource. This is a justified bounded process hypothesis, with effects still awaiting unchanged-source evaluation. A source-aware check cannot be moved to the source-blind Redline stage.
