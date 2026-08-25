# Phase 2, step 1 — `/frame`, as designed

> Draft written 2026-08-25 against commit `de06983`, from the `/frame` section of `00-brief.md` and from what this codebase answers. It is the input to the owner-level round (step 2) and, once that round has settled the residuals at the end, to the ticket breakdown. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

The dossier states what `/frame` is for; this file is the design that satisfies it, the boundaries judged along the way, and the residue only Thomas can settle. Everything above the residuals is settled — resolved from `docs/rules/`, from the Skills this one borrows from, and from what the collection already ships — and is not a question.

## What the Skill is

`/frame` maps a task before anything is built. It runs codebase recon in parallel with an interview and routes every open point into one of three bins: the codebase answers it, the frames answer it, or the owner answers it. Only the third bin becomes a question. What comes out is a Frame Record — the task, what binds, what the codebase said, what the owner decided, what the Skill decided in his stead, and what is deliberately still open — which is the input `/to-slices` synthesizes into the decision document and the tickets.

## The three bins, and the rule that separates them

**The codebase answers it.** What exists, how it is done here, what a term means, what the tests already cover, what the history says a thing was for. A recon subagent fetches it. It is never a question, and a question the Skill asked that a file could have answered is a defect of this Skill rather than an economy.

**The frames answer it.** A choice with one right answer inside the constraints already established: naming inside a convention the repository keeps, placement inside a structure it already has, a library already in its dependency set, the shape of an error beside its siblings. The Skill decides, and writes the choice, the alternative it passed over, and the frame it decided under into the decision ledger.

**Only the owner answers it.** Product behaviour, user experience, priority, architecture direction, and any trade-off carrying a cost, risk, or reversibility consequence he would want to weigh. Asked in frontier rounds, each question numbered, phrased as the consequence he is choosing between rather than the mechanism that delivers it, with a recommended answer and what that answer costs. The vocabulary is the repository's own — `CONTEXT.md` where it has one, established terms otherwise, and nothing invented for the occasion.

**The tie-break is reversibility.** A point that could sit in either of the last two bins goes to the owner when the decision is hard to reverse or would surprise him later, and to the ledger otherwise. The ledger is what makes that safe: a decision he would have made differently is one he vetoes, and a veto turns it back into a question.

## The frames themselves

Before any question, the Skill establishes what binds. It reads the repository's always-loaded file — `AGENTS.md`, `CLAUDE.md`, whichever it keeps — follows the pointers to the rule modules the task actually touches, reads the glossary for vocabulary, and finds how the repository verifies itself. That set is the Frames section of the record: the standing constraints every later decision is checked against, and the reason a ledger decision can be taken without asking. This is where phase 1 pays for itself — the frames are one short read here rather than a derivation across eighty records.

## Recon

Recon is delegated, and delegation here follows the collection's own rule rather than a private arrangement: the Skill routes through model-selector's public `route` Interface and reads none of its private references (`docs/rules/collection.md`, *Routing and evidence*). One route request covers a recon wave as an ordered batch, because every recon brief in a wave is the same execution class — read-only, reversible, no consequence of its own, heavy on context and tools, and checked by the main agent, which reads the answer and can spot-check the evidence addresses it carries. A selected decision launches its subagents with exactly the controls it names; a reported inheritance launches them on the exact main seat; a refusal means that recon is done on the main seat rather than replaced with a nearby model.

Every recon brief is self-contained and bounded: the question, where to look, and a return contract — the direct answer, the minimal evidence that supports it with the addresses a reader can check, anomalies, and whether coverage was incomplete. The raw material stays in the subagent's context, which is the whole point of sending it there.

Recon and interview run at the same time. The Skill asks the part of the frontier that does not depend on a running recon and holds only the questions that do, so a slow sweep never blocks the interview.

## The Frame Record

One Markdown file, written incrementally — after every round and after every recon report — so an interrupted session costs the last round and nothing more. Its sections are the contract `/to-slices` reads:

1. **Task** — in the owner's words, with the commit the framing was made against.
2. **Frames** — what binds, each with the address it was read from.
3. **Findings** — what the codebase answered, each with the address of its evidence.
4. **Decided by the owner** — every question and its answer, verbatim.
5. **Decision ledger** — every decision the Skill took in his stead: the choice, the alternative, the reason, the frame it was decided under. Numbered, so a veto names one.
6. **Open** — what is deliberately unanswered, who owns it, and what would answer it.
7. **Knowledge written** — the glossary terms and records this framing added, with their addresses.

A record whose section 6 is empty and whose section 4 has no entries is the degenerate case the dossier asks for: a simple task, nothing to ask, and the record written and handed over without a single round.

## Knowledge written as it crystallises

A term that gets pinned down is written into the glossary as it is pinned down, and a decision that meets all three criteria at once — hard to reverse, surprising without its context, the result of a real trade-off — earns a record. Under the target repository's own convention where it declares one; under the single-context default, `CONTEXT.md` plus `docs/adr/`, where it does not. A decision failing any of the three is a ledger entry and nothing more. This is the discipline `docs/rules/docs.md` already states for this repository, carried into a Skill that runs in any repository.

## What it ships

`skills/code/frame/`, with no engine of its own — nothing here is deterministic enough to be worth a script, and the pipeline's stated goal is no script runtime at all.

- `SKILL.md` — frontmatter plus a body that starts at its first step. `disable-model-invocation: true`; `argument-hint: '[--resume=<path>] [<task>] [-- <instruction>]'`; `kntnt.binaries: "uv"`, `kntnt.skills: "model-selector"`, `kntnt.capabilities: "subagents"`.
- `help.md` — the manpage, in the profile `docs/rules/skills.md` fixes.
- `agents/openai.yaml` — the Codex sidecar, mirroring the invocation policy.
- `references/recon.md` — the recon subagent's brief, filled in per question.
- `references/knowledge.md` — where a term and a record go, and the three criteria that gate one.

And two files in the Collection Library, because they have more than one consumer by construction:

- `library/references/tldr-mode.md` — the owner-facing register, **moved** from `skills/agents/tldr/references/mode.md`.
- `library/references/frame-record.md` — the Frame Record format, written by `/frame` and read by `/to-slices`.

## The invocation

`/frame [--resume=<path>] [<task>]`, and nothing else.

The operand is free text: the task, in whatever words he has. Bare, the task is taken from the conversation already had, which is the ordinary way this Skill starts — a discussion that has reached the point of *now let us actually do this*. Where the operand names a tracker issue and `gh` is on the machine, recon fetches it like any other fact; that is a recon route rather than a second grammar, and it is not a declared dependency.

`--resume=<path>` continues an unfinished record. It is a flag rather than an offer on the bare form deliberately: **`/frame` takes no `--yes` and has no unattended form at all.** Its questions are not yes/no questions, so the collection's `--yes` — every question that could be answered yes is answered yes — has nothing to answer here, and a flag with no work to do is refused rather than accepted. A framing with no human in it is not a cheaper framing; it is `/to-slices` reading a record nobody's judgement is in.

## The handoff, and the order things land in

The Skill ends in the register of `$LIBRARY/references/tldr-mode.md`: what it mapped, what he decided, what it decided, what is still open, and where the record is. `/to-slices` does not exist on the day `/frame` lands, so the first version ends by naming the record and what it is for; the ticket that builds `/to-slices` adds the prefilled next line, and its `SEE ALSO` entry with it. That is the dossier's own sequencing — `/frame` alone replaces the grill-with-docs pain the day it ships, and it is worth nothing less for having no successor yet.

## Boundaries judged rather than followed

**The dossier's file references for the mode documents contradict a rule phase 1 landed.** `00-brief.md` has all five Skills read `skills/agents/tldr/references/mode.md`, and `/dispatch` read `skills/agents/delegation/references/mode.md`. `docs/rules/skills.md` now says peer internals are not an interface: a Skill never reads another Skill's `references/`. The rule that resolves it is in the same module — a reference with several consumers belongs in the Collection Library — so the TL;DR mode moves to `library/references/tldr-mode.md` and `tldr` reads it there like everybody else. The delegation mode moves the same way, on the same reasoning, in the mini-cycle that needs it; doing it now would be churn against a design not yet written.

**The Frame Record format starts in the Library rather than moving there later.** By the letter of *ownership follows consumers* it has one consumer today. Its second consumer is named in the dossier, and the concern the rule protects against — one Skill owning another's input contract — is exactly what would happen if `/frame` held the format `/to-slices` must read.

**`subagents` and `model-selector` are declared as hard Dependencies.** Both bars are *cannot work without*, and a `/frame` with no subagents could technically read files on the main seat. It would be a different Skill: recon in the main context is recon competing with the interview for the context the interview exists to protect, and the promise never to ask what the codebase can answer degrades into asking because reading got expensive. `orchestrate` sets the precedent for both declarations.

**`git` is declared nowhere.** Recon reads history where there is history to read, and a repository without it loses one class of finding rather than the Skill.

**No rules module, and no `AGENTS.md` pointer, in this mini-cycle.** `docs/rules/docs.md` puts a rule governing one Skill's own behaviour in that Skill's own shipped documents. Nothing `/frame` establishes binds anybody else yet. When `/compile` needs the pipeline's shared conventions written down for more than one Skill, that is when the module is earned.

## What this Skill deliberately does not do

It does not slice, size, or sequence anything — that is `/to-slices`, and a framing that has already decided the tickets has stopped listening. It does not write code, and it does not build to find out. It publishes nothing to the tracker. It does not decide the seams the tests will be written at; recon may report the seams that exist, which is a finding and not a decision.

## Residuals for the owner

Five, all of them consequences he lives with rather than mechanics. Each carries the recommendation this design would take if it heard nothing back.

**R1 — Where a framing lives.** A Frame Record can be a committed repository artifact (a reviewer sees the reasoning behind the tickets), an untracked local file in the working tree (survives a lost session, resumable, invisible to everyone else), or session scratch (disposable, and gone with the session). *Recommended: untracked, at `.kntnt/frames/<slug>.md`.* It survives the session that made it, `--resume` can find it, and it does not become a second durable layer competing with the decision document `/to-slices` publishes — which is the layer meant to be read later, and the one kept from rotting.

**R2 — A question only an experiment can answer.** Some open points are not in any of the three bins: nobody knows until something is built. `/frame` can stop and build a throwaway prototype to answer one, or record it as open and let `/to-slices` sequence it as a spike of its own. *Recommended: record it as open.* It keeps framing cheap and bounded, and a spike that earns its own slice is visible work rather than a detour inside a conversation.

**R3 — Whether `/frame` ever runs without him.** As designed it does not: no `--yes`, no unattended form, and a task with nothing to ask passes through without asking anyway. *Recommended: keep it that way.* The alternative is a flag that takes every recommendation on his behalf, which produces a record whose owner decisions were made by the thing that wanted them answered.

**R4 — When the decision ledger is shown.** Either with each round's questions, so he vetoes as decisions are taken, or once at the end with the report. *Recommended: with each round.* A ledger decision that goes unvetoed for three rounds has had three rounds of decisions built on top of it, and reversing it then costs the whole branch rather than one entry.

**R5 — Whether records and glossary terms are written during framing.** The dossier says knowledge is written as it crystallises, which means his repository gains files during a design conversation, before a line of the work exists. The alternative is to propose them in the record and let `/land` write them once the work has landed. *Recommended: write them during framing.* The decision is made at the moment it is made, and a record written later is written by whoever survived the intervening context; what `/land` harvests is what implementation discovered, which is a different set.

## The slices, provisionally

Three tickets, pending the round above. Sized for one fresh context window each, and none of them a Solo Ticket — nothing here rewrites a rule every shipped file is under.

**S1 — The TL;DR mode moves into the Collection Library.** `library/references/tldr-mode.md` becomes the single copy; `tldr`'s `SKILL.md`, its `persist.md`, and its help pages point there; the suite and the Catalog follow. *Blocked by: nothing.* Delivers: a register any Skill may adopt without reading a peer's internals.

**S2 — The Frame Record format in the Library.** `library/references/frame-record.md`: the seven sections, what each is for, and what a consumer may rely on. *Blocked by: nothing.* Delivers: the input contract `/to-slices` will be written against, before either end of it exists.

**S3 — `/frame` itself.** The Skill directory, its two local references, the README section, the regenerated Catalog, and a green suite. *Blocked by: S1, S2.* Delivers: a task framed, a record written, and the questions the owner was actually asked being the ones only he could answer.
