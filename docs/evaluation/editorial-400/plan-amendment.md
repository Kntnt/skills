# Amendment to the plan: the private home carries Proofread

Written on 2026-09-24 and committed before the first valid run of either arm. [`plan.md`](plan.md) and [`runs/turn_run.sh`](runs/turn_run.sh) stay frozen as they were committed; this file replaces one thing in the plan's *How a run is made* and changes nothing else in it — not the matrix, the turn files, the judging, the criteria or the exit.

## Why

The fourteen pre-change runs were dispatched with `turn_run.sh` against `install-pre`, all at once, and every one of them stopped at Redline's shim before reviewing anything. The shim's dependency check reported:

```
"unsatisfied": [{"name": "proofread", "kind": "skill", "how": "check 'proofread' in /kntnt select"}]
```

The Manager counts a Skill a Skill depends on as present when it is Enabled at the Global or the Project layer — in a Harness's skills directory under the home, or in the project's. `turn_run.sh` gives each run a private home with no skills directory, so Proofread, which stands beside Redline in the staged install and is the Skill step 9 follows, is Enabled nowhere the Manager looks, and the run correctly refuses. #383's runs were subagents of a session on this machine's own home, where the collection is installed, so the check passed there without the install beside the Skill having anything to do with it. [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) passes it by installing the staged Skills into its private home.

Those fourteen replies are kept under [`voided/unsatisfied-dependency/`](voided/unsatisfied-dependency/), each with its run directory and its packet. They are not findings about Redline: each is the Skill correctly refusing an installation the evaluator put it in, and none reviewed the text.

## How a run is made, as amended

Every run of both arms, of the #392 rows and of any revise round is made with [`runs/turn_run_2.sh`](runs/turn_run_2.sh) in place of `turn_run.sh`. It is `turn_run.sh` with one change: before the session starts, it copies the staged install's `proofread/` into the private home's `~/.agents/skills/proofread`, the shared Global directory the Manager falls back to, so the dependency is met by the same Proofread the run follows. Claude Code reads no Skill from that directory, so the session is offered no Proofread Skill of its own; a probe made before this amendment was committed confirmed that a session with that home lists no Skill named `proofread`. The copy is inside the private root and is removed with it.

The seat, the installs, the turn files, the message, where runs execute, the `claudeMdExcludes` setting, the locks, the lanes and everything the plan says a run keeps are unchanged. The pre-change arm is dispatched again from the start, under the same names.
