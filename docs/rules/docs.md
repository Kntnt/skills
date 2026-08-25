# Rules — how this repository records decisions

Read before writing a decision record, before deciding where a rule belongs, and before authoring a document an agent loads.

This module covers where a rule is written down here, what earns a record in the archive, and how the two relate. It is not about what a ticket may claim while it waits, which is `tickets.md`, nor about the form of a Skill's shipped files, which is `skills.md`. It is the module a contributor reads when the question is *where does this go*.

The rules whose reasoning is settled in a decision record are named here in a phrase and cited to the record rather than argued again — the record is where the alternatives and their costs live, and a second telling of the argument is a second thing to keep true.

## Two documents, and the question each answers

**The rules document is what applies now, and it is the authority on it.** `docs/rules/` holds one module per subject, and every line of it is current law phrased as a rule. It is edited rather than grown: a rule that changes is rewritten where it stands, so a module goes on saying one thing about its subject. A reader who wants to know what is true today needs nothing else, and in particular needs to read nothing forward and apply no supersessions by hand.

**`docs/adr/` is a historical archive, read on demand and never auto-loaded.** A record describes the world at its own date and answers why a rule became what it is: what the alternatives were, what they cost, what evidence forced the choice. It does not answer what is true today and cannot be made to: records are not rewritten, so the archive as a whole states what was decided at many different dates, with nothing in it saying which of those decisions survived. That is the archive doing its job rather than a fault in it — the two questions have two documents, and conflating them is what this arrangement exists to end.

**A rule states itself once and cites the record for the reasoning.** The rules document does not reproduce a record's argument, and a record does not restate the rule as it now stands; each copy is a thing that has to be kept true, and one copy is the one a reviewer can diff. Where a change takes a decision in a rule area binding more than one Skill, the resulting rule is stated in the rules document in the same change — `general.md` carries the same duty from the change's side, as part of the sweep a change owes every claim it falsifies.

## Where a rule goes

**The subject decides the module.** A rule binding whoever writes here belongs in `docs/rules/`, in the module whose subject it is: `general.md` for code form, `python.md` for the language, `skills.md` for what a Skill ships, `collection.md` for what the Manager and the collection promise, `tickets.md` for what a ticket may claim and declare, and this module for how any of it is written down. A subject none of them covers is a new module, which is a new pointer in `AGENTS.md` in the same change.

**A definition is not a rule, and lives in `CONTEXT.md`.** That file says what a capitalised term means and what to avoid calling it; what is *true of* the term is a rule and belongs in the module that governs it. An entry that specifies behaviour is a rule wearing a glossary's clothes, and a reader looking for the law then has two places to look and no way to tell which is current.

**A rule governing one Skill's own behaviour needs nothing central.** That Skill's shipped documents are where a reader already meets it — its `SKILL.md`, its `help.md`, the files under its `references/` — and a second statement in the rules document is a second thing to keep true for the sake of a reader who was never going to look there. The test is who has to obey the rule: everybody who writes here, or one Skill's own body. Audience decides placement, and it decides it before format does.

## What earns a record

**A decision earns a record only when all three of these hold at once: it is hard to reverse, it is surprising without its context, and it is the result of a real trade-off.** A decision failing any of the three is a rule and goes where the section above puts it. Most of what a change settles is neither hard to reverse nor surprising, and a record written for it costs every later reader the same attention as one that had to be. An archive grown without that bar fills with how-texts wearing a why-document's clothes, and the three criteria are what keep them out.

**A record takes the next free number, and keeps it.** The number is the record's address and is how every other document cites it. What *next free* means, and what a gap in the sequence does and does not mean, is stated once in the archive's ingress, `docs/adr/README.md`.

**A record is never rewritten.** Its value is that it describes the world at its date, and a record edited to agree with today is a record that has stopped being evidence of anything. A change that falsifies an incidental example inside one may correct that example in place; nothing else in the body moves.

## The outrun-pointer duty is retired

**A later record no longer reaches back to annotate the record it narrows.** The duty ADR-0075 imposed existed because the archive was read as current law: a record whose premise a later one replaced went on asserting it, and a reader looking for how something works found a confident wrong answer in the one place this repository pointed at for architecture. The rules document removes that reader. Nothing is answered from the archive about what applies now, so the archive no longer has to be kept self-consistent about a question it is not asked.

**What replaces it is the rules document being the single current statement.** The pointer kept one shelf of prose true for a reader who had nowhere better to look; a module that is rewritten whenever its rule changes keeps the same reader right without any record having to be touched at all. Retiring the duty gives back everything ADR-0075 records it costing, the sanctioned edit to a body of documents whose whole discipline is not being edited most of all.

**What a reader owes in exchange is to read a record as of its own date.** A record written while the duty stood may carry a pointer sentence naming the record that outran it, and that sentence stays where it is; the absence of one now says nothing at all. What tells a reader whether a decision still holds is the rules document, in every case.

## The always-loaded file

**`AGENTS.md` is the only file loaded by default, and it is a pointer list.** Beyond the precedence it claims for itself and for the files it names, it holds no rule: a rule stated there is loaded into every session, most of which will never need it — exactly the dilution the rules document is organised against — and it is a rule in two places besides. What `AGENTS.md` does is route.

**Every entry is written as ``- `<path>` — read when <the class of work>``.** The situation names the class of work that covers every reason to open the file, rather than example terms from inside it — a pointer that lists terms does not fire on the terms it left out. Completeness is the test: if any heading or term in the target would not fire the line, the situation is too narrow. A module of the rules document is reachable only if a line here names it, and the suite fails a line whose path nothing carries.

## Skill bodies

**Every Skill body is authored under `/writing-for-agents`.** That skill governs how the prose is written — what an agent reading the body will actually execute, and what merely spends its context — while `skills.md` governs what the body has to carry. A body is an instruction loaded into somebody else's session, so a line it spends on ceremony is a line the reader pays for before reaching the instruction that matters, and the two documents are read together for that reason.
