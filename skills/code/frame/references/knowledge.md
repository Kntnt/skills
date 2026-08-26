# Where knowledge goes, and how it comes back

A framing produces two kinds of durable knowledge and one kind that is not durable at all. A term the framing pinned down goes into the repository's glossary. A decision that clears the bar below earns a record in its decision archive. Everything else the Skill decided is a ledger entry in section 5 and nothing more — a decision failing the bar is a rule or a preference, and a record written for it costs every later reader the same attention as one that had to be.

Both are written as they crystallise, in the round or the report that settles them, rather than collected up at the end. A term pinned down in round two is the vocabulary rounds three and four are phrased in, and knowledge written at the close is knowledge written by whoever is left holding the session.

Everything written goes into section 7 of the record with its address, as it is written. That section is the only list of what this framing put into the durable layer, and both duties below are performed against it.

## Where it goes

**Follow the target repository's own convention where it declares one.** Its always-loaded agent file and the documents that file points at say where a term is defined and where a decision is recorded; you read them in step 4, so you already hold the answer. A repository that keeps its glossary in one file and its records in one directory is told from one that keeps neither by looking, not by guessing.

**Where it declares none, the default is single-context**: `CONTEXT.md` at the repository root for the terms, `docs/adr/` beside it for the records, one file per record named for the decision and numbered with the next free number in that directory. Create either only when you have something to put in it.

**A term is what a word means, and nothing else.** What is *true of* the term — what happens to it, what may be done with it — is a rule, and a rule lives wherever that repository keeps its rules. A glossary entry that specifies behaviour leaves a later reader two places to look and no way to tell which is current.

**A record is written as of its own date and is never rewritten.** It says what the alternatives were, what they cost, and what forced the choice. It does not restate the rule that resulted; the rule lives where the repository keeps rules, and cites the record for the reasoning.

## The bar a record has to clear

All three at once, or it is a ledger entry:

1. **Hard to reverse.** Undoing it later costs real work — a migration, a rename across the tree, a published interface — rather than an edit.
2. **Surprising without its context.** A reader meeting the result cold would ask why it is like that, and the code cannot tell them.
3. **The result of a real trade-off.** Something was given up. A choice with one plausible option was not a decision, however carefully it was made.

Most of what a framing settles is none of these. That is the ordinary case, and the ledger is where it belongs.

## Withdrawing what a discarded framing wrote

A record the owner discards at the start of a run takes its section 7 with it, as an offer rather than a sweep. Go through the entries one at a time and, for each, name what it is, where it was written, and what removing it would take out; ask, and act on the answer. An entry the owner keeps stays where it is — a decision that cleared the bar above can stand on its own merit even where the work it came from was never built.

This is bounded because the manifest is. Nothing hunts for knowledge a framing wrote that is not on a list: an unbounded search has to guess, and a guess deletes records that were never this framing's to remove. Where the manifest is gone, the withdrawal is not attempted and the discard says so.
