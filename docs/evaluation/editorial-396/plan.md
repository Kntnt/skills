# Plan for #396: a subheading standing over a quotation does not pre-say it

Frozen on 2026-09-24, before the first run of either arm and before any product change. Nothing in this file or in [`write-judge-brief.md`](write-judge-brief.md) is edited after the first run.

**`<start>` is `385976f7`**, the head of the branch `kntnt-orchestrate/main/396` when the build began and before this file was committed. The pre-change arm is staged from it, and so is the corpus every run reads.

The requirement is the ticket's thread as it stood on 2026-09-23: the body, the triage addendum of 2026-09-22, the correction of 2026-09-23 on the load chain, and the two readiness addenda of 2026-09-23 19:42 and 19:49 UTC. Where they conflict the later one stands, so the second readiness addendum's withdrawal of *Items 3 and 4 do not undo Thomas's ruling* holds here: rules 3 and 4 below apply exactly as written.

## The failure

`docs/evaluation/editorial-364/` measured `main` at `218e3be1` on `claude-opus-5`. In two of its three `case-question-en_GB` drafts the bridge into the closing quotation was clean, and the section heading above it already said what the quotation says:

- `case-question-en_GB-r2`: **"Vale would use the schedule again for new jobs"**
- `case-question-en_GB-r3`: **"Vale would allow an extra week for the status names"**

over *"I would use it again for new jobs. I would allow another week to check the status names before adding the backlog."* Both judges of `r3` reported it unprompted. `headlines.md` line 31 — word a subheading from its whole section, in words its first sentence does not use — is met by such a subheading, and nothing in the shipped contract pairs a subheading with the quotation standing under it.

That evaluation is history for this one and not its comparison: it ran on another model and before `09fb8991` changed what Write loads. The comparison is the pre-change arm below, run in this evaluation from `<start>`, on the same seat and inputs as the post-change arm.

## What is built, and when

Only after the pre-change arm has been judged and the defect reproduced (see *Reproduced*). The addendum fixes what the candidate does, and its exact wording is written after the pre-change arm and recorded in `results.md` with its commit:

- `skills/kntnt/library/references/editorial/headlines.md` states that a subheading standing over a quotation may not pre-spend the judgement, the figure or the concession the quotation is there to carry, and its line-31 instruction can no longer be met by a subheading that says what a quotation under it says. It defines the quotation bridge — the narrative sentence or clause that stands immediately before a quotation and leads the reader into it, including a speech tag that carries anything besides the attribution — and says that a subheading standing over a quotation is outside the quotation bridge and governed by the subheading rule.
- `headlines.review.md` lists such a subheading in its *Avoid* list.
- The sweep: Write `SKILL.md` step 7, Write `help.md` line 21, Redline `references/correction.md` line 35, and `skills/kntnt/library/references/editorial/README.md`'s paragraph on `headlines.md`.
- Unchanged: `CONTEXT.md`; `case-study.md` line 17 byte for byte; `case-study.review.md`; `article_anatomy.py`. No new or changed shipped sentence uses a bare "bridge", because `CONTEXT.md` gives **Bridge** another meaning.

## How a run is made

Every Write run is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from the repository root:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=385976f7 \
  --invocation='/write --genre=case-study --language=<lang> --output=response source.md' \
  --input=<input> --input-name=source.md \
  --output=<scratch>/runs/<arm>/<row>-r<n> \
  --model=claude-opus-5-5 --effort=high
```

`<commit>` is `385976f7` for arm `pre`, the committed candidate for arm `post`, and the committed revised candidate for arm `revise`. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, starts one top-level `claude --print` session there with its own `HOME`, and keeps the Harness trace, the reply and before-and-after inventories in the packet. The prompt is the Formal Invocation and nothing else; #364's turn file and its four evaluator additions are not used.

`<scratch>` is this build's scratch directory. Packets are written there and copied into this directory's `runs/<arm>/<row>-r<n>/` only after they are judged. A void run (rule 8 below) is moved whole to `voided/` here before its row is run again.

**The seat.** Each run is `claude-opus-5-5` at high deliberation, the identity `run.json` requests and `trace-index.json` records. Each judge is a fresh `kntnt-opus-high` subagent, which launches `claude-opus-5-5` at high deliberation.

**No two runs on one input at a time** (#401). The two control rows share one input, so the runs go in two lanes, each one run after another: lane 1 is the three `case-question-en_GB` runs, and lane 2 the four control runs. The lanes run side by side.

## The matrix

The same seven runs in each arm. No Redline run of any kind is made.

| Row | Input | `<lang>` | Runs per arm |
| --- | --- | --- | --- |
| `case-question-en_GB` | `../editorial-329/followup/runs/account-candidate/case-question-en_GB-r1/write/supplied-input.md`, SHA-256 `75160dbc12d41294eccfc615f4a8e1b2df1b5202185f5ba1f24a2f3d5fd69afc` | `en_GB` | 3 |
| `case-study-en_US` | `../corpus/editorial-quality/sources/case-study.md`, SHA-256 `75188596831d5a0a28364ea4da4d1053f69900ca25237f08859696058c579f11` | `en_US` | 2 |
| `case-study-sv` | the same file | `sv` | 2 |

## What the judges are asked, and given

[`write-judge-brief.md`](write-judge-brief.md) is `../editorial-364/runs/write-judge-brief.md` with two changes and no others: point 4b, *Subheadings over quotations*, inserted after point 4 in the ticket's words, and the closing reply line asking for point 4b's per-class counts. Bridges are therefore classed (a), (b) or (c) on #364's frozen definition, and each subheading standing over a quotation is classed **pre-echo**, **prepares** or **neutral**.

Every draft is read by two judges, A and B. Each judge gets a directory of its own under `<scratch>`, named by a random token that names neither the arm, the row nor the run, holding:

- `work/source.md`: the packet's `supplied-input.md`;
- `response.md`: the packet's `response.txt`;
- `delivered.md`: the draft alone, as `response.txt` carries it, with Write's code fence and delivery account taken off and nothing added. It is left out where the run delivered nothing.

Nothing else from the packet goes in, because `run.json`, `transcripts/` and `trace-index.json` name the model and the revision. The judge writes `judgement.md` in its own directory and keeps any scratch there; the file is copied into the packet it judged as `judgement-a.md` or `judgement-b.md`. With no report files, the judge answers the brief's point 6 from the findings the reply mentions, as the brief provides. The scratch directory's own path carries this build's number, which is not the arm; the judge is told nothing of what the number is.

## How it is counted

**A subheading** counts once. It counts as a pre-echo when either judge classes it pre-echo against any quotation under it. Where the two judges split, both classes are recorded and the subheading counts as a pre-echo — #364's split rule: "Where they split, both classes are recorded, no judge is an oracle, and the row counts as unmet." A row's count is the number of its subheadings counted as a pre-echo, over all its drafts.

**Bridges.** For each arm, the total of bridges classed (a) under point 4, adding up every draft's count from both judges.

Both arms are counted by the same rule.

## Criteria

- **Reproduced.** The defect reproduces when at least one pre-change `case-question-en_GB` draft carries a subheading counted as a pre-echo.
- **Pass** (the target criterion). In the post-change arm no `case-question-en_GB` draft carries a subheading counted as a pre-echo, and that row's count is lower than in the pre-change arm.
- **Control rows.** Neither `case-study-en_US` nor `case-study-sv` has a higher count in the post-change arm than in the pre-change arm. A control row passes outright when none of its drafts carries one.
- **Bridge total.** The post-change arm's total of bridges classed (a) is not higher than the pre-change arm's. The table in `../editorial-364/results.md` is not the comparison. This control counts as passed in the pre-change arm.

F1, G2 and L1 are judged on every draft as the brief asks and recorded; they are not this ticket's criteria.

## Exit

1. **Not reproduced.** Where no pre-change `case-question-en_GB` draft carries a subheading counted as a pre-echo, the result is recorded as not reproduced, no candidate is written, no product file changes, and a decision record says so under the number reserved for this ticket, `0221`, as ADR-0212 did for #363 and ADR-0214 for #364.
2. **The candidate.** Where the post-change arm meets *Pass* and both controls, the candidate ships.
3. **One revise round**, at most, where it does not. The revised candidate is committed and the whole matrix — the target row and every control, seven runs — runs again as arm `revise`, and the pass and control criteria are read over that arm in place of the first candidate arm. It then ships where it meets them. Where it does not, it ships only if it beats the pre-change arm on the target criterion and no control that passed in the pre-change arm fails in its arm; otherwise the product stays as it is at `<start>`.
4. Either way the result is written as measured, each remaining miss is filed as its own `needs-triage` ticket naming #396, and the ticket is done. Where a post-change draft still carries a subheading counted as a pre-echo after any revise round, that ticket names extending `article_anatomy.py`'s `heading_pairs` to pair a subheading with each quotation under it as a repair to weigh.

No criterion is softened to fit a result, the corpus is not edited, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A run that completes and stops is a finding and is judged from the last draft the reply carries.

**Whose miss.** A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one: #397 (paratext authored into a finished text), #398 (the claim account's assurance), #400 (a paratext change accounted for as something else), #402 (anatomy conformance reported unexamined) and #415 (an unhedged assertion mounted above a kept limit). Both judges' readings are recorded; where they split, the split rule above decides.

## What is not measured

- The rule's text is general and Write loads `headlines.md` for `article`, `column` and `opinion` as well; those three genres are not run.
- No Redline run is made, so the Redline-side changes — `headlines.review.md`, `correction.md` — are unmeasured.
- `T1` and `R2` are not criteria here. Each packet keeps its trace, so they can be judged from it later.

## What is written

This file and the judge brief, committed before the first run; `results.md` beside them with the outcome, whichever way it falls, including whether `docs/rules/docs.md`'s three criteria for a decision record hold and which; the judged packets under `runs/<arm>/`; any void run under `voided/`; and one record, `../records/write-claude-<date>-396.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
