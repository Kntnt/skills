# Rules — where a rule and a decision go

Read before changing anything this repository has written down: before deciding where a rule belongs, before writing a decision record, before authoring a document an agent loads, and before altering prose that already states a rule.

This module covers where a rule is written down in this repository, what earns a record in the archive, how the two relate, and what a change owes the prose that already states what it changes. It is not about what a ticket may claim while it waits, which is `tickets.md`, nor about the form of a Skill's or a Feature's shipped files, which is `skills.md`, nor about code form, which is `general.md`. It is the module a contributor reads when the question is *where does this go*, and the one a contributor changing prose alone reads before changing it.

The capitalised terms are defined in [`CONTEXT.md`](../../CONTEXT.md). That file says what a term means; this module says what is true of it.

The rules whose reasoning is settled in a decision record are named here in a phrase and cited to the record rather than argued again — the record is where the alternatives and their costs live, and a second telling of the argument is a second thing to keep true.

## Two documents, and the question each answers

**The rules modules under `docs/rules/` are what applies now, and they are the authority on it.** One module per subject, every line of it current law phrased as a rule. A module is edited rather than grown: a rule that changes is rewritten where it stands, so the module goes on saying one thing about its subject. A reader who wants to know what is true today needs nothing else, and in particular needs to read nothing forward and apply no supersessions by hand.

**`docs/adr/` is a historical archive, read on demand and never loaded by default.** A record describes the world at its own date and answers why a rule became what it is: what the alternatives were, what they cost, what evidence forced the choice. It does not answer what is true today and cannot be made to — records are not rewritten, so the archive as a whole states what was decided at many different dates, with nothing in it saying which of those decisions survived. That is the archive doing its job rather than a fault in it. The two questions have two documents, and conflating them is what this arrangement exists to end; [`docs/adr/README.md`](../adr/README.md) is where a reader who opens the directory is told so.

**A rule states itself once and cites the record for the reasoning.** A rules module does not reproduce a record's argument, and a record does not restate the rule as it now stands; each copy is a thing that has to be kept true, and one copy is the one a reviewer can diff. Where a change takes a decision in a rule area binding more than one Skill, the resulting rule is stated in its module in the same change.

## Where a rule goes

**The subject decides the module.** A rule binding whoever writes here belongs in `docs/rules/`, in the module whose subject it is: `general.md` for code form, `python.md` for the language, `skills.md` for what a Skill or a Feature ships, `collection.md` for what the Manager's verbs and the collection promise, `routing.md` for how a Skill routes delegated work and what it may file as evidence, `tickets.md` for what a ticket may claim and declare, and this module for how any of it is written down and for what a change owes what is already written. A subject none of them covers is a new module, which is a new pointer in `AGENTS.md` in the same change.

**A definition is not a rule, and lives in `CONTEXT.md`.** That file says what a capitalised term means and what to avoid calling it; what is *true of* the term is a rule and belongs in the module that governs it. An entry that specifies behaviour is a rule wearing a glossary's clothes, and a reader looking for the law then has two places to look and no way to tell which is current.

**A rule governing one Skill's own behaviour lives in that Skill's shipped files and nowhere central.** Its `SKILL.md`, its `help.md`, the files under its `references/` — that is where the reader who has to obey it already meets it, and a second statement in a rules module is a second thing to keep true for the sake of a reader who was never going to look there. The test is who has to obey the rule: everybody who writes here, or one Skill's own body.

**Audience decides where a document goes, and it decides it before format does.** Every document here is written for somebody, and the somebody is what settles the directory: `docs/rules/` for whoever writes in this repository, a Skill's own shipped files for the agent running that Skill, `CONTEXT.md` for anybody using a term of this collection, `docs/adr/` for a reader asking why, `CONTRIBUTING.md` for a contributor from outside, `docs/evaluation/` for whoever runs a Skill against the fixture corpus, and `docs/research/` for a finding that informs work without binding it. A document filed by what it looks like rather than by who reads it is a document its reader does not find.

## What a change owes what is already written

**A rule this repository documents is a shared contract, so a change to it sweeps the prose that shows it.** The change is not finished when the module stating the rule is rewritten: every other surface that asserted the old rule goes on asserting it, and a reader who meets one of those first never learns that it changed. How a document is treated turns on what it asserts rather than on what it displays, and the archive is the case where that matters most — *A record is never rewritten*, below, says what a change does and does not do to one.

**Enumerate by what a surface asserts rather than by how it words it.** A caller of a symbol carries that symbol's own name, so a search for the name finds it; a sentence restating a rule carries whatever words its author chose, so a search for the wording finds only the copies that happen to agree with the one you are holding. The rules module, a `CONTEXT.md` entry, a manpage, a steps page, a README section, a comment beside the code, a docstring and a test's own name are all one contract's surfaces, and any of them can be the one left stranded — a docstring saying *tears down twice* states the teardown count as surely as the page that spells it out, and no search for the page's words will reach it.

**Enumerate what points at a rule as well as what states it.** A module's trigger line and its scope sentence, the exclusion clauses its siblings use to name its subject, this repository's subject index, and the pointers in `AGENTS.md` and `CONTRIBUTING.md`. A pointer asserts nothing, so no search for the rule's content reaches one, and a pointer left describing the narrower subject sends a reader to a module they will never open.

**Released history is left exactly as it stands, the changelog and closed tickets included.** It is an account of what shipped rather than of what holds now, so a change that falsifies today's rule falsifies nothing it claims.

## What earns a record

**A decision earns a record only when all three of the criteria `/domain-modeling` states hold at once: it is hard to reverse, it is surprising without its context, and it is the result of a real trade-off.** A decision failing any of the three is a rule and goes where *Where a rule goes* puts it. Most of what a change settles is neither hard to reverse nor surprising, and a record written for it costs every later reader the same attention as one that had to be written. An archive grown without that bar fills with how-texts wearing a why-document's clothes, and the three criteria are what keep them out.

**A record takes the next free number, and keeps it.** The number is the record's address and is how every other document cites it; the suite refuses a citation no record answers to. What *next free* means, and what a gap in the sequence does and does not mean, is stated once in the archive's ingress, [`docs/adr/README.md`](../adr/README.md).

**A record is never rewritten.** Its value is that it describes the world at its own date, and a record edited to agree with today is a record that has stopped being evidence of anything. A change that falsifies what a record asserts leaves it exactly as it stands and annotates it with nothing. A change that falsifies an incidental example inside one may correct that example in place; nothing else in the body moves.

## The outrun-pointer duty is retired

**A later record no longer reaches back to annotate the record it narrows.** The duty this repository used to impose existed because the archive was read as current law: a record whose premise a later one replaced went on asserting it, and a reader looking for how something works found a confident wrong answer in the one place this repository pointed at for architecture. The rules modules remove that reader. Nothing is answered from the archive about what applies now, so the archive no longer has to be kept self-consistent about a question it is not asked. The reasoning is in the reform's own record (ADR-0180).

**What replaces it is a rules module being the single current statement.** The pointer kept one shelf of prose true for a reader who had nowhere better to look; a module rewritten whenever its rule changes keeps the same reader right without any record having to be touched at all. Retiring the duty gives back everything ADR-0180 records that duty costing — the sanctioned edit to a body of documents whose whole discipline is not being edited, most of all.

**What a reader owes in exchange is to read a record as of its own date.** A record written while the duty stood may carry a pointer sentence naming the record that outran it, and that sentence stays where it is; the absence of one now says nothing at all. What tells a reader whether a decision still holds is the rules module, in every case.

## The always-loaded file

**`AGENTS.md` is the only file loaded by default, and it is a pointer list.** Beyond the precedence it claims for itself and for the files it names, it holds no rule: a rule stated there is loaded into every session, most of which will never need it — exactly the dilution the rules modules are organised against — and it is a rule in two places besides. What `AGENTS.md` does is route. The one standing exception is the section headed `## ⚠️ TEMPORARY: the rework branch is a source, not a successor`, which holds rules by exception — the standing of the `rework` branch and the `../skills-rework` worktree, and what may never be done to either — stated nowhere else in the tree. The exception ends when the section does: that section says of itself that it is removed once everything worth bringing over from `rework` has landed and the branch is deleted, so nothing has to remember to retire the exception separately.

**Every entry is written as ``- `<path>` — read when <the class of work>``.** The situation names the class of work that covers every reason to open the file, rather than example terms from inside it — a pointer that lists terms does not fire on the terms it left out. Completeness is the test: if any heading or term in the target would not fire the line, the situation is too narrow. A rules module is reachable only if a line there names it, and the suite fails a line whose path nothing carries.

## Skill bodies

**Every Skill body is authored under `/writing-for-agents`.** That skill governs how the prose is written — what an agent reading the body will actually execute, and what merely spends its context — while `skills.md` governs what the body has to carry. A body is an instruction loaded into somebody else's session, so a line it spends on ceremony is a line the reader pays for before reaching the instruction that matters, and the two documents are read together for that reason.
