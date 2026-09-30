# Plan for #464: a closing proposal is an ending

Frozen on 2026-09-30, before the first run of either arm. Nothing in this file, in the two judge briefs beside it, or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#429's plan](../editorial-429/plan.md), from which this one copies four things and nothing else: the two control briefs, the split rule, the runner and turn files, and void-run handling. The run table, the target, the control and the exit are written fresh from #464.

**`<start>` is `41fd4c55`**, the head of the branch `kntnt-orchestrate/main/464` when the build began. The pre-change arm is staged from it. **The candidate is `131c5c39`**, committed before this plan, and the post-change arm is staged from it. **The corpus commit is `41fd4c55`.** Every input and every frozen expectation is read from it; this ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-09-30: the body, the triage comment of 2026-09-30 14:01 UTC and the readiness addendum of 2026-09-30 14:10 UTC. Where they conflict, the later one stands.

## What is under test

The anatomy's rule that an ending is a section of its own stands; what changes is the test that tells an ending from a section that carries the argument. The change is conditional on this measurement: the ticket carries no maintainer ruling on the wording, so the protocol's *Not reproduced* and *One revise round* apply as written.

The candidate, `131c5c39`, changes the last paragraph of *Ending* in `skills/kntnt/library/references/editorial/article-anatomy.md`, the base half that Write, Redline and Redline's correction agents all load, and adds to it:

- stating the recommendation or proposal the text has built towards is closing content, even where the last section is the first place the text states it in full, and so are the writer's own reservation about it and the call to try or adopt it;
- what makes a section carry the argument is reasons or evidence the conclusion rests on that no earlier section gave;
- a last section that states the proposal, admits a doubt about it and asks the reader to act on it brings none, and is the ending.

Both sentences the #402 test pins stay: *opens no new line of argument* and *a section that carries the argument with a closing line appended is not an ending*. `article-anatomy.review.md` is not changed: it repairs closing content by a section of its own only *where the closing content stands inside a last section that carries the argument*, and it reads an ending *by the anatomy's test*, so it inherits the new test and its repair keeps its force. The candidate also rewords the module docstring of `skills/kntnt/library/scripts/article_anatomy.py`, the one paraphrase of the test outside the anatomy, adds `test_the_anatomy_counts_the_proposal_its_reservation_and_its_call_as_closing` to `tests/test_kntnt.py`, seen failing against `41fd4c55`'s wording, and regenerates `skills/kntnt/catalog.json`. No wording names or quotes a corpus fixture.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

Every Redline run of both arms, and of any revise round, is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) by [`runs/lane.sh`](runs/lane.sh), a copy of #429's with only its scratch path and its corpus commit substituted, which runs this command from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=41fd4c55 \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **`<commit>`** is `41fd4c55` for the pre-change arm, `131c5c39` for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own and installs them as the session's Skills, so the run's Proofread dependency is met by the Proofread staged beside Redline.
- **`<input>`** is the corpus control the matrix names, written from `41fd4c55` with `git show` into `<scratch>/inputs/`, never read from a working tree.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other. It copies the delivered `work/output.md` into the packet as `captured-output.md`.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/464.scratch`, this build's scratch directory. The packet, which is what survives a run, is written there.
- **The seat.** `claude-opus-5-5` at high deliberation, requested in `run.json` and recorded for the session and every nested agent in `trace-index.json`. The correction subagents and the nested Proofread pass run inside the session and take its seat. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **The private root.** The run's `HOME`, working directory, temporary directory and caches are made by `mkdtemp` under the system temporary directory and removed by the runner on every exit. The runner strips every `CLAUDE_*` variable, so no run has a session scratchpad; no fault under test lives in one.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) assigns every run of one input to one lane: `column-clean` to lane `C`, `opinion-flawed` to lane `G`. `lane.sh` makes a lane's runs one after the other, so no two runs of one input are in flight at once (#401), and at most two runs are in flight at any time. Within a lane the two arms alternate. A run whose packet exists is not made again.

## The run table

The table is the triage comment's, and it is exhaustive. Both arms run every row. `runs/matrix.tsv` lists all sixteen runs by name, lane, revision, input and invocation.

| Input | Invocation | Runs per arm | Run names | Judged by |
| --- | --- | --- | --- | --- |
| `column-clean` | `/redline --genre=column --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs | `<arm>-column-clean-resp-<n>`, `<arm>-column-clean-file-<n>` | two judges per run |
| `opinion-flawed` | `/redline --genre=opinion --language=sv --output=response input.md` | two | `<arm>-opinion-flawed-<n>` | two judges per run, `control-judge-brief.md` |

`<arm>` is `pre` or `post`. Each input is the corpus's `controls/<row>.md`, copied to `input.md`, and nothing else is in the working directory. No run has a contextual instruction or a technique. A pair is one response-target run and one file-target run, as the protocol's *A clean control* defines them.

That is eight runs per arm, sixteen before any revise round, and thirty-two judgements.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The two judges of one run are dispatched together and are not told of each other.

- **The briefs.** [`control-judge-brief.md`](control-judge-brief.md) and [`control-judge-brief-file.md`](control-judge-brief-file.md) are byte copies of #429's.
- **Which brief.** A response-target clean-control run and a flawed-control run are judged with `control-judge-brief.md`. A file-target clean-control run is judged with `control-judge-brief-file.md`.
- **The message.** A judge's message is its brief verbatim, a line `---`, a line naming the run directory, and a line giving its letter, `a` or `b`. It then carries one paragraph headed **Frozen expectation**: the row's *Frozen expectation and rejection* cell in the corpus README at `41fd4c55`, copied verbatim, which is also written to the run's `expectation.md`. Nothing else is added. No hint of the defect under investigation appears in any invocation, any brief or any message.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits that name neither the arm, the input, the run nor the target. It holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`; for a file-target run, also `work/output.md`, copied from `captured-output.md`. It holds nothing else. The judge writes `judgement-<letter>.md` there, and it is copied into the run's packet as `judgement-a.md` or `judgement-b.md`. The mapping from directory to run is kept in `runs/judges.tsv`. `<scratch>`'s path carries this build's number, which names neither the arm nor the expected verdict; the judge is told nothing of what it is, and every brief forbids reading any repository file or ticket. This is the same path substitution #429's plan states.

A response-target entry that returned only a no-change status has its `R1` scored `skipped`, with the reason the protocol gives: no text was delivered, and the file-target entry answers the criterion. A file-target run that leaves no `output.md` is recorded as delivering none, with its `R1` `skipped` for that reason; that is a defect, filed as its own issue.

## Criteria, fixed before the runs

- **`R1`**, on every `column-clean` run.
- **`C1`**, on every run: the run meets its row's frozen expectation, on `R1`, read against the row as `41fd4c55` leaves it.
- **`O1`**, on every run, from the runner's before-and-after inventories.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

`A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `R1`, `C1`, `O1` and `S1` as this evaluation's criteria. No criterion here is answered from the Harness trace.

### When `R1` is met

As #429's plan: a run meets `R1` when both judges pass it, and misses it when both fail it. Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary; in that case both readings are recorded and the run meets `R1`. `C1` is read by the same rule.

## Reading the target

- **A run adds a heading or splits the last section** when the text it delivered — the file-target run's `output.md`, or a text a response-target run delivered in its reply — holds a headline or subheading line that the input does not, or when the paragraphs of the input's last section, `Ännu en ruta, och ändå vill jag prova`, no longer stand together under one subheading. This session compares the heading lines and the last section mechanically. A response-target run that returned only the no-change status delivered no text and adds nothing.
- **Target:** no candidate run of `column-clean` adds a heading line or splits its last section.
- **Reproduced:** at least one pre-change run of `column-clean` does.
- **Not reproduced.** Where no pre-change run does, the result is recorded as not reproduced on this seat.

Any other heading difference, and every other difference in a delivered text, is recorded as measured, with the judges' classes and `R1`, and is not counted for or against the target. A miss the whose-miss rule assigns to another ticket is recorded under it.

## Reading the control

The control is read from the judges' answers under heading 3 of their brief, under the split rule.

- **A run of `opinion-flawed` passes** where the judges' heading-3 answers record that its closing content was given a section of its own, or that the reply reports the missing ending section, as the row's clause *no ending section, the closing exhortation sitting inside the last one and naming no act* requires.
- **An arm passes** where every run of `opinion-flawed` in that arm passes.
- **The candidate misses the control** only where the pre-change arm passed it and the candidate arm does not.

`C1` is recorded on every run too, and every other clause of the row is recorded as the judges answer it, and counts neither for nor against the control.

## Whose miss

The protocol's rule applies. A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded; where they split, the rule under *When `R1` is met* decides. A subheading added over `column-clean`'s ending, or its last section split, is this ticket's miss.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), a copy of #429's with only its paths substituted, with [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #429's:

3. **This build's scratch root** `<scratch>`, the packets and the judges' directories among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so neither is hashed.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/041e1ba1-3ffd-418b-8405-c4d6affc600c/scratchpad/`, which other sessions of the same run also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Exit

The ticket makes the change conditional on this measurement, so the protocol's semantics for that case apply as written.

1. **Not reproduced.** Where no pre-change run adds a heading line to `column-clean` or splits its last section, the candidate arm is still run and recorded, no product change ships, the candidate's change is reverted in the build's last commit, and a decision record, ADR-0229, records the non-reproduction.
2. **Reproduced, the target met and the control held.** The candidate ships.
3. **Reproduced, and the target missed or the control missed.** The protocol's one revise round may be taken, no larger than the subset that failed: every run, in the post-change arm's run names, of `column-clean` where the target missed, and of `opinion-flawed` where the control missed, against a revised candidate committed first and staged from its commit. The revised candidate ships if it meets the target and holds the control. Otherwise it ships only if it beats the pre-change arm on the target — fewer candidate runs than pre-change runs that add a heading line to `column-clean` or split its last section — and the control holds; where two candidates both qualify, the one with fewer target misses ships, or the first where they are level. Where none qualifies, the product stays as it was, and the build's last commit reverts the change.

Where the candidate ships, no decision record is written: the change is prose in a base half that one commit reverses, so it fails the first of `docs/rules/docs.md`'s three criteria; `results.md` says so.

**Filing.** Each remaining miss is filed as its own `needs-triage` issue naming #464. A miss the whose-miss rule assigns to an open ticket is recorded under that ticket and not filed again.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; so is a run that reports a file it wrote changed or deleted under it by another process. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again, and a void judgement is kept there too. A run that completes and stops is a finding.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

## What is written

This file, the two judge briefs and the four files under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; each run's packet under `runs/<run>/`, with its `expectation.md` and its two judgements; `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-464.md`, in the protocol's format. A packet's `stream.jsonl` and `transcripts/` are read for the seat, which its `trace-index.json` keeps, and are not committed. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
