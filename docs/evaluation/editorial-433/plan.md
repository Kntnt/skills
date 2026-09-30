# Plan for #433: a correction round returns no heading that repeats what it stands over

Frozen on 2026-09-30, before the first run of either arm and before any product change. Nothing in this file, in the judge brief beside it, or in `runs/matrix.tsv`, `runs/wave.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md), its staging section above all, and [the corpus](../corpus/editorial-quality/README.md) first, then [#402's plan](../editorial-402/plan.md), whose method this one copies in the parts listed under *What this plan copies from #402's*; this file says only what those leave open and what #433 settles differently.

**`<start>` is `2afeb95e`**, the head of the branch `kntnt-orchestrate/main/433` when the build began. It holds #429's change (merged in `0fe8b9f4`) and #439's staging section in the protocol. It is "the tree #429 leaves", and the pre-change arm is staged from it and from no other commit. **The corpus commit is `2afeb95e` too.** Both arms read their inputs and their frozen expectations from it. This ticket's diff does not touch the corpus.

The requirement is the ticket's whole thread as it stood on 2026-09-30: the body, the triage comment of 2026-09-28 15:07 UTC, the readiness addendum of 2026-09-28 18:49 UTC and readiness addendum 2 of 2026-09-28 19:02 UTC. Where they conflict, the later one stands. Thomas's ruling in the triage comment is not open here: step 7's whole-round rejection stays exactly as #389 decided it, and the fix goes where the loss starts, in the correction agent's headings.

## What this plan copies from #402's

Copied, with this build's start commit, genre names and paths substituted:

- *How a run is made*, whole.
- *Judging*, whole, except its pointer for `opinion-flawed` to `../editorial-383/runs/control-opinion-flawed/expectation.md`.
- From *Criteria, fixed before the runs*: the `R1` and `C1` line, the `O1` and `S1` lines, the sentence recording every other criterion `skipped`, and the first paragraph of *When `C1` is met*, which is the split rule.
- *Inventory scope*, whole, with this build's scratch root, working tree, session scratchpad and worktree list.
- From *Exit*, the **Void runs** paragraph and the sentence opening "No criterion is softened".
- From *The matrix*, the waves rule in this form: runs are dispatched in waves of at most four, each run in a wave on a different row.

Replaced by this plan's own sections, and not copied: #402's opening two paragraphs; *What is under test*; *The matrix*, by *Arms, rows and counts*; the paragraph under *When `C1` is met* opening "**The ending clause of `opinion-flawed`**", by *When a run delivers the ending*; *What the ticket's criteria read*, with its *What each reply says about conformance*, by *When a run delivers the ending* and *The controls, read*; *Exit*, apart from the two pieces above, by *What ships, for every outcome*; *What is not measured*, which has no counterpart here because Write loads neither file this ticket changes; and *What is written*, by this plan's own.

## What is under test

`opinion-flawed` ends `Nu är det dags att agera.` inside `## Diskussion`, the section that carries its argument. In #402's three runs of it, and in #429's two, the correction round wrote a repair of that ending and the re-review rejected the whole round, as step 7 requires, because a headline or subheading the correction agent had just written repeated what it stands over: the lead's first sentence, the call to action under a new ending subheading, or the start of its section. The delivered text came back as received, and its ending stayed inside the argument.

The fix goes in the correction agent. The candidate changes these four files and, by regeneration, `skills/kntnt/catalog.json`:

1. **`skills/editorial/redline/references/correction.md`.** Every headline and subheading the agent wrote or changed in the round is read against what it stands over: the headline against the standfirst where the text has one and otherwise the lead's opening, which the agent reads itself where `article_anatomy.py` reports the `headline-standfirst` pair with `following` set to `null`; a subheading against the first sentence of its section and any quotation in it. One that says the same thing again is reworded from the whole text's or the section's angle, within the brief's existing limits. Where it cannot be worded without repeating: a heading a finding asked the agent to repair is restored exactly as received and that finding is returned unresolved with the reason; a heading the agent changed for any other reason is restored exactly as received and the echo it could not avoid is reported with the pair and the reason; a heading the round would have to create, such as the subheading of a new ending section, is not created, the text there is left as received, and the finding that asked for it is returned unresolved with the reason. A heading the round creates names who decides or what is decided, and leaves the act to the sentence under it. An unrelated pre-existing echo still stays as received and is reported.
2. **`skills/kntnt/library/references/editorial/article-anatomy.review.md`.** The sentence `df6bb4a1` added and `0d015bdc` reverted, or one saying the same two things, goes back after the sentence about closing content that stands inside a last section carrying the argument: the new ending subheading does not say again what the paragraph under it says, and over an ending of one call to action it names what is decided or who decides it, leaving the act to the sentence.
3. **`tests/test_kntnt.py`.** `test_the_review_extension_repairs_an_ending_standing_inside_the_argument` asserts that wording again.
4. **`skills/editorial/redline/help.md`.** Its sentence on how correction agents treat echoes is brought into line with item 1.

Nothing under `skills/editorial/unslop/` changes, `article_anatomy.py` does not change, and step 7 of Redline's `SKILL.md` is not touched. The candidate's exact wording is written after the pre-change arm has been run and judged in full, and is recorded in `results.md` with its commit.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

Every Redline run, of both arms and of any revise round, is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree by [`runs/wave.sh`](runs/wave.sh):

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=2afeb95e \
  --invocation='<invocation from runs/matrix.tsv>' \
  --input=<scratch>/inputs/<row>.md --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation. The dispatching session is itself `claude-opus-5-5`.
- **The installs.** `<commit>` is `<start>` for the pre-change arm, the committed candidate for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, laid out so that the shim finds `HERE.parent / "kntnt"`. The candidate is committed before its install is staged.
- **The inputs.** `<scratch>/inputs/<row>.md` is `git show 2afeb95e:docs/evaluation/corpus/editorial-quality/controls/<row>.md`, written once before the row's first run. The invocation is the whole prompt; no turn file is sent, because the Skill is installed rather than named by path.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after both judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/433.scratch`.
- **No two runs on one input at a time** (#401). This build makes at most one run of a row at once. A run's correction subagents write inside its own private root, so a run of this build and a sibling build's run of the same row cannot collide in a shared scratchpad.
- **The staged runner's use.** It is used because it is the one way from this seat to give Redline a session that can start its correction subagents, as this ticket's first readiness addendum states. No criterion here is answered from the trace it keeps.

## Arms, rows and counts

These are exhaustive, and [`runs/matrix.tsv`](runs/matrix.tsv) lists every run by wave, name, arm, row and invocation.

| Row | SHA-256 (first 16) | Invocation | Pre-change arm | Candidate arm |
| --- | --- | --- | --- | --- |
| `opinion-flawed` (target) | `ab033d9f4c817c9e` | `/redline --genre=opinion --language=sv --output=response input.md` | 3 runs | 3 runs |
| `article-flawed` (control) | `1c0e3b3ef98e06b2` | `/redline --genre=article --language=sv --output=response input.md` | 1 run | 1 run |
| `case-study-flawed` (control) | `ce574061bd09328e` | `/redline --genre=casestudy --language=sv --output=response input.md` | 1 run | 1 run |
| `column-flawed` (control) | `9b12ad3fb2cb7401` | `/redline --genre=column --language=sv --output=response input.md` | 1 run | 1 run |

- Run names are `<arm>-control-<row>` for a control and `<arm>-control-opinion-flawed-<n>` for the target, `<arm>` being `pre`, `post` or `revise`.
- **Genre names.** `case-study-flawed` is invoked with `--genre=casestudy`, the installed name since #443; the hyphenated alias #402's matrix typed is refused. Fixture and row IDs keep their hyphens. This is the substitution the corpus README's paragraph "Revised for installed genre names" records, and not a change of method.
- The controls run in both arms, because "still meet `C1`" needs a pre-change reading. All four rows are flawed controls, so the protocol's rule that a clean control also runs to a file does not arise.
- **Waves.** Runs are dispatched in waves of at most four, each run in a wave on a different row: wave 1 holds the pre-change arm's first `opinion-flawed` run and its three controls, and waves 2 and 3 its second and third `opinion-flawed` runs. Waves 4 to 6 do the same for the candidate arm, and waves 7 to 9 for a revise round, restricted to the rows it re-runs.
- **Order.** The pre-change arm is run and judged in full before the candidate is committed. The not-reproduced gate below is decided on it.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket, judging by [`control-judge-brief.md`](control-judge-brief.md), a byte copy of [#402's](../editorial-402/control-judge-brief.md), itself a byte copy of #383's. The brief names no path and no seat, so nothing in it is substituted. A judge's message is the brief verbatim, a line `---`, a line naming the run directory, a line giving its letter, `a` or `b`, and one paragraph headed **Frozen expectation**: the row's *Frozen expectation and rejection* cell in the corpus README at `2afeb95e`, copied verbatim, which is also written to the run's `expectation.md`. Nothing else is added, and no hint of the defect under investigation appears in any invocation, brief or message.

**Neutral paths.** Each judge gets a directory of its own made by `mktemp -d <scratch>/j/XXXXXXXXXXXX`, whose last component names neither the arm, the row, the run nor this ticket, holding `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`, and nothing else; the packet's other files name the revision and the model. The judge writes `judgement-<letter>.md` there. The judgement is copied into the run's directory as `judgement-a.md` or `judgement-b.md`, the mapping from directory to run is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. The two judges of one run are dispatched together and are not told of each other. The directories are under `<scratch>` rather than the system temporary directory because this build's brief confines what it writes to its working tree and its scratch root. That is a path substitution: the scratch root's name carries this build's number, which names neither the arm nor the expected verdict, the judge is told nothing of what it is, and the brief forbids reading any repository file or ticket.

One judge suffices for a mechanical check — reading a reply for a finding, a diff, the inventory — and those the dispatching session makes itself from the recorded files. *When a run delivers the ending* and the misreport check under *The controls, read* are such checks.

## Criteria, fixed before the runs

As #383's plan defines them, on these runs:

- **`R1`** and **`C1`**, on every run: the run meets its row's frozen expectation, on `R1`, read against the row as `2afeb95e` leaves it. `C1` is defined in [#383's plan](../editorial-383/plan.md).
- **`O1`**, on every run, from the runner's before-and-after inventories.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

Every other criterion — `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` — is recorded `skipped` on every run. `O1` and `S1` are recorded as #402's plan defines them; they feed the record's `side effects` field and its criteria lines and decide no outcome of this ticket.

### When `C1` is met

#383's plan settles a split: both classes are recorded and neither judge is an oracle, and *"a difference counts against a run when both judges class it as taste outside any finding, or when either does and the reply covers it neither in the claim account nor in the closing summary."* As #397 applied it: a run meets `C1` when both judges pass it and misses it when both fail it; where they split, it misses unless the passage that decides the failing verdict is a difference the reply covers in its claim account or its closing summary, in which case both readings are recorded and the run meets `C1`.

## When a run delivers the ending

Whether a run delivers the ending is decided by the dispatching session from the text the reply returns, the text in the reply's fenced block. The session makes this reading itself, as it makes the misreport check, and no judge makes it. A run **delivers the ending** where the returned text meets all three of these conditions:

1. **Its last level-2 section is one the input did not have.** The input's sections are `## Bakgrund` and `## Diskussion`. The paragraph that stood under `## Diskussion` before its closing line, in whatever form the round delivered it, stands in an earlier section of the returned text, under that heading or a rewritten one. A `## Diskussion` that has only been renamed is not a new section.
2. **That last section holds the text's closing call to action.** The input's closing line `Nu är det dags att agera.` stands in no earlier section.
3. **That call names the actor and the act the body proposes.** In `opinion-flawed` they are in the lead's first sentence: `Kommunstyrelsen borde behålla telefonbokning under ett halvårs försök i alla sju lokaler.` The actor is kommunstyrelsen, and the act is keeping telephone booking. The last section names kommunstyrelsen as the one who acts, in its subheading or its text. Its call to action names keeping booking by telephone: a form of *behålla* or *ha kvar* whose object names telephone booking (*telefonbokning*, *telefonbokningen*, *bokning via telefon*), in any inflection. Whether the call also restates the half year or the seven venues does not decide the check.

A run whose round was rejected returns the text as received and does not deliver the ending. Nor does a run that leaves the closing inside `## Diskussion`, whether or not the closing is repaired there, as #397's pre-change run renamed `## Diskussion` to `## Kostnaden för två bokningsvägar är inte beräknad` and repaired the closing inside it. #402's post-change round would have delivered it, had it survived: `## Kommunstyrelsen bör behålla båda kanalerna under försöket` over `Nu bör kommunstyrelsen behålla telefonbokningen under ett halvårs försök i alla sju lokaler.`, with the argument left under the section before it.

**The judges' answers are recorded, not counted.** For every `opinion-flawed` run, `results.md` quotes the returned text's last section in full, gives the check's reading on each of the three conditions, and puts both judges' heading-3 answers on *Existing action/actor in body can repair the ending* beside it. Where a judge and the check disagree, the check decides and both are shown.

**Every `opinion-flawed` run counts**, as delivering or not delivering, whatever lost the ending. Where a behaviour another open ticket owns loses it — a round rejected for a new source attribution, say — the cause is recorded under that ticket's number, as the whose-miss rule says, and the run still counts as not delivering here. For this reading, that is a stated departure from the rule's "not counted against this one". The gate and the target are never read on a reduced count.

- **The target** is met where more than half of the candidate arm's `opinion-flawed` runs deliver the ending.
- **The not-reproduced gate** reads the pre-change arm by the same check.

## The controls, read

- Each control that met `C1` in its pre-change run must meet it in its candidate run. A control that missed `C1` before the change is recorded and does not count against the candidate.
- **No candidate reply reports a heading repair it did not deliver.** The dispatching session checks this mechanically on every candidate run, target and controls alike: every headline or subheading a reply reports as repaired must stand in the delivered text as reported. A heading reported as attempted in a rejected round is not reported as repaired, which Redline's step 11 already requires.

**Whose miss.** A miss caused by a behaviour another open ticket was filed against is recorded under that ticket's number, with both judges' readings recorded; where they split, the split rule above decides. The open tickets filed against behaviours a miss on these four rows could land on, as of `<start>`: #438 (what a case study's quotation bridge may carry), #451 (a finding saying the body never names whose proposal it is, on `opinion-flawed`), #452 (a paragraph length measured before the round), #453 (a miscount of the headings a round replaced), #454 to #461 (the claim account on a rewritten headline or subheading, and on a changed connective), #462 (a rewritten column headline's lost play on a word) and #466 (`column-flawed`'s headline repaired but its missing subject no longer reported). The ending of `opinion-flawed` is counted here whatever lost it, as *When a run delivers the ending* says.

## Inventory scope

Scopes 1 and 2 — the run's working directory, its staged install and its scratch — are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read once around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), which is #402's with this build's paths, calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #402's:

3. **The rest of this build's scratch root**, the other runs' packets and the judges' directories among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so a hash of either would report an editing session's change as a run's; this is the narrowing #383 declared.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/e1c56c23-fb82-46cd-bafe-65bb6c439e91/scratchpad/`, which sibling builds also write to. A change there is attributed by path before it is named in any run's `side effects`.

The worktree list at `<start>` holds the main checkout, `../skills-rework`, this build's working tree and `kntnt-orchestrate/438` and `kntnt-orchestrate/447`; the last two are sibling builds' and the rework worktree is read-only source, so none of the three is in scope beyond what scope 4 names.

A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## What ships, for every outcome

This is this ticket's own ship rule, and it departs from the protocol's revise-round rule on purpose: once the defect reproduces, Thomas's ruling places the fix in the correction brief whatever the measurement shows, so in outcome 3 one of the two candidate wordings ships even where neither meets the protocol's rule. Where the two disagree, this section wins.

**The candidate meets its criteria** where all three hold: (a) the target is met, as *When a run delivers the ending* reads it; (b) every control that met `C1` in its pre-change run meets it in its candidate run; (c) no candidate reply reports a heading repair it did not deliver.

1. **Not reproduced.** The pre-change arm delivers the ending, by the check above, in more than half of its `opinion-flawed` runs. The result is recorded as not reproduced. No candidate is committed, no candidate arm is run, and nothing under `skills/` or `tests/` changes. A decision record is written in `docs/adr/` saying why no product change shipped. This is the ticket's own measurement gate and the protocol's measurement-gated case; Thomas's ruling concerns step 7, not the brief change, so it does not override the gate.
2. **Reproduced, and the candidate meets its criteria.** The candidate ships.
3. **Reproduced, and the candidate misses.** One revise round is taken. The revised candidate is committed first, and its runs replace the first candidate's on the rows it re-runs. It re-runs these rows, and only these: `opinion-flawed`, at the arm's full count, where (a) missed or any `opinion-flawed` candidate run broke (c); and one run of each control that broke (b) or (c).
   - **The revised wording ships** where, with its runs in place, the candidate arm meets (a), (b) and (c).
   - **Otherwise it ships only on a count of misses over the re-run rows.** One miss is counted for each `opinion-flawed` run that does not deliver the ending, each control run that misses `C1` having met it pre-change, and each run whose reply reports a heading repair it did not deliver. The revised wording ships only where it has fewer misses than the first candidate had on the same rows, and no control of the subset misses `C1` where the first candidate's run met it.
   - **In every other case the first candidate's wording ships**, a level count included.

   Either way the fix ships: a correction round never returns a heading that repeats what it stands over. There is no revert and no decision record.

**What is filed.**

- **Outcomes 2 and 3.** Filing reads the runs of the wording that shipped: where the revised wording ships, its runs on the re-run rows and the first candidate's runs on the rest; otherwise the first candidate's runs throughout. One `needs-triage` issue naming #433 is filed per fixture whose reading missed in those runs, naming every miss on that fixture: `opinion-flawed`, where any of its runs did not deliver the ending, even where the target is met, or any of its replies reported a heading repair it did not deliver; a control that met `C1` in its pre-change run and missed it, or whose reply reported a heading repair it did not deliver.
- **A control that missed `C1` before the change** is recorded in `results.md` and not filed by this ticket.
- **Whose miss.** A miss the whose-miss rule assigns to an open ticket is recorded under that ticket's number and not filed again. A fixture's issue is filed unless every miss on it is assigned that way.
- **A replaced run.** Where the revised wording ships, the first candidate's misses on the rows it re-ran are recorded in `results.md` and not filed.
- **Outcome 1.** Nothing is filed. What the pre-change arm misses is recorded in `results.md`, each miss under the number of the open ticket that owns it, where one does.

`results.md` lists the number of every issue filed.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again. A run that completes and stops is a finding.

## What is written

This file, the judge brief and the four scripts and matrix under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; the judged packets under `runs/`, each with its `expectation.md` and two judgements, with `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one evaluation record, `../records/redline-claude-<YYYY-MM-DD>-433.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this build. A packet's `stream.jsonl` and `transcripts/` are read for the seat, which its `trace-index.json` keeps, and are not committed. Nothing else already under `docs/evaluation/` changes. A decision record is written in `docs/adr/` in outcome 1 alone.
