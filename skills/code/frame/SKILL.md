---
name: frame
description: Map a task before anything is built. Codebase recon runs beside an interview, the questions put to the owner are the ones neither the code nor the repository's own rules could answer, and what comes out is a Frame Record the next Skill builds from.
disable-model-invocation: true
argument-hint: '[<task>] | --resume=<path> [-- <instruction>]'
compatibility: Requires uv and the model-selector Skill, plus a harness that can run subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: "model-selector"
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# frame

Map a task before anything is built, and write what you mapped into a Frame Record. Every open point belongs to one of three parties, and only the third is a question: the codebase answers it, the frames answer it, or the owner answers it. Asking the owner what a file could have answered is this Skill's own defect rather than an economy.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, frame nothing, install nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

`/frame [<task>]` or `/frame --resume=<path>`, and nothing else. The two forms are exclusive, and the order is part of each: an operand written before a flag is refused, not repaired.

- `<task>` — the task in the owner's own words, free text. Everything from the first operand onwards is operand, so a word inside the task that looks like a flag is part of the task. Given none, the task is the one the conversation has already reached, which is the ordinary way this Skill starts; where the conversation holds no task either, ask for one before anything else.
- `--resume=<path>` — the Frame Record to continue. It is the direct address of a record; step 2 reaches the same place without it.

Invalid forms, each refused the same way:

- `--resume=<path>` given together with a `<task>` operand. A record carries the task it was opened with, in the owner's own words, and a second task on the same invocation is two framings with nothing to say which was meant.
- A `--`-prefixed token that is not `--resume=<path>`.

Refuse an invalid form as `$LIBRARY/references/invocation-envelope.md` says, then frame nothing and stop.

## The three bins, and the rule that separates them

Every open point the task carries goes into one of these. Sorting is the whole method, so sort each point explicitly rather than by feel.

**The codebase answers it.** What exists, how it is done here, what a term means, what the tests already cover, what the history says a thing was for. A recon subagent fetches it. It is never a question.

**The frames answer it.** A choice with one right answer inside the constraints already established: naming inside a convention the repository keeps, placement inside a structure it already has, a library already in its dependency set, the shape of an error beside its siblings. You decide it, and the ledger takes the choice, the alternative you passed over, the reason, and the frame you decided under.

**Only the owner answers it.** Product behaviour, user experience, priority, architecture direction, and any trade-off carrying a cost, a risk, or a reversibility consequence they would want to weigh.

**The tie-break is reversibility.** A point that could sit in either of the last two bins goes to the owner where the decision is hard to reverse or would surprise them later, and to the ledger otherwise. What makes that safe is the ledger being shown as it grows: a decision they would have made differently is one they veto while reversing it still costs one entry.

## The record

`$LIBRARY/references/frame-record.md` fixes the format: the seven sections, what each holds, what a consumer may rely on from it, and where the file lives. Read it before writing into a record, and write incrementally — after every round and after every recon report — so an interrupted session costs the last round and nothing more.

## What framing is not

It does not slice, size, or sequence the work; that belongs to the Skill that reads the record, and a framing that has already decided the tickets has stopped listening. It writes no code and builds nothing to find out: a question only an experiment can answer is section 6's, with what would answer it, for the next Skill to sequence as work of its own. It publishes nothing to the tracker. It decides no seam for tests — that a seam exists is a finding, and choosing one is not.

Every framing is attended. A task with nothing to ask produces a complete record without a single round, which is this Skill meeting a simple task rather than skipping the owner.

## Steps

1. Parse the arguments by the rules above. An invalid form is refused as `$LIBRARY/references/invocation-envelope.md` says; frame nothing and stop. Done when the form is settled, or you have stopped.
2. Read `.kntnt/frames/` in the repository being framed and settle which record this run writes. Every record there is unconsumed, nothing consuming one yet, so report each of them: its task, the commit it was framed against, and how far it got. Ask of each whether to resume it or discard it; `--resume=<path>` is that answer already given for one, and a path that is no readable Frame Record is said as such and nothing is framed. Discarding a record: follow [`knowledge.md`](references/knowledge.md) for the withdrawal it offers, then delete the record. A resumed record is continued from where its sections stand, with the frames re-read against the tree as it is now: where the tree has moved since the commit section 1 names, write the commit this run continues against beside it and re-check every finding whose address that move touched — `git diff --name-only <commit>..HEAD` says which — because a consumer reads every finding as of the commit the record names. Done when this run holds one record — a resumed one, or the path `.kntnt/frames/<slug>.md` a new one will be opened at — and every other record has been resumed, discarded, or left where it lies at the owner's word.
3. Make the directory silent, once and only where it is needed. `git check-ignore -q .kntnt/` answers whether it is already ignored by some means; where it is, write nothing and say nothing about it. Where it is not, append `.kntnt/` to `.git/info/exclude` and name that line in the closing report of this run alone. The ignore is local because the record is: no tracked file is touched by it. Outside a repository there is nothing to ignore and nothing to say. Done when the directory is ignored, or there was nothing to do.
4. Open the record and establish what binds, before a single question. A new record is opened with all seven headings the format fixes and section 1 written: the task in the owner's own words, and the commit this framing is made against. Then read the repository's always-loaded agent file — `AGENTS.md`, `CLAUDE.md`, whichever it keeps — follow its pointers to the rule modules this task actually touches, read the glossary it keeps, and find how it verifies itself. Write that set into section 2, each frame stated closely enough to apply and carrying the address it was read from. This is what lets a decision be taken in the owner's stead, and the glossary is the vocabulary every question is phrased in: a question in words the repository does not use is a question about your vocabulary. Done when the record exists with its seven headings, and section 2 holds the standing constraints every later decision will be checked against.
5. Sort the frontier and write the recon briefs. Take every open point the task carries, sort it by the rule above, and fill in [`recon.md`](references/recon.md) once per point the codebase answers — the question, where to look, and the return contract. A wave is the briefs that can be asked now; a point a running brief may settle waits for its answer rather than becoming a brief of its own. Done when every open point sits in a bin and every brief of the first wave is written.
6. Route the wave and launch it. Write one route request into your own scratch, holding the wave as an ordered batch. The envelope's `schema_version` is the integer `1` and its `requests` array holds one entry per brief, in the order you want them; each entry carries `request_id` — `recon-<n>`, which is the name its decision comes back under — `authority` of `execution`, a `stage` naming this as recon, the filled-in brief as its `workload`, `workload_tags` describing that class of work, `reversible` true, `checker` of `{"kind": "external", "signal": ...}` naming this session reading the answer and opening the evidence addresses it carries, and an empty `overrides`, this Skill locking neither model nor deliberation. The envelope needs nothing else on a first wave: the Interface assembles the current profile, Harness, and main-seat facts itself. The whole wave is one execution class — read-only, reversible, no consequence of its own, heavy on context and tools, and checked by you when the answer comes back — which is why it is one request. Ask for no verdict; a verdict is not this Skill's to route. Invoke `/model-selector route <path>` with that path as the whole of its Formal Invocation, and a Contextual Instruction after an explicit `--` only where the outer instruction holds guidance relevant to routing; `/model-selector route --help` is where that artifact's contract is published. Read none of that Skill's references, run none of its scripts, and recreate none of its selection rules. Keep the `snapshot` the response returns and copy it unchanged into the envelope of every later wave, so the whole framing is routed from one frozen account rather than from whatever the profile says an hour later. A refusal of the artifact itself rather than of a request is the contract having moved under this Skill: report it and route no wave, instead of guessing at fields. Then, per decision: `selected` launches its subagent with exactly the Harness-native controls it names; `inherit` launches on the exact main seat with no override, and the report says optimisation was unavailable; `refused` launches nothing, and that recon is yours to do on the main seat, at the cost in context the report also names. Never put a nearby model in the place of a refusal. Done when every brief of the wave is running or is yours.
7. Interview in frontier rounds while recon runs. This step and the two after it run together rather than in turn: a round, a report arriving mid-round, and the knowledge either of them crystallises interleave, and the record takes each as it lands. Ask the part of the frontier that does not depend on a running brief and hold the rest, so a slow sweep never blocks the round. Each round carries numbered questions, each phrased as the consequence being chosen between rather than the mechanism that delivers it, each with a recommended answer and what that answer costs, in the repository's own words. Beside them goes the ledger delta: the entries taken since the last round, one line each — the choice and the frame it was decided under — with the full reasoning staying in section 5. A veto turns that entry back into a question in the next round; the entry keeps its number and says it was vetoed, and the answer that replaces it is section 4's. Write every question and answer into section 4 verbatim, the answer being the owner's judgement and a paraphrase being yours in their name. Done when the frontier is empty: every point answered, decided, or deliberately open.
8. Fold each recon report into the record as it arrives. The direct answer goes into section 3 with the address of its evidence, an anomaly is a finding of its own, and coverage the brief could not complete says so. Open an address rather than trusting the paraphrase beside it where a decision is about to rest on it. A finding that opens a new point is sorted into the bins like any other, and the briefs it produces are routed and launched as step 6 routes the first wave. Done when every brief has reported and its answer stands in section 3.
9. Write knowledge as it crystallises, following [`knowledge.md`](references/knowledge.md): a term as it is pinned down, a record where the decision meets all three criteria at once. Everything written goes into section 7 with its address, which is the only manifest anybody can withdraw it against later. Done when section 7 lists everything durable this framing wrote outside the record.
10. Close in the register of `$LIBRARY/references/tldr-mode.md`: what you mapped, what the owner decided, what you decided in their stead, what is still open, and where the record is. Say what the record is for and that nothing consumes it yet, so it stays until a later run's step 2 offers it back. Name the ignore line only where this run wrote it. Done when the owner has that report and the record on disk holds all seven sections.
