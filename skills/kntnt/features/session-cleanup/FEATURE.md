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

**A session's start sweeps ended owners.** Ownership is the long-lived Harness process and its recorded start time, never the POSIX session of a hook or tool call. A matching live owner keeps its entire manifest, including scratch and containers, regardless of age. A dead owner or a different start time permits the next start to reclaim it; an unreadable start time keeps it. A start always preserves a manifest recording the hook itself or an ancestor, and an unreadable process chain permits no start sweep. Unknown ownership, including old terminal-only manifests, waits until the manifest has been untouched for a day. This fallback can reclaim work whose owner could not be identified; record under a supported local Harness for lifetime protection.

**The nearest Harness determines identity.** Claude Code exposes `CLAUDE_CODE_SESSION_ID` and `CLAUDE_PID`; Codex exposes `CODEX_SESSION_ID`, matching its lifecycle payload. An inherited outer Harness's variables do not win over the nearer process. Hooks use their event's session identity; OpenCode places it in `properties.info.id`. OpenCode's shell does not consistently expose a conversation ID, so its recordings use a process-and-start-time key: they remain protected until the shared server exits and a later start reclaims them. Ending one conversation leaves those process-owned records alone. Where no Harness can be identified, a recording shell supplies only a filename and the age fallback applies. Old terminal pointer files are retired automatically at lifecycle events; new ones are never written.
**It acts and records; it never reports.** The hook runs while the session's screen is disappearing, so there is nowhere to report to. Every action is a line in `~/.kntnt/session-cleanup/cleanup.log`, including a session that ended having recorded nothing at all — which is the one thing worth watching, because recording is the single step of this design that depends on an agent remembering to take it. The hook exits zero whatever happened: a cleanup that breaks a shutdown is worse than a leak.

## Reading the log

```
uv run ~/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py health
tail -f ~/.kntnt/session-cleanup/cleanup.log
```

`session` identifies the manifest being swept. On a start sweep, `sweeper_session` and `sweeper_harness` identify the session that initiated the action; they are present on both `acted` and `recorded-nothing` rows. A `recorded-nothing` row means that particular manifest contained no entries; it does not mean the named session just started.

Older hooks wrote a JSON answer to stderr and then tried to write a second answer if the first failed. A closed caller pipe could therefore produce `hook-failed … Broken pipe` after cleanup had already acted, and the second write could fail again. Hooks now write only to the log, so closing stdout or stderr cannot cause that reporting failure. The incident logs alone do not establish why the caller closed its pipe.
