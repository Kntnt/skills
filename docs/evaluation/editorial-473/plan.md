# Plan for #473: the press release follows the maintainer's instruction

Frozen on 2026-09-30, before the first run. Nothing in this file, in the four judge briefs beside it or in `inputs/` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) first; this file says what it leaves to a ticket.

**`<start>` is `41fd4c55`**, the head of the branch `kntnt-orchestrate/main/473` when the build began. **The candidate is the commit that adds this file.** It holds the rewritten `genres/pressrelease.md` and `genres/pressrelease.review.md`, the measuring script's `--genre=pressrelease`, the loading and measuring steps of Write, Redline and the correction brief, their tests and the regenerated catalog. Every run is staged from it, and so is every input: the inputs are written for this evaluation, live in `inputs/` beside this file, and are committed with it.

The requirement is the ticket's thread as it stood on 2026-09-30: the body, the comment on measurement of 09:36 UTC, the readiness addendum of 14:02 UTC and readiness addendum 2 of 14:10 UTC. Where they conflict, the later one stands.

## What this evaluation is

The instruction is Thomas's and ships whatever the measurement shows, as the protocol's *Not reproduced* says for a maintainer's ruling. There is **no pre-change arm**: the readiness addendum drops it, since nothing here is conditional on reproducing a fault. The measurement decides what is written down as met or missed and what is filed. No decision record is written for this evaluation.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. No Codex Harness and no GPT model is started, controlled or invoked.

Every run is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from the root of this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<candidate> --corpus-revision=<candidate> \
  --invocation='<invocation>' \
  --input=docs/evaluation/editorial-473/inputs/<input> --input-name=<name> \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **`<candidate>`** is the commit that adds this file. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from it with `git archive` into a private root of its own, so every run keeps the protocol's *Staging* and *Top-level runs*.
- **`<name>`** is `source.md` for a Write run and `input.md` for a Redline run.
- **`--capture-output-name=output.md`** is passed to the file-target run and to no other, and copies the delivered `work/output.md` into the packet as `captured-output.md`.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/473.scratch`, this build's scratch directory. Packets are written there and copied into `runs/<run>/` here only after they are judged.
- **The seat.** `claude-opus-5-5` at high deliberation for every run, every correction subagent and nested Proofread pass inside a run, and every judge. The runs request it in `run.json` and record it in `trace-index.json`. Each judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **Lanes.** Each input is in one lane, and a lane's runs are made one after another, so no two runs of one input are in flight at once (#401). Seven lanes run side by side: one for each of the six inputs run once, and one for the clean control's two runs.

## The inputs

All six are synthetic. *Tallmora*, *Tallmora Energi*, *Kvarnbacken* and every person named are invented for this evaluation and tied to no real organisation or customer; the addresses are under `example.se` and the telephone number is the corpus's placeholder.

| Input | What it is | Quotations |
| --- | --- | --- |
| `write-two-quotations.md` | Material for a release about a solar park, with a publication time, a full contact and two quotations: the managing director's comment on the news and the chair's message | two |
| `write-one-quotation.md` | The same material with one quotation carrying both a comment and the message, no publication time, no map link, and a contact with no email address | one |
| `write-no-quotation.md` | The same material with a publication time, a full contact and no quotation | none |
| `redline-old-two-quotations.md` | A release in the old shape, written from the same facts | two |
| `redline-old-one-quotation.md` | The same, with one quotation | one |
| `redline-old-no-quotation.md` | The same, with no quotation and no comment part at all | none |
| `redline-conforming.md` | A release that already conforms, measured at `0` by the candidate's script | two |

Every material carries detail beyond what the news needs — the number of inverters, the panels' orientation, the sheep grazing between the rows — and a caveat that the annual output is the company's own estimate.

### The defects each old-shape input plants

Each old-shape input plants the defects its quotation case allows, and this is the list the Redline judge is given as **Planted defects**:

- **`redline-old-two-quotations.md`:** a headline over 70 characters; a summary over 60 words; the second quotation standing directly after the first, before the body, as one comment part; the second quotation carrying figures (*"Parken har kostat 64 miljoner kronor och ger 7,5 gigawattimmar om året"*) besides its message; a body of three paragraphs; detail kept below the release as notes to the editor where the background is its place.
- **`redline-old-one-quotation.md`:** a headline over 70 characters; a summary over 60 words; detail kept below the release as notes to the editor where the background is its place.
- **`redline-old-no-quotation.md`:** a headline over 70 characters; a summary over 60 words; detail kept below the release as notes to the editor where the background is its place.

The diagnoses these fire are, in `pressrelease.review.md`: *The headline*, *The summary*, *The shape*, and on the two-quotation input also *Where the quotations stand*, *The second quotation* and *The body's length*.

## The runs

These are all the runs this evaluation makes:

| Run | Lane | Input | Invocation |
| --- | --- | --- | --- |
| `write-two` | 1 | `write-two-quotations.md` | `/write --genre=pressrelease --language=sv --output=response source.md` |
| `write-one` | 2 | `write-one-quotation.md` | `/write --genre=pressrelease --language=sv --output=response source.md` |
| `write-none` | 3 | `write-no-quotation.md` | `/write --genre=pressrelease --language=sv --output=response source.md` |
| `redline-two` | 4 | `redline-old-two-quotations.md` | `/redline --genre=pressrelease --language=sv --output=response input.md` |
| `redline-one` | 5 | `redline-old-one-quotation.md` | `/redline --genre=pressrelease --language=sv --output=response input.md` |
| `redline-none` | 6 | `redline-old-no-quotation.md` | `/redline --genre=pressrelease --language=sv --output=response input.md` |
| `control-response` | 7 | `redline-conforming.md` | `/redline --genre=pressrelease --language=sv --output=response input.md` |
| `control-file` | 7 | `redline-conforming.md` | `/redline --genre=pressrelease --language=sv --output=output.md input.md` |

No run has a contextual instruction or a technique. The two control runs are the protocol's clean-control pair: the response-target run and the file-target run, each a fresh session. That is eight runs and sixteen judgements.

## Judging

Two judges per run, A and B, each a fresh `kntnt-opus-high` subagent, blind to the ticket, to the model, to the revision and to each other. The two judges of one run are dispatched together.

- **Briefs.** A Write run is judged with [`write-judge-brief.md`](write-judge-brief.md); an old-shape Redline run with [`redline-judge-brief.md`](redline-judge-brief.md); `control-response` with [`control-judge-brief-response.md`](control-judge-brief-response.md); `control-file` with [`control-judge-brief-file.md`](control-judge-brief-file.md).
- **The message.** A judge's message is its brief's path, a line naming its directory, and, for an old-shape Redline run, one paragraph headed **Planted defects** copied verbatim from the input's bullet above. Nothing else is added.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits naming neither the run, the input nor the arm. It holds, for a Write run, `work/source.md` (the packet's `supplied-input.md`), `response.md` (its `response.txt`) and `delivered.md` (the draft alone, as the reply's fenced block carries it, with nothing added); for a Redline run, `work/input.md` and `response.md`; and for `control-file`, also `work/output.md` (its `captured-output.md`). Nothing else goes in, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement.md` there, and it is copied into the run's directory here as `judgement-a.md` or `judgement-b.md`. The mapping from token to run is kept in `runs/judges.tsv`. The scratch path carries this build's number, which names no arm; the judge is told nothing of it.

## Criteria, fixed before the runs

Each criterion is taken from the acceptance criteria. A criterion judged by the judges is **met** only where both judges pass it: one judge is enough to record a miss, as readiness addendum 2 says.

| Criterion | Question | Runs | Answered by |
| --- | --- | --- | --- |
| `P1` | The part order: headline, summary, quotation 1, body, quotation 2, background, links and attachments, contact, description; a publication time above the headline | Write, old-shape Redline | judges |
| `L1` | Both counted limits hold in the delivered text, or a failing one is reported with its measured figure | Write, old-shape Redline | this session, running the candidate's script with `--genre=pressrelease` on the delivered text |
| `M1` | The run measured the press release with the script and `--genre=pressrelease` | every run | this session, from the parent transcript: a command carrying both `article_anatomy.py` and `--genre=pressrelease` |
| `Q1` | Quotations only where the material has them; for `write-none`, the reply reports the missing quotation as a gap; for Redline, no quotation is written | Write, old-shape Redline | judges |
| `Q2` | Each quotation where the genre puts it for the number the material carries | Write, old-shape Redline | judges |
| `Q3` | The second quotation carries a message and no new fact | `write-two`, `redline-two` | judges |
| `B1` | A body of one or two short paragraphs | Write, old-shape Redline | judges |
| `K1` | Contact details as the material gives them, nothing added | Write, old-shape Redline | judges |
| `D1` | Each planted diagnosis fires | old-shape Redline | judges, per planted defect |
| `U1` | The conforming release comes back unchanged, apart from mechanical corrections | `control-file`, and `control-response` where it delivered a text | judges |
| `N1` | The conforming release draws no finding against a correct part | both control runs | judges |
| `F1` | None of the protocol's five rejections: no unsupported fact, no lost claim unreported | Write, old-shape Redline | judges |
| `O1` | Side effects: only what the output target allows | every run | this session, from the runner's inventories |

`D1` is recorded per planted defect: a defect fires where either the reply reports a finding naming it or the delivered text repairs it and the reply names the defect. A defect fires only where both judges say it fired.

The criteria of the editorial-quality matrix that are not listed here are not this evaluation's, and each record says so rather than scoring them.

## Whose miss

A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded, as the protocol's *Whose miss* says.

## Exit

The instruction ships whatever the measurement shows. The candidate is the product; a miss recorded here does not revert it.

1. **Every criterion is met.** The candidate ships, recorded as met.
2. **A criterion is missed.** The protocol's one revise round may be taken, no larger than the runs that missed, against a revised candidate committed first and staged from its commit, and read in place of the first candidate's runs of those inputs. Whichever wording has fewer misses over the re-run subset ships, the first where they are level. Every remaining miss is recorded as measured and filed as its own `needs-triage` issue naming #473, one issue per defect.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; its output is kept under `voided/` here and not deleted. A run that completes and stops is a finding, judged from what it delivered.

## Inventory scope

The runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch, are the side-effect evidence. Around the waves this session also reads `git status --porcelain --untracked-files=all` of this working tree, which no run writes to; a change there that the build did not make is named in the `side effects` of every run in flight.

## What is written

This file and its briefs and inputs, committed with the candidate before the first run; `results.md` beside them with every criterion per run, the counts and which exit was taken; the judged packets under `runs/<run>/`; any void run under `voided/`; and two records, one per Skill, as #386 did: `../records/write-claude-2026-09-30-473.md` and `../records/redline-claude-2026-09-30-473.md`. Their lines for `../records/README.md` and the changelog entry are written to `.kntnt-orchestrate/473.md` for the run to apply.
