# Rules — how a ticket is written

Read before filing a ticket in this repository.

This module covers what a ticket may claim about this repository while it waits to be built, what it must declare about how it may be scheduled, the shape a ticket takes here, and where its requirement lives once the thread has grown past the body. It is not about what work is worth a ticket or how a body of work is cut into tickets, and it says nothing about the tracker's own furniture — which label a ticket carries and which milestone it sits in are the tracker's business rather than this collection's law, and the one tracker relation that appears below appears because a ticket's body carries the same edge where no relation exists.

Everything here binds the ticket itself: a document written once and built hours or days later, by somebody who was not there, with sibling tickets landing in between and nobody in the loop to notice that the ground moved.

The capitalised term — Solo Ticket — is defined in [`CONTEXT.md`](../../CONTEXT.md). That file says what the term means; this module says what is true of it.

The rules whose reasoning is settled in a decision record are named here in a phrase and cited to the record rather than argued again — the record is where the alternatives and their costs live, and a second telling of the argument is a second thing to keep true. What the two records this module rests on hold is field evidence: the tickets that collided, the numbers they lost, the run that ended on a branch contradicting itself. That is what a reader needs before deciding a rule is taste, and it is a reason to open the record rather than something to copy out of it.

## What a ticket may assert

**A ticket claims nothing about this repository that a sibling ticket can falsify while it waits** (ADR-0067). Four rules follow, each carried by the finding that produced it, because a rule without its reason is a rule the next author talks themselves out of.

**Never name a record number.** Write *the next free number at the time of writing*, and require the commit to say which number was taken. *Next free* is one above the highest number the directory holds: a gap lower down is legitimate and does not make that number free (ADR-0067). A number in a ticket is a claim on a shared resource nobody has reserved, so a ticket naming one races every other ticket in its wave — and losing that race is invisible until integration. An unattended run closes the same gap from the other end, reserving each ticket in flight its own number in every numbered directory and handing it to the builder in the brief (ADR-0071).

**Cite symbols, not line numbers.** Name the function and the file — `collection_block` in `skills/kntnt/scripts/kntnt.py` — rather than the file and a line in it. Where a line number genuinely helps a reader locate something, mark it as of a named commit, so a reader who finds something else there knows to re-derive it rather than to doubt themselves. The cost of a bare line number is paid even when nothing breaks: every builder who notices the discrepancy has to decide whether it matters and say so.

**Quantify over the collection rather than enumerating it.** Write *every shipped Skill* rather than a table of names, and where a table is genuinely needed for the reasoning, say whether it is exhaustive or illustrative rather than leaving a builder to infer it. An enumeration is a snapshot of a collection that grows, and a builder who widens the work to what the ticket missed has done the author's job on top of their own.

**State the ticket's own vantage point.** One line in the body naming the commit the ticket was written against, its short hash being enough. It is the cheapest of the four and it repairs the other three when they fail: a builder who can see what the author saw can tell drift from error, instead of guessing which of the two they are looking at and how much else in the ticket to distrust.

**Nothing enforces this, and that is the decision rather than an omission** (ADR-0067). Only the first rule is mechanically checkable, and the check would mean the suite reaching the tracker over the network, which nothing else here does, for one rule out of four. What the suite does refuse is the harm that reached the tree: a number two records claim, and a citation no record answers. The residual risk stands plainly — a ticket filed with a doomed number, a moved line or a stale enumeration is caught only by a builder or a verifier noticing, hours later, at the cost of a correction or a rebuild.

**A closed ticket is never rewritten to comply.** It is the account of what was built, and the drift recorded in it is the evidence these rules rest on.

## Builds alone

**A ticket whose subject is a repository-wide invariant declares its own exclusivity in its body, on a line opening `Builds alone`, and whatever schedules it gives it a wave nothing else is in** (ADR-0099). A ticket carrying that line is a Solo Ticket. It takes the first wave its blockers admit it in — exactly the wave it would have taken without the line — and takes that wave by itself; its otherwise admissible siblings fall to the wave behind it. Nothing else about scheduling changes — ordering, ceilings and blocking behave as they did — and whatever computes the waves says which tickets ride alone and that their own bodies are why.

**An author writes the line where the ticket's subject is a rule every shipped file is under, which the ticket rewrites or newly enforces, and nowhere else.** That is the whole rule and it is deliberately narrow. A ticket that touches many files is not one of these; a ticket that changes what *every* file must look like is, because the set it governs includes the files a concurrent sibling has not written yet — which is precisely what a blocking edge cannot name, an edge naming a ticket that exists. Serialising such a ticket costs one wave of parallelism against a branch-level contradiction that only the merge can show, and by then the new instances exist.

**The declaration lives in the ticket's body, read the way the `Blocked by` line a ticket carries for its blocking edges already is** — a heading or a sentence, marked up or not. It therefore needs no tracker feature and survives a tracker with no relation to hold it. What is matched is the opening words, so a ticket that means it and spells it otherwise is a ticket the scheduler reads as any other. And it is a declaration rather than something inferred from the ticket's text: an inference wrong in the safe direction serialises a wave for nothing, and wrong in the other direction is the run that was lost.

**Nothing verifies that a Solo Ticket's subject really is repository-wide, in either direction** (ADR-0099). An over-cautious author buys silence with the run's parallelism, and two Solo Tickets admissible at once serialise into consecutive waves with their ordinary siblings waiting behind both; that is the cheap direction of the error, and it is accepted. The expensive direction — an invariant ticket whose author did not recognise it as one — is left to the wave check that reads the merged branch for coherence, at the cost of one correction round. The declaration keeps the common case off that branch and the check catches what the declaration missed, and neither has to be perfect for the pair to hold.

## The shape a ticket takes here

A ticket is written for a builder who has the ticket and nothing else, and checked by a verifier who has the ticket and the repository. Four parts carry that, and a ticket carries them in this order.

**What to build**, under that heading, in prose. It states the change and the reasoning a builder needs to make it, not a transcript of the edits: the builder is given the body as it was filed rather than a summary of it, so what is not written here is not known. Where the change re-implements something that exists elsewhere — a commit on another branch, a Skill in another collection — the ticket names it and how to read it, rather than describing it from memory.

**Acceptance criteria**, under that heading, as a checkbox list. Each one is a statement a fresh agent can check against the repository as it then stands, without asking the author and without having watched the work: an independent verifier that never saw the building session checks each of them, and a criterion whose answer is *ask whoever wrote it* is a criterion that fails for the wrong reason. The last of them is the project's own verification, named as the test suite or as the four checks [`CONTRIBUTING.md`](../../CONTRIBUTING.md) lists, so that what a ticket is held to includes what everything else is held to.

**`Blocked by`**, where the ticket depends on work that does not exist yet, naming each blocker and why it blocks. The tracker's native blocked-by relation takes precedence where the tracker has one and the body line is how the same edge is written where it has none; a blocker blocks until its own work is done, so a closed ticket whose work failed is a blocker still. A dependency discovered while building is a missing edge rather than something to build around: the builder stops and names the ticket it waits on, the edge is written to the tracker as the breakdown would have written it, and the ticket comes back when that work exists (ADR-0073).

**The vantage line**, last, after a horizontal rule: `Written against` and the short hash of the commit the ticket was written against. It is the fourth assertion above, and it is the line that lets a builder tell drift from error.

A ticket that rewrites an invariant carries its `Builds alone` line too, in the body, where its own reasoning is — a sentence saying which rule reaches every file, not a marker bolted to the end.

## The thread outranks the body

**A comment on a ticket outranks the body it amends, and the requirement is the whole thread rather than the body alone.** Where a comment contradicts the body, the later text stands: a question the body leaves open and a comment answers is answered, and the answer is the requirement. Acceptance criteria stated in a comment are acceptance criteria, and they are what the work is verified against — the brief a builder is given, the verifier's, and the amender's all carry the thread whole and all say so.

**So a ticket is read to the end of its thread before it is built, oldest comment first, from the tracker rather than from memory.** In this collection the settled decisions and the acceptance criteria often arrive as a comment, and a ticket read as its body alone is a ticket read as its untriaged self.

**A readiness addendum is one of those comments, and it voids what it amends.** Before a run, `/ready-for-agent-check` reads each `ready-for-agent` ticket the way an unattended builder will — one subagent per ticket, in a context that did not write it — and reports what would stop that builder; it writes nothing on the tracker, because what to do about a stop is the maintainer's to decide. What the maintainer then settles is written back onto the ticket as a comment, and that comment is the requirement wherever it touches the body: a criterion it replaces is replaced, a sentence it corrects is corrected, and a builder that has read only the body has read the version the check found wanting. An unattended run answers open questions the same way, writing each answer as a comment on its own ticket, which is how the answer reaches the builder at all.

**The amendment is written as a comment rather than folded back into the body.** The body is the ticket as it was filed and the thread is where every change to it stays visible, with its author and its date; a body quietly rewritten is a ticket whose builder and whose verifier cannot tell what was decided after the fact from what was asked for in the first place.
