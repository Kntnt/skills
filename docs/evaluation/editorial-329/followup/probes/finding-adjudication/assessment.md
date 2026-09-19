# Independent finding-adjudication assessment

Four native GPT diagnostic runs used the same frozen neutral task and complete source/draft/actual-report packages. The source detector was not changed. Every input was read in full; all four native sessions used inherited `gpt-6-astra/high`, without delegation or Skill invocation. These are adjudication diagnostics, not Write or Redline evaluations and not evidence of the main author's reliability.

| Case | Predeclared expected verdict | Actual verdict | Independent assessment |
|---|---|---|---|
| Column | Reject false positive | Unresolved | The model identifies the report's broader scope and the essay-basis contextual reading but requires a decisive exclusion of the literal alternative. It retains one unresolved finding. The expected removal of the false-positive refusal is not demonstrated. |
| Opinion | Reject false positive | Unresolved | The model recognizes the supplied sufficiency argument and criticizes the report's stronger prediction, but still retains the institution-wide knowledge reading as unresolved. The expected false-positive rejection is not demonstrated. |
| Chronology | Accept genuine finding | Accepted | Correctly preserves the September modifier over both coordinated predicates and confirms the source-compatible October selection. The unedited draft still contains the validated defect. |
| Document scope | Accept genuine finding | Accepted | Correctly keeps “it” attached to the complete submission and distinguishes that document from the supplied package. The withheld-consent counterexample establishes missing support. The unedited draft still contains the validated defect. |

The operation preserves both genuine findings but does not yet solve either observed refusal. None of these results authorizes treating a disputed final finding as cleared. The two accepted-control responses end with “No validated unresolved finding remains”, meaning their adjudication is settled; this must not be mistaken for a defect-free draft, since each accepts a still-unrepaired defect. Any runtime status must distinguish accepted defects, rejected findings and unresolved adjudications.

Full responses and native captures remain in the four run directories. [Provenance](provenance.json) records the exact pre-existing source/draft and report origins; [verification](verification.json) records full reads, identity, no side effects and cleanup. All four roots were removed by literal absolute path after capture; launcher group 84597 has ended. Every failed expectation remains visible.
