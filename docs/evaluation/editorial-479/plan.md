# Plan for #479: a pending closure read as a presupposition in a clean opinion's standfirst

Frozen on 2026-10-01, before the first run of either arm and before any product change. Nothing in this file, in the two judge briefs beside it, in `inputs/`, or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first. The requirement is the ticket's thread as it stood on 2026-10-01: the body and the triage comment of 11:18 UTC. Where they conflict, the later one stands.

**`<start>` is `fb169087`**, the commit this build started from. The pre-change arm is staged from it. **The corpus commit is `fb169087`.** Every corpus input and every frozen corpus expectation is read from it; this ticket's diff does not touch the corpus. **The candidate**, if one is written, is committed after the pre-change arm has been read and before the post-change arm is staged, and `results.md` names its commit.

## What the ticket measured, and what it is not

In #468's evaluation one candidate-arm run of six, `post-opinion-clean-file-1` (staged from `8a0c3bea`), deleted *innan den ena stängs* from `opinion-clean`'s standfirst on the finding that the clause presents the closure of one booking route as given while the body leaves it open. Both judges failed `R1`. No pre-change run of that evaluation, staged from `41fd4c55`, changed the standfirst. Those counts were made on other product versions. They are recorded in `results.md` as the ticket's history and are never read as this evaluation's baseline: the baseline is the pre-change arm below.

## What is under test

The ticket's change is conditional on the measurement. Whether any product change is written at all is decided by the pre-change arm.

- **The defect.** A review reads a passage of a clean opinion that sets out what is to happen before the decision the text argues over as an assertion, presupposition or prediction that the decision has an outcome the text does not carry, and records that reading as a finding. Its worst form is the one #468 measured: the finding is repaired by deleting or changing the passage, and the change is delivered.
- **The candidate**, if the defect reproduces, is the smallest change to the review prose at the place the pre-change arm's traces show the reading arising, with its test in `tests/`, the help and runtime prose it touches kept in agreement, and `skills/kntnt/catalog.json` regenerated. It does not exempt the word *innan*, the standfirst, or any form of words. It makes no change to the corpus, to Write's halves, to the correction budget, to the source-blind review, to the closing Proofread pass, to metadata handling or to the input and output contracts. Where it touches `base.review.md`, which #480 may also change, `results.md` says so, so that both targets are verified after integration.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

Every Redline run of both arms, and of any revise round, is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), by [`runs/lane.sh`](runs/lane.sh), which runs this command from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=<source> \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **`<commit>`** is `fb169087` for the pre-change arm, the candidate's commit for the post-change arm, and the committed revised candidate for a revise round. `runs/matrix.tsv` names the post-change rows' revision `candidate`, and `lane.sh` takes the commit as its third argument. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own and installs them as the session's Skills, so the run's Proofread dependency is met by the Proofread staged beside Redline.
- **`<input>`** is the input the matrix names, written with `git show` into `<scratch>/inputs/`, never read from a working tree: a corpus input from `fb169087`, and this evaluation's own input (source `frozen`) from the commit that last changed it, which is the commit that freezes this plan. `<source>` is that commit.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other. It copies the delivered `work/output.md` into the packet as `captured-output.md`.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/479.scratch`, this build's scratch directory. The packet is written there.
- **The seat.** `claude-opus-5-5` at high deliberation, for every run, every correction subagent and every judge. It is requested in `run.json` and recorded for the session and every nested agent in `trace-index.json`. The correction subagents and the nested Proofread pass run inside the session and take its seat. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **The private root.** The run's `HOME`, working directory, temporary directory and caches are made by `mkdtemp` under the system temporary directory and removed by the runner on every exit. The runner strips every `CLAUDE_*` variable, so no run has a session scratchpad; no fault under test lives in one.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) assigns every run to one of four lanes, one per input, and `lane.sh LANE ARM` makes that lane's runs of that arm one after the other. Every run of one input is in one lane, so no two runs of one input are in flight at once (#401), and at most four runs are in flight at any time. The pre-change arm is made in full, all four lanes, before any candidate exists. A run whose packet exists is not made again.

## The run table

The table is exhaustive. Both arms run every row; the post-change arm runs only if the defect reproduces. `runs/matrix.tsv` lists all thirty-four runs by name, lane, arm, revision, input source, input and invocation.

| Input | SHA-256 (first 16) | Role | Invocation | Runs per arm | Run names | Judge brief |
| --- | --- | --- | --- | --- | --- | --- |
| `opinion-clean` | `141efb2a4a3b9339` | Target: the supported order before a considered decision | `/redline --genre=opinion --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs | `<arm>-opinion-clean-{resp,file}-<n>` | `control-judge-brief.md` for `resp`, `control-judge-brief-file.md` for `file` |
| `opinion-closure-certain` | `7e636c8bbcf9fc1f` | The negative case: a real contradiction and an unsupported certain outcome | `/redline --genre=opinion --language=sv --output=output.md input.md` | three | `<arm>-opinion-closure-certain-<n>` | `control-judge-brief-file.md` |
| `article-clean` | `f183e6da31cf7808` | Control: #468's preserved standfirst | `/redline --genre=article --language=sv --output=response input.md`, and its pair | three pairs | `<arm>-article-clean-{resp,file}-<n>` | as `opinion-clean` |
| `opinion-flawed` | `ab033d9f4c817c9e` | Control: real defects in an opinion still detected | `/redline --genre=opinion --language=sv --output=response input.md` | two | `<arm>-opinion-flawed-<n>` | `control-judge-brief.md` |

`<arm>` is `pre` or `post`. The corpus inputs are `controls/<row>.md`. Each input is copied to `input.md` and nothing else is in the working directory. No run has a contextual instruction or a technique. A pair is one response-target run and one file-target run, as the protocol's *A clean control* defines them.

That is seventeen runs per arm, thirty-four if both arms run, and two judgements per run.

### The negative case

[`inputs/opinion-closure-certain.md`](inputs/opinion-closure-certain.md) is `opinion-clean` at `fb169087` with one change, in the standfirst's last sentence: *innan den ena stängs* becomes *innan telefonbokningen ändå stängs för gott*. Nothing else differs. It keeps the word *innan* and the standfirst position of the target, so a change that exempts either would let it through. The sentence now states as settled that the telephone booking closes for good whatever the trial shows, and the text's own argument contradicts that. `article_anatomy.py` at `fb169087` measures it as conforming, with a 41-word standfirst. Its frozen expectation, written for this evaluation and given to its judges exactly as the corpus rows' are, is:

> The standfirst's last sentence says that both booking routes should be tried for another half-year *innan telefonbokningen ändå stängs för gott*: it states as settled that the telephone booking closes for good whatever the trial shows. The headline (*Avskaffa inte telefonbokningen på ett antagande*), the lead (*Ett permanent beslut behöver bättre underlag än det som nu ligger på bordet*) and the ending (*Först då går det att väga alternativen*) argue that this decision is still to be weighed. Detect it: an internal contradiction and an outcome the text does not support, stated in the standfirst. It is repaired from the text's own content or reported unresolved. Otherwise the text conforms to the anatomy. Preserve the polemical final sentence, the early thesis, the attribution, the real administrative objection, the cost uncertainty and the ending's named decision for the council. Do not flatten to neutral exposition or add generic hedges. Reject any finding against a limit the text meets (47-character headline, 41-word standfirst, 33–40-character subheadings), any finding resting on the single-paragraph section, the one-sentence closing paragraph or the four-sentence paragraph, and a finding against the Swedish `Text:` byline form.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The two judges of one run are dispatched together and are not told of each other. The briefs are copied byte for byte from [`../editorial-468/`](../editorial-468/).

- **Which brief.** A response-target run is judged with `control-judge-brief.md`, and a file-target run with `control-judge-brief-file.md`.
- **The message.** A judge's message is its brief verbatim, a line `---`, a line naming the run directory, and a line giving its letter, `a` or `b`. It then carries one paragraph headed **Frozen expectation**: for a corpus row, the row's *Frozen expectation and rejection* cell in the corpus README at `fb169087`, copied verbatim; for `opinion-closure-certain`, the quoted paragraph above. It is also written to the run's `expectation.md`. Nothing else is added. No hint of the defect under investigation appears in any invocation, any brief or any message.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits that name neither the arm, the input, the run nor the target. It holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`; for a file-target run, also `work/output.md`, copied from `captured-output.md`. It holds nothing else, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement-<letter>.md` there, and it is copied into the run's packet as `judgement-a.md` or `judgement-b.md`. The mapping from directory to run is kept in `runs/judges.tsv`. The judges' directories are under `<scratch>`, whose path carries this build's number; that number names neither the arm nor the expected verdict, the judge is told nothing of what it is, and every brief forbids reading any repository file or ticket.

A response-target entry that returned only a no-change status has its `R1` scored `skipped` in the record, with the reason the protocol gives: no text was delivered, and the file-target entry answers the criterion. A file-target run that leaves no `output.md` is recorded as delivering none, with its `R1` `skipped` for that reason; that is a defect, filed as its own issue.

## Criteria, fixed before the runs

- **`R1`**, on every run: the corpus criterion, as the control briefs quote it.
- **`C1`**, on every run: the run meets its row's frozen expectation.
- **`O1`**, on every run, from the runner's before-and-after inventories: the run created, replaced or removed nothing its output target does not allow.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.
- **`T1`**, on every `opinion-clean` and `opinion-closure-certain` run, from the trace: the four stages under *The trace* below are each read and recorded. It is `pass` where every stage the run reached is recorded from its own evidence, and `skipped`, naming the gap, where the trace kept nothing that reaches a stage.

Every other criterion the record template names is recorded `skipped` on every run, naming these as this evaluation's criteria.

### When `R1` is met

A run meets `R1` when both judges pass it, and misses it when both fail it. Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary; in that case both readings are recorded and the run meets `R1`. `C1` is read by the same rule.

## The trace

The ticket asks that the first finding, the correction round's proposal, the re-review's decision and the delivered text be told apart, because a wrong deletion that is restored is a different observation from one that is delivered, and an accurate account does not make an impermissible change permissible. For every `opinion-clean` and `opinion-closure-certain` run, this session reads the four stages from the packet's transcripts and `trace-index.json` and writes them to the packet's `rounds.md`:

1. **The first review's findings.** The findings section of the first correction brief the run's session handed a subagent, quoted whole. Where the run started no correction subagent, the findings its reply reports, quoted, or `none`.
2. **The correction proposal.** For each round, the subagent's returned text compared with the text it was handed, every difference listed.
3. **The re-review's decision.** For each round, whether the session accepted the candidate, restored a difference that traced to no finding, or rejected the round and restored the text from before it, read from what the session did next and quoted from its own words.
4. **The delivered text.** Every difference between the input and the delivered text: the file-target run's `output.md`, or a text a response-target run delivered in its reply.

The extraction is mechanical and judges nothing. It is made by a script this session writes into `runs/` once the first packet exists, which is committed with the results and is not part of the method frozen here.

## Reading the Target: `opinion-clean`

A **closure-as-given finding** is a finding, at stage 1 or in the reply, that names a passage of `opinion-clean` which sets out what is to happen before the decision the text argues over, or names that decision as pending — the standfirst's *ett halvår till innan den ena stängs*, the lead's *Pröva först båda bokningsvägarna*, the ending's *säga ja till halvåret* or *Först då går det att väga alternativen*, among others — and calls it an assertion, presupposition or prediction of an outcome the text does not carry, such as that a route closes, that the switch happens or that the decision is already taken, or calls it a contradiction of another passage on that ground. This session calls each finding from its own words and writes the call in `results.md` beside the quoted finding. It reads the finding and not the arm label, but it made the runs and knows their arms, so **this call is not blind**; the judges' `R1` readings are recorded beside it and do not decide it. Every other finding a run records against `opinion-clean` is listed too, and not counted toward the Target.

- **A run shows the defect** where it records a closure-as-given finding at any stage, whatever became of it. It is recorded at one of three depths: **reported** (a finding left unresolved, or found and not acted on), **restored** (a round that changed the passage and was rejected or undone, so the text came back without the change), and **delivered** (the delivered text changes the passage the finding names).
- **Reproduced** where at least one pre-change run of six shows the defect.
- **The Target is met** where no candidate run shows the defect, and no candidate run misses `R1`.

## Reading the controls

- **`opinion-closure-certain`.** In one run, the planted defect is detected where the reply reports a finding that names the standfirst's settled closure, or its contradiction of the headline, the lead or the ending, or the delivered text repairs it and the reply names the repair. It is read from the two judges' answers under heading 3 of their brief. Where both judges record it as detected, or both as not, that stands. Where they split, this session reads the reply, quotes the finding or the repair it decides on, and records both judges' readings beside the call. **The negative case holds** where the candidate arm detects it in at least as many runs as the pre-change arm, and no more candidate runs miss `R1` than pre-change runs.
- **`article-clean`.** A standfirst difference counts as #468's plan counted it: any difference in the bold paragraph between the headline and the byline that both judges do not class as a mechanical correction. **The control holds** where no more candidate runs than pre-change runs show such a difference, and no more candidate runs than pre-change runs miss `R1`.
- **`opinion-flawed`.** The defects are #468's, clause by clause from the frozen expectation: (o1) unsupported motives; (o2) a population inference contradicted by the booking denominator; (o3) a cost contradiction; (o4) a vague final exhortation; (o5) no standfirst; (o6) `Bakgrund` and `Diskussion`, which label the sections instead of describing them; (o7) no ending section. Detection in one run is read as for the negative case. In one arm, a defect counts as detected where at least one of that arm's two runs detects it. **The control holds** unless a defect the pre-change arm detected goes undetected in the candidate arm.

## Whose miss

The protocol's rule applies. A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded; where they split, the rule under *When `R1` is met* decides. A working headline reported or rewritten is #480's; a fault in the reply's own account of its changes is #477's or #478's. A closure-as-given finding on `opinion-clean` is this ticket's.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), with [`runs/inventory.sh`](runs/inventory.sh), both copied from #468's with only their paths substituted:

3. **This build's scratch root** `<scratch>`, the packets and the judges' directories among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so neither is hashed.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/7bb3980e-f903-4106-b84f-69be7f823dbe/scratchpad/`, which other sessions of the same run also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Ship rule

The protocol's semantics for a ticket whose change is conditional on the measurement.

1. **Not reproduced.** Where no pre-change run of `opinion-clean` shows the defect, the result is recorded as not reproduced on this seat. No candidate is written, the post-change arm is not run, and nothing under `skills/` changes. One decision record, `docs/adr/0234`, records it, as the protocol's *Not reproduced* requires.
2. **Reproduced.** The candidate is written from the traces of the runs that show the defect, committed, and the post-change arm is made over the whole matrix from its commit and judged as above.
   - Where the Target is met and the negative case and every control hold, the candidate ships, recorded as met.
   - Otherwise the protocol's one revise round is taken, no larger than the subset that failed: every run, in the post-change arm's numbers, of each input whose reading missed or whose control failed, against a revised candidate committed first and staged from its commit. The revise round's runs are named `rev-<input>-…`, listed in `runs/matrix-revise.tsv` in `matrix.tsv`'s columns with the revised commit as their revision, and made by the frozen `lane.sh`; they are judged exactly as above. After it, the revised candidate ships where it meets the Target and the negative case and every control hold; otherwise it ships only where fewer of its `opinion-clean` runs show the defect than the pre-change arm's, and the negative case and every control hold, reading an input not re-run from the first candidate's arm; otherwise the product stays as it was at `<start>`, and no decision record is written, since the defect reproduced.

Whichever way it falls, the result is written as measured.

**Filing.** Each remaining miss is filed as its own `needs-triage` issue naming #479: the Target, where it is missed in the arm whose wording ships, or in the candidate arm where nothing ships; each control or negative case that fails; and any other miss a judged run shows that no open ticket carries. A miss the whose-miss rule assigns to an open ticket is recorded under that ticket and not filed again.

## Void runs

A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; so is a run that reports a file it wrote changed or deleted under it by another process. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again, and a void judgement is kept there too. A run that completes and stops is a finding.

No criterion is softened, no frozen plan, brief, input or fixture is edited to fit a result, and no arm is re-run to get a better reading.

## What is written

This file, the two judge briefs, `inputs/opinion-closure-certain.md` and the four files under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; each run's packet under `runs/<run>/`, with its `expectation.md`, its two judgements and, for the two opinion inputs, its `rounds.md`; the trace extraction script; `runs/judges.tsv` and the wave inventories under `runs/waves/`; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-479.md`, in the protocol's format. A packet's `stream.jsonl` and `transcripts/` are read for the seat and the trace, which its `trace-index.json` and `rounds.md` keep, and are not committed. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
