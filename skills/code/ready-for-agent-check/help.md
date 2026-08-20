# ready-for-agent-check

Read a ticket the way the agent that has to build it will read it, and find out what would stop it.

## Synopsis

`/ready-for-agent-check [#<ticket> ...]`

## Description

A ticket is written by somebody who knows what they meant. It is built by somebody who does not, hours or days later, in a session with no human in it. This skill puts a reader in that second position and asks the only question that matters there: could you carry this out from start to finish without stopping to ask?

Every ticket in scope is read by a subagent of its own, in a context window that had no part in writing it. That isolation is the whole mechanism and not a performance detail. A session that helped write a ticket reads its own intent back out of it and calls it clear; the builder cannot, and it is the builder's reading the maintainer needs to see. So the reviewer is told the ticket and nothing else — not what was decided while it was written, not that anybody thinks it is ready.

The reviewer is given the ticket as the tracker now holds it: the body it was filed with, then everything written on it since, oldest first and each comment attributed and dated. That matters here more than it looks. Triage posts its brief as a comment, so the settled decisions and the acceptance criteria of a triaged ticket are usually not in the body at all — a reviewer given the body alone would report a ticket full of open questions that were answered before it ever ran.

Half the check is done by looking rather than reading. A ticket makes claims about the code, the records, and the files, and those claims go stale between filing and building: a line number moves, a record number the ticket reserved is taken by something else, a list of *all the skills* stops being all of them. The reviewer checks each claim against the repository as it now stands and reports what the ticket says beside what is there.

Nothing is written. No label moves, no comment is posted, no ticket is closed. What comes back is advice, and what to do with it is yours.

## Scope

Typed bare, it checks every open ticket the tracker labels `ready-for-agent` — the set `/orchestrate` would work. Name tickets and it checks exactly those, whatever label they carry, so a ticket can be checked before it is labelled rather than after. That order is the useful one: the check exists to inform the decision to label, and a skill that demanded the label first would arrive after it.

## What it looks for

Seven ways a ticket fails the builder who gets it:

- **A decision left open** — options set out and none chosen, or a choice handed to the builder without saying the builder may make it. A criterion of the form *either do this, or explain why not* is a question, and a builder with nobody to ask stops at it.
- **A condition the builder cannot evaluate** — *if the other ticket has landed, do this, otherwise that*, where nothing available to the builder says which.
- **A criterion with no determinate outcome** — *appropriate*, *sensible*, *as needed*. A criterion nobody can be shown to have failed is one nothing verifies, and it gets marked done without anything being established.
- **A claim the repository no longer bears out** — a moved line, a renamed symbol, a reserved record number since taken, an enumeration that has grown.
- **A fact the ticket needs and does not carry** — a command named but not given, a convention cited but not located, a term the glossary does not define.
- **Scope that does not close** — nothing said about what is out of scope, or a scope that contradicts the criteria.
- **Work that is not an agent's to do** — product judgement, external access, a design decision deferred to a person, a check only a human can make. That ticket is not bad; it is a person's, and saying so is the answer.

## The report

Per ticket, one line answering whether a builder could carry it start to finish, and then the findings in two groups. **Stops** are what a builder cannot get past without asking — each one names the question it would ask and what the ticket would have to say instead for the question not to arise. **Costs** are what it gets past but pays for: a stale reference to reconcile, an ambiguity to resolve twice, a fact to go and find. Every finding quotes the sentence it is about.

There is no partial verdict. A reviewer that is unsure answers no, because the failure this check exists to prevent is a run that stops in the middle of the night.

## Options

None, and none is missing. This skill takes ticket references and nothing else: it reads the tracker, writes nothing back to it, changes nothing on disk, and asks no question — so there is no confirmation to assume, no layer to target, and no run to preview. A flag is refused rather than ignored where it has no work to do, which here is every flag there is.

## Notes

A flag with no work to do is refused rather than ignored, and this skill has no flags at all: nothing is written, nothing is asked, and nothing changes, so there is no question for `--yes` to answer and no gate for it to open. `/ready-for-agent-check --yes` is an error; `/ready-for-agent-check #12 #13` is not.

The verdict is advice and never a label. Nothing here moves a ticket to `ready-for-human`, takes a label off, or writes a comment — a check that relabelled what it disagreed with would be a second triage, made by a reader that was deliberately given less context than the first one had.

A ticket that passes is not a promise that the work will succeed, only that the ticket does not itself stop the builder. Whether the change is a good idea is triage's question, and it has already been asked.

## Dependencies

`gh` and `uv` on PATH, the manager installed, and a harness that can spawn subagents. The last one is a Capability no script can test: the skill asks you to confirm it, and does no work where it is not true. It is also the one this skill cannot do without in any degraded form — reviewing a ticket in the session that wrote it is not a lesser version of this check, it is the failure the check is built to avoid.

`gh` has to be authenticated for this repository, though only for reading: this skill never writes to the tracker.

## See also

`/orchestrate` works the tickets this skill reads, and is what a stop costs you when it is found at three in the morning instead of here. `/kntnt select` to Enable this skill elsewhere.
