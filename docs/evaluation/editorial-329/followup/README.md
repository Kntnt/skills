# Source fidelity follow-up — #329

Thomas approved reopening #329 with #349 and #352 blocking quality completion; #341 follows at lower priority. Starting revision: `7ff6ec0`. Original corpus and failed outputs remain immutable. This directory contains supplementary diagnosis and evaluation, not replacements for the first delivery.

## Diagnosis plan

1. Reconfirm original failures from the preserved complete sources and outputs. The existing native pipeline is the red-capable loop; model runs take minutes and semantic judgement cannot be reduced to a deterministic seconds-long text assertion. That limitation justifies using frozen replay probes rather than claiming a unit test establishes prose fidelity.
2. Ranked hypotheses: (H1) composing and self-checking share a completion decision that prematurely accepts the draft; a fresh source-aware checker should detect failures the writer delivered. (H2) checking focuses on prominent numbers/quotes and misses implications and narrative circumstances; an explicit claim-to-support check should improve both patterns. (H3) the source is pragmatically misread, not overlooked; a fresh comparison would repeat the same absent-versus-unknown confusion. Quote idiom is assessed separately.
3. Replay the complete two failed drafts with their sources in fresh native sessions, using a neutral fact-check prompt that names neither issue nor faulty passage. These are diagnostic probes, not Skill evaluations. Preserve all outputs, actual model identity and writable-root inventories.
4. Freeze supplementary cases, repetition counts and outcomes before product changes or candidate runs. Test a bounded repair and assess all original editorial criteria plus source-check execution, without new style prescriptions.

## Tracker

#329 reopened: https://github.com/Kntnt/skills/issues/329#issuecomment-5744979279. Before-state threads are preserved in `tracker/`.

## Replay result

Both neutral source-aware replay probes detected exactly the original unsupported claim without an issue hint: the opinion checker distinguished no claim from no work, and the case checker rejected the invented request to assess. Responses are preserved in `probes/`; both private roots were inspected and removed. The probes took 20.92 and 18.35 seconds. They establish a viable detector seam, not end-to-end repair or general reliability. The original complete examples remain the regression seam; shrinking them would discard genre and context interactions that the final repair must preserve.

The predeclared supplementary run plan is [matrix.md](matrix.md). New source packages were prepared independently and read in full before freezing.

## Candidate mechanism

The candidate replaces unobservable composition-only self-checking with a fresh, read-only source comparison on the inherited seat. The writer owns supported repairs. A changed or disputed draft receives one final fresh comparison; unresolved checking withholds delivery. Sources and checked prose are preserved, reports remain private and are cleaned. This adds subagent capability and latency, which help/README/declarations expose. At that first candidate, no genre rule, source fixture or editorial quality criterion changed. The broad code-preservation quantifier in the Skills rule now explicitly names editorial, anti-slop and mechanical passes, matching its existing subject; source comparison of newly generated claims is a different operation.

The supplementary corpus was frozen at `bf14dc2` before product edits. Original material is still byte-identical to `6e531f5`. Focused loading/account checks passed (3 tests). The external Skill validator reports the same two previously accepted extension-field complaints on baseline and candidate, with no new complaint.

## First candidate result and second candidate

All 54 invocations in the initial supplementary matrix completed. The baseline’s corrected F1 result is 4/8 drafts; the first candidate’s corrected F1 result is 14/23. The later personal-attribution audit supersedes one baseline and two first-candidate passes; their supplied question framing remains supported. The initial 20/23 judgement is preserved and superseded: four English opinion drafts also substitute disability status for functional ability, and three substitute digital skills for familiarity. Three other failures are unsupported supplier-choice dates in the US customer case (#344, reopened). Both Swedish cases retain a quote-translation defect that both paired Redlines miss (#341). All six candidate opinion drafts preserve #349's no-claim boundary; all five customer cases avoid #352's invented question. Preserve the baseline and first-candidate reports as phase-specific evidence.

The first neutral claim-ledger diagnostic also misses the chronology defect: it drops an inherited grammatical modifier while decomposing the sentence. A second neutral diagnostic reconstructs complete propositions with their grammatical scope and tests whether all source material could be true while a draft proposition is false. That diagnostic detects the timing addition without a date or clause hint. A separate neutral quotation-translation diagnostic detects the Swedish idiom obstruction and proposes one supported local repair.

Second candidate `82db439` makes those operations explicit in the bounded checker, gives the checker an exact scratch draft file, and adds a conditional translated-quotation comparison using already-resolved composition guidance. Redline gives reported speech an explicit review unit. Its opinion review now distinguishes advocated targets from factual feasibility predictions (#354); shared delivery owns the unchanged-with-findings exception while leaving unchanged in-place files untouched (#353). Both new issues are children and blockers of #329.

The [second matrix](matrix-second.md) fixes 56 Skill invocations before its results: the same 23 pairs plus ten specific controls. The independent review and full-source judgements remain the completion gate; a checker verdict is never sufficient evidence that an artifact passes. This phase is in progress.

## Findings while the second wave runs

Both new British-English absence-control drafts add a document-wide consent-status claim supported only at the source-package level (#355). The checker either imports an absent qualifier into its reconstruction or compares the wrong subject’s state. A neutral equivalence replay does not catch the mismatch; that failed hypothesis is retained and not copied into runtime guidance. A separate bounded negation experiment tests the precise truth condition.

The three unchanged timetable replays still produce two false-positive objections, now demanding a separate rationale for the exact interval (#354); one is clean. Delivery of unchanged text with findings follows the reconciled contract. Full outcomes remain in progress.

One internal checker deletion of a modest argumentative concession is recorded as a disputed preservation limitation. The final text preserves source facts, author stance and fair presentation of the company’s motives; the deletion is not counted as a demonstrated factual repair.


## Subsequent bounded refinements

The second wave's twelve supplementary/general Write cases finish at F1 10/12: both absence-en_GB outputs add an unsupported assertion about the entire submission (#355). Its delivery controls pass for response, unchanged in-place and separate-file destinations. The qualified-timetable objection still appears in two of three exact replays (#354), and the parent-only reported-speech instruction still misses the frozen Swedish idiom fault (#341). These are retained failures, not replaced by later passing samples.

Third candidate `7b86144d` tests each reconstructed claim's precise negation against supplied evidence and confines opinion findings to premises or inferences actually asserted. All three timetable replays are now clean; the certainty contrast still detects and reports an actual unsupported guarantee. The larger third matrix remains in progress. It has exposed untested factual presuppositions in personal attribution (#356): keeping “her” in both assertion and negation never tests whether that attribute has source support. A neutral diagnostic precedes any further product change.

Fourth candidate `ae24f9b3` changes only Redline's quotation review: one fresh source-blind focused reader per review/re-review, with parent validation and the existing correction budget. A failed reader produces a coverage gap rather than invented text findings or an extra correction round. The predeclared [quotation matrix](matrix-quotation.md) selects all quoted third-wave artifacts, preserves functioning English quotations, repeats the three known Swedish faulty artifacts four times in total, and verifies one quotation-free bypass. All four technical checks pass, including 1,873 tests; native outcome assessment remains separate.

The added source checker and conditional quotation reader increase execution time. [Resource word counts](reviews/reading-load-final.json) preserve each revision's reading load; native durations are reported separately and are not a controlled latency benchmark. No push, release or global installation has occurred. Local integration and final tracker disposition are pending the declared evaluations and independent review.
