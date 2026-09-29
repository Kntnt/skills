# Plan for #435: everything a reply says about a text is true of the text it names

Frozen on 2026-09-29, before the first run of either arm and before any product change. Nothing in this file, in the two judge briefs beside it or in the two inventory scripts under `runs/` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md), its section [*How an evaluation is staged*](../protocol.md#how-an-evaluation-is-staged) above all, and [the corpus](../corpus/editorial-quality/README.md) first, then [#398's plan](../editorial-398/plan.md), whose method this one copies; this file says only what that plan leaves open and what #435 settles differently.

**`<start>` is `e7773344`**, the head of the branch `kntnt-orchestrate/main/435` when the build began. The pre-change arm is staged from it. **The corpus commit is `e7773344` too.** Both arms read their inputs and the controls' frozen expectations from it. This ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-09-29: the body, the triage comment of 2026-09-28 15:07 UTC, the readiness addendum of 2026-09-28 18:48 UTC and readiness addendum 2 of 2026-09-29 08:55 UTC. Where they conflict the later one stands.

## What is under test

In [#398's evaluation](../editorial-398/results.md) judges found statements of Redline's reply false against the text outside what the reply says about the claims: a definite form called indefinite, a headline said to *stay at 52 characters* when the returned one has 56, two passages said to have *moved* when a heading was set over them, *the six unhelpful headings are gone* where one was replaced, one word naming two blocks, and a quotation placed under the wrong heading. #398 counted none of them, and filed them as #435.

The triage comment settles the behaviour, and nothing about it is conditional on this measurement: **every statement a reply makes about a text is true of the text it names**, counts, lengths, grammatical labels, where a passage stands and what a round did to a passage among them. A statement about the delivered text is checked against the delivered text after the last change to it, the closing mechanical pass included; a count or length the measuring script gives is taken from its measurement of the text the statement is about; a statement about the text as received says so; and a statement that cannot be made true is left out. The duty is written once, in a new section of `skills/kntnt/library/references/delivery.md` immediately after *The language of a report about the text*. Redline's step 11 and Unslop's step 9 point at it, Redline's step 11 says for the four anatomy genres that a count or length about the delivered text comes from step 6's measurement run on the final artifact from step 9, and both Skills' help pages say it in the reply paragraph. The candidate's exact wording is written after this plan is committed and is recorded in `results.md` with its commit.

**Unslop is changed and not measured here**, as #398 did not measure it. The shared sentence also reaches Write, Proofread and Brief, whose delivery steps follow `delivery.md`; none of them is changed or run.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent. So every Redline run, of both arms and of any revise round, is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=e7773344 \
  --invocation='<invocation from the matrix>' \
  --input=<scratch>/inputs/<input>.md --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `<start>` for the pre-change arm, the committed candidate for the candidate arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, laid out flat so that the shim finds `HERE.parent / "kntnt"`. The candidate is committed before its install is staged.
- **The inputs.** `<scratch>/inputs/<input>.md` is written once, before the first run, by `git show e7773344:<path>` of the path the matrix names. The invocation is the whole prompt; no turn file is sent.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit. That root stays under the system temporary directory and is not moved under `<scratch>`: every directory under `<scratch>` lies inside the repository checkout `/Users/thomas/Projects/skills`, and Claude Code loads each `CLAUDE.md` it finds above a session's working directory, so a run started there reads the collection's own agent guide, which no user's run of the Skill does. A probe session started under `<scratch>` on 2026-09-29 listed `/Users/thomas/Projects/skills/CLAUDE.md` among its instructions. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after both judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/435.scratch`.
- **No two runs on one input at a time** (#401). Runs on *different* inputs run side by side, at most four at once. The runs of one input — the two candidate runs on a draft, and a revise run — are made one after the other, and no candidate run starts on an input while its pre-change run is in flight.
- **The staged runner's use.** No criterion here is answered from the trace it keeps; it is used, as in #397, #398 and #402, because it is the one way from this seat to give Redline a session that can start its correction subagents.

## The matrix

The four drafts are `docs/evaluation/editorial-362/runs/{column-sv-r1,column-sv-r2,opinion-en_GB-r1,opinion-en_GB-r2}/redline/work/input.md`, copied byte for byte. Each carries its own `kntnt` map, so the invocation names no genre and no language. The ten controls are the ten rows of the corpus's *Redline controls* table, staged as the corpus says — only the linked artifact as `input.md` — with no contextual instruction and no technique. The invocations name the installed genres, `casestudy` and `webcopy`, as the corpus's table does since #443; fixture IDs, file names and run names keep their hyphens.

| Input | SHA-256 (first 16) at `e7773344` | Invocation |
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

Twelve hashes match the first 16 digits #398's plan pinned. `case-study-clean` and `opinion-clean` do not: #431 revised both rows in `8e10de0f`, before `<start>`, so both arms read the revised texts alike.

| Arm | Installed from | Runs |
| --- | --- | --- |
| pre-change | `<start>` | `pre-<draft>` once on each draft; `pre-control-<id>` once on each control: 14 runs |
| candidate | the committed candidate | `post-<draft>-a` then `post-<draft>-b` on each draft; `post-control-<id>` once on each control: 18 runs |
| revise | the committed revised candidate | `revise-<input>`, only where the ship rule below calls for it: each input it names, as many runs as that input has in the candidate arm |

Thirty-two Redline invocations and sixty-four judgements before any revise round. This table is exhaustive.

**A clean control is run once, to the response, not as the protocol's response-target and file-target pair.** This is a declared narrowing. The file-target run exists to answer `R1` from a delivered file, and this evaluation does not score `R1`. What it measures is whether the reply's statements are true of the text, and the frozen briefs judge a reply against `work/input.md` and `response.md` alone; a file-target run would need a third file the briefs do not name.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The draft runs are judged by [`redline-judge-brief.md`](redline-judge-brief.md), the controls by [`control-judge-brief.md`](control-judge-brief.md). Both are byte copies of #398's. A control judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**, as the brief says: the row's *Frozen expectation and rejection* cell at `e7773344`, copied verbatim to the run's `expectation.md`.

**Neutral paths.** Each judge gets a directory of its own made by `mktemp -d` under the system temporary directory, whose path names neither the arm, the input, the run nor this ticket, holding `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`, and nothing else. A directory under `<scratch>` would name this ticket's number in its path, which the protocol's *Blind paths* forbids. The judge writes `judgement-<letter>.md` there and keeps any scratch of its own there. The judgement is copied into the run's directory as `judgement-a.md` or `judgement-b.md`, the mapping from directory to run is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. The two judges of one run are dispatched together and are not told of each other.

## Criteria, fixed before the runs

### `A2`, and how a miss is read

`A2` is #398's: *a judge finds no statement false against the returned text, and no kind of difference the account leaves uncovered.* Neither brief names it. **A judge records an `A2` miss** where its judgement, under any heading, calls a statement of the reply false, inaccurate, imprecise, loose or misleading against a text, or records under heading 2 a difference that the reply does not report or reports inaccurately.

**Every such miss is read**, and each is put in exactly one of four classes. `results.md` records each one with its run, its judge and its class, quoting the reply and the judge.

1. **A claim-account miss.** The miss is about what the run did to a claim: an entry of the itemised account of removed, changed or added claims; a claim-changing difference that the account leaves out or misreports; or the sentence about the claims as a whole. These are the Control's, not the Target's.
2. **A counted miss outside the claim account.** A statement of the reply about a text, not in class 1, that asserts something the text it names contradicts. The Target counts these. Statements about the text as received are read against `work/input.md`, and all others against the returned text. The judge's word does not decide the class; what decides it is whether the text contradicts what the statement says. *The six unhelpful headings are gone* counts, although its judge called it loose, because one of the six was replaced rather than removed. A finding's description, an anatomy remark, a count, a length, a grammatical label, where a passage stands, and what a round did to a passage — *moved*, *removed*, *replaced*, *given a heading* — are all in scope.
3. **Recorded, not counted.** The statement is true of the text it names, and the judge faults only what it might suggest. The *med mellanrum* / *med mellanslag* note on a dash that comes back spaced is in this class.
4. **An omission.** A difference that no statement of the reply reports. It is not a false statement, so it is recorded and not counted here.

**Split judges.** One judge is enough to put a miss in a run, as in #398's plan.

### Whose miss

The protocol's whose-miss rule applies, with the tickets that are open when this plan is frozen and whose behaviour a run of these inputs can show: **#429** (a working heading rewritten as if the headline rules made it a finding), **#432** (`web-copy-clean`'s heading fact copied into the body, and a missing form link reported as a defect) and **#433** (the correction agent's headings that repeat what they stand over, and a whole-round rejection discarding `opinion-flawed`'s ending section with them). A closed ticket takes no miss: #397, #398, #399, #400, #402, #415, #430 and #431 are closed, and #398 and #400, the tickets filed against the claim account, take no class 1 miss.

- **Class 2** is this ticket's whatever part of the text the statement is about and whatever change it describes, anatomy remarks among them. Where the change a false statement describes is an open ticket's behaviour — a working heading rewritten, which #429 owns — the change is recorded under that ticket and the false statement still counts here.
- **Classes 1, 3 and 4** are recorded under the open ticket that carries them. A class 1 or class 4 miss that no open ticket carries is filed as the ship rule says.

### The Target and the Control

- **Unit.** The unit is the run. A run *carries a counted miss* where either judge records at least one class 2 miss in it. An arm's figure is the share of its runs that carry one: of 14 in the pre-change arm and of 18 in the candidate arm. The number of distinct class 2 statements per run is also recorded, and not scored.
- **Reproduced.** The pre-change arm reproduces the fault where at least one of its runs carries a counted miss.
- **Target.** The candidate arm's share is lower than the pre-change arm's, and no candidate run carries a class 2 miss about the delivered text that is a count, a length, a grammatical label, where a passage stands, or what a round did to a passage.
- **Control.** Matched per input and per kind. There are four kinds: the sentence about the claims as a whole, a removed claim, a changed claim and an added claim, each kind covering both a claim the account leaves out and one it misreports. The Control is missed on an input where a candidate run on it carries a class 1 miss of a kind that no pre-change run on that input carries. A class 1 miss the whose-miss rule assigns to another open ticket is not counted.

### Also on every run

- **`O1`**, from the runner's before-and-after inventories and the wave inventories.
- **`S1`**: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.
- **`R1`** on the drafts and **`C1`** on the controls, as the judges give them under heading 4. Recorded, not scored.

`A1`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `A2`, `O1` and `S1` as this evaluation's criteria.

## Inventory scope

Scopes 1 and 2 — the run's working directory, its staged install and its scratch — are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), which is #398's with this build's paths, calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #398's:

3. **The rest of this build's scratch root**, the other runs' packets among them.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/e1c56c23-fb82-46cd-bafe-65bb6c439e91/scratchpad/`, which sibling builds also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## What ships

The ticket's readiness addendum states the ship semantics outright, and they are not conditional on this measurement:

1. **The `delivery.md` change and the Skill changes ship in every outcome**: a met Target, a Target or Control missed after the revise round, and a pre-change arm that shows no counted miss. Nothing is reverted and **no decision record is written**.
2. **The measurement is met once the evaluation has been run under this plan and recorded.** The Target and the Control are what the result is read against, not conditions the build must meet.
3. **One revise round, at most, decides only which wording ships.** Where the candidate misses the Target or the Control, one round is run on the inputs whose candidate runs carry a class 2 miss or a Control miss, against a revised candidate committed first, each such input getting as many runs as it has in the candidate arm. Where no input carries either, no round is run. The Target and the Control are then read over the revised runs in place of the first candidate's runs on those inputs. If the revised candidate meets both, it ships. If it does not, the wording ships that has the lower share of runs carrying a class 2 miss over the revised inputs, comparing the first candidate's runs on those inputs with the revised runs; on a tie the first wording ships.
4. **Whichever way it falls**, the result is written as measured, and each remaining miss — every class 2 miss of the shipped wording's runs, and every class 1 or class 4 miss no open ticket carries — is filed as its own `needs-triage` issue naming #435.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its input is run again. A run that completes and stops is a finding.

## What is written

This file, the two judge briefs and the two inventory scripts, committed before the first run; `results.md` beside them with the outcome whichever way it falls, naming every Skill whose delivery step follows `delivery.md` and which of them were measured; the judged packets under `runs/`, each with `expectation.md` for a control and `judgement-a.md` and `judgement-b.md`, with `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-435.md`, in the protocol's format, dated the day the runs were made. Its line for `../records/README.md` is written to the build's note file and appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
