# Declared commit roles are checked before integration

Some release gates require a clean implementation commit whose SHA is then written into tracked evidence. One self-contained commit cannot express that relationship: amending the implementation changes the identity the evidence certifies.

**A ticket may declare ordered commit roles and their allowed Git pathspecs on a `Commit roles` body line.** The builder owns those commits. Before merging, Orchestrate walks the ticket branch from its current merge-base and accepts only one or more complete passes through the roles, one commit per role in declaration order, with every changed path inside that role's surfaces. At a ceiling of one, `record` performs the same check from the ticket's head saved at claim time.

The history is append-only. An amendment adds another complete pass, so a correction begins with a new implementation-role commit and fresh evidence follows it. Commits confined to `.kntnt-orchestrate/` do not occupy a role, and that directory may accompany an otherwise valid role commit. Marked integration and collision-repair merges are run-owned and skipped; an unmarked merge is ordinary ticket history and occupies the next role. That pair of run-owned merges is amended by ADR-0148, which adds the marked merge a resume makes to bring a preserved ticket branch forward.

The declaration is projected into run state. A declared ticket cannot begin unless its claim boundary is durably saved, while a checking verb with absent or unreadable state preserves the established undeclared behavior and performs no contract check. A successful ceiling-one record retains the boundary as `contract-base` provenance so reporting can recover the run's real base after scratch state disappears. **This narrows ADR-0051's statement that absent run state cannot change an answer and ADR-0054's statement that a ceiling-one run has one commit per ticket.**

The rejected alternative was an engine-mediated two-phase build in which Orchestrate committed between builder phases. It would make the engine author ticket work before an independent verdict; deterministic validation belongs to the engine, while authored build commits remain the builder's.

**What this costs.** The contract is enforced only when readable run state carries the tracker declaration. Violating history is preserved for inspection and terminally failed rather than amended, because later commits cannot undo a certified out-of-role commit.
