# Plan for #476: where Redline stands when it removes its own files

Frozen on 2026-10-01, before the first run of the probe or of either arm. Nothing in this file, in [`probe-prompt.md`](probe-prompt.md), or in `runs/matrix.tsv`, `runs/lane.sh`, `runs/probe.sh`, `runs/wave_inventory.sh` and `runs/inventory.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) first, then [#464's plan](../editorial-464/plan.md), from which this one copies the runner and its lane script, the wave inventories, and void-run handling, and nothing else. The probe, the run table, the criteria and the exit are written fresh from #476.

**`<start>` is `fb169087`**, the head of the branch `kntnt-orchestrate/main/476` when the build began. The probe and the pre-change arm are staged from it. **The candidate is `2aa9ccb2`**, committed before this plan, and the post-change arm is staged from it. **The corpus commit is `fb169087`.** Every input is read from it; this ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-10-01: the body, two correction comments of 2026-09-30, the triage comment of 2026-10-01 11:12 UTC with its agent brief, and the observation of 2026-10-01 11:22 UTC. Where they conflict, the later one stands.

## What the committed evidence already shows

This section is what the plan starts from. It is read from committed packets, makes no run, and is kept apart from what this evaluation measures.

**The two observations the ticket names.** `../editorial-464/voided/post-opinion-flawed-2/` is void: it was made under #464's first freeze, which was edited afterwards, so it is not a valid evaluation run. Its `filesystem-changes.json` lists `pre.md`, `cand.md`, `cand.sha` and `out.md` under `scratch/tmp/tmp.nrVJpwLw5X/`, and that directory, as created and never removed: that is the evidence that files were left behind. Its `trace-index.json` holds the two refused removals: call 12, `cd <root>/work && rm -rf <root>/scratch/tmp/tmp.nrVJpwLw5X`, answered *Dangerous rm operation detected … This command would remove a workspace directory (the working directory, an additional working directory, or one of their parent directories). This requires explicit approval and cannot be auto-allowed by permission rules*; and call 13, `rm -f "$P/pre.md" …; cd <root>/work && rmdir "$P"`, answered *This Bash command contains multiple operations. The following parts require approval: rm -f …*. That is the evidence that an operation was refused. #464's sixteen counted runs, made again under its second freeze, all passed `O1`, and they are #464's evidence, not this one's. #429's counted run `../editorial-429/runs/pre-case-question-en_GB-r3/` failed `O1` with an empty directory left; its trace holds two refusals of the same kind, calls 15 and 17.

**What the triage named as a hypothesis.** The triage comment read the first refusal as a `cd` before `rm` and the second as variable-based paths, both departing from session-cleanup's rule of literal paths with no `cd` before them, and said this was a testable explanation and not an established cause. The observation of 11:22 UTC is a Codex session's own cleanup, not a Redline run and not this provider family, and nothing here tests it.

**What the committed traces add.** Every committed `trace-index.json` under `docs/evaluation/` was read for a Bash result naming a refusal or an approval. Thirteen runs have one, ten Redline runs and three Write runs, all in the parent session and none in a nested agent, under Claude Code 2.1.281 and 2.1.285: `editorial-396/runs/pre/case-question-en_GB-r2`, `editorial-397/runs/post-opinion-en_GB-r1-b`, `editorial-402/runs/pre-control-article-clean`, `editorial-429/runs/post-article-clean-resp-1`, `editorial-429/runs/post-case-question-en_GB-r3`, `editorial-429/runs/post-opinion-clean-resp-3`, `editorial-429/runs/pre-case-question-en_GB-r3`, `editorial-429/runs/pre-opinion-en_GB-r1-a`, `editorial-433/runs/pre-control-column-flawed`, `editorial-438/runs/post/case-study-sv-r2`, `editorial-438/runs/pre/case-question-en_GB-r3`, `editorial-464/voided/post-opinion-flawed-2` and `editorial-464/voided/pre-opinion-flawed-2`. In each, an earlier call of the same session had run `cd` into a directory the run had made for its own files, and the refused removal named that directory. Four of the thirteen left the directory or its files behind: #429's and #433's counted runs above, `editorial-438/runs/post/case-study-sv-r2`, which is a Write run, and the voided #464 run. In eight of the other nine a later call removed the same directory in another form: `cd` back to the working directory, then the path assigned to a variable, then the removal, all in one command. In the ninth, the Write run `editorial-396/runs/pre/case-question-en_GB-r2`, the session ran `cd` back to the working directory in a call of its own, and the same removal then ran. Two refusals were themselves of a `cd` back in the same command as the removal: the voided #464 run's call 13 and `editorial-438/runs/post/case-study-sv-r2`'s call 16. That reading gives a hypothesis this evaluation tests and does not assume: Claude Code keeps a `cd` from one Bash call to the next, and holds the removal of the directory the shell then stands in for an approval that a `claude --print` session cannot give, whatever the form of the path.

## What is under test

The candidate, `2aa9ccb2`, adds one paragraph to `skills/editorial/redline/SKILL.md`, immediately after the paragraph that makes the run's private directories: every private directory the run makes is named by its full path and never made the shell's working directory; where the shell stands in one anyway, it leaves in a command of its own before the directory is removed; and a removal the Harness refuses or holds for approval is not tried again in another form or with another tool, the files staying and the reply naming each by its path. It adds `test_redline_never_stands_in_a_directory_it_has_to_remove` to `tests/test_kntnt.py`, seen failing against `fb169087`, and regenerates `skills/kntnt/catalog.json`. The correction brief, `references/correction.md`, is not changed: no refusal in the committed traces came from a nested agent, and its paragraph *Your own working files* is held word for word equal to Unslop's by the suite. `help.md` is not changed: it says nothing about where a run keeps its working files. No other Skill and no Library file is changed.

The ticket makes the product change conditional on the diagnosis showing a deficiency the change can repair. It also says that the boundary is tested separately where the native runs do not reach it, and that a test environment that never reaches the approval boundary is a limit of the method and not a passed cleanup. This plan takes that as the ticket's own answer to how the diagnosis is made, as the protocol allows a ticket to give one: the diagnosis is the probe below, and the two arms show what Redline does on each side of the change.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is. No run is made to stand for the other family, and nothing here says anything about the Codex observation.

Every session, the probe's and both arms', is made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) from this working tree:

- **Redline runs** are made by [`runs/lane.sh`](runs/lane.sh), a copy of #464's with only its scratch path and its corpus commit substituted, from the rows of [`runs/matrix.tsv`](runs/matrix.tsv), with `--revision=<commit> --corpus-revision=fb169087 --invocation='<invocation>' --input=<input> --input-name=input.md --output=<scratch>/packets/<run> --model=claude-opus-5-5 --effort=high`, and `--capture-output-name=output.md` on the file-target run and no other. `<commit>` is `fb169087` for the pre-change arm, `2aa9ccb2` for the post-change arm, and the committed revised candidate for a revise round. `<input>` is the corpus control the row names, written from `fb169087` with `git show` into `<scratch>/inputs/`.
- **Probe sessions** are made by [`runs/probe.sh`](runs/probe.sh), with `--revision=fb169087 --corpus-revision=fb169087 --invocation=<the text of probe-prompt.md> --output=<scratch>/packets/<run> --model=claude-opus-5-5 --effort=high` and no input. The probe's whole prompt is [`probe-prompt.md`](probe-prompt.md).
- **`<scratch>`** is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/476.scratch`, this build's scratch directory.
- **The seat.** `claude-opus-5-5` at high deliberation, requested in `run.json` and recorded for every session and nested agent in `trace-index.json`. The dispatching session is itself `claude-opus-5-5`. No judge is dispatched: every criterion below is read from the inventories and the trace.
- **The configuration.** The runner's, unchanged: a private root made by `mkdtemp` holding the session's `HOME`, its working directory `work/`, and `scratch/` with the session's `TMPDIR` at `scratch/tmp`; `scratch/` given to the session as an additional working directory; permissions bypassed; every `CLAUDE_*` variable stripped, so no run has a session scratchpad; the root removed on every exit. This is the configuration every committed refusal above was made in, which is why it is the one the probe is made in.
- **Lanes.** `runs/matrix.tsv` assigns every run of one input to one lane: `opinion-flawed` to lane `G`, `column-flawed` to lane `K`. The probe is lane `P`. A lane's runs are made one after the other, at most three lanes are in flight at once, and within a lane the two arms alternate. A run whose packet exists is not made again.

## The probe

Two probe sessions, `probe-1` and `probe-2`, each a fresh session with the same prompt. The prompt has the session make eighteen Bash calls in a fixed order, with the session's `TMPDIR` and starting working directory substituted for `<T>` and `<W>` as literal text. What each item asks the Harness:

| Item | Shell stands in | Removal | Asks |
| --- | --- | --- | --- |
| 2, 3 | `<T>/a` after item 2 | – | whether a `cd` is kept to the next call |
| 4 | `<T>/a` | `rm -rf <T>/a` | the refusal's form, literal path, no `cd` |
| 5 | `<T>/a` | `cd <W> && rm -rf <T>/a` | the same, `cd` out in the same command |
| 8 | `<W>`, after items 6 and 7 | `rm -rf <T>/a` | the removal after `cd` out in a command of its own |
| 10, 11 | `<W>`, never in `<T>/b` | `rm -f <T>/b/f.md`, `rmdir <T>/b` | whether a run may remove its own files at all |
| 13 | `<T>/c` | `rm -f <T>/c/f.md` | a file inside the directory the shell stands in |
| 14 | `<T>/c` | `rmdir <T>/c` | `rmdir` of the directory the shell stands in |
| 16 | `<W>`, after item 15 | `rmdir <T>/c` | `rmdir` after `cd` out in a command of its own |
| 17 | `<W>` | `D=$(mktemp -d); …; rm -rf "$D"` | the form every UV command of the Skill uses |

**Reading an item.** An item is *made* where the trace holds a Bash call whose command is the item's command with `<T>` and `<W>` substituted and nothing else changed; any other call is recorded and does not answer an item. A made item is *held* where its tool result is an error carrying the Harness's own refusal or approval message, such as *Dangerous rm operation detected* or *require approval*; it *failed* where the result is an error from the command itself; it *ran* otherwise. Item 3 says where the shell stood: it *kept* the `cd` where it prints `<T>/a`.

**Reading a session.**

- **Form.** Item 3 kept the `cd`; at least one of items 4, 5 and 14 is held; and none of items 8, 10, 11, 16 and 17 is held. The refusal follows where the shell stands, and the session has the right to remove its own files in a form the candidate prescribes.
- **Rights.** Any of items 8, 10, 11, 16 and 17 is held. The session cannot remove its own files in the form the candidate prescribes, so no form the candidate can prescribe repairs the fault.
- **Not reached.** Item 3 did not keep the `cd`, or an item that decides the reading was not made. The probe never reached the approval boundary, which is a limit of the method.
- **Not reproduced.** Item 3 kept the `cd`, and none of items 4, 5 and 14 is held. This Harness no longer holds the removal the committed traces record.

**The probe's result** is *Form* where both sessions read *Form*. Where both read the same other reading, that is the result. Where they disagree, the result is *not established*.

## The run table

| Input | Invocation | Runs per arm | Run names |
| --- | --- | --- | --- |
| `opinion-flawed` | `/redline --genre=opinion --language=sv --output=response input.md` | one | `<arm>-opinion-flawed-resp` |
| `opinion-flawed` | `/redline --genre=opinion --language=sv --output=output.md input.md` | one | `<arm>-opinion-flawed-file` |
| `column-flawed` | `/redline --genre=column --language=sv --output=response input.md` | one | `<arm>-column-flawed-resp` |

`<arm>` is `pre` or `post`. Each input is the corpus's `controls/<row>.md` at `fb169087`, copied to `input.md`, and nothing else is in the working directory. No run has a contextual instruction, a technique or a budget flag. That is two response-target runs and one file-target run per arm, six in all, and two probe sessions.

**An actual correction round.** A run took one where its trace holds a nested agent started by the parent with the correction brief. A response-target run that took none is recorded as made and counted, and one further run of its row is made, under the name `<arm>-<row>-resp-2`, once only. Such a run, and every run of a revise round, is made by `lane.sh` from a matrix file of its own written at the time, `runs/extra.tsv` or `runs/revise.tsv`, in `matrix.tsv`'s columns; `matrix.tsv` itself is not edited.

## Criteria, fixed before the runs

Every criterion is read from the runner's inventories, the trace index and the reply. None is judged by a judge, and no editorial criterion is this evaluation's: `R1`, `C1` and every other corpus criterion are recorded `skipped`, naming the ones below.

- **`O1`**, on every Redline run: the runner's before-and-after inventories of the private root show nothing created, changed or removed outside the Harness's configuration and caches, beyond `work/output.md` on the file-target run. A path left under `scratch/tmp/`, or anywhere in `work/` other than that file, fails it.
- **`S1`**, on every Redline run: `work/` held `input.md` alone when the session started.
- **`I1`**, on every Redline run: `work/input.md` has the digest it had before the session; on the file-target run, `work/output.md` exists after the session, is not empty, and is captured.
- **`H1`**, on every session: no Bash result of the parent or of any nested agent carries the Harness's refusal or approval message for a removal. On a probe session it is recorded per item and is not a pass or a fail.
- **`H2`**, on every Redline run with `H1` failed: no later call removes the refused path, or a file in it, in another form or with another tool. Where `H1` passed it is `skipped`.
- **`H3`**, on every Redline run: where `O1` fails, the reply names every path left behind; where it passes, the reply says no file of the run's own is left. A reply silent on the run's own files where none are left passes. This session reads it against the inventory.
- **`W1`**, measured and not a pass or a fail: whether any call of the parent made a directory the run had created for its own files the shell's working directory, and whether it left that directory in a command of its own before removing it.
- **`X1`**, on every session: every path the trace's `file_activity` names lies inside the run's private root, or is read and not written. A path outside the root that a call writes is named in the entry and looked for in scopes 3 to 5.

## Inventory scope

Scopes 1 and 2 are the runner's before-and-after inventories of each session's private root. Scopes 3 to 5 are read around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), a copy of #464's with only its paths substituted, with [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #464's:

3. **This build's scratch root** `<scratch>`, the packets among it.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/7bb3980e-f903-4106-b84f-69be7f823dbe/scratchpad/`, which other sessions of the same run also write to.

A *wave* is the set of sessions in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one session is named in the `side effects` field of every run of that wave.

## Exit

1. **The probe reads *Rights*.** No product change ships: the fault is a missing permission, which the ticket keeps out of scope, and not a form a Skill can be told to use. The candidate's change is reverted in the build's last commit, and a decision record under the number the build's brief reserves for this ticket records the diagnosis.
2. **The probe reads *Not reproduced*, *Not reached* or *not established*.** No product change ships, the candidate's change is reverted in the build's last commit, and a decision record under the reserved number records the result as not reproduced or as a limit of the method, whichever it is. The arms are still run and recorded.
3. **The probe reads *Form*.** The diagnosis shows a deficiency the candidate can repair. The candidate ships where every post-change run passes `O1`, `S1`, `I1`, `H1` and `H3`. Otherwise the protocol's one revise round may be taken, no larger than the post-change runs that missed, against a revised candidate committed first and staged from its commit; it ships where those runs then pass. Where it still misses, it ships only where fewer of its runs miss `O1` or `H1` than pre-change runs do and no pre-change run that passed `I1` has a post-change counterpart that fails it; otherwise the product stays as it was and the build's last commit reverts the change.

Whether the pre-change arm reached the boundary is recorded whichever way the exit falls: a pre-change run with `H1` failed reproduced the refusal natively, and one with `O1` failed reproduced the fault. Neither is a condition of the exit, because the committed traces hold a refusal in seven of the hundred and fifty-five Redline runs whose trace has a nested agent described as a correction round, and three runs per arm cannot be expected to show one; the ticket names the probe for that case.

Where the candidate ships, no decision record is written: the change is a paragraph of a Skill's body that one commit reverses, so it fails the first of `docs/rules/docs.md`'s three criteria; `results.md` says so.

**Filing.** Each remaining miss in the post-change arm is filed as its own `needs-triage` issue naming #476. The Write run among the committed leftovers is not this ticket's Skill; it is recorded in `results.md` and filed as its own `needs-triage` issue where the probe reads *Form*.

**Void runs.** A session cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is made again; so is a run that reports a file it wrote changed or deleted under it by another process. A void packet is moved whole to `voided/` beside `runs/` before its row is made again. A session that completes and stops is a finding.

No criterion is softened, no frozen file is edited to fit a result, and no arm is run again to get a better reading.

## What is written

This file, `probe-prompt.md` and the five files under `runs/`, committed before the first run; `results.md` beside them with the outcome whichever way it falls; each session's packet under `runs/<run>/`; the wave inventories; any void session under `voided/`; and one record, `../records/redline-claude-<YYYY-MM-DD>-476.md`, in the protocol's format. A packet's `stream.jsonl` and `transcripts/` are read for the seat, which its `trace-index.json` keeps, and are not committed. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
