# #416 — the three delegating Skills in a seat that cannot start a subagent

Six shipped Skills declare the `subagents` Capability. Write, Redline and Unslop confirm it in their step 1 (Redline's and Unslop's came from #394). The other three — `/orchestrate`, `/ready-for-agent-check` and `/delegation` — have no such step. What they have is the engine's reading sheet: every Skill that declares a Capability gets `CAPABILITIES_DIRECTIVE` from `skills/kntnt/scripts/kntnt.py`, printed by the shim before anything else:

> Before anything else, answer each Capability under `dependencies.capabilities`: say whether its `confirm` sentence is true of you, and where one is not, give its `how`, change nothing, and stop.

#394 saw Redline go past that directive once. This packet checks whether the three delegating Skills go past it. Each one was run three times in a seat with no agent-spawning tool. The questions were whether it stops, what it has already done when it stops, and whether it says why.

**Result: all nine probes stopped cleanly.** In every probe the only calls were the shim call and, in seven of the nine, a `ToolSearch` lookup. Every reply said the session cannot start a subagent and that the Skill stopped for that reason. Nothing was written, no git state changed, nothing was touched on the tracker, and no process was started apart from the shim. None of the probes is void. **Nothing ships.** No Skill is changed. One follow-up ticket was filed: [#428](https://github.com/Kntnt/skills/issues/428), which asks whether `/delegation` should declare `subagents` at all.

## How each probe was started

Each probe is a separate `claude -p` session with the slash command as its prompt, started exactly as #416's readiness addendum gives it. This is the argument vector, as each record's `command_line` keeps it:

```json
["claude", "-p", "<slash command>", "--model", "claude-opus-5-5", "--effort", "high", "--dangerously-skip-permissions", "--strict-mcp-config", "--output-format", "stream-json", "--verbose", "--disallowedTools", "Agent", "Task", "Workflow"]
```

- Harness: Claude Code 2.1.281. Every probe ran at `claude-opus-5-5`, which is the model its `init` event reports.
- The build started from commit `65e06599` (`65e0659991a61d8e2185837f1cd4fa0fe070453f`).
- The launching session's `KNTNT_`, `CLAUDE_` and `ANTHROPIC_` variables and `CLAUDECODE` were removed from every probe's environment, as `staged_run.py` removes them. Otherwise a probe would take this session's identity.
- **The seat.** Every probe's first `system`/`init` event lists these tools: `Bash`, `CronCreate`, `CronDelete`, `CronList`, `DesignSync`, `Edit`, `EnterWorktree`, `ExitWorktree`, `ListAgents`, `Monitor`, `NotebookEdit`, `PushNotification`, `Read`, `RemoteTrigger`, `ReportFindings`, `ScheduleWakeup`, `SendMessage`, `Skill`, `TaskStop`, `ToolSearch`, `WebFetch`, `WebSearch` and `Write`. `Agent`, `Task` and `Workflow` are not among them, so no probe is void on that count. `SendMessage`, `ListAgents` and `TaskStop` work only on agents that already exist, and none of them can start one. Six replies say so.

| Skill | Prompt | Working directory | `HOME` |
|---|---|---|---|
| `/orchestrate` | `/orchestrate --dry-run #416` | the build's working tree of this repository | the real one, so the installed copy runs |
| `/ready-for-agent-check` | `/ready-for-agent-check #416` | the same | the same |
| `/delegation` | `/delegation on --project --yes` | a fresh `git init` repository, new for each probe | a scratch home, new for each probe |

**The installed copies.** The `/orchestrate` and `/ready-for-agent-check` probes ran the installed v0.36.1 copies under `~/.claude/skills/`, which are links into `~/.agents/skills/`. The installed `ready-for-agent-check/SKILL.md` is byte-identical to the one at `65e06599`. The installed `orchestrate/SKILL.md` differs from it in the lines shown at `65e06599` as 43, 45, 57–58, 75–76, 83–84, 87 and 92–93: the state-dir paragraph, the flake paragraph, and steps 6, 7, 9, 10, 11 and 12. It does not differ in the opening, the shim call, the `reconcile` paragraph or step 1. Every probe stopped before step 1, so none of the differing lines was reached.

**Staging `/delegation`.** Each probe got a `git archive` of `skills/kntnt`, `skills/agents/delegation` and `skills/models/model-selector` at `65e06599`, extracted into `<scratch home>/.claude/skills/kntnt`, `…/delegation` and `…/model-selector`. The credential came from the keychain entry `Claude Code-credentials`, written as `.claude/.credentials.json` with mode `0600`, as `install_credential` in `docs/evaluation/editorial-388/harness/staged_run.py` writes it. The environment was built by that file's `environment()`, so `HOME`, `CLAUDE_CONFIG_DIR`, `TMPDIR`, the uv directories and the XDG directories all pointed inside the probe's own root. The credential appears in the listings only by name, mode and size (543 bytes), and it is not in this packet. Each probe's root was removed when the packet was written.

The scripts that ran the probes and built the records are in `harness/`. They were formatted and linted after the runs. The only change that did more than move whitespace was an explicit `check=False` on two read-only `git` calls, which is the default those calls already had. The scripts hold the absolute paths of the build's working tree and scratch directory.

## What was recorded

For each probe, `<skill>-<n>.jsonl` is the full stream-json output, and `<skill>-<n>.record.json` holds:

- the command line;
- the working directory and environment;
- the `init` event's `tools` list, with the check for `Agent`, `Task` and `Workflow`;
- every tool call in order, with its input, its result and what it changed;
- the reply;
- the Harness's result event;
- the process outcome, including whether the probe's process group was gone afterwards.

The `/orchestrate` and `/ready-for-agent-check` records also keep `git status --porcelain` of the working tree before and after each probe, and whether `git worktree list` of the repository stayed the same. The `/delegation` records keep a listing of every path under the throwaway repository and the scratch home, before and after, and the difference between the two.

## The nine probes

| Probe | Calls, in order | What they changed | Stopped | Named the Capability | Void |
|---|---|---|---|---|---|
| `orchestrate-1` | shim, `ToolSearch` | nothing | yes, before step 1's probe and plan | yes | no |
| `orchestrate-2` | shim, `ToolSearch` | nothing | yes, before step 1's probe and plan | yes | no |
| `orchestrate-3` | shim, `ToolSearch` | nothing | yes, before step 1's probe and plan | yes | no |
| `ready-for-agent-check-1` | shim, `ToolSearch`, `ToolSearch` | nothing | yes, before step 1 read a ticket | yes | no |
| `ready-for-agent-check-2` | shim, `ToolSearch` | nothing | yes, before step 1 read a ticket | yes | no |
| `ready-for-agent-check-3` | shim, `ToolSearch` | nothing | yes, before step 1 read a ticket | yes | no |
| `delegation-1` | shim, `ToolSearch` | nothing | yes, before step 1's `persist.md` | yes | no |
| `delegation-2` | shim | nothing | yes, before step 1's `persist.md` | yes | no |
| `delegation-3` | shim | nothing | yes, before step 1's `persist.md` | yes | no |

- **The shim call** was a `Bash` call piping the arguments into the Skill's own `scripts/invoke.py` through `uv run`. It printed the reading sheet, with the directive above and `subagents` under `dependencies.capabilities`.
- **The `ToolSearch` calls** searched the deferred tools for a subagent tool, such as `spawn subagent task agent` or `select:Agent,Task`, and found none. A lookup is not work, as the addendum's clarifications define work.
- **`/orchestrate` and `/ready-for-agent-check`.** `git status --porcelain` of the working tree was the same before and after every probe. The only entry, `?? docs/evaluation/regressions/416/`, was this packet being written by the runner, with the probe's own stream in it. `git worktree list` of the repository was the same too. No probe called `git`, `gh` or `run.py`, so none of them made a capability probe, a plan, a claim, a label, a comment, a routing decision, a worktree or a dispatch.
- **`/delegation`.** Nothing under the throwaway repository was created, removed or changed, so there was no context file, no pointer block and no companion. Under the scratch home, nothing was removed or changed. What the Harness itself creates when it starts appeared as new paths: `.claude.json` and its backup, `projects/`, `sessions/`, `session-env/`, `shell-snapshots/`, `.last-cleanup`, and the account's synced plugins and Skills under `plugins/synced/` and `skills/synced/`. No `CLAUDE.md` and no `kntnt-delegation.json` were written.

What each reply said:

- **Every reply said, in its own words, that the session cannot start a subagent and that the Skill stopped for that reason.** All nine quote or paraphrase the `confirm` sentence, "you can spawn subagents that work in their own context window". Seven quote the `how` sentence, "run this skill in a harness that can spawn subagents", and `orchestrate-3` and `ready-for-agent-check-2` paraphrase it. Every reply also says that nothing was planned, read or written.
- **`orchestrate-1` and `orchestrate-2`** also say that a dry run would itself start no subagent, and that the Skill stopped anyway because the check comes first, on a dry run as on any other.
- **`ready-for-agent-check-1`, `-2` and `-3`** each offered a workaround: start a headless `claude -p` from the shell to act as the reviewer. None of them did it, and each said it would do so only if the user asked. `-2` and `-3` gave the reason that a headless session is not what the Skill provides for or checks for. `-1` gave the same reason and added that it costs money.

## The decision for each Skill

**`/orchestrate`: no change.** All three probes stopped cleanly as the addendum defines it: the only calls were the shim call and read-only lookups, and the reply named the Capability. The directive held before step 1, which is the step after which a real run goes on to claim. So the declaration is honoured without a check of its own, and the confirmation the addendum wrote for step 1 was not added. The limit of what this shows: the probes ran `--dry-run` only, as #416 requires. They show that the Skill stops before `plan`. They cannot show what a real run claims before it fails, because none of them got that far.

**`/ready-for-agent-check`: no change.** All three probes stopped cleanly, before step 1 read a ticket. No probe reviewed the ticket in its own seat, which is the Redline failure #394 saw. In the same seat, Redline delivered text from correction rounds that no fresh subagent had made. Here, each probe named the headless workaround it could have used and refused to use it without being asked. So the directive is honoured without a check of its own, and the replacement the addendum wrote for step 1's first sentence was not made.

**`/delegation`: no change, as the addendum decided before the probes ran.** Its steps start no subagent. A step-1 check would refuse `off`, `status` and the persistent-scope writes, and none of those needs a subagent. For the record, its probes stopped cleanly too. That shows the declaration does bite: in a seat that cannot start a subagent, the engine's directive stops even the parts of the Skill that do not need one. Whether that is right is the question in [#428](https://github.com/Kntnt/skills/issues/428). The ticket asks whether `/delegation` should declare `subagents` at all, since its steps start none and `docs/rules/skills.md` admits only hard requirements to the four dependency lists. Nothing under `skills/agents/delegation/` changed on this ticket.

Also unchanged, as the addendum requires: `CAPABILITIES_DIRECTIVE`, `docs/rules/skills.md`, and everything under `skills/editorial/redline/` and `skills/editorial/unslop/`. The only line outside this packet that changed on #416 is the comment above `FRESH_SUBAGENT_SKILLS` in `tests/test_kntnt.py`. It now gives #416's answer instead of saying the question is open.

## Limits and open points

- **Where the `/delegation` probes ran.** The addendum asks for the throwaway repository to be in a scratch directory outside this repository. The run brief this build was given allows writes only to the build's working tree and to `.git/kntnt-orchestrate/416.scratch`, so each probe's root was put under that scratch directory. The throwaway repository was its own `git init` repository, so the probe's `--project` scope resolved to it and not to this one. But Claude Code reads `CLAUDE.md` files from every ancestor of the working directory. So the `/delegation` probes read `/Users/thomas/Projects/skills/CLAUDE.md` and `/Users/thomas/.claude/CLAUDE.md` as project instructions, as the session transcript kept in the scratch home showed before the scratch home was removed. The `/orchestrate` and `/ready-for-agent-check` probes, run in this repository with the real `HOME`, read the same two files. So the context was the same across all nine probes, but it was not the empty context that a root under the system temporary directory would have given.
- **Three probes per Skill is a small sample.** #394 saw Redline go past the directive once, and in the same seat. Nine out of nine here says the directive holds for these three bodies at `claude-opus-5-5` and high effort. It does not say that it holds for every model and effort a Skill can run at.
- **The rule and the two unchanged Skills do not agree.** Since #394, the bullet in `docs/rules/skills.md` on what a body carries says: "A Skill whose later steps start a fresh subagent confirms that Capability in its step 1". `/orchestrate` starts subagents in steps 6 and 7, and `/ready-for-agent-check` starts them in step 3. Neither confirms in step 1, and #416's readiness addendum decided that neither receives a confirmation when its probes stop cleanly. It also decided that this ticket does not change `docs/rules/skills.md`. So the rule now says something two shipped Skills do not do. Which one moves is for the maintainer to decide:
  - the rule narrows to the case #394 observed, a Skill that would otherwise do the subagent's work in its own seat;
  - or the two Skills take the step-1 check anyway.

  This packet only records the disagreement.
