# Rules — how a ticket is written

Read before filing a ticket in this repository, and before scheduling one.

This module covers what a ticket may claim about this repository while it waits to be built, and what it must declare about how it may be scheduled. It is not about what work is worth a ticket or how a body of work is cut into tickets, and it says nothing about the tracker's own shape — labels, milestones and relations are the tracker's furniture rather than this collection's law.

The capitalised term — Solo Ticket — is defined in [`CONTEXT.md`](../../CONTEXT.md). That file says what the term means; this module says what is true of it.

The rules whose reasoning is settled in a decision record are named here in a phrase and cited to the record rather than argued again — the record is where the alternatives and their costs live, and a second telling of the argument is a second thing to keep true. What the two records this module rests on hold is field evidence: the tickets that collided, the numbers they lost, the run that ended on a branch contradicting itself. That is what a reader needs before deciding a rule is taste, and it is a reason to open the record rather than something to copy out of it.

## Which layer a rule binds

Two kinds of document carry work here, and they age differently.

**A ticket is durable.** It is written once and built hours or days later, by somebody who was not there. Sibling tickets land in between, and an unattended run builds whatever the ticket said with nobody in the loop to notice that the ground moved (ADR-0112). Everything below binds the ticket, and binds it hardest for exactly that reason.

**A plan is compiled just in time.** It is produced against the tip the work starts from and consumed by the run that produced it, so nothing can land between its reading of the tree and its writing. A plan may therefore hold what a ticket may not — exact paths, line numbers, excerpts of the code as it stands — and holding them is what lets an executor work from the plan alone. The rules below are not relaxed for a plan; they do not reach it, because the drift they exist against needs time a plan never has.

An author's first question is which of the two they are writing. What waits is under these rules.

## What a ticket may assert

**A ticket claims nothing about this repository that a sibling ticket can falsify while it waits** (ADR-0112). Four rules follow, each carried by the findings that produced it, because a rule without its reason is a rule the next author talks themselves out of.

**Never name a record number.** Write *the next free number at the time of writing*, and require the commit to say which number was taken. *Next free* is one above the highest number the directory holds: a gap lower down is legitimate and does not make that number free (ADR-0112). A number in a ticket is a claim on a shared resource nobody has reserved, so a ticket naming one races every other ticket in its wave — and losing that race is invisible until integration.

**Cite symbols, not line numbers.** Name the function and the file — `collection_block` in `skills/kntnt/scripts/kntnt.py` — rather than the file and a line in it. Where a line number genuinely helps a reader locate something, mark it as of a named commit, so a reader who finds something else there knows to re-derive it rather than to doubt themselves. The cost of a bare line number is paid even when nothing breaks: every builder who notices the discrepancy has to decide whether it matters and say so.

**Quantify over the collection rather than enumerating it.** Write *every shipped Skill* rather than a table of names, and where a table is genuinely needed for the reasoning, say whether it is exhaustive or illustrative rather than leaving a builder to infer it. An enumeration is a snapshot of a collection that grows, and a builder who widens the work to what the ticket missed has done the author's job on top of their own.

**State the ticket's own vantage point.** One line in the body naming the commit the ticket was written against, its short hash being enough. It is the cheapest of the four and it repairs the other three when they fail: a builder who can see what the author saw can tell drift from error, instead of guessing which of the two they are looking at and how much else in the ticket to distrust.

**Nothing enforces this, and that is the decision rather than an omission** (ADR-0112). Only the first rule is mechanically checkable, and the check would mean the suite reaching the tracker over the network, which nothing else here does, for one rule out of four. What the suite does refuse is the harm that reached the tree: a number two records claim, and a citation no record answers. The residual risk stands plainly — a ticket filed with a doomed number, a moved line or a stale enumeration is caught only by a builder or a reviewer noticing, hours later, at the cost of a correction or a rebuild.

**A closed ticket is never rewritten to comply.** It is the account of what was built, and the drift recorded in it is the evidence these rules rest on.

## Builds alone

**A ticket whose subject is a repository-wide invariant declares its own exclusivity in its body, on a line opening `Builds alone`, and whatever schedules it gives it a wave nothing else is in** (ADR-0112). A ticket carrying that line is a Solo Ticket. It takes the first wave its blockers admit it in — exactly the wave it would have taken without the line — and takes that wave by itself; its otherwise admissible siblings fall to the wave behind it. Nothing else about scheduling changes — ordering, ceilings and blocking behave as they did — and whatever computes the waves says which tickets ride alone and that their own bodies are why.

**An author writes the line where the ticket's subject is a rule every shipped file is under, which the ticket rewrites or newly enforces, and nowhere else.** That is the whole rule and it is deliberately narrow. A ticket that touches many files is not one of these; a ticket that changes what *every* file must look like is, because the set it governs includes the files a concurrent sibling has not written yet — which is precisely what a blocking edge cannot name, an edge naming a ticket that exists. Serialising such a ticket costs one wave of parallelism against a branch-level contradiction that only the merge can show, and by then the new instances exist.

**The declaration lives in the ticket's body, read the way the `Blocked by` line a ticket carries for its blocking edges already is** — a heading or a sentence, marked up or not. It therefore needs no tracker feature and survives a tracker with no relation to hold it. What is matched is the opening words, so a ticket that means it and spells it otherwise is a ticket the scheduler reads as any other. And it is a declaration rather than something inferred from the ticket's text: an inference wrong in the safe direction serialises a wave for nothing, and wrong in the other direction is the night that was lost.

**Nothing verifies that a Solo Ticket's subject really is repository-wide, in either direction** (ADR-0112). An over-cautious author buys silence with the run's parallelism, and two Solo Tickets admissible at once serialise into consecutive waves with their ordinary siblings waiting behind both; that is the cheap direction of the error, and it is accepted. The expensive direction — an invariant ticket whose author did not recognise it as one — is left to whatever reads the merged branch for coherence, at the cost of one correction round. The declaration keeps the common case off that branch and the check catches what the declaration missed, and neither has to be perfect for the pair to hold.
