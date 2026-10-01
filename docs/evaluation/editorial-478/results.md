# Results for #478

Both arms ran on 2026-10-01 under the method [`plan.md`](plan.md) froze in `ca225468`, before the first run. Every Redline run, correction subagent, checker and replay ran on `claude-opus-5-5` at high deliberation in Claude Code 2.1.286, and every judge and classifier was a fresh `kntnt-opus-high` subagent. Each packet's `trace-index.json` records that model and deliberation for every agent, and every trace is complete. No Codex Harness and no GPT model was started, controlled or invoked. The record is [`../records/redline-claude-2026-10-01-478.md`](../records/redline-claude-2026-10-01-478.md).

**The headline result.** The fault is **not reproduced**. None of the eight pre-change runs carries a target miss: no claim account in them leaves out or shortens an attribution the run moved. So under *What ships* item 1, the candidate is reverted and the product stays as it was at `fb169087`. [ADR-0233](../../adr/0233-a-summing-sentences-attribution-in-redlines-reply-check-is-measured-first-and-not-reproduced.md) records why. No class 1 or class 2 miss was found in either arm, so nothing is filed.

Two further findings bear on what a later ticket would need:

- The narrator-to-Lind shape the ticket was filed on occurred once in the sixteen runs, in the candidate arm, in `post-case-study-clean-file-2`. Its drafted account was short in the same way as #475's. The candidate's checker named the shortfall, and the delivered account says who held which content before and who holds it now.
- Replayed on #475's saved checker input, the pre-change checker named the move in one replay of three, and the candidate's in three of three. The replays are diagnosis and decide nothing here.

## The historical gap

The ticket's run is #475's `post-control-case-study-clean`. Its five states are kept, each in a file of its own, under [`history/post-control-case-study-clean/`](history/post-control-case-study-clean/). [`runs/stages.py`](runs/stages.py) split them out of the committed packet, which was not changed. `checker-return.md` is what the checker returned, word for word:

- **The first list** has four items. The second says of finding 4's *Vad försöket krävde kommer i texten från Maya Linds citat, inte från någon anteckning* that the trial's requirements *come from Lind's quotes and also from this unattributed narration about Svale configuring the log and training six employees*.
- **The second list**, *Claim changes the account misses*, is `none`.

The run corrected finding 4 from the first list. It did not touch the entry *Det är nu Maya Lind som berättar vad försöket krävde, inte anteckningar.* So the attribution difference fell between the lists. The checker saw the narrator's share only as a false description of the received text. It did not see the delivered lead's *Vad det krävde berättar arbetsledaren Maya Lind om* as a moved attribution, because:

- the entry named a change of source, notes to Lind, and that change was true;
- no fact moved.

The run acts on each list as its brief says, and nothing told it to revisit an entry built on a description it had just corrected. That the run changed the text at all is #468's matter, closed since. A text change described correctly is still not a text change the product allows.

## The runs

| Arm | Staged from | Real runs | Replays |
| --- | --- | --- | --- |
| pre-change | `fb169087` (`<start>`) | `case-study-clean` as three response-target and file-target pairs, `case-study-flawed` twice: 8 | 3 of each contrast: 9 |
| candidate | `cbda0352` | the same eight, named `post-…` | the same nine, from the candidate's brief |

The corpus commit is `fb169087` in both arms. The inputs match the digests the plan pinned. Runs went in five lanes, as `runs/matrix.tsv` assigns them, from 11:56 to 15:53 UTC; each lane's start and end times are in `runs/logs/`.

**Three runs were void.** At 13:05 UTC the account's usage limit cut off three runs of lane A:

- `post-case-study-clean-resp-3`, with *API Error: This request would exceed your account's rate limit*, after 13 turns;
- `pre-case-study-clean-file-3` and `post-case-study-clean-file-3`, with *You've hit your session limit*, on their first turn.

Each had `terminal_reason: api_error`. Under the plan's *Void runs*, their packets were moved whole to [`voided/`](voided/), with the runner's output beside each as `runner-log.txt`. They were made again from the same commits, as wave 2, once the limit had reset, from 15:32 to 15:53 UTC. No judge had been sent a voided run.

Every judge and classifier finished before the limit or after the reset. Each judgement was checked for its last heading before it was counted, and none was cut off.

**One run needed a second splitter.** `post-case-study-clean-resp-3`, made again in wave 2, handed its checker the drafted reply between a `<<<REPLY` line and a `REPLY` line, where every other run used a backtick fence. The frozen `runs/stages.py` stops on that. [`runs/stages_delim.py`](runs/stages_delim.py) was written after the run to read either form and write the same files. It was used on that packet alone, and its `stages.json` says so in `split_by`. The plan's files are unchanged.

## The replays: diagnosis

Each contrast was replayed three times per arm in a fresh top-level session. Two blind judges read all eighteen returns under [`replay-judge-brief.md`](replay-judge-brief.md), each in shuffled neutral directories. The directories were `<scratch>/r/<letter>/<token>/`, one level deeper than the plan's `<scratch>/r/<token>/`, so that each judge had a set of its own; the letter is the judge's and names neither the arm nor the contrast. The mapping is `runs/replay-judges.tsv`.

| Contrast | Pre-change | Candidate |
| --- | --- | --- |
| `k1-narrator-to-person`: both judges answer heading 3 (*Caught*) `yes` | 1 of 3 | 3 of 3 |
| `k2-attribution-kept`: replays with an item either judge calls `false` | 3 of 3 | 3 of 3 |
| `k3-cause-and-scope-reported`: replays with an item either judge calls `false` | 1 of 3 | 0 of 3 |

**On `k1`**, the input is #475's own checker input, byte for byte save the Library path:

- `pre-replay-k1-1` named the move: *It moved the source of everything the trial required to Lind. Part of that content is still unattributed narration*.
- `pre-replay-k1-2` returned `none` on its second list and named the narration on its first, as #475's checker did.
- `pre-replay-k1-3` named only the move from the group's notes to Elm Quay's internal note.

All three candidate replays named the narrator's share and Lind. So the historical miss is not a fixed property of the old brief: it recurs in two replays of three. Both judges say heading 2 is `yes` on all six `k1` replays: the account in the input is short.

**On `k2` and `k3`**, every item either judge calls `false` is the same kind in both arms. It is a first-list item faulting the contrast's own closing sentence, *Utöver detta …* or *Utöver påståendena ovan …*, as reporting a further change. Both judges read that sentence as naming the non-claim side of the changes already listed. No replay in either arm put a moved attribution on its second list for `k2`. No replay put an item on `k3`'s second list.

## How every `A2` miss was read

Three fresh classifiers read all thirty-two judgements of the sixteen counted runs under [`runs/classify-brief.md`](runs/classify-brief.md). They worked in neutral directories, mapped in `runs/classifiers.tsv`, and each run's call is kept as its `classes.json`. This build read every call, and changed none.

| Run | Delivered text | `C1` (a / b) | Misses by class |
| --- | --- | --- | --- |
| `pre-case-study-clean-resp-1` | lead's last sentence removed | pass / pass | none |
| `pre-case-study-clean-file-1` | headline's speaker *Elm Quay* → *arbetsledare*; *gruppen* → *underhållsgruppen* | pass / fail | class 3: 1 |
| `pre-case-study-clean-resp-2` | unchanged: the round was rejected | pass / pass | none |
| `pre-case-study-clean-file-2` | headline's speaker → *arbetsledaren på Elm Quay*; lead's last sentence rewritten | fail / fail | class 3: 2 |
| `pre-case-study-clean-resp-3` | lead's first two sentences rewritten, its last removed | fail / pass | class 3: 4 |
| `pre-case-study-clean-file-3` | lead's first sentence rewritten | fail / pass | class 3: 1 |
| `pre-case-study-flawed-1` | repaired | pass / pass | none |
| `pre-case-study-flawed-2` | unchanged: the round was rejected | pass / pass | class 3: 1 |
| `post-case-study-clean-resp-1` | unchanged: the round was rejected | pass / pass | none |
| `post-case-study-clean-file-1` | headline's speaker → *Elm Quays arbetsledare*; lead's first sentence rewritten | fail / fail | class 3: 3 |
| `post-case-study-clean-resp-2` | unchanged: the round was rejected | pass / pass | class 3: 2 |
| `post-case-study-clean-file-2` | headline's speaker → *arbetsledare på Elm Quay*; lead: *Vad det krävde berättar arbetsledaren Maya Lind* | fail / pass | class 3: 1 |
| `post-case-study-clean-resp-3` | unchanged: the round was rejected | pass / pass | none |
| `post-case-study-clean-file-3` | headline's speaker → *Elm Quays arbetsledare*; standfirst's notes → *gruppens anteckningar*; lead's first sentence rewritten | fail / fail | class 4: 2 |
| `post-case-study-flawed-1` | repaired | pass / pass | none |
| `post-case-study-flawed-2` | unchanged: the round was rejected | pass / pass | none |

**No run in either arm carries a class 1 or class 2 miss**, so none carries a target miss.

Five delivered texts moved an attribution, the headline's speaker in all five. Three moved a second:

- `pre-case-study-clean-file-2`: the lead's requirements from the group's notes to the narrator;
- `post-case-study-clean-file-2`: the lead's requirements from the group's notes and the narrator to Lind;
- `post-case-study-clean-file-3`: the standfirst's notes to the group.

Both judges of each of those runs call its account of every move accurate. Each class 3 call faults a reason or a framing, not a statement the text contradicts. The two class 4 calls in `post-case-study-clean-file-3` are the standfirst growing from 40 to 43 words, which the reply does not mention. That difference moves no claim.

No miss is owned by #477: every finding about the note says it declines to credit the software. `pre-case-study-clean-resp-3` left an empty working directory in its private scratch. That is #476's behaviour, and it is recorded under #476 below.

**Where the attribution was caught.** In `post-case-study-clean-file-2`, the only run with the ticket's shape, the stages show where the account came from:

- **The drafted entry** was *det som försöket krävde tillskrivs nu Maya Linds berättelse i stället för gruppens anteckningar*. That is short in the same way as #475's.
- **The checker's second list** named it: *It names only the notes as the voice the content was taken from and leaves out the narrator.*
- **The delivered entry** says the attribution moved *från två röster till Lind*, and names the narrator's statements about the categories, Svale's configuration and the training of six staff.

This is the candidate working once, in the arm whose result does not decide Reproduced. Under the plan's split of the arms, it decides nothing.

## Reproduced, the Target and the Control

| Arm | Real runs with a target miss | Share |
| --- | --- | --- |
| pre-change | none | 0 of 8 |
| candidate | none | 0 of 8 |

- **Reproduced: not met.** No pre-change run carries a target miss, and the plan reads Reproduced from those eight runs alone.
- **Target.** Item 1, the halving of a zero share, is met trivially. Item 2 is met: three of three candidate `k1` replays have *Caught* `yes` from both judges. Neither is read for shipping, because Reproduced is not met.
- **Control.** All four controls hold:
  1. Every candidate run's delivered text equals the final Text Artifact its checker was shown, every `input.md` is unchanged, and `O1` holds.
  2. Neither arm has a class 1 or class 2 miss.
  3. The four candidate runs that returned the text unchanged each say no claim was removed, changed or added.
  4. Candidate `k2` and `k3` replays carrying a false item number 3, against 4 in the pre-change arm.

The Control is recorded and not read for shipping either.

**`C1`.** A run passes where both judges pass. Neither arm changes anything the run does before its checker, and every run's delivered text equals what its checker was shown.

- **Pre-change.** Four runs pass: `resp-1`, `resp-2` and both `flawed` runs. Four fail: `file-1`, `file-2`, `resp-3` and `file-3`.
- **Candidate.** Five runs pass: `resp-1`, `resp-2`, `resp-3` and both `flawed` runs. Three fail: `file-1`, `file-2` and `file-3`.

Each of the seven failures is a clean text changed on a finding a judge calls taste: a headline's speaker or a lead sentence rewritten. `case-study-clean` is still rewritten after #468, in all six file-target runs. That is outside this ticket's scope, and is noted here for whoever reads #468's result next.

**The checker.** Every one of the sixteen runs started one checker, after its run's Proofread pass, and none returned only the no-change status. In `pre-case-study-flawed-2` one later call removed the Proofread pass's private directory; the pass itself ran before the checker.

## What ships

Nothing.

- `skills/editorial/redline/references/reply-check.md`, `skills/editorial/redline/help.md`, `skills/kntnt/catalog.json` and `tests/test_kntnt.py` are restored to `fb169087`. The candidate stays in history as `cbda0352`.
- The check is still made once and the Correction Budget is unchanged, in both arms.
- No class 1 or class 2 miss of the pre-change arm stands to be filed, so nothing is filed.

## Side effects

`O1` and `S1` hold on all sixteen counted runs and all eighteen replays.

- **The runner's inventories.** Each packet's `filesystem-changes.json` shows no created, changed or removed path outside the Harness's configuration directory, its caches and the run's private scratch, save `work/output.md` on each file-target run.
- **The input and the Skills.** `work/input.md` is unchanged everywhere.
- **#476's leftover directory.** `pre-case-study-clean-resp-3` also left the empty working directory `scratch/tmp/tmp.1reKUB81FT` in its private scratch. Its reply names it and says the permission guard stopped its removal, which is #476's behaviour. The runner removed it with the root, and it is recorded under #476.
- **Synced skills.** Every run's private `HOME` also received the account's synced skills and plugins under `home/.claude/skills/synced/` and `home/.claude/plugins/synced/`. That is the Harness's own configuration. No trace shows a skill body other than `redline` loaded.

**The waves.** The runs were two waves, read around each into `runs/waves/`:

- Wave 1 was every run and replay made before the limit.
- Wave 2 was the three void runs made again.

Every change is attributed by path, and none is a run's:

- **This working tree.** Only the wave inventories' own files appeared.
- **The main checkout.** In wave 1 its `HEAD` moved from `fb169087` to `fe2587b7`: the orchestrating run integrated other tickets. In wave 2 it did not move.
- **The session scratchpad.** In wave 1 it gained the orchestrator's `own/gate-476.json`, `own/gate-479.json`, `own/verify-476.md` and `own/verify-479.md`, its `own/builders.txt` changed, and it gained `returned.md`. In wave 2 it gained the orchestrator's `own/amend-479-1.md`, `own/fill_amend.py`, `own/route-amend-479-1.json` and `own/verdict-479-initial.md`, and `own/builders.txt` changed again. No run of this build ran there, and no judge or classifier was given a path there. `returned.md` is named by no one, so it is named in the side effects of every wave-1 run in the record.
- **This build's scratch root.** It holds this build's inputs, packets, logs, tools and judge and classifier directories, and nothing else.

Every judge and classifier directory held only its inputs and its writing when collected, and each judge directory was removed once its judgement was copied.

## What is not measured

- **Unslop** carries the same claim account. It is neither changed nor run.
- **The GPT family.** The protocol forbids a Claude session from starting a Codex Harness, so Redline was not measured there.
- **Other criteria.** `T1` and `R2` are `skipped`, and every packet keeps its trace. `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are `skipped`.
