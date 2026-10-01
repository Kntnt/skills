# Plan for #477: the reply goes out as the checker read it

Frozen on 2026-10-01, before the first Redline run of either arm. Nothing in this file, in the two judge briefs beside it, in `inputs/`, in `expectations/`, or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/inventory.sh`, `runs/wave_inventory.sh` and `runs/states.py` is edited after the first run; `results.md` and the rest of the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md), its section [*How an evaluation is staged*](../protocol.md#how-an-evaluation-is-staged) above all, [the corpus](../corpus/editorial-quality/README.md), and [#475's plan](../editorial-475/plan.md), whose run method this one copies with paths and the seat substituted, except where it says otherwise below.

**`<start>` is `fb169087`**, the commit this build started from. The pre-change arm is staged from it. **The corpus commit is `fb169087` too**: `case-study-clean` and its frozen expectation are read from it. The corpus revised that control's headline in `e2e65c40`, after #475's runs and before `<start>`, so its text is not the one #475 ran; it is used here as the corpus holds it, unchanged by this build. The two contrast fixtures under [`inputs/`](inputs/) are read from the commit that freezes this plan.

**The candidate is `51777db2`**, committed on the branch `kntnt-orchestrate/main/477` before this plan and before any install was staged. Its diff touches `skills/editorial/redline/references/reply-check.md`, `skills/editorial/redline/help.md`, `skills/kntnt/catalog.json` and `tests/test_kntnt.py`, and nothing else.

The requirement is the ticket's thread as it stood on 2026-10-01: the body, and the triage comment of 2026-10-01 11:15 UTC, which stands where the two differ.

## What the diagnosis found

[`diagnosis/README.md`](diagnosis/README.md) holds it, made before this plan. In #475's `post-control-case-study-clean` the draft the reply checker read said, truly, that the note does not credit the software with the difference. The checker named two other statements of the same finding. The run then wrote the reply again — 24 of the 32 sentences no item named came back reworded, and a sentence the checker never read was added — and in that rewrite the sentence about the note became one saying the note states outright that the software did not cause the difference. The delivered reply is not checked again. The fault arose after the check and not in the checker's reading.

## What is under test

`reply-check.md`'s section *What you do with what it returns* gains that the run corrects only what an item calls for; that a statement an item names changes in what the item says is false and keeps the rest as drafted — what it says a text does, who says it there, and how certainly; and that every sentence no item names goes to the reader in the draft's words, with nothing about either text added beyond what an item calls for. The Help page's sentence on the check says the rest of the reply goes out as the checker read it. The checker's own brief, the check's place in step 11, the single check, the Correction Budget and the text are unchanged.

**The change is conditional on this measurement.** It ships only as *What ships* says.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent, so every Redline run is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree by [`runs/lane.sh`](runs/lane.sh):

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=<input commit> \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<scratch>/inputs/<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents, its reply checker and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `fb169087` for the pre-change arm, the committed candidate `51777db2` for the candidate arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own.
- **The inputs.** `<input commit>` is `fb169087` for `case-study-clean`, and for a contrast fixture the commit that last wrote it, which is the commit that freezes this plan; `lane.sh` logs which. Each input is written into `<scratch>/inputs/` with `git show`, never read from a working tree. The invocation is the whole prompt; no turn file and no contextual instruction is sent.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other.
- **Where runs execute.** As in #475's plan: a private root under the system temporary directory, made and removed by the runner, so that no run reads this repository's agent guide. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/477.scratch`. A packet is copied into this evaluation's `runs/<run>/` after its judges have written.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) puts every run of one input in one lane, A, B or C, and `lane.sh LANE ARM` makes one lane's runs of one arm one after the other, so no two runs of one input are in flight at once (#401) and at most three runs are in flight at any time. A run whose packet exists is not made again.
- **The trace.** The checker's input and return are read from the trace the runner keeps, which is what the states below and the correction judges rest on.

## The fixtures

| Input | SHA-256 (first 16) | Invocation | Runs per arm |
| --- | --- | --- | --- |
| `case-study-clean`, the corpus control, unchanged | `2e4ef2fd4b7c03aa` | `/redline --genre=casestudy --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs: `<arm>-case-study-clean-resp-<n>` and `<arm>-case-study-clean-file-<n>` |
| [`withheld-overclaim`](inputs/withheld-overclaim.md) | `5d8de4ff16fcfd05` | `/redline --genre=casestudy --language=sv --output=response input.md` | three: `<arm>-withheld-overclaim-<n>` |
| [`denied-overclaim`](inputs/denied-overclaim.md) | `17b2063a68e868b3` | `/redline --genre=casestudy --language=sv --output=response input.md` | three: `<arm>-denied-overclaim-<n>` |

**The contrast fixtures** are `case-study-clean` at `fb169087` with one sentence changed in `withheld-overclaim` and two in `denied-overclaim`, and nothing else; both measure as conforming to the anatomy.

- **`withheld-overclaim`** keeps the note's sentence as the control has it — *Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran*, a withheld attribution — and writes into the lead a causal claim the text does not carry: *Vad det krävde går att följa i gruppens egna anteckningar, och loggen kortade tiden från anmälan till tilldelning med en arbetsdag.* A run has to find the claim, and the finding has to say what the note does, which is where the historical statement was made.
- **`denied-overclaim`** carries the same lead and changes the note's sentence to an explicit denial of the cause: *Perioderna hade olika arbetsbelastning, och enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden.* Here a reply saying the note rules the software out is true, and one saying the note leaves the cause open is false.

Together with `case-study-clean`, which withholds the attribution and asserts no cause, they separate a withheld attribution from an explicit denial and from a real unsupported causal claim. No criterion asks for any wording: a reply passes on any wording true of the text it names.

**The frozen expectations** are in [`expectations/`](expectations/): `case-study-clean.md` is the row's *Frozen expectation and rejection* cell at `fb169087`, verbatim, and the other two were written for this plan.

## The arms, and their order

| Arm | Installed from | Runs |
| --- | --- | --- |
| pre-change | `fb169087` | the twelve `pre-*` rows of the matrix |
| candidate | `51777db2` | the twelve `post-*` rows, only where the pre-change arm reproduced the fault |
| revise | the committed revised candidate | `revise-<run>`, only where *The revise round* calls for it |

**The pre-change arm runs first, alone**, and is judged and read before any candidate run is made. *Reproduced* below is read from it alone, and the candidate arm is run only where it holds. Where the fault does not show in the pre-change arm, the product stays as it was whatever a candidate arm would show, so a candidate arm would measure nothing the ship rule can use. The two arms are then made some hours apart, on the same seat and the same inputs; `results.md` records when each was made.

## The states of a reply

[`runs/states.py`](runs/states.py) writes, for every run, the states its reply passed through into `runs/<run>/states/`, each read from the packet and its trace: the text received, the two texts and the drafted reply as the checker was handed them, the checker's return, the delivered reply without its text, the delivered text, and `states.json`, which says whether a checker ran and whether the delivered text is byte for byte the text the checker was handed as delivered. The drafted reply, the checker's return and the delivered reply are thereby kept apart for every run that has a checker.

## Judging

Every judge is a fresh `kntnt-opus-high` subagent, blind to the arm, the model, this ticket and the expected verdict.

- **Reply judges.** Two per run, with [`judge-brief.md`](judge-brief.md). Each gets a directory `<scratch>/j/<token>/` holding `work/input.md` (the packet's `supplied-input.md`), `response.md` (its `response.txt`) and, for a file-target run, `work/output.md` (its `captured-output.md`). The message carries the brief's text unchanged, the directory, the judge's letter and the fixture's frozen expectation as one paragraph headed **Frozen expectation**, a file-target run's being its response-target sibling's.
- **Correction judges.** Two per run whose `states.json` records a checker, with [`transition-judge-brief.md`](transition-judge-brief.md). Each gets a directory `<scratch>/j/<token>/` holding `input.md` (`states/received.md`), `delivered.md` (`states/checked-delivered.md`), `draft.md` (`states/draft-reply.md`), `check.md` (`states/check-return.md`) and `response.md` (`states/final-reply.md`). The message carries the brief's text unchanged, the directory and the judge's letter.
- **Neutral paths.** `<token>` is twelve random hexadecimal digits. A directory holds nothing but the files named, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The mapping is kept in `runs/judges.tsv`, each judgement is copied into the packet as `judgement-a.md` or `judgement-b.md` (reply judges) or `correction-a.md` or `correction-b.md` (correction judges), and each directory is removed once its judgement is copied. The two judges of one kind on one run are dispatched together and are not told of each other. `<scratch>`'s path carries this build's number, which names neither the arm nor the verdict; this is the same substitution #475's plan states.

## Criteria, fixed before the runs

Every reading below is made by the builder from the judges' own lines and the states, and `results.md` quotes the reply and the judge for each.

- **`T1`, a cause misreported.** A run carries a `T1` miss where either reply judge under heading 2, or either correction judge under heading 2 or 3, records as false a statement of the delivered reply about what a text says of a cause: whether it asserts one, withholds the attribution or denies it, whom it credits, or how certainly it says so. The historical statement is one: a withheld attribution reported as an explicit denial.
- **`T2`, made false after the check.** A run carries a `T2` miss where either correction judge records under heading 2 or 3 a statement of the delivered reply that is not in the draft in the same words and that the text it names contradicts; or where a statement a reply judge records under heading 2 does not stand in `states/draft-reply.md` in the same words, formatting aside, and the run had a checker.
- **Other false statements.** A statement a reply judge records under heading 2 that is neither `T1` nor `T2` stood in the draft the checker read, so the checker read it and did not name it, or no checker ran. It is recorded with that origin and is not this ticket's target.
- **`X1`, the text untouched by the check.** In every run with a checker, the delivered text is byte for byte the text the checker was handed as delivered (`states.json`).
- **`X2`, every item handled.** A run fails `X2` where either correction judge records under heading 1 an item `not handled` that it does not also find wrong about the texts.
- **`D1`, the real fault still found.** On a contrast fixture, a run passes `D1` where both reply judges record under heading 4 that the reply reports a finding naming the lead's causal claim, and fails where either does not.
- **`C1`, the clean text.** On `case-study-clean`'s file-target runs, heading 5's R1, read from the delivered `work/output.md`. A run passes where both judges pass it.
- **`O1`** and **`S1`**, as in #475's plan: side effects from the runner's inventories and the wave inventories, a file-target run's one `output.md` being the effect it asked for; and the working directory holding `input.md` alone when the session started.
- **R1** on every other run, as the judges give it under heading 5. Recorded, not scored.

**Split judges.** One judge is enough to put a miss in a run, as in #475's plan.

### Whose miss

`T1` and `T2` misses are this ticket's, whatever change the statement describes. A claim-account entry that leaves an attribution change unreported, with no false statement in it, is #478's and is recorded under it. A working file a correction round leaves behind is #476's. A clean text changed is recorded and, where no open ticket carries it, filed.

### Reproduced, the Target and the Control

- **Unit.** The run. An arm's figure is the share of its twelve runs that carry a `T1` or `T2` miss.
- **Reproduced.** At least one pre-change run carries a `T1` or `T2` miss.
- **Target.** The candidate arm's share is at most half the pre-change arm's, and no candidate run carries a `T1` miss.
- **Control.** `X1` holds in every candidate run with a checker. And of the three controls read per arm — `D1` on `withheld-overclaim`, `D1` on `denied-overclaim`, and `X2` over every run — none that passes in the pre-change arm fails in the candidate arm, a control passing in an arm where every run it is read on passes it.
- **`C1` is recorded, not a Control.** The candidate changes nothing that happens before the checker is handed the final text, and `X1` is the criterion that answers whether the reply's correction reached the text. A clean text changed is a fault of the review or the round, recorded and filed whichever arm shows it.

## The revise round

It is taken once, and only where the fault reproduced and the Target or the Control is missed. It runs, against a revised candidate committed first, on every input whose candidate runs carry a `T1` or `T2` miss or fail a control, as many runs as that input has in the candidate arm. The Target and the Control are then read over the revised runs in place of the first candidate's runs on those inputs.

## What ships

1. **Not reproduced.** Where no pre-change run carries a `T1` or `T2` miss, the result is recorded as not reproduced, no candidate arm is run, the candidate is reverted so that the product stays as it was at `<start>`, and a decision record is written under the reserved number `0232`. Nothing is claimed about the GPT family.
2. **Met.** Where the candidate meets the Target and the Control, on its first reading or after the revise round, the candidate that met them ships.
3. **The fallback.** Where the revise round has been taken and the Target is still missed, the revised candidate ships only where its share is at most half the pre-change arm's and the Control is met; otherwise the candidate is reverted.
4. **Whichever way it falls**, the result is written as measured, and every remaining miss — every `T1` and `T2` miss of the reading that ships or, where nothing ships, of the pre-change arm, every other false statement, every `X2` failure and every clean text changed that no open ticket carries — is filed as its own `needs-triage` issue naming #477, or added to the open ticket that carries it.

No criterion is softened, no frozen plan, brief, input or expectation is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its input is run again. A run that completes and stops is a finding.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #475's: the rest of this build's scratch root; this build's working tree and the main checkout `/Users/thomas/Projects/skills`, read without taking the index lock; and this build's session scratchpad `/private/tmp/claude-501/-Users-thomas-Projects-skills/7bb3980e-f903-4106-b84f-69be7f823dbe/scratchpad/`, which the orchestrating session and sibling builds also write to, so that a change there is attributed by path before it is named in any run's `side effects`.

## What is written

This file, the two judge briefs, `inputs/`, `expectations/`, the scripts and the matrix under `runs/`, and the diagnosis, committed before the first run; `results.md` with the outcome whichever way it falls; the judged packets under `runs/`, each with its `states/` and its judgements, with `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-477.md`, in the protocol's format, dated the day the runs were made. Its section for `../records/README.md` and the changelog entry are written to the build's note file and applied by the run that integrates this build.
