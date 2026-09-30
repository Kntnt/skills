# Plan for #471: a brief is a direction, and follows the template of twelve questions

Frozen on 2026-09-30, before the first run. Nothing in this file, in the two judge briefs beside it or in `inputs/` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) first; this file says what it leaves to a ticket.

**`<start>` is `62ff4597`**, the head of the branch `kntnt-orchestrate/main/471` when the build began. **The candidate is the commit that adds this file.** It holds the rewritten `writing-brief.md`, Brief's `SKILL.md` and `help.md`, the count-free surfaces (`README.md`, `CONTEXT.md`, `docs/rules/skills.md`, the editorial README, Redline's `brief-review.md` and `help.md`), their tests, the regenerated catalog, and the runner's extension described below. Every run is staged from it.

The requirement is the ticket's thread as it stood on 2026-09-30: the body and readiness addenda 1, 2 and 3. Where they conflict, the later one stands.

## What this evaluation is

The template and the Skill's new spirit are Thomas's ruling and ship whatever the measurement shows, as the protocol's *Not reproduced* says. There is **no pre-change arm**, as readiness addendum 1 says. The measurement decides what is written down as met or missed and what is filed. No decision record is written for the evaluation.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. No Codex Harness and no GPT model is started, controlled or invoked.

Every run is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from the root of this working tree. The candidate extends it in three ways, each covered by `tests/test_evaluation_harness.py`: `--extra-skill=brief` stages `skills/editorial/brief` beside the four editorial Skills and the Manager; `--input` may be left out, so an interview starts with an empty working directory; and `--turns=<file>`, a JSON array, continues one session turn by turn with `claude --print --resume <session-id>`, each turn sent once the one before it has ended, all of them in the one private root, with one before-and-after inventory for the whole session and every turn's stream and reply kept.

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<candidate> --corpus-revision=<candidate> \
  --invocation='<invocation>' \
  [--input=<input> --input-name=<name>] [--turns=<turns>] \
  --extra-skill=brief \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  --capture-output-name=<delivered>
```

- **`<candidate>`** is the commit that adds this file.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/471.scratch`, this build's scratch directory. Packets are written there and copied into `runs/<run>/` here only after they are judged.
- **The seat.** `claude-opus-5-5` at high deliberation for every run, every nested agent inside a run, and every judge. The runs request it in `run.json` and record it in `trace-index.json`. Each judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **Lanes.** The five Brief runs run side by side, one lane each. The three Write runs follow, side by side, each once the Brief run whose brief it takes is judged-ready, that is, has delivered `brief.md`.

## The inputs

All are synthetic. *Stigvikens Cykelkök*, *Alder Tool Library*, *Norrmyra bibliotek*, *Hollin Seed Circle*, *Brackwater Bakery*, *Tallow Ovens* and every person named are invented for this evaluation and tied to no real organisation or customer; the address is under `example.se` and the telephone number is a placeholder. Every answer the simulated user gives is frozen here, in `inputs/`, before the first run.

| Input | What it is |
| --- | --- |
| `interview-sv.turns.json` | Thirteen Swedish turns answering an interview for an article, one answer a turn in template order. The angle is first given as several angles and then narrowed to one; the conclusion is first given as a topic and then as a claim; the technique is ABT, chosen explicitly, and the user asks for help with the sketch; RIV and the chain check are left for the Skill to propose and then confirmed; no sources are known, and two things to find out are named. Each turn after a point the Skill may have commented on also carries the next answer, so the script stays aligned whether or not the Skill made a suggestion or asked a follow-up. |
| `interview-en.turns.json` | Thirteen English turns for a report whose source language is `en_GB` with a Swedish translation to follow. The sender's message is first given vaguely and then as a claim; the structure is the report's own form, and the Skill is asked to propose the sentence and the sketch; the search phrase is deliberately none; RIV and the chain check are proposed and confirmed; the sources are known but not yet counted. |
| `draft-notes.md` | Swedish notes for a press release, with no sources at all, a claim resting on memory, a quotation, a contact, and no angle, message or working title decided. |
| `review-new-brief.md` | An English brief written to the new template for web copy in free structure. The search phrase is not stated, one sketch step waits on a figure listed under question 12, and the written chain check has one *partly*. |
| `review-old-brief.md` | An English brief written to the old template of thirteen questions for a Swedish case study in ABT, with a `[WEAK: …]` marker on the reader, a *message* answer, a gap in RIV, no one-sentence form or sketch, and no chain check done. |

## The runs

| Run | Lane | Input | Invocation | Turns | Delivered |
| --- | --- | --- | --- | --- | --- |
| `interview-sv` | 1 | none | `/brief --output=brief.md -- Vi arbetar på svenska. Intervjua mig om en skrivbrief enligt mallen.` | `interview-sv.turns.json` | `brief.md` |
| `interview-en` | 2 | none | `/brief --output=brief.md -- We work in English. Interview me for a writing brief following the template.` | `interview-en.turns.json` | `brief.md` |
| `draft` | 3 | `draft-notes.md` as `notes.md` | `/brief --output=brief.md notes.md -- Gör ett utkast till en brief från anteckningarna.` | none | `brief.md` |
| `review-new` | 4 | `review-new-brief.md` as `existing.md` | `/brief --output=brief.md existing.md -- Review this brief.` | none | `brief.md` |
| `review-old` | 5 | `review-old-brief.md` as `existing.md` | `/brief --output=brief.md existing.md -- Review this brief.` | none | `brief.md` |
| `write-interview` | 6 | `interview-sv`'s delivered `brief.md` as `brief.md` | `/write --output=draft.md brief.md` | none | `draft.md` |
| `write-draft` | 7 | `draft`'s delivered `brief.md` as `brief.md` | `/write --output=draft.md brief.md` | none | `draft.md` |
| `write-review` | 8 | `review-new`'s delivered `brief.md` as `brief.md` | `/write --output=draft.md brief.md` | none | `draft.md` |

The Write runs take the brief as the Brief run delivered it, byte for byte, with no genre, technique or language options, as readiness addendum 3 says. A Brief run that delivers no `brief.md` leaves its Write run `skipped` with that reason. That is eight runs and sixteen judgements.

## Judging

Two judges per run, A and B, each a fresh `kntnt-opus-high` subagent, blind to the ticket, to the model, to the revision and to each other. The two judges of one run are dispatched together.

- **Briefs.** A Brief run is judged with [`brief-judge-brief.md`](brief-judge-brief.md), a Write run with [`write-judge-brief.md`](write-judge-brief.md).
- **The message.** A judge's message is its brief's path and a line naming its directory; for a Brief run, also one line naming the mode: `interview`, `draft`, `review of a brief written to the current template` or `review of a brief written to an older template of thirteen questions`. Nothing else is added.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits naming neither the run nor the input. For a Brief run it holds `conversation.md` (every prompt from `prompt.txt` and `prompts.json` beside every reply from `response*.txt`, in order, each under a heading `User, turn N` or `Skill, turn N`, with nothing else added), `brief.md` (the packet's `captured-output.md`, or the single line `NOT DELIVERED`) and, where the run had material, `work/<name>` (its `supplied-input.md`). For a Write run it holds `work/brief.md`, `response.md` (its `response.txt`) and `draft.md` (its `captured-output.md`, or `NOT DELIVERED`). Nothing else goes in, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement.md` there, and it is copied into the run's directory here as `judgement-a.md` or `judgement-b.md`. The mapping from token to run is kept in `runs/judges.tsv`.

## Criteria, fixed before the runs

Each criterion is taken from the acceptance criteria of the body and addenda. A criterion judged by the judges is **met** only where both judges pass it: one judge is enough to record a miss, as readiness addendum 3 says.

| Criterion | From | Question | Runs | Answered by |
| --- | --- | --- | --- | --- |
| `B1` | protocol, mode | Right mode and working language; an interview asks one question at a time in template order | Brief | judges |
| `B2` | addendum 1, headings | All twelve questions as headings in order; only the two English markers | Brief | judges |
| `B3` | body, criterion 2 | The sender's message (3) and the conclusion (9) are separate answers, and a written chain check has the line on whether the conclusion carries the message | Brief | judges |
| `B4` | body, criterion 3 | No answer marked weak; at most one follow-up per answer, only on angle, message or conclusion; no suggestion made twice | Brief | judges |
| `B5` | body, criterion 4 | No demand for sources, links or evidence and no marking of unsubstantiated claims; what needs finding out is open questions under 12 | Brief | judges |
| `B6` | body, criterion 5, and addenda 1–2 | The Skill's statement on whether the brief is enough to write agrees with the rule applied to the delivered brief | Brief | judges |
| `B7` | body, criterion 6, and addendum 1 | Question 7 has the one sentence and a step sketch, or a marked gap; in the draft, what the material does not carry is `[SUGGESTED: …]`, nothing is made up for a step | Brief | judges |
| `B8` | body, criterion 8 | The `kntnt` map holds only settled values; `language` is question 1's source language; the genre's own form omits the technique; free structure is `none` | Brief | judges |
| `B9` | addendum 3 | The chain check: proposed as `[SUGGESTED: …]` and confirmed in an interview, written as `[SUGGESTED: …]` in the draft, reported (or reported missing, none proposed) in a review | Brief | judges |
| `B10` | addenda 1–2, protocol modes | Review statuses, the older-template mapping, closing questions and both offers; the draft's offer of a gap interview | draft, reviews | judges |
| `T1` | body, criterion 7, second half | The run read the chosen technique's or genre's resource for the sketch: `techniques/abt.md` in `interview-sv`, `techniques/pac.md` in `interview-en` (the report's own form), `genres/pressrelease.md` in `draft`; and read no `article-anatomy.md` | the three runs named | this session, from the Harness trace (`trace-index.json` and the transcripts) |
| `G1` | body, criterion 7, first half | Nothing shipped links the Google documents | none | the verifier, against the repository; judges score it `skipped` |
| `G2` | body, criterion 2, first half | The template keeps the message and the conclusion apart | none | the verifier, against the repository; judges score it `skipped` |
| `F1` | protocol | None of the five rejections: no unsupported fact, source or brand detail presented as supplied | Brief | judges |
| `W1` | `brief-444`'s W1, restated | Write reads the brief, takes the settled genre, technique and language from its map, reports its configuration, and writes in question 1's language | Write | judges |
| `W2` | `brief-444`'s W2 | The draft follows the brief's direction and invents nothing the brief does not give | Write | judges |
| `O1` | protocol | Side effects: only the file the output target names is created in the working directory, and nothing else changes there | every run | this session, from the runner's inventories |

The criteria of the editorial-quality matrix that are not listed here are not this evaluation's, and each record says so rather than scoring them.

## Whose miss

A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded, as the protocol's *Whose miss* says. A Write miss that follows from the brief it was given is recorded against the Brief run and not against Write.

## Exit

The ruling ships whatever the measurement shows. The candidate is the product; a miss recorded here does not revert it.

1. **Every criterion is met.** The candidate ships, recorded as met.
2. **A criterion is missed.** The protocol's one revise round may be taken, no larger than the runs that missed, against a revised candidate committed first and staged from its commit, and read in place of the first candidate's runs of those inputs. Whichever wording has fewer misses over the re-run subset ships, the first where they are level. Every remaining miss is recorded as measured and filed as its own `needs-triage` issue naming #471, one issue per defect.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; its output is kept under `voided/` here and not deleted. A run that completes and stops is a finding, judged from what it delivered.

## Inventory scope

The runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch, are the side-effect evidence. Around the waves this session also reads `git status --porcelain --untracked-files=all` of this working tree, which no run writes to; a change there that the build did not make is named in the `side effects` of every run in flight.

## What is written

This file, its briefs and its inputs, committed with the candidate before the first run; `results.md` beside them with every criterion per run, the counts and which exit was taken; the judged packets under `runs/<run>/`; any void run under `voided/`; and two records, one per Skill: `../records/brief-claude-2026-09-30-471.md` and `../records/write-claude-2026-09-30-471.md`. Their lines for `../records/README.md` and the changelog entry are written to `.kntnt-orchestrate/471.md` for the run to apply.
