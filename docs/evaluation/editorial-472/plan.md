# Plan for #472: Redline reviews against the template of twelve questions

Frozen on 2026-09-30, before the first run. Nothing in this file, in the judge brief beside it or in `inputs/` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) first; this file says what it leaves to a ticket.

**`<start>` is `315c0afa`**, the head of the branch `kntnt-orchestrate/main/472` when the build began. **The candidate is the commit that adds this file.** It holds the rewritten `brief-review.md`, the one sentence added to Redline's `correction.md`, Redline's `help.md`, the new test in `tests/test_kntnt.py`, the regenerated catalog, and the runner's extension described below. Every run is staged from it.

The requirement is the ticket's thread as it stood on 2026-09-30: the body, the readiness addendum of 14:02 UTC and readiness addendum 2 of 14:10 UTC. Where they conflict, the later one stands.

## What this evaluation is

The behaviour is the one Thomas's ticket states, so it ships whatever the measurement shows, as the protocol's *Not reproduced* says. There is **no pre-change arm**, as the readiness addendum says: the review before the change cannot map a brief onto a template it does not know. The measurement decides what is written down as met or missed and what is filed. No decision record is written for the evaluation.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. No Codex Harness and no GPT model is started, controlled or invoked.

Every run is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from the root of this working tree. The candidate extends it in one way, covered by `tests/test_evaluation_harness.py`: `--extra-input=<path>=<name>`, which may be repeated, places a further file beside the input in the run's working directory under that name, and keeps a copy in the packet as `supplied-<name>`. It is how a run gets the brief and the material the brief points at.

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<candidate> --corpus-revision=<candidate> \
  --invocation='/redline --brief=brief.md --output=response input.md' \
  --input=docs/evaluation/editorial-472/inputs/<text> --input-name=input.md \
  --extra-input=docs/evaluation/editorial-472/inputs/<brief>=brief.md \
  --extra-input=docs/evaluation/editorial-472/inputs/<material>=material.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high
```

- **`<candidate>`** is the commit that adds this file.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/472.scratch`, this build's scratch directory. Packets are written there and copied into `runs/<run>/` here only after they are judged.
- **The invocation** is the same for every run: the brief by the Formal Invocation's `--brief`, as readiness addendum 2 says, the response as the Output Target, the default Correction Budget of one, and no genre, technique, language or Contextual Instruction. Genre, technique and language come from the brief's `kntnt` map.
- **The seat.** `claude-opus-5-5` at high deliberation for every run, every correction subagent, reply checker and nested Proofread pass inside a run, and every judge. The runs request it in `run.json` and record it in `trace-index.json`. Each judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **Lanes.** Each brief–text pair is one lane, and its two runs are made one after the other, so no two runs of one input are in flight at once (#401). The four lanes run side by side.

## The inputs

All are synthetic and in English. *Larkspur Ledger*, *the Hatherley Repair Café*, *Pellbrook Library* and every person named are invented for this evaluation and tied to no real organisation or customer. Each brief points at its material as `material.md`, which every run is given beside it.

| Input | What it is |
| --- | --- |
| `brief-a.md` | A brief to the new template for a newsletter piece, genre `general`, technique `abt`. The sender's message (question 3), that the app's receipt scanner makes a weekly receipt session a ten-minute job, is meant to be conveyed indirectly; the conclusion (question 9) is that ten minutes every Friday makes the January return a short job. The call to action is indirect. The sketch has five steps: the situation, the problem with the survey figure, the Friday session, the example of Priya Nand, and an ending back at the tin of receipts. |
| `material-a.md` | The survey, the interview and the support team's note that `brief-a.md` lists. |
| `text-a-carries.md` | A text that carries the sender's message without stating it: it leads the reader to a ten-minute Friday session with photographs in the app, and never says the scanner makes it ten minutes. It lands in the conclusion, its ending ties back to the tin of the hook, and its call to action is indirect. It departs from the sketch step by step while delivering the brief's one sentence: it opens on Priya's tin rather than a general drawer, carries her example through the text instead of in a step of its own, and moves the survey figure from the problem to after the Friday session. |
| `text-a-elsewhere.md` | A text on the same facts that leads elsewhere: it lands in handing the receipts to an accountant rather than a weekly habit, so it contradicts the sender's message and does not land in the conclusion. Its call to action is indirect: it leaves the reader thinking about an accountant. |
| `brief-b.md` | A brief to the new template for a community newsletter piece, genre `general`, free structure (`technique: none`). Its sketch makes one claim nothing supports (that members say the café has saved them money) and has a step that waits on an open research question (what share of items are fixed on the day); question 12 lists two sources and two things to find out, that share and the date and room of the December session. The call to action is direct. |
| `material-b.md` | The volunteer handbook and the September notes that `brief-b.md` lists. |
| `text-b.md` | A text that carries the message and lands in the conclusion. It leaves out the unsupported sketch claim and gives no figure for the share fixed. It makes one claim the material does not support: that the volunteers have kept more than a tonne of electrical goods out of landfill since the café opened. |
| `brief-c.md` | A brief to the old template as it stood at `41fd4c55`, with its thirteen questions and its check, for a council newsletter piece, genre `general`, technique `abt`. Its *message* answer is a one-sentence claim, the reader's answer carries a `[WEAK: …]` marker, its structure answer is `ABT.` alone, and the check is not done. |
| `material-c.md` | The club's leaflet and notes from a visit, which `brief-c.md` points at. |
| `text-c.md` | A text that lands in the old *message* answer. |

## The runs

| Run | Lane | Text as `input.md` | Brief as `brief.md` | Material as `material.md` |
| --- | --- | --- | --- | --- |
| `a-carries-1`, then `a-carries-2` | 1 | `text-a-carries.md` | `brief-a.md` | `material-a.md` |
| `a-elsewhere-1`, then `a-elsewhere-2` | 2 | `text-a-elsewhere.md` | `brief-a.md` | `material-a.md` |
| `b-1`, then `b-2` | 3 | `text-b.md` | `brief-b.md` | `material-b.md` |
| `c-1`, then `c-2` | 4 | `text-c.md` | `brief-c.md` | `material-c.md` |

Every run uses the one invocation above. That is eight runs and sixteen judgements.

## Judging

Two judges per run, A and B, each a fresh `kntnt-opus-high` subagent, blind to the ticket, to the model, to the revision and to each other. The two judges of one run are dispatched together, with [`judge-brief.md`](judge-brief.md).

- **The message.** A judge's message is its brief's path, a line naming its directory, and one paragraph headed **What the input was written to contain**, copied verbatim from the line for its pair below. Nothing else is added.
  - `a-carries`: *The brief is written to the current template. The text carries the sender's message (question 3) without stating it, lands in the conclusion (question 9), ends on the hook's tin of receipts, and has an indirect call to action. It departs from the brief's sketch step by step — order, merged steps, and where the survey figure stands — while delivering the brief's one sentence for the whole text.*
  - `a-elsewhere`: *The brief is written to the current template. The text leads the reader somewhere other than the sender's message (question 3) and contradicts it, and does not land in the conclusion (question 9). Its call to action is indirect.*
  - `b`: *The brief is written to the current template. Its sketch makes a claim nothing supports, that members say the café has saved them money, and a step of it waits on an open research question, the share of items fixed on the day; question 12 lists two open research questions. The text leaves the unsupported sketch claim out, gives no figure for the share, and makes one claim the material does not support: that the volunteers have kept more than a tonne of electrical goods out of landfill.*
  - `c`: *The brief is written to an older template of thirteen questions, with one question on the message where the current template has the sender's message (question 3) and the conclusion (question 9), and it does not keep the two apart. Its answer on the reader carries a `[WEAK: …]` marker.*
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits naming neither the run nor the input. It holds `work/input.md`, `work/brief.md` and `work/material.md` (the packet's `supplied-input.md`, `supplied-brief.md` and `supplied-material.md`) and `response.md` (its `response.txt`). Nothing else goes in, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement.md` there, and it is copied into the run's directory here as `judgement-a.md` or `judgement-b.md`. The mapping from token to run is kept in `runs/judges.tsv`.

## Criteria, fixed before the runs

Criteria 1–5 are the readiness addendum's five frozen criteria. A criterion judged by the judges is **met** only where both judges pass it: one judge is enough to record a miss, as readiness addendum 2 says.

| Criterion | From | Question | Runs | Answered by |
| --- | --- | --- | --- | --- |
| `K1` | criterion 1 | With `text-a-carries.md`, the sender's message is judged fulfilled, and no finding faults the text for not stating it. With `text-a-elsewhere.md`, it is judged a shortfall (partly or not fulfilled) because the text leads elsewhere or contradicts it. | A | judges |
| `K2` | criterion 2 | The structure is judged on the one sentence for the whole text, the hook's resolution and the conclusion, and no shortfall is recorded for departing from the sketch's steps or their order. An indirect call to action is judged by what the text leaves the reader with, and the text is not faulted for not asking the reader to do something. | A, B | judges |
| `K3` | criterion 3 | No open research question and no unsupported sketch claim becomes a shortfall of the text; each open research question is named as open. The tonne claim is reported as a claim the material does not support, and the delivered text gives it no support the material lacks. | B | judges |
| `K4` | criterion 4 | The old *message* answer is assessed as the conclusion, question 9. The sender's message, question 3, is reported unanswered. The `[WEAK: …]` answer on the reader is assessed and flagged **weak**. | C | judges |
| `K5` | criterion 5 | The report is per question, by the current template's number and heading: every one of its questions appears, answered with a status or named as unanswered, under its number and its heading as the template words it. | every run | judges |
| `M1` | addendum, *Repairs* | The delivered text does not state the sender's message outright where the input did not. | A | judges |
| `F1` | protocol | None of the protocol's five rejections: no unsupported fact added, and every claim removed or changed is reported. | every run | judges |
| `O1` | protocol | Side effects: nothing in the working directory is created, changed or removed, the three supplied files included, since the Output Target is the response. | every run | this session, from the runner's inventories |

The criteria of the editorial-quality matrix that are not listed here are not this evaluation's, and each record says so rather than scoring them.

## Whose miss

A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded, as the protocol's *Whose miss* says.

## Exit

The ruling ships whatever the measurement shows. The candidate is the product; a miss recorded here does not revert it.

1. **Every criterion is met.** The candidate ships, recorded as met.
2. **A criterion is missed.** The protocol's one revise round may be taken, no larger than the runs that missed, against a revised candidate committed first and staged from its commit, and read in place of the first candidate's runs of those inputs. Whichever wording has fewer misses over the re-run subset ships, the first where they are level. Every remaining miss is recorded as measured and filed as its own `needs-triage` issue naming #472, one issue per defect.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; its output is kept under `voided/` here and not deleted. A run that completes and stops is a finding, judged from what it delivered.

## Inventory scope

The runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch, are the side-effect evidence. Around the waves this session also reads `git status --porcelain --untracked-files=all` of this working tree, which no run writes to; a change there that the build did not make is named in the `side effects` of every run in flight.

## What is written

This file, its judge brief and its inputs, committed with the candidate before the first run; `results.md` beside them with every criterion per run, the counts and which exit was taken; the judged packets under `runs/<run>/`; any void run under `voided/`; and one record, `../records/redline-claude-2026-09-30-472.md`. Its line for `../records/README.md` and the changelog entry are written to `.kntnt-orchestrate/472.md` for the run to apply.
