# Real Skill runs for #380

Frozen before the first run. Product under test: `main` at `8a37e57e`, the commit this ticket was built from, with `#376`, `#377`, `#378` and `#379` in the tree. Nothing in the Collection differs from it. The corpus is taken from the same commit; `docs/evaluation/corpus/` is byte-identical there to `9a29bad3`, the corpus commit [#386](https://github.com/Kntnt/skills/issues/386) names, so the two evaluations' records are comparable.

The Claude-family evaluation for [#362](https://github.com/Kntnt/skills/issues/362) ran `opinion`, `column` and `case-study` only, ran the Swedish `opinion` once, and judged `F1`, `G2`, `L1` and `R1`. #386 then ran the eight Redline controls of the four article genres and the `column-sv` and `case-study-sv` pipeline rows against the revised corpus. This evaluation runs what both leave out — the `article` and `web-copy` pipeline rows in the locales the matrix selects as baseline, the `opinion` row in `sv` twice, and all three explicit technique pipelines — against every criterion the matrix applies to each side. No row here overlaps a row of either.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. No Codex Harness and no GPT model is started, controlled or invoked from here, and no GPT-family record of the same fixtures is opened before every fixture here is judged. The GPT-family retest of #362 is ordered separately on that ticket.

Each run and each judge is one fresh subagent with no history, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation); the checkers a Write run starts inherit that seat, as `source-check.md` says. The dispatching session's own seat is `claude-opus-5` at high deliberation as well, and it runs and judges nothing itself: every measured artefact is produced by a fresh subagent with no history of this plan. Both records name `claude-opus-5`.

The staged copy is not an installed Skill, so the Skill tool cannot start it. As in `records/write-claude-2026-08-26.md`, in `editorial-362/runs/plan.md` and in `editorial-386/runs/plan.md`, the turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. The staged install is a byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` side by side, taken from `8a37e57e` with `git archive` and never from a working copy, at

```text
/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/skills/
```

so the shim finds the Manager beside the Skill and the global install is never read. One install serves every run.

Each run has its own working directory holding only its input — `source.md` for Write, `input.md` for Redline — and its `scratch/`:

```text
/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/runs/<row>/<side>/work/
```

Every row here is a pipeline row, so every row has a `write/` and a `redline/` directory of that shape.

### What the evaluator adds to a turn

Three statements go into the turn beyond the invocation, and they are declared here because they are not the Skill's. [`write-turn.md`](write-turn.md) and [`redline-turn.md`](redline-turn.md) carry them and nothing else.

- Before the source-check scratch directory is removed, copy it whole to `evidence/` in the run directory. Write only.
- When the run is done, save the complete user-facing reply verbatim to `response.md` in the run directory, and give that same reply as the final message.
- Nobody is available to answer a question. Where the Skill tells the run to ask the user something, the question is stated in the final reply and the run stops there. This states the run's conditions; it replaces no step of the Skill.

Neither turn file paraphrases or replaces a step of the staged `SKILL.md`. It identifies the file and says to follow it exactly.

**Where the harness refuses the `response.md` write**, the evaluator saves the reply it received to `response.md` itself, the entry's `notes` say so, and that file is not counted as a side effect of the Skill. The same holds for a checker report that never reached `evidence/`: the account in `response.md` is then the only evidence of it, and the entry says so.

## The sixteen invocations

This list is exhaustive: eight `/write` runs, each followed by one source-blind `/redline` run on the draft it delivered. The rows are the `article` and `web-copy` rows of the pipeline matrix in the locales its *Baseline locales selected now* column names — `article` in `sv` and in `en_GB`, `web-copy` in `sv` — the `opinion` row in `sv` twice, and every row of the explicit technique pipelines. That column names the locale each row's baseline pair uses; it does not name the baseline instruction revision `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`, which is not staged here and against which no baseline arm is run.

| # | Row | Source | Write invocation |
| --- | --- | --- | --- |
| 1 | `article-sv` | `sources/article.md` | `/write --genre=article --language=sv --output=response source.md` |
| 2 | `article-en_GB` | `sources/article.md` | `/write --genre=article --language=en_GB --output=response source.md` |
| 3 | `web-copy-sv` | `sources/web-copy.md` | `/write --genre=web-copy --language=sv --output=response source.md` |
| 4 | `opinion-sv-r1` | `sources/opinion.md` | `/write --genre=opinion --language=sv --output=response source.md` |
| 5 | `opinion-sv-r2` | `sources/opinion.md` | `/write --genre=opinion --language=sv --output=response source.md` |
| 6 | `article-abt` | `sources/article.md` | `/write --genre=article --technique=abt --language=sv --output=response source.md` |
| 7 | `article-pac` | `sources/article.md` | `/write --genre=article --technique=pac --language=en_GB --output=response source.md` |
| 8 | `web-copy-abt` | `sources/web-copy.md` | `/write --genre=web-copy --technique=abt --language=sv --output=response source.md` |

`sources/<genre>.md` is copied to `source.md` in the row's `write/work/`, as the corpus README says. No contextual instruction is supplied on any row, and no technique on rows 1 to 5.

Each row's Redline invocation is `/redline --output=response input.md`, on a fresh session whose `input.md` is the draft that row's Write run delivered — its Kntnt metadata included and nothing else — and which never sees the source package. The invocation carries no `--genre` and no `--language`: the draft's own metadata resolves both, which is what the pipeline tests.

**A Write run that stops undelivered has no Redline**, and that row's Redline entry is recorded `skipped` with that reason. Its Write entry is still judged, on the last draft the run produced. No row is rerun, and every run is kept.

## Criteria per side

| Side | Judged | Recorded `skipped` |
| --- | --- | --- |
| Write, rows 1–5 | `F1 G1 G2 P1 W1 L1 L2 O1` | `T1 R2 T2` |
| Write, rows 6–8 | `F1 G1 G2 P1 W1 L1 L2 T2 O1` | `T1 R2` |
| Redline, rows 1–5 | `G1 G2 P1 W1 L1 L2 R1 O1` | `T1 R2 T2` |
| Redline, rows 6–8 | `G1 G2 P1 W1 L1 L2 R1 T2 O1` | `T1 R2` |

The lists are the pipeline matrix's own two — `F1 G1 G2 P1 W1 L1 L2 T1 R2 O1` on the Write side and `G1 G2 P1 W1 L1 L2 T1 R1 R2 O1` on the Redline side — with `T2` added on the three explicit-technique rows, as the *Explicit technique pipelines* section says. `F1` applies to Write alone, because Redline never sees the source material.

`O1` is not judged by a judge. It is read by the evaluator from the before-and-after inventory, which is a mechanical check.

### The three skipped criteria, and why

- **`T1`** — `skipped` on every entry. Its evidence is "resolved configuration **and actual loaded files**", and a Claude Code subagent's transcript cannot be read from the session that started it, so the loaded files are not observable here. It is not recorded `pass` on a run's own account of what it loaded, and not recorded `fail` for lacking a trace.
- **`R2`** — `skipped` on every entry, for the same reason: it asks what "the trace establish[es]", Redline's one closing installed Proofread pass among it.
- **`T2`** — `skipped` on rows 1 to 5. Its *Applies* column reads "Explicit technique cases and baseline", and the baseline arm it names runs the baseline instruction revision's automatic ABT, which is not run here. Rows 6, 7 and 8 select a technique explicitly and are judged on it.

`T1` and `R2` are a method limit, not a defect of either Skill. **So this evaluation does not settle whether the scoped contract loading happened, and does not settle whether Redline's closing Proofread pass ran**; the results file, both records and the comment on #362 say so in those terms. The trace-bearing Claude-family harness that would settle them is [#388](https://github.com/Kntnt/skills/issues/388), which both records name against every `T1` and `R2` line; no second issue is filed for it.

## Counted requirements are counted by script

`skills/kntnt/library/scripts/article_anatomy.py` is the script Write, Redline and Redline's correction brief measure the anatomy's counted limits with. The evaluation measures with the same script, from the evaluator's own copy at `.../eval-stage/evaluator/article_anatomy.py` and never from the staged install. That copy is the file as `8a37e57e` holds it, written out with `git show` before the first run, and it is byte-identical to the file at `9a29bad3` that #386 measured with, so the two evaluations' figures are the same measurement:

```text
uv run --no-cache --no-project /Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/evaluator/article_anatomy.py <path>
```

It prints one JSON object with `conforms`, `failures`, `norms`, `typical` and `parts`, and exits `0` when every counted requirement holds, `1` when one fails, and `2` when the text could not be read. The evaluator checks before the first run and again after the last that its copy is byte-identical to the file at `8a37e57e`.

It is run on every text this evaluation judges: a Write row's delivered draft to `anatomy-delivered.json`, and a Redline row's `work/input.md` and `delivered.md` to `anatomy-input.json` and `anatomy-delivered.json`. A Write row's source package is a brief rather than an article, so no `anatomy-input.json` exists on that side. Where a Write run stopped undelivered, the evaluator copies the last draft from `evidence/` to `last-draft.md` beside `work/` and measures it as `anatomy-last-draft.json`; `delivered.md` and `anatomy-delivered.json` are then absent, which is what a stopped run means.

**The anatomy binds the four article genres only.** On the six `article` and `opinion` rows — `article-sv`, `article-en_GB`, `opinion-sv-r1`, `opinion-sv-r2`, `article-abt` and `article-pac` — its counted requirements are requirements, and a count outside one is the failure. On the two `web-copy` rows, `web-copy-sv` and `web-copy-abt`, the corpus says the scale stays advisory, so the script's figures are recorded and quoted as description and no count makes a failure there on its own. The JSON files are kept beside the run either way, and **a judge is handed those figures and counts nothing itself**; where a count it needs is not in the file it says so rather than producing one.

## Two judges per artefact

Every delivered draft and every Redline reply is judged by two independent fresh subagents, each blind to the other, to this ticket, to the diagnostics, to the model identity and to any wording of the expected outcome beyond the criterion text. The briefs are beside this file:

| Brief | Judges | Criteria |
| --- | --- | --- |
| [`write-judge-brief.md`](write-judge-brief.md) | the delivered draft of rows 1–8, with `work/source.md` and `evidence/` available | `F1 G1 G2 P1 W1 L1 L2`, and `T2` where a technique was selected |
| [`redline-pair-judge-brief.md`](redline-pair-judge-brief.md) | the reply of each row's Redline run, with the source available for one separate question | `G1 G2 P1 W1 L1 L2 R1`, and `T2` where a technique was selected |

The two judges of one artefact write `judgement-a.md` and `judgement-b.md` in its run directory and are dispatched together, so neither can read the other's file. Each is pointed at a byte copy of its frozen brief by path, in the evaluator's own directory in the staging area, rather than having the text pasted into its turn, and reads nothing in this repository.

**Where the two split on a criterion**, both readings are recorded and neither judge is the oracle. The criterion's line reads `fail` where the dissenting judge names one of the protocol's five unconditional rejections and the artefact bears it out, and otherwise reads the evaluator's own verdict, with both readings named in the evidence sentence and the dissent in `notes`.

**One judge suffices for a mechanical check** — byte identity, a count, the presence of a report, an exit code, wall time. `O1` and the script's verdict are of that kind and have no judge at all.

## What the results file records per Write run

Seven fields, and this list is exhaustive:

1. **outcome** — `delivered` or `stopped`.
2. **judge class** — `valid delivery`, `valid stop` or `false stop`.
3. **comparisons** — how many source comparisons the run completed.
4. **delivered prose = last compared prose** — byte-identical or not, and `not delivered` for a stopped run.
5. **remaining findings reported** — which findings the delivery account reported beside the draft, the outcome [#376](https://github.com/Kntnt/skills/issues/376) decided.
6. **checker findings** — each one classed `supported`, `false` or `disputed`.
7. **wall time**.

A stopped run therefore has a row of its own with everywhere to be recorded and nothing left blank.

### The outcome #376 decided, and the residual

`source-check.md` as `8a37e57e` holds it is what a run is measured against, and it says: where the final comparison leaves an accepted defect or a genuinely unresolved material claim, the prose is delivered exactly as that comparison read it and every remaining finding is reported in the delivery account — the draft passage, the concrete problem, what the supplied material carries instead, and the smallest repair the checker proposed — with no prose changed after that comparison.

`F1` is recorded as it falls. **A residual the delivery account names is not a new defect and gets no `needs-triage` ticket**, and the run's `F1` line still reads `fail` for that passage, with the residual and its proposed repair quoted. **A residual no account names is a defect and gets its own ticket.**

## Inventory scope

`O1` and the `side effects` field are read from a `sha256` inventory taken before and after, never from a run's report of itself. `inventory.sh`, a byte copy of the script beside `editorial-386/runs/plan.md`, writes one sorted `sha256  path` line per regular file and skips nothing. The scope is every writable location staged for the run, which is the protocol's wider scope and not the narrower one that let a file survive outside the inventory in `records/write-claude-2026-08-26.md` and become #180:

1. **The run directory**, including `work/` and its `scratch/`.
2. **The staged install** at `.../380.scratch/eval-stage/skills/`.
3. **The rest of this ticket's scratch directory** at `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/`, other rows' directories and the evaluator's own directory among them. This is the Harness scratch area for this work: the runs are staged here rather than in the session scratchpad, because this ticket may write in its own working tree and in this directory and nowhere else.
4. **The working copy**, which is this ticket's working tree at `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380` and the developer's own tree at `/Users/thomas/Projects/skills`, which every turn tells the run not to read.

Scopes 1 and 2 are inventoried immediately before each run's turn is dispatched and immediately after its reply arrives, and land in that run's `inventory-before.txt` and `inventory-after.txt`. Scopes 3 and 4 are inventoried once around the wave, into `wave-<n>-before.txt` and `wave-<n>-after.txt` beside `runs/`. The ticket's own working tree is hashed in full; the evaluator writes nothing in it while the wave is in flight, so a change there during the wave is a run's. The developer's tree is covered by `git -C /Users/thomas/Projects/skills status --porcelain --untracked-files=all` and `git rev-parse HEAD` rather than by hashing it, because it carries other sessions' work in progress and a hash of it would report their edits as a run's; that substitution is a declared narrowing and is stated in both records.

Because one staged install serves a whole wave, a change under scope 2 or 3 during a wave cannot be attributed to one run of that wave. Such a change is named in the `side effects` field of every entry in the wave and in `notes`, and the narrower per-run scope is not used to explain it away.

## What each run directory holds

```text
runs/<row>/
  write/
    work/
      source.md              the only input exposed to the run
      scratch/               the only scratch the run may create
    response.md              the user-facing reply, verbatim
    delivered.md             the delivered draft, extracted from the reply
    last-draft.md            a stopped run's last draft, instead of delivered.md
    evidence/                the source-check scratch
    anatomy-delivered.json   the script on delivered.md
    inventory-before.txt
    inventory-after.txt
    judgement-a.md
    judgement-b.md
  redline/
    work/
      input.md               the draft the Write run delivered, and nothing else
      scratch/
    response.md
    delivered.md             the returned text; a byte copy of input.md where nothing changed
    anatomy-input.json
    anatomy-delivered.json
    inventory-before.txt
    inventory-after.txt
    judgement-a.md
    judgement-b.md
```

A Redline reply that changes nothing still gets a `delivered.md`: it is a byte copy of `work/input.md`, and the entry's `observed delivery` says `no change`.

## Where the results go

A results file beside this plan; the two records in the protocol's format under `docs/evaluation/records/`, named `write-claude-<run date>-380.md` and `redline-claude-<run date>-380.md`; and one bullet for each in the records index, appended below every line already there.

## What is fixed before any result exists

No criterion is softened to fit a result, no fixture is edited, and no wording of either Skill or of the Library is changed here. Nothing frozen under `docs/evaluation/` is edited. The rows, the invocations, the criteria, the seat, the briefs, the inventory scope and the script's role above are settled by this file. A real defect becomes its own ticket labelled `needs-triage`, named in the record, and is never absorbed by softening a criterion; where a defect this evaluation meets already has a ticket, that number is cited rather than a second one filed. A run that could not be staged or judged as written is recorded as it fell, and its remaining miss is filed as its own ticket.

## Corrected after the runs

One sentence of this plan was wrong when it was frozen and is corrected here: the paragraph on the anatomy grouped the rows as *five* `article` and `opinion` and *three* `web-copy`, where the eight-row table above has six of the first and two of the second. The evaluator applied the rule by genre throughout — the advisory reading appears on `web-copy-sv` and `web-copy-abt` and on no other entry — so no run, no judgement and no verdict is affected. One further sentence changed in the same commit, and is named here rather than left undeclared: *Where the results go* said the index bullets went to this ticket's note file, the index being the run's to append to rather than a builder's, and now says they are appended below every line already there, which is what the run did. Nothing else in this file is changed, and neither change touches a row, a criterion, a judgement or a figure.
