# T1 and R2, assigned from the trace

What this establishes is that the two criteria are **observable**. It judges `T1` and `R2` on two runs and judges nothing else: no other criterion is scored, no record is written, and neither run is an evaluation of Write or Redline. A Skill failing one of these lines here would be a defect filed against that Skill, not a fault in the method.

Every citation below is to [`trace-index.json`](README.md) in the run's own packet — an agent by its id, a call by its `ordinal`, a file by the `file_activity` entry that established it. Nothing is taken from either run's reply.

## Conditions common to both runs

- **harness** — Claude Code 2.1.278, one `claude --print` session per run, started by [`harness/staged_run.py`](harness/staged_run.py).
- **model** — `claude-opus-5` at `high`, requested and observed: every turn of both sessions and of all three nested agents carries that Seat, from each agent's own `seats`.
- **instruction revision** — `8a37e57eca854fea39dd25e5d2483e831edfc599`, exported with `git archive` into the run's own installation.
- **corpus revision** — `9a29bad3d0ab5419c687fe04ee965420574dff5d`, the commit that first holds the current editorial-quality matrix.
- **prompt** — the Formal Invocation and nothing else. `contextual-instruction.txt` reads `none` in both packets, and `prompt.txt` is one line.
- **provider isolation** — one Claude session started one Claude Harness. No Codex Harness and no GPT model was started, controlled or invoked.

## `write-web-copy-sv`

`/write --genre=web-copy --language=sv --output=response source.md` over [`sources/web-copy.md`](../corpus/editorial-quality/sources/web-copy.md). Session `1782324b…`, 575 seconds, exit 0, `trace-status.json` `complete`: three agents, 27 calls, no delegation without a child and no child without a delegation.

### T1 — `pass`

**Resolved configuration.** Genre `web-copy` and language `sv` come from the Formal Invocation, which `invocation.txt` holds verbatim; the run's own draft carries the map `genre: web-copy`, `technique: none`, `language: sv` (call 8). The language was verified rather than assumed: call 4 runs `languages.py resolve --scope=composition "sv"` — the composition scope alone, which is the scope Write is contracted to.

**Actual loaded files.** Everything the session opened under the staged installation, the Skill's own body included:

| Where | File | How |
|---|---|---|
| `skill_bodies` | the `write` body, 14891 characters, from `…/skills/write` | the Harness's own record of which installation answered the invocation |
| call 1 | `write/scripts/invoke.py` | run through the shim, as the body instructs |
| call 3 | the `genres/`, `techniques/`, `editorial/` and `references/` directories | listed, so `exact: false`: a listing says what is installed and opens none of it |
| call 5 | `references/editorial/base.md` | `exact` |
| call 6 | `references/editorial/genres/web-copy.md` | `exact` |
| call 7 | `references/editorial/web-craft.md` | `exact` |
| call 9 | `write/references/source-check.md`, `references/delivery.md` | `exact` |

Every other entry of `file_activity` is the run's own material — `work/source.md`, `scratch/draft.md`, the two check directories — or a `mktemp` template. Nothing else under the installation was opened.

**No technique was inferred from shape.** The techniques directory is listed at call 3 and no resource under it is ever opened. `web-copy` states *The technique this genre is ordinarily written with: None*, so level 6 of the precedence supplies nothing and the default stands — and the map the run wrote says `none`, which is the value rather than a gap.

**Only the selected genre was loaded.** `genres/` is listed at call 3; the one genre file opened is `web-copy.md`. No second genre resource appears anywhere in `file_activity`, so no opening of one was read past.

**Nothing outside the bounded contract was loaded.** No `.review.md` of any resource, no `anti-slop.md`, no `mechanics.md`, and neither `article-anatomy.md` nor `headlines.md` — which is correct rather than a gap: `web-copy` is not one of the four article genres those two are loaded for.

### R2 — `pass`, at Write's boundary

**Full scoped contract loading** is the table above: the base contract, the selected genre, the shared craft brief the genre links, and the composition scope the resolver returned. Nothing else.

**Fresh comparison agents, and the budget.** Write's verification is two comparisons at most, each made by an agent started fresh. The trace holds exactly two, both linked to the call that started them and both at `spawn_depth` 1:

- call 13 at `05:53:47.905Z` → agent `a99c24b5759a19123`, which reads `check1/draft-to-check.md`, `check1/material-source.md` and `check1/context.md` and writes `check1/report.md`, and nothing else.
- call 16 at `05:57:26.581Z` → agent `a99f298e6c0320811`, the same three files under `check2/` and `check2/report.md`.

Each carries its own instruction verbatim and reads only the three files it was handed, which is what *fresh* means here: neither opened the other's directory, the draft outside its own copy, or any part of the installation.

**Re-review between them, in that order.** Call 14 reads `check1/report.md` at `05:56:31`; call 15 rewrites `scratch/draft.md` at `05:57:10`; call 16 starts the second comparison at `05:57:26`. So the repair sits between the first report and the second reading of the text, and the second agent read the repaired prose rather than the draft the first one saw. Call 18 then runs `cmp draft.md check2/draft-to-check.md`, which is the run establishing for itself that the prose it delivers is the prose the last comparison read.

**No review half and no peer editorial pass.** The session never opened Proofread's or Redline's installation, and `skill_bodies` holds one entry, `write`. Write is contracted to stop before either, and the trace shows it stopping.

## `redline-web-copy-flawed`

`/redline --genre=web-copy --language=en_US --output=response input.md` over [`controls/web-copy-flawed.md`](../corpus/editorial-quality/controls/web-copy-flawed.md). Session `b5e09114…`, 337 seconds, exit 0, `trace-status.json` `complete`: two agents, 25 calls.

### T1 — `pass`

Genre `web-copy` and language `en_US` come from the Formal Invocation; the control carries no `kntnt` map, so no lower level was reached. Call 5 runs `languages.py resolve --scope=composition --scope=review --scope=anti-slop "en_US"` — the three scopes Redline is contracted to, and not the mechanics scope, which arrives later and belongs to the closing pass. The techniques directory is listed at call 3 and no technique resource is opened; `genres/` is listed there and `web-copy` is the one genre opened.

### R2 — `pass`

**Full scoped contract loading**, every entry `exact`:

| Call | Files |
|---|---|
| 4 | `references/delivery.md`, `references/invocation-envelope.md` |
| 6 | `references/editorial/base.md` **and** `base.review.md` |
| 7 | `genres/web-copy.md` **and** `genres/web-copy.review.md` |
| 8 | `web-craft.md` **and** `web-craft.review.md` |
| 9 | `anti-slop.md` |
| 10 | `redline/references/correction.md` |

Both halves of each resource, the anti-slop catalogue, and no `mechanics.md` — Redline's step 5 forbids loading mechanics guidance, and the trace shows none until the closing pass resolves its own at call 15.

**A fresh correction, once.** Call 11 at `05:54:05.212Z` starts agent `ac4e06f8cdb919a0f`, `general-purpose`, `spawn_depth` 1, description *Correct web-copy findings*. Its instruction is preserved verbatim and opens *You have not seen this text before, and there is nothing you are expected to remember* — the brief `correction.md` prescribes. It is the only delegation in the run, so the Correction Budget of 1 was spent once and no second round was taken. The agent loaded the contract for itself — `base.md`, `base.review.md`, `genres/web-copy.md`, `genres/web-copy.review.md`, `anti-slop.md`, `web-craft.md`, `web-craft.review.md`, and the language scopes — and wrote `scratch/corrected.md`.

**Re-review after it — the one clause the trace does not carry.** The correction agent ended at `05:55:34.474Z`; the session's next recorded call is 12 at `05:56:31.981Z`, which freezes the post-correction artifact for the closing pass. What the trace establishes is the order and the budget: one round, spent once, its result taken forward. It does not establish that a re-review happened, because a re-review opens no file and runs no command — re-reading a text already in hand leaves no tool call at all. The session's own turn between those two instants says it re-reviewed, and that is a claim rather than a record; `transcripts/parent.jsonl` preserves it verbatim for an evaluator who wants to read it, and this line does not rest on it.

So the `pass` above is a `pass` on four of the criterion's five clauses — scoped loading, a fresh correction, the budget, one closing installed Proofread pass with no substantive edit after it — with the fifth neither established nor contradicted. An evaluator who requires each clause to be independently recorded scores this line `skipped` for that clause and says so, exactly as the protocol's *the trace a criterion is answered from* directs. It is a limit of what a Harness records rather than of this packet, and it is the one such limit these two runs found.

**Exactly one closing installed Proofread pass.** Call 13 reads `proofread/SKILL.md` from the staged installation. Call 14 runs `proofread/scripts/invoke.py` once, with `--language=en_US --output=$MECHDIR/proofed.md $MECHDIR/artifact.md` — flags and two paths, no artifact contents. Call 15 resolves the mechanics scope and reads `mechanics.md`, which is the pass's own contract and is loaded nowhere before it. Call 16 produces `proofed.md` and compares the two by `shasum`. There is no second invocation of that shim anywhere in the trace.

**No substantive edit after it.** Every call after 16 is a read or a removal: call 17 removes the private directory and lists `work/` and `scratch/`, call 18 reads `scratch/corrected.md`, call 19 removes it. `work/input.md` is unchanged by `shasum` at call 17, and `filesystem-changes.json` shows nothing created, changed or removed under `work/` or `scratch/` between the inventories.

**What the trace also shows, and a record would have to say.** The closing pass produced its output by `cp "$MECHDIR/artifact.md" "$MECHDIR/proofed.md"` at call 16 — a no-change mechanical pass, the output byte-identical to its input. That the pass ran, ran once, and ran last is established; whether it *should* have corrected something is `L2`'s question and is not judged here. It is recorded because it is exactly the kind of thing a trace makes visible and a reply does not.

## `interrupted`

The same Write invocation on `claude-sonnet-5` at `low`, stopped by its own 45-second timeout. It is kept as the demonstration that an incomplete run is reported as one and preserved as one:

- `result.json` — `returncode` 143, `timed_out` true, `process_group_gone` true. The run's whole process group was ended and nothing of it survived.
- `trace-status.json` — `incomplete`, for `run-did-not-finish`, with the parent transcript present and no line unparsable.
- `trace-index.json` — the 12 calls the run had made by then are all there, including `base.md`, `genres/web-copy.md`, `web-craft.md` and `delivery.md`, so the partial evidence is readable rather than discarded.
- `cleanup.json` — the one private root, removed.

A trace this short answers neither criterion, and the point is that it says so rather than reading as a `pass` with nothing behind it. The other two ways a trace comes up short — a child that is not there, a record that ends mid-write — are in [`checks.md`](checks.md), made over the Redline packet's own material.

## What the method still cannot see

- **Inside a shell command.** A `cat` of one named file is as strong as a `Read`; a `grep -r`, a glob, or a path built from a command substitution names a request rather than a file, and the entry says so with `exact: false`. In both runs above every contract-loading entry is `exact`, so the limit does not bear on these two verdicts.
- **What a loaded file was used for.** The trace says a file was opened; whether the run then followed it is the artifact's question, which is what the other criteria are for.
- **A step that touches nothing.** A review, a re-review and a judgement open no file and run no command, so they reach the index only as the gap between two calls. The turns themselves are in `transcripts/parent.jsonl`, and a criterion resting on one is read there rather than off the index.
- **A tool result the Harness truncated.** The transcripts hold what the Harness kept. Where a result was offloaded, `transcripts/extra/` holds it; where it was truncated, the index reports `result_chars` against the excerpt it shows.
- **An effect outside the private root.** The inventories cover the root. The Redline run wrote `/tmp/redline_mechdir_388.txt` and removed it at call 17 — visible in the trace, absent from the inventories, and gone from the machine. A criterion about side effects still reads the working copy as well as the packet.
