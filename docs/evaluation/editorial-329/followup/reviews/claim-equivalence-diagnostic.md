# Independent claim-equivalence diagnostic

One authorized neutral comparison tested the complete source and failed draft from second-candidate `opinion-absence-en_GB-r1`. This diagnostic is separate from the frozen 56 Skill invocations and replaces no result. Product `82db439`, corpus `bf14dc2`; the prompt names no suspect phrase, subject or document.

## Hypothesis and result

The first Skill checker had silently restricted a whole-submission assertion by adding “as supplied in the source package” to its reconstructed proposition. The diagnostic therefore tested whether requiring meaning-equivalent reconstruction before source matching would reveal the error. It retained full claim accounting and the source-compatible counterexample test.

The [diagnostic response](../probes/claim-equivalence/run-1/response.txt) **misses the defect**. It now accurately reconstructs the actual claim: “The submission does not establish whether that consent actually exists.” It then labels that proposition supported because the supplied source leaves actual status unstated. No imported qualifier is needed for this second miss. The narrow hypothesis that reconstruction-equivalence enforcement alone would fix the problem is therefore not supported.

The remaining reasoning error is a transfer between knowledge scopes. The package says it does not disclose actual status; that does not establish what the separately referenced submission says. A submission that reported refusal, with that detail omitted from the package, is compatible with all supplied facts but contradicts the draft's whole-submission uncertainty assertion. The diagnostic asserts that it tested counterexamples but does not test this distinction concretely. Its reassurance that either consent state remains possible checks the underlying consent fact, not the claim about the document's contents.

The two native Skill failures remain F1 failures under #355. This unsuccessful diagnostic is not evidence for adding its prompt to the product, nor for relaxing the source-scope criterion. Any next experiment should isolate support-source versus claim-referent scope generally, rather than introduce a consent-specific prohibition.

## Native evidence and cleanup

The trace visibly reads the complete combined source and draft. Native identity is `gpt-6-astra` with high effort. The run completed with exit code zero, no timeout, and 103.42 seconds elapsed. Input and authentication remained unchanged; inventory differences outside the native home were empty. Runner PID/process group 71175 was registered at launch and exited. The literal temporary root was removed after evidence capture. Per-run `independent-audit.json` and `cleanup.json` record those facts. No product files were edited.
