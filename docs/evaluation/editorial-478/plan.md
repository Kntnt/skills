# Plan for #478: a sentence that says whose the content is moves its attribution

Frozen on 2026-10-01, before the first run of either arm and before the first replay. Nothing in this file, in the three judge briefs beside it, in `contrasts/` or in the scripts, the matrix and the expectations under `runs/` (`inventory.sh`, `wave_inventory.sh`, `lane.sh`, `matrix.tsv`, `stages.py`, `classify-brief.md`, `expectations/`) is edited after the first run; `results.md` and the rest of the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md), its section [*How an evaluation is staged*](../protocol.md#how-an-evaluation-is-staged) above all, and [the corpus](../corpus/editorial-quality/README.md) first, then [#475's plan](../editorial-475/plan.md) and [#468's plan](../editorial-468/plan.md), whose runner, lanes, briefs and void handling this plan copies with paths and the seat substituted. Where this plan departs from them, it says so.

The requirement is the ticket's thread as it stood on 2026-10-01: the body, and the triage comment of 11:16 UTC, which carries the Agent Brief and the acceptance criteria. Where they conflict the later one stands.

**`<start>` is `fb169087`**, the commit this build started from, and the pre-change arm is staged from it. **The corpus commit is `fb169087` too.** Both arms read their inputs and the controls' frozen expectations from it. `case-study-clean` is run as it stands there, unchanged: its headline was rewritten by #463 on 2026-09-30, after #475's run, so its text is not the one #475 ran.

**The candidate is `cbda0352`**, committed on the branch `kntnt-orchestrate/main/478` before this plan and before any install was staged. Its diff touches `skills/editorial/redline/references/reply-check.md`, `skills/editorial/redline/help.md`, `skills/kntnt/catalog.json` and `tests/test_kntnt.py`, and nothing else.

## The historical gap

[`history/post-control-case-study-clean/`](history/post-control-case-study-clean/) keeps, each in a file of its own, the five states of the #475 run the ticket was filed from, split out of [its committed packet](../editorial-475/runs/post-control-case-study-clean/) by [`runs/stages.py`](runs/stages.py): the text as received, the final Text Artifact the checker was shown, the reply as drafted, the checker's whole brief as filled in, what the checker returned, and the reply and the text as delivered. The packet itself is left as it is.

What those files show, read before this plan was written:

- **The text.** The lead's *Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar* became *Vad det krävde berättar arbetsledaren Maya Lind om. Hur många ärenden som registrerades, och hur snabbt de tilldelades, går att följa i Elm Quays interna försöksanteckning.* In the text, part of what the trial required is the narrator's (*Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare*) and part is Lind's quotation. The new sentence gives all of it to Lind, while every fact still stands in its place.
- **The draft.** Finding 4 said *Vad försöket krävde kommer i texten från Maya Linds citat, inte från någon anteckning*, and the claim account's entry said *vad försöket krävde tillskrivs nu arbetsledaren Maya Lind och inte anteckningar*.
- **The checker's return.** Its first list says of finding 4 that what the trial required *comes from Lind's quotes and also from this unattributed narration about Svale configuring the log and training six employees*. Its second list, the claim changes the account misses, is `none`.
- **The delivered reply.** The run corrected finding 4 to *Det som sägs om det kommer från den berättande texten och från Maya Linds citat* and left the entry as *Det är nu Maya Lind som berättar vad försöket krävde, inte anteckningar.*

So the attribution difference fell between the two lists. The checker read the narrator's share as a false statement about the text as received, and did not read the delivered sentence as an attribution move, because the sentence the account names did change its source (notes to Lind), the account says so, and no fact moved. The run acted on each list as its brief says, corrected the finding, and had nothing telling it to complete the entry. A delivered text that should not have been changed is #468's matter and is not judged here as allowed or not; this evaluation is about whether the account of it is complete.

## What is under test

The candidate changes the checker's second list in `reply-check.md`, and nothing the run does before the checker starts:

- A sentence that says whose a body of content is — that a person tells it, that a document shows it — carries an attribution for all of that content, wherever the content itself stands. Where the delivered text gives a person or a source content that the text as it arrived gave to another voice, the narrator's own among them, the attribution has moved even though every fact still stands where it stood.
- A statement on the first list that gets wrong whose a passage's content is may have a change built on it, and that change goes on the second list where the account reports it short.
- An item for a moved attribution says who the text gave which content to before and whom it gives it to now, and an entry that names one of the voices the content came from and leaves out another reports it short.

The manpage's sentence on what the account carries gains *a moved attribution by who the text gave which content to before and whom it gives it to now*. The check is still made once, by one subagent, on the reply alone, and the Correction Budget is unchanged.

**The change is conditional on this measurement.** It ships only as *What ships* below says.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent. Every Redline run and every replay is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree by [`runs/lane.sh`](runs/lane.sh), which is #475's with this build's paths and a `kind` column:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=fb169087 \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<scratch>/inputs/<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents, its checker and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Every judge and every classifier is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `fb169087` for the pre-change arm, the committed candidate `cbda0352` for the candidate arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own.
- **The inputs.** `<scratch>/inputs/<input>` is written by `git show fb169087:<path>` of the path the matrix names, never read from a working tree. The invocation is the whole prompt; no turn file is sent, and no contextual instruction.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit, outside the repository checkout, so no run reads the collection's own agent guide. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after its judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/478.scratch`.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) assigns every run to one of five lanes, one per input or contrast, and `lane.sh` makes a lane's runs one after the other, so no two runs of one input are in flight at once (#401) and at most five runs are in flight at any time. Within a lane the two arms alternate. A run whose packet exists is not made again.

## The real runs

| Input | SHA-256 (first 16) at `fb169087` | Invocation | Runs per arm | Run names |
| --- | --- | --- | --- | --- |
| `case-study-clean` | `2e4ef2fd4b7c03aa` | `/redline --genre=casestudy --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs | `<arm>-case-study-clean-resp-<n>`, `<arm>-case-study-clean-file-<n>` |
| `case-study-flawed` | `ce574061bd09328e` | `/redline --genre=casestudy --language=sv --output=response input.md` | two | `<arm>-case-study-flawed-<n>` |

`<arm>` is `pre` or `post`. Sixteen Redline invocations, eight per arm. `case-study-flawed` is the real-run contrast for a change of scope or cause: its frozen expectation asks for a causal contradiction to be repaired and a subheading that claims a conclusion the note declines to draw, so its runs move claims on purpose, and their accounts are read for completeness and for false entries alike.

**The five states.** After a run, `runs/stages.py` writes, under the packet's `stages/`, the text as received, the final Text Artifact the checker was shown, the reply as drafted, the checker's filled brief, what the checker returned, and the reply and the text as delivered, each to a file of its own, and in `stages.json` whether the delivered text equals the final Text Artifact the checker was shown. A run that returns only the short no-change status starts no checker, and its `stages/` holds the received text and the reply alone.

## The contrasts, frozen before the candidate is tried

Three contrasts, each a received text, a delivered text, a drafted reply and the measurement of the delivered text, under [`contrasts/`](contrasts/). [`contrasts/fill.py`](contrasts/fill.py) fills the checker's half of `reply-check.md` with them the way #475's run filled it, and the filled briefs are committed as `prompt-pre.txt` (from `fb169087`) and `prompt-post.txt` (from `cbda0352`). `<library>` is replaced by `~/.claude/skills/kntnt/library`, where the runner stages the Library of the arm's commit.

| Contrast | What it holds | What a right return is |
| --- | --- | --- |
| `k1-narrator-to-person` | #475's run, unchanged: the received text, final text, drafted reply and measurement its checker was given. `prompt-pre.txt` is that checker's brief byte for byte, save the Library path and the closing newline. | The second list names that the lead now gives Lind what the trial required, part of which the narrator stated. |
| `k2-attribution-kept` | `case-study-clean` with *gruppen* and *gruppens* in the standfirst and the lead named as *underhållsgruppen*, and a reply whose account says no claim moved. The lead's sentence about whose notes show what the trial required and gave is touched, and still gives it to the same group's notes. | No item, on either list, that the texts do not bear out; above all, no moved attribution. |
| `k3-cause-and-scope-reported` | `case-study-clean` with *om loggförsöket* dropped from the headline, widening the appraisal's scope, and *och anteckningen tillskriver därför* split into two sentences, losing the text's reason, and a reply whose account reports both changes in full, the speaker of the headline kept. | No item, on either list, that the texts do not bear out. |

**A replay is diagnosis.** It hands a filled brief to a fresh top-level session in place of the subagent a run starts, so it shows what the checker returns on a fixed input and nothing about what a run does with the return. It is marked as diagnosis in every place it is reported, and it never stands in for a Redline run. Each contrast is replayed three times per arm, `<arm>-replay-k<n>-<i>`: eighteen replays.

## Judging

Two independent judges per real run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket.

- **The briefs.** [`control-judge-brief.md`](control-judge-brief.md) and [`control-judge-brief-file.md`](control-judge-brief-file.md) are byte copies of #475's. A response-target run is judged with the first, a file-target run with the second. Both ask for every difference, headings and lead included, its class among them *attribution*, and whether the reply reports it accurately; so the whole text is judged, not the passage the ticket names.
- **The frozen expectation.** Each judge's message carries the row's *Frozen expectation and rejection* cell at `fb169087` as one paragraph headed **Frozen expectation**, as kept in [`runs/expectations/`](runs/expectations/) and copied to the run's `expectation.md`.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits. It holds `work/input.md`, `response.md` and, for a file-target run, `work/output.md`, and nothing else. The judge writes `judgement-<letter>.md` there; it is copied into the packet, and the directory is removed. The mapping is kept in `runs/judges.tsv`. The scratch path carries this build's number; the judge is told nothing of it, and every brief forbids reading any repository file or ticket. This is the path substitution #475's plan made and stated.
- **The replays.** Two judges, each a fresh `kntnt-opus-high` subagent, each given all eighteen replays under [`replay-judge-brief.md`](replay-judge-brief.md), in directories `<scratch>/r/<token>/` holding `received.md`, `delivered.md`, `reply.md` and `return.md` (the session's reply), in an order shuffled for each judge. The mapping is kept in `runs/replay-judges.tsv`.
- **Classifying.** Every `A2` miss of a real run is put in a class by fresh `kntnt-opus-high` subagents under [`runs/classify-brief.md`](runs/classify-brief.md), which is #475's with this ticket's owners and one more field, `attribution`, given to every class 1 miss. Each classifier gets neutral directories `<scratch>/c/<token>/` with the run's input, reply, delivered file where there is one, the expectation, both judgements and `kind.txt`, and writes `classes.json`, kept in the packet. The mapping is `runs/classifiers.tsv`. This build reads every class 1 and class 2 call and every attribution call, and records any it changes with its reason.
- **Where a miss arose.** For every class 1 and class 2 miss, this build reads the run's `stages/` and records whether the delivered statement was already in the draft and the checker's return named it, already in the draft and the return did not name it, or written by the run's correction of the draft. This reading is not blind; it is recorded beside the class and decides nothing.

## Criteria, fixed before the runs

### `A2`, its classes, and a target miss

`A2` and its four classes are #475's: a judge records an `A2` miss where its judgement calls a statement of the reply false, inaccurate, imprecise, loose or misleading against a text, or records under heading 2 a difference the reply does not report or reports inaccurately; class 1 is a claim-account miss, class 2 a counted miss outside the claim account, class 3 recorded and not counted, class 4 an omission. One judge is enough to put a miss in a run. Statements about the text as received are read against the input, and all others against the delivered text, so a statement a correction of the reply wrote after the check is read against the delivered text like any other.

**A target miss** is a class 1 miss whose claim change moved an attribution: the delivered text gives a person or a source content that the text as it arrived gave to another voice, the narrator's own among them, or to no one, and the account leaves it out or reports it short of who held which content before and who holds it now. An account that names one source the content came from and leaves out another reports it short, however each fact still stands. Whether every fact still stands in its place does not decide it. Names and fixed phrases do not decide it either: the test is what the delivered text now says about whose the content is.

### Whose miss

The open tickets whose behaviour a run of these inputs can show are **#476** (a correction round's working files left behind) and **#477** (a finding saying the case study's note explicitly rules out the software, where it only declines to credit it). A miss that is one of those behaviours is recorded under that ticket and not counted here. Both judges' readings are recorded. Every other class 1 and class 2 miss counts here, whoever owns the text change the statement describes: #468 is closed, and a clean text changed is recorded beside the miss but takes no miss away.

### The Target, Reproduced and the Control

- **Unit.** The run. A run *carries a target miss* where either judge records one. An arm's figure is the share of its eight real runs that carry one, both targets of `case-study-clean` and both runs of `case-study-flawed` included.
- **Reproduced.** The pre-change arm reproduces the fault where at least one of its eight real runs carries a target miss. Replays do not decide it.
- **Target.** Both of:
  1. the candidate arm's share is at most half the pre-change arm's;
  2. in at least two of the three candidate replays of `k1-narrator-to-person`, both replay judges answer heading 3 `yes`.
- **Control.** None of these holds:
  1. a candidate run whose delivered text differs from the final Text Artifact its checker was shown, or whose `input.md` changed, or whose side effects break `O1`;
  2. more candidate runs than pre-change runs carrying a class 1 or class 2 miss that is not a target miss and not owned elsewhere — an entry that reports a change the texts do not show, a sentence about the claims as a whole that contradicts a reported change, and any other such miss among them;
  3. a candidate run whose delivered text equals its input and whose reply says a claim was removed, changed or added;
  4. more candidate replays of `k2-attribution-kept` and `k3-cause-and-scope-reported` than pre-change replays of them carrying an item either replay judge calls `false`.

### `C1`, and the rest of every run

- **`C1`** is each control judge's heading-4 verdict, labelled `R1` in the briefs. It is recorded for every real run. The candidate changes nothing the run does before the checker, and control 1 above checks that the checker changed no text, so a `C1` failure is recorded with the change that caused it and is not a Control miss.
- **`O1`**, from the runner's before-and-after inventories and the wave inventories. For a file-target run, the one file created beside the input, `output.md`, is the effect that was asked for.
- **`S1`**: the working directory held `input.md` and nothing else when the session started.
- **The checker.** How many checkers each run started, read from `stages.json`: one on every run whose reply says anything about a text, none on a run returning only the no-change status. Recorded, and any other count is named in the results.

`A1`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `A2`, `C1`, `O1` and `S1` as this evaluation's criteria.

## The revise round

**It is taken where Reproduced is met and the Target or the Control is missed**, once and no more, against a revised candidate committed first. It reruns the inputs and contrasts whose candidate runs missed: `case-study-clean` as three pairs where a `case-study-clean` run carries a target miss or a Control miss, `case-study-flawed` twice where one of its runs does, and three replays of each contrast whose candidate replays missed. The Target and the Control are then read with the revised runs in place of the first candidate's runs on those inputs.

## What ships

1. **Not reproduced.** Where no pre-change real run carries a target miss, the result is recorded as not reproduced, the candidate is reverted so that the product stays as it was at `<start>`, whatever the replays show, and a decision record is written under the reserved number `0233`.
2. **Met.** Where the candidate meets the Target and the Control, on its first reading or after the revise round, the candidate that met them ships.
3. **The fallback.** Where the revise round has been taken and the Target is still missed, the revised candidate ships only where its share of real runs carrying a target miss is at most half the pre-change share and the Control is met. Otherwise the candidate is reverted and the product stays as it was.
4. **Whichever way it falls**, the result is written as measured, and each remaining miss — every class 1 and class 2 miss of the candidate reading that ships or, where nothing ships, of the pre-change arm, not owned by an open ticket — is filed as its own `needs-triage` issue naming #478. A miss owned by #476 or #477 is recorded there and not filed again.

No criterion is softened, no frozen plan, brief, contrast or fixture is edited to fit a result, and no arm is re-run to get a better reading. The number of checkers a run starts and the Correction Budget are not changed by any candidate.

**Void runs.** A run, replay or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its input is run again. A run that completes and stops is a finding.

## Inventory scope

Scopes 1 and 2 — the run's working directory, its staged install and its scratch — are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), #475's with this build's paths, calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #475's:

3. **The rest of this build's scratch root**, the other runs' packets among them.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/7bb3980e-f903-4106-b84f-69be7f823dbe/scratchpad/`, which the orchestrating session and sibling builds also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## What is written

This file, the three judge briefs, `history/`, `contrasts/` and the scripts, matrix, expectations and classify brief under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; the judged packets under `runs/`, each with its `stages/`, `expectation.md`, `judgement-a.md`, `judgement-b.md` and `classes.json`, the replays' packets with both replay judgements, `runs/judges.tsv`, `runs/replay-judges.tsv`, `runs/classifiers.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-478.md`, in the protocol's format, dated the day the runs were made. Its section for `../records/README.md` and the changelog entry are written to the build's note file and applied by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
