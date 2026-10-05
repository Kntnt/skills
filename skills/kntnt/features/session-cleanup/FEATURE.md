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
- Per-session manifests, a lock coordinating sweeps, and one log of every action taken, under `~/.kntnt/session-cleanup/`. Nothing is written outside these three places.

## How it decides

**Only recorded identities authorize signals.** A manifest line is data and never an instruction. Before TERM and again before KILL, both recorded and current start identities must be nonempty and match, and the process must still belong to the intended group. A missing or unreadable birth or group refuses cleanup; a mismatched birth is reported as `reused` and receives no destructive signal. Historical empty births are never backfilled. A recorded path is deleted only where it resolves, symbolic links followed, strictly inside a temp root — a line naming `/` cannot do what it says.

**The process group goes only where the recorded process leads one.** A follower is stopped alone, because signaling its group could reach the shell that started it. An absent leader with a surviving or unreadable group refuses cleanup, including after TERM; the remaining group is never signaled on its vanished leader's authority. A sent KILL is successful only when the subsequent observation finds the intended process and, for a leader, its group gone. A still visible process or group remains unresolved and can be checked again later.

**Registration initializes this Feature's state before identity probes.** `KNTNT_HOME` selects the state home when present, and the user's home is the default. A first registration can therefore use a fresh nested selected home. If the process birth cannot be read, `add pid` exits nonzero with a diagnostic and records no PID entry. An unreadable ancestry retains the existing unknown-owner policy below rather than inventing an owner.

**Refused process cleanup stays inspectable.** The log records the refusal and `manifest-kept`. Original manifest lines, including historical PID births and ownership, remain intact; appended consumption records remove completed work from the pending set. A retry acts only on unresolved PID entries. Transient probe failures can resolve later; an empty historical birth cannot, and a leaderless group may require the owner's manual review. Proven gone processes and completed stops still remove a manifest when every PID entry is resolved.

**A name authorizes one removal attempt.** A path or container entry is consumed before its action, so later sweeps cannot remove a replacement at the same name. A failed or unavailable name-based action requires manual review or a new explicit registration, as it did when a sweep removed its manifest outright. If consumption cannot be written, that action does not run. An interruption after consumption but before removal can leave the resource behind; ownership uncertainty favors a leak over repeated destruction. Sweeps and registrations in the same selected state home are coordinated by an advisory lock. Consumption preserves the manifest's age; new registrations refresh it. Consumption records refer to original line positions, so a later registration remains distinct even when its values match an earlier one.

**OS checks have a race window.** `ps` reports start times to the second, and observing birth and group membership and then sending a signal are separate operations. A process can exit, its PID can be reused, or group membership can change between those operations; same-second reuse can also be indistinguishable. The checks fail closed on observed uncertainty and changes, but provide no atomic kernel ownership guarantee. Long-lived work therefore needs its own process group, as the instruction block asks.

**A session's start sweeps ended owners.** Ownership is the long-lived Harness process and its recorded start time, never the POSIX session of a hook or tool call. A matching live owner keeps its entire manifest, including scratch and containers, regardless of age. A dead owner or a different start time permits the next start to reclaim it; an unreadable start time keeps it. A start always preserves a manifest recording the hook itself or an ancestor, and an unreadable, incomplete or cyclic process chain permits no start sweep. Unknown ownership, including old terminal-only manifests, waits until the manifest has been untouched for a day. This fallback can reclaim work whose owner could not be identified; record under a supported local Harness for lifetime protection.

**The nearest Harness determines identity.** Claude Code exposes `CLAUDE_CODE_SESSION_ID` and `CLAUDE_PID`; Codex exposes `CODEX_SESSION_ID`, matching its lifecycle payload. An inherited outer Harness's variables do not win over the nearer process. Hooks use their event's session identity; OpenCode places it in `properties.info.id`. OpenCode's shell does not consistently expose a conversation ID, so its recordings use a process-and-start-time key: they remain protected until the shared server exits and a later start reclaims them. Ending one conversation leaves those process-owned records alone. Where no Harness can be identified, a recording shell supplies only a filename and the age fallback applies. Old terminal pointer files are retired automatically at lifecycle events; new ones are never written.
**It acts and records; it never reports.** The hook runs while the session's screen is disappearing, so there is nowhere to report to. Every action is a line in `~/.kntnt/session-cleanup/cleanup.log`, including a session that ended having recorded nothing at all — which is the one thing worth watching, because recording is the single step of this design that depends on an agent remembering to take it. The hook exits zero whatever happened: a cleanup that breaks a shutdown is worse than a leak.

## Reading the log

```
uv run ~/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py health
tail -f ~/.kntnt/session-cleanup/cleanup.log
```

`session` identifies the manifest being swept. On a start sweep, `sweeper_session` and `sweeper_harness` identify the session that initiated the action; they are present on `acted`, `recorded-nothing`, and unreadable-history `manifest-kept` rows. A `recorded-nothing` row means that particular manifest contained no resource entries; it does not mean the named session just started. Original resource history still counts after consumption, so retiring fully consumed retained history emits neither another action nor an empty audit.

A manifest that cannot be read or decoded, or contains invalid lines without any readable resource history, is kept and logged as `manifest-kept`. It is not evidence that nothing was recorded. The public sweep result reports `entries: null` when its pending count is unknown; readable manifests still report the number of pending entries. A transient read failure can be retried, and retaining unknown history preserves its age. Invalid lines beside readable resource entries remain skipped so neighboring work can still be handled.

Older hooks wrote a JSON answer to stderr and then tried to write a second answer if the first failed. A closed caller pipe could therefore produce `hook-failed … Broken pipe` after cleanup had already acted, and the second write could fail again. Hooks now write only to the log, so closing stdout or stderr cannot cause that reporting failure. The incident logs alone do not establish why the caller closed its pipe.
