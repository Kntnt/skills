# Automatic run capture

Use this reference for `capture`. It measures ordinary Harness work; it never judges it. A finished session produces a Usage Record — what it cost and how long it took on the exact Seat it ran on — appended to its own store beside the evidence ledger. It is not a `RunObservation`, does not reuse `run-observations.md`'s envelope, and is never imported by `record`.

## Consent and lifecycle

Capture is an explicit opt-in mode of an Enabled Skill. Enabling the Skill installs nothing and captures nothing, because capture installs persistent Harness integration and handles local metadata, and neither should follow from a decision the user made about something else. The first opt-in states four things before anything is written: which local lifecycle integrations are installed, which metadata categories may be retained, how temporary data is cleaned up, and how capture is turned off.

Once opted in, capture follows the Skill's lifecycle in the layer it was enabled in. Every installed integration carries a stable ownership identity, so enable, repair, update, opt-out, disable, withdrawal, and uninstall converge on the same disk state however often they run. Removal is surgical: entries this feature installed go, and unrelated hooks, unrelated configuration, and Harness session history are left exactly as they were. Installation and removal are verified by reading the Harness's own file back, and a Harness that only partly applied is reported as that rather than as a complete one.

Making the Skill Disabled is sufficient to stop capture and remove what it owns. There is no second shutdown step, because the Manager asks the Skill to remove its integrations while the Skill's own files are still on disk — after they are deleted, nothing left on the machine knows what was installed or where. Accepted Usage Records survive every one of these transitions: turning a measurement off is not a reason to forget what it measured, and an explicit purge, if ever added, stays a separate act.

## Harnesses

Adapters exist for Claude Code, Codex, and OpenCode, whose supported lifecycle APIs can carry the contract: the first two through their owned hook tables, the third through a plugin file named for its owner. Session start, agent stop or idle, session end, and error are the moments observed. Each is a lifecycle signal and none is a verdict — a stop says a turn ended, never that its work succeeded, and there is no verdict for a Usage Record to carry either way.

Each adapter is verified against what its own Harness actually reads — event names, entry shape, and file location established from that Harness as installed, never assumed from a sibling's. Claude Code and Codex each keep an owned hook table in their own file, and confirmed live, Codex's own config file accepts the same PascalCase event names and the same nested matcher-group entry Claude Code's does; the flat, camelCase shape its unrelated app-server protocol reports back is not what the config file reads. A Harness outside the supported set, or one whose accepted shape cannot be established, reports an Unsatisfied integration capability and is never reported healthy.

Codex additionally reviews a hook that is new or has changed before it will run it, and this collection forges no trust decision and writes no trust record on the user's behalf — a gate is the Harness's own. A Codex integration that is correctly written is reported gated: present, and not yet active, naming what the user does to clear the review. OpenCode's plugin hands its event object on unmodified and redirects it onto the invoked command's own standard input, which is what carries the session identity nested inside it and what keeps the command from ever inheriting the session's own standard input, which a hook that reads it to end-of-file could otherwise block on.

A script cannot know which Harness invoked it and must not guess, so the Skill names the active Harness when installing, and the shared mechanics live in the Collection Library rather than in this Skill, where a second consumer finds them instead of reaching in here.

## The pipeline

A small per-session draft is created when substantive work begins, and updated only from allowed lifecycle, Seat, and usage signals. Two sessions at once are two drafts under two opaque identities, so neither can read or clear the other's.

Within one session, a Seat's own active window opens at the first lifecycle signal naming it and extends at every later one, so its Usage Record is timed on that Seat's own first and last turn rather than on the whole session's start and end. A session that ran on more than one Seat — the user switched model or deliberation mid-way — produces one Usage Record per Seat at the session's end, because each Seat is a distinct configuration the session actually ran on.

At `SessionEnd` or an error signal, every Seat window the draft holds becomes one Usage Record, appended to the store, and the draft is deleted. Idempotency is by session identity and Seat: a Usage Record whose key the store already holds is skipped rather than repeated, so a lifecycle signal redelivered after the store was already written adds nothing the second time. An error signal ends the session exactly as a normal end does — there is no outcome left for either to carry, so neither is a verdict of any kind.

The exact seat a session runs on is recorded once, at the opt-in, by the agent that knows it: no lifecycle payload carries it — a Harness reports what happened rather than what it is — and a script may not guess. A payload that does name a seat wins over it. A session with no Seat known at all — neither a payload nor the opt-in named one — still writes a Usage Record, its Seat fields explicit nulls, because nothing here waits for anybody to supply one.

## Data boundary

Temporary capture and the permanent Usage Record both carry only what one is built from: opaque session identity and usage key; the Harness and its inventory revision; the exact Seat — model, deliberation control, serving mode, access channel, and tool fingerprints; the usage categories the environment exposed — tokens, tool calls, retries, cost, quota, latency, and fallback; and the two instants a Seat ran between. Every measurement the environment did not expose stays an explicit `null`, because a zero is a reading and an absence is not.

Never full prompts, responses, reasoning, source files, diffs, terminal output, secrets, credentials, or complete Harness transcripts, and never an absolute path where an opaque identity is sufficient. A lifecycle payload is copied onto an allow-list rather than stripped afterwards, so nothing forbidden enters by sitting beside something wanted, and a raw session identifier — which is a path or a workspace name often enough — is hashed rather than kept.

A Usage Record carries no outcome, no Outcome Authority, no checker, no condition, no Cohort, and no configuration fingerprint. It is never quality: it enters no derived frontier, contributes to no success rate, clears no quality floor, and produces no evidence record, exactly as a Cohort-less ledger row already stays out of every comparison — applied here to a record that carries no outcome to compare in the first place.

## The hook path

Fail-open, always. A capture that cannot run must never block an agent response, a tool execution, or a session ending, so every failure inside the hook is swallowed and the hook exits clean.

Bounded and local, always. The synchronous path does local metadata I/O and nothing else: no network request, no model call, no test run, no repository-wide hashing, no transcript scan, and no long-lived background work.

## Boundary

This contract owns automatic capture of ordinary Harness work and the Usage Record it produces. It is not the routed-work observation representation `run-observations.md` owns, reuses none of that contract's envelope, validation, or import, and writes no ledger row of any kind. Deliberately routed work stays entirely `run-observations.md`'s, whose `observe` and `record` this reference never calls.
