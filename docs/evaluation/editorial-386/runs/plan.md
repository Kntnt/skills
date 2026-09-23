# Real Skill runs for #386

Frozen before the first run. Product under test: `main` at `9a29bad3`, a commit that holds `skills/kntnt/library/scripts/article_anatomy.py`. That commit is the corpus revision named in both records, and nothing in the Collection differs from it.

The corpus was revised for the [article anatomy](../../../../skills/kntnt/library/references/editorial/article-anatomy.md) and the [headline reference](../../../../skills/kntnt/library/references/editorial/headlines.md) beside it, and no record has been made against that revision. #380 runs the `article` and `opinion` pipeline rows against it. This evaluation runs what #380 leaves out — the eight Redline controls of the four article genres, and the `column-sv` and `case-study-sv` pipeline rows — and the two do not overlap.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. No Codex harness and no GPT model is started from here, and the GPT-family records of the same fixtures are opened only after every fixture here is judged.

Each run and each judge is one fresh subagent with no history, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation); the checkers a Write run starts inherit that seat, as `source-check.md` says. The dispatching session's own seat is `claude-fable-5-1`; runs are delegated to Opus to spare that seat's budget, which is a declared difference from "inherit the session's identity". Both records name `claude-opus-5`.

The staged copy is not an installed Skill, so the Skill tool cannot start it. As in `records/write-claude-2026-08-26.md` and in `editorial-362/runs/plan.md`, the turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. The staged install is a byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` side by side at

```text
/private/tmp/claude-501/-Users-thomas-Projects-skills/1152bc7f-820e-46e3-b676-a0818805225f/scratchpad/eval-stage/skills/
```

so the shim finds the Manager beside the Skill and the global install is never read. One install serves every run.

Each run has its own working directory holding only its input — `source.md` for Write, `input.md` for Redline — and its `scratch/`:

```text
/private/tmp/claude-501/-Users-thomas-Projects-skills/1152bc7f-820e-46e3-b676-a0818805225f/scratchpad/eval-stage/runs/<row>/
```

A control row's run directory is that directory itself. A pipeline row's is `<row>/write/` and `<row>/redline/`, each of the same shape, as the #362 runs are.

### What the evaluator adds to a turn

Three statements go into the turn beyond the invocation, and they are declared here because they are not the Skill's. `write-turn.md` and `redline-turn.md` carry them and nothing else.

- Before the source-check scratch directory is removed, copy it whole to `evidence/` in the run directory. Write only.
- When the run is done, save the complete user-facing reply verbatim to `response.md` in the run directory, and give that same reply as the final message.
- Nobody is available to answer a question. Where the Skill tells the run to ask the user something, the question is stated in the final reply and the run stops there. This states the run's conditions; it replaces no step of the Skill.

Neither turn file paraphrases or replaces a step of the staged `SKILL.md`. It identifies the file and says to follow it exactly.

**Where the harness refuses the `response.md` write**, the evaluator saves the reply it received to `response.md` itself, the entry's `notes` say so, and that file is not counted as a side effect of the Skill. The same holds for a checker report that never reached `evidence/`: the account in `response.md` is then the only evidence of it, and the entry says so.

## The twelve invocations

This list is exhaustive. The eight controls are staged as the corpus README's *Redline controls* section says — only the linked artifact copied to `input.md`, no contextual instruction and no technique. The two pipeline rows are staged as its *Material and staging* section says — `sources/<genre>.md` copied to `source.md`, then the draft Write delivered, its Kntnt metadata included and nothing else, copied to `input.md` for a fresh Redline session that never sees the source.

| # | Row | Side | Input | Invocation |
| --- | --- | --- | --- | --- |
| 1 | `article-clean` | Redline control | `controls/article-clean.md` | `/redline --genre=article --language=sv --output=response input.md` |
| 2 | `article-flawed` | Redline control | `controls/article-flawed.md` | `/redline --genre=article --language=sv --output=response input.md` |
| 3 | `case-study-clean` | Redline control | `controls/case-study-clean.md` | `/redline --genre=case-study --language=sv --output=response input.md` |
| 4 | `case-study-flawed` | Redline control | `controls/case-study-flawed.md` | `/redline --genre=case-study --language=sv --output=response input.md` |
| 5 | `column-clean` | Redline control | `controls/column-clean.md` | `/redline --genre=column --language=sv --output=response input.md` |
| 6 | `column-flawed` | Redline control | `controls/column-flawed.md` | `/redline --genre=column --language=sv --output=response input.md` |
| 7 | `opinion-clean` | Redline control | `controls/opinion-clean.md` | `/redline --genre=opinion --language=sv --output=response input.md` |
| 8 | `opinion-flawed` | Redline control | `controls/opinion-flawed.md` | `/redline --genre=opinion --language=sv --output=response input.md` |
| 9 | `column-sv` | Write | `sources/column.md` | `/write --genre=column --language=sv --output=response source.md` |
| 10 | `column-sv` | Redline | the draft from row 9 | `/redline --output=response input.md` |
| 11 | `case-study-sv` | Write | `sources/case-study.md` | `/write --genre=case-study --language=sv --output=response source.md` |
| 12 | `case-study-sv` | Redline | the draft from row 11 | `/redline --output=response input.md` |

Rows 10 and 12 carry no `--genre` and no `--language`: the draft's own Kntnt metadata resolves both, which is what the pipeline tests. No row is rerun, and every run is kept.

**A Write run that stops undelivered has no Redline**, and that row's Redline entry is recorded `skipped` with that reason. Its Write entry is still judged, on the last draft the run produced.

## Criteria per side

| Side | Judged | Recorded `skipped` |
| --- | --- | --- |
| Redline control, rows 1–8 | `G1 G2 P1 W1 L1 L2 R1 O1` | `T1 R2 T2` |
| Write, rows 9 and 11 | `F1 G1 G2 P1 W1 L1 L2 O1` | `T1 R2 T2` |
| Redline pair, rows 10 and 12 | `G1 G2 P1 W1 L1 L2 R1 O1` | `T1 R2 T2` |

The control lists come from the corpus README's *Redline controls* section; the pipeline lists come from its pipeline matrix. `F1` applies to Write alone, because Redline never sees the source material.

`O1` is not judged by a judge. It is read by the evaluator from the before-and-after inventory, which is a mechanical check.

### The three skipped criteria, and why

- **`T1`** — `skipped` on every entry. Its evidence is "resolved configuration **and actual loaded files**", and a Claude Code subagent's transcript cannot be read from the session that started it, so the loaded files are not observable here. It is not recorded `pass` on a run's own account of what it loaded, and not recorded `fail` for lacking a trace.
- **`R2`** — `skipped` on every entry, for the same reason: it asks what "the trace establish[es]", including Redline's one closing installed Proofread pass.
- **`T2`** — `skipped` on every entry, because no row selects a technique and none is expected to.

`T1` and `R2` are a method limit, not a defect of either Skill. So this evaluation says nothing about whether the scoped contract loading happened or whether Redline's closing Proofread pass ran; the results file and both records say so in those terms. A trace-bearing Claude-family harness is its own work: one `needs-triage` issue asks for it, and both records name that issue. Where #380's thread has already filed it, that issue number is cited rather than a second one filed.

## Counted requirements are counted by script

`skills/kntnt/library/scripts/article_anatomy.py` is the script Write, Redline and Redline's correction brief measure the anatomy's counted limits with. The evaluation measures with the same script, from the evaluator's own copy and never from the staged install. That copy is the file as `9a29bad3` holds it, written out with `git show 9a29bad3:skills/kntnt/library/scripts/article_anatomy.py` before the first run, because another session edits the repository's working copy while the runs are made and the file there may move:

```text
uv run --no-cache --no-project /private/tmp/claude-501/-Users-thomas-Projects-skills/1152bc7f-820e-46e3-b676-a0818805225f/scratchpad/eval-stage/evaluator/article_anatomy.py <path>
```

It prints one JSON object with `conforms`, `failures`, `norms`, `typical` and `parts`, and exits `0` when every counted requirement holds, `1` when one fails, and `2` when the text could not be read. The evaluator checks before the first run and again after the last that its copy is byte-identical to the file at `9a29bad3`. The staged install and the fixtures are taken from that commit the same way, with `git archive`, and not from the working copy.

It is run on every text the evaluation judges:

- a control row's `work/input.md` → `anatomy-input.json`, and its returned text `delivered.md` → `anatomy-delivered.json`;
- a Write row's delivered draft `delivered.md` → `anatomy-delivered.json`. The source package is a brief, not an article, so no input measurement exists for a Write row and no `anatomy-input.json` is written there;
- a pipeline Redline row's `work/input.md` and `delivered.md`, as for a control.

Where a Write run stopped undelivered, the evaluator copies the last draft from `evidence/` to `last-draft.md` beside `work/` and measures it as `anatomy-last-draft.json`; `delivered.md` and `anatomy-delivered.json` are then absent, which is what a stopped run means.

The JSON files are kept beside the run and their figures are quoted as the evidence for every counted line of `G2`, `W1` and `R1`. **A judge is handed those figures and counts nothing itself**, and where a count it needs is not in the file it says so rather than producing one.

## Two judges per artefact

Every delivered draft and every Redline reply is judged by two independent fresh subagents, each blind to the other, to this ticket, to the model identity and to any wording of the expected outcome beyond the criterion text and — for a control — the row's frozen expectation. The briefs are beside this file:

| Brief | Judges | Criteria |
| --- | --- | --- |
| [`write-judge-brief.md`](write-judge-brief.md) | the delivered draft of rows 9 and 11, with `work/source.md` available | `F1 G1 G2 P1 W1 L1 L2` |
| [`redline-control-judge-brief.md`](redline-control-judge-brief.md) | the reply of rows 1–8, against the row's frozen expectation | `G1 G2 P1 W1 L1 L2 R1` |
| [`redline-pair-judge-brief.md`](redline-pair-judge-brief.md) | the reply of rows 10 and 12, with the source available for one separate question | `G1 G2 P1 W1 L1 L2 R1` |

The two judges of one artefact write `judgement-a.md` and `judgement-b.md` in its run directory and are dispatched together, so neither can read the other's file. A control's frozen expectation is the corpus README row's *Frozen expectation and rejection* cell, copied verbatim by the evaluator to `expectation.md` in the run directory and named to the judge by that path; it is never pasted into the brief, so the brief stays the same for all eight controls.

**Where the two split on a criterion**, both readings are recorded and neither judge is the oracle. The criterion's line reads `fail` where the dissenting judge names one of the protocol's five unconditional rejections and the artefact bears it out, and otherwise reads the evaluator's own verdict, with both readings named in the evidence sentence and the dissent in `notes`.

**One judge suffices for a mechanical check** — byte identity, a count, the presence of a report, an exit code, wall time. `O1` and the script's verdict are of that kind and have no judge at all.

## Inventory scope

`O1` and the `side effects` field are read from a `sha256` inventory taken before and after, never from a run's report of itself. `inventory.sh` beside this file writes one sorted `sha256  path` line per regular file and skips nothing. The scope is every writable location staged for the run:

1. **The run directory**, including `work/` and its `scratch/`.
2. **The staged install** at `.../eval-stage/skills/`.
3. **The rest of the session scratchpad** at `/private/tmp/claude-501/-Users-thomas-Projects-skills/1152bc7f-820e-46e3-b676-a0818805225f/scratchpad/`, other rows' directories among them.
4. **The repository working copy** at `/Users/thomas/Projects/skills`, which every turn tells the run not to read.

Scopes 1 and 2 are inventoried immediately before each run's turn is dispatched and immediately after its reply arrives, and land in that run's `inventory-before.txt` and `inventory-after.txt`. Scopes 3 and 4 are inventoried once around each parallel wave, into `wave-<n>-before.txt` and `wave-<n>-after.txt` beside `runs/`. Scope 4 is covered by `git -C /Users/thomas/Projects/skills status --porcelain --untracked-files=all` and `git rev-parse HEAD` rather than by hashing the tree, because the tree carries another session's work in progress and a hash of it would report that session's edits as this run's; that substitution is a declared narrowing of the protocol's wider scope and is stated in both records.

Because one staged install serves a whole wave, a change under scope 2 or 3 during a wave cannot be attributed to one run of that wave. Such a change is named in the `side effects` field of every entry in the wave and in `notes`, and the narrower per-run scope is not used to explain it away. That is the lesson of `records/write-claude-2026-08-26.md`, which became #180.

## What each run directory holds

```text
runs/<row>/                    a control row; a pipeline row has write/ and redline/ of this shape
  work/                        the run's working directory
    input.md | source.md       the only input exposed to the run
    scratch/                   the only scratch the run may create
  response.md                  the user-facing reply, verbatim
  delivered.md                 the returned or delivered text, extracted from the reply
  evidence/                    the source-check scratch (Write only)
  expectation.md               the row's frozen expectation (controls only)
  anatomy-input.json           the script on work/input.md (not written for a Write row)
  anatomy-delivered.json       the script on delivered.md
  inventory-before.txt
  inventory-after.txt
  judgement-a.md
  judgement-b.md
```

A Redline reply that changes nothing still gets a `delivered.md`: it is a byte copy of `work/input.md`, and the entry's `observed delivery` says `no change`.

## What is fixed before any result exists

No criterion is softened to fit a result, no fixture is edited, and no wording of either Skill or of the Library is changed here. Nothing frozen under `docs/evaluation/` is edited. The rows, the invocations, the criteria, the seat, the briefs, the inventory scope and the script's role above are settled by this file, and a run that could not be staged or judged as written is recorded as it fell and its remaining miss filed as its own ticket.
