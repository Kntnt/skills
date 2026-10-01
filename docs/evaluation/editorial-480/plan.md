# Plan for #480: a working headline gets no finding

Frozen on 2026-10-01, before the first run of either arm and before any product change. Nothing in this file, in the two judge briefs beside it, in `inputs/`, in `validation/`, or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the rest of the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first. The requirement is the ticket's thread as it stood on 2026-10-01: the body and the triage comment of 11:20 UTC, which says that the target is the false finding the report leaves standing, not a text change that did not happen. Where they conflict, the comment stands.

**`<start>` is `fb169087`**, the commit this build started from. The pre-change arm is staged from it. **The corpus commit is `fb169087`.** `article-clean` and its frozen expectation are read from it. **The fixtures commit is `e5fcdf4f`**, committed before this plan: it holds the three contrast inputs under [`inputs/`](inputs/), the [validation brief](validation-brief.md) and the six validations under [`validation/`](validation/). `runs/lane.sh` writes every input from the fixtures commit, where `article-clean.md` is byte-identical to the corpus commit's (SHA-256 `f183e6da31cf7808…`).

**The candidate does not exist yet.** The triage comment asks for the existing balance to be diagnosed in the first review and in the report before the smallest motivated change is tried, so the candidate is written only after the pre-change arm has been run, judged and read, and only where that arm reproduces the defect. It is committed before its install is staged, and `results.md` names its commit. The two arms are therefore run one after the other, not interleaved in their lanes as #468's were; the time between them is recorded.

## What this plan copies

From [`../editorial-468/plan.md`](../editorial-468/plan.md), with only paths and the seat substituted:

- **The two control briefs**, byte for byte: [`control-judge-brief.md`](control-judge-brief.md) and [`control-judge-brief-file.md`](control-judge-brief-file.md).
- **The split rule**, stated under *When `R1` is met* below.
- **The turn files**: [`runs/wave_inventory.sh`](runs/wave_inventory.sh), with its scratch root, session scratchpad and working tree substituted; [`runs/inventory.sh`](runs/inventory.sh), a byte copy; and [`runs/lane.sh`](runs/lane.sh), with its scratch root and corpus commit substituted and one change: it writes every input from the fixtures commit rather than the corpus commit, since three inputs exist only there.
- **Void-run handling**, stated under *Void runs* below.

The run table, the Target, the Controls and the ship rule are written fresh from #480.

## The contrast inputs

The triage comment asks for at least three further cases frozen before any product change: another working headline that names its subject and works through an allusion, a headline that really does not let a reader tell what the text is about, and a real overclaim. Each is `article-clean` with its headline line alone replaced, so the headline is the one thing that differs between the four inputs, and every other part of the text keeps the frozen expectation `article-clean` already has.

| Input | Headline | Characters, words | SHA-256 (first 16) | Written to be |
| --- | --- | --- | --- | --- |
| `article-clean` | *Mätförsöket i Björkskolan visar när, inte varför* | 48, 7 | `f183e6da31cf7808` | working (the corpus's frozen control) |
| `article-allusion` | *Björkskolans temperaturgivare ger halva svaret* | 46, 5 | `c2fff2c6d236a21b` | working: names its subject, and its image says the measurements answer part of the question |
| `article-unnamed` | *Siffrorna visar när, inte varför* | 32, 5 | `5e43d4f391ba9e07` | unclear: names no subject, so a reader who sees only it cannot tell what the text is about |
| `article-overclaim` | *Mätförsöket visar att Björkskolans klassrum är för kalla* | 56, 8 | `ad383e72ac0c2894` | overclaiming: a verdict on the classrooms the text declines to give |

The counts are `article_anatomy.py`'s at `fb169087`, which exits 0 on all four inputs. `article-unnamed` keeps `article-clean`'s *när, inte varför* and drops its subject, so a candidate that exempted those words would show on it. `article-allusion` shares no word of `article-clean`'s headline but *Björkskolan*, and its allusion is another image, so a candidate that exempted a sentence template would not reach it.

**Validation.** Each contrast input was validated before this plan, by two fresh `kntnt-opus-high` subagents given the [validation brief](validation-brief.md), the text and nothing else. The brief asks plain reader questions — what a reader of the headline alone takes the text to be about, whether the text supports what the headline says, and which of *working*, *unclear* or *overclaiming* the headline is — and quotes no wording of this collection's, the current or any candidate's. All six validations gave their input the class it was written to have; they are in [`validation/`](validation/), mapped to their blind directories in `validation/validators.tsv`.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

Every Redline run of every arm is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), by [`runs/lane.sh`](runs/lane.sh), which runs this command from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=fb169087 \
  --invocation='<invocation from the matrix>' \
  --input=<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high \
  [--capture-output-name=output.md]
```

- **`<commit>`** is `fb169087` for the pre-change arm, the committed candidate for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, so the run's Proofread dependency is met by the Proofread staged beside Redline.
- **`<input>`** is the matrix's input, written from `e5fcdf4f` with `git show` into `<scratch>/inputs/`, never read from a working tree.
- **`--capture-output-name=output.md`** is passed to every file-target run and to no other.
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/480.scratch`, this build's scratch directory.
- **The seat.** `claude-opus-5-5` at high deliberation, for every run, every correction subagent, every reply checker, every judge and every validator. It is requested in `run.json` and recorded for the session and every nested agent in `trace-index.json`. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **The private root.** The run's `HOME`, working directory, temporary directory and caches are made under the system temporary directory and removed by the runner on every exit. The runner strips every `CLAUDE_*` variable, so no run has a session scratchpad; no fault under test lives in one.
- **Lanes.** The matrix assigns every run to one of four lanes, one per input, and `lane.sh` makes a lane's runs one after the other, so no two runs of one input are in flight at once (#401) and at most four runs are in flight at any time.

## The run table

Both arms run every row. [`runs/matrix.tsv`](runs/matrix.tsv) lists the pre-change arm's fourteen runs by name, lane, revision, input and invocation. The post-change arm's matrix, `runs/matrix-post.tsv`, is the same rows with `pre` replaced by `post` in the run name and the arm, and the candidate's commit in the revision column; it is written once the candidate is committed, before its first run, and differs from `matrix.tsv` in nothing else.

| Input | Invocation | Runs per arm | Run names | Brief |
| --- | --- | --- | --- | --- |
| `article-clean` | `/redline --genre=article --language=sv --output=response input.md`, and its pair with `--output=output.md` | three pairs | `<arm>-article-clean-{resp,file}-<n>` | the control briefs |
| `article-allusion` | the same pair | two pairs | `<arm>-article-allusion-{resp,file}-<n>` | the control briefs |
| `article-unnamed` | `/redline --genre=article --language=sv --output=response input.md` | two | `<arm>-article-unnamed-<n>` | `control-judge-brief.md` |
| `article-overclaim` | the same | two | `<arm>-article-overclaim-<n>` | `control-judge-brief.md` |

`<arm>` is `pre` or `post`. Each input is copied to `input.md` and nothing else is in the working directory. No run has a contextual instruction, a technique or a brief. A pair is one response-target run and one file-target run, as the protocol's *A clean control* defines them.

## Frozen expectations

`article-clean`'s is its row's *Frozen expectation and rejection* cell in the corpus README at `fb169087`, verbatim. The three contrast inputs' are these, frozen here, and each is written to its runs' `expectation.md`:

- **`article-allusion`**: Conforms to the anatomy. Preserve the calm explanation, the independent result-bearing standfirst, the byline, the quoted summary, the undecided funding and the ending's non-commercial next step. ABT-shaped logic must not select a technique. Reject any finding against a limit the text meets (46-character headline, 46-word standfirst, 32- and 34-character subheadings, no paragraph over 80 words), any finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count, a finding against the Swedish `Text:` byline form, and a name the text does not carry.
- **`article-unnamed`**: Detect that the headline names no subject: a reader who sees only *Siffrorna visar när, inte varför* cannot tell which figures it means or what the text is about. A repair names the subject from the text's own content and claims nothing the text does not; a finding not repaired is reported as unresolved. Everything else conforms to the anatomy. Preserve the calm explanation, the independent result-bearing standfirst, the byline, the quoted summary, the undecided funding and the ending's non-commercial next step. ABT-shaped logic must not select a technique. Reject any finding against a limit the text meets (32-character headline, 46-word standfirst, 32- and 34-character subheadings, no paragraph over 80 words), any finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count, a finding against the Swedish `Text:` byline form, and a name the text does not carry.
- **`article-overclaim`**: Detect that the headline claims more than the text: *Mätförsöket visar att Björkskolans klassrum är för kalla* gives a verdict on the classrooms that the text declines to give, since the limit is the office's own, chosen for the trial, 14 of 120 lesson periods had a reading under it, and the sensors measured neither draught nor the pupils' experience. A repair states the text's angle at the text's own strength; a finding not repaired is reported as unresolved. Everything else conforms to the anatomy. Preserve the calm explanation, the independent result-bearing standfirst, the byline, the quoted summary, the undecided funding and the ending's non-commercial next step. ABT-shaped logic must not select a technique. Reject any finding against a limit the text meets (56-character headline, 46-word standfirst, 32- and 34-character subheadings, no paragraph over 80 words), any finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count, a finding against the Swedish `Text:` byline form, and a name the text does not carry.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The two judges of one run are dispatched together and are not told of each other.

- **Which brief.** A response-target run is judged with `control-judge-brief.md`, and a file-target run with `control-judge-brief-file.md`.
- **The message.** A judge's message is its brief verbatim, a line `---`, a line naming the run directory, and a line giving its letter, `a` or `b`. It then carries one paragraph headed **Frozen expectation**: the input's expectation above, verbatim. Nothing else is added. No hint of the defect under investigation appears in any invocation, any brief or any message.
- **Neutral paths.** Each judge gets a directory of its own, `<scratch>/j/<token>/`, where `<token>` is twelve random hexadecimal digits. It holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`; for a file-target run, also `work/output.md`, copied from `captured-output.md`. It holds nothing else. The judge writes `judgement-<letter>.md` there, and it is copied into the run's packet as `judgement-a.md` or `judgement-b.md`. The mapping is kept in `runs/judges.tsv`.

A response-target run that returned only a no-change status has its `R1` scored `skipped`, with the protocol's reason: no text was delivered, and the file-target entry answers it. A file-target run that leaves no `output.md` is recorded as delivering none, with its `R1` `skipped` for that reason, and filed.

## Criteria, fixed before the runs

- **`R1`**, on every run: the corpus criterion, as the control briefs quote it.
- **`C1`**, on every run: the run meets its input's frozen expectation above.
- **`O1`**, on every run, from the runner's before-and-after inventories: the run created, replaced or removed nothing its output target does not allow.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

Every other criterion the record template names is recorded `skipped` on every run, naming these four as this evaluation's criteria. No criterion is answered from the Harness trace; the trace is read for the diagnosis below and for the seat.

### When `R1` is met

A run meets `R1` when both judges pass it, and misses it when both fail it. Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary; in that case both readings are recorded and the run meets `R1`. `C1` is read by the same rule.

## The Target: no finding against `article-clean`'s headline

The working headline is *Mätförsöket i Björkskolan visar när, inte varför*, and the corpus freezes `article-clean` as conforming to the anatomy.

- **A run shows the defect** when its reply reports any finding against the headline — left unresolved for the author, answered by a repair, or answered by a repair the run rejected — or offers the author a different headline, or when its delivered text's headline differs from the input's. A response-target run that returned only the no-change status shows no defect. This session reads every `article-clean` reply for it, quotes the passage that decides each call in `results.md`, and records beside it both judges' answers to the expectation's *Conforms to the anatomy*. The judges' answers do not decide the call, since the call is whether a passage is there, not how good it is. This session made the runs and knows their arms, so **this call is not blind**; it is stated here so that nobody reads it as a blind one.
- **Four stages, read apart.** For every run that shows the defect, `results.md` records apart from each other: the finding as the first review recorded it, the correction round's proposal where a round was taken, what the re-review established and whether the round was rejected and the text restored, and what the final report says. The first three are read from the run's transcript, the last from its reply. A round that was rejected and restored with the finding left standing is the defect, not a pass: the report still carries the false finding. A file-target run's `output.md` is the evidence for whether the text was preserved; the reply is the evidence for whether the report carries the finding.
- **`R1` and the defect are recorded apart.** A run whose text came back unchanged passes `R1` whatever its report says, and that pass is no evidence against the defect. #468's `post-article-clean-file-3`, which is the measurement the ticket was filed from, is restated in `results.md` the same way, its four stages apart, its `R1` pass apart from its `C1` miss; its voided first attempt is not counted.
- **Reproduced** when at least one of the six pre-change `article-clean` runs shows the defect.
- **The Target is met** when no candidate `article-clean` run shows the defect and every candidate `article-clean` file-target run meets `R1`.

## The Controls

Each is read in each arm. **A candidate regresses on a Control** only where the pre-change arm held it and the candidate arm does not.

- **The other working headline, `article-allusion`.** An arm holds it when none of its four `article-allusion` runs shows the defect, read exactly as the Target reads `article-clean`, against *Björkskolans temperaturgivare ger halva svaret*.
- **The headline that names no subject, `article-unnamed`.** A run detects it when its reply reports a finding against the headline whose defect is that a reader who sees only the headline cannot tell what the text is about — that it names no subject, or that its words have nothing to refer to — whether the run repaired it or left it unresolved. It is read from the two judges' answers to the expectation's *Detect* clause under heading 3 of their brief; where they split, this session reads the reply, quotes the finding it decides on, and records both judges' readings beside the call. The candidate regresses where its arm detects the defect in fewer runs than the pre-change arm.
- **The overclaim, `article-overclaim`.** Read the same way, against a finding that the headline claims more than the text supports. The candidate regresses where its arm detects the defect in fewer runs than the pre-change arm.
- **The standfirst's supported *kort*, #468's control.** The standfirst is the bold paragraph between the headline and the byline, and it is the same in `article-clean` and `article-allusion`. This session compares the standfirst of every delivered text of those two inputs with the input's, mechanically, and reads the judges' class for each difference. A difference both judges class as a mechanical correction does not count; any other counts. An arm holds the control when no run of those two inputs has a difference that counts.
- **The rest of the contract.** Every run's `C1`, `O1` and `S1` are recorded. A clause of an expectation one arm keeps and the other does not is recorded as measured. The whole-round rejection, the Correction Budget, the closing mechanical pass, the metadata, the input and the destinations are behaviour no candidate here changes; a run in which one of them visibly departs from Redline's steps is recorded and filed.

## Whose miss

The protocol's rule applies. A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded; where they split, the rule under *When `R1` is met* decides. #479 owns a standfirst clause cut from `opinion-clean`, and #477 and #478 own what a reply says about `case-study-clean`; none of them is an input here. A finding against `article-clean`'s or `article-allusion`'s headline, and a changed standfirst on either, is this ticket's.

## The candidate

Written only where the pre-change arm reproduces the defect. Before writing it, this session reads the transcripts of every pre-change `article-clean` and `article-allusion` run that shows the defect, and records in `results.md` which loaded passages the first review cites or paraphrases when it records the finding, and how the finding reaches the report. The candidate is the smallest change motivated by that reading. It may not name `när`, `varför`, Björkskolan, a measurement trial or any other word of the four inputs, and it may not exempt a sentence template; `results.md` gives the candidate's diff and the check of it against those words. The triage comment notes that the allowed headline shape and the requirement to name the subject already stand in the loaded headline resource, so a further restatement of that rule alone is not presumed to repair anything; the diagnosis says what the candidate changes instead, or why a restatement is what the reading points to. Where the change touches `base.review.md`, which #479 may also change, `results.md` says so, so that both targets are verified once the two are integrated.

## Ship rule

The protocol's semantics for a ticket whose change is conditional on the measurement.

1. **Not reproduced.** Where no pre-change `article-clean` run shows the defect, it is recorded as not reproduced on this seat. No candidate is written and no product file changes. A decision record, `docs/adr/0235`, records the non-reproduction as the protocol's *Not reproduced* requires. A pre-change `article-allusion` run that shows the defect is recorded in it and filed as its own `needs-triage` issue naming #480, and so is any Control the pre-change arm misses.
2. **Reproduced, the Target met and no Control regressed.** The candidate ships, recorded as met.
3. **Reproduced, and the Target missed or a Control regressed.** The protocol's one revise round is taken, no larger than the subset that failed: every run, in the post-change arm's numbers, of each input whose reading missed or whose Control regressed, against a revised candidate committed first and staged from its commit. Its runs are named `rev-<input>-…`, listed in `runs/matrix-revise.tsv` in `matrix.tsv`'s columns, made by the frozen `lane.sh` with that matrix as its second argument, and judged exactly as above. After it:
   - the revised candidate ships where it meets the Target and no Control regressed;
   - otherwise it ships only where it beats the pre-change arm on the Target, with fewer `article-clean` runs showing the defect than the pre-change arm's six, and no Control regressed; an input not re-run is read from the first candidate's arm;
   - otherwise the product stays as it was at `<start>`, and no decision record is written: the defect reproduced.

Whichever way it falls, the result is written as measured. Where a candidate ships, Redline's `help.md` and any other prose describing the changed behaviour are brought into line in the same commit, and the catalogue is regenerated.

**Filing.** Each remaining miss is filed as its own `needs-triage` issue naming #480: one for the Target where it is missed in the arm whose wording ships, or in the candidate arm where nothing ships, and one per Control regression. A miss the whose-miss rule assigns to an open ticket is recorded under that ticket and not filed again.

## Void runs

A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; so is a run that reports a file it wrote changed or deleted under it by another process. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again, and a void judgement is kept there too. A run that completes and stops is a finding.

No criterion is softened, no frozen plan, brief or input is edited to fit a result, and no arm is re-run to get a better reading.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of each run's private root. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), with [`runs/inventory.sh`](runs/inventory.sh):

3. **This build's scratch root** `<scratch>`, the packets and the judges' directories among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so neither is hashed.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/7bb3980e-f903-4106-b84f-69be7f823dbe/scratchpad/`, which other sessions of the same run also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## What is written

This file, the two judge briefs and the four files under `runs/`, committed before the first run; the inputs and validations, committed before this file; `results.md` beside them with the outcome whichever way it falls; each run's packet under `runs/<run>/`, with its `expectation.md` and its two judgements; `runs/judges.tsv`, `runs/matrix-post.tsv` and the wave inventories under `runs/waves/`; any void run under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-480.md`, in the protocol's format. A packet's `stream.jsonl` and `transcripts/` are read for the seat and the diagnosis and are not committed. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
