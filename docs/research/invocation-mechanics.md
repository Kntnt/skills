# The invocation mechanics of a Skill — problem statement

> Written 2026-09-05 against `main` at a69473f and `rework` at b140032, from a design conversation between Thomas and Claude. It states a problem and a candidate shape for its solution; it decides nothing. Its purpose is to be the input to a later discussion and, after that, to `/to-tickets`. Thomas settled the track the same day: `main` survives and `rework` is a source to cherry-pick from, so this work lands on `main`.

## The observation

Every Skill in this collection is invoked through the same mechanism: an Invocation Envelope split at the first standalone `--`, exact help forms routed to a shipped manpage, a strict Formal Invocation grammar in one fixed order, and one refusal shape for every invalid form. The mechanism is the same in every Skill, yet every Skill carries the text that asks the agent to perform it, and the agent performs it by reading. The observation is that this text is a large share of the small Skills, that it is identical from one Skill to the next, and that a mechanism this uniform and this deterministic should be stated once and, where it can be, executed by a script rather than re-derived by a model on every invocation.

## What every Skill carries today, measured on `main`

| Block | Where | Size | Count | Identical across Skills |
| --- | --- | --- | --- | --- |
| Dependency preamble: checker discovery, `$HERE`, `$LIBRARY` | body | 470–665 B | 13 of 16 | near-identical |
| `## Invocation Envelope` + `## Help` | body | ~345 B | 16 of 16 | identical but for the Skill name |
| Parse step and refusal clause ("A flag is refused rather than ignored … teaches that flags sometimes do nothing") | body, `## Arguments` and step 1 | 200–400 B | 16 of 16 | identical but for the help route |
| `## INVOCATION ENVELOPE` | `help.md` | 3,343 B | 16 pages | byte-identical |

The fixed body mechanics add up to about 15 KB of the 212 KB the sixteen bodies weigh, which is 7% overall, 14% on the median body, and 33% on `commit` and `push`. The manpages carry a further 53 KB of one paragraph set repeated sixteen times. The `## Arguments` sections, 29 KB in total, are mixed: the grammar line and the invalid forms are what the agent parses against and belong there under ADR-0046, but a large share of the prose argues the rule rather than states it, which is the register problem treated separately at the end of this file.

## How the mechanics are enforced today

The coding standard says it plainly: the Skills have no parser of their own, and the agent reading these files is the whole of the enforcement. The strictness ADR-0059 asks for — an undeclared flag refused, an operand before a flag refused, an incomplete form refused, never repaired — is carried out by a probabilistic reader applying a grammar it has just read, on every invocation, in every Skill.

Nothing tests that behaviour. The suite is structural: it holds the `argument-hint`, `## SYNOPSIS`, and `## OPTIONS` to one flag set, checks the invocation order of every written form, and checks that the refusal clause is present. The worked-cases table that pins the Envelope split exists as prose the agent is expected to internalise, not as a test anything runs. "Well-tested" therefore means "held to a form by the suite and exercised by daily use", and a rewrite of the mechanism has no behavioural safety net to lean on today.

The collection already runs part of the mechanism through scripts, unevenly. The Manager passes every verb's flags to `kntnt.py`, which parses them with `argparse`, refuses an undeclared flag with that verb's synopsis and help route, and prints a manpage on request through its `manpage` subcommand; `steps/help.md` tells the agent to pass the arguments on as they stand and to write none of the refusal itself. `orchestrate` passes its flags through to `run.py`. The editorial Skills resolve `--language` through `languages.py`. The Library holds `argument_grammar.py`, the one argument grammar for engines that refuse in JSON (ADR-0152). So the precedent for a script reading a Formal Invocation exists in the most-used Skill of the collection; what does not exist is one such reader that every Skill can call.

## What the `rework` branch has already done

Commit 7b795df on `rework`, "A Skill body starts at its first step", did the first half of what the observation asks for.

- `library/references/invocation-envelope.md` (5 KB) states the Envelope contract once: separator, boundaries on a Contextual Instruction, both refusals, nested Skills, and the worked-cases table.
- Every body replaces `## Invocation Envelope` and `## Help` with a two-line `## Invocation` that points at that file and names the Skill's own help routes. Every `## Arguments` ends with "refused as `$LIBRARY/references/invocation-envelope.md` says" instead of restating the refusal.
- Every manpage's `## INVOCATION ENVELOPE` shrinks from 3,343 B to an 865 B pointer.
- `docs/rules/skills.md` states the rule, and `docs/rules/docs.md` puts every body under `/writing-for-agents`.

What that bought is one editable copy of the contract, about 330 B per body, and about 2.5 KB per manpage. Nothing else in the existing bodies changed: measured from the fork commit, every body on `rework` is 300–330 B smaller and no Steps section was rewritten. The bodies on `rework` look far smaller than on `main` only because `main` has grown since the fork — `proofread` from 9.3 KB to 13.8 KB, `redline` from 12.9 KB to 22.8 KB, `model-selector` from 19.5 KB to 30.8 KB, `orchestrate` from 46.9 KB to 66.9 KB — in eleven days of tickets. The rule that every body is authored under `/writing-for-agents` exists on `rework`, but no existing body has yet been rewritten under it.

What it did not do is change who executes the contract. On `rework` as on `main`, the body tells the agent to split the Envelope, route help, parse against a prose grammar, and compose the refusal itself. The contract is now read from one file instead of sixteen, but it is still read.

## The problem, stated

1. The collection's strict invocation grammar is executed by the model, from a contract it reads and applies, on every invocation of every Skill, with no deterministic check and no behavioural test. The strictness the collection promises is therefore as reliable as the reader on that run.
2. The text that asks the model to do so is the same in every Skill, weighs a third of the small ones, and sits before the part that is the Skill. On `rework` the text is shorter but the arrangement is the same.

## A candidate shape for the solution

One Library engine, one call at the top of every body, doing everything mechanical that a body opens with today.

The body's first instruction becomes: hand the raw invocation payload to the engine, verbatim, on stdin; if it exits 2, print its stdout and stop; if it exits 0, its stdout is JSON carrying the command path, the flags, the operands, and the Contextual Instruction, and the Steps begin from that. The engine, in one call, locates the Manager and the Library, runs the existing dependency check, splits the Envelope at the first standalone `--`, answers an exact help form by printing the addressed page (as `kntnt.py manpage` already does), validates the Formal Invocation against the Skill's grammar, and on an invalid form prints the refusal in the collection's one shape — the error named, the addressed `## SYNOPSIS` verbatim, the help route — and exits 2.

The grammar need not be declared anew. The suite already machine-reads the `argument-hint` and every `## SYNOPSIS` form, and already holds the three grammar surfaces to one flag set; the engine can read the same surfaces. Where that proves too loose — valueless flags, operand arity, a value vocabulary such as `--in-place[=on|off]` — a small declaration in the shape ADR-0152 already gives engines is the fallback, and a rare exclusion such as `--output` against `--in-place=on` may stay in prose.

What stays prose is the semantic half of the Envelope: whether a Contextual Instruction is addressable, conflicting, or scope-widening; whether Conversation Context applies; the Capabilities the agent answers as the Harness; what an operand means once it is known to be one. That half is small, judgement rather than grammar, and already lives in `invocation-envelope.md` on `rework`.

The worked-cases table and each Skill's list of invalid forms then become tests of the engine, which is the behavioural safety net the mechanism has never had.

## What it costs and what constrains it

- **The payload reaches the model as text, never a process.** ADR-0008 forbids the `$ARGUMENTS` preprocessor for portability; Claude Code appends `ARGUMENTS: <input>` to the body when no placeholder receives it, and Codex leaves the invocation in the message. The model must hand the payload to the engine verbatim. That is the act the Manager already asks of it ("pass the user's flags on as they stand"), and it is simpler than applying a grammar, but a multi-line Contextual Instruction with quotes needs stdin or a heredoc rather than a shell argument.
- **`uv` becomes a dependency of every Skill that calls the engine.** ADR-0012 keeps a Skill with nothing to declare free of the checker so that it does not acquire `uv` for nothing; `tldr` and `brief` have no binaries today. Either the call is optional where the grammar has nothing to check, or that rule changes.
- **One `uv run` per invocation**, on the order of a few hundred milliseconds. The thirteen Skills with dependencies already pay it for the checker; the engine folds into the same call.
- **The rework's own doctrine.** The pipeline Skills are designed with no engine of their own because nothing in them is deterministic enough to be worth one. Argument parsing is exactly that deterministic, and a Library engine is what ADR-0152 already established for engines; this is an extension of that record, not a reversal of the doctrine.
- **It is a Solo Ticket.** The body of every shipped Skill changes under one invariant, so the ticket that rewrites the bodies builds alone (ADR-0099).
- **The contract file lives on `rework`.** `invocation-envelope.md` and the pointer form exist only there. Bringing them to `main` is the first step, and it is a re-implementation against `main`'s current bodies rather than a clean cherry-pick, `main` having changed every one of those bodies since the fork and added three Skills the rework never saw.

## Decisions to settle before tickets are written

1. **Track.** Settled 2026-09-05: `main`, as ordinary `ready-for-agent` tickets.
2. **Where the engine lives.** A verb on `kntnt.py`, which the body can already find before the Library is located, or a script in `library/scripts/` reached through the checker's answer.
3. **The grammar source.** Read from `argument-hint` and `## SYNOPSIS`, or from a small declaration per Skill.
4. **The flagless Skills.** Whether a Skill with no flags and no subcommands calls the engine at all.
5. **The payload transport.** Stdin, a heredoc, or a file.
6. **What the suite holds afterwards.** The engine's behaviour, with the worked-cases table and each Skill's invalid forms as its cases, in place of the clauses the suite pins in prose today.

## Candidate tickets, in dependency order

0. The envelope extraction from `rework` (commit 7b795df) re-implemented on `main`: the contract in `library/references/invocation-envelope.md`, the pointer form in every body and manpage, the rule in the standard, the suite adjusted. Builds alone.
1. The engine: Envelope split, help routing, grammar validation, and refusal, with the worked-cases table and the Manager's own verbs as its first tests. Additive; nothing else changes.
2. The Manager moves its own help routing and verb dispatch onto the engine, being the Skill that half-does this already.
3. Every other body opens with the one call, and its preamble, `## Invocation`, and refusal prose go. Builds alone.
4. The rules module and the suite: what a body has to carry changes, and the assertions that pin the old clauses change with it.
5. The manpage `## INVOCATION ENVELOPE` pointer and the README, if the engine changes what a reader is told.

## The related but separate problem: register

The observation above is about mechanism. A second observation, treated separately because its fix is different, is that the bodies argue their rules instead of stating them: `tldr` spends 1.5 KB of `## Arguments` explaining twice why a dash-prefixed token is prose, and the reason "because a flag accepted and ignored teaches that flags sometimes do nothing" appears in sixteen bodies. That is the rationale register of a decision record leaking into an instruction, and it is what ADR-0046's own test rejects: removing the passage changes nothing the agent does. `rework` has already put every body under `/writing-for-agents` as a rule, but no existing body has been rewritten under it yet, and on `main` the editorial and model-selector bodies have grown by half to three quarters since the fork, one ticket at a time. The mechanism work should land first, because it deletes the largest identical blocks and gives the prose rewrite a behavioural check to run against; the prose rewrite then goes one Skill per ticket, smallest first, with the editorial family verified against `docs/evaluation/protocol.md`.

**How a rewrite proves it removed and added nothing.** The Skills are well tried, and the suite is structural, so a rewritten body has no test to lean on outside the editorial family. Every prose ticket therefore carries a two-sided behaviour diff as an acceptance criterion: a reviewer with fresh context — a subagent given the body before and the body after, and nothing else, not the ticket and not the rewriting session's account — lists every behaviour present in one body and absent from the other: a step taken, a condition checked, a refusal, a delivery, a wait for confirmation, a file read, a script run. The list is empty, or every item on it is deliberate and named in the ticket. The engine's tests already hold the mechanics half of every body, and the editorial family additionally runs the fixture protocol; the diff is what covers every other Skill, which is most of them. A rewrite the reviewer cannot pass on its two bodies alone is a rewrite that changed something, whatever the rewriting session believed.
