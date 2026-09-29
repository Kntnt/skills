# Plan for #429: Redline leaves a heading that works

Frozen on 2026-09-30, before the first run of either arm. Nothing in this file, in the three judge briefs beside it, or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#397's plan](../editorial-397/plan.md) and [its amendment](../editorial-397/plan-amendment.md), whose method this one copies; this file says only what those leave open and what #429 settles differently.

**`<start>` is `e7773344`**, the head of the branch `kntnt-orchestrate/main/429` when the build began. It holds #431's revision of `case-study-clean` and `opinion-clean` and #439's staging section in the protocol. The pre-change arm is staged from it. **The candidate is `c7f639c6`**, committed before this plan, and the post-change arm is staged from it. **The corpus commit is `e7773344`.** Every input and every frozen expectation is read from it; this ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-09-29: the body, the triage comment of 2026-09-28 15:07 UTC, the readiness addendum of 2026-09-28 18:48 UTC and readiness addendum 2 of 2026-09-29 08:55 UTC. Where they conflict, the later one stands.

## What is under test

Thomas's ruling on the thread is the specification and is not open here: **on a finished text, Redline leaves a heading that works, and rewrites one only where a reader would be misled or lose something it can name.** It ships whatever this measurement shows. This is the maintainer's-ruling case of the protocol's *Not reproduced*. The measurement decides what is written down as met or missed, what is filed, and which wording ships where a revise round is taken.

The candidate, `c7f639c6`, changes `skills/kntnt/library/references/editorial/headlines.review.md`, step 6 of `skills/editorial/redline/SKILL.md` and the regenerated `skills/kntnt/catalog.json`, and no other file under `skills/`:

- The *Avoid* list opens on the ruling's test: an item is a finding where the review can name what a reader of that heading loses, with the seven finding cases of the triage comment as instances of that test. Every *Avoid* item is word for word as at `<start>`.
- *Leave alone* names the four working headings, bounded by *Avoid* item 1 and by the item on a subheading that pre-spends a quotation, as addendum 2 requires.
- The *Avoid* section's closing paragraph says that a repair keeps the text's recurring words and figures and its meaning.
- Step 6 names the heading defect *wording the reader has to read on to understand* by the new test: a heading from which a reader who sees only it cannot tell what the text is about.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

Every Redline run of both arms, and of any revise round, is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), as the readiness addendum requires, by [`runs/lane.sh`](runs/lane.sh), which runs this command from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=e7773344 \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **`<commit>`** is `e7773344` for the pre-change arm, `c7f639c6` for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own and installs them as the session's Skills, so the run's Proofread dependency is met by the Proofread staged beside Redline.
- **`<input>`** is the input the matrix names, written from `e7773344` with `git show` into `<scratch>/inputs/`, never read from a working tree.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other. It copies the delivered `work/output.md` into the packet as `captured-output.md`.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/429.scratch`, this build's scratch directory. The packet, which is what survives a run, is written there.
- **The seat.** `claude-opus-5-5` at high deliberation, requested in `run.json` and recorded for the session and every nested agent in `trace-index.json`. The correction subagents and the nested Proofread pass run inside the session and take its seat. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **The private root.** The run's `HOME`, working directory, temporary directory and caches are made by `mkdtemp` under the system temporary directory and removed by the runner on every exit, as in #397's amendment. A working directory under `<scratch>` would lie under `/Users/thomas/Projects/skills`, whose `CLAUDE.md` a Claude Code session loads from every directory above it. `mkdtemp` names the root, so no other session arrives at the same path. The runner strips every `CLAUDE_*` variable, so no run has a session scratchpad; no fault under test lives in one.
- **Lanes.** [`runs/matrix.tsv`](runs/matrix.tsv) assigns every run to one of seven lanes, and `lane.sh` makes a lane's runs one after the other. Every run of one input is in one lane, so no two runs of one input are in flight at once (#401), and at most seven runs are in flight at any time. Within a lane the two arms alternate. A run whose packet exists is not made again.

**Genre names.** A copied invocation uses the installed genre names (`--genre=casestudy`). That is not a change of method: it stands beside the path and seat substitution the protocol permits, and the *Redline controls* table's Genre column carries the installed names at `e7773344`. #396's two inputs carry the old metadata `genre: case-study`; they are staged unedited, and the invocation names `casestudy`. Where Redline's step 8 rewrites that metadata line to `casestudy`, the synchronisation is not a finding against the run.

## The run table

The table is the readiness addendum's, and it is exhaustive. Both arms run every row. `runs/matrix.tsv` lists all seventy-two runs by name, lane, revision, input and invocation.

| Input | SHA-256 (first 16) | Invocation | Runs per arm | Run names | Judged by |
| --- | --- | --- | --- | --- | --- |
| `article-clean` | `f183e6da31cf7808` | `/redline --genre=article --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs | `<arm>-article-clean-resp-<n>`, `<arm>-article-clean-file-<n>` | two judges per run |
| `case-study-clean` | `1457480f3e7e3066` | `/redline --genre=casestudy --language=sv --output=response input.md`, and its pair | three pairs | `<arm>-case-study-clean-{resp,file}-<n>` | two judges per run |
| `column-clean` | `98b65197fa9dd800` | `/redline --genre=column --language=sv --output=response input.md`, and its pair | three pairs | `<arm>-column-clean-{resp,file}-<n>` | two judges per run |
| `opinion-clean` | `141efb2a4a3b9339` | `/redline --genre=opinion --language=sv --output=response input.md`, and its pair | three pairs | `<arm>-opinion-clean-{resp,file}-<n>` | two judges per run |
| `column-sv-r1` | `4fe7a78864930951` | `/redline --output=response input.md` | two | `<arm>-column-sv-r1-{a,b}` | two judges per run, `redline-judge-brief.md` |
| `column-sv-r2` | `74b966f1352c4f42` | `/redline --output=response input.md` | two | `<arm>-column-sv-r2-{a,b}` | two judges per run, `redline-judge-brief.md` |
| `opinion-en_GB-r1` | `02171183566bb9a1` | `/redline --output=response input.md` | two | `<arm>-opinion-en_GB-r1-{a,b}` | two judges per run, `redline-judge-brief.md` |
| `article-flawed` | `1c0e3b3ef98e06b2` | `/redline --genre=article --language=sv --output=response input.md` | one | `<arm>-article-flawed` | two judges, `control-judge-brief.md` |
| `case-study-flawed` | `ce574061bd09328e` | `/redline --genre=casestudy --language=sv --output=response input.md` | one | `<arm>-case-study-flawed` | two judges, `control-judge-brief.md` |
| `column-flawed` | `9b12ad3fb2cb7401` | `/redline --genre=column --language=sv --output=response input.md` | one | `<arm>-column-flawed` | two judges, `control-judge-brief.md` |
| `opinion-flawed` | `ab033d9f4c817c9e` | `/redline --genre=opinion --language=sv --output=response input.md` | one | `<arm>-opinion-flawed` | two judges, `control-judge-brief.md` |
| #396's `case-question-en_GB-r2` | `c0d2614a4d58ae5c` | `/redline --genre=casestudy --language=en_GB --output=response input.md` | one | `<arm>-case-question-en_GB-r2` | none |
| #396's `case-question-en_GB-r3` | `9c1a422e3c5ace5c` | `/redline --genre=casestudy --language=en_GB --output=response input.md` | one | `<arm>-case-question-en_GB-r3` | none |

`<arm>` is `pre` or `post`. The clean controls are the corpus's `controls/<row>.md`; the drafts are `docs/evaluation/editorial-362/runs/<draft>/redline/work/input.md`; #396's inputs are `docs/evaluation/editorial-364/runs/b/<row>/delivered.md`. Each is copied to `input.md` and nothing else is in the working directory. No run has a contextual instruction or a technique. A pair is one response-target run and one file-target run, as the protocol's *A clean control* defines them, and "at least three runs per arm" is read as three pairs.

That is thirty-six runs per arm, seventy-two before any revise round, and 136 judgements.

## Judging

Two independent judges per judged run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The two judges of one run are dispatched together and are not told of each other.

- **The briefs.** [`redline-judge-brief.md`](redline-judge-brief.md) and [`control-judge-brief.md`](control-judge-brief.md) are byte copies of #397's. [`control-judge-brief-file.md`](control-judge-brief-file.md) is `control-judge-brief.md` with the two changes *Judging a file-target run* below declares, and no other.
- **Which brief.** A draft run is judged with `redline-judge-brief.md`. A response-target clean-control run and a flawed-control run are judged with `control-judge-brief.md`. A file-target clean-control run is judged with `control-judge-brief-file.md`.
- **The message.** A judge's message is its brief verbatim, a line `---`, a line naming the run directory, and a line giving its letter, `a` or `b`. A control judge's message then carries one paragraph headed **Frozen expectation**: the row's *Frozen expectation and rejection* cell in the corpus README at `e7773344`, copied verbatim, which is also written to the run's `expectation.md`. Nothing else is added. No hint of the defect under investigation appears in any invocation, any brief or any message.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits that name neither the arm, the input, the run nor the target. It holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`; for a file-target run, also `work/output.md`, copied from `captured-output.md`. It holds nothing else, because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model. The judge writes `judgement-<letter>.md` there, and it is copied into the run's packet as `judgement-a.md` or `judgement-b.md`. The mapping from directory to run is kept in `runs/judges.tsv`. The build's brief confines everything it writes to its working tree and `<scratch>`, so the judges' directories are under `<scratch>`, whose path carries this build's number; that number names neither the arm nor the expected verdict, the judge is told nothing of what it is, and every brief forbids reading any repository file or ticket. This is a path substitution, stated here so that it can be reviewed against the protocol's *Blind paths*.

### Judging a file-target run

This is a **deliberate change of method** made by this ticket, and it is the only one beyond paths, seat and genre names. The protocol's *A clean control* says that the clean-text criterion "is judged only from the file the file-target run delivered", and #397's control brief cannot see that file. So `control-judge-brief-file.md` differs from `control-judge-brief.md` in two places:

- its sentence "Read exactly those two files" names the three files, `work/input.md`, `work/output.md` and `response.md`;
- after that paragraph, it gains the sentence: *"In this run the Skill delivered its text to `work/output.md`. Every difference you list under heading 1 is between `work/input.md` and `work/output.md`, and R1's clause on clean texts is judged from that file alone, never from what the reply says it changed."*

A response-target run of the same pair is judged with the unchanged brief. In the record, a response-target entry that returned only a no-change status has its `R1` scored `skipped`, with the reason the protocol gives: no text was delivered, and the file-target entry answers the criterion. A file-target run that leaves no `output.md` is recorded as delivering none, with its `R1` `skipped` for that reason; that is a defect, filed as its own issue.

## Criteria, fixed before the runs

As #397's plan defines them, on these runs:

- **`R1`**, on every draft run and every clean-control run.
- **`C1`**, on every control run: the run meets its row's frozen expectation, on `R1`, read against the row as `e7773344` leaves it.
- **`O1`**, on every run, from the runner's before-and-after inventories.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

`A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `R1`, `C1`, `O1` and `S1` as this evaluation's criteria. No criterion here is answered from the Harness trace. #396's two inputs are not judged: their reading below is made by this session from the reply, as #397's plan permits for the presence of a report, and they are scored on `O1` and `S1` alone.

### When `R1` is met

As #397's plan: a run meets `R1` when both judges pass it, and misses it when both fail it. Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary; in that case both readings are recorded and the run meets `R1`. `C1` is read by the same rule.

## Reading the target

There are no bands. This counting rule is read per fixture, in each arm.

- **A clean control** meets the target in an arm when none of its six runs in that arm rewrote a heading. A heading is rewritten when any headline or subheading line in the delivered text (the file-target run's `output.md`, or a text a response-target run delivered in its reply) differs from the input, or is removed or added. A difference both judges class as a mechanical correction does not count. This session compares the heading lines mechanically, and reads the judges' class for each difference it finds.
- **A draft** meets the target in an arm when no run of it misses `R1` on a heading rewrite. A run misses on a heading rewrite when it misses `R1` under the split rule and the passage deciding a failing verdict is a heading difference. `R1` misses on anything else are recorded, and the whose-miss rule applies.
- **The one exception is `Rutan som inte finns` on `column-sv-r2`.** A run's rewrite of that headline does not count as a target miss when two things hold: the new headline keeps the column's recurring *ruta* (as *ruta*, *rutan*, *rutor* or *rutorna*), and neither judge classes the change as a change to what a claim says. That holds even where a judge fails `R1` on it as taste. The judges are told nothing about this; this session applies the exception when reading their verdicts, and `results.md` gives the judges' verdicts as written and says why a run was not counted. A rewrite that changes what a claim says, or one that drops *ruta*, is a miss.
- **The target is met** when every clean control and every draft meets it in the candidate arm.
- **Not reproduced.** Where the pre-change arm meets the target on every fixture, the result is recorded as not reproduced on this seat.

## Reading the controls

- **Flawed controls.** Each row's heading clauses are:
  - `article-flawed`: the headline "fails on truthfulness";
  - `case-study-flawed`: "two subheadings, neither describing its section, the second claiming a conclusion the note itself declines to draw";
  - `column-flawed`: the headline "names no subject of its own and … claims a change the column never makes";
  - `opinion-flawed`: "`Bakgrund` and `Diskussion`, which label the sections instead of describing them".

  A flawed control passes in an arm when the judges' answers under heading 3 of their brief, read by the split rule, record a finding in the reply that names each of its heading clauses. It passes whether the run repaired the heading or left it reported. `C1` is recorded too.
- **#396's control.** It fires on a run when the reply reports a finding that the subheading says what the closing quotation under it says. The subheadings are `Vale would use the schedule again for new jobs` on `-r2` and `Vale would allow an extra week for the status names` on `-r3`. It also fires when the reply changes that subheading and names that defect as the reason. "Still fires" is read against this evaluation's own pre-change arm. A draft on which the pre-change run fires and the candidate run does not is a regression. A draft on which neither fires is recorded as such and filed as its own `needs-triage` issue naming #396 and this ticket; it is not counted against this ticket.

## Whose miss

The protocol's rule applies. A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded; where they split, the rule under *When `R1` is met* decides. That covers #433 (whole-round rejection), #435 (the reply's incidental statements) and #400 (a changed heading accounted for as something else), among others. A heading rewritten on a finished text where the heading works is this ticket's miss.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of each run's private root, which holds its working directory, its staged install and its scratch. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), with [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #397's:

3. **This build's scratch root** `<scratch>`, the packets and the judges' directories among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so neither is hashed.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/e1c56c23-fb82-46cd-bafe-65bb6c439e91/scratchpad/`, which other sessions of the same run also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Exit

The ruling ships whatever the measurement shows. The measurement decides only what is written down as met or missed, what is filed, and which wording ships where a revise round is taken.

1. **The target is met and no control regresses.** The candidate ships, recorded as met.
2. **The target is missed, or a control that passed pre-change fails in the candidate arm.** The protocol's one revise round may be taken, no larger than the subset that failed: every run, in the post-change arm's numbers, of each fixture whose reading missed or regressed, against a revised candidate committed first and staged from its commit. Where it is taken, the wording that ships is whichever of the two candidates has fewer target misses over the re-run subset, or the first where they are level. Either way the change ships, and every remaining miss and every regression is recorded as measured and filed.
3. **Not reproduced.** The candidate still ships, the candidate arm is still run and recorded, and no decision record is written for the non-reproduction.

No branch writes a decision record. The change is prose in a review half that one commit reverses, so it fails the first of `docs/rules/docs.md`'s three criteria; `results.md` says so.

**Filing.** Each remaining miss is filed as its own `needs-triage` issue naming #429, one issue per fixture whose reading missed in the candidate arm. A miss the whose-miss rule assigns to an open ticket is recorded under that ticket and not filed again.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; so is a run that reports a file it wrote changed or deleted under it by another process. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again, and a void judgement is kept there too. A run that completes and stops is a finding.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

## What is written

This file, the three judge briefs and the four files under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; each judged run's packet under `runs/<run>/`, with its `expectation.md` for a control and its two judgements, and every other run's packet the same way; `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-429.md`, in the protocol's format. A packet's `stream.jsonl` and `transcripts/` are read for the seat, which its `trace-index.json` keeps, and are not committed, as #400 kept its transcripts out. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
