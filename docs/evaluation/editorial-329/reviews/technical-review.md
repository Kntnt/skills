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
