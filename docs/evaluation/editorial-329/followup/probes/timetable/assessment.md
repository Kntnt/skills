# Independent timetable replay assessment

The three predeclared repeats used the exact complete `opinion-absence-en_GB-r2` Write artifact and the same `/redline --output=response input.md` prompt at `8f92e1266493f40099b3274374b6c0223c2f76a8`. No source or evaluator judgement reached the invoked Skill. [Verification](verification.json) establishes input/prompt equality, unchanged product revision, actual inherited `gpt-6-astra/high` identity, complete scoped resources and one final installed Proofread invocation per run.

## Observed outcomes

| Run | Review outcome | Text outcome | Independent judgement |
|---|---|---|---|
| [r1](r1/response.txt) | One fresh correction, then an unresolved finding that the eight-week period lacks a supporting basis. | All prose and metadata preserved. | False positive. The response invokes the requirement for a supported next step but treats the expressly uncertain requested timetable as needing demonstrated feasibility. |
| [r2](r2/response.txt) | No findings; clean no-change status. | Input remains final. | Correct preservation of the proposal and its qualification. |
| [r3](r3/response.txt) | One fresh correction, then an unresolved finding demanding a basis for eight weeks or a policy for a longer study. | All prose and metadata preserved. | False positive. A contingency policy is not necessary to make this explicitly qualified request intelligible or to preserve its meaning. |

The false-positive judgement recurs in **2 of 3 diagnostic repeats**, in addition to the original candidate observation. This is a deliberately selected diagnostic input, not a population failure-rate estimate. The clean repetition remains recorded and does not erase the other two.

The root filed [#354](https://github.com/Kntnt/skills/issues/354) for this false positive and [#353](https://github.com/Kntnt/skills/issues/353) for the separate no-change delivery collision.

The artifact says the author is asking for eight weeks and explicitly states that completion within that period is not established. It does not assert that eight weeks will be sufficient. The proposed action, the actor and the knowledge limit are all clear. A reader can disagree with that proposal without the proposal thereby being a defective representation of a fact. The correction agents rightly refuse to replace the author's position or invent evidence; the error occurs earlier, when the review raises the finding.

## Criteria

The unchanged text supports the same G1/G2/P1/W1/L1/L2 passes in all three runs: a clear opinion and actor, relevant financial objection, qualified evidence and direct request, readable paragraphs, fluent British English and valid locale mechanics. The proposed timetable and acknowledged uncertainty coexist coherently; no prediction of timely completion is present.

- **T1 — pass, all three:** opinion/en_GB/none follows metadata and actual resource loading.
- **R1 — fail, r1 and r3; pass, r2:** r1/r3 produce a false-positive editorial finding, a qualitative contract failure; no factual claim or position is removed. R2 preserves the working text without inventing a requirement.
- **R2 — pass, all three:** full review contracts are visible, correction children in r1/r3 are fresh with no model/effort override, one default-budget round is respected and re-reviewed, and exactly one final Proofread pass follows. No substantive post-Proofread change appears.
- **O1 — pass for filesystem effects in all three; delivery branch skipped for r1/r3:** work, source and scratch remain unchanged at capture, with private native Harness state the only surviving changes. R2 correctly returns a no-change status. R1/r3 repeat the unchanged text under Redline step 11's unresolved-finding instruction; shared delivery guidance says otherwise, so that branch is a contract collision rather than clear model disobedience.
- **S1 — not applicable:** these are source-blind Redline invocations, not Write source comparisons.

Full artifacts and separate accounts were extracted faithfully. Differences from the original are at most trailing whitespace; all substantive prose and metadata match. The exact correction dispatch is encrypted, but fresh-spawn configuration, actual child resource reads and complete returns remain inspectable in each `native-audit.json` and native trace.

## Contract seam and minimal repair

The most specific contributing ambiguity is the second paragraph of `genres/opinion.review.md`: it checks “conclusions for support visible in the text” without distinguishing factual conclusions and predicted outcomes from advocated decisions or targets. The genre's ending requirement, “the specific change or stance the argument supports”, supplies a second nearby route to the same reading. R1's public finding explicitly appeals to a “supported next step”; R3 extends that reading into a required contingency policy. This is evidence of a plausible interpretive seam, not proof that one sentence uniquely caused the model's judgement.

Clarify that distinction within the existing opinion review paragraph. Continue checking factual premises, attributed claims, predictions, logical coherence and the grounds for the author's choice. Preserve an advocated action or target as advocacy, including acknowledged uncertainty about its outcome; a qualification does not turn the proposal into an unsupported factual promise. The repair should sharpen the current preservation requirement, not exempt opinions from factual support or make every proposed action automatically persuasive.

No new timetable section, example derived from this fixture, fixed duration rule, mandatory feasibility proof or general contingency-plan requirement is warranted. The base Claims boundary and the source-check workflow can remain unchanged. Root authors the final product wording and verifies it against these retained repeats and separate cases.

## Cleanup

The runner had registered all three private roots. They were already removed by the session-cleanup start hook at `2026-09-19T20:48:39Z` before the independent evaluator's literal-path deletion attempt. The evaluator verified all three roots absent and captured their exact registration/deletion records in [automatic-cleanup-events.json](automatic-cleanup-events.json). Individual `cleanup.json` receipts attribute the deletion correctly; no evidence or deliverable was deleted.
