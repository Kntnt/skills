# Automatic run capture

Use this reference for `capture`. It is the contract automatic local evidence collection runs under, and it reuses `run-observations.md` rather than restating it: what capture produces is the same normalized `RunObservation`, and what imports it is the same `record`.

## Consent and lifecycle

Capture is an explicit opt-in mode of an Enabled Skill. Enabling the Skill installs nothing and captures nothing, because capture installs persistent Harness integration and handles local metadata, and neither should follow from a decision the user made about something else. The first opt-in states four things before anything is written: which local lifecycle integrations are installed, which metadata categories may be retained, how temporary data is cleaned up, and how capture is turned off.

Once opted in, capture follows the Skill's lifecycle in the layer it was enabled in. Every installed integration carries a stable ownership identity, so enable, repair, update, opt-out, disable, withdrawal, and uninstall converge on the same disk state however often they run. Removal is surgical: entries this feature installed go, and unrelated hooks, unrelated configuration, and Harness session history are left exactly as they were. Installation and removal are verified by reading the Harness's own file back, and a Harness that only partly applied is reported as that rather than as a complete one.

Making the Skill Disabled is sufficient to stop capture and remove what it owns. There is no second shutdown step, because the Manager asks the Skill to remove its integrations while the Skill's own files are still on disk — after they are deleted, nothing left on the machine knows what was installed or where. Accepted evidence survives every one of these transitions: turning a measurement off is not a reason to forget what it measured, and an explicit purge, if ever added, stays a separate act.

## Harnesses

Adapters exist for Claude Code, Codex, and OpenCode, whose supported lifecycle APIs can carry the contract: the first two through their owned hook tables, the third through a plugin file named for its owner. Session start, agent stop or idle, session end, and error are the moments observed. Each is an observation and none is a verdict — a stop says a turn ended, never that its work succeeded.

Each adapter is verified against what its own Harness actually reads — event names, entry shape, and file location established from that Harness as installed, never assumed from a sibling's. Claude Code and Codex each keep an owned hook table in their own file, and confirmed live, Codex's own config file accepts the same PascalCase event names and the same nested matcher-group entry Claude Code's does; the flat, camelCase shape its unrelated app-server protocol reports back is not what the config file reads. A Harness outside the supported set, or one whose accepted shape cannot be established, reports an Unsatisfied integration capability and is never reported healthy.

Codex additionally reviews a hook that is new or has changed before it will run it, and this collection forges no trust decision and writes no trust record on the user's behalf — a gate is the Harness's own. A Codex integration that is correctly written is reported gated: present, and not yet active, naming what the user does to clear the review. OpenCode's plugin hands its event object on unmodified and redirects it onto the invoked command's own standard input, which is what carries the session identity nested inside it and what keeps the command from ever inheriting the session's own standard input, which a hook that reads it to end-of-file could otherwise block on.

A script cannot know which Harness invoked it and must not guess, so the Skill names the active Harness when installing, and the shared mechanics live in the Collection Library rather than in this Skill, where a second consumer finds them instead of reaching in here.

## The pipeline

A small per-session draft is created when substantive work begins, and updated only from allowed lifecycle, usage, checker, quota, and latency signals. Two sessions at once are two drafts under two opaque identities, so neither can read or clear the other's.

At an eligible completion boundary the draft becomes exactly one attempt in the routed-work envelope, is normalized and validated by the same code path `observe` uses, and is imported by the same code path `record` uses. Only the derived frontiers whose eligible run set actually changed are rebuilt, and the draft is deleted immediately after a successful import. An empty or irrelevant draft is discarded rather than kept.

The exact seat a session runs on is recorded once, at the opt-in, by the agent that knows it: no lifecycle payload carries a model, a Harness reports what happened rather than what it is, and a script may not guess. A payload that does name a seat wins over it, and captured work with neither waits for a human rather than being filed under a configuration it never ran on.

Ordinary work is not routed, so its attempt records the inheritance that actually happened: the exact main seat the session ran on, fingerprinted from that seat, under the `interactive_session` stratum. Its provenance names the captured environment rather than a frozen routing snapshot, because there was no routing to freeze, and `route_status` stays `inherit` so that nothing reads as a choice somebody made.

## What establishes an outcome

An objective checker, a frozen rubric, a declared failure signal, or explicit user confirmation. Nothing else. A self-report and a checker that is not independent are refused rather than downgraded, because unchecked work that becomes weak evidence is worse than work that becomes none.

Work that reaches a boundary with no established outcome enters bounded pending review and waits for a human, who may save it, mark it failed, or ignore it; the first two carry `user_confirmation` as their authority and the third discards the capture without recording anything. A Harness error is an infrastructure outcome with its own condition, kept apart from model quality exactly as the routed contract keeps it, so a broken environment can never make a configuration look worse than it is.

A session that ends abruptly writes no completion signal at all. Its draft is reconciled at the next suitable start or status pass: it becomes pending work awaiting judgement, never a success and never a failure.

## Data boundary

Temporary capture and the permanent record both carry only what an observation is built from: opaque session and task identity; timestamps and Harness identity; the exact resolved model, deliberation control, serving mode, access channel, and tool and policy fingerprints; checker identity and result; available token categories, tool counts, retries, fallbacks, provider bill, quota deltas, wall and first-useful-output latency; provenance; and sanitized artifact hashes. Every measurement the environment did not expose stays an explicit `null`, because a zero is a reading and an absence is not.

Never full prompts, responses, reasoning, source files, diffs, terminal output, secrets, credentials, or complete Harness transcripts, and never an absolute path where an opaque identity is sufficient. A lifecycle payload is copied onto an allow-list rather than stripped afterwards, so nothing forbidden enters by sitting beside something wanted, and a raw session identifier — which is a path or a workspace name often enough — is hashed rather than kept.

The permanent record is the minimal normalized `RunObservation` and the ledger records it implies. Derived quality, confidence, cost per success, quota burn, latency, and frontier membership stay disposable and reproducible, and quality, cash, quota, and latency are never collapsed into one irreversible rolling score.

## Retention and resource bounds

An imported capture is removed immediately. Pending and failed captures are kept at most 30 days, 100 drafts, and 1 MiB in total; whichever bound is exceeded, the oldest are removed first. Cleanup is deterministic and needs no permanently running daemon: it happens at a session start or a status pass. Accepted evidence is never subject to these bounds.

Status answers whether capture is enabled, adapter health per Harness, the pending-review count, the oldest pending age, and storage in use, without a network request or an evaluation.

## The hook path

Fail-open, always. A capture that cannot run must never block an agent response, a tool execution, or a session ending, so every failure inside the hook is swallowed and the hook exits clean.

Bounded and local, always. The synchronous path does local metadata I/O and nothing else: no network request, no model call, no test run, no repository-wide hashing, no transcript scan, and no long-lived background work.

Notifications are user-facing and debounced. They never enter the context of the model being measured, because a measurement reminder in that context changes the very configuration under measurement, and a notification that fails cannot affect whether capture was correct.

## Boundary

This contract owns automatic capture of ordinary Harness work. Deliberately routed work belongs to `run-observations.md`, whose envelope, validation, refusals, idempotency, and conflict rules this reuses unchanged; `record` remains the only ledger mutation either of them performs, and the two share one normalized representation rather than each having its own.
