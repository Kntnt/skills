---
name: session-cleanup
description: Leave the machine as the session found it — the agent records what it starts, and a lifecycle hook stops exactly that when the session ends or the next one begins.
metadata:
  kntnt.category: environment
  kntnt.harnesses: claude-code codex opencode
  kntnt.binaries: uv
  kntnt.capabilities: ""
  kntnt.integrations: scripts/session_cleanup.py
---

# session-cleanup

An agent session starts a dev server to look at a page, writes a scratch directory to hold an intermediate result, runs a container to reproduce a bug. Then the session ends, and every one of those is still running. Asking afterwards which of them belongs to the agent is a question nothing on the machine can answer: a process list cannot tell the agent's dev server from the user's, and a machine running several agent sessions at once cannot tell one session's work from another's at all.

The judgement is cheap at exactly one moment — when something is started, by the agent that started it and knows why. So this Feature installs two things that only work together: a block of prose telling the agent to write down what it starts, and a lifecycle hook that stops exactly what was written down. Neither is worth having alone. The block without the hook asks for a record nothing reads; the hook without the block reads an empty manifest forever while looking perfectly healthy. Enabling this Feature installs both into every supported Detected Harness, and disabling it takes both back out.

## Writes

- A fenced block, delimited by `<!-- kntnt.session-cleanup begin -->` and `<!-- kntnt.session-cleanup end -->`, at the end of each Harness's own global instruction file — `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`. These are files you own and read; everything above the fence is left exactly as it is, and disabling the Feature takes the fenced block away and nothing else.
- One session-lifecycle entry per Harness, in that Harness's own hook table — `~/.claude/settings.json`, `~/.codex/hooks.json` — or, for OpenCode, as the plugin file `~/.config/opencode/plugins/kntnt.session-cleanup.js`.
- Per-session manifests, and one log of every action taken, under `~/.kntnt/session-cleanup/`. Nothing is written outside these three places.

## How it decides

**Only what was recorded is ever stopped.** A manifest line is data and never an instruction. A recorded process is stopped only while its recorded start time still matches the one the machine reports, so a process id that has been reused since names something else and is left alone. A recorded path is deleted only where it resolves, symbolic links followed, strictly inside a temp root — a line naming `/` cannot do what it says. Nothing outside a manifest is ever touched, because the processes of another agent session running on the same machine are not this session's to end.

**The process group goes only where the recorded process leads one.** A process that is not its own group leader shares a group with whatever started it, which on this machine is the agent's own shell, so only a leader is stopped together with what it spawned. That is why the instruction block asks for long-lived work to be started in its own group.

**A session's start sweeps what earlier sessions left.** A manifest belonging to a session other than the one now starting belongs to a session that has already ended, however it ended — and a hard kill, a crash, and a Harness with a weak end event all end a session without its own end hook ever running. A manifest whose terminal is still alive elsewhere is left alone, because it may belong to a session still working; one sharing this terminal, one whose terminal is gone, and one older than a day are swept. That is what makes this self-healing rather than best-effort, and it is the same rule every owned integration in this collection is written under: nothing is remembered anywhere, and every run reads what is actually on disk.

**It acts and records; it never reports.** The hook runs while the session's screen is disappearing, so there is nowhere to report to. Every action is a line in `~/.kntnt/session-cleanup/cleanup.log`, including a session that ended having recorded nothing at all — which is the one thing worth watching, because recording is the single step of this design that depends on an agent remembering to take it. The hook exits zero whatever happened: a cleanup that breaks a shutdown is worse than a leak.

## Reading the log

```
uv run ~/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py health
tail -f ~/.kntnt/session-cleanup/cleanup.log
```

A run of `recorded-nothing` lines says the block is installed and the agent is not recording; a run of `acted` lines says it is.
