# Dispatch recovery and tracker transitions

Read this reference whenever a live journal exists, a ticket reaches a terminal verdict, a tracker transition is due, or cleanup and archive eligibility are being decided. `$HERE/scripts/journal.py` owns journal persistence only and remains no workflow engine; every scheduling, routing, review, Git, tracker, and verdict decision stays agent-authored.

## Journal and artifacts

The journal is clone-local under `<git-common-dir>/kntnt-pipeline/dispatch/`: `active/<sha256-of-full-integration-ref>/` is the branch's one active slot and `archive/<opened-UTC>-<run-fingerprint>/` is the completed location. Validate the immutable opening and complete hash-chained event sequence through the helper before acting. A missing artifact, broken chain, non-contiguous sequence, invocation mismatch, or contradictory Git state is a refusal to continue.

Every artifact is durable before the event that names it. Bundle escrows, Route responses, full-index patches, large review findings, dispatcher-write proposals, and observation inputs carry their SHA-256 and byte length. The projection is the only current run account; surviving worktrees, branches, tracker labels, and session memory cannot fill a missing event.

## Recovery matrix

| Last durable state | Required recovery |
| --- | --- |
| `attempt-started`, no patch event | Remove or ignore the disposable resources, recreate the same base and escrowed tests, and replay the named attempt under its recorded Route decision; spend no retry. |
| `patch-captured`, no review | Recreate a clean worktree, verify and apply the patch, materialise canonical tests, and perform the complete review without rerunning the executor. |
| `REVISE` recorded | Continue the live executor context; when it is unavailable, record `fresh-context`, rehydrate the same execution role and Route point from the complete plan, last accepted patch, and exact finding without consuming a revision round. Preserve that fact for the final report. |
| `landing-started`, no `landed` event | If the exact candidate is reachable and its trailers, tree, and test blobs agree, record it landed; if the ref remains at the old tip, rebuild the candidate from journal artifacts; any other ref state stops. |
| `REBUILD` recorded | Require the fresh accepted bundle named by the durable `/compile #<ticket>` handoff, verify it against the journal's new tip, and start the one fresh executor. |
| `human-conflict` recorded | Preserve only the named worktree and branch, accept the owner's direct resolution or durable instruction, re-hash tests, and repeat full review before landing. |
| `landed`, no `tracker-transition-completed` | Verify the selected baton, reachability, tree, and test blobs; reuse or create the concrete `T-LAND` plan, apply it idempotently, verify the tracker, and record completion before retirement. |
| `parked`, no `tracker-transition-completed` | Recover the PARK class and exact question or handoff, reuse or create its concrete transition plan, apply it idempotently, verify every preservation and assignment field, and record completion before retirement. |
| `tracker-transition-completed`, no retirement | Re-read and verify the recorded post-state, reapply the same planned receipt if drifted, then complete bundle retirement and cleanup without executing the ticket again. |
| `stranded`, no cleanup event | Re-establish the recorded blocker or refusal, release escrow and disposable resources, and preserve the untouched or stale canonical plan slot for later replacement or reuse. |

The matrix separates an executor return from durable patch capture and a candidate commit from integration-ref advancement. Replaying either boundary from session memory risks duplicating paid work or landing twice.

A review-driven REBUILD retains its exact `review_sequence` and existing post-review semantics. A selected but unstarted stale plan instead records pre-execution evidence: `selection_sequence`, previous `HEAD`, stale bundle fingerprint, and the new `HEAD`; it never invents `review_sequence`. Both forms project `await-recompile`, spend the same one-REBUILD budget, and permit the next accepted bundle only when its execution base equals the recorded new `HEAD` and its fingerprint differs from the stale bundle.

## Portable tracker-transition contract

This table is the sole authoritative tracker-transition contract. Resolve the repository's governing agent instructions, their issue-tracker pointer, and their triage-label pointer before mutation. Prefer a repository or track override when one exists; otherwise use the tracker's canonical role mapping.

`executable_ready_label` is the one lifecycle label whose removal makes the complete executable-ready predicate false. Any companion required label is scope and belongs in `preserved_labels`, the complete pre-mutation label set excluding only `executable_ready_label`. Resolve `needs_info_label` and `ready_for_human_label` from their canonical roles. A missing, ambiguous, or contradictory resolution refuses mutation.

| Transition ID | Trigger and notice | Label delta | Assignment | Verified unchanged |
| --- | --- | --- | --- | --- |
| `T-LAND` | Durable verified landing; no notice | Remove `executable_ready_label`; add nothing | Preserve | `preserved_labels`, milestone, open status, and all other fields |
| `T-PARK-INFO` | Owner-owned information question; post the exact question | Remove `executable_ready_label`; add `needs_info_label` | Unassign | `preserved_labels`, milestone, status, and all other fields |
| `T-PARK-HUMAN` | Human repair or conflict handoff; post the exact handoff | Remove `executable_ready_label`; add `ready_for_human_label` | Unassign | `preserved_labels`, milestone, status, and all other fields |

Every row is an idempotent desired-state mutation. Before changing the tracker, record `tracker-transition-planned` with the transition ID, concrete label values, exact `preserved_labels`, milestone, status, assignees, complete pre-projection, and the agent-instruction and convention addresses that resolved them. After mutation, re-read the tracker, verify the complete recorded contract, and record `tracker-transition-completed` with the same resolution and observed post-projection. Recovery reuses that durable resolution instead of resolving current conventions again.

The tracker transition completes before bundle retirement. A landed or parked ticket is never executed again merely to finish a transition or cleanup.

## Bundle lifecycle and retained evidence

Retire a landed or parked consumed bundle only after its terminal event and current verified `tracker-transition-completed` event. Remove the canonical `accepted` pointer only when it still names the consumed fingerprint, remove an immutable bundle only when no pointer names it, remove the escrow, then record `bundle-retired`. A stranded ticket releases its escrow without retirement and leaves its stranded canonical slot available for later replacement or reuse.

Under R2, the latest full parked patch remains beside the compact archive until that ticket lands or is explicitly abandoned. It is inspectable evidence and never authority for a new plan or automatic replay.

A human conflict is the only resource-retention exception: preserve only the named worktree and branch, clean every other owned resource, complete all independent work, and report the immutable-test warning plus one exact owner decision. Record the owner's answer before acting. A mechanical instruction already inside the Binding contract resumes through the same invocation and receives full review before landing and cleanup; an instruction that changes durable product intent is posted to the child and requires the explicit `/compile #<ticket>` plus resume checkpoint before any new execution.

## Outcomes and completion

The projection has exactly three ticket outcomes. **Landed** names a reachable landing commit and bundle fingerprint. **Parked** names the complete owner question or exhausted-review/conflict handoff and verified tracker transition. **Stranded** names the blocker, Route or environment refusal, stopped integration, or discovered dependency that prevented execution without inventing an owner question. If an R3 receipt records `fresh-context`, explicitly name the rehydrated fresh-context in the final report and say it continued without consuming a revision round.

Completion requires every selected ticket to have one exact terminal reason; the integration tree is clean; the active journal is atomically archived; all ordinary worktrees and temporary branches are removed; every landed or parked bundle is retired; every stranded escrow is released while its stranded canonical slot remains; and no retained conflict resource exists in a completed run. The archived receipt keeps identities, footprints, allocations, tests, Route decisions, verdicts, tracker receipts, and terminal evidence, but not retired plan or patch copies already durable in Git.
