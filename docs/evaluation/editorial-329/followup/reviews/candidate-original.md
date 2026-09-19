# Original-source candidate evaluation — #349 follow-up

The eleven frozen original-source pairs completed at instruction revision `8f92e12`: six opinion pairs, three American English customer-case pairs and two Swedish customer-case pairs. All 22 invocations used native Codex CLI 0.155.1, with the inherited `gpt-6-astra` / `high` identity observed in all 41 parent/child sessions. The supplementary matrix is frozen at `bf14dc2`; original source bytes are unchanged from `6e531f5`.

## Independent outcomes

| Defect class | Observable precheck / checker action | Delivered Write outcome | Paired final outcome |
|---|---|---|---|
| #349, no claim becomes categorical absence | Five of six opinion prechecks visibly contain the defect; all five checkers detect it, all five parent runs make the supported local repair, and five fresh second checkers approve. The sixth has one no-findings report. | 0/6 occurrences; all six final opinion artifacts pass F1. | 0/6 occurrences; all six Redlines preserve the exact input. |
| #352, invented interview question | Five customer-case checkers return no findings; complete inline precheck drafts cannot be reconstructed from encrypted dispatch. | 0/5 invented questions, including 0/3 en_US and 0/2 sv. | 0/5 invented questions. |
| #344, unsupported supplier-selection date | All three en_US case checkers miss the same temporal scope change. | 3/3 en_US F1 failures: “In September 2025” governs both the trial decision and supplier choice; the source dates only the decision. The two Swedish versions separate the sentences and pass F1. | The chronology defect remains in all three en_US finals. Source-blind Redline cannot establish the hidden source limit. |
| #341, Swedish quote idiom | Source-support checkers approve meaning; that is not an idiom judgement. | 2/2 sv L1 failures: “innan nästa byggnad kommer i gång” still lacks the activity referent. | Both Redlines return no-change accounts, leaving 2/2 L1 and R1 failures. |

The overall final Write source-fidelity result is **8/11 F1 passes and 3/11 F1 failures**. This is an observed result on these fixed sources, not a reliability guarantee. Six Writes have no evaluated prose failure, three fail F1 and two separately fail L1. Nine Redlines pass all applicable criteria; two Swedish case Redlines fail L1/R1. No draft is withheld and no paired invocation is skipped.

Two American English case Redlines make legitimate local repetition repairs; nine Redlines make no changes. The repairs preserve complete quotations, facts, customer voice and qualifications. All runs preserve metadata selection, no automatic technique, scoped resource loading, final installed Proofread boundaries and the output contract. No source was supplied to Redline: all eleven staged `input.md` files are byte-identical to the extracted complete Write artifacts.

## Source-check process evidence and limit

All sixteen checkers are fresh, inherit model and effort without override, visibly read the complete original source, and return a report that the parent reads before cleanup. No checker delegates or invokes another Skill. No comparison exceeds the two-pass bound. Five supported local #349 repairs and their second approvals are observable in the reports and delivered text.

Native dispatch encrypts the complete inline draft/task. The complete precheck and approved draft bytes therefore cannot be recovered for comparison against delivered prose. S1's exact complete-draft access/identity component is **skipped as a method limitation**, not passed from the checker's approval. Final F1 judgements are independent comparisons of actual delivered text with the complete source. All readable precheck quotations and checker reports are retained.

The three en_US F1 failures were initially missed by this evaluator. Independent final review noticed the coordinated September modifier; re-reading confirmed it in all three repetitions. [The observation history](candidate-original-observations.md) preserves the provisional assessments and their explicit supersession. Formal records score the confirmed failures. [#344 was reopened](https://github.com/Kntnt/skills/issues/344#issuecomment-5745163428); no source, artifact or criterion was changed to remove the failure.

## Full evidence

- [Write record](../../../records/write-gpt-2026-09-19-349-followup-original.md): all eleven invocations, complete drafts/responses, criteria, source-check reports and native traces.
- [Redline record](../../../records/redline-gpt-2026-09-19-349-followup-original.md): all eleven source-blind pairs, final artifacts, findings and preservation judgements.
- [Verified inventory](candidate-original-inventory.json): 22 complete invocations, 41 native sessions, exact source-blind inputs, inherited identities and all private roots absent.
- [Chronological observation history](candidate-original-observations.md): independent judgements and visible corrections.

Every all-root before/after inventory shows no surviving Skill effect outside native `home/.codex/` state; authentication and supplied input are unchanged. All 22 private roots were removed by literal absolute paths after native trace/inventory capture. The owned Write batch and all Redline runners completed. The three evaluator helpers pass Ruff lint and format checks. No product files were edited, no commits were made by this evaluator, and no new baseline outcomes or other-provider records were opened.
