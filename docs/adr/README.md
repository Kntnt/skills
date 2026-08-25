# Decision records

This directory is a historical archive. Each file is one decision, written when it was taken, describing the world as it stood then and saying why the choice was made — what the alternatives were, what they cost, and what evidence forced it.

**It is not the authority on what applies now.** [`docs/rules/`](../rules/) is. Read a record to learn why a rule is what it is; read the rules document to learn what the rule is. Nothing here is loaded by default, and nothing here should be read forward and reconciled by hand to derive today's law — that derivation is exactly what the rules document exists to make unnecessary.

**A record is never rewritten, and nothing is annotated into it when a later decision outruns it.** So read a record as of its own date. A record written while an earlier convention stood may carry a sentence naming the record that outran it; that sentence stays where it is, and the absence of one says nothing. [`docs/rules/docs.md`](../rules/docs.md) states the rule, why the pointer duty was retired, and what a decision has to be before it earns a record here at all.

**A number is an address, not a position.** A record is `NNNN-slug.md` and is cited from anywhere in the repository as `ADR-NNNN`; the number belongs to that record for good, and the suite refuses a citation no record answers to. Gaps are legitimate — a number whose record was deleted, or was never written, stays empty rather than being reused, so the sequence is not dense and is not meant to be. The next free number is one above the highest the directory holds, never the lowest gap.
