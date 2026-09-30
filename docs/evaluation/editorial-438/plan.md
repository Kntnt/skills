# Plan for #438: what a quotation bridge may carry is stated where the writer reads

Frozen on 2026-09-30, before the first run of any arm. Nothing in this file is edited after the first run, and the judge brief it names, [`../editorial-396/write-judge-brief.md`](../editorial-396/write-judge-brief.md), is used as it stands, byte for byte.

**`<start>` is `2afeb95e`**, the head of the branch `kntnt-orchestrate/main/438` when the build began and before this file was committed. The pre-change arm is staged from it, and so is the corpus every run reads.

The requirement is the ticket's thread as it stood on 2026-09-28: the body, the triage comment of 15:07 UTC and the readiness addendum of 18:46 UTC. Where they conflict the later one stands. Both `#396`'s plan, from which this one copies its method, and the readiness addendum's *Staging* clause, which replaces the ticket's earlier "as for #429", are followed as written.

## What this evaluation is

A control, not a reproduction. `docs/evaluation/editorial-364/` and ADR-0214 measured the sentence *"A bridge should prepare a quotation rather than pre-say it."* in the Claude family and found the fault it guards against does not reproduce there. This ticket rests on the pair rule (`docs/rules/skills.md`, the editorial README's `## Review extensions`), not on a reproduced miss, so:

- The `pre` arm is not read for a defect. A `pre` arm with no quotation bridge classed (a) is the expected reading.
- The protocol's not-reproduced exit is not this ticket's in any outcome. No result is recorded as "not reproduced" and no decision record is written.
- Shipping is conditional on the two controls below, as the triage comment says (*The candidate ships if*). The protocol's fallback that lets a failed revised candidate ship for beating the pre-change arm on a target criterion does not apply, because the ticket has no target criterion.

## What is built, and when

The change is one rewrite in `skills/kntnt/library/references/editorial/genres/casestudy.md`, in the paragraph that opens *"Let attributed quotations carry the customer's experience and judgement"*: the sentence *"A bridge should prepare a quotation rather than pre-say it."* is replaced where it stands, and the paragraph's other two sentences stay byte for byte. The new wording stays at *should*, says *quotation bridge* every time, does not repeat `headlines.md`'s definition of the term, and states:

- that a quotation bridge carries the speaker, the occasion or the question the quotation answers where the material gives one, and any fact the quotation does not itself give;
- that it does not carry the quotation's judgement, figure or concession;
- a reader test in the form `headlines.md` gives the subheading over a quotation and `article-anatomy.md` gives the lead: a reader who has just read the quotation bridge meets the quotation as new material, never as the quotation bridge said again.

`genres/casestudy.review.md` and `headlines.md` stay byte for byte as at `<start>`. The change ships with its tests in `tests/test_kntnt.py` and the regenerated catalog. The exact wording of each candidate is recorded in `results.md` with its commit. The candidate is committed before any post-change run is staged, and the `pre` arm reads none of it, because every run stages its install from a commit with `git archive`.

## How a run is made

Every Write run is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from the repository root:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=2afeb95e \
  --invocation='/write --genre=casestudy --language=<lang> --output=response source.md' \
  --input=<input> --input-name=source.md \
  --output=<scratch>/runs/<arm>/<row>-r<n> \
  --model=claude-opus-5-5 --effort=high
```

`<commit>` is `2afeb95e` for arm `pre`, the committed candidate for arm `post`, and the committed revised candidate for arm `revise`. The genre is passed on the invocation as the installed name `casestudy`; the staged inputs carry no `kntnt` map and no `genre:` metadata and are not edited. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, starts one top-level `claude --print` session there with its own `HOME`, and keeps the Harness trace, the reply and before-and-after inventories in the packet. The prompt is the Formal Invocation and nothing else.

`<scratch>` is this build's scratch directory, `.git/kntnt-orchestrate/438.scratch`. Packets are written there and copied into this directory's `runs/<arm>/<row>-r<n>/` only after they are judged. A void run (see *Void runs* below) is moved whole to `voided/` here before its row is run again.

**The seat.** Each run is `claude-opus-5-5` at high deliberation, the identity `run.json` requests and `trace-index.json` records. Each judge is a fresh `kntnt-opus-high` subagent, which launches `claude-opus-5-5` at high deliberation.

**No two runs on one input at a time** (#401). The two control rows share one input, so the runs of an arm go in two lanes, each one run after another: lane 1 is the three `case-question-en_GB` runs, and lane 2 the four control runs. The lanes run side by side. Arms are run one after another, not side by side.

## The matrix

The same seven runs in each arm. No Redline run of any kind is made.

| Row | Input | `<lang>` | Runs per arm |
| --- | --- | --- | --- |
| `case-question-en_GB` | `../editorial-329/followup/runs/account-candidate/case-question-en_GB-r1/write/supplied-input.md`, SHA-256 `75160dbc12d41294eccfc615f4a8e1b2df1b5202185f5ba1f24a2f3d5fd69afc` | `en_GB` | 3 |
| `case-study-en_US` | `../corpus/editorial-quality/sources/case-study.md`, SHA-256 `75188596831d5a0a28364ea4da4d1053f69900ca25237f08859696058c579f11` | `en_US` | 2 |
| `case-study-sv` | the same file | `sv` | 2 |

Both hashes were checked against the files at `2afeb95e` before this plan was committed.

## Arms and run counts

These are all the runs this evaluation makes:

| Arm | Staged from | `case-question-en_GB` | `case-study-en_US` | `case-study-sv` | Write runs | Judgements |
| --- | --- | --- | --- | --- | --- | --- |
| `pre` | `2afeb95e` | 3 | 2 | 2 | 7 | 14 |
| `post` | the committed candidate | 3 | 2 | 2 | 7 | 14 |
| `revise`, only where `post` fails the ship rule | the committed revised candidate | 3 | 2 | 2 | 7 | 14 |

The revise round reruns the whole matrix. Both controls are totals over every draft in an arm, set against the pre-change arm's total, so the subset that failed is the whole arm, which keeps to the protocol's "no larger than the subset that failed". The `revise` arm is read in place of `post`, against the same `pre` arm, which is not rerun.

## What the judges are asked, and given

[`../editorial-396/write-judge-brief.md`](../editorial-396/write-judge-brief.md) is used as it stands. Bridges are therefore classed (a), (b) or (c) on #364's frozen definition under point 4, and each subheading standing over a quotation is classed **pre-echo**, **prepares** or **neutral** under point 4b. The brief names no path and no seat, so nothing is substituted in it.

Every draft is read by two judges, A and B. Each judge is a fresh `kntnt-opus-high` subagent and gets a directory of its own under `<scratch>`, named by a random token that names neither the arm, the row nor the run, holding:

- `work/source.md`: the packet's `supplied-input.md`;
- `response.md`: the packet's `response.txt`;
- `delivered.md`: the draft alone, as `response.txt` carries it, with Write's code fence and delivery account taken off and nothing added. It is left out where the run delivered nothing.

Nothing else from the packet goes in, because `run.json`, `transcripts/` and `trace-index.json` name the model and the revision. The judge writes `judgement.md` in its own directory and keeps any scratch there; the file is copied into the packet it judged as `judgement-a.md` or `judgement-b.md`. With no report files, the judge answers the brief's point 6 from the findings the reply mentions, as the brief provides. The scratch directory's own path carries this build's number, which is not the arm; the judge is told nothing of what the number is. A judge is told the brief's path, its own directory and where to write, and nothing of the hypothesis, the arm or the ticket.

## How it is counted

Both counts are per-arm totals, and both arms are counted by the same rule.

- **Quotation bridges classed (a).** For each arm, the total, over every draft, of the point-4 count of bridges classed (a), adding up both judges.
- **Subheadings over a quotation counted as a pre-echo.** A subheading counts once. It counts as a pre-echo when either judge classes it pre-echo under point 4b, a split included, against any quotation under it. Both classes are recorded on a split (#364's split rule: "Where they split, both classes are recorded, no judge is an oracle, and the row counts as unmet."). The total is added up over all three rows of the arm.

## The ship rule

The candidate meets it when both of these hold, its arm read against the `pre` arm:

1. the candidate arm's total of quotation bridges classed (a) is not higher than the `pre` arm's;
2. the candidate arm's total of subheadings counted as a pre-echo is not higher than the `pre` arm's.

Where the `pre` arm's total is 0, the candidate arm's total must be 0 too. F1, G2 and L1 are judged and recorded on every draft, as the brief asks, and are not this ticket's criteria.

## What ships, in every outcome

1. **`post` meets the ship rule.** The candidate ships: the `casestudy.md` change, the test changes and the regenerated catalog.
2. **`post` misses it.** One revise round is taken. The revised wording is committed, the `revise` arm is run over the whole matrix, and it is read in place of `post`. Where it meets the ship rule, it ships as in 1.
3. **`revise` misses it too.** Nothing ships. `genres/casestudy.md` and `tests/test_kntnt.py` end byte-identical to `<start>`, the candidate commits being reverted and not left in place; the result is recorded as measured; each failed control is filed as its own `needs-triage` issue naming #438; no decision record is written, and ADR-0214 stands as the account of the Claude-family measurement; the ticket is done.

No criterion is softened to fit a result, the corpus is not edited, and no arm is re-run to get a better reading.

## Void runs

A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; its output is kept under `voided/` and not deleted. A run that completes and stops is a finding and is judged from the last draft the reply carries.

**Whose miss.** A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one, with both judges' readings recorded (the protocol's *Whose miss*). The two controls above are this ticket's only criteria.

## What is not measured

- The GPT family. The retest stays #395's, Thomas's hand step, and it measures whatever wording this ticket ships.
- The rule's effect on the review half: no Redline run is made.
- `T1` and `R2` are not criteria here. Each packet keeps its trace, so they can be judged from it later.

## What is written

This file, committed before the first run; `results.md` beside it with each arm's two totals, whether the ship rule was met, which of the three outcomes was taken, and the wording of each candidate with its commit; the judged packets under `runs/<arm>/`; any void run under `voided/`; and one record, `../records/write-claude-<date>-438.md`, in the protocol's format. Its line for `../records/README.md` and the changelog entry are written to `.kntnt-orchestrate/438.md` for the run to apply.
