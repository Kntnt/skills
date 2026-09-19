# Independent claim-scope diagnostic

This diagnostic is separate from the fixed Skill matrix. It does not replace any failed result or establish general reliability. The reviewer received authorization for exactly one additional neutral native comparison using the complete existing `claim-support/input.md`; the prompt names neither dates nor the suspect clause.

## Result

The initial claim ledger in [run 1](../probes/claim-support/run-1/response.txt) reports no findings. It correctly isolates the dated decision but reconstructs supplier choice without the inherited date, then labels that incomplete proposition supported. The trace proves the entire source and draft were available. The miss is in the comparison, not missing source material.

The [second prompt](../probes/claim-support/scope-counterexample-prompt.txt) requires complete standalone propositions with inherited grammatical modifiers, followed by a source-compatible counterexample test. Its [response](../probes/claim-support/run-2-scope-counterexample/response.txt) identifies exactly one defect: the leading September modifier dates both the decision and supplier choice. It reconstructs both predicates with the date and gives a valid counterexample: a September decision, an October 1 choice, and an eight-week trial completed before the December 4 note satisfy the entire supplied source while making the draft’s supplier-choice date false. It proposes moving the date directly after “decided”. The remaining propositions, attributed interpretation, quotations, reservations and invitation are judged supported without collateral false positives.

## Independent assessment

The source does not entail the supplier-choice date. Narrative proximity makes it plausible but does not establish it. Requiring support for this definite circumstance applies the same standard that rejects an invented interview question; accepting it would weaken the existing F1 criterion. The two probes show a concrete execution seam: claim decomposition can remove the very modifier that needs checking.

The smallest general intervention is to require reconstruction before support matching and preserve modifier scope in each resulting proposition. A source-compatible counterexample then tests entailment rather than plausibility. It needs no case-specific date example, forbidden-word list or new source-fidelity norm. Requiring complete accounting increases report length and execution time; the broader candidate matrix must test preservation, overblocking, mixed source states and false-positive rates. One successful diagnostic is evidence for trying the process, not proof of a cure.

## Native evidence and cleanup

Both runs used immutable product `8f92e12` and corpus `bf14dc2`; native turn contexts confirm `gpt-6-astra` with high effort. Both read the complete input, exited successfully without timeout, preserved input/authentication and left no non-home changes. The second run took 145.78 seconds. Its runner PID/process group 25832 was registered on launch and exited. Its literal temporary root was removed after capture; run 1’s root was already absent when independently checked. Per-run `independent-audit.json` and `cleanup.json` retain those facts. No product files were edited by this reviewer.
