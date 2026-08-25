# Phase 1, step 2 — the doc reform, as settled

> Decisions taken with Thomas on 2026-08-25, informed by the triage in `02-adr-triage.md`. This file is the input to the ticket breakdown. Written against commit `e75e266`. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

## What was decided

**The rules document is `docs/rules/`.** `docs/coding-standard/` is renamed to it and gains three modules: `collection.md` (the Manager's behavioural law), `tickets.md` (how a ticket is written), and `docs.md` (how this repository records decisions). The existing `general.md`, `python.md` and `skills.md` move unchanged in content. No shipped Skill file points at the old path — the rename touches `AGENTS.md`, `CONTRIBUTING.md`, `skills.md`'s own internal links and the suite, and nothing else.

**`CONTEXT.md` keeps its name and place and holds definitions only.** Every normative sentence in it moves to `docs/rules/collection.md`; what stays is the term, what it means, and its *Avoid* list. This also makes the file safe against Matt Pocock's `/grill-with-docs` regenerating it: today a regeneration would destroy specifications that live nowhere else, and afterwards it costs at most some wording.

**Six consolidation records, and orchestrate's set gets none.** The six are: the distribution model; the invocation grammar; what a Skill ships; the editorial contract; routing and evidence; how this repository records decisions and writes tickets. The 22 records belonging to orchestrate's runtime die with the Skill in phase 3 — their ideas are already absorbed into the pipeline design. Twenty-one of them are marked `†` in the triage table, which means one thing only: the `/dispatch` design should cite that record's field evidence from git rather than rediscover it. The mark is not what keeps a record alive through phase 1 — being cited by `run.py` or the orchestrate tests is, which is why ADR-0058 stays too without carrying the mark.

**ADR-0075's outrun-pointer duty is retired.** The archive becomes strictly historical: `docs/adr/` is never auto-loaded, its ingress says the rules document is the authority on what applies now, and a record is written only under domain-modeling's three criteria — hard to reverse, surprising without context, the result of a real trade-off. The suite keeps numbering uniqueness and citation resolution and loses the relation machinery.

**`AGENTS.md` stays a pure pointer list.** It is the only always-loaded file. The rules modules are reached through `read when` lines, and `/compile` inlines the module a ticket actually touches.

**A Skill is lean, and a rule that costs lines in every Skill must earn them.** Measured across the collection, 27 % of all shipped Skill prose is collection ceremony before the first step — 82 % of the Manager's body, 70 % of `delegation`'s, 59 % of `commit`'s. The ceremony is mandated by `skills.md`, so the cut is a rule change. Every Skill body is authored under `/writing-for-agents`, which becomes a rules line and an `AGENTS.md` pointer.

**The Invocation Envelope keeps its behaviour and loses its restatements.** The contract — the reserved separator, what a Contextual Instruction may and may not settle, the two refusal categories — becomes one reference in the Collection Library plus a rules line. Each Skill body and each manpage carries a pointer instead of the section. The mandated rationale for why a flag is refused leaves every body, and the test pinning it goes with it. A user meets the same behaviour.

## The slices

Eleven tickets. Each is sized for one fresh context window and declares its blocking edges. Two rewrite a rule every shipped file is under and therefore declare `Builds alone` (ADR-0099). None of them names a record number for a record it creates; each consolidation ticket takes the next free number at the time of writing and its commit says which number was taken (ADR-0067).

**T1 — Rename `docs/coding-standard/` to `docs/rules/`.** Move the three modules unchanged, update the References lines in `AGENTS.md`, the standard's own internal links, `CONTRIBUTING.md` step 3, and every path the suite resolves. No prose changes. *Blocked by: nothing.* Delivers: one directory whose name says what it holds, with a green suite.

**T2 — `docs/rules/collection.md`.** State the Manager's behavioural law as rules: layers and detection, the transport boundary, the Catalog and its fallback, the Digest and *Deviating*, what Select, Update and Uninstall each promise, the dependency gate and Capabilities, disk-as-truth and disk-as-report, the Sandbox, the renderer boundary. Draw from the records the triage bins `C1` and from `CONTEXT.md`'s normative sentences, citing each record for the reasoning rather than restating it. *Blocked by: T1.* Delivers: a reader can learn what the Manager promises without opening a record.

**T3 — `CONTEXT.md` holds definitions only.** Strip every normative sentence from the glossary, leaving term, meaning and *Avoid*; where a term's law now lives in `collection.md`, the entry says so in one clause. Remove the four orchestrate-only terms the pipeline does not keep, and keep Solo Ticket. *Blocked by: T2.* Delivers: a glossary a regeneration cannot destroy anything irreplaceable in.

**T4 — `docs/rules/tickets.md`.** State the four assertions rule (no record numbers, symbols rather than line numbers, quantify rather than enumerate, name the vantage commit) and the Solo Ticket declaration, with the split between the durable ticket layer and the just-in-time plan layer stated explicitly. Replace the two record-specific References lines in `AGENTS.md` with one pointer here. *Blocked by: T1.* Delivers: a ticket author meets the rules in one place.

**T5 — `docs/rules/docs.md`.** State the model: the rules document is what applies now, `docs/adr/` is a historical archive read on demand and never auto-loaded, a record is earned under the three criteria, the outrun-pointer duty is retired, `AGENTS.md` is a pointer list written to the `read when` convention, audience decides placement, and every Skill body is authored under `/writing-for-agents`. Add the archive's ingress under `docs/adr/`. *Blocked by: T1.* Delivers: the next author knows where a rule goes without asking.

**T6 — Cut the per-skill ceremony. `Builds alone`.** Rewrite the mandates in `docs/rules/skills.md`; move the Invocation Envelope contract to one Collection Library reference; replace the `## Invocation Envelope` section, the `## Help` prose and the refusal rationale in every shipped `SKILL.md` with pointers; do the same for the `## INVOCATION ENVELOPE` section in every manpage; delete the test that pins the rationale and adjust the suite to the new shape. Excludes `skills/code/orchestrate/`, which phase 3 deletes. *Blocked by: T1.* Delivers: every Skill body starts at its first step within a screen, with identical user-facing behaviour.

**T7 — The distribution model record.** Write the consolidation record for the `C1` set: name every record it supersedes, carry forward only the why-chains still alive, and leave the rules where T2 put them. *Blocked by: T2.* Delivers: 25 records' reasoning in one readable record.

**T8 — The grammar and Skill-form records.** Write the two consolidation records for the `C2` and `C3` sets, taking consecutive next-free numbers. *Blocked by: T6, T7.* Delivers: the invocation grammar and what a Skill ships, each in one record, matching the rules as T6 left them.

**T9 — The editorial and routing records.** Write the two consolidation records for the `C4` and `C5` sets. *Blocked by: T8.* Delivers: the editorial contract and the routing-and-evidence chain, each in one record.

**T10 — The decisions-and-tickets record.** Write the consolidation record for the `C6` set, which is also this reform's own record: what the rules document is, what the archive is, and why the pointer duty is retired. *Blocked by: T4, T5, T9.* Delivers: the reform is recorded where a reader will look for it.

**T11 — Delete the folded and dropped records, and repoint every surviving citation. `Builds alone`.** Delete every record the triage table bins `DROP` or `C1`–`C6`, except the twenty-two the table identifies as orchestrate's runtime, which phase 3 removes with the Skill — 73 records in all. Repoint every citation to a deleted number in `skills/kntnt/scripts/kntnt.py`, the model-selector and Library scripts, `docs/rules/`, `docs/research/`, `docs/evaluation/`, `CONTRIBUTING.md`, `CONTEXT.md` and the twelve test modules that cite one. Rewrite `tests/test_adr.py`: numbering uniqueness and citation resolution stay, the relation machinery and its hand-written pairs go. Leave `CHANGELOG.md` and closed tickets exactly as they stand. *Blocked by: T10.* Delivers: an archive of 29 records — 6 consolidations, 1 kept, 22 orchestrate records awaiting phase 3 — with every citation in the tree resolving.

## What phase 1 deliberately does not do

Orchestrate's 22 records and its `CONTEXT.md` terms survive phase 1 and are swept in phase 3 with the Skill, because 64 citations in its own `run.py` and the whole of `tests/test_orchestrate.py` depend on them while the code ships. The pipeline's own rules module waits for phase 2, when there is something to state. `CHANGELOG.md` is never rewritten.
