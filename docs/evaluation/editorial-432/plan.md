# Plan for #432: a web page's own form and a heading's fact are not findings

Frozen on 2026-09-29, before the first run of either arm and before the candidate is committed. Nothing in this file or in the three judge briefs beside it is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first. The method is [#397's plan](../editorial-397/plan.md) as [its amendment](../editorial-397/plan-amendment.md) amends it, with paths, seat and evaluation number substituted. This file departs from that method only where the readiness addendum of 2026-09-29 on #432 says so, and each departure is named as one below.

**`<start>` is `e7773344`**, the head of the branch `kntnt-orchestrate/main/432` when the build began. The pre-change arm is staged from it. **The corpus commit is `e7773344` too.** Both arms read their inputs and their frozen expectations from it. This ticket's diff does not touch the corpus.

The requirement is the ticket's thread: the body, the triage comment of 2026-09-28 and the readiness addendum of 2026-09-29. Where they conflict, the later one stands.

## What is under test

On `web-copy-clean`, in both arms of [#397](../editorial-397/results.md), both judges of both runs failed `R1` against the row *Preserve a complete information page without sales template or CTA. Short headings and variable section length work. No invention of destination or function.* Each run did two things. It copied `inom tre arbetsdagar` from the subheading `Svar inom tre arbetsdagar` into the sentence under it, because the reply time stood only in the heading. And it left an unresolved finding that the page names a form it neither holds nor links, asking for a link or a location.

Thomas's ruling in the triage comment is the specification and is not open here: **the row is right on both points, and the review guidance is narrowed.** The candidate states two limits on findings in the review guidance, in `genres/webcopy.review.md` and `base.review.md`:

- A form, button or link reference is a finding only where the copy places or describes it differently from what the artifact shows. #345's case, *the form below* over what is only a link, stays a finding.
- A heading may carry a fact its section does not repeat. What is a finding is a body that needs the heading to be understood.

No base half changes. The candidate's wording is committed after this plan and before the candidate arm is staged, and `results.md` records it with its commit. The ruling ships whatever this measurement shows. The measurement decides which wording ships where a revise round is taken, and what is written down.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

As [#397's amendment](../editorial-397/plan-amendment.md) makes every run, and as the readiness addendum requires: each run is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=e7773344 \
  --invocation='<invocation from the table>' \
  --input=<scratch>/inputs/<input> --input-name=<input.md or source.md> \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **The seat.** `claude-opus-5-5` at high deliberation, for the session, its correction subagents and its nested Proofread pass, which take the session's seat. `run.json` records the request and `trace-index.json` what ran. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `<start>` for the pre-change arm, the committed candidate for the candidate arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own.
- **The inputs.** `<scratch>/inputs/` holds `web-copy-clean.md` and `web-copy-flawed.md`, each `git show e7773344:docs/evaluation/corpus/editorial-quality/controls/<row>.md`, and `web-copy-source.md`, `git show e7773344:docs/evaluation/corpus/editorial-quality/sources/web-copy.md`. All three are written once before the first run. The invocation is the whole prompt. No turn file is sent.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit. It is not under this build's scratch, because a working directory there would sit under `/Users/thomas/Projects/skills`, whose `CLAUDE.md` a Claude Code session loads from every directory above it. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after its judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/432.scratch`.
- **No two runs on one input at a time** (#401). This build makes at most one run of an input at once, across both arms. The three inputs are `web-copy-clean`, `web-copy-flawed` and the `web-copy-sv` pipeline, so at most three runs are in flight together. #397's lock on `case-study-clean` does not apply: no row of this evaluation is that row.

## The runs

This table is exhaustive for one arm, and both arms run every row. It is the readiness addendum's table.

| Input | Invocation | Runs per arm | Judged by |
| --- | --- | --- | --- |
| `web-copy-clean` (`controls/web-copy-clean.md` as `input.md`) | `/redline --genre=webcopy --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs; a pair is one response-target run and one file-target run, as the protocol's *A clean control* defines them | two blind judges per run: response-target runs on [`control-judge-brief.md`](control-judge-brief.md), file-target runs on [`control-judge-brief-file-target.md`](control-judge-brief-file-target.md) |
| `web-copy-flawed` (`controls/web-copy-flawed.md` as `input.md`) | `/redline --genre=webcopy --language=en_US --output=response input.md` | one | two blind judges, on [`control-judge-brief.md`](control-judge-brief.md), with the row's frozen expectation |
| `web-copy-sv`, as the pipeline in the corpus README's staging paragraph | `/write --genre=webcopy --language=sv --output=response source.md` from `sources/web-copy.md`, then, in a fresh session given only that draft as `input.md`, `/redline --output=response input.md`, with both halves installed from that arm's own commit | one pipeline | the Redline half by two blind judges on [`redline-judge-brief.md`](redline-judge-brief.md); the Write half is not judged |

That is nine staged runs per arm, eight Redline runs and one Write run, or eighteen before any revise round. The sixteen Redline runs are judged, by thirty-two judgements.

**The run names**, with `<arm>` one of `pre`, `post` and `revise`:

- `<arm>-web-copy-clean-response-<n>` and `<arm>-web-copy-clean-file-<n>`, for pair `<n>` of 1 to 3. Pair 1's response-target run is made first, then its file-target run, then pair 2, and so on.
- `<arm>-web-copy-flawed`.
- `<arm>-web-copy-sv-write`, then `<arm>-web-copy-sv-redline`.

**The file-target runs** are made with `--capture-output-name=output.md`, so the runner keeps the file the run delivered as `captured-output.md` in the packet.

**The pipeline's draft.** The Write run's `response.txt` delivers the draft in a fenced Markdown block. The draft is that block's content, from the line after its opening fence to the line before its closing fence, taken byte for byte with one final newline. It is written to `<scratch>/inputs/<arm>-web-copy-sv-draft.md` and becomes the Redline run's `input.md`. A Write reply that holds no such block delivers no draft. Its Redline half is then not made, and the miss is recorded and filed.

## Judging

Two independent judges per Redline run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. [`control-judge-brief.md`](control-judge-brief.md) and [`redline-judge-brief.md`](redline-judge-brief.md) are byte copies of #397's. A control judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**: the row's *Frozen expectation and rejection* cell at `e7773344`, copied verbatim. Beyond that paragraph, the message names the judge's directory and its letter, and nothing else. Nothing in any message, brief or invocation mentions the target.

**Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, named by a random twelve-hex-digit token that names neither the arm, the row, the run nor the target. For a response-target run and for the pipeline's Redline half, it holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`, and nothing else. The packet's other files name the revision and the model. The judge writes `judgement-<letter>.md` there. The judgement is copied into the run's directory as `judgement-a.md` or `judgement-b.md`, and the mapping from directory to run is kept in `runs/judges.tsv`. The two judges of one run are dispatched together and are not told of each other.

**The scratch root's name.** The build's brief confines everything it writes to its working tree and its scratch directory, and names both by this ticket's number. So a judge's directory carries that number in its parent's path, as #397's did. The judge is told nothing of what the number is.

**Judging a file-target run.** This is a change of method, adopted by the readiness addendum from #429 and declared here before the first run. The protocol's [*A clean control*](../protocol.md#a-clean-control) says the criterion that a clean text comes back unchanged is judged only from the file the file-target run delivered, compared with the input that run was staged with. #397's `control-judge-brief.md` reads only `work/input.md` and `response.md`, and cannot see that file. So:

- A file-target run's judge directory holds three files: `work/input.md`, from the packet's `supplied-input.md`; `work/output.md`, from `captured-output.md`; and `response.md`, from `response.txt`.
- Its judges use [`control-judge-brief-file-target.md`](control-judge-brief-file-target.md). It is `control-judge-brief.md` with two changes. Its sentence "Read exactly those two files" names the three files. After that paragraph it gains: *"In this run the Skill delivered its text to `work/output.md`. Every difference you list under heading 1 is between `work/input.md` and `work/output.md`, and R1's clause on clean texts is judged from that file alone, never from what the reply says it changed."*
- A response-target run that returned only a no-change status has its `R1` scored `skipped` in the record, for the reason the protocol gives: no text was delivered, and the file-target entry answers the criterion. Its judges still write.
- A file-target run that leaves no `output.md` is recorded as delivering none, with its `R1` `skipped`, and filed as its own issue.

One judge suffices for a mechanical check — reading a reply for a finding, a diff, the inventory — and those the dispatching session makes itself from the recorded files.

## Criteria, fixed before the runs

As #397's plan defines them, on these runs:

- **`C1`**, on every run of `web-copy-clean` and `web-copy-flawed`: the run meets its row's frozen expectation, on `R1`, read against the row as `e7773344` leaves it.
- **`R1`**, on the pipeline's Redline half.
- **`O1`**, on every run, from the runner's before-and-after inventories. For a file-target run, the one file created beside the input, `output.md`, is the effect that was asked for.
- **`S1`**, on every run: the working directory held the one input and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

Every other criterion — `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` — is recorded `skipped` on every run. The Write run is recorded with every criterion `skipped` but `O1` and `S1`: it stages the Redline half's input and is not judged.

### When `R1` is met

#397's plan, *When `R1` is met*, settles a split between two judges, for `R1` and `C1` alike:

- A run meets `R1` when both judges pass it, and misses it when both fail it.
- Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary. In that case both readings are recorded and the run meets `R1`.

## Reading the target and the controls

These are the readiness addendum's readings.

**The target, run by run.** A run carries a target miss where either of these holds:

- its reply reports the page's form as missing, or asks for a link, a location or an included form, where the copy names the page's own form and the artifact carries no interface markup;
- its delivered text copies a fact a subheading carries into the body under that subheading.

This build reads the target from the reply and from the delivered text — the file-target run's `output.md`, or a text a response-target run returned — quoting the passage that decides it, as #397's plan reads the presence of a report. Both judges' `C1` verdicts are recorded beside it. The judges are told nothing about the target.

- **Target met.** No candidate run of `web-copy-clean` carries a target miss.
- **Reproduced.** At least one pre-change run of `web-copy-clean` carries one.

**`web-copy-flawed` meets its row in a run** where two things hold:

- it meets `C1` under the split rule;
- either judge's heading-3 answer records a finding in the reply naming the misleading *Book and pay* action.

That is the triage comment's case of a link labelled as something it does not do, which stays a finding.

**`web-copy-sv`'s Redline half meets its row in a run** where it meets `R1` under the split rule.

**A regression.** A control that met its reading in the pre-change arm and misses it in the candidate arm is a regression.

**Whose miss.** A miss caused by a behaviour another open ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded. A closed ticket takes no miss, as #435's second addendum reads the protocol's rule. Where two judges split, the rule above decides.

## Inventory scope

As #397's plan, with its paths replaced, and as its amendment reads scopes 1 and 2:

- **Scopes 1 and 2: the run's private root**, holding its working directory, its staged install and its scratch — the runner's before-and-after inventories, per run.

The other three are read around each wave:

3. **The rest of this build's scratch root**, other runs' packets and the judges' directories among them.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, which is #383's declared narrowing.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/e1c56c23-fb82-46cd-bafe-65bb6c439e91/scratchpad/`.

Scopes 3 to 5 are read by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), which is #397's with this build's paths, beside [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #397's. Wave 1 is every run of both arms, read once before the first run and once after the last. A revise round is wave 2. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Exit

This is the protocol's ruling case: **the change ships whatever the measurement shows.**

1. **The candidate** ships where no candidate run carries a target miss and no control regresses.
2. **A missed target or a control regression.** One revise round may be taken, on the rows that missed: every candidate-arm run of each input on which the target or a control reading missed, against a revised candidate committed first. Where the revised wording carries no target miss and regresses no control over the re-run rows, it ships. Otherwise the wording with fewer target misses over the re-run rows ships; where they are level, the first wording ships.
3. **Not reproduced.** Where no pre-change run of `web-copy-clean` carries a target miss, the result is recorded as not reproduced. The candidate still ships, the candidate arm is still run and recorded, and no decision record is written.
4. **Filing.** Every remaining miss and every regression is filed as its own `needs-triage` issue naming #432.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. So is a run that reports a file it wrote changed or deleted under it by another process. A void run is moved whole to `voided/` beside `runs/` before its row is run again. A run that completes and stops is a finding.

## What is written

This file and the three judge briefs, committed before the first run. `results.md` beside them with the outcome whichever way it falls. The judged packets under `runs/`, each with `expectation.md` for a control and its two judgements, the Write run's packet with the draft taken from it, and the wave inventories beside them. Any void run under `voided/`. One record, `../records/redline-claude-<date>-432.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
