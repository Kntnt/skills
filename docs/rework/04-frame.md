# Phase 2, step 1 — `/frame`, as designed

> Draft written 2026-08-25 against commit `de06983`, from the `/frame` section of `00-brief.md` and from what this codebase answers. It was the input to the owner-level round (step 2), which ran on 2026-08-26 and settled every residual; it is now the input to the ticket breakdown. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

The dossier states what `/frame` is for; this file is the design that satisfies it, the boundaries judged along the way, and what the owner settled. Everything here is settled — resolved from `docs/rules/`, from the Skills this one borrows from, and from what the collection already ships, or answered by Thomas in the round recorded below. Nothing in it is still a question.

## What the Skill is

`/frame` maps a task before anything is built. It runs codebase recon in parallel with an interview and routes every open point into one of three bins: the codebase answers it, the frames answer it, or the owner answers it. Only the third bin becomes a question. What comes out is a Frame Record — the task, what binds, what the codebase said, what the owner decided, what the Skill decided in his stead, and what is deliberately still open — which is the input `/to-slices` synthesizes into the decision document and the tickets.

## The three bins, and the rule that separates them

**The codebase answers it.** What exists, how it is done here, what a term means, what the tests already cover, what the history says a thing was for. A recon subagent fetches it. It is never a question, and a question the Skill asked that a file could have answered is a defect of this Skill rather than an economy.

**The frames answer it.** A choice with one right answer inside the constraints already established: naming inside a convention the repository keeps, placement inside a structure it already has, a library already in its dependency set, the shape of an error beside its siblings. The Skill decides, and writes the choice, the alternative it passed over, and the frame it decided under into the decision ledger.

**Only the owner answers it.** Product behaviour, user experience, priority, architecture direction, and any trade-off carrying a cost, risk, or reversibility consequence he would want to weigh. Asked in frontier rounds, each question numbered, phrased as the consequence he is choosing between rather than the mechanism that delivers it, with a recommended answer and what that answer costs. The vocabulary is the repository's own — `CONTEXT.md` where it has one, established terms otherwise, and nothing invented for the occasion.

**The tie-break is reversibility.** A point that could sit in either of the last two bins goes to the owner when the decision is hard to reverse or would surprise him later, and to the ledger otherwise. The ledger is what makes that safe: a decision he would have made differently is one he vetoes, and a veto turns it back into a question.

**The ledger is shown as it grows.** Every round carries, beside its questions, the entries taken since the last round — one line each, the choice and the frame it was decided under, the full reasoning staying in the record. That keeps the veto window open where it is cheap: an entry standing unvetoed for three rounds has had three rounds of decisions built on top of it, and reversing it then costs the branch rather than the entry. A round where nothing was decided in his stead adds nothing to read.

## The frames themselves

Before any question, the Skill establishes what binds. It reads the repository's always-loaded file — `AGENTS.md`, `CLAUDE.md`, whichever it keeps — follows the pointers to the rule modules the task actually touches, reads the glossary for vocabulary, and finds how the repository verifies itself. That set is the Frames section of the record: the standing constraints every later decision is checked against, and the reason a ledger decision can be taken without asking. This is where phase 1 pays for itself — the frames are one short read here rather than a derivation across eighty records.

## Recon

Recon is delegated, and delegation here follows the collection's own rule rather than a private arrangement: the Skill routes through model-selector's public `route` Interface and reads none of its private references (`docs/rules/collection.md`, *Routing and evidence*). One route request covers a recon wave as an ordered batch, because every recon brief in a wave is the same execution class — read-only, reversible, no consequence of its own, heavy on context and tools, and checked by the main agent, which reads the answer and can spot-check the evidence addresses it carries. A selected decision launches its subagents with exactly the controls it names; a reported inheritance launches them on the exact main seat; a refusal means that recon is done on the main seat rather than replaced with a nearby model.

Every recon brief is self-contained and bounded: the question, where to look, and a return contract — the direct answer, the minimal evidence that supports it with the addresses a reader can check, anomalies, and whether coverage was incomplete. The raw material stays in the subagent's context, which is the whole point of sending it there.

Recon and interview run at the same time. The Skill asks the part of the frontier that does not depend on a running recon and holds only the questions that do, so a slow sweep never blocks the interview.

## The Frame Record

One Markdown file at `.kntnt/frames/<slug>.md` in the target repository, untracked, written incrementally — after every round and after every recon report — so an interrupted session costs the last round and nothing more. Its sections are the contract `/to-slices` reads:

1. **Task** — in the owner's words, with the commit the framing was made against.
2. **Frames** — what binds, each with the address it was read from.
3. **Findings** — what the codebase answered, each with the address of its evidence.
4. **Decided by the owner** — every question and its answer, verbatim.
5. **Decision ledger** — every decision the Skill took in his stead: the choice, the alternative, the reason, the frame it was decided under. Numbered, so a veto names one.
6. **Open** — what is deliberately unanswered, who owns it, and what would answer it.
7. **Knowledge written** — the glossary terms and records this framing added, with their addresses. It is also a manifest, and the only one: the sole list a discarded framing's knowledge can be withdrawn from entry by entry, and the sole list `/land` can check that knowledge against.

A record whose section 6 is empty and whose section 4 has no entries is the degenerate case the dossier asks for: a simple task, nothing to ask, and the record written and handed over without a single round.

### Where it lives, and how long it lives

**Untracked, and ignored locally.** The record survives the session that made it and `--resume` finds it, while never becoming a second durable layer competing with the decision document `/to-slices` publishes — which is the layer meant to be read later, and the one kept from rotting. The silence in `git status` is bought without writing a tracked file: `/frame` appends `.kntnt/` to `.git/info/exclude`, and only where `.kntnt/` is not already ignored by some means. A local artifact gets a local ignore, and that an exclude does not survive a clone costs nothing, because the record does not survive one either. The report names the line on the run that wrote it and says nothing on the runs that did not.

**A record is a baton, not an archive.** `/to-slices` deletes the record it consumed, once the decision document and the tickets are published: everything durable has by then moved into layers built to be read later, and a record kept past that moment is a stale second account of decisions the tracker now holds. The principle is settled here; the mechanism belongs to `/to-slices`' own mini-cycle, and that brief inherits this requirement.

**A framing nobody consumed is met with visibility, not a sweep.** `/frame` reads `.kntnt/frames/` to resolve `--resume` in any case, so it reports at start every record still lying there unconsumed and asks, for each, whether to resume it or discard it. Discarding also offers the removal of what that record's section 7 lists, entry by entry — the one moment a framing's knowledge can be withdrawn against a manifest instead of guessed at.

## Knowledge written as it crystallises

A term that gets pinned down is written into the glossary as it is pinned down, and a decision that meets all three criteria at once — hard to reverse, surprising without its context, the result of a real trade-off — earns a record. Under the target repository's own convention where it declares one; under the single-context default, `CONTEXT.md` plus `docs/adr/`, where it does not. A decision failing any of the three is a ledger entry and nothing more. This is the discipline `docs/rules/docs.md` already states for this repository, carried into a Skill that runs in any repository.

**Nothing here carries a sweeping cleanup duty, and none is added anywhere else either.** Knowledge a framing wrote that the work later contradicted, or that the work never reached, is not hunted for: with no manifest the task is unbounded, and a search that has to guess deletes legitimate records — a decision that passed the three-criteria gate can stand on its own merit even where the work was never built. Two bounded duties take its place, each performed with the manifest in hand:

- **`/frame`, at discard.** A record thrown away at the start's *resume or discard* takes its section 7 with it as an offer, entry by entry.
- **`/land`, at landing.** The knowledge a framing wrote — reached through the decision document, which is what names it — is checked against what the implementation actually did, and corrected or replaced where the two diverge. The mechanism belongs to `/land`'s own mini-cycle, and that brief inherits this requirement as `/to-slices`' inherits delete-on-consumption.

## What it ships

`skills/code/frame/`, with no engine of its own — nothing here is deterministic enough to be worth a script, and the pipeline's stated goal is no script runtime at all.

- `SKILL.md` — frontmatter plus a body that starts at its first step. `disable-model-invocation: true`; `argument-hint: '[--resume=<path>] [<task>] [-- <instruction>]'`; `kntnt.binaries: "uv"`, `kntnt.skills: "model-selector"`, `kntnt.capabilities: "subagents"`.
- `help.md` — the manpage, in the profile `docs/rules/skills.md` fixes.
- `agents/openai.yaml` — the Codex sidecar, mirroring the invocation policy.
- `references/recon.md` — the recon subagent's brief, filled in per question.
- `references/knowledge.md` — where a term and a record go, the three criteria that gate one, and how a discarded framing's entries are offered back for removal against section 7.

And two files in the Collection Library, because they have more than one consumer by construction:

- `library/references/tldr-mode.md` — the owner-facing register, **moved** from `skills/agents/tldr/references/mode.md`.
- `library/references/frame-record.md` — the Frame Record format and its lifecycle: written by `/frame`, read by `/to-slices`, and deleted by it on consumption.

## The invocation

`/frame [--resume=<path>] [<task>]`, and nothing else.

The operand is free text: the task, in whatever words he has. Bare, the task is taken from the conversation already had, which is the ordinary way this Skill starts — a discussion that has reached the point of *now let us actually do this*. Where the operand names a tracker issue and `gh` is on the machine, recon fetches it like any other fact; that is a recon route rather than a second grammar, and it is not a declared dependency.

`--resume=<path>` names an unfinished record to continue. The bare form reaches the same place without a path, since the start reports what `.kntnt/frames/` still holds and asks what to do with each; the flag is the direct address rather than the only route.

**`/frame` has no unattended form.** That is an owner decision rather than a property of its grammar: a framing with no human in it is not a cheaper framing, it is `/to-slices` reading a record nobody's judgement is in, and a record whose owner decisions were made by the thing that wanted them answered carries his name on judgement that is not his. Where an unattended framing is ever wanted, that is its own decision at that time. The graceful degradation the dossier asks for is untouched — a task with nothing to ask passes through without asking.

## The handoff, and the order things land in

The Skill ends in the register of `$LIBRARY/references/tldr-mode.md`: what it mapped, what he decided, what it decided, what is still open, and where the record is. `/to-slices` does not exist on the day `/frame` lands, so the first version ends by naming the record and what it is for; the ticket that builds `/to-slices` adds the prefilled next line, and its `SEE ALSO` entry with it. That is the dossier's own sequencing — `/frame` alone replaces the grill-with-docs pain the day it ships, and it is worth nothing less for having no successor yet.

One consequence of that order is worth naming: until `/to-slices` exists, nothing consumes a record, so every framing stays in `.kntnt/frames/` and the start-of-run *resume or discard* is the only thing that clears it. That is the interim state working as intended rather than a defect — the sweep exists precisely because a record can outlive its purpose — and it ends when `/to-slices` lands.

## Boundaries judged rather than followed

**The dossier's file references for the mode documents contradict a rule phase 1 landed.** `00-brief.md` has all five Skills read `skills/agents/tldr/references/mode.md`, and `/dispatch` read `skills/agents/delegation/references/mode.md`. `docs/rules/skills.md` now says peer internals are not an interface: a Skill never reads another Skill's `references/`. The rule that resolves it is in the same module — a reference with several consumers belongs in the Collection Library — so the TL;DR mode moves to `library/references/tldr-mode.md` and `tldr` reads it there like everybody else. The delegation mode moves the same way, on the same reasoning, in the mini-cycle that needs it; doing it now would be churn against a design not yet written.

**The Frame Record format starts in the Library rather than moving there later.** By the letter of *ownership follows consumers* it has one consumer today. Its second consumer is named in the dossier, and the concern the rule protects against — one Skill owning another's input contract — is exactly what would happen if `/frame` held the format `/to-slices` must read.

**`subagents` and `model-selector` are declared as hard Dependencies.** Both bars are *cannot work without*, and a `/frame` with no subagents could technically read files on the main seat. It would be a different Skill: recon in the main context is recon competing with the interview for the context the interview exists to protect, and the promise never to ask what the codebase can answer degrades into asking because reading got expensive. `orchestrate` sets the precedent for both declarations.

**`git` is declared nowhere.** Recon reads history where there is history to read, and a repository without it loses one class of finding rather than the Skill.

**A rule the rule layer stated only half of, now stated whole.** This design was written believing `/frame` had to argue `--yes` away rather than simply not write it, and the documents allowed the misreading: `docs/rules/collection.md` fixes what the flag *means* across the collection, `skills.md` and the Library's `invocation-envelope.md` both state that a flag with no work to do is refused rather than ignored — but nothing said that a Skill's grammar names a flag exactly where that flag has a function, and that there is no collection-wide flag set every Skill is expected to offer. That line now sits in `docs/rules/skills.md` under *The collection's flag grammar*, cited to ADR-0108, whose body already carried the reasoning: *a flag is allowed where it has a function on this run, not where it has one somewhere in the Skill*. The context line pointing the other way is ADR-0029's title quoted in ADR-0108's fold list; the deleted record really was titled that, and its own body had already withdrawn the *every verb* half. The archive stands as history and the rule line is the authority.

**No rules module, and no `AGENTS.md` pointer, in this mini-cycle.** `docs/rules/docs.md` puts a rule governing one Skill's own behaviour in that Skill's own shipped documents. Nothing `/frame` establishes binds anybody else yet. When `/compile` needs the pipeline's shared conventions written down for more than one Skill, that is when the module is earned.

## What this Skill deliberately does not do

It does not slice, size, or sequence anything — that is `/to-slices`, and a framing that has already decided the tickets has stopped listening. It does not write code, and it does not build to find out. It publishes nothing to the tracker. It does not decide the seams the tests will be written at; recon may report the seams that exist, which is a finding and not a decision.

## Settled by the owner

The five points this design could not settle were put to Thomas on 2026-08-26 and answered in one round. They are recorded here as decisions, not as open questions; the frontier is empty.

**O1 — A framing lives untracked, and is ignored locally.** `.kntnt/frames/<slug>.md`, with `.kntnt/` appended to `.git/info/exclude` rather than to `.gitignore`. The recommendation had `/frame` write one line into a tracked file once per repository; the exclude buys the same silence in `git status` while `/frame` keeps its own promise to touch nothing tracked, and a local artifact gets a local ignore. That an exclude does not survive a clone is not a cost, because neither does the record. Written only where `.kntnt/` is not already ignored, and named in the report on the run that wrote it. With it came the lifecycle the recommendation did not have: the record is a baton, deleted by `/to-slices` on consumption, and an unconsumed one is met at start with *resume or discard* rather than accumulating.

**O2 — A question only an experiment can answer is recorded as open.** With what would answer it, for `/to-slices` to sequence as a spike slice of its own. `/frame` does not stop to build.

**O3 — `/frame` has no unattended form.** The question as asked was malformed and is withdrawn: it treated `--yes` as a collection-wide flag every Skill must either carry or refuse, when a flag's *meaning* is uniform across the Skills that carry it and its *presence* follows its function. `/frame` asks no yes/no question, so `--yes` is simply not in its grammar and needs no argument against it — the strict grammar refuses every undeclared flag alike. What stands as a decision is the substance: no auto-accept flag, no unattended mode, because a record whose owner decisions were made by the thing that wanted them answered carries his name on judgement that is not his. Should an unattended framing ever be wanted, that is its own decision then. The rule-layer gap the malformed question exposed is closed under *Boundaries judged rather than followed*.

**O4 — The ledger is shown per round, as a delta.** Only the entries taken since the last round, one line each — the choice and the frame it was decided under — with the full reasoning in the record.

**O5 — Knowledge is written during framing.** And no sweeping cleanup duty is created anywhere to compensate: instead the two bounded duties under *Knowledge written as it crystallises* — `/frame` offering removal against section 7 at discard, `/land` reconciling the framing's knowledge against what implementation actually did.

## The slices

Three tickets, the owner round having settled everything they rest on. Sized for one fresh context window each, and none of them a Solo Ticket — nothing here rewrites a rule every shipped file is under.

**S1 — The TL;DR mode moves into the Collection Library.** `library/references/tldr-mode.md` becomes the single copy, and `tldr`'s `SKILL.md` and its `persist.md` point there — its help pages describe the mode without naming the file, so nothing in them changes. The suite's assertion on the persist template becomes per-Skill, `delegation` keeping its own local mode until the mini-cycle that moves it, and the Catalog follows. *Blocked by: nothing.* Delivers: a register any Skill may adopt without reading a peer's internals.

**S2 — The Frame Record format in the Library.** `library/references/frame-record.md`: the seven sections, what each is for, what a consumer may rely on, and the record's lifecycle — a baton its consumer deletes, section 7 doubling as the manifest that `/frame` withdraws knowledge against and `/land` checks it against. *Blocked by: nothing.* Delivers: the input contract `/to-slices` will be written against, before either end of it exists.

**S3 — `/frame` itself.** The Skill directory, its two local references, the README section, the regenerated Catalog, and a green suite. Carries what the owner round added: the `.git/info/exclude` line written once and only where needed, the start-of-run report of unconsumed records with *resume or discard* and the section-7 removal offer on a discard, and the per-round ledger delta. *Blocked by: S1, S2.* Delivers: a task framed, a record written, and the questions the owner was actually asked being the ones only he could answer.

The rule-layer line the round produced — flag presence follows function, in `docs/rules/skills.md` — is not a slice: it was written during the round itself, against ADR-0108, and it brought the tree into agreement with itself in the same commit. One shipped file changed with it — `ready-for-agent-check`'s `SKILL.md` argued the absence of `--yes` rather than simply not writing it, the single such case in the tree — together with the assertion that had pinned that sentence, the suite having enforced the very shape the new rule forbids. No other Skill's files were touched.

**Three requirements land outside this mini-cycle and are recorded here so the briefs that own them inherit them.** `/to-slices` deletes the Frame Record it consumed, once the decision document and the tickets are published. `/to-slices` also sequences a question only an experiment can answer — carried in the record's section 6 with what would answer it — as a spike slice of its own. `/land` checks the knowledge a framing wrote — reached through the decision document — against what the implementation actually did, and corrects or replaces it where the two diverge.
