# Plan for #475: Redline's reply is checked against both texts by a reader that did not write it

Frozen on 2026-09-30, before the first run of either arm. Nothing in this file, in the three judge briefs beside it or in the scripts and the matrix under `runs/` (`inventory.sh`, `wave_inventory.sh`, `lane.sh`, `matrix.tsv`) is edited after the first run; `results.md` and the rest of the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md), its section [*How an evaluation is staged*](../protocol.md#how-an-evaluation-is-staged) above all, and [the corpus](../corpus/editorial-quality/README.md) first, then [#435's plan](../editorial-435/plan.md), which this one copies with paths and the seat substituted, except where #475's thread replaces a part of it; this file says which.

**`<start>` is `41fd4c55`**, the commit the build starts from, and the pre-change arm is staged from it. **The corpus commit is `41fd4c55` too.** Both arms read their inputs and the controls' frozen expectations from it. Nothing in the corpus or in #362's inputs has changed since `e7773344`, the corpus commit of #435's plan: every input's digest below matches the one #435's plan pinned.

**The candidate is `29d4b674`**, committed on the branch `kntnt-orchestrate/main/475` before this plan and before any install was staged. Its diff touches `skills/editorial/redline/SKILL.md`, `skills/editorial/redline/help.md`, the new `skills/editorial/redline/references/reply-check.md`, `skills/kntnt/catalog.json` and `tests/test_kntnt.py`, and nothing else.

The requirement is the ticket's thread as it stood on 2026-09-30: the body, the readiness addendum of 2026-09-30 14:10 UTC and readiness addendum 2 of 2026-09-30 14:16 UTC. Where they conflict the later one stands.

## What is under test

[#435's evaluation](../editorial-435/results.md) left 9 of its 18 shipped-reading runs carrying either a statement that the text it names contradicts, or a claim-account entry that leaves out or misstates part of what a change did to a claim. #435 filed them as #451–#462, and each is closed as folded into #475. Every one breaks a duty Redline's step 11 already states. More wording is unlikely to close what is left; what found those misses was a reader comparing the two texts fresh.

The candidate changes one thing about how Redline delivers. Once step 9 has produced the final Text Artifact and the reply is drafted, and before anything is delivered, step 11 starts one fresh subagent from `references/reply-check.md`. It is given the text as it arrived, the delivered text, the drafted reply, two Library paths for the duties it applies (`delivery.md`'s *The truth of a report about the text*, and `base.review.md`'s claim-account sentences), and, for `article`, `casestudy`, `column` and `opinion`, the full output of step 6's measuring command run on the delivered text. It returns two lists: every statement of the reply that the text it names contradicts, and every difference between the two texts that moves a claim and that the claim account leaves out or reports short of what it did. The run corrects the reply alone from them; the delivered text is unchanged by it, and the check is made once. It runs on every run whose reply says anything about a text, which is every run except one returning only the short no-change status. The Help page's reply paragraph says so.

**The change is conditional on this measurement.** It ships only as *The Target, the Control and what ships* below says.

**Unslop is not changed and not run.** It carries the same claim account and is out of #475's scope.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent. So every Redline run, of both arms and of any revise round, is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree by [`runs/lane.sh`](runs/lane.sh), which is #429's with this build's paths:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=41fd4c55 \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<scratch>/inputs/<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents, its checker and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `<start>` for the pre-change arm, the committed candidate `29d4b674` for the candidate arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, laid out flat so that the shim finds `HERE.parent / "kntnt"`. A revised candidate is committed before its install is staged.
- **The inputs.** `<scratch>/inputs/<input>` is written by `git show 41fd4c55:<path>` of the path the matrix names, never read from a working tree. The invocation is the whole prompt; no turn file is sent.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other. It copies the delivered `work/output.md` into the packet as `captured-output.md`.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit. That root is not moved under `<scratch>`: every directory under `<scratch>` lies inside the repository checkout `/Users/thomas/Projects/skills`, and Claude Code loads each `CLAUDE.md` it finds above a session's working directory, so a run started there would read the collection's own agent guide, which no user's run of the Skill does. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after both judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/475.scratch`.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) assigns every run to one of seven lanes, A to G, and `lane.sh` makes a lane's runs one after the other. Every run of one input is in one lane, so no two runs on one input are in flight at once (#401), and at most seven runs are in flight at any time. Within a lane the two arms alternate on each input, so neither arm has the service to itself at another hour. A run whose packet exists is not made again.
- **The staged runner's use.** No criterion here is answered from the trace it keeps; it is used because it is the one way from this seat to give Redline a session that can start its correction subagents and its checker.

## The matrix

The four drafts are `docs/evaluation/editorial-362/runs/{column-sv-r1,column-sv-r2,opinion-en_GB-r1,opinion-en_GB-r2}/redline/work/input.md`, copied byte for byte. Each carries its own `kntnt` map, so the invocation names no genre and no language. The ten controls are the ten rows of the corpus's *Redline controls* table, staged as the corpus says — only the linked artifact as `input.md` — with no contextual instruction and no technique. The invocations name the installed genres, `casestudy` and `webcopy`, as the corpus's table does; fixture IDs, file names and run names keep their hyphens.

| Input | SHA-256 (first 16) at `41fd4c55` | Invocation |
| --- | --- | --- |
| `column-sv-r1` | `4fe7a78864930951` | `/redline --output=response input.md` |
| `column-sv-r2` | `74b966f1352c4f42` | `/redline --output=response input.md` |
| `opinion-en_GB-r1` | `02171183566bb9a1` | `/redline --output=response input.md` |
| `opinion-en_GB-r2` | `cfefda44d50dcb42` | `/redline --output=response input.md` |
| `article-clean` | `f183e6da31cf7808` | `/redline --genre=article --language=sv --output=response input.md` |
| `article-flawed` | `1c0e3b3ef98e06b2` | `/redline --genre=article --language=sv --output=response input.md` |
| `case-study-clean` | `1457480f3e7e3066` | `/redline --genre=casestudy --language=sv --output=response input.md` |
| `case-study-flawed` | `ce574061bd09328e` | `/redline --genre=casestudy --language=sv --output=response input.md` |
| `column-clean` | `98b65197fa9dd800` | `/redline --genre=column --language=sv --output=response input.md` |
| `column-flawed` | `9b12ad3fb2cb7401` | `/redline --genre=column --language=sv --output=response input.md` |
| `opinion-clean` | `141efb2a4a3b9339` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `opinion-flawed` | `ab033d9f4c817c9e` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `web-copy-clean` | `8de234f1c80fe947` | `/redline --genre=webcopy --language=sv --output=response input.md` |
| `web-copy-flawed` | `a5470e4b3aea20a0` | `/redline --genre=webcopy --language=en_US --output=response input.md` |

Each of the five `*-clean` controls is also run once to a file, as the protocol's [*A clean control*](../protocol.md#a-clean-control) requires of a clean control whose `R1` is scored: its invocation with `--output=response` replaced by `--output=output.md`, a new file beside the input.

| Arm | Installed from | Runs |
| --- | --- | --- |
| pre-change | `<start>` | `pre-<draft>-a` and `pre-<draft>-b` on each draft; `pre-control-<id>` once on each control; `pre-control-<id>-file` once on each clean control: 23 runs |
| candidate | `29d4b674` | `post-<draft>-a` and `post-<draft>-b` on each draft; `post-control-<id>` once on each control; `post-control-<id>-file` once on each clean control: 23 runs |
| revise | the committed revised candidate | `revise-<run>`, only where *The revise round* below calls for it: each input it names, as many runs as that input has in the candidate arm |

Forty-six Redline invocations and ninety-two judgements before any revise round. This table is exhaustive. `runs/matrix.tsv` lists all forty-six by lane, name, arm, revision, input and invocation.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket.

- **The briefs.** [`redline-judge-brief.md`](redline-judge-brief.md) and [`control-judge-brief.md`](control-judge-brief.md) are byte copies of #435's. [`control-judge-brief-file.md`](control-judge-brief-file.md) is a byte copy of #429's.
- **Which brief.** A draft run is judged with `redline-judge-brief.md`. A control's response-target run is judged with `control-judge-brief.md`. A clean control's file-target run is judged with `control-judge-brief-file.md`.
- **The frozen expectation.** A control judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**, as the briefs say: the row's *Frozen expectation and rejection* cell at `41fd4c55`, copied verbatim to the run's `expectation.md`. A file-target run's judge gets the same paragraph as its response-target sibling's.
- **The message.** Each judge is sent the brief's text, unchanged, the run directory, and its letter, `a` or `b`, and for a control the frozen expectation. Nothing else.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits that name neither the arm, the input, the run nor the target. It holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`; for a file-target run, also `work/output.md`, copied from `captured-output.md`. It holds nothing else, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement-<letter>.md` there, and it is copied into the run's packet as `judgement-a.md` or `judgement-b.md`. The mapping from directory to run is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. The two judges of one run are dispatched together and are not told of each other. The build's brief confines everything it writes to its working tree and `<scratch>`, so the judges' directories are under `<scratch>`, whose path carries this build's number; that number names neither the arm nor the expected verdict, the judge is told nothing of what it is, and every brief forbids reading any repository file or ticket. This is a path substitution, as #429's plan made the same one, stated here so that it can be reviewed against the protocol's *Blind paths*.

## Criteria, fixed before the runs

### `A2`, and how a miss is read

`A2` is #398's: *a judge finds no statement false against the returned text, and no kind of difference the account leaves uncovered.* Neither brief names it. **A judge records an `A2` miss** where its judgement, under any heading, calls a statement of the reply false, inaccurate, imprecise, loose or misleading against a text, or records under heading 2 a difference that the reply does not report or reports inaccurately.

**Every such miss is read**, and each is put in exactly one of four classes. `results.md` records each one with its run, its judge and its class, quoting the reply and the judge.

1. **A claim-account miss.** The miss is about what the run did to a claim: an entry of the itemised account of removed, changed or added claims; a claim-changing difference that the account leaves out or misreports; or the sentence about the claims as a whole. A difference that moves a claim and that no statement of the reply reports is class 1, because the claim account leaves it out, a sense or double sense lost among them.
2. **A counted miss outside the claim account.** A statement of the reply about a text, not in class 1, that asserts something the text it names contradicts. Statements about the text as received are read against `work/input.md`, and all others against the returned text. The judge's word does not decide the class; what decides it is whether the text contradicts what the statement says. *The six unhelpful headings are gone* counts, although its judge called it loose, because one of the six was replaced rather than removed. A finding's description, an anatomy remark, a count, a length, a grammatical label, where a passage stands, and what a round did to a passage — *moved*, *removed*, *replaced*, *given a heading* — are all in scope.
3. **Recorded, not counted.** The statement is true of the text it names, and the judge faults only what it might suggest. The *med mellanrum* / *med mellanslag* note on a dash that comes back spaced is in this class.
4. **An omission.** A difference that moves no claim and that no statement of the reply reports. It is not a false statement, so it is recorded and not counted here.

**Split judges.** One judge is enough to put a miss in a run, as in #398's and #435's plans.

**Which runs count.** The Target is read over the eighteen response-target runs of each arm: the eight draft runs and the ten controls' `--output=response` runs. A file-target run's `A2` misses are read and classed like any other, and recorded, not counted.

### Whose miss

The protocol's whose-miss rule applies, with the tickets that are open when this plan is frozen and whose behaviour a run of these inputs can show: **#463** (`case-study-clean`'s headline rewritten as an overclaim the standfirst under it already bounds), **#464** (a subheading added over `column-clean`'s ending) and **#468** (a clean text changed over a loss no reader suffers, a supported judgement dropped or an unstated premise written in). A closed ticket takes no miss: #429, #432, #433, #435 and #451–#462 are closed.

- **Class 1 and class 2 misses are this ticket's**, whatever part of the text the statement is about and whatever change it describes. Where the change a false or short statement describes is an open ticket's behaviour, the change is recorded under that ticket and the false or short statement still counts here.
- **Classes 3 and 4** are recorded under the open ticket that carries them. A class 4 miss that no open ticket carries is filed as *What ships* says.
- **A C1 failure** caused by a change another open ticket owns is recorded under that ticket and is not a Control miss.

### `C1`

`C1` is the control judge's heading-4 verdict, labelled `R1` in `control-judge-brief.md` and `control-judge-brief-file.md`. A control passes `C1` in an arm where both judges pass it, and fails where either fails.

- **A clean control's `C1`** is read from its file-target run, whose judges read `work/output.md`, the file that run delivered.
- **A flawed control's `C1`** is read from its response-target run.

### The Target, the Control and Reproduced

- **Unit.** The unit is the run. A run *carries a miss* where either judge records a class 1 or class 2 miss in it. An arm's figure is the share of its eighteen response-target runs that carry one. The number of distinct class 1 and class 2 misses per run is also recorded, and not scored.
- **Reproduced.** The pre-change arm reproduces the fault where at least one of its runs carries a class 1 or class 2 miss.
- **Target.** The candidate arm's share is at most half the pre-change arm's share, and no candidate run carries a class 2 miss that is a count or a length.
- **Control.** No control that passed `C1` in the pre-change arm fails it in the candidate arm, save a failure *Whose miss* assigns to another open ticket.

### Also on every run

- **`O1`**, from the runner's before-and-after inventories and the wave inventories. For a file-target run, the one file created beside the input, `output.md`, is the effect that was asked for.
- **`S1`**: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.
- **`R1`** on the drafts, as the judges give it under heading 4. Recorded, not scored.
- **The checker.** Whether a candidate run started the checker, read from its `trace-index.json` and transcripts. Recorded, not scored.

`A1`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `A2`, `C1`, `O1` and `S1` as this evaluation's criteria.

## The revise round

**It is taken whenever the Target or the Control is missed**, once and no more. It runs, against a revised candidate committed first, on two sets of inputs:

- the inputs whose candidate response-target runs carry a class 1 or class 2 miss;
- every control whose `C1` was missed in the candidate arm.

Each such input gets as many runs as it has in the candidate arm, a clean control its response-target and its file-target run. Both the Target and the Control are then read over the revised runs, in place of the first candidate's runs on those inputs.

## What ships

1. **Not reproduced.** Where no pre-change run carries a class 1 or class 2 miss, the result is recorded as not reproduced, the candidate is reverted so that the product stays as it was at `<start>`, and a decision record is written under the reserved number `0235`.
2. **Met.** Where the candidate meets the Target and the Control, on its first reading or after the revise round, the candidate that met them ships.
3. **The fallback.** Where the revise round has been taken and the Target is still missed, the protocol's *One revise round* asks whether the candidate *beats the pre-change arm on the target criterion*. This evaluation reads *beats* as the same halving: the revised reading's share is at most half the pre-change arm's. Where it is, and the Control is met, the revised candidate ships. Otherwise the candidate is reverted and the product stays as it was. A gain inside run-to-run variation does not pay for a subagent on every run, so a smaller gain ships nothing.
4. **A decision record where the halving is missed** is written only where `docs/rules/docs.md`'s criteria for a record hold, and the commit that records the result says which way they fell.
5. **Whichever way it falls**, the result is written as measured, and each remaining miss — every class 1 and class 2 miss of the candidate reading that ships or, where nothing ships, of the pre-change arm, and every class 4 miss no open ticket carries — is filed as its own `needs-triage` issue naming #475.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its input is run again. A run that completes and stops is a finding.

## Inventory scope

Scopes 1 and 2 — the run's working directory, its staged install and its scratch — are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), which is #435's with this build's paths, calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #435's:

3. **The rest of this build's scratch root**, the other runs' packets among them.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/041e1ba1-3ffd-418b-8405-c4d6affc600c/scratchpad/`, which the orchestrating session and sibling builds also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## What is written

This file, the three judge briefs, the two inventory scripts, `lane.sh` and `matrix.tsv`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; the judged packets under `runs/`, each with `expectation.md` for a control and `judgement-a.md` and `judgement-b.md`, with `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-475.md`, in the protocol's format, dated the day the runs were made. Its section for `../records/README.md` and the changelog entry are written to the build's note file and applied by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
