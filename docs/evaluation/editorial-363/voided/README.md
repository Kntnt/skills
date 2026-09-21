# Attempts that were made and do not count

Ten `r`-arm attempts, preserved whole and counted against nothing. They are kept because the ticket says to preserve every run, and because the reason they are void is itself a finding.

**Why they are void.** Both editorial Skills declare `kntnt.capabilities: "subagents"`, and both require one: Write to start the fresh source checker, Redline to start the fresh correction agent its step 7 describes. The session that resumed this ticket is itself a subagent of an orchestrating session, and a subagent of that harness has no agent-spawning tool at all. Write's step 1 caught this and stopped correctly — that stop is `r-case-study-sv-r2-response.md` here, and it is the whole of what that attempt produced. Redline has no equivalent step, so Redline attempts in the same seat ran to completion and reported correction rounds whose fresh seat cannot be established. That gap is [#394](https://github.com/Kntnt/skills/issues/394).

Two of these attempts finished after a session-harness run had already started in the same directory, so which artefacts belonged to which run could not be established for them either. Where provenance could not be established the attempt was treated as not completed and the row was re-run, which is what the ticket instructs.

Every `r`-arm row was then re-run as a fresh top-level Claude Code session, and those runs are the ones under [`../runs/r/`](../runs/r/).

## What is here

- `en-positive-r2/`, `en-us-r1-r1/`, `en-us-r1-r2/`, `metonymy-sv-r1/`, `metonymy-sv-r2/`, `rhythm-en_GB-r1/`, `rhythm-en_GB-r2/` — seven Redline attempts in the subagent seat, each with the reply it gave, the artefact it delivered and its mechanical-pass evidence.
- `subagent-seat/case-study-sv-r1/` and `subagent-seat/case-study-sv-r3/` — two Write attempts in that seat that did produce checker evidence, which is why the seat's capability could not simply be assumed absent, and which is part of why the whole set is set aside rather than half of it kept.
- `r-case-study-sv-r2-response.md` and `r-case-study-sv-r2-finished.txt` — the Write run that stopped on the unsatisfied capability. This is the one attempt here that behaved exactly as its contract says it should.
