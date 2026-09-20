# Rules — what a commit message claims about a ticket

Read before writing a commit message that names a ticket, and before writing anything that tells somebody else how to write one.

This module covers what a commit message in this repository may claim about a ticket and who has the authority to close one. It is not about what a ticket may claim while it waits to be built, which is [`tickets.md`](tickets.md), nor about where a rule is written down, which is [`docs.md`](docs.md), nor about the form of the code a commit carries, which is [`general.md`](general.md).

The rule below is settled in a decision record and is named here in a phrase and cited to it rather than argued again — the record is where the field evidence, the alternatives and their costs live, and a second telling of the argument is a second thing to keep true.

## Who closes a ticket

**A commit claims to close a ticket only where whoever writes the commit is also whoever decides that the work holds** (ADR-0200). The tracker obeys a closing trailer without asking anything, so the trailer is a claim on that authority, and a commit written by somebody whose work a separate verdict decides has no such authority to claim.

**Where the author is the judge, `Closes #<number>` is the ordinary way to close.** An agent or a person who takes a ticket directly and commits their own work is both, so one authority is at work and the trailer says what is true. `/commit` is that case, and its own body says so.

**Where somebody else decides, the commit writes `Refs #<number>` and closes nothing.** No closing keyword stands before the reference — the tracker's `close`, `fix` and `resolve` families, in every spelling and every case. The closing belongs to whoever records the outcome: under `/orchestrate` that is the engine's `record --outcome=done`, which closes a passing ticket and leaves a failed one open. Every brief the Skill hands a subagent that may commit says this, and the suite reads the reference directory itself rather than a list of briefs, so one added later is held to it from the moment it exists.

**The reference follows the authority, which is what keeps the history legible.** `Refs` says somebody else decided; `Closes` says the author did. Reconciliation rests on that: it finds the commit that finished a parked ticket by hand through the closing reference in it, which is exactly the case where the reference is still correct.
