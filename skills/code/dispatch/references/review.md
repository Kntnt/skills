# Dispatch tech-lead review

The dispatcher performs this review on the unchanged main seat after every attempt and again on every landing candidate. Read the repository result, not the executor's confidence or summary.

## Review frame

Verify the consumed bundle identities and their recorded source fingerprints, all STOP conditions, the exact footprint and ordered changed paths, every canonical test blob, and the full diff including binary, mode, symlink, creation, and deletion changes. A sibling landing does not retroactively stale an already-consumed parallel plan; integration review judges that patch on a fresh candidate against the newer combined tip. Run every done criterion, every seam command, and the complete repository gate in the environment each command declares.

Account for every executor report departure. A reported Advisory departure may pass when the Binding contract remains satisfied. An undocumented departure, out-of-footprint write, changed compiler-owned test, weakened invariant, missing criterion, wider product choice, or unverified dispatcher-owned write fails review. Tool success alone does not override a contradicting diff or identity.

On a landing candidate, repeat the complete review against the fresh current integration tip using only the accepted patch, canonical test blobs, and dispatcher-owned writes. Verify the combined tree rather than carrying the attempt verdict forward.

## Verdicts

Return exactly one verdict with its evidence. The four are disjoint.

**APPROVE** means every binding identity, ownership check, done criterion, seam command, full-diff judgement, and complete repository gate passes. Only the exact accepted patch may enter landing.

**REVISE** means the plan remains honest and one constructive correction is fully determined inside the Binding contract. Name the failed check, exact defect, required correction boundary, and binding source. Continue the same execution role for at most two review-informed rounds after the initial attempt; every round receives this full review. A third revision condition becomes PARK.

**REBUILD** means the current integration tip or a fresh integration fact makes the compiled plan the wrong vantage. Record one durable `/compile #<ticket>` plus exact resume handoff and, after that user checkpoint supplies a fresh accepted bundle, start one fresh executor. A second rebuild condition becomes PARK.

**PARK** means an owner decision is required, two REVISE rounds are exhausted, the one REBUILD did not produce an integrable result, or no safe next action can be established. Classify it as an owner-owned information question or a human repair/conflict handoff, give one complete question or handoff, and select `T-PARK-INFO` or `T-PARK-HUMAN` from `recovery.md`.

“Try again” is not a constructive finding. A correction is executable only when the existing Binding contract determines one answer; two plausible intents make it PARK even when either edit is small.
