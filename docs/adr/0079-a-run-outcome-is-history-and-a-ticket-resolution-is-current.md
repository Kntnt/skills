# A Run Outcome is history and a Ticket Resolution is current

One recorded outcome answered two questions until a failed or conflicted unattended run was rescued outside Orchestrate: what the run did, and whether the ticket's work is complete now. Treating the last marker as both made the report permanently wrong when a person later completed and landed the work, while overwriting the failure would make the historical account wrong instead.

**So the Run Outcome is the immutable historical result of the unattended attempt, while the Ticket Resolution is the current account that groups the report.** Reconciliation moves an unsuccessful ticket to a done Ticket Resolution without changing its failed or conflicted Run Outcome, and the report annotates the done ticket with that provenance. This supersedes ADR-0051 only where its single outcome served both meanings; the tracker remains the store, and a recorded result still prevents the ticket from being offered to another run.

**Reconciliation is an explicit maintainer assertion, never an inference from tracker closure.** A closed ticket may be a duplicate or rejected request, so the engine accepts reconciliation only when the ticket is already closed, its Run Outcome is failed or conflicted, and the named completion commit is reachable from the repository's default branch. These checks establish that the asserted repair landed without pretending that Orchestrate built or independently verified it.

**The maintainer normally names only the ticket.** Reconciliation finds the completion commit on the default branch when exactly one candidate can be established, and asks the maintainer to identify it when none or several remain. It never guesses. Repeating the same Reconciliation is a no-op; a later attempt naming a different completion commit is refused as contradictory rather than silently replacing the first assertion.

**Reconciliation is an explicit Orchestrate action, not a maintenance tool or knowledge of marker grammar.** The completed ticket exchanges stale readiness and claim markers for a neutral history marker that lets later reports find it without presenting it as active work. The same truthful cleanup applies to successful tickets from the adoption of this model onward; existing tracker records are neither migrated nor given compatibility behavior solely for their old shape.

**Work that depends on a failed or conflicted ticket remains unavailable after tracker closure alone.** It becomes available only when Reconciliation establishes that the requested work landed.

**What this costs.** Report and Plan now project current state from more than one historical fact instead of reading one winning marker, and the maintainer performs one explicit action after rescuing work. In return, the report says what still needs action, the earlier unattended failure remains auditable, dependencies remain truthful, and tracker closure alone never manufactures completed work.
