# A parked ticket resumes its lifetime attempt

Parking used to preserve Orchestrate's tracker markers and working tree without stating whether those facts were intentional. A caller could read the same parked ticket as having a fresh correction budget or only the unspent part of its old one, while an isolated tree could resume without the blocker it had waited for.

**The amendment budget belongs to the ticket's lifetime.** The tracker ledger is append-only (ADR-0084), and parking changes neither its markers nor its count. A resumed building phase is the same attempt, while only a newly recorded building phase spends another. Reports retain `amends_spent` as the lifetime total and split the attempts this invocation inherited from those it newly spent.

**Preserved commits are the mandatory base of a resume.** Isolating an existing ticket tree brings the run branch into that ticket branch before dispatch, so the preserved attempt gains everything integrated while it was parked. Uncommitted work is left for a person. A collision confined to Declared Generated Files is regenerated under ADR-0106; any other collision is reported and left unmerged.

**A resume collision is repaired only to prepare the resumed amend.** The repair runs on the ticket branch, takes no verdict of its own, and reaches neither the run branch nor the tracker as an outcome. The resumed amend's fresh verifier runs the complete gate and checks the whole ticket, including the repair. A disagreement the repairer cannot settle parks the ticket again without spending an amendment.

This **narrows ADR-0055**. Its ordinary collision path still independently verifies a repair and may rebuild after a failed repair. When the collision arises while the engine is bringing a preserved ticket forward, verification is instead deferred to the already-required fresh verifier of the resumed amend and no collision rebuild is spent.

**What this costs.** Resume now performs a merge before dispatch and may need a repair role that produces no separately judged attempt. The per-invocation report split uses session memory because tracker markers deliberately carry no run identity. In return, the park report predicts the remaining budget exactly, preserved work cannot be silently replaced, and resolved blockers are present when work continues.
