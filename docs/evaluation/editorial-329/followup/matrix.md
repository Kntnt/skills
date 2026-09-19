# Supplementary fidelity matrix

Freeze this matrix and its new source packages in a commit before changing product instructions or running its cases. The original corpus at `6e531f5` and its criteria remain unchanged. Starting product revision: `7ff6ec0`. This matrix supplements the completed original matrix; it does not reclassify earlier failures.

## Runs fixed in advance

Every candidate row is a fresh native Write invocation followed by a separate fresh, source-blind Redline invocation. Use the existing isolated `harness/run.py`, preserving full responses, extracted complete artifacts, native parent/child traces, all-root inventories and cleanup. Each repetition is independent. Candidate and baseline use the same inherited observed GPT identity, invocation and source. No model overrides, quality hints or rubric reach the invoked Skill.

| Source | Genre / locale | Candidate repetitions | New baseline repetitions |
|---|---|---:|---:|
| Original opinion | opinion / sv | 2 | 2 |
| Original opinion | opinion / en_GB | 2 | 0 |
| Original opinion | opinion / en_US | 2 | 0 |
| Original customer case | case-study / en_US | 3 | 2 |
| Original customer case | case-study / sv | 2 | 0 |
| `fixtures/opinion-unknown-sv.md` | opinion / sv | 2 | 1 |
| `fixtures/opinion-absence-en_GB.md` | opinion / en_GB | 2 | 1 |
| `fixtures/case-unprompted-en_US.md` | case-study / en_US | 2 | 1 |
| `fixtures/case-question-en_GB.md` | case-study / en_GB | 2 | 1 |
| Original article | article / sv | 1 | 0 |
| Original column | column / sv | 1 | 0 |
| Original web-copy | web-copy / en_US | 1 | 0 |
| Original article, same brief/material | general / en_GB | 1 | 0 |

Total: **23 candidate Write + 23 paired Redline + 8 baseline Write = 54 Skill invocations**. The two earlier neutral replay probes are diagnostic experiments, not part of this count. Baseline Redline is unnecessary for the source-aware comparison and is not claimed. The general row tests the changed Write workflow outside the shared five-genre loading path; the supplied article brief still supplies its requested form.

Invocations retain the original form: `/write --genre=<genre> --language=<locale> --output=response source.md`, then `/redline --output=response input.md`. Only the complete Write artifact, including metadata, is copied into `input.md`; source, delivery account, checker findings and evaluator judgement are excluded.

## Judgement

Apply every original matrix criterion applicable to each Skill: F1/G1/G2/P1/W1/L1/L2/T1/R2/O1 for Write; G1/G2/P1/W1/L1/L2/T1/R1/R2/O1 for Redline. T2 applies if a non-five genre selects a technique. Source-aware evaluation also checks whether the final paired artifact preserves source fidelity, without treating missing source knowledge as a Redline failure. Unknown information remains unknown; warranted certainty remains warranted; supported interview circumstances are allowed. Optional facts and particular words are not mandatory.

Add **S1** for a candidate source-check workflow: actual trace establishes complete source and candidate access, a checker independent of composition, bounded execution, support for accepted corrections, and verification of the final prose before delivery. A checker's approval is process evidence, never an F1 pass by itself. Record detection, parent repair and delivered-text judgement separately. Preserve any precheck draft available in the native trace.

For baseline S1 is not applicable, since no independent check was promised. Historical R2's ban on loading editorial review halves and peer editorial passes remains; a bounded source-fidelity comparison is the explicit workflow change being evaluated, not an unreported relaxation. No literary or semantic criterion is weakened.

Compare baseline and candidate only after each has been judged independently. Report observed rates with denominators for each defect class, not a statistical reliability guarantee. Candidate verification requires repeated repair or prevention on original failures, successful transfer to the new cases, preserved supported details and voice, and no unreported source or filesystem failures. An isolated later pass cannot erase a fail. Additional attempts after a product change are recorded separately and rerun the affected cases; they never silently replace this matrix.

#341 is a separate idiom outcome. A source check that approves its meaning does not resolve L1. Judge the two Swedish customer cases and the existing frozen source-blind case control separately before deciding its disposition. Run that unchanged Redline control once after any idiom-specific repair; it is conditional additional coverage, not included in the 54.
