# Plan for #468: a loss counted as its reader suffers it, and no premise written in

Frozen on 2026-09-30, before the first run of either arm. Nothing in this file, in the two judge briefs beside it, or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first. The requirement is the ticket's thread as it stood on 2026-09-30: the body, the triage comment of 14:01 UTC and the readiness addendum of 14:10 UTC. Where they conflict, the later one stands.

**`<start>` is `41fd4c55`**, the commit this build started from. The pre-change arm is staged from it. **The candidate is `8a0c3bea`**, committed before this plan, and the post-change arm is staged from it. **The corpus commit is `41fd4c55`.** Every input and every frozen expectation is read from it; this ticket's diff does not touch the corpus.

## What this plan copies

The readiness addendum names four things this plan copies from [`../editorial-429/plan.md`](../editorial-429/plan.md), with only paths and the seat substituted, and nothing else:

- **The two control briefs**, byte for byte: [`control-judge-brief.md`](control-judge-brief.md) and [`control-judge-brief-file.md`](control-judge-brief-file.md).
- **The split rule**, stated under *When `R1` is met* below.
- **The runner and turn files**: [`runs/lane.sh`](runs/lane.sh), with its scratch root and corpus commit substituted; [`runs/wave_inventory.sh`](runs/wave_inventory.sh), with its scratch root, session scratchpad and working tree substituted; [`runs/inventory.sh`](runs/inventory.sh), a byte copy; and [`runs/matrix.tsv`](runs/matrix.tsv) in #429's columns, listing this plan's runs.
- **Void-run handling**, stated under *Void runs* below.

#429's heading target, its controls and its ruling-ships exit are not copied. This ticket's Target, Control and ship rule replace them, below.

## What is under test

The ticket's change is conditional on the measurement. It has two halves, and each is read, reproduced or not, and shipped or not, apart from the other.

- **The reader-loss half.** `skills/kntnt/library/references/editorial/base.review.md` gains, in its opening paragraph beside the finding rule, that a loss is counted as the reader who meets the passage in its place would suffer it, not as the strictest reading of a single word could construct it, for every passage, the headline, the standfirst and each subheading as much as the body; and that a writer's own judgement the text supports is not a claim the text does not carry. `headlines.review.md`'s *Leave alone* no longer states that rule in its own words and points at the base review. Its fixture is `article-clean`.
- **The premise half.** `base.review.md`'s smallest-correction paragraph gains, beside *Introduce no new evidence, experience, attribution or outcome*, that a repair writes in no premise, assumption or inference that the text's argument leaves implicit: where a reader cannot follow the argument without it, the gap is reported for the author as unresolved, and where a reader can, it is no finding. Redline's `references/correction.md` gains *or writing a premise the text leaves unstated* in the sentence that lists what the correction agent leaves alone. Its fixture is `opinion-clean`.

The candidate also changes `tests/test_kntnt.py` and the regenerated `skills/kntnt/catalog.json`, and no other file under `skills/`. `base.md` and `headlines.md`, the halves Write loads, are not changed.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

Every Redline run of both arms, and of any revise round, is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), by [`runs/lane.sh`](runs/lane.sh), which runs this command from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=41fd4c55 \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **`<commit>`** is `41fd4c55` for the pre-change arm, `8a0c3bea` for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own and installs them as the session's Skills, so the run's Proofread dependency is met by the Proofread staged beside Redline.
- **`<input>`** is the input the matrix names, written from `41fd4c55` with `git show` into `<scratch>/inputs/`, never read from a working tree.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other. It copies the delivered `work/output.md` into the packet as `captured-output.md`.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/468.scratch`, this build's scratch directory. The packet is written there.
- **The seat.** `claude-opus-5-5` at high deliberation, for every run, every correction subagent and every judge. It is requested in `run.json` and recorded for the session and every nested agent in `trace-index.json`. The correction subagents and the nested Proofread pass run inside the session and take its seat. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **The private root.** The run's `HOME`, working directory, temporary directory and caches are made by `mkdtemp` under the system temporary directory and removed by the runner on every exit. The runner strips every `CLAUDE_*` variable, so no run has a session scratchpad; no fault under test lives in one.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) assigns every run to one of four lanes, one per input, and `lane.sh` makes a lane's runs one after the other. Every run of one input is in one lane, so no two runs of one input are in flight at once (#401), and at most four runs are in flight at any time. Within a lane the two arms alternate. A run whose packet exists is not made again.

## The run table

The table is the ticket's, and it is exhaustive. Both arms run every row. `runs/matrix.tsv` lists all thirty-two runs by name, lane, revision, input and invocation.

| Input | SHA-256 (first 16) | Invocation | Runs per arm | Run names | Judged by |
| --- | --- | --- | --- | --- | --- |
| `article-clean` | `f183e6da31cf7808` | `/redline --genre=article --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs | `<arm>-article-clean-resp-<n>`, `<arm>-article-clean-file-<n>` | two judges per run |
| `opinion-clean` | `141efb2a4a3b9339` | `/redline --genre=opinion --language=sv --output=response input.md`, and its pair | three pairs | `<arm>-opinion-clean-{resp,file}-<n>` | two judges per run |
| `article-flawed` | `1c0e3b3ef98e06b2` | `/redline --genre=article --language=sv --output=response input.md` | two | `<arm>-article-flawed-<n>` | two judges per run, `control-judge-brief.md` |
| `opinion-flawed` | `ab033d9f4c817c9e` | `/redline --genre=opinion --language=sv --output=response input.md` | two | `<arm>-opinion-flawed-<n>` | two judges per run, `control-judge-brief.md` |

`<arm>` is `pre` or `post`. The inputs are the corpus's `controls/<row>.md`. Each is copied to `input.md` and nothing else is in the working directory. No run has a contextual instruction or a technique. A pair is one response-target run and one file-target run, as the protocol's *A clean control* defines them.

That is sixteen runs per arm, thirty-two before any revise round, and sixty-four judgements.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The two judges of one run are dispatched together and are not told of each other.

- **Which brief.** A response-target clean-control run and a flawed-control run are judged with `control-judge-brief.md`. A file-target clean-control run is judged with `control-judge-brief-file.md`.
- **The message.** A judge's message is its brief verbatim, a line `---`, a line naming the run directory, and a line giving its letter, `a` or `b`. It then carries one paragraph headed **Frozen expectation**: the row's *Frozen expectation and rejection* cell in the corpus README at `41fd4c55`, copied verbatim, which is also written to the run's `expectation.md`. Nothing else is added. No hint of the defect under investigation appears in any invocation, any brief or any message.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits that name neither the arm, the input, the run nor the target. It holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`; for a file-target run, also `work/output.md`, copied from `captured-output.md`. It holds nothing else, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement-<letter>.md` there, and it is copied into the run's packet as `judgement-a.md` or `judgement-b.md`. The mapping from directory to run is kept in `runs/judges.tsv`. The judges' directories are under `<scratch>`, whose path carries this build's number; that number names neither the arm nor the expected verdict, the judge is told nothing of what it is, and every brief forbids reading any repository file or ticket.

A response-target entry that returned only a no-change status has its `R1` scored `skipped` in the record, with the reason the protocol gives: no text was delivered, and the file-target entry answers the criterion. A file-target run that leaves no `output.md` is recorded as delivering none, with its `R1` `skipped` for that reason; that is a defect, filed as its own issue.

## Criteria, fixed before the runs

- **`R1`**, on every run: the corpus criterion, as the control briefs quote it.
- **`C1`**, on every run: the run meets its row's frozen expectation, read against the row as `41fd4c55` leaves it.
- **`O1`**, on every run, from the runner's before-and-after inventories: the run created, replaced or removed nothing its output target does not allow.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

Every other criterion the record template names is recorded `skipped` on every run, naming `R1`, `C1`, `O1` and `S1` as this evaluation's criteria. No criterion here is answered from the Harness trace.

### When `R1` is met

A run meets `R1` when both judges pass it, and misses it when both fail it. Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary; in that case both readings are recorded and the run meets `R1`. `C1` is read by the same rule.

## The delivered text

A run's delivered text is the file-target run's `output.md`, or a text a response-target run delivered in its reply. A response-target run whose reply returns only a no-change status delivered no text, and a reply that reports a finding and delivers no text changed nothing. Both targets are read under each Target below, since the Target speaks of every run.

## Reading the Target

Each half is read on its own fixture, in each arm.

### The reader-loss half: `article-clean`'s standfirst

The standfirst is the bold paragraph between the headline and the byline. This session compares the standfirst of each run's delivered text with the input's, mechanically, and reads the judges' class for each difference it finds.

- **What counts.** A difference in the standfirst that both judges class as a mechanical correction does not count. Any other difference in the standfirst counts: a word removed, added or replaced, a sentence split or joined, the standfirst removed or moved.
- **A run shows the defect** when its delivered text has a standfirst difference that counts.
- **Reproduced** when at least one pre-change run shows the defect.
- **The Target is met** when no candidate run shows the defect.

### The premise half: what `opinion-clean` gains

This session reads every difference between the input and the delivered text of each `opinion-clean` run, the file-target runs' `output.md` and any text a response-target run delivered in its reply. An addition is a difference whose delivered side has words the input's side does not: a sentence, a clause or a paragraph added, or words put in place of others.

- **The test.** An addition counts toward the Target where it asserts something no sentence of the input states: a premise, an assumption or an inference. An addition that only names what a sentence of the input already states is a clarification, such as a lead that names both booking routes the text already names, or the two routes the proposal already weighs. A clarification is recorded and not counted.
- **Who calls it.** This session calls each addition, from the two texts, and writes the call beside it in `results.md` with the input sentence that states it, or the words no input sentence states. The judges' classes are recorded beside each call and do not decide it. The session reads the text and not the arm label, but it made the runs and knows their arms, so **this call is not blind**. It is the addendum's rule, and it is stated here so that nobody reads the call as a blind one.
- **A run shows the defect** when its delivered text has at least one addition that counts.
- **Reproduced** when at least one pre-change run shows the defect.
- **The Target is met** when no candidate run shows the defect.

## Reading the Control

The Control is the two flawed rows. The defects each row names, clause by clause from its frozen expectation at `41fd4c55`, are:

- **`article-flawed`**: (a1) unsupported catastrophe and health certainty visible against the text's explicit limits; (a2) a standfirst and lead that repeat each other and open on the same word; (a3) a concept explained late; (a4) an unbroken paragraph mixing unlike jobs; (a5) no byline; (a6) a 187-word lead; (a7) no subheading anywhere, so no section and no ending; (a8) a closing sales line unrelated to the explanation; (a9) a headline that fails on truthfulness.
- **`opinion-flawed`**: (o1) unsupported motives; (o2) a population inference contradicted by the booking denominator; (o3) a cost contradiction; (o4) a vague final exhortation; (o5) no standfirst; (o6) `Bakgrund` and `Diskussion`, which label the sections instead of describing them; (o7) no ending section, the closing exhortation sitting inside the last one and naming no act.

- **In one run**, a defect is detected where the reply reports a finding that names it, or the delivered text repairs it and the reply names the repair. It is read from the two judges' answers under heading 3 of their brief. Where both judges record it as detected, or both as not, that stands. Where they split, this session reads the reply, quotes the finding or the repair it decides on, and records both judges' readings beside the call.
- **In one arm**, a defect counts as detected where at least one of that arm's two runs detects it.
- **The candidate misses the Control** only on a defect the pre-change arm detected and the candidate arm did not. A defect neither arm detected is recorded as such and is no regression.
- `C1` is recorded for every flawed run too, and a preservation clause of either row that one arm keeps and the other does not is recorded as measured.

## Whose miss

The protocol's rule applies. A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded; where they split, the rule under *When `R1` is met* decides. A standfirst changed on `article-clean`, or a premise written into `opinion-clean`, is this ticket's.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), with [`runs/inventory.sh`](runs/inventory.sh):

3. **This build's scratch root** `<scratch>`, the packets and the judges' directories among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so neither is hashed.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/041e1ba1-3ffd-418b-8405-c4d6affc600c/scratchpad/`, which other sessions of the same run also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Ship rule

The protocol's semantics for a ticket whose change is conditional on the measurement. Each half is read apart from the other.

1. **Not reproduced.** Where no pre-change run shows a half's defect, that half is recorded as not reproduced on this seat. Its text change does not ship: the final commit restores its files, and its test, to their state at `<start>`. The candidate arm is still run and recorded. One decision record, `docs/adr/0230`, records every half not reproduced, as the protocol's *Not reproduced* requires; where both halves reproduce, no decision record is written, since the change is prose in a review half that one commit reverses.
2. **Reproduced, the Target met and the Control held.** The half ships, recorded as met.
3. **Reproduced, and the Target missed or the Control regressed.** The protocol's one revise round is taken, no larger than the subset that failed: every run, in the post-change arm's numbers, of each fixture whose reading missed or whose Control regressed, against a revised candidate committed first and staged from its commit. The revise round's runs are named `rev-<fixture>-…`, listed in `runs/matrix-revise.tsv` in `matrix.tsv`'s columns, and made by the frozen `lane.sh` with that matrix as its second argument; they are judged exactly as above. After it:
   - a reproduced half ships where the revised candidate meets its Target and the Control holds;
   - otherwise it ships only where the revised candidate beats the pre-change arm on that half's Target, with fewer runs showing the defect than the pre-change arm's over the same fixture, and no Control defect the pre-change arm detected goes undetected in the revised candidate's arm; a flawed row not re-run is read from the first candidate's arm;
   - otherwise that half's product stays as it was at `<start>`, and no decision record is written for it: its defect reproduced.

The Control is read for the candidate as a whole, since both halves are in every candidate run, so a Control defect that stays undetected keeps both halves out under the second branch. Whichever way it falls, the result is written as measured.

**Filing.** Each remaining miss is filed as its own `needs-triage` issue naming #468: one issue per fixture whose Target reading missed in the arm whose wording ships, or in the candidate arm where nothing ships, and one per Control regression. A miss the whose-miss rule assigns to an open ticket is recorded under that ticket and not filed again.

## Void runs

A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; so is a run that reports a file it wrote changed or deleted under it by another process. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again, and a void judgement is kept there too. A run that completes and stops is a finding.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

## What is written

This file, the two judge briefs and the four files under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; each run's packet under `runs/<run>/`, with its `expectation.md` and its two judgements; `runs/judges.tsv` and the wave inventories under `runs/waves/`; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-468.md`, in the protocol's format. A packet's `stream.jsonl` and `transcripts/` are read for the seat, which its `trace-index.json` keeps, and are not committed. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
